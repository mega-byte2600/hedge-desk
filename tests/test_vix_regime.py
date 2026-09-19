"""Deterministic tests for the VIX regime intake (no network)."""

import json
import unittest
from datetime import datetime, timezone

from hedge_desk.vix_regime import vix_regime


def _chart(close, symbol="^VIX", day="2026-09-18"):
    ts = int(datetime.fromisoformat(day + "T00:00:00+00:00").timestamp())
    return {
        "chart": {
            "result": [{
                "meta": {"symbol": symbol},
                "timestamp": [ts],
                "indicators": {"quote": [{
                    "open": [close], "high": [close], "low": [close],
                    "close": [close], "volume": [1000000],
                }]},
            }]
        }
    }


def _transport(payload):
    return lambda url: (200, json.dumps(payload).encode("utf-8"))


class VixRegimeTests(unittest.TestCase):
    def test_low_regime(self):
        r = vix_regime(datetime(2026, 9, 19, tzinfo=timezone.utc),
                       transport=_transport(_chart("14.81")))
        self.assertEqual(r["mode"], "REAL_VIX")
        self.assertEqual(r["regime"], "LOW")
        self.assertEqual(r["last_close"], "14.81")

    def test_elevated_regime(self):
        r = vix_regime(datetime(2026, 9, 19, tzinfo=timezone.utc),
                       transport=_transport(_chart("24.5")))
        self.assertEqual(r["regime"], "ELEVATED")

    def test_high_regime(self):
        r = vix_regime(datetime(2026, 9, 19, tzinfo=timezone.utc),
                       transport=_transport(_chart("35.0")))
        self.assertEqual(r["regime"], "HIGH")

    def test_blocked_on_transport_failure(self):
        r = vix_regime(datetime(2026, 9, 19, tzinfo=timezone.utc),
                       transport=lambda url: (500, b""))
        self.assertEqual(r["mode"], "BLOCKED")

    def test_rejects_naive_cutoff(self):
        with self.assertRaises(ValueError):
            vix_regime(datetime(2026, 9, 19))


if __name__ == "__main__":
    unittest.main()