import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IOS = ROOT / "ios" / "TradeDesk" / "TradeDesk"


class IOSProductSurfaceTests(unittest.TestCase):
    def test_ios_uses_current_emporion_product_contract(self):
        app = (IOS / "TradeDeskApp.swift").read_text(encoding="utf-8")
        store = (IOS / "ReportStore.swift").read_text(encoding="utf-8")

        self.assertIn('navigationTitle("Emporion")', app)
        self.assertIn('EMPORION · RESEARCH PLATFORM', app)
        self.assertIn('Markets · Intelligence · Discipline', app)
        self.assertIn('Seven research desks · Six evaluated workflows', app)
        self.assertIn('ARCHITECTURE ONLY', app)
        self.assertIn('envelope.registry', app)
        self.assertIn('https://hedge-desk.onrender.com', app)
        self.assertIn('https://hedge-desk.onrender.com/report.json', store)
        self.assertNotIn('chatgpt.site', app + store)

    def test_ios_keeps_six_evaluated_workflows_inside_seven_desk_architecture(self):
        store = (IOS / "ReportStore.swift").read_text(encoding="utf-8")

        self.assertIn('let registry: [RegistryDesk]', store)
        self.assertIn('expected.union(["bonds-rates-desk"])', store)
        self.assertIn('decoded.registry.count == architecture.count', store)
        self.assertIn('report.projects.count == expected.count', store)
        self.assertIn('decodeIfPresent([RegistryDesk].self', store)
        self.assertIn('RegistryDesk.defaultArchitecture', store)

    def test_ios_exposes_same_public_research_sources_as_web(self):
        app = (IOS / "TradeDeskApp.swift").read_text(encoding="utf-8")
        web_resources = (ROOT / "web" / "resources.js").read_text(encoding="utf-8")

        self.assertIn('ResourcesList().tabItem { Label("Resources", systemImage: "books.vertical") }', app)
        self.assertIn('navigationTitle("Research Resources")', app)
        self.assertIn('PRIMARY-SOURCE FIRST', app)
        self.assertIn('Inclusion does not imply affiliation, endorsement, sponsorship, investment advice, or trade authorization.', app)

        expected_sources = {
            "https://www.newyorkfed.org/markets/reference-rates",
            "https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics",
            "https://www.federalreserve.gov/monetarypolicy.htm",
            "https://fred.stlouisfed.org/",
            "https://www.finra.org/finra-data/fixed-income",
            "https://www.cmegroup.com/markets/interest-rates.html",
            "https://www.sec.gov/search-filings",
            "https://www.earningswhispers.com/",
            "https://finviz.com/",
            "https://www.bls.gov/",
            "https://www.bea.gov/",
            "https://www.cboe.com/",
        }
        for url in expected_sources:
            self.assertIn(url, app)
            self.assertIn(url, web_resources)

    def test_product_positioning_asset_captures_open_user_owned_model(self):
        positioning = (ROOT / "docs" / "PRODUCT_POSITIONING_AND_MEASUREMENT.md").read_text(encoding="utf-8")

        self.assertIn('developed iteratively since 1998', positioning)
        self.assertIn('Bring your watchlist. Research it your way.', positioning)
        self.assertIn('Your choice. Your data. Your money.', positioning)
        self.assertIn('Your money should work as hard for you as you do for it.', positioning)
        self.assertIn('Weekly Researched Watchlist Decisions', positioning)
        self.assertIn('User-implemented automation', positioning)
        self.assertIn('default product boundary remains paper/research oriented', positioning)


if __name__ == "__main__":
    unittest.main()
