"""Read-only Schwab market-data REST adapter.

The adapter uses Schwab's production Market Data API over HTTPS. It does not
stream, retry throttled requests, cache licensed payloads, or place orders.
Callers must use the broker-link token lifecycle before passing a bearer token.
"""

from __future__ import annotations

import json
import hashlib
import os
import threading
import time
from collections import deque
import urllib.error
import urllib.parse
import urllib.request
from collections import OrderedDict
from typing import Callable, Optional

SCHWAB_MARKET_DATA_BASE = "https://api.schwabapi.com/marketdata/v1"
Transport = Callable[[str, str, dict], tuple[int, bytes]]

# Schwab does not expose a public contractual market-data RPM limit page.
# Emporion therefore paces below the widely observed ~120 req/min ceiling.
_DEFAULT_RPM = 90
_MAX_RPM = 120
_QUOTE_BATCH_SIZE = 50
_RATE_LOCK = threading.Lock()
_RATE_WINDOW = deque()


def _configured_rpm() -> int:
    try:
        rpm = int(os.getenv("SCHWAB_MARKET_DATA_RPM", str(_DEFAULT_RPM)))
    except (TypeError, ValueError):
        return _DEFAULT_RPM
    return max(1, min(rpm, _MAX_RPM))


def _pace() -> None:
    rpm = _configured_rpm()
    while True:
        with _RATE_LOCK:
            now = time.monotonic()
            while _RATE_WINDOW and now - _RATE_WINDOW[0] >= 60.0:
                _RATE_WINDOW.popleft()
            if len(_RATE_WINDOW) < rpm:
                _RATE_WINDOW.append(now)
                return
            wait = max(0.01, 60.0 - (now - _RATE_WINDOW[0]))
        time.sleep(wait)


def _default_transport(method: str, url: str, headers: dict) -> tuple[int, bytes]:
    request = urllib.request.Request(url, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


class SchwabMarketDataBroker:
    """Read-only quotes, option chains, expiration chains, history, and hours."""

    name = "schwab_market_data"

    def __init__(
        self,
        transport: Optional[Transport] = None,
        base_url: str = SCHWAB_MARKET_DATA_BASE,
        quote_cache_seconds: float = 1.0,
    ) -> None:
        parsed = urllib.parse.urlparse(base_url)
        if parsed.scheme != "https" or parsed.hostname != "api.schwabapi.com":
            raise ValueError("Schwab Market Data requires the official HTTPS host")
        if quote_cache_seconds < 0 or quote_cache_seconds > 5:
            raise ValueError("quote cache must be between zero and five seconds")
        self._transport = transport or _default_transport
        if base_url.rstrip("/") != SCHWAB_MARKET_DATA_BASE:
            raise ValueError("Schwab Market Data requires the official API base")
        self.base_url = SCHWAB_MARKET_DATA_BASE
        self.quote_cache_seconds = quote_cache_seconds
        self._quote_cache: OrderedDict[tuple, tuple[float, dict]] = OrderedDict()
        self._quote_lock = threading.Lock()

    def _get(self, path: str, token: str, params: Optional[dict] = None) -> dict:
        if not token:
            return {"status": "error", "error": "missing_token", "read_only": True}
        query = urllib.parse.urlencode(params or {}, doseq=True)
        url = self.base_url + path + ("?" + query if query else "")
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        _pace()
        try:
            status, raw = self._transport("GET", url, headers)
        except Exception:
            return {"status": "error", "error": "transport_failure", "read_only": True}
        if status == 429:
            return {"status": "error", "error": "throttled", "http_status": 429, "read_only": True}
        if status >= 400:
            return {"status": "error", "http_status": status, "read_only": True}
        try:
            data = json.loads(raw or b"{}")
        except (TypeError, ValueError, UnicodeDecodeError):
            return {"status": "error", "error": "bad_json", "read_only": True}
        if not isinstance(data, (dict, list)):
            return {"status": "error", "error": "unexpected_response_schema", "read_only": True}
        return {"status": "ok", "read_only": True, "data": data}

    def quotes(self, token: str, symbols: list[str], *, indicative: bool = False) -> dict:
        if not symbols or any(not isinstance(s, str) or not s.strip() for s in symbols):
            return {"status": "error", "error": "invalid_symbols", "read_only": True}
        normalized = tuple(sorted({s.strip().upper() for s in symbols}))
        key = (hashlib.sha256(token.encode()).digest(), normalized, indicative)
        now = time.monotonic()
        with self._quote_lock:
            cached = self._quote_cache.get(key)
            if cached and cached[0] > now:
                self._quote_cache.move_to_end(key)
                return cached[1]
            if cached:
                del self._quote_cache[key]
        merged = {}
        for start in range(0, len(normalized), _QUOTE_BATCH_SIZE):
            batch = normalized[start:start + _QUOTE_BATCH_SIZE]
            result = self._get(
                "/quotes", token,
                {"symbols": ",".join(batch), "indicative": str(indicative).lower()},
            )
            if result.get("status") != "ok":
                return result
            payload = result.get("data")
            if not isinstance(payload, dict):
                return {"status": "error", "error": "unexpected_response_schema", "read_only": True}
            merged.update(payload)

        result = {"status": "ok", "read_only": True, "data": merged}
        if self.quote_cache_seconds:
            with self._quote_lock:
                self._quote_cache[key] = (now + self.quote_cache_seconds, result)
                self._quote_cache.move_to_end(key)
                while len(self._quote_cache) > 512:
                    self._quote_cache.popitem(last=False)
        return result

    def option_chain(self, token: str, symbol: str, **filters) -> dict:
        if not isinstance(symbol, str) or not symbol.strip():
            return {"status": "error", "error": "invalid_symbol", "read_only": True}
        allowed = {
            "contractType", "strikeCount", "includeUnderlyingQuote", "strategy",
            "interval", "strike", "range", "fromDate", "toDate", "volatility",
            "underlyingPrice", "interestRate", "daysToExpiration", "expMonth",
        }
        if set(filters) - allowed:
            return {"status": "error", "error": "unsupported_chain_filter", "read_only": True}
        return self._get("/chains", token, {"symbol": symbol.strip(), **filters})

    def expiration_chain(self, token: str, symbol: str) -> dict:
        if not isinstance(symbol, str) or not symbol.strip():
            return {"status": "error", "error": "invalid_symbol", "read_only": True}
        return self._get("/expirationchain", token, {"symbol": symbol.strip()})

    def price_history(self, token: str, symbol: str, **params) -> dict:
        allowed = {
            "periodType", "period", "frequencyType", "frequency", "startDate",
            "endDate", "needExtendedHoursData", "needPreviousClose",
        }
        if not isinstance(symbol, str) or not symbol.strip() or set(params) - allowed:
            return {"status": "error", "error": "invalid_history_request", "read_only": True}
        return self._get(f"/pricehistory", token, {"symbol": symbol.strip(), **params})

    def movers(self, token: str, symbol_id: str, **params) -> dict:
        if not isinstance(symbol_id, str) or not symbol_id.strip():
            return {"status": "error", "error": "invalid_symbol", "read_only": True}
        allowed = {"sort", "frequency"}
        if set(params) - allowed:
            return {"status": "error", "error": "invalid_movers_request", "read_only": True}
        return self._get(f"/movers/{urllib.parse.quote(symbol_id.strip(), safe='')}", token, params)

    def instruments(self, token: str, symbols: str, projection: str) -> dict:
        if not isinstance(symbols, str) or not symbols.strip():
            return {"status": "error", "error": "invalid_symbols", "read_only": True}
        if not isinstance(projection, str) or not projection.strip():
            return {"status": "error", "error": "invalid_projection", "read_only": True}
        return self._get("/instruments", token, {"symbol": symbols.strip(), "projection": projection.strip()})

    def instrument_by_cusip(self, token: str, cusip_id: str) -> dict:
        if not isinstance(cusip_id, str) or not cusip_id.strip():
            return {"status": "error", "error": "invalid_cusip", "read_only": True}
        return self._get(f"/instruments/{urllib.parse.quote(cusip_id.strip(), safe='')}", token)

    def market_hours_all(self, token: str, markets: str = "", *, date: str = "") -> dict:
        params = {}
        if markets:
            params["markets"] = markets
        if date:
            if len(date) != 10 or date[4] != "-" or date[7] != "-":
                return {"status": "error", "error": "invalid_date", "read_only": True}
            params["date"] = date
        return self._get("/markets", token, params or None)

    def market_hours(self, token: str, market_id: str, *, date: str = "") -> dict:
        if not isinstance(market_id, str) or not market_id.strip():
            return {"status": "error", "error": "invalid_market", "read_only": True}
        if date and (len(date) != 10 or date[4] != "-" or date[7] != "-"):
            return {"status": "error", "error": "invalid_date", "read_only": True}
        params = {"date": date} if date else None
        paths = {"equity": "/markets/equity", "option": "/markets/option", "bond": "/markets/bond", "future": "/markets/future", "forex": "/markets/forex"}
        path = paths.get(market_id.strip().lower())
        if path is None:
            return {"status": "error", "error": "invalid_market", "read_only": True}
        return self._get(path, token, params)


__all__ = ["SchwabMarketDataBroker", "SCHWAB_MARKET_DATA_BASE"]
