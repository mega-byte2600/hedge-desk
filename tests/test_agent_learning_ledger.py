import unittest

from hedge_desk.agents.learning_ledger import (
    MistakeType,
    OutcomeGrade,
    AgentPrediction,
    PaperOutcome,
    agent_score,
    grade_prediction,
)


class AgentLearningLedgerTests(unittest.TestCase):
    def test_correct_paper_outcome_improves_score_without_trade_authority(self):
        prediction = AgentPrediction(
            prediction_id="p1",
            agent_name="quantdesk",
            candidate_id="SPY-001",
            expected_direction="premium_decay",
            expected_premium_capture=100.0,
            expected_max_loss=300.0,
            thesis="IV is rich against realized volatility.",
            invalidation="Spread widens or realized volatility jumps.",
            source_hashes=["abc"],
        )
        outcome = PaperOutcome(
            prediction_id="p1",
            realized_premium_capture=125.0,
            realized_drawdown=80.0,
            thesis_state="strengthening",
        )
        record = grade_prediction(prediction, outcome)
        self.assertEqual(record.grade, OutcomeGrade.CORRECT)
        self.assertEqual(record.mistake_type, MistakeType.NONE)
        self.assertFalse(record.trade_authorized)
        self.assertIn("NO_AGENT_ORDER_PLACEMENT", record.safety_invariants)

    def test_rule_block_missed_is_penalized(self):
        prediction = AgentPrediction(
            prediction_id="p2",
            agent_name="earnings-agent",
            candidate_id="AAPL-002",
            expected_direction="premium_decay",
            expected_premium_capture=75.0,
            expected_max_loss=250.0,
            thesis="Earnings vol premium should compress.",
            invalidation="Account or DTE gate blocks.",
            source_hashes=["def"],
        )
        outcome = PaperOutcome(
            prediction_id="p2",
            realized_premium_capture=0.0,
            realized_drawdown=0.0,
            thesis_state="unresolved",
            rule_blocks_triggered=["OPTIONS_LEVEL_TOO_LOW"],
        )
        record = grade_prediction(prediction, outcome)
        self.assertEqual(record.grade, OutcomeGrade.WRONG)
        self.assertEqual(record.mistake_type, MistakeType.RULE_BLOCK_MISSED)
        self.assertLess(record.score_delta, 0)

    def test_agent_score_aggregates_records(self):
        prediction = AgentPrediction("p3", "dividend-agent", "KO-001", "premium_decay", 50.0, 200.0, "thesis", "invalid", [])
        good = grade_prediction(prediction, PaperOutcome("p3", 60.0, 30.0, "intact"))
        bad = grade_prediction(prediction, PaperOutcome("p3", 0.0, 0.0, "unresolved", ["SOURCE_STALE"]))
        self.assertEqual(agent_score([good, bad])["dividend-agent"], -1.0)


if __name__ == "__main__":
    unittest.main()
