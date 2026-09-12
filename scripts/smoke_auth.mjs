#!/usr/bin/env node
// Auth lifecycle smoke test (local/demo use).
//
// Drives sign-in, subscribe, broker status, and logout through the real UI, plus
// browser back/forward across routes and a small-viewport pass. The route walk in
// smoke_console.mjs covers rendering; this covers the session lifecycle it cannot
// reach, because reading the OTP requires the server log.
//
// Usage:
//   bash scripts/demo.sh > /tmp/demo.log 2>&1 &     # codes print to that log
//   node scripts/smoke_auth.mjs http://127.0.0.1:8765 /tmp/demo.log [email]
//
// Playwright is not a project dependency; SKIPs (exit 0) when it is unavailable.

import fs from 'node:fs';

import { loadPlaywright, launchEngine } from './playwright_loader.mjs';

const BASE = process.argv[2] || 'http://127.0.0.1:8765';
const LOG = process.argv[3] || '/tmp/demo.log';
const EMAIL = process.argv[4] || 'lifecycle-check@example.com';

const playwright = loadPlaywright();
if (!playwright) {
  console.log('SKIP: playwright not found (see scripts/smoke_console.mjs header).');
  process.exit(0);
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const results = [];
const rec = (name, ok, detail = '') => {
  results.push({ name, ok, detail });
  console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? '  — ' + detail : ''}`);
};

function otpFor(email) {
  // The dev transport prints: [membership-mail] TO=<email> ... code is:\n\n<code>
  const text = fs.readFileSync(LOG, 'utf8');
  const esc = email.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const all = [...text.matchAll(new RegExp(`\\[membership-mail\\] TO=${esc}[\\s\\S]*?code is:\\s*\\n+\\s*(\\S+)`, 'g'))];
  return all.length ? all[all.length - 1][1] : null;
}

async function api(page, url) {
  return page.evaluate(async (u) => {
    const r = await fetch(u, { headers: { accept: 'application/json' } });
    let body = null;
    try { body = await r.json(); } catch (e) { body = null; }
    return { status: r.status, body };
  }, url);
}

async function signIn(page, email) {
  await page.evaluate(() => {
    const m = document.getElementById('acct-modal');
    if (m && m.open) m.close();
    document.getElementById('acct-btn').click();
  });
  await page.waitForSelector('#acct-modal[open]', { timeout: 8000 });
  await page.fill('#acct-email', email);
  await page.click('#acct-send');
  let code = null;
  for (let i = 0; i < 40 && !code; i++) { await sleep(250); code = otpFor(email); }
  if (!code) throw new Error('no OTP captured for ' + email + ' (is the server logging to ' + LOG + '?)');
  await page.fill('#acct-code', code);
  await page.click('#acct-verify');
  await sleep(1500);
}

(async () => {
  const launched = await launchEngine('chromium');
  if (launched.error) { console.log('SKIP: no browser available — ' + launched.error); process.exit(0); }
  const browser = launched.browser;
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e.message).slice(0, 160)));

  await page.goto(`${BASE}/#overview`, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await sleep(2500);

  // --- guest sign-in ---
  await signIn(page, EMAIL);
  let me = await api(page, '/api/auth/me');
  rec('guest sign-in creates an authenticated session', me.body?.authenticated === true, `role=${me.body?.role}`);
  let tier = await api(page, '/api/tier');
  rec('guest tier is synthetic', tier.body?.tier === 'synthetic' && tier.body?.real_data === false, `tier=${tier.body?.tier}`);

  // --- real data is gated for a guest ---
  const real = await api(page, '/api/data/real');
  rec('guest is denied real data', real.status === 403, `HTTP ${real.status}`);

  // --- subscribe -> member ---
  await page.evaluate(() => {
    const m = document.getElementById('acct-modal');
    if (!m.open) document.getElementById('acct-btn').click();
  });
  await sleep(600);
  const subBtn = await page.$('#acct-subscribe');
  await subBtn.click();
  await sleep(1500);
  tier = await api(page, '/api/tier');
  me = await api(page, '/api/auth/me');
  rec('subscribe upgrades the session to MEMBER', me.body?.role === 'MEMBER', `role=${me.body?.role}`);
  rec('member gains real-data entitlement', tier.body?.real_data === true, `tier=${tier.body?.tier}`);

  // --- broker status degrades cleanly when unconfigured ---
  const broker = await api(page, '/api/broker/status');
  rec('broker status answers without error', broker.status === 200 && broker.body?.configured === false,
    `configured=${broker.body?.configured} linked=${broker.body?.linked}`);

  // --- GP console for the GP address ---
  const browser2 = (await launchEngine('chromium')).browser;
  const gpPage = await browser2.newPage();
  const gpEmail = process.env.GP_EMAIL || 'gp@example.com';
  await gpPage.goto(`${BASE}/#overview`, { waitUntil: 'domcontentloaded' });
  await sleep(2000);
  try {
    await signIn(gpPage, gpEmail);
    await gpPage.evaluate(() => {
      const m = document.getElementById('acct-modal');
      if (m && m.open) m.close();
      document.getElementById('acct-btn').click();
    });
    await sleep(1000);
    const gp = await gpPage.evaluate(() => ({
      visible: getComputedStyle(document.getElementById('acct-gp')).display !== 'none',
      cap: (document.getElementById('acct-gp-cap') || {}).textContent || '',
    }));
    rec('GP console renders for the GP address', gp.visible && /LP seats/.test(gp.cap), gp.cap.trim());
  } catch (e) {
    rec('GP console renders for the GP address', false, String(e.message).slice(0, 80));
  }
  await browser2.close();

  // --- logout ---
  await page.evaluate(() => {
    const m = document.getElementById('acct-modal');
    if (!m.open) document.getElementById('acct-btn').click();
  });
  await sleep(600);
  const outBtn = await page.$('#acct-logout');
  await outBtn.click();
  await sleep(1500);
  me = await api(page, '/api/auth/me');
  rec('logout ends the session', me.body?.authenticated === false, `authenticated=${me.body?.authenticated}`);

  // --- back / forward across routes ---
  const before = errors.length;
  await page.click('[data-nav="candidates"]'); await sleep(900);
  await page.click('[data-nav="scenarios"]'); await sleep(900);
  await page.click('[data-nav="journal"]'); await sleep(900);
  await page.goBack(); await sleep(900);
  await page.goBack(); await sleep(900);
  await page.goForward(); await sleep(900);
  const nav = await page.evaluate(() => ({
    hash: location.hash,
    nodes: document.querySelectorAll('#main *').length,
    ready: document.readyState,
  }));
  rec('back/forward keeps the console rendering', nav.nodes > 50 && nav.ready === 'complete',
    `hash=${nav.hash} nodes=${nav.nodes} errors=${errors.length - before}`);

  // --- small viewport ---
  await page.setViewportSize({ width: 390, height: 844 });
  const beforeMobile = errors.length;
  let mobileOk = true;
  for (const route of ['overview', 'candidates', 'desks', 'scenarios', 'journal', 'resources', 'desk', 'about']) {
    await page.goto(`${BASE}/#${route}`, { waitUntil: 'domcontentloaded' });
    await sleep(1200);
    const state = await Promise.race([
      page.evaluate(() => document.readyState),
      new Promise((_, rj) => setTimeout(() => rj(new Error('BLOCKED')), 6000)),
    ]).catch(() => 'BLOCKED');
    const nav = await page.evaluate(() => !!document.querySelector('[data-nav]'));
    if (state === 'BLOCKED' || !nav) { mobileOk = false; break; }
  }
  rec('mobile viewport (390x844) renders all routes', mobileOk, `errors=${errors.length - beforeMobile}`);

  await browser.close();
  const failed = results.filter((r) => !r.ok);
  console.log(`\n${results.length - failed.length}/${results.length} auth-lifecycle checks passed`);
  for (const f of failed) console.log(`  FAIL ${f.name} — ${f.detail}`);
  if (errors.length) console.log(`page errors: ${errors.slice(0, 5).join(' | ')}`);
  process.exit(failed.length ? 1 : 0);
})().catch((e) => { console.error('FAILED: ' + e.message); process.exit(2); });
