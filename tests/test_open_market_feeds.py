import json
import os
import unittest
from urllib.parse import parse_qs, urlparse
from unittest.mock import patch

from hedge_desk.data.open_market_feeds import (
    cftc_cot,
    eia_v2,
    finra_fixed_income,
    nyfed_reference_rates,
    sec_companyfacts,
    sec_submissions,
    treasury_latest_auctions,
)


def _transport(payload, status=200, seen=None):
    raw = json.dumps(payload).encode("utf-8")

    def fetch(url):
        if seen is not None:
            seen.append(url)
        return status, raw

    return fetch


class OpenMarketFeedTests(unittest.TestCase):
    def test_treasury_auctions_uses_official_endpoint_and_rows(self):
        seen = []
        result = treasury_latest_auctions(
            limit=2,
            transport=_transport(
                {"data": [{"cusip": "912TEST01"}, {"cusip": "912TEST02"}]},
                seen=seen,
            ),
        )
        self.assertEqual(result.provider_id, "treasury-fiscaldata")
        self.assertEqual(result.row_count, 2)
        parsed = urlparse(seen[0])
        self.assertEqual(parsed.scheme, "https")
        self.assertEqual(parsed.hostname, "api.fiscaldata.treasury.gov")
        self.assertTrue(parsed.path.endswith("/auctions_query"))
        self.assertEqual(parse_qs(parsed.query).get("page[size]"), ["2"])

    def test_finra_public_fixed_income_dataset_is_allowlisted(self):
        seen = []
        result = finra_fixed_income(
            "corporateMarketBreadth",
            limit=5,
            transport=_transport([{"advances": 100, "declines": 80}], seen=seen),
        )
        self.assertEqual(result.provider_id, "finra")
        self.assertEqual(result.dataset, "corporateMarketBreadth")
        self.assertEqual(result.row_count, 1)
        parsed = urlparse(seen[0])
        self.assertEqual(parsed.hostname, "api.finra.org")
        self.assertEqual(
            parsed.path,
            "/data/group/fixedIncomeMarket/name/corporateMarketBreadth",
        )
        with self.assertRaisesRegex(ValueError, "unsupported FINRA"):
            finra_fixed_income("arbitraryDataset", transport=_transport([]))

    def test_cftc_tff_uses_official_public_reporting_api(self):
        seen = []
        result = cftc_cot(
            "tff_futures_only",
            limit=3,
            transport=_transport([{"market_and_exchange_names": "TEST"}], seen=seen),
        )
        self.assertEqual(result.provider_id, "cftc-cot")
        self.assertEqual(result.row_count, 1)
        parsed = urlparse(seen[0])
        self.assertEqual(parsed.hostname, "publicreporting.cftc.gov")
        self.assertEqual(parsed.path, "/resource/gpe5-46if.json")
        self.assertEqual(parse_qs(parsed.query).get("$limit"), ["3"])

    def test_nyfed_latest_and_history_use_official_no_key_api(self):
        seen = []
        latest = nyfed_reference_rates(
            transport=_transport(
                {"refRates": [{"type": "SOFR", "percentRate": 3.88}]},
                seen=seen,
            )
        )
        self.assertEqual(latest.provider_id, "nyfed-markets")
        self.assertEqual(latest.dataset, "all-latest")
        self.assertEqual(latest.row_count, 1)
        self.assertEqual(
            seen[0], "https://markets.newyorkfed.org/api/rates/all/latest.json"
        )

        seen.clear()
        history = nyfed_reference_rates(
            "SOFR",
            limit=5,
            transport=_transport(
                {"refRates": [{"type": "SOFR", "percentRate": 3.88}]},
                seen=seen,
            ),
        )
        self.assertEqual(history.dataset, "sofr")
        self.assertTrue(seen[0].endswith("/api/rates/secured/sofr/last/5.json"))
        with self.assertRaisesRegex(ValueError, "unsupported NY Fed"):
            nyfed_reference_rates("LIBOR", transport=_transport({"refRates": []}))

    def test_eia_requires_key_and_does_not_return_it_in_result(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("EIA_API_KEY", None)
            with self.assertRaisesRegex(ValueError, "EIA_API_KEY"):
                eia_v2("petroleum/stoc/wstk", transport=_transport({}))

        seen = []
        result = eia_v2(
            "petroleum/stoc/wstk",
            data=("value",),
            limit=4,
            api_key="secret-test-key",
            transport=_transport({"response": {"data": [{"value": "1"}]}}, seen=seen),
        )
        self.assertEqual(result.provider_id, "eia-open-data")
        self.assertEqual(result.dataset, "petroleum/stoc/wstk")
        self.assertNotIn("secret-test-key", repr(result))
        query = parse_qs(urlparse(seen[0]).query)
        self.assertEqual(query.get("api_key"), ["secret-test-key"])

    def test_sec_submissions_normalizes_cik(self):
        seen = []
        payload = {"cik": "320193", "name": "Example"}
        result = sec_submissions(320193, transport=_transport(payload, seen=seen))
        self.assertEqual(result["cik"], "320193")
        self.assertTrue(seen[0].endswith("CIK0000320193.json"))

    def test_sec_companyfacts_requires_facts(self):
        seen = []
        result = sec_companyfacts(
            "0000320193",
            transport=_transport({"facts": {"us-gaap": {}}}, seen=seen),
        )
        self.assertIn("facts", result)
        self.assertIn("/api/xbrl/companyfacts/CIK0000320193.json", seen[0])
        with self.assertRaisesRegex(ValueError, "malformed"):
            sec_companyfacts(320193, transport=_transport({"entityName": "Example"}))

    def test_open_feed_adapters_fail_closed_on_bad_http_and_json(self):
        with self.assertRaisesRegex(ValueError, "status 503"):
            treasury_latest_auctions(transport=lambda _url: (503, b"down"))
        with self.assertRaisesRegex(ValueError, "malformed JSON"):
            cftc_cot(transport=lambda _url: (200, b"not-json"))

    def test_limits_and_routes_are_validated_before_network(self):
        with self.assertRaisesRegex(ValueError, "limit"):
            treasury_latest_auctions(limit=0, transport=_transport({"data": []}))
        with self.assertRaisesRegex(ValueError, "invalid EIA route"):
            eia_v2("../secret", api_key="x", transport=_transport({}))


if __name__ == "__main__":
    unittest.main()
