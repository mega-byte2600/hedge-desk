import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"

class RealEstateLazyRouteTests(unittest.TestCase):
    def test_real_estate_is_lazy_and_cannot_block_spa_boot(self):
        app = (WEB / "app.js").read_text(encoding="utf-8")
        self.assertNotIn("import { realEstatePage", app)
        self.assertNotIn("from './real-estate-ui.js'", app.splitlines()[0:5])
        self.assertIn("await import('./real-estate-ui.js')", app)
        self.assertIn("The rest of Emporion remains available.", app)

    def test_real_estate_assets_are_packaged_but_not_globally_loaded(self):
        index = (WEB / "index.html").read_text(encoding="utf-8")
        build = (ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8")
        self.assertIn('data-nav="real-estate"', index)
        self.assertNotIn('src="./real-estate-ui.js"', index)
        self.assertNotIn('href="./real-estate.css"', index)
        for asset in ("real-estate-ui.js","real-estate-model.mjs","real-estate.css"):
            self.assertIn(f'"{asset}"', build)

    def test_real_estate_route_does_not_touch_execution_boundaries(self):
        ui = (WEB / "real-estate-ui.js").read_text(encoding="utf-8")
        app = (WEB / "app.js").read_text(encoding="utf-8")
        self.assertNotIn("trade_authorized", ui)
        self.assertNotIn("/api/order", ui)
        self.assertIn("live_orders_enabled!==false", app)

if __name__ == "__main__":
    unittest.main()
