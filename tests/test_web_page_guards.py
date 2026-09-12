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

        Matches both ``new MutationObserver(() => { ... })`` and the bare-identifier
        form ``new MutationObserver(enhanceCandidates)`` — the latter is how
        candidate-context.js slipped past an earlier version of this check.
        """
        write = re.compile(
            r"\.innerHTML\s*=|insertAdjacentHTML|\.appendChild\(|\.prepend\(|"
            r"\.append\(|\.textContent\s*=|\.setAttribute\("
        )
        defer = re.compile(r"requestAnimationFrame|queueMicrotask|setTimeout")
        offenders = []
        for path in sorted(WEB.glob("*.js")) + sorted(WEB.glob("*.mjs")):
            src = path.read_text(encoding="utf-8")
            for match in re.finditer(
                r"new MutationObserver\(\s*(?:\(\)\s*=>\s*\{|([A-Za-z_$][\w$]*)\s*\))", src
            ):
                line = src[: match.start()].count("\n") + 1
                if match.group(1):
                    # bare identifier callback: the whole named function must defer
                    fn = re.search(
                        rf"function\s+{re.escape(match.group(1))}\s*\([^)]*\)\s*\{{(.*?)\n\}}",
                        src,
                        re.S,
                    )
                    body = fn.group(1) if fn else src[match.end(): match.end() + 600]
                    if defer.search(body) or not write.search(body):
                        continue
                    offenders.append(f"{path.name}:{line} -> {match.group(1)}()")
                else:
                    body = src[match.end(): match.end() + 600]
                    if write.search(body) and not defer.search(body):
                        offenders.append(f"{path.name}:{line}")
        self.assertEqual(
            offenders,
            [],
            "these MutationObserver callbacks write without deferring, which can "
            "re-enter and lock the main thread: " + ", ".join(offenders),
        )

    def test_route_derivation_has_one_definition(self):
        """Enhancers must share currentRoute() from core.mjs.

        Four modules each derived the route with a different default, so on a
        plain "/" load the overview subtitle was written onto the Candidates page.
        """
        core = (WEB / "core.mjs").read_text(encoding="utf-8")
        self.assertIn("export function currentRoute()", core)
        for name in ("ui-polish.js", "acknowledgements.js", "professional.js"):
            src = (WEB / name).read_text(encoding="utf-8")
            self.assertIn("from './core.mjs'", src, f"{name} must import from core.mjs")
            self.assertIn("currentRoute", src, f"{name} must use the shared currentRoute")
            self.assertNotIn("location.hash || '#overview'", src, f"{name} must not keep a private route default")


class YellowSheetSaveTests(unittest.TestCase):
    """The Yellow Sheet lifecycle fields are written by a second submit listener.

    app.js registers a `document` submit listener first and saves the note
    synchronously inside it, so the extension listener must run *after* that save and
    extend the stored record directly. The shipped version deferred itself with
    queueMicrotask and then compared note counts: the microtask drains at the
    checkpoint right after its own listener returns (before app.js saves), and the
    count guard `notes.length !== before + 1` could never be satisfied because
    `before` was read after the save. Symbol, position, horizon, planned exit, trade
    status, entry/exit execution, why-exit and post-trade review were collected and
    silently discarded.
    """

    def _listener(self):
        src = (WEB / "yellow-sheet.js").read_text(encoding="utf-8")
        marker = "document.addEventListener('submit'"
        self.assertIn(marker, src)
        return src[src.index(marker):]

    def test_extension_runs_after_the_base_save(self):
        listener = self._listener()
        self.assertNotIn(
            "{ capture: true }",
            listener,
            "the extension must be a bubble-phase listener so app.js's save has already "
            "run; capturing makes it read the store before the record exists",
        )

    def test_extension_is_not_deferred(self):
        listener = self._listener()
        self.assertNotIn(
            "queueMicrotask",
            listener,
            "a microtask queued here drains before app.js's bubble listener saves, so "
            "the record being extended does not exist yet",
        )

    def test_extension_confirms_the_base_save_landed(self):
        listener = self._listener()
        self.assertIn(
            "last.thesis !== values.thesis",
            listener,
            "the extension must confirm the just-saved record is the one being extended",
        )
        self.assertIn("yellow_sheet_extended", listener, "the extension must be idempotent")

    def test_lifecycle_fields_are_written(self):
        listener = self._listener()
        for field in ("symbol", "position", "horizon", "planned_exit", "trade_status",
                      "entry_execution", "exit_execution", "why_exit", "post_trade_review"):
            self.assertIn(field, listener, f"{field} must be persisted")

    def test_app_js_still_loads_before_yellow_sheet_js(self):
        """The extension depends on this order; reordering breaks it."""
        html = (WEB / "index.html").read_text(encoding="utf-8")
        self.assertLess(
            html.index("./app.js"),
            html.index("./yellow-sheet.js"),
            "app.js must load before yellow-sheet.js so its save listener runs first",
        )


if __name__ == "__main__":
    unittest.main()
