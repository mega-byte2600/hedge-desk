"""Console export must retain the engine's publication boundary."""
import copy
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from scripts.build_web import export_report
from hedge_desk.overnight import build_morning_report


class WebExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = build_morning_report(datetime(2026, 9, 6, tzinfo=timezone.utc), 'fixed-test-commit')

    def test_valid_export_preserves_immutable_engine_result(self):
        with tempfile.TemporaryDirectory() as folder:
            export_report(self.report, folder)
            result = json.loads((Path(folder) / 'report.json').read_text())
            self.assertEqual(result['report'], json.loads(json.dumps(self.report)))
            self.assertEqual(result['summary']['report_sha256'], self.report['report_sha256'])
            self.assertEqual(len(result['registry']), 6)
            self.assertFalse(result['report']['live_orders_enabled'])

    def test_tampered_report_does_not_replace_published_snapshot(self):
        with tempfile.TemporaryDirectory() as folder:
            export_report(self.report, folder)
            original = (Path(folder) / 'report.json').read_bytes()
            modified = copy.deepcopy(self.report)
            modified['projects'][0]['layers'][3]['metrics']['risk_of_ruin'] = '0.2'
            with self.assertRaises(ValueError):
                export_report(modified, folder)
            self.assertEqual((Path(folder) / 'report.json').read_bytes(), original)

    def test_live_report_cannot_be_exported(self):
        modified = copy.deepcopy(self.report)
        modified['live_orders_enabled'] = True
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                export_report(modified, folder)
            self.assertFalse((Path(folder) / 'report.json').exists())
