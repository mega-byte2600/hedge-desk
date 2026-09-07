const liveEscape = value => String(value ?? '')
  .replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;').replaceAll("'", '&#39;');

let liveCandidateCache = null;
let liveCandidateInflight = null;

function liveRoute() {
  return (location.hash || '#overview').slice(1).split('?')[0] || 'overview';
}

function liveDate(value) {
  if (!value) return 'Unavailable';
  try {
    return new Date(value).toLocaleString(undefined, {dateStyle: 'medium', timeStyle: 'short'});
  } catch {
    return value;
  }
}

function liveAge(seconds) {
  if (seconds == null) return 'Unavailable';
  const hours = Math.floor(Number(seconds) / 3600);
  if (hours < 1) return '< 1 hour';
  if (hours < 48) return `${hours} hours`;
  return `${Math.floor(hours / 24)} days`;
}

async function fetchLiveCandidates(force = false) {
  if (!force && liveCandidateCache) return liveCandidateCache;
  if (liveCandidateInflight) return liveCandidateInflight;
  liveCandidateInflight = fetch('/api/candidates', {cache: 'no-store'})
    .then(response => {
      if (!response.ok) throw new Error(`Candidate API returned ${response.status}`);
      return response.json();
    })
    .then(payload => {
      if (payload?.mode !== 'RESEARCH_ONLY' || !Array.isArray(payload?.candidates)) {
        throw new Error('Unsupported operational candidate contract');
      }
      if (payload.candidates.some(row => row.trade_authorized !== false)) {
        throw new Error('Candidate contract violated research-only boundary');
      }
      liveCandidateCache = payload;
      return payload;
    })
    .finally(() => { liveCandidateInflight = null; });
  return liveCandidateInflight;
}

function sourceRows(payload) {
  return payload.sources.map(source => `
    <tr>
      <td><strong>${liveEscape(source.provider)}</strong><small>${liveEscape(source.source_id)}</small></td>
      <td>${source.available ? '<span class="live-state ok">AVAILABLE</span>' : '<span class="live-state unavailable">UNAVAILABLE</span>'}</td>
      <td>${liveEscape(source.observed_at ? liveDate(source.observed_at) : '—')}</td>
      <td>${liveEscape(source.age_seconds == null ? '—' : liveAge(source.age_seconds))}</td>
      <td>${liveEscape(source.expected_delay)}</td>
    </tr>`).join('');
}

function candidateRows(payload) {
  return payload.candidates.map(row => {
    const contexts = (row.source_context || []).filter(item => item.available);
    const sourceLabel = row.provider || contexts.map(item => item.provider).join(' + ') || 'Method data pending';
    const asOf = row.observed_at || contexts.map(item => item.observed_at).filter(Boolean).sort().at(-1);
    const delay = row.expected_delay || contexts.map(item => item.expected_delay).filter(Boolean)[0] || 'Not connected';
    const value = row.observed_value == null ? '' : `<small>${liveEscape(row.observed_value)} ${liveEscape(row.observed_unit || '')}</small>`;
    return `
      <tr>
        <td><strong class="mono">${liveEscape(row.symbol)}</strong>${value}<small>${liveEscape(row.instrument_type)}</small></td>
        <td>${liveEscape(row.desk_id.replaceAll('-', ' '))}</td>
        <td><span class="live-state">${liveEscape(row.stage.replaceAll('_', ' '))}</span></td>
        <td>${liveEscape(sourceLabel)}</td>
        <td>${liveEscape(asOf ? liveDate(asOf) : 'Unavailable')}</td>
        <td>${liveEscape(delay)}</td>
      </tr>`;
  }).join('');
}

function liveCandidatesMarkup(payload) {
  const treasury = payload.sources.find(source => source.source_id === 'us-treasury-daily-par-yield-curve');
  const curve = treasury?.available ? Object.entries(treasury.curve || {}).map(([maturity, value]) =>
    `<div class="live-curve-cell"><span>${liveEscape(maturity)}</span><strong>${liveEscape(value)}%</strong></div>`).join('') : '';
  return `
    <section id="live-candidates" class="live-candidates" aria-label="Operational research candidates">
      <div class="live-summary">
        <article><span>DATA STATE</span><strong>${liveEscape(payload.data_state.replaceAll('_', ' '))}</strong><small>Refreshed ${liveEscape(liveDate(payload.generated_at))}</small></article>
        <article><span>SOURCES</span><strong>${payload.sources_available} / ${payload.sources_total}</strong><small>Real public sources reachable</small></article>
        <article><span>PRIORITY</span><strong>Bonds / Rates / Credit</strong><small>Fixed income leads acquisition and context</small></article>
        <article><span>TRADE AUTHORITY</span><strong>None</strong><small>Human final gate remains required</small></article>
      </div>
      ${curve ? `<section class="live-curve"><div class="live-section-head"><div><span>U.S. TREASURY CURVE</span><h2>Official public rates</h2></div><div>${liveEscape(liveDate(treasury.observed_at))}<br><small>${liveEscape(treasury.expected_delay)}</small></div></div><div class="live-curve-grid">${curve}</div></section>` : ''}
      <section class="live-panel">
        <div class="live-section-head">
          <div><span>RESEARCH UNIVERSE</span><h2>Source-enriched candidates</h2></div>
          <button id="refresh-live-data" class="btn">↻ Refresh data</button>
        </div>
        <div class="table-scroll">
          <table><thead><tr><th>Instrument</th><th>Desk</th><th>Stage</th><th>Source context</th><th>As of</th><th>Delay / cadence</th></tr></thead>
          <tbody>${candidateRows(payload)}</tbody></table>
        </div>
        <div class="live-note">Rows are research inputs, not recommendations. A source can enrich a candidate without method-qualifying it. Missing data remains unavailable; no test fixture is substituted.</div>
      </section>
      <section class="live-panel">
        <div class="live-section-head"><div><span>PROVENANCE</span><h2>Operational data sources</h2></div></div>
        <div class="table-scroll"><table><thead><tr><th>Provider</th><th>Status</th><th>Provider as-of</th><th>Age</th><th>Expected delay</th></tr></thead>
        <tbody>${sourceRows(payload)}</tbody></table></div>
      </section>
    </section>`;
}

function installLiveStyle() {
  if (document.getElementById('live-data-style')) return;
  const style = document.createElement('style');
  style.id = 'live-data-style';
  style.textContent = `
    body[data-route='candidates'] #main>.notice,
    body[data-route='candidates'] #main>.stats,
    body[data-route='candidates'] #main>.panel{display:none}
    .live-candidates{display:grid;gap:18px;margin-bottom:28px}
    .live-summary{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border:1px solid #d7dee2;border-radius:6px;background:#fff;overflow:hidden}
    .live-summary article{padding:18px;border-right:1px solid #e7ebee}.live-summary article:last-child{border-right:0}
    .live-summary span,.live-section-head span{font:10px 'IBM Plex Mono',monospace;letter-spacing:.8px;color:#74818a}
    .live-summary strong{display:block;font-size:16px;margin:8px 0 4px}.live-summary small,.live-note,.live-section-head small{color:#6b7780;font-size:11px;line-height:1.5}
    .live-panel,.live-curve{border:1px solid #d7dee2;border-radius:6px;background:#fff;overflow:hidden}
    .live-section-head{display:flex;justify-content:space-between;align-items:center;gap:18px;padding:16px 18px;border-bottom:1px solid #e7ebee}
    .live-section-head h2{font-size:16px;margin:5px 0 0}.live-section-head>div:last-child{text-align:right;color:#52616a;font-size:11px}
    .live-curve-grid{display:grid;grid-template-columns:repeat(10,minmax(60px,1fr));overflow-x:auto}.live-curve-cell{padding:14px;border-right:1px solid #eef1f3;text-align:center}.live-curve-cell:last-child{border-right:0}.live-curve-cell span{display:block;font:10px 'IBM Plex Mono',monospace;color:#74818a}.live-curve-cell strong{display:block;margin-top:6px;font-size:15px}
    .live-note{padding:13px 18px;border-top:1px solid #eef1f3;background:#fafbfc}
    .live-state{font:9px 'IBM Plex Mono',monospace;letter-spacing:.35px;color:#53616a}.live-state.ok{color:#2c6a45}.live-state.unavailable{color:#9d3f3f}
    .live-error{padding:18px;border:1px solid #e5c2c2;background:#fff7f7;border-radius:6px;color:#7d2f2f}
    @media(max-width:900px){.live-summary{grid-template-columns:repeat(2,minmax(0,1fr))}.live-summary article:nth-child(2){border-right:0}.live-summary article:nth-child(-n+2){border-bottom:1px solid #e7ebee}}
    @media(max-width:600px){.live-summary{grid-template-columns:1fr}.live-summary article{border-right:0;border-bottom:1px solid #e7ebee}.live-summary article:last-child{border-bottom:0}.live-section-head{align-items:flex-start;flex-direction:column}.live-section-head>div:last-child{text-align:left}}
  `;
  document.head.appendChild(style);
}

async function renderLiveCandidates(force = false) {
  if (liveRoute() !== 'candidates') return;
  installLiveStyle();
  document.getElementById('live-candidates')?.remove();
  const main = document.querySelector('#main');
  const status = main?.querySelector('#wall-street-context') || main?.querySelector('.page-head');
  if (!main || !status) return;
  const loading = document.createElement('section');
  loading.id = 'live-candidates';
  loading.className = 'live-candidates';
  loading.innerHTML = '<div class="live-panel"><div class="live-note">Loading operational public data…</div></div>';
  status.insertAdjacentElement('afterend', loading);
  try {
    const payload = await fetchLiveCandidates(force);
    if (liveRoute() !== 'candidates') return;
    loading.outerHTML = liveCandidatesMarkup(payload);
    document.getElementById('refresh-live-data')?.addEventListener('click', () => {
      liveCandidateCache = null;
      renderLiveCandidates(true);
    });
  } catch (error) {
    loading.innerHTML = `<div class="live-error"><strong>Operational data unavailable</strong><br>${liveEscape(error.message)}. No substitute data is shown.</div>`;
  }
}

window.addEventListener('hashchange', () => requestAnimationFrame(() => renderLiveCandidates(false)));
window.addEventListener('DOMContentLoaded', () => {
  const main = document.querySelector('#main');
  if (main) {
    new MutationObserver(() => {
      if (liveRoute() === 'candidates' && !document.getElementById('live-candidates')) {
        requestAnimationFrame(() => renderLiveCandidates(false));
      }
    }).observe(main, {childList: true});
  }
  renderLiveCandidates(false);
});
