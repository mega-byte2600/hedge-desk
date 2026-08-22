"""Deterministic vertical-spread enumeration from a validated snapshot."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, Tuple

from .snapshot import OptionSnapshot
from .spreads import (
    OptionQuote,
    OptionType,
    VerticalCreditSpread,
    VerticalSpreadCalculation,
    calculate_vertical_credit_spread,
)


@dataclass(frozen=True)
class SpreadScanPolicy:
    quantity: int = 1
    commission_per_contract: Decimal = Decimal("0.65")
    quote_tolerance_seconds: int = 2
    planned_exit_days_before_expiration: int = 7
    minimum_open_interest: int = 100
    minimum_volume: int = 10
    maximum_leg_spread_fraction: Decimal = Decimal("0.25")
    maximum_contract_count: int = 500
    maximum_pair_count: int = 20000


@dataclass(frozen=True)
class SpreadPairEvaluation:
    pair_id: str
    short_contract_id: str
    long_contract_id: str
    admissible: bool
    reason_code: str
    calculation: Optional[VerticalSpreadCalculation]


@dataclass(frozen=True)
class SpreadScanResult:
    source_id: str
    symbol: str
    evaluated_at: datetime
    disposition: str
    pair_count: int
    admissible_count: int
    evaluations: Tuple[SpreadPairEvaluation, ...]


def _pair_reason(exc: ValueError) -> str:
    mapping = {
        "candidate has reached its planned pre-expiration exit window": "EXIT_WINDOW_REACHED",
        "spread leg quotes are not timestamp-compatible": "QUOTE_TIMESTAMPS_MISALIGNED",
        "spread quantity exceeds executable displayed size": "DISPLAYED_SIZE_INSUFFICIENT",
        "spread leg open interest is below policy": "OPEN_INTEREST_BELOW_POLICY",
        "spread leg volume is below policy": "VOLUME_BELOW_POLICY",
        "option leg bid-ask spread exceeds liquidity policy": "BID_ASK_SPREAD_TOO_WIDE",
        "spread does not provide executable positive credit": "EXECUTABLE_CREDIT_NONPOSITIVE",
        "spread economics must have positive credit and max loss": "SPREAD_ECONOMICS_INVALID",
    }
    return mapping.get(str(exc), "PAIR_VALIDATION_FAILED")


def _ordered_pairs(quotes: Tuple[OptionQuote, ...]):
    ordered = sorted(
        quotes,
        key=lambda quote: (
            quote.expiration,
            quote.option_type.value,
            quote.strike,
            quote.contract_id,
        ),
    )
    for short in ordered:
        for long in ordered:
            if short.contract_id == long.contract_id:
                continue
            if short.expiration != long.expiration or short.option_type is not long.option_type:
                continue
            valid_orientation = (
                short.option_type is OptionType.PUT and short.strike > long.strike
            ) or (
                short.option_type is OptionType.CALL and short.strike < long.strike
            )
            if valid_orientation:
                yield short, long


def scan_vertical_credit_spreads(
    snapshot: OptionSnapshot,
    evaluated_at: datetime,
    policy: SpreadScanPolicy = SpreadScanPolicy(),
) -> SpreadScanResult:
    """Enumerate all admissible pairs; no ranking, probability, or RoR is inferred."""
    if evaluated_at.tzinfo is None:
        raise ValueError("scan timestamp must be timezone-aware")
    if len(snapshot.option_quotes) > policy.maximum_contract_count:
        raise ValueError("option snapshot exceeds contract-count safety limit")
    pairs = tuple(_ordered_pairs(snapshot.option_quotes))
    if len(pairs) > policy.maximum_pair_count:
        raise ValueError("option snapshot exceeds pair-count safety limit")
    evaluations = []
    for short, long in pairs:
        pair_id = f"{short.contract_id}--{long.contract_id}"
        spread = VerticalCreditSpread(
            pair_id,
            short,
            long,
            snapshot.underlying_quote,
            policy.quantity,
            policy.commission_per_contract,
            policy.quote_tolerance_seconds,
            policy.planned_exit_days_before_expiration,
            policy.minimum_open_interest,
            policy.minimum_volume,
            policy.maximum_leg_spread_fraction,
        )
        try:
            calculation = calculate_vertical_credit_spread(spread, evaluated_at)
        except ValueError as exc:
            evaluations.append(
                SpreadPairEvaluation(
                    pair_id,
                    short.contract_id,
                    long.contract_id,
                    False,
                    _pair_reason(exc),
                    None,
                )
            )
        else:
            evaluations.append(
                SpreadPairEvaluation(
                    pair_id,
                    short.contract_id,
                    long.contract_id,
                    True,
                    "",
                    calculation,
                )
            )
    ordered_evaluations = tuple(sorted(evaluations, key=lambda item: item.pair_id))
    admissible_count = sum(item.admissible for item in ordered_evaluations)
    return SpreadScanResult(
        snapshot.source_id,
        snapshot.underlying_quote.symbol,
        evaluated_at,
        "CANDIDATES_FOR_CONTROL_PIPELINE" if admissible_count else "NO_TRADE",
        len(ordered_evaluations),
        admissible_count,
        ordered_evaluations,
    )
