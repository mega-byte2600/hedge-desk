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


def _fake_csp_transport(url):
    # A Cboe-chain-shaped payload with a ~10% OTM put so the CSP scan finds a
    # candidate offline (symbol-agnostic; the scan reads the payload).
    import json
    payload = {
        "data": {
            "symbol": "AAPL", "current_price": "100.00", "bid": "100.00", "ask": "100.00",
            "options": [
                {"option": "AAPL261023P00090000", "bid": 1.19, "ask": 1.25,
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
                       vix_transport=_fake_transport, macro_transport=_fake_rates_transport)
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

    def test_report_is_verifiable(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = run_nightly(["AAPL"], artifacts_dir=tmp, transport=_fake_transport,
                       chain_transport=_fake_chain_transport, csp_transport=_fake_csp_transport,
                       rates_transport=_fake_rates_transport,
                       vix_transport=_fake_transport, macro_transport=_fake_rates_transport)
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