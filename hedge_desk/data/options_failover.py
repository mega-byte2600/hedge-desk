"""Options-chain failover: Yahoo -> Nasdaq -> CBOE -> data unavailable.

Standing source order is Yahoo first, Nasdaq second, free fallbacks after.
The previous failure mode was STALLING on Yahoo 401s (10-01 premarket,
10-03 daily lost the whole Premium IV desk). This module never stalls: each
source gets its bounded attempts, every attempt is logged, and when every
source is down the result is a literal data-unavailable with reasons —
never synthetic data.

CBOE parsing is deliberately NOT duplicated here: raw CBOE bytes feed the
repo's tested ``hedge_desk.cboe_chain.build_snapshot_from_cboe``. Yahoo v7
payloads are parsed by the conservative parser below (the repo has no Yahoo
options parser today — see README).
"""

from __future__ import annotations

import json
import time
import urllib.parse
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from .yahoo_transport import Transport, YahooBlocked, YahooSession

YAHOO_OPTIONS_URL = "https://query2.finance.yahoo.com/v7/finance/options/{symbol}"
NASDAQ_OPTIONS_URL = "https://api.nasdaq.com/api/quote/{symbol}/option-chain?assetclass=stocks"
CBOE_OPTIONS_URL = "https://cdn.cboe.com/api/global/delayed_quotes/options/{symbol}.json"


@dataclass
class ChainResult:
    """Outcome of the failover chain. ok=False means data unavailable —
    check .reason, never invent a payload."""

    ok: bool
    source_id: str
    payload: bytes
    reason: str
    attempts: List[Dict[str, str]] = field(default_factory=list)

    @property
    def data_unavailable(self) -> str:
        return "" if self.ok else f"data unavailable: {self.reason}"


def _attempt(source: str, ok: bool, detail: str = "") -> Dict[str, str]:
    return {"source": source, "ok": "yes" if ok else "no", "detail": detail}


def parse_yahoo_options(body: bytes) -> List[Dict[str, Any]]:
    """Conservative parser for Yahoo v7 optionChain payloads.

    Returns one dict per contract: expiry, type, strike, bid, ask, volume,
    openInterest, impliedVolatility. Fail-closed: any shape deviation raises
    ValueError — the chain then moves to the next source.
    """
    try:
        doc = json.loads(body.decode("utf-8"))
        results = doc["optionChain"]["result"]
        if not results:
            raise ValueError("empty result list")
        node = results[0]
        contracts: List[Dict[str, Any]] = []
        for chain in node.get("options", []):
            expiry = chain.get("expirationDate")
            for side, otype in (("calls", "call"), ("puts", "put")):
                for c in chain.get(side, []) or []:
                    try:
                        contracts.append({
                            "expiry": int(expiry),
                            "type": otype,
                            "strike": float(c["strike"]),
                            "bid": float(c.get("bid") or 0.0),
                            "ask": float(c.get("ask") or 0.0),
                            "volume": int(c.get("volume") or 0),
                            "openInterest": int(c.get("openInterest") or 0),
                            "impliedVolatility": float(c.get("impliedVolatility") or 0.0),
                        })
                    except (KeyError, TypeError, ValueError) as exc:
                        raise ValueError(f"contract shape unexpected: {exc}") from exc
        if not contracts:
            raise ValueError("no contracts parsed")
        return contracts
    except (KeyError, IndexError, TypeError, ValueError, UnicodeDecodeError) as exc:
        raise ValueError(f"yahoo options payload malformed: {exc}") from exc


def fetch_yahoo_options(session: YahooSession, symbol: str) -> Tuple[bytes, str]:
    """Yahoo v7 options chain via the hardened session. Returns (raw, note)."""
    raw = session.get(YAHOO_OPTIONS_URL.format(symbol=symbol.upper()))
    contracts = parse_yahoo_options(raw)  # fail-closed on shape
    return raw, f"{len(contracts)} contracts"


def fetch_nasdaq_options(transport: Transport, symbol: str) -> Tuple[bytes, str]:
    """Nasdaq option-chain, best-effort. Verified 2026-10-04: the endpoint
    returns rCode 400 'Symbol not exists' from datacenter IPs — treated as a
    normal source failure, not an error. Strict shape validation."""
    url = NASDAQ_OPTIONS_URL.format(symbol=symbol.upper())
    req_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36",
        "Accept": "application/json",
    }
    status, body = transport(url, req_headers)
    if status != 200:
        raise YahooBlocked(f"nasdaq HTTP {status}")
    try:
        doc = json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise YahooBlocked(f"nasdaq payload not JSON: {exc}") from exc
    rcode = (doc.get("status") or {}).get("rCode")
    if rcode != 200:
        msg = ((doc.get("status") or {}).get("bCodeMessage") or [{}])[0].get(
            "errorMessage", "unknown")
        raise YahooBlocked(f"nasdaq rCode {rcode}: {msg}")
    rows = ((doc.get("data") or {}).get("table") or {}).get("rows") or []
    if not rows:
        raise YahooBlocked("nasdaq returned no rows")
    return body, f"{len(rows)} rows"


def fetch_cboe_options(transport: Transport, symbol: str) -> Tuple[bytes, str]:
    """CBOE delayed-quotes payload (raw bytes). Parse with the repo's tested
    hedge_desk.cboe_chain.build_snapshot_from_cboe — do not reimplement it."""
    url = CBOE_OPTIONS_URL.format(symbol=symbol.upper())
    status, body = transport(url, {"User-Agent": "hedge-desk/1.0"})
    if status != 200:
        raise YahooBlocked(f"cboe HTTP {status}")
    try:
        doc = json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise YahooBlocked(f"cboe payload not JSON: {exc}") from exc
    if not isinstance(doc.get("data"), dict) or not doc["data"].get("options"):
        raise YahooBlocked("cboe payload has no options")
    return body, f"{len(doc['data']['options'])} contracts (delayed)"


def fetch_options_chain(
    symbol: str,
    session: Optional[YahooSession] = None,
    transport: Optional[Transport] = None,
    sleeper: Callable[[float], None] = time.sleep,
) -> ChainResult:
    """Run the Yahoo -> Nasdaq -> CBOE chain for one symbol's options chain.

    Never raises on source failure: returns ChainResult(ok=False) with the
    per-source reasons joined into a literal data-unavailable string.
    """
    attempts: List[Dict[str, str]] = []
    if session is not None:
        sess = session
    elif transport is not None:
        sess = YahooSession(transport=transport, sleeper=sleeper)
    else:
        sess = YahooSession(sleeper=sleeper)  # real network via default factory
    # NOTE: passing the fixture transport keeps the Yahoo leg on fixtures too.
    plain = sess.transport

    # 1. Yahoo (hardened: crumb, refresh-once, backoff)
    try:
        raw, note = fetch_yahoo_options(sess, symbol)
        attempts.append(_attempt("yahoo", True, note))
        attempts.extend(
            {"source": "yahoo", "ok": "info", "detail": f"{e['event']}: {e['detail']}"}
            for e in sess.attempts_log
        )
        return ChainResult(True, "yahoo", raw, "", attempts)
    except (YahooBlocked, ValueError) as exc:
        attempts.append(_attempt("yahoo", False, str(exc)[:160]))

    # 2. Nasdaq (best-effort, strict shape check)
    try:
        raw, note = fetch_nasdaq_options(plain, symbol)
        attempts.append(_attempt("nasdaq", True, note))
        return ChainResult(True, "nasdaq", raw, "", attempts)
    except (YahooBlocked, ValueError) as exc:
        attempts.append(_attempt("nasdaq", False, str(exc)[:160]))

    # 3. CBOE delayed quotes (repo's own benchmark source)
    try:
        raw, note = fetch_cboe_options(plain, symbol)
        attempts.append(_attempt("cboe", True, note))
        return ChainResult(True, "cboe", raw, "", attempts)
    except (YahooBlocked, ValueError) as exc:
        attempts.append(_attempt("cboe", False, str(exc)[:160]))

    reason = "; ".join(
        f"{a['source']} failed ({a['detail']})" for a in attempts if a["ok"] == "no"
    )
    return ChainResult(False, "none", b"", reason or "all sources failed", attempts)
