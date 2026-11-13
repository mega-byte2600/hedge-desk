/* market-ticker.mjs — scrolling markets strip + editable watchlist.
 *
 * Pattern adapted from the HARDBALL free-agent wire ticker
 * (hardball src/dashboard_p6.py, _marquee_strip_html): the content is
 * rendered twice and a CSS transform animation moves it from 0 to -50%,
 * which makes the loop continuous with no gap and no JavaScript
 * animation frame. The difference here is that the scroll duration is
 * computed from the measured track width, so the speed in pixels per
 * second stays constant no matter how many rows the feed carries.
 * HARDBALL uses a fixed 210s duration for a ~60-item wire (roughly
 * 260 px/s by estimate); this strip carries ~13 short numeric rows, so
 * a fixed 210s would crawl. The speed constant below is the tuning
 * knob; change it in one place.
 *
 * Data: the browser reads only web/market-ticker.json, a committed
 * artifact built by scripts/build_market_ticker.py from Yahoo Finance
 * v8 chart closes. No live quote request leaves the browser. When the
 * feed is missing, malformed, or stale, the strip reads
 * "data unavailable" and nothing is invented.
 *
 * Watchlist: the six default names, four indices, and three yields come
 * from the feed and cannot be removed. Added symbols live in
 * localStorage (this browser only, symbols only — no account or
 * brokerage data, per the research-input boundary). An added symbol
 * shows a quote only once a feed refresh includes it; until then it
 * reads "data unavailable".
 *
 * Brand: Noir Institutional. Direction is shown with an arrow glyph
 * and a sign, never with color: green is reserved for live-data
 * semantics (the fresh-feed dot only), and the Noir palette has no
 * red for down moves.
 */

export const FEED_URL = './market-ticker.json';
export const WATCHLIST_KEY = 'emporion.market-ticker.watchlist.v1';
export const MAX_ADDED_SYMBOLS = 20;
export const FEED_SCHEMA_VERSION = 'market-ticker-1';

/* Scroll speed. HARDBALL reference: fixed 210s over a ~60-item wire,
 * roughly 260 px/s estimated from rendered text width. 80 px/s keeps
 * short numeric rows readable; Sol owns the visual call. */
export const TICKER_SPEED_PX_PER_SECOND = 80;
export const TICKER_MIN_DURATION_S = 20;
export const TICKER_MAX_DURATION_S = 180;
export const TICKER_FALLBACK_DURATION_S = 60;

/* A feed older than this reads "data unavailable". 96 hours covers a
 * Friday close through a Monday holiday without calling fresh data
 * stale; the as-of date is always shown next to the strip. */
export const STALE_AFTER_MS = 96 * 60 * 60 * 1000;

const KINDS = new Set(['etf', 'equity', 'index', 'rate']);
const SYMBOL_RE = /^\^?[A-Z]{1,6}(\.[A-Z]{1,2})?$/;

export function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

/* Normalize a user-typed symbol. Returns the canonical symbol or null
 * when the input is not a plausible ticker. A leading ^ is kept so
 * index symbols (^GSPC) can be added the same way as equities. */
export function normalizeSymbol(raw) {
  if (typeof raw !== 'string') return null;
  const cleaned = raw.trim().toUpperCase().replace(/\s+/g, '');
  if (!SYMBOL_RE.test(cleaned)) return null;
  return cleaned;
}

export function parseWatchlist(storage) {
  let raw = null;
  try {
    raw = storage.getItem(WATCHLIST_KEY);
  } catch {
    return [];
  }
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    const out = [];
    for (const entry of parsed) {
      const sym = normalizeSymbol(entry);
      if (sym && !out.includes(sym)) out.push(sym);
    }
    return out.slice(0, MAX_ADDED_SYMBOLS);
  } catch {
    return [];
  }
}

export function saveWatchlist(storage, symbols) {
  try {
    storage.setItem(WATCHLIST_KEY, JSON.stringify(symbols));
    return true;
  } catch {
    return false;
  }
}

/* Pure list operations; the caller persists the returned list. */
export function addSymbol(list, raw) {
  const sym = normalizeSymbol(raw);
  if (!sym) return { list, added: null, error: 'Enter a ticker symbol, such as AMD or ^GSPC.' };
  if (list.includes(sym)) return { list, added: null, error: `${sym} is already on the watchlist.` };
  if (list.length >= MAX_ADDED_SYMBOLS) {
    return { list, added: null, error: `The watchlist holds ${MAX_ADDED_SYMBOLS} added symbols.` };
  }
  return { list: [...list, sym], added: sym, error: null };
}

export function removeSymbol(list, raw) {
  const sym = normalizeSymbol(raw);
  if (!sym) return list;
  return list.filter((s) => s !== sym);
}

export function validateFeed(feed) {
  if (!feed || typeof feed !== 'object' || Array.isArray(feed)) {
    return { ok: false, error: 'Feed is not an object.' };
  }
  if (feed.schema_version !== FEED_SCHEMA_VERSION) {
    return { ok: false, error: 'Feed schema version is not market-ticker-1.' };
  }
  if (Number.isNaN(Date.parse(feed.generated_at))) {
    return { ok: false, error: 'Feed has no usable generated_at timestamp.' };
  }
  if (!Array.isArray(feed.quotes) || feed.quotes.length === 0) {
    return { ok: false, error: 'Feed carries no quotes.' };
  }
  const bySymbol = new Map();
  for (const q of feed.quotes) {
    if (!q || typeof q.symbol !== 'string' || !q.symbol) return { ok: false, error: 'A quote has no symbol.' };
    if (typeof q.label !== 'string' || !q.label) return { ok: false, error: `Quote ${q.symbol} has no label.` };
    if (!KINDS.has(q.kind)) return { ok: false, error: `Quote ${q.symbol} has unknown kind.` };
    for (const key of ['price', 'previous_close', 'change', 'change_pct']) {
      if (typeof q[key] !== 'number' || !Number.isFinite(q[key])) {
        return { ok: false, error: `Quote ${q.symbol} has no usable ${key}.` };
      }
    }
    if (typeof q.market_date !== 'string' || !q.market_date) {
      return { ok: false, error: `Quote ${q.symbol} has no market date.` };
    }
    bySymbol.set(q.symbol, q);
  }
  return { ok: true, error: null, bySymbol, generatedAt: feed.generated_at, asOf: feed.as_of || null };
}

export function isFeedStale(feed, nowMs) {
  const generated = Date.parse(feed && feed.generated_at);
  if (Number.isNaN(generated)) return true;
  return nowMs - generated > STALE_AFTER_MS;
}

/* Duration for one half of the doubled track, from its measured width.
 * Clamped so a very short or very long wire stays readable. */
export function animationDurationSeconds(halfWidthPx, speedPxPerSecond = TICKER_SPEED_PX_PER_SECOND) {
  if (!Number.isFinite(halfWidthPx) || halfWidthPx <= 0) return TICKER_FALLBACK_DURATION_S;
  const seconds = halfWidthPx / speedPxPerSecond;
  return Math.min(TICKER_MAX_DURATION_S, Math.max(TICKER_MIN_DURATION_S, seconds));
}

/* How many times one set of rows must repeat inside each half of the
 * track so the half is at least as wide as the viewport. With one copy
 * narrower than the viewport the loop would show an empty gap. */
export function repeatCountFor(copyWidthPx, viewportWidthPx) {
  if (!Number.isFinite(copyWidthPx) || copyWidthPx <= 0) return 1;
  if (!Number.isFinite(viewportWidthPx) || viewportWidthPx <= 0) return 1;
  return Math.max(1, Math.ceil(viewportWidthPx / copyWidthPx));
}

function formatNumber(value) {
  return value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function signed(value, digits = 2) {
  const sign = value > 0 ? '+' : value < 0 ? '−' : '';
  return `${sign}${Math.abs(value).toFixed(digits)}`;
}

/* Display strings for one quote. Rates show percentage points, not a
 * percent change: a 10-year yield moving 4.998 to 5.103 is +0.11 pp. */
export function formatQuote(q) {
  const direction = q.change > 0 ? 'up' : q.change < 0 ? 'down' : 'flat';
  const arrow = direction === 'up' ? '▲' : direction === 'down' ? '▼' : '•';
  if (q.kind === 'rate') {
    return {
      direction,
      price: `${formatNumber(q.price)}%`,
      move: `${arrow} ${signed(q.change)} pp`,
      aria: `${q.label} ${formatNumber(q.price)} percent, ${direction === 'flat' ? 'unchanged' : `${direction} ${Math.abs(q.change).toFixed(2)} percentage points`}`,
    };
  }
  const prefix = q.kind === 'index' ? '' : '$';
  return {
    direction,
    price: `${prefix}${formatNumber(q.price)}`,
    move: `${arrow} ${signed(q.change)} (${signed(q.change_pct)}%)`,
    aria: `${q.label} ${prefix}${formatNumber(q.price)}, ${direction === 'flat' ? 'unchanged' : `${direction} ${Math.abs(q.change).toFixed(2)} (${Math.abs(q.change_pct).toFixed(2)} percent)`}`,
  };
}

function quoteItemHtml(q, added) {
  const f = formatQuote(q);
  const tag = added ? 'Added' : q.kind === 'index' ? 'Index' : q.kind === 'rate' ? 'Yield' : q.kind === 'etf' ? 'ETF' : 'Stock';
  return `<span class="mkt-item" aria-label="${escapeHtml(f.aria)}">`
    + `<span class="mkt-sym">${escapeHtml(q.symbol)}</span>`
    + `<span class="mkt-tag">${tag}</span>`
    + `<span class="mkt-label-text">${escapeHtml(q.label)}</span>`
    + `<span class="mkt-price">${escapeHtml(f.price)}</span>`
    + `<span class="mkt-move mkt-${f.direction}">${escapeHtml(f.move)}</span></span>`;
}

function unavailableItemHtml(symbol) {
  return `<span class="mkt-item mkt-unavailable" aria-label="${escapeHtml(symbol)}, data unavailable">`
    + `<span class="mkt-sym">${escapeHtml(symbol)}</span>`
    + `<span class="mkt-tag">Added</span>`
    + `<span class="mkt-na">data unavailable</span></span>`;
}

/* One set of rows, in feed order, with added symbols appended. Added
 * symbols with no quote in the feed render as data unavailable. */
export function tickerSetHtml(bySymbol, feedOrder, addedSymbols) {
  const parts = [];
  for (const sym of feedOrder) {
    const q = bySymbol.get(sym);
    if (q) parts.push(quoteItemHtml(q, false));
  }
  for (const sym of addedSymbols) {
    if (feedOrder.includes(sym)) continue;
    const q = bySymbol.get(sym);
    parts.push(q ? quoteItemHtml(q, true) : unavailableItemHtml(sym));
  }
  return parts.join('');
}

export function stripHtml({ setHtml, asOfLabel, fresh, paused }) {
  const dot = fresh ? '<span class="mkt-dot mkt-dot-live" aria-hidden="true"></span>' : '<span class="mkt-dot" aria-hidden="true"></span>';
  const status = fresh ? `as of ${asOfLabel}` : 'data unavailable';
  return `<div class="mkt-strip${paused ? ' mkt-paused' : ''}">`
    + `<div class="mkt-rail"><span class="mkt-eyebrow">Markets</span>${dot}<span class="mkt-asof">${escapeHtml(status)}</span>`
    + `<button type="button" class="mkt-btn" data-mkt-action="toggle-panel" aria-expanded="false">Watchlist</button>`
    + `<button type="button" class="mkt-btn" data-mkt-action="toggle-pause" aria-pressed="${paused ? 'true' : 'false'}">${paused ? 'Play' : 'Pause'}</button></div>`
    + `<div class="mkt-viewport"><div class="mkt-track" role="marquee" aria-label="Market prices ticker" aria-live="off">`
    + `<span class="mkt-half">${setHtml}</span><span class="mkt-half" aria-hidden="true">${setHtml}</span>`
    + `</div></div></div>`;
}

export function unavailableStripHtml(reason) {
  return `<div class="mkt-strip"><div class="mkt-rail"><span class="mkt-eyebrow">Markets</span>`
    + `<span class="mkt-dot" aria-hidden="true"></span><span class="mkt-asof">data unavailable</span>`
    + `<button type="button" class="mkt-btn" data-mkt-action="toggle-panel" aria-expanded="false">Watchlist</button></div>`
    + `<div class="mkt-viewport"><div class="mkt-static" role="status">Market data unavailable${reason ? ` — ${escapeHtml(reason)}` : ''}.</div></div></div>`;
}

export function panelHtml({ rows, addedSymbols, asOfLabel, source, formError }) {
  const rowHtml = rows.map((row) => {
    if (row.quote) {
      const f = formatQuote(row.quote);
      return `<div class="mkt-row"><span class="mkt-sym">${escapeHtml(row.symbol)}</span>`
        + `<span class="mkt-label-text">${escapeHtml(row.quote.label)}</span>`
        + `<span class="mkt-price">${escapeHtml(f.price)}</span>`
        + `<span class="mkt-move mkt-${f.direction}">${escapeHtml(f.move)}</span>`
        + (row.added ? `<button type="button" class="mkt-btn" data-mkt-action="remove" data-mkt-symbol="${escapeHtml(row.symbol)}">Remove</button>` : '<span></span>')
        + `</div>`;
    }
    return `<div class="mkt-row"><span class="mkt-sym">${escapeHtml(row.symbol)}</span>`
      + `<span class="mkt-label-text">Added symbol</span><span class="mkt-na">data unavailable</span><span></span>`
      + `<button type="button" class="mkt-btn" data-mkt-action="remove" data-mkt-symbol="${escapeHtml(row.symbol)}">Remove</button></div>`;
  }).join('');
  return `<div class="mkt-panel" hidden><form data-mkt-action="add-form">`
    + `<label class="mkt-field">Add a symbol <input name="symbol" maxlength="8" autocomplete="off" spellcheck="false" placeholder="AMD" aria-label="Ticker symbol to add"></label>`
    + `<button type="submit" class="mkt-btn mkt-btn-primary">Add</button>`
    + `<button type="button" class="mkt-btn" data-mkt-action="reset">Reset watchlist</button></form>`
    + (formError ? `<p class="mkt-error" role="alert">${escapeHtml(formError)}</p>` : '')
    + `<p class="mkt-note">Symbols are saved in this browser only. A new symbol shows a quote after the next feed refresh; until then it reads data unavailable. The feed rows cannot be removed.${asOfLabel ? ` Prices as of ${escapeHtml(asOfLabel)}.` : ''}${source ? ` Source: ${escapeHtml(source)}.` : ''}</p>`
    + `<div class="mkt-grid">${rowHtml}</div>`
    + `<p class="mkt-note">${addedSymbols.length} added symbol${addedSymbols.length === 1 ? '' : 's'}.</p></div>`;
}

function panelRows(bySymbol, feedOrder, addedSymbols) {
  const rows = feedOrder.filter((s) => bySymbol.has(s)).map((s) => ({ symbol: s, quote: bySymbol.get(s), added: false }));
  for (const sym of addedSymbols) {
    if (feedOrder.includes(sym)) continue;
    rows.push({ symbol: sym, quote: bySymbol.get(sym) || null, added: true });
  }
  return rows;
}

/* Measure one half of the track and set the duration so the speed in
 * pixels per second stays constant. Runs after render and on resize. */
export function applyTickerSpeed(host) {
  const track = host.querySelector('.mkt-track');
  const viewport = host.querySelector('.mkt-viewport');
  const half = host.querySelector('.mkt-half');
  if (!track || !viewport || !half) return;
  const halfWidth = half.scrollWidth || 0;
  const repeats = repeatCountFor(halfWidth, viewport.clientWidth || 0);
  if (repeats > 1 && !half.dataset.repeated) {
    const set = half.innerHTML;
    for (const el of host.querySelectorAll('.mkt-half')) {
      el.innerHTML = set.repeat(repeats);
      el.dataset.repeated = '1';
    }
  }
  const width = (half.scrollWidth || halfWidth) || 0;
  track.style.setProperty('--mkt-duration', `${animationDurationSeconds(width)}s`);
}

export async function mountMarketTicker(host, deps = {}) {
  const fetchFn = deps.fetchFn || fetch;
  const storage = deps.storage || (typeof localStorage !== 'undefined' ? localStorage : null);
  const nowMs = deps.nowMs || Date.now();
  const storageShim = storage || { getItem: () => null, setItem: () => {} };
  let added = parseWatchlist(storageShim);
  let paused = false;
  let panelOpen = false;
  let formError = null;

  let feed = null;
  let checked = { ok: false, error: 'Feed could not be loaded.' };
  try {
    const response = await fetchFn(FEED_URL, { cache: 'default' });
    if (!response.ok) throw new Error(`Feed request failed (${response.status}).`);
    feed = await response.json();
    checked = validateFeed(feed);
  } catch (err) {
    checked = { ok: false, error: err && err.message ? err.message : 'Feed could not be loaded.' };
  }
  const stale = checked.ok && isFeedStale(feed, nowMs);
  const usable = checked.ok && !stale;
  const bySymbol = usable ? checked.bySymbol : new Map();
  const feedOrder = usable ? feed.quotes.map((q) => q.symbol) : [];
  const asOfLabel = usable && feed.as_of ? new Date(`${feed.as_of}T12:00:00Z`).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' }) : null;

  function render() {
    const setHtml = tickerSetHtml(bySymbol, feedOrder, added);
    host.innerHTML = (usable
      ? stripHtml({ setHtml, asOfLabel, fresh: true, paused })
      : unavailableStripHtml(stale ? 'the latest feed is stale' : checked.error))
      + panelHtml({ rows: panelRows(bySymbol, feedOrder, added), addedSymbols: added, asOfLabel, source: usable ? feed.source : null, formError });
    const panel = host.querySelector('.mkt-panel');
    if (panel) panel.hidden = !panelOpen;
    const toggle = host.querySelector('[data-mkt-action="toggle-panel"]');
    if (toggle) toggle.setAttribute('aria-expanded', panelOpen ? 'true' : 'false');
    if (usable) applyTickerSpeed(host);
  }

  host.addEventListener('click', (event) => {
    const button = event.target.closest('[data-mkt-action]');
    if (!button || !host.contains(button)) return;
    const action = button.dataset.mktAction;
    if (action === 'toggle-panel') {
      panelOpen = !panelOpen;
      formError = null;
      render();
    } else if (action === 'toggle-pause') {
      paused = !paused;
      render();
    } else if (action === 'remove') {
      added = removeSymbol(added, button.dataset.mktSymbol || '');
      saveWatchlist(storageShim, added);
      formError = null;
      render();
    } else if (action === 'reset') {
      added = [];
      saveWatchlist(storageShim, added);
      formError = null;
      render();
    }
  });

  host.addEventListener('submit', (event) => {
    const form = event.target.closest('form[data-mkt-action="add-form"]');
    if (!form || !host.contains(form)) return;
    event.preventDefault();
    const input = form.querySelector('input[name="symbol"]');
    const result = addSymbol(added, input ? input.value : '');
    if (result.error) {
      formError = result.error;
    } else {
      added = result.list;
      formError = saveWatchlist(storageShim, added) ? null : 'This browser would not save the symbol.';
    }
    render();
    const next = host.querySelector('input[name="symbol"]');
    if (next) next.focus();
  });

  render();

  if (typeof window !== 'undefined' && typeof window.addEventListener === 'function') {
    let queued = false;
    window.addEventListener('resize', () => {
      if (queued) return;
      queued = true;
      const raf = typeof requestAnimationFrame === 'function' ? requestAnimationFrame : (fn) => setTimeout(fn, 0);
      raf(() => {
        queued = false;
        if (usable) applyTickerSpeed(host);
      });
    });
  }
  return { usable, stale, added };
}

/* Self-mount when loaded as a module script in the page shell. The
 * explicit #market-ticker hook is the only mount point; nothing else
 * on the page is selected or rewritten. */
if (typeof document !== 'undefined') {
  const start = () => {
    const host = document.getElementById('market-ticker');
    if (host && !host.dataset.mounted) {
      host.dataset.mounted = '1';
      mountMarketTicker(host).catch(() => {
        host.innerHTML = unavailableStripHtml('the ticker could not start');
      });
    }
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, { once: true });
  } else {
    start();
  }
}
