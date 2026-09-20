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


def wheel_fit_for_equity(account_equity: str) -> Dict[str, object]:
    """Given real account equity, state how the cash-secured-put wheel fits.

    The 2%-of-equity max-loss rule means a position's worst-case loss (its
    collateral, e.g. a $3,200 cash-secured put) must stay under 2% of the account.
    This surfaces the honest consequence: at a small account the wheel's $1k-4.4k
    candidates are blocked by survivability, and a larger account is needed to run
    any of them. Returns the max allowed position size and an explanation.
    """
    equity = Decimal(account_equity)
    if equity <= 0:
        raise ValueError("account_equity must be positive")
    max_allowed_loss = equity * MAX_LOSS_FRACTION_EQUITY
    return {
        "max_position_collateral": str(max_allowed_loss.quantize(Decimal("0.01"))),
        "explanation": (
            f"2% of equity = ${max_allowed_loss.quantize(Decimal('0.01')):.2f} "
            "worst-case position loss allowed. Any candidate whose worst-case "
            "loss exceeds this fails survivability - the wheel needs an account "
            "roughly 50x the position size."
        ),
    }


def scale_position_to_equity(
    max_loss_per_contract: str,
    capital_per_contract: str,
    account_equity: str,
) -> Dict[str, object]:
    """Size how many contracts the GP can sell so total worst-case loss stays <= 2% of equity.

    Keeps the small-desk 2%-of-equity max-loss discipline (the scale) while
    scaling position size up automatically as the account grows (the compounding
    path to "get big"). For a cash-secured put, worst-case loss per contract is
    the collateral (stock -> $0), so contracts = floor(2% of equity / capital per
    contract). At a small account this is 0; as equity compounds, more contracts
    fit. Returns plain derived numbers, no fabricated P&L, no performance claim.
    """
    mloss = Decimal(max_loss_per_contract)
    capital = Decimal(capital_per_contract)
    equity = Decimal(account_equity)
    if equity <= 0 or mloss <= 0 or capital <= 0:
        raise ValueError("equity, max_loss, and capital must be positive")
    budget = equity * MAX_LOSS_FRACTION_EQUITY
    contracts = int(budget / mloss)  # floor
    return {
        "max_contracts": contracts,
        "position_capital": str((capital * contracts).quantize(Decimal("0.01"))),
        "max_contracts_explanation": (
            f"2% of equity = ${budget.quantize(Decimal('0.01'))} max total loss; "
            f"each contract risks ${mloss.quantize(Decimal('0.01'))}, so up to "
            f"{contracts} contract(s) fit. Contracts scale up as equity compounds."
        ),
    }


__all__ = ["evaluate_premium", "wheel_fit_for_equity", "scale_position_to_equity"]