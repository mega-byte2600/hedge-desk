"""Weekly options-seed selection for the Emporion 30-day decision workbench.

Phase 1 data foundation: from a REAL Cboe delayed SPY chain, select the single
~30-DTE cash-secured-put-style contract the workbench seeds from, and expose it
as derived analytics (never the raw chain payload — the repo is public open
source and Cboe delayed-quote redistribution is reserved).

Selection policy (documented, tested, no discretion):
  * expiry: days-to-expiration in (7, 30] — the workbench models contracts of no
    more than 30 days, and stays clear of the 7-day pre-expiry exit window the
    premium desk uses. Closest DTE to 30 wins.
  * contract: out-of-the-money PUT (strike < underlying mid), executable
    bid/ask (bid>0, ask>0, ask>=bid, sizes>0), exchange delta closest to -0.30
    (the desk's standard premium-selling target delta — a policy input, not a
    recommendation). Tie-break: higher open interest, then lower ask.

Unavailable-field policy (verified against the live payload 2026-09-30):
Cboe emits exactly 0.0 for iv/greeks it did not compute. For a ~30-DTE OTM put
the true values are never exactly 0.0, so 0.0 (or missing) is surfaced as null
with reason "unavailable_in_source" — never as a fabricated zero.

Money is Decimal, serialised as strings. No probability, no Risk of Ruin, no
trade authorisation. Paper only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple

from hedge_desk import cboe_chain
from hedge_desk.options import OptionType

SEED_SCHEMA_VERSION = "hedge-desk-options-seed-1.0.0"
TARGET_DTE = 30
MIN_DTE = 7  # must clear the desk's 7-day pre-expiry exit window
MAX_DTE = 30  # workbench scope: contracts of no more than 30 days
TARGET_PUT_DELTA = Decimal("-0.30")

# Data-mode contract the workbench UI relies on (the `data_mode` field):
#   "batch"    — weekly-refreshed derived analytics from a delayed chain
#                (this seed); `as_of` is when the chain snapshot was taken.
#   "live"     — reserved: a real-time quote for the same contract (not wired).
#   "scenario" — user-driven hypothetical projection from real base data;
#                never presented as market data.
DATA_MODES = ("batch", "live", "scenario")
DATA_MODE = "batch"

# Freshness contract: the refresh job runs weekly; the UI shows
# "batch · <date> — stale, refresh pending" when older than this.
SEED_FRESHNESS_DAYS = 8


@dataclass(frozen=True)
class SeedContract:
    contract_id: str
    strike: Decimal
    expiration: date
    dte: int
    bid: Decimal
    ask: Decimal
    mid: Decimal
    iv: Optional[Decimal]
    delta: Decimal
    gamma: Optional[Decimal]
    theta: Optional[Decimal]
    vega: Optional[Decimal]
    rho: Optional[Decimal]
    unavailable: Tuple[Tuple[str, str], ...]
    open_interest: int
    volume: int


def _unavailable(value: Any, allow_negative: bool = False) -> bool:
    """Cboe sends exactly 0.0 for analytics it did not compute. IV is never
    negative-or-zero when computed; delta and the Greeks are signed, so only
    an exact 0.0 marks them unavailable (a ~30-DTE OTM put never has a true
    zero delta/gamma/theta/vega/rho). Unavailable is surfaced as null with a
    reason — never as a fabricated zero."""
    try:
        v = Decimal(str(value))
    except Exception:
        return True
    return v == 0 if allow_negative else v <= 0


def _dec_or_none(value: Any, field: str, missing: List[Tuple[str, str]]) -> Optional[Decimal]:
    if _unavailable(value, allow_negative=True):
        missing.append((field, "unavailable_in_source"))
        return None
    return Decimal(str(value))


def select_seed_put(raw: bytes, symbol: str, as_of: datetime) -> SeedContract:
    """Select the ~30-DTE OTM put from a real Cboe delayed chain payload."""
    if as_of.tzinfo is None:
        raise ValueError("as_of must be timezone-aware")
    symbol = str(symbol).upper().strip()
    if not symbol:
        raise ValueError("symbol required")
    try:
        data = json.loads(raw.decode("utf-8"))["data"]
    except (KeyError, IndexError, TypeError, ValueError, UnicodeDecodeError) as exc:
        raise ValueError("cboe payload malformed") from exc
    opts = data.get("options")
    if not isinstance(opts, list) or not opts:
        raise ValueError("cboe payload has no options")
    underlying_mid = (
        cboe_chain._d(data.get("bid")) + cboe_chain._d(data.get("ask"))
    ) / Decimal(2)
    if underlying_mid <= 0:
        underlying_mid = cboe_chain._d(data.get("current_price"))
    if underlying_mid <= 0:
        raise ValueError("cboe underlying price invalid")

    today = as_of.date()
    expiries: Dict[date, None] = {}
    parsed_items: List[Tuple[dict, date, Decimal]] = []
    for item in opts:
        p = cboe_chain._parse_symbol(str(item.get("option", "")))
        if p is None:
            continue
        under, expiry, ot, strike = p
        if under.upper() != symbol or ot is not OptionType.PUT:
            continue
        expiries.setdefault(expiry, None)
        parsed_items.append((item, expiry, strike))
    candidates = [
        (abs((exp - today).days - TARGET_DTE), exp)
        for exp in expiries
        if MIN_DTE < (exp - today).days <= MAX_DTE
    ]
    if not candidates:
        raise ValueError("cboe chain has no put expiration within 30 days")
    candidates.sort()
    chosen_expiry = candidates[0][1]
    dte = (chosen_expiry - today).days

    ranked: List[Tuple[Decimal, int, Decimal, dict, Decimal]] = []
    for item, expiry, strike in parsed_items:
        if expiry != chosen_expiry:
            continue
        if strike >= underlying_mid:
            continue  # OTM puts only
        bid = cboe_chain._d(item.get("bid"))
        ask = cboe_chain._d(item.get("ask"))
        try:
            bid_size = int(float(item.get("bid_size") or 0))
            ask_size = int(float(item.get("ask_size") or 0))
        except (TypeError, ValueError):
            continue
        if bid <= 0 or ask <= 0 or ask < bid or bid_size <= 0 or ask_size <= 0:
            continue  # unexecutable quote
        if _unavailable(item.get("iv")) or _unavailable(item.get("delta"), allow_negative=True):
            continue  # cannot rank or price without exchange IV/delta
        delta = Decimal(str(item.get("delta")))
        oi = int(float(item.get("open_interest") or 0))
        ranked.append((abs(delta - TARGET_PUT_DELTA), -oi, ask, item, strike))
    if not ranked:
        raise ValueError("cboe chain has no selectable ~30-DTE OTM put")
    ranked.sort()
    _, _, _, item, strike = ranked[0]

    missing: List[Tuple[str, str]] = []
    iv = _dec_or_none(item.get("iv"), "implied_volatility", missing)
    delta = Decimal(str(item.get("delta")))
    gamma = _dec_or_none(item.get("gamma"), "gamma", missing)
    theta = _dec_or_none(item.get("theta"), "theta", missing)
    vega = _dec_or_none(item.get("vega"), "vega", missing)
    rho = _dec_or_none(item.get("rho"), "rho", missing)
    bid = cboe_chain._d(item.get("bid"))
    ask = cboe_chain._d(item.get("ask"))
    return SeedContract(
        contract_id=str(item.get("option")),
        strike=strike,
        expiration=chosen_expiry,
        dte=dte,
        bid=bid,
        ask=ask,
        mid=(bid + ask) / Decimal(2),
        iv=iv,
        delta=delta,
        gamma=gamma,
        theta=theta,
        vega=vega,
        rho=rho,
        unavailable=tuple(missing),
        open_interest=int(float(item.get("open_interest") or 0)),
        volume=int(float(item.get("volume") or 0)),
    )


def seed_to_dict(
    seed: SeedContract,
    symbol: str,
    raw_data: Dict[str, Any],
    as_of: datetime,
    refresh: Dict[str, Any],
) -> Dict[str, Any]:
    """Serialise the selected contract as derived analytics. Decimals become
    strings; unavailable analytics become explicit nulls with reasons."""
    def s(v: Optional[Decimal]) -> Optional[str]:
        return str(v) if v is not None else None

    underlying_bid = cboe_chain._d(raw_data.get("bid"))
    underlying_ask = cboe_chain._d(raw_data.get("ask"))
    return {
        "schema_version": SEED_SCHEMA_VERSION,
        "mode": "REAL_CBOE_DELAYED_SEED",
        "symbol": symbol.upper(),
        "contract_id": seed.contract_id,
        "option_type": "PUT",
        "strike": str(seed.strike),
        "expiration": seed.expiration.isoformat(),
        "days_to_expiration": seed.dte,
        "bid": str(seed.bid),
        "ask": str(seed.ask),
        "mid": str(seed.mid),
        "implied_volatility": s(seed.iv),
        "delta": str(seed.delta),
        "gamma": s(seed.gamma),
        "theta": s(seed.theta),
        "vega": s(seed.vega),
        "rho": s(seed.rho),
        "unavailable_fields": [
            {"field": f, "reason": r} for f, r in seed.unavailable
        ],
        "open_interest": seed.open_interest,
        "volume": seed.volume,
        "underlying_bid": str(underlying_bid),
        "underlying_ask": str(underlying_ask),
        "underlying_price": str(cboe_chain._d(raw_data.get("current_price"))),
        "as_of": as_of.isoformat(),
        "source": "cboe-delayed",
        "data_mode": DATA_MODE,
        "refresh": refresh,
        "trade_authorized": False,
        "note": (
            "Single-contract derived selection from a real delayed Cboe chain "
            "for research. Raw chain payloads are never committed. No "
            "probability, no Risk of Ruin. No order placed."
        ),
    }


__all__ = [
    "DATA_MODE",
    "DATA_MODES",
    "SEED_FRESHNESS_DAYS",
    "SEED_SCHEMA_VERSION",
    "SeedContract",
    "seed_freshness",
    "select_seed_put",
    "seed_to_dict",
    "validate_seed_dict",
]


def seed_freshness(as_of: datetime, now: datetime) -> str:
    """Return "fresh" if the seed snapshot `as_of` is within
    SEED_FRESHNESS_DAYS of `now`, else "stale". Pure: pass fixed clocks.
    Both args must be timezone-aware; a future `as_of` counts as fresh."""
    if as_of.tzinfo is None or now.tzinfo is None:
        raise ValueError("as_of and now must be timezone-aware")
    return "fresh" if now - as_of <= timedelta(days=SEED_FRESHNESS_DAYS) else "stale"


def validate_seed_dict(d: Dict[str, Any]) -> None:
    """Fail-closed validation of a seed dict before the workbench models from
    it. Raises ValueError with a machine-readable reason on anything that
    smells synthetic: wrong schema, unknown data_mode, missing contract
    identity, non-executable bid/ask, null IV, zero-filled or undeclared
    greeks, or DTE beyond the 30-day workbench scope. A rejected seed renders
    as "data unavailable" in the UI — never as invented numbers.

    Greeks rule (mirrors the unavailable-field policy in select_seed_put):
    an unavailable greek is None AND declared in unavailable_fields with a
    reason; a present greek is never exactly 0.0 (the source emits 0.0 for
    analytics it did not compute, which select_seed_put surfaces as null).
    """
    if not isinstance(d, dict):
        raise ValueError("seed_not_a_dict")
    if d.get("schema_version") != SEED_SCHEMA_VERSION:
        raise ValueError("seed_bad_schema_version")
    if d.get("data_mode") not in DATA_MODES:
        raise ValueError("seed_unknown_data_mode")
    for f in ("contract_id", "expiration", "as_of", "source"):
        if not d.get(f):
            raise ValueError(f"seed_missing_{f}")
    dte = d.get("days_to_expiration")
    if not isinstance(dte, int) or dte <= 0 or dte > MAX_DTE:
        raise ValueError("seed_dte_out_of_workbench_scope")

    def _money(v: Any) -> Decimal:
        try:
            return Decimal(str(v))
        except Exception:
            raise ValueError("seed_bad_money") from None

    bid, ask = _money(d.get("bid")), _money(d.get("ask"))
    if bid <= 0 or ask <= 0 or ask < bid:
        raise ValueError("seed_unexecutable_quote")
    iv = d.get("implied_volatility")
    if iv is None or _money(iv) <= 0:
        raise ValueError("seed_null_or_zero_iv")

    declared = {
        e.get("field") for e in d.get("unavailable_fields", []) if isinstance(e, dict)
    }
    for field in ("delta", "gamma", "theta", "vega", "rho"):
        v = d.get(field)
        if v is None:
            if field not in declared:
                raise ValueError(f"seed_undeclared_unavailable_greek:{field}")
        elif _money(v) == 0:
            raise ValueError(f"seed_zero_filled_greek:{field}")
