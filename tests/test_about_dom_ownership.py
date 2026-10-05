"""About-page DOM ownership regression test.

Guards the root causes of the 2026-10-04 About incidents:
- PRs #146/#149: two modules owned the same About branding at the same time.
  brand-logo.js injected a second Emporion lockup into the About header that
  professional.js already rendered -> duplicate logos on prod.
- PR #150: professional.js watched #main with a MutationObserver whose
  zero-arg callback re-ran renderContext() on EVERY childList mutation --
  including the ones renderContext() itself makes -> self-triggering loop
  that made the About page disappear/flicker on prod.

Static analysis over web/*.js source (dist/ excluded). These are
single-ownership invariants: if a future change breaks one, the change is
re-introducing the exact failure class, not a styling preference.

What this test deliberately does NOT cover (Sol's lane): rendered visual
output. A browser-level visual check remains the complement, not a
substitute.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = REPO_ROOT / "web"


def web_sources():
    """All web JS source files, excluding build output."""
    return sorted(p for p in WEB_DIR.glob("*.js") if "dist" not in p.parts)


def read(p):
    return p.read_text(encoding="utf-8")


class AboutDomOwnershipTests(unittest.TestCase):
    def test_about_logo_has_single_owner(self):
        """Exactly one module may create the About logo.

        The duplicate-logo incident happened because a second module injected
        About branding. If another file starts mentioning .emporion-about-logo,
        that is the incident recurring -- fail the build.
        """
        owners = [p.name for p in web_sources() if "emporion-about-logo" in read(p)]
        self.assertEqual(
            owners, ["professional.js"],
            f"About logo ownership violated: {owners}. "
            "Exactly one module (professional.js) may own .emporion-about-logo.",
        )

    def test_about_brand_block_has_single_creator(self):
        """Only professional.js may define the About brand block.

        aboutCapitalBlock() is the sole constructor of the About header
        branding. A second definition or a second injection site is the
        #146 failure.
        """
        creators = [p.name for p in web_sources() if "aboutCapitalBlock" in read(p)]
        self.assertEqual(
            creators, ["professional.js"],
            f"About brand-block creator violated: {creators}.",
        )

    def test_no_foreign_about_brand_injection(self):
        """No module besides professional.js may inject About branding.

        brand-logo.js's #146 injection referenced the About header. Any future
        file touching the About brand selectors below is re-introducing
        overlapping ownership.
        """
        markers = ("emporion-about-logo", "aboutCapitalBlock", "ws-about-brand")
        violators = [
            p.name
            for p in web_sources()
            if p.name != "professional.js"
            and any(m in read(p) for m in markers)
        ]
        self.assertEqual(
            violators, [],
            f"Foreign About-brand injection: {violators}. "
            "About branding is owned solely by professional.js.",
        )

    def test_mutation_observers_guard_self_mutations(self):
        """professional.js observers must inspect mutation records, never blind-render.

        The #150 render loop: a zero-arg MutationObserver callback re-ran
        renderContext() on every mutation, including its own. The fix inspects
        the mutation records and skips self-mutations. Lock the fix in.
        """
        src = read(WEB_DIR / "professional.js")

        blind = re.findall(r"new\s+MutationObserver\(\s*\(\s*\)\s*=>", src)
        self.assertEqual(
            blind, [],
            "professional.js contains a zero-arg MutationObserver callback -- "
            "the #150 self-triggering pattern. The callback must take the "
            "mutation records and skip self-mutations.",
        )

        guarded = re.findall(r"new\s+MutationObserver\(\s*\(\s*[A-Za-z_]", src)
        self.assertTrue(
            guarded,
            "professional.js has no MutationObserver that inspects its mutation "
            "records -- the #150 guard appears to have been removed.",
        )
        self.assertIn(
            "addedNodes", src,
            "professional.js observer no longer inspects addedNodes -- "
            "the self-mutation filter from #150 is gone.",
        )

    def test_sidebar_remains_scrollable(self):
        """The fixed sidebar must stay vertically scrollable.

        2026-10-04 (#152): the About nav link was clipped below the viewport
        on shorter screens because .sidebar had no overflow-y. If the
        overflow-y is removed, nav items clip again -- fail the build.
        """
        css = read(WEB_DIR / "noir-shell.css")
        blocks = re.findall(r"\.sidebar\s*\{[^}]*\}", css)
        self.assertTrue(blocks, ".sidebar rule not found in noir-shell.css")
        self.assertTrue(
            any("overflow-y" in b for b in blocks),
            ".sidebar lost its overflow-y -- nav items will clip below the "
            "viewport again (see #152).",
        )


if __name__ == "__main__":
    unittest.main()
