import test from 'node:test';
import assert from 'node:assert/strict';
import { calcRental, calcAnalysis, rentalDefaults, analysisDefaults, round100 } from './real-estate-model.mjs';

test('Analysis default Year 1 NOI matches workbook reference case', () => {
  const r=calcAnalysis();
  assert.equal(r.years[0].pgr,2346100);
  assert.equal(r.years[0].egi,2272100);
  assert.equal(r.years[0].totalExpenses,1006400);
  assert.equal(r.years[0].noi,1265700);
});

test('Analysis money rounding is nearest $100 at calculation cadence', () => {
  assert.equal(round100(123449),123400);
  assert.equal(round100(123451),123500);
});

test('Rental default Year 1 NOI matches extracted workbook behavior', () => {
  const r=calcRental();
  const y1=r.rows.slice(0,12).reduce((s,x)=>s+x.noi,0);
  assert.ok(Math.abs(y1-1704028.4)<0.01);
});

test('Rental preserves asymmetric post-120-month expense tails', () => {
  const r=calcRental();
  const m123=r.rows[122];
  assert.equal(m123.propertyTax,0);
  assert.ok(m123.utilities>0);
  assert.ok(m123.other2>0);
});

test('Corrected year-8 expenses remain active for 8-year holds', () => {
  const r=calcAnalysis({...analysisDefaults,holdYears:8});
  assert.ok(r.years[7].salary>0);
  assert.ok(r.years[7].utilities>0);
  assert.ok(r.years[7].maintenance>0);
});

test('NOI sensitivity is isolated from sale-price sensitivity', () => {
  const a=calcAnalysis({...analysisDefaults,salePriceVariation:0.10});
  const b=calcAnalysis({...analysisDefaults,salePriceVariation:0.35});
  assert.equal(a.risk.noiNpv,b.risk.noiNpv);
  assert.equal(a.risk.noiChange,b.risk.noiChange);
});

test('Sale sensitivity respects configured selling-cost economics instead of hardcoded 5%', () => {
  const a=calcAnalysis({...analysisDefaults,sellingCosts:100000});
  const b=calcAnalysis({...analysisDefaults,sellingCosts:1200000});
  assert.notEqual(a.risk.saleNpv,b.risk.saleNpv);
});

test('DCF streams produce finite default IRRs and NPV', () => {
  const r=calcAnalysis();
  assert.ok(Number.isFinite(r.beforeTaxIrr));
  assert.ok(Number.isFinite(r.afterTaxIrr));
  assert.ok(Number.isFinite(r.npv));
  assert.ok(r.ratios.dscr>0);
});

test('Rental selected-month returns and sensitivities are finite', () => {
  const r=calcRental();
  const s=r.rows[r.selectedMonth-1];
  assert.ok(Number.isFinite(s.irrAnnual));
  assert.ok(Number.isFinite(s.mirrAnnual));
  assert.equal(r.capScenarios.length,7);
  assert.equal(r.rateScenarios.length,7);
});
