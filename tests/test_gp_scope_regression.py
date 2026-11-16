import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"


class GpScopeRegressionTests(unittest.TestCase):
    def test_research_desks_stay_in_the_existing_single_sidebar_entry(self):
        index = (WEB / "index.html").read_text(encoding="utf-8")
        nav = index.split('<nav aria-label="Workspace">', 1)[1].split("</nav>", 1)[0]

        self.assertEqual(nav.count('data-nav="desks"'), 1)
        self.assertIn('href="#desks" data-nav="desks"', nav)
        for route in ("desk5", "desk6", "desk7"):
            self.assertNotIn(f'data-nav="{route}"', nav)
            self.assertNotIn(f'href="#{route}"', nav)

    def test_each_specialist_desk_remains_reachable_inside_research_desks(self):
        app = (WEB / "app.js").read_text(encoding="utf-8")
        architecture = (WEB / "desk-architecture.js").read_text(encoding="utf-8")

        for route in ("desk5", "desk6", "desk7"):
            self.assertIn(f"{route}:", app)
        for project_id in (
            "open-quant-ai-model-lab",
            "event-futures-desk",
            "bonds-rates-desk",
        ):
            self.assertIn(project_id, app)
        self.assertIn("const routeFor=", app)
        self.assertIn('href="#${routeFor}"', app)
        self.assertIn("Seven research desks", architecture)


if __name__ == "__main__":
    unittest.main()
