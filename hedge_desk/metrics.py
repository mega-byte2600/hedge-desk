"""Deterministic descriptive metrics; no inference or significance claims."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Tuple


@dataclass(frozen=True)
class DescriptivePerformance:
    sample_size: int
    total_pnl: Decimal
    mean_pnl: Decimal
    median_pnl: Decimal
    win_rate: Decimal
    profit_factor: Decimal
    maximum_drawdown: Decimal
    expected_shortfall: Decimal
    expected_shortfall_confidence: Decimal
    inference_status: str = "INSUFFICIENT_SYNTHETIC_SAMPLE"


def _median(values: Tuple[Decimal, ...]) -> Decimal:
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[midpoint]
    return (ordered[midpoint - 1] + ordered[midpoint]) / Decimal("2")


def evaluate_pnl_series(
    pnls: Tuple[Decimal, ...],
    expected_shortfall_confidence: Decimal = Decimal("0.80"),
) -> DescriptivePerformance:
    """Describe a declared P&L sequence without treating it as an IID sample."""
    if not pnls:
        raise ValueError("at least one P&L observation is required")
    if any(not isinstance(value, Decimal) or not value.is_finite() for value in pnls):
        raise ValueError("P&L observations must be finite Decimals")
    if (
        not isinstance(expected_shortfall_confidence, Decimal)
        or not expected_shortfall_confidence.is_finite()
    ):
        raise ValueError("expected shortfall confidence must be a finite Decimal")
    if not Decimal("0") < expected_shortfall_confidence < Decimal("1"):
        raise ValueError("expected shortfall confidence must be between zero and one")

    total = sum(pnls, Decimal("0"))
    wins = sum(value > 0 for value in pnls)
    gross_profit = sum((value for value in pnls if value > 0), Decimal("0"))
    gross_loss = -sum((value for value in pnls if value < 0), Decimal("0"))
    profit_factor = (
        gross_profit / gross_loss if gross_loss > 0 else Decimal("Infinity")
    )

    equity = Decimal("0")
    peak = Decimal("0")
    maximum_drawdown = Decimal("0")
    for pnl in pnls:
        equity += pnl
        peak = max(peak, equity)
        maximum_drawdown = max(maximum_drawdown, peak - equity)

    tail_fraction = Decimal("1") - expected_shortfall_confidence
    tail_count = max(1, int((Decimal(len(pnls)) * tail_fraction).to_integral_value(rounding="ROUND_CEILING")))
    tail = tuple(sorted(pnls)[:tail_count])
    expected_shortfall = sum(tail, Decimal("0")) / Decimal(tail_count)

    return DescriptivePerformance(
        sample_size=len(pnls),
        total_pnl=total,
        mean_pnl=total / Decimal(len(pnls)),
        median_pnl=_median(pnls),
        win_rate=Decimal(wins) / Decimal(len(pnls)),
        profit_factor=profit_factor,
        maximum_drawdown=maximum_drawdown,
        expected_shortfall=expected_shortfall,
        expected_shortfall_confidence=expected_shortfall_confidence,
    )
