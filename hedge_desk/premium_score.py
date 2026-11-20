"""Premium-selling score for defined-risk credit verticals (GP brief 2026-11-19).

Objective stated by the GP: the desk sells option premium, so candidates are
ranked by how well they capture time value at the right point in the
contract's life, Wall-Street style. The score is a transparent weighted sum
of four sub-scores in [0, 1]; every input and weight is reported so a trader
can see WHY a structure ranks where it does.

1. Volatility edge (30%) — variance risk premium: short-leg implied vol over
   the underlying's 21-day realized vol, (IV - RV) / IV, saturating at 0.5.
   Implied vol has historically exceeded subsequently realized vol on index
   options (Carr & Wu 2009, "Variance Risk Premiums", RFS 22(3); Bollerslev,
   Tauchen & Zhou 2009); selling when the spread is wide is the core edge.
   No RV available -> 0 (no unearned credit) and a ``RV_UNAVAILABLE`` flag.
2. Time-value efficiency (25%) — return on COLLATERAL (credit / spread
   width), scaled to 30 days, full marks at 30%/30 days (SOUL rule 8).
3. Entry window (25%) — days to expiration. Full score 30-45 DTE, linear to
   zero at 14 and 60 DTE: theta accelerates inside ~45 DTE while gamma risk
   becomes dominant inside ~21 DTE (CBOE PUT/BXM index methodology rolls
   monthly; widely used practitioner management: enter 30-45 DTE, exit at
   50% of max profit or 21 DTE, whichever comes first).
4. Short-strike placement (20%) — |delta| of the short leg. Full score
   0.16-0.30 (about 70-84% risk-neutral probability of expiring OTM), linear
   to zero at 0.05 and 0.45.

Deterministic and pure: no network, no randomness, no order, no RoR.
The score ranks research candidates; it never authorizes a trade.
"""
from __future__ import annotations

import math
from typing import Any, Dict, Optional

SCHEMA_VERSION = "hedge-desk-premium-score-1.0.0"
WEIGHTS = {"vol_edge": 0.30, "time_value": 0.25, "entry_window": 0.25, "strike_placement": 0.20}
MANAGEMENT = {"take_profit_pct_of_credit": 50, "time_exit_dte": 21}


def _ramp(x: float, zero_lo: float, full_lo: float, full_hi: float, zero_hi: float) -> float:
    if x <= zero_lo or x >= zero_hi:
        return 0.0
    if full_lo <= x <= full_hi:
        return 1.0
    if x < full_lo:
        return (x - zero_lo) / (full_lo - zero_lo)
    return (zero_hi - x) / (zero_hi - full_hi)


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def parse_occ(contract: str) -> Optional[Dict[str, Any]]:
    """'SPY261224C00740000' -> {'type': 'C', 'strike': 740.0}."""
    s = str(contract).strip().upper()
    if len(s) < 15 or s[-9] not in "CP":
        return None
    try:
        return {"type": s[-9], "strike": int(s[-8:]) / 1000.0}
    except ValueError:
        return None


def short_leg_delta(spot: float, strike: float, years: float, iv: float, is_call: bool,
                    rate: float = 0.0, dividend_yield: float = 0.0) -> Optional[float]:
    """Black-Scholes-Merton delta of the short leg (absolute value), with the
    same continuous rate r and dividend yield q as win_probability model 2.0.0:
    call e^{-qT} N(d1), put e^{-qT} (N(d1) - 1)."""
    if spot <= 0 or strike <= 0 or years <= 0 or iv <= 0:
        return None
    d1 = (math.log(spot / strike) + (rate - dividend_yield + 0.5 * iv * iv) * years) / (iv * math.sqrt(years))
    disc = math.exp(-dividend_yield * years)
    return abs(disc * _norm_cdf(d1) if is_call else disc * (_norm_cdf(d1) - 1.0))


def annualized_rv(daily_log_return_sd: Optional[float]) -> Optional[float]:
    return None if daily_log_return_sd is None else float(daily_log_return_sd) * math.sqrt(252.0)


# GP brief bands (hard eligibility) and time-value scale.
DELTA_BAND = (0.16, 0.30)        # ~70-84% risk-neutral OTM probability
DTE_BAND = (21.0, 60.0)          # managed-exit floor (21) to longest useful window
ROC_30D_FULL = 0.30              # 30% return on collateral per 30 days = full marks


def rank_key(row: Dict[str, Any]):
    """Eligible first, then premium score, then return on collateral."""
    p = row.get("premium") or {}
    return (not p.get("eligible", False), -float(p.get("premium_score") or 0),
            -float((p.get("inputs") or {}).get("return_on_collateral") or 0), row.get("contract_id", ""))


def short_leg_id(row: Dict[str, Any]) -> str:
    return str(row.get("contract_id", "")).split("--")[0]


def unique_by_short_leg(rows):
    """One row per short strike/expiry: several long wings on the same short
    leg are the same trade decision, so a shortlist shows only the best."""
    seen, out = set(), []
    for r in rows:
        k = short_leg_id(r)
        if k not in seen:
            seen.add(k)
            out.append(r)
    return out


# SPY trailing 12-month distribution yield (approx. 1.2%); an explicit,
# overridable assumption until a dividend feed is wired.
DEFAULT_DIVIDEND_YIELD = {"SPY": 0.012}


def score_structure(structure: Dict[str, Any], spot: float,
                    realized_vol_annual: Optional[float],
                    rate: float = 0.0, dividend_yield: float = 0.0) -> Dict[str, Any]:
    """Return the premium score block for one credit vertical."""
    flags = []
    dte = float(structure.get("days_to_expiration") or 0)
    credit = float(structure.get("net_credit") or 0)
    max_loss = float(structure.get("maximum_loss") or 0)
    iv = float(structure["short_leg_iv"]) if structure.get("short_leg_iv") else None
    short_id = str(structure.get("contract_id", "")).split("--")[0]
    occ = parse_occ(short_id)

    if iv is None:
        flags.append("IV_UNAVAILABLE")
    if realized_vol_annual and iv:
        vrp = (iv - realized_vol_annual) / iv
        vol_edge = min(1.0, max(0.0, vrp / 0.5))
    else:
        # Conservative: no measured edge -> no credit (was a neutral 0.5,
        # which handed every structure 15 points it had not earned).
        vrp, vol_edge = None, 0.0
        flags.append("RV_UNAVAILABLE")
    monthly_ror = (credit / max_loss) * (30.0 / dte) if max_loss > 0 and dte > 0 else 0.0
    # SOUL rule 8: return on COLLATERAL. For a defined-risk vertical the
    # collateral is the full width (credit + max loss), not the max loss.
    collateral = credit + max_loss
    roc = credit / collateral if collateral > 0 else 0.0
    roc_30d = roc * (30.0 / dte) if dte > 0 else 0.0
    time_value = min(1.0, max(0.0, roc_30d / ROC_30D_FULL))
    entry_window = _ramp(dte, 14, 30, 45, 60)
    delta = (short_leg_delta(spot, occ["strike"], dte / 365.0, iv, occ["type"] == "C", rate, dividend_yield)
             if occ and iv else None)
    if delta is None:
        flags.append("DELTA_UNAVAILABLE")
    strike_placement = _ramp(delta, 0.05, 0.16, 0.30, 0.45) if delta is not None else 0.0
    parts = {"vol_edge": vol_edge, "time_value": time_value,
             "entry_window": entry_window, "strike_placement": strike_placement}
    score = 100.0 * sum(WEIGHTS[k] * v for k, v in parts.items())
    # Eligibility = the GP brief as hard constraints. Ineligible structures
    # stay visible (with reasons) but can never outrank an eligible one.
    reasons = []
    if delta is None or not (DELTA_BAND[0] <= delta <= DELTA_BAND[1]):
        reasons.append("DELTA_OUT_OF_BAND")
    if vrp is None or vrp <= 0:
        reasons.append("NO_VOL_EDGE")
    if not (DTE_BAND[0] <= dte <= DTE_BAND[1]):
        reasons.append("DTE_OUT_OF_WINDOW")
    return {
        "premium_score": round(score, 1),
        "eligible": not reasons,
        "eligibility_reasons": reasons,
        "components": {k: round(v, 3) for k, v in parts.items()},
        "inputs": {"short_leg_iv": iv, "realized_vol_21d_annual": realized_vol_annual,
                   "variance_risk_premium": None if vrp is None else round(vrp, 4),
                   "monthly_return_on_risk": round(monthly_ror, 4),
                   "collateral_usd": round(collateral, 2),
                   "return_on_collateral": round(roc, 4),
                   "return_on_collateral_30d": round(roc_30d, 4),
                   "annualized_return_on_risk": round(monthly_ror * 365.0 / 30.0, 4),
                   "rate": rate, "dividend_yield": dividend_yield,
                   "short_leg_abs_delta": None if delta is None else round(delta, 4),
                   "days_to_expiration": dte},
        "management": {"take_profit_at_credit_captured": round(credit * MANAGEMENT["take_profit_pct_of_credit"] / 100, 2),
                       "time_exit_dte": MANAGEMENT["time_exit_dte"],
                       "days_until_time_exit": max(0, int(dte) - MANAGEMENT["time_exit_dte"])},
        "flags": flags,
        "weights": WEIGHTS,
        "schema_version": SCHEMA_VERSION,
    }


def rank_chain_income(chain: Dict[str, Any], realized_vol_annual: Optional[float],
                      rate: float = 0.0, dividend_yield: Optional[float] = None) -> Dict[str, Any]:
    """Annotate and re-rank a real_chain_income payload by premium score."""
    try:
        spot = (float(chain["underlying_bid"]) + float(chain["underlying_ask"])) / 2
    except (KeyError, TypeError, ValueError):
        return chain
    if dividend_yield is None:
        dividend_yield = DEFAULT_DIVIDEND_YIELD.get(str(chain.get("symbol", "")).upper(), 0.0)
    out = dict(chain)
    for key in ("income_structures", "gated_income_structures"):
        rows = []
        for s in chain.get(key) or []:
            r = dict(s)
            r["premium"] = score_structure(r, spot, realized_vol_annual, rate, dividend_yield)
            rows.append(r)
        rows.sort(key=rank_key)
        if key in chain:
            out[key] = rows
    out["ranking"] = {"by": "premium_score", "schema_version": SCHEMA_VERSION,
                      "realized_vol_21d_annual": realized_vol_annual, "weights": WEIGHTS,
                      "rate": rate, "dividend_yield": dividend_yield}
    return out


__all__ = ["score_structure", "rank_chain_income", "rank_key", "unique_by_short_leg", "DELTA_BAND", "parse_occ", "short_leg_delta",
           "annualized_rv", "WEIGHTS", "SCHEMA_VERSION"]
