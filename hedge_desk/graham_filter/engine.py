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
invented hurdle. `PROPOSED_STANDARDS` carries Graham-sourced values (see
PROVENANCE) and is explicitly marked unapproved — pass it deliberately or
not at all.
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


# ---------------------------------------------------------------------------
# PROPOSED standards — Graham-sourced, NOT user-approved.
#
# Every value below is anchored in Benjamin Graham's published criteria
# (The Intelligent Investor / Security Analysis) with chapter-level
# provenance. Where Graham states a principle but no number, the value is
# marked interpreted=True and the reasoning is shown — an interpretation is
# never presented as Graham's own words. NOTHING here is user-approved: the
# UI must badge these as proposed, exactly as it badged the prototype.
# Import and pass PROPOSED_STANDARDS deliberately, or preferably replace it
# with real user-approved Standards. It must never become an implicit
# default.
# ---------------------------------------------------------------------------

PROVENANCE = {
    "margin_strong": {
        "value": 33.0,
        "source": (
            "The Intelligent Investor, Ch. 15 — net-net rule: buy at no more "
            "than 2/3 of net current asset value (a one-third discount), "
            "Graham's canonical 'decisive' margin of safety."
        ),
        "interpreted": True,
        "reasoning": (
            "Graham never rated put-strike cushions; 33% maps his only hard "
            "numerical margin-of-safety rule (the one-third NCAV discount) "
            "onto total cushion %. A >=33% cushion is a decisive margin in "
            "Graham's terms."
        ),
        "what_would_change_it": (
            "The user defines their own cushion bands for puts, or picks a "
            "different Graham anchor."
        ),
        "approved": False,
    },
    "margin_adequate": {
        "value": 20.0,
        "source": (
            "The Intelligent Investor, Ch. 20 (margin-of-safety principle). "
            "No direct Graham number exists for an 'adequate' band."
        ),
        "interpreted": True,
        "reasoning": (
            "Set between the net-net anchor (33) and the thin floor (10): a "
            "cushion that absorbs a one-fifth adverse move before impairment "
            "— a passing but not decisive margin."
        ),
        "what_would_change_it": "The user defines their own bands.",
        "approved": False,
    },
    "margin_thin": {
        "value": 10.0,
        "source": (
            "The Intelligent Investor, Ch. 1 (investment requires safety of "
            "principal) and Ch. 20. No direct Graham number exists for a "
            "'thin' band."
        ),
        "interpreted": True,
        "reasoning": (
            "Double-digit minimum: absorbs a 10% adverse move before capital "
            "impairment. Below this there is, in Graham's terms, no safety "
            "of principal at all — hence NONE below 10."
        ),
        "what_would_change_it": "The user defines their own floor.",
        "approved": False,
    },
    "manic_vix": {
        "value": 30.0,
        "source": (
            "The Intelligent Investor, Ch. 8 (Mr. Market: markets swing "
            "between mania and depression). The VIX did not exist in Graham's "
            "lifetime (created 1993); 30 is the market-convention fear "
            "threshold, roughly 1.5x the ~19-20 long-run average."
        ),
        "interpreted": True,
        "reasoning": (
            "Ch. 8 gives the principle but no number. 30 operationalizes "
            "'manic' with the standard practitioner fear line."
        ),
        "what_would_change_it": (
            "The user picks a different fear threshold or a different fear gauge."
        ),
        "approved": False,
    },
    "complacent_vix": {
        "value": 14.0,
        "source": (
            "The Intelligent Investor, Ch. 8 (Mr. Market). VIX below ~14 sits "
            "in the index's historical low zone — the practitioner read of "
            "complacency."
        ),
        "interpreted": True,
        "reasoning": (
            "Mirror of manic_vix: Ch. 8's depressive/complacent pole, "
            "quantified at the VIX's historical low zone."
        ),
        "what_would_change_it": "The user picks a different complacency line.",
        "approved": False,
    },
    "manic_margin_bump": {
        "value": 5.0,
        "source": (
            "The Intelligent Investor, Ch. 20 — the margin of safety must be "
            "larger when the future is less certain (its function is "
            "'rendering unnecessary an accurate estimate of the future')."
        ),
        "interpreted": True,
        "reasoning": (
            "Graham demands more margin under greater uncertainty but gives "
            "no number. 5 points = half the thin floor: a material, not "
            "prohibitive, extra cushion when Mr. Market is manic."
        ),
        "what_would_change_it": (
            "User judgment on how much extra cushion fear markets must pay."
        ),
        "approved": False,
    },
    "default_hurdle": {
        "value": 12.0,
        "source": (
            "The Intelligent Investor, Ch. 11 — the valuation formula "
            "Value = EPS x (8.5 + 2g): 8.5 is Graham's no-growth P/E, i.e. a "
            "1/8.5 = 11.8% required earnings yield for a no-growth business."
        ),
        "interpreted": True,
        "reasoning": (
            "A cash-secured put is a no-growth income operation. Graham's "
            "no-growth baseline demands ~12% yield; the premium hurdle is set "
            "there (rounded). Consistent with Ch. 5's bond thinking: required "
            "yield well above default-free rates."
        ),
        "what_would_change_it": (
            "The user sets their own definition of 'adequate return'."
        ),
        "approved": False,
    },
    "per_symbol_hurdles": {
        "value": {},
        "source": (
            "No Graham source exists — Graham never set per-ticker return "
            "hurdles. Deliberately empty: every symbol falls back to "
            "default_hurdle uniformly."
        ),
        "interpreted": True,
        "reasoning": (
            "Per-name differentiation is a user judgment call, not something "
            "Graham published. An empty map is honest; inventing per-ticker "
            "bars would be invention."
        ),
        "what_would_change_it": "The user assigns per-name hurdles.",
        "approved": False,
    },
}

PROPOSED_STANDARDS = Standards(
    margin_strong=PROVENANCE["margin_strong"]["value"],
    margin_adequate=PROVENANCE["margin_adequate"]["value"],
    margin_thin=PROVENANCE["margin_thin"]["value"],
    manic_vix=PROVENANCE["manic_vix"]["value"],
    complacent_vix=PROVENANCE["complacent_vix"]["value"],
    manic_margin_bump=PROVENANCE["manic_margin_bump"]["value"],
    default_hurdle=PROVENANCE["default_hurdle"]["value"],
    per_symbol_hurdles=dict(PROVENANCE["per_symbol_hurdles"]["value"]),
    label="PROPOSED — Toby, pending user approval",
)


def _require_standards(std: Optional[Standards]) -> Standards:
    if std is None:
        raise ValueError(
            "no standards configured: pass user-approved Standards, or "
            "explicitly opt into PROPOSED_STANDARDS (unapproved)."
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
