from datetime import datetime, timezone
import unittest

from hedge_desk.evaluation import Disposition, EvaluationLayer, EvaluationStatus
from hedge_desk.overnight import build_morning_report, evaluate_reference_projects


NOW = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)


class OvernightEvaluationTests(unittest.TestCase):
    def test_every_project_has_complete_distinct_layers(self) -> None:
        evaluations = evaluate_reference_projects()
        self.assertEqual(len(evaluations), 5)
        for evaluation in evaluations:
            self.assertEqual(tuple(layer.layer for layer in evaluation.layers), tuple(EvaluationLayer))

    def test_only_working_foundation_reaches_human_review(self) -> None:
        evaluations = evaluate_reference_projects()
        self.assertEqual(evaluations[0].disposition, Disposition.HUMAN_REVIEW)
        self.assertEqual(evaluations[0].layers[-1].status, EvaluationStatus.PENDING)
        self.assertTrue(all(item.disposition is Disposition.NO_TRADE for item in evaluations[1:]))
        self.assertEqual(evaluations[0].layers[0].metrics["days_to_expiration"], "24")
        self.assertEqual(
            evaluations[0].layers[0].metrics["planned_exit_date"], "2026-08-14"
        )
        risk_layer = evaluations[0].layers[3]
        self.assertEqual(len(risk_layer.metrics["risk_input_artifact"]), 64)
        self.assertEqual(len(risk_layer.artifact_refs), 2)

    def test_morning_report_is_explicitly_paper_and_reconciles(self) -> None:
        report = build_morning_report(NOW)
        self.assertEqual(report["environment"], "paper")
        self.assertFalse(report["live_orders_enabled"])
        self.assertEqual(report["real_money_pnl"], "0")
        self.assertEqual(report["real_trades_executed"], 0)
        self.assertEqual(report["portfolio_stress"]["scenario_count"], 5)
        self.assertEqual(report["portfolio_stress"]["real_money_pnl"], "0")
        self.assertTrue(report["chronological_replay"]["valid"])
        self.assertTrue(report["audit_chain"]["valid"])
        self.assertEqual(report["audit_chain"]["event_count"], 9)
        self.assertEqual(report["summary"], {"projects_evaluated": 5, "human_review": 1, "no_trade": 4})
        self.assertIn("Synthetic fixtures only", report["limitations"][0])

    def test_fixed_clock_produces_identical_report(self) -> None:
        self.assertEqual(build_morning_report(NOW), build_morning_report(NOW))


if __name__ == "__main__":
    unittest.main()
