// Options Workbench — pure ES-module logic.
// No DOM, no fetch, no storage. Every export is a deterministic pure function
// of its inputs so the browser UI and node --test share one implementation.
//
// Pricing: 240-step binomial lattice for American exercise
// (American = max(hold, intrinsic) at every node, so American >= European by
// construction), closed-form Black-Scholes for European.
// Balance-sheet, stress grid, ARC/RCU and roll economics follow
// ~/workspace/hedge-desk/options-risk-model-2026-09-30.md.
//
// NOTE: this module never computes, estimates, infers, modifies, or
// substitutes for the user's own authoritative risk control. That control
// is theirs alone and lives outside this module as a confirm-only step.

export const MAX_DTE = 30;
export const STALE_DAYS = 8;
export const EXPECTED_SEED_SCHEMA = 'hedge-desk-options-seed-1.0.0';

// ---------------------------------------------------------------------------
// "data unavailable" wording — GAP-2. Missing data always reads exactly
// `data unavailable` plus a reason. Never zero, never invented.
// ---------------------------------------------------------------------------
export const DATA_UNAVAILABLE = 'data unavailable';
export const unavailable = (reason) => `${DATA_UNAVAILABLE} — ${reason}`;
export const REASON_SEED_ENDPOINT_UNREACHABLE = 'seed endpoint unreachable';
export const REASON_SEED_FETCH_FAILED = 'seed fetch failed';
export const REASON_SEED_SCHEMA_INVALID = 'seed payload failed validation';
export const REASON_NO_DAILY_HISTORY = "underlying daily closes not in this week's seed";
export const REASON_CHART_LIB_FAILED = 'chart library failed to load';
export const REASON_NO_IV_HISTORY = "contract 52-week IV history not in this week's seed";
export const dteLimitReason = (n) => `contract DTE ${n} exceeds the 30-day workbench limit`;

/** Hard gate G1: modeled panels refuse contracts past the 30-day limit. */
export const dteGuard = (dte) => (dte > MAX_DTE ? unavailable(dteLimitReason(dte)) : null);

// ---------------------------------------------------------------------------
// Formatting (deterministic; used by the UI and asserted in tests)
// ---------------------------------------------------------------------------
const usd0 = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0, maximumFractionDigits: 0 });
const usd2 = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2, maximumFractionDigits: 2 });
export const fmtMoney = (n, decimals = 0) => (decimals === 2 ? usd2 : usd0).format(n);
export const fmtSigned = (n) => `${n < 0 ? '−' : '+'}${usd0.format(Math.abs(n)).slice(1)}`;
export const fmtDate = (d) => d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' });

// ---------------------------------------------------------------------------
// Seed schema: parse + validate
// ---------------------------------------------------------------------------
const num = (v) => {
  if (typeof v === 'number') return v;
  if (typeof v === 'string' && v.trim() !== '') return Number(v);
  return NaN;
};

const SOURCE_LABELS = {
  'cboe-delayed': 'Cboe delayed chain',
  'barchart-delayed': 'Barchart delayed chain',
};

const humanSource = (s) => SOURCE_LABELS[s] || String(s || '').replace(/[-_]+/g, ' ').trim() || 'unknown source';

export function validateSeed(raw) {
  const errors = [];
  if (!raw || typeof raw !== 'object') return { ok: false, errors: ['seed is not an object'] };
  if (raw.schema_version !== EXPECTED_SEED_SCHEMA) errors.push(`schema_version must be ${EXPECTED_SEED_SCHEMA}`);
  if (typeof raw.mode !== 'string' || !raw.mode) errors.push('mode missing');
  if (typeof raw.symbol !== 'string' || !raw.symbol) errors.push('symbol missing');
  if (typeof raw.contract_id !== 'string' || !raw.contract_id) errors.push('contract_id missing');
  if (raw.option_type !== 'PUT' && raw.option_type !== 'CALL') errors.push('option_type must be PUT or CALL');
  const strike = num(raw.strike);
  if (!isFinite(strike) || strike <= 0) errors.push('strike must be a positive number');
  if (typeof raw.expiration !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(raw.expiration)) errors.push('expiration must be YYYY-MM-DD');
  const dte = num(raw.days_to_expiration);
  if (!isFinite(dte) || dte <= 0) errors.push('days_to_expiration must be a positive number');
  for (const f of ['bid', 'ask', 'mid', 'implied_volatility']) {
    const v = num(raw[f]);
    if (!isFinite(v) || v < 0) errors.push(`${f} must be a non-negative number`);
  }
  const iv = num(raw.implied_volatility);
  if (!(iv > 0 && iv <= 100)) errors.push('implied_volatility out of range');
  for (const f of ['delta', 'gamma', 'theta', 'vega', 'rho']) {
    if (raw[f] !== undefined && raw[f] !== null && !isFinite(num(raw[f]))) errors.push(`${f} must be numeric`);
  }
  const spot = num(raw.underlying_price);
  if (!isFinite(spot) || spot <= 0) errors.push('underlying_price must be a positive number');
  if (Number.isNaN(Date.parse(raw.as_of))) errors.push('as_of must be a parseable date');
  if (typeof raw.source !== 'string' || !raw.source) errors.push('source missing');
  if (!raw.refresh || (raw.refresh.status !== 'ok' && raw.refresh.status !== 'fetch_failed')) {
    errors.push("refresh.status must be 'ok' or 'fetch_failed'");
  }
  if (raw.trade_authorized !== false) errors.push('trade_authorized must be false');
  if (raw.daily_history !== undefined && raw.daily_history !== null) {
    if (!Array.isArray(raw.daily_history) || raw.daily_history.some((x) => !isFinite(num(x)) || num(x) <= 0)) {
      errors.push('daily_history must be an array of positive numbers when present');
    }
  }
  return { ok: errors.length === 0, errors };
}

/** Normalize a validated seed into the shape the workbench models. */
export function parseSeed(raw) {
  const ivRaw = num(raw.implied_volatility);
  const ivPct = ivRaw <= 1 ? ivRaw * 100 : ivRaw; // schema stores a fraction; tolerate percent
  const g = (f) => (raw[f] === undefined || raw[f] === null ? null : num(raw[f]));
  const asOf = new Date(raw.as_of);
  return {
    symbol: raw.symbol,
    contractId: raw.contract_id,
    optionType: raw.option_type,
    strike: num(raw.strike),
    expiration: raw.expiration,
    dte: num(raw.days_to_expiration),
    bid: num(raw.bid),
    ask: num(raw.ask),
    mid: num(raw.mid),
    premium: num(raw.mid),
    ivPct,
    greeks: { delta: g('delta'), gamma: g('gamma'), theta: g('theta'), vega: g('vega'), rho: g('rho') },
    oi: raw.open_interest === undefined ? null : Number(raw.open_interest),
    volume: raw.volume === undefined ? null : Number(raw.volume),
    spot: num(raw.underlying_price),
    spotBid: raw.underlying_bid === undefined ? null : num(raw.underlying_bid),
    spotAsk: raw.underlying_ask === undefined ? null : num(raw.underlying_ask),
    asOf,
    asOfLabel: fmtDate(asOf),
    source: raw.source,
    sourceLabel: humanSource(raw.source),
    dataMode: raw.data_mode || 'batch',
    refreshStatus: raw.refresh.status,
    refreshReason: raw.refresh.reason || null,
    dailyHistory: raw.daily_history ? raw.daily_history.map(num) : null,
    unavailableFields: Array.isArray(raw.unavailable_fields) ? raw.unavailable_fields : [],
    note: raw.note || '',
  };
}

export const isStaleSeed = (seed, now = new Date()) =>
  seed.refreshStatus === 'fetch_failed' || (now - seed.asOf) / 86400000 > STALE_DAYS;

// ---------------------------------------------------------------------------
// Option pricing engine
// ---------------------------------------------------------------------------
export function normCdf(x) {
  const t = 1 / (1 + 0.2316419 * Math.abs(x));
  const d = 0.3989422804014327 * Math.exp(-x * x / 2);
  const p = 1 - d * t * (0.31938153 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))));
  return x >= 0 ? p : 1 - p;
}

function blackScholes(spot, strike, days, rate, vol, isCall) {
  if (days <= 0) return isCall ? Math.max(spot - strike, 0) : Math.max(strike - spot, 0);
  const t = days / 365;
  const rootT = Math.sqrt(t);
  const d1 = (Math.log(spot / strike) + (rate + vol * vol / 2) * t) / (vol * rootT);
  const d2 = d1 - vol * rootT;
  if (isCall) return spot * normCdf(d1) - strike * Math.exp(-rate * t) * normCdf(d2);
  return strike * Math.exp(-rate * t) * normCdf(-d2) - spot * normCdf(-d1);
}

export const blackScholesPut = (spot, strike, days, rate, vol) => blackScholes(spot, strike, days, rate, vol, false);
export const blackScholesCall = (spot, strike, days, rate, vol) => blackScholes(spot, strike, days, rate, vol, true);

function binomial(spot, strike, days, rate, vol, exercise, isCall, n = 240) {
  const intrinsic = isCall ? Math.max(spot - strike, 0) : Math.max(strike - spot, 0);
  if (days <= 0 || vol <= 0) return intrinsic;
  const dt = days / 365 / n;
  const u = Math.exp(vol * Math.sqrt(dt));
  const d = 1 / u;
  const p = (Math.exp(rate * dt) - d) / (u - d);
  const q = 1 - p;
  const disc = Math.exp(-rate * dt);
  const opt = new Array(n + 1);
  for (let i = 0; i <= n; i++) {
    const sT = spot * Math.pow(u, 2 * i - n);
    opt[i] = isCall ? Math.max(sT - strike, 0) : Math.max(strike - sT, 0);
  }
  for (let j = n - 1; j >= 0; j--) {
    for (let k = 0; k <= j; k++) {
      const hold = disc * (p * opt[k + 1] + q * opt[k]);
      if (exercise === 'american') {
        const here = spot * Math.pow(u, 2 * k - j);
        opt[k] = Math.max(hold, isCall ? here - strike : strike - here);
      } else {
        opt[k] = hold;
      }
    }
  }
  return opt[0];
}

export const binomialPut = (spot, strike, days, rate, vol, exercise, n) => binomial(spot, strike, days, rate, vol, exercise, false, n);
export const binomialCall = (spot, strike, days, rate, vol, exercise, n) => binomial(spot, strike, days, rate, vol, exercise, true, n);

export const pricePut = (spot, strike, days, ivPct, rate, exercise) =>
  exercise === 'american'
    ? binomialPut(spot, strike, days, rate, ivPct / 100, 'american')
    : blackScholesPut(spot, strike, days, rate, ivPct / 100);

export const priceCall = (spot, strike, days, ivPct, rate, exercise) =>
  exercise === 'american'
    ? binomialCall(spot, strike, days, rate, ivPct / 100, 'american')
    : blackScholesCall(spot, strike, days, rate, ivPct / 100);

export function d2Of(spot, strike, days, rate, vol) {
  if (days <= 0 || vol <= 0) return spot > strike ? 8 : -8;
  const t = days / 365;
  return (Math.log(spot / strike) + (rate - vol * vol / 2) * t) / (vol * Math.sqrt(t));
}

function modelGreeksKind(spot, strike, days, ivPct, rate, exercise, isCall) {
  const price = isCall ? priceCall : pricePut;
  const dS = Math.max(spot * 0.02, 1.0);
  const dI = 0.5;
  const dR = 0.005;
  const base = price(spot, strike, days, ivPct, rate, exercise);
  const upP = price(spot + dS, strike, days, ivPct, rate, exercise);
  const dwnP = price(spot - dS, strike, days, ivPct, rate, exercise);
  const retired = price(spot, strike, Math.max(days - 1, 0), ivPct, rate, exercise);
  const upI = price(spot, strike, days, ivPct + dI, rate, exercise);
  const dwnI = price(spot, strike, days, Math.max(ivPct - dI, 1), rate, exercise);
  const upR = price(spot, strike, days, ivPct, rate + dR, exercise);
  const dwnR = price(spot, strike, days, ivPct, Math.max(rate - dR, 0), exercise);
  return {
    price: base,
    delta: (upP - dwnP) / (2 * dS),
    gamma: (upP - 2 * base + dwnP) / (dS * dS),
    thetaDay: -(base - retired) * 100, // $/contract/day, short-option sign
    vegaPt: ((upI - dwnI) / (2 * dI)) * 100, // $/contract per IV point
    rhoPt: ((upR - dwnR) / (2 * dR)) * 0.01 * 100, // $/contract per 1-pt rate move
  };
}

export const modelGreeksPut = (spot, strike, days, ivPct, rate, exercise) =>
  modelGreeksKind(spot, strike, days, ivPct, rate, exercise, false);
export const modelGreeksCall = (spot, strike, days, ivPct, rate, exercise) =>
  modelGreeksKind(spot, strike, days, ivPct, rate, exercise, true);

/** Reg-T style uncovered-put writer margin: premium + 20% of spot − OTM,
 *  floored at premium + 10% of spot. Approximation; broker rules vary. */
export function regTMargin(spot, strike, premium) {
  const per = premium * 100;
  const otm = Math.max(spot - strike, 0) * 100;
  return Math.max(per + (0.2 * spot * 100 - otm), per + 0.1 * spot * 100, 0);
}

// ---------------------------------------------------------------------------
// Window-contingent check — GAP-1.
// Real single-day variance-contribution math for the IV-vs-realized panel.
// Flags WINDOW-CONTINGENT when one day drives > 30% of realized variance.
// ---------------------------------------------------------------------------
export function windowContingent(dailyCloses) {
  if (!Array.isArray(dailyCloses) || dailyCloses.length < 2) {
    return { realizedVol: null, maxDayShare: null, windowContingent: false, days: 0 };
  }
  const sq = [];
  for (let i = 1; i < dailyCloses.length; i++) {
    const r = Math.log(dailyCloses[i] / dailyCloses[i - 1]);
    sq.push(r * r);
  }
  const total = sq.reduce((a, b) => a + b, 0);
  if (!(total > 0)) return { realizedVol: null, maxDayShare: null, windowContingent: false, days: sq.length };
  const maxDayShare = Math.max(...sq) / total;
  const realizedVol = Math.sqrt(total / sq.length) * Math.sqrt(252);
  return { realizedVol, maxDayShare, windowContingent: maxDayShare > 0.3, days: sq.length };
}

// ---------------------------------------------------------------------------
// Strategy balance-sheet models — risk spec sections 2–6.
// st: {spot, strike, days, ivPct, rate, exercise, premium} (premium $/share).
// All five strategies modeled; the covered strangle carries the 200-share
// two-sided post-assignment state.
// ---------------------------------------------------------------------------
export const STRATEGIES = {
  put: 'Cash-secured put',
  call: 'Covered call',
  strangle: 'Covered strangle',
  spread: 'Put credit spread',
  naked: 'Naked put',
};

const ENC_TAGS = {
  put: ['cash_reserved', 'conditional_purchase_100'],
  call: ['shares_encumbered_100', 'no_cash_reserve'],
  strangle: ['cash_reserved', 'shares_encumbered_100', 'dual_assignment'],
  spread: ['defined_loss_cap', 'offset_assignment'],
  naked: ['unfunded_exposure', 'margin_is_execution_constraint_only'],
};

export function strategyModel(key, st) {
  if (!STRATEGIES[key]) throw new Error(`unknown strategy: ${key}`);
  const { spot, strike: Kp, days, ivPct, rate, exercise, premium: putPrem } = st;
  const Kc = Math.round((spot * 1.09) / 5) * 5; // mirrored call wing, scenario
  const Kl = Kp - 5; // defined-risk wing, scenario
  const callPrem = priceCall(spot, Kc, days, ivPct, rate, exercise);
  const longPrem = pricePut(spot, Kl, days, ivPct, rate, exercise);
  const totalPrem = putPrem + callPrem;
  const netSpreadCredit = putPrem - longPrem;
  const spreadMargin = Math.max((5 - netSpreadCredit) * 100, 0);
  const cb = Kp - putPrem; // put assignment cost basis
  const regt = regTMargin(spot, Kp, putPrem);
  const gPut = modelGreeksPut(spot, Kp, days, ivPct, rate, exercise);
  const gCall = modelGreeksCall(spot, Kc, days, ivPct, rate, exercise);
  const gLong = modelGreeksPut(spot, Kl, days, ivPct, rate, exercise);

  const expiryPnl = (s) => {
    switch (key) {
      case 'put':
      case 'naked':
        return (putPrem - Math.max(Kp - s, 0)) * 100;
      case 'call':
        return (callPrem - Math.max(s - Kc, 0)) * 100 + (s - spot) * 100;
      case 'strangle':
        return (putPrem - Math.max(Kp - s, 0)) * 100 + (callPrem - Math.max(s - Kc, 0)) * 100 + (s - spot) * 100;
      case 'spread':
        return (putPrem - Math.max(Kp - s, 0)) * 100 + (Math.max(Kl - s, 0) - longPrem) * 100;
      default:
        return 0;
    }
  };

  // Mid-life mark value of the position at shocked inputs.
  const markValue = (s, dd, vv) => {
    const pv = (putPrem - pricePut(s, Kp, dd, vv, rate, exercise)) * 100;
    const cv = (callPrem - priceCall(s, Kc, dd, vv, rate, exercise)) * 100;
    const lv = (pricePut(s, Kl, dd, vv, rate, exercise) - longPrem) * 100;
    const sv = (s - spot) * 100;
    switch (key) {
      case 'put':
      case 'naked':
        return pv;
      case 'call':
        return cv + sv;
      case 'strangle':
        return pv + cv + sv;
      case 'spread':
        return pv + lv;
      default:
        return 0;
    }
  };
  const markShift = (s, dd, vv) => markValue(s, dd, vv) - markValue(spot, days, ivPct);

  const sharesText = (s) => {
    const putAssign = s < Kp;
    const callWin = s > Kc;
    switch (key) {
      case 'put':
        return putAssign
          ? `+100 assigned @ basis ${fmtMoney(cb, 2)} (${fmtMoney(Kp * 100)} deployed)`
          : 'put expires OTM; premium kept';
      case 'call':
        return callWin ? `100 called away at ${fmtMoney(Kc)}` : '100 shares held; call expires OTM';
      case 'strangle':
        return `${putAssign ? '+100 assigned (put wing)' : 'put wing OTM'} · ${
          callWin ? '100 called away (call wing)' : 'call wing OTM'
        } · 100 shares held — 200-share two-sided stress state`;
      case 'spread':
        if (s < Kl) return '100 assigned / 100 exercised — wing offset, defined loss';
        return putAssign ? 'short leg assigns; long wing neutralizes on exercise' : 'both legs OTM';
      default:
        return putAssign ? `+100 assigned UNFUNDED @ basis ${fmtMoney(cb, 2)}` : 'put expires OTM';
    }
  };

  // Position Greeks: share-equivalents (stock leg = 100 delta).
  const legs =
    key === 'call'
      ? [{ s: -1, g: gCall }, 'stock']
      : key === 'strangle'
        ? [{ s: -1, g: gPut }, { s: -1, g: gCall }, 'stock']
        : key === 'spread'
          ? [{ s: -1, g: gPut }, { s: 1, g: gLong }]
          : [{ s: -1, g: gPut }];
  const greeks = { delta: 0, gamma: 0, theta: 0, vega: 0 };
  for (const L of legs) {
    if (L === 'stock') {
      greeks.delta += 100;
      continue;
    }
    greeks.delta += L.s * L.g.delta * 100;
    greeks.gamma += L.s * L.g.gamma * 100;
    greeks.theta += L.s * L.g.thetaDay;
    greeks.vega += L.s * L.g.vegaPt;
  }

  const model = {
    key,
    name: STRATEGIES[key],
    Kc,
    Kl,
    callPrem,
    longPrem,
    encTags: ENC_TAGS[key],
    expiryPnl,
    markShift,
    sharesText,
    greeks,
  };

  switch (key) {
    case 'put':
      Object.assign(model, {
        premiumPerContract: putPrem * 100,
        maxProfit: putPrem * 100,
        maxLoss: (Kp - putPrem) * 100,
        lossDefined: false,
        breakevens: [Kp - putPrem],
        encumberedCapital: Kp * 100,
        assets: [{ label: 'Cash reserve held against assignment', text: fmtMoney(Kp * 100) }],
        liabilities: [
          { label: 'Conditional purchase', text: `100 shares @ ${fmtMoney(Kp)}` },
          { label: 'Premium retained (revenue offset)', text: fmtMoney(putPrem * 100) },
        ],
        assignmentCash: fmtMoney(Kp * 100),
        assignmentShares: '+100 shares',
        costBasis: fmtMoney(cb, 2),
        riskNote: 'Fully funded: a large shock hurts, but cannot create a capital call.',
      });
      break;
    case 'call':
      Object.assign(model, {
        premiumPerContract: callPrem * 100,
        maxProfit: (Kc - spot) * 100 + callPrem * 100,
        maxLoss: (spot - callPrem) * 100,
        lossDefined: false,
        breakevens: [spot - callPrem],
        encumberedCapital: Math.max(spot * 100 - callPrem * 100, 0),
        assets: [{ label: '100 shares already owned', text: `≈ ${fmtMoney(spot * 100)}` }],
        liabilities: [{ label: 'Delivery obligation if called', text: `100 shares above ${fmtMoney(Kc)}` }],
        assignmentCash: '$0 — shares already owned',
        assignmentShares: `−100 (called away) above ${fmtMoney(Kc)}`,
        costBasis: `${fmtMoney(spot - callPrem, 2)} effective downside basis`,
        riskNote: 'No cash reserve needed: shares are already owned. The binding risk is upside foregone.',
      });
      break;
    case 'strangle':
      Object.assign(model, {
        premiumPerContract: totalPrem * 100,
        maxProfit: (Kc - spot) * 100 + totalPrem * 100,
        maxLoss: (Kp - totalPrem) * 100,
        lossDefined: false,
        breakevens: [Kp - totalPrem, Kc + totalPrem],
        encumberedCapital: Kp * 100 + spot * 100,
        assets: [
          { label: '100 shares held', text: `≈ ${fmtMoney(spot * 100)}` },
          { label: 'Cash reserve (put wing)', text: fmtMoney(Kp * 100) },
        ],
        liabilities: [
          { label: 'Conditional purchase (put wing)', text: `100 shares @ ${fmtMoney(Kp)}` },
          { label: 'Delivery obligation (call wing)', text: `100 shares above ${fmtMoney(Kc)}` },
        ],
        assignmentCash: `put wing ${fmtMoney(Kp * 100)} + 100 shares held`,
        assignmentShares: '+100 (put) and −100 (call) — 200-share two-sided stress state',
        costBasis: `put wing ${fmtMoney(cb, 2)} · shares basis ${fmtMoney(spot - totalPrem, 2)}`,
        riskNote: 'Post-assignment stress: the put can assign +100 while 100 stay encumbered under the call — a 200-share state.',
      });
      break;
    case 'spread':
      Object.assign(model, {
        premiumPerContract: netSpreadCredit * 100,
        maxProfit: netSpreadCredit * 100,
        maxLoss: spreadMargin,
        lossDefined: true,
        breakevens: [Kp - netSpreadCredit],
        encumberedCapital: spreadMargin,
        assets: [{ label: 'Net credit banked', text: fmtMoney(netSpreadCredit * 100) }],
        liabilities: [{ label: 'Capped loss obligation', text: `${fmtMoney(spreadMargin)} if spread pins below ${fmtMoney(Kl)}` }],
        assignmentCash: `${fmtMoney(Kp * 100)} intraday if short assigns; nets to ${fmtMoney(spreadMargin)} via the long wing`,
        assignmentShares: '100 assigned / 100 exercised — net zero',
        costBasis: `${fmtMoney(Kp - netSpreadCredit, 2)} (short wing floor pre-offset)`,
        riskNote: 'Defined risk: short-leg assignment is neutralized by exercising the long wing. The cap, not the broker, is the control.',
      });
      break;
    default: // naked
      Object.assign(model, {
        premiumPerContract: putPrem * 100,
        maxProfit: putPrem * 100,
        maxLoss: (Kp - putPrem) * 100,
        lossDefined: false,
        breakevens: [Kp - putPrem],
        encumberedCapital: Math.max(regt, 1),
        regtMargin: regt,
        assets: [{ label: 'Premium banked', text: fmtMoney(putPrem * 100) }],
        liabilities: [
          { label: 'UNFUNDED conditional purchase', text: `100 shares @ ${fmtMoney(Kp)}` },
          { label: 'Broker margin (execution constraint only)', text: `${fmtMoney(regt)} — not risk capital` },
        ],
        assignmentCash: `${fmtMoney(Kp * 100)} UNFUNDED`,
        assignmentShares: '+100 shares unfunded',
        costBasis: `${fmtMoney(cb, 2)} (unfunded)`,
        riskNote: 'No reserve booked. Broker margin is the broker\u2019s limit, not risk capital.',
      });
      break;
  }
  return model;
}

// ---------------------------------------------------------------------------
// Stress grid — risk spec section 8. Nine rows; stressed loss is the worst of
// the seven mark/expiry rows (assignment rows are state illustrations).
// ---------------------------------------------------------------------------
export function stressGrid(model, st) {
  const { spot, days, ivPct } = st;
  const rows = [];
  for (const m of [-0.3, -0.2, -0.1, -0.05]) {
    const s = spot * (1 + m);
    rows.push({ state: `${(m * 100).toFixed(0)}% @ expiry`, pnl: model.expiryPnl(s), shares: model.sharesText(s) });
  }
  rows.push({
    state: 'Vol expansion +5 pts @ half life',
    pnl: model.markShift(spot, Math.max(Math.round(days / 2), 1), ivPct + 5),
    shares: 'marks only; no share change yet',
  });
  rows.push({
    state: 'Gap down −8% @ 5 DTE, vol +10',
    pnl: model.markShift(spot * 0.92, 5, ivPct + 10),
    shares: `if pinned: ${model.sharesText(spot * 0.92)}`,
  });
  rows.push({
    state: 'Gap up +8% @ 5 DTE, vol +5',
    pnl: model.markShift(spot * 1.08, 5, ivPct + 5),
    shares: `if pinned: ${model.sharesText(spot * 1.08)}`,
  });
  rows.push({
    state: 'Full assignment −15% @ expiry',
    pnl: model.expiryPnl(spot * 0.85),
    shares: model.sharesText(spot * 0.85),
  });
  rows.push({
    state: 'Early assignment −12% now (American)',
    pnl: model.expiryPnl(spot * 0.88),
    shares: `${model.sharesText(spot * 0.88)} · intrinsic approx.`,
  });
  const stressedLoss = Math.min(...rows.slice(0, 7).map((r) => r.pnl));
  return { rows, stressedLoss };
}

// ---------------------------------------------------------------------------
// Available Risk Capital & Risk Capital Utilization — risk spec sections 1, 9.
// ARC = NLV − Reserved Capital − Stress Reserves − Existing Contingent Exposure
// RCU = Stressed Portfolio Loss / Available Risk Capital
// Broker buying power never enters these formulas.
// ---------------------------------------------------------------------------
export function riskCapitalUtilization({ nlv, reserved, stressReserves, contingentExposure, encumberedCapital, stressedTradeLoss }) {
  const arcBefore = nlv - reserved - stressReserves - contingentExposure;
  const arcAfter = arcBefore - encumberedCapital;
  const lossAfter = Math.min(stressedTradeLoss, 0); // existing-book loss not modeled
  const rcuBefore = arcBefore > 0 ? 0 : null;
  const rcuAfter = arcAfter > 0 ? Math.abs(lossAfter) / arcAfter : null;
  const marginal = rcuBefore !== null && rcuAfter !== null ? rcuAfter - rcuBefore : null;
  return { arcBefore, arcAfter, rcuBefore, rcuAfter, marginal };
}

// ---------------------------------------------------------------------------
// Roll economics (put-write mechanics): close at 21 DTE, sell a fresh 30-day
// put at the same moneyness just after. Flat spot, flat IV.
// ---------------------------------------------------------------------------
export function rollPlan(st) {
  const { spot, strike, days, ivPct, rate, exercise } = st;
  const trigger = Math.min(21, Math.max(days - 5, 2));
  const elapsed = days - trigger;
  const closeCost = pricePut(spot, strike, trigger, ivPct, rate, exercise) * 100;
  const moneyness = 1 - strike / spot;
  const newStrike = Math.round((spot * (1 - moneyness)) / 5) * 5;
  const newCredit = pricePut(spot, newStrike, days, ivPct, rate, exercise) * 100;
  const net = newCredit - closeCost;
  const capitalAtRisk = newStrike * 100;
  const yieldPct = (net / capitalAtRisk) * 100;
  const annualized = elapsed > 0 ? (yieldPct * 365) / elapsed : 0;
  return {
    trigger,
    elapsed,
    closeCost,
    newStrike,
    newCredit,
    net,
    newBreakeven: newStrike - newCredit / 100,
    capitalAtRisk,
    yieldPct,
    annualized,
  };
}

// ---------------------------------------------------------------------------
// Harvest model: sell the put, buy back at a profit target, redeploy.
// ---------------------------------------------------------------------------
export function harvestModel(st, targetPct, stress) {
  const { spot, strike, days, ivPct, rate, exercise, premium } = st;
  const capture = premium * 100;
  const buyBack = premium * (1 - targetPct / 100);
  let tStar = days;
  let reached = false;
  for (let i = 1; i <= days; i++) {
    if (pricePut(spot, strike, days - i, ivPct, rate, exercise) <= buyBack) {
      tStar = Math.max(i, 3);
      reached = true;
      break;
    }
  }
  const perCycle = reached ? (capture * targetPct) / 100 : capture;
  const cycles = Math.min(365 / tStar, 40);
  const stack = perCycle * cycles;
  const gross = capture * cycles;
  let stressed = null;
  if (stress && stress !== 'none') {
    const drift = stress === 'm10' ? -0.1 : -0.05;
    const spotExp = spot * (1 + drift);
    stressed = stack - perCycle + (premium - Math.max(strike - spotExp, 0)) * 100;
  }
  return {
    tStar,
    reached,
    perCycle,
    cycles,
    stack,
    gross,
    debits: gross - stack,
    yieldPct: (stack / (strike * 100)) * 100,
    stressed,
  };
}

// ---------------------------------------------------------------------------
// Probability framework — backed out of the option's own IV (risk-neutral).
// ---------------------------------------------------------------------------
export function probabilityFrame(st) {
  const { spot, strike, days, ivPct, rate, exercise, premium } = st;
  const v = ivPct / 100;
  const popFull = normCdf(d2Of(spot, strike, days, rate, v));
  const expectedMove = spot * v * Math.sqrt(days / 365);
  const g = modelGreeksPut(spot, strike, days, ivPct, rate, exercise);
  const buyBack = premium * 0.5;
  let targetDays = null;
  for (let i = 1; i <= days; i++) {
    if (pricePut(spot, strike, days - i, ivPct, rate, exercise) <= buyBack) {
      targetDays = i;
      break;
    }
  }
  return {
    popFull,
    popAssign: 1 - popFull,
    expectedMove,
    targetDays,
    deltaImplied: Math.abs(g.delta),
    plus2Sigma: spot + 2 * expectedMove,
    cushion: spot - strike,
  };
}

// ---------------------------------------------------------------------------
// Scenario grid data: modeled short-put P&L per contract across spot × DTE.
// ---------------------------------------------------------------------------
export function scenarioGridData(st) {
  const { spot, strike, days, ivPct, rate, exercise, premium } = st;
  const pcts = [-0.3, -0.2, -0.15, -0.1, -0.075, -0.05, -0.025, 0, 0.05, 0.1];
  const spots = pcts.map((p) => spot * (1 + p));
  const dtes = [days, Math.round(days * 0.75), Math.round(days * 0.5), Math.round(days * 0.25), 1, 0]
    .filter((v, i, a) => a.indexOf(v) === i && v >= 0)
    .sort((a, b) => b - a);
  const pctText = (p) => `${p > 0 ? '+' : ''}${(p * 100).toFixed(1).replace(/\.0$/, '')}%`;
  const x = spots.map((s, i) => `${fmtMoney(s)} ${pctText(pcts[i])}`);
  const y = dtes.map((d) => (d === 0 ? 'Expiry' : `${d} DTE`));
  const z = dtes.map((d) => spots.map((s) => (premium - pricePut(s, strike, d, ivPct, rate, exercise)) * 100));
  const flat = z.flat();
  return { x, y, z, best: Math.max(...flat), worst: Math.min(...flat) };
}

// ---------------------------------------------------------------------------
// Outlook → structure ranking (Trade Optimizer pattern).
// ---------------------------------------------------------------------------
const OUTLOOK_ORDER = {
  neutral: ['csp', 'condor', 'bput', 'ccall'],
  bullish: ['ccall', 'csp', 'bput', 'condor'],
  bearish: ['cash', 'ccall', 'bput', 'csp'],
  eventvol: ['condor', 'bput', 'csp_half', 'ccall'],
};

export const OUTLOOKS = {
  neutral: 'Neutral',
  bullish: 'Bullish',
  bearish: 'Bearish',
  eventvol: 'High-vol / event',
};

export function structureRanking(outlook, st) {
  const { spot, strike, days, ivPct, rate, exercise, premium } = st;
  const v = ivPct / 100;
  const popPut = normCdf(d2Of(spot, strike, days, rate, v));
  const kLow = strike - 5;
  const spreadCredit = (pricePut(spot, strike, days, ivPct, rate, exercise) - pricePut(spot, kLow, days, ivPct, rate, exercise)) * 100;
  const cCallK = Math.round((spot * 1.03) / 5) * 5;
  const cCallCredit = priceCall(spot, cCallK, days, ivPct, rate, exercise) * 100;
  const condKPut = strike - 5;
  const condKCall = Math.round((spot * 1.03) / 5) * 5;
  const condCredit =
    (pricePut(spot, strike, days, ivPct, rate, exercise) -
      pricePut(spot, condKPut, days, ivPct, rate, exercise) +
      priceCall(spot, condKCall, days, ivPct, rate, exercise) -
      priceCall(spot, condKCall + 5, days, ivPct, rate, exercise)) *
    100;
  const cards = {
    csp: {
      key: 'csp',
      title: `Cash-secured put · ${fmtMoney(strike)}`,
      note: 'The seed structure: collect the modeled credit, post full collateral.',
      credit: premium * 100,
      basis: `Collateral ${fmtMoney(strike * 100)}`,
      retention: `${(popPut * 100).toFixed(1)}%`,
    },
    bput: {
      key: 'bput',
      title: `Bull put spread · ${fmtMoney(strike)} / ${fmtMoney(kLow)}`,
      note: `Defined-risk twin of the seed put: smaller credit, capped loss of ${fmtMoney(500 - spreadCredit)}.`,
      credit: spreadCredit,
      basis: `Margin ≈ ${fmtMoney(500 - Math.max(spreadCredit, 0))}`,
      retention: `${(popPut * 100).toFixed(1)}%`,
    },
    ccall: {
      key: 'ccall',
      title: `Covered call · ${fmtMoney(cCallK)}`,
      note: 'Needs owning 100 shares; income is capped upside for the month.',
      credit: cCallCredit,
      basis: `100 shares ≈ ${fmtMoney(spot * 100)}`,
      retention: `${(normCdf(-d2Of(spot, cCallK, days, rate, v)) * 100).toFixed(1)}%`,
    },
    condor: {
      key: 'condor',
      title: `Iron condor · ${fmtMoney(condKPut)}/${fmtMoney(strike)} + ${fmtMoney(condKCall)}/${fmtMoney(condKCall + 5)}`,
      note: 'Defined-risk range seller: profits only if the underlying stays inside the wings.',
      credit: condCredit,
      basis: `Margin ≈ ${fmtMoney(Math.max(500 - condCredit, 0))}`,
      retention: 'Range-only',
    },
    csp_half: {
      key: 'csp_half',
      title: 'Cash-secured put · half size',
      note: 'Same seed put at half size: keep the income idea, halve the event-day pain.',
      credit: (premium * 100) / 2,
      basis: `Collateral ${fmtMoney(strike * 100)} (half size)`,
      retention: `${(popPut * 100).toFixed(1)}%`,
    },
    cash: {
      key: 'cash',
      title: 'No sale qualifies — stand aside',
      note: 'Thin premium and adverse tape: the cash balance is the position.',
      credit: 0,
      basis: 'Risk $0',
      retention: '100% rest',
      isCash: true,
    },
  };
  return (OUTLOOK_ORDER[outlook] || OUTLOOK_ORDER.neutral).map((k, i) => ({ rank: i + 1, ...cards[k] }));
}
