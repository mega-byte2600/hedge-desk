"""The copy-quality gate as a CI test.

Agent-pushed website copy is a common failure mode (AI slop and internal
jargon leaking into user-facing copy with no human in the loop). The
deterministic lint in scripts/lint_copy.py is the open-source standard:
it fails closed on known slop patterns. This test runs it inside the suite
so CI enforces it on every commit.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import lint_copy  # noqa: E402


class CopyQualityGateTests(unittest.TestCase):
    def test_no_slop_or_internal_jargon_in_shipped_copy(self):
        hits = lint_copy.lint()
        self.assertEqual(hits, [], "copy-quality gate failed:\n" + "\n".join(hits))


class AboutCopyConsistencyTests(unittest.TestCase):
    """Source copy must match served copy on the About page.

    Found 2026-11-21, Saturday polish: web/ui-polish.js rewrites the About
    card's first paragraph on every render (MutationObserver), so the
    paragraph in web/app.js about() is dead copy at runtime — and it had
    drifted stale, still calling Bonds & Rates "in development" after main
    shipped the Desk 7 indicator board (PR #169). The served text is the
    product decision ("six specialized research workflows"); this pins
    app.js to it so the two cannot drift again.
    """

    SERVED_ABOUT = (
        "Emporion is an independent market research platform built around "
        "six specialized research workflows, explicit evidence requirements, "
        "deterministic controls, and human judgment."
    )

    def test_about_source_copy_matches_served_copy(self):
        app_js = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        self.assertIn(self.SERVED_ABOUT, app_js)
        self.assertNotIn("in development", app_js)


if __name__ == "__main__":
    unittest.main()
