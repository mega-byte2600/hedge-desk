"""Guards for the browser bundle that Python unit tests cannot otherwise reach.

The console's page enhancers register MutationObservers over ``main`` and then
write into that same subtree. A callback that is not idempotent re-enters
itself and spin-locks the page's main thread, which freezes the whole console
solid (no clicks, no sign-in). These tests keep the guards in place.
"""

import re
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "web"


class MutationObserverGuardTests(unittest.TestCase):
    def setUp(self):
        self.src = (WEB / "ror-positioning.js").read_text(encoding="utf-8")

    def test_risk_tape_write_is_guarded(self):
        """The RISK tape rewrite must be idempotent, like the risk block."""
        guard = re.search(r"if \(riskTape[^\n]*rorTape[^\n]*\)\s*\{", self.src)
        self.assertIsNotNone(
            guard,
            "ror-positioning.js must guard the risk-tape innerHTML write; "
            "unguarded it re-triggers its own MutationObserver and freezes the page",
        )

    def test_observer_does_not_call_the_mutator_synchronously(self):
        """A synchronous observer callback can never yield, so it must be deferred."""
        self.assertNotIn("new MutationObserver(() => applyRoRPositioning())", self.src)
        self.assertIn("() => requestAnimationFrame(applyRoRPositioning)", self.src)


if __name__ == "__main__":
    unittest.main()
