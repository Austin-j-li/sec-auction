/* Instructions and engines acceptance: token and ChatGPT sign-in, engine gating, draft/edit/stale save/publish/default,
   a Fable run and a Sol run under different instructions through the fake worker, Compare and Activity. No model is called. */
/* Run from repo root: node _dev/tools/cockpit/acceptance/test_instructions.mjs (COCKPIT_TEST_DIST=<dist> to test a staged build) */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import playwright from '/home/uctpiaj/work/vm-browser/node_modules/playwright/index.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '../../../..');
const EVIDENCE = resolve(process.env.COCKPIT_INSTRUCTIONS_EVIDENCE || resolve(tmpdir(), 'cockpit-instructions-acceptance'));
const STAGED_DIST = process.env.COCKPIT_TEST_DIST ? resolve(process.env.COCKPIT_TEST_DIST) : null;
const ACCESS = {}; // each user's Cloudflare Access token, signed by the fixture's own key (serve_fixture.py --two-users)
const TOKEN = `sk-ant-oat01-${'A'.repeat(40)}`;
const STALE = 'Someone saved this draft since you opened it.';
const FABLE = 'Fable’s safety filter often blocks runs partway (6 of 11 test prompts); a blocked run fails and must be restarted.';
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

async function fixtureInfo() {
  for await (const line of createInterface({ input: fixture.stdout })) if (line.startsWith('{')) { const info = JSON.parse(line); Object.assign(ACCESS, info.access); return info; }
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
  // The stale save below answers 409 on purpose; any other console error counts.
  page.on('console', message => { if (message.type() === 'error' && !message.text().includes('status of 409')) browserErrors.push(`${user}: ${message.text()}`); });
  page.on('dialog', dialog => dialog.accept());
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

const selectedId = page => new URL(page.url()).searchParams.get('id');
const editor = page => page.getByRole('textbox', { name: 'Instruction text' });
async function appendAndSave(page, line) {
  const box = editor(page);
  await box.fill(`${await box.inputValue()}\n${line}`);
  await page.getByRole('button', { name: 'Save draft' }).click();
}

async function waitForJobs(page, count, timeout = 120000) {
  const until = Date.now() + timeout;
  for (;;) {
    const jobs = (await api(page, '/api/deal/synthetic/jobs')).body.jobs;
    if (jobs.length >= count && jobs.every(job => ['completed', 'failed', 'timed_out', 'cancelled'].includes(job.state))) return jobs;
    if (Date.now() > until) throw new Error(`runs did not finish: ${JSON.stringify(jobs)}`);
    await new Promise(done => setTimeout(done, 1000));
  }
}

async function startRun(page, base, engine, instructionId) {
  await page.goto(base + '/deal/synthetic');
  await page.getByRole('button', { name: 'Extract', exact: true }).click();
  const dialog = page.getByRole('dialog', { name: 'Start an extraction' });
  await dialog.getByLabel('Instruction').locator(`option[value="${instructionId}"]`).waitFor({ state: 'attached' });
  await dialog.getByLabel('Engine').selectOption(engine);
  await dialog.getByLabel('Instruction').selectOption(instructionId);
  const summary = await dialog.locator('.extract-summary').innerText();
  await dialog.getByRole('button', { name: 'Start extraction' }).click();
  await dialog.waitFor({ state: 'detached' });
  return summary;
}

async function run() {
  await mkdir(EVIDENCE, { recursive: true });
  const { url: base, root } = await fixtureInfo();
  const browser = await playwright.chromium.launch({ headless: true, executablePath: '/opt/google/chrome/chrome', args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  try {
    const austin = await userPage(browser, base, 'austin');
    const alex = await userPage(browser, base, 'alex');

    // (1) Austin connects Claude with a pasted token and ChatGPT with the device sign-in.
    await austin.goto(base + '/settings');
    await austin.getByText('Paste a token instead').click();
    await austin.getByLabel('Token').fill(TOKEN);
    await austin.getByRole('button', { name: 'Save token' }).click();
    await austin.getByRole('button', { name: 'Reconnect Claude account' }).waitFor({ timeout: 20000 });
    await austin.getByRole('button', { name: 'Connect ChatGPT account' }).click();
    const code = austin.locator('.device-code');
    await code.waitFor({ timeout: 20000 });
    const link = await austin.locator('#chatgpt-account-head').locator('xpath=../..').locator('.connect-link').getAttribute('href');
    record('ChatGPT sign-in shows link and code', link === 'https://auth.openai.com/codex/device' && (await code.innerText()) === 'TSTB-IOSMS', link);
    await austin.getByText('Waiting for you to approve…').waitFor();
    await austin.screenshot({ path: resolve(EVIDENCE, 'austin-chatgpt-code.png') });
    await writeFile(resolve(root, 'codex-flag'), 'approve');
    await austin.getByText('ChatGPT account connected.').waitFor({ timeout: 30000 });
    const account = (await api(austin, '/api/account')).body;
    record('both of Austin’s accounts connected', account.claude.connected && account.chatgpt.connected && !JSON.stringify(account).includes('sk-ant-oat'), JSON.stringify(account.chatgpt));
    record('Austin’s engines all usable', account.engines.every(engine => engine.connected), JSON.stringify(account.engines));
    await austin.screenshot({ path: resolve(EVIDENCE, 'austin-settings.png') });

    // (2) Engine gating: Alex has connected nothing, so every engine (Sol and Astra included) is disabled.
    await alex.goto(base + '/deal/synthetic');
    await alex.getByRole('button', { name: 'Extract', exact: true }).click();
    const alexDialog = alex.getByRole('dialog', { name: 'Start an extraction' });
    await alexDialog.getByLabel('Engine').waitFor();
    const alexOptions = await alexDialog.getByLabel('Engine').locator('option').evaluateAll(options => options.map(option => ({ value: option.value, disabled: option.disabled, text: option.textContent })));
    record('Sol and Astra disabled without ChatGPT', ['sol6', 'astra6'].every(id => alexOptions.find(option => option.value === id)?.disabled && alexOptions.find(option => option.value === id).text.includes('connect your ChatGPT account in Settings')), JSON.stringify(alexOptions));
    record('no Start button without an account', await alexDialog.getByRole('button', { name: 'Start extraction' }).count() === 0 && await alexDialog.getByRole('link', { name: 'Open settings' }).count() === 1);
    await alex.screenshot({ path: resolve(EVIDENCE, 'alex-extract-gated.png') });
    await alexDialog.getByRole('button', { name: 'Close' }).first().click();

    await austin.goto(base + '/deal/synthetic');
    await austin.getByRole('button', { name: 'Extract', exact: true }).click();
    const austinDialog = austin.getByRole('dialog', { name: 'Start an extraction' });
    await austinDialog.getByLabel('Engine').selectOption('fable51');
    await austinDialog.getByText(FABLE).waitFor();
    record('Fable shows its warning', true);
    const soloOptions = await austinDialog.getByLabel('Engine').locator('option').evaluateAll(options => options.filter(option => option.disabled).length);
    record('Austin’s engines are enabled', soloOptions === 0);
    await austin.screenshot({ path: resolve(EVIDENCE, 'austin-extract-fable.png') });
    await austinDialog.getByRole('button', { name: 'Cancel' }).click();

    // (3) Instructions: Alex starts a draft from Version 1; Austin opens it before Alex saves.
    const list = (await api(alex, '/api/instructions')).body;
    const version1 = list.items.find(item => item.name === 'Version 1');
    record('Version 1 imported as the default', Boolean(version1) && list.default_id === version1.id, JSON.stringify(list));
    await alex.goto(`${base}/instructions?id=${version1.id}`);
    await alex.getByRole('button', { name: 'New draft from this' }).click();
    await editor(alex).waitFor();
    const draftId = selectedId(alex);
    record('draft created from Version 1', Boolean(draftId) && draftId !== version1.id && (await alex.locator('.instruction-entry.selected').innerText()).includes('draft'));
    await austin.goto(`${base}/instructions?id=${draftId}`);
    await editor(austin).waitFor();

    await appendAndSave(alex, 'Alex: state the objective before the procedure.');
    await alex.getByText('Saved', { exact: true }).waitFor();
    await alex.getByRole('button', { name: 'Changes from Version 1' }).click();
    await alex.locator('.diff-add', { hasText: 'Alex: state the objective before the procedure.' }).waitFor();
    record('diff shows the added line', (await alex.locator('.diff-summary').innerText()).includes('1 line added'));
    await alex.screenshot({ path: resolve(EVIDENCE, 'alex-draft-diff.png') });

    await appendAndSave(austin, 'Austin: a stale edit.');
    await austin.getByText(STALE).waitFor();
    record('stale save refused with a message', true);
    await austin.screenshot({ path: resolve(EVIDENCE, 'austin-stale.png') });
    await austin.getByRole('button', { name: 'Reload the draft' }).click();
    await austin.getByText(STALE).waitFor({ state: 'detached' });
    await austin.waitForFunction(() => document.querySelector('textarea[aria-label="Instruction text"]')?.value.includes('Alex: state the objective'), null, { timeout: 10000 });
    record('reload shows Alex’s saved text', (await editor(austin).inputValue()).includes('Alex: state the objective') && !(await editor(austin).inputValue()).includes('Austin: a stale edit.'));

    await austin.getByRole('button', { name: 'Publish…' }).click();
    const publish = austin.getByRole('dialog', { name: 'Publish this draft' });
    await publish.getByLabel('Name').fill('Test version 2');
    await publish.getByLabel('Change note').fill('State the objective before the procedure.');
    await publish.getByRole('button', { name: 'Publish', exact: true }).click();
    await publish.waitFor({ state: 'detached' });
    await austin.getByRole('button', { name: 'Make default' }).click();
    await austin.locator('.instruction-status', { hasText: 'default' }).waitFor();
    const published = (await api(austin, '/api/instructions')).body;
    const version2 = published.items.find(item => item.name === 'Test version 2');
    record('published as Test version 2 with its note and made default', version2?.id === draftId && version2.status === 'published' && version2.note === 'State the objective before the procedure.' && published.default_id === version2.id, JSON.stringify(version2));
    await austin.screenshot({ path: resolve(EVIDENCE, 'austin-published.png') });

    // (4) A second draft for the Sol run, then one Fable run under Version 1 and one Sol run under the draft.
    await austin.getByRole('button', { name: 'New draft from this' }).click();
    await austin.waitForFunction(id => new URL(location.href).searchParams.get('id') !== id, draftId);
    await editor(austin).waitFor();
    const secondId = selectedId(austin);
    await appendAndSave(austin, 'Austin: say when the filing is silent.');
    await austin.getByText('Saved', { exact: true }).waitFor();
    const second = (await api(austin, `/api/instructions/${secondId}`)).body.item;

    const fableSummary = await startRun(austin, base, 'fable51', version1.id);
    const solSummary = await startRun(austin, base, 'sol6', secondId);
    record('extract summaries name engine, instruction and plan', fableSummary.startsWith('Fable 5.1 · medium · Version 1 · on Austin’s Claude plan') && solSummary.startsWith(`GPT-6-Sol · medium · ${second.label} · on Austin’s ChatGPT plan`), `${fableSummary} | ${solSummary}`);
    const jobs = await waitForJobs(austin, 2);
    const fableJob = jobs.find(job => job.params.engine === 'fable51'), solJob = jobs.find(job => job.params.engine === 'sol6');
    record('both runs completed', fableJob?.state === 'completed' && solJob?.state === 'completed', JSON.stringify(jobs));
    record('runs froze their instructions', fableJob.params.instruction.sha256 === version1.sha256 && solJob.params.instruction.sha256 === second.sha256 && solJob.params.instruction.status === 'draft', JSON.stringify([fableJob.params, solJob.params]));

    await austin.goto(base + '/deal/synthetic');
    await austin.getByRole('tab', { name: 'Runs' }).click();
    const runLines = await austin.locator('.run-head > div > span').allInnerTexts();
    record('Runs tab names engine and instruction', runLines.some(line => line.startsWith('GPT-6-Sol · medium · draft')) && runLines.some(line => line.startsWith('Fable 5.1 · medium · Version 1')), JSON.stringify(runLines));
    await austin.screenshot({ path: resolve(EVIDENCE, 'austin-runs.png') });
    const versions = (await api(austin, '/api/deal/synthetic')).body.versions;
    const fableVersion = versions.find(v => v.id === fableJob.version_id), solVersion = versions.find(v => v.id === solJob.version_id);
    record('version labels name engine and instruction', fableVersion?.label.startsWith('Fable 5.1 · medium · Version 1') && solVersion?.label.startsWith(`GPT-6-Sol · medium · ${second.label}`), JSON.stringify([fableVersion?.label, solVersion?.label]));
    const dropdown = await austin.getByLabel('Version', { exact: true }).locator('option').allInnerTexts();
    record('both versions in the dropdown', dropdown.some(text => text.startsWith('Fable 5.1')) && dropdown.some(text => text.startsWith('GPT-6-Sol')), JSON.stringify(dropdown));

    await austin.getByRole('tab', { name: 'Changes' }).click();
    await austin.getByRole('group', { name: 'Compare' }).getByLabel('From').selectOption(fableVersion.id);
    await austin.getByRole('group', { name: 'Compare' }).getByLabel('To').selectOption(solVersion.id);
    await austin.getByText('These versions were made under different instructions').waitFor();
    const compare = (await api(austin, `/api/deal/synthetic/compare?from=${encodeURIComponent(fableVersion.id)}&to=${encodeURIComponent(solVersion.id)}`)).body;
    record('Compare reports different instructions', compare.same_instruction === false, JSON.stringify({ same: compare.same_instruction }));
    await austin.screenshot({ path: resolve(EVIDENCE, 'austin-compare.png') });

    // (5) Activity lists the instruction events, linked to the Instructions page.
    await alex.goto(base + '/activity');
    // A draft's label names its current text, so the item (written at creation) is matched by its author and parent.
    for (const text of [/Started draft [0-9a-f]{7} \(Austin\) from Test version 2/, 'Published Test version 2: State the objective before the procedure.', 'Made Test version 2 the default instruction']) {
      await alex.locator('.activity-detail', { hasText: text }).first().waitFor();
    }
    record('Activity shows the instruction items', await alex.locator('.activity-table a.deal-link', { hasText: 'Instructions' }).count() >= 4);
    const kinds = new Set((await api(alex, '/api/activity?limit=100')).body.items.map(item => item.kind));
    record('instruction kinds in the feed', ['instruction_draft', 'instruction_published', 'instruction_default'].every(kind => kinds.has(kind)), JSON.stringify([...kinds]));
    await alex.locator('.activity-table a.deal-link', { hasText: 'Instructions' }).first().click();
    await alex.getByRole('heading', { name: 'Instructions', level: 1 }).waitFor();
    record('instruction item opens the Instructions page', new URL(alex.url()).pathname === '/instructions');
    await alex.screenshot({ path: resolve(EVIDENCE, 'alex-activity-instructions.png') });
    record('no browser errors', browserErrors.length === 0, browserErrors.join('\n'));
  } finally {
    await browser.close();
    fixture.kill('SIGTERM');
  }
  console.log(JSON.stringify({ passed: results.length, results, evidence: EVIDENCE }, null, 2));
}

run().catch(error => { fixture.kill('SIGTERM'); console.error(error); console.error(serverStderr.slice(-3000)); process.exit(1); });
