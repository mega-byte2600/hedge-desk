"""Claim discipline on the public surface — an engineering control, not a slogan.

Direction taken from FINRA Rule 2210 (Communications with the Public: fair, balanced,
not misleading) and the repo's own audit in docs/EMPORION_MARKETING_CLAIM_AUDIT.md.

The product has no registration, no performance record, no approved status, and no
market access. Public copy therefore must not:
  * promise outcomes (guaranteed, risk-free, will make, beat the market),
  * imply regulatory status or approval (SEC-approved, FINRA-registered, insured, FDIC),
  * imply we act as a registered representative, broker, or adviser,
  * present paper or synthetic output as a live result.

This scans the shipped surface (the files that become dist/, which is what visitors
receive) so a claim that drifts fails a CI run instead of reaching a demo audience.
It is a tripwire for the obvious violations, not a legal review.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"

# The shipped surface: everything the console can render or fetch.
SHIPPED_GLOBS = ("*.js", "*.mjs", "*.html", "*.css", "*.json")

# Patterns that must never appear in shipped copy. Each is a plain-language claim the
# product cannot support; the banned list is deliberately narrow so ordinary honest
# wording is not flagged.
BANNED = [
    (r"\bguarantee(d|s)?\b", "guaranteed outcome"),
    (r"\brisk[-\s]?free\b", "risk-free claim"),
    (r"\bsec[-\s]?approved\b", "implied SEC approval"),
    (r"\bfinra[-\s]?registered\b", "implied FINRA registration"),
    (r"\bregistered (representative|rep|broker|adviser|advisor)\b", "implied registration"),
    (r"\bfdic\b|\bsipc\b", "implied insurance"),
    (r"\binsured\b", "implied insurance"),
    (r"\bbeat the market\b", "performance promise"),
    (r"\bwill (make|earn|return) you\b", "performance promise"),
    (r"\bno risk\b", "risk-free claim"),
]


def _shipped_text() -> list[tuple[str, str]]:
    out = []
    for pattern in SHIPPED_GLOBS:
        for path in sorted(WEB.glob(pattern)):
            if path.name.endswith(".test.mjs"):
                continue
            try:
                out.append((path.name, path.read_text(encoding="utf-8")))
            except (UnicodeDecodeError, OSError):
                continue
    return out


NEGATION = re.compile(r"\b(not|no|never|cannot|can't|isn't|aren't|without|nor)\b", re.I)


def _is_negated(text: str, start: int) -> bool:
    """True when the match sits inside a disclaimer.

    Disclaimers legitimately contain these words — "not investment advice or a
    performance guarantee", "no guarantee of results". An earlier version of this
    check flagged the product's own risk disclaimer, which is the opposite of a
    violation, so a negation in the short window before the match clears it.
    """
    window = text[max(0, start - 48): start]
    return bool(NEGATION.search(window))


class PublicClaimTests(unittest.TestCase):
    def test_shipped_surface_makes_no_unsupportable_claim(self):
        offenders = []
        for name, text in _shipped_text():
            for pattern, why in BANNED:
                for m in re.finditer(pattern, text, re.I):
                    if _is_negated(text, m.start()):
                        continue          # a disclaimer, not a claim
                    snippet = text[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")
                    offenders.append(f"{name}: '{m.group(0)}' ({why}) ...{snippet.strip()}...")
        self.assertEqual(
            offenders,
            [],
            "public copy must not make claims the product cannot support:\n  "
            + "\n  ".join(offenders[:10]),
        )

    def test_negation_guard_does_not_disable_the_check(self):
        # The negation guard must not swallow real violations.
        self.assertFalse(_is_negated("We guarantee returns.", 3))
        self.assertTrue(_is_negated("not investment advice or a performance guarantee.", 44))
        for phrase, should_flag in [
            ("guaranteed results", True),
            ("not a guarantee", False),
            ("no risk of loss", False),
            ("risk-free returns", True),
            ("SEC-approved strategy", True),
            ("we are not SEC-approved", False),
        ]:
            match = None
            for pattern, _ in BANNED:
                match = re.search(pattern, phrase, re.I)
                if match:
                    break
            hit = bool(match) and not _is_negated(phrase, match.start())
            self.assertEqual(hit, should_flag, f"{phrase!r} -> expected flagged={should_flag}")


    def test_paper_only_boundary_is_stated_on_the_shipped_surface(self):
        # The boundary is the product's central honest claim; it must exist and must
        # not be phrased as a live-trading capability.
        text = "\n".join(t for _, t in _shipped_text())
        self.assertRegex(
            text,
            r"paper[-\s]?only|not .{0,40}(live|real).{0,20}(trading|orders)|no orders",
            "the shipped surface must state the paper-only / no-orders boundary",
        )

    def test_scan_actually_reads_the_surface(self):
        # A guard that silently scans nothing is worse than no guard.
        files = _shipped_text()
        self.assertGreater(len(files), 5, "expected the console bundle files to be scanned")
        self.assertTrue(any(n == "app.js" for n, _ in files), "app.js should be in the surface")


if __name__ == "__main__":
    unittest.main()
