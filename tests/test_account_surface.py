import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"


class AccountSurfaceTests(unittest.TestCase):
    def test_sign_in_control_is_present_and_not_hidden(self):
        index = (WEB / "index.html").read_text(encoding="utf-8")
        acct = (WEB / "account.js").read_text(encoding="utf-8")

        self.assertIn('id="acct-btn"', index)
        self.assertIn('id="acct-label"', index)
        self.assertIn('id="acct-modal"', index)
        self.assertIn('id="acct-tier"', index)
        self.assertIn('id="acct-social"', index)
        self.assertIn("account.js", index)
        self.assertIn("/api/auth/me", acct)
        self.assertIn("/api/auth/request", acct)
        self.assertIn("/api/auth/verify", acct)
        self.assertIn("/api/tier", acct)
        # social login (Supabase Auth) wiring
        self.assertIn("/api/auth/providers", acct)
        self.assertIn("/api/auth/social", acct)
        self.assertIn("signInWithOAuth", acct)
        # supply-chain: the CDN import must be pinned to an exact version
        self.assertNotIn("supabase-js@2'", acct)
        self.assertRegex(acct, r"@supabase/supabase-js@\d+\.\d+\.\d+")

    def test_broker_ui_is_present_and_read_only(self):
        index = (WEB / "index.html").read_text(encoding="utf-8")
        acct = (WEB / "account.js").read_text(encoding="utf-8")
        self.assertIn('id="acct-broker"', index)
        self.assertIn('id="acct-broker-connect"', index)
        self.assertIn("/api/broker/status", acct)
        self.assertIn("/api/broker/authorize", acct)
        self.assertIn("/api/broker/link", acct)
        # the UI must describe the connection as read-only, never order-capable
        self.assertIn("read-only", (index + acct).lower())
        for forbidden in ("placeOrder", "submitOrder", "place_order", "submit_order"):
            self.assertNotIn(forbidden, acct)

    def test_guest_tier_stays_open_not_walled(self):
        # The research console must remain publicly reachable; sign-in is an
        # opt-in membership layer, not a gate on the whole site.
        index = (WEB / "index.html").read_text(encoding="utf-8")
        app = (WEB / "app.js").read_text(encoding="utf-8")
        self.assertNotIn("require login", index.lower())
        # the console renders from a public report fetch (report.json and/or /api/report)
        has_public_fetch = ("./report.json" in app) or ("/api/report" in app)
        self.assertTrue(has_public_fetch, "console must load a public report")

    def test_account_ui_ships_in_deploy_bundle(self):
        build = (ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8")
        self.assertIn('"account.js"', build)


if __name__ == "__main__":
    unittest.main()
