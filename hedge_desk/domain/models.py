"""Typed records forming the auditable Hedge Desk decision contract."""

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Tuple


class AccountType(str, Enum):
    INDIVIDUAL = "individual"
    TRADITIONAL_IRA = "traditional_ira"
    ROTH_IRA = "roth_ira"
    TRUST = "trust"


class ProductType(str, Enum):
    EQUITY = "equity"
    DEFINED_RISK_OPTION = "defined_risk_option"
    UNDEFINED_RISK_OPTION = "undefined_risk_option"
    FUTURE = "future"


class DecisionStatus(str, Enum):
    RISK_PASS = "risk_pass"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class Account:
    account_id: str
    account_type: AccountType
    equity: Decimal
    cash: Decimal
    options_approved: bool = False
    futures_approved: bool = False

    def __post_init__(self) -> None:
        if self.equity <= 0:
            raise ValueError("account equity must be positive")
        if self.cash < 0:
            raise ValueError("account cash cannot be negative")


@dataclass(frozen=True)
class TradeCandidate:
    candidate_id: str
    symbol: str
    product_type: ProductType
    quantity: int
    entry_price: Decimal
    max_loss: Decimal
    expected_win: Decimal
    win_probability: Decimal
    quote_timestamp: datetime
    average_daily_dollar_volume: Decimal
    thesis: str
    invalidation: str

    def __post_init__(self) -> None:
        if not self.candidate_id or not self.symbol:
            raise ValueError("candidate identity is required")
        if self.quantity <= 0 or self.entry_price <= 0:
            raise ValueError("quantity and entry price must be positive")
        if self.max_loss < 0 or self.expected_win < 0:
            raise ValueError("loss and win amounts cannot be negative")
        if not Decimal("0") <= self.win_probability <= Decimal("1"):
            raise ValueError("win probability must be between zero and one")
        if self.quote_timestamp.tzinfo is None:
            raise ValueError("quote timestamp must be timezone-aware")
        if not self.thesis.strip() or not self.invalidation.strip():
            raise ValueError("thesis and invalidation are required")


@dataclass(frozen=True)
class Decision:
    candidate_id: str
    account_id: str
    status: DecisionStatus
    reason_codes: Tuple[str, ...]
    risk_of_ruin_before: Decimal
    risk_of_ruin_after: Decimal
    evaluated_at: datetime
    risk_model_id: str
    risk_model_version: str
    risk_input_sha256: str

    def __post_init__(self) -> None:
        if self.evaluated_at.tzinfo is None:
            raise ValueError("decision timestamp must be timezone-aware")
        if not self.risk_model_id or not self.risk_model_version:
            raise ValueError("risk model identity and version are required")
        if len(self.risk_input_sha256) != 64:
            raise ValueError("risk input artifact hash is required")
        if self.status is DecisionStatus.BLOCKED and not self.reason_codes:
            raise ValueError("blocked decisions require reason codes")


def utc_now() -> datetime:
    """Return a timezone-aware timestamp; callers inject clocks in tests."""
    return datetime.now(timezone.utc)
