"""Deterministic tests for the Yellow Sheet decision artifact (no network)."""

import json
import os
import tempfile
import unittest
from datetime import datetime, timezone

from hedge_desk.yellow_sheet import (record_yellow_sheet, read_yellow_sheets,
                                     summarize_yellow_sheets)


class YellowSheetTests(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".jsonl")
        os.close(fd)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def _risk_state(self):
        return {"strategy": "CASH_SECURED_PUT", "strike": "32", "dte": 34,
                "collateral_required": "3200.00", "return_on_capital": "0.0128",
                "survivability": "INDETERMINATE", "fits_gp_rules": True}

    def test_record_and_read_roundtrip(self):
        t = datetime(2026, 9, 19, tzinfo=timezone.utc)
        e = record_yellow_sheet(
            self.path, symbol="NKE", strategy="CASH_SECURED_PUT",
            thesis="Collect premium; defined-risk put ~10% OTM.",
            invalidation="Underlying gaps below strike within the DTE.",
            planned_exit="Let expire worthless at 34 DTE.",
            risk_state=self._risk_state(), bound_report_sha256="ab" * 32,
            recorded_at=t)
        self.assertFalse(e["trade_authorized"])
        self.assertIn("risk_state", e)
        self.assertEqual(len(e["entry_sha256"]), 64)
        sheets = read_yellow_sheets(self.path)
        self.assertEqual(len(sheets), 1)
        self.assertEqual(sheets[0]["symbol"], "NKE")
        self.assertEqual(sheets[0]["risk_state"]["return_on_capital"], "0.0128")

    def test_requires_thesis_and_invalidation(self):
        with self.assertRaises(ValueError):
            record_yellow_sheet(self.path, symbol="NKE", strategy="CASH_SECURED_PUT",
                                thesis="", invalidation="", decision="PAPER_OPEN")

    def test_rejects_unknown_decision(self):
        with self.assertRaises(ValueError):
            record_yellow_sheet(self.path, symbol="NKE", strategy="CASH_SECURED_PUT",
                                thesis="t", invalidation="i", decision="BOUGHT")

    def test_rejects_non_mapping_risk_state(self):
        with self.assertRaises(ValueError):
            record_yellow_sheet(self.path, symbol="NKE", strategy="CASH_SECURED_PUT",
                                thesis="t", invalidation="i",
                                risk_state="3200.00")

    def test_detects_tamper(self):
        record_yellow_sheet(self.path, symbol="NKE", strategy="CASH_SECURED_PUT",
                            thesis="t", invalidation="i")
        lines = open(self.path).read().splitlines()
        entry = json.loads(lines[0])
        entry["thesis"] = "CHANGED"
        with open(self.path, "w") as fh:
            fh.write(json.dumps(entry, sort_keys=True) + "\n")
        with self.assertRaises(ValueError):
            read_yellow_sheets(self.path)

    def test_summary_ledger(self):
        for _ in range(2):
            record_yellow_sheet(self.path, symbol="NKE", strategy="CASH_SECURED_PUT",
                                thesis="t", invalidation="i")
        record_yellow_sheet(self.path, symbol="AAL", strategy="CASH_SECURED_PUT",
                            thesis="t", invalidation="i", decision="NO_TRADE")
        s = summarize_yellow_sheets(self.path)
        self.assertEqual(s["sheet_count"], 3)
        self.assertEqual(s["by_decision"]["PAPER_OPEN"], 2)
        self.assertEqual(s["by_decision"]["NO_TRADE"], 1)


if __name__ == "__main__":
    unittest.main()