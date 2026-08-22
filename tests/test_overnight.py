from datetime import datetime, timezone
import unittest

from hedge_desk.evaluation import Disposition, EvaluationLayer, EvaluationStatus
from hedge_desk.overnight import build_morning_report, evaluate_reference_projects


NOW = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)


class OvernightEvaluationTests(unittest.TestCase):
    def test_every_project_has_complete_distinct_layers(self) -> None:
        evaluations = evaluate_reference_projects()
        self.assertEqual(len(evaluations), 6)
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
        self.assertEqual(
            evaluations[0].layers[0].metrics["event_calendar_complete_through"],
            "2026-08-21",
        )
        self.assertEqual(
            evaluations[0].layers[0].metrics["admissible_vertical_pairs"], "1"
        )
        self.assertEqual(
            evaluations[0].layers[2].metrics["candidate_handoff_count"], "1"
        )
        self.assertEqual(
            evaluations[0].layers[2].metrics["handoff_next_action"],
            "VALIDATED_RISK_INPUT_REQUIRED",
        )
        self.assertEqual(
            evaluations[0].layers[2].metrics["handoff_trade_authorized"], "false"
        )
        risk_layer = evaluations[0].layers[3]
        self.assertEqual(len(risk_layer.metrics["risk_input_artifact"]), 64)
        self.assertEqual(
            risk_layer.metrics["risk_source_artifact"],
            evaluations[0].layers[2].metrics["handoff_calculation_artifact"],
        )
        self.assertEqual(len(risk_layer.artifact_refs), 2)
        model_lab = evaluations[4]
        self.assertEqual(model_lab.project_id, "open-quant-ai-model-lab")
        self.assertEqual(
            model_lab.layers[2].metrics["authoritative_risk_input"], "false"
        )
        self.assertEqual(model_lab.layers[3].status, EvaluationStatus.BLOCKED)
        earnings = evaluations[1]
        self.assertEqual(earnings.project_id, "earnings-event-desk")
        self.assertEqual(earnings.layers[0].metrics["surprise_alignment"], "BOTH_POSITIVE")
        self.assertEqual(
            earnings.layers[2].metrics["directional_trade_authorized"], "false"
        )
        arbitrage = evaluations[2]
        self.assertEqual(arbitrage.project_id, "arbitrage-observer")
        self.assertEqual(arbitrage.layers[2].metrics["trade_authorized"], "false")
        self.assertEqual(arbitrage.layers[3].status, EvaluationStatus.BLOCKED)
        dividend = evaluations[3]
        self.assertEqual(dividend.project_id, "dividend-opportunity-desk")
        self.assertEqual(
            dividend.layers[2].metrics["long_call_cash_dividend_entitlement"], "0"
        )
        self.assertEqual(dividend.layers[2].metrics["trade_authorized"], "false")
        futures = evaluations[5]
        self.assertEqual(futures.project_id, "event-futures-desk")
        self.assertEqual(futures.layers[2].metrics["trade_authorized"], "false")
        self.assertEqual(futures.layers[4].status, EvaluationStatus.BLOCKED)

    def test_morning_report_is_explicitly_paper_and_reconciles(self) -> None:
        report = build_morning_report(NOW)
        self.assertEqual(report["environment"], "paper")
        self.assertFalse(report["live_orders_enabled"])
        self.assertEqual(report["real_money_pnl"], "0")
        self.assertEqual(report["real_trades_executed"], 0)
        self.assertEqual(report["code_commit"], "LOCAL_UNSPECIFIED")
        self.assertEqual(report["portfolio_stress"]["scenario_count"], 5)
        self.assertEqual(report["portfolio_stress"]["real_money_pnl"], "0")
        self.assertEqual(len(report["data_batch"]["required_sources"]), 10)
        self.assertIn(
            "synthetic-futures-event", report["data_batch"]["required_sources"]
        )
        self.assertTrue(report["chronological_replay"]["valid"])
        self.assertTrue(report["audit_chain"]["valid"])
        self.assertEqual(report["audit_chain"]["event_count"], 7)
        self.assertEqual(
            report["chronological_replay"]["events"][-1]["kind"], "HUMAN_PENDING"
        )
        self.assertEqual(report["summary"], {"projects_evaluated": 6, "human_review": 1, "no_trade": 5})
        self.assertIn("Synthetic fixtures only", report["limitations"][0])

    def test_fixed_clock_produces_identical_report(self) -> None:
        self.assertEqual(build_morning_report(NOW), build_morning_report(NOW))


if __name__ == "__main__":
    unittest.main()
