import json
import unittest
from unittest.mock import patch

from hedge_desk import live_desk_data


class _Response:
    def __init__(self, payload):
        self._payload = payload
    def read(self):
        return json.dumps(self._payload).encode("utf-8")
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False


class DashboardSingleSourceTests(unittest.TestCase):
    def test_yahoo_quote_carries_observation_timestamp_and_frequency(self):
        payload = {
            "chart": {
                "result": [{
                    "timestamp": [1760000000, 1760086400],
                    "indicators": {"quote": [{"close": [100.0, 101.0]}]},
                }]
            }
        }
        with patch("urllib.request.urlopen", return_value=_Response(payload)):
            quote = live_desk_data._fetch_yahoo("SPY")
        self.assertEqual(quote["last"], 101.0)
        self.assertEqual(quote["data_frequency"], "daily_close")
        self.assertTrue(quote["observed_at"].endswith("+00:00"))
        self.assertIn("daily chart", quote["source"])

    def test_dashboard_route_no_longer_embeds_stale_morning_artifact(self):
        text = open("web/app.js", encoding="utf-8").read()
        start = text.index("function dashboard()")
        end = text.index("function workbench()", start)
        dashboard = text[start:end]
        self.assertNotIn('src="/dashboard"', dashboard)
        self.assertNotIn('data-src="/dashboard"', dashboard)
        self.assertIn("One source of truth", dashboard)
        self.assertIn("delayed/EOD", dashboard)


if __name__ == "__main__":
    unittest.main()
