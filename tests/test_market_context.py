import os
import unittest
from unittest.mock import patch

from hedge_desk.data.open_market_feeds import OpenFeedResult
from hedge_desk.market_context import MARKET_CONTEXT_SCHEMA, build_market_context


def _result(provider, dataset, rows):
    return OpenFeedResult(provider, dataset, tuple(rows))


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

        with patch.dict(
            os.environ,
            {
                "EIA_API_KEY": "do-not-return",
                "FINRA_CLIENT_ID": "client-id",
                "FINRA_CLIENT_SECRET": "do-not-return-secret",
            },
            clear=False,
        ):
            context = build_market_context(
                fred_fetch=lambda series, start, end: (("2026-09-25", "3.88"),),
                bls_fetch=lambda series: _result("bls", series, [{}]),
                ecb_fetch=lambda currencies: _result("ecb-fx", "EXR", [{}]),
                bls_fetch=lambda series: _result(
                    "bls", series, [{"seriesID": series, "year": "2026", "period": "M08", "value": "325.0"}]
                ),
                ecb_fetch=lambda currencies: _result(
                    "ecb-fx", "EXR", [{"CURRENCY": "USD", "CURRENCY_DENOM": "EUR", "TIME_PERIOD": "2026-09-25", "OBS_VALUE": "1.17"}]
                ),
                nyfed_fetch=nyfed_fetch,
                treasury_fetch=treasury_fetch,
                cftc_fetch=cftc_fetch,
                eia_fetch=eia_fetch,
                finra_fetch=finra_fetch,
            )

        self.assertEqual(context["schema_version"], MARKET_CONTEXT_SCHEMA)
        self.assertEqual(context["status"], "LIVE")
        self.assertEqual(context["live_sources"], 8)
        self.assertEqual(context["blocked_sources"], 0)
        self.assertEqual(context["unconfigured_sources"], 0)
        self.assertFalse(context["trade_authorized"])
        self.assertEqual(
            context["sources"]["nyfed-markets"]["observations"]["SOFR"]["percentRate"],
            3.88,
        )
        self.assertNotIn("do-not-return", repr(context))
        self.assertNotIn("do-not-return-secret", repr(context))
        self.assertIn(("corporateMarketBreadth", 10), calls)

    def test_keyed_sources_are_explicitly_unconfigured(self):
        with patch.dict(os.environ, {}, clear=True):
            context = build_market_context(
                fred_fetch=lambda series, start, end: (("2026-09-25", "3.88"),),
                nyfed_fetch=lambda: _result("nyfed-markets", "all-latest", [{"type": "SOFR"}]),
                treasury_fetch=lambda limit: _result("treasury-fiscaldata", "x", [{}]),
                cftc_fetch=lambda report, limit: _result("cftc-cot", report, [{}]),
            )
        self.assertEqual(context["sources"]["eia-open-data"]["status"], "UNCONFIGURED")
        self.assertEqual(context["sources"]["finra"]["status"], "UNCONFIGURED")
        self.assertEqual(context["unconfigured_sources"], 2)

    def test_provider_failure_degrades_but_does_not_fabricate(self):
        def broken():
            raise RuntimeError("secret-bearing upstream detail")

        with patch.dict(os.environ, {}, clear=True):
            context = build_market_context(
                fred_fetch=broken,
                bls_fetch=lambda series: _result("bls", series, [{}]),
                ecb_fetch=lambda currencies: _result("ecb-fx", "EXR", [{}]),
                nyfed_fetch=broken,
                treasury_fetch=lambda limit: _result("treasury-fiscaldata", "x", [{}]),
                cftc_fetch=lambda report, limit: _result("cftc-cot", report, [{}]),
            )
        self.assertEqual(context["status"], "DEGRADED")
        self.assertEqual(context["sources"]["nyfed-markets"]["status"], "BLOCKED")
        # Error details are now surfaced for diagnostics (with credentials redacted),
        # so the raw message appears — but actual secrets must never leak.
        self.assertIn("detail", context["sources"]["nyfed-markets"])
        # Credential patterns are redacted
        from hedge_desk.market_context import _blocked
        redacted = _blocked("test", "FAIL", "failed with api_key=supersecret123")
        self.assertNotIn("supersecret123", repr(redacted))
        self.assertIn("[REDACTED]", repr(redacted))


if __name__ == "__main__":
    unittest.main()
