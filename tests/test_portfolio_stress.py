from decimal import Decimal
import unittest

from hedge_desk.portfolio_stress import (
    build_portfolio_stress_report,
    build_stress_circuit_breaker,
)


class PortfolioStressTests(unittest.TestCase):
    def test_combined_capital_path_is_exact_and_cost_inclusive(self) -> None:
        report = build_portfolio_stress_report()
        self.assertEqual(report["scenario_count"], 5)
        self.assertEqual(report["real_money_pnl"], "0")
        self.assertEqual(len(report["fixture_sha256"]), 64)
        self.assertEqual(len(report["stress_report_sha256"]), 64)
        first = report["scenarios"][0]
        self.assertEqual(first["combined_net_pnl"], "98.40")
        self.assertEqual(first["ending_capital"], "100098.40")
        crowded = report["scenarios"][-1]
        self.assertEqual(crowded["combined_net_pnl"], "-4655.60")
        self.assertEqual(crowded["disposition"], "FREEZE_NEW_RISK")
        self.assertIn("DRAWDOWN_LIMIT_BREACHED", crowded["reason_codes"])
        self.assertIn("event-futures-desk", crowded["net_pnl_by_project"])

    def test_results_are_reproducible_and_not_statistical_inference(self) -> None:
        self.assertEqual(build_portfolio_stress_report(), build_portfolio_stress_report())
        self.assertEqual(
            build_portfolio_stress_report()["inference_status"],
            "INSUFFICIENT_SYNTHETIC_SAMPLE",
        )

    def test_invalid_capital_policy_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            build_portfolio_stress_report(Decimal("0"))
        with self.assertRaises(ValueError):
            build_portfolio_stress_report(maximum_drawdown_fraction=Decimal("1"))
        with self.assertRaisesRegex(ValueError, "finite"):
            build_portfolio_stress_report(starting_capital=Decimal("Infinity"))

    def test_stress_artifact_drives_back_office_circuit_breaker(self) -> None:
        report = build_portfolio_stress_report()
        breaker = build_stress_circuit_breaker(report)
        self.assertTrue(breaker.new_risk_frozen)
        self.assertEqual(
            breaker.reason_codes, ("PORTFOLIO_DRAWDOWN_CIRCUIT_BREAKER",)
        )
        report["descriptive_metrics"]["maximum_drawdown"] = "0"
        with self.assertRaisesRegex(ValueError, "integrity"):
            build_stress_circuit_breaker(report)


if __name__ == "__main__":
    unittest.main()
