function currentRoute() {
  return (location.hash || '#overview').slice(1).split('?')[0] || 'overview';
}

const deskMethods = [
  ['Overnight Premium', 'Defined-risk premium after liquidity, volatility, event, and executable-spread checks.', 'DATA INTEGRATION'],
  ['Earnings Event', 'Point-in-time expectations, confirmed events, release evidence, and post-event reaction.', 'DATA INTEGRATION'],
  ['Box / Parity Observer', 'Parity and box relationships after spreads, fees, settlement, and financing.', 'DATA INTEGRATION'],
  ['Dividend Opportunity', 'Payout durability, cash generation, shareholder yield, and valuation.', 'DATA INTEGRATION'],
  ['Global Quant & AI Research Lab', 'Global finance-AI, ML, datasets, benchmarks, and reproducible model evaluation.', 'DATA INTEGRATION'],
  ['Futures Event', 'Physical events, futures curves, liquidity, and contract specifications.', 'DATA INTEGRATION'],
  ['Bonds & Rates', 'Treasury curves, real rates, Fed policy, credit spreads, duration, and liquidity stress anchor cross-asset research.', 'ARCHITECTURE ONLY']
];

function applyBrand() {
  document.title = 'Emporion | Markets · Intelligence · Discipline';
  const meta = document.querySelector('meta[name="description"]');
  if (meta) meta.content = 'Emporion is an independent market research and decision-support platform with a seven-desk research architecture, scenario analysis, Yellow Sheets, and human review. A Bolton Investment Group (BIG) Project.';

  const icon = document.querySelector('link[rel="icon"]');
  if (icon) icon.href = './emporion-institutional-seal.svg';

  const brand = document.querySelector('.brand');
  if (brand && !brand.querySelector('.brand-logo')) {
    brand.innerHTML = '<img class="brand-logo" src="./emporion-institutional-seal.svg" alt="" width="46" height="46"><span>EMPORION<small>MARKETS · INTELLIGENCE · DISCIPLINE</small></span>';
  }

  const sidebarBottom = document.querySelector('.sidebar-bottom');
  if (sidebarBottom) {
    const mode = sidebarBottom.querySelector('.mode');
    if (mode) mode.textContent = 'RESEARCH PLATFORM';
    const p = sidebarBottom.querySelector('p');
    if (p) p.innerHTML = 'Seven research desks.<br>Six evaluated workflows.';
  }

  const footerBrand = document.querySelector('footer > span:first-child');
  if (footerBrand) footerBrand.innerHTML = 'EMPORION <span class="muted">/ A Bolton Investment Group (BIG) Project</span>';

  const topStatus = document.querySelector('.top-status');
  if (topStatus) topStatus.textContent = 'Independent research platform';
}

function statusStrip() {
  return `
    <section id="wall-street-context" class="ws-status" aria-label="Research platform status">
      <div class="ws-tape">
        <span><b>EMPORION</b></span>
        <span><b>MODE</b> RESEARCH</span>
        <span><b>DESKS</b> SEVEN</span>
        <span><b>EVALUATED</b> SIX</span>
        <span><b>DECISION</b> HUMAN REVIEW</span>
        <a href="./README_PUBLIC.md" download>README ↓</a>
      </div>
    </section>`;
}

function overviewBlock() {
  if (currentRoute() !== 'overview') return '';
  return `
    <section class="ws-operational ws-overview" aria-label="Research platform overview">
      <div class="ws-overview-grid">
        <article><div class="ws-label">RESEARCH FOCUS</div><h2>Bonds / Rates / Credit</h2><p>Treasury curves and auctions, sovereign debt, credit spreads, SOFR and repo, swaps and OIS, municipals, and structured fixed income are first in the acquisition queue.</p></article>
        <article><div class="ws-label">MARKET DATA</div><h2>Integrating</h2><p>Research views are being connected to sourced financial data with clear provider and timestamp information.</p></article>
        <article><div class="ws-label">DECISION PROCESS</div><h2>Human review</h2><p>Research workflows surface candidates and supporting analysis for structured human review.</p></article>
      </div>
      <div class="ws-desk-list">
        <div class="ws-list-head"><span>Research desk</span><span>Operating state</span></div>
        ${deskMethods.map(([name,,state]) => `<div class="ws-list-row"><strong>${name}</strong><span class="ws-state">${state}</span></div>`).join('')}
      </div>
    </section>`;
}

function desksBlock() {
  if (currentRoute() !== 'desks') return '';
  return `
    <section class="ws-operational ws-desk-methods" aria-label="Research desk methods">
      ${deskMethods.map(([name, method, state], index) => `
        <article>
          <div class="ws-label">DESK 0${index + 1}</div>
          <h2>${name}</h2>
          <p>${method}</p>
          <span class="ws-state">${state}</span>
        </article>`).join('')}
    </section>`;
}

function aboutCapitalBlock() {
  if (currentRoute() !== 'about') return '';
  return `
    <section class="ws-capital" aria-label="Emporion project overview">
      <div class="ws-capital-head">
        <div><div class="ws-label">EMPORION</div><h2>Markets · Intelligence · Discipline</h2><p class="ws-brandline">A Bolton Investment Group (BIG) Project</p></div>
        <span class="ws-boundary">RESEARCH PLATFORM</span>
      </div>
      <div class="ws-capital-grid">
        <article><h3>Data first</h3><p>Public, open, or properly licensed financial data supports the research workflows.</p></article>
        <article><h3>Quantitative research</h3><p>Specialized desks combine quantitative methods, AI and machine-learning research, source provenance, and repeatable evidence.</p></article>
        <article><h3>Structured decisions</h3><p>Candidates are evaluated through defined research methods, scenarios, and documented decision criteria.</p></article>
        <article><h3>Human judgment</h3><p>Emporion is designed to support research and decision-making. Human review remains central to the process.</p></article>
      </div>
      <div class="ws-inspiration">
        <div class="ws-label">RESEARCH & INVESTING INSPIRATIONS</div>
        <p><strong>High-Flyer / DeepSeek team</strong> · <strong>Warren Buffett</strong> · <strong>Benjamin Graham</strong> · <strong>Ray Dalio / Bridgewater Associates</strong></p>
        <p class="ws-inspiration-note">Inspirations only. No affiliation, endorsement, sponsorship, personal relationship, proprietary access, or claim of comparable results.</p>
      </div>
      <p class="ws-legal">Emporion is an independent research and software project. This site does not offer investment management, accept capital, or provide investment advice.</p>
    </section>`;
}

function installStyle() {
  if (document.getElementById('ws-polish-style')) return;
  const style = document.createElement('style');
  style.id = 'ws-polish-style';
  style.textContent = `
    .ws-status,.ws-capital,.ws-operational{margin:-4px 0 27px;border:1px solid #d7dee2;background:#fff;border-radius:6px;overflow:hidden;box-shadow:0 1px 0 rgba(16,24,32,.03)}
    .ws-tape{display:flex;align-items:center;gap:20px;flex-wrap:wrap;padding:10px 16px;background:#101820;color:#cdd6dc;font:10px 'IBM Plex Mono',monospace;letter-spacing:.55px;text-transform:uppercase}
    .ws-tape span{white-space:nowrap}.ws-tape b{color:#b8d8ff;font-weight:600}.ws-tape a{margin-left:auto;color:#b8d8ff;font-weight:500}.ws-tape a:hover{text-decoration:underline}
    .ws-label{font:10px 'IBM Plex Mono',monospace;color:#74818a;letter-spacing:1px;font-weight:500}
    .brand small{font-size:8px!important;letter-spacing:.7px!important;line-height:1.35!important}
    .ws-overview-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}.ws-overview-grid article{padding:22px;border-right:1px solid #e6eaed}.ws-overview-grid article:last-child{border-right:0}.ws-overview-grid h2{font-size:18px;margin:8px 0}.ws-overview-grid p{font-size:12px;line-height:1.6;color:#596871;margin:0}
    .ws-desk-list{border-top:1px solid #e6eaed}.ws-list-head,.ws-list-row{display:grid;grid-template-columns:1fr 180px;align-items:center;padding:11px 18px;border-bottom:1px solid #eef1f3}.ws-list-head{font:10px 'IBM Plex Mono',monospace;letter-spacing:.7px;color:#74818a;text-transform:uppercase;background:#fafbfc}.ws-list-row:last-child{border-bottom:0}.ws-list-row strong{font-size:13px}.ws-state{font:10px 'IBM Plex Mono',monospace;letter-spacing:.45px;color:#52616a}
    .ws-desk-methods{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}.ws-desk-methods article{padding:22px;border-right:1px solid #e6eaed;border-bottom:1px solid #e6eaed}.ws-desk-methods article:nth-child(2n){border-right:0}.ws-desk-methods article:nth-last-child(-n+2){border-bottom:0}.ws-desk-methods h2{font-size:16px;margin:8px 0}.ws-desk-methods p{font-size:12px;line-height:1.6;color:#596871;min-height:38px}
    .ws-capital-head{padding:19px 21px;border-bottom:1px solid #e6eaed;display:flex;align-items:center;justify-content:space-between;gap:18px}.ws-capital-head h2{margin-top:7px}.ws-brandline{margin:6px 0 0;font:10px 'IBM Plex Mono',monospace;letter-spacing:.6px;color:#6d7a83}.ws-boundary{font:10px 'IBM Plex Mono',monospace;letter-spacing:.7px;background:#f3f5f6;border:1px solid #d8dfe3;padding:7px 9px;border-radius:3px;color:#58666f;white-space:nowrap}
    .ws-capital-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}.ws-capital-grid article{padding:20px 21px;border-right:1px solid #e6eaed;border-bottom:1px solid #e6eaed}.ws-capital-grid article:nth-child(2n){border-right:0}.ws-capital-grid article:nth-last-child(-n+2){border-bottom:0}.ws-capital-grid h3{font-size:14px;margin:0 0 8px}.ws-capital-grid p{font-size:12px;line-height:1.6;color:#596871;margin:0}
    .ws-inspiration{padding:18px 21px;border-top:1px solid #e6eaed;background:#fafbfc}.ws-inspiration p{font-size:12px;line-height:1.6;color:#53616a;margin:9px 0 0}.ws-inspiration-note{font-size:11px!important;color:#75818a!important}.ws-legal{margin:0;padding:14px 21px;background:#101820;color:#cbd4da;font-size:11px;line-height:1.55}
    body[data-route='overview'] #main>.notice,body[data-route='overview'] #main>.stats,body[data-route='overview'] #main>.split,body[data-route='overview'] #main>.lower{display:none}
    body[data-route='desks'] #main>.cards{display:none}
    @media(max-width:800px){.ws-overview-grid,.ws-desk-methods{grid-template-columns:1fr}.ws-overview-grid article,.ws-desk-methods article{border-right:0;border-bottom:1px solid #e6eaed}.ws-overview-grid article:last-child,.ws-desk-methods article:last-child{border-bottom:0}.ws-list-head,.ws-list-row{grid-template-columns:1fr}.ws-state{margin-top:5px}}
    @media(max-width:650px){.ws-capital-grid{grid-template-columns:1fr}.ws-capital-grid article{border-right:0;border-bottom:1px solid #e6eaed}.ws-capital-grid article:last-child{border-bottom:0}.ws-tape{gap:9px 14px}.ws-tape a{margin-left:0;width:100%}.ws-capital-head{align-items:flex-start;flex-direction:column}}
  `;
  document.head.appendChild(style);
}

function renderContext() {
  installStyle();
  applyBrand();
  document.body.dataset.route = currentRoute();
  document.getElementById('wall-street-context')?.remove();
  document.querySelectorAll('.ws-operational,.ws-capital').forEach(node => node.remove());
  const main = document.querySelector('main');
  const head = main?.querySelector('.page-head');
  if (!main || !head) return;
  const holder = document.createElement('div');
  holder.innerHTML = statusStrip() + overviewBlock() + desksBlock() + aboutCapitalBlock();
  let cursor = head;
  for (const node of [...holder.children]) {
    cursor.insertAdjacentElement('afterend', node);
    cursor = node;
  }
}

window.addEventListener('hashchange', () => requestAnimationFrame(renderContext));
window.addEventListener('DOMContentLoaded', () => {
  applyBrand();
  const main = document.querySelector('main');
  if (main) {
    const observer = new MutationObserver(() => {
      applyBrand();
      if (!document.getElementById('wall-street-context')) requestAnimationFrame(renderContext);
    });
    observer.observe(main, {childList:true});
  }
  renderContext();
});
