import unittest

from hedge_desk.burry_sensitivity import calculate_depreciation_sensitivity


class BurrySensitivityTests(unittest.TestCase):
    def inputs(self):
        return {
            "asset_cost_millions": "17000",
            "reported_life_years": "6",
            "scenario_life_years": "3",
            "service_fraction_pct": "100",
            "tax_rate_pct": "0",
            "reported_net_income_millions": "88100",
            "diluted_shares_millions": "6240",
            "share_price": "480",
        }

    def test_one_cohort_six_to_three_year_sensitivity_is_reproducible(self):
        result = calculate_depreciation_sensitivity(self.inputs())
        self.assertEqual(result["additional_annual_depreciation_millions"], "2833.33")
        self.assertEqual(result["after_tax_earnings_delta_millions"], "2833.33")
        self.assertEqual(result["scenario_net_income_millions"], "85266.67")
        self.assertEqual(result["trade_authorized"], False)
        self.assertEqual(result["calculation_label"], "one-cohort straight-line depreciation sensitivity")

    def test_rejects_economic_life_not_shorter_than_reported_life(self):
        inputs = self.inputs()
        inputs["scenario_life_years"] = "6"
        with self.assertRaisesRegex(ValueError, "shorter"):
            calculate_depreciation_sensitivity(inputs)

    def test_rejects_nonfinite_and_out_of_range_inputs(self):
        inputs = self.inputs()
        inputs["tax_rate_pct"] = "NaN"
        with self.assertRaisesRegex(ValueError, "permitted range"):
            calculate_depreciation_sensitivity(inputs)
        inputs["tax_rate_pct"] = "101"
        with self.assertRaisesRegex(ValueError, "permitted range"):
            calculate_depreciation_sensitivity(inputs)


if __name__ == "__main__":
    unittest.main()
