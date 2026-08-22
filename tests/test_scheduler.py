from dataclasses import replace
from datetime import datetime, timezone
import unittest

from hedge_desk.overnight import build_morning_report
from hedge_desk.demo import json_value
from hedge_desk.scheduler import (
    ScheduledRunRequest,
    ScheduledRunStatus,
    execute_scheduled_run,
    validate_scheduled_run_receipt,
    validate_serialized_scheduled_run_receipt,
)


NOW = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)


class SchedulerTests(unittest.TestCase):
    def test_forged_prior_receipt_cannot_suppress_or_authorize_run(self) -> None:
        request = ScheduledRunRequest("run-1", NOW)
        forged = replace(
            execute_scheduled_run(request, (), lambda _: build_morning_report(NOW))[-1],
            receipt_sha256="f" * 64,
        )
        result = execute_scheduled_run(
            ScheduledRunRequest("run-2", NOW),
            (forged,),
            lambda _: build_morning_report(NOW),
        )[-1]
        self.assertIs(result.status, ScheduledRunStatus.FAILED_CLOSED)
        self.assertEqual(result.reason_codes, ("PRIOR_RECEIPT_INVALID",))

    def test_paper_run_completes_with_report_hash(self) -> None:
        receipts = execute_scheduled_run(
            ScheduledRunRequest("run-1", NOW), (), build_morning_report
        )
        self.assertIs(receipts[-1].status, ScheduledRunStatus.COMPLETE)
        self.assertEqual(len(receipts[-1].report_sha256 or ""), 64)
        self.assertEqual(validate_scheduled_run_receipt(receipts[-1]), ())
        self.assertEqual(
            validate_serialized_scheduled_run_receipt(json_value(receipts[-1])), ()
        )
        self.assertEqual(len(receipts[-1].receipt_sha256), 64)

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

    def test_failed_run_can_recover_once_under_new_bound_identity(self) -> None:
        def broken(_):
            raise RuntimeError("synthetic interruption")

        receipts = execute_scheduled_run(
            ScheduledRunRequest("run-1", NOW), (), broken
        )
        recovery = ScheduledRunRequest("run-1-recovery-1", NOW, recovery_of="run-1")
        receipts = execute_scheduled_run(recovery, receipts, build_morning_report)
        self.assertIs(receipts[-1].status, ScheduledRunStatus.COMPLETE)
        self.assertEqual(receipts[-1].recovery_of, "run-1")
        receipts = execute_scheduled_run(recovery, receipts, build_morning_report)
        self.assertIs(receipts[-1].status, ScheduledRunStatus.DUPLICATE_SUPPRESSED)

    def test_recovery_requires_matching_failed_source_run(self) -> None:
        recovery = ScheduledRunRequest("recovery-1", NOW, recovery_of="missing")
        receipts = execute_scheduled_run(recovery, (), build_morning_report)
        self.assertIs(receipts[-1].status, ScheduledRunStatus.FAILED_CLOSED)
        self.assertEqual(receipts[-1].reason_codes, ("INVALID_RECOVERY_REQUEST",))
        self.assertIsNone(receipts[-1].report_sha256)

    def test_receipt_status_and_report_tampering_is_detected(self) -> None:
        receipt = execute_scheduled_run(
            ScheduledRunRequest("run-1", NOW), (), build_morning_report
        )[-1]
        tampered = replace(receipt, report_sha256="f" * 64)
        self.assertIn(
            "SCHEDULER_RECEIPT_HASH_MISMATCH",
            validate_scheduled_run_receipt(tampered),
        )
        invalid_state = replace(
            receipt,
            status=ScheduledRunStatus.FAILED_CLOSED,
        )
        self.assertIn(
            "SCHEDULER_NONCOMPLETE_REPORT_HASH_PRESENT",
            validate_scheduled_run_receipt(invalid_state),
        )


if __name__ == "__main__":
    unittest.main()
