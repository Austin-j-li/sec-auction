/* Two-user trace acceptance: Alex comments and edits, Austin sees it, marks it read and unread. */
/* Run from repo root: node _dev/tools/cockpit/acceptance/test_trace.mjs */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { mkdir } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import playwright from '/home/uctpiaj/work/vm-browser/node_modules/playwright/index.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '../../../..');
const EVIDENCE = resolve(process.env.COCKPIT_TRACE_EVIDENCE || '/tmp/cockpit-trace-acceptance');
const EMAILS = { austin: 'junyu.li.24@ucl.ac.uk', alex: 'a.gorbenko@ucl.ac.uk' };
const fixture = spawn('python3', [resolve(HERE, 'serve_fixture.py'), '--two-users'], { cwd: REPO, stdio: ['ignore', 'pipe', 'pipe'] });
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
  for await (const line of createInterface({ input: fixture.stdout })) if (line.startsWith('{')) return JSON.parse(line).url;
  throw new Error(`fixture exited: ${serverStderr}`);
}

async function userPage(browser, base, user) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 }, extraHTTPHeaders: { 'Cf-Access-Authenticated-User-Email': EMAILS[user] } });
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
    const alex = await userPage(browser, base, 'alex');
    const session = await api(alex, '/api/session');
    record('alex identity', session.body.user === 'alex' && session.body.can_edit);
    const deal = (await api(alex, '/api/deal/synthetic')).body;
    const first = deal.ledger.rows[0];
    const saved = await api(alex, '/api/deal/synthetic/edit', { revision: deal.workspace.revision, base_sha256: deal.workspace.base_sha256, reason: 'Alex names the bidder', operations: [{ type: 'update', sheet: 'Deal ledger', uid: first.uid, values: { Who: 'Party A (Alex)' } }] });
    record('alex saves an edit', saved.status === 200);
    await alex.goto(base + '/deal/synthetic#row-1');
    await alex.locator('.comments textarea').first().fill('Alex asks: is this dated right?');
    await alex.getByRole('button', { name: 'Comment', exact: true }).click();
    await alex.locator('.comment-body', { hasText: 'Alex asks' }).waitFor();
    record('alex comments through the UI', true);
    await alex.screenshot({ path: resolve(EVIDENCE, 'alex-comment.png') });

    const austin = await userPage(browser, base, 'austin');
    const line = austin.locator('.unseen-line').first();
    await line.waitFor();
    const text = await line.innerText();
    record('overview digest', /Alex/.test(text) && /1 edit/.test(text) && /1 comment/.test(text), text);
    await austin.screenshot({ path: resolve(EVIDENCE, 'austin-overview.png') });
    await austin.goto(base + '/deal/synthetic#row-1');
    await austin.locator('.whats-new').waitFor();
    record('what\'s new shown', (await austin.locator('.whats-new-meta').first().innerText()).includes('Alex'));
    record('row mark for Alex', await austin.locator('.event-item .initials-mark', { hasText: 'AG' }).first().isVisible());
    record('austin sees alex comment', await austin.locator('.comment-body', { hasText: 'Alex asks' }).isVisible());
    await austin.screenshot({ path: resolve(EVIDENCE, 'austin-deal.png') });
    await austin.locator('.comments').first().getByRole('button', { name: 'Reply' }).click();
    await austin.locator('.replies textarea').fill('Austin: yes, page 27.');
    await austin.locator('.replies').getByRole('button', { name: 'Reply' }).click();
    await austin.locator('.comment-body', { hasText: 'page 27' }).waitFor();
    record('austin replies', true);
    await austin.getByRole('button', { name: 'Mark as read' }).click();
    await austin.getByRole('button', { name: 'Mark unread' }).waitFor();
    const unseenAfterRead = (await api(austin, '/api/deals')).body.find(d => d.slug === 'synthetic').unseen.by;
    record('mark as read clears', Object.keys(unseenAfterRead).length === 0, JSON.stringify(unseenAfterRead));
    await austin.getByRole('button', { name: 'Mark unread' }).click();
    await austin.getByRole('button', { name: 'Mark as read' }).waitFor();
    const unseenAfterUnread = (await api(austin, '/api/deals')).body.find(d => d.slug === 'synthetic').unseen.by;
    record('mark unread restores', unseenAfterUnread.alex?.edits === 1, JSON.stringify(unseenAfterUnread));

    await alex.goto(base + '/');
    const alexLine = alex.locator('.unseen-line').first();
    await alexLine.waitFor();
    record('alex sees austin reply in digest', (await alexLine.innerText()).includes('Austin'));
    await alex.goto(base + '/activity');
    await alex.locator('text=Austin: yes, page 27.').first().waitFor();
    record('activity page lists the reply', true);
    await alex.screenshot({ path: resolve(EVIDENCE, 'alex-activity.png') });

    const anonymous = await browser.newContext();
    const reader = await anonymous.newPage();
    await reader.goto(base + '/deal/synthetic#row-1');
    await reader.locator('.comment-body', { hasText: 'Alex asks' }).waitFor();
    record('unknown reader: read-only comments, no what\'s new', (await reader.locator('.comments textarea').count()) === 0 && (await reader.locator('.whats-new').count()) === 0);
    record('no browser errors', browserErrors.length === 0, browserErrors.join('\n'));
  } finally {
    await browser.close();
    fixture.kill('SIGTERM');
  }
  console.log(JSON.stringify({ passed: results.length, results, evidence: EVIDENCE }, null, 2));
}

run().catch(error => { fixture.kill('SIGTERM'); console.error(error); process.exit(1); });
