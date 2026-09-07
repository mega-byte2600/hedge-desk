const PAGE_META = {
  overview: {
    goal: 'Give a concise operating view of the six research desks, control state, and decision readiness.',
    check: 'Reference fixture only. No current market signal is implied and live orders remain disabled.',
    sources: 'Validated synthetic engine fixtures; control report; candidate contract.'
  },
  candidates: {
    goal: 'Show which symbols each desk is investigating and exactly what evidence is still required.',
    check: 'Seed universe, not picks. Method-qualified candidates remain zero until current evidence and scoring are connected.',
    sources: 'Candidate contract; desk methodology; future timestamped market/provider evidence.'
  },
  desks: {
    goal: 'Explain each desk mandate, its evidence standard, and the gate that stops the next decision.',
    check: 'A desk disposition is a research-control result, not an order recommendation.',
    sources: 'Validated engine report; desk registry; deterministic control layers.'
  },
  scenarios: {
    goal: 'Stress research logic against deterministic scenarios before capital or human approval is considered.',
    check: 'Scenario values are declared fixtures and war games, not historical or forecast returns.',
    sources: 'Versioned synthetic scenarios; deterministic lifecycle and risk outputs.'
  },
  controls: {
    goal: 'Make provenance, source entitlement, release requirements, and non-overridable controls inspectable.',
    check: 'Only sources actually wired to the public build are shown as operational; research references are labeled separately.',
    sources: 'Synthetic fixtures; Papers With Backtest adapter metadata; report hashes and release-gate evidence.'
  },
  journal: {
    goal: 'Create a durable research thesis record before a decision: Interest → Hypothesis → Investigation → Evidence → Rule → Trade → Review.',
    check: 'Browser-local Yellow Sheets do not authorize trades and do not alter deterministic engine decisions.',
    sources: 'User-authored browser-local research notes plus exported copies.'
  },
  about: {
    goal: 'Explain what Hedge Desk is, what mbolton built, and the operating boundary of the MVP.',
    check: 'Paper-only research platform. No autonomous live trading and no claim of proprietary hedge-fund data.',
    sources: 'Public repository, validated research build, and documented public/open research references.'
  }
};

function currentRoute() {
  return (location.hash || '#overview').slice(1).split('?')[0] || 'overview';
}

function contextBlock(report) {
  const route = currentRoute();
  const meta = PAGE_META[route] || PAGE_META.overview;
  const evaluated = report?.report?.projects?.[0]?.evaluated_at;
  const asOf = evaluated ? new Date(evaluated).toLocaleString(undefined, {dateStyle:'medium', timeStyle:'short'}) : 'Reference fixture';
  return `
    <section id="wall-street-context" class="ws-context" aria-label="Research context and data timing">
      <div class="ws-tape">
        <span><b>BUILD</b> mbolton</span>
        <span><b>MODE</b> PAPER RESEARCH</span>
        <span><b>MARKET DATA</b> REFERENCE SNAPSHOT</span>
        <span><b>QUOTE DELAY</b> N/A · REAL-TIME FEED NOT CONNECTED</span>
        <a href="./README_PUBLIC.md" download>DOWNLOAD README ↓</a>
      </div>
      <div class="ws-grid">
        <article><div class="ws-label">01 / GOAL</div><p>${meta.goal}</p></article>
        <article><div class="ws-label">02 / GOAL CHECK</div><p>${meta.check}</p></article>
        <article><div class="ws-label">03 / DATA SOURCES</div><p>${meta.sources}</p></article>
        <article><div class="ws-label">DATA TIMING</div><p><strong>As of:</strong> ${asOf}<br><strong>Last real-time quote:</strong> Not connected<br><strong>Displayed delay:</strong> N/A until a timestamped provider is wired.</p></article>
      </div>
      <details class="ws-method-note">
        <summary>Research-source boundary</summary>
        <p>Public High-Flyer / DeepSeek research, models, repositories, methods, and open infrastructure may inform the Quant / AI Model Lab where applicable. They are research references, not a claim of access to proprietary High-Flyer trading data, positions, internal signals, or non-public research. The current public console uses validated synthetic fixtures and explicitly labeled adapter metadata until live or delayed market feeds are connected.</p>
      </details>
    </section>`;
}

function installStyle() {
  if (document.getElementById('ws-polish-style')) return;
  const style = document.createElement('style');
  style.id = 'ws-polish-style';
  style.textContent = `
    .ws-context{margin:-4px 0 27px;border:1px solid #d7dee2;background:#fff;border-radius:6px;overflow:hidden;box-shadow:0 1px 0 rgba(16,24,32,.03)}
    .ws-tape{display:flex;align-items:center;gap:20px;flex-wrap:wrap;padding:10px 16px;background:#101820;color:#cdd6dc;font:10px 'IBM Plex Mono',monospace;letter-spacing:.55px;text-transform:uppercase}
    .ws-tape span{white-space:nowrap}.ws-tape b{color:#c7ed8b;font-weight:500}.ws-tape a{margin-left:auto;color:#c7ed8b;font-weight:500}.ws-tape a:hover{text-decoration:underline}
    .ws-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr))}.ws-grid article{padding:17px 18px;border-right:1px solid #e6eaed;min-height:126px}.ws-grid article:last-child{border-right:0}.ws-grid p{font-size:12px;line-height:1.55;color:#4f5e67;margin:10px 0 0}.ws-grid strong{font-weight:600;color:#26343d}.ws-label{font:10px 'IBM Plex Mono',monospace;color:#74818a;letter-spacing:1px;font-weight:500}
    .ws-method-note{border-top:1px solid #e6eaed;padding:12px 18px;background:#fafbfc}.ws-method-note summary{font:11px 'IBM Plex Mono',monospace;color:#4f5e67;letter-spacing:.45px}.ws-method-note p{font-size:12px;color:#66737b;margin:10px 0 2px;max-width:1200px}
    @media(max-width:1200px){.ws-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.ws-grid article:nth-child(2){border-right:0}.ws-grid article:nth-child(-n+2){border-bottom:1px solid #e6eaed}}
    @media(max-width:650px){.ws-grid{grid-template-columns:1fr}.ws-grid article{border-right:0;border-bottom:1px solid #e6eaed;min-height:auto}.ws-grid article:last-child{border-bottom:0}.ws-tape{gap:9px 14px}.ws-tape a{margin-left:0;width:100%}}
  `;
  document.head.appendChild(style);
}

let reportCache;
async function getReport() {
  if (reportCache) return reportCache;
  try { reportCache = await fetch('./report.json', {cache:'no-store'}).then(r => r.json()); }
  catch { reportCache = {}; }
  return reportCache;
}

let scheduled = false;
async function renderContext() {
  if (scheduled) return;
  scheduled = true;
  requestAnimationFrame(async () => {
    scheduled = false;
    installStyle();
    document.getElementById('wall-street-context')?.remove();
    const main = document.querySelector('main');
    const head = main?.querySelector('.page-head');
    if (!main || !head) return;
    const holder = document.createElement('div');
    holder.innerHTML = contextBlock(await getReport());
    head.insertAdjacentElement('afterend', holder.firstElementChild);
  });
}

window.addEventListener('hashchange', renderContext);
window.addEventListener('DOMContentLoaded', () => {
  const main = document.querySelector('main');
  if (main) new MutationObserver(renderContext).observe(main, {childList:true, subtree:true});
  renderContext();
});
