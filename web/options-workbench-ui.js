// Options Workbench — DOM layer. Exports mountWorkbench(host).
// Pure logic lives in options-workbench.mjs; this file only renders it.
// No trade execution: the seed's trade_authorized=false is enforced here and
// the Risk of Ruin gate is a confirm-only step — this tool never calculates,
// estimates, infers, modifies, or substitutes for it.
import * as W from './options-workbench.mjs';

const $ = (tag, cls, text) => {
  const el = document.createElement(tag);
  if (cls) el.className = cls;
  if (text !== undefined && text !== null) el.textContent = text;
  return el;
};

const chip = (text, kind) => $('span', `wb-chip${kind ? ' wb-chip-' + kind : ''}`, text);

const SOURCE_NOTE = 'source: Cboe delayed chain';

/** Figure caption: names the data batch and flags scenario math. */
function figCap(seed, scenarioActive, extra) {
  const p = $('p', 'wb-figcap');
  p.appendChild(chip(`batch · ${seed.asOfLabel}`, 'batch'));
  if (scenarioActive) p.appendChild(chip('scenario — hypothetical projection from real base data', 'scenario'));
  p.appendChild($('span', 'wb-src', `${SOURCE_NOTE}${extra ? ' · ' + extra : ''}`));
  return p;
}

let plotlyPromise = null;
/** GAP-3: the pinned local plotly is the only chart path; if it fails to
 *  load, panels read "data unavailable — chart library failed to load". */
async function ensurePlotly() {
  if (window.Plotly) return window.Plotly;
  if (!plotlyPromise) {
    plotlyPromise = import('./vendor/plotly-2.35.2.min.js').then(
      () => window.Plotly,
      () => null,
    );
  }
  return plotlyPromise;
}

async function plot(container, data, layout, seed, scenarioActive, extra) {
  container.innerHTML = '';
  const box = $('div', 'wb-plot');
  container.appendChild(box);
  const P = await ensurePlotly();
  if (!P) {
    box.appendChild($('p', 'wb-unavail', W.unavailable(W.REASON_CHART_LIB_FAILED)));
    container.appendChild(figCap(seed, scenarioActive, extra));
    return;
  }
  const base = {
    margin: { l: 52, r: 12, t: 8, b: 40 },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { size: 11 },
    xaxis: { gridcolor: 'rgba(128,128,128,.25)' },
    yaxis: { gridcolor: 'rgba(128,128,128,.25)' },
    showlegend: false,
  };
  await P.newPlot(box, data, { ...base, ...layout }, { responsive: true, displayModeBar: false });
  container.appendChild(figCap(seed, scenarioActive, extra));
}

function renderTable(container, headers, rows, seed, scenarioActive, extra) {
  const table = $('table', 'wb-table');
  const thead = $('thead');
  const hr = $('tr');
  for (const h of headers) hr.appendChild($('th', '', h));
  thead.appendChild(hr);
  table.appendChild(thead);
  const tb = $('tbody');
  for (const r of rows) {
    const tr = $('tr');
    for (const c of r) {
      const td = $('td');
      if (typeof c === 'string' && c.startsWith('−')) td.className = 'neg';
      if (typeof c === 'string' && c.startsWith('+') && c !== '+100 shares') td.className = 'pos';
      td.textContent = c;
      tr.appendChild(td);
    }
    tb.appendChild(tr);
  }
  table.appendChild(tb);
  container.appendChild(table);
  container.appendChild(figCap(seed, scenarioActive, extra));
}

/**
 * Mount the workbench into `host`. State machine:
 * loading -> batch | stale -> seed facts + modeled panels
 *         -> missing (data unavailable — seed endpoint unreachable)
 */
/** Guide tab panel: the consolidated Options Guide (was a standalone page). */
function guidePanel() {
  const box = $('div', 'wb-card');
  box.appendChild($('h3', '', 'Selling options premium — visual guide'));
  const dl = document.createElement('a');
  dl.href = '/guide/selling-options-premium';
  dl.download = 'selling-options-premium-guide.html';
  dl.className = 'wb-download';
  dl.textContent = 'Download guide';
  box.appendChild(dl);
  const shell = $('div', 'frame-shell');
  const skel = $('div', 'skeleton');
  skel.setAttribute('aria-hidden', 'true');
  shell.appendChild(skel);
  const frame = document.createElement('iframe');
  frame.className = 'autofit-frame guide-frame';
  frame.setAttribute('data-autofit', '');
  frame.src = '/guide/selling-options-premium';
  frame.title = 'Selling options premium guide';
  shell.appendChild(frame);
  box.appendChild(shell);
  return box;
}

export function mountWorkbench(host) {
  host.innerHTML = '';
  const root = $('section', 'wb');
  root.appendChild($('h2', 'wb-title', 'Options Workbench'));

  // Top-level tabs: Workbench | Guide. The standalone Options Guide page
  // was consolidated here (less is more): same content, one fewer page.
  const tabBar = $('div', 'wb-tabs wb-toptabs');
  const btnWb = $('button', 'wb-tab active', 'Workbench');
  const btnGuide = $('button', 'wb-tab', 'Guide');
  btnWb.type = 'button';
  btnGuide.type = 'button';
  btnWb.setAttribute('aria-pressed', 'true');
  btnGuide.setAttribute('aria-pressed', 'false');
  tabBar.appendChild(btnWb);
  tabBar.appendChild(btnGuide);
  root.appendChild(tabBar);

  const wbWrap = $('div', 'wb-workbench-panel');
  const guideWrap = $('div', 'wb-guide-panel');
  guideWrap.hidden = true;
  guideWrap.appendChild(guidePanel());
  root.appendChild(wbWrap);
  root.appendChild(guideWrap);
  host.appendChild(root);

  const selectTab = (which) => {
    const wb = which === 'wb';
    btnWb.classList.toggle('active', wb);
    btnGuide.classList.toggle('active', !wb);
    btnWb.setAttribute('aria-pressed', wb ? 'true' : 'false');
    btnGuide.setAttribute('aria-pressed', wb ? 'false' : 'true');
    wbWrap.hidden = !wb;
    guideWrap.hidden = wb;
  };
  btnWb.addEventListener('click', () => selectTab('wb'));
  btnGuide.addEventListener('click', () => selectTab('guide'));

  const stateLine = $('div', 'wb-state');
  stateLine.appendChild(chip('loading…', 'loading'));
  wbWrap.appendChild(stateLine);
  const body = $('div', 'wb-body');
  wbWrap.appendChild(body);

  fetch('./api/options-seed', { headers: { accept: 'application/json' } })
    .then(async (res) => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then((raw) => {
      const v = W.validateSeed(raw);
      if (!v.ok) {
        stateLine.innerHTML = '';
        stateLine.appendChild(chip(W.unavailable(W.REASON_SEED_SCHEMA_INVALID), 'missing'));
        body.appendChild($('p', 'wb-unavail', v.errors.join('; ')));
        return;
      }
      const seed = W.parseSeed(raw);
      renderWorkbench(stateLine, body, seed);
    })
    .catch(() => {
      stateLine.innerHTML = '';
      stateLine.appendChild(chip(W.unavailable(W.REASON_SEED_ENDPOINT_UNREACHABLE), 'missing'));
    });
}

function batchChip(seed) {
  const stale = W.isStaleSeed(seed);
  const text = stale
    ? `batch · ${seed.asOfLabel} — stale, refresh pending`
    : `batch · ${seed.asOfLabel}`;
  return chip(text, stale ? 'stale' : 'batch');
}

function scenarioState(seed) {
  return {
    ratePct: 5.29, // scenario input: the seed carries no rate field; marked hypothetical
    ivPct: seed.ivPct,
    target: seed.spot,
    exercise: 'american',
  };
}

function currentSt(seed, sc) {
  return {
    spot: seed.spot,
    strike: seed.strike,
    days: seed.dte,
    ivPct: sc.ivPct,
    rate: sc.ratePct / 100,
    exercise: sc.exercise,
    premium: seed.mid,
  };
}

const scenarioActive = (seed, sc) =>
  Math.abs(sc.ivPct - seed.ivPct) > 1e-9 ||
  Math.abs(sc.target - seed.spot) > 1e-9 ||
  sc.exercise !== 'american' ||
  true; // rate is always a hypothetical scenario input

function renderWorkbench(stateLine, body, seed) {
  stateLine.innerHTML = '';
  stateLine.appendChild(batchChip(seed));

  const dteMsg = W.dteGuard(seed.dte);
  if (seed.dte > W.MAX_DTE) {
    body.appendChild($('p', 'wb-unavail', dteMsg));
    body.appendChild(seedFacts(seed, { ratePct: 5.29 }));
    return;
  }

  const sc = scenarioState(seed);

  body.appendChild(seedFacts(seed, sc));
  body.appendChild(scenarioControls(seed, sc, () => refresh(body, seed, sc)));
  const main = $('div', 'wb-main');
  body.appendChild(main);
  refresh(main, seed, sc);
}

function refresh(main, seed, sc) {
  main.innerHTML = '';
  const st = currentSt(seed, sc);
  const sa = scenarioActive(seed, sc);
  main.appendChild(strategySection(seed, st, sa));
  main.appendChild(rollSection(seed, st, sa));
  main.appendChild(harvestSection(seed, st, sa));
  main.appendChild(probSection(seed, st, sa));
  main.appendChild(outlookSection(seed, st, sa));
  main.appendChild(riskSection(seed, st, sa));
  main.appendChild(rorGate());
}

function seedFacts(seed, sc) {
  const box = $('div', 'wb-card');
  box.appendChild($('h3', '', `${seed.symbol} ${seed.strike} ${seed.optionType} · expires ${seed.expiration}`));
  const facts = $('dl', 'wb-facts');
  const add = (k, v) => {
    facts.appendChild($('dt', '', k));
    facts.appendChild($('dd', '', v));
  };
  add('Spot', `${W.fmtMoney(seed.spot, 2)} (bid ${W.fmtMoney(seed.spotBid ?? seed.spot, 2)} / ask ${W.fmtMoney(seed.spotAsk ?? seed.spot, 2)})`);
  add('Quote', `bid ${W.fmtMoney(seed.bid, 2)} · ask ${W.fmtMoney(seed.ask, 2)} · mid ${W.fmtMoney(seed.mid, 2)}`);
  add('Contract', seed.contractId);
  add('Implied vol', `${seed.ivPct.toFixed(2)}%`);
  add('DTE', String(seed.dte));
  if (seed.greeks.delta !== null) {
    add('Seed Greeks', `Δ ${seed.greeks.delta} · Γ ${seed.greeks.gamma} · Θ ${seed.greeks.theta} · Vega ${seed.greeks.vega} · ρ ${seed.greeks.rho}`);
  }
  add('Open interest / volume', `${seed.oi ?? '—'} / ${seed.volume ?? '—'}`);
  add('Data', `${seed.sourceLabel} · ${seed.dataMode} · as of ${seed.asOfLabel}`);
  box.appendChild(facts);
  const cap = $('p', 'wb-figcap');
  cap.appendChild(chip(`batch · ${seed.asOfLabel}`, 'batch'));
  cap.appendChild($('span', 'wb-src', SOURCE_NOTE));
  box.appendChild(cap);
  return box;
}

function labeledNumber(label, value, step, onChange, note) {
  const wrap = $('label', 'wb-ctl');
  wrap.appendChild($('span', 'wb-ctl-label', label));
  const input = document.createElement('input');
  input.type = 'number';
  input.value = String(value);
  input.step = String(step);
  input.addEventListener('input', () => {
    const v = Number(input.value);
    if (isFinite(v)) onChange(v);
  });
  wrap.appendChild(input);
  if (note) wrap.appendChild($('small', 'wb-ctl-note', note));
  return wrap;
}

function scenarioControls(seed, sc, onChange) {
  const box = $('div', 'wb-card');
  box.appendChild($('h3', '', 'Scenario controls'));
  box.appendChild($('p', 'wb-note', 'Sliders and fields below are hypothetical: they project from the real seed data and never change it.'));
  const grid = $('div', 'wb-ctls');
  grid.appendChild(labeledNumber('Rate (%)', sc.ratePct, 0.25, (v) => { sc.ratePct = v; onChange(); },
    'hypothetical — the seed carries no rate field'));
  grid.appendChild(labeledNumber('IV override (%)', sc.ivPct, 0.5, (v) => { sc.ivPct = v; onChange(); },
    `seed IV ${seed.ivPct.toFixed(2)}%`));
  grid.appendChild(labeledNumber('Target price ($)', sc.target, 5, (v) => { sc.target = v; onChange(); },
    `seed spot ${W.fmtMoney(seed.spot, 2)}`));
  const exWrap = $('label', 'wb-ctl');
  exWrap.appendChild($('span', 'wb-ctl-label', 'Exercise'));
  const sel = document.createElement('select');
  for (const [v, t] of [['american', 'American'], ['european', 'European']]) {
    const o = document.createElement('option');
    o.value = v;
    o.textContent = t;
    sel.appendChild(o);
  }
  sel.value = sc.exercise;
  sel.addEventListener('change', () => { sc.exercise = sel.value; onChange(); });
  exWrap.appendChild(sel);
  exWrap.appendChild($('small', 'wb-ctl-note', 'American = max(hold, intrinsic) at every node'));
  grid.appendChild(exWrap);
  box.appendChild(grid);
  return box;
}

function strategySection(seed, st, sa) {
  const box = $('div', 'wb-card');
  box.appendChild($('h3', '', 'Strategy balance sheets'));
  const tabs = $('div', 'wb-tabs');
  const panel = $('div', 'wb-tabpanel');
  const keys = Object.keys(W.STRATEGIES);
  let active = 'put';
  const buttons = {};
  for (const k of keys) {
    const b = $('button', 'wb-tab', W.STRATEGIES[k]);
    b.type = 'button';
    b.setAttribute('aria-pressed', k === active ? 'true' : 'false');
    b.addEventListener('click', () => {
      active = k;
      for (const [kk, bb] of Object.entries(buttons)) {
        bb.classList.toggle('active', kk === active);
        bb.setAttribute('aria-pressed', kk === active ? 'true' : 'false');
      }
      renderStrategyTab(panel, seed, st, sa, active);
    });
    buttons[k] = b;
    tabs.appendChild(b);
  }
  buttons[active].classList.add('active');
  box.appendChild(tabs);
  box.appendChild(panel);
  renderStrategyTab(panel, seed, st, sa, active);
  return box;
}

function econRow(k, v) {
  const d = $('div', 'wb-econ');
  d.appendChild($('dt', '', k));
  d.appendChild($('dd', '', v));
  return d;
}

function renderStrategyTab(panel, seed, st, sa, key) {
  panel.innerHTML = '';
  const m = W.strategyModel(key, st);
  panel.appendChild($('h4', '', m.name));

  const econ = $('dl', 'wb-econgrid');
  econ.appendChild(econRow('Premium / contract', W.fmtMoney(m.premiumPerContract)));
  econ.appendChild(econRow('Max profit', W.fmtMoney(m.maxProfit)));
  econ.appendChild(econRow('Max loss', `${W.fmtMoney(m.maxLoss)}${m.lossDefined ? ' (defined)' : ' (open-ended)'}`));
  econ.appendChild(econRow('Breakeven(s)', m.breakevens.map((b) => W.fmtMoney(b, 2)).join(' · ')));
  econ.appendChild(econRow('Encumbered capital', W.fmtMoney(m.encumberedCapital)));
  econ.appendChild(econRow('Assignment', `${m.assignmentShares} · ${m.assignmentCash}`));
  econ.appendChild(econRow('Cost basis', m.costBasis));
  econ.appendChild(econRow('Greeks (position)', `Δ ${m.greeks.delta.toFixed(0)} · Γ ${m.greeks.gamma.toFixed(3)} · Θ ${W.fmtMoney(m.greeks.theta)}/day · Vega ${W.fmtMoney(m.greeks.vega)}/pt`));
  panel.appendChild(econ);

  const bs = $('div', 'wb-bs');
  const assets = $('div', 'wb-bs-col');
  assets.appendChild($('h5', '', 'Assets'));
  for (const a of m.assets) assets.appendChild($('p', '', `${a.label}: ${a.text}`));
  const liabs = $('div', 'wb-bs-col');
  liabs.appendChild($('h5', '', 'Liabilities'));
  for (const l of m.liabilities) liabs.appendChild($('p', '', `${l.label}: ${l.text}`));
  bs.appendChild(assets);
  bs.appendChild(liabs);
  panel.appendChild(bs);
  panel.appendChild($('p', 'wb-note', m.riskNote));
  panel.appendChild($('p', 'wb-note', 'Encumbrance tags: ' + m.encTags.join(', ')));

  // P&L at expiry chart
  const pnlBox = $('div', 'wb-fig');
  pnlBox.appendChild($('h5', '', 'P&L at expiry'));
  panel.appendChild(pnlBox);
  plot(pnlBox, pnlTraces(m, st), { yaxis: { title: 'P&L ($)' } }, seed, sa, m.name).catch(() => {});

  // Time value vs spot chart
  const tvBox = $('div', 'wb-fig');
  tvBox.appendChild($('h5', '', 'Time value across spot (short-put wing)'));
  panel.appendChild(tvBox);
  plot(tvBox, tvTraces(st), { yaxis: { title: 'Time value ($/contract)' } }, seed, sa, m.name).catch(() => {});

  // Decay chart
  const decBox = $('div', 'wb-fig');
  decBox.appendChild($('h5', '', 'Value decay to expiry (flat spot, flat IV)'));
  panel.appendChild(decBox);
  plot(decBox, decayTraces(m, st), { yaxis: { title: 'Position value ($)' }, xaxis: { title: 'DTE' } }, seed, sa, m.name).catch(() => {});

  // Theta chart
  const thBox = $('div', 'wb-fig');
  thBox.appendChild($('h5', '', 'Daily theta across spot (position)'));
  panel.appendChild(thBox);
  plot(thBox, thetaTraces(m, st), { yaxis: { title: 'Theta ($/day)' } }, seed, sa, m.name).catch(() => {});

  // Stress grid
  const sg = $('div', 'wb-fig');
  sg.appendChild($('h5', '', 'Stress grid'));
  panel.appendChild(sg);
  const { rows, stressedLoss } = W.stressGrid(m, st);
  renderTable(sg, ['State', 'P&L', 'Share state'], rows.map((r) => [r.state, W.fmtSigned(Math.round(r.pnl)), r.shares]), seed, sa, m.name);
  sg.appendChild($('p', 'wb-note', `Stressed loss (worst of the first seven rows): ${W.fmtSigned(Math.round(stressedLoss))}`));

  // Scenario heatmap
  const hmBox = $('div', 'wb-fig');
  hmBox.appendChild($('h5', '', 'Scenario grid — modeled P&L per contract'));
  panel.appendChild(hmBox);
  const g = W.scenarioGridData(st);
  plot(hmBox, [{
    type: 'heatmap', x: g.x, y: g.y, z: g.z, colorscale: 'RdYlGn', zmid: 0,
    hovertemplate: '%{y} · %{x}<br>%{z:$.0f}<extra></extra>',
  }], { xaxis: { tickangle: -30 } }, seed, sa, m.name).catch(() => {});
}

function pnlTraces(m, st) {
  const n = 60;
  const xs = [];
  const ys = [];
  for (let i = 0; i <= n; i++) {
    const s = st.spot * (0.7 + (0.6 * i) / n);
    xs.push(s);
    ys.push(m.expiryPnl(s));
  }
  const traces = [{
    x: xs, y: ys, type: 'scatter', mode: 'lines', line: { width: 2 },
    hovertemplate: 'spot %{x:$.0f}<br>P&L %{y:$.0f}<extra></extra>',
  }];
  for (const b of m.breakevens) {
    traces.push({
      x: [b, b], y: [Math.min(...ys), Math.max(...ys)], type: 'scatter', mode: 'lines',
      line: { dash: 'dot', color: '#888' }, hovertemplate: `breakeven ${W.fmtMoney(b, 2)}<extra></extra>`,
    });
  }
  traces.push({
    x: [st.spot, st.spot], y: [Math.min(...ys), Math.max(...ys)], type: 'scatter', mode: 'lines',
    line: { dash: 'dash', color: '#4a90d9' }, hovertemplate: `current spot ${W.fmtMoney(st.spot, 2)}<extra></extra>`,
  });
  return traces;
}

function tvTraces(st) {
  const n = 50;
  const xs = [];
  const ys = [];
  for (let i = 0; i <= n; i++) {
    const s = st.spot * (0.7 + (0.6 * i) / n);
    xs.push(s);
    ys.push((W.pricePut(s, st.strike, st.days, st.ivPct, st.rate, st.exercise) - Math.max(st.strike - s, 0)) * 100);
  }
  return [{ x: xs, y: ys, type: 'scatter', mode: 'lines', line: { width: 2 }, hovertemplate: 'spot %{x:$.0f}<br>TV %{y:$.0f}<extra></extra>' }];
}

function decayTraces(m, st) {
  const xs = [];
  const ys = [];
  for (let d = st.days; d >= 0; d -= 1) {
    xs.push(d);
    ys.push(m.markShift(st.spot, d, st.ivPct));
  }
  return [{ x: xs, y: ys, type: 'scatter', mode: 'lines', line: { width: 2 }, hovertemplate: '%{x} DTE<br>%{y:$.0f}<extra></extra>' }];
}

function thetaTraces(m, st) {
  const n = 40;
  const xs = [];
  const ys = [];
  for (let i = 0; i <= n; i++) {
    const s = st.spot * (0.8 + (0.4 * i) / n);
    xs.push(s);
    ys.push(positionThetaAt(m, st, s));
  }
  return [{ x: xs, y: ys, type: 'scatter', mode: 'lines', line: { width: 2 }, hovertemplate: 'spot %{x:$.0f}<br>theta %{y:$.0f}/day<extra></extra>' }];
}

function positionThetaAt(m, st, s) {
  const legs = [];
  const gPut = (kk) => W.modelGreeksPut(s, kk, st.days, st.ivPct, st.rate, st.exercise).thetaDay;
  const gCall = (kk) => W.modelGreeksCall(s, kk, st.days, st.ivPct, st.rate, st.exercise).thetaDay;
  switch (m.key) {
    case 'put':
    case 'naked':
      return -gPut(st.strike);
    case 'call':
      return -gCall(m.Kc);
    case 'strangle':
      return -gPut(st.strike) - gCall(m.Kc);
    case 'spread':
      return -gPut(st.strike) + gPut(m.Kl);
    default:
      return 0;
  }
}

function rollSection(seed, st, sa) {
  const box = $('div', 'wb-card');
  box.appendChild($('h3', '', 'Roll plan'));
  const plan = W.rollPlan(st);
  const econ = $('dl', 'wb-econgrid');
  econ.appendChild(econRow('Close trigger', `${plan.trigger} DTE (after ~${plan.elapsed} days held)`));
  econ.appendChild(econRow('Close cost', W.fmtMoney(plan.closeCost, 2)));
  econ.appendChild(econRow('Fresh 30-day put', `${W.fmtMoney(plan.newStrike)} strike`));
  econ.appendChild(econRow('New credit', W.fmtMoney(plan.newCredit, 2)));
  econ.appendChild(econRow('Net roll credit', W.fmtMoney(plan.net, 2)));
  econ.appendChild(econRow('New breakeven', W.fmtMoney(plan.newBreakeven, 2)));
  econ.appendChild(econRow('Capital at risk', W.fmtMoney(plan.capitalAtRisk)));
  econ.appendChild(econRow('Roll yield', `${plan.yieldPct.toFixed(2)}% (${plan.annualized.toFixed(1)}% annualized)`));
  box.appendChild(econ);
  box.appendChild($('p', 'wb-note', 'Close at 21 DTE, then sell a fresh 30-day put at the same moneyness. Flat spot, flat IV — a scenario, not a forecast.'));
  const fig = $('div', 'wb-fig');
  box.appendChild(fig);
  plot(fig, [{
    type: 'bar', x: ['Close cost', 'New credit', 'Net'],
    y: [-plan.closeCost, plan.newCredit, plan.net],
    marker: { color: ['#d9534f', '#5cb85c', '#4a90d9'] },
    hovertemplate: '%{x}: %{y:$.2f}<extra></extra>',
  }], { yaxis: { title: 'Dollars' } }, seed, sa, 'roll plan').catch(() => {});
  return box;
}

function harvestSection(seed, st, sa) {
  const box = $('div', 'wb-card');
  box.appendChild($('h3', '', 'Harvest model — continuous premium capture'));
  let targetPct = 50;
  let stress = 'none';
  const ctls = $('div', 'wb-ctls');
  const pctWrap = $('label', 'wb-ctl');
  pctWrap.appendChild($('span', 'wb-ctl-label', 'Profit target (%)'));
  const pctSel = document.createElement('select');
  for (const v of [25, 50, 75]) {
    const o = document.createElement('option');
    o.value = String(v);
    o.textContent = `${v}%`;
    pctSel.appendChild(o);
  }
  pctSel.value = String(targetPct);
  pctWrap.appendChild(pctSel);
  ctls.appendChild(pctWrap);
  const stWrap = $('label', 'wb-ctl');
  stWrap.appendChild($('span', 'wb-ctl-label', 'Stress path'));
  const stSel = document.createElement('select');
  for (const [v, t] of [['none', 'None'], ['m5', '−5% drift'], ['m10', '−10% drift']]) {
    const o = document.createElement('option');
    o.value = v;
    o.textContent = t;
    stSel.appendChild(o);
  }
  stWrap.appendChild(stSel);
  ctls.appendChild(stWrap);
  box.appendChild(ctls);
  const out = $('div', 'wb-fig');
  box.appendChild(out);

  const render = () => {
    out.innerHTML = '';
    const h = W.harvestModel(st, targetPct, stress);
    const econ = $('dl', 'wb-econgrid');
    econ.appendChild(econRow('Buy-back day', h.reached ? `day ${h.tStar}` : `not reached — hold to expiry (day ${h.tStar})`));
    econ.appendChild(econRow('Net per cycle', W.fmtMoney(h.perCycle, 2)));
    econ.appendChild(econRow('Cycles / year', h.cycles.toFixed(1)));
    econ.appendChild(econRow('Stacked premium', W.fmtMoney(h.stack, 2)));
    econ.appendChild(econRow('Gross debits paid', W.fmtMoney(h.debits, 2)));
    econ.appendChild(econRow('Yield on strike capital', `${h.yieldPct.toFixed(2)}%`));
    if (h.stressed !== null) econ.appendChild(econRow('Stressed stack', W.fmtMoney(h.stressed, 2)));
    out.appendChild(econ);
    const n = Math.min(Math.ceil(h.cycles), 12);
    const xs = [];
    const ys = [];
    for (let i = 1; i <= n; i++) {
      xs.push(`Cycle ${i}`);
      ys.push(h.perCycle * i);
    }
    plot(out, [{
      type: 'bar', x: xs, y: ys, marker: { color: '#4a90d9' },
      hovertemplate: '%{x}<br>cumulative %{y:$.0f}<extra></extra>',
    }], { yaxis: { title: 'Cumulative captured premium ($)' } }, seed, sa, `harvest target ${targetPct}%`).catch(() => {});
  };
  pctSel.addEventListener('change', () => { targetPct = Number(pctSel.value); render(); });
  stSel.addEventListener('change', () => { stress = stSel.value; render(); });
  render();
  return box;
}

function probSection(seed, st, sa) {
  const box = $('div', 'wb-card');
  box.appendChild($('h3', '', 'Probability framework'));
  const p = W.probabilityFrame(st);
  const econ = $('dl', 'wb-econgrid');
  econ.appendChild(econRow('P(full premium)', `${(p.popFull * 100).toFixed(1)}%`));
  econ.appendChild(econRow('P(assignment)', `${(p.popAssign * 100).toFixed(1)}%`));
  econ.appendChild(econRow('Expected move (1σ)', `${W.fmtMoney(p.expectedMove, 2)} over ${st.days} days`));
  econ.appendChild(econRow('50%-profit target day', p.targetDays === null ? 'not reached in window' : `day ${p.targetDays}`));
  econ.appendChild(econRow('Delta-implied assignment odds', `${(p.deltaImplied * 100).toFixed(1)}%`));
  econ.appendChild(econRow('+2σ price', W.fmtMoney(p.plus2Sigma, 2)));
  econ.appendChild(econRow('Downside cushion to strike', W.fmtMoney(p.cushion, 2)));
  box.appendChild(econ);
  box.appendChild($('p', 'wb-note', 'Odds are backed out of the option’s own IV — a risk-neutral market quote, not a forecast of where the stock goes.'));
  if (seed.dailyHistory) {
    const wc = W.windowContingent(seed.dailyHistory);
    const wbox = $('div', 'wb-iv');
    wbox.appendChild($('h5', '', 'IV vs realized'));
    wbox.appendChild($('p', '', `Realized vol (window): ${wc.realizedVol !== null ? (wc.realizedVol * 100).toFixed(1) + '%' : '—'} · IV: ${st.ivPct.toFixed(2)}%`));
    if (wc.windowContingent) {
      wbox.appendChild($('p', 'wb-warn', `WINDOW-CONTINGENT — one day drives ${(wc.maxDayShare * 100).toFixed(0)}% of realized variance; the verdict depends on that day.`));
    } else {
      wbox.appendChild($('p', 'wb-note', 'No single day dominates the window.'));
    }
    box.appendChild(wbox);
  } else {
    box.appendChild($('p', 'wb-unavail', W.unavailable(W.REASON_NO_DAILY_HISTORY)));
  }
  const fig = $('div', 'wb-fig');
  fig.appendChild($('h5', '', 'Terminal price density (IV-implied)'));
  box.appendChild(fig);
  const sigma = p.expectedMove;
  const xs = [];
  const ys = [];
  for (let i = 0; i <= 80; i++) {
    const x = st.spot - 4 * sigma + (8 * sigma * i) / 80;
    xs.push(x);
    ys.push(Math.exp(-((x - st.spot) ** 2) / (2 * sigma * sigma)));
  }
  plot(fig, [
    { x: xs, y: ys, type: 'scatter', mode: 'lines', fill: 'tozeroy', line: { width: 2 }, hovertemplate: 'price %{x:$.0f}<extra></extra>' },
    { x: [st.strike, st.strike], y: [0, 1], type: 'scatter', mode: 'lines', line: { dash: 'dot', color: '#d9534f' }, hovertemplate: `strike ${W.fmtMoney(st.strike)}<extra></extra>` },
    { x: [st.spot, st.spot], y: [0, 1], type: 'scatter', mode: 'lines', line: { dash: 'dash', color: '#4a90d9' }, hovertemplate: `spot ${W.fmtMoney(st.spot, 2)}<extra></extra>` },
  ], { yaxis: { visible: false }, xaxis: { title: 'Price at expiry' } }, seed, sa, 'IV-implied density').catch(() => {});
  return box;
}

function outlookSection(seed, st, sa) {
  const box = $('div', 'wb-card');
  box.appendChild($('h3', '', 'Trade optimizer — structure ranking'));
  const wrap = $('label', 'wb-ctl');
  wrap.appendChild($('span', 'wb-ctl-label', 'Market outlook'));
  const sel = document.createElement('select');
  for (const [v, t] of Object.entries(W.OUTLOOKS)) {
    const o = document.createElement('option');
    o.value = v;
    o.textContent = t;
    sel.appendChild(o);
  }
  box.appendChild(wrap);
  wrap.appendChild(sel);
  const list = $('ol', 'wb-rank');
  box.appendChild(list);
  const render = () => {
    list.innerHTML = '';
    for (const c of W.structureRanking(sel.value, st)) {
      const li = $('li', c.isCash ? 'wb-rank-cash' : '');
      li.appendChild($('strong', '', `#${c.rank} — ${c.title}`));
      li.appendChild($('p', '', c.note));
      li.appendChild($('p', 'wb-note', `Credit ${W.fmtMoney(c.credit, 2)} · ${c.basis} · keeps premium ${c.retention}`));
      list.appendChild(li);
    }
    list.appendChild(figCap(seed, sa, 'structure ranking'));
  };
  sel.addEventListener('change', render);
  render();
  return box;
}

function riskSection(seed, st, sa) {
  const box = $('div', 'wb-card');
  box.appendChild($('h3', '', 'Available risk capital & utilization'));
  box.appendChild($('p', 'wb-note', 'Your inputs — hypothetical scenario. Buying power is an execution constraint only; it never enters the ARC formula.'));
  const inputs = { nlv: 250000, reserved: 50000, stressReserves: 25000, contingentExposure: 0 };
  const ctls = $('div', 'wb-ctls');
  const out = $('div', 'wb-fig');
  const render = () => {
    out.innerHTML = '';
    const model = W.strategyModel('put', st);
    const { stressedLoss } = W.stressGrid(model, st);
    const r = W.riskCapitalUtilization({
      ...inputs,
      encumberedCapital: model.encumberedCapital,
      stressedTradeLoss: stressedLoss,
    });
    const econ = $('dl', 'wb-econgrid');
    econ.appendChild(econRow('ARC before', W.fmtMoney(r.arcBefore)));
    econ.appendChild(econRow('ARC after (reserving the put)', W.fmtMoney(r.arcAfter)));
    econ.appendChild(econRow('RCU before', r.rcuBefore === null ? '— (no available capital)' : `${(r.rcuBefore * 100).toFixed(1)}%`));
    econ.appendChild(econRow('RCU after', r.rcuAfter === null ? '— (no available capital)' : `${(r.rcuAfter * 100).toFixed(1)}%`));
    econ.appendChild(econRow('Marginal RCU', r.marginal === null ? '—' : `${(r.marginal * 100).toFixed(1)}%`));
    out.appendChild(econ);
    out.appendChild($('p', 'wb-note', 'ARC = NLV − Reserved − Stress reserves − Contingent exposure. RCU = stressed loss / ARC.'));
    out.appendChild($('p', 'wb-unavail', W.unavailable('broker buying power not connected — shown as an execution constraint only, never as risk capital')));
    out.appendChild(figCap(seed, sa, 'risk capital'));
  };
  const defs = [
    ['Net liquidation value ($)', 'nlv'],
    ['Reserved capital ($)', 'reserved'],
    ['Stress reserves ($)', 'stressReserves'],
    ['Existing contingent exposure ($)', 'contingentExposure'],
  ];
  for (const [label, k] of defs) {
    ctls.appendChild(labeledNumber(label, inputs[k], 1000, (v) => { inputs[k] = v; render(); }));
  }
  box.appendChild(ctls);
  box.appendChild(out);
  render();
  return box;
}

function rorGate() {
  const box = $('div', 'wb-card wb-ror');
  box.appendChild($('h3', '', 'Risk of Ruin gate — confirm only'));
  const label = $('label', 'wb-check');
  const cb = document.createElement('input');
  cb.type = 'checkbox';
  label.appendChild(cb);
  label.appendChild($('span', '', 'I have confirmed my personal Risk of Ruin against my own threshold.'));
  box.appendChild(label);
  box.appendChild($('p', 'wb-note', 'This tool never calculates, estimates, infers, modifies, or substitutes for your Risk of Ruin. The gate is yours alone.'));
  box.appendChild($('p', 'wb-note', 'Paper-only desk: the seed carries trade_authorized=false, and this UI offers no execution path.'));
  return box;
}
