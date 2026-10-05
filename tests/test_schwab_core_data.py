import unittest
from unittest.mock import patch

from hedge_desk import schwab_core_data as core


class SchwabCoreDataTests(unittest.TestCase):
    def test_parse_quote_maps_schwab_payload_to_console_shape(self):
        item = {
            "quote": {
                "lastPrice": 512.34,
                "closePrice": 510.00,
                "netPercentChange": 0.46,
            },
            "reference": {"description": "SPDR S&P 500 ETF"},
        }
        parsed = core._parse_quote("SPY", item)
        self.assertEqual(parsed["symbol"], "SPY")
        self.assertEqual(parsed["last"], 512.34)
        self.assertEqual(parsed["prev_close"], 510.0)
        self.assertEqual(parsed["change_pct"], 0.46)
        self.assertEqual(parsed["source"], core.SOURCE_NAME)

    @patch("hedge_desk.schwab_core_data._access_token", return_value="TOKEN")
    @patch("hedge_desk.schwab_core_data.SchwabMarketDataBroker")
    @patch("hedge_desk.live_desk_data._fetch_yahoo")
    def test_schwab_is_primary_and_yahoo_only_fills_missing_symbols(
        self, yahoo, broker_cls, _token
    ):
        broker = broker_cls.return_value
        broker.quotes.return_value = {
            "status": "ok",
            "data": {
                "SPY": {
                    "quote": {"lastPrice": 500.0, "closePrice": 495.0},
                    "reference": {"description": "SPY"},
                }
            },
        }
        yahoo.return_value = {
            "symbol": "QQQ",
            "name": "QQQ",
            "last": 450.0,
            "prev_close": 449.0,
            "change_pct": 0.22,
            "source": "Yahoo Finance",
        }

        data, unavailable = core.fetch_market_snapshot(["SPY", "QQQ"])

        self.assertEqual(data["SPY"]["source"], core.SOURCE_NAME)
        self.assertEqual(data["QQQ"]["source"], core.FALLBACK_SOURCE_NAME)
        self.assertEqual(yahoo.call_count, 1)
        self.assertEqual(yahoo.call_args.args[0], "QQQ")
        self.assertEqual(unavailable, [])

    @patch("hedge_desk.schwab_core_data._access_token", side_effect=RuntimeError("not_ready"))
    @patch("hedge_desk.live_desk_data._fetch_yahoo")
    def test_unavailable_schwab_falls_back_without_synthetic_data(self, yahoo, _token):
        yahoo.return_value = {
            "symbol": "SPY",
            "name": "SPY",
            "last": 500.0,
            "prev_close": 499.0,
            "change_pct": 0.2,
            "source": "Yahoo Finance",
        }
        data, unavailable = core.fetch_market_snapshot(["SPY"])
        self.assertEqual(data["SPY"]["source"], core.FALLBACK_SOURCE_NAME)
        self.assertEqual(unavailable, [])


if __name__ == "__main__":
    unittest.main()
