"""Point-in-time ten-year dividend and shareholder-payout research metrics."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, Tuple


@dataclass(frozen=True)
class AnnualPayoutObservation:
    fiscal_year: int
    dividends_per_share: Decimal
    earnings_per_share: Decimal
    average_share_price: Decimal
    buybacks: Decimal
    issuance: Decimal
    market_cap: Decimal
    available_at: datetime
    source_artifact_sha256: str


@dataclass(frozen=True)
class DividendResearchResult:
    admissible: bool
    reason_codes: Tuple[str, ...]
    ten_year_average_dividend_yield: Optional[Decimal]
    ten_year_average_payout_ratio: Optional[Decimal]
    ten_year_average_net_shareholder_yield: Optional[Decimal]
    dividend_cut_count: int
    long_call_cash_dividend_entitlement: Decimal = Decimal("0")
    trade_authorized: bool = False


def _valid_hash(value: str) -> bool:
    try:
        return len(value) == 64 and int(value, 16) >= 0
    except ValueError:
        return False


def evaluate_dividend_history(
    observations: Tuple[AnnualPayoutObservation, ...],
    decision_time: datetime,
) -> DividendResearchResult:
    if decision_time.tzinfo is None:
        raise ValueError("decision timestamp must be timezone-aware")
    reasons = []
    if len(observations) != 10:
        reasons.append("TEN_YEAR_HISTORY_REQUIRED")
    years = sorted(item.fiscal_year for item in observations)
    if years and years != list(range(years[0], years[0] + len(years))):
        reasons.append("FISCAL_YEAR_HISTORY_NOT_CONSECUTIVE")
    if len(years) != len(set(years)):
        reasons.append("DUPLICATE_FISCAL_YEAR")
    if any(item.available_at.tzinfo is None for item in observations):
        reasons.append("PAYOUT_TIMESTAMP_NOT_TIMEZONE_AWARE")
    elif any(item.available_at > decision_time for item in observations):
        reasons.append("PAYOUT_LOOKAHEAD_VIOLATION")
    if any(not _valid_hash(item.source_artifact_sha256) for item in observations):
        reasons.append("PAYOUT_SOURCE_HASH_INVALID")
    if any(
        item.dividends_per_share < 0
        or item.average_share_price <= 0
        or item.market_cap <= 0
        or item.buybacks < 0
        or item.issuance < 0
        for item in observations
    ):
        reasons.append("PAYOUT_INPUT_INVALID")
    if any(item.earnings_per_share <= 0 for item in observations):
        reasons.append("PAYOUT_COVERAGE_UNAVAILABLE")
    reason_codes = tuple(sorted(set(reasons)))
    ordered = tuple(sorted(observations, key=lambda item: item.fiscal_year))
    cuts = sum(
        later.dividends_per_share < earlier.dividends_per_share
        for earlier, later in zip(ordered, ordered[1:])
    )
    if reason_codes:
        return DividendResearchResult(False, reason_codes, None, None, None, cuts)
    count = Decimal(len(ordered))
    dividend_yield = sum(
        (item.dividends_per_share / item.average_share_price for item in ordered),
        Decimal("0"),
    ) / count
    payout_ratio = sum(
        (item.dividends_per_share / item.earnings_per_share for item in ordered),
        Decimal("0"),
    ) / count
    shareholder_yield = sum(
        (
            item.dividends_per_share / item.average_share_price
            + (item.buybacks - item.issuance) / item.market_cap
            for item in ordered
        ),
        Decimal("0"),
    ) / count
    return DividendResearchResult(
        True, (), dividend_yield, payout_ratio, shareholder_yield, cuts
    )
