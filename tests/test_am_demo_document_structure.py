"""Document-structure regression: the AM demo page must not have duplicate or
out-of-order numbered section headings.

This closes a measure gap: prior tests rendered isolated per-panel helpers
(_csp_block/_csp_top_pick) and never the full page, so two consecutive "6."
headings (Paper-outcome loop and Rates environment) shipped undetected. A
byte-identical served-vs-disk check (S6) passed because both copies carried the
same defect. Numbering is presentation, not data — this test measures the
document's structural integrity, not just its values.
"""

import unittest
import re

from hedge_desk.am_demo import _render_report_page


# The page uses order-list-like main section headings:
#   1, 2, 3, 4, 4b, 5, 6, 7, 8
# "4b" is a deliberately nested sub-numbered panel and is allowed once.
EXPECTED_HEADINGS = ["1", "2", "3", "4", "4b", "5", "6", "7", "8"]

_MINIMAL_REPORT = {
    "schema_version": "test",
    "mode": "paper-research",
    "generated_at": "2026-09-20T00:00:00+00:00",
    "eod_batch_status": "READY_FOR_RESEARCH",
    "eod_manifest_sha256": "x",
    "data_freshness": {"as_of": "2026-09-18", "is_current": True},
    "candidate_count": 0,
    "symbol_count": 0,
    "candidates": [],
    "features": {"mode": "test", "symbols": [], "features": [], "note": ""},
    "cash_secured_put_scan": {},
    "chain_income": {},
    "yellow_sheets": [],
    "paper_outcome_summary": {"recorded": 0, "entries": []},
    "vix_regime": {"mode": "BLOCKED"},
    "rates_environment": {"mode": "BLOCKED"},
    "macro_environment": {"mode": "BLOCKED"},
    "earnings_actuals": {"mode": "BLOCKED"},
    "watchlist": [],
    "scale_path": None,
}


def _render():
    return _render_report_page(
        report=_MINIMAL_REPORT,
        chain_note="test",
        structures=[],
        generated="2026-09-20 00:00 UTC",
    )


class FullPageStructureTests(unittest.TestCase):
    def test_main_section_headings_are_unique_and_sequential(self):
        html = _render()

        # Extract the main numbered section headings: any "<h2>N. Title" tag.
        # Panels 4b/7/8 sit inline after a wrapping <div>, so they are not
        # line-initial — match the tag wherever it appears in the line.
        headings = re.findall(r'<h2>\s*(\d+b?)\.\s', html)

        # Headings must appear in exactly the expected order (which itself has
        # no repeats), and every allowed number must be present.
        self.assertEqual(
            headings,
            EXPECTED_HEADINGS,
            "Main section headings out of order or duplicated. Got %r, "
            "expected %r." % (headings, EXPECTED_HEADINGS),
        )
        self.assertEqual(
            len(headings),
            len(set(headings)),
            "A numbered section heading appears more than once.",
        )

    def test_no_literal_duplicate_number_before_following_number(self):
        # A cheap structural guard independent of the expected list: examine the
        # raw ordered-number tokens in the h2 haystack. Any number appearing
        # twice when the next distinct number should be the next integer is a
        # collision. We keep this tolerant to extra sub-numbered panels by only
        # enforcing uniqueness with the canonical list above; this test is the
        # duplicate guard.
        html = _render()
        nums = re.findall(r'<h2>\s*(\d+b?)\.', html)
        self.assertEqual(len(nums), len(set(nums)), "duplicate heading number: %r" % nums)


if __name__ == "__main__":
    unittest.main()