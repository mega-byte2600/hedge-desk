import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DeskCoverageCopyTests(unittest.TestCase):
    def test_mobile_research_desk_cards_show_actual_short_and_event_mandates(self):
        source = (ROOT / "web" / "professional.js").read_text(encoding="utf-8")
        self.assertIn("Desk 5 · Short Sale Research", source)
        self.assertIn("Desk 6 · Weather / War / Futures", source)
        self.assertIn("data-desk-route=\"${route}\"", source)
        self.assertNotIn("Global Quant & AI Research Lab", source)
        self.assertNotIn("['Futures Event'", source)

    def test_desk5_and_desk6_routes_render_evidence_and_feed_gates(self):
        app = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        self.assertIn("function desk5()", app)
        self.assertIn("function desk6()", app)
        self.assertIn("hydrateDesk5()", app)
        self.assertIn("hydrateDesk6()", app)
        self.assertIn("SEC EDGAR", app)
        self.assertIn("FINRA short interest", app)
        self.assertIn("8-K item lead", app)
        self.assertIn("CME Market Data APIs", app)
        self.assertIn("NOT INGESTED · no contract-month curve", app)
        build = (ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8")
        self.assertIn('"desk-research.css"', build)

    def test_desk7_snapshot_age_is_visible(self):
        app = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        self.assertIn("Snapshot is ${ageDays} days old", app)
        self.assertIn("dashboard does not.", app)

    def test_research_desks_keep_one_sidebar_entry_and_open_from_the_desk_page(self):
        index = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        app = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        self.assertEqual(index.count('data-nav="desks"'), 1)
        for route in ("desk5", "desk6", "desk7"):
            self.assertNotIn(f'data-nav="{route}"', index)
            self.assertIn(f"'{route}'", app)
        self.assertIn("includes(route)?'desks':route", app)


if __name__ == "__main__":
    unittest.main()
