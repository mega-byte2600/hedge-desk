"""Rate and futures primitives: the closed-form arithmetic two thin desks were missing.

Bonds & Rates published nothing, and Futures Event had no basis or spread arithmetic. Both
gaps are filled with the domain's *basic* material, which is closed-form and testable - no
signal invention and no forecasting, because the domain does not ask for either.

All money and prices are ``Decimal``. Yields and durations are expressed as ratios, not
percentages, so callers cannot confuse 0.045 with 4.5.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable

from hedge_desk.options.valuation import money

SIX = Decimal("0.000001")


def _d(value) -> Decimal:
    if isinstance(value, float):
        # A float price is a bug at the boundary: convert via str so 0.1 stays 0.1.
        return Decimal(str(value))
    return Decimal(value)


# ------------------------------------------------------------------ bonds


def bond_price_from_yield(
    face: Decimal,
    coupon_rate: Decimal,
    yield_rate: Decimal,
    years: Decimal,
    periods_per_year: int = 2,
) -> Decimal:
    """Present value of a bond's cash flows at a given yield.

    Standard discounted-cash-flow pricing: the coupon annuity plus the principal, each
    period discounted at (yield / periods per year). This is the price<->yield relationship
    the domain treats as fundamental.
    """
    face, coupon_rate, yield_rate, years = _d(face), _d(coupon_rate), _d(yield_rate), _d(years)
    if periods_per_year < 1:
        raise ValueError("periods_per_year must be >= 1")
    if years < 0:
        raise ValueError("years cannot be negative")
    n = int(years * periods_per_year)
    coupon = face * coupon_rate / periods_per_year
    per_period = yield_rate / periods_per_year
    if per_period == 0:
        return money(coupon * n + face)
    discount = (Decimal(1) + per_period) ** n
    pv_coupons = coupon * (Decimal(1) - Decimal(1) / discount) / per_period
    pv_face = face / discount
    return money(pv_coupons + pv_face)


def current_yield(face: Decimal, coupon_rate: Decimal, price: Decimal) -> Decimal:
    """Annual coupon income over price. The domain's simplest yield measure."""
    face, coupon_rate, price = _d(face), _d(coupon_rate), _d(price)
    if price <= 0:
        raise ValueError("price must be > 0")
    return (face * coupon_rate / price).quantize(SIX, rounding=ROUND_HALF_UP)


def macaulay_duration(
    face: Decimal,
    coupon_rate: Decimal,
    yield_rate: Decimal,
    years: Decimal,
    periods_per_year: int = 2,
) -> Decimal:
    """Weighted average time to the cash flows, in years.

    The first-order sensitivity that turns a yield view into a price expectation.
    """
    face, coupon_rate, yield_rate, years = _d(face), _d(coupon_rate), _d(yield_rate), _d(years)
    n = int(years * periods_per_year)
    coupon = face * coupon_rate / periods_per_year
    per_period = yield_rate / periods_per_year
    total = Decimal(0)
    weighted = Decimal(0)
    for period in range(1, n + 1):
        cash = coupon + (face if period == n else Decimal(0))
        pv = cash / ((Decimal(1) + per_period) ** period)
        total += pv
        weighted += pv * period
    if total == 0:
        return Decimal("0")
    return (weighted / total / periods_per_year).quantize(SIX, rounding=ROUND_HALF_UP)


def price_change_from_duration(duration: Decimal, price: Decimal, yield_change: Decimal) -> Decimal:
    """First-order price impact of a yield move: -D x P x delta-y.

    Reported as a signed money amount. A positive yield change lowers the price.
    """
    duration, price, yield_change = _d(duration), _d(price), _d(yield_change)
    return money(-duration * price * yield_change)


def credit_spread(bond_yield_rate: Decimal, benchmark_yield_rate: Decimal) -> Decimal:
    """Compensation for credit risk: the bond's yield less the benchmark's."""
    return (_d(bond_yield_rate) - _d(benchmark_yield_rate)).quantize(SIX, rounding=ROUND_HALF_UP)


# ------------------------------------------------------------------ futures


def futures_basis(cash_price: Decimal, futures_price: Decimal) -> Decimal:
    """Basis = cash - futures. Negative basis (contango) is the normal carry state."""
    return money(_d(cash_price) - _d(futures_price))


def annualised_carry(basis: Decimal, cash_price: Decimal, days_to_expiry: int) -> Decimal:
    """Basis expressed as an annualised rate, so contracts of different tenors compare."""
    basis, cash_price = _d(basis), _d(cash_price)
    if cash_price <= 0:
        raise ValueError("cash_price must be > 0")
    if days_to_expiry <= 0:
        raise ValueError("days_to_expiry must be > 0")
    return ((basis / cash_price) * (Decimal(365) / days_to_expiry)).quantize(SIX, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class CalendarSpread:
    """Long one expiry, short another, on the same underlying."""

    symbol: str
    near_price: Decimal
    far_price: Decimal

    def __post_init__(self) -> None:
        if not self.symbol:
            raise ValueError("a spread needs its underlying")
        if _d(self.near_price) <= 0 or _d(self.far_price) <= 0:
            raise ValueError("prices must be > 0")

    @property
    def spread(self) -> Decimal:
        """Far minus near. Positive is contango, negative is backwardation."""
        return money(_d(self.far_price) - _d(self.near_price))

    @property
    def structure(self) -> str:
        return "CONTANGO" if self.spread > 0 else ("BACKWARDATION" if self.spread < 0 else "FLAT")

    def reason_codes(self) -> list[str]:
        return [f"CALENDAR_{self.structure}", "SPREAD_IS_NOT_A_FORECAST"]


@dataclass(frozen=True)
class ProcessingSpread:
    """A gross-processing-style spread across legs of a production chain.

    Values are per-unit prices for each leg; the spread is the output value less input
    costs. This is arithmetic on quoted inputs, not a margin estimate.
    """

    name: str
    output_value: Decimal
    input_costs: tuple[Decimal, ...]

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("a processing spread needs a name")
        if not self.input_costs:
            raise ValueError("at least one input cost is required")

    @property
    def gross_margin(self) -> Decimal:
        return money(_d(self.output_value) - sum((_d(c) for c in self.input_costs), Decimal(0)))

    @property
    def is_positive(self) -> bool:
        return self.gross_margin > 0

    def reason_codes(self) -> list[str]:
        return ["PROCESSING_MARGIN_POSITIVE" if self.is_positive else "PROCESSING_MARGIN_NEGATIVE"]


def curve_slope(points: Iterable[tuple[int, Decimal]]) -> Decimal:
    """Slope between the first and last point of a curve, in rate per year.

    A two-point slope is the honest minimum: it states the shape without inventing a
    fitted model the domain does not support.
    """
    pairs = [(_d(y), _d(r)) for y, r in points]
    if len(pairs) < 2:
        raise ValueError("need at least two curve points")
    pairs.sort(key=lambda p: p[0])
    (y0, r0), (y1, r1) = pairs[0], pairs[-1]
    if y1 == y0:
        raise ValueError("curve points must differ in tenor")
    # Tenors are in years for rates work; if they were passed in months this would be
    # wrong, so the contract is explicit here.
    return ((r1 - r0) / (y1 - y0)).quantize(SIX, rounding=ROUND_HALF_UP)


def curve_shape(slope: Decimal) -> str:
    slope = _d(slope)
    if slope > 0:
        return "UPWARD_SLOPING"
    if slope < 0:
        return "INVERTED"
    return "FLAT"


__all__ = [
    "CalendarSpread",
    "ProcessingSpread",
    "annualised_carry",
    "bond_price_from_yield",
    "credit_spread",
    "current_yield",
    "curve_shape",
    "curve_slope",
    "futures_basis",
    "macaulay_duration",
    "price_change_from_duration",
]
