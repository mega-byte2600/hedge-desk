from decimal import Decimal
import unittest

from hedge_desk.metrics import evaluate_pnl_series


class DescriptiveMetricsTests(unittest.TestCase):
    def test_exact_reference_metrics(self) -> None:
        metrics = evaluate_pnl_series(
            (
                Decimal("77.40"), Decimal("-2.60"), Decimal("-132.60"),
                Decimal("-382.60"), Decimal("-407.60"),
            )
        )
        self.assertEqual(metrics.sample_size, 5)
        self.assertEqual(metrics.total_pnl, Decimal("-848.00"))
        self.assertEqual(metrics.mean_pnl, Decimal("-169.60"))
        self.assertEqual(metrics.median_pnl, Decimal("-132.60"))
        self.assertEqual(metrics.win_rate, Decimal("0.2"))
        self.assertEqual(metrics.maximum_drawdown, Decimal("925.40"))
        self.assertEqual(metrics.expected_shortfall, Decimal("-407.60"))
        self.assertEqual(metrics.inference_status, "INSUFFICIENT_SYNTHETIC_SAMPLE")

    def test_empty_series_and_invalid_confidence_fail(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_pnl_series(())
        with self.assertRaises(ValueError):
            evaluate_pnl_series((Decimal("1"),), Decimal("1"))
        for value in (Decimal("NaN"), Decimal("Infinity")):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "finite"):
                evaluate_pnl_series((value,))


if __name__ == "__main__":
    unittest.main()
