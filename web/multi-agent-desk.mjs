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
  'Six independent, isolated profiles — not six agreeable copies of one model.',
  'Each carries a persistent SOUL identity: who it is, what it owns, what it must not do, how it behaves.',
  'Six distinct model families (deepseek, glm, gpt, claude, gemini, qwen) for genuine cognitive diversity.',
  'Free agents, not a fixed matrix: a SOUL deploys to whichever trading desk needs it, like a specialist unit.',
  'Isolated state, sessions, memory, and skills per profile; independent verification and explicit handoffs.',
  'RISK is an independent challenge function that is not rewarded for agreeing with the others.',
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

export function renderSouls(timeline) {
  const hasTimeline = !!(timeline && typeof timeline.total_commits === 'number');
  const total = hasTimeline ? timeline.total_commits : null;
  const generated = hasTimeline && timeline.generated_at ? new Date(timeline.generated_at).toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' }) : '';

  const cd = hasTimeline && timeline.target_live ? countdown(timeline.target_live) : null;

  const soulCards = SOULS.map(s => `
    <article class="panel soul-card" style="display:flex;flex-direction:column;gap:14px">
      <div style="display:flex;justify-content:space-between;gap:12px;align-items:flex-start">
        <div style="display:flex;gap:12px;align-items:center">
          <span class="soul-icon" style="display:grid;place-items:center;width:42px;height:42px;border-radius:6px;background:var(--ink);color:#d1ef9f;font-size:22px">${s.icon}</span>
          <div><div class="eyebrow">AGENT · ${escapeHTML(s.role.toUpperCase())}</div><h2 style="margin:2px 0 0">${escapeHTML(s.name)}</h2></div>
        </div>
        <span class="tag">${escapeHTML(s.family)}</span>
      </div>
      <p style="margin:0">${escapeHTML(s.mandate)}</p>
      <div class="soul-model mono" style="font:12px 'IBM Plex Mono',monospace;background:#0f1a24;color:#c7ed8b;border-radius:4px;padding:8px 10px">${escapeHTML(s.model)}</div>
      <details><summary>SOUL — ownership &amp; boundaries</summary>
        <p><strong>Owns:</strong> ${escapeHTML(s.owns)}</p>
        <p><strong>Does NOT own:</strong> ${escapeHTML(s.notOwn)}</p>
        <p class="small"><strong>Principle:</strong> ${escapeHTML(s.principle)}</p>
      </details>
    </article>`).join('');

  return `
  ${headHTML()}
  <div class="notice"><strong>MULTI-AGENT RESEARCH DESK</strong><span>The Emporion team — six isolated, independently-governed specialists. Paper-only; no agent authorizes or executes a trade.</span><span class="tag">PAPER_ONLY</span></div>

  <div class="stats">
    <div class="stat"><div class="eyebrow">Agents</div><div class="stat-value">6</div><div class="stat-foot">Isolated profiles</div></div>
    <div class="stat"><div class="eyebrow">Model families</div><div class="stat-value">6</div><div class="stat-foot">deepseek · glm · gpt · claude · gemini · qwen</div></div>
    <div class="stat"><div class="eyebrow">Commits to main</div><div class="stat-value">${total === null ? '—' : total}</div><div class="stat-foot">${total === null ? 'Commit history unavailable' : 'Reproducible history'}</div></div>
    ${cd ? `<div class="stat"><div class="eyebrow">Countdown to live</div><div class="stat-value mono">${cd.d}d ${cd.h}h ${cd.m}m ${cd.s}s</div><div class="stat-foot">${cd.live ? 'LIVE' : 'target ' + new Date(timeline.target_live).toLocaleDateString()}</div></div>` : ''}
  </div>

  <div class="section-gap">
    <section class="panel"><div class="panel-head"><div><h2>The team</h2><p>Six SOULs, each with its own model, mandate, and hard boundaries.</p></div></div>
      <div class="soul-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px">${soulCards}</div>
    </section>
  </div>

  <div class="section-gap">
    <section class="panel"><div class="panel-head"><div><h2>Deployment model</h2><p>Free agents, not a fixed matrix.</p></div></div>
      <div class="panel-body" style="display:grid;gap:10px">${DEPLOYMENT.map(t => `<div class="deploy-line" style="display:flex;gap:10px;align-items:flex-start"><span style="color:#c7ed8b">▸</span><span>${escapeHTML(t)}</span></div>`).join('')}</div>
    </section>
  </div>

  <div class="section-gap">
    <section class="panel"><div class="panel-head"><div><h2>Results &amp; progress toward go-live</h2><p>${generated ? 'Snapshot generated ' + generated + '. Real commit history from the repository.' : 'Commit history could not be loaded, so no count is shown.'}</p></div></div>
      <div class="panel-body" style="display:grid;gap:14px">
        <div class="progress-track" style="position:relative;height:10px;background:#e1e6e9;border-radius:5px;overflow:hidden">
          <div style="position:absolute;inset:0 0 auto auto;width:42%;background:#c7ed8b;border-radius:5px"></div>
        </div>
        <div class="small">Reference deployment track — the console is live once the Render service is healthy.</div>
        <div style="display:flex;gap:10px;flex-wrap:wrap">${SOULS.map(s => `<span class="tag">${escapeHTML(s.family)} ${escapeHTML(s.role)}</span>`).join('')}</div>
      </div>
    </section>
  </div>`;
}

function headHTML() {
  return `<div class="page-head"><div><h1>Multi-agent research desk</h1><p class="subtitle">Six specialized agents, each with its own SOUL identity, model, and mandate.</p></div></div>`;
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

function tickCountdown() {
  if (!isBrowser) return;
  const node = document.querySelector('.stat .mono');
  if (!node || !_timelineCache) return;
  const cd = countdown(_timelineCache.target_live);
  node.textContent = `${cd.d}d ${cd.h}h ${cd.m}m ${cd.s}s`;
}
