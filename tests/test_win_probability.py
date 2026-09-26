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
