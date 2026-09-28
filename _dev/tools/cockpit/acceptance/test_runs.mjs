/* Runs acceptance: connect through the sign-in flow, extract with a fake runner, open, hide, rebase and compare. No model is called. */
/* Run from repo root: node _dev/tools/cockpit/acceptance/test_runs.mjs */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { mkdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import playwright from '/home/uctpiaj/work/vm-browser/node_modules/playwright/index.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '../../../..');
const EVIDENCE = resolve(process.env.COCKPIT_RUNS_EVIDENCE || resolve(tmpdir(), 'cockpit-runs-acceptance'));
const ACCESS = {}; // each user's Cloudflare Access token, signed by the fixture's own key (serve_fixture.py --two-users)
const fixture = spawn('python3', [resolve(HERE, 'serve_fixture.py'), '--two-users', '--runs'], { cwd: REPO, stdio: ['ignore', 'pipe', 'pipe'] });
let serverStderr = '';
fixture.stderr.setEncoding('utf8');
fixture.stderr.on('data', data => { serverStderr += data; });
const results = [];
const browserErrors = [];

function record(name, passed, detail = '') {
  results.push({ name, passed });
  assert.ok(passed, `${name} ${detail}`);
}

async function fixtureUrl() {
  for await (const line of createInterface({ input: fixture.stdout })) if (line.startsWith('{')) { const info = JSON.parse(line); Object.assign(ACCESS, info.access); return info.url; }
  throw new Error(`fixture exited: ${serverStderr}`);
}

async function userPage(browser, base, user) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 }, extraHTTPHeaders: { 'Cf-Access-Jwt-Assertion': ACCESS[user] } });
  const page = await context.newPage();
  page.on('pageerror', error => browserErrors.push(`${user}: ${error.message}`));
  page.on('console', message => { if (message.type() === 'error') browserErrors.push(`${user}: ${message.text()}`); });
  await page.goto(base + '/');
  return page;
}

async function api(page, path, body) {
  return page.evaluate(async ({ path, body }) => {
    const session = await (await fetch('/api/session')).json();
    const response = await fetch(path, body === undefined ? {} : { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Cockpit-CSRF': session.csrf_token }, body: JSON.stringify(body) });
    return { status: response.status, body: await response.json() };
  }, { path, body });
}

async function run() {
  await mkdir(EVIDENCE, { recursive: true });
  const base = await fixtureUrl();
  const browser = await playwright.chromium.launch({ headless: true, executablePath: '/opt/google/chrome/chrome', args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  try {
    const austin = await userPage(browser, base, 'austin');
    const alex = await userPage(browser, base, 'alex');

    // Connect through the sign-in link and code, as Austin would in the browser.
    await austin.goto(base + '/settings');
    await austin.getByRole('button', { name: 'Connect Claude account' }).click();
    const link = austin.locator('.connect-link');
    await link.waitFor({ timeout: 20000 });
    record('sign-in link shown', (await link.getAttribute('href')).startsWith('https://claude.com/cai/oauth/authorize'));
    await austin.getByLabel('Code').fill('good-code');
    await austin.getByRole('button', { name: 'Submit' }).click();
    await austin.getByRole('button', { name: 'Disconnect' }).waitFor({ timeout: 20000 });
    const account = await api(austin, '/api/account');
    record('account connected, token not returned', account.body.claude.connected && !JSON.stringify(account.body).includes('sk-ant-oat'), JSON.stringify(account.body));
    record('alex is not connected by austin', !(await api(alex, '/api/account')).body.claude.connected);
    await austin.screenshot({ path: resolve(EVIDENCE, 'austin-settings.png') });

    // Alex, not connected, is sent to Settings.
    await alex.goto(base + '/deal/synthetic');
    await alex.getByRole('button', { name: 'Extract' }).click();
    await alex.getByRole('dialog', { name: 'Start an extraction' }).getByRole('link', { name: 'Open settings' }).waitFor();
    record('unconnected user is sent to settings', true);
    await alex.getByRole('dialog', { name: 'Start an extraction' }).getByRole('button', { name: 'Close' }).first().click();

    // Austin starts a run; the fake runner finishes and the worker imports it.
    await austin.goto(base + '/deal/synthetic');
    await austin.getByRole('button', { name: 'Extract' }).click();
    const dialog = austin.getByRole('dialog', { name: 'Start an extraction' });
    await dialog.getByRole('button', { name: 'Start extraction' }).click();
    await austin.getByRole('tab', { name: 'Runs' }).waitFor();
    const open = austin.getByRole('button', { name: 'Open version' });
    await open.waitFor({ timeout: 60000 });
    const jobs = (await api(austin, '/api/deal/synthetic/jobs')).body.jobs;
    const ident = jobs[0].version_id;
    record('run completed and imported', jobs[0].state === 'completed' && Boolean(ident), JSON.stringify(jobs[0]));
    await austin.screenshot({ path: resolve(EVIDENCE, 'austin-runs.png') });

    // Open, hide and unhide the new original.
    await open.click();
    await austin.getByRole('button', { name: 'Hide' }).waitFor();
    record('open version switches the dropdown', (await austin.getByLabel('Version', { exact: true }).inputValue()) === ident);
    await austin.getByRole('button', { name: 'Hide' }).click();
    await austin.getByRole('button', { name: 'Unhide' }).waitFor();
    record('hide recorded', (await api(austin, '/api/deal/synthetic')).body.versions.find(v => v.id === ident).hidden === true);
    await austin.getByRole('button', { name: 'Unhide' }).click();
    await austin.getByRole('button', { name: 'Hide' }).waitFor();

    // Rebase the working copy onto the new run.
    await austin.getByRole('button', { name: 'Use as working-copy base…' }).click();
    const rebase = austin.getByRole('dialog', { name: 'Use as working-copy base' });
    await rebase.getByLabel('Reason').fill('Take the new Opus run');
    await rebase.getByRole('button', { name: 'Use as base' }).click();
    await rebase.waitFor({ state: 'detached' });
    const deal = (await api(austin, '/api/deal/synthetic')).body;
    record('working copy rebased', deal.workspace.base_version === ident && deal.ledger.rows[1].cells.Who === 'Party A (new run)', JSON.stringify({ base: deal.workspace.base_version, who: deal.ledger.rows[1].cells.Who }));

    // Compare the catalog original with the new run.
    const original = deal.versions.find(v => !v.started_at && v.id !== 'working');
    await austin.goto(base + '/deal/synthetic');
    await austin.getByRole('tab', { name: 'Changes' }).click();
    await austin.getByRole('group', { name: 'Compare' }).getByLabel('From').selectOption(original.id);
    await austin.getByRole('group', { name: 'Compare' }).getByLabel('To').selectOption(ident);
    await austin.locator('#workspace-panel', { hasText: 'Party A (new run)' }).waitFor();
    record('compare shows the renamed bidder', true);
    await austin.screenshot({ path: resolve(EVIDENCE, 'austin-compare.png') });

    // Alex sees the run in the feed, linked to its version.
    const feed = (await api(alex, '/api/deal/synthetic/activity')).body.items;
    const extraction = feed.find(item => item.kind === 'extraction');
    record('alex sees the extraction with its version', extraction?.actor === 'austin' && extraction.version_id === ident, JSON.stringify(feed.slice(0, 3)));
    record('rebase activity carries its revision', feed.find(item => item.kind === 'rebase')?.revision === 1);
    record('no browser errors', browserErrors.length === 0, browserErrors.join('\n'));
  } finally {
    await browser.close();
    fixture.kill('SIGTERM');
  }
  console.log(JSON.stringify({ passed: results.length, results, evidence: EVIDENCE }, null, 2));
}

run().catch(error => { fixture.kill('SIGTERM'); console.error(error); console.error(serverStderr.slice(-3000)); process.exit(1); });
