import json
import os
import unittest
from urllib.parse import parse_qs, urlparse
from unittest.mock import patch

from hedge_desk.data.public_signal_feeds import (
    bea_nipa_table,
    nws_active_alerts,
    usda_nass_crop_progress,
)


def _transport(payload, seen=None, status=200):
    raw = json.dumps(payload).encode("utf-8")

    def fetch(request):
        if seen is not None:
            seen.append(request)
        return status, raw

    return fetch


class PublicSignalFeedTests(unittest.TestCase):
    def test_nws_active_alerts_uses_official_api_and_caps_rows(self):
        seen = []
        payload = {
            "features": [
                {
                    "properties": {
                        "id": "one",
                        "event": "Flood Warning",
                        "severity": "Severe",
                        "certainty": "Likely",
                        "urgency": "Immediate",
                        "headline": "Flood Warning issued",
                        "areaDesc": "Example County",
                        "sent": "2026-09-28T20:00:00-07:00",
                    }
                },
                {"properties": {"id": "two", "event": "Wind Advisory"}},
            ]
        }
        result = nws_active_alerts(area="CA", limit=1, transport=_transport(payload, seen))
        self.assertEqual(result.provider_id, "nws")
        self.assertEqual(result.dataset, "active-alerts")
        self.assertEqual(result.row_count, 1)
        self.assertEqual(result.rows[0]["event"], "Flood Warning")
        parsed = urlparse(seen[0].full_url)
        self.assertEqual(parsed.hostname, "api.weather.gov")
        self.assertEqual(parsed.path, "/alerts/active")
        query = parse_qs(parsed.query)
        self.assertEqual(query["area"], ["CA"])
        self.assertEqual(query["status"], ["actual"])
        self.assertIn("hedge-desk", seen[0].get_header("User-agent").lower())

    def test_nws_rejects_invalid_area(self):
        with self.assertRaisesRegex(ValueError, "two-letter"):
            nws_active_alerts(area="CAL")

    def test_bea_nipa_uses_server_side_key_and_does_not_return_it(self):
        seen = []
        payload = {
            "BEAAPI": {
                "Results": {
                    "Data": [
                        {
                            "TableName": "T10101",
                            "LineNumber": "1",
                            "LineDescription": "Gross domestic product",
                            "TimePeriod": "2026Q2",
                            "DataValue": "31,098.027",
                        }
                    ]
                }
            }
        }
        with patch.dict(os.environ, {"BEA_API_KEY": "bea-secret"}, clear=False):
            result = bea_nipa_table(transport=_transport(payload, seen))
        self.assertEqual(result.provider_id, "bea")
        self.assertEqual(result.dataset, "NIPA:T10101")
        self.assertEqual(result.row_count, 1)
        parsed = urlparse(seen[0].full_url)
        self.assertEqual(parsed.hostname, "apps.bea.gov")
        query = parse_qs(parsed.query)
        self.assertEqual(query["datasetname"], ["NIPA"])
        self.assertEqual(query["method"], ["GetData"])
        self.assertEqual(query["UserID"], ["bea-secret"])
        self.assertNotIn("bea-secret", repr(result))

    def test_bea_requires_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "BEA_API_KEY"):
                bea_nipa_table()

    def test_usda_nass_uses_narrow_weekly_crop_query(self):
        seen = []
        payload = {
            "data": [
                {
                    "commodity_desc": "CORN",
                    "week_ending": "2026-09-27",
                    "statisticcat_desc": "CONDITION",
                    "unit_desc": "PCT EXCELLENT",
                    "Value": "15",
                }
            ]
        }
        with patch.dict(os.environ, {"USDA_NASS_API_KEY": "nass-secret"}, clear=False):
            result = usda_nass_crop_progress(
                "CORN", year=2026, transport=_transport(payload, seen)
            )
        self.assertEqual(result.provider_id, "usda-nass")
        self.assertEqual(result.dataset, "weekly:CORN")
        self.assertEqual(result.row_count, 1)
        parsed = urlparse(seen[0].full_url)
        self.assertEqual(parsed.hostname, "quickstats.nass.usda.gov")
        query = parse_qs(parsed.query)
        self.assertEqual(query["source_desc"], ["SURVEY"])
        self.assertEqual(query["freq_desc"], ["WEEKLY"])
        self.assertEqual(query["commodity_desc"], ["CORN"])
        self.assertEqual(query["agg_level_desc"], ["NATIONAL"])
        self.assertEqual(query["key"], ["nass-secret"])
        self.assertNotIn("nass-secret", repr(result))

    def test_usda_nass_requires_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "USDA_NASS_API_KEY"):
                usda_nass_crop_progress()

    def test_transient_failures_retry_then_fail_closed(self):
        calls = {"count": 0}

        def failing(request):
            calls["count"] += 1
            return 503, b"temporary"

        with patch("hedge_desk.data.public_signal_feeds.time.sleep", return_value=None):
            with self.assertRaisesRegex(ValueError, "status 503"):
                nws_active_alerts(transport=failing)
        self.assertEqual(calls["count"], 3)


if __name__ == "__main__":
    unittest.main()
