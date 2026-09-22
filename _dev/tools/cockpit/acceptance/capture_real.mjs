/* Read-only viewport load check for the preserved 67-event Datalink raw deal. */
/* Run: node _dev/tools/cockpit/acceptance/capture_real.mjs */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { createHash } from 'node:crypto';
import { createInterface } from 'node:readline';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import playwright from '/home/uctpiaj/work/vm-browser/node_modules/playwright/index.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '../../../..');
const EVIDENCE = resolve(REPO, '_dev/reviews/2026-09-21-v1132-cockpit/cockpit-verification');
const fixture = spawn('python3', [resolve(HERE, 'serve_fixture.py'), '--real-readonly'], { cwd: REPO, stdio: ['ignore', 'pipe', 'pipe'] });
let stderr = '';
fixture.stderr.setEncoding('utf8');
fixture.stderr.on('data', chunk => { stderr += chunk; });
let browser;

async function url() {
  for await (const line of createInterface({ input: fixture.stdout })) {
    if (line.startsWith('{')) return JSON.parse(line).url;
  }
  throw new Error(`Real preview server failed: ${stderr}`);
}

async function digest(path) { return createHash('sha256').update(await readFile(path)).digest('hex'); }

async function run() {
  await mkdir(EVIDENCE, { recursive: true });
  const workbook = resolve(REPO, 'extraction/datalink.xlsx');
  const workbookBefore = await digest(workbook);
  const base = await url();
  const response = await fetch(base + '/api/deal/datalink');
  assert.equal(response.status, 200, `Datalink API status ${response.status}`);
  const deal = await response.json();
  assert.equal(deal.ledger.rows.length, 67);
  const source = resolve(REPO, 'raw_filing', deal.filing.file);
  const sourceBefore = await digest(source);
  const late = [...deal.ledger.rows].reverse().find(row => row.quote?.located);
  assert.ok(late && Number(late.id) >= 50, 'late located event expected');
  const session = await fetch(base + '/api/session').then(r => r.json());
  assert.equal(session.can_edit, false, 'read-only preview must deny writes');

  browser = await playwright.chromium.launch({ headless: true, executablePath: '/opt/google/chrome/chrome', args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const results = [];
  for (const viewport of [{ width: 1440, height: 1000, label: 'desktop' }, { width: 1024, height: 768, label: 'laptop' }]) {
    const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height }, reducedMotion: 'reduce' });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(`${base}/deal/datalink#row-${late.id}`, { waitUntil: 'networkidle', timeout: 90000 });
    await page.locator('.event-item.selected').waitFor({ timeout: 60000 });
    await page.locator('.filing-block').first().waitFor({ timeout: 60000 });
    assert.equal(await page.locator('.event-item').count(), 67);
    assert.ok((await page.locator('.event-item.selected').innerText()).includes(`#${late.id}`));
    const list = await page.locator('.record-list').boundingBox();
    const selected = await page.locator('.event-item.selected').boundingBox();
    assert.ok(list && selected && selected.y >= list.y - 2 && selected.y + selected.height <= list.y + list.height + 2, `${viewport.label}: late event is clipped from list`);
    const heading = await page.locator('.record-editor .editor-head h2').innerText();
    assert.ok(heading.includes(`#${late.id}`), `${viewport.label}: editor did not select late event`);
    const horizontal = await page.evaluate(() => ({ width: innerWidth, scrollWidth: document.documentElement.scrollWidth }));
    assert.ok(horizontal.scrollWidth <= horizontal.width + 2, `${viewport.label}: document overflow ${JSON.stringify(horizontal)}`);
    assert.equal(errors.length, 0, `${viewport.label}: ${errors.join('; ')}`);
    await page.screenshot({ path: resolve(EVIDENCE, `real-datalink-${viewport.label}-late-row.png`), fullPage: false });
    results.push({ viewport, selected_row: late.id, late_event_visible: true, editor_heading: heading, filing_blocks: await page.locator('.filing-block').count(), horizontal, browser_errors: errors });
    await context.close();
  }
  assert.equal(await digest(workbook), workbookBefore, 'original workbook changed');
  assert.equal(await digest(source), sourceBefore, 'original filing changed');
  const result = { run_at: new Date().toISOString(), mode: 'copied real inputs in isolated read-only localhost server', original_workbook_sha256: workbookBefore, original_source_sha256: sourceBefore, raw_rows: deal.ledger.rows.length, selected_late_row: late.id, results };
  await writeFile(resolve(EVIDENCE, 'real-preview-results.json'), JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify({ passed: results.length, selected_late_row: late.id, screenshots: results.map(item => `real-datalink-${item.viewport.label}-late-row.png`) }, null, 2));
}

try { await run(); }
catch (error) {
  await mkdir(EVIDENCE, { recursive: true });
  await writeFile(resolve(EVIDENCE, 'real-preview-results.json'), JSON.stringify({ run_at: new Date().toISOString(), error: error.stack || String(error), server_stderr: stderr }, null, 2) + '\n');
  console.error(error.stack || error);
  process.exitCode = 1;
} finally {
  if (browser) await browser.close().catch(() => {});
  fixture.kill('SIGTERM');
  await Promise.race([once(fixture, 'exit'), new Promise(resolve => setTimeout(resolve, 5000))]);
}
