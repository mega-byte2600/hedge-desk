import json
import os
import unittest
from urllib.parse import parse_qs, urlparse
from unittest.mock import patch

from decimal import Decimal
from hedge_desk.data.open_market_feeds import (
    bls_latest_series,
    cftc_cot,
    ecb_exchange_rates,
    fdic_failures,
    nasdaq_earnings_calendar,
    nasdaq_option_chain,
    nasdaq_quote,
    treasury_yield_curve,
    world_bank_indicator,
    eia_v2,
    finra_fixed_income,
    nyfed_reference_rates,
    oecd_composite_leading_indicator,
    eurostat_quarterly_gdp,
    usgs_earthquakes,
    nasa_eonet_events,
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

    def test_ecb_fx_uses_official_eurofxref_feed(self):
        seen = []
        xml = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<gesmes:Envelope xmlns:gesmes="http://www.gesmes.org/xml/2002-08-01"'
            b' xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref">'
            b"<Cube><Cube time='2026-09-28'>"
            b"<Cube currency='USD' rate='1.1723'/>"
            b"<Cube currency='JPY' rate='171.20'/>"
            b"</Cube></Cube></gesmes:Envelope>"
        )

        def transport(url):
            seen.append(url)
            return 200, xml

        result = ecb_exchange_rates(("USD", "JPY"), transport=transport)
        self.assertEqual(result.provider_id, "ecb-fx")
        self.assertEqual(result.dataset, "eurofxref-daily")
        self.assertEqual(result.row_count, 2)
        parsed = urlparse(seen[0])
        self.assertEqual(parsed.hostname, "www.ecb.europa.eu")
        self.assertIn("eurofxref-daily.xml", parsed.path)
        by_ccy = {row["currency"]: row for row in result.rows}
        self.assertEqual(by_ccy["USD"]["rate"], "1.1723")
        self.assertEqual(by_ccy["USD"]["date"], "2026-09-28")
        self.assertEqual(by_ccy["USD"]["base"], "EUR")
        with self.assertRaisesRegex(ValueError, "unsupported ECB"):
            ecb_exchange_rates(("BTC",), transport=transport)

    def test_ecb_fx_fails_closed_on_bad_xml(self):
        def transport(url):
            return 200, b"not xml"
        with self.assertRaisesRegex(ValueError, "malformed XML"):
            ecb_exchange_rates(("USD",), transport=transport)


    def test_treasury_yield_curve_uses_fred_dgs_tenors(self):
        seen = []

        def fake_fred(series, start, end, transport=None):
            seen.append(series)
            return (("2026-09-25", Decimal("4.10")), ("2026-09-24", Decimal("4.09")))

        with patch("hedge_desk.rates_desk.fred_series_rows", side_effect=fake_fred):
            result = treasury_yield_curve(2026)
        self.assertEqual(result.provider_id, "fred")
        self.assertEqual(result.dataset, "treasury_par_yield_curve_DGS")
        tenors = {row["tenor"] for row in result.rows}
        self.assertIn("DGS10", tenors)
        self.assertIn("DGS2", tenors)
        row = next(r for r in result.rows if r["tenor"] == "DGS10" and r["date"] == "2026-09-25")
        self.assertEqual(row["value"], "4.10")
        with self.assertRaisesRegex(ValueError, "invalid Treasury yield-curve year"):
            treasury_yield_curve(1800)

    def test_treasury_yield_curve_fails_closed_when_fred_fails(self):
        def fake_fred(series, start, end, transport=None):
            raise ValueError("fred down")
        with patch("hedge_desk.rates_desk.fred_series_rows", side_effect=fake_fred):
            with self.assertRaisesRegex(ValueError, "FRED fetch failed"):
                treasury_yield_curve(2026)

    def test_nasdaq_quote_parses_watchlist_snapshots(self):
        seen = []
        payload = {
            "data": {
                "symbol": "SPY",
                "primaryData": {
                    "lastSalePrice": "$765.05",
                    "netChange": "-0.50",
                    "percentageChange": "-0.07%",
                    "lastTradeTimestamp": "Sep 28, 2026 4:53 PM ET",
                    "isRealTime": True,
                    "bidPrice": "$765.02",
                    "askPrice": "$765.08",
                },
            }
        }

        def transport(url):
            seen.append(url)
            return 200, json.dumps(payload).encode("utf-8")

        result = nasdaq_quote(("SPY", "AAPL"), transport=transport)
        self.assertEqual(result.provider_id, "nasdaq")
        self.assertEqual(result.row_count, 2)
        self.assertEqual(urlparse(seen[0]).hostname, "api.nasdaq.com")
        self.assertIn("assetclass=etf", seen[0])  # SPY auto-detected as ETF
        self.assertIn("assetclass=stocks", seen[1])  # AAPL defaults to stocks
        self.assertEqual(result.rows[0]["symbol"], "SPY")
        self.assertEqual(result.rows[0]["lastSalePrice"], "$765.05")
        self.assertTrue(result.rows[0]["isRealTime"])
        with self.assertRaisesRegex(ValueError, "invalid Nasdaq symbol"):
            nasdaq_quote(("BAD SYM!!",), transport=transport)

    def test_nasdaq_quote_fails_closed_on_rate_limit(self):
        def transport(url):
            return 429, b"too many requests"
        with self.assertRaisesRegex(ValueError, "status 429"):
            nasdaq_quote(("SPY",), transport=transport)

    def test_nasdaq_option_chain_drops_group_headers(self):
        payload = {
            "data": {
                "table": {
                    "rows": [
                        {"expirygroup": "October 2026", "strike": None},
                        {
                            "expirygroup": "October 2026", "strike": "765.00",
                            "c_Last": "5.20", "c_Bid": "5.10", "c_Ask": "5.30",
                            "c_Volume": "1200", "c_Openinterest": "3400",
                            "p_Last": "4.80", "p_Bid": "4.70", "p_Ask": "4.90",
                            "p_Volume": "900", "p_Openinterest": "2100",
                        },
                    ]
                }
            }
        }

        def transport(url):
            return 200, json.dumps(payload).encode("utf-8")

        result = nasdaq_option_chain("SPY", limit=5, transport=transport)
        self.assertEqual(result.provider_id, "nasdaq")
        self.assertEqual(result.row_count, 1)
        row = result.rows[0]
        self.assertEqual(row["strike"], "765.00")
        self.assertEqual(row["callBid"], "5.10")
        self.assertEqual(row["putAsk"], "4.90")
        with self.assertRaisesRegex(ValueError, "no strike rows"):
            nasdaq_option_chain("SPY", transport=lambda url: (200, json.dumps({"data": {"table": {"rows": []}}}).encode()))

    def test_nasdaq_earnings_calendar_returns_rows(self):
        payload = {"data": {"rows": [{"symbol": "JEF", "name": "Jefferies", "time": "beforeMarket"}]}}

        def transport(url):
            return 200, json.dumps(payload).encode("utf-8")

        result = nasdaq_earnings_calendar("2026-09-29", transport=transport)
        self.assertEqual(result.provider_id, "nasdaq")
        self.assertEqual(result.dataset, "earnings-calendar")
        self.assertEqual(result.row_count, 1)
        self.assertEqual(result.rows[0]["symbol"], "JEF")
        self.assertEqual(result.rows[0]["calendarDate"], "2026-09-29")
        with self.assertRaisesRegex(ValueError, "invalid earnings-calendar date"):
            nasdaq_earnings_calendar("not-a-date", transport=transport)

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

    def test_oecd_cli_is_bounded_official_csv(self):
        seen = []
        raw = b"REF_AREA,MEASURE,TIME_PERIOD,OBS_VALUE\nUSA,CLI,2025-10,99.5\nUSA,CLI,2025-11,99.7\n"
        result = oecd_composite_leading_indicator(
            start_period="2025-10", end_period="2025-11",
            transport=lambda url: (seen.append(url) or (200, raw)),
        )
        self.assertEqual((result.provider_id, result.dataset, result.row_count), ("oecd", "DF_CLI", 2))
        self.assertEqual(result.rows[-1]["OBS_VALUE"], "99.7")
        parsed = urlparse(seen[0])
        self.assertEqual(parsed.hostname, "sdmx.oecd.org")
        self.assertIn("USA.M.LI...AA...H", parsed.path)
        query = parse_qs(parsed.query)
        self.assertEqual(query["startPeriod"], ["2025-10"])
        self.assertEqual(query["endPeriod"], ["2025-11"])
        self.assertEqual(query["format"], ["csvfile"])

    def test_eurostat_quarterly_gdp_parses_jsonstat_and_narrows_query(self):
        seen = []
        payload = {
            "id": ["freq", "unit", "na_item", "s_adj", "geo", "time"],
            "size": [1, 1, 1, 1, 1, 2],
            "dimension": {"time": {"category": {"index": {"2025Q4": 0, "2026Q1": 1}}}},
            "value": ["123.4", "124.5"],
        }
        result = eurostat_quarterly_gdp(transport=_transport(payload, seen=seen))
        self.assertEqual(result.provider_id, "eurostat")
        self.assertEqual(result.row_count, 2)
        self.assertEqual(result.rows[-1]["value"], "124.5")
        parsed = urlparse(seen[0])
        self.assertEqual(parsed.hostname, "ec.europa.eu")
        self.assertTrue(parsed.path.endswith("/namq_10_gdp"))
        query = parse_qs(parsed.query)
        self.assertEqual(query["geo"], ["EA20"])
        self.assertEqual(query["na_item"], ["B1GQ"])
        self.assertEqual(query["lastTimePeriod"], ["8"])

    def test_usgs_earthquakes_uses_bounded_geojson_query(self):
        seen = []
        payload = {"features": [{
            "id": "us-test", "properties": {"mag": 5.2, "time": 1790000000000,
                "place": "30 km west of example", "title": "M 5.2 - example", "url": "https://earthquake.usgs.gov/test"},
            "geometry": {"coordinates": [-120.1, 35.4, 8.2]},
        }]}
        result = usgs_earthquakes(transport=_transport(payload, seen=seen))
        self.assertEqual(result.provider_id, "usgs")
        self.assertEqual(result.row_count, 1)
        self.assertEqual(result.rows[0]["magnitude"], 5.2)
        self.assertEqual(result.rows[0]["latitude"], 35.4)
        parsed = urlparse(seen[0])
        self.assertEqual(parsed.hostname, "earthquake.usgs.gov")
        self.assertTrue(parsed.path.endswith("/fdsnws/event/1/query"))
        query = parse_qs(parsed.query)
        self.assertEqual(query["format"], ["geojson"])
        self.assertEqual(query["minmagnitude"], ["4.5"])
        self.assertEqual(query["limit"], ["25"])

    def test_nasa_eonet_returns_open_event_evidence_with_bounded_query(self):
        seen = []
        payload = {"events": [{
            "id": "EONET_1", "title": "Example wildfire",
            "categories": [{"id": "wildfires"}], "sources": [{"id": "InciWeb"}],
            "geometry": [{"date": "2026-10-02T12:00:00Z", "type": "Point", "coordinates": [-120.0, 37.0]}],
        }]}
        result = nasa_eonet_events(transport=_transport(payload, seen=seen))
        self.assertEqual(result.provider_id, "nasa-eonet")
        self.assertEqual(result.row_count, 1)
        self.assertEqual(result.rows[0]["categories"], ["wildfires"])
        parsed = urlparse(seen[0])
        self.assertEqual(parsed.hostname, "eonet.gsfc.nasa.gov")
        self.assertTrue(parsed.path.endswith("/api/v3/events"))
        query = parse_qs(parsed.query)
        self.assertEqual(query["status"], ["open"])
        self.assertEqual(query["days"], ["30"])
        self.assertEqual(query["limit"], ["25"])

    def test_global_feed_adapters_reject_unbounded_or_malformed_inputs(self):
        called = []
        transport = lambda url: (called.append(url) or (200, b"{}"))
        with self.assertRaises(ValueError):
            oecd_composite_leading_indicator(start_period="2026-13", transport=transport)
        with self.assertRaises(ValueError):
            eurostat_quarterly_gdp(periods=41, transport=transport)
        with self.assertRaises(ValueError):
            usgs_earthquakes(days=366, transport=transport)
        with self.assertRaises(ValueError):
            nasa_eonet_events(limit=501, transport=transport)
        self.assertEqual(called, [])

    def test_oecd_rejects_invalid_periods_and_empty_or_malformed_csv(self):
        for country in ("US", "U$A", "ééé"):
            with self.subTest(country=country), self.assertRaisesRegex(ValueError, "country code"):
                oecd_composite_leading_indicator(country=country, transport=lambda _url: (200, b""))
        for kwargs in (
            {"start_period": "2026-1"},
            {"end_period": "2026-00"},
            {"start_period": "2026-03", "end_period": "2026-02"},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                oecd_composite_leading_indicator(**kwargs, transport=lambda _url: (200, b""))
        for raw in (b"", b"TIME_PERIOD,OTHER\n2026-01,x\n", b"TIME_PERIOD,OBS_VALUE\n2026-01,\n"):
            with self.subTest(raw=raw), self.assertRaisesRegex(ValueError, "oecd"):
                oecd_composite_leading_indicator(
                    start_period="2026-01", end_period="2026-01",
                    transport=lambda _url, value=raw: (200, value),
                )

    def test_eurostat_rejects_ambiguous_sparse_and_malformed_jsonstat(self):
        malformed = (
            ([], "not an object"),
            ({"id": "time", "size": [], "dimension": {}}, "dimensions"),
            ({"id": ["geo"], "size": [1], "dimension": {}}, "time dimension"),
            ({"id": ["time"], "size": [], "dimension": {}}, "time dimension"),
            ({"id": ["time", "geo"], "size": [2, 2], "dimension": {}}, "ambiguous"),
            ({"id": ["time"], "size": [1], "dimension": {"time": {"category": {"index": {}}}}}, "time categories"),
            ({"id": ["time"], "size": [1], "dimension": {"time": {"category": {"index": {"2026Q1": 0}}}}}, "no observation values"),
            ({"id": ["time"], "size": [1], "dimension": {"time": {"category": {"index": {"2026Q1": 0}}}}, "value": []}, "no GDP observations"),
        )
        for payload, expected in malformed:
            with self.subTest(expected=expected), self.assertRaisesRegex(ValueError, expected):
                eurostat_quarterly_gdp(transport=_transport(payload))
        sparse = {"id": ["time"], "size": [2],
                  "dimension": {"time": {"category": {"index": {"2026Q1": 0, "2026Q2": 1}}}},
                  "value": {"1": 124.0}}
        result = eurostat_quarterly_gdp(transport=_transport(sparse))
        self.assertEqual(result.rows, ({"date": "2026Q2", "value": 124.0, "geo": "EA20",
                                       "indicator": "B1GQ", "unit": "CLV10_MEUR"},))

    def test_event_feeds_skip_incomplete_records_and_fail_closed_on_bad_payloads(self):
        with self.assertRaisesRegex(ValueError, "magnitude"):
            usgs_earthquakes(min_magnitude=float("nan"), transport=_transport({"features": []}))
        with self.assertRaisesRegex(ValueError, "features"):
            usgs_earthquakes(transport=_transport({}))
        earthquakes = usgs_earthquakes(transport=_transport({"features": [
            None,
            {"properties": "bad"},
            {"id": "sparse", "properties": {"mag": 4.8}, "geometry": {"coordinates": []}},
        ]}))
        self.assertEqual(earthquakes.row_count, 1)
        self.assertEqual(earthquakes.rows[0], {"event_id": "sparse", "magnitude": 4.8})

        with self.assertRaisesRegex(ValueError, "events"):
            nasa_eonet_events(transport=_transport({}))
        events = nasa_eonet_events(transport=_transport({"events": [
            None,
            {"id": "bare", "geometry": [], "categories": "bad", "sources": "bad"},
            {"id": "located", "geometry": [{"date": "2026-10-03", "coordinates": [1, 2]}],
             "categories": [{"id": "fire"}, None, {}], "sources": [{"id": "official"}]},
        ]}))
        self.assertEqual(events.row_count, 2)
        self.assertEqual(events.rows[0]["categories"], [])
        self.assertIsNone(events.rows[0]["date"])
        self.assertEqual(events.rows[1]["categories"], ["fire"])

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
