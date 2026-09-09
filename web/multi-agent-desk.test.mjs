import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {renderSouls, countdown, SOULS} from './multi-agent-desk.mjs';

test('the desk has six distinct agents with models from six families', () => {
  assert.equal(SOULS.length, 6);
  const families = new Set(SOULS.map(s => s.family));
  assert.equal(families.size, 6, 'six distinct model families');
  const names = new Set(SOULS.map(s => s.name));
  assert.equal(names.size, 6, 'six distinct identities');
});

test('every agent carries ownership, boundaries, and a principle', () => {
  for (const s of SOULS) {
    assert.ok(s.owns && s.owns.length > 0, s.name + ' owns');
    assert.ok(s.notOwn && s.notOwn.length > 0, s.name + ' boundaries');
    assert.ok(s.principle && s.principle.length > 0, s.name + ' principle');
    assert.ok(s.model.includes('/'), s.name + ' model slug');
  }
});

test('countdown computes days/hours/minutes/seconds and flags live', () => {
  // Deterministic: build the target from an explicit offset in ms and assert
  // exact components, independent of when the test runs.
  const now = Date.now();
  const dayMs = 86400000, hourMs = 3600000, minMs = 60000, secMs = 1000;
  const target = new Date(now + 3 * dayMs + 2 * hourMs + 30 * minMs + 15 * secMs).toISOString();
  const cd = countdown(target);
  assert.ok(cd.d === 3, 'expected 3 days, got ' + cd.d);
  assert.ok(cd.h === 2, 'expected 2 hours, got ' + cd.h);
  assert.ok(cd.m === 30, 'expected 30 minutes, got ' + cd.m);
  assert.ok(!cd.live);
  // Rounding: exactly-now target means live immediately (diff clamped to 0).
  const past = new Date(now - 1000).toISOString();
  const gone = countdown(past);
  assert.equal(gone.live, true);
  assert.equal(gone.d, 0);
});

test('renderSouls emits the team, deployment, and progress sections', () => {
  const html = renderSouls({ total_commits: 350, generated_at: new Date().toISOString(), target_live: new Date(Date.now() + 86400000).toISOString() });
  assert.ok(html.includes('Multi-agent research desk'));
  assert.ok(html.includes('The team'));
  assert.ok(html.includes('Deployment model'));
  assert.ok(html.includes('Results &amp; progress'));
  assert.ok(html.includes('350'));
  assert.ok(!/<img[^>]*onerror/i.test(html), 'no event-handler injection');
});
