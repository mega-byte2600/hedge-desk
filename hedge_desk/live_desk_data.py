"""Live market data for the desk console. No synthetic fixtures, ever.

This module fetches real market data from Schwab Market Data Production, with Yahoo failover, and assembles it
into per-desk payloads for the web console. It is fail-closed: when real data
cannot be obtained, the desk reports ``data_unavailable`` with an explicit
reason. Synthetic, fixture, reference, or invented data is never returned.

Data rule (user directive 2026-09-30, enforced 2026-10-03):
- Production surfaces show live timestamped data or the latest real batch.
- Missing data renders as ``data unavailable`` plus reason.
- Scenario/hypothetical controls must be labeled
  ``scenario -- hypothetical projection from real base data``.
"""

from datetime import datetime, timezone
import json
import urllib.request

# Yahoo is retained only as a real-data failover path.
YAHOO_CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=5d"
FRED_SERIES = "https://api.stlouisfed.org/fred/series/observations"

DATA_UNAVAILABLE = "data_unavailable"
STATUS_LIVE = "live"
STATUS_BATCH = "batch"

# Desk -> Yahoo symbols for the live snapshot.
DESK_SYMBOLS = {
    "overnight-premium-desk": ["SPY", "QQQ", "^VIX"],
    "earnings-event-desk": ["AAPL", "MSFT", "NVDA", "TSLA"],
    "arbitrage-observer": ["SPY", "QQQ", "DIA"],
    "dividend-opportunity-desk": ["SPY", "DIA"],
    "open-quant-ai-model-lab": ["SPY", "QQQ", "IWM", "DIA"],
    "event-futures-desk": ["USO", "GLD"],
    "bonds-rates-desk": ["TLT", "IEF"],
}

SYMBOL_NAMES = {
    "SPY": "S&P 500 ETF", "QQQ": "Nasdaq 100 ETF", "DIA": "Dow ETF",
    "IWM": "Russell 2000 ETF", "^VIX": "VIX", "AAPL": "Apple",
    "MSFT": "Microsoft", "NVDA": "Nvidia", "TSLA": "Tesla",
    "USO": "WTI Crude ETF", "GLD": "Gold ETF", "TLT": "20Y Treasury ETF",
    "IEF": "7-10Y Treasury ETF",
}


def _fetch_yahoo(symbol, timeout=8):
    """Fetch the last two daily closes for a symbol. Returns dict or None."""
    try:
        req = urllib.request.Request(
            YAHOO_CHART.format(symbol=symbol),
            headers={"User-Agent": "Mozilla/5.0 (compatible; hedge-desk/1.0)"},
        )
        payload = json.load(urllib.request.urlopen(req, timeout=timeout))
        result = (payload.get("chart") or {}).get("result") or []
        if not result:
            return None
        closes = [
            c for c in (result[0].get("indicators") or {}).get("quote", [{}])[0].get("close", [])
            if c is not None
        ]
        if len(closes) < 2:
            return None
        prev, last = closes[-2], closes[-1]
        change_pct = (last - prev) / prev * 100 if prev else 0.0
        return {
            "symbol": symbol,
            "name": SYMBOL_NAMES.get(symbol, symbol),
            "last": round(last, 2),
            "prev_close": round(prev, 2),
            "change_pct": round(change_pct, 2),
            "source": "Yahoo Finance",
        }
    except Exception:
        return None


def fetch_market_snapshot(symbols, timeout=8):
    """Fetch production quotes with Schwab primary and Yahoo per-symbol failover."""
    from hedge_desk.schwab_core_data import fetch_market_snapshot as schwab_primary
    return schwab_primary(symbols, timeout=timeout)


def build_desk_projects(fetcher=None):
    """Build per-desk project entries backed by real market data.

    Each entry carries ``data_status`` of ``live``, ``batch``, or
    ``data_unavailable``. No synthetic fixtures are ever produced.
    """
    if fetcher is None:
        fetcher = fetch_market_snapshot
    now = datetime.now(timezone.utc).isoformat()
    # Union of symbols across desks; fetch once.
    symbols = sorted({s for syms in DESK_SYMBOLS.values() for s in syms})
    quotes, unavailable = fetcher(symbols)
    unavailable_by_symbol = {u["symbol"]: u["reason"] for u in unavailable}

    projects = []
    for project_id, syms in DESK_SYMBOLS.items():
        live_data = {}
        missing = []
        for symbol in syms:
            if symbol in quotes:
                live_data[symbol] = quotes[symbol]
            else:
                missing.append({
                    "symbol": symbol,
                    "reason": unavailable_by_symbol.get(symbol, "no data"),
                })
        if live_data and not missing:
            status = STATUS_LIVE
            reason = ""
        elif live_data:
            status = STATUS_LIVE
            reason = "partial: " + ", ".join(m["symbol"] for m in missing) + " unavailable"
        else:
            status = DATA_UNAVAILABLE
            reason = "no live quotes available for " + ", ".join(syms)
        projects.append({
            "project_id": project_id,
            "evaluated_at": now,
            "data_status": status,
            "data_as_of": now,
            "data_source": ", ".join(sorted({q.get("source", "unknown") for q in live_data.values()})) if live_data else "data unavailable",
            "reason": reason,
            "live_data": live_data,
            "unavailable": missing,
        })
    return projects


def build_live_console_report(code_commit, fetcher=None):
    """Build the console report payload from real data only.

    Raises RuntimeError (fail-closed) if no live data could be obtained at
    all; the route layer maps this to a 503 with an explicit reason.
    """
    now = datetime.now(timezone.utc)
    projects = build_desk_projects(fetcher=fetcher)
    live_count = sum(1 for p in projects if p["data_status"] == STATUS_LIVE)
    if live_count == 0:
        raise RuntimeError("data unavailable: no live market quotes could be fetched")
    return {
        "report_type": "live_market_console",
        "runner_version": "2.0.0",
        "code_commit": code_commit,
        "generated_at": now.isoformat(),
        "environment": "paper",
        "complete": True,
        "live_orders_enabled": False,
        "real_money_pnl": "0",
        "real_trades_executed": 0,
        "summary": {
            "desks_reporting": live_count,
            "desks_total": len(projects),
        },
        "limitations": [
            "Primary market data: Schwab Trader API / Market Data; Yahoo Finance is failover only.",
            "Paper research context only; no trade authorization.",
            "Data may be delayed; verify before any decision.",
        ],
        "projects": projects,
        "scenarios": build_real_scenarios(fetcher=fetcher),
        "synthetic_data": False,
    }


# Standard hypothetical moves applied to the real base snapshot.
# Each scenario is labeled as a hypothetical projection from real base data.
SCENARIO_MOVES = [
    ("-10%", -0.10, "severe drawdown"),
    ("-5%", -0.05, "sharp selloff"),
    ("-3%", -0.03, "pullback"),
    ("+3%", 0.03, "rally"),
    ("+5%", 0.05, "strong rally"),
]


def build_real_scenarios(fetcher=None):
    """Build scenario lab entries as hypothetical projections from real base data.

    Each scenario takes the live quote as its base and applies a hypothetical
    move. Labeled per the data rule:
    ``scenario -- hypothetical projection from real base data``.
    """
    if fetcher is None:
        fetcher = fetch_market_snapshot
    now = datetime.now(timezone.utc).isoformat()
    symbols = ["SPY", "QQQ", "IWM"]
    quotes, _ = fetcher(symbols)
    scenarios = []
    for symbol in symbols:
        quote = quotes.get(symbol)
        if not quote:
            continue
        base = quote["last"]
        for label, move, description in SCENARIO_MOVES:
            projected = round(base * (1 + move), 2)
            scenarios.append({
                "scenario_id": f"{symbol}-move-{label}".replace("%", "pct").replace("+", "up").replace("-", "down"),
                "group": "hypothetical-move",
                "base_symbol": symbol,
                "base_price": base,
                "base_as_of": now,
                "data_source": quote["source"],
                "hypothetical_move": label,
                "description": description,
                "projected_price": projected,
                "label": "scenario -- hypothetical projection from real base data",
                "disposition": "HYPOTHETICAL",
                "reason_codes": [
                    f"Base is the live {symbol} quote ({base}) as of {now[:10]}.",
                    "No position, P&L, or trade implication is computed.",
                ],
            })
    return scenarios
