/* Read-only visual QA of the actual nine-deal catalog through an ephemeral server. */
/* Run: node _dev/tools/cockpit/acceptance/capture_catalog.mjs */

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
const fixture = spawn('python3', [resolve(HERE, 'serve_fixture.py'), '--actual-catalog-readonly'], { cwd: REPO, stdio: ['ignore', 'pipe', 'pipe'] });
let stderr = '';
fixture.stderr.setEncoding('utf8');
fixture.stderr.on('data', chunk => { stderr += chunk; });
let browser;

async function url() {
  for await (const line of createInterface({ input: fixture.stdout })) if (line.startsWith('{')) return JSON.parse(line).url;
  throw new Error(`Catalog preview server failed: ${stderr}`);
}
async function digest(path) { return createHash('sha256').update(await readFile(path)).digest('hex'); }
async function request(base, path) { const result = await fetch(base + path); assert.equal(result.status, 200, `${path}: ${result.status}`); return result.json(); }

async function run() {
  await mkdir(EVIDENCE, { recursive: true });
  const files = ['_dev/cockpit/catalog.json', 'extraction/datalink.xlsx', 'extraction/mac-gray.xlsx'];
  const before = Object.fromEntries(await Promise.all(files.map(async file => [file, await digest(resolve(REPO, file))])));
  const base = await url();
  const session = await request(base, '/api/session');
  assert.equal(session.can_edit, false);
  const deals = await request(base, '/api/deals');
  assert.equal(deals.length, 9);
  assert.deepEqual(new Set(deals.map(deal => deal.slug)), new Set(['datalink', 'kraton', 'mac-gray', 'meredith', 'penford', 'petsmart', 'providence-worcester', 'stec', 'synacor']));
  const historiesBefore = Object.fromEntries(await Promise.all(['datalink', 'mac-gray'].map(async slug => [slug, await request(base, `/api/deal/${slug}/history`)])));
  const details = {};
  for (const slug of ['datalink', 'mac-gray']) {
    details[slug] = await request(base, `/api/deal/${slug}`);
    assert.equal(details[slug].workspace.editable, true); // version capability; read-only session still prevents edits
    assert.deepEqual(details[slug].versions.map(version => version.id), ['working', 'opus55-medium']);
    assert.equal(details[slug].workspace.base_version, 'opus55-medium');
    const immutable = await request(base, `/api/deal/${slug}?version=opus55-medium`);
    assert.equal(immutable.workspace.editable, false);
    files.push(`raw_filing/${details[slug].filing.file}`);
    before[`raw_filing/${details[slug].filing.file}`] = await digest(resolve(REPO, `raw_filing/${details[slug].filing.file}`));
  }

  browser = await playwright.chromium.launch({ headless: true, executablePath: '/opt/google/chrome/chrome', args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, reducedMotion: 'reduce' });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(base + '/', { waitUntil: 'networkidle', timeout: 90000 });
  await page.getByRole('heading', { name: 'Deal ledgers' }).waitFor();
  assert.equal(await page.locator('.deal-table tbody tr').count(), 9);
  await page.screenshot({ path: resolve(EVIDENCE, 'catalog-nine-overview.png'), fullPage: true });

  const pages = [];
  for (const slug of ['datalink', 'mac-gray']) {
    const deal = details[slug];
    const late = [...deal.ledger.rows].reverse().find(row => row.quote?.located);
    assert.ok(late);
    await page.goto(`${base}/deal/${slug}#row-${late.id}`, { waitUntil: 'networkidle', timeout: 90000 });
    await page.locator('.event-item.selected').waitFor({ timeout: 60000 });
    assert.equal(await page.locator('.event-item').count(), deal.ledger.rows.length);
    assert.ok((await page.locator('.deal-subline').innerText()).includes('Opus 5.5 medium extraction'));
    assert.equal(await page.getByRole('button', { name: 'Save changes' }).isDisabled(), true);
    await page.screenshot({ path: resolve(EVIDENCE, `catalog-${slug}-working.png`), fullPage: false });
    await page.getByRole('tab', { name: /^Review/ }).click();
    await page.getByRole('heading', { name: 'Review findings' }).waitFor();
    assert.equal(await page.locator('.finding').count(), deal.findings.length);
    await page.screenshot({ path: resolve(EVIDENCE, `catalog-${slug}-review.png`), fullPage: false });
    await page.getByRole('combobox', { name: 'Version' }).selectOption('opus55-medium');
    await page.getByText('Source version').waitFor();
    assert.equal(await page.getByRole('button', { name: 'Save changes' }).isDisabled(), true);
    await page.screenshot({ path: resolve(EVIDENCE, `catalog-${slug}-raw.png`), fullPage: false });
    pages.push({ slug, working_base: deal.workspace.base_version, working_rows: deal.ledger.rows.length, findings: deal.findings.length, versions: deal.versions.map(version => version.id), selected_late_row: late.id });
  }
  assert.equal(errors.length, 0, errors.join('; '));
  await context.close();
  for (const file of files) assert.equal(await digest(resolve(REPO, file)), before[file], `${file} changed during preview`);
  for (const slug of ['datalink', 'mac-gray']) assert.deepEqual(await request(base, `/api/deal/${slug}/history`), historiesBefore[slug], `${slug} history changed`);
  const outcome = { run_at: new Date().toISOString(), mode: 'actual catalog ephemeral localhost server; forced read-only session', nine_deals: deals.map(deal => deal.slug), pages, protected_sha256: before, browser_errors: errors, screenshots: ['catalog-nine-overview.png', ...pages.flatMap(item => [`catalog-${item.slug}-working.png`, `catalog-${item.slug}-review.png`, `catalog-${item.slug}-raw.png`])] };
  await writeFile(resolve(EVIDENCE, 'catalog-preview-results.json'), JSON.stringify(outcome, null, 2) + '\n');
  console.log(JSON.stringify({ passed: pages.length + 1, screenshots: outcome.screenshots }, null, 2));
}

try { await run(); }
catch (error) {
  await mkdir(EVIDENCE, { recursive: true });
  await writeFile(resolve(EVIDENCE, 'catalog-preview-results.json'), JSON.stringify({ run_at: new Date().toISOString(), error: error.stack || String(error), server_stderr: stderr }, null, 2) + '\n');
  console.error(error.stack || error);
  process.exitCode = 1;
} finally {
  if (browser) await browser.close().catch(() => {});
  fixture.kill('SIGTERM');
  await Promise.race([once(fixture, 'exit'), new Promise(resolve => setTimeout(resolve, 5000))]);
}
