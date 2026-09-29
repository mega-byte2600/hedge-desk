import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"


class MobileWebSurfaceTests(unittest.TestCase):
    def test_production_surface_loads_phone_only_hardening(self):
        index = (WEB / "index.html").read_text(encoding="utf-8")
        mobile = (WEB / "mobile.css").read_text(encoding="utf-8")

        self.assertIn('viewport-fit=cover', index)
        self.assertIn('<link rel="stylesheet" href="./mobile.css">', index)
        self.assertIn('@media (max-width: 600px)', mobile)
        self.assertIn('env(safe-area-inset-top)', mobile)
        self.assertIn('-webkit-overflow-scrolling: touch', mobile)
        self.assertIn('.table-scroll table', mobile)
        self.assertIn('min-width: 640px', mobile)
        self.assertIn('font-size: 16px', mobile)
        self.assertIn('min-height: 44px', mobile)
        self.assertIn('100dvh', mobile)

    def test_mobile_hardening_does_not_replace_desktop_stylesheet(self):
        index = (WEB / "index.html").read_text(encoding="utf-8")
        self.assertIn('<link rel="stylesheet" href="./styles.css">', index)
        self.assertLess(index.index('./styles.css'), index.index('./mobile.css'))


if __name__ == "__main__":
    unittest.main()
