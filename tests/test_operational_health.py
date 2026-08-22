from copy import deepcopy
from datetime import datetime, timedelta, timezone
import unittest

from hedge_desk.demo import json_value
from hedge_desk.operational_health import evaluate_paper_run_health
from hedge_desk.overnight import build_morning_report
from hedge_desk.scheduler import ScheduledRunRequest, execute_scheduled_run


NOW = datetime(2026, 8, 22, 9, 0, tzinfo=timezone.utc)
COMMIT = "a" * 40


def artifacts():
    report = build_morning_report(NOW, COMMIT)
    receipt = json_value(execute_scheduled_run(
        ScheduledRunRequest("health-run", NOW), (), lambda _: report
    )[-1])
    audit = report["audit_chain"]
    return report, receipt, audit["event_count"], audit["head_hash"]


class OperationalHealthTests(unittest.TestCase):
    def test_complete_fresh_consistent_run_is_healthy_paper_only(self) -> None:
        report, receipt, count, head = artifacts()
        result = evaluate_paper_run_health(
            report, receipt, count, head, NOW + timedelta(seconds=900), 900, COMMIT
        )
        self.assertEqual(result.status, "HEALTHY_PAPER")
        self.assertFalse(result.live_authorized)
        microsecond_late = evaluate_paper_run_health(
            report, receipt, count, head,
            NOW + timedelta(seconds=900, microseconds=1), 900, COMMIT,
        )
        self.assertIn("LATEST_RUN_STALE", microsecond_late.reason_codes)
        self.assertEqual(microsecond_late.report_age_seconds, 901)

    def test_stale_commit_or_journal_mismatch_blocks(self) -> None:
        report, receipt, count, head = artifacts()
        result = evaluate_paper_run_health(
            report, receipt, count + 1, head, NOW + timedelta(seconds=901), 900,
            "b" * 40,
        )
        self.assertIn("LATEST_RUN_STALE", result.reason_codes)
        self.assertIn("CODE_COMMIT_MISMATCH", result.reason_codes)
        self.assertIn("AUDIT_JOURNAL_REPORT_MISMATCH", result.reason_codes)

    def test_live_flag_and_receipt_tamper_fail_closed(self) -> None:
        report, receipt, count, head = artifacts()
        attacked = deepcopy(report)
        attacked["live_orders_enabled"] = True
        receipt["report_sha256"] = "f" * 64
        result = evaluate_paper_run_health(
            attacked, receipt, count, head, NOW, 900, COMMIT
        )
        self.assertIn("PAPER_ONLY_VIOLATION", result.reason_codes)
        self.assertIn("REPORT_RECEIPT_HASH_MISMATCH", result.reason_codes)
        self.assertNotEqual(result.status, "HEALTHY_PAPER")
        with self.assertRaisesRegex(ValueError, "nonnegative integer"):
            evaluate_paper_run_health(
                report, receipt, count, head, NOW, True, COMMIT
            )


if __name__ == "__main__":
    unittest.main()
