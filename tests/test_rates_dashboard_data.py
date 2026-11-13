"""Tests for the Desk 7 rates-dashboard data generator and page contract.

Deterministic and fixture-based: no network, fixed clocks where time
matters. The generator module is loaded by path (ticker-test precedent).
"""

import ast
import importlib.util
import json
import re
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_rates_dashboard_data", ROOT / "scripts" / "build_rates_dashboard_data.py"
)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def _obs(*pairs):
    return [(d, float(v)) for d, v in pairs]


def _kalshi_market(event, suffix, close, price="0.5000", bid="0.4900",
                   ask="0.5100", prev="0.4800", vol="1000.00"):
    return {
        "ticker": f"{event}-{suffix}",
        "event_ticker": event,
        "close_time": close,
        "status": "active",
        "last_price_dollars": price,
        "yes_bid_dollars": bid,
        "yes_ask_dollars": ask,
        "previous_price_dollars": prev,
        "volume_24h_fp": vol,
        # Bare keys return null on the real API and must never be read.
        "last_price": None,
        "yes_bid": None,
    }


def _kalshi_group(event, close, prices=None):
    prices = prices or {}
    markets = []
    for suffix, _label in mod.KALSHI_OUTCOMES:
        markets.append(_kalshi_market(event, suffix, close, **prices.get(suffix, {})))
    return markets


def _calendar():
    return {
        "source": "federalreserve.gov (fixture)",
        "read_date": "2026-11-13",
        "meeting_label": "December 8–9 FOMC",
        "calendar": [["Next FOMC meeting", "Dec 8-9, 2026 (Tue-Wed)"]],
        "fedwatch_note": "Fixture FedWatch note.",
        "michigan": {
            "value": 4.3,
            "observation_date": "2026-11-01",
            "label": "Nov prelim",
            "source": "U-M Surveys of Consumers",
            "read_date": "2026-11-13",
        },
    }


def _full_series():
    """Minimal valid observations for every series in SERIES_LIMITS."""
    tenor = _obs(("2026-08-12", 4.0), ("2026-10-09", 4.5), ("2026-11-10", 4.98))
    monthly = _obs(("2026-08-01", 100.0), ("2026-09-01", 101.0), ("2026-10-01", 102.0))
    weekly = _obs(("2026-10-17", 200000), ("2026-10-24", 195000),
                  ("2026-10-31", 191000), ("2026-11-07", 200000))
    series = {}
    for sid in mod.SERIES_LIMITS:
        if sid in mod.TENOR_SERIES:
            series[sid] = tenor
        elif sid == "ICSA":
            series[sid] = weekly
        elif sid == "MICH":
            series[sid] = _obs(("2026-09-01", 4.6))
        else:
            series[sid] = monthly
    # DGS10 must end at the base value the payload asserts.
    series["DGS10"] = _obs(("2026-08-12", 4.68), ("2026-10-09", 5.24), ("2026-11-10", 4.98))
    return series


def _kalshi_front():
    return {
        "event_ticker": "KXFEDDECISION-26DEC",
        "meeting_label": "Dec-2026",
        "outcomes": [
            {"label": label, "price": 0.1, "bid": 0.09, "ask": 0.11,
             "prev": 0.1, "vol24h": 1000.0}
            for _suffix, label in mod.KALSHI_OUTCOMES
        ],
    }


class FredParsingTest(unittest.TestCase):
    def test_newest_first_sorted_and_missing_skipped(self):
        stdout = json.dumps({"DGS10": [
            {"date": "2026-11-10", "value": "4.98"},
            {"date": "2026-11-09", "value": "."},
            {"date": "2026-11-06", "value": "4.86"},
        ]})
        self.assertEqual(
            mod.parse_fred_observations(stdout, "DGS10"),
            [("2026-11-06", 4.86), ("2026-11-10", 4.98)],
        )

    def test_duplicate_date_last_non_missing_wins(self):
        stdout = json.dumps({"DGS10": [
            {"date": "2026-11-10", "value": "."},
            {"date": "2026-11-10", "value": "4.98"},
        ]})
        self.assertEqual(
            mod.parse_fred_observations(stdout, "DGS10"), [("2026-11-10", 4.98)]
        )

    def test_empty_observations_fail(self):
        with self.assertRaises(RuntimeError):
            mod.parse_fred_observations(json.dumps({"DGS10": []}), "DGS10")

    def test_missing_series_key_fails(self):
        with self.assertRaises(RuntimeError):
            mod.parse_fred_observations(json.dumps({"OTHER": []}), "DGS10")

    def test_helper_error_dict_fails(self):
        # The helper reports a per-series failure as {"error": ...}.
        stdout = json.dumps({"DGS10": {"error": "HTTPError: 500"}})
        with self.assertRaises(RuntimeError):
            mod.parse_fred_observations(stdout, "DGS10")

    def test_bad_json_fails(self):
        with self.assertRaises(RuntimeError):
            mod.parse_fred_observations("not json", "DGS10")

    def test_non_numeric_value_fails(self):
        stdout = json.dumps({"DGS10": [{"date": "2026-11-10", "value": "abc"}]})
        with self.assertRaises(RuntimeError):
            mod.parse_fred_observations(stdout, "DGS10")


class MonthlyChangeTest(unittest.TestCase):
    def test_oct_2025_gap_renders_as_gap(self):
        obs = _obs(("2025-09-01", 324.245), ("2025-11-01", 325.063),
                   ("2025-12-01", 326.031))
        changes = mod.monthly_pct_changes(obs)
        # No Nov-2025 point (Sep -> Nov is not consecutive); no interpolation.
        self.assertEqual(changes, [["2025-12-01", 0.298]])

    def test_arithmetic_matches_snapshot_values(self):
        self.assertEqual(
            mod.monthly_pct_changes(_obs(("2026-09-01", 336.298), ("2026-10-01", 337.476))),
            [["2026-10-01", 0.35]],
        )
        self.assertEqual(
            mod.monthly_pct_changes(_obs(("2026-09-01", 159.699), ("2026-10-01", 160.254))),
            [["2026-10-01", 0.348]],
        )

    def test_zero_previous_skipped(self):
        self.assertEqual(
            mod.monthly_pct_changes(_obs(("2026-09-01", 0.0), ("2026-10-01", 5.0))),
            [],
        )


class PayrollAndClaimsAverageTest(unittest.TestCase):
    def test_pay_avg3_arithmetic(self):
        changes = [["2025-10-01", -140.0], ["2025-11-01", 41.0],
                   ["2025-12-01", -17.0], ["2026-01-01", 160.0]]
        self.assertEqual(
            mod.trailing_avg_consecutive(changes, 3, 1),
            [["2025-12-01", -38.7], ["2026-01-01", 61.3]],
        )

    def test_pay_avg3_window_broken_by_gap(self):
        changes = [["2025-09-01", 10.0], ["2025-11-01", 20.0], ["2025-12-01", 30.0]]
        # Sep -> Nov is not consecutive, so no 3-window qualifies.
        self.assertEqual(mod.trailing_avg_consecutive(changes, 3, 1), [])

    def test_icsa_avg4_arithmetic(self):
        claims = [["2026-05-16", 210000.0], ["2026-05-23", 212000.0],
                  ["2026-05-30", 225000.0], ["2026-06-06", 230000.0]]
        self.assertEqual(mod.trailing_avg(claims, 4), [["2026-06-06", 219250]])


class SnapshotTest(unittest.TestCase):
    def _hist(self, dgs30_dates=None):
        dates = ["2026-08-05", "2026-08-12", "2026-09-11",
                 "2026-10-09", "2026-10-13", "2026-11-09", "2026-11-10"]
        hist = {}
        for i, sid in enumerate(mod.TENOR_SERIES):
            use = dates if sid != "DGS30" or dgs30_dates is None else dgs30_dates
            hist[sid] = [(d, float(i)) for d in use]
        return hist

    def test_date_proximity_selection(self):
        snaps = mod.curve_snapshots(self._hist())
        self.assertEqual(
            [s["label"] for s in snaps],
            ["Latest (2026-11-10)", "~30d ago (2026-10-09)",
             "~60d ago (2026-09-11)", "~90d ago (2026-08-12)"],
        )
        # ~30d target is 2026-10-11; 2026-10-13 is AFTER it and must not win.
        self.assertEqual(snaps[1]["date"], "2026-10-09")
        self.assertEqual(snaps[0]["y"], [0.0, 1.0, 2.0, 3.0, 4.0])

    def test_non_common_date_excluded(self):
        dates = ["2026-08-05", "2026-08-12", "2026-09-11",
                 "2026-10-13", "2026-11-09", "2026-11-10"]
        snaps = mod.curve_snapshots(self._hist(dgs30_dates=dates))
        # 2026-10-09 is missing from DGS30, so ~30d falls back to 2026-09-11.
        self.assertEqual(snaps[1]["date"], "2026-09-11")

    def test_missing_tenor_yields_no_snapshots(self):
        hist = self._hist()
        del hist["DGS30"]
        self.assertEqual(mod.curve_snapshots(hist), [])

    def test_no_common_dates_yields_no_snapshots(self):
        hist = {sid: [(f"2026-01-0{i}", 1.0)] for i, sid in enumerate(mod.TENOR_SERIES, 1)}
        self.assertEqual(mod.curve_snapshots(hist), [])


class KalshiSelectionTest(unittest.TestCase):
    def test_front_meeting_by_nearest_future_close(self):
        markets = (
            _kalshi_group("KXFEDDECISION-26OCT", "2026-10-28T18:59:00Z")
            + _kalshi_group("KXFEDDECISION-26DEC", "2026-12-09T18:59:00Z")
            + _kalshi_group("KXFEDDECISION-27JAN", "2027-01-27T18:59:00Z")
        )
        now = datetime(2026, 11, 13, tzinfo=timezone.utc)
        front = mod.select_front_meeting(markets, now)
        self.assertEqual(front["event_ticker"], "KXFEDDECISION-26DEC")
        self.assertEqual(front["meeting_label"], "Dec-2026")
        self.assertEqual(
            [o["label"] for o in front["outcomes"]],
            ["Hike >25bps", "Hike 25bps", "Hike 0bps", "Cut >25bps", "Cut 25bps"],
        )

    def test_no_hardcoded_ticker_after_front_meeting_passes(self):
        markets = (
            _kalshi_group("KXFEDDECISION-26DEC", "2026-12-09T18:59:00Z")
            + _kalshi_group("KXFEDDECISION-27JAN", "2027-01-27T18:59:00Z")
        )
        now = datetime(2026, 12, 10, tzinfo=timezone.utc)
        front = mod.select_front_meeting(markets, now)
        self.assertEqual(front["event_ticker"], "KXFEDDECISION-27JAN")
        self.assertEqual(front["meeting_label"], "Jan-2027")

    def test_no_future_meeting_is_core_failure(self):
        markets = _kalshi_group("KXFEDDECISION-26OCT", "2026-10-28T18:59:00Z")
        with self.assertRaises(mod.CoreDataError):
            mod.select_front_meeting(markets, datetime(2026, 11, 13, tzinfo=timezone.utc))

    def test_missing_outcome_is_core_failure(self):
        markets = _kalshi_group("KXFEDDECISION-26DEC", "2026-12-09T18:59:00Z")
        markets = [m for m in markets if not m["ticker"].endswith("-H25")]
        with self.assertRaises(mod.CoreDataError):
            mod.select_front_meeting(markets, datetime(2026, 11, 13, tzinfo=timezone.utc))

    def test_null_dollars_field_is_core_failure(self):
        markets = _kalshi_group("KXFEDDECISION-26DEC", "2026-12-09T18:59:00Z")
        markets[1]["last_price_dollars"] = None  # H25 last is null
        with self.assertRaises(mod.CoreDataError):
            mod.select_front_meeting(markets, datetime(2026, 11, 13, tzinfo=timezone.utc))

    def test_bare_price_keys_are_never_read(self):
        # A market carrying ONLY bare last_price/yes_bid (dollars keys
        # absent) must fail: bare keys returning null is not "no market",
        # and their presence must not satisfy the price requirement.
        markets = _kalshi_group("KXFEDDECISION-26DEC", "2026-12-09T18:59:00Z")
        for m in markets:
            del m["last_price_dollars"]
            m["last_price"] = "0.5000"
        with self.assertRaises(mod.CoreDataError):
            mod.select_front_meeting(markets, datetime(2026, 11, 13, tzinfo=timezone.utc))

    def test_zero_bid_is_legitimate(self):
        markets = _kalshi_group(
            "KXFEDDECISION-26DEC", "2026-12-09T18:59:00Z",
            prices={"C25": {"bid": "0.0000", "price": "0.0100"}},
        )
        front = mod.select_front_meeting(markets, datetime(2026, 11, 13, tzinfo=timezone.utc))
        c25 = [o for o in front["outcomes"] if o["label"] == "Cut 25bps"][0]
        self.assertEqual(c25["bid"], 0.0)
        self.assertEqual(c25["price"], 0.01)

    def test_meeting_label_parse_and_fallback(self):
        self.assertEqual(
            mod.meeting_label_from_event_ticker("KXFEDDECISION-26DEC"), "Dec-2026"
        )
        self.assertEqual(
            mod.meeting_label_from_event_ticker("KXFEDDECISION-27JAN"), "Jan-2027"
        )
        self.assertEqual(
            mod.meeting_label_from_event_ticker("KXFEDDECISION-ODD"),
            "KXFEDDECISION-ODD",
        )


class BuildPayloadTest(unittest.TestCase):
    def test_schema_complete(self):
        payload = mod.build_payload(
            _full_series(), _kalshi_front(), _calendar(),
            "2026-11-13T17:22:22Z", [],
        )
        self.assertEqual(payload["schema_version"], "rates-dashboard-1")
        self.assertEqual(payload["generated_at"], "2026-11-13T17:22:22Z")
        self.assertEqual(payload["as_of"], "2026-11-10")
        self.assertEqual(payload["base_10y"], 4.98)
        self.assertEqual(payload["base_10y_date"], "2026-11-10")
        self.assertEqual(payload["tenor_labels"], ["3M", "2Y", "5Y", "10Y", "30Y"])
        self.assertEqual(len(payload["snapshots"]), 4)
        self.assertEqual(len(payload["kalshi"]), 5)
        self.assertEqual(payload["kalshi_meeting_label"], "Dec-2026")
        self.assertEqual(payload["michigan"]["value"], 4.3)
        self.assertEqual(payload["michigan_fred"], {"value": 4.6, "date": "2026-09-01"})
        self.assertEqual(payload["manual"]["meeting_label"], "December 8–9 FOMC")
        self.assertEqual(payload["unavailable"], [])
        for key in ("curve_hist", "infl", "be", "pay_chg", "pay_avg3",
                    "unrate", "icsa", "icsa_avg4", "jolts", "slopes", "spreads"):
            self.assertIn(key, payload)

    def test_missing_dgs10_is_core_failure(self):
        series = _full_series()
        series["DGS10"] = None
        with self.assertRaises(mod.CoreDataError):
            mod.build_payload(series, _kalshi_front(), _calendar(), "2026-11-13T00:00:00Z", [])

    def test_missing_kalshi_is_core_failure(self):
        with self.assertRaises(mod.CoreDataError):
            mod.build_payload(_full_series(), {}, _calendar(), "2026-11-13T00:00:00Z", [])

    def test_non_core_quarantine_keeps_payload_schema_complete(self):
        series = _full_series()
        series["T10YIE"] = None
        unavailable = [{"series": "T10YIE", "reason": "helper boom"}]
        payload = mod.build_payload(
            series, _kalshi_front(), _calendar(), "2026-11-13T00:00:00Z", unavailable
        )
        self.assertNotIn("T10YIE", payload["be"])
        self.assertIn("T5YIE", payload["be"])
        self.assertEqual(payload["unavailable"][0]["series"], "T10YIE")
        self.assertEqual(payload["unavailable"][0]["reason"], "helper boom")

    def test_unavailable_entries_carry_series_and_reason(self):
        payload = mod.build_payload(
            _full_series(), _kalshi_front(), _calendar(), "2026-11-13T00:00:00Z",
            [{"series": "X", "reason": "y"}],
        )
        for entry in payload["unavailable"]:
            self.assertIn("series", entry)
            self.assertIn("reason", entry)


class SkipUnchangedTest(unittest.TestCase):
    def test_generated_at_excluded(self):
        payload = {"schema_version": "rates-dashboard-1", "base_10y": 4.98,
                   "generated_at": "2026-11-13T00:00:00Z"}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.json"
            path.write_text(json.dumps({**payload, "generated_at": "2026-11-12T00:00:00Z"}))
            self.assertTrue(mod.payload_unchanged(path, payload))

    def test_value_change_is_not_unchanged(self):
        payload = {"schema_version": "rates-dashboard-1", "base_10y": 4.98,
                   "generated_at": "2026-11-13T00:00:00Z"}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.json"
            path.write_text(json.dumps({**payload, "base_10y": 4.99}))
            self.assertFalse(mod.payload_unchanged(path, payload))

    def test_missing_or_corrupt_file_is_not_unchanged(self):
        payload = {"schema_version": "rates-dashboard-1", "generated_at": "x"}
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(mod.payload_unchanged(Path(tmp) / "nope.json", payload))
            bad = Path(tmp) / "bad.json"
            bad.write_text("{not json")
            self.assertFalse(mod.payload_unchanged(bad, payload))


class MainWiringTest(unittest.TestCase):
    def _run_main(self, tmp, fred_side_effect=None, kalshi_side_effect=None, extra=None):
        cal = Path(tmp) / "calendar.json"
        cal.write_text(json.dumps(_calendar()))
        out = Path(tmp) / "data.json"
        series = _full_series()
        markets = (
            _kalshi_group("KXFEDDECISION-26DEC", "2099-12-09T18:59:00Z")
            + _kalshi_group("KXFEDDECISION-27JAN", "2100-01-27T18:59:00Z")
        )

        def fake_fred(sid, limit):
            if fred_side_effect:
                fred_side_effect(sid)
            return series[sid]

        def fake_kalshi():
            if kalshi_side_effect:
                kalshi_side_effect()
            return markets

        with mock.patch.object(mod, "fetch_fred_series", side_effect=fake_fred), \
             mock.patch.object(mod, "fetch_kalshi_markets", side_effect=fake_kalshi):
            code = mod.main(["--out", str(out), "--calendar", str(cal)] + (extra or []))
        return code, out

    def test_main_writes_schema_valid_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = self._run_main(tmp)
            self.assertEqual(code, 0)
            payload = json.loads(out.read_text())
            self.assertEqual(payload["schema_version"], "rates-dashboard-1")
            self.assertEqual(payload["kalshi_event_ticker"], "KXFEDDECISION-26DEC")
            self.assertEqual(payload["unavailable"], [])

    def test_main_skips_unchanged_and_force_rewrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = self._run_main(tmp)
            self.assertEqual(code, 0)
            first = out.read_bytes()
            code, _ = self._run_main(tmp)
            self.assertEqual(code, 0)
            # Second run rewrites the same path only when forced; the file
            # must be byte-identical because the payload is unchanged.
            # (The second _run_main call writes to the same temp dir path.)
            self.assertEqual(out.read_bytes(), first)
            code, _ = self._run_main(tmp, extra=["--force"])
            self.assertEqual(code, 0)

    def test_main_quarantines_one_series(self):
        def boom(sid):
            if sid == "JTSJOL":
                raise RuntimeError("helper boom")
        with tempfile.TemporaryDirectory() as tmp:
            code, out = self._run_main(tmp, fred_side_effect=boom)
            self.assertEqual(code, 0)
            payload = json.loads(out.read_text())
            self.assertEqual(payload["jolts"], [])
            self.assertEqual(payload["unavailable"][0]["series"], "JTSJOL")

    def test_main_core_failure_writes_nothing(self):
        def boom(sid):
            if sid == "DGS10":
                raise RuntimeError("helper boom")
        with tempfile.TemporaryDirectory() as tmp:
            code, out = self._run_main(tmp, fred_side_effect=boom)
            self.assertEqual(code, 2)
            self.assertFalse(out.exists())

    def test_main_kalshi_failure_writes_nothing(self):
        def boom():
            raise RuntimeError("Kalshi down")
        with tempfile.TemporaryDirectory() as tmp:
            code, out = self._run_main(tmp, kalshi_side_effect=boom)
            self.assertEqual(code, 2)
            self.assertFalse(out.exists())


class DashboardHtmlTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "web" / "rates-dashboard.html").read_text(encoding="utf-8")

    def test_fetches_json_with_no_cache(self):
        self.assertIn(
            "fetch('./rates-dashboard-data.json', {cache: 'no-cache'})", self.html
        )

    def test_no_baked_payload(self):
        self.assertNotIn("const D = {", self.html)

    def test_fail_closed_markers(self):
        self.assertIn("Data unavailable.", self.html)
        self.assertIn("unavail", self.html)
        self.assertIn("rates-dashboard-1", self.html)
        self.assertIn("schema_version", self.html)
        self.assertIn("failAll", self.html)

    def test_heading_sequence_intact(self):
        headings = re.findall(r"<h2[^>]*>(.*?)</h2>", self.html)
        self.assertEqual(headings, [
            "1. Yield curve — now vs then",
            "2. Fed decision pricing — December 8–9 FOMC",
            "3. Inflation vs the 2% target",
            "4. Labor — demand, slack, and the fast signal",
            "5. Curve slope + credit spreads",
            "6. Graham lens — intrinsic value &amp; margin of safety",
        ])

    def test_preserved_surface(self):
        for marker in (
            'id="market-ticker"',
            '<script type="module" src="./market-ticker.mjs"></script>',
            'href="./index.html#desks"',
            "HYPOTHETICAL projection from real base data.",
            'id="rSlider"',
            'id="gSlider"',
            'id="bondSide"',
            '<script src="./vendor/plotly-2.35.2.min.js"></script>',
            "--noir-bg:#0a0a0c",
            "Decision question:",
        ):
            self.assertIn(marker, self.html)

    def test_dynamic_text_hooks_present(self):
        for marker in ('id="asOfLine"', 'id="panel2Heading"', 'id="curveSrc"',
                       'id="kalshiSrc"', 'id="inflSrc"'):
            self.assertIn(marker, self.html)


class ConsoleAssetsTest(unittest.TestCase):
    def test_json_ships_with_page(self):
        tree = ast.parse((ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8"))
        assets = None
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "CONSOLE_ASSETS" for t in node.targets
            ):
                assets = ast.literal_eval(node.value)
        self.assertIsNotNone(assets)
        self.assertIn("rates-dashboard.html", assets)
        self.assertIn("rates-dashboard-data.json", assets)


class SeedJsonTest(unittest.TestCase):
    def test_committed_seed_parses_with_schema(self):
        payload = json.loads((ROOT / "web" / "rates-dashboard-data.json").read_text())
        self.assertEqual(payload["schema_version"], "rates-dashboard-1")
        self.assertIn("generated_at", payload)
        self.assertIn("as_of", payload)
        for key in ("tenor_labels", "snapshots", "curve_hist", "base_10y",
                    "base_10y_date", "kalshi", "kalshi_meeting_label", "infl",
                    "be", "pay_chg", "pay_avg3", "unrate", "icsa", "icsa_avg4",
                    "jolts", "slopes", "spreads", "michigan", "manual",
                    "unavailable"):
            self.assertIn(key, payload)
        self.assertIsInstance(payload["base_10y"], (int, float))
        # Lower bounds pin a HEALTHY pull: a regeneration that silently
        # returned 1 observation per series (the --limit=N failure class)
        # must fail this test, not ship.
        self.assertGreaterEqual(len(payload["curve_hist"]["10Y"]), 60)
        self.assertGreaterEqual(len(payload["infl"]["CPIAUCSL"]), 10)
        self.assertGreaterEqual(len(payload["snapshots"]), 3)
        self.assertGreaterEqual(len(payload["icsa"]), 20)
        self.assertEqual(len(payload["kalshi"]), 5)
        self.assertEqual(
            [o["label"] for o in payload["kalshi"]],
            ["Hike >25bps", "Hike 25bps", "Hike 0bps", "Cut >25bps", "Cut 25bps"],
        )
        for entry in payload["unavailable"]:
            self.assertIn("series", entry)
            self.assertIn("reason", entry)


if __name__ == "__main__":
    unittest.main()
