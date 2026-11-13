#!/usr/bin/env python3
"""Build the market-ticker feed: web/market-ticker.json.

Session-aware: during the regular NYSE session the feed carries
intraday quotes from Yahoo Finance v8 1-minute bars (last bar + prior
close, each quote stamped with its own quote_time); after the close it
carries daily closes. A dumb 30-minute cron tick drives this script
and the script itself decides whether the market is open, so nights,
weekends, and holidays stay quiet with no push and no deploy churn.

Modes (--mode auto is the default):
  auto      market state from the America/New_York clock: session
            (09:30-16:00 ET, weekdays) -> intraday; 16:00-16:35 ET ->
            one close refresh; pre-market, after-hours, and weekends
            exit 0 without touching the feed.
  intraday  pull 1m bars regardless of the clock (manual runs, tests).
  close     pull 5d/1d closes regardless of the clock.

Holiday rule: in intraday mode the run first probes SPY 1-minute bars.
If the newest bar is not dated today (ET), there was no session today
and the run exits 0 keeping the last close feed. A failed probe (Yahoo
unreachable) does NOT count as a holiday: the run proceeds and the
per-symbol fallback chain decides.

Fallback chain, per symbol, in order (never a wrong number: a symbol
whose sources all fail is quarantined, not guessed):
  1. Yahoo Finance v8 chart (browser User-Agent only, no cookie/crumb).
  2. Nasdaq quote API chart endpoint, for equities/ETFs (same symbol)
     and the Nasdaq Composite (^IXIC via COMP). Change is computed
     within Nasdaq's own basis (last sale vs its previousClose); the
     quote is stamped with the fetch time because Nasdaq's timestamp
     is date-only. ^GSPC, ^DJI, and ^RUT have no verified Nasdaq
     route (their Nasdaq symbols return "Symbol not exists"), so
     they are Yahoo-only and quarantine on Yahoo failure.
  3. FRED daily yields, for ^TNX (DGS10), ^FVX (DGS5), ^IRX (DTB3),
     via the keyed fred_observations helper. FRED observations lag
     one to two days; the quote is stamped with the observation date
     and session "close", never presented as today's yield. If the
     helper is absent (this checkout is not the cron VM), yields
     degrade to quarantine instead of failing the run.

Quarantine rule: a failed symbol is recorded under "unavailable" (with
its label, kind, and reason) and the feed still writes when at least
one quote succeeds, so one dead symbol cannot blank the strip. When
every symbol fails, the run exits 2 and writes nothing, leaving the
previous feed in place. This replaces the old all-or-nothing rule,
which was too blunt for intraday refresh: a single Yahoo 500 during
the session must not freeze all fourteen rows.

Skip-if-unchanged: by default the run writes nothing when the quotes,
unavailable list, display order, as-of date, and mode are identical
to the committed feed, so the 30-minute tick does not churn deploys
on quiet stretches. --force writes regardless. generated_at and
market_state are excluded from the comparison (the first changes on
every run; the second is a clock label, not data).

Delay honesty: no delay figure is ever asserted. Quotes carry
quote_time (last bar, fetch time, or observation date, per
time_basis) and the strip displays the as-of time from those
timestamps. Whether Yahoo's 1m bars lag the live market, and by how
much, was measured live on Friday 2026-11-13 before
any "delayed" label is considered.

The browser never calls Yahoo or Nasdaq (both send no CORS headers);
it reads only this committed artifact for feed rows. User-added
symbols are fetched in the browser from the CNBC quote API, which
does send Access-Control-Allow-Origin: *. See web/market-ticker.mjs.

Standard library only. The FRED route shells out to the keyed helper
CLI (subprocess is stdlib); the helper itself is outside this repo.

Usage:
    python3 scripts/build_market_ticker.py
    python3 scripts/build_market_ticker.py --mode close --force
    python3 scripts/build_market_ticker.py --extra-symbols AMD,AVGO
    python3 scripts/build_market_ticker.py --out /tmp/market-ticker.json
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, time, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "web" / "market-ticker.json"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
TIMEOUT = 30
ET = ZoneInfo("America/New_York")

# (Yahoo symbol, display label, kind). Labels name exactly what each row
# is: SPY/QQQ are ETFs, not the indices themselves; ^FVX is the 5-year
# yield, never the 2-year; ^IRX is the 13-week bill, not a 2-year proxy.
DEFAULT_SYMBOLS = (
    ("SPY", "SPY, S&P 500 ETF", "etf"),
    ("QQQ", "QQQ, Nasdaq-100 ETF", "etf"),
    ("AAPL", "Apple", "equity"),
    ("MSFT", "Microsoft", "equity"),
    ("NVDA", "NVIDIA", "equity"),
    ("TSLA", "Tesla", "equity"),
    ("PLTR", "Palantir", "equity"),
    ("^GSPC", "S&P 500 index", "index"),
    ("^IXIC", "Nasdaq Composite index", "index"),
    ("^DJI", "Dow Jones Industrial Average", "index"),
    ("^RUT", "Russell 2000 index", "index"),
    ("^TNX", "10-year Treasury yield", "rate"),
    ("^FVX", "5-year Treasury yield", "rate"),
    ("^IRX", "13-week Treasury bill yield", "rate"),
)

SESSION_OPEN = time(9, 30)
SESSION_CLOSE = time(16, 0)
CLOSE_WINDOW_END = time(16, 35)

# Nasdaq fallback mapping for the one index with a verified Nasdaq
# route. Equities/ETFs map to themselves; ^GSPC, ^DJI, ^RUT have no
# verified Nasdaq symbol and stay Yahoo-only (see module docstring).
NASDAQ_INDEX_FALLBACK = {"^IXIC": "COMP"}
FRED_SERIES = {"^TNX": "DGS10", "^FVX": "DGS5", "^IRX": "DTB3"}
FRED_HELPER_DEFAULT = (
    Path.home()
    / "workspace"
    / "custom-connectors"
    / "custom.legacy-fred"
    / "bin"
    / "fred_observations.py"
)
FRED_HELPER_PYTHONPATH = "/opt/muse/skills/custom-connector-setup/bin"


class Quarantined(RuntimeError):
    """All quote sources failed for one symbol; the row quarantines."""

    def __init__(self, symbol: str, reason: str):
        super().__init__(f"{symbol}: {reason}")
        self.symbol = symbol
        self.reason = reason


def iso_z(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def et_date_of(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp, tz=ET).date().isoformat()


def market_state(now_et: datetime) -> str:
    """Regular-session state for an America/New_York-aware datetime."""
    if now_et.weekday() >= 5:
        return "weekend"
    tick = now_et.time()
    if tick < SESSION_OPEN:
        return "pre-market"
    if tick < SESSION_CLOSE:
        return "session"
    if tick < CLOSE_WINDOW_END:
        return "close-window"
    return "after-hours"


def fetch_yahoo_chart(symbol: str, range_: str, interval: str) -> tuple[list, list, dict]:
    """Return (timestamps, closes, meta) from the Yahoo v8 chart API."""
    url = (
        "https://query2.finance.yahoo.com/v8/finance/chart/"
        f"{urllib.parse.quote(symbol, safe='')}"
        f"?range={range_}&interval={interval}&includePrePost=false"
    )
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, ValueError) as exc:
        raise RuntimeError(f"{symbol}: request failed: {exc}") from exc
    result = (payload.get("chart") or {}).get("result") or []
    if not result:
        err = (payload.get("chart") or {}).get("error") or {}
        raise RuntimeError(
            f"{symbol}: no chart result: {err.get('description', 'unknown')}"
        )
    meta = result[0].get("meta") or {}
    quote = ((result[0].get("indicators") or {}).get("quote") or [{}])[0]
    closes = quote.get("close") or []
    timestamps = result[0].get("timestamp") or []
    if len(closes) != len(timestamps):
        raise RuntimeError(f"{symbol}: close/timestamp length mismatch")
    return timestamps, closes, meta


def parse_intraday_bars(
    timestamps: list, closes: list, today_et: str, symbol: str
) -> tuple[int, float]:
    """Newest usable 1m bar; it must be dated today (ET)."""
    pairs = [(t, c) for t, c in zip(timestamps, closes) if c is not None]
    if not pairs:
        raise RuntimeError(f"{symbol}: no usable intraday bars")
    last_ts, last_close = pairs[-1]
    if et_date_of(last_ts) != today_et:
        raise RuntimeError(f"{symbol}: newest bar is not dated today")
    return last_ts, float(last_close)


def previous_close_from_daily(symbol: str, today_et: str) -> float:
    """Prior close from the 5d/1d series, for symbols whose 1m meta
    carries no previousClose (PLTR). The newest daily bar must be
    today's in-progress bar, so the bar before it is the prior close;
    otherwise the basis is wrong and the caller must fall back."""
    timestamps, closes, _meta = fetch_yahoo_chart(symbol, "5d", "1d")
    pairs = [(t, c) for t, c in zip(timestamps, closes) if c is not None]
    if len(pairs) < 2:
        raise RuntimeError(f"{symbol}: fewer than two daily closes")
    if et_date_of(pairs[-1][0]) != today_et:
        raise RuntimeError(f"{symbol}: daily series has no bar dated today")
    return float(pairs[-2][1])


def yahoo_intraday_quote(
    symbol: str, label: str, kind: str, today_et: str
) -> dict:
    timestamps, closes, meta = fetch_yahoo_chart(symbol, "1d", "1m")
    last_ts, last = parse_intraday_bars(timestamps, closes, today_et, symbol)
    prev = meta.get("previousClose")
    if prev is None:
        prev = meta.get("chartPreviousClose")
    if prev is None:
        prev = previous_close_from_daily(symbol, today_et)
    prev = float(prev)
    if prev == 0:
        raise RuntimeError(f"{symbol}: previous close is zero")
    return {
        "symbol": symbol,
        "label": label,
        "kind": kind,
        "price": round(last, 4),
        "previous_close": round(prev, 4),
        "change": round(last - prev, 4),
        "change_pct": round((last - prev) / prev * 100.0, 4),
        "market_date": today_et,
        "quote_time": iso_z(datetime.fromtimestamp(last_ts, tz=timezone.utc)),
        "time_basis": "bar",
        "session": "intraday",
        "source": "Yahoo Finance v8 chart (1m)",
        "currency": meta.get("currency") or ("USD" if kind != "rate" else "pct"),
    }


def yahoo_close_quote(symbol: str, label: str, kind: str) -> dict:
    timestamps, closes, meta = fetch_yahoo_chart(symbol, "5d", "1d")
    pairs = [(t, c) for t, c in zip(timestamps, closes) if c is not None]
    if len(pairs) < 2:
        raise RuntimeError(f"{symbol}: fewer than two closes returned")
    (prev_ts, prev), (last_ts, last) = pairs[-2], pairs[-1]
    prev = float(prev)
    last = float(last)
    if prev == 0:
        raise RuntimeError(f"{symbol}: previous close is zero")
    return {
        "symbol": symbol,
        "label": label,
        "kind": kind,
        "price": round(last, 4),
        "previous_close": round(prev, 4),
        "change": round(last - prev, 4),
        "change_pct": round((last - prev) / prev * 100.0, 4),
        "market_date": et_date_of(last_ts),
        # Daily-bar timestamp, not the close print time; the strip
        # labels close rows by date (see market-ticker.mjs).
        "quote_time": iso_z(datetime.fromtimestamp(last_ts, tz=timezone.utc)),
        "time_basis": "bar",
        "session": "close",
        "source": "Yahoo Finance v8 chart",
        "currency": meta.get("currency") or ("USD" if kind != "rate" else "pct"),
    }


def parse_nasdaq_chart_payload(payload: dict, symbol: str) -> tuple[float, float, str]:
    """(last sale, previous close, market date) from a Nasdaq chart
    response. Change is computed within Nasdaq's own basis: its
    previousClose differs from Yahoo's for some symbols (AAPL 355.36
    vs 355.63 on 2026-11-12), so the two bases must never mix."""
    data = payload.get("data") or {}
    if not isinstance(data, dict) or not data:
        status = payload.get("status") or {}
        raise RuntimeError(f"{symbol}: Nasdaq returned no data: {status}")
    try:
        clean = lambda v: float(str(v).replace("$", "").replace(",", "").strip())
        last = clean(data["lastSalePrice"])
        prev = clean(data["previousClose"])
        market_date = datetime.strptime(
            str(data["timeAsOf"]).strip(), "%b %d, %Y"
        ).date().isoformat()
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError(f"{symbol}: unparseable Nasdaq payload: {exc}") from exc
    if prev == 0:
        raise RuntimeError(f"{symbol}: Nasdaq previous close is zero")
    return last, prev, market_date


def nasdaq_quote(
    symbol: str, label: str, kind: str, mode: str, now_utc: datetime
) -> dict:
    """Fallback quote from the Nasdaq chart endpoint. quote_time is
    the fetch time: Nasdaq's timestamp is date-only, so stamping the
    fetch is the honest statement (observed at, not traded at)."""
    if symbol in NASDAQ_INDEX_FALLBACK:
        nasdaq_symbol, assetclass = NASDAQ_INDEX_FALLBACK[symbol], "index"
    elif symbol.startswith("^"):
        raise RuntimeError(f"{symbol}: no verified Nasdaq route for this index")
    else:
        nasdaq_symbol, assetclass = symbol, "stocks"
    url = (
        "https://api.nasdaq.com/api/quote/"
        f"{urllib.parse.quote(nasdaq_symbol, safe='')}"
        f"/chart?assetclass={assetclass}"
    )
    headers = {**UA, "Accept": "application/json"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, ValueError) as exc:
        raise RuntimeError(f"{symbol}: Nasdaq request failed: {exc}") from exc
    last, prev, market_date = parse_nasdaq_chart_payload(payload, symbol)
    return {
        "symbol": symbol,
        "label": label,
        "kind": kind,
        "price": round(last, 4),
        "previous_close": round(prev, 4),
        "change": round(last - prev, 4),
        "change_pct": round((last - prev) / prev * 100.0, 4),
        "market_date": market_date,
        "quote_time": iso_z(now_utc),
        "time_basis": "fetch",
        "session": "intraday" if mode == "intraday" else "close",
        "source": "Nasdaq quote API",
        "currency": "USD" if kind != "rate" else "pct",
    }


def parse_fred_observations(stdout: str, series: str) -> list[tuple[str, float]]:
    """(date, value) pairs from fred_observations.py JSON output,
    skipping FRED's "." missing-value marker."""
    try:
        data = json.loads(stdout)
    except ValueError as exc:
        raise RuntimeError(f"FRED {series}: unparseable helper output: {exc}") from exc
    rows = data.get(series) or []
    parsed = []
    for row in rows:
        try:
            value = float(row["value"])
        except (KeyError, TypeError, ValueError):
            continue
        parsed.append((str(row["date"]), value))
    if len(parsed) < 2:
        raise RuntimeError(f"FRED {series}: fewer than two observations")
    # The helper returns newest-first; sort chronologically so the
    # last pair is always (previous, latest).
    parsed.sort(key=lambda pair: pair[0])
    return parsed


def fred_quote(symbol: str, label: str, kind: str) -> dict:
    """Fallback yield from FRED daily observations. Stamped with the
    observation date at the 16:00 ET close and session "close": FRED
    lags a day or two, and the row must say so by its own fields."""
    series = FRED_SERIES[symbol]
    helper = Path(os.environ.get("FRED_HELPER", str(FRED_HELPER_DEFAULT)))
    if not helper.is_file():
        raise RuntimeError(f"FRED {series}: helper not found at {helper}")
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        FRED_HELPER_PYTHONPATH + (f":{existing}" if existing else "")
    )
    try:
        proc = subprocess.run(
            [sys.executable, str(helper), series, "--limit=2"],
            capture_output=True,
            text=True,
            timeout=60,
            env=env,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError(f"FRED {series}: helper failed: {exc}") from exc
    if proc.returncode != 0:
        raise RuntimeError(
            f"FRED {series}: helper exited {proc.returncode}: {proc.stderr[:200]}"
        )
    (_prev_date, prev), (last_date, last) = parse_fred_observations(
        proc.stdout, series
    )[-2:]
    if prev == 0:
        raise RuntimeError(f"FRED {series}: previous observation is zero")
    close_et = datetime.combine(
        date.fromisoformat(last_date), time(16, 0), tzinfo=ET
    )
    return {
        "symbol": symbol,
        "label": label,
        "kind": kind,
        "price": round(last, 4),
        "previous_close": round(prev, 4),
        "change": round(last - prev, 4),
        "change_pct": round((last - prev) / prev * 100.0, 4),
        "market_date": last_date,
        "quote_time": iso_z(close_et),
        "time_basis": "obs-date",
        "session": "close",
        "source": f"FRED {series}",
        "currency": "pct",
    }


def build_quote_with_fallback(
    symbol: str,
    label: str,
    kind: str,
    mode: str,
    today_et: str,
    now_utc: datetime,
) -> dict:
    """Yahoo first, then the verified fallback for this symbol's class.
    Raises Quarantined when every attempted source fails."""
    attempted: list[str] = ["Yahoo"]
    try:
        if mode == "intraday":
            return yahoo_intraday_quote(symbol, label, kind, today_et)
        return yahoo_close_quote(symbol, label, kind)
    except RuntimeError as exc:
        print(f"build_market_ticker: Yahoo failed for {symbol}: {exc}", file=sys.stderr)

    if symbol in NASDAQ_INDEX_FALLBACK or not symbol.startswith("^"):
        attempted.append("Nasdaq")
        try:
            return nasdaq_quote(symbol, label, kind, mode, now_utc)
        except RuntimeError as exc:
            print(
                f"build_market_ticker: Nasdaq failed for {symbol}: {exc}",
                file=sys.stderr,
            )
    if symbol in FRED_SERIES:
        attempted.append("FRED")
        try:
            return fred_quote(symbol, label, kind)
        except RuntimeError as exc:
            print(
                f"build_market_ticker: FRED failed for {symbol}: {exc}",
                file=sys.stderr,
            )
    raise Quarantined(symbol, f"no quote from {', '.join(attempted)}")


def session_has_bars_today(today_et: str) -> bool:
    """True when SPY 1m bars exist dated today (ET). A failed probe
    returns True: an unreachable Yahoo must not masquerade as a
    holiday; the per-symbol chain then decides, fail-closed."""
    try:
        timestamps, closes, _meta = fetch_yahoo_chart("SPY", "1d", "1m")
    except RuntimeError as exc:
        print(
            f"build_market_ticker: session probe failed ({exc}); proceeding",
            file=sys.stderr,
        )
        return True
    pairs = [(t, c) for t, c in zip(timestamps, closes) if c is not None]
    if not pairs:
        return False
    return et_date_of(pairs[-1][0]) == today_et


def canonical_feed(feed: dict) -> dict:
    """The comparison basis for skip-if-unchanged: data, not labels.
    generated_at changes on every run and market_state is a clock
    label; neither may force a rewrite."""
    return {
        key: feed.get(key)
        for key in (
            "quotes",
            "unavailable",
            "unavailable_symbols",
            "order",
            "as_of",
            "mode",
        )
    }


def feed_unchanged(out: Path, feed: dict) -> bool:
    if not out.is_file():
        return False
    try:
        existing = json.loads(out.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return False
    return canonical_feed(existing) == canonical_feed(feed)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--extra-symbols",
        default="",
        help="Comma-separated extra Yahoo symbols (best-effort).",
    )
    parser.add_argument(
        "--mode",
        choices=("auto", "intraday", "close"),
        default="auto",
        help="auto: decide from the America/New_York clock (default).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Write even when the feed is unchanged.",
    )
    args = parser.parse_args(argv)

    now_utc = datetime.now(timezone.utc)
    now_et = now_utc.astimezone(ET)
    state = market_state(now_et)
    today_et = now_et.date().isoformat()

    if args.mode == "auto":
        if state == "session":
            mode = "intraday"
        elif state == "close-window":
            mode = "close"
        else:
            print(
                f"build_market_ticker: quiet ({state} {now_et:%H:%M} ET); feed untouched"
            )
            return 0
    else:
        mode = args.mode

    if mode == "intraday" and not session_has_bars_today(today_et):
        print(
            "build_market_ticker: no SPY bars dated today; no session, "
            "keeping the last close feed"
        )
        return 0

    quotes: list[dict] = []
    unavailable: list[dict] = []
    order: list[str] = []
    requested: list[tuple[str, str, str]] = list(DEFAULT_SYMBOLS)
    for raw in (s.strip() for s in args.extra_symbols.split(",")):
        if not raw:
            continue
        symbol = raw.upper()
        if any(s == symbol for s, _label, _kind in requested):
            continue
        requested.append((symbol, symbol, "equity"))

    for symbol, label, kind in requested:
        order.append(symbol)
        try:
            quotes.append(
                build_quote_with_fallback(
                    symbol, label, kind, mode, today_et, now_utc
                )
            )
        except Quarantined as exc:
            print(f"build_market_ticker: quarantined: {exc}", file=sys.stderr)
            unavailable.append(
                {
                    "symbol": symbol,
                    "label": label,
                    "kind": kind,
                    "reason": exc.reason,
                }
            )
        except Exception as exc:  # Never let one symbol kill the feed.
            print(
                f"build_market_ticker: unexpected failure for {symbol}: "
                f"{type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
            unavailable.append(
                {
                    "symbol": symbol,
                    "label": label,
                    "kind": kind,
                    "reason": f"unexpected {type(exc).__name__}",
                }
            )

    if not quotes:
        print(
            "build_market_ticker: no quotes from any source; refusing to write",
            file=sys.stderr,
        )
        return 2

    as_of = max(q["market_date"] for q in quotes)
    sources: list[str] = []
    for q in quotes:
        if q["source"] not in sources:
            sources.append(q["source"])
    feed = {
        "schema_version": "market-ticker-1",
        "generated_at": iso_z(now_utc),
        "source": "; ".join(sources),
        "as_of": as_of,
        "mode": mode,
        "market_state": state,
        "quotes": quotes,
        "order": order,
        "unavailable": unavailable,
        "unavailable_symbols": [u["symbol"] for u in unavailable],
    }

    if not args.force and feed_unchanged(args.out, feed):
        print(
            f"build_market_ticker: unchanged ({len(quotes)} quotes, "
            f"as of {as_of}, mode {mode}); no write"
        )
        return 0

    tmp = args.out.with_suffix(args.out.suffix + ".tmp")
    tmp.write_text(json.dumps(feed, indent=2) + "\n", encoding="utf-8")
    tmp.replace(args.out)
    print(
        f"wrote {args.out}: {len(quotes)} quotes, "
        f"{len(unavailable)} unavailable, as of {as_of}, mode {mode}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
