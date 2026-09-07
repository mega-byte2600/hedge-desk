const RESOURCE_GROUPS = [
  {
    title: 'Rates, Bonds & Monetary Policy',
    note: 'Primary institutional sources first.',
    links: [
      ['New York Fed · Reference Rates', 'https://www.newyorkfed.org/markets/reference-rates', 'SOFR, EFFR, repo reference rates, money-market plumbing, and monetary-policy implementation.'],
      ['U.S. Treasury · Interest Rate Statistics', 'https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics', 'Official Treasury par yield curves, real yield curves, bill rates, and related rate statistics.'],
      ['Federal Reserve Board · Monetary Policy', 'https://www.federalreserve.gov/monetarypolicy.htm', 'FOMC policy statements, implementation information, reports, and official Federal Reserve policy materials.'],
      ['FRED · Federal Reserve Bank of St. Louis', 'https://fred.stlouisfed.org/', 'Macro, rates, credit, inflation, employment, and financial-market time series.'],
      ['FINRA · Fixed Income Data', 'https://www.finra.org/finra-data/fixed-income', 'TRACE and other fixed-income market data for corporate and agency debt research.'],
      ['CME Group · Interest Rates', 'https://www.cmegroup.com/markets/interest-rates.html', 'Treasury, SOFR, Fed Funds, and other listed interest-rate futures and options.']
    ]
  },
  {
    title: 'Filings, Earnings & Fundamental Research',
    note: 'Primary filings and event research.',
    links: [
      ['SEC · EDGAR', 'https://www.sec.gov/search-filings', 'Official U.S. public-company filings, registration statements, ownership forms, and filing search.'],
      ['Earnings Whispers', 'https://www.earningswhispers.com/', 'Earnings calendars, reported results, and expectation-focused event research.'],
      ['Finviz', 'https://finviz.com/', 'Screening, market maps, fundamentals, technical context, and news discovery.']
    ]
  },
  {
    title: 'Macro, Derivatives & Market Structure',
    note: 'Official statistics and exchange-level market context.',
    links: [
      ['BLS · U.S. Bureau of Labor Statistics', 'https://www.bls.gov/', 'Official employment, CPI, PPI, productivity, and labor-market statistics.'],
      ['BEA · U.S. Bureau of Economic Analysis', 'https://www.bea.gov/', 'Official GDP, personal income, consumption, trade, and national accounts.'],
      ['Cboe Global Markets', 'https://www.cboe.com/', 'Options, volatility, index, and market-structure resources.']
    ]
  }
];

function resourceCards(group) {
  return group.links.map(([name, url, description]) => `
    <a class="resource-card" href="${url}" target="_blank" rel="noopener noreferrer">
      <span class="eyebrow">EXTERNAL RESEARCH SOURCE</span>
      <h2>${name}</h2>
      <p>${description}</p>
      <span class="resource-open">Open source ↗</span>
    </a>`).join('');
}

function installResourceStyles() {
  if (document.getElementById('resource-page-style')) return;
  const style = document.createElement('style');
  style.id = 'resource-page-style';
  style.textContent = `
    .resource-intro{margin-bottom:22px}.resource-intro strong{color:#101820}
    .resource-section{margin:0 0 24px}.resource-section-head{margin:0 0 12px}.resource-section-head h2{margin:0 0 4px}.resource-section-head p{margin:0;color:#6b7780;font-size:12px}
    .resource-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
    .resource-card{display:block;padding:20px;border:1px solid #dce2e6;border-radius:6px;background:#fff;color:inherit;text-decoration:none;transition:transform .14s ease,border-color .14s ease,box-shadow .14s ease}
    .resource-card:hover{transform:translateY(-1px);border-color:#9aa8b1;box-shadow:0 4px 14px rgba(16,24,32,.06)}
    .resource-card h2{font-size:16px;margin:8px 0 8px}.resource-card p{font-size:12px;line-height:1.6;color:#596871;margin:0 0 16px}.resource-open{font:10px 'IBM Plex Mono',monospace;letter-spacing:.45px;color:#334a5c;text-transform:uppercase}
    .resource-disclaimer{margin-top:6px;padding:14px 16px;border:1px solid #e2e6e9;border-radius:5px;background:#fafbfc;color:#6b7780;font-size:11px;line-height:1.55}
    @media(max-width:760px){.resource-grid{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);
}

function renderResources() {
  const main = document.getElementById('main');
  if (!main) return;
  if (location.hash !== '#resources') {
    delete main.dataset.resourcePage;
    return;
  }
  if (main.querySelector('.resource-page-root')) return;
  main.dataset.resourcePage = 'true';
  installResourceStyles();
  document.querySelectorAll('[data-nav]').forEach(link => {
    const active = link.dataset.nav === 'resources';
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'page'); else link.removeAttribute('aria-current');
  });
  const breadcrumb = document.getElementById('breadcrumb');
  if (breadcrumb) breadcrumb.textContent = 'Research resources';
  main.innerHTML = `<div class="resource-page-root">
    <div class="page-head"><div><h1>Research resources</h1><p class="subtitle">Institutional sources, market infrastructure, and selected research tools used to orient Emporion research.</p></div></div>
    <div class="notice resource-intro"><strong>PRIMARY-SOURCE FIRST</strong><span>For rates, bonds, policy, filings, and macro data, start with the institution that produces or administers the underlying information.</span></div>
    ${RESOURCE_GROUPS.map(group => `
      <section class="resource-section">
        <div class="resource-section-head"><h2>${group.title}</h2><p>${group.note}</p></div>
        <div class="resource-grid">${resourceCards(group)}</div>
      </section>`).join('')}
    <div class="resource-disclaimer">External resources are provided for research convenience. Inclusion does not imply affiliation, endorsement, sponsorship, or that Emporion relies on any source for investment advice or trade authorization.</div>
  </div>`;
}

window.addEventListener('hashchange', () => requestAnimationFrame(renderResources));
window.addEventListener('DOMContentLoaded', () => {
  const main = document.getElementById('main');
  if (main) {
    new MutationObserver(() => requestAnimationFrame(renderResources)).observe(main, {childList:true});
  }
  requestAnimationFrame(renderResources);
});
