from datetime import datetime, timezone
import unittest

from hedge_desk.overnight import build_morning_report
from hedge_desk.scheduler import (
    ScheduledRunRequest,
    ScheduledRunStatus,
    execute_scheduled_run,
)


NOW = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)


class SchedulerTests(unittest.TestCase):
    def test_paper_run_completes_with_report_hash(self) -> None:
        receipts = execute_scheduled_run(
            ScheduledRunRequest("run-1", NOW), (), build_morning_report
        )
        self.assertIs(receipts[-1].status, ScheduledRunStatus.COMPLETE)
        self.assertEqual(len(receipts[-1].report_sha256 or ""), 64)

    def test_duplicate_delivery_is_suppressed(self) -> None:
        request = ScheduledRunRequest("run-1", NOW)
        receipts = execute_scheduled_run(request, (), build_morning_report)
        receipts = execute_scheduled_run(request, receipts, build_morning_report)
        self.assertIs(receipts[-1].status, ScheduledRunStatus.DUPLICATE_SUPPRESSED)
        self.assertEqual(receipts[-1].reason_codes, ("DUPLICATE_RUN_SUPPRESSED",))

    def test_live_environment_fails_closed_without_calling_builder(self) -> None:
        called = False

        def builder(_):
            nonlocal called
            called = True
            return {}

        receipts = execute_scheduled_run(
            ScheduledRunRequest("live-1", NOW, environment="live"), (), builder
        )
        self.assertFalse(called)
        self.assertIs(receipts[-1].status, ScheduledRunStatus.FAILED_CLOSED)
        self.assertEqual(receipts[-1].reason_codes, ("PAPER_ONLY_VIOLATION",))

    def test_evaluator_exception_fails_closed(self) -> None:
        def broken(_):
            raise RuntimeError("synthetic evaluator failure")

        receipts = execute_scheduled_run(
            ScheduledRunRequest("broken-1", NOW), (), broken
        )
        self.assertIs(receipts[-1].status, ScheduledRunStatus.FAILED_CLOSED)
        self.assertEqual(receipts[-1].reason_codes, ("EVALUATION_EXCEPTION",))
        self.assertIsNone(receipts[-1].report_sha256)


if __name__ == "__main__":
    unittest.main()
