"""Deterministic reference cases for the market-implied win-probability model."""

import unittest
from datetime import date, datetime, timezone
from decimal import Decimal

from hedge_desk.risk.win_probability import (
    MODEL_ID,
    MODEL_VERSION,
    implied_volatility,
    win_probability_for_short_put,
)


class WinProbabilityTests(unittest.TestCase):
    def test_10pct_otm_put_high_win_probability(self):
        # CCL-like: spot 22.29, short 20 put, 34 DTE, mid 0.415.
        r = win_probability_for_short_put(
            spot=Decimal("22.29"), strike=Decimal("20"),
            expiration=date(2026, 10, 30),
            as_of=datetime(2026, 9, 26, 14, 47, tzinfo=timezone.utc),
            option_mid_price=Decimal("0.415"),
        )
        self.assertGreater(r.win_probability, Decimal("0.70"))
        self.assertLess(r.win_probability, Decimal("0.90"))
        self.assertLess(r.put_delta, Decimal("0"))
        self.assertEqual(r.model_id, MODEL_ID)
        self.assertEqual(r.model_version, MODEL_VERSION)

    def test_at_the_money_put_about_half(self):
        # ATM put: win probability ~0.5.
        r = win_probability_for_short_put(
            spot=Decimal("100"), strike=Decimal("100"),
            expiration=date(2026, 10, 30),
            as_of=datetime(2026, 9, 26, 14, 47, tzinfo=timezone.utc),
            option_mid_price=Decimal("3.00"),
        )
        self.assertGreater(r.win_probability, Decimal("0.40"))
        self.assertLess(r.win_probability, Decimal("0.60"))

    def test_deep_otm_put_high_win(self):
        # Deep OTM put: win probability high.
        r = win_probability_for_short_put(
            spot=Decimal("100"), strike=Decimal("80"),
            expiration=date(2026, 10, 30),
            as_of=datetime(2026, 9, 26, 14, 47, tzinfo=timezone.utc),
            option_mid_price=Decimal("0.20"),
        )
        self.assertGreater(r.win_probability, Decimal("0.90"))

    def test_invalid_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            win_probability_for_short_put(
                spot=Decimal("0"), strike=Decimal("20"),
                expiration=date(2026, 10, 30),
                as_of=datetime(2026, 9, 26, 14, 47, tzinfo=timezone.utc),
                option_mid_price=Decimal("0.415"),
            )
        with self.assertRaises(ValueError):
            win_probability_for_short_put(
                spot=Decimal("22.29"), strike=Decimal("20"),
                expiration=date(2026, 9, 20),  # before as_of
                as_of=datetime(2026, 9, 26, 14, 47, tzinfo=timezone.utc),
                option_mid_price=Decimal("0.415"),
            )

    def test_implied_volatility_roundtrip(self):
        # A known price should back out a positive IV.
        iv = implied_volatility(0.415, 22.29, 20.0, 34 / 365.0, 0.0)
        self.assertIsNotNone(iv)
        self.assertGreater(iv, 0.1)
        self.assertLess(iv, 2.0)


if __name__ == "__main__":
    unittest.main()


class RiskNeutralReferenceCases(unittest.TestCase):
    """Hull, Options Futures and Other Derivatives, Example 15.6:
    S=42, K=40, r=10%, sigma=20%, T=0.5 -> d1=0.7693, d2=0.6278,
    put price 0.81, N(d2)=0.7349 (risk-neutral P(S_T > K))."""

    def test_hull_example_d2_and_cdf(self):
        from hedge_desk.risk.win_probability import _bs_d2, _bs_put_price, _norm_cdf

        self.assertAlmostEqual(_bs_d2(42, 40, 0.5, 0.10, 0.20), 0.6278, places=4)
        self.assertAlmostEqual(_norm_cdf(0.6278), 0.7349, places=4)
        self.assertAlmostEqual(_bs_put_price(42, 40, 0.5, 0.10, 0.20), 0.81, places=2)
        self.assertEqual(_norm_cdf(0.0), 0.5)

    def test_delta_rule_overstates_short_put_win_probability(self):
        from datetime import date, datetime, timezone
        from decimal import Decimal

        from hedge_desk.risk.win_probability import win_probability_for_short_put

        r = win_probability_for_short_put(
            spot=Decimal("100"), strike=Decimal("95"), expiration=date(2026, 12, 18),
            as_of=datetime(2026, 11, 18, 21, 0, tzinfo=timezone.utc),
            option_mid_price=Decimal("1.20"))
        self.assertIsNotNone(r.risk_neutral_win_probability)
        self.assertLess(r.risk_neutral_win_probability, r.win_probability)
        self.assertAlmostEqual(float(r.win_probability - r.risk_neutral_win_probability), 0.0256, places=3)
        self.assertEqual(r.model_version, "1.0.0")  # gate value unchanged
