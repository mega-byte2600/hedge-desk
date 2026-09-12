#!/usr/bin/env node
// Social login (Supabase Auth) check.
//
// Social login is gated behind configuration, so on the deployed service the buttons
// do not render at all (`/api/auth/providers` -> enabled:false). This exercises the
// configured path end to end without any real provider credentials: it mints an
// HS256 token signed with a LOCAL, synthetic secret of the same shape Supabase issues,
// then checks the UI, the endpoint, and the failure modes.
//
// What this cannot cover, and does not claim to: a real Google/GitHub/Microsoft/Apple
// round trip, which needs a live Supabase project with those providers enabled.
//
//   SMOKE_JWT_SECRET=local-synthetic-secret \
//   node scripts/smoke_social.mjs http://127.0.0.1:8765

import crypto from 'node:crypto';
import { launchEngine } from './playwright_loader.mjs';

const BASE = process.argv[2] || 'http://127.0.0.1:8765';
const SECRET = process.env.SMOKE_JWT_SECRET || '';
const EMAIL = process.env.SMOKE_SOCIAL_EMAIL || 'social-check@example.com';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const results = [];
const rec = (name, ok, detail = '') => {
  results.push({ name, ok, detail });
  console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? '  — ' + detail : ''}`);
};

const b64url = (buf) => Buffer.from(buf).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

function mintToken(email, ttlSeconds = 3600, aud = 'authenticated') {
  const header = b64url(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
  const payload = b64url(JSON.stringify({
    sub: '00000000-0000-4000-8000-000000000000',
    email,
    aud,
    role: 'authenticated',
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + ttlSeconds,
  }));
  const sig = crypto.createHmac('sha256', SECRET).update(`${header}.${payload}`).digest('base64')
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  return `${header}.${payload}.${sig}`;
}

(async () => {
  if (!SECRET) {
    console.log('SKIP: set SMOKE_JWT_SECRET to the secret the local server was started with.');
    process.exit(0);
  }
  const launched = await launchEngine('chromium');
  if (launched.error) { console.log('SKIP: no browser — ' + launched.error); process.exit(0); }
  const { browser } = launched;
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e.message).slice(0, 140)));
  await page.goto(`${BASE}/#overview`, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await sleep(2500);

  const post = (body) => page.evaluate(async ([b, payload]) => {
    const r = await fetch(b + '/api/auth/social', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    let parsed = null;
    try { parsed = await r.json(); } catch (e) { /* non-JSON */ }
    return { status: r.status, body: parsed };
  }, [BASE, body]);

  // S1 — the service advertises the configured providers
  const providers = await page.evaluate(async (b) => (await fetch(b + '/api/auth/providers')).json(), BASE);
  rec('providers endpoint reports the configured providers',
    providers.enabled === true && Array.isArray(providers.providers) && providers.providers.length > 0,
    `enabled=${providers.enabled} providers=[${(providers.providers || []).join(',')}]`);

  // S2 — the console renders a button per provider
  await page.click('#acct-btn');
  await sleep(900);
  const buttons = await page.$$eval('#acct-social button', (b) => b.map((x) => x.textContent.trim()).filter(Boolean));
  await page.evaluate(() => document.getElementById('acct-modal').close());
  rec('account modal renders the social buttons',
    buttons.length === (providers.providers || []).length && buttons.length > 0,
    `${buttons.length} button(s): ${buttons.join(' / ')}`);

  // S3 — a valid Supabase-shaped token creates a real session
  const token = mintToken(EMAIL);
  const good = await post({ access_token: token });
  const me = await page.evaluate(async (b) => (await fetch(b + '/api/auth/me')).json(), BASE);
  rec('valid token signs the user in (session created)',
    good.status === 200 && me.authenticated === true && me.email === EMAIL,
    `HTTP ${good.status} role=${good.body?.role} me=${me.email}/${me.role}`);

  // S4 — a tampered signature is refused
  const tampered = mintToken(EMAIL).replace(/.$/, (c) => (c === 'A' ? 'B' : 'A'));
  const bad = await post({ access_token: tampered });
  rec('tampered token is refused', bad.status === 401, `HTTP ${bad.status}`);

  // S5 — an expired token is refused
  const expired = mintToken(EMAIL, -60);
  const old = await post({ access_token: expired });
  rec('expired token is refused', old.status === 401, `HTTP ${old.status}`);

  // S6 — wrong audience is refused
  const wrongAud = mintToken(EMAIL, 3600, 'anon');
  const wa = await post({ access_token: wrongAud });
  rec('wrong-audience token is refused', wa.status === 401, `HTTP ${wa.status}`);

  // S7 — missing token is a 400, not a crash
  const none = await post({});
  rec('missing token is rejected', none.status === 400, `HTTP ${none.status}`);

  // S8 — a social sign-in must not demote an existing member role
  // (the endpoint reuses upsert_guest + access_for, so raise the role and re-sign-in)
  const lpEmail = process.env.SMOKE_LP_EMAIL || '';
  if (lpEmail) {
    const lpToken = mintToken(lpEmail);
    await post({ access_token: lpToken });
    const after = await page.evaluate(async (b) => (await fetch(b + '/api/auth/me')).json(), BASE);
    rec('social sign-in preserves an existing higher role', after.role !== 'GUEST', `role=${after.role}`);
  } else {
    console.log('  [skip] S8 role-preservation needs SMOKE_LP_EMAIL (covered by unit tests)');
  }

  await browser.close();
  const failed = results.filter((r) => !r.ok);
  console.log(`\n${results.length - failed.length}/${results.length} social-login checks passed`);
  if (errors.length) console.log(`page errors: ${errors.slice(0, 3).join(' | ')}`);
  process.exit(failed.length ? 1 : 0);
})().catch((e) => { console.error('FAILED: ' + e.message); process.exit(2); });
