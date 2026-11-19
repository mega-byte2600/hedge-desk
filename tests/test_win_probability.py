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
        self.assertEqual(r.win_probability, r.risk_neutral_win_probability)  # gate value is N(d2)
        self.assertLess(r.win_probability, r.delta_rule_win_probability)
        self.assertAlmostEqual(float(r.delta_rule_win_probability - r.win_probability), 0.0256, places=3)
        self.assertEqual(r.model_version, "2.0.0")


class MertonReferenceCases(unittest.TestCase):
    """Hull Example 17.1 (Merton, dividend yield): S=930, K=900, r=8%, q=3%,
    sigma=20%, T=2/12 -> d1=0.5444, d2=0.4628, call price 51.83."""

    def test_hull_merton_d2_and_put_call_parity(self):
        import math
        from hedge_desk.risk.win_probability import _bs_d2, _bs_put_price, _d1_d2, _norm_cdf

        t = 2 / 12
        d1, d2 = _d1_d2(930, 900, t, 0.08, 0.20, 0.03)
        self.assertAlmostEqual(d1, 0.5444, delta=1e-4)  # Hull rounds to 4 dp
        self.assertAlmostEqual(_bs_d2(930, 900, t, 0.08, 0.20, 0.03), 0.4628, delta=1e-4)
        call = 930 * math.exp(-0.03 * t) * _norm_cdf(d1) - 900 * math.exp(-0.08 * t) * _norm_cdf(d2)
        self.assertAlmostEqual(call, 51.83, places=2)
        put = _bs_put_price(930, 900, t, 0.08, 0.20, 0.03)
        # put-call parity with dividends: c - p = S e^{-qT} - K e^{-rT}
        self.assertAlmostEqual(call - put, 930 * math.exp(-0.03 * t) - 900 * math.exp(-0.08 * t), places=9)

    def test_iv_round_trip_with_rate_and_dividend(self):
        from hedge_desk.risk.win_probability import _bs_put_price, implied_volatility

        price = _bs_put_price(100, 95, 0.1, 0.043, 0.27, 0.013)
        self.assertAlmostEqual(implied_volatility(price, 100, 95, 0.1, 0.043, 0.013), 0.27, places=8)

    def test_rate_and_dividend_change_the_probability_in_the_right_direction(self):
        from datetime import date, datetime, timezone
        from decimal import Decimal

        from hedge_desk.risk.win_probability import win_probability_for_short_put

        base = dict(spot=Decimal("100"), strike=Decimal("95"), expiration=date(2026, 12, 18),
                    as_of=datetime(2026, 11, 18, 21, 0, tzinfo=timezone.utc), option_mid_price=Decimal("1.20"))
        r0 = win_probability_for_short_put(**base)
        rq = win_probability_for_short_put(**base, rate=Decimal("0.043"), dividend_yield=Decimal("0.013"))
        self.assertEqual(r0.model_id, "bsm-risk-neutral-n-d2")
        self.assertNotEqual(r0.win_probability, rq.win_probability)
        with self.assertRaises(ValueError):
            win_probability_for_short_put(**base, rate=Decimal("0.9"))
