import unittest

from hedge_desk.research_intelligence import (
    ResearchDecision,
    ResearchSource,
    SourceType,
    assess_source,
)


class ResearchIntelligenceTests(unittest.TestCase):
    def test_high_quality_reproducible_source_reaches_integration_review(self) -> None:
        source = ResearchSource(
            name="Official rates dataset",
            url="https://example.test/rates",
            source_type=SourceType.OFFICIAL,
            use_cases=("bonds", "macro", "risk"),
            signal_value=4,
            data_value=5,
            implementation_value=5,
            risk_value=5,
            credibility=5,
            reproducible=True,
            license_status="OPEN_OR_PUBLIC_REVIEWED",
        )
        result = assess_source(source)
        self.assertEqual(result.decision, ResearchDecision.INTEGRATE)
        self.assertGreaterEqual(result.score, 80)

    def test_unreviewed_license_does_not_hide_review_requirement(self) -> None:
        source = ResearchSource(
            name="Open repository",
            url="https://example.test/repo",
            source_type=SourceType.REPOSITORY,
            use_cases=("quant",),
            signal_value=3,
            data_value=2,
            implementation_value=4,
            risk_value=2,
            credibility=3,
            reproducible=True,
        )
        result = assess_source(source)
        self.assertIn("LICENSE_REVIEW_REQUIRED", result.reasons)

    def test_blocked_license_fails_closed(self) -> None:
        source = ResearchSource(
            name="Restricted source",
            url="https://example.test/restricted",
            source_type=SourceType.DATASET,
            use_cases=("earnings",),
            signal_value=5,
            data_value=5,
            implementation_value=5,
            risk_value=5,
            credibility=5,
            reproducible=True,
            license_status="BLOCKED",
        )
        result = assess_source(source)
        self.assertEqual(result.decision, ResearchDecision.REJECT)
        self.assertEqual(result.score, 0)
        self.assertEqual(result.reasons, ("LICENSE_BLOCK",))

    def test_scores_outside_contract_are_rejected(self) -> None:
        source = ResearchSource(
            name="Bad score",
            url="https://example.test/bad",
            source_type=SourceType.INDUSTRY_BLOG,
            use_cases=("sentiment",),
            signal_value=6,
            data_value=1,
            implementation_value=1,
            risk_value=1,
            credibility=1,
            reproducible=False,
        )
        with self.assertRaisesRegex(ValueError, "between 0 and 5"):
            assess_source(source)


if __name__ == "__main__":
    unittest.main()
