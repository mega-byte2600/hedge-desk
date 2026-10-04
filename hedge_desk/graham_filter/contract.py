"""
Graham Filter — serialization / UI contract.

The exact JSON the frontend consumes. This is a contract: the UI renders
from these fields and these fields only. Verdict strings are literal —
the UI must display them verbatim, never reword.

Verdict column values (exact):
    INVESTMENT | SPECULATION | NEEDS-YOU | DATA-UNAVAILABLE

ON/OFF filter toggle semantics:
    mode "hide_speculation" (toggle ON,  default): SPECULATION rows are
        dropped from the list. NEEDS-YOU and DATA-UNAVAILABLE rows are
        ALWAYS shown — the user must see what needs them and what is
        missing data.
    mode "all"              (toggle OFF): every row is shown, including
        SPECULATION.

Row schema (to_dict):
    {
        "symbol": "SPY",
        "verdict": "INVESTMENT",
        "reason": "Passes all three tests",
        "margin": {
            "price_cushion_pct": 5.0,
            "premium_cushion_pct": 1.05,
            "total_margin_pct": 6.05,
            "rating": "STRONG",            # STRONG | ADEQUATE | THIN | NONE
            "breakeven": 564.0,
            "bar_pct": 0.0,                # VIX bump applied (0 when calm)
        } | null,                          # null when DATA-UNAVAILABLE
        "return": {
            "annualized_pct": 12.8,
            "hurdle_pct": 10.0,
            "clears_hurdle": true,
        } | null,                          # null when DATA-UNAVAILABLE
        "own_it": true,                    # true | false | null (unanswered)
        "regime": "NORMAL",                # MANIC | COMPLACENT | NORMAL | null
        "data_unavailable_fields": [],     # e.g. ["premium", "vix"]
        "standards": {
            "label": "PROTOTYPE — UNAPPROVED",
            "approved": false,             # UI must badge unapproved standards
        },
        "assessed_at": "2026-10-04T19:00:00+00:00",
    }

Batch shape: {"rows": [row, ...], "filter": "hide_speculation", "count": n}
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from .engine import Assessment

VERDICTS = ("INVESTMENT", "SPECULATION", "NEEDS-YOU", "DATA-UNAVAILABLE")

# Toggle ON  -> "hide_speculation"   (SPECULATION rows dropped)
# Toggle OFF -> "all"                (everything shown)
FILTER_MODES = ("hide_speculation", "all")
DEFAULT_FILTER = "hide_speculation"


def to_dict(
    a: Assessment,
    standards_label: str,
    standards_approved: bool,
) -> dict:
    margin = None
    if a.total_margin_pct is not None:
        margin = {
            "price_cushion_pct": a.price_cushion_pct,
            "premium_cushion_pct": a.premium_cushion_pct,
            "total_margin_pct": a.total_margin_pct,
            "rating": a.margin_rating,
            "breakeven": a.breakeven,
            "bar_pct": a.margin_bar_pct,
        }
    ret = None
    if a.annualized_return_pct is not None:
        ret = {
            "annualized_pct": a.annualized_return_pct,
            "hurdle_pct": a.hurdle_pct,
            "clears_hurdle": a.clears_hurdle,
        }
    return {
        "symbol": a.symbol,
        "verdict": a.verdict,
        "reason": a.reason,
        "margin": margin,
        "return": ret,
        "own_it": a.own_it,
        "regime": a.regime,
        "data_unavailable_fields": list(a.data_unavailable_fields),
        "standards": {
            "label": standards_label,
            "approved": standards_approved,
        },
        "assessed_at": datetime.now(timezone.utc).isoformat(),
    }


def apply_filter(rows: list[dict], mode: str = DEFAULT_FILTER) -> list[dict]:
    """Apply the ON/OFF toggle to serialized rows."""
    if mode not in FILTER_MODES:
        raise ValueError(f"unknown filter mode: {mode!r} (want one of {FILTER_MODES})")
    if mode == "hide_speculation":
        return [r for r in rows if r["verdict"] != "SPECULATION"]
    return list(rows)


def to_batch(
    assessments: list[Assessment],
    standards_label: str,
    standards_approved: bool,
    filter_mode: str = DEFAULT_FILTER,
) -> dict:
    rows = [to_dict(a, standards_label, standards_approved) for a in assessments]
    shown = apply_filter(rows, filter_mode)
    return {"rows": shown, "filter": filter_mode, "count": len(shown)}
