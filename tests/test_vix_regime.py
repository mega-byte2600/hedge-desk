"""Deterministic tests for the VIX regime intake (no network)."""

import json
import unittest
from datetime import datetime, timezone

from hedge_desk.vix_regime import apply_vix_regime_filter, vix_regime


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

    def test_single_null_print_does_not_block_regime(self):
        # A stale null close (e.g. a holiday-shortened session months back)
        # is dropped and counted; today's regime still reads.
        payload = {
            "chart": {"result": [{
                "meta": {"symbol": "^VIX"},
                "timestamp": [1754006400, 1789761600],
                "indicators": {"quote": [{
                    "open": [None, 14.9], "high": [None, 15.0], "low": [None, 14.8],
                    "close": [None, 14.87], "volume": [0, 1000000],
                }]},
            }]}
        }
        r = vix_regime(datetime(2026, 9, 19, tzinfo=timezone.utc),
                       transport=_transport(payload))
        self.assertEqual(r["mode"], "REAL_VIX")
        self.assertEqual(r["last_close"], "14.87")
        self.assertEqual(r["dropped_null_days"], 1)
        self.assertEqual(len(r["history"]), 1)

    def test_future_day_blocked(self):
        # A chart whose last bar is dated after `now` is point-in-time
        # invalid: block rather than serve a future regime read.
        r = vix_regime(datetime(2026, 9, 19, tzinfo=timezone.utc),
                       transport=_transport(_chart("14.81", day="2026-09-20")))
        self.assertEqual(r["mode"], "BLOCKED")
        self.assertIn("future", r["reason"])

    def test_series_length_mismatch_blocked(self):
        payload = _chart("14.81")
        payload["chart"]["result"][0]["timestamp"] = [1, 2]  # 2 ts vs 1 close
        r = vix_regime(datetime(2026, 9, 19, tzinfo=timezone.utc),
                       transport=_transport(payload))
        self.assertEqual(r["mode"], "BLOCKED")
        self.assertIn("length mismatch", r["reason"])

    def test_corrupt_timestamp_blocked_not_crash(self):
        payload = _chart("14.81")
        payload["chart"]["result"][0]["timestamp"] = [10 ** 30]
        r = vix_regime(datetime(2026, 9, 19, tzinfo=timezone.utc),
                       transport=_transport(payload))
        self.assertEqual(r["mode"], "BLOCKED")
        self.assertIn("corrupt timestamp", r["reason"])

    def test_rejects_naive_cutoff(self):
        with self.assertRaises(ValueError):
            vix_regime(datetime(2026, 9, 19))


    def test_high_vix_regime_blocks_csp_candidates(self):
        csp = {"NKE": {"mode": "CASH_SECURED_PUT", "fits_gp_rules": True,
                       "eval_reasons": []}}
        vix = {"mode": "REAL_VIX", "regime": "HIGH"}
        out = apply_vix_regime_filter(vix, csp)
        self.assertFalse(out["NKE"]["fits_gp_rules"])
        self.assertIn("VIX_HIGH_REGIME", out["NKE"]["eval_reasons"])

    def test_low_vix_regime_leaves_candidates_unchanged(self):
        csp = {"NKE": {"mode": "CASH_SECURED_PUT", "fits_gp_rules": True,
                       "eval_reasons": []}}
        out = apply_vix_regime_filter({"mode": "REAL_VIX", "regime": "LOW"}, csp)
        self.assertTrue(out["NKE"]["fits_gp_rules"])
        self.assertEqual(out["NKE"]["eval_reasons"], [])

    def test_blocked_vix_leaves_candidates_unchanged(self):
        csp = {"NKE": {"mode": "CASH_SECURED_PUT", "fits_gp_rules": True,
                       "eval_reasons": []}}
        out = apply_vix_regime_filter({"mode": "BLOCKED"}, csp)
        self.assertTrue(out["NKE"]["fits_gp_rules"])


if __name__ == "__main__":
    unittest.main()