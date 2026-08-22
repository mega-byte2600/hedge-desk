from copy import deepcopy
from datetime import datetime, timezone
import unittest

from hedge_desk.overnight import build_morning_report
from hedge_desk.reporting import finalize_report, validate_report


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

    def test_missing_war_game_manifest_is_blocked(self) -> None:
        report = build_morning_report(NOW)
        report["war_games"].pop("fixture_manifest")
        report = finalize_report(report)
        self.assertIn("WAR_GAME_MANIFEST_INVALID", validate_report(report).reason_codes)


if __name__ == "__main__":
    unittest.main()
