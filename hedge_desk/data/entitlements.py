"""Deterministic data-entitlement readiness checks; no vendor payload access."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, Tuple


DATA_STACK_SCHEMA_VERSION = "hedge-desk-data-stack-1.1.0"


@dataclass(frozen=True)
class DataSubscription:
    source_id: str
    monthly_cost: Decimal
    entitlement_id: str
    historical_nbbo_quotes: bool
    expired_option_contracts: bool
    option_chain_snapshots: bool
    corporate_actions: bool
    point_in_time_timestamps: bool
    trades: bool
    open_interest: bool
    historical_years: int
    real_time_nbbo: bool
    commercial_use_allowed: bool
    redistribution_allowed: bool


@dataclass(frozen=True)
class DataReadinessResult:
    ready_for_internal_options_research: bool
    ready_for_live_production_data: bool
    total_monthly_cost: Decimal
    reason_codes: Tuple[str, ...]
    live_production_reason_codes: Tuple[str, ...]
    raw_payload_commit_allowed: bool = False


def evaluate_options_data_stack(
    subscriptions: Tuple[DataSubscription, ...],
    monthly_budget: Decimal,
) -> DataReadinessResult:
    """Require executable historical evidence within budget and fail closed."""
    if not isinstance(monthly_budget, Decimal) or not monthly_budget.is_finite():
        raise ValueError("monthly budget must be a finite Decimal")
    if monthly_budget < 0:
        raise ValueError("monthly budget cannot be negative")
    if not subscriptions:
        return DataReadinessResult(
            False, False, Decimal("0"), ("DATA_SOURCE_ABSENT",),
            ("DATA_SOURCE_ABSENT",),
        )
    identities = [item.source_id for item in subscriptions]
    if (
        any(not isinstance(item, str) or not item for item in identities)
        or len(identities) != len(set(identities))
    ):
        raise ValueError("subscription source identities must be unique and nonempty")
    if any(not isinstance(item.entitlement_id, str) for item in subscriptions):
        raise ValueError("subscription entitlement identities must be strings")
    if any(
        not isinstance(item.monthly_cost, Decimal) or not item.monthly_cost.is_finite()
        for item in subscriptions
    ):
        raise ValueError("subscription costs must be finite Decimals")
    reasons = []
    total = sum((item.monthly_cost for item in subscriptions), Decimal("0"))
    if any(item.monthly_cost < 0 for item in subscriptions):
        reasons.append("SUBSCRIPTION_COST_INVALID")
    if total > monthly_budget:
        reasons.append("MONTHLY_DATA_BUDGET_EXCEEDED")
    if any(not item.entitlement_id for item in subscriptions):
        reasons.append("DATA_ENTITLEMENT_UNVERIFIED")
    required_capabilities = {
        "HISTORICAL_NBBO_QUOTES_ABSENT": any(
            item.historical_nbbo_quotes for item in subscriptions
        ),
        "EXPIRED_OPTION_CONTRACTS_ABSENT": any(
            item.expired_option_contracts for item in subscriptions
        ),
        "OPTION_CHAIN_SNAPSHOTS_ABSENT": any(
            item.option_chain_snapshots for item in subscriptions
        ),
        "CORPORATE_ACTIONS_ABSENT": any(
            item.corporate_actions for item in subscriptions
        ),
        "POINT_IN_TIME_TIMESTAMPS_ABSENT": any(
            item.point_in_time_timestamps for item in subscriptions
        ),
        "OPTION_TRADES_ABSENT": any(item.trades for item in subscriptions),
        "OPEN_INTEREST_ABSENT": any(item.open_interest for item in subscriptions),
        "MINIMUM_HISTORY_DEPTH_ABSENT": any(
            item.historical_years >= 5 for item in subscriptions
        ),
    }
    reasons.extend(
        reason for reason, present in required_capabilities.items() if not present
    )
    reason_codes = tuple(sorted(set(reasons)))
    production_reasons = list(reason_codes)
    if not any(item.real_time_nbbo for item in subscriptions):
        production_reasons.append("REAL_TIME_NBBO_ABSENT")
    if not any(item.commercial_use_allowed for item in subscriptions):
        production_reasons.append("COMMERCIAL_USE_PERMISSION_ABSENT")
    production_reason_codes = tuple(sorted(set(production_reasons)))
    return DataReadinessResult(
        not reason_codes,
        not production_reason_codes,
        total,
        reason_codes,
        production_reason_codes,
        False,
    )


def parse_data_stack_manifest(payload: Dict[str, Any]) -> Tuple[Decimal, Tuple[DataSubscription, ...]]:
    expected = {"schema_version", "monthly_budget", "subscriptions"}
    if set(payload) != expected or payload.get("schema_version") != DATA_STACK_SCHEMA_VERSION:
        raise ValueError("data stack manifest schema invalid")
    if not isinstance(payload["monthly_budget"], str):
        raise ValueError("monthly budget must be an exact decimal string")
    rows = payload["subscriptions"]
    if not isinstance(rows, list):
        raise ValueError("subscriptions must be a list")
    fields = {
        "source_id", "monthly_cost", "entitlement_id", "historical_nbbo_quotes",
        "expired_option_contracts", "option_chain_snapshots", "corporate_actions",
        "point_in_time_timestamps", "trades", "open_interest", "historical_years",
        "real_time_nbbo", "commercial_use_allowed",
        "redistribution_allowed",
    }
    subscriptions = []
    for row in rows:
        if not isinstance(row, dict) or set(row) != fields:
            raise ValueError("subscription schema invalid")
        if not isinstance(row["monthly_cost"], str):
            raise ValueError("subscription cost must be an exact decimal string")
        bool_fields = fields - {
            "source_id", "monthly_cost", "entitlement_id", "historical_years"
        }
        if any(type(row[field]) is not bool for field in bool_fields):
            raise ValueError("subscription capabilities must be boolean")
        if type(row["historical_years"]) is not int or row["historical_years"] < 0:
            raise ValueError("subscription historical years must be a nonnegative integer")
        if not isinstance(row["source_id"], str) or not isinstance(
            row["entitlement_id"], str
        ):
            raise ValueError("subscription identities must be strings")
        try:
            monthly_cost = Decimal(row["monthly_cost"])
        except ArithmeticError as exc:
            raise ValueError("subscription cost decimal invalid") from exc
        if not monthly_cost.is_finite():
            raise ValueError("subscription cost decimal must be finite")
        subscriptions.append(
            DataSubscription(
                row["source_id"], monthly_cost, row["entitlement_id"],
                row["historical_nbbo_quotes"], row["expired_option_contracts"],
                row["option_chain_snapshots"], row["corporate_actions"],
                row["point_in_time_timestamps"], row["trades"],
                row["open_interest"], row["historical_years"],
                row["real_time_nbbo"], row["commercial_use_allowed"],
                row["redistribution_allowed"],
            )
        )
    try:
        budget = Decimal(payload["monthly_budget"])
    except ArithmeticError as exc:
        raise ValueError("monthly budget decimal invalid") from exc
    if not budget.is_finite():
        raise ValueError("monthly budget decimal must be finite")
    return budget, tuple(subscriptions)
