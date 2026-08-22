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


@dataclass(frozen=True)
class DividendCompanyHistory:
    symbol: str
    observations: Tuple[AnnualPayoutObservation, ...]


@dataclass(frozen=True)
class DividendUniversePolicy:
    maximum_average_payout_ratio: Decimal = Decimal("0.75")
    maximum_dividend_cuts: int = 0
    minimum_net_shareholder_yield: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        values = (
            self.maximum_average_payout_ratio,
            self.minimum_net_shareholder_yield,
        )
        if any(
            not isinstance(value, Decimal) or not value.is_finite()
            for value in values
        ):
            raise ValueError("dividend policy values must be finite Decimals")
        if (
            self.maximum_average_payout_ratio <= 0
            or self.minimum_net_shareholder_yield < 0
            or type(self.maximum_dividend_cuts) is not int
            or self.maximum_dividend_cuts < 0
        ):
            raise ValueError("dividend universe policy is invalid")


@dataclass(frozen=True)
class DividendRankedCandidate:
    rank: int
    symbol: str
    ten_year_average_dividend_yield: Decimal
    ten_year_average_payout_ratio: Decimal
    ten_year_average_net_shareholder_yield: Decimal
    yield_per_payout_ratio: Decimal
    dividend_cut_count: int
    long_call_cash_dividend_entitlement: Decimal
    trade_authorized: bool = False


@dataclass(frozen=True)
class DividendUniverseEvaluation:
    disposition: str
    candidates: Tuple[DividendRankedCandidate, ...]
    rejected_symbols: Tuple[Tuple[str, Tuple[str, ...]], ...]
    trade_authorized: bool = False


@dataclass(frozen=True)
class CapeObservation:
    symbol: str
    cape_ratio: Decimal
    observed_at: datetime
    received_at: datetime
    source_artifact_sha256: str


@dataclass(frozen=True)
class DividendCapeInput:
    history: DividendCompanyHistory
    cape: CapeObservation


@dataclass(frozen=True)
class DividendCapeCandidate:
    rank: int
    symbol: str
    cape_ratio: Decimal
    yield_per_payout_ratio: Decimal
    valuation_adjusted_distribution_score: Decimal
    long_call_cash_dividend_entitlement: Decimal = Decimal("0")
    trade_authorized: bool = False


@dataclass(frozen=True)
class DividendCapeEvaluation:
    disposition: str
    candidates: Tuple[DividendCapeCandidate, ...]
    rejected_symbols: Tuple[Tuple[str, Tuple[str, ...]], ...]
    trade_authorized: bool = False


def _valid_hash(value: str) -> bool:
    try:
        return isinstance(value, str) and len(value) == 64 and int(value, 16) > 0
    except ValueError:
        return False


def evaluate_dividend_history(
    observations: Tuple[AnnualPayoutObservation, ...],
    decision_time: datetime,
) -> DividendResearchResult:
    if decision_time.tzinfo is None:
        raise ValueError("decision timestamp must be timezone-aware")
    numeric_values = tuple(
        value
        for item in observations
        for value in (
            item.dividends_per_share,
            item.earnings_per_share,
            item.average_share_price,
            item.buybacks,
            item.issuance,
            item.market_cap,
        )
    )
    if any(
        not isinstance(value, Decimal) or not value.is_finite()
        for value in numeric_values
    ):
        raise ValueError("dividend numeric inputs must be finite Decimals")
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


def evaluate_dividend_universe(
    histories: Tuple[DividendCompanyHistory, ...],
    decision_time: datetime,
    policy: DividendUniversePolicy = DividendUniversePolicy(),
) -> DividendUniverseEvaluation:
    """Rank admissible histories; never convert research ranking into a trade."""
    if not histories:
        raise ValueError("dividend universe cannot be empty")
    symbols = [item.symbol for item in histories]
    if any(not symbol for symbol in symbols) or len(symbols) != len(set(symbols)):
        raise ValueError("dividend universe symbols must be unique and nonempty")
    admitted = []
    rejected = []
    for company in sorted(histories, key=lambda item: item.symbol):
        result = evaluate_dividend_history(company.observations, decision_time)
        reasons = list(result.reason_codes)
        if result.admissible:
            assert result.ten_year_average_payout_ratio is not None
            assert result.ten_year_average_dividend_yield is not None
            assert result.ten_year_average_net_shareholder_yield is not None
            if result.ten_year_average_payout_ratio <= 0:
                reasons.append("NONPOSITIVE_AVERAGE_PAYOUT_RATIO")
            if (
                result.ten_year_average_payout_ratio
                > policy.maximum_average_payout_ratio
            ):
                reasons.append("AVERAGE_PAYOUT_RATIO_ABOVE_POLICY")
            if result.dividend_cut_count > policy.maximum_dividend_cuts:
                reasons.append("DIVIDEND_CUTS_ABOVE_POLICY")
            if (
                result.ten_year_average_net_shareholder_yield
                < policy.minimum_net_shareholder_yield
            ):
                reasons.append("NET_SHAREHOLDER_YIELD_BELOW_POLICY")
        reason_codes = tuple(sorted(set(reasons)))
        if reason_codes:
            rejected.append((company.symbol, reason_codes))
            continue
        admitted.append((company.symbol, result))
    ordered = sorted(
        admitted,
        key=lambda item: (
            -(
                item[1].ten_year_average_dividend_yield
                / item[1].ten_year_average_payout_ratio
            ),
            -item[1].ten_year_average_net_shareholder_yield,
            item[0],
        ),
    )
    candidates = tuple(
        DividendRankedCandidate(
            rank,
            symbol,
            result.ten_year_average_dividend_yield,
            result.ten_year_average_payout_ratio,
            result.ten_year_average_net_shareholder_yield,
            result.ten_year_average_dividend_yield
            / result.ten_year_average_payout_ratio,
            result.dividend_cut_count,
            result.long_call_cash_dividend_entitlement,
        )
        for rank, (symbol, result) in enumerate(ordered, start=1)
    )
    return DividendUniverseEvaluation(
        "RANKED_RESEARCH_ONLY" if candidates else "NO_TRADE",
        candidates,
        tuple(rejected),
        False,
    )


def evaluate_dividend_cape_universe(
    inputs: Tuple[DividendCapeInput, ...],
    decision_time: datetime,
    policy: DividendUniversePolicy = DividendUniversePolicy(),
) -> DividendCapeEvaluation:
    """Combine ten-year distributions with PIT CAPE; research ranking only."""
    if not inputs:
        raise ValueError("dividend CAPE universe cannot be empty")
    if any(
        not isinstance(item.cape.cape_ratio, Decimal)
        or not item.cape.cape_ratio.is_finite()
        for item in inputs
    ):
        raise ValueError("CAPE inputs must be finite Decimals")
    symbols = [item.history.symbol for item in inputs]
    if len(symbols) != len(set(symbols)):
        raise ValueError("dividend CAPE universe symbols must be unique")
    history_evaluation = evaluate_dividend_universe(
        tuple(item.history for item in inputs), decision_time, policy
    )
    ranked_by_symbol = {item.symbol: item for item in history_evaluation.candidates}
    rejected = dict(history_evaluation.rejected_symbols)
    admitted = []
    for item in sorted(inputs, key=lambda value: value.history.symbol):
        symbol = item.history.symbol
        reasons = list(rejected.get(symbol, ()))
        cape = item.cape
        if cape.symbol != symbol:
            reasons.append("CAPE_SYMBOL_MISMATCH")
        if cape.observed_at.tzinfo is None or cape.received_at.tzinfo is None:
            reasons.append("CAPE_TIMESTAMP_NOT_TIMEZONE_AWARE")
        else:
            if cape.received_at < cape.observed_at:
                reasons.append("CAPE_RECEIVED_BEFORE_OBSERVED")
            if cape.received_at > decision_time:
                reasons.append("CAPE_LOOKAHEAD_VIOLATION")
        if cape.cape_ratio <= 0:
            reasons.append("CAPE_RATIO_INVALID")
        if not _valid_hash(cape.source_artifact_sha256):
            reasons.append("CAPE_SOURCE_HASH_INVALID")
        if symbol not in ranked_by_symbol and not reasons:
            reasons.append("DIVIDEND_HISTORY_NOT_ADMISSIBLE")
        reason_codes = tuple(sorted(set(reasons)))
        if reason_codes:
            rejected[symbol] = reason_codes
            continue
        dividend = ranked_by_symbol[symbol]
        admitted.append((
            symbol,
            cape.cape_ratio,
            dividend.yield_per_payout_ratio,
            dividend.yield_per_payout_ratio / cape.cape_ratio,
        ))
    ordered = sorted(admitted, key=lambda value: (-value[3], value[0]))
    candidates = tuple(
        DividendCapeCandidate(rank, symbol, cape, efficiency, score)
        for rank, (symbol, cape, efficiency, score) in enumerate(ordered, start=1)
    )
    return DividendCapeEvaluation(
        "CAPE_ADJUSTED_RESEARCH_ONLY" if candidates else "NO_TRADE",
        candidates,
        tuple(sorted(rejected.items())),
        False,
    )
