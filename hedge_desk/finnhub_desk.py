"""Finnhub quote adapter with a deploy-safe HTTP path and local CLI fallback.

When ``FINNHUB_API_KEY`` is present, quotes come directly from Finnhub's official
REST API using the authentication header so the secret never appears in a URL.
Local development may fall back to the existing skill CLI. The adapter remains
read-only and never authorizes an order.
"""

from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple


RequestTransport = Callable[[urllib.request.Request], Tuple[int, bytes]]
FINNHUB_QUOTE_URL = "https://finnhub.io/api/v1/quote"


def _skill_cli_path() -> Optional[Path]:
    p = Path.home() / "workspace" / "skills" / "finnhub" / "bin" / "finnhub_quote.py"
    return p if p.is_file() else None


def _default_transport(request: urllib.request.Request) -> Tuple[int, bytes]:
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:
        return 0, str(exc).encode("utf-8")


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


def _quote_from_payload(symbol: str, q: object) -> Optional[FinnhubQuote]:
    if not isinstance(q, dict) or "error" in q:
        return None
    current = _decimal(q.get("c"))
    if current is None or current == 0:
        return None
    return FinnhubQuote(
        symbol=symbol.upper(),
        current=current,
        high=_decimal(q.get("h")) or current,
        low=_decimal(q.get("l")) or current,
        open=_decimal(q.get("o")) or current,
        prev_close=_decimal(q.get("pc")) or current,
        timestamp=int(q.get("t") or 0),
    )


def _fetch_http_quotes(
    symbols: List[str],
    api_key: str,
    transport: RequestTransport,
) -> Dict[str, FinnhubQuote]:
    out: Dict[str, FinnhubQuote] = {}
    for symbol in symbols:
        normalized = symbol.strip().upper()
        if not normalized or len(normalized) > 16 or not all(
            ch.isalnum() or ch in ".-" for ch in normalized
        ):
            continue
        query = urllib.parse.urlencode({"symbol": normalized})
        request = urllib.request.Request(
            f"{FINNHUB_QUOTE_URL}?{query}",
            headers={
                "Accept": "application/json",
                "User-Agent": "hedge-desk/1.0 research",
                "X-Finnhub-Token": api_key,
            },
        )
        try:
            status, raw = transport(request)
        except Exception as exc:
            raise ValueError(f"finnhub transport failed for {normalized}: {exc}") from exc
        if status == 429:
            raise ValueError("finnhub rate limit exceeded")
        if status != 200 or not raw:
            raise ValueError(f"finnhub fetch failed for {normalized} (status {status})")
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            raise ValueError(f"finnhub malformed JSON for {normalized}") from exc
        quote = _quote_from_payload(normalized, payload)
        if quote is not None:
            out[normalized] = quote
    return out


def _fetch_cli_quotes(symbols: List[str]) -> Dict[str, FinnhubQuote]:
    cli = _skill_cli_path()
    if cli is None:
        raise ValueError("FINNHUB_API_KEY not configured and finnhub skill CLI not installed")
    try:
        proc = subprocess.run(
            ["python3", str(cli)] + symbols,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ValueError(f"finnhub CLI failed: {exc}") from exc
    if proc.returncode != 0:
        raise ValueError(f"finnhub CLI exit {proc.returncode}")
    try:
        payload = json.loads(proc.stdout or "{}")
    except ValueError as exc:
        raise ValueError(f"finnhub CLI bad JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("finnhub CLI payload is not an object")
    out: Dict[str, FinnhubQuote] = {}
    for sym in symbols:
        normalized = sym.upper()
        quote = _quote_from_payload(normalized, payload.get(normalized, {}))
        if quote is not None:
            out[normalized] = quote
    return out


def fetch_quotes(
    symbols: List[str],
    *,
    transport: RequestTransport = _default_transport,
) -> Dict[str, FinnhubQuote]:
    """Fetch quotes through env-key HTTP in deployment, CLI fallback locally."""

    api_key = os.environ.get("FINNHUB_API_KEY", "").strip()
    if api_key:
        return _fetch_http_quotes(symbols, api_key, transport)
    return _fetch_cli_quotes(symbols)


def quote_summary(symbols: List[str]) -> Dict[str, object]:
    """Multi-symbol quote summary. Fail closed per symbol."""
    try:
        quotes = fetch_quotes(symbols)
    except ValueError as exc:
        return {
            "mode": "BLOCKED",
            "reason": str(exc),
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
        "note": "Quotes via Finnhub; availability and timeliness depend on the configured plan.",
    }


__all__ = ["FINNHUB_QUOTE_URL", "FinnhubQuote", "fetch_quotes", "quote_summary"]
