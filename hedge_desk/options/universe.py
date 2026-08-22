"""Cross-underlying ranking of executable defined-risk option economics."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Tuple

from .handoff import build_candidate_control_handoffs
from .scanner import SpreadScanPolicy, scan_vertical_credit_spreads
from .session import MarketSessionGate
from .snapshot import OptionSnapshot


@dataclass(frozen=True)
class RankedOptionCandidate:
    rank: int
    symbol: str
    candidate_id: str
    maximum_win: Decimal
    maximum_loss: Decimal
    credit_to_maximum_loss: Decimal
    calculation_sha256: str
    next_action: str = "VALIDATED_RISK_INPUT_REQUIRED"
    trade_authorized: bool = False


@dataclass(frozen=True)
class OptionUniverseEvaluation:
    disposition: str
    candidates: Tuple[RankedOptionCandidate, ...]
    rejected_underlyings: Tuple[Tuple[str, Tuple[str, ...]], ...]
    ranking_basis: str = "executable_credit_to_defined_maximum_loss"
    probability_inferred: bool = False
    trade_authorized: bool = False


def evaluate_option_universe(
    snapshots: Tuple[OptionSnapshot, ...],
    evaluated_at: datetime,
    session_gate: MarketSessionGate,
    policy: SpreadScanPolicy = SpreadScanPolicy(),
) -> OptionUniverseEvaluation:
    if not snapshots:
        raise ValueError("option universe cannot be empty")
    symbols = [item.underlying_quote.symbol for item in snapshots]
    if len(symbols) != len(set(symbols)):
        raise ValueError("option universe symbols must be unique")
    admitted = []
    rejected = []
    for snapshot in sorted(snapshots, key=lambda item: item.underlying_quote.symbol):
        symbol = snapshot.underlying_quote.symbol
        scan = scan_vertical_credit_spreads(snapshot, evaluated_at, policy)
        handoffs = build_candidate_control_handoffs(scan, session_gate)
        calculations = {
            item.calculation.spread_id: item.calculation
            for item in scan.evaluations
            if item.admissible and item.calculation is not None
        }
        if not handoffs:
            reasons = session_gate.reason_codes or tuple(
                sorted({item.reason_code for item in scan.evaluations if item.reason_code})
            ) or ("NO_VERTICAL_PAIR",)
            rejected.append((symbol, reasons))
            continue
        for handoff in handoffs:
            calculation = calculations[handoff.candidate_id]
            admitted.append((symbol, handoff, calculation))
    ordered = sorted(
        admitted,
        key=lambda item: (
            -(item[2].net_credit / item[2].maximum_loss),
            item[0],
            item[1].candidate_id,
        ),
    )
    candidates = tuple(
        RankedOptionCandidate(
            rank,
            symbol,
            handoff.candidate_id,
            calculation.net_credit,
            calculation.maximum_loss,
            calculation.net_credit / calculation.maximum_loss,
            handoff.calculation_sha256,
        )
        for rank, (symbol, handoff, calculation) in enumerate(ordered, start=1)
    )
    return OptionUniverseEvaluation(
        "RESEARCH_CANDIDATES_FOR_CONTROL_PIPELINE" if candidates else "NO_TRADE",
        candidates,
        tuple(rejected),
    )
