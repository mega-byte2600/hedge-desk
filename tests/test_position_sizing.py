"""Deterministic tests for the small-desk position filter (GP rules)."""

import unittest
from hedge_desk.position_sizing import evaluate_premium


class PremiumFilterTests(unittest.TestCase):
    def test_equity_is_required_not_invented(self):
        with self.assertRaises(ValueError):
            evaluate_premium("76", "500", "90", "", 34)

    def test_big_capital_flagged(self):
        # Cash-secured put collateral offsets by credit. A $60 strike at ~zero
        # credit requires $6,000 (> the $5k GP cap) -> flagged.
        r = evaluate_premium("0", "500", "60", "25000", 34)
        self.assertIn("CAPITAL_OVER_5K", r["reasons"])
        self.assertFalse(r["fits_gp_rules"])
        self.assertEqual(r["collateral_required"], "6000.00")

    def test_small_underlying_under_5k(self):
        # $45 strike -> $4500 collateral, under cap.
        r = evaluate_premium("40", "200", "45", "25000", 34)
        self.assertNotIn("CAPITAL_OVER_5K", r["reasons"])

    def test_dte_band(self):
        self.assertIn("DTE_OUTSIDE_30_45", evaluate_premium("40", "200", "45", "25000", 20)["reasons"])

    def test_never_authorizes(self):
        self.assertFalse(evaluate_premium("40", "200", "45", "25000", 34)["trade_authorized"])


if __name__ == "__main__":
    unittest.main()