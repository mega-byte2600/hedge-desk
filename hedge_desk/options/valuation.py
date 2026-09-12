"""Option valuation primitives: the basic-concept layer the domain calls "valuing options".

Pure, deterministic functions over ``Decimal`` — no market prediction, no model licence
needed. These answer the arithmetic a premium seller must know before a structure is
worth defending: what is it worth, where do I break even, what is my worst case, and am I
about to be assigned.

Deliberately arithmetic-only. Nothing here estimates a probability, forecasts a price, or
substitutes for the deterministic risk gate.

Conventions:
  * money and per-share values are ``Decimal``; no floats touch a price
  * ``multiplier`` is the contract multiplier (100 for standard US equity options)
  * a *credit* structure is one that receives premium up front
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Optional

CENT = Decimal("0.01")
STANDARD_MULTIPLIER = Decimal("100")


def money(value: Decimal) -> Decimal:
    """Quantise a monetary value to cents, half-up (banker's rounding would surprise a trader)."""
    return Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)


class OptionType(str, Enum):
    CALL = "CALL"
    PUT = "PUT"


class Moneyness(str, Enum):
    IN_THE_MONEY = "ITM"
    AT_THE_MONEY = "ATM"
    OUT_OF_THE_MONEY = "OTM"


def intrinsic_value(option_type: OptionType | str, strike: Decimal, underlying: Decimal) -> Decimal:
    """Value if exercised right now. Never negative."""
    kind = OptionType(option_type)
    strike, underlying = Decimal(strike), Decimal(underlying)
    if kind is OptionType.CALL:
        return money(max(Decimal("0"), underlying - strike))
    return money(max(Decimal("0"), strike - underlying))


def extrinsic_value(premium: Decimal, intrinsic: Decimal) -> Decimal:
    """The part of the premium that is time and volatility, never negative.

    A premium below intrinsic is a data error (or a crossed quote), not a negative
    time value, so it clamps at zero rather than reporting nonsense.
    """
    return money(max(Decimal("0"), Decimal(premium) - Decimal(intrinsic)))


def moneyness(
    option_type: OptionType | str,
    strike: Decimal,
    underlying: Decimal,
    tolerance: Decimal = Decimal("0.01"),
) -> Moneyness:
    """ITM / ATM / OTM, with an explicit tolerance band for 'at the money'."""
    strike, underlying, tolerance = Decimal(strike), Decimal(underlying), Decimal(tolerance)
    if abs(underlying - strike) <= tolerance:
        return Moneyness.AT_THE_MONEY
    itm = (underlying > strike) if OptionType(option_type) is OptionType.CALL else (underlying < strike)
    return Moneyness.IN_THE_MONEY if itm else Moneyness.OUT_OF_THE_MONEY


# ---------------------------------------------------------------- breakevens


def short_put_breakeven(strike: Decimal, premium: Decimal) -> Decimal:
    """A short put profits above (strike - premium). Under it, the seller is losing."""
    return money(Decimal(strike) - Decimal(premium))


def short_call_breakeven(strike: Decimal, premium: Decimal) -> Decimal:
    """A short call profits below (strike + premium)."""
    return money(Decimal(strike) + Decimal(premium))


def credit_spread_breakeven(
    short_strike: Decimal, net_credit: Decimal, option_type: OptionType | str = OptionType.PUT
) -> Decimal:
    """Breakeven of a short vertical credit spread, expressed on the underlying.

    For a put-side credit spread the seller keeps the credit until the underlying falls
    to (short strike - credit); for a call-side spread it is (short strike + credit).
    """
    kind = OptionType(option_type)
    if kind is OptionType.PUT:
        return money(Decimal(short_strike) - Decimal(net_credit))
    return money(Decimal(short_strike) + Decimal(net_credit))


# ---------------------------------------------------------------- risk shape


@dataclass(frozen=True)
class SpreadRiskShape:
    """Maximum profit, maximum loss and the capital at risk for a credit spread."""

    net_credit: Decimal
    width: Decimal
    contracts: int
    multiplier: Decimal = STANDARD_MULTIPLIER

    def __post_init__(self) -> None:
        if self.contracts < 1:
            raise ValueError("contracts must be >= 1")
        if self.width <= 0:
            raise ValueError("spread width must be > 0")
        if self.net_credit < 0:
            raise ValueError("a credit structure cannot have a negative credit")

    @property
    def max_profit(self) -> Decimal:
        """The credit received, if the spread expires worthless."""
        return money(self.net_credit * self.multiplier * self.contracts)

    @property
    def max_loss(self) -> Decimal:
        """(width - credit) per share, times multiplier and contracts."""
        return money((self.width - self.net_credit) * self.multiplier * self.contracts)

    @property
    def risk_reward(self) -> Optional[Decimal]:
        """Max profit per unit of max loss. ``None`` when nothing is at risk."""
        if self.max_loss == 0:
            return None
        return (self.max_profit / self.max_loss).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


# ---------------------------------------------------------------- assignment


@dataclass(frozen=True)
class AssignmentRisk:
    """Whether a short option is exposed to assignment, and how urgently."""

    option_type: OptionType
    strike: Decimal
    underlying: Decimal
    days_to_expiry: int
    dividend_pending: bool = False

    @property
    def in_the_money(self) -> bool:
        return self.intrinsic() > 0

    def intrinsic(self) -> Decimal:
        return intrinsic_value(self.option_type, self.strike, self.underlying)

    @property
    def assignment_likely(self) -> bool:
        """A short option that finishes in the money is exposed to assignment. This is a
        flag, not a probability: a pending dividend on an ITM short call raises the odds
        and is reported through reason_codes rather than as a second boolean."""
        if self.days_to_expiry < 0:
            raise ValueError("days_to_expiry cannot be negative")
        return self.intrinsic() > 0

    @property
    def pin_risk(self) -> bool:
        """At or very near the strike with little time left: the ugly zone where
        assignment is decided by pennies after the close."""
        if self.days_to_expiry > 1:
            return False
        return abs(Decimal(self.underlying) - Decimal(self.strike)) <= Decimal("0.25")

    def reason_codes(self) -> list[str]:
        codes: list[str] = []
        if self.intrinsic() > 0:
            codes.append("SHORT_OPTION_IN_THE_MONEY")
        if self.option_type is OptionType.CALL and self.dividend_pending and self.intrinsic() > 0:
            codes.append("DIVIDEND_ASSIGNMENT_RISK")
        if self.pin_risk:
            codes.append("PIN_RISK_NEAR_STRIKE")
        if not codes:
            codes.append("NO_ASSIGNMENT_FLAG")
        return codes


__all__ = [
    "AssignmentRisk",
    "Moneyness",
    "OptionType",
    "SpreadRiskShape",
    "credit_spread_breakeven",
    "extrinsic_value",
    "intrinsic_value",
    "money",
    "moneyness",
    "short_call_breakeven",
    "short_put_breakeven",
]
