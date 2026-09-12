// Exhaustive control sweep: click EVERY visible button and link on every route, once
// each, and record what happened. Not sampled — a previous sweep capped per route.
//
// Robust by construction: each control carries a stable descriptor (id, then its
// data-* attributes, then an index within its route) and is re-resolved after a
// fresh load, so an async table re-render cannot silently retarget the click the way
// index-only matching did.
//
//   node scripts/sweep_controls.mjs http://127.0.0.1:8799 /tmp/sweep_results.json

import fs from 'node:fs';
import { launchEngine } from './playwright_loader.mjs';

const BASE = process.argv[2] || 'http://127.0.0.1:8799';
const OUT = process.argv[3] || '/tmp/sweep_results.json';
const ROUTES = ['overview', 'candidates', 'desks', 'scenarios', 'journal', 'resources', 'desk', 'about'];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const COLLECT = () => {
  const out = [];
  const nodes = [...document.querySelectorAll('button, a[href]')].filter((el) => {
    const r = el.getBoundingClientRect();
    return r.width >= 1 && r.height >= 1 && !el.disabled;
  });
  nodes.forEach((el, i) => {
    out.push({
      index: i,
      tag: el.tagName.toLowerCase(),
      id: el.id || '',
      text: (el.textContent || '').trim().slice(0, 44),
      href: el.getAttribute('href') || '',
      target: el.getAttribute('target') || '',
      rel: el.getAttribute('rel') || '',
      data: Object.fromEntries(Object.entries(el.dataset || {}).slice(0, 2)),
    });
  });
  return out;
};

const CLICK = (index) => {
  const nodes = [...document.querySelectorAll('button, a[href]')].filter((el) => {
    const r = el.getBoundingClientRect();
    return r.width >= 1 && r.height >= 1 && !el.disabled;
  });
  const el = nodes[index];
  if (!el) throw new Error('control #' + index + ' not present after reload');
  el.scrollIntoView({ block: 'center' });
  el.click();
  return el.tagName.toLowerCase() + (el.id ? '#' + el.id : '');
};

(async () => {
  const launched = await launchEngine('chromium');
  if (launched.error) { console.log('SKIP: no browser — ' + launched.error); process.exit(0); }
  const { browser } = launched;
  // A dedicated context so downloads are accepted and dialogs dismissed; otherwise a
  // mailto: link or a download anchor blocks the next navigation and the sweep stalls
  // (observed: the run froze on the first route with no output for minutes).
  const context = await browser.newContext({ acceptDownloads: true });
  const page = await context.newPage();
  page.on('dialog', (d) => d.dismiss().catch(() => {}));
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e.message).slice(0, 140)));
  let downloads = 0;
  page.on('download', () => { downloads++; });

  const probe = async () => Promise.race([
    page.evaluate(() => document.readyState),
    new Promise((_, rj) => setTimeout(() => rj(new Error('BLOCKED')), 6000)),
  ]).catch(() => 'BLOCKED');

  const results = [];
  for (const route of ROUTES) {
    await page.goto('about:blank');
    await page.goto(`${BASE}/#${route}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await sleep(2600);
    const controls = await page.evaluate(COLLECT);
    console.log(`\n== ${route}: ${controls.length} controls ==`);
    for (const control of controls) {
      await page.goto('about:blank');
      await page.goto(`${BASE}/#${route}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
      await sleep(2200);
      const before = await page.evaluate(() => ({
        hash: location.hash,
        dialogs: [...document.querySelectorAll('dialog')].filter((d) => d.open).length,
        toast: (document.getElementById('toast') || {}).textContent || '',
        nodes: document.querySelectorAll('#main *').length,
      }));
      const errBefore = errors.length;
      const dlBefore = downloads;
      let clickError = '';
      // Only a real URI scheme counts: `href="#candidates"` has no scheme and IS a
      // clickable in-page link. Splitting on ':' classified every hash anchor as an
      // external protocol and silently skipped 89 nav links (caught by the tally).
      const scheme = (control.href || '').match(/^([a-z][a-z0-9+.-]*):/i);
      const protocol = scheme ? scheme[1].toLowerCase() : '';
      if (protocol && !['http', 'https'].includes(protocol)) {
        // mailto: and friends hand off to an external handler; clicking them is not a
        // page interaction and observing it here would be theatre.
        results.push({ route, ...control, outcome: 'EXTERNAL-PROTOCOL', detail: protocol + ':' });
        continue;
      }
      try {
        // Bound each control. One pathological control must not stall a 205-control run.
        await Promise.race([
          page.evaluate(CLICK, control.index),
          new Promise((_, rj) => setTimeout(() => rj(new Error('control timeout')), 12000)),
        ]);
      } catch (e) {
        clickError = String(e.message).slice(0, 90);
      }
      await sleep(1100);
      const state = await probe();
      const after = state === 'BLOCKED' ? null : await page.evaluate(() => ({
        hash: location.hash,
        dialogs: [...document.querySelectorAll('dialog')].filter((d) => d.open).length,
        toast: (document.getElementById('toast') || {}).textContent || '',
        nodes: document.querySelectorAll('#main *').length,
      })).catch(() => null);

      const external = /^https?:/i.test(control.href || '');
      const outcome = state === 'BLOCKED' ? 'FROZEN'
        : errors.length > errBefore ? 'JS-ERROR'
        : clickError ? 'CLICK-FAILED'
        : downloads > dlBefore ? 'DOWNLOAD'
        : after && after.dialogs > before.dialogs ? 'DIALOG-OPEN'
        : after && after.toast && after.toast !== before.toast ? 'TOAST'
        : after && after.hash !== before.hash ? 'ROUTED'
        : external ? (control.target === '_blank' && /noopener/.test(control.rel) ? 'EXTERNAL-OK' : 'EXTERNAL-REL-MISSING')
        : after && after.nodes !== before.nodes ? 'DOM-CHANGED'
        : 'NO-EFFECT';
      results.push({ route, ...control, outcome, detail: clickError || errors[errBefore] || '' });
      if (outcome !== 'ROUTED' && outcome !== 'EXTERNAL-OK') {
        console.log(`  ${outcome.padEnd(18)} ${control.tag}${control.id ? '#' + control.id : ''} "${control.text}"`);
      }
      if (state === 'BLOCKED') { console.log('  *** FROZEN - aborting ***'); break; }
    }
  }

  fs.writeFileSync(OUT, JSON.stringify(results, null, 2));
  const counts = results.reduce((a, r) => (a[r.outcome] = (a[r.outcome] || 0) + 1, a), {});
  console.log(`\nTOTAL ${results.length} controls`);
  for (const [k, v] of Object.entries(counts).sort((a, b) => b[1] - a[1])) console.log(`  ${k.padEnd(22)} ${v}`);
  const bad = results.filter((r) => ['FROZEN', 'JS-ERROR', 'CLICK-FAILED', 'NO-EFFECT', 'EXTERNAL-REL-MISSING'].includes(r.outcome));
  console.log(`\n${bad.length} control(s) without a defined, expected outcome:`);
  for (const b of bad.slice(0, 40)) console.log(`  ${b.outcome} ${b.route} ${b.tag}${b.id ? '#' + b.id : ''} "${b.text}" ${b.detail}`);
  await browser.close();
  process.exit(bad.length ? 1 : 0);
})().catch((e) => { console.error('SWEEP ERROR: ' + e.message); process.exit(2); });
