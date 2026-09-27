"""Finnhub market-data adapter — free tier, official API.

Provides real-time quotes via the Finnhub API using the securely-stored
``custom.finnhub`` credential. Free tier: 60 calls/minute, no card.

Use for: quote fallback when Yahoo fails, real-time price checks.

Source: https://finnhub.io (official API)
Auth: stored credential via skill CLI (surrogate exchange).
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Dict, List, Optional


def _skill_cli_path() -> Optional[Path]:
    p = Path.home() / "workspace" / "skills" / "finnhub" / "bin" / "finnhub_quote.py"
    return p if p.is_file() else None


@dataclass(frozen=True)
class FinnhubQuote:
    symbol: str
    current: Decimal
    high: Decimal
    low: Decimal
    open: Decimal
    prev_close: Decimal
    timestamp: int

    def change(self) -> Decimal:
        return self.current - self.prev_close

    def change_pct(self) -> Decimal:
        if self.prev_close == 0:
            return Decimal("0")
        return 100 * self.change() / self.prev_close


def _decimal(value: object) -> Optional[Decimal]:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None


def fetch_quotes(symbols: List[str]) -> Dict[str, FinnhubQuote]:
    """Fetch real-time quotes for symbols via the Finnhub skill CLI.

    Returns {symbol: FinnhubQuote}. Symbols with no quote are omitted.
    Raises ValueError if the CLI is missing or fails.
    """
    cli = _skill_cli_path()
    if cli is None:
        raise ValueError("finnhub skill CLI not installed")
    try:
        proc = subprocess.run(
            ["python3", str(cli)] + symbols,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError) as e:
        raise ValueError(f"finnhub CLI failed: {e}") from e
    if proc.returncode != 0:
        raise ValueError(f"finnhub CLI exit {proc.returncode}")
    try:
        payload = json.loads(proc.stdout or "{}")
    except ValueError as e:
        raise ValueError(f"finnhub CLI bad JSON: {e}") from e
    out: Dict[str, FinnhubQuote] = {}
    for sym in symbols:
        q = payload.get(sym.upper(), {})
        if "error" in q:
            continue
        current = _decimal(q.get("c"))
        if current is None or current == 0:
            continue
        out[sym.upper()] = FinnhubQuote(
            symbol=sym.upper(),
            current=current,
            high=_decimal(q.get("h")) or current,
            low=_decimal(q.get("l")) or current,
            open=_decimal(q.get("o")) or current,
            prev_close=_decimal(q.get("pc")) or current,
            timestamp=int(q.get("t") or 0),
        )
    return out


def quote_summary(symbols: List[str]) -> Dict[str, object]:
    """Multi-symbol quote summary. Fail-closed per symbol."""
    try:
        quotes = fetch_quotes(symbols)
    except ValueError as e:
        return {
            "mode": "BLOCKED",
            "reason": str(e),
            "data_source": "finnhub-api",
        }
    rows = []
    for sym in symbols:
        q = quotes.get(sym.upper())
        if q is None:
            rows.append({"symbol": sym.upper(), "mode": "BLOCKED"})
        else:
            rows.append(
                {
                    "symbol": q.symbol,
                    "mode": "REAL_FINNHUB_QUOTE",
                    "current": str(q.current),
                    "change": str(q.change()),
                    "change_pct": str(round(q.change_pct(), 2)),
                    "high": str(q.high),
                    "low": str(q.low),
                    "prev_close": str(q.prev_close),
                }
            )
    return {
        "schema_version": "hedge-desk-finnhub-1.0.0",
        "mode": "REAL_FINNHUB_QUOTE",
        "quotes": rows,
        "data_source": "finnhub-api",
        "note": "Real-time quotes via Finnhub. Free tier 60/min.",
    }


__all__ = ["FinnhubQuote", "fetch_quotes", "quote_summary"]
