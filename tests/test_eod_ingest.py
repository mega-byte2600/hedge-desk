"""Deterministic tests for the real EOD ingest adapter (no network)."""

import json
import unittest
from datetime import datetime, timezone

from hedge_desk.data.eod_ingest import (
    EOD_INGEST_VERSION,
    EOD_SOURCE_ID,
    _canonical_payload,
    _parse_chart_payload,
    ingest_eod,
)

TS = 1789761600  # 2026-09-18-ish epoch


def _chart_payload(symbol, timestamps=(TS - 86400, TS), nulls=()):
    quote = {
        "open": [100.0, 101.5],
        "high": [102.0, 103.0],
        "low": [99.0, 100.5],
        "close": [101.0, 102.25],
        "volume": [1000, 1200],
    }
    for i, field in nulls:
        quote[field][i] = None
    return {
        "chart": {
            "result": [
                {
                    "meta": {"symbol": symbol},
                    "timestamp": list(timestamps),
                    "indicators": {"quote": [quote]},
                }
            ]
        }
    }.__repr__()


def _transport_for(raw: bytes, status: int = 200):
    return lambda url: (status, raw)


def _ok_transport(symbol="AAPL"):
    payload = {
        "chart": {
            "result": [
                {
                    "meta": {"symbol": symbol},
                    "timestamp": [TS - 86400, TS],
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
    return lambda url: (200, json.dumps(payload).encode("utf-8"))


class EodIngestTests(unittest.TestCase):
    def setUp(self):
        self.cutoff = datetime(2026, 9, 19, 15, 0, tzinfo=timezone.utc)

    def test_real_batch_passes_and_is_non_synthetic(self):
        result = ingest_eod(["AAPL"], self.cutoff, transport=_ok_transport("AAPL"))
        src = result["source_results"][0]
        self.assertEqual(result["mode"], "REAL_EOD_BATCH")
        self.assertEqual(result["batch_status"], "READY_FOR_RESEARCH")
        self.assertEqual(src["status"], "PASS")
        self.assertEqual(src["reason_codes"], [])
        self.assertEqual(src["days_count"], 2)
        self.assertEqual(len(src["artifact_sha256"]), 64)
        artifact = result["artifacts"]["AAPL"]
        self.assertFalse(artifact["synthetic"])
        self.assertFalse(artifact["redistribution_allowed"])
        self.assertEqual(artifact["source_id"], EOD_SOURCE_ID)

    def test_transport_failure_quarantines(self):
        result = ingest_eod(["AAPL"], self.cutoff, transport=lambda url: (0, b""))
        src = result["source_results"][0]
        self.assertEqual(src["status"], "QUARANTINE")
        self.assertEqual(src["reason_codes"], ["TRANSPORT_FAILED"])
        self.assertNotEqual(result["batch_status"], "READY_FOR_RESEARCH")

    def test_unknown_symbol_maps_to_symbol_unknown(self):
        result = ingest_eod(["AAPL"], self.cutoff, transport=lambda url: (404, b"{}"))
        self.assertEqual(result["source_results"][0]["reason_codes"], ["SYMBOL_UNKNOWN"])

    def test_malformed_payload_rejected(self):
        result = ingest_eod(["AAPL"], self.cutoff, transport=lambda url: (200, b"not json"))
        self.assertEqual(result["source_results"][0]["status"], "REJECT")
        self.assertEqual(result["source_results"][0]["reason_codes"], ["PAYLOAD_MALFORMED"])

    def test_future_day_rejected(self):
        # Timestamp after cutoff -> FUTURE_DAY rejection.
        future = int(datetime(2026, 9, 30, tzinfo=timezone.utc).timestamp())
        result = ingest_eod(["AAPL"], self.cutoff, transport=_ok_transport_future(future))
        self.assertEqual(result["source_results"][0]["reason_codes"], ["FUTURE_DAY"])

    def test_canonical_payload_is_deterministic(self):
        from hedge_desk.data.eod_ingest import EodDay

        days = (EodDay("2026-09-18", "102.25", "101.5", "103.0", "100.5", 1200),)
        a = _canonical_payload("AAPL", days)
        b = _canonical_payload("AAPL", days)
        self.assertEqual(a, b)

    def test_parse_rejects_series_length_mismatch(self):
        days, reason = _parse_chart_payload("X", b'{"chart":{"result":[{"meta":{"symbol":"X"},"timestamp":[1],"indicators":{"quote":[{"open":[],"close":[1],"volume":[2]}]}}]}}')
        self.assertEqual(days, ())
        self.assertEqual(reason, "SERIES_LENGTH_MISMATCH")


def _ok_transport_future(future_ts):
    payload = {
        "chart": {
            "result": [
                {
                    "meta": {"symbol": "AAPL"},
                    "timestamp": [future_ts],
                    "indicators": {
                        "quote": [
                            {
                                "open": [100.0],
                                "high": [102.0],
                                "low": [99.0],
                                "close": [101.0],
                                "volume": [1000],
                            }
                        ]
                    },
                }
            ]
        }
    }
    return lambda url: (200, json.dumps(payload).encode("utf-8"))


if __name__ == "__main__":
    unittest.main()