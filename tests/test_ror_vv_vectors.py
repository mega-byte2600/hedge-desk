from decimal import Decimal, localcontext
from fractions import Fraction
import json
from pathlib import Path
import unittest

from hedge_desk.risk import RISK_MODEL_ID, RISK_MODEL_VERSION, estimate_risk_of_ruin


VECTORS = Path(__file__).parent / "fixtures" / "ror_vv_vectors.json"


def independent_fraction_oracle(vector):
    equity = Decimal(vector["account_equity"])
    loss = Decimal(vector["maximum_loss"])
    probability = Fraction(Decimal(vector["win_probability"]))
    win = Fraction(Decimal(vector["expected_win"]))
    loss_fraction = Fraction(loss)
    expectancy = probability * win - (1 - probability) * loss_fraction
    units = int(equity / loss) if loss > 0 else 0
    if loss <= 0 or equity <= 0 or expectancy <= 0 or units <= 0:
        return Decimal("1")
    odds = ((1 - probability) * loss_fraction) / (probability * win)
    if odds >= 1:
        return Decimal("1")
    exact = odds ** units
    with localcontext() as context:
        context.prec = 40
        return Decimal(exact.numerator) / Decimal(exact.denominator)


class RiskOfRuinVVVectorTests(unittest.TestCase):
    def test_golden_vectors_and_independent_fraction_oracle(self) -> None:
        payload = json.loads(VECTORS.read_text(encoding="utf-8"))
        self.assertEqual(payload["model_id"], RISK_MODEL_ID)
        self.assertEqual(payload["model_version"], RISK_MODEL_VERSION)
        tolerance = Decimal(payload["relative_oracle_tolerance"])
        for vector in payload["vectors"]:
            with self.subTest(vector=vector["id"]):
                inputs = tuple(Decimal(vector[key]) for key in (
                    "account_equity", "maximum_loss", "win_probability", "expected_win"
                ))
                actual = estimate_risk_of_ruin(*inputs)
                self.assertEqual(actual, Decimal(vector["expected_output"]))
                oracle = independent_fraction_oracle(vector)
                scale = max(abs(oracle), Decimal("1E-100"))
                self.assertLessEqual(abs(actual - oracle) / scale, tolerance)

    def test_fixture_schema_and_vector_identities_are_strict(self) -> None:
        payload = json.loads(VECTORS.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema_version"], "ror-vv-vectors-1.0.0")
        identities = [item["id"] for item in payload["vectors"]]
        self.assertEqual(len(identities), len(set(identities)))


if __name__ == "__main__":
    unittest.main()
