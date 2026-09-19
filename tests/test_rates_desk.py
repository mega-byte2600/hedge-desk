"""Deterministic tests for the real FRED rates desk (no network)."""

import unittest
from datetime import date
from decimal import Decimal

from hedge_desk.rates_desk import (
    _parse_fred_csv,
    rates_environment,
)


class _FakeTransport:
    def __init__(self, data):
        self.data = data  # series_id -> csv text

    def __call__(self, url):
        series = url.split("id=")[1].split("&")[0]
        csv = self.data.get(series, "observation_date,VALUE\n")
        return 200, csv.encode("utf-8")


class RatesDeskTests(unittest.TestCase):
    def test_parse_fred_csv(self):
        raw = "observation_date,DFF\n2026-09-16,3.63\n2026-09-17,3.88\n".encode()
        rows = _parse_fred_csv(raw)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][1], Decimal("3.63"))
        self.assertEqual(rows[-1][1], Decimal("3.88"))

    def test_rates_environment_reports_curve_and_change(self):
        data = {
            "DFF": "observation_date,DFF\n2026-07-01,3.63\n2026-09-17,3.88\n",
            "DGS2": "observation_date,DGS2\n2026-09-17,4.67\n",
            "DGS10": "observation_date,DGS10\n2026-09-17,4.94\n",
        }
        result = rates_environment(
            lookback_days=60, transport=_FakeTransport(data), as_of=date(2026, 9, 17)
        )
        self.assertEqual(result["mode"], "REAL_FRED_RATES")
        self.assertEqual(result["fed_funds_effective_rate"], "3.88")
        self.assertEqual(result["fed_funds_change_over_window"], "0.25")
        self.assertEqual(result["curve_shape"], "UPWARD_SLOPING")
        self.assertFalse(result["trade_authorized"])
        self.assertEqual(result["data_source"], "fred-public-csv-http-200")

    def test_rates_environment_inverted_curve(self):
        data = {
            "DFF": "observation_date,DFF\n2026-07-01,3.63\n2026-09-17,3.88\n",
            "DGS2": "observation_date,DGS2\n2026-09-17,5.10\n",
            "DGS10": "observation_date,DGS10\n2026-09-17,4.80\n",
        }
        result = rates_environment(
            lookback_days=60, transport=_FakeTransport(data), as_of=date(2026, 9, 17)
        )
        self.assertEqual(result["curve_shape"], "INVERTED")
        self.assertTrue(result["spread_10y_2y_points"].startswith("-"))


if __name__ == "__main__":
    unittest.main()