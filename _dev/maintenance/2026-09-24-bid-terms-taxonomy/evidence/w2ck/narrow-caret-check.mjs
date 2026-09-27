// Quick headless check: the Excel options caret stays beside Export Excel at every width.
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import playwright from '/home/uctpiaj/work/vm-browser/node_modules/playwright/index.mjs';

const repo = '/home/uctpiaj/work/tmp/v114-scratch/pkg/w2ck';
const dist = process.env.DIST;
const out = process.env.OUT;
const server = spawn('python3', [resolve(repo, '_dev/tools/cockpit/acceptance/serve_fixture.py')], { cwd: repo, stdio: ['ignore', 'pipe', 'inherit'] });
let base;
for await (const line of createInterface({ input: server.stdout })) if (line.startsWith('{')) { base = JSON.parse(line).url; break; }
const browser = await playwright.chromium.launch({ headless: true, executablePath: '/opt/google/chrome/chrome', args: ['--no-sandbox', '--disable-dev-shm-usage'] });
const results = [];
try {
  const page = await browser.newPage();
  await page.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (url.pathname.startsWith('/api/')) return route.continue();
    const asset = url.pathname.startsWith('/assets/') ? url.pathname.slice(1) : 'index.html';
    const type = asset.endsWith('.js') ? 'text/javascript' : asset.endsWith('.css') ? 'text/css' : asset.endsWith('.woff2') ? 'font/woff2' : 'text/html';
    try { return route.fulfill({ body: await readFile(resolve(dist, asset)), contentType: type }); } catch { return route.continue(); }
  });
  for (const view of ['working', 'v1132-raw']) {
    await page.setViewportSize({ width: 1440, height: 800 });
    await page.goto(`${base}/deal/synthetic`, { waitUntil: 'networkidle' });
    await page.waitForSelector('.export-options');
    if (view !== 'working') {
      await page.locator('select[aria-label="Version"]').selectOption(view);
      await page.waitForTimeout(1000);
    }
    for (const width of [1600, 1440, 1300, 1200, 1150, 1100, 1024, 950, 900, 850, 821, 820, 768, 700, 600, 560, 480, 420, 390, 360, 320]) {
      await page.setViewportSize({ width, height: 800 });
      await page.waitForTimeout(150);
      const g = await page.evaluate(() => {
        const box = s => document.querySelector(s)?.getBoundingClientRect().toJSON();
        return { exp: box('.export-button'), caret: box('.export-options'), save: box('.save-button'), doc: document.documentElement.scrollWidth };
      });
      const sameLine = Math.abs(g.caret.top - g.exp.top) < 2;
      const adjacent = g.caret.left >= g.exp.right && g.caret.left - g.exp.right <= 8;
      const saveAfter = !(Math.abs(g.save.top - g.caret.top) < 2 && g.save.right <= g.caret.left);
      results.push({ view, width, sameLine, adjacent, gap: Math.round(g.caret.left - g.exp.right), saveAfter, overflow: g.doc > width });
      if ([1440, 1100, 900, 820, 560, 390, 320].includes(width)) await page.locator('.deal-toolbar').screenshot({ path: resolve(out, `toolbar-${view}-${width}.png`) });
    }
  }
} finally {
  await browser.close();
  server.kill('SIGTERM');
}
console.log(JSON.stringify(results));
const bad = results.filter(r => !r.sameLine || !r.adjacent || !r.saveAfter);
console.log(bad.length ? `FAIL ${JSON.stringify(bad)}` : `OK ${results.length} widths`);
assert.equal(bad.length, 0);
