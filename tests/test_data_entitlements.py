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
        "point_in_time_timestamps": True,
        "trades": True,
        "open_interest": True,
        "historical_years": 8,
        "real_time_nbbo": False,
        "commercial_use_allowed": False,
        "redistribution_allowed": False,
    }
    values.update(changes)
    return DataSubscription(**values)


class DataEntitlementTests(unittest.TestCase):
    def test_complete_internal_stack_is_ready_but_raw_commit_is_forbidden(self) -> None:
        result = evaluate_options_data_stack((subscription(),), Decimal("100"))
        self.assertTrue(result.ready_for_internal_options_research)
        self.assertFalse(result.ready_for_live_production_data)
        self.assertEqual(result.live_production_reason_codes, (
            "COMMERCIAL_USE_PERMISSION_ABSENT", "REAL_TIME_NBBO_ABSENT"
        ))
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

    def test_live_data_readiness_requires_realtime_and_commercial_permission(self) -> None:
        result = evaluate_options_data_stack((subscription(
            real_time_nbbo=True, commercial_use_allowed=True
        ),), Decimal("100"))
        self.assertTrue(result.ready_for_internal_options_research)
        self.assertTrue(result.ready_for_live_production_data)
        self.assertEqual(result.live_production_reason_codes, ())

    def test_history_timestamp_trade_and_open_interest_gaps_block_research(self) -> None:
        result = evaluate_options_data_stack((subscription(
            historical_years=4,
            point_in_time_timestamps=False,
            trades=False,
            open_interest=False,
        ),), Decimal("100"))
        self.assertEqual(result.reason_codes, (
            "MINIMUM_HISTORY_DEPTH_ABSENT",
            "OPEN_INTEREST_ABSENT",
            "OPTION_TRADES_ABSENT",
            "POINT_IN_TIME_TIMESTAMPS_ABSENT",
        ))

    def test_manifest_rejects_float_costs_and_unknown_fields(self) -> None:
        base = {
            "schema_version": "hedge-desk-data-stack-1.1.0",
            "monthly_budget": "100",
            "subscriptions": [],
        }
        invalid = dict(base, monthly_budget=100.0)
        with self.assertRaisesRegex(ValueError, "exact decimal string"):
            parse_data_stack_manifest(invalid)
        invalid = dict(base, extra=True)
        with self.assertRaisesRegex(ValueError, "schema invalid"):
            parse_data_stack_manifest(invalid)

    def test_manifest_rejects_nonfinite_money_and_nonstring_identity(self) -> None:
        import json
        from pathlib import Path

        base = json.loads(
            (Path(__file__).parents[1] / "examples" / "data-stack.synthetic.json")
            .read_text(encoding="utf-8")
        )
        for field, value, reason in (
            ("monthly_budget", "NaN", "must be finite"),
            ("monthly_cost", "Infinity", "must be finite"),
            ("source_id", 7, "identities must be strings"),
        ):
            payload = json.loads(json.dumps(base))
            if field == "monthly_budget":
                payload[field] = value
            else:
                payload["subscriptions"][0][field] = value
            with self.assertRaisesRegex(ValueError, reason):
                parse_data_stack_manifest(payload)

    def test_direct_nonfinite_decimal_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "finite Decimal"):
            evaluate_options_data_stack((subscription(),), Decimal("NaN"))
        with self.assertRaisesRegex(ValueError, "finite Decimals"):
            evaluate_options_data_stack(
                (subscription(monthly_cost=Decimal("Infinity")),), Decimal("100")
            )


if __name__ == "__main__":
    unittest.main()
