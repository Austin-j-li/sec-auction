import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { mkdir } from 'node:fs/promises';
import { resolve } from 'node:path';
import playwright from '/home/uctpiaj/work/vm-browser/node_modules/playwright/index.mjs';

const EVIDENCE = resolve(process.env.S2_UI_EVIDENCE);
const fixture = spawn('python3', [resolve(process.env.S2_UI_DIR, 'serve_s2.py')], { stdio: ['ignore', 'pipe', 'pipe'] });
let serverStderr = ''; fixture.stderr.setEncoding('utf8'); fixture.stderr.on('data', d => { serverStderr += d; });
const results = [], errors = [];
const record = (name, passed, detail = '') => { results.push({ name, passed }); assert.ok(passed, `${name} ${detail}`); };
async function announced() { for await (const line of createInterface({ input: fixture.stdout })) if (line.startsWith('{')) return JSON.parse(line); throw new Error(serverStderr); }

async function run() {
  await mkdir(EVIDENCE, { recursive: true });
  const { url, version } = await announced();
  const browser = await playwright.chromium.launch({ headless: true, executablePath: '/opt/google/chrome/chrome', args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  try {
    const page = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
    page.on('pageerror', e => errors.push(e.message)); page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    await page.goto(url + '/');
    const tip = await page.locator('.deal-table small.mono[title^="Live check"]').first().getAttribute('title');
    record('all deals tooltip names the checker', /^Live check: checker \d+\.\d+, v1\.13\.2 rules$/.test(tip), tip);

    await page.goto(url + '/deal/synthetic');
    await page.getByRole('tab', { name: 'Review' }).click();
    const lines = await page.locator('.checker-lines').textContent();
    record('review tab: live check line', /^Live check: checker \d+\.\d+, v1\.13\.2 rules$/.test(lines.trim()), lines);
    await page.getByRole('tab', { name: 'Ledger' }).click();
    const formality = page.locator('.field-cell', { has: page.getByText('Formality', { exact: true }) }).locator('select');
    const options = await formality.locator('option').allInnerTexts();
    record('listed field offers Other…', options.includes('Other…') && options.includes('Formal'), options.join('|'));
    await formality.selectOption({ label: 'Other…' });
    await page.locator('.field-cell', { has: page.getByText('Formality', { exact: true }) }).getByRole('button', { name: 'Choose from the list' }).waitFor();
    record('Other… switches to free text', true);
    await page.getByRole('tab', { name: 'Rounds' }).click();
    const outcome = page.locator('.field-cell', { has: page.getByText('Deadline outcome', { exact: true }) });
    const addOutcome = page.getByLabel('Add a Deadline outcome value');
    await addOutcome.selectOption('Extended');
    await addOutcome.selectOption('Enforced');
    const typed = await page.getByRole('textbox', { name: /^Deadline outcome/ }).inputValue();
    record('deadline picker builds "A; B"', typed === 'Extended; Enforced', typed);
    const choices = await addOutcome.locator('option').allInnerTexts();
    record('v1.13.2 deadline list includes No deadline stated', choices.includes('No deadline stated') && choices.includes('Late bids accepted'), choices.join('|'));
    await page.screenshot({ path: resolve(EVIDENCE, 'deadline-picker.png') });
    await page.getByRole('button', { name: 'Discard edits and load latest' }).count(); // no conflict expected
    page.once('dialog', d => d.accept());
    await page.getByLabel('Version', { exact: true }).selectOption(version);
    await page.getByRole('button', { name: 'Use as working-copy base…' }).waitFor();
    const picker = await page.getByLabel('Version', { exact: true }).locator('option').allInnerTexts();
    record('version picker shows the checker version', picker.some(label => /checker \d+\.\d+/.test(label)), picker.join('|'));
    await page.getByRole('tab', { name: 'Review' }).click();
    const importLine = await page.locator('.checker-lines').textContent();
    record('review tab: at-import line for a run version', /Live check: checker [\d.]+, v1\.14 rules\s*At import: checker [\d.]+, \d+ errors?, \d+ warnings?/.test(importLine), importLine);
    await page.getByRole('tab', { name: 'Rounds' }).click();
    const v114 = await page.getByLabel('Add a Deadline outcome value').locator('option').allInnerTexts();
    record('v1.14 deadline list', v114.includes('Extended (late bid accepted)') && !v114.includes('Late bids accepted'), v114.join('|'));

    await page.getByRole('button', { name: 'Use as working-copy base…' }).click();
    const dialog = page.getByRole('dialog', { name: 'Use as working-copy base' });
    await dialog.locator('.rebase-list').waitFor();
    const listed = await dialog.locator('.rebase-list li').allInnerTexts();
    record('rebase dialog lists what stops applying', listed.some(l => l.startsWith('1 revision saved')) && listed.some(l => l.startsWith('1 row mark stops')) && listed.some(l => l.startsWith('1 finding judgment carries over')) && listed.some(l => l.startsWith('1 row thread')), listed.join('\n'));
    await page.screenshot({ path: resolve(EVIDENCE, 'rebase-dialog.png') });
    await dialog.getByLabel('Reason').fill('Rebase for the smoke test');
    await dialog.getByRole('button', { name: 'Use as base' }).click();
    await dialog.waitFor({ state: 'detached', timeout: 8000 }).catch(async () => { console.error('DIALOG: ' + await dialog.innerText()); await page.screenshot({ path: resolve(EVIDENCE, 'rebase-stuck.png') }); throw new Error('rebase dialog stayed'); });
    await page.getByRole('tab', { name: 'Review' }).click();
    await page.getByRole('button', { name: /Uncertain date/ }).click();
    record('carried judgment is shown', await page.getByText(/Judgment carried over from v1132-raw at revision 2/).count() === 1);
    const context = await page.locator('.thread-context').first().innerText();
    record('orphaned thread reads on an earlier base', context.startsWith('On an earlier base (revision 1)'), context);
    await page.screenshot({ path: resolve(EVIDENCE, 'after-rebase-review.png') });

    await page.getByRole('tab', { name: 'History' }).click();
    const download = page.locator('#revision-1').getByRole('link', { name: 'Download' });
    record('history offers a revision download', (await download.getAttribute('href')).endsWith('/export?version=rev:1'));
    await page.locator('#revision-1').getByRole('button', { name: 'Compare with working copy' }).click();
    await page.locator('.changes-tab .head-count', { hasText: 'Revision 1 → Working copy' }).waitFor();
    record('revision compares with the working copy', true);
    await page.screenshot({ path: resolve(EVIDENCE, 'revision-compare.png') });

    // Extract dialog: the default instruction matches the catalog base's (v1.13.2), so no line until the base changes; after the rebase it differs.
    await page.getByRole('button', { name: 'Extract' }).click();
    const extract = page.getByRole('dialog', { name: 'Start an extraction' });
    await extract.getByRole('button', { name: 'Start extraction' }).waitFor();
    await extract.getByRole('button', { name: 'Start extraction' }).and(page.locator(':enabled')).waitFor();
    await extract.locator('.extract-warning').first().waitFor({ timeout: 5000 }).catch(() => {});
    const notice = await extract.locator('.extract-warning').allInnerTexts();
    record('extract dialog warns when the working copy is under another instruction', notice.some(t => t.startsWith('The working copy (revision 2) is under another instruction with v1.14 columns')), notice.join('|'));
    await page.screenshot({ path: resolve(EVIDENCE, 'extract-notice.png') });
    record('no browser errors', errors.length === 0, errors.join('\n'));
  } finally { await browser.close(); fixture.kill('SIGTERM'); }
  console.log(JSON.stringify({ passed: results.length, results, evidence: EVIDENCE }, null, 2));
}
run().catch(e => { fixture.kill('SIGTERM'); console.error(e); console.error(serverStderr.slice(-3000)); process.exit(1); });
