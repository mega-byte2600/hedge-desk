from dataclasses import replace
from datetime import datetime, timezone
import unittest

from hedge_desk.short_research import (
    ShortResearchCase,
    ShortResearchStatus,
    SourceReference,
    review_short_research,
)
from hedge_desk.live_desk_data import build_desk_projects


class ShortResearchTests(unittest.TestCase):
    def setUp(self):
        now = datetime(2026, 11, 16, 12, tzinfo=timezone.utc)
        self.case = ShortResearchCase(
            symbol="TEST",
            as_of=now,
            bear_thesis="Filing evidence points to worsening cash conversion.",
            sources=(
                SourceReference("SEC_FILING", "10-Q", "https://www.sec.gov/Archives/edgar/data/1/test.htm", now),
                SourceReference("SHORT_INTEREST_REPORT", "Exchange position report, settlement 2026-10-30", "https://www.nasdaq.com/market-activity/stocks/test/short-interest", now),
                SourceReference("INDEPENDENT_SOURCE", "Regulator notice", "https://www.finra.org/rules-guidance/notices", now),
            ),
            catalyst_and_timing="Earnings release expected next quarter.",
            counter_thesis="Management may recover margins after restructuring.",
            valuation_basis="Compare normalized free cash flow with peers.",
            liquidity_and_volatility="Use current sourced volume and volatility observations.",
            borrow_status="UNKNOWN",
            invalidation_conditions="Thesis invalid if margins and cash conversion recover.",
            conflicts_disclosed=True,
        )

    def test_complete_case_can_only_advance_to_independent_review(self):
        review = review_short_research(self.case)
        self.assertEqual(review.status, ShortResearchStatus.READY_FOR_INDEPENDENT_REVIEW)
        self.assertFalse(review.borrow_confirmed)
        self.assertFalse(review.trade_authorized)

    def test_missing_sec_primary_evidence_stays_incomplete(self):
        case = replace(self.case, sources=(self.case.sources[1],))
        review = review_short_research(case)
        self.assertEqual(review.status, ShortResearchStatus.INCOMPLETE_RESEARCH)
        self.assertIn("SEC_FILING_EVIDENCE_MISSING", review.reason_codes)

    def test_short_sale_volume_is_not_accepted_as_short_interest_evidence(self):
        sources = tuple(s for s in self.case.sources if s.source_type != "SHORT_INTEREST_REPORT") + (
            replace(self.case.sources[0], source_type="DAILY_SHORT_SALE_VOLUME", label="FINRA daily short-sale volume"),
        )
        case = replace(self.case, sources=sources)
        review = review_short_research(case)
        self.assertEqual(review.status, ShortResearchStatus.INCOMPLETE_RESEARCH)
        self.assertIn("DATED_SHORT_INTEREST_REPORT_MISSING", review.reason_codes)
        self.assertFalse(review.trade_authorized)

    def test_unpublished_or_non_https_sources_fail_closed(self):
        invalid = replace(self.case.sources[0], url="http://example.com", published_at=datetime(2026, 11, 16))
        case = replace(self.case, sources=(invalid, self.case.sources[1]))
        review = review_short_research(case)
        self.assertEqual(review.status, ShortResearchStatus.INCOMPLETE_RESEARCH)
        self.assertIn("SOURCE_REFERENCE_INVALID", review.reason_codes)

    def test_future_source_fails_point_in_time_gate(self):
        future = replace(self.case.sources[0], published_at=datetime(2026, 11, 17, tzinfo=timezone.utc))
        case = replace(self.case, sources=(future,) + self.case.sources[1:])
        self.assertIn("SOURCE_AFTER_RESEARCH_AS_OF", review_short_research(case).reason_codes)

    def test_broker_confirmed_borrow_requires_broker_source(self):
        review = review_short_research(replace(self.case, borrow_status="BROKER_CONFIRMED"))
        self.assertIn("BROKER_BORROW_EVIDENCE_MISSING", review.reason_codes)

    def test_unreviewed_conflicts_block_human_review_stage(self):
        review = review_short_research(replace(self.case, conflicts_disclosed=False))
        self.assertIn("CONFLICTS_NOT_REVIEWED", review.reason_codes)
        self.assertFalse(review.trade_authorized)

    def test_desk5_does_not_substitute_a_default_symbol_universe(self):
        requested = []

        def fake_fetcher(symbols):
            requested.extend(symbols)
            return {}, [{"symbol": symbol, "reason": "fixture"} for symbol in symbols]

        projects = build_desk_projects(fake_fetcher)
        desk5 = next(p for p in projects if p["project_id"] == "open-quant-ai-model-lab")
        self.assertEqual(desk5["live_data"], {})
        self.assertEqual(desk5["data_status"], "data_unavailable")
        self.assertIn("approved watchlist symbols required", desk5["reason"])


if __name__ == "__main__":
    unittest.main()
