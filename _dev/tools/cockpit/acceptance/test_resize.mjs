/* Isolated real-mouse acceptance for browser-only cockpit resizing. */
/* Run from repo root: COCKPIT_TEST_DIST=/tmp/cockpit-resize-dist node _dev/tools/cockpit/acceptance/test_resize.mjs */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { createInterface } from 'node:readline';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import playwright from '/home/uctpiaj/work/vm-browser/node_modules/playwright/index.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const repo = resolve(here, '../../../..');
const dist = resolve(process.env.COCKPIT_TEST_DIST || resolve(repo, '_dev/tools/cockpit/dist'));
const evidence = resolve(process.env.COCKPIT_RESIZE_EVIDENCE || '/tmp/cockpit-resize-acceptance');
const server = spawn('python3', [resolve(here, 'serve_fixture.py')], { cwd: repo, stdio: ['ignore', 'pipe', 'pipe'] });
let stderr = '';
server.stderr.setEncoding('utf8');
server.stderr.on('data', chunk => { stderr += chunk; });
let browser;

async function fixtureUrl() {
  for await (const line of createInterface({ input: server.stdout })) if (line.startsWith('{')) return JSON.parse(line).url;
  throw new Error(`Fixture did not start: ${stderr}`);
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

async function width(locator) { return (await locator.boundingBox()).width; }
async function height(locator) { return (await locator.boundingBox()).height; }

async function drag(page, locator, dx, dy, corner = false) {
  await locator.scrollIntoViewIfNeeded();
  const box = await locator.boundingBox();
  assert.ok(box, 'drag target is visible');
  const x = corner ? box.x + box.width - 3 : box.x + box.width / 2;
  const y = corner ? box.y + box.height - 3 : box.y + box.height / 2;
  await page.mouse.move(x, y);
  await page.mouse.down();
  await page.mouse.move(x + dx, y + dy, { steps: 8 });
  await page.mouse.up();
  await page.waitForTimeout(80);
}

async function noDocumentOverflow(page) {
  const value = await page.evaluate(() => ({ viewport: innerWidth, scroll: document.documentElement.scrollWidth, geometry: Object.fromEntries(['.workbench','.filing-column','.workbench>.split-handle','.workspace-column','.tabs','.workspace-scroll'].map(name => { const el=document.querySelector(name), box=el?.getBoundingClientRect(); return [name,box&&{x:box.x,width:box.width,right:box.right,grid:getComputedStyle(el).gridTemplateColumns}]; })), offenders: [...document.querySelectorAll('*')].filter(el => el.getBoundingClientRect().right > innerWidth + 2).slice(0, 8).map(el => ({ tag: el.tagName, className: typeof el.className === 'string' ? el.className : '', right: el.getBoundingClientRect().right })) }));
  assert.ok(value.scroll <= value.viewport + 2, `document overflow: ${JSON.stringify(value)}`);
}

async function withinX(control, pane, label) {
  const item = await control.boundingBox(), owner = await pane.boundingBox();
  assert.ok(item && owner && item.x >= owner.x - 2 && item.x + item.width <= owner.x + owner.width + 2, `${label}: ${JSON.stringify({ item, owner })}`);
}

async function quoteVisible(page, label) {
  const bounds = await page.evaluate(() => {
    const scroll = document.querySelector('.filing-scroll'), mark = document.querySelector('mark.selected');
    return scroll && mark ? { scroll: scroll.getBoundingClientRect().toJSON(), mark: mark.getBoundingClientRect().toJSON() } : null;
  });
  assert.ok(bounds && bounds.mark.top >= bounds.scroll.top - 2 && bounds.mark.bottom <= bounds.scroll.bottom + 2, `${label}: selected quote is outside filing pane: ${JSON.stringify(bounds)}`);
}

async function run() {
  await mkdir(evidence, { recursive: true });
  const base = await fixtureUrl();
  browser = await playwright.chromium.launch({ headless: true, executablePath: '/opt/google/chrome/chrome', ignoreDefaultArgs: ['--hide-scrollbars'], args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, reducedMotion: 'reduce' });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await useStagedAssets(page);
  await page.goto(base + '/deal/synthetic', { waitUntil: 'networkidle' });
  await page.locator('.event-item.selected').waitFor();
  await quoteVisible(page, 'initial load');
  const main = page.locator('.workbench > .split-handle');
  const nested = page.locator('.ledger-layout > .split-handle');
  const originalFiling = await width(page.locator('.filing-column'));
  const originalList = await width(page.locator('.record-list'));
  await page.screenshot({ path: resolve(evidence, 'desktop-before.png') });
  await drag(page, main, 110, 0);
  assert.ok(await width(page.locator('.filing-column')) > originalFiling + 80, 'filing pane grows by mouse drag');
  await page.waitForFunction(() => document.querySelector('.ledger-layout')?.classList.contains('split-horizontal'));
  await drag(page, main, -190, 0);
  await page.waitForFunction(() => document.querySelector('.ledger-layout')?.classList.contains('split-vertical'));
  await drag(page, nested, 60, 0);
  assert.ok(await width(page.locator('.record-list')) > originalList + 40, 'event list grows by mouse drag');

  const selectedBefore = await page.locator('.event-item.selected').innerText();
  await nested.focus();
  await page.keyboard.press('ArrowRight');
  await page.waitForTimeout(80);
  assert.ok(await width(page.locator('.record-list')) > originalList + 50, 'separator responds to arrow key');
  assert.equal(await page.locator('.event-item.selected').innerText(), selectedBefore, 'separator key does not change selected event');
  await page.keyboard.press('Home');
  await page.waitForTimeout(80);
  assert.ok(await width(page.locator('.record-list')) < originalList, 'Home moves separator to minimum');
  await page.keyboard.press('End');
  await page.waitForTimeout(80);
  assert.ok(await width(page.locator('.record-list')) > originalList, 'End moves separator to maximum');
  await nested.dblclick();
  await page.waitForTimeout(80);
  assert.ok(Math.abs(await width(page.locator('.record-list')) - originalList) < 3, 'double-click resets list width');
  await drag(page, nested, 50, 0);

  const area = page.locator('.record-editor .resizable-textarea').first();
  const textBefore = await area.locator('textarea').inputValue();
  const areaWidth = await width(area), areaHeight = await height(area);
  await drag(page, area, -85, 75, true);
  assert.ok(await width(area) < areaWidth - 35, 'text box shrinks in width by corner drag');
  assert.ok(await height(area) > areaHeight + 35, 'text box grows in height by corner drag');
  await drag(page, area, 40, -30, true);
  assert.ok(await width(area) > areaWidth - 70, 'text box grows back in width');
  await drag(page, area, 0, 240, true);
  assert.ok(await height(area) > 260, 'text box grows beyond Fluent default height cap');
  assert.equal(await area.locator('textarea').inputValue(), textBefore, 'resizing preserves text');
  await page.screenshot({ path: resolve(evidence, 'desktop-after.png') });

  const savedFiling = await width(page.locator('.filing-column'));
  const savedList = await width(page.locator('.record-list'));
  await page.reload({ waitUntil: 'networkidle' });
  await page.locator('.event-item.selected').waitFor();
  await quoteVisible(page, 'reload');
  assert.ok(Math.abs(await width(page.locator('.filing-column')) - savedFiling) < 3, 'filing width survives reload');
  assert.ok(Math.abs(await width(page.locator('.record-list')) - savedList) < 3, 'list width survives reload');
  assert.equal(await page.getByText('No unsaved edits').count(), 1, 'resizing has no draft changes');
  const revision = await page.evaluate(async () => (await (await fetch('/api/deal/synthetic')).json()).workspace.revision);
  assert.equal(revision, 0, 'resizing did not save deal data');

  for (const label of ['Rounds', 'Questions', 'Deal facts']) {
    await page.getByRole('tab', { name: new RegExp(`^${label}`) }).click();
    await page.locator('.other-sheet > .section-head h2').getByText(label, { exact: true }).waitFor();
    await page.waitForFunction(() => {
      const panel = document.querySelector('.sheet-body');
      const list = panel?.querySelector('.sheet-list');
      return panel && list && Math.abs(list.getBoundingClientRect().width - parseFloat(getComputedStyle(panel).getPropertyValue('--split-size'))) < 2;
    });
    const list = page.locator('.sheet-list');
    const previous = await width(list);
    await drag(page, page.locator('.sheet-body > .split-handle'), 45, 0);
    assert.ok(await width(list) > previous + 25, `${label} list grows by mouse drag`);
  }
  await page.getByRole('tab', { name: /^Review/ }).click();
  await page.locator('.finding-title').first().click();
  const findingComment = page.locator('.finding-body .comments .resizable-textarea').first();
  const findingHeight = await height(findingComment);
  await drag(page, findingComment, -35, 60, true);
  assert.ok(await height(findingComment) > findingHeight + 25, 'finding comment box resizes');
  await page.getByRole('tab', { name: /^Ledger/ }).click();
  const rowComment = page.locator('.comments .resizable-textarea').first();
  const rowHeight = await height(rowComment);
  await drag(page, rowComment, -35, 60, true);
  assert.ok(await height(rowComment) > rowHeight + 25, 'event comment box resizes');

  await main.focus();
  await page.keyboard.press('Home');
  await page.waitForTimeout(80);
  await withinX(page.getByRole('textbox', { name: 'Search filing' }), page.locator('.filing-column'), 'search at minimum filing width');
  await withinX(page.getByRole('button', { name: 'Go', exact: true }), page.locator('.filing-column'), 'page jump at minimum filing width');
  await page.keyboard.press('End');
  await page.waitForTimeout(80);
  await withinX(page.locator('.record-editor').getByRole('textbox', { name: 'When', exact: true }), page.locator('.record-editor'), 'editor input at minimum workspace width');
  await withinX(page.locator('.record-list .section-head').getByRole('button', { name: 'Add' }), page.locator('.record-list'), 'Add at minimum event-list width');
  await page.getByRole('tab', { name: /^Review/ }).click();
  if (!await page.getByRole('combobox', { name: 'Finding judgment' }).isVisible()) await page.locator('.finding-title').first().click();
  await withinX(page.getByRole('combobox', { name: 'Finding judgment' }), page.locator('.workspace-column'), 'review decision control at minimum workspace width');
  await page.getByRole('tab', { name: /^Ledger/ }).click();
  await noDocumentOverflow(page);

  await page.setViewportSize({ width: 850, height: 800 });
  await page.waitForFunction(() => document.querySelector('.workspace-column')?.getBoundingClientRect().width >= 398);
  await noDocumentOverflow(page);
  assert.ok(await width(page.locator('.workspace-column')) >= 398, 'workspace retains usable minimum width');
  await page.screenshot({ path: resolve(evidence, 'narrow-desktop.png') });
  await page.reload({ waitUntil: 'networkidle' });
  await page.locator('.event-item.selected').waitFor();
  assert.ok(await width(page.locator('.workspace-column')) >= 398, 'saved large filing width clamps on narrow-desktop reload');
  await quoteVisible(page, 'narrow-desktop reload');
  await noDocumentOverflow(page);
  await page.setViewportSize({ width: 390, height: 850 });
  await page.locator('.ledger-layout > .split-handle').waitFor();
  await page.waitForFunction(() => document.querySelector('.ledger-layout')?.classList.contains('split-horizontal'));
  const listHeight = await height(page.locator('.record-list'));
  const itemHeight = await height(page.locator('.event-item').first());
  await drag(page, page.locator('.ledger-layout > .split-handle'), 0, 70);
  assert.ok(await height(page.locator('.record-list')) > listHeight + 40, 'mobile list grows in height');
  assert.ok(await height(page.locator('.event-item').first()) > itemHeight + 40, 'mobile list cards follow height');
  await page.locator('.ledger-layout > .split-handle').focus();
  const beforeKeyHeight = await height(page.locator('.record-list'));
  const beforeKeySelection = await page.locator('.event-item.selected').innerText();
  await page.keyboard.press('ArrowDown');
  await page.waitForTimeout(80);
  assert.ok(await height(page.locator('.record-list')) > beforeKeyHeight + 5, 'mobile separator responds to ArrowDown');
  assert.equal(await page.locator('.event-item.selected').innerText(), beforeKeySelection, 'mobile separator ArrowDown does not change event');
  await noDocumentOverflow(page);
  await page.screenshot({ path: resolve(evidence, 'mobile-after.png') });
  await page.reload({ waitUntil: 'networkidle' });
  assert.ok(await height(page.locator('.record-list')) > listHeight + 40, 'mobile height survives reload');
  await page.getByRole('combobox', { name: 'Version' }).selectOption({ index: 1 });
  await page.getByText('Read only version').waitFor();
  assert.ok(await page.locator('.ledger-layout > .split-handle').isVisible(), 'splitter works on read-only source version');
  const readonlyArea = page.locator('.record-editor .resizable-textarea').first();
  const readonlyWidth = await width(readonlyArea), readonlyHeight = await height(readonlyArea);
  await drag(page, readonlyArea, -35, 50, true);
  assert.ok(await width(readonlyArea) < readonlyWidth - 15 && await height(readonlyArea) > readonlyHeight + 20, 'read-only text box resizes in both dimensions');
  assert.equal(errors.length, 0, `browser errors: ${errors.join('; ')}`);
  await writeFile(resolve(evidence, 'results.json'), JSON.stringify({ passed: true, dist, screenshots: ['desktop-before.png', 'desktop-after.png', 'narrow-desktop.png', 'mobile-after.png'], browserErrors: errors }, null, 2) + '\n');
  console.log(JSON.stringify({ passed: true, dist, evidence, browserErrors: errors }, null, 2));
  await context.close();
}

try { await run(); }
catch (error) { console.error(error.stack || error); process.exitCode = 1; }
finally {
  if (browser) await browser.close().catch(() => {});
  server.kill('SIGTERM');
  await Promise.race([once(server, 'exit'), new Promise(resolve => setTimeout(resolve, 5000))]);
}
