"""Deterministic tests for the nightly orchestrator (no network)."""

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from hedge_desk.nightly import NIGHTLY_VERSION, run_nightly


def _fake_chain_transport(url):
    # A minimal Cboe-chain-shaped payload with a valid OTM call, so the nightly
    # chain step produces one real-structure income row in offline tests.
    import json

    payload = {
        "data": {
            "symbol": "SPY",
            "current_price": "760.00",
            "bid": "760.00",
            "ask": "760.00",
            "options": [
                {
                    "option": "SPY261023C00764000",
                    "bid": 2.0,
                    "ask": 2.2,
                    "bid_size": 25,
                    "ask_size": 30,
                    "open_interest": 500,
                    "volume": 200,
                },
                {
                    "option": "SPY261023P00756000",
                    "bid": 2.5,
                    "ask": 2.7,
                    "bid_size": 25,
                    "ask_size": 30,
                    "open_interest": 500,
                    "volume": 200,
                },
            ],
        }
    }
    return 200, json.dumps(payload).encode("utf-8")


def _fake_transport(url):
    symbol = url.split("chart/")[1].split("?")[0]
    payload = {
        "chart": {
            "result": [
                {
                    "meta": {"symbol": symbol},
                    "timestamp": [1789761600 - 86400, 1789761600],
                    "indicators": {
                        "quote": [
                            {
                                "open": [100.0, 101.5],
                                "high": [102.0, 103.0],
                                "low": [99.0, 100.5],
                                "close": [101.0, 102.25],
                                "volume": [1000, 1200],
                            }
                        ]
                    },
                }
            ]
        }
    }
    return 200, json.dumps(payload).encode("utf-8")


def _fake_rates_transport(url):
    # FRED CSV for the series id in the URL (DFF/DGS2/DGS10).
    series = url.split("id=")[1].split("&")[0]
    values = {"DFF": "3.88", "DGS2": "4.67", "DGS10": "4.94"}
    v = values.get(series, "1.0")
    return 200, f"observation_date,{series}\n2026-09-17,{v}\n".encode("utf-8")


def _fake_vix_transport(url):
    # A low VIX (14.81 -> LOW regime) so the regime risk filter does not block
    # the CSP candidates in the offline nightly test.
    import json
    ts = 1789761600
    payload = {
        "chart": {"result": [{
            "meta": {"symbol": "^VIX"},
            "timestamp": [ts],
            "indicators": {"quote": [{
                "open": [14.5], "high": [15.0], "low": [14.4],
                "close": [14.81], "volume": [1000000],
            }]},
        }]}
    }
    return 200, json.dumps(payload).encode("utf-8")


def _fake_csp_transport(url):
    # A Cboe-chain-shaped payload with a ~10% OTM put that FITS the GP wheel
    # (sub-$5k collateral, return-on-capital in band) so the CSP scan finds a
    # fits_gp_rules candidate offline. current_price 36 -> target strike ~32.4,
    # nearest 32; bid 0.41 -> collateral $3,200, RoC 1.28% (in 0.5-2% band).
    # Expiration is computed RELATIVE to today (38 DTE) so the fixture stays in
    # the 30-45 DTE window no matter when the test runs — a hardcoded date drifts
    # out of band as real time advances (was 2026-10-23, broke after 2026-09-25).
    import json
    from datetime import datetime, timedelta, timezone
    exp = (datetime.now(timezone.utc) + timedelta(days=38)).strftime("%y%m%d")
    payload = {
        "data": {
            "symbol": "AAPL", "current_price": "36.00", "bid": "36.00", "ask": "36.10",
            "options": [
                {"option": f"AAPL{exp}P00032000", "bid": 0.41, "ask": 0.45,
                 "bid_size": 25, "ask_size": 30, "open_interest": 500, "volume": 200},
            ],
        }
    }
    return 200, json.dumps(payload).encode("utf-8")


class NightlyTests(unittest.TestCase):
    def test_run_nightly_writes_content_addressed_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = run_nightly(["AAPL"], artifacts_dir=tmp, transport=_fake_transport,
                       chain_transport=_fake_chain_transport, csp_transport=_fake_csp_transport,
                       rates_transport=_fake_rates_transport,
                       vix_transport=_fake_vix_transport, macro_transport=_fake_rates_transport)
            self.assertEqual(report["schema_version"], NIGHTLY_VERSION)
            self.assertEqual(report["mode"], "REAL_EOD_NIGHTLY")
            self.assertEqual(len(report["report_sha256"]), 64)
            self.assertIn("report_path", report)
            path = Path(report["report_path"])
            self.assertTrue(path.exists())
            # No secrets/PII fields anywhere.
            blob = json.dumps(report).lower()
            for banned in ("token", "password", "secret", "oauth", "apikey"):
                self.assertNotIn(banned, blob)
            # No trade authorized.
            self.assertTrue(
                all(not c["trade_authorized"] for c in report["candidates"])
            )
            # ENGINEER peer-review: green must mean the desk WORKED, not just that
            # a report-shaped object was produced. Assert real content.
            self.assertGreaterEqual(len(report["candidates"]), 1,
                                    "nightly produced no equity candidates")
            self.assertTrue(report["candidates"][0]["symbol"],
                            "candidate missing symbol")
            # the fake csp transport returns a ~10% OTM put -> must fit the wheel
            csp = report["cash_secured_put_scan"]
            self.assertTrue(any(v.get("fits_gp_rules") for v in csp.values()),
                            "no cash-secured-put candidate fits the GP wheel")
            # real-data desks present and honest
            self.assertEqual(report["vix_regime"]["mode"], "REAL_VIX")
            self.assertIn("macro_environment", report)
            self.assertIn("data_freshness", report)
            self.assertIsInstance(report["data_freshness"]["is_current"], bool)

    def test_report_is_verifiable(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = run_nightly(["AAPL"], artifacts_dir=tmp, transport=_fake_transport,
                       chain_transport=_fake_chain_transport, csp_transport=_fake_csp_transport,
                       rates_transport=_fake_rates_transport,
                       vix_transport=_fake_vix_transport, macro_transport=_fake_rates_transport)
            body = {
                k: v
                for k, v in report.items()
                if k not in ("report_sha256", "report_path", "latest_path")
            }
            expected = hashlib.sha256(
                json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ).hexdigest()
            self.assertEqual(report["report_sha256"], expected)


if __name__ == "__main__":
    unittest.main()