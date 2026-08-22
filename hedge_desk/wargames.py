"""Deterministic, synthetic war games for paper strategy evaluation."""

from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal
from hashlib import sha256
import json
from typing import Any, Dict, Tuple

from hedge_desk.demo import FIXTURE_AS_OF, build_reference_plan, json_value
from hedge_desk.paper import (
    approve_paper_trade,
    close_paper_trade,
    evaluate_paper_fill,
    execute_paper_open,
)
from hedge_desk.metrics import evaluate_pnl_series


WAR_GAME_VERSION = "premium-spread-war-games-1.0.0"
WAR_GAME_FIXTURE_SCHEMA_VERSION = "war-game-fixtures-1.0.0"


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


@dataclass(frozen=True)
class EarningsWarGame:
    scenario_id: str
    start_price: Decimal
    end_price: Decimal
    shares: int
    equity_cost: Decimal
    option_entry_debit: Decimal
    option_exit_credit: Decimal
    option_cost: Decimal
    hedged_gross_pnl: Decimal
    hedged_cost: Decimal


@dataclass(frozen=True)
class ArbitrageWarGame:
    scenario_id: str
    gross_edge: Decimal
    quantity: int
    fees: Decimal
    slippage_reserve: Decimal
    financing_cost: Decimal
    minimum_edge_buffer: Decimal
    quotes_synchronized: bool = True
    depth_available: int = 1
    settlement_compatible: bool = True


@dataclass(frozen=True)
class DividendWarGame:
    scenario_id: str
    start_price: Decimal
    end_price: Decimal
    shares: int
    dividend_per_share_received: Decimal
    share_cost: Decimal
    call_entry_debit: Decimal
    call_exit_credit: Decimal
    call_cost: Decimal


@dataclass(frozen=True)
class ExecutionWarGame:
    scenario_id: str
    available_combo_size: int
    current_net_credit: Decimal
    checked_offset_seconds: int
    contract_adjustment_pending: bool = False


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


EARNINGS_WAR_GAMES: Tuple[EarningsWarGame, ...] = (
    EarningsWarGame(
        "surprise-followthrough", Decimal("100"), Decimal("104"), 10,
        Decimal("4"), Decimal("2.50"), Decimal("4.00"), Decimal("4"),
        Decimal("25"), Decimal("5"),
    ),
    EarningsWarGame(
        "positive-surprise-iv-crush", Decimal("100"), Decimal("101"), 10,
        Decimal("4"), Decimal("4.00"), Decimal("2.00"), Decimal("4"),
        Decimal("5"), Decimal("5"),
    ),
    EarningsWarGame(
        "headline-beat-guidance-reversal", Decimal("100"), Decimal("94"), 10,
        Decimal("4"), Decimal("3.00"), Decimal("0.50"), Decimal("4"),
        Decimal("-20"), Decimal("5"),
    ),
)


ARBITRAGE_WAR_GAMES: Tuple[ArbitrageWarGame, ...] = (
    ArbitrageWarGame(
        "net-edge-survives", Decimal("80"), 1, Decimal("12"), Decimal("15"),
        Decimal("8"), Decimal("20"),
    ),
    ArbitrageWarGame(
        "one-tick-erased-by-costs", Decimal("20"), 1, Decimal("12"),
        Decimal("10"), Decimal("4"), Decimal("5"),
    ),
    ArbitrageWarGame(
        "stale-fourth-leg", Decimal("100"), 1, Decimal("12"), Decimal("15"),
        Decimal("8"), Decimal("20"), quotes_synchronized=False,
    ),
    ArbitrageWarGame(
        "insufficient-depth", Decimal("100"), 2, Decimal("12"), Decimal("15"),
        Decimal("8"), Decimal("20"), depth_available=1,
    ),
    ArbitrageWarGame(
        "settlement-mismatch", Decimal("100"), 1, Decimal("12"), Decimal("15"),
        Decimal("8"), Decimal("20"), settlement_compatible=False,
    ),
)


DIVIDEND_WAR_GAMES: Tuple[DividendWarGame, ...] = (
    DividendWarGame(
        "normal-dividend-entitlement", Decimal("50"), Decimal("52"), 100,
        Decimal("1"), Decimal("4"), Decimal("2"), Decimal("3.50"), Decimal("5"),
    ),
    DividendWarGame(
        "special-dividend", Decimal("50"), Decimal("48"), 100, Decimal("5"),
        Decimal("5"), Decimal("2"), Decimal("1"), Decimal("5"),
    ),
    DividendWarGame(
        "dividend-cut", Decimal("50"), Decimal("48"), 100, Decimal("0.10"),
        Decimal("5"), Decimal("2"), Decimal("0.50"), Decimal("5"),
    ),
    DividendWarGame(
        "yield-trap", Decimal("50"), Decimal("35"), 100, Decimal("0.25"),
        Decimal("4"), Decimal("2"), Decimal("0.10"), Decimal("5"),
    ),
)


EXECUTION_WAR_GAMES: Tuple[ExecutionWarGame, ...] = (
    ExecutionWarGame("approved-terms-available", 1, Decimal("118.70"), 120),
    ExecutionWarGame("stale-entry-quote", 1, Decimal("118.70"), 121),
    ExecutionWarGame("partial-combo-size", 0, Decimal("118.70"), 60),
    ExecutionWarGame("approved-credit-unavailable", 1, Decimal("118.69"), 60),
    ExecutionWarGame(
        "contract-adjustment-pending", 1, Decimal("118.70"), 60, True
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


def run_earnings_war_games() -> Tuple[Dict[str, str], ...]:
    results = []
    for scenario in EARNINGS_WAR_GAMES:
        equity = (
            (scenario.end_price - scenario.start_price) * Decimal(scenario.shares)
            - scenario.equity_cost
        )
        option = (
            (scenario.option_exit_credit - scenario.option_entry_debit) * Decimal("100")
            - scenario.option_cost
        )
        hedged = scenario.hedged_gross_pnl - scenario.hedged_cost
        arms = {"EQUITY": equity, "DEFINED_RISK_OPTION": option, "HEDGED_EQUITY": hedged, "NO_TRADE": Decimal("0")}
        selected = max(sorted(arms), key=lambda arm: arms[arm])
        results.append(
            {
                "scenario_id": scenario.scenario_id,
                "equity_net_pnl": str(equity),
                "option_net_pnl": str(option),
                "hedged_equity_net_pnl": str(hedged),
                "no_trade_net_pnl": "0",
                "best_hindsight_arm": selected,
            }
        )
    return tuple(results)


def run_arbitrage_war_games() -> Tuple[Dict[str, str], ...]:
    results = []
    for scenario in ARBITRAGE_WAR_GAMES:
        reasons = []
        if not scenario.quotes_synchronized:
            reasons.append("QUOTES_NOT_SYNCHRONIZED")
        if scenario.depth_available < scenario.quantity:
            reasons.append("INSUFFICIENT_DEPTH")
        if not scenario.settlement_compatible:
            reasons.append("SETTLEMENT_MISMATCH")
        net_edge = (
            scenario.gross_edge * Decimal(scenario.quantity)
            - scenario.fees
            - scenario.slippage_reserve
            - scenario.financing_cost
        )
        if net_edge < scenario.minimum_edge_buffer:
            reasons.append("EDGE_BELOW_SAFETY_BUFFER")
        results.append(
            {
                "scenario_id": scenario.scenario_id,
                "gross_edge": str(scenario.gross_edge * Decimal(scenario.quantity)),
                "net_edge": str(net_edge),
                "disposition": "NO_TRADE" if reasons else "NET_EDGE_CANDIDATE",
                "reason_codes": ",".join(sorted(reasons)),
            }
        )
    return tuple(results)


def run_dividend_war_games() -> Tuple[Dict[str, str], ...]:
    results = []
    for scenario in DIVIDEND_WAR_GAMES:
        share_pnl = (
            (scenario.end_price - scenario.start_price) * Decimal(scenario.shares)
            + scenario.dividend_per_share_received * Decimal(scenario.shares)
            - scenario.share_cost
        )
        call_pnl = (
            (scenario.call_exit_credit - scenario.call_entry_debit) * Decimal("100")
            - scenario.call_cost
        )
        arms = {"SHARES": share_pnl, "LONG_CALL": call_pnl, "NO_TRADE": Decimal("0")}
        selected = max(sorted(arms), key=lambda arm: arms[arm])
        results.append(
            {
                "scenario_id": scenario.scenario_id,
                "share_net_pnl": str(share_pnl),
                "call_net_pnl": str(call_pnl),
                "call_dividend_received": "0",
                "no_trade_net_pnl": "0",
                "best_hindsight_arm": selected,
            }
        )
    return tuple(results)


def run_execution_war_games() -> Tuple[Dict[str, Any], ...]:
    plan = approve_paper_trade(build_reference_plan(), "war-game-human", FIXTURE_AS_OF)
    results = []
    for scenario in EXECUTION_WAR_GAMES:
        check = evaluate_paper_fill(
            plan,
            scenario.available_combo_size,
            scenario.current_net_credit,
            FIXTURE_AS_OF + timedelta(seconds=scenario.checked_offset_seconds),
            scenario.contract_adjustment_pending,
        )
        results.append(
            {
                "scenario_id": scenario.scenario_id,
                "disposition": "READY_FOR_PAPER_OPEN" if check.ready else "NO_TRADE",
                "reason_codes": list(check.reason_codes),
            }
        )
    return tuple(results)


def build_war_game_manifest() -> Dict[str, Any]:
    """Content-address every declared scenario input using canonical JSON."""
    fixtures = {
        "premium": json_value(PREMIUM_WAR_GAMES),
        "earnings": json_value(EARNINGS_WAR_GAMES),
        "arbitrage": json_value(ARBITRAGE_WAR_GAMES),
        "dividend": json_value(DIVIDEND_WAR_GAMES),
        "execution": json_value(EXECUTION_WAR_GAMES),
    }
    scenario_ids = [
        scenario["scenario_id"]
        for group in fixtures.values()
        for scenario in group
    ]
    if len(scenario_ids) != len(set(scenario_ids)):
        raise ValueError("war-game scenario identities must be globally unique")
    payload = {
        "schema_version": WAR_GAME_FIXTURE_SCHEMA_VERSION,
        "fixtures": fixtures,
    }
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return {
        "schema_version": WAR_GAME_FIXTURE_SCHEMA_VERSION,
        "scenario_count": len(scenario_ids),
        "scenario_ids": scenario_ids,
        "fixture_sha256": sha256(canonical).hexdigest(),
    }


def build_war_game_report() -> Dict[str, Any]:
    results = run_premium_war_games()
    earnings = run_earnings_war_games()
    arbitrage = run_arbitrage_war_games()
    dividend = run_dividend_war_games()
    execution = run_execution_war_games()
    pnls = tuple(result.net_pnl for result in results)
    wins = sum(result.profitable for result in results)
    premium_metrics = evaluate_pnl_series(pnls)
    no_trade_controls = (
        sum(item["best_hindsight_arm"] == "NO_TRADE" for item in earnings)
        + sum(item["disposition"] == "NO_TRADE" for item in arbitrage)
        + sum(item["best_hindsight_arm"] == "NO_TRADE" for item in dividend)
        + sum(item["disposition"] == "NO_TRADE" for item in execution)
    )
    return {
        "report_type": "synthetic_hypothetical_war_games",
        "version": WAR_GAME_VERSION,
        "environment": "paper",
        "source": "synthetic_fixture",
        "all_declared_scenarios_included": True,
        "fixture_manifest": build_war_game_manifest(),
        "summary": {
            "total_scenario_count": (
                len(results) + len(earnings) + len(arbitrage) + len(dividend)
                + len(execution)
            ),
            "scenario_count_by_mvp": {
                "overnight-premium-desk": len(results),
                "earnings-event-desk": len(earnings),
                "arbitrage-observer": len(arbitrage),
                "dividend-opportunity-desk": len(dividend),
                "execution-controls": len(execution),
            },
            "no_trade_control_count": no_trade_controls,
            "premium_fixed_trade": {
                "profitable_scenarios": wins,
                "losing_scenarios": len(results) - wins,
                "mean_pnl": str(sum(pnls, Decimal("0")) / Decimal(len(pnls))),
                "worst_pnl": str(min(pnls)),
                "best_pnl": str(max(pnls)),
                "descriptive_metrics": json_value(premium_metrics),
                "sequence_label": "declared_synthetic_stress_order_not_time_series",
                "statistical_significance_computed": False,
            },
        },
        "premium": json_value(results),
        "earnings": earnings,
        "arbitrage": arbitrage,
        "dividend": dividend,
        "execution_controls": execution,
        "limitations": [
            "These are deterministic synthetic stresses, not historical or live results.",
            "A profitable scenario does not establish strategy expectancy.",
            "Assignment cost is a declared synthetic reserve, not a broker quote.",
        ],
    }
