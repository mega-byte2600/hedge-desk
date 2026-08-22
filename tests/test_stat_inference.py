from decimal import Decimal
import unittest

from hedge_desk.stat_inference import (
    DirectionalInferencePolicy,
    evaluate_directional_hits,
)


class DirectionalInferenceTests(unittest.TestCase):
    def test_insufficient_sample_withholds_inference(self) -> None:
        result = evaluate_directional_hits((True, False, True))
        self.assertEqual(result.inference_status, "INSUFFICIENT_SAMPLE")
        self.assertIsNone(result.one_sided_exact_p_value)
        self.assertIsNone(result.wilson_confidence_interval)
        self.assertFalse(result.trade_authorized)

    def test_exact_binomial_reference_vector_and_wilson_interval(self) -> None:
        # Independently reproducible exact vector: P[X >= 70], X~Bin(100, 0.5).
        result = evaluate_directional_hits((True,) * 70 + (False,) * 30)
        self.assertEqual(
            result.one_sided_exact_p_value,
            Decimal("0.000039250698227968348114678788334695237907144096119565"),
        )
        self.assertTrue(result.statistically_significant)
        self.assertEqual(result.alpha, Decimal("0.005"))
        self.assertEqual(result.confidence_level, Decimal("0.95"))
        lower, upper = result.wilson_confidence_interval or (Decimal(0), Decimal(0))
        self.assertLess(lower, Decimal("0.7"))
        self.assertGreater(upper, Decimal("0.7"))
        self.assertFalse(result.trade_authorized)

    def test_threshold_is_inclusive_and_not_a_trade_gate(self) -> None:
        outcomes = (True,) * 70 + (False,) * 30
        baseline = evaluate_directional_hits(outcomes)
        policy = DirectionalInferencePolicy(
            alpha=baseline.one_sided_exact_p_value or Decimal("0.005")
        )
        result = evaluate_directional_hits(outcomes, policy)
        self.assertEqual(result.one_sided_exact_p_value, policy.alpha)
        self.assertTrue(result.statistically_significant)
        self.assertFalse(result.trade_authorized)

    def test_malformed_policy_and_outcomes_fail_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "95% only"):
            DirectionalInferencePolicy(confidence_level=Decimal("0.99"))
        with self.assertRaisesRegex(ValueError, "booleans"):
            evaluate_directional_hits((True, 1) * 50)
        with self.assertRaisesRegex(ValueError, "finite"):
            DirectionalInferencePolicy(alpha=Decimal("NaN"))
        with self.assertRaisesRegex(ValueError, "positive integer"):
            DirectionalInferencePolicy(minimum_sample_size=True)


if __name__ == "__main__":
    unittest.main()
