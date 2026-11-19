"""Reproducible depreciation scenario math; no Burry-specific scoring formula."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Mapping


def _decimal(inputs: Mapping[str, object], key: str, *, minimum: Decimal, maximum: Decimal | None = None) -> Decimal:
    try:
        value = Decimal(str(inputs[key]))
    except (KeyError, InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"{key} must be a finite decimal") from exc
    if not value.is_finite() or value < minimum or (maximum is not None and value > maximum):
        raise ValueError(f"{key} is outside the permitted range")
    return value


def calculate_depreciation_sensitivity(inputs: Mapping[str, object]) -> dict:
    """Calculate one-cohort straight-line D&A sensitivity using Decimal arithmetic."""
    cost = _decimal(inputs, "asset_cost_millions", minimum=Decimal("0.000001"))
    reported_life = _decimal(inputs, "reported_life_years", minimum=Decimal("0.000001"))
    scenario_life = _decimal(inputs, "scenario_life_years", minimum=Decimal("0.000001"))
    if scenario_life >= reported_life:
        raise ValueError("scenario_life_years must be shorter than reported_life_years")
    service = _decimal(inputs, "service_fraction_pct", minimum=Decimal("0"), maximum=Decimal("100")) / Decimal("100")
    tax = _decimal(inputs, "tax_rate_pct", minimum=Decimal("0"), maximum=Decimal("100")) / Decimal("100")
    net_income = _decimal(inputs, "reported_net_income_millions", minimum=Decimal("0.000001"))
    shares = _decimal(inputs, "diluted_shares_millions", minimum=Decimal("0.000001"))
    price = _decimal(inputs, "share_price", minimum=Decimal("0.000001"))

    pretax_delta = cost * service * (Decimal("1") / scenario_life - Decimal("1") / reported_life)
    after_tax_delta = pretax_delta * (Decimal("1") - tax)
    adjusted_income = net_income - after_tax_delta
    base_eps = net_income / shares
    adjusted_eps = adjusted_income / shares
    implied_pe = price / base_eps
    scenario_price = adjusted_eps * implied_pe if adjusted_eps > 0 else None
    move_pct = (scenario_price / price - Decimal("1")) * Decimal("100") if scenario_price is not None else None

    def out(value: Decimal | None) -> str | None:
        return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)) if value is not None else None

    return {
        "additional_annual_depreciation_millions": out(pretax_delta),
        "after_tax_earnings_delta_millions": out(after_tax_delta),
        "scenario_net_income_millions": out(adjusted_income),
        "reported_eps": out(base_eps),
        "scenario_eps": out(adjusted_eps),
        "implied_pe_unchanged": out(implied_pe),
        "scenario_price_unchanged_pe": out(scenario_price),
        "scenario_change_pct": out(move_pct),
        "trade_authorized": False,
        "calculation_label": "one-cohort straight-line depreciation sensitivity",
    }


__all__ = ["calculate_depreciation_sensitivity"]
