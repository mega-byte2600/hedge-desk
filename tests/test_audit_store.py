from pathlib import Path
import tempfile
import unittest

from hedge_desk.audit import append_audit_event, build_reference_audit
from hedge_desk.audit_store import (
    append_audit_journal,
    initialize_audit_journal,
    read_audit_journal,
)


class AuditJournalTests(unittest.TestCase):
    def test_initialize_read_append_and_duplicate_suppression(self) -> None:
        chain = build_reference_audit()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.jsonl"
            created = initialize_audit_journal(path, chain)
            self.assertEqual(created.status, "INITIALIZED")
            self.assertEqual(read_audit_journal(path), chain)
            duplicate = append_audit_journal(path, chain[-1])
            self.assertEqual(duplicate.status, "DUPLICATE_SUPPRESSED")
            extended = append_audit_event(
                chain, chain[-1].run_id, "MORNING_REPORT", chain[-1].occurred_at,
                "morning-report", chain[-1].candidate_id, chain[-1].output_sha256,
                "f" * 64, "reporter-1.0.0", "paper-report-1.0.0",
            )
            appended = append_audit_journal(path, extended[-1])
            self.assertEqual(appended.status, "APPENDED")
            self.assertEqual(read_audit_journal(path), extended)

    def test_existing_or_corrupt_journal_fails_closed(self) -> None:
        chain = build_reference_audit()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.jsonl"
            initialize_audit_journal(path, chain)
            self.assertEqual(initialize_audit_journal(path, chain).status, "BLOCKED")
            with path.open("a", encoding="utf-8") as stream:
                stream.write("{corrupt}\n")
            with self.assertRaisesRegex(ValueError, "AUDIT_JOURNAL_CORRUPT"):
                read_audit_journal(path)
            self.assertEqual(append_audit_journal(path, chain[-1]).status, "BLOCKED")

    def test_empty_journal_and_empty_initialization_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.jsonl"
            self.assertEqual(
                initialize_audit_journal(path, ()).reason_codes,
                ("AUDIT_JOURNAL_EMPTY",),
            )
            path.write_text("", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "AUDIT_JOURNAL_EMPTY"):
                read_audit_journal(path)

    def test_missing_parent_returns_write_failure_not_exception(self) -> None:
        chain = build_reference_audit()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing" / "audit.jsonl"
            result = initialize_audit_journal(path, chain)
            self.assertEqual(result.status, "BLOCKED")
            self.assertEqual(result.reason_codes, ("AUDIT_JOURNAL_WRITE_FAILED",))


if __name__ == "__main__":
    unittest.main()
