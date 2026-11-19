"""Market-implied win probability for a short put, from real option data.

Model 2.0.0 (GP-approved promotion, 2026-11-19): the win probability of a
short put is the Black-Scholes-Merton risk-neutral probability that the
underlying finishes ABOVE the strike at expiration:

    win_probability = P_Q(S_T > K) = N(d2)
    d2 = [ln(S/K) + (r - q - sigma^2/2) T] / (sigma sqrt(T))

with r the continuously-compounded risk-free rate, q the continuous dividend
yield, T in ACT/365 years, and sigma the implied volatility backed out of the
real option mid price under the SAME (r, q) by bisection on the Merton put
price (Hull, *Options, Futures, and Other Derivatives*, 11th ed., §15.8
eq. 15.21 and §17.4: N(d2) is the risk-neutral exercise probability; Merton
1973 for the dividend yield).

Model 1.0.0 used 1 - |delta_put| = N(d1) adjusted, which OVERSTATES the short
put's win probability by about phi(d2) * sigma * sqrt(T) (≈2.6 points for a
30-day 5%-OTM put at 28% IV). That value is still reported as
``delta_rule_win_probability`` for audit only.

IMPORTANT: this is a RISK-NEUTRAL (pricing-measure) probability implied by
the option market, not a forecast of the real-world (physical-measure)
probability. The two differ by the variance risk premium; on index puts the
real-world win rate has historically been higher than N(d2) implies. Use it
as the market's price of the outcome, not as an edge estimate.

Sourced, reproducible model input — not a performance claim. Exact reference
cases live in tests/test_win_probability.py.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

MODEL_ID = "bsm-risk-neutral-n-d2"
MODEL_VERSION = "2.0.0"
_PROB_FLOOR, _PROB_CAP = Decimal("0.0001"), Decimal("0.9999")


def _norm_cdf(x: float) -> float:
    """Standard normal CDF via the C-library erf (exact to double precision)."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _d1_d2(s: float, k: float, t: float, r: float, sigma: float, q: float = 0.0):
    vt = sigma * math.sqrt(t)
    d1 = (math.log(s / k) + (r - q + 0.5 * sigma * sigma) * t) / vt
    return d1, d1 - vt


def _bs_put_price(s: float, k: float, t: float, r: float, sigma: float, q: float = 0.0) -> float:
    """Merton put price with continuous dividend yield q."""
    if t <= 0 or sigma <= 0:
        return max(k * math.exp(-r * max(t, 0)) - s * math.exp(-q * max(t, 0)), 0.0)
    d1, d2 = _d1_d2(s, k, t, r, sigma, q)
    return k * math.exp(-r * t) * _norm_cdf(-d2) - s * math.exp(-q * t) * _norm_cdf(-d1)


def _bs_d2(s: float, k: float, t: float, r: float, sigma: float, q: float = 0.0) -> float:
    return _d1_d2(s, k, t, r, sigma, q)[1]


def _bs_put_delta(s: float, k: float, t: float, r: float, sigma: float, q: float = 0.0) -> float:
    if t <= 0 or sigma <= 0:
        return -1.0 if k > s else 0.0
    d1, _ = _d1_d2(s, k, t, r, sigma, q)
    return math.exp(-q * t) * (_norm_cdf(d1) - 1.0)


def implied_volatility(
    option_price: float,
    spot: float,
    strike: float,
    years_to_expiry: float,
    rate: float = 0.0,
    dividend_yield: float = 0.0,
    lo: float = 0.001,
    hi: float = 5.0,
    tol: float = 1e-10,
    max_iter: int = 300,
) -> Optional[float]:
    """Back out implied volatility from a put price by bisection on Merton.

    Returns None if the price is outside the no-arbitrage band
    [max(K e^{-rT} - S e^{-qT}, 0), K e^{-rT}].
    """
    if option_price <= 0 or spot <= 0 or strike <= 0 or years_to_expiry <= 0:
        return None
    t = years_to_expiry
    lower = max(strike * math.exp(-rate * t) - spot * math.exp(-dividend_yield * t), 0.0)
    if option_price < lower or option_price >= strike * math.exp(-rate * t):
        return None
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        price = _bs_put_price(spot, strike, t, rate, mid, dividend_yield)
        if abs(price - option_price) < tol:
            return mid
        if price < option_price:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


@dataclass(frozen=True)
class WinProbabilityResult:
    win_probability: Decimal               # N(d2): the gate value (model 2.0.0)
    implied_volatility: Decimal
    put_delta: Decimal
    model_id: str
    model_version: str
    source: str
    risk_neutral_win_probability: Optional[Decimal] = None  # == win_probability (kept for API stability)
    delta_rule_win_probability: Optional[Decimal] = None    # model 1.0.0 value, audit only
    rate: Decimal = Decimal("0")
    dividend_yield: Decimal = Decimal("0")
    years_to_expiry: Optional[Decimal] = None
    measure: str = "risk-neutral"


def _clamp(p: float) -> Decimal:
    return min(_PROB_CAP, max(_PROB_FLOOR, Decimal(repr(p))))


def win_probability_for_short_put(
    spot: Decimal,
    strike: Decimal,
    expiration: date,
    as_of: datetime,
    option_mid_price: Decimal,
    rate: Decimal = Decimal("0.0"),
    dividend_yield: Decimal = Decimal("0.0"),
) -> WinProbabilityResult:
    """Win probability = N(d2) under Black-Scholes-Merton, IV from the real mid.

    ``rate`` and ``dividend_yield`` are continuously compounded annual rates
    (e.g. Decimal("0.043")). Pass the Treasury yield matching the expiry and
    the underlying's dividend yield for accuracy; both default to 0.
    ``as_of`` must be timezone-aware and before ``expiration``.
    Raises ValueError on invalid inputs (fail closed — never fabricate).
    """
    if as_of.tzinfo is None:
        raise ValueError("as_of must be timezone-aware")
    if spot <= 0 or strike <= 0 or option_mid_price <= 0:
        raise ValueError("spot, strike, and option price must be positive")
    if not (Decimal("-0.05") <= rate <= Decimal("0.25")) or not (Decimal("0") <= dividend_yield <= Decimal("0.25")):
        raise ValueError("rate or dividend_yield outside plausible bounds")
    years = (expiration - as_of.date()).days / 365.0
    if years <= 0:
        raise ValueError("expiration must be after as_of")
    s, k, r, q = float(spot), float(strike), float(rate), float(dividend_yield)
    iv = implied_volatility(float(option_mid_price), s, k, years, r, q)
    if iv is None:
        raise ValueError("could not back out implied volatility from option price")
    _, d2 = _d1_d2(s, k, years, r, iv, q)
    delta = _bs_put_delta(s, k, years, r, iv, q)
    win = _clamp(_norm_cdf(d2))
    return WinProbabilityResult(
        win_probability=win,
        implied_volatility=Decimal(repr(iv)),
        put_delta=Decimal(repr(delta)),
        model_id=MODEL_ID,
        model_version=MODEL_VERSION,
        source="cboe-delayed-public-http-200",
        risk_neutral_win_probability=win,
        delta_rule_win_probability=_clamp(1.0 - abs(delta)),
        rate=rate,
        dividend_yield=dividend_yield,
        years_to_expiry=Decimal(repr(years)),
    )


__all__ = [
    "MODEL_ID",
    "MODEL_VERSION",
    "WinProbabilityResult",
    "win_probability_for_short_put",
    "implied_volatility",
]
