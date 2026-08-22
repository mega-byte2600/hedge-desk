from decimal import Decimal
import unittest

from hedge_desk.stat_evaluation import (
    ForecastObservation,
    InferencePolicy,
    REFERENCE_FORECASTS,
    evaluate_calibration,
)


class StatEvaluationTests(unittest.TestCase):
    def test_reference_calibration_is_exact_and_inference_is_withheld(self) -> None:
        result = evaluate_calibration(REFERENCE_FORECASTS)
        self.assertEqual(result.sample_size, 6)
        self.assertEqual(result.brier_score, Decimal("0.23"))
        self.assertEqual(result.mean_predicted_probability, Decimal("0.5"))
        self.assertEqual(result.observed_event_rate, Decimal("0.5"))
        self.assertEqual(result.alpha, Decimal("0.005"))
        self.assertEqual(result.confidence_level, Decimal("0.95"))
        self.assertEqual(result.inference_status, "INSUFFICIENT_SAMPLE")
        self.assertIsNone(result.p_value)
        self.assertIsNone(result.confidence_interval)

    def test_large_sample_still_requires_validated_inference_method(self) -> None:
        observations = tuple(
            ForecastObservation(f"f-{index}", Decimal("0.5"), index % 2 == 0)
            for index in range(100)
        )
        result = evaluate_calibration(observations)
        self.assertEqual(result.inference_status, "METHOD_VALIDATION_REQUIRED")
        self.assertIsNone(result.p_value)

    def test_duplicate_identity_and_invalid_probability_fail(self) -> None:
        duplicate = (REFERENCE_FORECASTS[0], REFERENCE_FORECASTS[0])
        with self.assertRaises(ValueError):
            evaluate_calibration(duplicate)
        with self.assertRaises(ValueError):
            ForecastObservation("bad", Decimal("1.01"), True)


if __name__ == "__main__":
    unittest.main()
