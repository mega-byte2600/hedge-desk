"""Enforced stop-loss rules: deterministic, outside any model (ADR-0008).

GP decisions 2026-11-20:
- Every paper position carries a stop, and the stop is ENFORCED: when it
  triggers, the paper runner closes the position by itself, in every mode.
- Undefined-risk structures (naked options, futures) are allowed only with an
  explicit stop sized so the stop-defined loss fits the immutable 2% cap
  (SOUL.md order 7). A stop is not a guaranteed loss limit: price can gap
  through it overnight or in a halt, so those positions always carry
  ``GAP_RISK_NOT_GUARANTEED``.

Agents never set or change these numbers. No Risk of Ruin is computed here.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Tuple

from hedge_desk.risk.limits import SOUL_MAX_LOSS_FRACTION_EQUITY

STOP_LOSS_POLICY_VERSION = "enforced-stop-loss-1.0.0"

BASIS_DEFINED_RISK = "DEFINED_RISK"
BASIS_STOP_DEFINED = "STOP_DEFINED"

GAP_RISK_NOT_GUARANTEED = "GAP_RISK_NOT_GUARANTEED"
EQUITY_UNCONFIGURED = "EQUITY_UNCONFIGURED"


def _finite_positive(value: object) -> bool:
    return isinstance(value, Decimal) and value.is_finite() and value > 0


@dataclass(frozen=True)
class StopLossPolicy:
    # Matches PremiumExitPolicy.maximum_loss_fraction: stop at 50% of max loss.
    stop_fraction_of_max_loss: Decimal = Decimal("0.50")
    version: str = STOP_LOSS_POLICY_VERSION

    def __post_init__(self) -> None:
        value = self.stop_fraction_of_max_loss
        if not isinstance(value, Decimal) or not value.is_finite():
            raise ValueError("stop fraction must be a finite Decimal")
        if not Decimal("0") < value <= Decimal("1"):
            raise ValueError("stop fraction must be in (0, 1]")


@dataclass(frozen=True)
class StopRule:
    """The loss, in dollars, at which a paper position is force-closed."""

    trigger_loss: Decimal
    basis: str
    flags: Tuple[str, ...]
    policy_version: str

    def to_dict(self) -> dict:
        return {
            "trigger_loss": str(self.trigger_loss),
            "basis": self.basis,
            "flags": list(self.flags),
            "policy_version": self.policy_version,
        }


def defined_risk_stop_rule(
    maximum_loss: Decimal,
    account_equity: Optional[Decimal],
    policy: StopLossPolicy = StopLossPolicy(),
) -> StopRule:
    """Stop for a defined-risk structure: the lower of the policy fraction of
    max loss and 2% of equity. Without configured equity, the fraction alone
    applies and the rule says so (``EQUITY_UNCONFIGURED``)."""
    if not _finite_positive(maximum_loss):
        raise ValueError("maximum loss must be a positive finite Decimal")
    trigger = (maximum_loss * policy.stop_fraction_of_max_loss).quantize(Decimal("0.01"))
    flags = []
    if account_equity is None:
        flags.append(EQUITY_UNCONFIGURED)
    else:
        if not _finite_positive(account_equity):
            raise ValueError("account equity must be a positive finite Decimal")
        cap = (account_equity * SOUL_MAX_LOSS_FRACTION_EQUITY).quantize(Decimal("0.01"))
        trigger = min(trigger, cap)
    return StopRule(trigger, BASIS_DEFINED_RISK, tuple(sorted(flags)), policy.version)


def stop_defined_rule(
    stop_loss_amount: Optional[Decimal],
    account_equity: Optional[Decimal],
) -> Tuple[Optional[StopRule], Tuple[str, ...]]:
    """Validate a stop for an undefined-risk structure (C5).

    Returns ``(rule, blocking_reasons)``. A rule is returned only when there
    are no blocking reasons. Equity is required: without it the 2% cap
    cannot be checked, so the structure fails closed.
    """
    reasons = []
    if stop_loss_amount is None:
        reasons.append("STOP_LOSS_REQUIRED")
    elif not _finite_positive(stop_loss_amount):
        reasons.append("STOP_LOSS_INVALID")
    if account_equity is None:
        reasons.append("EQUITY_REQUIRED_FOR_STOP_DEFINED_RISK")
    elif not _finite_positive(account_equity):
        reasons.append("EQUITY_INVALID")
    if not reasons and stop_loss_amount > account_equity * SOUL_MAX_LOSS_FRACTION_EQUITY:
        reasons.append("STOP_LOSS_EXCEEDS_2PCT_EQUITY")
    if reasons:
        return None, tuple(sorted(reasons))
    rule = StopRule(
        stop_loss_amount.quantize(Decimal("0.01")),
        BASIS_STOP_DEFINED,
        (GAP_RISK_NOT_GUARANTEED,),
        STOP_LOSS_POLICY_VERSION,
    )
    return rule, ()


def stop_triggered(marked_pnl: Decimal, rule: StopRule) -> bool:
    """True when the marked loss has reached the stop (loss >= trigger)."""
    if not isinstance(marked_pnl, Decimal) or not marked_pnl.is_finite():
        raise ValueError("marked P&L must be a finite Decimal")
    return -marked_pnl >= rule.trigger_loss
