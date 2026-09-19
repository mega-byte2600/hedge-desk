"""Deterministic tests for the feature plane (no network)."""

import unittest
from decimal import Decimal

from hedge_desk.data.eod_ingest import EodDay
from hedge_desk.features import (
    FEATURES_VERSION,
    build_feature_bundle_from_days,
    build_symbol_features,
)


def _series(closes):
    """Build a rising closes series with fixed OHLC; deterministic."""
    days = []
    for i, c in enumerate(closes):
        days.append(EodDay(
            f"2026-{(i//28)+1:02d}-{(i%28)+1:02d}",
            str(c), str(c - Decimal("0.5")), str(c + Decimal("1")),
            str(c - Decimal("1")), 1000,
        ))
    return days


class FeaturePlaneTests(unittest.TestCase):
    def test_return_windows(self):
        # 25 rising bars: 1d, 5d, 21d returns all present.
        closes = [Decimal(100 + i) for i in range(25)]
        f = build_symbol_features("TEST", _series(closes))
        self.assertIsNotNone(f.return_1d)
        self.assertIsNotNone(f.return_5d)
        self.assertIsNotNone(f.return_21d)
        self.assertGreater(Decimal(f.return_21d), Decimal("0"))
        self.assertEqual(f.source_days, 25)

    def test_insufficient_bars_for_21d(self):
        closes = [Decimal(100 + i) for i in range(5)]
        f = build_symbol_features("TEST", _series(closes))
        self.assertIsNone(f.return_21d)
        self.assertIsNone(f.realized_vol_21d)
        self.assertIn("NEED_22_BARS_FOR_21D", f.reason_codes)

    def test_candle_bias(self):
        # All candles close > open -> bias +1; descending -> -1.
        up = [EodDay("2026-09-01", "110", "100", "112", "99", 1000)]
        self.assertEqual(build_symbol_features("X", up).candle_bias, 1)
        down = [EodDay("2026-09-01", "90", "100", "101", "88", 1000)]
        self.assertEqual(build_symbol_features("X", down).candle_bias, -1)

    def test_determinism(self):
        closes = [Decimal(100 + i) for i in range(30)]
        days = _series(closes)
        a = build_feature_bundle_from_days({"T": days})
        b = build_feature_bundle_from_days({"T": days})
        self.assertEqual(a["schema_version"], FEATURES_VERSION)
        self.assertEqual(
            a["features"]["T"]["feature_sha256"],
            b["features"]["T"]["feature_sha256"],
        )

    def test_never_authorizes_or_predicts(self):
        closes = [Decimal(100 + i) for i in range(30)]
        b = build_feature_bundle_from_days({"T": _series(closes)})
        self.assertNotIn("trade_authorized", json_check(b))

    def test_flat_range_position_is_none(self):
        rows = [EodDay(f"2026-{i:02d}-01", "50", "50", "50", "50", 1000) for i in range(1, 22)]
        f = build_symbol_features("X", rows)
        # flat high==low -> range_position stays None (no quadratic loss)
        self.assertIsNone(f.range_position_21d)


def json_check(bundle):
    import json
    return json.dumps(bundle).lower()


if __name__ == "__main__":
    unittest.main()