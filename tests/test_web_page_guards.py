"""Guards for the browser bundle that Python unit tests cannot otherwise reach.

The console's page enhancers register MutationObservers over ``main`` and then
write into that same subtree. A callback that is neither idempotent nor deferred
re-enters itself: the observer callback is a microtask, so it re-queues on its own
mutation and the queue never drains. The page then locks its main thread solid —
no clicks, no sign-in, and on a busy machine the whole browser process stops
responding.

This happened twice, so each mutating enhancer is pinned here:
  * web/ror-positioning.js   — the RISK tape rewrite froze every page load.
  * web/multi-agent-desk.mjs — renderDeskView froze on navigating to the #desk tab.

It only reproduces on routes that are actually visited, which is why these are
source-level checks with a route-walk note rather than a load-time smoke test.
"""

import re
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "web"


class MutationObserverGuardTests(unittest.TestCase):
    def test_ror_positioning_tape_write_is_guarded(self):
        """The RISK tape rewrite must be idempotent, like the risk block."""
        src = (WEB / "ror-positioning.js").read_text(encoding="utf-8")
        guard = re.search(r"if \(riskTape[^\n]*rorTape[^\n]*\)\s*\{", src)
        self.assertIsNotNone(
            guard,
            "ror-positioning.js must guard the risk-tape innerHTML write; "
            "unguarded it re-triggers its own MutationObserver and freezes the page",
        )

    def test_ror_positioning_observer_is_deferred(self):
        src = (WEB / "ror-positioning.js").read_text(encoding="utf-8")
        self.assertNotIn("new MutationObserver(() => applyRoRPositioning())", src)
        self.assertIn("() => requestAnimationFrame(applyRoRPositioning)", src)

    def test_multi_agent_desk_render_is_reentrancy_guarded(self):
        """renderDeskView writes #main, which the desk observer watches."""
        src = (WEB / "multi-agent-desk.mjs").read_text(encoding="utf-8")
        body = src.split("async function renderDeskView()", 1)[-1].split("\nfunction ", 1)[0]
        self.assertIn(
            "_deskRendering",
            body,
            "renderDeskView must bail out when a render is already in flight; "
            "without it the observer re-fires on its own loading-HTML write "
            "and the microtask queue never drains (the #desk tab hangs the page)",
        )
        self.assertIn("_deskRendering = true", body)
        self.assertIn("_deskRendering = false", body)

    def test_multi_agent_desk_observer_is_deferred(self):
        src = (WEB / "multi-agent-desk.mjs").read_text(encoding="utf-8")
        self.assertNotIn("new MutationObserver(() => { if (location.hash", src)
        self.assertIn("requestAnimationFrame", src)

    def test_no_synchronous_observer_callbacks_that_write(self):
        """Every MutationObserver callback that writes to the DOM must defer.

        A synchronously-invoked callback that mutates a subtree it observes cannot
        yield, so it hard-freezes the page. Deferring (rAF or a microtask) is the
        pattern the other enhancers use. Callbacks that only read, or that write
        outside the observed subtree, are not flagged.
        """
        write = re.compile(
            r"\.innerHTML\s*=|insertAdjacentHTML|\.appendChild\(|\.prepend\(|"
            r"\.append\(|\.textContent\s*=|\.setAttribute\("
        )
        defer = re.compile(r"requestAnimationFrame|queueMicrotask|setTimeout")
        offenders = []
        for path in sorted(WEB.glob("*.js")) + sorted(WEB.glob("*.mjs")):
            src = path.read_text(encoding="utf-8")
            for match in re.finditer(r"new MutationObserver\(\(\)\s*=>\s*\{", src):
                body = src[match.end(): match.end() + 600]
                if write.search(body) and not defer.search(body):
                    line = src[: match.start()].count("\n") + 1
                    offenders.append(f"{path.name}:{line}")
        self.assertEqual(
            offenders,
            [],
            "these MutationObserver callbacks write without deferring, which can "
            "re-enter and lock the main thread: " + ", ".join(offenders),
        )


if __name__ == "__main__":
    unittest.main()
