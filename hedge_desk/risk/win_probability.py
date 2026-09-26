"""Market-implied win probability for a short put, from real option data.

The win probability of a cash-secured put / short-put leg is the probability
the underlying stays above the short strike at expiration. The standard,
sourced market convention is to use the put's Black-Scholes delta as the
probability of finishing in-the-money: |delta_put| ~= P(ITM). So

    win_probability = 1 - |delta_put|

where delta_put is computed from REAL option inputs (strike, spot, time to
expiry, risk-free rate) and an implied volatility backed out of the real
option mid price by Black-Scholes inversion (bisection).

This is a sourced, reproducible model input — NOT a fabricated number and NOT
a performance claim. It is a financial-model change and therefore requires
reference cases and independent review before release (AGENTS.md). It is
built and tested here; it is not self-approved for release.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

# Black-Scholes normal CDF (Abramowitz & Stegun 7.1.26, 7.1.28).
def _norm_cdf(x: float) -> float:
    if x < -6.0:
        return 0.0
    if x > 6.0:
        return 1.0
    t = 1.0 / (1.0 + 0.2316419 * abs(x))
    d = 0.3989422804014327 * math.exp(-0.5 * x * x)
    # A&S 7.1.26: this polynomial is the TAIL probability for positive x.
    tail = d * t * (0.319381530 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))))
    return 1.0 - tail if x >= 0 else tail


def _bs_put_price(s: float, k: float, t: float, r: float, sigma: float) -> float:
    if t <= 0 or sigma <= 0:
        return max(k - s, 0.0)
    d1 = (math.log(s / k) + (r + 0.5 * sigma * sigma) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    return k * math.exp(-r * t) * _norm_cdf(-d2) - s * _norm_cdf(-d1)


def _bs_put_delta(s: float, k: float, t: float, r: float, sigma: float) -> float:
    if t <= 0 or sigma <= 0:
        return -1.0 if k > s else 0.0
    d1 = (math.log(s / k) + (r + 0.5 * sigma * sigma) * t) / (sigma * math.sqrt(t))
    return _norm_cdf(d1) - 1.0


def implied_volatility(
    option_price: float,
    spot: float,
    strike: float,
    years_to_expiry: float,
    rate: float = 0.0,
    lo: float = 0.01,
    hi: float = 5.0,
    tol: float = 1e-8,
    max_iter: int = 200,
) -> Optional[float]:
    """Back out implied volatility from a put price by bisection on BS."""
    if option_price <= 0 or spot <= 0 or strike <= 0 or years_to_expiry <= 0:
        return None
    intrinsic = max(strike - spot, 0.0)
    if option_price < intrinsic:
        return None
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        price = _bs_put_price(spot, strike, years_to_expiry, rate, mid)
        if abs(price - option_price) < tol:
            return mid
        if price < option_price:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


@dataclass(frozen=True)
class WinProbabilityResult:
    win_probability: Decimal
    implied_volatility: Decimal
    put_delta: Decimal
    model_id: str
    model_version: str
    source: str


MODEL_ID = "market-implied-put-delta"
MODEL_VERSION = "1.0.0"


def win_probability_for_short_put(
    spot: Decimal,
    strike: Decimal,
    expiration: date,
    as_of: datetime,
    option_mid_price: Decimal,
    rate: Decimal = Decimal("0.0"),
) -> WinProbabilityResult:
    """Win probability = 1 - |put delta|, IV backed out of the real mid price.

    ``as_of`` must be timezone-aware. ``expiration`` must be after ``as_of``.
    Raises ValueError on invalid inputs (fail closed — never fabricate).
    """
    if as_of.tzinfo is None:
        raise ValueError("as_of must be timezone-aware")
    if spot <= 0 or strike <= 0 or option_mid_price <= 0:
        raise ValueError("spot, strike, and option price must be positive")
    years = (expiration - as_of.date()).days / 365.0
    if years <= 0:
        raise ValueError("expiration must be after as_of")

    iv = implied_volatility(
        float(option_mid_price), float(spot), float(strike), years, float(rate)
    )
    if iv is None:
        raise ValueError("could not back out implied volatility from option price")
    delta = _bs_put_delta(float(spot), float(strike), years, float(rate), iv)
    win_prob = Decimal("1") - abs(Decimal(str(delta)))
    # Clamp to a sane probability band; never 0 or 1 (a degenerate claim).
    win_prob = min(Decimal("0.9999"), max(Decimal("0.0001"), win_prob))
    return WinProbabilityResult(
        win_probability=win_prob,
        implied_volatility=Decimal(str(iv)),
        put_delta=Decimal(str(delta)),
        model_id=MODEL_ID,
        model_version=MODEL_VERSION,
        source="cboe-delayed-public-http-200",
    )


__all__ = [
    "MODEL_ID",
    "MODEL_VERSION",
    "WinProbabilityResult",
    "win_probability_for_short_put",
    "implied_volatility",
]
