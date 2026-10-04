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

    def test_insecure_or_unofficial_host_rejected(self):
        for url in ("http://api.schwabapi.com/marketdata/v1", "https://example.com"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                SchwabMarketDataBroker(base_url=url)


if __name__ == "__main__":
    unittest.main()
