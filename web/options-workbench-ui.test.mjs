// DOM-level lock for the delayed-data reference note (GP decision C3,
// SOUL.md order 4; ENGINEERING_LESSONS rule 1 and rule 2). A source-text grep
// passes even if the note is never appended; this renders the section with a
// minimal fake DOM and asserts the hooked note is actually in the output.
import test from 'node:test';
import assert from 'node:assert/strict';

class FakeEl {
  constructor(tag) { this.tagName = tag; this.children = []; this.attrs = {}; this.className = ''; this.textContent = ''; this.style = {}; }
  appendChild(c) { this.children.push(c); return c; }
  setAttribute(k, v) { this.attrs[k] = String(v); }
  getAttribute(k) { return this.attrs[k] ?? null; }
  addEventListener() {}
  querySelector() { return null; }
}
globalThis.document = { createElement: (t) => new FakeEl(t), head: new FakeEl('head'), body: new FakeEl('body') };

const { probSection } = await import('./options-workbench-ui.js');

function find(node, pred) {
  if (pred(node)) return node;
  for (const c of node.children || []) { const hit = find(c, pred); if (hit) return hit; }
  return null;
}

const ST = { spot: 762.63, strike: 749, days: 29, ivPct: 15.26, rate: 0.05292, exercise: 'american', premium: 6.485 };
const SEED = { asOfLabel: '2026-11-18', sourceLabel: 'Cboe delayed chain', dataMode: 'batch' };

test('probability section renders the delayed-data reference note under its hook', () => {
  const box = probSection(SEED, ST, false);
  const note = find(box, (n) => n.getAttribute && n.getAttribute('data-hook') === 'wb-prob-delayed-reference');
  assert.ok(note, 'reference note must be appended to the rendered section');
  assert.equal(note.textContent, 'Reference only — computed from delayed option data. Not a probability claim.');
});

test('original risk-neutral sentence still renders unchanged', () => {
  const box = probSection(SEED, ST, false);
  const hit = find(box, (n) => typeof n.textContent === 'string' && n.textContent.includes('a risk-neutral market quote, not a forecast of where the stock goes.'));
  assert.ok(hit);
});
