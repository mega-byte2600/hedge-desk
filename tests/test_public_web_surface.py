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

        self.assertIn("Emporion", combined)
        self.assertIn("Markets · Intelligence · Discipline", combined)
        self.assertIn("A Bolton Investment Group (BIG) Project", combined)
        self.assertIn('emporion-institutional-seal.svg', combined)
        self.assertIn('Independent research platform', combined)
        self.assertIn('RESEARCH PLATFORM', combined)
        self.assertIn('Seven research desks.<br>Six evaluated workflows.', combined)
        self.assertIn('<b>DESKS</b> SEVEN', combined)
        self.assertIn('<b>EVALUATED</b> SIX', combined)
        self.assertNotIn('AI-native', combined)
        self.assertNotIn('brandmark', combined)
        self.assertNotIn('Controls & evidence', combined)
        self.assertNotIn('function controlsBlock()', professional)

    def test_public_copy_does_not_claim_advice_management_or_live_orders(self):
        public_assets = [
            WEB / "index.html",
            WEB / "professional.js",
            WEB / "resources.js",
            WEB / "iphone-preview.html",
        ]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in public_assets).lower()

        forbidden_claims = [
            "licensed advisor",
            "investment adviser",
            "advisory services",
            "investment management services",
            "accept capital",
            "raise capital",
            "limited partners",
            "guaranteed returns",
            "beats wall street",
            "places live orders",
            "executes live orders",
            "automatically authorized to trade",
            "turnkey live automation",
        ]

        for claim in forbidden_claims:
            self.assertNotIn(claim, combined)

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
        professional = (WEB / "professional.js").read_text(encoding="utf-8")
        build = (ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8")

        self.assertIn('Research desks <b>7</b>', index)
        self.assertIn('./desk-architecture.js', index)
        self.assertIn('"desk-architecture.js"', build)
        self.assertIn('Bonds &amp; Rates', architecture)
        self.assertIn('DESK 07 · MACRO ANCHOR', architecture)
        self.assertIn('Architecture only', architecture)
        self.assertIn('No evaluated signal is published for this desk yet.', architecture)
        self.assertIn("['Bonds & Rates'", professional)
        self.assertIn('Seven research desks.<br>Six evaluated workflows.', professional)
        self.assertIn('<b>DESKS</b> SEVEN', professional)
        self.assertIn('<b>EVALUATED</b> SIX', professional)
        self.assertNotIn('Six research workflows.<br>Structured decision support.', professional)
        self.assertNotIn('<b>WORKFLOWS</b> SIX DESKS', professional)

    def test_homepage_marketing_hierarchy_is_process_first(self):
        professional = (WEB / "professional.js").read_text(encoding="utf-8")
        audit = (ROOT / "docs" / "EMPORION_MARKETING_CLAIM_AUDIT.md").read_text(encoding="utf-8")

        for fragment in [
            "Too much information, too little decision discipline.",
            "Bring your watchlist. Research it your way.",
            "Your choice. Your data. Your money.",
            "Candidate intake",
            "Research desks",
            "Scenario analysis",
            "Yellow Sheets",
            "Human review",
            "Research only",
            "Decision ready",
            "User-controlled extension",
        ]:
            self.assertIn(fragment, professional)

        self.assertIn("Watchlist import or connection | Roadmap / not implemented", audit)
        self.assertIn("Broker connection | Extension point", audit)
        self.assertIn("Live order placement | Roadmap / not implemented", audit)
        self.assertIn("Turnkey automation | Roadmap / not implemented", audit)

    def test_candidate_page_explains_the_mvp_without_overclaiming_functionality(self):
        app = (WEB / "app.js").read_text(encoding="utf-8")
        explainer = (WEB / "candidate-context.js").read_text(encoding="utf-8")
        index = (WEB / "index.html").read_text(encoding="utf-8")
        build = (ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8")

        for fragment in [
            "Candidates are the research queue, not recommendations.",
            "HOW EMPORION TURNS A SYMBOL INTO A DECISION",
            "Institutional-style trade decision workflow",
            "Research the idea",
            "Challenge the thesis",
            "Decide with discipline",
            "Candidate intake",
            "Desk method",
            "Evidence qualification",
            "Scenario + Yellow Sheet",
            "Human decision",
            "Published paper snapshot",
            "does not authorize a trade",
        ]:
            self.assertIn(fragment, explainer)

        self.assertIn('./candidate-context.js', index)
        self.assertIn('"candidate-context.js"', build)
        self.assertLess(index.index('./app.js'), index.index('./candidate-context.js'))
        self.assertIn("Current market evidence and method scoring are not connected yet.", app)
        self.assertIn("Method-qualified picks','0'", app)
        self.assertIn("Trade authorization','0'", app)
        self.assertNotIn("automatically executes", explainer.lower())
        self.assertNotIn("live candidate scoring", explainer.lower())
        self.assertNotIn("guaranteed alpha", explainer.lower())
        self.assertNotIn("generates alpha", explainer.lower())

    def test_workspace_navigation_resets_scroll_without_duplicate_click_stickiness(self):
        index = (WEB / "index.html").read_text(encoding="utf-8")
        build = (ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8")
        stability = (WEB / "navigation-stability.js").read_text(encoding="utf-8")

        self.assertIn("./navigation-stability.js", index)
        self.assertIn('"navigation-stability.js"', build)
        self.assertIn("const WORKSPACE_ROUTES = new Set", stability)
        self.assertIn("'scenarios'", stability)
        self.assertIn("'journal'", stability)
        self.assertIn("'resources'", stability)
        self.assertIn("function resetWorkspaceScroll()", stability)
        self.assertIn("window.scrollTo({ top: 0, left: 0, behavior: 'auto' })", stability)
        self.assertIn("main.focus({ preventScroll: true })", stability)
        self.assertIn("currentRoute() === link.dataset.nav", stability)
        self.assertIn("window.addEventListener('hashchange', resetWorkspaceScroll)", stability)

    def test_workspace_router_and_enhancers_do_not_lock_after_scenario_lab(self):
        app = (WEB / "app.js").read_text(encoding="utf-8")
        polish = (WEB / "ui-polish.js").read_text(encoding="utf-8")
        yellow = (WEB / "yellow-sheet.js").read_text(encoding="utf-8")

        self.assertIn("resources:'Research resources'", app)
        self.assertIn("function resources()", app)
        self.assertIn("journal,resources,about", app)
        self.assertIn("function setText(node, value)", polish)
        self.assertIn("node.textContent !== value", polish)
        self.assertIn("function setText(node, value)", yellow)
        self.assertIn("node.textContent !== value", yellow)
        self.assertIn("if (secondSub) setText(secondSub", yellow)

    def test_scenario_lab_contract_is_snapshot_driven_and_fail_closed(self):
        app = (WEB / "app.js").read_text(encoding="utf-8")
        core = (WEB / "core.mjs").read_text(encoding="utf-8")

        self.assertIn("function scenarios()", app)
        self.assertIn("function renderScenarios()", app)
        self.assertIn("scenarioRows(report)", app)
        self.assertIn("filterRows(scenarioRows(report)", app)
        self.assertIn("report.war_games", core)
        self.assertIn("report.portfolio_stress.scenarios", core)
        self.assertIn("candidate.report?.environment!=='paper'", app)
        self.assertIn("candidate.report.live_orders_enabled!==false", app)
        self.assertIn("candidate.report.projects.length!==6", app)
        self.assertIn("Exact engine record. Synthetic fixture only.", app)
        self.assertNotIn("runScenario", app)
        self.assertNotIn("executeScenario", app)


if __name__ == "__main__":
    unittest.main()
