"""Collateral and margin requirements per option strategy.

The domain treats collateral and margin for option structures as basic material, and the
product claims "defined risk" without ever encoding what the broker will actually hold.
This closes that: given a structure, what capital is locked, and on what basis.

Numbers live in ``MarginPolicy`` as versioned data rather than as constants scattered
through the code, so a policy change is a reviewable record rather than a silent edit.
Reg T-style factors are labelled as the conventional baseline they are — this is a
research requirement model, not a broker's margin calculation and not a compliance claim.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Optional

from hedge_desk.options.valuation import STANDARD_MULTIPLIER, money


class Strategy(str, Enum):
    CASH_SECURED_PUT = "CASH_SECURED_PUT"
    COVERED_CALL = "COVERED_CALL"
    CREDIT_SPREAD = "CREDIT_SPREAD"


@dataclass(frozen=True)
class MarginPolicy:
    """Versioned requirement assumptions.

    ``version`` is required because a requirement is only reproducible if the policy that
    produced it is identifiable — the same reason the risk engine carries reason codes.
    """

    version: str
    multiplier: Decimal = STANDARD_MULTIPLIER
    # A cash-secured put conventionally holds the strike, less the credit received.
    put_credit_offsets_collateral: bool = True
    # A vertical credit spread holds the spread width, less the net credit.
    spread_credit_offsets_margin: bool = True
    # Conventional Reg T-style maintenance on the short-leg requirement.
    maintenance_factor: Decimal = Decimal("1.00")

    def __post_init__(self) -> None:
        if not self.version:
            raise ValueError("a margin policy must be versioned")
        if self.maintenance_factor <= 0:
            raise ValueError("maintenance_factor must be > 0")


DEFAULT_POLICY = MarginPolicy(version="regt-baseline-1")


@dataclass(frozen=True)
class Requirement:
    """What a structure locks up, with the basis and reason codes for review."""

    strategy: Strategy
    requirement: Decimal
    policy_version: str
    basis: str
    reason_codes: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.requirement < 0:
            raise ValueError("a requirement cannot be negative")


def _contracts(contracts: int) -> int:
    if contracts < 1:
        raise ValueError("contracts must be >= 1")
    return contracts


def cash_secured_put_collateral(
    strike: Decimal,
    net_credit: Decimal = Decimal("0"),
    contracts: int = 1,
    policy: MarginPolicy = DEFAULT_POLICY,
) -> Requirement:
    """Cash held against a short put: the strike per share, less the credit if the policy allows.

    This is the requirement that makes a put "cash secured": assignment must be fundable.
    """
    strike, net_credit = Decimal(strike), Decimal(net_credit)
    if strike <= 0:
        raise ValueError("strike must be > 0")
    contracts = _contracts(contracts)
    gross = strike * policy.multiplier * contracts
    offset = (net_credit * policy.multiplier * contracts) if policy.put_credit_offsets_collateral else Decimal("0")
    requirement = money(gross - offset)
    codes = ["COLLATERAL_CASH_SECURED", "ASSIGNMENT_MUST_BE_FUNDABLE"]
    if policy.put_credit_offsets_collateral and offset > 0:
        codes.append("CREDIT_OFFSETS_COLLATERAL")
    return Requirement(
        strategy=Strategy.CASH_SECURED_PUT,
        requirement=requirement,
        policy_version=policy.version,
        basis=f"strike {strike} x {policy.multiplier} x {contracts} - credit offset {money(offset)}",
        reason_codes=codes,
    )


def covered_call_requirement(
    share_price: Decimal,
    contracts: int = 1,
    policy: MarginPolicy = DEFAULT_POLICY,
) -> Requirement:
    """A covered call's requirement is the shares themselves: 100 per contract.

    Reported as the capital represented by those shares, because that is what is actually
    committed. The shares are the collateral; the call premium is income, not margin.
    """
    share_price = Decimal(share_price)
    if share_price <= 0:
        raise ValueError("share_price must be > 0")
    contracts = _contracts(contracts)
    requirement = money(share_price * policy.multiplier * contracts)
    return Requirement(
        strategy=Strategy.COVERED_CALL,
        requirement=requirement,
        policy_version=policy.version,
        basis=f"{contracts} contract(s) x {policy.multiplier} shares x {share_price}",
        reason_codes=["SHARES_ARE_COLLATERAL", "UPSIDE_CAPPED_AT_STRIKE"],
    )


def credit_spread_margin(
    width: Decimal,
    net_credit: Decimal,
    contracts: int = 1,
    policy: MarginPolicy = DEFAULT_POLICY,
) -> Requirement:
    """Margin for a vertical credit spread: the width, less the credit.

    This equals the structure's maximum loss, which is the point of a defined-risk spread:
    the capital at risk is bounded and knowable before entry.
    """
    width, net_credit = Decimal(width), Decimal(net_credit)
    if width <= 0:
        raise ValueError("width must be > 0")
    if net_credit < 0:
        raise ValueError("net credit cannot be negative")
    if net_credit >= width:
        raise ValueError("a credit at or above the width is a pricing error, not a structure")
    contracts = _contracts(contracts)
    gross = width * policy.multiplier * contracts
    offset = (net_credit * policy.multiplier * contracts) if policy.spread_credit_offsets_margin else Decimal("0")
    requirement = money((gross - offset) * policy.maintenance_factor)
    codes = ["DEFINED_RISK", "MARGIN_EQUALS_MAX_LOSS"]
    if offset > 0:
        codes.append("CREDIT_OFFSETS_MARGIN")
    return Requirement(
        strategy=Strategy.CREDIT_SPREAD,
        requirement=requirement,
        policy_version=policy.version,
        basis=f"(width {width} - credit {net_credit}) x {policy.multiplier} x {contracts}"
              f" x maintenance {policy.maintenance_factor}",
        reason_codes=codes,
    )


def requirement_for(strategy: Strategy | str, **kwargs) -> Requirement:
    """Single entry point, so callers cannot invent a strategy's requirement inline."""
    kind = Strategy(strategy)
    if kind is Strategy.CASH_SECURED_PUT:
        return cash_secured_put_collateral(**kwargs)
    if kind is Strategy.COVERED_CALL:
        return covered_call_requirement(**kwargs)
    return credit_spread_margin(**kwargs)


__all__ = [
    "DEFAULT_POLICY",
    "MarginPolicy",
    "Requirement",
    "Strategy",
    "cash_secured_put_collateral",
    "covered_call_requirement",
    "credit_spread_margin",
    "requirement_for",
]
