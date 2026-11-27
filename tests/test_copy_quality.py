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


class SchwabDisclosureTests(unittest.TestCase):
    """The Desk 5 'Broker data status' panel is locked compliance copy.

    Desk 5 shows borrow / short-interest data, so the view must say plainly
    that Schwab / thinkorswim is not connected and no account, locate, or
    order endpoint is accessed. The panel was dropped in a squash merge
    (PR #169) and restored by this branch; pin the exact wording in
    web/app.js so it cannot silently disappear again.
    """

    LOCKED_FRAGMENTS = (
        "Broker data status",
        "Schwab / thinkorswim is not connected to this research view.",
        "No Schwab account, positions, balances, order history, "
        "locate request, or order endpoint is accessed here.",
    )

    def test_broker_data_status_panel_present_in_desk5(self):
        src = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        for fragment in self.LOCKED_FRAGMENTS:
            self.assertIn(fragment, src,
                          f"Schwab disclosure missing from web/app.js: {fragment!r}")


if __name__ == "__main__":
    unittest.main()
