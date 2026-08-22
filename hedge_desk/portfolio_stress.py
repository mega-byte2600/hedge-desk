"""Deterministic combined-MVP capital-path stresses using synthetic fixtures."""

import json
from dataclasses import dataclass
from decimal import Decimal
from hashlib import sha256
from typing import Any, Dict, Tuple

from hedge_desk.demo import json_value
from hedge_desk.metrics import evaluate_pnl_series
from hedge_desk.backoffice import CircuitBreakerResult, evaluate_drawdown_circuit_breaker


PORTFOLIO_STRESS_VERSION = "combined-mvp-capital-path-1.0.0"


@dataclass(frozen=True)
class StrategyShock:
    project_id: str
    gross_pnl: Decimal
    costs: Decimal


@dataclass(frozen=True)
class PortfolioStressScenario:
    scenario_id: str
    shocks: Tuple[StrategyShock, ...]


SCENARIOS: Tuple[PortfolioStressScenario, ...] = (
    PortfolioStressScenario(
        "quiet-decay",
        (
            StrategyShock("overnight-premium-desk", Decimal("80"), Decimal("2.60")),
            StrategyShock("earnings-event-desk", Decimal("0"), Decimal("0")),
            StrategyShock("arbitrage-observer", Decimal("0"), Decimal("0")),
            StrategyShock("dividend-opportunity-desk", Decimal("25"), Decimal("4")),
            StrategyShock("event-futures-desk", Decimal("0"), Decimal("0")),
        ),
    ),
    PortfolioStressScenario(
        "equity-gap-and-volatility-shock",
        (
            StrategyShock("overnight-premium-desk", Decimal("-380"), Decimal("2.60")),
            StrategyShock("earnings-event-desk", Decimal("-600"), Decimal("8")),
            StrategyShock("arbitrage-observer", Decimal("0"), Decimal("0")),
            StrategyShock("dividend-opportunity-desk", Decimal("-1450"), Decimal("5")),
            StrategyShock("event-futures-desk", Decimal("-450"), Decimal("50")),
        ),
    ),
    PortfolioStressScenario(
        "false-arbitrage-and-stale-market",
        (
            StrategyShock("overnight-premium-desk", Decimal("-130"), Decimal("2.60")),
            StrategyShock("earnings-event-desk", Decimal("0"), Decimal("0")),
            StrategyShock("arbitrage-observer", Decimal("-250"), Decimal("35")),
            StrategyShock("dividend-opportunity-desk", Decimal("0"), Decimal("0")),
            StrategyShock("event-futures-desk", Decimal("0"), Decimal("0")),
        ),
    ),
    PortfolioStressScenario(
        "dividend-cut-correlation",
        (
            StrategyShock("overnight-premium-desk", Decimal("-200"), Decimal("2.60")),
            StrategyShock("earnings-event-desk", Decimal("-300"), Decimal("8")),
            StrategyShock("arbitrage-observer", Decimal("0"), Decimal("0")),
            StrategyShock("dividend-opportunity-desk", Decimal("-1200"), Decimal("5")),
            StrategyShock("event-futures-desk", Decimal("-250"), Decimal("50")),
        ),
    ),
    PortfolioStressScenario(
        "all-signals-crowded-exit",
        (
            StrategyShock("overnight-premium-desk", Decimal("-380"), Decimal("27.60")),
            StrategyShock("earnings-event-desk", Decimal("-750"), Decimal("58")),
            StrategyShock("arbitrage-observer", Decimal("-400"), Decimal("85")),
            StrategyShock("dividend-opportunity-desk", Decimal("-1600"), Decimal("55")),
            StrategyShock("event-futures-desk", Decimal("-1200"), Decimal("100")),
        ),
    ),
)


def build_portfolio_stress_report(
    starting_capital: Decimal = Decimal("100000"),
    maximum_drawdown_fraction: Decimal = Decimal("0.05"),
) -> Dict[str, Any]:
    if starting_capital <= 0:
        raise ValueError("starting capital must be positive")
    if not Decimal("0") < maximum_drawdown_fraction < Decimal("1"):
        raise ValueError("drawdown fraction must be between zero and one")
    scenario_ids = [scenario.scenario_id for scenario in SCENARIOS]
    if len(scenario_ids) != len(set(scenario_ids)):
        raise ValueError("portfolio stress scenario identities must be unique")

    fixture_payload = json.dumps(
        json_value(SCENARIOS), sort_keys=True, separators=(",", ":")
    ).encode()
    scenario_results = []
    capital = starting_capital
    peak = starting_capital
    sequence_pnls = []
    for scenario in SCENARIOS:
        net_by_project = {
            shock.project_id: shock.gross_pnl - shock.costs for shock in scenario.shocks
        }
        pnl = sum(net_by_project.values(), Decimal("0"))
        sequence_pnls.append(pnl)
        capital += pnl
        peak = max(peak, capital)
        drawdown = peak - capital
        limit = starting_capital * maximum_drawdown_fraction
        reasons = ("DRAWDOWN_LIMIT_BREACHED",) if drawdown > limit else ()
        scenario_results.append(
            {
                "scenario_id": scenario.scenario_id,
                "net_pnl_by_project": {k: str(net_by_project[k]) for k in sorted(net_by_project)},
                "combined_net_pnl": str(pnl),
                "ending_capital": str(capital),
                "drawdown": str(drawdown),
                "disposition": "FREEZE_NEW_RISK" if reasons else "WITHIN_SYNTHETIC_LIMIT",
                "reason_codes": list(reasons),
            }
        )
    metrics = evaluate_pnl_series(tuple(sequence_pnls))
    report = {
        "report_type": "synthetic_hypothetical_portfolio_stress",
        "version": PORTFOLIO_STRESS_VERSION,
        "source": "synthetic_fixture",
        "sequence_label": "declared_stress_order_not_historical_time_series",
        "starting_capital": str(starting_capital),
        "maximum_drawdown_fraction": str(maximum_drawdown_fraction),
        "scenario_count": len(SCENARIOS),
        "fixture_sha256": sha256(fixture_payload).hexdigest(),
        "scenarios": scenario_results,
        "descriptive_metrics": json_value(metrics),
        "inference_status": "INSUFFICIENT_SYNTHETIC_SAMPLE",
        "real_money_pnl": "0",
    }
    report["stress_report_sha256"] = sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return report


def build_stress_circuit_breaker(report: Dict[str, Any]) -> CircuitBreakerResult:
    """Bridge a verified stress artifact into the deterministic Back Office gate."""
    payload = {key: value for key, value in report.items() if key != "stress_report_sha256"}
    expected_hash = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if report.get("stress_report_sha256") != expected_hash:
        raise ValueError("portfolio stress report integrity check failed")
    current_drawdown = Decimal(report["descriptive_metrics"]["maximum_drawdown"])
    maximum_drawdown = (
        Decimal(report["starting_capital"])
        * Decimal(report["maximum_drawdown_fraction"])
    )
    return evaluate_drawdown_circuit_breaker(
        current_drawdown, maximum_drawdown, expected_hash
    )


def validate_portfolio_stress_report(value: Dict[str, Any]) -> Tuple[str, ...]:
    """Require the frozen stress report to equal a fresh deterministic run."""
    expected = build_portfolio_stress_report(
        Decimal(value.get("starting_capital", "0")),
        Decimal(value.get("maximum_drawdown_fraction", "0")),
    )
    return () if value == expected else ("PORTFOLIO_STRESS_REFERENCE_MISMATCH",)
