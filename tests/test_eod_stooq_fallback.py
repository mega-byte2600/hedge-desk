"""Deterministic tests for the Yahoo -> Stooq EOD fallback (no network).

Handoff 2026-09-26 (data-source redundancy): when Yahoo's chart API fails,
the EOD ingest falls back to Stooq's free CSV before giving up. The result's
source_id says which source actually served the data. If both fail, the
symbol is QUARANTINED honestly — never invented.
"""

import json
import unittest
from datetime import datetime, timezone

from hedge_desk.data.eod_ingest import (
    EOD_SOURCE_ID,
    STOOQ_SOURCE_ID,
    _fetch_one_symbol,
    _parse_stooq_csv,
)

_CUTOFF = datetime(2026, 9, 26, 20, 0, tzinfo=timezone.utc)

_YAHOO_JSON = json.dumps(
    {
        "chart": {
            "result": [
                {
                    "meta": {"symbol": "AAPL"},
                    "timestamp": [1758844800, 1758931200],
                    "indicators": {
                        "quote": [
                            {
                                "open": [770.0, 774.0],
                                "high": [775.0, 776.0],
                                "low": [768.0, 772.0],
                                "close": [774.0, 775.0],
                                "volume": [1000, 2000],
                            }
                        ]
                    },
                }
            ]
        }
    }
).encode("utf-8")

_STOOQ_CSV = b"""Date,Open,High,Low,Close,Volume
2026-09-25,770.10,775.50,768.00,774.25,1234567
2026-09-26,774.30,776.00,772.10,775.80,987654"""


class StooqParseTests(unittest.TestCase):
    def test_parses_valid_csv(self):
        days, reason = _parse_stooq_csv("AAPL", _STOOQ_CSV)
        self.assertEqual(reason, "")
        self.assertEqual(len(days), 2)
        self.assertEqual(days[0].date, "2026-09-25")
        self.assertEqual(days[1].close, "775.80")
        self.assertEqual(days[1].volume, 987654)

    def test_skips_nd_rows(self):
        raw = b"""Date,Open,High,Low,Close,Volume
2026-09-25,N/D,N/D,N/D,N/D,0
2026-09-26,774.30,776.00,772.10,775.80,987654"""
        days, reason = _parse_stooq_csv("AAPL", raw)
        self.assertEqual(len(days), 1)
        self.assertEqual(days[0].date, "2026-09-26")

    def test_empty_csv(self):
        days, reason = _parse_stooq_csv("AAPL", b"Date,Open,High,Low,Close,Volume\n")
        self.assertEqual(days, ())
        self.assertEqual(reason, "EMPTY_PAYLOAD")

    def test_malformed(self):
        days, reason = _parse_stooq_csv("AAPL", b"not a csv at all\n")
        self.assertEqual(days, ())
        self.assertIn(reason, ("EMPTY_PAYLOAD", "PAYLOAD_MALFORMED"))


class FallbackTests(unittest.TestCase):
    def test_yahoo_primary_no_fallback(self):
        def yahoo_ok(url):
            if "yahoo" in url:
                return 200, _YAHOO_JSON
            raise AssertionError("Stooq must not be called when Yahoo works")

        r = _fetch_one_symbol("AAPL", yahoo_ok, "5d", _CUTOFF)
        self.assertEqual(r.status.value, "PASS")
        self.assertEqual(r.source_id, EOD_SOURCE_ID)
        self.assertEqual(len(r.days), 2)

    def test_yahoo_down_stooq_serves(self):
        seen = []

        def yahoo_down(url):
            seen.append(url)
            if "yahoo" in url:
                return 500, b""
            if "stooq" in url:
                return 200, _STOOQ_CSV
            return 404, b""

        r = _fetch_one_symbol("AAPL", yahoo_down, "5d", _CUTOFF)
        self.assertEqual(r.status.value, "PASS")
        self.assertEqual(r.source_id, STOOQ_SOURCE_ID)
        self.assertEqual(len(r.days), 2)
        self.assertEqual(r.days[-1].close, "775.80")
        # Stooq URL uses lowercase .us symbol and date window.
        stooq_urls = [u for u in seen if "stooq" in u]
        self.assertTrue(stooq_urls)
        self.assertIn("aapl.us", stooq_urls[0])

    def test_yahoo_malformed_stooq_serves(self):
        def yahoo_garbage(url):
            if "yahoo" in url:
                return 200, b"{not json"
            if "stooq" in url:
                return 200, _STOOQ_CSV
            return 404, b""

        r = _fetch_one_symbol("AAPL", yahoo_garbage, "5d", _CUTOFF)
        self.assertEqual(r.status.value, "PASS")
        self.assertEqual(r.source_id, STOOQ_SOURCE_ID)

    def test_both_down_honest_quarantine(self):
        def both_down(url):
            return 0, b""

        r = _fetch_one_symbol("AAPL", both_down, "5d", _CUTOFF)
        self.assertEqual(r.status.value, "QUARANTINE")
        self.assertEqual(r.days, ())
        self.assertEqual(r.artifact_sha256, "0" * 64)


if __name__ == "__main__":
    unittest.main()
