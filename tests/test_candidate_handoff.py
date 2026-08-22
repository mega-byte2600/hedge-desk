from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import unittest

from hedge_desk.options import (
    OptionQuote,
    OptionSnapshot,
    OptionType,
    UnderlyingQuote,
    MarketSessionEvidence,
    build_candidate_control_handoffs,
    evaluate_market_session,
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
    def _session(self):
        return evaluate_market_session(
            MarketSessionEvidence(
                "OPRA", NOW - timedelta(hours=1),
                NOW + timedelta(hours=1),
                NOW - timedelta(hours=2), "b" * 64,
            ),
            NOW,
            900,
        )

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
        )), self._session())[0]
        self.assertEqual(handoff.source_artifact_sha256, "a" * 64)
        self.assertEqual(handoff.maximum_win, "118.70")
        self.assertEqual(handoff.maximum_loss, "381.30")
        self.assertEqual(handoff.next_action, "VALIDATED_RISK_INPUT_REQUIRED")
        self.assertFalse(handoff.trade_authorized)
        self.assertEqual(handoff.market_calendar_sha256, "b" * 64)
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
        forward = build_candidate_control_handoffs(self._scan(liquid), self._session())
        reverse = build_candidate_control_handoffs(
            self._scan(tuple(reversed(liquid))), self._session()
        )
        self.assertEqual(forward, reverse)
        rejected = self._scan((
            quote("P95", "95", "0.50", "0.60"),
            quote("P90", "90", "0.75", "0.80"),
        ))
        self.assertEqual(build_candidate_control_handoffs(rejected, self._session()), ())

    def test_blocked_session_withholds_candidate_handoff(self) -> None:
        scan = self._scan((
            quote("P95", "95", "2.00", "2.10"),
            quote("P90", "90", "0.75", "0.80"),
        ))
        blocked = evaluate_market_session(
            MarketSessionEvidence(
                "OPRA", NOW - timedelta(hours=2), NOW - timedelta(hours=1),
                NOW - timedelta(hours=3), "b" * 64,
            ),
            NOW,
            900,
        )
        self.assertFalse(blocked.admissible)
        self.assertEqual(build_candidate_control_handoffs(scan, blocked), ())

    def test_calendar_lineage_tamper_invalidates_handoff(self) -> None:
        handoff = build_candidate_control_handoffs(self._scan((
            quote("P95", "95", "2.00", "2.10"),
            quote("P90", "90", "0.75", "0.80"),
        )), self._session())[0]
        reasons = validate_candidate_control_handoff(
            replace(handoff, market_calendar_sha256="c" * 64)
        )
        self.assertIn("HANDOFF_HASH_MISMATCH", reasons)


if __name__ == "__main__":
    unittest.main()
