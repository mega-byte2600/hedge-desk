"""The public topbar must keep its breadcrumb and status text visually separated."""

import re
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "web"
STYLES = WEB / "styles.css"
INDEX = WEB / "index.html"


def rule_body(css: str, selector: str) -> str:
    """Return the declaration block for a selector, or '' if absent."""
    match = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", css)
    return match.group(1) if match else ""


class TopbarSpacingTests(unittest.TestCase):
    def test_stylesheet_exists(self):
        self.assertTrue(STYLES.exists(), "web/styles.css is missing")

    def test_status_has_an_explicit_gap_from_the_breadcrumb(self):
        css = STYLES.read_text(encoding="utf-8")
        body = rule_body(css, ".top-status")
        self.assertTrue(body, ".top-status rule not found")
        self.assertRegex(
            body,
            r"margin-left\s*:\s*\d+(\.\d+)?(px|rem|em)",
            "the status text needs a left margin so it stays distinct from the breadcrumb",
        )

    def test_account_control_is_removed(self):
        css = STYLES.read_text(encoding="utf-8")
        html = INDEX.read_text(encoding="utf-8")
        self.assertNotIn(".top-account", css)
        self.assertNotIn("acct-btn", html)

    def test_breadcrumb_and_status_are_separate_elements(self):
        html = INDEX.read_text(encoding="utf-8")
        header = re.search(r"<header class=\"topbar\">(.*?)</header>", html, re.S)
        if header is None:
            self.fail("topbar header not found")
        block = header.group(1)
        self.assertIn('id="breadcrumb"', block, "breadcrumb element missing")
        self.assertIn('class="top-status"', block, "status element missing")
        self.assertNotRegex(
            block,
            r"</strong>Independent",
            "breadcrumb and status must not be adjacent in markup without a separating element",
        )


if __name__ == "__main__":
    unittest.main()
