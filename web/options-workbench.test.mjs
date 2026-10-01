import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import {
  MAX_DTE,
  DATA_UNAVAILABLE,
  unavailable,
  REASON_NO_DAILY_HISTORY,
  REASON_SEED_ENDPOINT_UNREACHABLE,
  dteGuard,
  dteLimitReason,
  validateSeed,
  parseSeed,
  blackScholesPut,
  blackScholesCall,
  binomialPut,
  binomialCall,
  pricePut,
  modelGreeksPut,
  windowContingent,
  strategyModel,
  stressGrid,
  riskCapitalUtilization,
  rollPlan,
  regTMargin,
} from './options-workbench.mjs';

// Fixed fixture mirrored from artifacts/options-seed-latest.json (REAL_CBOE_DELAYED_SEED).
const VALID_SEED = {
  schema_version: 'hedge-desk-options-seed-1.0.0',
  mode: 'REAL_CBOE_DELAYED_SEED',
  symbol: 'SPY',
  contract_id: 'SPY261030P00749000',
  option_type: 'PUT',
  strike: '749',
  expiration: '2026-10-30',
  days_to_expiration: 29,
  bid: '6.45',
  ask: '6.52',
  mid: '6.485',
  implied_volatility: '0.1526',
  delta: '-0.3022',
  gamma: '0.0106',
  theta: '-0.198',
  vega: '0.7685',
  rho: '-0.1703',
  unavailable_fields: [],
  open_interest: 859,
  volume: 309,
  underlying_bid: '765.53',
  underlying_ask: '765.54',
  underlying_price: '762.63',
  as_of: '2026-10-01T01:12:10.807728+00:00',
  source: 'cboe-delayed',
  data_mode: 'batch',
  refresh: { status: 'ok', refreshed_at: '2026-10-01T01:12:10.807728+00:00', reason: null },
  trade_authorized: false,
  note: 'test fixture',
};

const st = (over = {}) => ({
  spot: 762.63, strike: 749, days: 29, ivPct: 15.26, rate: 0.05292, exercise: 'american', premium: 6.485, ...over,
});

test('G1: DTE cap — 30 passes, 31+ is refused with the exact wording', () => {
  assert.equal(MAX_DTE, 30);
  assert.equal(dteGuard(30), null);
  assert.equal(dteGuard(29), null);
  assert.equal(dteGuard(31), 'data unavailable — contract DTE 31 exceeds the 30-day workbench limit');
  assert.equal(dteGuard(45), 'data unavailable — contract DTE 45 exceeds the 30-day workbench limit');
});

test('G2: American >= European on the fixed fixture (puts and calls)', () => {
  // Exact deterministic reference cases for the pricing engine.
  assert.ok(Math.abs(blackScholesPut(762.63, 749, 29, 0.05292, 0.1526) - 6.247330682271951) < 1e-9);
  const amPut = binomialPut(762.63, 749, 29, 0.05292, 0.1526, 'american');
  const euPut = blackScholesPut(762.63, 749, 29, 0.05292, 0.1526);
  assert.ok(Math.abs(amPut - 6.3651465505735025) < 1e-9);
  assert.ok(amPut >= euPut, `american put ${amPut} < european put ${euPut}`);
  const amCall = binomialCall(762.63, 749, 29, 0.05292, 0.1526, 'american');
  const euCall = blackScholesCall(762.63, 749, 29, 0.05292, 0.1526);
  assert.ok(amCall >= euCall - 1e-12, `american call ${amCall} < european call ${euCall}`);
  assert.ok(pricePut(762.63, 749, 29, 15.26, 0.05292, 'american') >= pricePut(762.63, 749, 29, 15.26, 0.05292, 'european'));
});

test('G4: balance-sheet states — CSP reserves strike x 100, call encumbers shares', () => {
  const put = strategyModel('put', st());
  assert.equal(put.encumberedCapital, 74900);
  assert.ok(put.assets.some((a) => a.label.includes('Cash reserve')));
  assert.ok(put.liabilities.some((l) => l.label.includes('Conditional purchase')));
  assert.equal(put.maxProfit, 648.5);
  const call = strategyModel('call', st());
  assert.ok(call.encTags.includes('shares_encumbered_100'));
  assert.ok(call.assets.some((a) => a.label.includes('100 shares')));
});

test('G4: covered strangle carries the 200-share two-sided stress state', () => {
  const sg = strategyModel('strangle', st());
  assert.ok(sg.assignmentShares.includes('200-share'), sg.assignmentShares);
  assert.equal(sg.assets.length, 2);
  assert.equal(sg.liabilities.length, 2);
  // Down -30%: both the owned 100 and the assigned +100 decline.
  const pnl = sg.expiryPnl(762.63 * 0.7);
  const putWing = (6.485 - (749 - 762.63 * 0.7)) * 100;
  assert.ok(Math.abs(pnl - (putWing + (762.63 * 0.7 - 762.63) * 100 + (sg.callPrem - 0) * 100)) < 1e-6);
});

test('balance sheet: credit spread caps loss at width minus credit; naked keeps margin as execution constraint', () => {
  const sp = strategyModel('spread', st());
  assert.equal(sp.lossDefined, true);
  assert.ok(Math.abs(sp.maxLoss + sp.premiumPerContract - 500) < 1e-6, `maxLoss ${sp.maxLoss} credit ${sp.premiumPerContract}`);
  assert.equal(sp.encumberedCapital, sp.maxLoss);
  const nk = strategyModel('naked', st());
  assert.equal(nk.lossDefined, false);
  assert.ok(nk.regtMargin > 0 && nk.regtMargin < 74900, `regt ${nk.regtMargin} must be below full assignment capital`);
  assert.ok(nk.liabilities.some((l) => l.label.includes('execution constraint only') || l.text.includes('execution constraint only')));
  assert.throws(() => strategyModel('bogus', st()), /unknown strategy/);
});

test('position Greeks: short put is long theta, long delta', () => {
  const g = strategyModel('put', st()).greeks;
  assert.ok(g.theta > 0, `short-put theta ${g.theta}`);
  assert.ok(g.delta > 0, `short-put delta ${g.delta} (short puts are long delta)`);
  const mg = modelGreeksPut(762.63, 749, 29, 15.26, 0.05292, 'american');
  assert.ok(isFinite(mg.vegaPt) && mg.vegaPt > 0);
});

test('G5: ARC = NLV - Reserved - StressReserves - ContingentExposure; RCU = StressedLoss / ARC', () => {
  const r = riskCapitalUtilization({
    nlv: 500000, reserved: 100000, stressReserves: 50000, contingentExposure: 0,
    encumberedCapital: 74900, stressedTradeLoss: -20000,
  });
  assert.equal(r.arcBefore, 350000);
  assert.equal(r.arcAfter, 275100);
  assert.equal(r.rcuBefore, 0);
  assert.ok(Math.abs(r.rcuAfter - 20000 / 275100) < 1e-12);
  assert.ok(Math.abs(r.marginal - r.rcuAfter) < 1e-12, 'marginal = RCU_after - RCU_before');
  const dead = riskCapitalUtilization({
    nlv: 100000, reserved: 60000, stressReserves: 40000, contingentExposure: 10000,
    encumberedCapital: 1000, stressedTradeLoss: -500,
  });
  assert.ok(dead.arcBefore <= 0 && dead.rcuBefore === null && dead.rcuAfter === null && dead.marginal === null);
});

test('stress grid: nine rows; stressed loss is the worst of the seven mark/expiry rows', () => {
  const model = strategyModel('put', st());
  const grid = stressGrid(model, st());
  assert.equal(grid.rows.length, 9);
  assert.deepEqual(
    grid.rows.map((r) => r.state),
    ['-30% @ expiry', '-20% @ expiry', '-10% @ expiry', '-5% @ expiry',
      'Vol expansion +5 pts @ half life', 'Gap down −8% @ 5 DTE, vol +10', 'Gap up +8% @ 5 DTE, vol +5',
      'Full assignment −15% @ expiry', 'Early assignment −12% now (American)'],
  );
  assert.equal(grid.stressedLoss, Math.min(...grid.rows.slice(0, 7).map((r) => r.pnl)));
  assert.ok(grid.stressedLoss < 0, 'a -30% expiry row must lose money on a short put');
});

test('GAP-1: window-contingent flags when one day drives >30% of realized variance', () => {
  // One crash day: ln(50/100)^2 dominates -> ~99.9% of variance.
  const crash = windowContingent([100, 100.5, 101, 100.2, 99.8, 100.3, 99.5, 100.1, 99.9, 100.4, 100, 99.7, 100.2, 99.6, 100, 50, 50.5]);
  assert.equal(crash.windowContingent, true);
  assert.ok(crash.maxDayShare > 0.3);
  assert.ok(crash.realizedVol > 0 && isFinite(crash.realizedVol));
  // Smooth tape: equal 0.5% daily moves -> max share = 1/n < 30%.
  const smooth = [100];
  for (let i = 0; i < 20; i++) smooth.push(smooth[i] * 1.005);
  const calm = windowContingent(smooth);
  assert.equal(calm.windowContingent, false);
  assert.ok(calm.maxDayShare < 0.3, `share ${calm.maxDayShare}`);
  // Degenerate input degrades cleanly, never throws.
  const empty = windowContingent([]);
  assert.equal(empty.windowContingent, false);
  assert.equal(empty.realizedVol, null);
});

test('GAP-2: missing data reads exactly "data unavailable" plus a reason', () => {
  assert.equal(DATA_UNAVAILABLE, 'data unavailable');
  assert.equal(unavailable(REASON_SEED_ENDPOINT_UNREACHABLE), 'data unavailable — seed endpoint unreachable');
  assert.equal(unavailable(REASON_NO_DAILY_HISTORY), "data unavailable — underlying daily closes not in this week's seed");
  assert.equal(dteLimitReason(45), 'contract DTE 45 exceeds the 30-day workbench limit');
  assert.equal(unavailable(dteLimitReason(45)), 'data unavailable — contract DTE 45 exceeds the 30-day workbench limit');
});

test('seed validation: accepts the real schema, rejects bad payloads, DTE>30 stays parseable', () => {
  const v = validateSeed(VALID_SEED);
  assert.equal(v.ok, true, JSON.stringify(v.errors));
  const s = parseSeed(VALID_SEED);
  assert.equal(s.dte, 29);
  assert.ok(Math.abs(s.ivPct - 15.26) < 1e-9, `ivPct ${s.ivPct}`);
  assert.equal(s.premium, 6.485);
  assert.equal(s.dailyHistory, null);
  assert.equal(validateSeed({ ...VALID_SEED, schema_version: 'x' }).ok, false);
  assert.ok(validateSeed({ ...VALID_SEED, schema_version: 'x' }).errors.some((e) => e.includes('schema_version')));
  assert.equal(validateSeed({ ...VALID_SEED, trade_authorized: true }).ok, false);
  assert.equal(validateSeed({ ...VALID_SEED, strike: 'abc' }).ok, false);
  assert.equal(validateSeed({ ...VALID_SEED, refresh: { status: 'broken' } }).ok, false);
  assert.equal(validateSeed(null).ok, false);
  // DTE > 30 is valid data; the display guard (dteGuard) handles it, not validation.
  assert.equal(validateSeed({ ...VALID_SEED, days_to_expiration: 45 }).ok, true);
  const withHistory = { ...VALID_SEED, daily_history: [100, 101, 102] };
  assert.equal(validateSeed(withHistory).ok, true);
  assert.deepEqual(parseSeed(withHistory).dailyHistory, [100, 101, 102]);
  assert.equal(validateSeed({ ...VALID_SEED, daily_history: ['x'] }).ok, false);
});

test('roll economics: close cost, new credit, net, breakeven, capital at risk', () => {
  const plan = rollPlan(st());
  assert.equal(plan.trigger, 21);
  assert.ok(plan.closeCost > 0 && plan.newCredit > 0);
  assert.ok(Math.abs(plan.net - (plan.newCredit - plan.closeCost)) < 1e-9);
  assert.ok(Math.abs(plan.newBreakeven - (plan.newStrike - plan.newCredit / 100)) < 1e-9);
  assert.equal(plan.capitalAtRisk, plan.newStrike * 100);
});

test('reg-T margin stays below full assignment capital (buying power is not risk capital)', () => {
  const m = regTMargin(762.63, 749, 6.485);
  assert.ok(m > 0 && m < 74900, `regt ${m}`);
});

test('G6: zero RoR computation — the logic module never mentions it', () => {
  const src = readFileSync(new URL('./options-workbench.mjs', import.meta.url), 'utf8');
  assert.ok(!/risk\s*of\s*ruin/i.test(src), 'no Risk of Ruin mention in the logic module');
  assert.ok(!/\bror\b/i.test(src), 'no RoR token in the logic module');
  for (const f of ['./options-workbench-ui.js']) {
    if (!existsSync(new URL(f, import.meta.url))) continue; // UI lands in a later commit
    const ui = readFileSync(new URL(f, import.meta.url), 'utf8');
    assert.ok(!/risk\s*of\s*ruin\s*(value|engine|gate\s*=|threshold)/i.test(ui), 'no RoR computation in the UI');
    assert.ok(!/\bror_?value\b|\briskOfRuin\s*\(/i.test(ui), 'no RoR value plumbing in the UI');
  }
});
