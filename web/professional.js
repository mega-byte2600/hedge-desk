
import { currentRoute } from './core.mjs';

const deskMethods = [
  ['Overnight Premium', 'Sells defined risk premium, and only after liquidity, volatility, event, and spread checks pass.', 'Active'],
  ['Earnings Event', 'Compares what was expected against what the company confirmed, and how the stock reacted.', 'Active'],
  ['Box / Parity Observer', 'Checks parity and box relationships after spreads, fees, settlement, and financing.', 'Active'],
  ['Dividend Opportunity', 'Asks whether the payout can survive: cash generation, shareholder yield, and valuation.', 'Active'],
  ['Global Quant & AI Research Lab', 'Covers quantitative and machine learning research, datasets, benchmarks, and reproducible model checks.', 'Active'],
  ['Futures Event', 'Reads physical events against futures curves, liquidity, and contract specifications.', 'Active'],
  ['Bonds & Rates', 'Uses Treasury curves, real rates, Fed policy, credit spreads, duration, and liquidity stress as the backdrop for other research.', 'Coming soon']
];

function applyBrand() {
  document.title = 'Emporion | Markets · Intelligence · Discipline';
  const meta = document.querySelector('meta[name="description"]');
  if (meta) meta.content = 'Emporion is an independent market research and decision-support platform with a seven-desk research architecture, scenario analysis, Yellow Sheets, portfolio survival controls, and human review. A Bolton Investment Group (BIG) Project.';

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
        <span>Independent research</span>
        <span><b>6</b> desks + 1 coming soon</span>
        <span>Human review</span>
        <span>No orders placed</span>
        <a href="./README_PUBLIC.md" download>README ↓</a>
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
        <article><h3>Coordinated research</h3><p>Specialized desk-agent roles are designed to gather, synthesize, challenge, and share research across one decision system rather than operate as isolated bots.</p></article>
        <article><h3>Structured decisions</h3><p>Candidates are evaluated through defined research methods, scenarios, documented decision criteria, and a separate portfolio-survival risk state.</p></article>
        <article><h3>Survival discipline</h3><p>Research conviction does not override portfolio-survival controls. Human review remains central, but it does not erase a blocked risk or compliance state.</p></article>
      </div>
      <p class="ws-legal">Emporion is an independent research and software project for structured market review. Users remain responsible for their own decisions, accounts, and implementation choices.</p>
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
    .ws-process{padding:16px 20px;border-top:1px solid #e6eaed;background:#fafbfc}.ws-process-line{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:9px;font:11px 'IBM Plex Mono',monospace;text-transform:uppercase;letter-spacing:.45px;color:#34434c}.ws-process-line i{display:block;width:22px;height:1px;background:#b9c4cb}
    .ws-ror{border-top:1px solid #e6eaed;background:#fff;padding:18px 20px}.ws-ror-grid{display:grid;grid-template-columns:1.2fr 1fr 1fr;margin:10px -20px -18px}.ws-ror-grid article{padding:18px 20px;border-top:1px solid #e6eaed;border-right:1px solid #e6eaed}.ws-ror-grid article:last-child{border-right:0}.ws-ror-grid h2,.ws-ror-grid h3{margin:0 0 8px}.ws-ror-grid h2{font-size:18px}.ws-ror-grid h3{font-size:13px}.ws-ror-grid p{font-size:12px;line-height:1.6;color:#596871;margin:0}
    .ws-continuum{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid #e6eaed}.ws-continuum article{padding:16px 20px;border-right:1px solid #e6eaed}.ws-continuum article:last-child{border-right:0}.ws-continuum strong{display:block;font-size:13px;margin-bottom:6px}.ws-continuum span{display:block;font-size:12px;line-height:1.55;color:#596871}
    .ws-desk-list{border-top:1px solid #e6eaed}.ws-list-head,.ws-list-row{display:grid;grid-template-columns:1fr 180px;align-items:center;padding:11px 18px;border-bottom:1px solid #eef1f3}.ws-list-head{font:10px 'IBM Plex Mono',monospace;letter-spacing:.7px;color:#74818a;text-transform:uppercase;background:#fafbfc}.ws-list-row:last-child{border-bottom:0}.ws-list-row strong{font-size:13px}.ws-state{font:10px 'IBM Plex Mono',monospace;letter-spacing:.45px;color:#52616a}
    .ws-list-row-action{cursor:pointer}.ws-list-row-action:hover{background:#f7f9fa}.ws-list-row-action:focus-visible{outline:2px solid #101820;outline-offset:-2px}
    .ws-desk-openable{cursor:pointer}.ws-desk-openable:hover{background:#f7f9fa}.ws-desk-openable:focus-visible{outline:2px solid #101820;outline-offset:-2px}
    .ws-desk-methods{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}.ws-desk-methods article{padding:22px;border-right:1px solid #e6eaed;border-bottom:1px solid #e6eaed}.ws-desk-methods article:nth-child(2n){border-right:0}.ws-desk-methods article:nth-last-child(-n+2){border-bottom:0}.ws-desk-methods h2{font-size:16px;margin:8px 0}.ws-desk-methods p{font-size:12px;line-height:1.6;color:#596871;min-height:38px}
    .ws-capital-head{padding:19px 21px;border-bottom:1px solid #e6eaed;display:flex;align-items:center;justify-content:space-between;gap:18px}.ws-capital-head h2{margin-top:7px}.ws-brandline{margin:6px 0 0;font:10px 'IBM Plex Mono',monospace;letter-spacing:.6px;color:#6d7a83}.ws-boundary{font:10px 'IBM Plex Mono',monospace;letter-spacing:.7px;background:#f3f5f6;border:1px solid #d8dfe3;padding:7px 9px;border-radius:3px;color:#58666f;white-space:nowrap}
    .ws-capital-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}.ws-capital-grid article{padding:20px 21px;border-right:1px solid #e6eaed;border-bottom:1px solid #e6eaed}.ws-capital-grid article:nth-child(2n){border-right:0}.ws-capital-grid article:nth-last-child(-n+2){border-bottom:0}.ws-capital-grid h3{font-size:14px;margin:0 0 8px}.ws-capital-grid p{font-size:12px;line-height:1.6;color:#596871;margin:0}
    .ws-inspiration-note{font-size:11px!important;color:#75818a!important}.ws-legal{margin:0;padding:14px 21px;background:#101820;color:#cbd4da;font-size:11px;line-height:1.55}
    body[data-route='desks'] #main>.cards{display:none}
    @media(max-width:800px){.ws-overview-grid,.ws-desk-methods,.ws-continuum,.ws-ror-grid{grid-template-columns:1fr}.ws-overview-grid article,.ws-desk-methods article,.ws-continuum article,.ws-ror-grid article{border-right:0;border-bottom:1px solid #e6eaed}.ws-overview-grid article:last-child,.ws-desk-methods article:last-child,.ws-continuum article:last-child,.ws-ror-grid article:last-child{border-bottom:0}.ws-list-head,.ws-list-row{grid-template-columns:1fr}.ws-state{margin-top:5px}.ws-process-line i{width:12px}}
    @media(max-width:650px){.ws-capital-grid{grid-template-columns:1fr}.ws-capital-grid article{border-right:0;border-bottom:1px solid #e6eaed}.ws-capital-grid article:last-child{border-bottom:0}.ws-tape{gap:9px 14px}.ws-tape a{margin-left:0;width:100%}.ws-capital-head{align-items:flex-start;flex-direction:column}}
  `;
  document.head.appendChild(style);
}

// Make the visible desk surfaces open a desk, like app.js's cards do.
//
// This module hides app.js's own desk cards on this route
// (body[data-route='desks'] #main>.cards{display:none}) and substitutes its own
// markup. That substitute was inert, so the only control that opens a desk's
// detail dialog (and from there "Write Yellow Sheet") was the hidden one — i.e.
// unreachable on the Research desks tab. Each visible card/row is wired to the
// real button app.js rendered, matched by the desk name it displays, so no
// project id is guessed. Bonds & Rates has no evaluated research yet, so its
// card goes to the institutional rates sources instead of doing nothing.
function wireDeskRows() {
  const surfaces = [
    ...document.querySelectorAll('#main .ws-desk-methods article'),
    ...document.querySelectorAll('#main .ws-desk-list .ws-list-row'),
  ];
  const openers = [...document.querySelectorAll('#main>.cards button[data-desk]')];
  if (!surfaces.length || !openers.length) return;
  const nameOf = (el) => (el?.textContent || '').trim().toLowerCase();
  // Two surfaces name the same desk differently ("Global Quant & AI Research Lab"
  // in this module's copy vs "Quant / AI Model Lab" on app.js's card), so exact
  // and substring matching both miss it. Significant-token overlap catches that
  // pair without matching distinct desks: "Futures Event" and "Earnings Event"
  // share only the word "event", and the rule needs two.
  const tokens = (text) => new Set(text.split(/[^a-z0-9]+/).filter((t) => t.length > 2));
  const sharesTwoTokens = (a, b) => {
    const ta = tokens(a);
    let hits = 0;
    for (const t of tokens(b)) if (ta.has(t)) hits++;
    return hits >= 2;
  };
  for (const node of surfaces) {
    if (node.dataset.wired === 'true') continue;
    const label = nameOf(node.querySelector('h2') || node.querySelector('strong'));
    if (!label) continue;
    // Bonds & Rates has no evaluated research yet: its card links to the
    // institutional rates sources rather than sitting inert.
    if (label.includes('bonds') && label.includes('rates')) {
      node.dataset.wired = 'true';
      node.classList.add('ws-desk-openable');
      node.setAttribute('role', 'link');
      node.setAttribute('tabindex', '0');
      const go = (event) => {
        event.preventDefault();
        location.hash = '#resources';
      };
      node.addEventListener('click', go);
      node.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') go(event);
      });
      continue;
    }
    const opener = openers.find((button) => {
      const heading = nameOf(button.closest('.desk-card')?.querySelector('h2'));
      if (!heading) return false;
      return heading === label || heading.includes(label) || label.includes(heading)
        || sharesTwoTokens(heading, label);
    });
    if (!opener) continue;
    node.dataset.wired = 'true';
    node.classList.add('ws-desk-openable');
    node.setAttribute('role', 'button');
    node.setAttribute('tabindex', '0');
    const open = (event) => {
      event.preventDefault();
      opener.click();
    };
    node.addEventListener('click', open);
    node.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') open(event);
    });
  }
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
  holder.innerHTML = statusStrip() + desksBlock() + aboutCapitalBlock();
  let cursor = head;
  for (const node of [...holder.children]) {
    cursor.insertAdjacentElement('afterend', node);
    cursor = node;
  }
  wireDeskRows();
}

window.addEventListener('hashchange', () => requestAnimationFrame(renderContext));
window.addEventListener('DOMContentLoaded', () => {
  applyBrand();
  const main = document.querySelector('main');
  if (main) {
    // Deferred: applyBrand runs on every mutation of main and rewrites the
    // footer, sidebar and sidebar copy. That is safe today only because those
    // nodes are siblings of main rather than descendants; observing a broader
    // scope would make it the third instance of this codebase's freeze bug.
    const observer = new MutationObserver(() => requestAnimationFrame(() => {
      applyBrand();
      if (!document.getElementById('wall-street-context')) renderContext();
    }));
    observer.observe(main, {childList:true});
  }
  renderContext();
});