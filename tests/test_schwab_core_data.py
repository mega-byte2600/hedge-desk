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

    @patch("hedge_desk.schwab_core_data.default_broker_store")
    @patch("hedge_desk.schwab_core_data.SchwabOAuthConfig.from_environment")
    @patch("hedge_desk.schwab_core_data.SchwabOAuth")
    @patch("hedge_desk.schwab_core_data.SchwabTokenManager")
    def test_market_data_token_does_not_require_account_selection(
        self, manager_cls, oauth_cls, config_from_env, store_factory
    ):
        with patch.dict("os.environ", {"SCHWAB_DATA_EMAIL": "data@example.com"}, clear=False):
            config_from_env.return_value.configured = True
            store = store_factory.return_value
            store.token_state.return_value = {
                "access_token": "access",
                "refresh_token": "refresh",
                "access_expires_at": "2026-10-05T12:00:00+00:00",
                "refresh_token_issued_at": "2026-10-01T12:00:00+00:00",
                "scope": "api",
                "updated_at": "2026-10-05T11:00:00+00:00",
                "selected_account_hash": "",
            }
            manager_cls.return_value.access_token.return_value = "usable"
            token = core._access_token()

        self.assertEqual(token, "usable")
        self.assertEqual(
            manager_cls.call_args.kwargs["refresh_token_max_age"].days,
            7,
        )
        state = manager_cls.return_value.access_token.call_args.args[0]
        self.assertEqual(state.selected_account_hash, "")

    @patch("hedge_desk.schwab_core_data.default_broker_store")
    @patch("hedge_desk.schwab_core_data.SchwabOAuthConfig.from_environment")
    def test_status_ready_requires_oauth_and_link_not_selected_account(
        self, config_from_env, store_factory
    ):
        with patch.dict("os.environ", {"SCHWAB_DATA_EMAIL": "data@example.com"}, clear=False):
            config_from_env.return_value.configured = True
            store_factory.return_value.connection.return_value = {"linked": True}
            status = core.status()

        self.assertTrue(status["ready"])
        self.assertNotIn("account_selected", status)

    @patch("hedge_desk.schwab_core_data._access_token", return_value="TOKEN")
    @patch("hedge_desk.schwab_core_data.SchwabMarketDataBroker")
    @patch("hedge_desk.live_desk_data._fetch_yahoo")
    def test_material_delta_promotes_corroborative_source(
        self, yahoo, broker_cls, _token
    ):
        broker_cls.return_value.quotes.return_value = {
            "status": "ok",
            "data": {
                "SPY": {
                    "quote": {"lastPrice": 500.0, "closePrice": 499.0},
                    "reference": {"description": "SPY"},
                }
            },
        }
        yahoo.return_value = {
            "symbol": "SPY",
            "name": "SPY",
            "last": 510.0,
            "prev_close": 509.0,
            "change_pct": 0.2,
            "source": "Yahoo Finance",
        }
        with patch.dict("os.environ", {"EMPORION_MARKET_DATA_DELTA_BPS": "50"}, clear=False):
            data, unavailable = core.fetch_market_snapshot(["SPY"])

        self.assertEqual(unavailable, [])
        self.assertEqual(data["SPY"]["source_role"], "primary_on_delta")
        self.assertEqual(data["SPY"]["displaced_primary_source"], core.SOURCE_NAME)
        self.assertGreater(data["SPY"]["corroboration_delta_bps"], 50)

    @patch("hedge_desk.schwab_core_data._access_token", return_value="TOKEN")
    @patch("hedge_desk.schwab_core_data.SchwabMarketDataBroker")
    @patch("hedge_desk.live_desk_data._fetch_yahoo")
    def test_small_delta_keeps_schwab_primary(
        self, yahoo, broker_cls, _token
    ):
        broker_cls.return_value.quotes.return_value = {
            "status": "ok",
            "data": {
                "SPY": {
                    "quote": {"lastPrice": 500.0, "closePrice": 499.0},
                    "reference": {"description": "SPY"},
                }
            },
        }
        yahoo.return_value = {
            "symbol": "SPY",
            "name": "SPY",
            "last": 500.1,
            "prev_close": 499.0,
            "change_pct": 0.2,
            "source": "Yahoo Finance",
        }
        with patch.dict("os.environ", {"EMPORION_MARKET_DATA_DELTA_BPS": "50"}, clear=False):
            data, unavailable = core.fetch_market_snapshot(["SPY"])

        self.assertEqual(unavailable, [])
        self.assertEqual(data["SPY"]["source_role"], "primary")
        self.assertEqual(data["SPY"]["primary_source"], core.SOURCE_NAME)
        self.assertLess(data["SPY"]["corroboration_delta_bps"], 50)


if __name__ == "__main__":
    unittest.main()
