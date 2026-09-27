/* Built UI acceptance against serve_fixture.py, using a private headless Chrome. */
/* Run from repo root: node _dev/tools/cockpit/acceptance/test_browser.mjs */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { createInterface } from 'node:readline';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import playwright from '/home/uctpiaj/work/vm-browser/node_modules/playwright/index.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '../../../..');
const EVIDENCE = resolve(process.env.COCKPIT_BROWSER_EVIDENCE || '/tmp/cockpit-browser-acceptance');
const STAGED_DIST = process.env.COCKPIT_TEST_DIST ? resolve(process.env.COCKPIT_TEST_DIST) : null;
const results = [];
const screenshots = [];
const browsers = [];
const fixture = spawn('python3', [resolve(HERE, 'serve_fixture.py'), '--catalog-pending'], { cwd: REPO, stdio: ['ignore', 'pipe', 'pipe'] });
let serverStderr = '';
fixture.stderr.setEncoding('utf8');
fixture.stderr.on('data', data => { serverStderr += data; });

async function fixtureUrl() {
  const lines = createInterface({ input: fixture.stdout });
  for await (const line of lines) {
    if (line.startsWith('{')) return JSON.parse(line).url;
  }
  throw new Error(`Synthetic server exited before announcing URL: ${serverStderr}`);
}

async function useStagedAssets(context) {
  if (!STAGED_DIST) return;
  await context.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (url.pathname.startsWith('/api/')) return route.continue();
    const asset = url.pathname.startsWith('/assets/') ? url.pathname.slice(1) : 'index.html';
    const type = asset.endsWith('.js') ? 'text/javascript' : asset.endsWith('.css') ? 'text/css' : asset.endsWith('.woff2') ? 'font/woff2' : 'text/html';
    try { return route.fulfill({ body: await readFile(resolve(STAGED_DIST, asset)), contentType: type }); }
    catch { return route.continue(); }
  });
}

async function waitForRevision(page, revision) {
  await page.waitForFunction(expected => document.querySelector('.deal-subline')?.textContent.includes(`Revision ${expected}`), revision);
}

function record(name, passed, detail = '') {
  results.push({ name, passed, detail });
  if (!passed) throw new Error(`${name}: ${detail}`);
}

async function screenshot(page, filename) {
  const path = resolve(EVIDENCE, filename);
  await page.screenshot({ path, fullPage: false });
  screenshots.push(filename);
}

async function chooseTab(page, name) {
  await page.getByRole('tab', { name: new RegExp(`^${name}(?:\\b|$)`) }).click();
  await page.waitForTimeout(80);
}

async function assertNoOverflow(page, label) {
  const state = await page.evaluate(() => ({ width: innerWidth, scrollWidth: document.documentElement.scrollWidth }));
  record(`${label} horizontal fit`, state.scrollWidth <= state.width + 2, JSON.stringify(state));
}

async function assertControlWithin(page, control, pane, label) {
  const [item, owner] = await Promise.all([control.boundingBox(), pane.boundingBox()]);
  record(label, Boolean(item && owner && item.x >= owner.x - 2 && item.x + item.width <= owner.x + owner.width + 2), JSON.stringify({ item, owner }));
}

async function api(page, path) {
  return page.evaluate(async path => { const response = await fetch(path); return { status: response.status, body: await response.json() }; }, path);
}

async function saveUi(page, reason) {
  await page.getByRole('textbox', { name: 'Reason for this revision' }).fill(reason);
  await page.getByRole('button', { name: 'Save changes' }).click();
  try { await page.getByText('Revision saved', { exact: true }).waitFor({ timeout: 15000 }); }
  catch (error) {
    await screenshot(page, 'debug-save-failure.png');
    const alerts = await page.getByRole('alert').allTextContents();
    throw new Error(`${reason}: save did not complete; alerts=${JSON.stringify(alerts)}; ${error.message}`);
  }
}

async function run() {
  await mkdir(EVIDENCE, { recursive: true });
  const base = await fixtureUrl();
  const browser = await playwright.chromium.launch({ headless: true, executablePath: '/opt/google/chrome/chrome', args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  browsers.push(browser);
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, acceptDownloads: true, reducedMotion: 'reduce' });
  await useStagedAssets(context);
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(base + '/', { waitUntil: 'networkidle' });
  await page.getByRole('heading', { name: 'Deal ledgers' }).waitFor();
  record('overview synthetic deal', await page.getByRole('row').filter({ hasText: 'Synthetic Acme' }).count() === 1);
  record('overview pending catalog deal', (await page.getByRole('row').filter({ hasText: 'Pending Acme' }).locator('td').nth(2).innerText()).trim() === 'No extraction yet');
  await screenshot(page, 'desktop-overview.png');
  await page.getByRole('row').filter({ hasText: 'Pending Acme' }).click();
  await page.getByRole('heading', { name: 'Pending Acme' }).waitFor();
  record('pending catalog shows repository provenance', await page.getByText('Repository filing · pending.htm').count() === 1 && await page.getByText('Added by Someone').count() === 0);
  await screenshot(page, 'desktop-pending-catalog.png');
  await page.getByRole('button', { name: 'All deals' }).click();
  await page.getByRole('row').filter({ hasText: 'Synthetic Acme' }).click();
  await page.getByRole('heading', { name: 'Synthetic Acme' }).waitFor();
  await page.locator('.filing-block').first().waitFor();
  await assertNoOverflow(page, 'desktop 1440');
  await screenshot(page, 'desktop-ledger.png');

  await page.getByRole('textbox', { name: 'Search filing' }).fill('supplemental');
  await page.getByText('1 / 1', { exact: true }).waitFor();
  record('source search highlight', await page.locator('mark.search-mark').count() > 0);
  const sourcePane = page.locator('.filing-scroll');
  await page.getByRole('textbox', { name: 'Page', exact: true }).fill('2');
  await page.getByRole('button', { name: 'Go', exact: true }).click();
  const scroll = await sourcePane.evaluate(element => element.scrollTop);
  record('source page jump', scroll > 0, `scrollTop=${scroll}`);
  await screenshot(page, 'desktop-source-search.png');
  await page.getByRole('textbox', { name: 'Search filing' }).clear();
  await page.locator('mark.quote-mark').first().click();
  record('source quote to ledger navigation', new URL(page.url()).hash === '#row-1', page.url());
  await page.getByRole('button', { name: 'Show in filing' }).click();
  record('ledger row to source quote', await page.locator('mark.quote-mark.selected').first().isVisible());
  await page.locator('.event-item').filter({ hasText: 'Offer' }).click();
  await page.getByRole('button', { name: 'Open question R1' }).click();
  record('ledger R flag opens review item', await page.getByRole('tab', { name: /^Questions/ }).getAttribute('aria-selected') === 'true' && (await page.locator('.sheet-editor h3').innerText()) === 'R1');
  await chooseTab(page, 'Ledger');
  await page.locator('.event-item').filter({ hasText: 'Offer' }).click();
  await page.getByRole('button', { name: 'Open question Q1' }).click();
  record('ledger flag opens question', await page.getByRole('tab', { name: /^Questions/ }).getAttribute('aria-selected') === 'true' && (await page.locator('.sheet-editor h3').innerText()) === 'Q1');
  await page.locator('.reference-links').getByRole('button', { name: /#2 Offer/ }).click();
  record('question returns to referenced event', await page.getByRole('tab', { name: /^Ledger/ }).getAttribute('aria-selected') === 'true' && new URL(page.url()).hash === '#row-2');
  await page.locator('.event-item').filter({ hasText: 'Invitation' }).click();

  for (const tab of ['Rounds', 'Questions', 'Deal facts', 'Review', 'Changes', 'History']) {
    await chooseTab(page, tab);
    record(`${tab} tab renders`, await page.getByRole('tabpanel').isVisible());
  }
  await screenshot(page, 'desktop-history-empty.png');
  await chooseTab(page, 'Ledger');
  await page.locator('.record-editor').getByRole('textbox', { name: 'Note', exact: true }).fill('Synthetic edited note');
  let unsavedPrompt = false;
  page.once('dialog', dialog => { unsavedPrompt = true; dialog.dismiss(); });
  await page.getByRole('button', { name: 'All deals' }).click();
  record('unsaved navigation prompt retained deal', unsavedPrompt && new URL(page.url()).pathname === '/deal/synthetic');

  await chooseTab(page, 'Rounds');
  await page.getByRole('textbox', { name: 'How opened' }).fill('Synthetic opening edited');
  await chooseTab(page, 'Questions');
  await page.getByRole('textbox', { name: 'Recommended answer' }).fill('Still uncertain in fixture');
  await chooseTab(page, 'Deal facts');
  await page.getByRole('textbox', { name: 'Value' }).fill('Synthetic Acme UI');
  await chooseTab(page, 'Review');
  await page.locator('.mechanical-panel summary').click();
  record('mechanical global report visible', await page.locator('.mechanical-content').isVisible() && (await page.locator('.mechanical-content').innerText()).includes('presentation.wrap_text'));
  await page.locator('.mechanical-panel summary').click();
  await page.getByRole('button', { name: /Uncertain date/ }).click();
  await page.getByRole('button', { name: 'Find quote in filing' }).click();
  await page.waitForFunction(() => document.querySelector('input[aria-label="Search filing"]')?.value.startsWith('Acme received'));
  record('finding to source search', (await page.getByRole('textbox', { name: 'Search filing' }).inputValue()).startsWith('Acme received'));
  await page.getByRole('combobox', { name: 'Finding judgment' }).selectOption('supported');
  await screenshot(page, 'desktop-review-edit.png');
  await saveUi(page, 'Browser edited all four sheets');
  const saved = await api(page, '/api/deal/synthetic');
  record('browser save revision', saved.status === 200 && saved.body.workspace.revision === 1);
  record('browser four sheets persisted', saved.body.ledger.rows[0].cells.Note === 'Synthetic edited note' && saved.body.rounds.rows[0].cells['How opened'] === 'Synthetic opening edited' && saved.body.questions.rows[0].cells['Recommended answer'] === 'Still uncertain in fixture' && saved.body.facts[0].value === 'Synthetic Acme UI');
  record('browser decision attribution', saved.body.findings[0].judgment === 'supported' && saved.body.findings[0].actor === 'local');
  await screenshot(page, 'desktop-saved.png');

  await chooseTab(page, 'Changes');
  await page.getByRole('tabpanel').getByText('Synthetic Acme UI').waitFor();
  record('changes tab full value', await page.getByRole('tabpanel').getByText('Synthetic Acme UI').count() > 0);
  await chooseTab(page, 'History');
  await page.getByText('Browser edited all four sheets').waitFor();
  record('history attribution', await page.getByText(/local/).count() > 0);
  await screenshot(page, 'desktop-history.png');
  await page.getByRole('combobox', { name: 'Version' }).selectOption('version-1-raw');
  await page.getByText('Read only version').waitFor();
  record('raw version read only', await page.getByRole('button', { name: 'Save changes' }).isDisabled());
  await page.getByRole('combobox', { name: 'Version' }).selectOption('working');
  await waitForRevision(page, 1);
  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('link', { name: 'Export Excel' }).click();
  const download = await downloadPromise;
  record('Excel download', download.suggestedFilename() === 'synthetic-working-r1.xlsx');
  const fourSheetPromise = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Excel download options' }).click();
  await page.getByRole('menuitem', { name: 'Four sheets only (checker format)' }).click();
  const fourSheet = await fourSheetPromise;
  record('four-sheet Excel download', fourSheet.url().endsWith('source=0') && fourSheet.suggestedFilename() === 'synthetic-working-r1.xlsx');

  await chooseTab(page, 'Ledger');
  await page.getByRole('button', { name: 'Clone to split' }).click();
  await page.locator('.record-editor').getByRole('textbox', { name: 'Event' }).fill('Synthetic split event');
  await saveUi(page, 'Browser insert event');
  let current = await api(page, '/api/deal/synthetic');
  record('browser insert', current.body.ledger.rows.length === 4 && current.body.ledger.rows.some(r => r.cells.Event === 'Synthetic split event'));
  await page.locator('.event-item').filter({ hasText: 'Synthetic split event' }).click();
  await page.getByRole('button', { name: 'Move up' }).click();
  await saveUi(page, 'Browser move event');
  current = await api(page, '/api/deal/synthetic');
  record('browser move', current.body.ledger.rows[0].cells.Event === 'Synthetic split event');
  await page.getByRole('button', { name: 'Delete', exact: true }).click();
  await page.getByRole('dialog', { name: 'Delete record' }).waitFor();
  record('delete dialog receives focus', await page.evaluate(() => Boolean(document.activeElement?.closest('[role="dialog"]'))));
  await page.keyboard.press('Escape');
  await page.getByRole('dialog', { name: 'Delete record' }).waitFor({ state: 'hidden' });
  record('delete dialog Escape returns focus', await page.getByRole('button', { name: 'Delete', exact: true }).evaluate(element => element === document.activeElement));
  await page.getByRole('button', { name: 'Delete', exact: true }).click();
  await page.getByRole('dialog', { name: 'Delete record' }).getByRole('button', { name: 'Stage deletion' }).click();
  await saveUi(page, 'Browser delete event');
  current = await api(page, '/api/deal/synthetic');
  record('browser delete', current.body.ledger.rows.length === 3 && !current.body.ledger.rows.some(r => r.cells.Event === 'Synthetic split event'));

  await chooseTab(page, 'History');
  page.once('dialog', dialog => dialog.accept());
  await page.locator('.history-item').filter({ hasText: 'Browser edited all four sheets' }).getByRole('button', { name: 'Restore' }).click();
  await page.getByText('Revision saved', { exact: true }).waitFor();
  current = await api(page, '/api/deal/synthetic');
  record('browser restore appends history', current.body.workspace.revision === 5 && current.body.ledger.rows.length === 3);
  await screenshot(page, 'desktop-restored.png');

  await chooseTab(page, 'History');
  record('base revision restore control', await page.locator('.history-item').filter({ hasText: 'Revision 0' }).getByRole('button', { name: 'Restore' }).count() === 1);
  page.once('dialog', dialog => dialog.accept());
  await page.locator('.history-item').filter({ hasText: 'Revision 0' }).getByRole('button', { name: 'Restore' }).click();
  await waitForRevision(page, 6);
  current = await api(page, '/api/deal/synthetic');
  record('browser undo first save', current.body.workspace.revision === 6 && current.body.facts[0].value === 'Synthetic Acme');

  await chooseTab(page, 'Ledger');
  const noteField = page.locator('.record-editor').getByRole('textbox', { name: 'Note', exact: true });
  await noteField.fill('Delayed save value');
  let releaseSave;
  let sawDelayedRequest;
  const delayedRequest = new Promise(resolve => { sawDelayedRequest = resolve; });
  const gate = new Promise(resolve => { releaseSave = resolve; });
  const delayedRoute = async route => { sawDelayedRequest(); await gate; await route.continue(); };
  await page.route('**/api/deal/synthetic/edit', delayedRoute);
  await page.getByRole('button', { name: 'Save changes' }).click();
  await delayedRequest;
  record('save pending blocks editor', await noteField.isDisabled());
  record('save pending blocks version change', await page.getByRole('combobox', { name: 'Version' }).isDisabled());
  releaseSave();
  await page.getByText('Revision saved', { exact: true }).waitFor();
  await page.unroute('**/api/deal/synthetic/edit', delayedRoute);
  current = await api(page, '/api/deal/synthetic');
  record('delayed save keeps edit', current.body.ledger.rows[0].cells.Note === 'Delayed save value');

  await noteField.fill('Browser draft after conflict');
  const external = await page.evaluate(async () => {
    const [session, deal] = await Promise.all([fetch('/api/session').then(r => r.json()), fetch('/api/deal/synthetic').then(r => r.json())]);
    const response = await fetch('/api/deal/synthetic/edit', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Cockpit-CSRF': session.csrf_token }, body: JSON.stringify({ revision: deal.workspace.revision, base_sha256: deal.workspace.base_sha256, reason: 'Concurrent synthetic edit', operations: [{ type: 'update', sheet: 'Deal ledger', uid: deal.ledger.rows[1].uid, values: { Note: 'Other editor value' } }] }) });
    return response.status;
  });
  record('simulated concurrent save', external === 200, `status=${external}`);
  await page.getByRole('button', { name: 'Save changes' }).click();
  await page.getByRole('button', { name: 'Download staged edits' }).waitFor();
  record('conflict keeps browser draft', await noteField.inputValue() === 'Browser draft after conflict');
  const draftDownload = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Download staged edits' }).click();
  const draft = await draftDownload;
  const draftText = await readFile(await draft.path(), 'utf8');
  record('conflict draft export includes edit', draftText.includes('Browser draft after conflict'));
  await screenshot(page, 'desktop-conflict.png');
  page.once('dialog', dialog => dialog.accept());
  await page.getByRole('button', { name: 'Discard edits and load latest' }).click();
  await waitForRevision(page, 8);
  const reloadedNote = await noteField.inputValue();
  record('explicit conflict reload', reloadedNote === 'Other editor value', `note=${JSON.stringify(reloadedNote)}`);

  // Bulk Process/Round: pick events in select mode (click, then shift-click a range), confirm, stage, save once.
  await chooseTab(page, 'Ledger');
  await page.locator('.event-item').filter({ hasText: 'Offer' }).click();
  await page.getByRole('button', { name: 'Select', exact: true }).click();
  record('select mode hides Add', await page.locator('.record-list').getByRole('button', { name: 'Add', exact: true }).count() === 0);
  await page.locator('.event-item').filter({ hasText: 'Offer' }).click();
  await page.locator('.event-item').filter({ hasText: 'Signing' }).click({ modifiers: ['Shift'] });
  record('shift-click picks a range', (await page.locator('.pick-count').innerText()) === '2 selected' && await page.locator('.event-item[aria-pressed="true"]').count() === 2);
  await page.getByRole('button', { name: 'Set Process/Round…' }).click();
  const bulkDialog = page.getByRole('dialog', { name: 'Set Process and Round' });
  await bulkDialog.waitFor();
  record('bulk dialog receives focus', await page.evaluate(() => document.activeElement?.closest('[role="dialog"]') != null));
  await bulkDialog.getByRole('textbox', { name: 'Round' }).fill('1');
  record('bulk dialog says when nothing changes', (await bulkDialog.locator('.bulk-summary').innerText()).startsWith('No selected event changes'));
  await bulkDialog.getByRole('textbox', { name: 'Round' }).fill('2');
  const summary = await bulkDialog.locator('.bulk-summary').innerText();
  record('bulk dialog confirms the rows that change', summary.includes('This changes 2 events') && summary.includes('#2–#3'), summary);
  await screenshot(page, 'desktop-bulk-dialog.png');
  await bulkDialog.getByRole('button', { name: 'Stage for 2 events' }).click();
  await bulkDialog.waitFor({ state: 'hidden' });
  record('bulk edit staged as two changes', (await page.locator('.work-state').innerText()).includes('2 unsaved changes'));
  record('bulk edit default reason', await page.getByRole('textbox', { name: 'Reason for this revision' }).inputValue() === 'Set Round 2 on 2 events');
  // A later edit of one picked event's Round, in the open editor, is saved after the bulk value.
  await page.locator('.record-editor').getByRole('textbox', { name: /^Round/ }).fill('3');
  await page.getByRole('button', { name: 'Save changes' }).click();
  await page.getByText('Revision saved', { exact: true }).waitFor();
  current = await api(page, '/api/deal/synthetic');
  const bulkHistory = await api(page, '/api/deal/synthetic/history');
  record('bulk edit saved as one revision', current.body.workspace.revision === 9 && current.body.ledger.rows.map(r => r.cells.Round).join() === '1,3,2'
    && bulkHistory.body.history[0].reason === 'Set Round 2 on 2 events' && bulkHistory.body.history[0].summary === '2 changes');
  await screenshot(page, 'desktop-bulk-saved.png');
  await page.getByRole('button', { name: 'Done', exact: true }).click();
  record('select mode ends', await page.locator('.pick-bar').count() === 0 && await page.locator('.record-list').getByRole('button', { name: 'Add', exact: true }).count() === 1);

  for (const viewport of [{ width: 1024, height: 768, label: 'laptop' }, { width: 390, height: 844, label: 'narrow' }]) {
    const narrow = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height }, reducedMotion: 'reduce' });
    await useStagedAssets(narrow);
    const view = await narrow.newPage();
    view.on('pageerror', error => errors.push(error.message));
    await view.goto(base + '/deal/synthetic', { waitUntil: 'networkidle' });
    await view.getByRole('heading', { name: 'Synthetic Acme' }).waitFor();
    await assertNoOverflow(view, `${viewport.label} ${viewport.width}`);
    if (viewport.label === 'laptop') {
      await assertControlWithin(view, view.getByRole('button', { name: 'Go', exact: true }), view.locator('.filing-pane'), `${viewport.label} Page Go contained`);
      await assertControlWithin(view, view.locator('.record-editor').getByRole('textbox', { name: 'When', exact: true }), view.locator('.record-editor'), `${viewport.label} When editor contained`);
    }
    await screenshot(view, `${viewport.label}-ledger.png`);
    await view.getByRole('button', { name: 'Select', exact: true }).click();
    await view.locator('.event-item').first().click();
    await assertNoOverflow(view, `${viewport.label} select mode`);
    await assertControlWithin(view, view.getByRole('button', { name: 'Set Process/Round…' }), view.locator('.record-list'), `${viewport.label} Set Process/Round contained`);
    await screenshot(view, `${viewport.label}-select-mode.png`);
    await view.getByRole('button', { name: 'Done', exact: true }).click();
    if (viewport.label === 'narrow') {
      await view.getByRole('group', { name: 'Visible pane' }).getByRole('button', { name: 'Filing' }).click();
      record('narrow filing pane', await view.getByRole('region', { name: 'SEC filing' }).isVisible());
      await assertControlWithin(view, view.getByRole('button', { name: 'Go', exact: true }), view.locator('.filing-pane'), 'narrow Page Go contained');
      await screenshot(view, 'narrow-filing.png');
      await view.getByRole('group', { name: 'Visible pane' }).getByRole('button', { name: 'Workspace' }).click();
      await chooseTab(view, 'Review');
      await screenshot(view, 'narrow-review.png');
    }
    await narrow.close();
  }
  record('no browser exceptions', errors.length === 0, errors.join('; '));
  await context.close();
  await writeFile(resolve(EVIDENCE, 'browser-results.json'), JSON.stringify({ run_at: new Date().toISOString(), results, screenshots, chrome: '/opt/google/chrome/chrome', mode: 'isolated headless synthetic fixture' }, null, 2) + '\n');
  console.log(JSON.stringify({ passed: results.length, screenshots }, null, 2));
}

try {
  await run();
} catch (error) {
  const failure = { run_at: new Date().toISOString(), results, screenshots, error: error.stack || String(error), server_stderr: serverStderr };
  await mkdir(EVIDENCE, { recursive: true });
  await writeFile(resolve(EVIDENCE, 'browser-results.json'), JSON.stringify(failure, null, 2) + '\n');
  console.error(error.stack || error);
  process.exitCode = 1;
} finally {
  for (const browser of browsers) await browser.close().catch(() => {});
  fixture.kill('SIGTERM');
  await Promise.race([once(fixture, 'exit'), new Promise(resolve => setTimeout(resolve, 5000))]);
}
