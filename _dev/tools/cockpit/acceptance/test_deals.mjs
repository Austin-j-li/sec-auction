/* Add-deal acceptance: seed search, pasted link with document choice, pending page, Add and extract through the fake runner, then hiding and unhiding deals. No network or model is used. */
/* Run from repo root: node _dev/tools/cockpit/acceptance/test_deals.mjs (COCKPIT_TEST_DIST=<dist> to test a staged build) */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { mkdir, readFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import playwright from '/home/uctpiaj/work/vm-browser/node_modules/playwright/index.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '../../../..');
const EVIDENCE = resolve(process.env.COCKPIT_DEALS_EVIDENCE || resolve(tmpdir(), 'cockpit-deals-acceptance'));
const STAGED_DIST = process.env.COCKPIT_TEST_DIST ? resolve(process.env.COCKPIT_TEST_DIST) : null;
const ACCESS = {}; // each user's Cloudflare Access token, signed by the fixture's own key (serve_fixture.py --two-users)
const PASTED_INDEX = 'https://www.sec.gov/Archives/edgar/data/88/0000000088-22-000002-index.htm';
const fixture = spawn('python3', [resolve(HERE, 'serve_fixture.py'), '--two-users', '--runs', '--deals'], { cwd: REPO, stdio: ['ignore', 'pipe', 'pipe'] });
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
  if (STAGED_DIST) await context.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (url.pathname.startsWith('/api/')) return route.continue();
    const asset = url.pathname.startsWith('/assets/') ? url.pathname.slice(1) : 'index.html';
    const type = asset.endsWith('.js') ? 'text/javascript' : asset.endsWith('.css') ? 'text/css' : asset.endsWith('.woff2') ? 'font/woff2' : asset.endsWith('.svg') ? 'image/svg+xml' : 'text/html';
    try { return route.fulfill({ body: await readFile(resolve(STAGED_DIST, asset)), contentType: type }); }
    catch { return route.continue(); }
  });
  const page = await context.newPage();
  page.on('pageerror', error => browserErrors.push(`${user}: ${error.message}`));
  // The refused link below answers 400 and the refused run on a hidden deal 409, on purpose; any other console error counts.
  page.on('console', message => { if (message.type() === 'error' && !/status of (400|409)/.test(message.text())) browserErrors.push(`${user}: ${message.text()}`); });
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
    await api(austin, '/api/account/claude', { action: 'token', token: 'sk-ant-oat01-' + 'A'.repeat(40) });

    // Seed: search, choose, check the preselected document and names, add.
    await austin.goto(base + '/');
    await austin.getByRole('button', { name: 'Add deal' }).click();
    const dialog = austin.getByRole('dialog', { name: 'Add a deal' });
    await dialog.getByLabel('Deal name').fill('delta');
    await dialog.getByRole('button', { name: 'Choose' }).click();
    const proxy = dialog.getByRole('radio', { name: /delta-proxy\.htm/ });
    await proxy.waitFor({ timeout: 20000 });
    record('seed lookup preselects the proxy', await proxy.isChecked());
    record('suggested name and short name', (await dialog.getByLabel('Deal name').inputValue()) === 'Delta Systems' && (await dialog.getByLabel('Short name').inputValue()) === 'delta-systems');
    await austin.screenshot({ path: resolve(EVIDENCE, 'seed-lookup.png') });
    await dialog.getByRole('button', { name: 'Add', exact: true }).click();
    await austin.getByRole('heading', { name: 'No extraction yet' }).waitFor();
    record('added deal opens as pending', austin.url().endsWith('/deal/delta-systems') && (await api(austin, '/api/deal/delta-systems')).body.pending === true);
    await austin.locator('.filing-block', { hasText: 'Delta met three bidders.' }).waitFor();
    record('pending deal shows its filing', true);
    await austin.screenshot({ path: resolve(EVIDENCE, 'pending-deal.png') });

    // Already added now says Open; a review row without a link asks for a pasted link.
    await austin.goto(base + '/');
    const overviewRow = austin.locator('.deal-table tr', { hasText: 'Delta Systems' });
    record('overview lists the pending deal', (await overviewRow.textContent()).includes('No extraction yet'));
    await austin.getByRole('button', { name: 'Add deal' }).click();
    await dialog.getByLabel('Deal name').fill('delta');
    await dialog.getByRole('button', { name: 'Open' }).waitFor();
    await dialog.getByLabel('Deal name').fill('kilo');
    await dialog.getByRole('button', { name: 'Paste link' }).click();
    await dialog.getByText('The seed has no usable link for').waitFor();
    record('review row without a link asks for one', true);

    // A link that is not EDGAR's is refused.
    await dialog.getByLabel('EDGAR link').fill('https://example.com/filing-index.htm');
    await dialog.getByRole('button', { name: 'Look up' }).click();
    await dialog.getByText('not an EDGAR filing link').waitFor();
    record('non-EDGAR link refused', true);
    await dialog.getByRole('button', { name: 'Close' }).click();

    // Pasted link: choose another document (Background warning), go back to the offer, Add and extract.
    await austin.getByRole('button', { name: 'Add deal' }).click();
    await dialog.getByRole('tab', { name: 'Paste a link' }).click();
    await dialog.getByLabel('EDGAR link').fill(PASTED_INDEX);
    await dialog.getByRole('button', { name: 'Look up' }).click();
    const offer = dialog.getByRole('radio', { name: /echo-offer\.htm/ });
    await offer.waitFor({ timeout: 20000 });
    record('tender offer exhibit preselected', await offer.isChecked());
    await dialog.getByRole('radio', { name: /echo-cover\.htm/ }).check();
    await dialog.getByText('has no “Background of the Merger” or similar heading').waitFor();
    record('background warning on the cover form', true);
    await offer.check();
    record('warning clears on the offer', (await dialog.getByText('has no “Background of the Merger”').count()) === 0);
    record('names come from the subject company', (await dialog.getByLabel('Short name').inputValue()) === 'echo-labs');
    await austin.screenshot({ path: resolve(EVIDENCE, 'pasted-lookup.png') });
    await dialog.getByRole('button', { name: 'Add and extract' }).click();
    const extract = austin.getByRole('dialog', { name: 'Start an extraction' });
    await extract.getByRole('button', { name: 'Start extraction' }).click();
    await austin.getByLabel('Version', { exact: true }).waitFor({ timeout: 60000 });
    const deal = (await api(austin, '/api/deal/echo-labs')).body;
    const jobs = (await api(austin, '/api/deal/echo-labs/jobs')).body.jobs;
    record('first run becomes the working-copy base', !deal.pending && jobs[0].state === 'completed' && deal.workspace.base_version === jobs[0].version_id, JSON.stringify({ base: deal.workspace?.base_version, job: jobs[0] }));
    record('the page reloads into the workspace', await austin.getByRole('tab', { name: /Ledger/ }).isVisible());
    await austin.screenshot({ path: resolve(EVIDENCE, 'after-first-run.png') });

    // Alex sees who added what.
    const feed = (await api(alex, '/api/activity?kind=deal_added')).body.items;
    record('alex sees both additions by austin', feed.length === 2 && feed.every(item => item.actor === 'austin'), JSON.stringify(feed));

    // Hiding (phase 5): Austin hides Echo Labs from its overflow menu; it leaves the list for both, still opens by URL with a banner, and can be unhidden.
    await austin.goto(base + '/deal/echo-labs');
    await austin.getByRole('button', { name: 'More deal actions' }).click();
    await austin.getByRole('menuitem', { name: 'Hide deal…' }).click();
    const hide = austin.getByRole('dialog', { name: 'Hide deal' });
    record('hide asks first', (await hide.textContent()).includes('for both of you?It stays in the store and can be shown again.'), await hide.textContent());
    await hide.getByRole('button', { name: 'Hide deal' }).click();
    const banner = austin.locator('.hidden-banner');
    await banner.waitFor();
    record('hidden deal shows the banner and no Extract', /^Hidden by Austin on \d+ \w{3}·Unhide$/.test(await banner.textContent()) && (await austin.getByRole('button', { name: 'Extract' }).count()) === 0, await banner.textContent());
    await austin.screenshot({ path: resolve(EVIDENCE, 'hidden-deal.png') });
    const refusedRun = await api(austin, '/api/deal/echo-labs/jobs', { action: 'extract' });
    record('extract on a hidden deal is refused', refusedRun.status === 409 && refusedRun.body.error.includes('unhide the deal first'), JSON.stringify(refusedRun));
    await alex.goto(base + '/');
    await alex.locator('.deal-table').waitFor();
    record('hidden deal leaves alex\'s list', (await alex.locator('.deal-table tr', { hasText: 'echo-labs' }).count()) === 0);
    await alex.getByRole('checkbox', { name: 'Show hidden (1)' }).check();
    const hiddenRow = alex.locator('.deal-table tr.hidden-deal', { hasText: 'echo-labs' });
    record('show hidden lists it dimmed and marked', (await hiddenRow.count()) === 1 && (await hiddenRow.locator('.hidden-mark').textContent()) === 'Hidden');
    await alex.screenshot({ path: resolve(EVIDENCE, 'hidden-list.png') });
    await hiddenRow.locator('.deal-link').click();
    await alex.locator('.hidden-banner', { hasText: 'Hidden by Austin on' }).waitFor();
    record('hidden deal opens by URL for alex', alex.url().endsWith('/deal/echo-labs'));
    await alex.locator('.hidden-banner').getByRole('button', { name: 'Unhide' }).click();
    await alex.locator('.hidden-banner').waitFor({ state: 'detached' });
    record('unhide from the banner', (await api(alex, '/api/deals')).body.find(item => item.slug === 'echo-labs').hidden === false);
    // Unhide from the list: Delta Systems hidden over the API, shown again from its row.
    record('pending deal hides', (await api(austin, '/api/deals/delta-systems/visibility', { action: 'hide' })).status === 200);
    await alex.goto(base + '/');
    await alex.getByRole('checkbox', { name: 'Show hidden (1)' }).check();
    await alex.locator('.deal-table tr.hidden-deal', { hasText: 'delta-systems' }).getByRole('button', { name: 'Unhide' }).click();
    await alex.getByRole('checkbox', { name: /Show hidden/ }).waitFor({ state: 'detached' });
    record('unhide from the list', (await alex.locator('.deal-table tr.hidden-deal').count()) === 0 && (await alex.locator('.deal-table tr', { hasText: 'delta-systems' }).count()) === 1);
    const kinds = (await api(austin, '/api/activity?limit=10')).body.items.map(item => `${item.actor}:${item.kind}:${item.slug}`);
    record('hiding is in the activity feed', ['alex:unhide_deal:delta-systems', 'austin:hide_deal:delta-systems', 'alex:unhide_deal:echo-labs', 'austin:hide_deal:echo-labs'].every((entry, i) => kinds[i] === entry), JSON.stringify(kinds));
    record('no browser errors', browserErrors.length === 0, browserErrors.join('\n'));
  } finally {
    await browser.close();
    fixture.kill('SIGTERM');
  }
  console.log(JSON.stringify({ passed: results.length, results, evidence: EVIDENCE }, null, 2));
}

run().catch(error => { fixture.kill('SIGTERM'); console.error(error); console.error(serverStderr.slice(-3000)); process.exit(1); });
