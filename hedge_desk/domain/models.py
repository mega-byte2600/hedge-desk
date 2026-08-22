"""Typed records forming the auditable Hedge Desk decision contract."""

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Optional, Tuple


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


def _finite_decimal(value: object) -> bool:
    return isinstance(value, Decimal) and value.is_finite()


def _valid_sha256(value: object) -> bool:
    try:
        return isinstance(value, str) and len(value) == 64 and int(value, 16) > 0
    except ValueError:
        return False


@dataclass(frozen=True)
class Account:
    account_id: str
    account_type: AccountType
    equity: Decimal
    cash: Decimal
    options_approved: bool = False
    futures_approved: bool = False
    options_disclosure_version: Optional[str] = None
    options_disclosure_acknowledged_at: Optional[datetime] = None
    broker_options_policy_version: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.account_id:
            raise ValueError("account identity is required")
        if not _finite_decimal(self.equity) or not _finite_decimal(self.cash):
            raise ValueError("account money values must be finite Decimals")
        if self.equity <= 0:
            raise ValueError("account equity must be positive")
        if self.cash < 0:
            raise ValueError("account cash cannot be negative")
        if type(self.options_approved) is not bool or type(self.futures_approved) is not bool:
            raise ValueError("account approval flags must be boolean")
        if (
            self.options_disclosure_acknowledged_at is not None
            and self.options_disclosure_acknowledged_at.tzinfo is None
        ):
            raise ValueError("options disclosure acknowledgement must be timezone-aware")


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
        if type(self.quantity) is not int or self.quantity <= 0:
            raise ValueError("quantity must be a positive integer")
        decimal_values = (
            self.entry_price,
            self.max_loss,
            self.expected_win,
            self.win_probability,
            self.average_daily_dollar_volume,
        )
        if any(not _finite_decimal(value) for value in decimal_values):
            raise ValueError("candidate numeric values must be finite Decimals")
        if self.entry_price <= 0:
            raise ValueError("quantity and entry price must be positive")
        if self.max_loss < 0 or self.expected_win < 0:
            raise ValueError("loss and win amounts cannot be negative")
        if not Decimal("0") <= self.win_probability <= Decimal("1"):
            raise ValueError("win probability must be between zero and one")
        if self.average_daily_dollar_volume < 0:
            raise ValueError("daily dollar volume cannot be negative")
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
    risk_source_artifact_sha256: str
    portfolio_snapshot_sha256: str

    def __post_init__(self) -> None:
        if self.evaluated_at.tzinfo is None:
            raise ValueError("decision timestamp must be timezone-aware")
        if not self.risk_model_id or not self.risk_model_version:
            raise ValueError("risk model identity and version are required")
        if not (
            _finite_decimal(self.risk_of_ruin_before)
            and _finite_decimal(self.risk_of_ruin_after)
            and Decimal("0") <= self.risk_of_ruin_before <= Decimal("1")
            and Decimal("0") <= self.risk_of_ruin_after <= Decimal("1")
        ):
            raise ValueError("decision RoR values must be finite and between zero and one")
        if not _valid_sha256(self.risk_input_sha256):
            raise ValueError("risk input artifact hash is required")
        if not _valid_sha256(self.risk_source_artifact_sha256):
            raise ValueError("risk source artifact hash is required")
        if not _valid_sha256(self.portfolio_snapshot_sha256):
            raise ValueError("risk portfolio snapshot hash is required")
        if self.reason_codes != tuple(sorted(set(self.reason_codes))):
            raise ValueError("decision reason codes must be unique and sorted")
        if self.status is DecisionStatus.BLOCKED and not self.reason_codes:
            raise ValueError("blocked decisions require reason codes")


def utc_now() -> datetime:
    """Return a timezone-aware timestamp; callers inject clocks in tests."""
    return datetime.now(timezone.utc)
