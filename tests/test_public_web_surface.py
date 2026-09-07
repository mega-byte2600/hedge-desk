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

    def test_public_brand_and_copy_stay_launch_safe(self):
        index = (WEB / "index.html").read_text(encoding="utf-8")
        professional = (WEB / "professional.js").read_text(encoding="utf-8")
        combined = index + professional

        self.assertIn('emporion-institutional-seal.svg', combined)
        self.assertIn('Independent research platform', combined)
        self.assertNotIn('AI-native', combined)
        self.assertNotIn('brandmark', combined)
        self.assertNotIn('Controls & evidence', combined)
        self.assertNotIn('function controlsBlock()', professional)

    def test_research_resources_page_is_public_and_packaged(self):
        index = (WEB / "index.html").read_text(encoding="utf-8")
        resources = (WEB / "resources.js").read_text(encoding="utf-8")
        build = (ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8")

        self.assertIn('href="#resources"', index)
        self.assertIn('data-nav="resources"', index)
        self.assertIn('./resources.js', index)
        self.assertIn('"resources.js"', build)
        self.assertIn('https://www.newyorkfed.org/markets/reference-rates', resources)
        self.assertIn('https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics', resources)
        self.assertIn('https://www.sec.gov/search-filings', resources)
        self.assertIn('https://www.earningswhispers.com/', resources)
        self.assertIn('https://finviz.com/', resources)
        self.assertIn('PRIMARY-SOURCE FIRST', resources)

    def test_seven_desk_architecture_is_public_and_packaged(self):
        index = (WEB / "index.html").read_text(encoding="utf-8")
        architecture = (WEB / "desk-architecture.js").read_text(encoding="utf-8")
        build = (ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8")

        self.assertIn('Research desks <b>7</b>', index)
        self.assertIn('./desk-architecture.js', index)
        self.assertIn('"desk-architecture.js"', build)
        self.assertIn('Bonds &amp; Rates', architecture)
        self.assertIn('DESK 07 · MACRO ANCHOR', architecture)
        self.assertIn('Architecture only', architecture)
        self.assertIn('No evaluated signal is published for this desk yet.', architecture)


if __name__ == "__main__":
    unittest.main()
