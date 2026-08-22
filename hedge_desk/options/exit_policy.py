"""Executable paper exit monitoring for defined-risk credit spreads."""

import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from hashlib import sha256
from typing import Tuple

from .spreads import OptionQuote, VerticalSpreadCalculation


EXIT_POLICY_VERSION = "premium-exit-monitor-1.0.0"


@dataclass(frozen=True)
class PremiumExitPolicy:
    profit_capture_fraction: Decimal = Decimal("0.50")
    maximum_loss_fraction: Decimal = Decimal("0.50")
    maximum_quote_age_seconds: int = 120
    quote_tolerance_seconds: int = 2

    def __post_init__(self) -> None:
        for value in (self.profit_capture_fraction, self.maximum_loss_fraction):
            if not isinstance(value, Decimal) or not value.is_finite():
                raise ValueError("exit fractions must be finite Decimals")
            if not Decimal("0") < value <= Decimal("1"):
                raise ValueError("exit fractions must be in (0, 1]")
        if (
            type(self.maximum_quote_age_seconds) is not int
            or self.maximum_quote_age_seconds < 0
            or type(self.quote_tolerance_seconds) is not int
            or self.quote_tolerance_seconds < 0
        ):
            raise ValueError("exit quote timing limits invalid")


@dataclass(frozen=True)
class PremiumExitEvaluation:
    spread_id: str
    evaluated_at: datetime
    action: str
    reason_codes: Tuple[str, ...]
    executable_close_debit: Decimal
    close_commission: Decimal
    marked_pnl: Decimal
    profit_capture_fraction: Decimal
    loss_fraction_of_maximum: Decimal
    days_to_expiration: int
    policy_version: str
    artifact_sha256: str
    trade_authorized: bool = False


def evaluate_premium_exit(
    opened_spread: VerticalSpreadCalculation,
    current_short_quote: OptionQuote,
    current_long_quote: OptionQuote,
    evaluated_at: datetime,
    close_commission_per_contract: Decimal,
    event_escalation_required: bool = False,
    policy: PremiumExitPolicy = PremiumExitPolicy(),
) -> PremiumExitEvaluation:
    """Mark an executable close and choose a human-review action."""
    if evaluated_at.tzinfo is None:
        raise ValueError("exit evaluation timestamp must be timezone-aware")
    if (
        not isinstance(close_commission_per_contract, Decimal)
        or not close_commission_per_contract.is_finite()
        or close_commission_per_contract < 0
    ):
        raise ValueError("close commission must be a finite nonnegative Decimal")
    if type(event_escalation_required) is not bool:
        raise ValueError("event escalation flag must be boolean")
    expected_contracts = opened_spread.input_contract_ids
    if (
        current_short_quote.contract_id != expected_contracts[0]
        or current_long_quote.contract_id != expected_contracts[1]
    ):
        raise ValueError("exit quotes do not match opened contracts")
    if (
        current_short_quote.underlying != current_long_quote.underlying
        or current_short_quote.option_type is not current_long_quote.option_type
        or current_short_quote.expiration != current_long_quote.expiration
        or current_short_quote.source_id != current_long_quote.source_id
    ):
        raise ValueError("exit quote legs are incompatible")
    if current_short_quote.underlying != opened_spread.underlying:
        raise ValueError("exit underlying does not match opened spread")
    if current_short_quote.source_id != opened_spread.quote_source_id:
        raise ValueError("exit quote source does not match opened spread")
    if current_short_quote.expiration != opened_spread.expiration_date:
        raise ValueError("exit expiration does not match opened spread")
    quote_times = (current_short_quote.quoted_at, current_long_quote.quoted_at)
    if (max(quote_times) - min(quote_times)).total_seconds() > policy.quote_tolerance_seconds:
        raise ValueError("exit quotes are not timestamp-compatible")
    quote_age = (evaluated_at - max(quote_times)).total_seconds()
    if quote_age < 0:
        raise ValueError("exit quote cannot be from the future")
    if quote_age > policy.maximum_quote_age_seconds:
        raise ValueError("exit quote is stale")

    multiplier = Decimal(opened_spread.contract_multiplier)
    quantity = Decimal(opened_spread.quantity)
    close_debit = (
        current_short_quote.ask - current_long_quote.bid
    ) * multiplier * quantity
    if close_debit < 0:
        raise ValueError("executable close debit cannot be negative")
    close_commission = close_commission_per_contract * Decimal("2") * quantity
    marked_pnl = opened_spread.net_credit - close_debit - close_commission
    capture = marked_pnl / opened_spread.net_credit
    loss_fraction = max(Decimal("0"), -marked_pnl / opened_spread.maximum_loss)
    days_to_expiration = (opened_spread.expiration_date - evaluated_at.date()).days

    reasons = []
    if event_escalation_required:
        reasons.append("EVENT_ESCALATION_REQUIRED")
    if days_to_expiration <= opened_spread.planned_exit_days_before_expiration:
        reasons.append("PLANNED_EXIT_WINDOW_REACHED")
    if capture >= policy.profit_capture_fraction:
        reasons.append("PROFIT_CAPTURE_TARGET_REACHED")
    if loss_fraction >= policy.maximum_loss_fraction:
        reasons.append("LOSS_REVIEW_THRESHOLD_REACHED")
    reason_codes = tuple(sorted(set(reasons)))
    action = "CLOSE_REVIEW_REQUIRED" if reason_codes else "MONITOR"
    payload = {
        "action": action,
        "close_commission": str(close_commission),
        "days_to_expiration": days_to_expiration,
        "evaluated_at": evaluated_at.isoformat(),
        "executable_close_debit": str(close_debit),
        "loss_fraction_of_maximum": str(loss_fraction),
        "marked_pnl": str(marked_pnl),
        "policy": {
            "maximum_loss_fraction": str(policy.maximum_loss_fraction),
            "maximum_quote_age_seconds": policy.maximum_quote_age_seconds,
            "profit_capture_fraction": str(policy.profit_capture_fraction),
            "quote_tolerance_seconds": policy.quote_tolerance_seconds,
            "version": EXIT_POLICY_VERSION,
        },
        "profit_capture_fraction": str(capture),
        "reason_codes": list(reason_codes),
        "spread_id": opened_spread.spread_id,
        "trade_authorized": False,
    }
    artifact_sha256 = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return PremiumExitEvaluation(
        opened_spread.spread_id, evaluated_at, action, reason_codes, close_debit,
        close_commission, marked_pnl, capture, loss_fraction, days_to_expiration,
        EXIT_POLICY_VERSION, artifact_sha256, False,
    )
