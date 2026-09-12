#!/usr/bin/env node
// Console route-walk smoke test.
//
// Walks every tab of the web console in a real browser, in several orders, and
// asserts the page stays responsive AND that each route actually rendered its
// content. This exists because the two worst bugs on this project were invisible
// to the Python suite and to a plain page load:
//
//   * web/ror-positioning.js froze the page ~1s after load.
//   * web/multi-agent-desk.mjs froze it on navigating to the #desk tab.
//
// Both were MutationObserver callbacks that wrote into the subtree they observed
// without an idempotency guard or deferral. Neither reproduces unless the route is
// actually visited, so a load-only smoke test would have missed them. The Python
// guard tests in tests/test_web_page_guards.py pin the source pattern; this script
// proves the behaviour end to end.
//
// Usage:
//   python scripts/build_web.py            # build dist/ first
//   bash scripts/demo.sh                   # serve on :8765 (or any PORT)
//   node scripts/smoke_console.mjs http://127.0.0.1:8765
//
// Playwright is not a project dependency. The script looks for it in the usual
// places and SKIPS (exit 0) when it is unavailable, so it never breaks a run.
// Override the lookup with PLAYWRIGHT_PATH=/path/to/node_modules/playwright.

import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

// This file is ESM (.mjs), so bare `require` does not exist. Playwright is loaded
// by path at runtime, which needs the CJS loader.
const require = createRequire(import.meta.url);

const BASE = process.argv[2] || process.env.CONSOLE_URL || 'http://127.0.0.1:8765';

function loadPlaywright() {
  const candidates = [];
  if (process.env.PLAYWRIGHT_PATH) candidates.push(process.env.PLAYWRIGHT_PATH);
  candidates.push('playwright');
  // npx cache: ~/.npm/_npx/<hash>/node_modules/playwright
  try {
    const npxDir = path.join(process.env.HOME || '', '.npm', '_npx');
    for (const hash of fs.readdirSync(npxDir)) {
      candidates.push(path.join(npxDir, hash, 'node_modules', 'playwright'));
    }
  } catch (e) { /* no npx cache */ }
  for (const c of candidates) {
    try { return require(c); } catch (e) { /* try next */ }
  }
  return null;
}

const playwright = loadPlaywright();
if (!playwright) {
  console.log('SKIP: playwright not found.');
  console.log('  install once:  npm i -g playwright && npx playwright install chromium');
  console.log('  or point at a copy:  PLAYWRIGHT_PATH=/path/to/node_modules/playwright node scripts/smoke_console.mjs');
  process.exit(0);
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const ALL = ['overview', 'candidates', 'desks', 'scenarios', 'journal', 'resources', 'desk', 'about'];
// A marker element that must exist in #main once the route has fully rendered.
const MARKER = {
  overview: '.stats', candidates: '.notice', desks: '.cards', scenarios: '#scenario-rows',
  journal: '#note-form', resources: '.resource-page-root', desk: '.soul-card', about: '.about-card',
};

let browser = null;
const watchdog = setTimeout(() => {
  console.error('FAIL: console did not settle within 240s — the page is locked up.');
  try { if (browser) browser.close().catch(() => {}); } catch (e) {}
  process.exit(4);
}, 240000);
watchdog.unref && watchdog.unref();

async function probe(page) {
  try {
    return await Promise.race([
      page.evaluate(() => document.readyState),
      new Promise((_, rj) => setTimeout(() => rj(new Error('BLOCKED')), 6000)),
    ]);
  } catch (e) { return 'BLOCKED'; }
}

async function stackNow(page, client) {
  const paused = new Promise((res) => client.once('Debugger.paused', res));
  try { client.send('Debugger.pause').catch(() => {}); } catch (e) {}
  const ev = await Promise.race([
    paused, new Promise((_, rj) => setTimeout(() => rj(new Error('no-pause-event')), 12000)),
  ]).catch((e) => ({ error: e.message }));
  if (ev.error) return ['  (could not pause the debugger: ' + ev.error + ')'];
  const frames = (ev.callFrames || []).slice(0, 5).map(
    (f) => `  stack: ${f.functionName || '(anonymous)'} @ ${(f.url || '(inline)').split('/').pop()}:${f.location.lineNumber + 1}`);
  try { await client.send('Debugger.resume'); } catch (e) {}
  return frames;
}

(async () => {
  console.log(`console smoke test -> ${BASE}`);
  browser = await playwright.chromium.launch({ args: ['--disable-dev-shm-usage', '--no-sandbox'] });
  const page = await browser.newPage();
  const client = await page.context().newCDPSession(page);
  await client.send('Debugger.enable');

  await page.goto(BASE + '/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await sleep(2500);
  const initial = await probe(page);
  console.log(`  load: responsive=${initial}`);
  if (initial === 'BLOCKED') {
    console.error('FAIL: the console froze while loading.');
    process.exit(1);
  }

  const walks = [
    ['forward', ALL],
    ['reverse', [...ALL].reverse()],
    ['toggle x3', ['journal', 'resources', 'desk', 'about', 'journal', 'resources', 'desk', 'about', 'desk', 'journal', 'about', 'resources']],
  ];

  let steps = 0, misses = 0;
  for (const [label, routes] of walks) {
    console.log(`  walk: ${label}`);
    for (const route of routes) {
      steps++;
      try { await page.click(`[data-nav="${route}"]`, { timeout: 5000 }); }
      catch (e) { console.log(`    ${route}: click failed (${e.message.split('\n')[0].slice(0, 70)})`); }
      await sleep(1500);
      const state = await probe(page);
      if (state === 'BLOCKED') {
        console.error(`    ${route}: *** FROZEN ***`);
        for (const f of await stackNow(page, client)) console.error(f);
        console.error('FAIL: the console locked its main thread.');
        clearTimeout(watchdog);
        try { await browser.close(); } catch (e) {}
        process.exit(1);
      }
      const marker = await page.evaluate((s) => !!document.querySelector(s), MARKER[route]).catch(() => false);
      if (!marker) misses++;
      console.log(`    ${route}: responsive=${state} content=${marker ? 'ok' : 'MISSING'}`);
    }
  }

  clearTimeout(watchdog);
  try { await browser.close(); } catch (e) {}
  if (misses) {
    console.error(`FAIL: ${misses} route(s) did not render their content.`);
    process.exit(2);
  }
  console.log(`PASS: ${steps} route visits, all responsive with content.`);
})().catch((e) => { console.error('FAILED: ' + e.message); process.exit(3); });
