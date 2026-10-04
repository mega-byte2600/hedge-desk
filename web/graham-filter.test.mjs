import assert from 'node:assert/strict';
import fs from 'node:fs';
import { BML, FILTER_KEY, OWN_IT_KEY, assessShortPut, extractShortPutRows, mrMarketContext, readFilter, readOwnIt, saveFilter, saveOwnIt } from './graham-filter.mjs';

{
  const r = assessShortPut({ symbol:'SPY', spot:100, strike:95, premium:1, dte:30, ownIt:true, vix:20 });
  assert.equal(r.marginRating, 'STRONG');
  assert.equal(r.verdict, 'INVESTMENT');
  assert.ok(Math.abs(r.totalMarginPct - (5 + (1/95)*100)) < 1e-12);
  assert.ok(Math.abs(r.annualizedPct - ((1/95)*100*(365/30))) < 1e-12);
}
{
  const r = assessShortPut({ symbol:'SPY', spot:100, strike:99, premium:0, dte:30, ownIt:true, vix:20 });
  assert.equal(r.marginRating, 'THIN');
  assert.equal(r.verdict, 'NEEDS_YOU');
  assert.equal(r.reason, 'RETURN_BELOW_HURDLE');
}
{
  const r = assessShortPut({ symbol:'SPY', spot:100, strike:100, premium:0.1, dte:30, ownIt:true, vix:20 });
  assert.equal(r.marginRating, 'NONE');
  assert.equal(r.verdict, 'SPECULATION');
}
{
  const r = assessShortPut({ symbol:'SPY', spot:100, strike:90, premium:2, dte:30, ownIt:false, vix:20 });
  assert.equal(r.verdict, 'SPECULATION');
  assert.equal(r.reason, 'DO_NOT_WANT_ASSIGNED_SHARES');
}
{
  const r = assessShortPut({ symbol:'SPY', spot:100, strike:90, premium:2, dte:30, ownIt:null, vix:20 });
  assert.equal(r.verdict, 'NEEDS_YOU');
  assert.equal(r.reason, 'OWNERSHIP_QUESTION_UNANSWERED');
}
{
  const r = assessShortPut({ symbol:'XYZ', spot:100, strike:94, premium:1, dte:30, ownIt:true, vix:31 });
  assert.equal(r.market.regime, 'MANIC');
  assert.equal(r.marginRating, 'THIN');
  assert.equal(r.hurdlePct, BML.hurdleDefault);
}
{
  assert.equal(mrMarketContext(13.9).regime, 'COMPLACENT');
  assert.equal(mrMarketContext(30).regime, 'NORMAL');
  assert.equal(mrMarketContext(30.01).regime, 'MANIC');
}
{
  const feed={candidates:[
    {symbol:'AAL',method:'CASH_SECURED_PUT defined-risk premium'},
    {symbol:'AAL',method:'COVERED_CALL defined-risk premium'},
  ]};
  const nightly={cash_secured_put_scan:{AAL:{candidate:{found:true,contract_id:'AAL1',underlying_mid:'10',strike:'9',net_credit_per_share:'0.2',dte:30,expiration:'2026-11-01'}}}};
  const rows=extractShortPutRows(feed,nightly);
  assert.equal(rows[0].grahamEligible,true);
  assert.equal(rows[0].grahamMarket.premium,'0.2');
  assert.equal(rows[1].grahamEligible,false);
  assert.equal(rows[1].grahamMarket,null);
}

// Exact rating boundaries, baseline regime.
{
  const atStrong = assessShortPut({symbol:'XYZ',spot:100,strike:96,premium:0.96,dte:30,ownIt:true,vix:20});
  assert.ok(Math.abs(atStrong.totalMarginPct - 5) < 1e-12);
  assert.equal(atStrong.marginRating,'STRONG');

  const atAdequate = assessShortPut({symbol:'XYZ',spot:100,strike:99,premium:0.99,dte:30,ownIt:true,vix:20});
  assert.ok(Math.abs(atAdequate.totalMarginPct - 2) < 1e-12);
  assert.equal(atAdequate.marginRating,'ADEQUATE');

  const atThin = assessShortPut({symbol:'XYZ',spot:100,strike:100,premium:0.5,dte:30,ownIt:true,vix:20});
  assert.ok(Math.abs(atThin.totalMarginPct - 0.5) < 1e-12);
  assert.equal(atThin.marginRating,'THIN');
}
// Manic regime shifts each margin threshold upward by exactly 2 percentage points.
{
  const r = assessShortPut({symbol:'XYZ',spot:100,strike:95,premium:1.9,dte:30,ownIt:true,vix:31});
  assert.ok(Math.abs(r.totalMarginPct - 7) < 1e-12);
  assert.equal(r.marginRating,'STRONG');
}
// Bad or absent market inputs fail closed to NEEDS_YOU.
{
  assert.equal(assessShortPut({symbol:'SPY',spot:null,strike:95,premium:1,dte:30,ownIt:true,vix:20}).reason,'MISSING_MARKET_DATA');
  assert.equal(assessShortPut({symbol:'SPY',spot:100,strike:0,premium:1,dte:30,ownIt:true,vix:20}).reason,'INVALID_MARKET_DATA');
  assert.equal(assessShortPut({symbol:'SPY',spot:100,strike:95,premium:-1,dte:30,ownIt:true,vix:20}).reason,'INVALID_MARKET_DATA');
  assert.equal(assessShortPut({symbol:'SPY',spot:100,strike:95,premium:1,dte:0,ownIt:true,vix:20}).reason,'INVALID_MARKET_DATA');
}
// Persistence is symbol-level by design because the human question is whether
// the trader wants the underlying shares, not whether they like one contract.
{
  const map = new Map();
  const storage = {getItem:k=>map.has(k)?map.get(k):null,setItem:(k,v)=>map.set(k,v)};
  assert.equal(readOwnIt(storage,'AAL'),null);
  saveOwnIt(storage,'AAL',true);
  assert.equal(readOwnIt(storage,'AAL'),true);
  saveOwnIt(storage,'AAL',false);
  assert.equal(readOwnIt(storage,'AAL'),false);
  saveOwnIt(storage,'AAL',null);
  assert.equal(readOwnIt(storage,'AAL'),null);
  assert.equal(readFilter(storage),true);
  saveFilter(storage,false);
  assert.equal(map.get(FILTER_KEY),'off');
  assert.equal(readFilter(storage),false);
  saveFilter(storage,true);
  assert.equal(map.get(FILTER_KEY),'on');
  assert.equal(readFilter(storage),true);
  assert.ok(OWN_IT_KEY.includes('graham'));
}
// Production-shaped integration: the committed nightly artifact must expose
// finite VIX plus real CSP candidates that the Graham model can consume.
{
  const nightly = JSON.parse(fs.readFileSync(new URL('../artifacts/am-report-latest.json', import.meta.url), 'utf8'));
  const vix = Number(nightly?.vix_regime?.last_close);
  assert.ok(Number.isFinite(vix));
  const scans = Object.entries(nightly?.cash_secured_put_scan || {}).filter(([,scan])=>scan?.candidate?.found === true);
  assert.ok(scans.length > 0);
  for (const [symbol, scan] of scans) {
    const c = scan.candidate;
    for (const value of [c.underlying_mid,c.strike,c.net_credit_per_share,c.dte]) assert.ok(Number.isFinite(Number(value)), symbol);
    const unanswered = assessShortPut({symbol,spot:c.underlying_mid,strike:c.strike,premium:c.net_credit_per_share,dte:c.dte,ownIt:null,vix});
    assert.ok(['NEEDS_YOU','SPECULATION'].includes(unanswered.verdict));
    const rejected = assessShortPut({symbol,spot:c.underlying_mid,strike:c.strike,premium:c.net_credit_per_share,dte:c.dte,ownIt:false,vix});
    assert.equal(rejected.verdict,'SPECULATION');
    assert.equal(rejected.reason,'DO_NOT_WANT_ASSIGNED_SHARES');
  }
}

console.log('graham-filter: deterministic, boundary, persistence, and nightly-artifact cases passed');
