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

    def test_about_page_publishes_the_access_tiers_openly(self):
        # The membership model is public, not hidden: guests can read exactly
        # what the tiers are and what each gets.
        app = (WEB / "app.js").read_text(encoding="utf-8")
        self.assertIn("Access & membership", app)
        self.assertIn("Guest", app)
        self.assertIn("Member", app)
        self.assertIn("LP", app)
        # honest framing: read-only broker + not investment advice
        self.assertIn("read-only", app.lower())
        self.assertIn("Not a paid tier", app)
        self.assertIn("investment advice", app.lower())
        # guests can open the sign-in surface from the public page
        self.assertIn("open-account", app)

    def test_public_brand_and_copy_stay_launch_safe(self):
        index = (WEB / "index.html").read_text(encoding="utf-8")
        professional = (WEB / "professional.js").read_text(encoding="utf-8")
        combined = index + professional

        self.assertIn("Emporion", combined)
        self.assertIn("Markets · Intelligence · Discipline", combined)
        self.assertIn("A Bolton Investment Group (BIG) Project", combined)
        self.assertIn('brand/emporion-logo-hermes-transparent.png', index)
        self.assertNotIn('emporion-institutional-seal.svg', combined)
        self.assertIn('Independent research platform', combined)
        self.assertIn('RESEARCH PLATFORM', combined)
        self.assertIn('Seven research desks.<br>Six evaluated workflows.', combined)
        self.assertIn('<b>6</b> desks + 1 coming soon', combined)
        self.assertIn('No orders placed', combined)
        self.assertNotIn('AI-native', combined)
        self.assertNotIn('brandmark', combined)
        self.assertNotIn('Controls & evidence', combined)
        self.assertNotIn('function controlsBlock()', professional)

    def test_noir_brand_contrast_is_enforced(self):
        index = (WEB / "index.html").read_text(encoding="utf-8")
        noir = (WEB / "noir-shell.css").read_text(encoding="utf-8")
        build = (ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8")

        self.assertLess(index.index("./styles.css"), index.index("./noir-shell.css"))
        self.assertIn("brand/emporion-logo-hermes-transparent.png", index)
        self.assertIn('"brand/emporion-logo-hermes-transparent.png"', build)
        self.assertNotIn("emporion-institutional-seal.svg", index)
        self.assertIn("body, .shell, main", noir)
        self.assertIn(".wb-card, .wb-chip", noir)
        self.assertIn("background: var(--noir-surface) !important", noir)
        self.assertIn(".brand-logo, .emporion-about-logo", noir)
        self.assertIn("background: transparent !important", noir)
        self.assertIn(".graham-needs-you", noir)
        self.assertIn("color: var(--brass-bright) !important", noir)

    def test_noir_brand_palette_meets_readable_contrast(self):
        def luminance(hex_color):
            value = hex_color.lstrip("#")
            channels = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
            def linearize(channel):
                return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
            r, g, b = [linearize(channel) for channel in channels]
            return 0.2126 * r + 0.7152 * g + 0.0722 * b

        def contrast(foreground, background):
            high, low = sorted((luminance(foreground), luminance(background)), reverse=True)
            return (high + 0.05) / (low + 0.05)

        backgrounds = ("#0a0a0c", "#121215", "#0e0e11")
        foregrounds = ("#c6a15b", "#dcb96f", "#f4f1e8", "#a39e93")
        for foreground in foregrounds:
            for background in backgrounds:
                self.assertGreaterEqual(
                    contrast(foreground, background),
                    4.5,
                    f"{foreground} on {background} must remain WCAG AA readable",
                )

    def test_professional_desk_surface_is_noir_not_light(self):
        professional = (WEB / "professional.js").read_text(encoding="utf-8")
        self.assertIn("background:#121215", professional)
        self.assertIn("color:#dcb96f", professional)
        self.assertIn("color:#f4f1e8", professional)
        self.assertNotIn("border:1px solid #d7dee2;background:#fff", professional)
        self.assertNotIn(".ws-ror{border-top:1px solid #e6eaed;background:#fff", professional)
        self.assertNotIn("background:#fafbfc", professional)
        self.assertNotIn("background:#f7f9fa", professional)

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

        self.assertIn('Research desks <b>6+1</b>', index)
        self.assertIn('./desk-architecture.js', index)
        self.assertIn('"desk-architecture.js"', build)
        self.assertIn('Bonds &amp; Rates', architecture)
        self.assertIn('DESK 07</span>', architecture)
        self.assertIn('Coming soon', architecture)
        self.assertIn('Research for this desk is still in progress.', architecture)
        self.assertIn("['Bonds & Rates'", professional)
        self.assertIn('Seven research desks.<br>Six evaluated workflows.', professional)
        self.assertIn('<b>6</b> desks + 1 coming soon', professional)
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

    def test_homepage_explains_ror_as_independent_survival_gate(self):
        professional = (WEB / "professional.js").read_text(encoding="utf-8")

        for fragment in [
            "Deterministic risk gate",
            "RISK OF RUIN / PORTFOLIO SURVIVAL",
            "Survival before conviction.",
            "research thesis cannot override the risk gate",
            "independent portfolio-survival checkpoint",
            "Human review comes after the risk state",
        ]:
            self.assertIn(fragment, professional)

        self.assertNotIn("RoR guarantees", professional)
        self.assertNotIn("RoR authorizes", professional)
        self.assertNotIn("human can override", professional.lower())

    def test_candidate_page_explains_the_mvp_without_overclaiming_functionality(self):
        app = (WEB / "app.js").read_text(encoding="utf-8")
        explainer = (WEB / "candidate-context.js").read_text(encoding="utf-8")
        index = (WEB / "index.html").read_text(encoding="utf-8")
        build = (ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8")

        for fragment in [
            "Candidates are the research queue, not recommendations.",
            "HOW EMPORION TURNS A SYMBOL INTO A DECISION",
            "institutional-style trade decision workflow",
            "Research the idea",
            "Challenge the thesis",
            "Decide with discipline",
            "Candidate intake",
            "Desk research",
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
        self.assertIn("Overnight candidates", app)
        self.assertIn("Overnight wheel candidates from the nightly batch", app)
        self.assertIn("Short puts',assessed.filter", app)
        # The internal "Trade authorization 0" stat was UI slop (user-directed
        # removal 2026-09-26); the no-orders boundary is stated once in
        # disclosures.json and enforced in the API payload contract.
        self.assertNotIn("Trade authorization','0'", app)
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
        self.assertNotIn("'scenarios'", stability)
        self.assertIn("'journal'", stability)
        self.assertIn("'resources'", stability)
        self.assertIn("function resetWorkspaceScroll()", stability)
        self.assertIn("window.scrollTo({ top: 0, left: 0, behavior: 'auto' })", stability)
        self.assertIn("main.focus({ preventScroll: true })", stability)
        self.assertIn("currentRoute() === link.dataset.nav", stability)
        self.assertIn("window.addEventListener('hashchange', resetWorkspaceScroll)", stability)

    def test_workspace_router_and_enhancers_do_not_lock_after_candidate_filter(self):
        app = (WEB / "app.js").read_text(encoding="utf-8")
        polish = (WEB / "ui-polish.js").read_text(encoding="utf-8")
        yellow = (WEB / "yellow-sheet.js").read_text(encoding="utf-8")

        self.assertIn("resources:'Research resources'", app)
        self.assertIn("function resources()", app)
        self.assertIn("journal,resources,guide,workbench", app)
        self.assertIn("workbench,'real-estate':realEstate,brief,about", app)
        self.assertIn("function setText(node, value)", polish)
        self.assertIn("node.textContent !== value", polish)
        self.assertIn("function setText(node, value)", yellow)
        self.assertIn("node.textContent !== value", yellow)
        self.assertIn("if (secondSub) setText(secondSub", yellow)

    def test_graham_filter_contract_is_embedded_and_fail_closed(self):
        app = (WEB / "app.js").read_text(encoding="utf-8")
        index = (WEB / "index.html").read_text(encoding="utf-8")
        graham = (WEB / "graham-filter.mjs").read_text(encoding="utf-8")

        self.assertIn("assessShortPut", app)
        self.assertIn("extractShortPutRows", app)
        self.assertIn("fetch('./api/am-report'", app)
        self.assertIn("graham-filter-toggle", app)
        self.assertIn("Own if assigned?", app)
        self.assertIn("MR. MARKET", app)
        self.assertIn("verdict = 'SPECULATION'", graham)
        self.assertIn("verdict = 'NEEDS_YOU'", graham)
        self.assertIn("verdict = 'INVESTMENT'", graham)
        self.assertIn("config.manicBump", graham)
        self.assertNotIn('href="#scenarios"', index)
        self.assertNotIn('./scenario-lab.js', index)
        self.assertNotIn("function scenarios()", app)
        self.assertNotIn("renderScenarios()", app)
        self.assertIn("candidate.report?.environment!=='paper'", app)
        self.assertIn("candidate.report.live_orders_enabled!==false", app)
        self.assertIn("candidate.report.synthetic_data!==false", app)


if __name__ == "__main__":
    unittest.main()