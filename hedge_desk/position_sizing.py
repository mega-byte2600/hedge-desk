"""Tiny position filter for the GP's real rules (small desk, appropriate scale).

The GP's rules, encoded as computed checks, not a framework:
- Return on CAPITAL DEPLOYED (net_credit / collateral), not max-loss dollars.
- Max ~2% per trade on capital; ~30-45 DTE; conservative premium wheel.
- Capital required under $5k (just getting started).
- Survivability: max loss must not risk the ability to keep trading.

One function, returns a plain dict. Nothing invented: account_equity is a real
input. trade_authorized stays False. No order.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Dict, Tuple

from hedge_desk.options.requirements import cash_secured_put_collateral

# Reviewable bounds (small scale, GP standing rules), not scattered magic numbers.
MAX_RETURN_ON_CAPITAL = Decimal("0.02")     # <=2% per trade on capital deployed
MAX_CAPITAL_REQUIRED = Decimal("5000")      # <$5k collateral (just getting started)
MAX_LOSS_FRACTION_EQUITY = Decimal("0.02")  # max loss <=2% of real account equity


def evaluate_premium(
    net_credit: str,
    max_loss: str,
    short_strike: str,
    account_equity: str,
    days_to_expiration: int,
) -> Dict[str, object]:
    """Return a plain dict verdict + computed numbers; rejects fabricated inputs."""
    if not account_equity or Decimal(account_equity) <= 0:
        raise ValueError("account_equity is required (real balance, never invented)")
    credit = Decimal(net_credit)
    loss = Decimal(max_loss)
    equity = Decimal(account_equity)
    collateral = cash_secured_put_collateral(
        Decimal(short_strike), credit, 1
    ).requirement

    # Return on capital deployed = credit_per_contract / collateral_in_dollars.
    # credit is per-share; collateral is dollars (strike*100 - credit*100), so
    # multiply credit by 100 to keep both sides in dollars (the x100 cancels to
    # credit/(strike-credit)). Dividing per-share credit by dollar collateral
    # would report a 100x-too-small number (the units bug QUANT caught).
    return_on_capital = (credit * Decimal("100")) / collateral if collateral else Decimal("0")
    loss_fraction = loss / equity
    reasons: list[str] = []
    if loss_fraction > MAX_LOSS_FRACTION_EQUITY:
        reasons.append("MAX_LOSS_TOO_LARGE_FOR_ACCOUNT")
    if collateral > MAX_CAPITAL_REQUIRED:
        reasons.append("CAPITAL_OVER_5K")
    if not Decimal("0.005") <= return_on_capital <= MAX_RETURN_ON_CAPITAL:
        reasons.append("RETURN_NOT_IN_GP_BAND")
    if not 30 <= days_to_expiration <= 45:
        reasons.append("DTE_OUTSIDE_30_45")

    return {
        "collateral_required": str(collateral.quantize(Decimal("0.01"))),
        "return_on_capital": str(return_on_capital.quantize(Decimal("0.0001"))),
        "max_loss_fraction_of_equity": str(loss_fraction.quantize(Decimal("0.0001"))),
        "fits_gp_rules": not reasons,
        "reasons": reasons,
        "trade_authorized": False,
    }


__all__ = ["evaluate_premium"]