"""Deterministic portfolio exposure gates independent of authoritative RoR."""

import json
from dataclasses import dataclass
from decimal import Decimal
from hashlib import sha256
from typing import Tuple

from hedge_desk.domain import Account, TradeCandidate


PORTFOLIO_POLICY_VERSION = "paper-portfolio-1.0.0"


@dataclass(frozen=True)
class PositionExposure:
    position_id: str
    symbol: str
    maximum_loss: Decimal

    def __post_init__(self) -> None:
        if not self.position_id or not self.symbol or self.maximum_loss < 0:
            raise ValueError("position identity, symbol, and nonnegative loss are required")


@dataclass(frozen=True)
class PortfolioPolicy:
    maximum_aggregate_loss_fraction: Decimal = Decimal("0.05")
    maximum_symbol_loss_fraction: Decimal = Decimal("0.02")
    maximum_open_positions: int = 10


@dataclass(frozen=True)
class PortfolioGateResult:
    reason_codes: Tuple[str, ...]
    snapshot_sha256: str
    aggregate_maximum_loss_after: Decimal
    symbol_maximum_loss_after: Decimal


@dataclass(frozen=True)
class CircuitBreakerResult:
    new_risk_frozen: bool
    reason_codes: Tuple[str, ...]
    artifact_sha256: str


def evaluate_drawdown_circuit_breaker(
    current_drawdown: Decimal,
    maximum_drawdown: Decimal,
    source_report_sha256: str,
) -> CircuitBreakerResult:
    """Create a deterministic Back Office new-risk state from validated inputs."""
    if current_drawdown < 0 or maximum_drawdown <= 0:
        raise ValueError("drawdown inputs must be nonnegative with a positive limit")
    try:
        valid_hash = len(source_report_sha256) == 64 and int(source_report_sha256, 16) >= 0
    except ValueError:
        valid_hash = False
    if not valid_hash:
        raise ValueError("circuit-breaker source report hash must be valid")
    frozen = current_drawdown > maximum_drawdown
    reasons = ("PORTFOLIO_DRAWDOWN_CIRCUIT_BREAKER",) if frozen else ()
    payload = {
        "current_drawdown": str(current_drawdown),
        "maximum_drawdown": str(maximum_drawdown),
        "new_risk_frozen": frozen,
        "reason_codes": list(reasons),
        "source_report_sha256": source_report_sha256,
    }
    artifact_sha256 = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return CircuitBreakerResult(frozen, reasons, artifact_sha256)


def evaluate_portfolio_gate(
    account: Account,
    candidate: TradeCandidate,
    positions: Tuple[PositionExposure, ...],
    policy: PortfolioPolicy = PortfolioPolicy(),
) -> PortfolioGateResult:
    if len({position.position_id for position in positions}) != len(positions):
        raise ValueError("portfolio position identities must be unique")
    snapshot_payload = [
        {
            "maximum_loss": str(position.maximum_loss),
            "position_id": position.position_id,
            "symbol": position.symbol,
        }
        for position in sorted(positions, key=lambda item: item.position_id)
    ]
    snapshot_sha256 = sha256(
        json.dumps(snapshot_payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    aggregate = sum(
        (position.maximum_loss for position in positions), Decimal("0")
    ) + candidate.max_loss
    symbol_loss = sum(
        (
            position.maximum_loss
            for position in positions
            if position.symbol == candidate.symbol
        ),
        Decimal("0"),
    ) + candidate.max_loss
    reasons = []
    if len(positions) + 1 > policy.maximum_open_positions:
        reasons.append("MAXIMUM_OPEN_POSITIONS")
    if aggregate / account.equity > policy.maximum_aggregate_loss_fraction:
        reasons.append("PORTFOLIO_AGGREGATE_LOSS_LIMIT")
    if symbol_loss / account.equity > policy.maximum_symbol_loss_fraction:
        reasons.append("SYMBOL_CONCENTRATION_LIMIT")
    return PortfolioGateResult(
        tuple(sorted(reasons)), snapshot_sha256, aggregate, symbol_loss
    )
