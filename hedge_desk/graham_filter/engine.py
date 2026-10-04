"""
Graham Filter — production engine.

Pure assessment logic for the trade-desk candidate workflow. No market data
is hardcoded here: every candidate payload must arrive with its own values,
timestamp, and source. Anything missing -> "data unavailable", never a guess.

Three tests (Graham, The Intelligent Investor):
  1. Margin of Safety (Ch. 20) — price cushion + premium cushion vs. standard.
  2. Adequate Return  (Ch. 1)  — annualized premium / capital at risk vs. hurdle.
  3. Own It?          (Ch. 1)  — investment vs. speculation gate, answered by
                                 the human. True / False / None (unanswered).

Mr. Market (Ch. 8) is context only: a VIX regime read that raises the margin
bar when fear is high. It never predicts and never overrides the three tests.

Verdict precedence (documented, do not reorder without user approval):
  1. data unavailable  — any required field missing/invalid. Fail closed.
  2. SPECULATION       — own-it answered No.
  3. SPECULATION       — margin rating NONE (no safety at all).
  4. NEEDS-YOU         — own-it unanswered.
  5. NEEDS-YOU         — return below hurdle ("inadequate return", NOT
                         speculation — a deliberate distinction).
  6. INVESTMENT        — passes all three tests.

STANDARDS ARE NEVER DEFAULTED. Every threshold in `Standards` is a required
field: there is no production default, because any default would be an
invented hurdle. `PROTOTYPE_STANDARDS` carries the first prototype's values
and is explicitly marked unapproved — pass it deliberately or not at all.
Calling assess()/market_regime()/assess_all() without standards raises
ValueError: a missing configuration is a programming error, not a verdict.
See STANDARDS.md for the full list of thresholds needing user approval.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

# ---------------------------------------------------------------------------
# Standards configuration — every field required, no invented defaults
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Standards:
    """BML judgment, made explicit. Construct with real, approved values.

    `label` is metadata only (not a threshold): name the standards set so
    assessments can record their provenance.
    """
    margin_strong: float      # total margin % rated STRONG at/above this
    margin_adequate: float    # ADEQUATE at/above this
    margin_thin: float        # THIN at/above this, else NONE
    manic_vix: float          # VIX above this = MANIC regime
    complacent_vix: float     # VIX below this = COMPLACENT regime
    manic_margin_bump: float  # extra margin demanded when MANIC
    default_hurdle: float     # annual % used when no per-symbol hurdle
    per_symbol_hurdles: dict = field(default_factory=dict)
    label: str = "user-approved"


# !!! UNAPPROVED — prototype values only. Every number below was chosen for
# !!! the first prototype and NONE of it is user-approved. Import and pass
# !!! this deliberately, or preferably replace it with real Standards.
# !!! It must never become an implicit default.
PROTOTYPE_STANDARDS = Standards(
    margin_strong=5.0,
    margin_adequate=2.0,
    margin_thin=0.5,
    manic_vix=30.0,
    complacent_vix=14.0,
    manic_margin_bump=2.0,
    default_hurdle=15.0,
    per_symbol_hurdles={
        "SPY": 15, "QQQ": 15, "AAPL": 20,
        "TSLA": 25, "NVDA": 22, "MSFT": 18,
    },
    label="PROTOTYPE — UNAPPROVED",
)


def _require_standards(std: Optional[Standards]) -> Standards:
    if std is None:
        raise ValueError(
            "no standards configured: pass user-approved Standards, or "
            "explicitly opt into PROTOTYPE_STANDARDS (unapproved)."
        )
    return std


# ---------------------------------------------------------------------------
# Candidate payload
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Candidate:
    """One cash-secured-put candidate. All fields required for assessment."""
    symbol: Optional[str]
    spot: Optional[float]        # underlying last price
    strike: Optional[float]      # put strike
    premium: Optional[float]     # premium per share (e.g. mid of bid/ask)
    dte: Optional[int]           # days to expiration
    timestamp: Optional[str]     # when the data was observed (ISO)
    source: Optional[str]        # where the data came from (e.g. "Yahoo Finance")


# ---------------------------------------------------------------------------
# Assessment
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = ("symbol", "spot", "strike", "premium", "dte", "timestamp", "source")


def _missing_fields(c: Candidate) -> list[str]:
    missing = [f for f in REQUIRED_FIELDS if getattr(c, f) in (None, "")]
    # Numeric sanity: non-positive spot/strike/dte are not assessable data.
    for f in ("spot", "strike", "dte"):
        v = getattr(c, f)
        if v is not None and v <= 0:
            missing.append(f"{f}<=0")
    if c.premium is not None and c.premium < 0:
        missing.append("premium<0")
    return missing


@dataclass(frozen=True)
class Assessment:
    symbol: str
    verdict: str            # INVESTMENT | SPECULATION | NEEDS-YOU | DATA-UNAVAILABLE
    reason: str
    # Test 1 — margin of safety
    price_cushion_pct: Optional[float] = None
    premium_cushion_pct: Optional[float] = None
    total_margin_pct: Optional[float] = None
    margin_rating: Optional[str] = None      # STRONG | ADEQUATE | THIN | NONE
    breakeven: Optional[float] = None
    margin_bar_pct: Optional[float] = None  # bar applied after VIX bump
    # Test 2 — adequate return
    annualized_return_pct: Optional[float] = None
    hurdle_pct: Optional[float] = None
    clears_hurdle: Optional[bool] = None
    # Test 3 — own it
    own_it: Optional[bool] = None
    # Context
    regime: Optional[str] = None            # MANIC | COMPLACENT | NORMAL
    data_unavailable_fields: tuple = ()


def market_regime(vix: float, std: Optional[Standards] = None) -> str:
    """Mr. Market context read. Never a prediction, never a trade signal."""
    std = _require_standards(std)
    if vix > std.manic_vix:
        return "MANIC"
    if vix < std.complacent_vix:
        return "COMPLACENT"
    return "NORMAL"


def assess(
    c: Candidate,
    vix: float,
    own_it: Optional[bool] = None,
    std: Optional[Standards] = None,
    hurdle_override: Optional[float] = None,
) -> Assessment:
    """Run the three tests on one candidate. Deterministic: same inputs,
    same verdict, every time. `std` is required — no invented defaults."""
    std = _require_standards(std)
    regime = market_regime(vix, std)

    missing = _missing_fields(c)
    if missing:
        return Assessment(
            symbol=c.symbol or "UNKNOWN",
            verdict="DATA-UNAVAILABLE",
            reason="data unavailable: " + ", ".join(missing),
            own_it=own_it,
            regime=regime,
            data_unavailable_fields=tuple(missing),
        )

    # --- Test 1: Margin of Safety (Ch. 20) ---
    price_cushion = (c.spot - c.strike) / c.spot * 100.0
    premium_cushion = c.premium / c.strike * 100.0
    total_margin = price_cushion + premium_cushion
    breakeven = c.strike - c.premium

    bump = std.manic_margin_bump if regime == "MANIC" else 0.0
    if total_margin >= std.margin_strong + bump:
        rating = "STRONG"
    elif total_margin >= std.margin_adequate + bump:
        rating = "ADEQUATE"
    elif total_margin >= std.margin_thin:
        rating = "THIN"
    else:
        rating = "NONE"

    # --- Test 2: Adequate Return (Ch. 1) ---
    # capital at risk per contract = strike * 100; income = premium * 100
    period_pct = c.premium / c.strike * 100.0
    ann_pct = period_pct * (365.0 / c.dte)
    hurdle = hurdle_override if hurdle_override is not None else std.per_symbol_hurdles.get(
        c.symbol, std.default_hurdle
    )
    clears = ann_pct >= hurdle

    # --- Combined verdict (precedence is contractual — see module docstring) ---
    if own_it is False:
        verdict, reason = "SPECULATION", "Own-it: No — speculation per Graham Ch.1"
    elif rating == "NONE":
        verdict, reason = (
            "SPECULATION",
            f"Margin {total_margin:.2f}% — no safety",
        )
    elif own_it is None:
        verdict, reason = "NEEDS-YOU", 'Answer "Own It?" to complete'
    elif not clears:
        verdict, reason = (
            "NEEDS-YOU",
            f"Inadequate return: {ann_pct:.1f}% below {hurdle:g}% hurdle",
        )
    else:
        verdict, reason = "INVESTMENT", "Passes all three tests"

    return Assessment(
        symbol=c.symbol,
        verdict=verdict,
        reason=reason,
        price_cushion_pct=price_cushion,
        premium_cushion_pct=premium_cushion,
        total_margin_pct=total_margin,
        margin_rating=rating,
        breakeven=breakeven,
        margin_bar_pct=bump,
        annualized_return_pct=ann_pct,
        hurdle_pct=hurdle,
        clears_hurdle=clears,
        own_it=own_it,
        regime=regime,
    )


def assess_all(
    candidates: list[Candidate],
    vix: float,
    own_it_answers: dict,
    std: Optional[Standards] = None,
    hurdle_override: Optional[float] = None,
    filter_speculation: bool = True,
) -> list[Assessment]:
    """Assess a batch. With filter_speculation, SPECULATION verdicts are
    dropped from the returned list (the ON/OFF filter in the desk UI)."""
    std = _require_standards(std)
    out = []
    for c in candidates:
        a = assess(c, vix, own_it_answers.get(c.symbol), std, hurdle_override)
        if filter_speculation and a.verdict == "SPECULATION":
            continue
        out.append(a)
    return out
