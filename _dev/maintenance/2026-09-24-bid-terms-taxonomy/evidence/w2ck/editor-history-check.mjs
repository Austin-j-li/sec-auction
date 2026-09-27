// Quick headless check: "Choose from the list" brings the drop-down back after an off-list value was typed;
// the History tab's Download links use the server's names.
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import playwright from '/home/uctpiaj/work/vm-browser/node_modules/playwright/index.mjs';

const repo = '/home/uctpiaj/work/tmp/v114-scratch/pkg/w2ck';
const dist = process.env.DIST, out = process.env.OUT;
const server = spawn('python3', [resolve(repo, '_dev/tools/cockpit/acceptance/serve_fixture.py')], { cwd: repo, stdio: ['ignore', 'pipe', 'inherit'] });
let base;
for await (const line of createInterface({ input: server.stdout })) if (line.startsWith('{')) { base = JSON.parse(line).url; break; }
const browser = await playwright.chromium.launch({ headless: true, executablePath: '/opt/google/chrome/chrome', args: ['--no-sandbox', '--disable-dev-shm-usage'] });
const log = [];
try {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, acceptDownloads: true });
  await context.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (url.pathname.startsWith('/api/')) return route.continue();
    const asset = url.pathname.startsWith('/assets/') ? url.pathname.slice(1) : 'index.html';
    const type = asset.endsWith('.js') ? 'text/javascript' : asset.endsWith('.css') ? 'text/css' : asset.endsWith('.woff2') ? 'font/woff2' : 'text/html';
    try { return route.fulfill({ body: await readFile(resolve(dist, asset)), contentType: type }); } catch { return route.continue(); }
  });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(base + '/deal/synthetic', { waitUntil: 'networkidle' });
  await page.locator('.event-item').filter({ hasText: 'Offer' }).click();
  const formality = page.locator('.record-editor').getByRole('combobox', { name: /^Formality/ });
  await formality.selectOption('__other__');
  const text = page.locator('.record-editor').getByRole('textbox', { name: /^Formality/ });
  await text.fill('Formal-ish');
  log.push(['typed off-list value in free text', await text.inputValue()]);
  await page.locator('.field-cell').filter({ has: page.getByRole('textbox', { name: /^Formality/ }) }).getByRole('button', { name: 'Choose from the list' }).click();
  log.push(['stored off-list values offering Choose from the list', await page.locator('.field-cell').filter({ hasText: 'Not on this version’s list' }).evaluateAll(cells => cells.map(cell => cell.querySelector('label')?.textContent))]);
  const back = page.locator('.record-editor').getByRole('combobox', { name: /^Formality/ });
  await back.waitFor();
  const shown = await back.evaluate(select => ({ value: select.value, label: select.selectedOptions[0]?.textContent }));
  log.push(['after Choose from the list', shown]);
  assert.deepEqual(shown, { value: 'Formal-ish', label: 'Formal-ish (not on the list)' });
  await page.locator('.record-editor').screenshot({ path: resolve(out, 'choose-from-list-kept.png') });
  await back.selectOption('Formal');
  assert.equal(await back.inputValue(), 'Formal');
  assert.equal(await back.locator('option', { hasText: 'not on the list' }).count(), 0);
  log.push(['picked Formal; off-list entry gone', true]);
  await page.getByRole('button', { name: 'Save changes' }).click();
  await page.getByText('Revision saved').waitFor();
  await page.getByRole('tab', { name: /^History/ }).click();
  await page.locator('#revision-1 .history-actions a').first().waitFor();
  const links = await page.locator('.history-actions a').evaluateAll(anchors => anchors.map(a => [a.textContent, a.getAttribute('href'), a.getAttribute('download')]));
  log.push(['history links', links]); console.log(JSON.stringify(log, null, 1));
  assert.ok(links.some(([label, href, download]) => label === 'Download' && href === '/api/deal/synthetic/export?version=rev%3A1' && download === ''));
  assert.ok(links.some(([label, href]) => label === 'Four sheets' && href === '/api/deal/synthetic/export?version=rev%3A0&source=0'));
  const [download] = await Promise.all([page.waitForEvent('download'), page.locator('#revision-0 .history-actions a', { hasText: 'Download' }).click()]);
  log.push(['revision 0 download name', download.suggestedFilename()]);
  assert.equal(download.suggestedFilename(), 'synthetic-working-r0.xlsx');
  assert.equal(errors.length, 0, errors.join('; '));
} finally {
  await browser.close();
  server.kill('SIGTERM');
}
console.log(JSON.stringify(log, null, 1));
console.log('OK');
