import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"


class AccountSurfaceTests(unittest.TestCase):
    def test_sign_in_and_membership_surface_is_removed(self):
        index = (WEB / "index.html").read_text(encoding="utf-8")
        app = (WEB / "app.js").read_text(encoding="utf-8")
        for retired in ("acct-btn", "acct-modal", "acct-email", "Sign in", "account.js"):
            self.assertNotIn(retired, index)
        for retired in ("Access & membership", "open-account", "Sign in"):
            self.assertNotIn(retired, app)
        self.assertFalse((WEB / "account.js").exists())

    def test_account_ui_is_not_packaged_for_deploy(self):
        build = (ROOT / "scripts" / "build_web.py").read_text(encoding="utf-8")
        self.assertNotIn('"account.js"', build)

    def test_account_styles_are_removed(self):
        styles = (WEB / "styles.css").read_text(encoding="utf-8")
        self.assertNotIn("acct-", styles)
        self.assertNotIn("top-account", styles)

    def test_public_research_report_remains_available(self):
        app = (WEB / "app.js").read_text(encoding="utf-8")
        self.assertIn("./api/report", app)


if __name__ == "__main__":
    unittest.main()
