import json
import os
import unittest
from urllib.parse import parse_qs, urlparse
from unittest.mock import patch

from hedge_desk.data.open_market_feeds import (
    bls_latest_series,
    cftc_cot,
    ecb_exchange_rates,
    fdic_failures,
    treasury_yield_curve,
    world_bank_indicator,
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


def _request_transport(payloads, seen=None):
    encoded = [json.dumps(payload).encode("utf-8") for payload in payloads]
    index = {"value": 0}

    def fetch(request):
        if seen is not None:
            seen.append(request)
        i = index["value"]
        index["value"] += 1
        return 200, encoded[i]

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

    def test_finra_public_fixed_income_dataset_is_allowlisted_and_bearer_authenticated(self):
        seen = []
        result = finra_fixed_income(
            "corporateMarketBreadth",
            limit=5,
            access_token="test-access-token",
            request_transport=_request_transport(
                [[{"advances": 100, "declines": 80}]], seen=seen
            ),
        )
        self.assertEqual(result.provider_id, "finra")
        self.assertEqual(result.dataset, "corporateMarketBreadth")
        self.assertEqual(result.row_count, 1)
        request = seen[0]
        parsed = urlparse(request.full_url)
        self.assertEqual(parsed.hostname, "api.finra.org")
        self.assertEqual(
            parsed.path,
            "/data/group/fixedIncomeMarket/name/corporateMarketBreadth",
        )
        self.assertEqual(request.get_header("Authorization"), "Bearer test-access-token")
        with self.assertRaisesRegex(ValueError, "unsupported FINRA"):
            finra_fixed_income(
                "arbitraryDataset",
                access_token="x",
                request_transport=_request_transport([[]]),
            )

    def test_finra_requires_server_side_credentials_when_no_token_is_injected(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "FINRA_CLIENT_ID"):
                finra_fixed_income(
                    "corporateMarketBreadth",
                    request_transport=_request_transport([[]]),
                )

    def test_finra_oauth_flow_uses_basic_then_bearer_without_returning_secret(self):
        seen = []
        result = finra_fixed_income(
            "corporateMarketBreadth",
            client_id="public-client",
            client_secret="test-client-secret",
            request_transport=_request_transport(
                [
                    {"access_token": "short-lived-token", "token_type": "Bearer"},
                    [{"advances": 101, "declines": 79}],
                ],
                seen=seen,
            ),
        )
        self.assertEqual(len(seen), 2)
        token_request, data_request = seen
        self.assertEqual(token_request.get_method(), "POST")
        self.assertEqual(urlparse(token_request.full_url).hostname, "ews.fip.finra.org")
        self.assertTrue(token_request.get_header("Authorization").startswith("Basic "))
        self.assertEqual(data_request.get_header("Authorization"), "Bearer short-lived-token")
        self.assertNotIn("test-client-secret", repr(result))


    def test_bls_latest_series_uses_official_public_api(self):
        seen = []
        payload = {
            "status": "REQUEST_SUCCEEDED",
            "Results": {
                "series": [
                    {
                        "seriesID": "CUUR0000SA0",
                        "data": [
                            {
                                "year": "2026",
                                "period": "M08",
                                "periodName": "August",
                                "value": "325.0",
                                "latest": "true",
                            }
                        ],
                    }
                ]
            },
        }
        result = bls_latest_series(
            "CUUR0000SA0", transport=_transport(payload, seen=seen)
        )
        self.assertEqual(result.provider_id, "bls")
        self.assertEqual(result.dataset, "CUUR0000SA0")
        self.assertEqual(result.row_count, 1)
        parsed = urlparse(seen[0])
        self.assertEqual(parsed.hostname, "api.bls.gov")
        self.assertIn("/publicAPI/v2/timeseries/data/CUUR0000SA0", parsed.path)
        self.assertEqual(parse_qs(parsed.query).get("latest"), ["true"])
        with self.assertRaisesRegex(ValueError, "unsupported BLS"):
            bls_latest_series("BAD", transport=_transport(payload))

    def test_ecb_fx_uses_official_sdmx_api_and_parses_csv(self):
        seen = []

        def transport(url):
            seen.append(url)
            raw = (
                "KEY,FREQ,CURRENCY,CURRENCY_DENOM,EXR_TYPE,EXR_SUFFIX,TIME_PERIOD,OBS_VALUE,OBS_STATUS\n"
                "EXR.D.USD.EUR.SP00.A,D,USD,EUR,SP00,A,2026-09-25,1.1700,A\n"
            ).encode("utf-8")
            return 200, raw

        result = ecb_exchange_rates(("USD",), transport=transport)
        self.assertEqual(result.provider_id, "ecb-fx")
        self.assertEqual(result.dataset, "EXR")
        self.assertEqual(result.row_count, 1)
        parsed = urlparse(seen[0])
        self.assertEqual(parsed.hostname, "data-api.ecb.europa.eu")
        self.assertIn("/service/data/EXR/D.USD.EUR.SP00.A", parsed.path)
        self.assertEqual(parse_qs(parsed.query).get("lastNObservations"), ["1"])
        self.assertEqual(result.rows[0]["CURRENCY"], "USD")
        with self.assertRaisesRegex(ValueError, "unsupported ECB"):
            ecb_exchange_rates(("BTC",), transport=transport)


    def test_treasury_yield_curve_uses_official_feed(self):
        seen = []
        xml = b'''<?xml version="1.0" encoding="utf-8"?>
        <feed xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"
              xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices">
          <entry><content><m:properties>
            <d:NEW_DATE>2026-09-25</d:NEW_DATE>
            <d:BC_2YEAR>3.70</d:BC_2YEAR>
            <d:BC_10YEAR>4.10</d:BC_10YEAR>
          </m:properties></content></entry>
        </feed>'''
        def transport(url):
            seen.append(url)
            return 200, xml
        result = treasury_yield_curve(2026, transport=transport)
        self.assertEqual(result.provider_id, "treasury-rates")
        self.assertEqual(result.row_count, 1)
        self.assertEqual(urlparse(seen[0]).hostname, "home.treasury.gov")

    def test_fdic_failures_uses_official_api(self):
        seen = []
        payload = {"data": [{"data": {"NAME": "Example Bank", "FAILDATE": "01/01/2026"}}]}
        result = fdic_failures(limit=1, transport=_transport(payload, seen=seen))
        self.assertEqual(result.provider_id, "fdic")
        self.assertEqual(result.row_count, 1)
        self.assertEqual(urlparse(seen[0]).hostname, "api.fdic.gov")

    def test_world_bank_indicator_uses_official_api(self):
        seen = []
        payload = [
            {"page": 1},
            [{"countryiso3code": "USA", "date": "2025", "value": 100.0}],
        ]
        result = world_bank_indicator(
            "NY.GDP.MKTP.CD", country="USA", per_page=1,
            transport=_transport(payload, seen=seen)
        )
        self.assertEqual(result.provider_id, "world-bank")
        self.assertEqual(result.row_count, 1)
        self.assertEqual(urlparse(seen[0]).hostname, "api.worldbank.org")
        with self.assertRaisesRegex(ValueError, "unsupported World Bank"):
            world_bank_indicator("BAD.SERIES", transport=_transport(payload))

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
