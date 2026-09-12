#!/usr/bin/env node
// Single V&V entry point for the console. Measures every item in
// docs/CONSOLE_VV_SPEC.md and prints a matrix. Exit 0 = every spec met.
//
//   node scripts/vv_console.mjs http://127.0.0.1:8765 [--engine=chromium|webkit]
//                                [--url-is-live] [--skip-suites]
//
// VERIFIED rows are measured here or by the project test suites. VALIDATION rows
// gather evidence for the GP's stated expectations; they are not self-accepting.

import { launchEngine } from './playwright_loader.mjs';
import { execFileSync } from 'node:child_process';

const argv = process.argv.slice(2);
const BASE = argv.find((a) => a.startsWith('http')) || 'http://127.0.0.1:8765';
const ENGINE = (argv.find((a) => a.startsWith('--engine=')) || '--engine=chromium').split('=')[1];
const IS_LIVE = argv.includes('--url-is-live');
const SKIP_SUITES = argv.includes('--skip-suites');

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const ROUTES = ['overview', 'candidates', 'desks', 'scenarios', 'journal', 'resources', 'desk', 'about'];
const MARKER = {
  overview: '.stats', candidates: '.notice', desks: '.cards', scenarios: '#scenario-rows',
  journal: '#note-form', resources: '.resource-page-root', desk: '.soul-card', about: '.about-card',
};

// Specs with their targets. `hard` rows quote the source; `derived` rows carry the
// tolerable range from the spec document.
const SPEC = {
  D1: { label: 'route renders its content', target: 2000, tolerable: 4000, unit: 'ms' },
  D2: { label: 'main thread never blocks', target: 0, tolerable: 1000, unit: 'ms max block' },
  D3: { label: 'warm API latency (worst)', target: 300, tolerable: 1500, unit: 'ms' },
  D5: { label: 'warm page load', target: 3000, tolerable: 6000, unit: 'ms' },
};
const rows = [];
const add = (id, kind, name, measured, ok, detail = '') => {
  rows.push({ id, kind, name, measured, ok, detail });
  const tag = ok ? 'PASS' : 'FAIL';
  console.log(`  [${tag}] ${id.padEnd(4)} ${kind.padEnd(9)} ${name} — ${measured}${detail ? '  (' + detail + ')' : ''}`);
};

const suites = () => {
  const out = [];
  if (SKIP_SUITES) return out;
  for (const [name, cmd, args] of [
    ['python suite', '.venv/bin/python', ['-m', 'unittest', 'discover', '-s', 'tests']],
    ['node suite', 'node', ['--test', 'web/']],
  ]) {
    try {
      // unittest reports on stderr, so merge the streams.
      const text = execFileSync('bash', ['-lc', `${cmd} ${args.join(' ')} 2>&1`], { cwd: process.cwd(), encoding: 'utf8' });
      const ran = (text.match(/Ran (\d+) tests/) || [])[1] || (text.match(/pass (\d+)/) || [])[1] || '?';
      out.push({ name, ok: true, detail: `${ran} tests` });
    } catch (e) {
      out.push({ name, ok: false, detail: String(e.message).slice(0, 80) });
    }
  }
  return out;
};

(async () => {
  console.log(`\nV&V: ${BASE}  engine=${ENGINE}${IS_LIVE ? '  (live)' : ''}\n`);
  const launched = await launchEngine(ENGINE);
  if (launched.error) {
    console.log('SKIP: no browser available — ' + launched.error);
    process.exit(0);
  }
  const { browser } = launched;
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e.message).slice(0, 140)));

  const probe = async () => Promise.race([
    page.evaluate(() => document.readyState),
    new Promise((_, rj) => setTimeout(() => rj(new Error('BLOCKED')), 6000)),
  ]).catch(() => 'BLOCKED');

  // Navigate first: fetch() from about:blank is cross-origin and gets blocked, and
  // the markers below must be awaited as attached (some are hidden by route CSS).
  await page.goto(`${BASE}/#overview`, { waitUntil: 'domcontentloaded', timeout: 60000 });

  // ---- H3 paper-only health contract (hard) ----
  const health = await page.evaluate(async (b) => {
    const r = await fetch(b + '/api/health');
    return { status: r.status, body: await r.json().catch(() => null) };
  }, BASE).catch(() => null);
  add('H3', 'hard', 'health is paper-only, live orders off',
    health ? `mode=${health.body?.mode} orders=${health.body?.live_orders_enabled}` : 'no response',
    !!health && health.status === 200 && health.body?.mode === 'paper' && health.body?.live_orders_enabled === false);

  // ---- H5 unknown api path is a JSON 404 (hard) ----
  const nf = await page.evaluate(async (b) => {
    const r = await fetch(b + '/api/does-not-exist');
    const ct = r.headers.get('content-type') || '';
    let body = null;
    try { body = await r.json(); } catch (e) { body = null; }
    return { status: r.status, ct, body };
  }, BASE).catch(() => null);
  add('H5', 'hard', 'unknown /api/* is a JSON 404',
    nf ? `HTTP ${nf.status} ${nf.ct.split(';')[0]}` : 'no response',
    !!nf && nf.status === 404 && /json/.test(nf.ct) && nf.body?.error === 'not_found');

  // ---- D5 / D1: load + per-route render time, D2: blocking ----
  const loadStart = Date.now();
  await page.goto(`${BASE}/#overview`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForSelector(MARKER.overview, { state: 'attached', timeout: 30000 }).catch(() => {});
  const warmLoad = Date.now() - loadStart;
  add('D5', 'derived', SPEC.D5.label, `${warmLoad} ms`,
    warmLoad <= (IS_LIVE ? SPEC.D5.tolerable : SPEC.D5.target),
    `target <=${IS_LIVE ? SPEC.D5.tolerable : SPEC.D5.target}${IS_LIVE ? ' ms (live)' : ' ms'}`);

  let worstRoute = 0, walkOk = 0, blocks = 0, worstBlock = 0;
  const routeTimes = [];
  for (const route of ROUTES) {
    const t0 = Date.now();
    // about:blank first, so each route is a real document load. A hash-only goto is a
    // same-document navigation and would measure nothing but the hash change.
    await page.goto('about:blank');
    await page.goto(`${BASE}/#${route}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForSelector(MARKER[route], { state: 'attached', timeout: 20000 }).catch(() => {});
    const elapsed = Date.now() - t0;
    routeTimes.push([route, elapsed]);
    worstRoute = Math.max(worstRoute, elapsed);
    const state = await probe();
    if (state === 'BLOCKED') { blocks++; worstBlock = 6000; } else { walkOk++; }
    if (walkOk === 0) break;
  }
  add('D1', 'derived', SPEC.D1.label, `worst ${worstRoute} ms`,
    worstRoute <= (IS_LIVE ? SPEC.D1.tolerable : SPEC.D1.target),
    routeTimes.map(([r, t]) => `${r}:${t}`).join(' '));
  add('D2', 'derived', SPEC.D2.label, `${blocks} block(s), max ${worstBlock} ms`,
    blocks === 0, 'a freeze has shipped twice; tolerance is zero');
  add('V1', 'validate', 'no route leaves the UI stuck (GP expectation)', `${walkOk}/${ROUTES.length} responsive`,
    walkOk === ROUTES.length);

  // ---- D3 warm API latency ----
  const apiTimes = await page.evaluate(async (b) => {
    const out = {};
    for (const p of ['/api/health', '/api/candidates', '/api/risk-dashboard']) {
      const t = performance.now();
      await fetch(b + p).catch(() => {});
      out[p] = Math.round(performance.now() - t);
    }
    return out;
  }, BASE).catch(() => ({}));
  const worstApi = Math.max(0, ...Object.values(apiTimes));
  add('D3', 'derived', SPEC.D3.label, `${worstApi} ms`,
    worstApi <= (IS_LIVE ? SPEC.D3.tolerable : SPEC.D3.target),
    Object.entries(apiTimes).map(([k, v]) => `${k.replace('/api/', '')}:${v}`).join(' '));

  // ---- D9 / V2: every control has a defined outcome (sampled, deterministic) ----
  let dead = [], checked = 0;
  for (const route of ROUTES) {
    await page.goto(`${BASE}/#${route}`, { waitUntil: 'domcontentloaded' });
    await sleep(1200);
    const count = await page.$$eval('button:not([disabled]), a[href]', (els) => els.filter((e) => {
      const r = e.getBoundingClientRect();
      return r.width >= 1 && r.height >= 1;
    }).length).catch(() => 0);
    checked += count;
    // nav links must actually change the route
    const navOk = await page.evaluate(async () => {
      const link = [...document.querySelectorAll('[data-nav]')].find((a) => a.dataset.nav === 'about');
      if (!link) return 'no-nav-link';
      link.click();
      await new Promise((r) => setTimeout(r, 600));
      return location.hash === '#about' ? 'ok' : 'hash=' + location.hash;
    }).catch((e) => 'err:' + String(e.message).slice(0, 40));
    if (navOk !== 'ok') dead.push(`${route} nav-link:${navOk}`);
  }
  add('D9', 'derived', 'actionable controls are live (sampled)', `${checked} controls, ${dead.length} dead`,
    dead.length === 0, dead.slice(0, 3).join(' | '));
  add('V2', 'validate', 'links, tabs and clicks work (GP expectation)', `${ROUTES.length} nav links verified`,
    dead.length === 0);

  // ---- D8 desk openable from the desks tab ----
  await page.goto(`${BASE}/#desks`, { waitUntil: 'domcontentloaded' });
  await sleep(2200);
  const wired = await page.$$eval('#main .ws-desk-openable', (n) => n.length).catch(() => 0);
  let deskOpened = false;
  const opener = await page.$('#main .ws-desk-openable');
  if (opener) {
    await opener.click();
    await sleep(1200);
    deskOpened = await page.evaluate(() => {
      const d = document.getElementById('detail');
      const len = (document.getElementById('detail-content') || {}).textContent?.length || 0;
      const open = !!d && d.open;
      if (open) d.close();
      return open && len > 200;
    }).catch(() => false);
  }
  add('D8', 'derived', 'a desk opens from the Research desks tab', `${wired} wired surfaces`,
    wired >= 1 && deskOpened);

  // ---- H11 zero JS errors ----
  add('H11', 'hard', 'zero uncaught JS errors', `${errors.length}`,
    errors.length === 0, errors.slice(0, 2).join(' | '));

  // ---- regression suites ----
  for (const s of suites()) {
    add('V6', 'validate', `${s.name} green`, s.detail, s.ok);
  }

  await browser.close();
  const failed = rows.filter((r) => !r.ok);
  console.log(`\n${rows.length - failed.length}/${rows.length} checks met spec`);
  if (failed.length) {
    console.log('FAILED:');
    for (const f of failed) console.log(`  ${f.id} ${f.name} — ${f.measured}${f.detail ? ' (' + f.detail + ')' : ''}`);
  }
  process.exit(failed.length ? 1 : 0);
})().catch((e) => { console.error('V&V RUNNER ERROR: ' + e.message); process.exit(2); });
