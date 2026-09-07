function currentRoute() {
  return (location.hash || '#overview').slice(1).split('?')[0] || 'overview';
}

const deskMethods = [
  ['Overnight Premium', 'Defined-risk premium after liquidity, volatility, event, and executable-spread checks.'],
  ['Earnings Event', 'Point-in-time expectations, confirmed events, release evidence, and post-event reaction.'],
  ['Box / Parity Observer', 'Parity and box relationships after spreads, fees, settlement, and financing.'],
  ['Dividend Opportunity', 'Payout durability, cash generation, shareholder yield, and valuation.'],
  ['Global Quant & AI Research Lab', 'Global finance-AI, ML, datasets, benchmarks, and reproducible model evaluation.'],
  ['Futures Event', 'Physical events, futures curves, liquidity, and contract specifications.']
];

function statusStrip() {
  return `
    <section id="wall-street-context" class="ws-status" aria-label="Operating status">
      <div class="ws-tape">
        <span><b>HEDGE DESK</b></span>
        <span><b>MODE</b> RESEARCH</span>
        <span><b>EXECUTION</b> DISABLED</span>
        <span><b>HUMAN GATE</b> REQUIRED</span>
        <span><b>DATA</b> OPEN / PUBLIC SOURCES INTEGRATING</span>
        <a href="./README_PUBLIC.md" download>README ↓</a>
      </div>
    </section>`;
}

function overviewBlock() {
  if (currentRoute() !== 'overview') return '';
  return `
    <section class="ws-operational ws-overview" aria-label="Operational research status">
      <div class="ws-overview-grid">
        <article><div class="ws-label">DATA PRIORITY</div><h2>Bonds / Rates / Credit</h2><p>Treasury curves and auctions, sovereign debt, credit spreads, SOFR and repo, swaps and OIS, municipals, and structured fixed income are first in the acquisition queue.</p></article>
        <article><div class="ws-label">MARKET DATA</div><h2>Integrating</h2><p>Operational views will show only sourced observations with provider, timestamp, freshness, and delay. Missing feeds remain unavailable rather than being replaced by test values.</p></article>
        <article><div class="ws-label">DECISION CONTROL</div><h2>Human gate required</h2><p>Research may qualify a candidate. Deterministic risk controls and final human approval remain separate from model or desk output.</p></article>
      </div>
      <div class="ws-desk-list">
        <div class="ws-list-head"><span>Research desk</span><span>Operating state</span></div>
        ${deskMethods.map(([name]) => `<div class="ws-list-row"><strong>${name}</strong><span class="ws-state">DATA INTEGRATION</span></div>`).join('')}
      </div>
    </section>`;
}

function desksBlock() {
  if (currentRoute() !== 'desks') return '';
  return `
    <section class="ws-operational ws-desk-methods" aria-label="Research desk methods">
      ${deskMethods.map(([name, method], index) => `
        <article>
          <div class="ws-label">DESK 0${index + 1}</div>
          <h2>${name}</h2>
          <p>${method}</p>
          <span class="ws-state">OPERATIONAL DATA PENDING</span>
        </article>`).join('')}
    </section>`;
}

function controlsBlock() {
  if (currentRoute() !== 'controls') return '';
  return `
    <section class="ws-operational ws-controls" aria-label="Production data and control boundary">
      <div class="ws-overview-grid">
        <article><div class="ws-label">PROVENANCE</div><h2>Required</h2><p>Every operational observation must carry source, provider timestamp, received time, expected delay, freshness state, and use-rights metadata.</p></article>
        <article><div class="ws-label">TEST DATA</div><h2>Isolated</h2><p>CI, Golden Master, and scenario inputs stay outside operational market views and cannot substitute for missing provider data.</p></article>
        <article><div class="ws-label">EXECUTION</div><h2>Disabled</h2><p>No production broker adapter or autonomous order path is enabled. Deterministic controls and human approval remain mandatory.</p></article>
      </div>
    </section>`;
}

function aboutCapitalBlock() {
  if (currentRoute() !== 'about') return '';
  return `
    <section class="ws-capital" aria-label="Research governance">
      <div class="ws-capital-head">
        <div><div class="ws-label">RESEARCH GOVERNANCE</div><h2>Yellow Sheets</h2></div>
        <span class="ws-boundary">RESEARCH RECORD</span>
      </div>
      <div class="ws-capital-grid">
        <article><h3>Thesis</h3><p>Record the idea, evidence, decision rule, risk conditions, and what would invalidate the thesis before capital is considered.</p></article>
        <article><h3>Diligence</h3><p>Create an auditable research record that can be challenged, reviewed, and compared across desks and future authorized partners.</p></article>
        <article><h3>Decision boundary</h3><p>Research may produce an actionable candidate. It does not authorize an order. Deterministic controls and human approval remain separate gates.</p></article>
        <article><h3>Capital boundary</h3><p>The public console is research infrastructure. Any future investment vehicle, investor onboarding, or capital process would remain separate.</p></article>
      </div>
      <div class="ws-inspiration">
        <div class="ws-label">RESEARCH & INVESTING INSPIRATIONS</div>
        <p><strong>High-Flyer / DeepSeek team</strong> · <strong>Warren Buffett</strong> · <strong>Benjamin Graham</strong> · <strong>Ray Dalio / Bridgewater Associates</strong></p>
        <p class="ws-inspiration-note">Inspirations only. No affiliation, endorsement, sponsorship, personal relationship, proprietary access, or claim of comparable results.</p>
      </div>
      <p class="ws-legal">Research only. No public offering, subscription, capital acceptance, or live autonomous trading is provided through this site.</p>
    </section>`;
}

function installStyle() {
  if (document.getElementById('ws-polish-style')) return;
  const style = document.createElement('style');
  style.id = 'ws-polish-style';
  style.textContent = `
    .ws-status,.ws-capital,.ws-operational{margin:-4px 0 27px;border:1px solid #d7dee2;background:#fff;border-radius:6px;overflow:hidden;box-shadow:0 1px 0 rgba(16,24,32,.03)}
    .ws-tape{display:flex;align-items:center;gap:20px;flex-wrap:wrap;padding:10px 16px;background:#101820;color:#cdd6dc;font:10px 'IBM Plex Mono',monospace;letter-spacing:.55px;text-transform:uppercase}
    .ws-tape span{white-space:nowrap}.ws-tape b{color:#c7ed8b;font-weight:500}.ws-tape a{margin-left:auto;color:#c7ed8b;font-weight:500}.ws-tape a:hover{text-decoration:underline}
    .ws-label{font:10px 'IBM Plex Mono',monospace;color:#74818a;letter-spacing:1px;font-weight:500}
    .ws-overview-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}.ws-overview-grid article{padding:22px;border-right:1px solid #e6eaed}.ws-overview-grid article:last-child{border-right:0}.ws-overview-grid h2{font-size:18px;margin:8px 0}.ws-overview-grid p{font-size:12px;line-height:1.6;color:#596871;margin:0}
    .ws-desk-list{border-top:1px solid #e6eaed}.ws-list-head,.ws-list-row{display:grid;grid-template-columns:1fr 180px;align-items:center;padding:11px 18px;border-bottom:1px solid #eef1f3}.ws-list-head{font:10px 'IBM Plex Mono',monospace;letter-spacing:.7px;color:#74818a;text-transform:uppercase;background:#fafbfc}.ws-list-row:last-child{border-bottom:0}.ws-list-row strong{font-size:13px}.ws-state{font:10px 'IBM Plex Mono',monospace;letter-spacing:.45px;color:#52616a}
    .ws-desk-methods{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}.ws-desk-methods article{padding:22px;border-right:1px solid #e6eaed;border-bottom:1px solid #e6eaed}.ws-desk-methods article:nth-child(2n){border-right:0}.ws-desk-methods article:nth-last-child(-n+2){border-bottom:0}.ws-desk-methods h2{font-size:16px;margin:8px 0}.ws-desk-methods p{font-size:12px;line-height:1.6;color:#596871;min-height:38px}
    .ws-capital-head{padding:19px 21px;border-bottom:1px solid #e6eaed;display:flex;align-items:center;justify-content:space-between;gap:18px}.ws-capital-head h2{margin-top:7px}.ws-boundary{font:10px 'IBM Plex Mono',monospace;letter-spacing:.7px;background:#f3f5f6;border:1px solid #d8dfe3;padding:7px 9px;border-radius:3px;color:#58666f;white-space:nowrap}
    .ws-capital-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}.ws-capital-grid article{padding:20px 21px;border-right:1px solid #e6eaed;border-bottom:1px solid #e6eaed}.ws-capital-grid article:nth-child(2n){border-right:0}.ws-capital-grid article:nth-last-child(-n+2){border-bottom:0}.ws-capital-grid h3{font-size:14px;margin:0 0 8px}.ws-capital-grid p{font-size:12px;line-height:1.6;color:#596871;margin:0}
    .ws-inspiration{padding:18px 21px;border-top:1px solid #e6eaed;background:#fafbfc}.ws-inspiration p{font-size:12px;line-height:1.6;color:#53616a;margin:9px 0 0}.ws-inspiration-note{font-size:11px!important;color:#75818a!important}.ws-legal{margin:0;padding:14px 21px;background:#101820;color:#cbd4da;font-size:11px;line-height:1.55}
    body[data-route='overview'] #main>.notice,body[data-route='overview'] #main>.stats,body[data-route='overview'] #main>.split,body[data-route='overview'] #main>.lower{display:none}
    body[data-route='desks'] #main>.cards{display:none}
    body[data-route='controls'] #main>.stats,body[data-route='controls'] #main>.panel,body[data-route='controls'] #main>.section-gap{display:none}
    @media(max-width:800px){.ws-overview-grid,.ws-desk-methods{grid-template-columns:1fr}.ws-overview-grid article,.ws-desk-methods article{border-right:0;border-bottom:1px solid #e6eaed}.ws-overview-grid article:last-child,.ws-desk-methods article:last-child{border-bottom:0}.ws-list-head,.ws-list-row{grid-template-columns:1fr}.ws-state{margin-top:5px}}
    @media(max-width:650px){.ws-capital-grid{grid-template-columns:1fr}.ws-capital-grid article{border-right:0;border-bottom:1px solid #e6eaed}.ws-capital-grid article:last-child{border-bottom:0}.ws-tape{gap:9px 14px}.ws-tape a{margin-left:0;width:100%}.ws-capital-head{align-items:flex-start;flex-direction:column}}
  `;
  document.head.appendChild(style);
}

function renderContext() {
  installStyle();
  document.body.dataset.route = currentRoute();
  document.getElementById('wall-street-context')?.remove();
  document.querySelectorAll('.ws-operational,.ws-capital').forEach(node => node.remove());
  const main = document.querySelector('main');
  const head = main?.querySelector('.page-head');
  if (!main || !head) return;
  const holder = document.createElement('div');
  holder.innerHTML = statusStrip() + overviewBlock() + desksBlock() + controlsBlock() + aboutCapitalBlock();
  let cursor = head;
  for (const node of [...holder.children]) {
    cursor.insertAdjacentElement('afterend', node);
    cursor = node;
  }
}

window.addEventListener('hashchange', () => requestAnimationFrame(renderContext));
window.addEventListener('DOMContentLoaded', () => {
  const main = document.querySelector('main');
  if (main) {
    const observer = new MutationObserver(() => {
      if (!document.getElementById('wall-street-context')) requestAnimationFrame(renderContext);
    });
    observer.observe(main, {childList:true});
  }
  renderContext();
});
