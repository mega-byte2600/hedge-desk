"""
Graham Filter — candidate payload adapter.

Boundary between the outside world and the pure engine. Accepts a plain
dict in a documented minimal shape, validates every field, and NEVER
invents a value: anything missing or mistyped becomes None, which the
engine turns into a literal DATA-UNAVAILABLE verdict.

Documented minimal candidate shape (keys beyond these are ignored):
    {
        "symbol":    str,    # ticker, e.g. "SPY" (required)
        "spot":      number, # underlying last price (required, > 0)
        "strike":    number, # put strike (required, > 0)
        "premium":   number, # premium per share, e.g. mid of bid/ask (required, >= 0)
        "dte":       number, # days to expiration (required, > 0)
        "timestamp": str,    # when observed, ISO-8601 (required, non-empty)
        "source":    str,    # where from, e.g. "Yahoo Finance" (required, non-empty)
    }

Validation rules:
  - numerics: int/float only (bool rejected), finite (no NaN/inf).
  - strings: stripped; empty/whitespace-only counts as missing.
  - vix: validated the same way; a missing/invalid VIX is DATA-UNAVAILABLE
    (the margin bar cannot be computed without the regime read — never assume calm).
  - own_it: True / False / None only; anything else -> None (unanswered).
  - the adapter never raises on bad input. A non-dict payload, like bad
    fields, degrades to DATA-UNAVAILABLE. Missing *configuration* (no
    standards) still raises ValueError from the engine — that is a
    programming error, not a verdict.
"""

from __future__ import annotations

import math
from typing import Any, Optional

from .engine import Assessment, Candidate, Standards, assess


def _num(v: Any) -> Optional[float]:
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)) and math.isfinite(v):
        return v
    return None


def _str(v: Any) -> Optional[str]:
    if isinstance(v, str) and v.strip():
        return v.strip()
    return None


def _own_it(v: Any) -> Optional[bool]:
    return v if v is True or v is False else None


def adapt(payload: Any) -> Candidate:
    """Build a Candidate from an untrusted dict. Never raises."""
    p = payload if isinstance(payload, dict) else {}
    return Candidate(
        symbol=_str(p.get("symbol")),
        spot=_num(p.get("spot")),
        strike=_num(p.get("strike")),
        premium=_num(p.get("premium")),
        dte=_num(p.get("dte")),
        timestamp=_str(p.get("timestamp")),
        source=_str(p.get("source")),
    )


def adapt_assess(
    payload: Any,
    vix: Any,
    own_it: Any = None,
    std: Optional[Standards] = None,
    hurdle_override: Optional[float] = None,
) -> Assessment:
    """Validate payload + VIX, then run the engine. Returns an Assessment
    in all cases except missing standards (ValueError — fail fast)."""
    c = adapt(payload)
    v = _num(vix)
    if v is None or v <= 0:
        return Assessment(
            symbol=c.symbol or "UNKNOWN",
            verdict="DATA-UNAVAILABLE",
            reason="data unavailable: vix",
            own_it=_own_it(own_it),
            data_unavailable_fields=("vix",),
        )
    return assess(c, v, _own_it(own_it), std=std, hurdle_override=hurdle_override)
