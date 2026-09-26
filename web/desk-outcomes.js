import { escapeHTML as e, human, statusClass } from './core.mjs';

// Progressive enhancement for the #desks route: surfaces what the research
// desks ACTUALLY produced in the last nightly batch, above the reference
// fixture cards. A Chartered Financial Analyst reads what happened, not what
// a fixture says could happen — so real outputs render first, honestly
// labeled, and the fixtures remain below as the published reference set.
//
// Fail-soft: if the real-data endpoints are unreachable, the tab renders
// exactly as before. Nothing here authorizes a trade.

let cached = null;
let loading = null;

const tag = value => `<span class="tag ${statusClass(value)}">${e(human(value))}</span>`;

async function getDeskOutputs() {
  if (cached) return cached;
  if (!loading) {
    loading = Promise.all([
      fetch('./api/earnings-candidates', { cache: 'no-store' })
        .then(r => { if (!r.ok) throw new Error('earnings unavailable'); return r.json(); })
        .catch(() => null),
      fetch('./api/macro-candidates', { cache: 'no-store' })
        .then(r => { if (!r.ok) throw new Error('macro unavailable'); return r.json(); })
        .catch(() => null),
    ]).then(([earnings, macro]) => {
      if (!earnings && !macro) return null;
      cached = { earnings, macro };
      return cached;
    });
  }
  return loading;
}

function earningsRows(feed) {
  if (!feed || !Array.isArray(feed.candidates)) return '';
  return feed.candidates.map(c => {
    const obs = c.observation || {};
    const eps = obs.latest_quarterly_eps != null ? `$${e(obs.latest_quarterly_eps)}` : '—';
    const period = e(obs.latest_quarterly_period || '');
    return `<tr><td><strong class="mono">${e(c.symbol)}</strong></td>` +
      `<td>${tag(c.stage)}</td><td>${eps}</td><td>${period}</td>` +
      `<td>${tag(c.trade_authorized ? 'AUTHORIZED' : 'PAPER_ONLY')}</td></tr>`;
  }).join('');
}

function macroRows(feed) {
  if (!feed) return '';
  if (!Array.isArray(feed.candidates) || feed.candidates.length === 0) {
    const reason = feed.reason ? ` — ${e(feed.reason)}` : '';
    return `<tr><td colspan="4"><span class="small">Withheld${reason}. No values shown rather than fabricated ones.</span></td></tr>`;
  }
  return feed.candidates.map(c =>
    `<tr><td><strong class="mono">${e(c.symbol)}</strong></td>` +
    `<td>${e(c.method || c.stage || '')}</td>` +
    `<td>${e(c.data_source || '')}</td>` +
    `<td>${tag(c.trade_authorized ? 'AUTHORIZED' : 'PAPER_ONLY')}</td></tr>`
  ).join('');
}

function deskOutputsPanel(data) {
  if (!data) return '';
  const { earnings, macro } = data;
  const eCount = earnings && Array.isArray(earnings.candidates) ? earnings.candidates.length : 0;
  const mCount = macro && Array.isArray(macro.candidates) ? macro.candidates.length : 0;
  return `<div class="notice" data-desk-outcomes-enhanced="true"><strong>LAST NIGHT'S DESK OUTPUTS — REAL DATA</strong>` +
    `<span>What the earnings and macro desks actually produced in the committed nightly batch. Fixture cards below remain the published reference set.</span>${tag('PAPER_ONLY')}</div>` +
    `<div class="stats" data-desk-outcomes-stats="true">` +
    `<article class="stat"><div class="eyebrow">Earnings actuals</div><div class="stat-value">${eCount}</div><div class="stat-foot">Real SEC EDGAR filings</div></article>` +
    `<article class="stat"><div class="eyebrow">Macro observations</div><div class="stat-value">${mCount}</div><div class="stat-foot">Real FRED observations</div></article>` +
    `<article class="stat"><div class="eyebrow">Trade authorization</div><div class="stat-value">0</div><div class="stat-foot">Research output only</div></article>` +
    `</div>` +
    `<div class="section-gap">${`<section class="panel"><div class="panel-head"><div><div class="eyebrow">EARNINGS DESK</div><h2>EDGAR actuals</h2></div></div>` +
      `<div class="table-scroll"><table><thead><tr><th>Filer</th><th>Stage</th><th>Latest quarterly EPS</th><th>Period</th><th>Authorization</th></tr></thead>` +
      `<tbody>${earningsRows(earnings) || '<tr><td colspan="5"><span class="small">No earnings actuals in this batch.</span></td></tr>'}</tbody></table></div></section>`}</div>` +
    `<div class="section-gap">${`<section class="panel"><div class="panel-head"><div><div class="eyebrow">MACRO DESK</div><h2>FRED observations</h2></div></div>` +
      `<div class="table-scroll"><table><thead><tr><th>Series</th><th>Reading</th><th>Source</th><th>Authorization</th></tr></thead>` +
      `<tbody>${macroRows(macro)}</tbody></table></div></section>`}</div>`;
}

async function enhanceDesksRoute() {
  if (location.hash !== '#desks') return;
  const main = document.querySelector('#main');
  if (!main || main.querySelector('[data-desk-outcomes-enhanced]')) return;
  try {
    const data = await getDeskOutputs();
    if (location.hash !== '#desks' || !data) return;
    const head = main.querySelector('.page-head');
    if (head && !main.querySelector('[data-desk-outcomes-enhanced]')) {
      head.insertAdjacentHTML('afterend', deskOutputsPanel(data));
    }
  } catch {
    // Reference fixture cards remain available if the enhancement cannot load.
  }
}

window.addEventListener('hashchange', () => queueMicrotask(enhanceDesksRoute));
const observer = new MutationObserver(() => {
  if (location.hash === '#desks') queueMicrotask(enhanceDesksRoute);
});
const main = document.querySelector('#main');
if (main) observer.observe(main, { childList: true });
queueMicrotask(enhanceDesksRoute);
