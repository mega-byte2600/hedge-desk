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
 * Data: feed rows come only from web/market-ticker.json, a committed
 * artifact built by scripts/build_market_ticker.py (Yahoo v8 chart,
 * Nasdaq/FRED fallbacks, session-aware refresh). User-added symbols
 * are different: they are fetched live in the browser from the CNBC
 * quote API, the one keyless quote endpoint verified to send
 * Access-Control-Allow-Origin: * (Yahoo and Nasdaq send no CORS
 * headers, measured 2026-11-12; no API key is involved). An added
 * quote is stamped with the time the browser checked it, and a symbol
 * that returns no quote reads "data unavailable" — nothing invented.
 * Feed rows never use the browser fetch, and added rows never touch
 * the committed feed.
 *
 * Watchlist: the fourteen feed rows come from the feed and cannot be
 * removed; added symbols live in this browser only (localStorage).
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

/* A close-mode feed older than this reads "data unavailable". 96
 * hours covers a Friday close through a Monday holiday without
 * calling fresh data stale; the as-of date is always shown next to
 * the strip. */
export const STALE_AFTER_MS = 96 * 60 * 60 * 1000;

/* An intraday feed is stale when its newest quote_time is older than
 * this. 90 minutes covers the 30-minute refresh cadence plus deploy
 * lag plus one missed run; a feed that stops updating mid-session
 * must say so instead of showing old prices as current. */
export const INTRADAY_STALE_AFTER_MS = 90 * 60 * 1000;

/* Added symbols re-check on this cadence while the page is visible.
 * 15 minutes keeps added quotes reasonably fresh without hammering
 * the quote endpoint from an idle tab. (The committed feed refreshes
 * every 30 minutes; the two cadences are independent.) */
export const ADDED_REFRESH_MS = 15 * 60 * 1000;

/* The single external host this module may call, and only for
 * user-added symbols. Verified 2026-11-12: the endpoint answers with
 * Access-Control-Allow-Origin: *, needs no key, and returns code 1
 * for unknown symbols. Do not add another host without re-verifying
 * its CORS headers live and updating the surface test allowlist. */
export const CNBC_QUOTE_URL = 'https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol';
export const CNBC_QUOTE_PARAMS = 'requestMethod=quick&noform=1&partnerId=2&fund=1&exthrs=1&output=json';

/* Yahoo-style symbols the user may type, mapped to the CNBC symbol
 * that returns the same instrument. ^TNX maps to US10Y (a true yield
 * quote, "5.125%"), NOT to .TNX, which is a yield index scaled x10
 * (51.03 for a 5.103% yield). ^IRX is deliberately unmapped: .IRX is
 * likewise x10-scaled and US3M is a different tenor, so an added
 * ^IRX honestly reads data unavailable rather than a wrong number. */
export const CNBC_SYMBOL_MAP = {
  '^GSPC': '.SPX',
  '^IXIC': '.IXIC',
  '^DJI': '.DJI',
  '^RUT': '.RUT',
  '^TNX': 'US10Y',
  '^FVX': 'US5Y',
};

export function cnbcSymbolFor(symbol) {
  return CNBC_SYMBOL_MAP[symbol] || symbol;
}

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
  if (feed && feed.mode === 'intraday') {
    const times = (feed.quotes || [])
      .map((q) => Date.parse(q.quote_time))
      .filter((t) => Number.isFinite(t));
    if (times.length > 0) {
      return nowMs - Math.max(...times) > INTRADAY_STALE_AFTER_MS;
    }
    /* Intraday mode with no quote timestamps: fall through to the
     * generated_at rule rather than inventing a freshness verdict. */
  }
  const generated = Date.parse(feed && feed.generated_at);
  if (Number.isNaN(generated)) return true;
  return nowMs - generated > STALE_AFTER_MS;
}

/* The as-of label the strip shows. Intraday feeds label the newest
 * quote time ("10:15 AM ET · Nov 13"); close feeds label the close
 * date ("Nov 12, 2026 close"). No delay figure is ever asserted: the
 * label is the measured timestamp, nothing more. */
export function asOfLabelFor(feed) {
  if (!feed || typeof feed !== 'object') return null;
  if (feed.mode === 'intraday') {
    const times = (feed.quotes || [])
      .map((q) => Date.parse(q.quote_time))
      .filter((t) => Number.isFinite(t));
    const newest = times.length > 0 ? Math.max(...times) : Date.parse(feed.generated_at);
    if (Number.isFinite(newest)) {
      const at = new Date(newest);
      const clock = at.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', timeZone: 'America/New_York' });
      const day = at.toLocaleDateString('en-US', { month: 'short', day: 'numeric', timeZone: 'America/New_York' });
      return `${clock} ET · ${day}`;
    }
  }
  if (typeof feed.as_of === 'string' && feed.as_of) {
    const day = new Date(`${feed.as_of}T12:00:00Z`).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' });
    return `${day} close`;
  }
  return null;
}

/* "10:15 AM ET" for a browser-check timestamp (added symbols). */
export function formatCheckedTime(checkedAtMs) {
  return new Date(checkedAtMs).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', timeZone: 'America/New_York' }) + ' ET';
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

/* --- CNBC quotes for user-added symbols --- */

/* CNBC numbers arrive as strings with commas and, for yields, a
 * trailing % sign ("7,592.40", "5.125%"); change may carry a leading
 * +. Returns null when the value is not a usable number. */
export function parseCnbcNumber(value) {
  if (typeof value === 'number') return Number.isFinite(value) ? value : null;
  if (typeof value !== 'string') return null;
  const cleaned = value.trim().replaceAll(',', '').replace(/%$/, '').replace(/^\+/, '');
  if (!cleaned) return null;
  const parsed = Number(cleaned);
  return Number.isFinite(parsed) ? parsed : null;
}

/* CNBC reports an unchanged quote as the string "UNCH". */
export function parseCnbcChange(value) {
  if (typeof value === 'string' && value.trim().toUpperCase() === 'UNCH') return 0;
  return parseCnbcNumber(value);
}

/* Parse one CNBC FormattedQuote payload into a quote-shaped object,
 * or null when the symbol is unknown or the payload unusable. The
 * previous close is DERIVED (last minus change): CNBC's own
 * previous_day_closing field echoes the last price and is unusable.
 * quote_time is the browser's check time: CNBC's last_time format
 * varies, so the honest stamp is when this browser observed the
 * quote, and the UI labels it as a check time. */
export function parseCnbcQuote(payload, userSymbol, fetchedAtMs) {
  const list = payload && payload.FormattedQuoteResult && payload.FormattedQuoteResult.FormattedQuote;
  const raw = Array.isArray(list) ? list[0] : null;
  if (!raw || raw.code !== 0) return null;
  const last = parseCnbcNumber(raw.last);
  const change = parseCnbcChange(raw.change);
  if (last === null || change === null) return null;
  const prev = last - change;
  if (!Number.isFinite(prev) || prev === 0) return null;
  const round4 = (v) => Math.round(v * 10000) / 10000;
  const kind = raw.type === 'BOND' ? 'rate' : raw.type === 'INDEX' ? 'index' : 'equity';
  const label = typeof raw.name === 'string' && raw.name.trim() ? raw.name.trim() : userSymbol;
  const marketDate = typeof raw.last_time === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(raw.last_time) ? raw.last_time : null;
  return {
    symbol: userSymbol,
    label,
    kind,
    price: round4(last),
    previous_close: round4(prev),
    change: round4(change),
    change_pct: round4((change / prev) * 100),
    market_date: marketDate,
    quote_time: new Date(fetchedAtMs).toISOString(),
    time_basis: 'fetch',
    session: 'intraday',
    source: 'CNBC quote API',
    checked_at_ms: fetchedAtMs,
  };
}

export function cnbcQuoteUrl(userSymbol) {
  const url = new URL(CNBC_QUOTE_URL);
  url.search = `${CNBC_QUOTE_PARAMS}&symbols=${encodeURIComponent(cnbcSymbolFor(userSymbol))}`;
  return url.toString();
}

/* Fetch quotes for added symbols, four requests at a time (the CNBC
 * endpoint answers one symbol per request; batching with commas
 * returns a single empty quote). Every failure leaves the symbol
 * without a quote — the row reads data unavailable. */
export async function fetchAddedQuotes(symbols, fetchFn, fetchedAtMs) {
  const out = new Map();
  const signal = typeof AbortSignal !== 'undefined' && typeof AbortSignal.timeout === 'function'
    ? AbortSignal.timeout(15000)
    : undefined;
  for (let i = 0; i < symbols.length; i += 4) {
    const chunk = symbols.slice(i, i + 4);
    const results = await Promise.all(chunk.map(async (symbol) => {
      try {
        const response = await fetchFn(cnbcQuoteUrl(symbol), { signal });
        if (!response.ok) return null;
        return parseCnbcQuote(await response.json(), symbol, fetchedAtMs);
      } catch {
        return null;
      }
    }));
    for (const quote of results) {
      if (quote) out.set(quote.symbol, quote);
    }
  }
  return out;
}

function quoteItemHtml(q, added) {
  const f = formatQuote(q);
  const tag = added ? 'Added' : q.kind === 'index' ? 'Index' : q.kind === 'rate' ? 'Yield' : q.kind === 'etf' ? 'ETF' : 'Stock';
  const title = added && q.source === 'CNBC quote API' && Number.isFinite(q.checked_at_ms)
    ? ` title="${escapeHtml(`${q.source}, checked ${formatCheckedTime(q.checked_at_ms)}`)}"` : '';
  return `<span class="mkt-item" aria-label="${escapeHtml(f.aria)}"${title}>`
    + `<span class="mkt-sym">${escapeHtml(q.symbol)}</span>`
    + `<span class="mkt-tag">${tag}</span>`
    + `<span class="mkt-label-text">${escapeHtml(q.label)}</span>`
    + `<span class="mkt-price">${escapeHtml(f.price)}</span>`
    + `<span class="mkt-move mkt-${f.direction}">${escapeHtml(f.move)}</span></span>`;
}

function unavailableItemHtml(symbol, tag = 'Added') {
  return `<span class="mkt-item mkt-unavailable" aria-label="${escapeHtml(symbol)}, data unavailable">`
    + `<span class="mkt-sym">${escapeHtml(symbol)}</span>`
    + `<span class="mkt-tag">${escapeHtml(tag)}</span>`
    + `<span class="mkt-na">data unavailable</span></span>`;
}

function kindTag(kind) {
  return kind === 'index' ? 'Index' : kind === 'rate' ? 'Yield' : kind === 'etf' ? 'ETF' : 'Stock';
}

/* One set of rows, in feed order, with added symbols appended. Feed
 * rows whose quote quarantined render as data unavailable rows (from
 * opts.unavailable) instead of silently vanishing; added symbols
 * resolve from the feed first, then from live CNBC quotes
 * (opts.addedQuotes), and otherwise read data unavailable. */
export function tickerSetHtml(bySymbol, feedOrder, addedSymbols, opts = {}) {
  const addedQuotes = opts.addedQuotes || new Map();
  const unavailable = new Map((opts.unavailable || []).map((u) => [u.symbol, u]));
  const parts = [];
  for (const sym of feedOrder) {
    const q = bySymbol.get(sym);
    if (q) {
      parts.push(quoteItemHtml(q, false));
    } else if (unavailable.has(sym)) {
      parts.push(unavailableItemHtml(sym, kindTag(unavailable.get(sym).kind)));
    }
  }
  for (const sym of addedSymbols) {
    if (feedOrder.includes(sym)) continue;
    const q = bySymbol.get(sym) || addedQuotes.get(sym);
    parts.push(q ? quoteItemHtml(q, true) : unavailableItemHtml(sym));
  }
  return parts.join('');
}

export function stripHtml({ setHtml, asOfLabel, fresh, paused }) {
  const dot = fresh ? '<span class="mkt-dot mkt-dot-live" aria-hidden="true"></span>' : '<span class="mkt-dot" aria-hidden="true"></span>';
  const status = fresh ? (asOfLabel ? `as of ${asOfLabel}` : 'as of latest feed') : 'data unavailable';
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

export function panelHtml({ rows, addedSymbols, asOfLabel, source, formError, addedCheckedLabel }) {
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
      + `<span class="mkt-label-text">${escapeHtml(row.label || 'Added symbol')}</span><span class="mkt-na">data unavailable</span><span></span>`
      + (row.added ? `<button type="button" class="mkt-btn" data-mkt-action="remove" data-mkt-symbol="${escapeHtml(row.symbol)}">Remove</button>` : '<span></span>') + `</div>`;
  }).join('');
  const addedNote = addedCheckedLabel ? ` Added quotes via CNBC, checked ${escapeHtml(addedCheckedLabel)}.` : '';
  return `<div class="mkt-panel" hidden><form data-mkt-action="add-form">`
    + `<label class="mkt-field">Add a symbol <input name="symbol" maxlength="8" autocomplete="off" spellcheck="false" placeholder="AMD" aria-label="Ticker symbol to add"></label>`
    + `<button type="submit" class="mkt-btn mkt-btn-primary">Add</button>`
    + `<button type="button" class="mkt-btn" data-mkt-action="reset">Reset watchlist</button></form>`
    + (formError ? `<p class="mkt-error" role="alert">${escapeHtml(formError)}</p>` : '')
    + `<p class="mkt-note">Symbols are saved in this browser only. An added symbol fetches a live quote in this browser; one that returns no quote reads data unavailable. The feed rows cannot be removed.${asOfLabel ? ` Prices as of ${escapeHtml(asOfLabel)}.` : ''}${source ? ` Source: ${escapeHtml(source)}.` : ''}${addedNote}</p>`
    + `<div class="mkt-grid">${rowHtml}</div>`
    + `<p class="mkt-note">${addedSymbols.length} added symbol${addedSymbols.length === 1 ? '' : 's'}.</p></div>`;
}

function panelRows(bySymbol, feedOrder, addedSymbols, opts = {}) {
  const addedQuotes = opts.addedQuotes || new Map();
  const unavailable = new Map((opts.unavailable || []).map((u) => [u.symbol, u]));
  const rows = [];
  for (const s of feedOrder) {
    if (bySymbol.has(s)) {
      rows.push({ symbol: s, quote: bySymbol.get(s), added: false });
    } else if (unavailable.has(s)) {
      rows.push({ symbol: s, quote: null, label: unavailable.get(s).label || s, added: false });
    }
  }
  for (const sym of addedSymbols) {
    if (feedOrder.includes(sym)) continue;
    rows.push({ symbol: sym, quote: bySymbol.get(sym) || addedQuotes.get(sym) || null, added: true });
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

/* Display order: the feed's explicit order (which includes
 * quarantined rows) when present, else quote order (v1 feeds). */
export function displayOrder(feed) {
  if (Array.isArray(feed.order) && feed.order.length > 0) return [...feed.order];
  return (feed.quotes || []).map((q) => q.symbol);
}

/* Quarantined rows with labels: the feed's detailed list when
 * present, else the v1 plain symbol list. */
export function unavailableDetails(feed) {
  if (Array.isArray(feed.unavailable) && feed.unavailable.length > 0) return feed.unavailable;
  if (Array.isArray(feed.unavailable_symbols)) {
    return feed.unavailable_symbols.map((s) => ({ symbol: s, label: s, kind: 'equity' }));
  }
  return [];
}

export async function mountMarketTicker(host, deps = {}) {
  const fetchFn = deps.fetchFn || fetch;
  const storage = deps.storage || (typeof localStorage !== 'undefined' ? localStorage : null);
  const storageShim = storage || { getItem: () => null, setItem: () => {} };
  let added = parseWatchlist(storageShim);
  let paused = false;
  let panelOpen = false;
  let formError = null;

  let feed = null;
  let checked = { ok: false, error: 'Feed could not be loaded.' };
  let stale = false;
  let usable = false;
  let bySymbol = new Map();
  let feedOrder = [];
  let unavailableEntries = [];
  let asOfLabel = null;
  let addedQuotes = new Map();
  let addedCheckedLabel = null;

  async function loadFeed(nowMs) {
    try {
      const response = await fetchFn(FEED_URL, { cache: 'no-cache' });
      if (!response.ok) throw new Error(`Feed request failed (${response.status}).`);
      feed = await response.json();
      checked = validateFeed(feed);
    } catch (err) {
      feed = null;
      checked = { ok: false, error: err && err.message ? err.message : 'Feed could not be loaded.' };
    }
    stale = checked.ok && isFeedStale(feed, nowMs);
    usable = checked.ok && !stale;
    bySymbol = usable ? checked.bySymbol : new Map();
    feedOrder = usable ? displayOrder(feed) : [];
    unavailableEntries = usable ? unavailableDetails(feed) : [];
    asOfLabel = usable ? asOfLabelFor(feed) : null;
  }

  async function refreshAdded(nowMs) {
    const wanted = added.filter((s) => !feedOrder.includes(s) && !bySymbol.has(s));
    addedQuotes = wanted.length > 0 ? await fetchAddedQuotes(wanted, fetchFn, nowMs) : new Map();
    const times = [...addedQuotes.values()].map((q) => q.checked_at_ms).filter((t) => Number.isFinite(t));
    addedCheckedLabel = times.length > 0 ? formatCheckedTime(Math.max(...times)) : null;
  }

  function render() {
    const setHtml = tickerSetHtml(bySymbol, feedOrder, added, { addedQuotes, unavailable: unavailableEntries });
    host.innerHTML = (usable
      ? stripHtml({ setHtml, asOfLabel, fresh: true, paused })
      : unavailableStripHtml(stale ? 'the latest feed is stale' : checked.error))
      + panelHtml({ rows: panelRows(bySymbol, feedOrder, added, { addedQuotes, unavailable: unavailableEntries }), addedSymbols: added, asOfLabel, source: usable ? feed.source : null, formError, addedCheckedLabel });
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
      const sym = normalizeSymbol(button.dataset.mktSymbol || '');
      added = removeSymbol(added, button.dataset.mktSymbol || '');
      if (sym) addedQuotes.delete(sym);
      saveWatchlist(storageShim, added);
      formError = null;
      render();
    } else if (action === 'reset') {
      added = [];
      addedQuotes = new Map();
      addedCheckedLabel = null;
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
      render();
    } else {
      added = result.list;
      formError = saveWatchlist(storageShim, added) ? null : 'This browser would not save the symbol.';
      render();
      /* The new row renders immediately (data unavailable until its
       * quote arrives), then upgrades in place when CNBC answers. */
      refreshAdded(Date.now()).then(() => {
        render();
        const next = host.querySelector('input[name="symbol"]');
        if (next) next.focus();
      });
      return;
    }
    const next = host.querySelector('input[name="symbol"]');
    if (next) next.focus();
  });

  await loadFeed(deps.nowMs || Date.now());
  render();
  await refreshAdded(Date.now());
  render();

  /* Long-open pages stay fresh without a reload: re-read the feed
   * artifact and re-check added symbols every 15 minutes, skipping
   * ticks while the tab is hidden so idle pages make no requests. */
  if (typeof setInterval === 'function' && deps.refresh !== false) {
    const tick = async () => {
      if (typeof document !== 'undefined' && document.visibilityState === 'hidden') return;
      const nowMs = Date.now();
      await loadFeed(nowMs);
      await refreshAdded(nowMs);
      render();
    };
    setInterval(() => { tick().catch(() => {}); }, deps.refreshMs || ADDED_REFRESH_MS);
  }

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
