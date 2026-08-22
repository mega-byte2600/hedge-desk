"""Executable-side multi-leg arbitrage research economics."""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Tuple


class LegSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass(frozen=True)
class ArbitrageLeg:
    leg_id: str
    side: LegSide
    bid: Decimal
    ask: Decimal
    displayed_size: int
    quoted_at: datetime
    settlement_date: date
    source_artifact_sha256: str


@dataclass(frozen=True)
class ArbitrageEvaluation:
    admissible: bool
    disposition: str
    reason_codes: Tuple[str, ...]
    executable_entry_cashflow: Decimal
    net_edge: Decimal
    trade_authorized: bool = False


def _valid_hash(value: str) -> bool:
    try:
        return len(value) == 64 and int(value, 16) >= 0
    except ValueError:
        return False


def evaluate_arbitrage_package(
    legs: Tuple[ArbitrageLeg, ...],
    quantity: int,
    contract_multiplier: int,
    terminal_present_value: Decimal,
    fees: Decimal,
    slippage_reserve: Decimal,
    financing_cost: Decimal,
    minimum_edge_buffer: Decimal,
    quote_tolerance_seconds: int = 1,
) -> ArbitrageEvaluation:
    if len(legs) < 2 or quantity <= 0 or contract_multiplier <= 0:
        raise ValueError("multi-leg package, quantity, and multiplier are required")
    if len({leg.leg_id for leg in legs}) != len(legs):
        raise ValueError("arbitrage leg identities must be unique")
    if any(value < 0 for value in (fees, slippage_reserve, financing_cost, minimum_edge_buffer)):
        raise ValueError("costs and safety buffer cannot be negative")
    reasons = []
    if any(leg.quoted_at.tzinfo is None for leg in legs):
        reasons.append("QUOTE_TIMESTAMP_NOT_TIMEZONE_AWARE")
    else:
        times = tuple(leg.quoted_at for leg in legs)
        if (max(times) - min(times)).total_seconds() > quote_tolerance_seconds:
            reasons.append("QUOTES_NOT_SYNCHRONIZED")
    if len({leg.settlement_date for leg in legs}) != 1:
        reasons.append("SETTLEMENT_MISMATCH")
    if any(leg.displayed_size < quantity for leg in legs):
        reasons.append("INSUFFICIENT_DEPTH")
    if any(leg.bid < 0 or leg.ask <= 0 or leg.ask < leg.bid for leg in legs):
        reasons.append("INVALID_EXECUTABLE_QUOTE")
    if any(not _valid_hash(leg.source_artifact_sha256) for leg in legs):
        reasons.append("ARBITRAGE_SOURCE_HASH_INVALID")
    multiplier_quantity = Decimal(contract_multiplier * quantity)
    entry_cashflow = sum(
        (
            leg.bid * multiplier_quantity
            if leg.side is LegSide.SELL
            else -leg.ask * multiplier_quantity
        )
        for leg in legs
    )
    net_edge = (
        entry_cashflow + terminal_present_value - fees - slippage_reserve - financing_cost
    )
    if net_edge < minimum_edge_buffer:
        reasons.append("EDGE_BELOW_SAFETY_BUFFER")
    reason_codes = tuple(sorted(set(reasons)))
    return ArbitrageEvaluation(
        not reason_codes,
        "NET_EDGE_RESEARCH_CANDIDATE" if not reason_codes else "NO_TRADE",
        reason_codes,
        entry_cashflow,
        net_edge,
    )
