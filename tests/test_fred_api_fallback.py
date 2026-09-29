"""Deterministic tests for the FRED API-key fallback route (no network).

``hedge_desk.rates_desk`` defaults to the no-auth FRED CSV endpoint. When
FRED_API_KEY is set, it uses the official FRED JSON API instead — same
source, alternate route for networks where the CSV download stalls. The key
is free at https://fred.stlouisfed.org/docs/api/api_key.html

These tests use fake transports; they never touch the network or the
production cache.
"""

import datetime as _dt
import json
import os
import unittest
from decimal import Decimal

from hedge_desk.rates_desk import (
    _fred_url,
    _parse_fred_json,
    fred_series_rows,
)

_START = _dt.date(2026, 9, 1)
_END = _dt.date(2026, 9, 26)

_JSON_BODY = json.dumps(
    {
        "observations": [
            {"date": "2026-09-24", "value": "5.18"},
            {"date": "2026-09-25", "value": "."},  # FRED marks missing as "."
            {"date": "2026-09-26", "value": "5.20"},
        ]
    }
).encode("utf-8")


class FredUrlTests(unittest.TestCase):
    def setUp(self):
        self._old = os.environ.get("FRED_API_KEY")

    def tearDown(self):
        if self._old is None:
            os.environ.pop("FRED_API_KEY", None)
        else:
            os.environ["FRED_API_KEY"] = self._old

    def test_no_key_uses_csv_route(self):
        os.environ.pop("FRED_API_KEY", None)
        url, keyed = _fred_url("DGS10", _START, _END)
        self.assertFalse(keyed)
        self.assertIn("fredgraph.csv", url)
        self.assertIn("id=DGS10", url)

    def test_key_set_uses_official_api_route(self):
        os.environ["FRED_API_KEY"] = "TESTKEY"
        url, keyed = _fred_url("DGS10", _START, _END)
        self.assertTrue(keyed)
        self.assertIn("api.stlouisfed.org/fred/series/observations", url)
        self.assertIn("series_id=DGS10", url)

    def test_blank_key_falls_back_to_csv(self):
        os.environ["FRED_API_KEY"] = "   "
        url, keyed = _fred_url("DGS10", _START, _END)
        self.assertFalse(keyed)
        self.assertIn("fredgraph.csv", url)


class FredJsonParseTests(unittest.TestCase):
    def test_parses_observations_skipping_missing(self):
        rows = _parse_fred_json(_JSON_BODY)
        self.assertEqual(
            rows,
            (
                ("2026-09-24", Decimal("5.18")),
                ("2026-09-26", Decimal("5.20")),
            ),
        )

    def test_empty_observations(self):
        rows = _parse_fred_json(b'{"observations": []}')
        self.assertEqual(rows, ())


class FredKeyedFetchTests(unittest.TestCase):
    def setUp(self):
        self._old = os.environ.get("FRED_API_KEY")
        self._old_cache = os.environ.get("HEDGE_DESK_CACHE_DIR")
        os.environ["FRED_API_KEY"] = "TESTKEY"
        os.environ["HEDGE_DESK_CACHE_DIR"] = "off"

    def tearDown(self):
        if self._old is None:
            os.environ.pop("FRED_API_KEY", None)
        else:
            os.environ["FRED_API_KEY"] = self._old
        if self._old_cache is None:
            os.environ.pop("HEDGE_DESK_CACHE_DIR", None)
        else:
            os.environ["HEDGE_DESK_CACHE_DIR"] = self._old_cache

    def test_keyed_fetch_hits_api_and_parses(self):
        seen = {}

        def fake_api(url):
            seen["url"] = url
            self.assertIn("api.stlouisfed.org", url)
            return 200, _JSON_BODY

        rows = fred_series_rows(
            "DGS10", _START, _END, transport=fake_api
        )
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ("2026-09-24", Decimal("5.18")))
        # Key travels only inside the transport URL, never printed/logged here.
        self.assertIn("api_key=TESTKEY", seen["url"])

    def test_keyed_fetch_failure_is_honest(self):
        def fake_down(url):
            return 0, b""

        with self.assertRaises(ValueError) as ctx:
            fred_series_rows(
                "DGS10", _START, _END, transport=fake_down, retries=0
            )
        self.assertIn("fred fetch failed", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
