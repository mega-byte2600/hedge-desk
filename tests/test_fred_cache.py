"""Deterministic tests for the FRED observation disk cache (no network)."""

import os
import tempfile
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

from hedge_desk.rates_desk import fred_series_rows


CSV = "observation_date,DGS10\n2026-09-16,4.90\n2026-09-17,4.94\n"


class _FakeTransport:
    def __init__(self):
        self.calls = 0

    def __call__(self, url):
        self.calls += 1
        return 200, CSV.encode("utf-8")


class _FailingTransport:
    def __call__(self, url):
        raise AssertionError("transport must not be called on a cache hit")


class FredCacheTests(unittest.TestCase):
    def setUp(self):
        self._old = os.environ.get("HEDGE_DESK_CACHE_DIR")
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["HEDGE_DESK_CACHE_DIR"] = self.tmp.name
        self.start = date(2026, 7, 19)
        self.end = date(2026, 9, 17)

    def tearDown(self):
        if self._old is None:
            os.environ.pop("HEDGE_DESK_CACHE_DIR", None)
        else:
            os.environ["HEDGE_DESK_CACHE_DIR"] = self._old
        self.tmp.cleanup()

    def _cache_file(self):
        return (
            Path(self.tmp.name)
            / "fred"
            / "DGS10"
            / f"{self.start.isoformat()}_{self.end.isoformat()}.json"
        )

    def test_miss_fetches_and_writes_cache(self):
        t = _FakeTransport()
        rows = fred_series_rows("DGS10", self.start, self.end, t)
        self.assertEqual(t.calls, 1)
        self.assertEqual(rows[-1], ("2026-09-17", Decimal("4.94")))
        self.assertTrue(self._cache_file().is_file())

    def test_hit_skips_transport(self):
        t = _FakeTransport()
        fred_series_rows("DGS10", self.start, self.end, t)
        rows = fred_series_rows("DGS10", self.start, self.end, _FailingTransport())
        self.assertEqual(rows[-1], ("2026-09-17", Decimal("4.94")))

    def test_corrupt_cache_falls_through_to_fetch(self):
        f = self._cache_file()
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("{not json", encoding="utf-8")
        t = _FakeTransport()
        rows = fred_series_rows("DGS10", self.start, self.end, t)
        self.assertEqual(t.calls, 1)
        self.assertEqual(rows[-1][1], Decimal("4.94"))

    def test_different_windows_do_not_collide(self):
        t = _FakeTransport()
        fred_series_rows("DGS10", self.start, self.end, t)
        other_end = date(2026, 9, 16)
        fred_series_rows("DGS10", self.start, other_end, t)
        self.assertEqual(t.calls, 2)

    def test_cache_disabled_skips_disk(self):
        os.environ["HEDGE_DESK_CACHE_DIR"] = "off"
        t = _FakeTransport()
        fred_series_rows("DGS10", self.start, self.end, t)
        fred_series_rows("DGS10", self.start, self.end, t)
        self.assertEqual(t.calls, 2)
        self.assertFalse((Path(self.tmp.name) / "fred").exists())

    def test_transport_failure_raises_fail_closed(self):
        def boom(url):
            return 500, b""

        with self.assertRaises(ValueError):
            fred_series_rows("DGS10", self.start, self.end, boom)


if __name__ == "__main__":
    unittest.main()
