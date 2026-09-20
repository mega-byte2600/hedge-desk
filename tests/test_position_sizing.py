"""Deterministic tests for the small-desk position filter (GP rules)."""

import unittest
from hedge_desk.position_sizing import evaluate_premium, wheel_fit_for_equity


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

    def test_return_on_capital_is_per_contract_over_dollar_collateral(self):
        # Reference case (NKE): credit 0.41/share, strike 32.
        # collateral = (32 - 0.41)*100 = 3159.00; return_on_capital =
        # credit_per_contract / collateral = 41 / 3159 = 1.298% (in the 0.5-2% band).
        # Regression: this was credit/collateral = 0.41/3159 = 0.013% (100x too small).
        r = evaluate_premium("0.41", "3159", "32", "25000", 34)
        self.assertEqual(r["collateral_required"], "3159.00")
        self.assertEqual(r["return_on_capital"], "0.0130")
        self.assertNotIn("RETURN_NOT_IN_GP_BAND", r["reasons"])


    def test_wheel_fit_scales_with_equity(self):
        # 2% of $25k = $500 max position; 2% of $250k = $5,000.
        self.assertEqual(wheel_fit_for_equity("25000")["max_position_collateral"], "500.00")
        self.assertEqual(wheel_fit_for_equity("250000")["max_position_collateral"], "5000.00")

    def test_wheel_fit_rejects_non_positive_equity(self):
        with self.assertRaises(ValueError):
            wheel_fit_for_equity("0")


if __name__ == "__main__":
    unittest.main()