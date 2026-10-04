import assert from 'node:assert/strict';
import { BML, assessShortPut, extractShortPutRows, mrMarketContext } from './graham-filter.mjs';

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

console.log('graham-filter: deterministic reference cases passed');
