from decimal import Decimal
import unittest

from hedge_desk.wargames import build_war_game_report, run_premium_war_games


class PremiumWarGameTests(unittest.TestCase):
    def test_all_declared_scenarios_are_reported(self) -> None:
        report = build_war_game_report()
        self.assertTrue(report["all_declared_scenarios_included"])
        self.assertEqual(report["summary"]["scenario_count"], 5)
        self.assertEqual(report["summary"]["profitable_scenarios"], 1)
        self.assertEqual(report["summary"]["losing_scenarios"], 4)

    def test_reference_scenario_pnls_are_exact(self) -> None:
        results = {result.scenario_id: result for result in run_premium_war_games()}
        self.assertEqual(results["favorable-decay"].net_pnl, Decimal("77.40"))
        self.assertEqual(results["no-edge-after-costs"].net_pnl, Decimal("-2.60"))
        self.assertEqual(results["iv-shock"].net_pnl, Decimal("-132.60"))
        self.assertEqual(results["gap-through-width"].net_pnl, Decimal("-382.60"))
        self.assertEqual(results["assignment-operations"].net_pnl, Decimal("-407.60"))

    def test_report_does_not_mislabel_synthetic_results_as_money_made(self) -> None:
        report = build_war_game_report()
        self.assertEqual(report["environment"], "paper")
        self.assertEqual(report["source"], "synthetic_fixture")
        self.assertIn("not historical or live results", report["limitations"][0])


if __name__ == "__main__":
    unittest.main()
