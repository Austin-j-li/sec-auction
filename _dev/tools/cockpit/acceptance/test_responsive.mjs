/* Responsive cockpit acceptance with visible native scrollbars in private Chrome. */
/* Run: COCKPIT_TEST_DIST=/tmp/cockpit-responsive-final-dist node _dev/tools/cockpit/acceptance/test_responsive.mjs */
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { createInterface } from 'node:readline';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import playwright from '/home/uctpiaj/work/vm-browser/node_modules/playwright/index.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const repo = resolve(here, '../../../..');
const dist = resolve(process.env.COCKPIT_TEST_DIST || resolve(repo, '_dev/tools/cockpit/dist'));
const evidence = resolve(process.env.COCKPIT_RESPONSIVE_EVIDENCE || resolve(tmpdir(), 'cockpit-responsive-acceptance'));
const server = spawn('python3', [resolve(here, 'serve_fixture.py')], { cwd: repo, stdio: ['ignore', 'pipe', 'pipe'] });
let browser;
let stderr = '';
server.stderr.setEncoding('utf8');
server.stderr.on('data', value => { stderr += value; });

async function fixtureUrl() {
  for await (const line of createInterface({ input: server.stdout })) if (line.startsWith('{')) return JSON.parse(line).url;
  throw new Error('Fixture did not start: ' + stderr);
}
async function useStagedAssets(page) {
  await page.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (url.pathname.startsWith('/api/')) return route.continue();
    const asset = url.pathname.startsWith('/assets/') ? url.pathname.slice(1) : 'index.html';
    const type = asset.endsWith('.js') ? 'text/javascript' : asset.endsWith('.css') ? 'text/css' : asset.endsWith('.woff2') ? 'font/woff2' : 'text/html';
    try { return route.fulfill({ body: await readFile(resolve(dist, asset)), contentType: type }); }
    catch { return route.continue(); }
  });
}
async function geometry(page) {
  return page.evaluate(() => {
    const box = selector => document.querySelector(selector)?.getBoundingClientRect().toJSON();
    const tab = document.querySelector('.tabs');
    const editor = document.querySelector('.record-editor');
    const list = document.querySelector('.record-list');
    return {
      width: innerWidth, height: innerHeight, documentWidth: document.documentElement.scrollWidth,
      documentHeight: document.documentElement.scrollHeight,
      layout: document.querySelector('.ledger-layout')?.classList.contains('split-horizontal') ? 'compact' : 'columns',
      workspace: box('.workspace-column'), editor: box('.record-editor'), list: box('.record-list'),
      tabClient: tab?.clientWidth, tabScroll: tab?.scrollWidth,
      editorClient: editor?.clientWidth, editorScroll: editor?.scrollWidth, editorLeft: editor?.scrollLeft,
      dock: box('.save-dock'), selected: box('.event-item.selected'), location: box('.event-item.selected .quote-location'),
      exportButton: box('.export-button'), exportOptions: box('.export-options'),
      listScroll: document.querySelector('.event-list')?.getBoundingClientRect().toJSON()
    };
  });
}
async function setViewport(page, width, height = 800, expectLedger = true) {
  await page.setViewportSize({ width, height });
  await page.waitForFunction(({ width, expectLedger }) => {
    if (innerWidth !== width || !document.querySelector('.workspace-column')) return false;
    if (!expectLedger) return true;
    const root = document.querySelector('.ledger-layout');
    const list = root?.querySelector('.record-list');
    const compact = ![1440, 768].includes(width);
    if (!root || !list || root.classList.contains('split-horizontal') !== compact) return false;
    return Math.abs(list.getBoundingClientRect()[compact ? 'height' : 'width'] - parseFloat(getComputedStyle(root).getPropertyValue('--split-size'))) < 2;
  }, { width, expectLedger });
}
async function dragCorner(page, locator, dx, dy) {
  await locator.scrollIntoViewIfNeeded();
  const b = await locator.boundingBox();
  await page.mouse.move(b.x + b.width - 3, b.y + b.height - 3);
  await page.mouse.down();
  await page.mouse.move(b.x + b.width - 3 + dx, b.y + b.height - 3 + dy, { steps: 12 });
  await page.mouse.up();
}

async function run() {
  await mkdir(evidence, { recursive: true });
  const base = await fixtureUrl();
  browser = await playwright.chromium.launch({ headless: true, executablePath: '/opt/google/chrome/chrome', ignoreDefaultArgs: ['--hide-scrollbars'], args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const context = await browser.newContext({ viewport: { width: 1440, height: 800 }, reducedMotion: 'reduce' });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await useStagedAssets(page);
  await page.goto(base + '/deal/synthetic', { waitUntil: 'networkidle' });
  await page.locator('.event-item.selected').waitFor();
  const matrix = [];
  for (const width of [1440, 1280, 1024, 850, 768, 560, 390]) {
    await setViewport(page, width);
    const value = await geometry(page);
    matrix.push(value);
    assert.ok(value.documentWidth <= width + 2, `${width}px document fits: ${JSON.stringify(value)}`);
    assert.ok(value.editor.width >= 350, `${width}px editor remains readable: ${value.editor.width}`);
    assert.equal(value.layout, [1440, 768].includes(width) ? 'columns' : 'compact', `${width}px inner orientation`);
    const caretGap = value.exportOptions.left - value.exportButton.right;
    assert.ok(Math.abs(value.exportOptions.top - value.exportButton.top) < 2 && caretGap >= 0 && caretGap <= 16,
      `${width}px Excel options caret stays beside Export Excel: ${JSON.stringify({ button: value.exportButton, caret: value.exportOptions })}`);
    if (value.layout === 'compact' && value.location) {
      assert.ok(value.location.bottom <= value.listScroll.bottom - 8, `${width}px source badge clears list scrollbar: ${JSON.stringify({ location: value.location, listScroll: value.listScroll })}`);
    }
    if ([1440, 1024, 390].includes(width)) await page.screenshot({ path: resolve(evidence, `matrix-${width}.png`) });
  }

  await setViewport(page, 1440);
  await page.getByRole('tab', { name: /^History/ }).click();
  await setViewport(page, 390, 800, false);
  await page.waitForFunction(() => {
    const tab = document.querySelector('.tabs [aria-selected="true"]'), nav = document.querySelector('.tabs');
    return tab && nav && tab.getBoundingClientRect().right <= nav.getBoundingClientRect().right + 2;
  });
  const left = page.getByRole('button', { name: 'Scroll workspace tabs left' });
  const right = page.getByRole('button', { name: 'Scroll workspace tabs right' });
  assert.ok(await left.isEnabled(), 'left tab arrow shows when History is active at narrow width');
  for (let i = 0; i < 10 && await left.isEnabled(); i++) {
    await left.click({ timeout: 1500 }).catch(async error => { if (await left.isEnabled()) throw error; });
    await page.waitForTimeout(80);
  }
  assert.ok(await left.isDisabled(), 'tab arrows reach left edge');
  for (let i = 0; i < 10 && await right.isEnabled(); i++) {
    await right.click({ timeout: 1500 }).catch(async error => { if (await right.isEnabled()) throw error; });
    await page.waitForTimeout(80);
  }
  assert.ok(await right.isDisabled(), 'tab arrows reach right edge');
  await page.screenshot({ path: resolve(evidence, 'history-tabs-390.png') });
  await page.getByRole('tab', { name: /^Ledger/ }).click();

  await setViewport(page, 1024, 768);
  const note = page.locator('.record-editor').getByRole('textbox', { name: 'Note', exact: true });
  const initial = await note.inputValue();
  const field = page.locator('.record-editor .resizable-textarea').first();
  const before = await field.boundingBox();
  await dragCorner(page, field, 280, 90);
  const after = await field.boundingBox();
  let overflow = await geometry(page);
  assert.ok(after.width > before.width + 180 && after.height > before.height + 50, 'native textarea grows in both dimensions');
  assert.ok(overflow.editorScroll > overflow.editorClient + 180, 'widened textarea creates horizontal editor overflow');
  assert.equal(await note.inputValue(), initial, 'resizing does not edit field value');
  await page.screenshot({ path: resolve(evidence, 'native-horizontal-start-1024.png') });
  const scrollbar = await page.locator('.record-editor').boundingBox();
  const scrollbarY = scrollbar.y + scrollbar.height - 6;
  await page.mouse.move(scrollbar.x + 65, scrollbarY);
  await page.mouse.down();
  await page.mouse.move(scrollbar.x + 250, scrollbarY, { steps: 12 });
  await page.mouse.up();
  await page.waitForTimeout(100);
  overflow = await geometry(page);
  assert.ok(overflow.editorLeft > 80, `native scrollbar thumb drag advances horizontally: ${overflow.editorLeft}`);
  await page.screenshot({ path: resolve(evidence, 'native-horizontal-end-1024.png') });

  await setViewport(page, 1024, 600);
  await page.waitForTimeout(200);
  const short = await geometry(page);
  await page.screenshot({ path: resolve(evidence, 'short-before-dirty-1024.png') });
  assert.ok(short.documentHeight <= 600, `short laptop avoids body scroll: ${short.documentHeight}`);
  await note.fill(initial + ' short viewport draft');
  const dirty = await geometry(page);
  assert.ok(dirty.dock && dirty.dock.bottom <= 600 && dirty.dock.top >= 0, 'dirty save dock stays on screen');
  assert.ok(await page.getByRole('button', { name: 'Save changes' }).isEnabled(), 'dirty save action remains accessible');
  assert.ok(await note.inputValue() === initial + ' short viewport draft', 'draft survives short viewport reflow');
  await page.screenshot({ path: resolve(evidence, 'dirty-short-1024.png') });
  await setViewport(page, 390, 760);
  assert.equal(await note.inputValue(), initial + ' short viewport draft', 'draft survives narrow reflow');
  assert.equal(errors.length, 0, `browser errors: ${errors.join('; ')}`);
  const revision = await page.evaluate(async () => (await (await fetch('/api/deal/synthetic')).json()).workspace.revision);
  assert.equal(revision, 0, 'responsive interactions did not save deal data');
  await writeFile(resolve(evidence, 'results.json'), JSON.stringify({ passed: true, dist, matrix, browserErrors: errors }, null, 2) + '\n');
  console.log(JSON.stringify({ passed: true, dist, evidence, matrix: matrix.map(({ width, layout, editor }) => ({ width, layout, editorWidth: Math.round(editor.width) })), browserErrors: errors }, null, 2));
  await context.close();
}
try { await run(); }
catch (error) { console.error(error.stack || error); process.exitCode = 1; }
finally {
  if (browser) await browser.close().catch(() => {});
  server.kill('SIGTERM');
  await Promise.race([once(server, 'exit'), new Promise(resolve => setTimeout(resolve, 5000))]);
}
