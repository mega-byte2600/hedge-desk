from datetime import datetime, timezone
from decimal import Decimal
import unittest

from hedge_desk.backoffice import (
    BackOfficeStatus,
    evaluate_paper_reconciliation,
    serialize_paper_reconciliation,
    validate_serialized_paper_reconciliation,
)


NOW = datetime(2026, 8, 22, 12, 0, tzinfo=timezone.utc)


def reconcile(**changes):
    values = {
        "plan_sha256": "a" * 64,
        "internal_positions_sha256": "b" * 64,
        "broker_positions_sha256": "b" * 64,
        "internal_cash": Decimal("100118.70"),
        "broker_cash": Decimal("100118.70"),
        "unresolved_fill_count": 0,
        "unresolved_lifecycle_count": 0,
        "reconciled_at": NOW,
    }
    values.update(changes)
    return evaluate_paper_reconciliation(**values)


class BackOfficeReconciliationTests(unittest.TestCase):
    def test_nonfinite_cash_cannot_reconcile(self) -> None:
        for value in (Decimal("Infinity"), Decimal("-Infinity"), Decimal("NaN")):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "finite"):
                evaluate_paper_reconciliation(
                    "a" * 64, "b" * 64, "b" * 64,
                    value, value, 0, 0, NOW,
                )

    def test_exact_paper_ledgers_reconcile_but_never_certify_live_release(self) -> None:
        result = reconcile()
        self.assertIs(result.status, BackOfficeStatus.PASS)
        self.assertEqual(result.reason_codes, ())
        self.assertFalse(result.live_release_evidence_eligible)
        self.assertEqual(len(result.artifact_sha256), 64)
        self.assertEqual(result, reconcile())

    def test_cash_position_and_exception_mismatches_block_together(self) -> None:
        result = reconcile(
            broker_positions_sha256="c" * 64,
            broker_cash=Decimal("100118.69"),
            unresolved_fill_count=1,
            unresolved_lifecycle_count=2,
        )
        self.assertIs(result.status, BackOfficeStatus.BLOCK)
        self.assertEqual(result.reason_codes, (
            "CASH_LEDGER_MISMATCH",
            "POSITION_LEDGER_MISMATCH",
            "UNRESOLVED_FILL_EXCEPTIONS",
            "UNRESOLVED_LIFECYCLE_EXCEPTIONS",
        ))
        self.assertFalse(result.live_release_evidence_eligible)

    def test_bad_plan_or_live_environment_fails_closed(self) -> None:
        result = reconcile(plan_sha256="0" * 64, environment="live")
        self.assertIs(result.status, BackOfficeStatus.BLOCK)
        self.assertIn("RECONCILIATION_PLAN_HASH_INVALID", result.reason_codes)
        self.assertIn(
            "PAPER_RECONCILIATION_ENVIRONMENT_REQUIRED", result.reason_codes
        )

    def test_non_decimal_cash_or_negative_exception_count_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "cash values must be Decimal"):
            reconcile(internal_cash=100)  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            reconcile(unresolved_fill_count=-1)

    def test_serialized_artifact_is_reconstructed_and_tamper_detected(self) -> None:
        serialized = serialize_paper_reconciliation(reconcile())
        self.assertEqual(validate_serialized_paper_reconciliation(serialized), ())
        serialized["broker_cash"] = "999"
        self.assertIn(
            "BACK_OFFICE_RECONCILIATION_ARTIFACT_INVALID",
            validate_serialized_paper_reconciliation(serialized),
        )


if __name__ == "__main__":
    unittest.main()
