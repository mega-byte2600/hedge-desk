"""Deterministic tests for the data-freshness gate (no network)."""

import unittest
from datetime import date

from hedge_desk.freshness import expected_trading_day, freshness_summary


class FreshnessTests(unittest.TestCase):
    def test_expected_trading_day_skips_weekend(self):
        # 2026-09-19 is a Saturday -> expected trading day is Friday 09-18.
        self.assertEqual(expected_trading_day(date(2026, 9, 19)), date(2026, 9, 18))
        # a Wednesday stays itself
        self.assertEqual(expected_trading_day(date(2026, 9, 16)), date(2026, 9, 16))

    def test_current_when_as_of_matches_expected(self):
        s = freshness_summary(["2026-09-18"], date(2026, 9, 19))
        self.assertTrue(s["is_current"])
        self.assertEqual(s["as_of"], "2026-09-18")
        self.assertEqual(s["expected_trading_day"], "2026-09-18")

    def test_stale_when_as_of_is_prior_day(self):
        # running on Thursday's close when Friday's is expected -> not current
        s = freshness_summary(["2026-09-17"], date(2026, 9, 18))
        self.assertFalse(s["is_current"])
        self.assertIn("not yet", s["note"])

    def test_no_bars_is_not_current(self):
        s = freshness_summary([], date(2026, 9, 18))
        self.assertFalse(s["is_current"])
        self.assertIsNone(s["as_of"])


if __name__ == "__main__":
    unittest.main()