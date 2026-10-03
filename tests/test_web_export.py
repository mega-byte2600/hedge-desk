"""Static export must never carry synthetic data (fail-closed stub)."""
import json
import tempfile
import unittest
from pathlib import Path
from scripts.build_web import export_report


class WebExportTests(unittest.TestCase):
    def test_export_writes_fail_closed_stub(self):
        with tempfile.TemporaryDirectory() as folder:
            stub = export_report({}, folder)
            self.assertEqual(stub["status"], "data_unavailable")
            self.assertFalse(stub["synthetic_data"])
            on_disk = json.loads((Path(folder) / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(on_disk["status"], "data_unavailable")

    def test_export_never_embeds_report_content(self):
        # Even if handed a full report, the static export must not embed it:
        # the console loads live data from /api/report.
        fake_report = {"report_type": "paper_hypothetical_morning_evaluation",
                       "projects": [{"project_id": "x"}]}
        with tempfile.TemporaryDirectory() as folder:
            export_report(fake_report, folder)
            text = (Path(folder) / "report.json").read_text(encoding="utf-8")
            self.assertNotIn("paper_hypothetical", text)
            self.assertNotIn("project_id", text)
