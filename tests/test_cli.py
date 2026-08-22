import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from hedge_desk.overnight import build_morning_report
from datetime import datetime, timezone


class CliTests(unittest.TestCase):
    def test_markdown_is_rendered_from_exact_json_report_hash(self) -> None:
        report = build_morning_report(
            datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "morning.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "hedge_desk.cli",
                    "--morning-markdown",
                    "--report-input",
                    str(path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        self.assertIn(report["report_sha256"], result.stdout)

    def test_scheduler_receipt_is_bound_to_exact_report_hash(self) -> None:
        report = build_morning_report(
            datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "morning.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable, "-m", "hedge_desk.cli",
                    "--scheduled-receipt", "--idempotency-key", "test-run",
                    "--report-input", str(path),
                ],
                check=True, capture_output=True, text=True,
            )
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["status"], "COMPLETE")
        self.assertEqual(receipt["report_sha256"], report["report_sha256"])


if __name__ == "__main__":
    unittest.main()
