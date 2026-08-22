from decimal import Decimal
import json
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
    run_model_governance_war_games,
    run_compliance_war_games,
    run_premium_timing_war_games,
    run_premium_cadence_war_games,
    run_candidate_pipeline_war_games,
    run_premium_war_games,
    run_option_universe_war_games,
    run_strategic_allocation_war_games,
    validate_war_game_report,
)


class PremiumWarGameTests(unittest.TestCase):
    def test_all_declared_scenarios_are_reported(self) -> None:
        report = build_war_game_report()
        self.assertTrue(report["all_declared_scenarios_included"])
        self.assertEqual(report["summary"]["total_scenario_count"], 66)
        self.assertEqual(report["summary"]["no_trade_control_count"], 39)
        premium = report["summary"]["premium_fixed_trade"]
        self.assertEqual(premium["profitable_scenarios"], 1)
        self.assertEqual(premium["losing_scenarios"], 4)
        self.assertFalse(premium["statistical_significance_computed"])
        self.assertEqual(
            premium["descriptive_metrics"]["inference_status"],
            "INSUFFICIENT_SYNTHETIC_SAMPLE",
        )
        self.assertEqual(report["fixture_manifest"]["scenario_count"], 66)
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
        self.assertEqual(len(set(build_war_game_manifest()["scenario_ids"])), 66)

    def test_monthly_cadence_blocks_new_entries_but_not_monitoring(self) -> None:
        results = {
            item["scenario_id"]: item
            for item in run_premium_cadence_war_games()
        }
        self.assertEqual(
            results["cadence-monthly-window-open"]["disposition"],
            "NEW_ENTRY_RESEARCH_WINDOW",
        )
        for scenario_id in (
            "cadence-same-month-blocked", "cadence-future-ledger-entry"
        ):
            self.assertEqual(results[scenario_id]["disposition"], "NO_TRADE")
            self.assertTrue(results[scenario_id]["monitoring_allowed"])
            self.assertFalse(results[scenario_id]["trade_authorized"])

    def test_strategic_allocation_stresses_block_concentration_and_bad_weights(self) -> None:
        results = {
            item["scenario_id"]: item
            for item in run_strategic_allocation_war_games()
        }
        self.assertEqual(
            results["allocation-diversified-high-cape"]["disposition"],
            "RESEARCH_CONTROL_PASS",
        )
        self.assertEqual(
            results["allocation-concentrated-high-cape"]["disposition"],
            "NO_TRADE",
        )
        self.assertIn(
            "HIGH_CAPE_US_EQUITY_CONCENTRATION",
            results["allocation-concentrated-high-cape"]["reason_codes"],
        )
        self.assertEqual(
            results["allocation-weights-malformed"]["disposition"], "NO_TRADE"
        )
        self.assertTrue(all(not item["trade_authorized"] for item in results.values()))
        self.assertTrue(all(not item["risk_of_ruin_calculated"] for item in results.values()))

    def test_underlying_universe_ranks_or_returns_no_trade(self) -> None:
        results = {
            item["scenario_id"]: item for item in run_option_universe_war_games()
        }
        self.assertEqual(
            results["underlying-executable-ranking"]["top_ranked_underlying"],
            "STRONG",
        )
        self.assertEqual(
            results["underlying-thin-market-no-trade"]["disposition"], "NO_TRADE"
        )
        self.assertEqual(
            results["underlying-closed-session-no-trade"]["disposition"], "NO_TRADE"
        )
        self.assertTrue(all(not item["probability_inferred"] for item in results.values()))
        self.assertTrue(all(not item["trade_authorized"] for item in results.values()))

    def test_serialized_report_matches_fresh_deterministic_run(self) -> None:
        serialized = json.loads(json.dumps(build_war_game_report()))
        self.assertEqual(validate_war_game_report(serialized), ())

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

    def test_front_office_cannot_release_without_back_office_certification(self) -> None:
        results = {
            item["scenario_id"]: item for item in run_compliance_war_games()
        }
        blocked = results["front-office-without-back-office-release"]
        self.assertEqual(blocked["disposition"], "NO_TRADE")
        self.assertFalse(blocked["human_override_allowed"])
        self.assertIn(
            "RELEASE_REQUIREMENT_UNSATISFIED:BACK_OFFICE_RECONCILIATION_CERTIFIED",
            blocked["reason_codes"],
        )

    def test_back_office_reconciliation_mismatches_are_declared_no_trade_games(self) -> None:
        results = {
            item["scenario_id"]: item for item in run_compliance_war_games()
        }
        expected = {
            "back-office-cash-ledger-mismatch": "CASH_LEDGER_MISMATCH",
            "back-office-position-ledger-mismatch": "POSITION_LEDGER_MISMATCH",
            "back-office-unresolved-lifecycle-exception": (
                "UNRESOLVED_LIFECYCLE_EXCEPTIONS"
            ),
        }
        for scenario_id, reason in expected.items():
            self.assertEqual(results[scenario_id]["disposition"], "NO_TRADE")
            self.assertFalse(results[scenario_id]["human_override_allowed"])
            self.assertIn(reason, results[scenario_id]["reason_codes"])

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

    def test_model_governance_never_becomes_authoritative_risk(self) -> None:
        results = {
            item["scenario_id"]: item for item in run_model_governance_war_games()
        }
        self.assertEqual(
            results["quant-ai-agree-research-only"]["disposition"],
            "RESEARCH_HYPOTHESIS_ONLY",
        )
        self.assertTrue(
            all(not item["authoritative_risk_input"] for item in results.values())
        )

    def test_model_split_leakage_attacks_are_no_trade(self) -> None:
        results = {
            item["scenario_id"]: item
            for item in run_model_governance_war_games()
        }
        expected = {
            "model-train-validation-overlap": "TRAIN_VALIDATION_PURGE_VIOLATION",
            "model-future-test-lookahead": "MODEL_SPLIT_POINT_IN_TIME_VIOLATION",
            "model-split-hash-collision": "MODEL_SPLIT_HASH_COLLISION",
        }
        for scenario_id, reason in expected.items():
            self.assertEqual(results[scenario_id]["disposition"], "NO_TRADE")
            self.assertIn(reason, results[scenario_id]["reason_codes"])
            self.assertFalse(results[scenario_id]["split_trade_authorized"])
        self.assertIn(
            "RESEARCH_TEAMS_DISAGREE",
            results["quant-ai-disagree"]["reason_codes"],
        )
        self.assertIn(
            "OPEN_LICENSE_REQUIRED",
            results["ai-artifact-license-blocked"]["reason_codes"],
        )

    def test_compliance_attacks_always_fail_closed(self) -> None:
        results = {
            item["scenario_id"]: item for item in run_compliance_war_games()
        }
        self.assertTrue(
            all(item["disposition"] == "NO_TRADE" for item in results.values())
        )
        self.assertTrue(
            all(not item["human_override_allowed"] for item in results.values())
        )
        self.assertIn(
            "PAPER_ONLY_VIOLATION",
            results["live-environment-request"]["reason_codes"],
        )
        self.assertIn(
            "COMPLIANCE_ARTIFACT_HASH_MISMATCH",
            results["compliance-artifact-tamper"]["reason_codes"],
        )
        self.assertIn(
            "COMPLIANCE_STATUS_INCONSISTENT",
            results["agent-compliance-pass-override"]["reason_codes"],
        )
        self.assertIn(
            "OPTIONS_DISCLOSURE_ACKNOWLEDGEMENT_REQUIRED",
            results["options-disclosure-missing"]["reason_codes"],
        )
        self.assertIn(
            "OPTIONS_DISCLOSURE_ACKNOWLEDGED_AFTER_CANDIDATE",
            results["options-disclosure-after-candidate"]["reason_codes"],
        )

    def test_premium_timing_ladder_hits_exact_exit_boundary(self) -> None:
        results = {
            item["scenario_id"]: item for item in run_premium_timing_war_games()
        }
        self.assertEqual(results["timing-8-dte"]["lifecycle_action"], "MONITOR")
        self.assertEqual(results["timing-8-dte"]["exit_policy_action"], "MONITOR")
        self.assertEqual(
            results["timing-planned-exit-7-dte"]["lifecycle_action"],
            "CLOSE_REVIEW_REQUIRED",
        )
        self.assertEqual(
            results["timing-planned-exit-7-dte"]["net_pnl_if_closed"],
            "77.40",
        )
        self.assertIn(
            "PROFIT_CAPTURE_TARGET_REACHED",
            results["timing-planned-exit-7-dte"]["exit_policy_reason_codes"],
        )
        self.assertEqual(
            results["timing-adverse-1-dte"]["net_pnl_if_closed"], "-362.60"
        )
        self.assertIn(
            "LOSS_REVIEW_THRESHOLD_REACHED",
            results["timing-adverse-1-dte"]["exit_policy_reason_codes"],
        )
        self.assertTrue(
            all(not item["trade_authorized"] for item in results.values())
        )
        self.assertEqual(
            results["timing-expiration"]["lifecycle_action"],
            "EXPIRATION_RECONCILIATION_REQUIRED",
        )

    def test_candidate_pipeline_attacks_never_reach_back_office(self) -> None:
        results = {
            item["scenario_id"]: item
            for item in run_candidate_pipeline_war_games()
        }
        self.assertTrue(all(not item["trade_authorized"] for item in results.values()))
        self.assertIn(
            "VALIDATED_RISK_INPUT_REQUIRED",
            results["candidate-awaits-validated-risk"]["reason_codes"],
        )
        self.assertIn(
            "NO_ADMISSIBLE_CANDIDATE",
            results["candidate-thin-market"]["reason_codes"],
        )
        self.assertIn(
            "HANDOFF_HASH_MISMATCH",
            results["candidate-handoff-economics-tamper"]["reason_codes"],
        )
        self.assertIn(
            "UNTRUSTED_TRADE_AUTHORIZATION",
            results["candidate-front-office-authorization"]["reason_codes"],
        )


if __name__ == "__main__":
    unittest.main()
