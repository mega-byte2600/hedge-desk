from dataclasses import replace
from datetime import date, datetime, timezone
from decimal import Decimal
import unittest

from hedge_desk.options import (
    OptionQuote,
    OptionSnapshot,
    OptionType,
    UnderlyingQuote,
    build_candidate_control_handoffs,
    scan_vertical_credit_spreads,
    validate_candidate_control_handoff,
)


NOW = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)


def quote(contract_id, strike, bid, ask):
    return OptionQuote(
        contract_id, "TEST", OptionType.PUT, Decimal(strike), date(2026, 9, 18),
        Decimal(bid), Decimal(ask), 25, 25, NOW, "licensed", 1000, 500,
    )


class CandidateHandoffTests(unittest.TestCase):
    def _scan(self, quotes):
        snapshot = OptionSnapshot(
            "hedge-desk-option-snapshot-1.0.0",
            "licensed",
            UnderlyingQuote(
                "TEST", Decimal("99.99"), Decimal("100.01"), NOW, "licensed"
            ),
            tuple(quotes),
            "a" * 64,
        )
        return scan_vertical_credit_spreads(snapshot, NOW)

    def test_handoff_binds_source_and_economics_without_probability(self) -> None:
        handoff = build_candidate_control_handoffs(self._scan((
            quote("P95", "95", "2.00", "2.10"),
            quote("P90", "90", "0.75", "0.80"),
        )))[0]
        self.assertEqual(handoff.source_artifact_sha256, "a" * 64)
        self.assertEqual(handoff.maximum_win, "118.70")
        self.assertEqual(handoff.maximum_loss, "381.30")
        self.assertEqual(handoff.next_action, "VALIDATED_RISK_INPUT_REQUIRED")
        self.assertFalse(handoff.trade_authorized)
        self.assertNotIn("probability", handoff.__dataclass_fields__)
        self.assertNotIn("risk_of_ruin", handoff.__dataclass_fields__)
        self.assertEqual(validate_candidate_control_handoff(handoff), ())
        self.assertIn(
            "HANDOFF_HASH_MISMATCH",
            validate_candidate_control_handoff(
                replace(handoff, maximum_win="999999")
            ),
        )
        self.assertIn(
            "UNTRUSTED_TRADE_AUTHORIZATION",
            validate_candidate_control_handoff(
                replace(handoff, trade_authorized=True)
            ),
        )

    def test_handoffs_are_deterministic_and_rejected_pairs_are_omitted(self) -> None:
        liquid = (
            quote("P95", "95", "2.00", "2.10"),
            quote("P90", "90", "0.75", "0.80"),
        )
        forward = build_candidate_control_handoffs(self._scan(liquid))
        reverse = build_candidate_control_handoffs(self._scan(tuple(reversed(liquid))))
        self.assertEqual(forward, reverse)
        rejected = self._scan((
            quote("P95", "95", "0.50", "0.60"),
            quote("P90", "90", "0.75", "0.80"),
        ))
        self.assertEqual(build_candidate_control_handoffs(rejected), ())


if __name__ == "__main__":
    unittest.main()
