"""Deterministic tests for the paper outcome log (no network)."""

import json
import os
import tempfile
import unittest
from datetime import datetime, timezone

from hedge_desk.paper_log import (ALLOWED_OUTCOMES, append_outcome, read_log,
                                  summarize)


class PaperLogTests(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".jsonl")
        os.close(fd)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_append_and_read_roundtrip(self):
        t = datetime(2026, 9, 19, tzinfo=timezone.utc)
        e = append_outcome(self.path, candidate_id="SPY261023P00762000",
                           symbol="SPY", strategy="CASH_SECURED_PUT",
                           outcome="EXPIRED_WORTHLESS", entered_at=t,
                           premium_received="9.91")
        self.assertFalse(e["trade_authorized"])
        self.assertTrue(e["entry_sha256"])
        entries = read_log(self.path)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["symbol"], "SPY")
        self.assertEqual(entries[0]["outcome"], "EXPIRED_WORTHLESS")

    def test_rejects_unknown_outcome(self):
        with self.assertRaises(ValueError):
            append_outcome(self.path, candidate_id="X", symbol="SPY",
                           strategy="CASH_SECURED_PUT", outcome="MADE_MONEY")

    def test_rejects_naive_entered_at(self):
        from datetime import datetime as naive_dt
        with self.assertRaises(ValueError):
            append_outcome(self.path, candidate_id="X", symbol="SPY",
                           strategy="CREDIT_SPREAD", outcome="ENTERED_PAPER",
                           entered_at=naive_dt(2026, 9, 19))

    def test_detects_tamper(self):
        append_outcome(self.path, candidate_id="SPY261023P00762000",
                       symbol="SPY", strategy="CASH_SECURED_PUT",
                       outcome="ENTERED_PAPER")
        # corrupt the outcome in-place without recomputing the hash
        lines = open(self.path).read().splitlines()
        entry = json.loads(lines[0])
        entry["outcome"] = "EXPIRED_WORTHLESS"
        with open(self.path, "w") as fh:
            fh.write(json.dumps(entry, sort_keys=True) + "\n")
        with self.assertRaises(ValueError):
            read_log(self.path)

    def test_summary_tallies_not_performance(self):
        for oc in ("ENTERED_PAPER", "EXPIRED_WORTHLESS", "EXPIRED_WORTHLESS"):
            append_outcome(self.path, candidate_id="C1", symbol="SPY",
                           strategy="CASH_SECURED_PUT", outcome=oc)
        s = summarize(self.path)
        self.assertEqual(s["entry_count"], 3)
        self.assertEqual(s["outcome_counts"]["EXPIRED_WORTHLESS"], 2)
        self.assertNotIn("pnl", s)
        self.assertNotIn("return", s)

    def test_append_only_sequences(self):
        for i in range(3):
            append_outcome(self.path, candidate_id=f"C{i}", symbol="SPY",
                           strategy="CASH_SECURED_PUT", outcome="UNKNOWN")
        seqs = [e["seq"] for e in read_log(self.path)]
        self.assertEqual(seqs, [1, 2, 3])


if __name__ == "__main__":
    unittest.main()