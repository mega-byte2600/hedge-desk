"""Deterministic tests for the WTI front-month oil desk (no network)."""

import json
import tempfile
import unittest
from pathlib import Path

from hedge_desk.oil_desk import OIL_DESK_SCHEMA_VERSION, WTI_SYMBOL, oil_market
from hedge_desk.nightly import run_nightly

TIMESTAMPS = [1789584000, 1789670400, 1789756800, 1789843200, 1789929600]
CLOSES = [60.0, 61.5, 62.25, 61.75, 64.5]


def _oil_payload(symbol=WTI_SYMBOL, closes=CLOSES, timestamps=TIMESTAMPS):
    return {
        "chart": {
            "result": [
                {
                    "meta": {"symbol": symbol},
                    "timestamp": list(timestamps),
                    "indicators": {
                        "quote": [
                            {
                                "open": closes,
                                "high": closes,
                                "low": closes,
                                "close": list(closes),
                                "volume": [1000] * len(closes),
                            }
                        ]
                    },
                }
            ]
        }
    }


def _oil_transport(payload=None, status=200):
    body = json.dumps(payload if payload is not None else _oil_payload()).encode()
    seen = {}

    def transport(url):
        seen["url"] = url
        return status, body

    transport.seen = seen
    return transport


class OilDeskTests(unittest.TestCase):
    def test_oil_market_reports_close_and_change(self):
        transport = _oil_transport()
        result = oil_market(transport=transport, lookback_days=5)
        self.assertEqual(result["schema_version"], OIL_DESK_SCHEMA_VERSION)
        self.assertEqual(result["mode"], "REAL_YAHOO_WTI")
        self.assertEqual(result["symbol"], "CL=F")
        self.assertEqual(result["as_of"], "2026-09-20")
        self.assertEqual(result["last_close"], "64.5")
        self.assertEqual(result["window_first_date"], "2026-09-16")
        self.assertEqual(result["window_first_close"], "60.0")
        self.assertEqual(result["net_change_over_window"], "4.5")
        self.assertEqual(result["observation_count"], 5)
        self.assertEqual(result["data_source"], "yahoo-public-chart-v8")
        self.assertFalse(result["trade_authorized"])
        # The request targets the WTI front-month futures chart.
        self.assertIn("chart/CL=F", transport.seen["url"])

    def test_lookback_window_slices_long_series(self):
        closes = [50.0 + i for i in range(10)]
        stamps = [1789584000 + 86400 * i for i in range(10)]
        result = oil_market(
            transport=_oil_transport(_oil_payload(closes=closes, timestamps=stamps)),
            lookback_days=5,
        )
        # Last 6 closes: 54..59 -> change over the 5-day lookback is 5.0.
        self.assertEqual(result["observation_count"], 6)
        self.assertEqual(result["net_change_over_window"], "5.0")
        self.assertEqual(result["window_first_close"], "54.0")

    def test_empty_result_raises(self):
        transport = _oil_transport({"chart": {"result": []}})
        with self.assertRaises(ValueError):
            oil_market(transport=transport)

    def test_http_error_raises(self):
        transport = _oil_transport(status=500)
        with self.assertRaises(ValueError):
            oil_market(transport=transport)

    def test_malformed_json_raises(self):
        def transport(url):
            return 200, b"not json{{"

        with self.assertRaises(ValueError):
            oil_market(transport=transport)

    def test_null_close_raises(self):
        closes = [60.0, None, 62.0]
        transport = _oil_transport(_oil_payload(closes=closes, timestamps=TIMESTAMPS[:3]))
        with self.assertRaises(ValueError):
            oil_market(transport=transport)

    def test_symbol_mismatch_raises(self):
        transport = _oil_transport(_oil_payload(symbol="BZ=F"))
        with self.assertRaises(ValueError):
            oil_market(transport=transport)

    def test_invalid_lookback_raises(self):
        for bad in (0, -3, "5"):
            with self.assertRaises(ValueError):
                oil_market(transport=_oil_transport(), lookback_days=bad)


def _fake_eod_transport(url):
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


def _fake_chain_transport(url):
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


class _FakeRatesTransport:
    def __call__(self, url):
        series = url.split("id=")[1].split("&")[0]
        data = {
            "DFF": "observation_date,DFF\n2026-07-01,3.63\n2026-09-17,3.88\n",
            "DGS2": "observation_date,DGS2\n2026-09-17,4.67\n",
            "DGS10": "observation_date,DGS10\n2026-09-17,4.94\n",
        }
        return 200, data.get(series, "observation_date,VALUE\n").encode("utf-8")


def _failing_oil_transport(url):
    return 500, b""


class NightlyOilTests(unittest.TestCase):
    def _run(self, oil_transport, tmp):
        return run_nightly(
            ["AAPL"],
            artifacts_dir=tmp,
            transport=_fake_eod_transport,
            chain_transport=_fake_chain_transport,
            rates_transport=_FakeRatesTransport(),
            oil_transport=oil_transport,
        )

    def test_failing_oil_transport_blocks_without_breaking_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = self._run(_failing_oil_transport, tmp)
            oil = report["oil_market"]
            self.assertEqual(oil["mode"], "BLOCKED")
            self.assertTrue(oil["reason"])
            # The rest of the report is intact.
            self.assertEqual(report["rates_environment"]["mode"], "REAL_FRED_RATES")
            self.assertTrue(Path(report["report_path"]).exists())
            self.assertIn("WTI", report["note"])

    def test_working_oil_transport_lands_in_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = self._run(_oil_transport(), tmp)
            oil = report["oil_market"]
            self.assertEqual(oil["mode"], "REAL_YAHOO_WTI")
            self.assertEqual(oil["symbol"], "CL=F")
            self.assertEqual(oil["last_close"], "64.5")
            self.assertFalse(oil["trade_authorized"])


if __name__ == "__main__":
    unittest.main()
