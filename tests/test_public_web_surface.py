import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"


class PublicWebSurfaceTests(unittest.TestCase):
    def test_internal_controls_page_is_not_publicly_navigable(self):
        index = (WEB / "index.html").read_text(encoding="utf-8")
        guard = (WEB / "public-surface.js").read_text(encoding="utf-8")

        self.assertNotIn('href="#controls"', index)
        self.assertNotIn('data-nav="controls"', index)
        self.assertNotIn('Controls & evidence', index)
        self.assertIn("new Set(['controls'])", guard)
        self.assertIn("history.replaceState(null, '', '#overview')", guard)
        self.assertLess(index.index('./public-surface.js'), index.index('./app.js'))

    def test_public_route_guard_is_packaged_for_deployment(self):
        build = (ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8")
        self.assertIn('"public-surface.js"', build)

    def test_about_page_includes_public_contributor_contact(self):
        acknowledgements = (WEB / "acknowledgements.js").read_text(encoding="utf-8")
        self.assertIn('CONTRIBUTE / CONTACT', acknowledgements)
        self.assertIn('mailto:michael.bolton.ph@dartmouth.edu', acknowledgements)
        self.assertIn('https://github.com/mega-byte2600/hedge-desk', acknowledgements)


if __name__ == "__main__":
    unittest.main()
