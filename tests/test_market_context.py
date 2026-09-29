import os
import unittest
from unittest.mock import patch

from hedge_desk.data.open_market_feeds import OpenFeedResult
from hedge_desk.market_context import MARKET_CONTEXT_SCHEMA, build_market_context


def _result(provider, dataset, rows):
    return OpenFeedResult(provider, dataset, tuple(rows))


def _common_fakes():
    return {
        "treasury_curve_fetch": lambda: _result(
            "treasury-rates",
            "treasury_par_yield_curve_DGS",
            [{"tenor": "DGS10", "date": "2026-09-25", "value": "4.10"}],
        ),
        "fdic_fetch": lambda limit: _result(
            "fdic", "bank-failures", [{"NAME": "Example Bank", "FAILDATE": "01/01/2026"}]
        ),
        "world_bank_fetch": lambda indicator, country, per_page: _result(
            "world-bank", indicator, [{"countryiso3code": "USA", "date": "2025", "value": 100.0}]
        ),
        "bls_fetch": lambda series: _result(
            "bls", series, [{"seriesID": series, "year": "2026", "period": "M08", "value": "325.0"}]
        ),
        "ecb_fetch": lambda currencies: _result(
            "ecb-fx", "eurofxref-daily", [{"currency": "USD", "base": "EUR", "date": "2026-09-25", "rate": "1.17"}]
        ),
        "nws_fetch": lambda limit: _result(
            "nws", "active-alerts", [{"event": "Flood Warning", "severity": "Severe"}]
        ),
        "nasdaq_quote_fetch": lambda symbols: _result(
            "nasdaq", "quote-info", [{"symbol": "SPY", "lastSalePrice": "$765.05"}]
        ),
        "nasdaq_earn_fetch": lambda day: _result(
            "nasdaq", "earnings-calendar", [{"symbol": "JEF", "calendarDate": "2026-09-29"}]
        ),
    }


class MarketContextTests(unittest.TestCase):
    def test_builds_cross_asset_context_without_exposing_credentials(self):
        calls = []

        def nyfed_fetch():
            return _result(
                "nyfed-markets",
                "all-latest",
                [{"type": "SOFR", "percentRate": 3.88, "effectiveDate": "2026-09-24"}],
            )

        def treasury_fetch(limit):
            calls.append(("treasury", limit))
            return _result(
                "treasury-fiscaldata",
                "treasury-securities-auctions",
                [{"auction_date": "2026-09-24", "security_type": "Bill", "security_term": "4-Week"}],
            )

        def cftc_fetch(report, limit):
            calls.append((report, limit))
            return _result(
                "cftc-cot",
                report,
                [{"market_and_exchange_names": "U.S. TREASURY BONDS", "report_date_as_yyyy_mm_dd": "2026-09-22"}],
            )

        def eia_fetch(route, data, limit):
            calls.append((route, data, limit))
            return _result(
                "eia-open-data",
                route,
                [{"period": "2026-09-18", "value": "415000", "units": "MBBL"}],
            )

        def finra_fetch(dataset, limit):
            calls.append((dataset, limit))
            return _result(
                "finra",
                dataset,
                [{"date": "2026-09-25", "advances": 101, "declines": 79}],
            )

        def bea_fetch(table_name, frequency, year, limit):
            calls.append(("bea", table_name, frequency, year, limit))
            return _result(
                "bea",
                f"NIPA:{table_name}",
                [{"LineDescription": "Gross domestic product", "TimePeriod": "2026Q2", "DataValue": "31098.027"}],
            )

        def usda_fetch(commodity, year, limit):
            calls.append(("usda", commodity, year, limit))
            return _result(
                "usda-nass",
                f"weekly:{commodity}",
                [{"commodity_desc": commodity, "week_ending": "2026-09-27", "Value": "15"}],
            )

        with patch.dict(
            os.environ,
            {
                "EIA_API_KEY": "do-not-return",
                "FINRA_CLIENT_ID": "client-id",
                "FINRA_CLIENT_SECRET": "do-not-return-secret",
                "BEA_API_KEY": "bea-do-not-return",
                "USDA_NASS_API_KEY": "usda-do-not-return",
            },
            clear=False,
        ):
            context = build_market_context(
                fred_fetch=lambda series, start, end: (("2026-09-25", "3.88"),),
                nyfed_fetch=nyfed_fetch,
                treasury_fetch=treasury_fetch,
                cftc_fetch=cftc_fetch,
                eia_fetch=eia_fetch,
                finra_fetch=finra_fetch,
                bea_fetch=bea_fetch,
                usda_fetch=usda_fetch,
                **_common_fakes(),
            )

        self.assertEqual(context["schema_version"], MARKET_CONTEXT_SCHEMA)
        self.assertEqual(context["status"], "LIVE")
        self.assertEqual(context["live_sources"], 16)
        self.assertEqual(context["sources"]["nws"]["status"], "LIVE")
        self.assertEqual(context["sources"]["bea"]["status"], "LIVE")
        self.assertEqual(context["sources"]["usda-nass"]["status"], "LIVE")
        self.assertEqual(context["sources"]["nasdaq-quotes"]["status"], "LIVE")
        self.assertEqual(context["sources"]["nasdaq-earnings"]["status"], "LIVE")
        self.assertEqual(
            context["sources"]["nasdaq-quotes"]["observations"][0]["lastSalePrice"], "$765.05"
        )
        self.assertEqual(context["blocked_sources"], 0)
        self.assertEqual(context["unconfigured_sources"], 0)
        self.assertFalse(context["trade_authorized"])
        self.assertEqual(
            context["sources"]["nyfed-markets"]["observations"]["SOFR"]["percentRate"],
            3.88,
        )
        self.assertNotIn("do-not-return", repr(context))
        self.assertIn(("corporateMarketBreadth", 10), calls)
        self.assertIn(("bea", "T10101", "Q", "X", 25), calls)
        self.assertTrue(any(item[0] == "usda" and item[1] == "CORN" for item in calls))

    def test_keyed_sources_are_explicitly_unconfigured(self):
        with patch.dict(os.environ, {}, clear=True):
            context = build_market_context(
                fred_fetch=lambda series, start, end: (("2026-09-25", "3.88"),),
                nyfed_fetch=lambda: _result("nyfed-markets", "all-latest", [{"type": "SOFR"}]),
                treasury_fetch=lambda limit: _result("treasury-fiscaldata", "x", [{}]),
                cftc_fetch=lambda report, limit: _result("cftc-cot", report, [{}]),
                **_common_fakes(),
            )
        self.assertEqual(context["sources"]["eia-open-data"]["status"], "UNCONFIGURED")
        self.assertEqual(context["sources"]["finra"]["status"], "UNCONFIGURED")
        self.assertEqual(context["sources"]["bea"]["status"], "UNCONFIGURED")
        self.assertEqual(context["sources"]["usda-nass"]["status"], "UNCONFIGURED")
        self.assertEqual(context["unconfigured_sources"], 4)

    def test_provider_failure_degrades_but_does_not_fabricate(self):
        def broken(*args, **kwargs):
            raise RuntimeError("secret-bearing upstream detail")

        fakes = _common_fakes()
        fakes["nws_fetch"] = broken
        with patch.dict(os.environ, {}, clear=True):
            context = build_market_context(
                fred_fetch=broken,
                nyfed_fetch=broken,
                treasury_fetch=lambda limit: _result("treasury-fiscaldata", "x", [{}]),
                cftc_fetch=lambda report, limit: _result("cftc-cot", report, [{}]),
                **fakes,
            )
        self.assertEqual(context["status"], "DEGRADED")
        self.assertEqual(context["sources"]["nyfed-markets"]["status"], "BLOCKED")
        self.assertEqual(context["sources"]["nws"]["status"], "BLOCKED")
        self.assertIn("detail", context["sources"]["nyfed-markets"])

        from hedge_desk.market_context import _blocked

        redacted = _blocked(
            "test",
            "FAIL",
            "failed with api_key=supersecret123 UserID=bea-secret key=nass-secret",
        )
        self.assertNotIn("supersecret123", repr(redacted))
        self.assertNotIn("bea-secret", repr(redacted))
        self.assertNotIn("nass-secret", repr(redacted))
        self.assertIn("[REDACTED]", repr(redacted))


if __name__ == "__main__":
    unittest.main()
