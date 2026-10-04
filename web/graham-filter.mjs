export const BML = Object.freeze({
  margin: Object.freeze({ strong: 5.0, adequate: 2.0, thin: 0.5 }),
  manicVix: 30,
  manicBump: 2.0,
  complacentVix: 14,
  hurdleDefault: 15.0,
  hurdles: Object.freeze({ SPY: 15, QQQ: 15, AAPL: 20, TSLA: 25, NVDA: 22, MSFT: 18 }),
});

const finite = value => Number.isFinite(Number(value));

export function mrMarketContext(vix, config = BML) {
  const value = Number(vix);
  if (!Number.isFinite(value)) {
    return { regime: 'UNAVAILABLE', vix: null, read: 'VIX unavailable. Graham thresholds remain at baseline.' };
  }
  if (value > config.manicVix) {
    return { regime: 'MANIC', vix: value, read: 'Premiums are fat. Demand more margin of safety.', marginBump: config.manicBump };
  }
  if (value < config.complacentVix) {
    return { regime: 'COMPLACENT', vix: value, read: "Don't chase pennies.", marginBump: 0 };
  }
  return { regime: 'NORMAL', vix: value, read: 'Normal volatility regime. Use baseline discipline.', marginBump: 0 };
}

export function assessShortPut(input, config = BML) {
  const symbol = String(input?.symbol || '').toUpperCase();
  const ownIt = input?.ownIt === true ? true : input?.ownIt === false ? false : null;
  const vix = finite(input?.vix) ? Number(input.vix) : null;
  const market = mrMarketContext(vix, config);
  const hurdle = Number(config.hurdles[symbol] ?? config.hurdleDefault);

  if (![input?.spot, input?.strike, input?.premium, input?.dte].every(finite)) {
    return {
      verdict: 'NEEDS_YOU',
      marginRating: 'UNAVAILABLE',
      totalMarginPct: null,
      annualizedPct: null,
      hurdlePct: hurdle,
      returnPass: false,
      ownIt,
      reason: 'MISSING_MARKET_DATA',
      market,
    };
  }

  const spot = Number(input.spot);
  const strike = Number(input.strike);
  const premium = Number(input.premium);
  const dte = Number(input.dte);
  if (spot <= 0 || strike <= 0 || premium < 0 || dte <= 0) {
    return {
      verdict: 'NEEDS_YOU',
      marginRating: 'UNAVAILABLE',
      totalMarginPct: null,
      annualizedPct: null,
      hurdlePct: hurdle,
      returnPass: false,
      ownIt,
      reason: 'INVALID_MARKET_DATA',
      market,
    };
  }

  const totalMarginPct = ((spot - strike) / spot) * 100 + (premium / strike) * 100;
  const annualizedPct = (premium / strike) * 100 * (365 / dte);
  const bump = market.regime === 'MANIC' ? config.manicBump : 0;
  const thresholds = {
    strong: config.margin.strong + bump,
    adequate: config.margin.adequate + bump,
    thin: config.margin.thin + bump,
  };
  const marginRating =
    totalMarginPct >= thresholds.strong ? 'STRONG' :
    totalMarginPct >= thresholds.adequate ? 'ADEQUATE' :
    totalMarginPct >= thresholds.thin ? 'THIN' : 'NONE';
  const returnPass = annualizedPct >= hurdle;

  let verdict = 'INVESTMENT';
  let reason = 'ALL_TESTS_PASS';
  if (ownIt === false) {
    verdict = 'SPECULATION';
    reason = 'DO_NOT_WANT_ASSIGNED_SHARES';
  } else if (marginRating === 'NONE') {
    verdict = 'SPECULATION';
    reason = 'NO_MARGIN_OF_SAFETY';
  } else if (ownIt === null) {
    verdict = 'NEEDS_YOU';
    reason = 'OWNERSHIP_QUESTION_UNANSWERED';
  } else if (!returnPass) {
    verdict = 'NEEDS_YOU';
    reason = 'RETURN_BELOW_HURDLE';
  }

  return { verdict, marginRating, totalMarginPct, annualizedPct, hurdlePct: hurdle, returnPass, ownIt, reason, market };
}

export function extractShortPutRows(candidateFeed, nightlyReport) {
  const rows = Array.isArray(candidateFeed?.candidates) ? candidateFeed.candidates : [];
  const scans = nightlyReport?.cash_secured_put_scan || {};
  return rows.map(row => {
    const isShortPut = String(row.method || '').startsWith('CASH_SECURED_PUT');
    if (!isShortPut) return { ...row, grahamEligible: false, grahamMarket: null };
    const scan = scans[row.symbol]?.candidate;
    if (!scan || scan.found !== true) return { ...row, grahamEligible: true, grahamMarket: null };
    return {
      ...row,
      grahamEligible: true,
      grahamMarket: {
        contractId: scan.contract_id || '',
        spot: scan.underlying_mid,
        strike: scan.strike,
        premium: scan.net_credit_per_share,
        dte: scan.dte,
        expiration: scan.expiration || '',
      },
    };
  });
}

export const OWN_IT_KEY = 'emporion.graham.ownit.v1';
export const FILTER_KEY = 'emporion.graham.filter.v1';

export function readOwnIt(storage, symbol) {
  try {
    const state = JSON.parse(storage.getItem(OWN_IT_KEY) || '{}');
    return state[symbol] === true ? true : state[symbol] === false ? false : null;
  } catch {
    return null;
  }
}

export function saveOwnIt(storage, symbol, value) {
  const state = (() => {
    try { return JSON.parse(storage.getItem(OWN_IT_KEY) || '{}'); } catch { return {}; }
  })();
  if (value === null) delete state[symbol];
  else state[symbol] = Boolean(value);
  storage.setItem(OWN_IT_KEY, JSON.stringify(state));
}

export function readFilter(storage) {
  try { return storage.getItem(FILTER_KEY) !== 'off'; } catch { return true; }
}

export function saveFilter(storage, enabled) {
  storage.setItem(FILTER_KEY, enabled ? 'on' : 'off');
}
