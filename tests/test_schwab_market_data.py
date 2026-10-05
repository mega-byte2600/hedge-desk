import unittest
from urllib.parse import parse_qs, urlparse

from hedge_desk.brokers.schwab_market_data import SchwabMarketDataBroker


class SchwabMarketDataTests(unittest.TestCase):
    def test_quotes_batches_symbols_in_one_request(self):
        seen = []

        def transport(method, url, headers):
            seen.append((method, url, headers))
            return 200, b'{"SPY":{"quote":{"lastPrice":500}}}'

        adapter = SchwabMarketDataBroker(transport=transport)
        result = adapter.quotes("token", ["SPY", "QQQ"])
        cached = adapter.quotes("token", ["QQQ", "SPY"])
        self.assertEqual(result["status"], "ok")
        self.assertEqual(cached["data"], result["data"])
        self.assertEqual(len(seen), 1)
        self.assertTrue(result["read_only"])
        self.assertEqual(seen[0][0], "GET")
        self.assertEqual(parse_qs(urlparse(seen[0][1]).query)["symbols"], ["QQQ,SPY"])
        self.assertEqual(seen[0][2]["Authorization"], "Bearer token")

    def test_option_chain_rejects_unknown_filter_and_quotes_values(self):
        seen = []

        def transport(method, url, headers):
            seen.append(url)
            return 200, b'{}'

        adapter = SchwabMarketDataBroker(transport=transport)
        self.assertEqual(adapter.option_chain("t", "SPY", nonsense=1)["error"], "unsupported_chain_filter")
        result = adapter.option_chain("t", "SPY", contractType="CALL", daysToExpiration=14)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(parse_qs(urlparse(seen[0]).query)["daysToExpiration"], ["14"])

    def test_throttles_are_returned_without_retry(self):
        calls = []

        def transport(method, url, headers):
            calls.append(url)
            return 429, b"rate limited"

        result = SchwabMarketDataBroker(transport=transport).expiration_chain("t", "SPY")
        self.assertEqual(result["error"], "throttled")
        self.assertEqual(len(calls), 1)

    def test_market_request_cannot_change_destination_or_path(self):
        seen = []
        adapter = SchwabMarketDataBroker(transport=lambda m, u, h: (seen.append(u) or 200, b"{}"))
        for market in ("equity", "option", "bond", "future", "forex"):
            self.assertEqual(adapter.market_hours("t", market, date="2026-10-05")["status"], "ok")
            self.assertEqual(urlparse(seen[-1]).path, "/marketdata/v1/markets/" + market)
        for attack in ("//evil.example", "../trader/v1/accounts", "equity?redirect=https://evil.example", "", "equity#fragment"):
            self.assertEqual(adapter.market_hours("t", attack)["error"], "invalid_market")
        self.assertEqual(len(seen), 5)
        self.assertEqual(adapter.market_hours("t", "equity", date="bad")["error"], "invalid_date")

    def test_provider_failures_return_stable_errors_without_payload_leaks(self):
        for status, raw, error in ((500, b"secret", None), (200, b"invalid-json-secret", "bad_json"), (200, b"123", "unexpected_response_schema")):
            adapter = SchwabMarketDataBroker(transport=lambda *args: (status, raw))
            result = adapter.price_history("token", "SPY", period=1)
            self.assertEqual(result["status"], "error")
            self.assertNotIn("secret", str(result))
            if error: self.assertEqual(result["error"], error)
        def failing(*args): raise RuntimeError("private transport detail")
        result = SchwabMarketDataBroker(transport=failing).expiration_chain("t", "SPY")
        self.assertEqual(result["error"], "transport_failure")

    def test_invalid_inputs_do_not_send_requests(self):
        def never(*args): raise AssertionError("must not send")
        adapter = SchwabMarketDataBroker(transport=never)
        requests = [adapter.quotes("t", []), adapter.quotes("t", [""]), adapter.option_chain("t", ""), adapter.expiration_chain("t", ""), adapter.price_history("t", "SPY", unexpected=1), adapter.price_history("t", ""), adapter.expiration_chain("", "SPY")]
        self.assertTrue(all(r["status"] == "error" for r in requests))
        for seconds in (-1, 6):
            with self.assertRaises(ValueError): SchwabMarketDataBroker(quote_cache_seconds=seconds)

    def test_insecure_or_unofficial_host_rejected(self):
        for url in ("http://api.schwabapi.com/marketdata/v1", "https://example.com"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                SchwabMarketDataBroker(base_url=url)

    def test_full_market_data_surface_routes_to_official_paths(self):
        seen = []

        def transport(method, url, headers):
            seen.append((method, url, headers))
            return 200, b'{}'

        adapter = SchwabMarketDataBroker(transport=transport)
        self.assertEqual(adapter.movers("t", "$SPX", sort="VOLUME", frequency=5)["status"], "ok")
        self.assertEqual(urlparse(seen[-1][1]).path, "/marketdata/v1/movers/%24SPX")

        self.assertEqual(adapter.market_hours_all("t", "equity,option", date="2026-10-05")["status"], "ok")
        self.assertEqual(urlparse(seen[-1][1]).path, "/marketdata/v1/markets")

        self.assertEqual(adapter.instruments("t", "AAPL", "fundamental")["status"], "ok")
        self.assertEqual(urlparse(seen[-1][1]).path, "/marketdata/v1/instruments")

        self.assertEqual(adapter.instrument_by_cusip("t", "037833100")["status"], "ok")
        self.assertEqual(urlparse(seen[-1][1]).path, "/marketdata/v1/instruments/037833100")

    def test_full_market_data_surface_rejects_invalid_inputs_without_network(self):
        def never(*args):
            raise AssertionError("must not send")

        adapter = SchwabMarketDataBroker(transport=never)
        self.assertEqual(adapter.movers("t", "", sort="VOLUME")["status"], "error")
        self.assertEqual(adapter.movers("t", "$SPX", nope=1)["status"], "error")
        self.assertEqual(adapter.market_hours_all("t", "equity", date="bad")["status"], "error")
        self.assertEqual(adapter.instruments("t", "", "fundamental")["status"], "error")
        self.assertEqual(adapter.instruments("t", "AAPL", "")["status"], "error")
        self.assertEqual(adapter.instrument_by_cusip("t", "")["status"], "error")

    def test_quote_batching_caps_requests_at_fifty_symbols(self):
        seen = []
        def transport(method, url, headers):
            seen.append(parse_qs(urlparse(url).query)["symbols"][0].split(","))
            payload = {symbol: {"quote": {"lastPrice": 1}} for symbol in seen[-1]}
            import json
            return 200, json.dumps(payload).encode()

        symbols = [f"S{i}" for i in range(101)]
        adapter = SchwabMarketDataBroker(transport=transport, quote_cache_seconds=0)
        result = adapter.quotes("token", symbols)

        self.assertEqual(result["status"], "ok")
        self.assertEqual([len(batch) for batch in seen], [50, 50, 1])
        self.assertEqual(len(result["data"]), 101)

    def test_configured_rpm_is_conservatively_capped(self):
        from unittest.mock import patch
        from hedge_desk.brokers import schwab_market_data as md

        with patch.dict("os.environ", {"SCHWAB_MARKET_DATA_RPM": "999"}, clear=False):
            self.assertEqual(md._configured_rpm(), 120)
        with patch.dict("os.environ", {"SCHWAB_MARKET_DATA_RPM": "90"}, clear=False):
            self.assertEqual(md._configured_rpm(), 90)
        with patch.dict("os.environ", {"SCHWAB_MARKET_DATA_RPM": "bad"}, clear=False):
            self.assertEqual(md._configured_rpm(), 90)


if __name__ == "__main__":
    unittest.main()
