import unittest

from hedge_desk.quantdesk.ml_options import (
    OptionQuote,
    black_scholes_price,
    curate_option_quote,
    realized_volatility_20d,
)


class QuantDeskMLOptionsTests(unittest.TestCase):
    def test_black_scholes_call_price_is_reasonable(self):
        price = black_scholes_price("call", 100.0, 100.0, 30 / 365, 0.04, 0.0, 0.20)
        self.assertGreater(price, 1.0)
        self.assertLess(price, 5.0)

    def test_realized_volatility_uses_twenty_day_sequence(self):
        closes = [100.0, 101.0, 99.5, 100.5, 102.0, 103.0, 101.0, 100.0, 99.0, 98.5,
                  99.5, 100.5, 101.5, 102.5, 104.0, 103.5, 102.0, 101.0, 102.0, 103.0]
        vol = realized_volatility_20d(closes)
        self.assertGreater(vol, 0.0)
        self.assertLess(vol, 1.0)

    def test_curated_row_has_bid_ask_and_distilled_labels_but_no_trade_authority(self):
        quote = OptionQuote(
            symbol="spy",
            option_type="call",
            underlying_price=500.0,
            strike=505.0,
            dte=35,
            risk_free_rate=0.04,
            dividend_yield=0.012,
            bid=6.10,
            ask=6.35,
            volume=120,
            open_interest=850,
            underlying_closes_20d=[
                490.0, 492.0, 491.5, 493.0, 494.5, 496.0, 497.5, 498.0, 499.0, 500.0,
                501.0, 500.5, 502.0, 503.0, 501.5, 500.0, 499.5, 501.0, 502.5, 500.0,
            ],
        )
        row = curate_option_quote(quote)
        self.assertEqual(row.symbol, "SPY")
        self.assertTrue(row.liquidity_pass)
        self.assertIn("market_bid", row.labels)
        self.assertIn("market_ask", row.labels)
        self.assertIn("distilled_mean", row.labels)
        self.assertFalse(row.trade_authorized)


if __name__ == "__main__":
    unittest.main()
