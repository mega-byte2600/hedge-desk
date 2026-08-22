"""Deterministic, synthetic war games for paper strategy evaluation."""

from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal
from typing import Any, Dict, Tuple

from hedge_desk.demo import FIXTURE_AS_OF, build_reference_plan, json_value
from hedge_desk.paper import approve_paper_trade, close_paper_trade, execute_paper_open


WAR_GAME_VERSION = "premium-spread-war-games-1.0.0"


@dataclass(frozen=True)
class PremiumWarGame:
    scenario_id: str
    description: str
    exit_debit_per_share: Decimal
    exit_commission_per_contract: Decimal
    additional_operational_cost: Decimal = Decimal("0")


@dataclass(frozen=True)
class PremiumWarGameResult:
    scenario_id: str
    description: str
    entry_credit: Decimal
    exit_debit: Decimal
    exit_commission: Decimal
    additional_operational_cost: Decimal
    net_pnl: Decimal
    profitable: bool
    maximum_loss_reference: Decimal


PREMIUM_WAR_GAMES: Tuple[PremiumWarGame, ...] = (
    PremiumWarGame(
        "favorable-decay",
        "Premium contracts before the planned exit.",
        Decimal("0.40"),
        Decimal("0.65"),
    ),
    PremiumWarGame(
        "no-edge-after-costs",
        "Gross spread value is unchanged and commissions create a loss.",
        Decimal("1.20"),
        Decimal("0.65"),
    ),
    PremiumWarGame(
        "iv-shock",
        "Implied volatility expands and the spread becomes more expensive.",
        Decimal("2.50"),
        Decimal("0.65"),
    ),
    PremiumWarGame(
        "gap-through-width",
        "Underlying gaps through both strikes and the spread approaches full width.",
        Decimal("5.00"),
        Decimal("0.65"),
    ),
    PremiumWarGame(
        "assignment-operations",
        "Adverse move plus synthetic assignment and operational handling cost.",
        Decimal("5.00"),
        Decimal("0.65"),
        Decimal("25.00"),
    ),
)


def run_premium_war_games() -> Tuple[PremiumWarGameResult, ...]:
    """Replay every declared scenario; no scenario selection is permitted."""
    plan = build_reference_plan()
    approved = approve_paper_trade(plan, "war-game-human", FIXTURE_AS_OF)
    opened = execute_paper_open(approved, FIXTURE_AS_OF + timedelta(minutes=1))
    results = []
    for index, scenario in enumerate(PREMIUM_WAR_GAMES, start=1):
        closed = close_paper_trade(
            opened,
            scenario.exit_debit_per_share,
            scenario.exit_commission_per_contract,
            FIXTURE_AS_OF + timedelta(days=index),
        )
        net_pnl = closed.realized_pnl - scenario.additional_operational_cost
        results.append(
            PremiumWarGameResult(
                scenario.scenario_id,
                scenario.description,
                opened.entry_credit,
                closed.exit_debit,
                closed.exit_commission,
                scenario.additional_operational_cost,
                net_pnl,
                net_pnl > 0,
                plan.spread.maximum_loss,
            )
        )
    return tuple(results)


def build_war_game_report() -> Dict[str, Any]:
    results = run_premium_war_games()
    pnls = tuple(result.net_pnl for result in results)
    wins = sum(result.profitable for result in results)
    return {
        "report_type": "synthetic_hypothetical_war_games",
        "version": WAR_GAME_VERSION,
        "environment": "paper",
        "source": "synthetic_fixture",
        "all_declared_scenarios_included": True,
        "summary": {
            "scenario_count": len(results),
            "profitable_scenarios": wins,
            "losing_scenarios": len(results) - wins,
            "mean_pnl": str(sum(pnls, Decimal("0")) / Decimal(len(pnls))),
            "worst_pnl": str(min(pnls)),
            "best_pnl": str(max(pnls)),
        },
        "results": json_value(results),
        "limitations": [
            "These are deterministic synthetic stresses, not historical or live results.",
            "A profitable scenario does not establish strategy expectancy.",
            "Assignment cost is a declared synthetic reserve, not a broker quote.",
        ],
    }
