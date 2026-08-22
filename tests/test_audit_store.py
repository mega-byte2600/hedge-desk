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


if __name__ == "__main__":
    unittest.main()
