import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"


class GrahamCandidateSurfaceTests(unittest.TestCase):
    def test_graham_module_is_loaded_through_app_and_packaged(self):
        index = (WEB / "index.html").read_text(encoding="utf-8")
        app = (WEB / "app.js").read_text(encoding="utf-8")
        build = (ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8")

        self.assertIn("./graham-filter.mjs", app)
        self.assertIn('"graham-filter.mjs"', build)
        self.assertNotIn("./scenario-lab.js", index)
        self.assertNotIn('"scenario-lab.js"', build)

    def test_surface_uses_real_nightly_inputs_and_stays_non_authoritative(self):
        app = (WEB / "app.js").read_text(encoding="utf-8")
        graham = (WEB / "graham-filter.mjs").read_text(encoding="utf-8")

        self.assertIn("fetch('./api/am-report',{cache:'no-store'})", app)
        self.assertIn("cash_secured_put_scan", app)
        self.assertIn("vix_regime", app)
        self.assertIn("does not authorize trades", app)
        self.assertIn("RoR and order flow are unchanged", app)
        self.assertNotIn("trade_authorized", graham)
        self.assertNotIn("risk_of_ruin", graham.lower())
        self.assertNotIn("/api/order", app)

    def test_surface_exposes_required_human_question_and_filter_behavior(self):
        app = (WEB / "app.js").read_text(encoding="utf-8")
        graham = (WEB / "graham-filter.mjs").read_text(encoding="utf-8")

        self.assertIn("Own if assigned?", app)
        self.assertIn("Hide Graham speculation", app)
        self.assertIn("NEEDS YOU remains visible", app)
        self.assertIn("DO_NOT_WANT_ASSIGNED_SHARES", graham)
        self.assertIn("NO_MARGIN_OF_SAFETY", graham)
        self.assertIn("RETURN_BELOW_HURDLE", graham)
        self.assertIn("OWNERSHIP_QUESTION_UNANSWERED", graham)


if __name__ == "__main__":
    unittest.main()
