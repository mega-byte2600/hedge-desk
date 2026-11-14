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
        self.assertEqual(data["schema_version"], "desk7-indicators-1")
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
        self.assertIn("p.project_id==='bonds-rates-desk'", app)
        self.assertIn('href="#desk7"', app)
        self.assertIn("Indicator dashboard", app)
        # No second Desk 07 card: the live report already carries bonds-rates-desk
        # as a project, so the dashboard link rides on the existing card.
        self.assertNotIn("desk7Card", app)

    def test_visible_desk7_card_opens_indicator_dashboard(self):
        # professional.js hides app.js's cards and substitutes its own markup;
        # the visible Bonds & Rates card must land on #desk7, not #resources.
        prof = (WEB / "professional.js").read_text(encoding="utf-8")
        self.assertIn("location.hash = '#desk7'", prof)
        self.assertIn("indicator dashboard", prof)

    def test_desks_view_tolerates_missing_layers_and_disposition(self):
        # The live /api/report payload omits layers/disposition for every
        # project; gates() threw and the whole Desks view never rendered.
        # The dashboard link rides the Desks view, so the guards ship here.
        app = (WEB / "app.js").read_text(encoding="utf-8")
        self.assertIn("p.layers||[]", app)
        self.assertIn("p.disposition?tag(p.disposition)", app)

    def test_fail_closed_copy_and_no_execution_boundaries(self):
        app = (WEB / "app.js").read_text(encoding="utf-8")
        payload = (WEB / "desk7-indicators.json").read_text(encoding="utf-8")
        self.assertIn("<h2>Desk 7 indicators unavailable</h2><p>data unavailable</p>", app)
        self.assertIn("The rest of Emporion remains available.", app)
        self.assertNotIn("trade_authorized", payload)
        self.assertNotIn("/api/order", payload)
        self.assertIn("live_orders_enabled!==false", app)


if __name__ == "__main__":
    unittest.main()
