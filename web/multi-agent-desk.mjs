// Multi-agent desk demo + results/progress view for the Emporion web console.
// Renders the six-agent team (SOUL identities), their backing models, the
// deployment model, and a results/progress timeline toward go-live.
//
// Pure data + render helpers are exported for node:test; browser wiring runs
// only when `window` is present so the module is importable in a test runner.

export const SOULS = [
  { name: 'orchestrator', role: 'Coordinator', model: 'deepseek/deepseek-v4-pro', family: 'deepseek', icon: '◈',
    mandate: 'Routes work to the right specialist by mandate, synthesizes results, escalates disagreement. Never overrides a specialist by fiat.',
    owns: 'Task routing, synthesis, escalation, explicit handoffs, division of labor.',
    notOwn: 'Specialist analysis, accepting/rejecting portfolio risk, overriding a domain expert.',
    principle: 'Routes, synthesizes, escalates — does not do the specialists\u2019 jobs.' },
  { name: 'quant', role: 'Quantitative research', model: 'z-ai/glm-5.3', family: 'glm', icon: '∑',
    mandate: 'Factor research, signals, statistical testing, backtesting, falsification of investment hypotheses.',
    owns: 'Quantitative research, market data analysis, quant datasets, backtests, statistical rigor.',
    notOwn: 'Software engineering, narrative research, risk decisions, acquiring new datasets.',
    principle: 'Data before narrative. Never fabricates data or results.' },
  { name: 'engineer', role: 'Software & systems', model: 'openai/gpt-6-astra-flex', family: 'gpt', icon: '▦',
    mandate: 'Architecture, coding, testing, integrations, deployment, infrastructure for the desk software.',
    owns: 'Desk software, pipelines, integrations, deployment, reliability.',
    notOwn: 'Quant methods, risk decisions, research narratives, dataset sourcing.',
    principle: 'Inspect before modifying. Simple, testable, reliable systems.' },
  { name: 'research', role: 'Deep research', model: 'anthropic/claude-haiku-4.5', family: 'claude', icon: '◎',
    mandate: 'Deep financial, economic, company, industry, academic and alternative-data research.',
    owns: 'Company/industry/macro research, literature, alternative-data reconnaissance.',
    notOwn: 'Statistical testing, dataset acquisition, risk decisions, production code.',
    principle: 'Trace claims to evidence. Distinguish fact, inference, speculation.' },
  { name: 'risk', role: 'Independent challenge', model: 'google/gemini-3.8-flash', family: 'gemini', icon: '◔',
    mandate: 'Independent challenge, portfolio risk, risk of ruin, concentration, leverage, liquidity, tail risk, model risk.',
    owns: 'Independent risk challenge, tail risk, model risk, survivability, the final say on acceptable risk.',
    notOwn: 'Originating research, building models, writing production code.',
    principle: 'Independent — not rewarded for agreeing. Quantified challenge, escalates without hedging.' },
  { name: 'data', role: 'Data stewardship', model: 'qwen/qwen3.8-flash', family: 'qwen', icon: '▤',
    mandate: 'Find, acquire, validate, normalize, catalogue, maintain datasets. Search aggressively for open sources.',
    owns: 'Data sourcing, acquisition, validation, normalization, cataloguing, reproducibility.',
    notOwn: 'Data analysis, production pipelines, risk decisions, provenance shortcuts.',
    principle: 'Provenance, quality, lineage, reproducibility. Filesystem-first.' },
];

const DEPLOYMENT = [
  'Six specialists run as separate profiles with separate state, so one cannot quietly drift into another.',
  'Each has a written remit: what it is responsible for, what it must not touch, and how it works.',
  'They run on different underlying models, chosen so their judgements stay independent of each other.',
  'A specialist moves to whichever desk needs it, instead of sitting in a fixed team chart.',
  'Sessions, memory, and skills stay separate per specialist, and handoffs are stated out loud.',
  'Risk is a challenge role with no incentive to agree with the desk it is reviewing.',
];

export function escapeHTML(s) {
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

export function countdown(targetISO) {
  const target = new Date(targetISO).getTime();
  const now = Date.now();
  const diff = Math.max(0, target - now);
  const d = Math.floor(diff / 86400000);
  const h = Math.floor((diff % 86400000) / 3600000);
  const m = Math.floor((diff % 3600000) / 60000);
  const s = Math.floor((diff % 60000) / 1000);
  return { d, h, m, s, live: diff === 0 };
}

function progressBar() {
  // Two rows per agent, one per field. Bars are decorative, not data.
  return '';
}

export function renderSouls(_timeline) {
  // Build telemetry (commit counts, go-live countdown, deployment track) is deliberately
  // NOT rendered here. This desk page is public product surface; how many commits landed
  // and when we intend to go live is internal deployment detail and belongs in ops docs.
  const soulCards = SOULS.map(s => `
    <article class="panel soul-card" style="display:flex;flex-direction:column;gap:14px">
      <div style="display:flex;justify-content:space-between;gap:12px;align-items:flex-start">
        <div style="display:flex;gap:12px;align-items:center">
          <span class="soul-icon" style="display:grid;place-items:center;width:42px;height:42px;border-radius:6px;background:var(--ink);color:#d1ef9f;font-size:22px">${s.icon}</span>
          <div><div class="eyebrow">${escapeHTML(s.role.toUpperCase())}</div><h2 style="margin:2px 0 0">${escapeHTML(s.name)}</h2></div>
        </div>
      </div>
      <p style="margin:0">${escapeHTML(s.mandate)}</p>
      <details><summary>What this specialist owns, and what it does not</summary>
        <p><strong>Owns:</strong> ${escapeHTML(s.owns)}</p>
        <p><strong>Does NOT own:</strong> ${escapeHTML(s.notOwn)}</p>
        <p class="small"><strong>Principle:</strong> ${escapeHTML(s.principle)}</p>
      </details>
    </article>`).join('');

  return `
  ${headHTML()}
  <div class="notice"><strong>MULTI-AGENT RESEARCH DESK</strong><span>Six specialists staff this desk. Each works independently of the others, and none of them can place a trade.</span><span class="tag">PAPER_ONLY</span></div>

  <div class="stats">
    <div class="stat"><div class="eyebrow">Agents</div><div class="stat-value">6</div><div class="stat-foot">Separate profiles, separate state</div></div>
  </div>

  <div class="section-gap">
    <section class="panel"><div class="panel-head"><div><h2>The team</h2><p>Each has a defined remit, and limits it does not cross.</p></div></div>
      <div class="soul-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px">${soulCards}</div>
    </section>
  </div>

  <div class="section-gap">
    <section class="panel"><div class="panel-head"><div><h2>How the desk is staffed</h2><p>Each specialist works independently, rather than as one team with one opinion.</p></div></div>
      <div class="panel-body" style="display:grid;gap:10px">${DEPLOYMENT.map(t => `<div class="deploy-line" style="display:flex;gap:10px;align-items:flex-start"><span style="color:#c7ed8b">▸</span><span>${escapeHTML(t)}</span></div>`).join('')}</div>
    </section>
  </div>

  </div>`;
}

function headHTML() {
  return `<div class="page-head"><div><h1>Multi-agent research desk</h1><p class="subtitle">Each has its own remit and its own way of working the problem.</p></div></div>`;
}

// ── Browser wiring (guarded so the module is importable under node:test) ──
const isBrowser = typeof window !== 'undefined' && typeof document !== 'undefined';
let _timelineCache = null;
let _deskRendering = false;

async function loadTimeline() {
  if (_timelineCache) return _timelineCache;
  try {
    const res = await fetch('./timeline.json', { cache: 'no-store' });
    if (!res.ok) throw Error('timeline unavailable');
    _timelineCache = await res.json();
  } catch (e) {
    // Return nothing rather than inventing a history. A fabricated commit count
    // rendered under a "Real commit history from the repository" label is a claim
    // the dashboard cannot support, so the view says it is unavailable instead.
    return null;
  }
  return _timelineCache;
}

async function renderDeskView() {
  if (!isBrowser) return;
  const main = document.getElementById('main');
  if (!main) return;
  if (location.hash !== '#desk') return;
  // Re-entrancy guard. This write lands inside the subtree the observer below
  // watches, so without it the observer re-fires on its own mutation, writes the
  // loading HTML again, and the microtask queue never drains — the page locks up
  // solid before the first await resolves. Navigating to the multi-agent desk
  // tab was enough to hang the whole renderer.
  if (_deskRendering) return;
  if (main.dataset.deskView === 'rendered' && document.querySelector('.soul-card')) return;
  _deskRendering = true;
  main.dataset.deskView = 'loading';
  main.innerHTML = '<div class="loading">Loading multi-agent desk…</div>';
  try {
    const timeline = await loadTimeline();
    if (location.hash !== '#desk') return;
    main.innerHTML = renderSouls(timeline);
    main.dataset.deskView = 'rendered';
  } finally {
    _deskRendering = false;
  }
}

if (isBrowser) {
  // Increment the live countdown each second.
  setInterval(tickCountdown, 1000);

  window.addEventListener('hashchange', () => { if (location.hash === '#desk') renderDeskView(); });
  document.addEventListener('DOMContentLoaded', () => {
    if (location.hash === '#desk') renderDeskView();
    const main = document.getElementById('main');
    if (main) {
      // Deferred, like every other page enhancer: a synchronous observer callback
      // that writes into its own subtree can never yield and freezes the page.
      new MutationObserver(() => requestAnimationFrame(() => {
        if (location.hash === '#desk' && !_deskRendering && !document.querySelector('.soul-card')) {
          renderDeskView();
        }
      })).observe(main, { childList: true, subtree: true });
    }
  });
}

let _lastTick = '';

function tickCountdown() {
  if (!isBrowser) return;
  // Only while the desk view is on screen. The stat node lives inside #main, so
  // writing it fires every subtree observer on the page; ticking on every route
  // meant a full enhancement cascade once a second, forever.
  if (location.hash !== '#desk') return;
  const node = document.querySelector('.stat .mono');
  if (!node || !_timelineCache) return;
  const cd = countdown(_timelineCache.target_live);
  const next = `${cd.d}d ${cd.h}h ${cd.m}m ${cd.s}s`;
  if (next === _lastTick) return;
  node.textContent = next;
  _lastTick = next;
}
