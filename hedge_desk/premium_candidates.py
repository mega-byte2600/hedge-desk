"""Turn a real EOD equities batch into premium-desk candidate economics.

Increment 3 of the true-MVP re-scope (docs/MVP_RESCOPE_2026.md): the equities
EOD screen is the universe feeder; the Overnight Premium Desk is the product.
This module consumes the validated EOD batch and, for each symbol, computes the
defined-risk premium-selling structures the desk already models — cash-secured
put, covered call, vertical credit spread — using the versioned collateral and
margin requirements in ``hedge_desk.options.requirements``.

Honesty boundary (matches the desk's discipline):
- It computes COLLATERAL / MARGIN REQUIREMENTS from the real EOD close. It does
  NOT fabricate option prices, implied volatility, probability, or Risk of Ruin.
- It does NOT place an order and does NOT authorize a trade.
- A candidate is a research structure with a knowable capital requirement, not a
  promise of income. Premium income is only knowable from a real option chain
  (the existing BYO-data option-snapshot path), which this module does not fake.
- Every structure carries the exact requirement basis and reason codes from the
  versioned margin policy, so a reviewer can reproduce the number.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, Sequence, Tuple

from hedge_desk.data.eod_ingest import EodDay
from hedge_desk.options.requirements import (
    DEFAULT_POLICY,
    Strategy,
    cash_secured_put_collateral,
    covered_call_requirement,
    credit_spread_margin,
)

PREMIUM_CANDIDATE_VERSION = "hedge-desk-premium-candidate-1.0.0"

# Simple, explicit, reviewable structure assumptions (NOT market data).
# These are the "options basics" the GP named: sell a put at a strike below the
# close, sell a call at a strike above the close, or a defined-risk vertical.
# The strike offsets are policy constants, not quotes.
CASH_SECURED_PUT_STRIKE_OFFSET = Decimal("0.90")  # 10% below close
COVERED_CALL_STRIKE_OFFSET = Decimal("1.10")  # 10% above close
CREDIT_SPREAD_WIDTH = Decimal("5.00")  # $5 wide vertical
# A placeholder net credit is NOT used: margin is computed at zero credit so the
# requirement is the maximum possible capital at risk (conservative, no invented
# premium). Real premium comes only from a real option chain.
ZERO_CREDIT = Decimal("0")


@dataclass(frozen=True)
class PremiumCandidate:
    symbol: str
    close: str
    strategy: str
    strike: str
    requirement: str
    requirement_basis: str
    reason_codes: Tuple[str, ...]
    policy_version: str
    trade_authorized: bool = False


def _close_decimal(day: EodDay) -> Decimal:
    value = Decimal(day.close)
    if not value.is_finite() or value <= 0:
        raise ValueError(f"non-positive close for {day.date}")
    return value


def build_premium_candidates(
    eod_result: Dict[str, object],
) -> Dict[str, object]:
    """Build premium-desk candidate economics from a validated EOD batch.

    Only PASS symbols with a real close are considered. Each symbol yields up to
    three defined-risk structures with their collateral/margin requirement.
    """
    source_results = eod_result.get("source_results")
    if not isinstance(source_results, list):
        raise ValueError("eod result missing source_results")
    candidates: list[PremiumCandidate] = []
    for row in source_results:
        if not isinstance(row, dict):
            continue
        if row.get("status") != "PASS":
            continue
        symbol = str(row.get("symbol", ""))
        last_close = row.get("last_day_close")
        if not symbol or last_close is None:
            continue
        close = Decimal(str(last_close))
        if not close.is_finite() or close <= 0:
            continue

        # Cash-secured put: sell a put 10% below close. Collateral = strike.
        put_strike = (close * CASH_SECURED_PUT_STRIKE_OFFSET).quantize(Decimal("0.01"))
        put_req = cash_secured_put_collateral(
            put_strike, ZERO_CREDIT, 1, DEFAULT_POLICY
        )
        candidates.append(
            PremiumCandidate(
                symbol, str(close), Strategy.CASH_SECURED_PUT.value,
                str(put_strike), str(put_req.requirement), put_req.basis,
                tuple(put_req.reason_codes), put_req.policy_version,
            )
        )

        # Covered call: own 100 shares, sell a call 10% above close.
        call_strike = (close * COVERED_CALL_STRIKE_OFFSET).quantize(Decimal("0.01"))
        call_req = covered_call_requirement(close, 1, DEFAULT_POLICY)
        candidates.append(
            PremiumCandidate(
                symbol, str(close), Strategy.COVERED_CALL.value,
                str(call_strike), str(call_req.requirement), call_req.basis,
                tuple(call_req.reason_codes), call_req.policy_version,
            )
        )

        # Vertical credit spread: $5 wide, margin = width (max loss) at zero credit.
        spread_req = credit_spread_margin(
            CREDIT_SPREAD_WIDTH, ZERO_CREDIT, 1, DEFAULT_POLICY
        )
        candidates.append(
            PremiumCandidate(
                symbol, str(close), Strategy.CREDIT_SPREAD.value,
                f"{CREDIT_SPREAD_WIDTH} wide", str(spread_req.requirement),
                spread_req.basis, tuple(spread_req.reason_codes),
                spread_req.policy_version,
            )
        )

    ordered = tuple(sorted(candidates, key=lambda c: (c.symbol, c.strategy)))
    return {
        "schema_version": PREMIUM_CANDIDATE_VERSION,
        "mode": "PREMIUM_DESK_CANDIDATES_FROM_REAL_EOD",
        "candidate_count": len(ordered),
        "symbol_count": len({c.symbol for c in ordered}),
        "candidates": [
            {
                "symbol": c.symbol,
                "close": c.close,
                "strategy": c.strategy,
                "strike": c.strike,
                "requirement": c.requirement,
                "requirement_basis": c.requirement_basis,
                "reason_codes": list(c.reason_codes),
                "policy_version": c.policy_version,
                "trade_authorized": c.trade_authorized,
            }
            for c in ordered
        ],
        "note": (
            "Collateral/margin requirements computed from real EOD closes. "
            "No option prices, probability, or Risk of Ruin are fabricated. "
            "Premium income requires a real option chain (BYO-data path). "
            "No order is placed and no trade is authorized."
        ),
    }


__all__ = [
    "PREMIUM_CANDIDATE_VERSION",
    "PremiumCandidate",
    "build_premium_candidates",
]