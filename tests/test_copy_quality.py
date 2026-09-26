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


if __name__ == "__main__":
    unittest.main()
