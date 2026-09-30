#!/usr/bin/env python3
"""Copy-quality gate for agent-pushed website copy.

Problem: agents pushing copy to production websites is a common failure mode.
AI slop (throat-clearing, hedging, corporate filler) and internal jargon
("paper-only" chants, trade_authorized flags, effective-dates) leak into
user-facing copy, and no human reviews every agent commit.

This is the open-source version of the standard: a deterministic, no-LLM
lint that fails closed. It scans the shipped surface for known slop patterns
and fails with file:line hits. Run it in CI on every commit that touches
user-facing copy.

Design notes (from real incidents in this repo):
- The compliance boundary ("does not place orders") is stated ONCE in
  web/disclosures.json (pinned by tests/test_disclosures.py). Repeating it
  on every card is slop, not safety. This lint bans the chant, not the claim.
- trade_authorized stays in API payloads (the real safety contract). It must
  never render as UI copy.
- Pattern lists are deliberately narrow: a lint that false-positives on
  ordinary honest wording gets disabled. Add a pattern only with a real
  incident behind it.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"

# User-facing copy sources. report.json/timeline.json are data/history, not copy.
COPY_GLOBS = ("*.js", "*.mjs", "*.html", "*.css")
COPY_EXTRA = (
    ROOT / "scripts" / "build_plotly_dashboard.py",
    ROOT / "hedge_desk" / "web_app.py",  # contains dashboard JS template
    # Incident 2026-09-29: the daily brief publishes to production with no
    # human review. Its rendered copy (titles, details, desk notes) gets the
    # same slop/jargon gate as every other user-facing surface.
    WEB / "research-brief.json",
)
SKIP_FILES = {p.name for p in WEB.glob("*.test.*")}

# (pattern, reason) — add only with a real incident behind the entry.
SLOP = [
    (r"stated plainly,?", "throat-clearing (incident 2026-09-26: disclosures intro)"),
    (r"it's important to note", "hedging filler"),
    (r"it's worth noting", "hedging filler"),
    (r"in today'?s fast-paced", "corporate filler"),
    (r"\bdelve into\b", "AI-ism"),
    (r"\bfurthermore,", "AI-ism"),
    (r"\bmoreover,", "AI-ism"),
    (r"\butilize\b", "AI-ism, prefer 'use'"),
    (r"\brobust solution\b", "corporate filler"),
    (r"\bcutting-edge\b", "corporate filler"),
    (r"\bseamless\b", "corporate filler"),
    (r"\bgame-?changer\b", "corporate filler"),
    (r"\bdeep dive\b", "AI-ism"),
]

# Internal concepts that must never render as user-facing copy.
LEAKS = [
    (r"tag\(\s*['\"]PAPER_ONLY['\"]\s*\)", "paper-only tag chant (incident 2026-09-26)"),
    (r"Effective\s+(\$\{|20\d\d-)", "effective-date in rendered copy (incident 2026-09-26)"),
    (r"trade_authorized\s*\?\s*['\"]AUTHORIZED['\"]", "auth ternary rendered as UI copy"),
    # Incident 2026-09-26: internal reason_codes displayed raw via replaceAll.
    # Reason codes (UPSTREAM_OR_AUTH_FAILURE, etc.) must be mapped to plain
    # language, never string-munged into display text.
    (r"reason_code\?\s*\.\s*replaceAll\(\s*['\"]_['\"]", "raw reason_code displayed via replaceAll (incident 2026-09-26: UPSTREAM OR AUTH FAILURE)"),
    # Incident 2026-09-26: internal mode enums rendered directly in tables.
    # Only match display contexts (esc(), f-string interpolation, textContent).
    # Logic comparisons (if mode == "...") are fine.
    (r"esc\([^)]*REAL_CBOE_CHAIN_INCOME", "internal mode code in display path (use _human_status)"),
    (r"esc\([^)]*READY_FOR_RESEARCH", "internal mode code in display path (use _human_status)"),
    (r"textContent\s*=\s*['\"]REAL_", "internal mode code assigned to UI text"),
    # Incident 2026-09-26: engineering jargon in user-facing summaries.
    (r"production probes", "engineering jargon in user copy (incident 2026-09-26)"),
    (r"strategy-input", "engineering jargon in user copy (incident 2026-09-26)"),
    # Incident 2026-09-26: finance/trader jargon in user-facing labels.
    (r"\bEOD batch\b", "trader jargon in user copy, use 'Daily prices' (incident 2026-09-26)"),
    (r"\([\"']CSP scan", "acronym jargon in user label, spell out (incident 2026-09-26)"),
    (r"VIX regime", "jargon in user copy, use 'Market volatility' (incident 2026-09-26)"),
    (r"positioning rows", "jargon in user copy (incident 2026-09-26)"),
    (r"adv\s+\$\{", "trader abbreviation in user copy, spell out 'up/down' (incident 2026-09-26)"),
    (r"observations['\"`]\s*;", "stats jargon in user copy, use 'data points' (incident 2026-09-26)"),
    # Incident 2026-09-26: meaningless internal status labels on the desk list.
    (r"DATA INTEGRATION", "internal status jargon in user copy, use 'Active' (incident 2026-09-26)"),
    (r"ARCHITECTURE ONLY", "internal status jargon in user copy, use 'Framework' (incident 2026-09-26)"),
    (r"Operating state", "jargon header in user copy, use 'Status' (incident 2026-09-26)"),
]


def iter_copy_files():
    for pattern in COPY_GLOBS:
        for path in sorted(WEB.glob(pattern)):
            if path.name in SKIP_FILES:
                continue
            yield path
    for path in COPY_EXTRA:
        yield path


def lint() -> list[str]:
    hits = []
    for path in iter_copy_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for pattern, reason in SLOP + LEAKS:
                if re.search(pattern, line, re.IGNORECASE):
                    hits.append(f"{path.relative_to(ROOT)}:{lineno}: [{reason}] {line.strip()[:100]}")
    return hits


def main() -> int:
    hits = lint()
    if hits:
        print(f"copy-quality gate FAILED: {len(hits)} hit(s)\n")
        for h in hits:
            print(" ", h)
        print("\nFix the copy or, if a hit is a false positive, narrow the pattern")
        print("(patterns are deliberately narrow; see module docstring).")
        return 1
    print("copy-quality gate passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
