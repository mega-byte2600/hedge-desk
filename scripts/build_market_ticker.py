#!/usr/bin/env python3
"""Build the market-ticker feed: web/market-ticker.json.

Pulls closing quotes from the Yahoo Finance v8 chart endpoint (browser
User-Agent only; no cookie/crumb needed for v8) for the fixed watchlist,
four headline indices, and three Treasury yields, and writes one
timestamped JSON artifact the static site reads. No credentials, no paid
API, standard library only.

Fail-closed: every default symbol must return two usable closes or the
run exits non-zero and writes nothing, leaving the previous feed in
place. Extra symbols passed with --extra-symbols are best-effort: a
failed extra is recorded under "unavailable_symbols" instead of failing
the run, so one bad user-added symbol cannot block the feed.

The browser never calls Yahoo directly (CORS); it reads only this
committed artifact, and shows "data unavailable" when the artifact is
missing, malformed, or stale. See web/market-ticker.mjs for the
staleness rule.

Usage:
    python3 scripts/build_market_ticker.py
    python3 scripts/build_market_ticker.py --extra-symbols AMD,AVGO
    python3 scripts/build_market_ticker.py --out /tmp/market-ticker.json
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "web" / "market-ticker.json"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
TIMEOUT = 30

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
    ("^GSPC", "S&P 500 index", "index"),
    ("^IXIC", "Nasdaq Composite index", "index"),
    ("^DJI", "Dow Jones Industrial Average", "index"),
    ("^RUT", "Russell 2000 index", "index"),
    ("^TNX", "10-year Treasury yield", "rate"),
    ("^FVX", "5-year Treasury yield", "rate"),
    ("^IRX", "13-week Treasury bill yield", "rate"),
)


def fetch_closes(symbol: str) -> tuple[list[float], list[int], dict]:
    """Return (closes, timestamps, meta) for the last 5 trading days."""
    url = (
        "https://query2.finance.yahoo.com/v8/finance/chart/"
        f"{urllib.parse.quote(symbol, safe='')}"
        "?range=5d&interval=1d&includePrePost=false"
    )
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"{symbol}: request failed: {exc}") from exc
    result = (payload.get("chart") or {}).get("result") or []
    if not result:
        err = (payload.get("chart") or {}).get("error") or {}
        raise RuntimeError(f"{symbol}: no chart result: {err.get('description', 'unknown')}")
    meta = result[0].get("meta") or {}
    quote = ((result[0].get("indicators") or {}).get("quote") or [{}])[0]
    closes = quote.get("close") or []
    timestamps = result[0].get("timestamp") or []
    if len(closes) != len(timestamps):
        raise RuntimeError(f"{symbol}: close/timestamp length mismatch")
    return closes, timestamps, meta


def build_quote(symbol: str, label: str, kind: str) -> dict:
    closes, timestamps, meta = fetch_closes(symbol)
    pairs = [(t, c) for t, c in zip(timestamps, closes) if c is not None]
    if len(pairs) < 2:
        raise RuntimeError(f"{symbol}: fewer than two closes returned")
    (prev_ts, prev), (last_ts, last) = pairs[-2], pairs[-1]
    if prev == 0:
        raise RuntimeError(f"{symbol}: previous close is zero")
    tz_name = meta.get("exchangeTimezoneName") or "America/New_York"
    try:
        tz = ZoneInfo(tz_name)
    except Exception:
        tz = timezone.utc
    market_date = datetime.fromtimestamp(last_ts, tz=tz).date().isoformat()
    return {
        "symbol": symbol,
        "label": label,
        "kind": kind,
        "price": round(float(last), 4),
        "previous_close": round(float(prev), 4),
        "change": round(float(last) - float(prev), 4),
        "change_pct": round((float(last) - float(prev)) / float(prev) * 100.0, 4),
        "market_date": market_date,
        "currency": meta.get("currency") or ("USD" if kind != "rate" else "pct"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--extra-symbols",
        default="",
        help="Comma-separated extra Yahoo symbols (best-effort).",
    )
    args = parser.parse_args(argv)

    quotes: list[dict] = []
    for symbol, label, kind in DEFAULT_SYMBOLS:
        try:
            quotes.append(build_quote(symbol, label, kind))
        except RuntimeError as exc:
            print(f"build_market_ticker: {exc}", file=sys.stderr)
            print("build_market_ticker: refusing to write a partial feed", file=sys.stderr)
            return 2

    unavailable: list[str] = []
    for raw in (s.strip() for s in args.extra_symbols.split(",")):
        if not raw:
            continue
        symbol = raw.upper()
        if any(q["symbol"] == symbol for q in quotes):
            continue
        try:
            quotes.append(build_quote(symbol, symbol, "equity"))
        except RuntimeError as exc:
            print(f"build_market_ticker: extra symbol skipped: {exc}", file=sys.stderr)
            unavailable.append(symbol)

    as_of = max(q["market_date"] for q in quotes)
    feed = {
        "schema_version": "market-ticker-1",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": "Yahoo Finance v8 chart",
        "as_of": as_of,
        "quotes": quotes,
        "unavailable_symbols": unavailable,
    }
    tmp = args.out.with_suffix(args.out.suffix + ".tmp")
    tmp.write_text(json.dumps(feed, indent=2) + "\n", encoding="utf-8")
    tmp.replace(args.out)
    print(f"wrote {args.out}: {len(quotes)} quotes, as of {as_of}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
