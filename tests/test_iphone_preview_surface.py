import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"


class IPhonePreviewSurfaceTests(unittest.TestCase):
    def test_standalone_preview_is_packaged_and_product_aligned(self):
        preview = (WEB / "iphone-preview.html").read_text(encoding="utf-8")
        build = (ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8")

        self.assertIn('Emporion iPhone Preview', preview)
        self.assertIn('Seven research desks · Six evaluated workflows', preview)
        self.assertIn('Bonds & Rates', preview)
        self.assertIn('Yellow Sheets', preview)
        self.assertIn('data-tab="resources"', preview)
        self.assertIn('PRIMARY-SOURCE FIRST', preview)
        self.assertIn('New York Fed · Reference Rates', preview)
        self.assertIn('SEC · EDGAR', preview)
        self.assertIn('BLS · U.S. Bureau of Labor Statistics', preview)
        self.assertIn('Your choice. Your data. Your money.', preview)
        self.assertIn('"iphone-preview.html"', build)


if __name__ == "__main__":
    unittest.main()
