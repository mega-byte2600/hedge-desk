from copy import deepcopy
from datetime import datetime, timezone
import unittest

from hedge_desk.overnight import build_morning_report
from hedge_desk.reporting import (
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

    def test_tampering_invalidates_report_hash(self) -> None:
        report = build_morning_report(NOW)
        report["summary"]["human_review"] = 99
        self.assertIn("REPORT_HASH_INVALID", validate_report(report).reason_codes)

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

    def test_zero_trade_report_cannot_claim_executed_replay(self) -> None:
        report = build_morning_report(NOW)
        report["chronological_replay"]["events"][-1]["kind"] = "EXIT"
        report = finalize_report(report)
        self.assertIn("REPLAY_STATE_MISMATCH", validate_report(report).reason_codes)

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

    def test_incomplete_data_batch_is_blocked(self) -> None:
        report = build_morning_report(NOW)
        report["data_batch"]["status"] = "INCOMPLETE"
        report = finalize_report(report)
        self.assertIn("DATA_BATCH_NOT_READY", validate_report(report).reason_codes)

    def test_human_markdown_leads_with_actual_zero_money_status(self) -> None:
        markdown = render_morning_markdown(build_morning_report(NOW))
        self.assertIn("Real money P&L: $0", markdown)
        self.assertIn("Real trades executed: 0", markdown)
        self.assertIn("Premium synthetic total P&L: $-848.00", markdown)
        self.assertIn("NO_TRADE controls: 11", markdown)
        self.assertIn("Combined-MVP capital stress", markdown)
        self.assertIn("Starting synthetic capital: $100000", markdown)
        self.assertIn("BIG proposal (agent research)", markdown)
        self.assertIn("finite-capital-ruin-approximation 0.1.0-unvalidated", markdown)
        self.assertIn("Validated risk-input artifact", markdown)
        self.assertIn("Code commit: `LOCAL_UNSPECIFIED`", markdown)
        self.assertIn("Earnings option-arm synthetic total: $-312.00", markdown)
        self.assertIn("Arbitrage gated-policy synthetic total: $45", markdown)
        self.assertIn("Dividend shares-arm synthetic total: $-1083.00", markdown)

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

    def test_rehashed_outer_report_cannot_hide_tampered_stress_metrics(self) -> None:
        report = build_morning_report(NOW)
        report["portfolio_stress"]["descriptive_metrics"]["maximum_drawdown"] = "0"
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
