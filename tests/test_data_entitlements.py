from decimal import Decimal
import unittest

from hedge_desk.data.entitlements import (
    DataSubscription,
    evaluate_options_data_stack,
    parse_data_stack_manifest,
)


def subscription(**changes):
    values = {
        "source_id": "permissioned-options-feed",
        "monthly_cost": Decimal("80"),
        "entitlement_id": "internal-research-license",
        "historical_nbbo_quotes": True,
        "expired_option_contracts": True,
        "option_chain_snapshots": True,
        "corporate_actions": True,
        "redistribution_allowed": False,
    }
    values.update(changes)
    return DataSubscription(**values)


class DataEntitlementTests(unittest.TestCase):
    def test_complete_internal_stack_is_ready_but_raw_commit_is_forbidden(self) -> None:
        result = evaluate_options_data_stack((subscription(),), Decimal("100"))
        self.assertTrue(result.ready_for_internal_options_research)
        self.assertEqual(result.total_monthly_cost, Decimal("80"))
        self.assertFalse(result.raw_payload_commit_allowed)

    def test_quote_gap_and_budget_overrun_fail_closed(self) -> None:
        result = evaluate_options_data_stack(
            (subscription(monthly_cost=Decimal("101"), historical_nbbo_quotes=False),),
            Decimal("100"),
        )
        self.assertFalse(result.ready_for_internal_options_research)
        self.assertEqual(
            result.reason_codes,
            ("HISTORICAL_NBBO_QUOTES_ABSENT", "MONTHLY_DATA_BUDGET_EXCEEDED"),
        )

    def test_entitlement_and_corporate_actions_are_mandatory(self) -> None:
        result = evaluate_options_data_stack(
            (subscription(entitlement_id="", corporate_actions=False),), Decimal("100")
        )
        self.assertIn("DATA_ENTITLEMENT_UNVERIFIED", result.reason_codes)
        self.assertIn("CORPORATE_ACTIONS_ABSENT", result.reason_codes)

    def test_manifest_rejects_float_costs_and_unknown_fields(self) -> None:
        base = {
            "schema_version": "hedge-desk-data-stack-1.0.0",
            "monthly_budget": "100",
            "subscriptions": [],
        }
        invalid = dict(base, monthly_budget=100.0)
        with self.assertRaisesRegex(ValueError, "exact decimal string"):
            parse_data_stack_manifest(invalid)
        invalid = dict(base, extra=True)
        with self.assertRaisesRegex(ValueError, "schema invalid"):
            parse_data_stack_manifest(invalid)


if __name__ == "__main__":
    unittest.main()
