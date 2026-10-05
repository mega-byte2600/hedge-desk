import test from 'node:test';
import assert from 'node:assert/strict';
import { realEstatePage, mountRealEstate } from './real-estate-ui.js';

test('Real Estate UI module imports without browser globals at module load', () => {
  assert.equal(typeof realEstatePage, 'function');
  assert.equal(typeof mountRealEstate, 'function');
});

test('Real Estate page exposes both workbook-parity tabs and no execution controls', () => {
  const html=realEstatePage();
  assert.match(html,/data-re-tab="rental"/);
  assert.match(html,/data-re-tab="analysis"/);
  assert.match(html,/Investment inputs/);
  assert.match(html,/Analysis inputs/);
  assert.doesNotMatch(html,/order|trade_authorized|execute trade/i);
});

test('Real Estate page does not expose internal workbook defect commentary', () => {
  const html=realEstatePage();
  assert.doesNotMatch(html,/Corrected model port/i);
  assert.doesNotMatch(html,/Known spreadsheet defects/i);
  assert.doesNotMatch(html,/year-8/i);
  assert.doesNotMatch(html,/NOI sensitivity sale-price leakage/i);
});
