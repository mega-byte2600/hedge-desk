from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
import unittest

from hedge_desk.overnight import build_morning_report
from hedge_desk.reporting import (
    build_control_summary,
    compare_morning_reports,
    finalize_report,
    render_morning_markdown,
    validate_report,
)


NOW = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)


class ReportingTests(unittest.TestCase):
    def test_complete_morning_report_is_publishable(self) -> None:
        report = build_morning_report(NOW)
        self.assertTrue(validate_report(report).publishable)
        self.assertEqual(len(report["report_sha256"]), 64)

    def test_control_summary_is_validated_and_truthfully_separates_results(self) -> None:
        report = build_morning_report(NOW)
        summary = build_control_summary(report)
        self.assertEqual(summary["report_type"], "paper_morning_control_summary")
        self.assertEqual(summary["projects_evaluated"], 6)
        self.assertEqual(summary["human_review"], 1)
        self.assertEqual(summary["no_trade_projects"], 5)
        self.assertEqual(summary["real_money_pnl"], "0")
        self.assertEqual(summary["real_trades_executed"], 0)
        self.assertEqual(summary["war_game_scenarios"], 66)
        self.assertEqual(summary["no_trade_controls"], 39)
        self.assertEqual(summary["portfolio_stress_scenarios"], 5)
        self.assertEqual(summary["synthetic_stress_total_pnl"], "-9936.00")
        self.assertEqual(summary["release_status"], "LIVE_RELEASE_BLOCKED")
        self.assertFalse(summary["live_transition_authorized"])
        self.assertEqual(summary["paper_back_office_reconciliation"], "pass")
        self.assertFalse(summary["paper_reconciliation_live_release_eligible"])
        self.assertTrue(summary["premium_new_entry_evaluation_allowed"])
        self.assertTrue(summary["premium_monitoring_allowed"])
        self.assertEqual(summary["premium_exit_review_scenarios"], 3)
        self.assertTrue(summary["strategic_allocation_admissible"])
        self.assertEqual(
            summary["strategic_allocation_policy_version"],
            "diversification-cape-policy-1.0.0",
        )
        self.assertFalse(summary["strategic_allocation_ror_calculated"])

        report["real_money_pnl"] = "1"
        report = finalize_report(report)
        with self.assertRaisesRegex(ValueError, "not publishable"):
            build_control_summary(report)

    def test_tampering_invalidates_report_hash(self) -> None:
        report = build_morning_report(NOW)
        report["summary"]["human_review"] = 99
        self.assertIn("REPORT_HASH_INVALID", validate_report(report).reason_codes)

    def test_rehashed_strategic_allocation_tampering_is_blocked(self) -> None:
        report = build_morning_report(NOW)
        report["strategic_allocation"]["cape_ratio"] = "20"
        report = finalize_report(report)
        self.assertIn(
            "STRATEGIC_ALLOCATION_INVALID", validate_report(report).reason_codes
        )

    def test_rehashed_summary_must_reconcile_to_registered_projects(self) -> None:
        report = build_morning_report(NOW)
        report["summary"]["human_review"] = 0
        report["summary"]["no_trade"] = 6
        report = finalize_report(report)
        self.assertIn("PROJECT_SUMMARY_INVALID", validate_report(report).reason_codes)
        with self.assertRaisesRegex(ValueError, "not publishable"):
            build_control_summary(report)

    def test_rehashed_duplicate_or_unknown_project_identity_is_blocked(self) -> None:
        report = build_morning_report(NOW)
        report["projects"][1]["project_id"] = report["projects"][0]["project_id"]
        report = finalize_report(report)
        self.assertIn("PROJECT_SUMMARY_INVALID", validate_report(report).reason_codes)

    def test_malformed_nested_report_fails_closed_without_parser_exception(self) -> None:
        for mutation in ("unhashable_project_id", "missing_layers", "bad_stress"):
            report = build_morning_report(NOW)
            if mutation == "unhashable_project_id":
                report["projects"][0]["project_id"] = {"agent": "injected"}
            elif mutation == "missing_layers":
                report["projects"][0].pop("layers")
            else:
                report["portfolio_stress"]["scenarios"] = None
            report = finalize_report(report)
            decision = validate_report(report)
            self.assertFalse(decision.publishable)
            self.assertTrue(decision.reason_codes)
            with self.assertRaisesRegex(ValueError, "not publishable"):
                build_control_summary(report)

    def test_real_profit_claim_is_blocked_even_with_rehashed_report(self) -> None:
        report = build_morning_report(NOW)
        report["real_money_pnl"] = "1000"
        report = finalize_report(report)
        self.assertIn("REAL_PERFORMANCE_CLAIM_BLOCKED", validate_report(report).reason_codes)

    def test_missing_code_commit_is_publication_blocked(self) -> None:
        report = build_morning_report(NOW)
        report["code_commit"] = ""
        report = finalize_report(report)
        self.assertIn("CODE_COMMIT_MISSING", validate_report(report).reason_codes)

    def test_prohibited_promotional_claim_is_blocked(self) -> None:
        report = build_morning_report(NOW)
        report["marketing_claim"] = "Guaranteed profit"
        report = finalize_report(report)
        self.assertIn("PROHIBITED_PERFORMANCE_CLAIM", validate_report(report).reason_codes)

    def test_missing_replay_lineage_is_blocked(self) -> None:
        report = build_morning_report(NOW)
        report["chronological_replay"]["valid"] = False
        report = finalize_report(report)
        self.assertIn("REPLAY_LINEAGE_INVALID", validate_report(report).reason_codes)

    def test_rehashed_outer_report_cannot_hide_audit_event_tampering(self) -> None:
        report = build_morning_report(NOW)
        report["audit_chain"]["events"][3]["policy_version"] = "agent-policy"
        report = finalize_report(report)
        self.assertIn("AUDIT_CHAIN_INVALID", validate_report(report).reason_codes)

    def test_zero_trade_report_cannot_claim_executed_replay(self) -> None:
        report = build_morning_report(NOW)
        report["chronological_replay"]["events"][-1]["kind"] = "EXIT"
        report = finalize_report(report)
        self.assertIn("REPLAY_STATE_MISMATCH", validate_report(report).reason_codes)

    def test_rehashed_report_cannot_hide_replay_time_tampering(self) -> None:
        report = build_morning_report(NOW)
        report["chronological_replay"]["events"][3]["received_time"] = (
            "2026-07-28T19:00:00+00:00"
        )
        report = finalize_report(report)
        self.assertIn("REPLAY_LINEAGE_INVALID", validate_report(report).reason_codes)

    def test_replay_artifacts_must_match_candidate_control_artifacts(self) -> None:
        report = build_morning_report(NOW)
        report["chronological_replay"]["events"][4]["artifact_id"] = "wrong-risk"
        report = finalize_report(report)
        self.assertIn(
            "REPLAY_ARTIFACT_LINEAGE_MISMATCH",
            validate_report(report).reason_codes,
        )

    def test_missing_war_game_manifest_is_blocked(self) -> None:
        report = build_morning_report(NOW)
        report["war_games"].pop("fixture_manifest")
        report = finalize_report(report)
        self.assertIn("WAR_GAME_MANIFEST_INVALID", validate_report(report).reason_codes)

    def test_rehashed_outer_report_cannot_hide_war_game_metric_tampering(self) -> None:
        report = build_morning_report(NOW)
        report["war_games"]["summary"]["arbitrage_policy_metrics"]["total_pnl"] = "999"
        report = finalize_report(report)
        self.assertIn("WAR_GAME_DISCLOSURE_INVALID", validate_report(report).reason_codes)

    def test_recomputed_inner_hash_cannot_hide_war_game_tampering(self) -> None:
        report = build_morning_report(NOW)
        war_games = report["war_games"]
        war_games["premium"][0]["net_pnl"] = "999"
        payload = {
            key: value for key, value in war_games.items()
            if key != "war_game_report_sha256"
        }
        war_games["war_game_report_sha256"] = sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        report = finalize_report(report)
        self.assertIn("WAR_GAME_DISCLOSURE_INVALID", validate_report(report).reason_codes)

    def test_incomplete_data_batch_is_blocked(self) -> None:
        report = build_morning_report(NOW)
        report["data_batch"]["status"] = "INCOMPLETE"
        report = finalize_report(report)
        self.assertIn("DATA_BATCH_NOT_READY", validate_report(report).reason_codes)

    def test_rehashed_report_cannot_hide_source_batch_tampering(self) -> None:
        report = build_morning_report(NOW)
        report["data_batch"]["source_results"][0]["artifact_sha256"] = "f" * 64
        report = finalize_report(report)
        self.assertIn("DATA_BATCH_NOT_READY", validate_report(report).reason_codes)

    def test_human_cannot_relabel_live_release_as_authorized(self) -> None:
        report = build_morning_report(NOW)
        report["release_readiness"]["live_transition_authorized"] = True
        report = finalize_report(report)
        self.assertIn(
            "LIVE_RELEASE_DISCLOSURE_INVALID", validate_report(report).reason_codes
        )

    def test_human_markdown_leads_with_actual_zero_money_status(self) -> None:
        markdown = render_morning_markdown(build_morning_report(NOW))
        self.assertIn("Real money P&L: $0", markdown)
        self.assertIn("Real trades executed: 0", markdown)
        self.assertIn("Premium synthetic total P&L: $-848.00", markdown)
        self.assertIn("NO_TRADE controls: 39", markdown)
        self.assertIn("Combined-MVP capital stress", markdown)
        self.assertIn("Starting synthetic capital: $100000", markdown)
        self.assertIn("BIG proposal (agent research)", markdown)
        self.assertIn("finite-capital-ruin-approximation 0.1.0-unvalidated", markdown)
        self.assertIn("Validated risk-input artifact", markdown)
        self.assertIn("Code commit: `LOCAL_UNSPECIFIED`", markdown)
        self.assertIn("Live release status: LIVE_RELEASE_BLOCKED", markdown)
        self.assertIn("Live transition authorized: false", markdown)
        self.assertIn("Paper Back Office reconciliation: pass", markdown)
        self.assertIn("Paper reconciliation live-release eligible: false", markdown)
        self.assertIn("Premium new-entry evaluation allowed: true", markdown)
        self.assertIn("Premium monitoring allowed: true", markdown)
        self.assertIn("Earnings option-arm synthetic total: $-312.00", markdown)
        self.assertIn("Arbitrage gated-policy synthetic total: $45", markdown)
        self.assertIn("Dividend shares-arm synthetic total: $-1083.00", markdown)

    def test_rehashed_premium_cadence_tamper_is_blocked(self) -> None:
        report = build_morning_report(NOW)
        report["premium_cadence"]["monitoring_allowed"] = False
        report = finalize_report(report)
        self.assertIn("PREMIUM_CADENCE_INVALID", validate_report(report).reason_codes)

    def test_unpublishable_report_cannot_be_rendered(self) -> None:
        report = build_morning_report(NOW)
        report["environment"] = "live"
        with self.assertRaises(ValueError):
            render_morning_markdown(report)

    def test_fabricated_stat_inference_is_blocked(self) -> None:
        report = build_morning_report(NOW)
        report["stat_evaluation"]["p_value"] = "0.001"
        report = finalize_report(report)
        self.assertIn("STAT_DISCLOSURE_INVALID", validate_report(report).reason_codes)

    def test_tampered_portfolio_stress_disclosure_is_blocked(self) -> None:
        report = build_morning_report(NOW)
        report["portfolio_stress"]["real_money_pnl"] = "1"
        report = finalize_report(report)
        self.assertIn(
            "PORTFOLIO_STRESS_DISCLOSURE_INVALID",
            validate_report(report).reason_codes,
        )

    def test_rehashed_back_office_reconciliation_tamper_is_blocked(self) -> None:
        report = build_morning_report(NOW)
        report["back_office_reconciliation"]["broker_cash"] = "999"
        report = finalize_report(report)
        self.assertIn(
            "BACK_OFFICE_RECONCILIATION_INVALID",
            validate_report(report).reason_codes,
        )

    def test_rehashed_reconciliation_lineage_tamper_is_blocked(self) -> None:
        report = build_morning_report(NOW)
        premium = report["projects"][0]
        compliance = next(
            layer for layer in premium["layers"]
            if layer["layer"] == "DETERMINISTIC_COMPLIANCE"
        )
        compliance["metrics"]["paper_reconciliation_artifact"] = "f" * 64
        report = finalize_report(report)
        self.assertIn(
            "BACK_OFFICE_RECONCILIATION_LINEAGE_MISMATCH",
            validate_report(report).reason_codes,
        )

    def test_rehashed_outer_report_cannot_hide_tampered_stress_metrics(self) -> None:
        report = build_morning_report(NOW)
        report["portfolio_stress"]["descriptive_metrics"]["maximum_drawdown"] = "0"
        report = finalize_report(report)
        self.assertIn(
            "PORTFOLIO_STRESS_DISCLOSURE_INVALID",
            validate_report(report).reason_codes,
        )

    def test_recomputed_inner_hash_cannot_hide_stress_scenario_tampering(self) -> None:
        report = build_morning_report(NOW)
        stress = report["portfolio_stress"]
        stress["scenarios"][0]["combined_net_pnl"] = "999"
        payload = {
            key: value for key, value in stress.items()
            if key != "stress_report_sha256"
        }
        stress["stress_report_sha256"] = sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        report = finalize_report(report)
        self.assertIn(
            "PORTFOLIO_STRESS_DISCLOSURE_INVALID",
            validate_report(report).reason_codes,
        )

    def test_run_comparison_is_deterministic_and_never_claims_real_profit(self) -> None:
        previous = build_morning_report(NOW)
        current = build_morning_report(NOW)
        first = compare_morning_reports(previous, current)
        second = compare_morning_reports(previous, current)
        self.assertEqual(first, second)
        self.assertEqual(first["project_disposition_changes"], [])
        self.assertEqual(first["real_money_pnl_change"], "0")
        self.assertEqual(first["real_trades_executed_change"], 0)
        self.assertEqual(len(first["comparison_sha256"]), 64)

    def test_run_comparison_rejects_tampered_input(self) -> None:
        previous = build_morning_report(NOW)
        current = deepcopy(previous)
        current["summary"]["no_trade"] = 999
        with self.assertRaises(ValueError):
            compare_morning_reports(previous, current)


if __name__ == "__main__":
    unittest.main()
