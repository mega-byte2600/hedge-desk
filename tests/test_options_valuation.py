"""Reference cases for the option valuation, requirement, and rate/futures primitives.

Financial arithmetic needs exact deterministic reference cases, not spot checks: every
number here is hand-checkable, and money is compared as Decimal strings so a float can
never sneak into a price unnoticed.
"""

import unittest
from decimal import Decimal

from hedge_desk.options.requirements import (
    DEFAULT_POLICY,
    MarginPolicy,
    Strategy,
    cash_secured_put_collateral,
    covered_call_requirement,
    credit_spread_margin,
    requirement_for,
)
from hedge_desk.options.valuation import (
    AssignmentRisk,
    Moneyness,
    OptionType,
    SpreadRiskShape,
    credit_spread_breakeven,
    extrinsic_value,
    intrinsic_value,
    moneyness,
    short_call_breakeven,
    short_put_breakeven,
)
from hedge_desk.rates_futures import (
    CalendarSpread,
    ProcessingSpread,
    annualised_carry,
    bond_price_from_yield,
    credit_spread,
    current_yield,
    curve_shape,
    curve_slope,
    futures_basis,
    macaulay_duration,
    price_change_from_duration,
)


class IntrinsicAndExtrinsicTests(unittest.TestCase):
    def test_put_intrinsic(self):
        self.assertEqual(intrinsic_value(OptionType.PUT, Decimal("100"), Decimal("95")), Decimal("5.00"))

    def test_call_intrinsic(self):
        self.assertEqual(intrinsic_value(OptionType.CALL, Decimal("100"), Decimal("108")), Decimal("8.00"))

    def test_otm_is_worthless_not_negative(self):
        self.assertEqual(intrinsic_value(OptionType.PUT, Decimal("100"), Decimal("105")), Decimal("0.00"))
        self.assertEqual(intrinsic_value(OptionType.CALL, Decimal("100"), Decimal("95")), Decimal("0.00"))

    def test_extrinsic_clamps_at_zero_on_a_crossed_quote(self):
        # premium below intrinsic is a data error, not negative time value
        self.assertEqual(extrinsic_value(Decimal("4.00"), Decimal("5.00")), Decimal("0.00"))

    def test_extrinsic_is_premium_less_intrinsic(self):
        self.assertEqual(extrinsic_value(Decimal("7.50"), Decimal("5.00")), Decimal("2.50"))

    def test_moneyness_bands(self):
        self.assertEqual(moneyness(OptionType.PUT, Decimal("100"), Decimal("95")), Moneyness.IN_THE_MONEY)
        self.assertEqual(moneyness(OptionType.PUT, Decimal("100"), Decimal("105")), Moneyness.OUT_OF_THE_MONEY)
        self.assertEqual(moneyness(OptionType.CALL, Decimal("100"), Decimal("100.00")), Moneyness.AT_THE_MONEY)

    def test_float_input_is_not_accepted_silently(self):
        # 0.1 + 0.2 in floats is a defect in a price; Decimal(value) on a float would
        # import that error, so the module converts via str.
        self.assertEqual(intrinsic_value(OptionType.PUT, Decimal("100"), Decimal("100.1")), Decimal("0.00"))


class BreakevenTests(unittest.TestCase):
    def test_short_put_breakeven(self):
        self.assertEqual(short_put_breakeven(Decimal("100"), Decimal("2.60")), Decimal("97.40"))

    def test_short_call_breakeven(self):
        self.assertEqual(short_call_breakeven(Decimal("450"), Decimal("6.25")), Decimal("456.25"))

    def test_credit_spread_breakevens_by_side(self):
        self.assertEqual(credit_spread_breakeven(Decimal("100"), Decimal("2.60"), OptionType.PUT), Decimal("97.40"))
        self.assertEqual(credit_spread_breakeven(Decimal("450"), Decimal("6.25"), OptionType.CALL), Decimal("456.25"))


class SpreadRiskShapeTests(unittest.TestCase):
    def test_defined_risk_reference_case(self):
        # $5 wide, $2.60 credit, one contract
        shape = SpreadRiskShape(net_credit=Decimal("2.60"), width=Decimal("5"), contracts=1)
        self.assertEqual(shape.max_profit, Decimal("260.00"))
        self.assertEqual(shape.max_loss, Decimal("240.00"))
        self.assertEqual(shape.risk_reward, Decimal("1.0833"))

    def test_scales_with_contracts(self):
        shape = SpreadRiskShape(net_credit=Decimal("2.60"), width=Decimal("5"), contracts=10)
        self.assertEqual(shape.max_profit, Decimal("2600.00"))
        self.assertEqual(shape.max_loss, Decimal("2400.00"))

    def test_invalid_structures_are_rejected(self):
        with self.assertRaises(ValueError):
            SpreadRiskShape(net_credit=Decimal("2.60"), width=Decimal("5"), contracts=0)
        with self.assertRaises(ValueError):
            SpreadRiskShape(net_credit=Decimal("-1"), width=Decimal("5"), contracts=1)
        with self.assertRaises(ValueError):
            SpreadRiskShape(net_credit=Decimal("2.60"), width=Decimal("0"), contracts=1)


class AssignmentRiskTests(unittest.TestCase):
    def test_itm_short_put_is_flagged(self):
        risk = AssignmentRisk(OptionType.PUT, Decimal("100"), Decimal("95"), days_to_expiry=3)
        self.assertTrue(risk.assignment_likely)
        self.assertIn("SHORT_OPTION_IN_THE_MONEY", risk.reason_codes())

    def test_otm_short_option_is_clean(self):
        risk = AssignmentRisk(OptionType.PUT, Decimal("100"), Decimal("105"), days_to_expiry=3)
        self.assertFalse(risk.assignment_likely)
        self.assertEqual(risk.reason_codes(), ["NO_ASSIGNMENT_FLAG"])

    def test_pin_risk_near_the_strike_at_the_end(self):
        risk = AssignmentRisk(OptionType.CALL, Decimal("450"), Decimal("450.10"), days_to_expiry=1)
        self.assertTrue(risk.pin_risk)
        self.assertIn("PIN_RISK_NEAR_STRIKE", risk.reason_codes())

    def test_pin_risk_needs_imminence(self):
        risk = AssignmentRisk(OptionType.CALL, Decimal("450"), Decimal("450.10"), days_to_expiry=5)
        self.assertFalse(risk.pin_risk)

    def test_dividend_assignment_reason_code(self):
        risk = AssignmentRisk(OptionType.CALL, Decimal("450"), Decimal("460"), days_to_expiry=2, dividend_pending=True)
        self.assertIn("DIVIDEND_ASSIGNMENT_RISK", risk.reason_codes())

    def test_negative_days_rejected(self):
        with self.assertRaises(ValueError):
            _ = AssignmentRisk(OptionType.PUT, Decimal("100"), Decimal("95"), days_to_expiry=-1).assignment_likely


class RequirementTests(unittest.TestCase):
    def test_cash_secured_put_holds_strike_less_credit(self):
        req = cash_secured_put_collateral(Decimal("100"), Decimal("2.60"))
        self.assertEqual(req.requirement, Decimal("9740.00"))
        self.assertEqual(req.strategy, Strategy.CASH_SECURED_PUT)
        self.assertEqual(req.policy_version, DEFAULT_POLICY.version)
        self.assertIn("ASSIGNMENT_MUST_BE_FUNDABLE", req.reason_codes)

    def test_cash_secured_put_without_credit_offset(self):
        policy = MarginPolicy(version="test-no-offset", put_credit_offsets_collateral=False)
        req = cash_secured_put_collateral(Decimal("100"), Decimal("2.60"), policy=policy)
        self.assertEqual(req.requirement, Decimal("10000.00"))

    def test_covered_call_is_the_shares(self):
        req = covered_call_requirement(Decimal("450"))
        self.assertEqual(req.requirement, Decimal("45000.00"))
        self.assertIn("SHARES_ARE_COLLATERAL", req.reason_codes)

    def test_credit_spread_margin_equals_max_loss(self):
        req = credit_spread_margin(Decimal("5"), Decimal("2.60"))
        self.assertEqual(req.requirement, Decimal("240.00"))
        self.assertIn("MARGIN_EQUALS_MAX_LOSS", req.reason_codes)

    def test_a_credit_at_or_above_the_width_is_rejected(self):
        with self.assertRaises(ValueError):
            credit_spread_margin(Decimal("5"), Decimal("5"))

    def test_requirement_is_versioned(self):
        policy = MarginPolicy(version="regt-2026a", maintenance_factor=Decimal("1.25"))
        req = credit_spread_margin(Decimal("5"), Decimal("2.60"), policy=policy)
        self.assertEqual(req.policy_version, "regt-2026a")
        self.assertEqual(req.requirement, Decimal("300.00"))

    def test_an_unversioned_policy_is_refused(self):
        with self.assertRaises(ValueError):
            MarginPolicy(version="")

    def test_requirement_for_dispatches(self):
        self.assertEqual(requirement_for("CREDIT_SPREAD", width=Decimal("5"), net_credit=Decimal("2.60")).requirement,
                         Decimal("240.00"))
        self.assertEqual(requirement_for("COVERED_CALL", share_price=Decimal("100")).requirement,
                         Decimal("10000.00"))


class BondTests(unittest.TestCase):
    def test_par_bond_prices_at_face(self):
        price = bond_price_from_yield(Decimal("1000"), Decimal("0.05"), Decimal("0.05"), Decimal("2"))
        self.assertEqual(price, Decimal("1000.00"))

    def test_price_falls_when_yield_rises(self):
        low = bond_price_from_yield(Decimal("1000"), Decimal("0.05"), Decimal("0.04"), Decimal("10"))
        high = bond_price_from_yield(Decimal("1000"), Decimal("0.05"), Decimal("0.06"), Decimal("10"))
        self.assertGreater(low, high)
        self.assertGreater(low, Decimal("1000.00"))
        self.assertLess(high, Decimal("1000.00"))

    def test_current_yield_reference_case(self):
        # $50 annual coupon on a $900 price
        self.assertEqual(current_yield(Decimal("1000"), Decimal("0.05"), Decimal("900")), Decimal("0.055556"))

    def test_duration_of_a_two_year_par_bond(self):
        d = macaulay_duration(Decimal("1000"), Decimal("0.05"), Decimal("0.05"), Decimal("2"))
        self.assertEqual(d, Decimal("1.928012"))

    def test_duration_rises_with_maturity(self):
        short = macaulay_duration(Decimal("1000"), Decimal("0.05"), Decimal("0.05"), Decimal("2"))
        long = macaulay_duration(Decimal("1000"), Decimal("0.05"), Decimal("0.05"), Decimal("30"))
        self.assertGreater(long, short)

    def test_price_change_from_duration_signs(self):
        # a 25bp rise in yield lowers the price
        self.assertEqual(price_change_from_duration(Decimal("4.5"), Decimal("1000"), Decimal("0.0025")),
                         Decimal("-11.25"))
        self.assertEqual(price_change_from_duration(Decimal("4.5"), Decimal("1000"), Decimal("-0.0025")),
                         Decimal("11.25"))

    def test_credit_spread(self):
        self.assertEqual(credit_spread(Decimal("0.0625"), Decimal("0.045")), Decimal("0.017500"))

    def test_zero_yield_does_not_divide_by_zero(self):
        price = bond_price_from_yield(Decimal("1000"), Decimal("0.05"), Decimal("0"), Decimal("2"))
        self.assertEqual(price, Decimal("1100.00"))


class FuturesTests(unittest.TestCase):
    def test_basis_is_cash_minus_futures(self):
        self.assertEqual(futures_basis(Decimal("450"), Decimal("455")), Decimal("-5.00"))
        self.assertEqual(futures_basis(Decimal("455"), Decimal("450")), Decimal("5.00"))

    def test_annualised_carry(self):
        carry = annualised_carry(Decimal("-5"), Decimal("450"), 90)
        self.assertEqual(carry, Decimal("-0.045062"))

    def test_carry_rejects_nonsense_tenor(self):
        with self.assertRaises(ValueError):
            annualised_carry(Decimal("-5"), Decimal("450"), 0)

    def test_calendar_spread_structure(self):
        self.assertEqual(CalendarSpread("ES", Decimal("4500"), Decimal("4520")).structure, "CONTANGO")
        self.assertEqual(CalendarSpread("ES", Decimal("4520"), Decimal("4500")).structure, "BACKWARDATION")
        self.assertEqual(CalendarSpread("ES", Decimal("4500"), Decimal("4500")).structure, "FLAT")

    def test_calendar_spread_states_it_is_not_a_forecast(self):
        self.assertIn("SPREAD_IS_NOT_A_FORECAST",
                      CalendarSpread("ES", Decimal("4500"), Decimal("4520")).reason_codes())

    def test_processing_spread_gross_margin(self):
        spread = ProcessingSpread("crack", Decimal("30"), (Decimal("12"), Decimal("9")))
        self.assertEqual(spread.gross_margin, Decimal("9.00"))
        self.assertTrue(spread.is_positive)
        self.assertIn("PROCESSING_MARGIN_POSITIVE", spread.reason_codes())

    def test_processing_spread_negative_margin(self):
        spread = ProcessingSpread("crack", Decimal("18"), (Decimal("12"), Decimal("9")))
        self.assertEqual(spread.gross_margin, Decimal("-3.00"))
        self.assertFalse(spread.is_positive)

    def test_curve_slope_and_shape(self):
        self.assertEqual(curve_slope([(2, Decimal("0.042")), (10, Decimal("0.045"))]), Decimal("0.000375"))
        self.assertEqual(curve_shape(Decimal("0.000375")), "UPWARD_SLOPING")
        self.assertEqual(curve_shape(Decimal("-0.0004")), "INVERTED")

    def test_curve_slope_needs_two_points(self):
        with self.assertRaises(ValueError):
            curve_slope([(2, Decimal("0.042"))])


if __name__ == "__main__":
    unittest.main()
