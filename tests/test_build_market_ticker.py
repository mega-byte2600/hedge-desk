"""Unit tests for scripts/build_market_ticker.py.

No network: HTTP fetchers and the FRED helper are stubbed. The tests
pin market-hours gating, the fallback chain and quarantine rule, the
payload parsers (Yahoo bars, Nasdaq chart, FRED observations), and
the skip-if-unchanged comparison.
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_market_ticker", ROOT / "scripts" / "build_market_ticker.py"
)
assert SPEC is not None and SPEC.loader is not None
gmt = importlib.util.module_from_spec(SPEC)
sys.modules["build_market_ticker"] = gmt
SPEC.loader.exec_module(gmt)

ET = ZoneInfo("America/New_York")


def et_moment(day, hour, minute=0):
    return datetime(2026, 11, day, hour, minute, tzinfo=ET)


def canned_quote(symbol="SPY", **overrides):
    quote = {
        "symbol": symbol,
        "label": symbol,
        "kind": "etf",
        "price": 757.12,
        "previous_close": 759.81,
        "change": -2.69,
        "change_pct": -0.3541,
        "market_date": "2026-11-12",
        "quote_time": "2026-11-12T21:00:00Z",
        "time_basis": "bar",
        "session": "close",
        "source": "Yahoo Finance v8 chart",
        "currency": "USD",
    }
    quote.update(overrides)
    return quote


class MarketStateTest(unittest.TestCase):
    def test_session_boundaries(self):
        # Friday 2026-11-13.
        self.assertEqual(gmt.market_state(et_moment(13, 9, 29)), "pre-market")
        self.assertEqual(gmt.market_state(et_moment(13, 9, 30)), "session")
        self.assertEqual(gmt.market_state(et_moment(13, 15, 59)), "session")
        self.assertEqual(gmt.market_state(et_moment(13, 16, 0)), "close-window")
        self.assertEqual(gmt.market_state(et_moment(13, 16, 34)), "close-window")
        self.assertEqual(gmt.market_state(et_moment(13, 16, 35)), "after-hours")
        self.assertEqual(gmt.market_state(et_moment(13, 21, 0)), "after-hours")

    def test_weekend_is_quiet(self):
        self.assertEqual(gmt.market_state(et_moment(14, 10, 0)), "weekend")
        self.assertEqual(gmt.market_state(et_moment(15, 10, 0)), "weekend")


class IntradayParsingTest(unittest.TestCase):
    def test_newest_usable_bar(self):
        t_open = int(et_moment(13, 9, 31).timestamp())
        t_late = int(et_moment(13, 15, 15).timestamp())
        ts, close = gmt.parse_intraday_bars(
            [t_open, t_late], [None, 757.12], "2026-11-13", "SPY"
        )
        self.assertEqual((ts, close), (t_late, 757.12))

    def test_stale_bars_are_not_todays_session(self):
        t_old = int(et_moment(12, 16, 0).timestamp())
        with self.assertRaises(RuntimeError):
            gmt.parse_intraday_bars([t_old], [757.12], "2026-11-13", "SPY")

    def test_no_usable_bars(self):
        t_now = int(et_moment(13, 10, 0).timestamp())
        with self.assertRaises(RuntimeError):
            gmt.parse_intraday_bars([t_now], [None], "2026-11-13", "SPY")


class NasdaqParsingTest(unittest.TestCase):
    def test_chart_payload(self):
        # Real shape observed 2026-11-12: dollar signs and commas.
        payload = {
            "data": {
                "lastSalePrice": "$25,366.09",
                "previousClose": "$25,466.19",
                "timeAsOf": "Nov 12, 2026",
            }
        }
        last, prev, market_date = gmt.parse_nasdaq_chart_payload(payload, "^IXIC")
        self.assertEqual((last, prev, market_date), (25366.09, 25466.19, "2026-11-12"))

    def test_empty_data_fails(self):
        with self.assertRaises(RuntimeError):
            gmt.parse_nasdaq_chart_payload(
                {"data": None, "status": {"rCode": 400}}, "DJI"
            )

    def test_missing_previous_close_fails(self):
        with self.assertRaises(RuntimeError):
            gmt.parse_nasdaq_chart_payload(
                {"data": {"lastSalePrice": "100", "timeAsOf": "Nov 12, 2026"}},
                "AAPL",
            )


class FredParsingTest(unittest.TestCase):
    def test_observations_skip_missing_marker(self):
        stdout = json.dumps(
            {
                "DGS10": [
                    {"date": "2026-11-09", "value": "4.88"},
                    {"date": "2026-11-10", "value": "."},
                    {"date": "2026-11-10", "value": "4.98"},
                ]
            }
        )
        self.assertEqual(
            gmt.parse_fred_observations(stdout, "DGS10"),
            [("2026-11-09", 4.88), ("2026-11-10", 4.98)],
        )

    def test_newest_first_helper_order_is_sorted_chronologically(self):
        # The real helper returns newest-first; the quote builder
        # takes [-2:] as (previous, latest), so order matters.
        stdout = json.dumps(
            {
                "DGS10": [
                    {"date": "2026-11-10", "value": "4.98"},
                    {"date": "2026-11-09", "value": "4.88"},
                ]
            }
        )
        self.assertEqual(
            gmt.parse_fred_observations(stdout, "DGS10"),
            [("2026-11-09", 4.88), ("2026-11-10", 4.98)],
        )

    def test_fewer_than_two_observations_fails(self):
        stdout = json.dumps({"DGS10": [{"date": "2026-11-10", "value": "4.98"}]})
        with self.assertRaises(RuntimeError):
            gmt.parse_fred_observations(stdout, "DGS10")

    def test_unparseable_output_fails(self):
        with self.assertRaises(RuntimeError):
            gmt.parse_fred_observations("not json", "DGS10")


class FredQuoteTest(unittest.TestCase):
    def test_missing_helper_degrades_to_error(self):
        with mock.patch.dict(os.environ, {"FRED_HELPER": "/nonexistent/fred.py"}):
            with self.assertRaises(RuntimeError):
                gmt.fred_quote("^TNX", "10-year Treasury yield", "rate")

    def test_helper_output_becomes_an_obs_date_quote(self):
        stdout = json.dumps(
            {
                "DGS10": [
                    {"date": "2026-11-09", "value": "4.88"},
                    {"date": "2026-11-10", "value": "4.98"},
                ]
            }
        )
        proc = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=stdout, stderr=""
        )
        with tempfile.NamedTemporaryFile() as helper:
            with (
                mock.patch.dict(os.environ, {"FRED_HELPER": helper.name}),
                mock.patch.object(gmt.subprocess, "run", return_value=proc),
            ):
                quote = gmt.fred_quote("^TNX", "10-year Treasury yield", "rate")
        self.assertEqual(quote["price"], 4.98)
        self.assertEqual(quote["previous_close"], 4.88)
        self.assertEqual(quote["market_date"], "2026-11-10")
        self.assertEqual(quote["session"], "close")
        self.assertEqual(quote["time_basis"], "obs-date")
        self.assertEqual(quote["source"], "FRED DGS10")
        # 16:00 EST on the observation date.
        self.assertEqual(quote["quote_time"], "2026-11-10T21:00:00Z")


class SessionProbeTest(unittest.TestCase):
    def test_bars_today_means_session(self):
        t_now = int(et_moment(13, 10, 0).timestamp())
        with mock.patch.object(
            gmt, "fetch_yahoo_chart", return_value=([t_now], [100.0], {})
        ):
            self.assertTrue(gmt.session_has_bars_today("2026-11-13"))

    def test_no_bars_today_means_no_session(self):
        t_old = int(et_moment(12, 16, 0).timestamp())
        with mock.patch.object(
            gmt, "fetch_yahoo_chart", return_value=([t_old], [100.0], {})
        ):
            self.assertFalse(gmt.session_has_bars_today("2026-11-13"))

    def test_failed_probe_proceeds(self):
        with mock.patch.object(
            gmt, "fetch_yahoo_chart", side_effect=RuntimeError("down")
        ):
            self.assertTrue(gmt.session_has_bars_today("2026-11-13"))


class FallbackChainTest(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 13, 15, 15, tzinfo=timezone.utc)

    def test_nasdaq_covers_equities_when_yahoo_fails(self):
        sentinel = canned_quote("AAPL", source="Nasdaq quote API")
        with (
            mock.patch.object(
                gmt, "yahoo_intraday_quote", side_effect=RuntimeError("yahoo down")
            ),
            mock.patch.object(gmt, "nasdaq_quote", return_value=sentinel) as nasdaq,
        ):
            out = gmt.build_quote_with_fallback(
                "AAPL", "Apple", "equity", "intraday", "2026-11-13", self.now
            )
        self.assertIs(out, sentinel)
        nasdaq.assert_called_once()

    def test_ixic_uses_comp_but_gspc_is_yahoo_only(self):
        sentinel = canned_quote("^IXIC", source="Nasdaq quote API")
        with (
            mock.patch.object(
                gmt, "yahoo_intraday_quote", side_effect=RuntimeError("yahoo down")
            ),
            mock.patch.object(gmt, "nasdaq_quote", return_value=sentinel) as nasdaq,
        ):
            gmt.build_quote_with_fallback(
                "^IXIC", "Nasdaq Composite index", "index",
                "intraday", "2026-11-13", self.now,
            )
        nasdaq.assert_called_once()
        with (
            mock.patch.object(
                gmt, "yahoo_intraday_quote", side_effect=RuntimeError("yahoo down")
            ),
            mock.patch.object(gmt, "nasdaq_quote") as nasdaq,
        ):
            with self.assertRaises(gmt.Quarantined) as caught:
                gmt.build_quote_with_fallback(
                    "^GSPC", "S&P 500 index", "index",
                    "intraday", "2026-11-13", self.now,
                )
        nasdaq.assert_not_called()
        self.assertIn("Yahoo", caught.exception.reason)
        self.assertNotIn("Nasdaq", caught.exception.reason)

    def test_yields_fall_back_to_fred(self):
        sentinel = canned_quote("^TNX", source="FRED DGS10")
        with (
            mock.patch.object(
                gmt, "yahoo_close_quote", side_effect=RuntimeError("yahoo down")
            ),
            mock.patch.object(gmt, "nasdaq_quote") as nasdaq,
            mock.patch.object(gmt, "fred_quote", return_value=sentinel) as fred,
        ):
            out = gmt.build_quote_with_fallback(
                "^TNX", "10-year Treasury yield", "rate",
                "close", "2026-11-13", self.now,
            )
        self.assertIs(out, sentinel)
        nasdaq.assert_not_called()
        fred.assert_called_once()

    def test_all_sources_failing_quarantines(self):
        with (
            mock.patch.object(
                gmt, "yahoo_close_quote", side_effect=RuntimeError("yahoo down")
            ),
            mock.patch.object(
                gmt, "nasdaq_quote", side_effect=RuntimeError("nasdaq down")
            ),
        ):
            with self.assertRaises(gmt.Quarantined) as caught:
                gmt.build_quote_with_fallback(
                    "AAPL", "Apple", "equity", "close", "2026-11-13", self.now
                )
        self.assertEqual(caught.exception.reason, "no quote from Yahoo, Nasdaq")


class SkipUnchangedTest(unittest.TestCase):
    def test_generated_at_and_market_state_do_not_force_a_rewrite(self):
        feed = {
            "schema_version": "market-ticker-1",
            "generated_at": "2026-11-13T15:15:00Z",
            "source": "Yahoo Finance v8 chart",
            "as_of": "2026-11-13",
            "mode": "intraday",
            "market_state": "session",
            "quotes": [canned_quote()],
            "order": ["SPY"],
            "unavailable": [],
            "unavailable_symbols": [],
        }
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "market-ticker.json"
            out.write_text(json.dumps(feed), encoding="utf-8")
            relabeled = dict(feed, generated_at="2026-11-13T15:45:00Z",
                             market_state="close-window")
            self.assertTrue(gmt.feed_unchanged(out, relabeled))
            changed = dict(feed, quotes=[canned_quote(price=758.0)])
            self.assertFalse(gmt.feed_unchanged(out, changed))

    def test_missing_or_corrupt_existing_feed_is_not_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "market-ticker.json"
            self.assertFalse(gmt.feed_unchanged(out, {"quotes": []}))
            out.write_text("not json", encoding="utf-8")
            self.assertFalse(gmt.feed_unchanged(out, {"quotes": []}))


class MainWiringTest(unittest.TestCase):
    def test_close_run_writes_then_skips_when_unchanged(self):
        def fake_build(symbol, label, kind, mode, today_et, now_utc):
            return canned_quote(symbol, label=label, kind=kind)

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "market-ticker.json"
            with mock.patch.object(gmt, "build_quote_with_fallback",
                                    side_effect=fake_build):
                self.assertEqual(gmt.main(["--mode", "close", "--out", str(out)]), 0)
                first = out.read_bytes()
                feed = json.loads(first)
                self.assertEqual(feed["mode"], "close")
                self.assertEqual(len(feed["quotes"]), len(gmt.DEFAULT_SYMBOLS))
                self.assertEqual(feed["order"][0], "SPY")
                self.assertIn("PLTR", feed["order"])
                self.assertEqual(feed["unavailable"], [])
                self.assertEqual(gmt.main(["--mode", "close", "--out", str(out)]), 0)
                self.assertEqual(out.read_bytes(), first)
                self.assertEqual(
                    gmt.main(["--mode", "close", "--force", "--out", str(out)]), 0
                )

    def test_all_quarantined_writes_nothing_and_exits_2(self):
        def always_quarantine(symbol, label, kind, mode, today_et, now_utc):
            raise gmt.Quarantined(symbol, "no quote from Yahoo")

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "market-ticker.json"
            with mock.patch.object(gmt, "build_quote_with_fallback",
                                    side_effect=always_quarantine):
                self.assertEqual(gmt.main(["--mode", "close", "--out", str(out)]), 2)
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
