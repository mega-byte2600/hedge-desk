import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  TICKER_SPEED_PX_PER_SECOND,
  MAX_ADDED_SYMBOLS,
  STALE_AFTER_MS,
  normalizeSymbol,
  parseWatchlist,
  saveWatchlist,
  addSymbol,
  removeSymbol,
  validateFeed,
  isFeedStale,
  animationDurationSeconds,
  repeatCountFor,
  formatQuote,
  escapeHtml,
  tickerSetHtml,
  stripHtml,
  panelHtml,
} from './market-ticker.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));

function fakeStorage(initial = {}) {
  const store = { ...initial };
  return {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = v; },
    _store: store,
  };
}

function quote(overrides = {}) {
  return {
    symbol: 'SPY',
    label: 'SPY, S&P 500 ETF',
    kind: 'etf',
    price: 757.12,
    previous_close: 759.81,
    change: -2.69,
    change_pct: -0.3541,
    market_date: '2026-11-12',
    ...overrides,
  };
}

function feed(overrides = {}) {
  return {
    schema_version: 'market-ticker-1',
    generated_at: '2026-11-12T20:25:41Z',
    source: 'Yahoo Finance v8 chart',
    as_of: '2026-11-12',
    quotes: [quote()],
    unavailable_symbols: [],
    ...overrides,
  };
}

test('normalizeSymbol accepts tickers and caret indices, rejects the rest', () => {
  assert.equal(normalizeSymbol('amd'), 'AMD');
  assert.equal(normalizeSymbol(' ^gspc '), '^GSPC');
  assert.equal(normalizeSymbol('BRK.B'), 'BRK.B');
  assert.equal(normalizeSymbol(''), null);
  assert.equal(normalizeSymbol('TOOLONGNAME'), null);
  assert.equal(normalizeSymbol('AAPL!'), null);
  assert.equal(normalizeSymbol('A A P L'), 'AAPL');
  assert.equal(normalizeSymbol(123), null);
  assert.equal(normalizeSymbol(null), null);
});

test('parseWatchlist tolerates corrupt storage and caps the list', () => {
  const KEY = 'emporion.market-ticker.watchlist.v1';
  assert.deepEqual(parseWatchlist(fakeStorage({})), []);
  assert.deepEqual(parseWatchlist(fakeStorage({ [KEY]: 'not json' })), []);
  assert.deepEqual(parseWatchlist(fakeStorage({ [KEY]: '{"a":1}' })), []);
  assert.deepEqual(parseWatchlist(fakeStorage({ [KEY]: '["AMD","amd","BAD!","AVGO"]' })), ['AMD', 'AVGO']);
  const many = Array.from({ length: 30 }, (_, i) => String.fromCharCode(65 + (i % 26)) + String.fromCharCode(65 + Math.floor(i / 26)));
  assert.equal(parseWatchlist(fakeStorage({ [KEY]: JSON.stringify(many) })).length, MAX_ADDED_SYMBOLS);
  assert.deepEqual(parseWatchlist({ getItem: () => { throw new Error('denied'); } }), []);
});

test('addSymbol dedupes, validates, and caps; removeSymbol drops one', () => {
  const first = addSymbol([], 'amd');
  assert.deepEqual(first.list, ['AMD']);
  assert.equal(first.added, 'AMD');
  assert.equal(first.error, null);
  const dupe = addSymbol(['AMD'], 'AMD');
  assert.equal(dupe.added, null);
  assert.match(dupe.error, /already/);
  const bad = addSymbol([], '!!!');
  assert.equal(bad.added, null);
  assert.match(bad.error, /ticker symbol/);
  const full = Array.from({ length: MAX_ADDED_SYMBOLS }, (_, i) => String.fromCharCode(65 + (i % 26)) + String.fromCharCode(65 + Math.floor(i / 26)));
  const capped = addSymbol(full, 'AMD');
  assert.equal(capped.added, null);
  assert.match(capped.error, /holds 20/);
  assert.deepEqual(removeSymbol(['AMD', 'AVGO'], 'amd'), ['AVGO']);
  assert.deepEqual(removeSymbol(['AMD'], '!!!'), ['AMD']);
});

test('saveWatchlist reports storage failure instead of throwing', () => {
  const ok = fakeStorage();
  assert.equal(saveWatchlist(ok, ['AMD']), true);
  assert.equal(JSON.parse(ok._store['emporion.market-ticker.watchlist.v1'])[0], 'AMD');
  assert.equal(saveWatchlist({ setItem: () => { throw new Error('denied'); } }, ['AMD']), false);
});

test('validateFeed accepts a good feed and rejects bad shapes', () => {
  const good = validateFeed(feed());
  assert.equal(good.ok, true);
  assert.equal(good.bySymbol.get('SPY').price, 757.12);
  assert.equal(validateFeed(null).ok, false);
  assert.equal(validateFeed(feed({ schema_version: 'other-1' })).ok, false);
  assert.equal(validateFeed(feed({ generated_at: 'nope' })).ok, false);
  assert.equal(validateFeed(feed({ quotes: [] })).ok, false);
  assert.equal(validateFeed(feed({ quotes: [quote({ price: Number.NaN })] })).ok, false);
  assert.equal(validateFeed(feed({ quotes: [quote({ kind: 'crypto' })] })).ok, false);
  assert.equal(validateFeed(feed({ quotes: [quote({ market_date: '' })] })).ok, false);
  assert.equal(validateFeed(feed({ quotes: [quote({ label: '' })] })).ok, false);
});

test('isFeedStale uses the 96-hour rule against generated_at', () => {
  assert.equal(STALE_AFTER_MS, 96 * 60 * 60 * 1000);
  const generated = Date.parse('2026-11-12T20:25:41Z');
  assert.equal(isFeedStale(feed(), generated + 95 * 3600e3), false);
  assert.equal(isFeedStale(feed(), generated + 97 * 3600e3), true);
  assert.equal(isFeedStale(feed({ generated_at: 'junk' }), generated), true);
});

test('animation duration holds pixels-per-second constant within clamps', () => {
  assert.equal(TICKER_SPEED_PX_PER_SECOND, 80);
  assert.equal(animationDurationSeconds(8000), 100);
  assert.equal(animationDurationSeconds(800), 20);
  assert.equal(animationDurationSeconds(20000), 180);
  assert.equal(animationDurationSeconds(0), 60);
  assert.equal(animationDurationSeconds(Number.NaN), 60);
  assert.equal(animationDurationSeconds(4800, 120), 40);
});

test('repeatCountFor widens short content to cover the viewport', () => {
  assert.equal(repeatCountFor(1800, 1200), 1);
  assert.equal(repeatCountFor(300, 1200), 4);
  assert.equal(repeatCountFor(1200, 1200), 1);
  assert.equal(repeatCountFor(0, 1200), 1);
  assert.equal(repeatCountFor(500, 0), 1);
});

test('formatQuote reference cases: equity, index, rate, flat', () => {
  const spy = formatQuote(quote());
  assert.equal(spy.price, '$757.12');
  assert.equal(spy.move, '▼ −2.69 (−0.35%)');
  assert.equal(spy.direction, 'down');
  const idx = formatQuote(quote({ symbol: '^GSPC', label: 'S&P 500 index', kind: 'index', price: 7592.40, previous_close: 7619.38, change: -26.98, change_pct: -0.3541 }));
  assert.equal(idx.price, '7,592.40');
  assert.equal(idx.move, '▼ −26.98 (−0.35%)');
  const rate = formatQuote(quote({ symbol: '^TNX', label: '10-year Treasury yield', kind: 'rate', price: 5.10, previous_close: 4.99, change: 0.11, change_pct: 2.20 }));
  assert.equal(rate.price, '5.10%');
  assert.equal(rate.move, '▲ +0.11 pp');
  assert.equal(rate.direction, 'up');
  const flat = formatQuote(quote({ change: 0, change_pct: 0 }));
  assert.equal(flat.direction, 'flat');
  assert.equal(flat.move, '• 0.00 (0.00%)');
});

test('escapeHtml neutralizes markup in labels and input', () => {
  assert.equal(escapeHtml('<script>"&\'</script>'), '&lt;script&gt;&quot;&amp;&#39;&lt;/script&gt;');
});

test('tickerSetHtml keeps feed order, appends added, marks missing unavailable', () => {
  const bySymbol = new Map([['SPY', quote()], ['AMD', quote({ symbol: 'AMD', label: 'Advanced Micro Devices', kind: 'equity', price: 100, previous_close: 99, change: 1, change_pct: 1.01 })]]);
  const html = tickerSetHtml(bySymbol, ['SPY'], ['AMD', 'NOPE']);
  assert.ok(html.indexOf('SPY') < html.indexOf('AMD'));
  assert.ok(html.includes('data unavailable'));
  assert.ok(html.includes('NOPE'));
  const symCount = (html.match(/mkt-sym">SPY</g) || []).length;
  assert.equal(symCount, 1);
  const dupe = tickerSetHtml(bySymbol, ['SPY'], ['SPY']);
  assert.equal((dupe.match(/mkt-sym">SPY</g) || []).length, 1);
});

test('stripHtml doubles the set once, hides the duplicate from assistive tech', () => {
  const html = stripHtml({ setHtml: '<span>X</span>', asOfLabel: 'Nov 12, 2026', fresh: true, paused: false });
  assert.equal((html.match(/mkt-half/g) || []).length, 2);
  assert.ok(html.includes('aria-hidden="true"'));
  assert.ok(html.includes('as of Nov 12, 2026'));
  assert.ok(!html.includes('mkt-paused'));
  const paused = stripHtml({ setHtml: '', asOfLabel: null, fresh: true, paused: true });
  assert.ok(paused.includes('mkt-paused'));
  assert.ok(paused.includes('aria-pressed="true"'));
});

test('panelHtml offers remove only for added rows and escapes errors', () => {
  const rows = [
    { symbol: 'SPY', quote: quote(), added: false },
    { symbol: 'NOPE', quote: null, added: true },
  ];
  const html = panelHtml({ rows, addedSymbols: ['NOPE'], asOfLabel: 'Nov 12, 2026', source: 'Yahoo Finance v8 chart', formError: '<b>oops</b>' });
  assert.equal((html.match(/data-mkt-action="remove"/g) || []).length, 1);
  assert.ok(html.includes('&lt;b&gt;oops&lt;/b&gt;'));
  assert.ok(!html.includes('<b>oops</b>'));
  assert.ok(html.includes('data unavailable'));
  assert.ok(html.includes('1 added symbol.'));
});

test('committed feed validates and carries the fixed rows', () => {
  const raw = readFileSync(join(HERE, 'market-ticker.json'), 'utf-8');
  const parsed = JSON.parse(raw);
  const checked = validateFeed(parsed);
  assert.equal(checked.ok, true, checked.error || 'feed invalid');
  const symbols = parsed.quotes.map((q) => q.symbol);
  for (const sym of ['SPY', 'QQQ', 'AAPL', 'MSFT', 'NVDA', 'TSLA', '^GSPC', '^IXIC', '^DJI', '^RUT', '^TNX', '^FVX', '^IRX']) {
    assert.ok(symbols.includes(sym), `feed missing ${sym}`);
  }
  assert.match(parsed.as_of, /^\d{4}-\d{2}-\d{2}$/);
  const kinds = Object.fromEntries(parsed.quotes.map((q) => [q.symbol, q.kind]));
  assert.equal(kinds.SPY, 'etf');
  assert.equal(kinds['^GSPC'], 'index');
  assert.equal(kinds['^TNX'], 'rate');
});
