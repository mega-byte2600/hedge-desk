import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"

REQUIRED_INDICATOR_FIELDS = ("name", "series", "source", "why", "trigger", "read", "vote", "broker")


class Desk7IndicatorsTests(unittest.TestCase):
    def test_json_schema_tally_and_call(self):
        data = json.loads((WEB / "desk7-indicators.json").read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], "desk7-indicators-2")
        self.assertEqual(data["as_of"], "2026-11-13")
        indicators = data["indicators"]
        self.assertEqual(len(indicators), 10)
        for item in indicators:
            for field in REQUIRED_INDICATOR_FIELDS:
                self.assertIsInstance(item[field], str, field)
                self.assertTrue(item[field].strip(), field)
            self.assertIn(item["vote"], ("HIKE", "CUT", "NEUTRAL"))
        counts = Counter(item["vote"] for item in indicators)
        self.assertEqual(dict(counts), {"HIKE": 5, "CUT": 1, "NEUTRAL": 4})
        self.assertEqual(
            data["decision"]["tally"],
            {"hike": counts["HIKE"], "cut": counts["CUT"], "neutral": counts["NEUTRAL"]},
        )
        self.assertEqual(data["decision"]["call"], "25bp hike on Dec 9")
        self.assertEqual(data["decision"]["meeting"], "Dec 8-9")
        self.assertEqual(data["market_pricing"]["total_hike"], "$1.00")
        self.assertEqual(len(data["what_would_change"]), 3)
        self.assertTrue(data["graham"]["lines"])
        self.assertIn("UNVERIFIED", data["graham"]["spread"])

    def test_route_wired_and_asset_packaged(self):
        app = (WEB / "app.js").read_text(encoding="utf-8")
        index = (WEB / "index.html").read_text(encoding="utf-8")
        build = (ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8")
        self.assertIn("desk7:'Desk 7", app)
        self.assertIn("function desk7()", app)
        self.assertIn("hydrateDesk7", app)
        self.assertIn("desk7-indicators.json", app)
        self.assertIn("route==='desk7'", app)
        self.assertIn('data-nav="desk7"', index)
        self.assertIn('"desk7-indicators.json"', build)

    def test_desk7_card_links_to_indicator_dashboard(self):
        app = (WEB / "app.js").read_text(encoding="utf-8")
        self.assertIn("'bonds-rates-desk':'desk7'", app)
        self.assertIn('href="#${routeFor}"', app)
        self.assertIn("function desk7()", app)

    def test_visible_desk7_card_opens_indicator_dashboard(self):
        # professional.js hides app.js's cards and substitutes its own markup;
        # the visible Bonds & Rates card must land on #desk7, not #resources.
        prof = (WEB / "professional.js").read_text(encoding="utf-8")
        self.assertIn("['Desk 7 · Bonds & Rates'", prof)
        self.assertIn('data-desk-route="${route}"', prof)
        self.assertIn("location.hash = `#${route}`", prof)

    def test_desks_view_tolerates_missing_layers_and_disposition(self):
        # The live /api/report payload omits layers/disposition for every
        # project; gates() threw and the whole Desks view never rendered.
        # The dashboard link rides the Desks view, so the guards ship here.
        app = (WEB / "app.js").read_text(encoding="utf-8")
        self.assertIn("const ls=p.layers||[]", app)
        self.assertIn("p?.disposition", app)

    def test_fail_closed_copy_and_no_execution_boundaries(self):
        app = (WEB / "app.js").read_text(encoding="utf-8")
        payload = (WEB / "desk7-indicators.json").read_text(encoding="utf-8")
        self.assertIn("<h2>Desk 7 indicators unavailable</h2><p>data unavailable</p>", app)
        self.assertIn("The rest of Emporion remains available.", app)
        self.assertNotIn("trade_authorized", payload)
        self.assertNotIn("/api/order", payload)
        self.assertIn("live_orders_enabled!==false", app)


    def test_gauge_encoding_recomputes_every_vote(self):
        # Each gauge carries the trigger rule as numbers. Recomputing the
        # vote from value + tripwires must reproduce the stated vote, so a
        # chart can never show a marker on the wrong side of its tripwire.
        data = json.loads((WEB / "desk7-indicators.json").read_text(encoding="utf-8"))
        gauged = [item for item in data["indicators"] if item["gauge"] is not None]
        self.assertEqual(len(gauged), 9)
        fomc = [item for item in data["indicators"] if item["name"] == "FOMC vote and guidance"]
        self.assertEqual(len(fomc), 1)
        self.assertIsNone(fomc[0]["gauge"])
        for item in gauged:
            g = item["gauge"]
            self.assertEqual(len(g["values"]), len(g["labels"]), item["name"])
            self.assertEqual(len(g["values"]), len(g["display"]), item["name"])
            lo, hi = g["window"]
            for value in g["values"]:
                self.assertGreaterEqual(value, lo, item["name"])
                self.assertLessEqual(value, hi, item["name"])
            if g["hike_at"] is not None:
                self.assertGreaterEqual(g["hike_at"], lo, item["name"])
                self.assertLessEqual(g["hike_at"], hi, item["name"])
            if g["cut_at"] is not None:
                self.assertGreaterEqual(g["cut_at"], lo, item["name"])
                self.assertLessEqual(g["cut_at"], hi, item["name"])
            implied = "NEUTRAL"
            for value in g["values"]:
                if g["hike_at"] is not None and (
                    (g["hike_when"] == "above" and value > g["hike_at"])
                    or (g["hike_when"] == "below" and value < g["hike_at"])
                ):
                    implied = "HIKE"
                if g["cut_at"] is not None and (
                    (g["cut_when"] == "above" and value > g["cut_at"])
                    or (g["cut_when"] == "below" and value < g["cut_at"])
                ):
                    implied = "CUT"
            self.assertEqual(implied, item["vote"], item["name"])

    def test_kalshi_markets_sum_to_over_round_and_total_hike(self):
        data = json.loads((WEB / "desk7-indicators.json").read_text(encoding="utf-8"))
        markets = data["market_pricing"]["kalshi_markets"]
        self.assertEqual(len(markets), 4)
        self.assertAlmostEqual(sum(m["last"] for m in markets), 1.05)
        hike = sum(m["last"] for m in markets if m["family"] == "hike")
        self.assertAlmostEqual(hike, 1.00)
        self.assertEqual(data["market_pricing"]["total_hike"], "$1.00")
        for market in markets:
            self.assertIn(market["family"], ("hike", "hold", "cut"))
            self.assertGreater(market["last"], 0)

    def test_plotly_charts_wired_and_theme_safe(self):
        app = (WEB / "app.js").read_text(encoding="utf-8")
        self.assertIn("desk7-indicators-2", app)
        self.assertIn('id="desk7-vote-chart"', app)
        self.assertIn('id="desk7-gauge-chart"', app)
        self.assertIn('id="desk7-kalshi-chart"', app)
        self.assertIn("renderDesk7Charts", app)
        self.assertIn("vendor/plotly-2.35.2.min.js", app)
        self.assertIn("plotly_click", app)
        self.assertIn("desk7-row-", app)
        self.assertIn("Chart unavailable. The table below carries the same data.", app)
        # Vote colors: brass for HIKE, muted for NEUTRAL, workbench blue for
        # CUT. Live green (#35c26e) is reserved for live-data semantics and
        # must not appear in the Desk 7 chart block.
        block = app[app.index("const DESK7_VOTE_COLOR") : app.index("function fitFrame")]
        self.assertIn("'#dcb96f'", block)
        self.assertIn("'#a39e93'", block)
        self.assertIn("'#4a90d9'", block)
        self.assertNotIn("#35c26e", block)


if __name__ == "__main__":
    unittest.main()
