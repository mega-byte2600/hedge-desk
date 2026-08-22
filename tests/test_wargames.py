from decimal import Decimal
import unittest

from hedge_desk.wargames import (
    build_war_game_report,
    build_war_game_manifest,
    run_arbitrage_war_games,
    run_dividend_war_games,
    run_earnings_war_games,
    run_execution_war_games,
    run_lifecycle_war_games,
    run_futures_event_war_games,
    run_premium_war_games,
)


class PremiumWarGameTests(unittest.TestCase):
    def test_all_declared_scenarios_are_reported(self) -> None:
        report = build_war_game_report()
        self.assertTrue(report["all_declared_scenarios_included"])
        self.assertEqual(report["summary"]["total_scenario_count"], 33)
        self.assertEqual(report["summary"]["no_trade_control_count"], 15)
        premium = report["summary"]["premium_fixed_trade"]
        self.assertEqual(premium["profitable_scenarios"], 1)
        self.assertEqual(premium["losing_scenarios"], 4)
        self.assertFalse(premium["statistical_significance_computed"])
        self.assertEqual(
            premium["descriptive_metrics"]["inference_status"],
            "INSUFFICIENT_SYNTHETIC_SAMPLE",
        )
        self.assertEqual(report["fixture_manifest"]["scenario_count"], 33)
        self.assertEqual(len(report["fixture_manifest"]["fixture_sha256"]), 64)
        self.assertEqual(len(report["war_game_report_sha256"]), 64)
        summary = report["summary"]
        self.assertEqual(
            summary["earnings_fixed_arm_metrics"]["EQUITY"]["total_pnl"], "-22"
        )
        self.assertEqual(
            summary["earnings_fixed_arm_metrics"]["DEFINED_RISK_OPTION"]["total_pnl"],
            "-312.00",
        )
        self.assertEqual(summary["arbitrage_policy_metrics"]["total_pnl"], "45")
        self.assertEqual(
            summary["dividend_fixed_arm_metrics"]["SHARES"]["total_pnl"],
            "-1083.00",
        )

    def test_fixture_manifest_is_reproducible(self) -> None:
        self.assertEqual(build_war_game_manifest(), build_war_game_manifest())
        self.assertEqual(len(set(build_war_game_manifest()["scenario_ids"])), 33)

    def test_reference_scenario_pnls_are_exact(self) -> None:
        results = {result.scenario_id: result for result in run_premium_war_games()}
        self.assertEqual(results["favorable-decay"].net_pnl, Decimal("77.40"))
        self.assertEqual(results["no-edge-after-costs"].net_pnl, Decimal("-2.60"))
        self.assertEqual(results["iv-shock"].net_pnl, Decimal("-132.60"))
        self.assertEqual(results["gap-through-width"].net_pnl, Decimal("-382.60"))
        self.assertEqual(results["assignment-operations"].net_pnl, Decimal("-407.60"))

    def test_report_does_not_mislabel_synthetic_results_as_money_made(self) -> None:
        report = build_war_game_report()
        self.assertEqual(report["environment"], "paper")
        self.assertEqual(report["source"], "synthetic_fixture")
        self.assertIn("not historical or live results", report["limitations"][0])

    def test_earnings_iv_crush_can_make_call_lose_after_positive_move(self) -> None:
        results = {item["scenario_id"]: item for item in run_earnings_war_games()}
        iv_crush = results["positive-surprise-iv-crush"]
        self.assertEqual(iv_crush["equity_net_pnl"], "6")
        self.assertEqual(iv_crush["option_net_pnl"], "-204.00")
        self.assertEqual(iv_crush["best_hindsight_arm"], "EQUITY")

    def test_arbitrage_requires_executable_net_edge(self) -> None:
        results = {item["scenario_id"]: item for item in run_arbitrage_war_games()}
        self.assertEqual(results["net-edge-survives"]["disposition"], "NET_EDGE_CANDIDATE")
        self.assertEqual(results["one-tick-erased-by-costs"]["disposition"], "NO_TRADE")
        self.assertIn("QUOTES_NOT_SYNCHRONIZED", results["stale-fourth-leg"]["reason_codes"])

    def test_long_call_never_receives_dividend(self) -> None:
        results = {item["scenario_id"]: item for item in run_dividend_war_games()}
        self.assertTrue(all(item["call_dividend_received"] == "0" for item in results.values()))
        self.assertEqual(results["normal-dividend-entitlement"]["best_hindsight_arm"], "SHARES")
        self.assertEqual(results["yield-trap"]["best_hindsight_arm"], "NO_TRADE")

    def test_execution_terms_cancel_instead_of_partial_or_worse_fill(self) -> None:
        results = {item["scenario_id"]: item for item in run_execution_war_games()}
        self.assertEqual(
            results["approved-terms-available"]["disposition"],
            "READY_FOR_PAPER_OPEN",
        )
        for scenario_id in (
            "stale-entry-quote",
            "partial-combo-size",
            "approved-credit-unavailable",
            "contract-adjustment-pending",
        ):
            self.assertEqual(results[scenario_id]["disposition"], "NO_TRADE")

    def test_lifecycle_events_require_explicit_operational_actions(self) -> None:
        results = {item["scenario_id"]: item for item in run_lifecycle_war_games()}
        self.assertEqual(results["normal-monitoring"]["action"], "MONITOR")
        self.assertEqual(
            results["ex-dividend-early-assignment-risk"]["action"],
            "CLOSE_REVIEW_REQUIRED",
        )
        self.assertEqual(
            results["assignment-notice"]["action"],
            "ASSIGNMENT_RECONCILIATION_REQUIRED",
        )
        self.assertEqual(
            results["unconfirmed-settlement-terms"]["action"],
            "BLOCK_AND_ESCALATE",
        )

    def test_futures_events_subtract_curve_basis_roll_and_costs(self) -> None:
        results = {
            item["scenario_id"]: item for item in run_futures_event_war_games()
        }
        self.assertEqual(
            results["weather-surprise-edge-survives"]["disposition"],
            "EVENT_RESEARCH_CANDIDATE",
        )
        self.assertTrue(all(not item["trade_authorized"] for item in results.values()))
        self.assertEqual(
            results["weather-event-already-priced"]["disposition"], "NO_TRADE"
        )
        self.assertIn(
            "PHYSICAL_DELIVERY_DISABLED",
            results["physical-delivery-contract-disabled"]["reason_codes"],
        )


if __name__ == "__main__":
    unittest.main()
