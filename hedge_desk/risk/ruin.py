"""Conservative MVP risk-of-ruin approximation and hard blockers."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, localcontext
from typing import List, Tuple

from hedge_desk.domain import Account, TradeCandidate


RISK_MODEL_ID = "finite-capital-ruin-approximation"
RISK_MODEL_VERSION = "0.1.0-unvalidated"


@dataclass(frozen=True)
class RiskPolicy:
    maximum_risk_of_ruin: Decimal = Decimal("0.04")
    maximum_quote_age_seconds: int = 900
    minimum_daily_dollar_volume: Decimal = Decimal("1000000")
    maximum_single_trade_loss_fraction: Decimal = Decimal("0.01")
    assumed_loss_sequence: int = 20
    required_risk_model_id: str = RISK_MODEL_ID
    required_risk_model_version: str = RISK_MODEL_VERSION
    permitted_validator_ids: Tuple[str, ...] = (
        "classic-vv-fixture-validator",
        "classic-vv-test-validator",
    )

    def __post_init__(self) -> None:
        decimal_limits = (
            self.maximum_risk_of_ruin,
            self.minimum_daily_dollar_volume,
            self.maximum_single_trade_loss_fraction,
        )
        if any(
            not isinstance(value, Decimal) or not value.is_finite()
            for value in decimal_limits
        ):
            raise ValueError("risk policy decimal limits must be finite Decimals")
        if not Decimal("0") <= self.maximum_risk_of_ruin <= Decimal("1"):
            raise ValueError("maximum risk of ruin must be between zero and one")
        if self.minimum_daily_dollar_volume < 0:
            raise ValueError("minimum liquidity cannot be negative")
        if not Decimal("0") < self.maximum_single_trade_loss_fraction <= Decimal("1"):
            raise ValueError("single-trade loss fraction must be in (0, 1]")
        if (
            type(self.maximum_quote_age_seconds) is not int
            or self.maximum_quote_age_seconds < 0
            or type(self.assumed_loss_sequence) is not int
            or self.assumed_loss_sequence <= 0
        ):
            raise ValueError("risk policy integer limits invalid")
        if not self.required_risk_model_id or not self.required_risk_model_version:
            raise ValueError("required risk model identity is missing")
        if (
            not self.permitted_validator_ids
            or any(not isinstance(value, str) or not value for value in self.permitted_validator_ids)
            or len(self.permitted_validator_ids) != len(set(self.permitted_validator_ids))
        ):
            raise ValueError("risk validator allowlist invalid")


def estimate_risk_of_ruin(
    account_equity: Decimal,
    max_loss: Decimal,
    win_probability: Decimal,
    expected_win: Decimal,
) -> Decimal:
    """Estimate ruin probability for repeated equal-risk trials.

    This finite-capital approximation is deliberately conservative and is an
    MVP control—not a validated prediction. Non-positive expectancy returns
    certainty of ruin. Independent model validation is required before any
    live-capital use.
    """
    if max_loss <= 0 or account_equity <= 0:
        return Decimal("1")

    loss_probability = Decimal("1") - win_probability
    expectancy = win_probability * expected_win - loss_probability * max_loss
    if expectancy <= 0:
        return Decimal("1")

    capital_units = int(account_equity / max_loss)
    if capital_units <= 0:
        return Decimal("1")

    payoff_adjusted_win = (
        win_probability * expected_win
        / (win_probability * expected_win + loss_probability * max_loss)
    )
    if payoff_adjusted_win <= Decimal("0.5"):
        return Decimal("1")

    with localcontext() as context:
        context.prec = 40
        odds = (Decimal("1") - payoff_adjusted_win) / payoff_adjusted_win
        estimate = odds ** capital_units
    return min(Decimal("1"), max(Decimal("0"), estimate))


def risk_gate(
    account: Account,
    candidate: TradeCandidate,
    evaluated_at: datetime,
    policy: RiskPolicy,
    validated_risk_of_ruin_after: Decimal,
) -> List[str]:
    """Return hard blockers while consuming, never calculating, authoritative RoR."""
    reasons: List[str] = []
    age_seconds = (evaluated_at - candidate.quote_timestamp).total_seconds()

    if candidate.max_loss <= 0:
        reasons.append("MAX_LOSS_UNDEFINED")
    if age_seconds < 0:
        reasons.append("QUOTE_FROM_FUTURE")
    elif age_seconds > policy.maximum_quote_age_seconds:
        reasons.append("STALE_QUOTE")
    if candidate.average_daily_dollar_volume < policy.minimum_daily_dollar_volume:
        reasons.append("INSUFFICIENT_LIQUIDITY")
    if candidate.max_loss / account.equity > policy.maximum_single_trade_loss_fraction:
        reasons.append("SINGLE_TRADE_LOSS_LIMIT")

    if validated_risk_of_ruin_after > policy.maximum_risk_of_ruin:
        reasons.append("RISK_OF_RUIN_LIMIT")

    return sorted(set(reasons))
