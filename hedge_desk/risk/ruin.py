"""Conservative MVP risk-of-ruin approximation and hard blockers."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, localcontext
from typing import List

from hedge_desk.domain import Account, TradeCandidate


@dataclass(frozen=True)
class RiskPolicy:
    maximum_risk_of_ruin: Decimal = Decimal("0.04")
    maximum_quote_age_seconds: int = 900
    minimum_daily_dollar_volume: Decimal = Decimal("1000000")
    maximum_single_trade_loss_fraction: Decimal = Decimal("0.01")
    assumed_loss_sequence: int = 20


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
) -> List[str]:
    """Return hard risk blockers for a proposed paper trade."""
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

    ruin_after = estimate_risk_of_ruin(
        account.equity,
        candidate.max_loss,
        candidate.win_probability,
        candidate.expected_win,
    )
    if ruin_after > policy.maximum_risk_of_ruin:
        reasons.append("RISK_OF_RUIN_LIMIT")

    return sorted(set(reasons))

