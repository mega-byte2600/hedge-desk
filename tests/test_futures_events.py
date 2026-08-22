from dataclasses import replace
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import unittest

from hedge_desk.futures_events import (
    FuturesContractSnapshot,
    FuturesEventCandidate,
    FuturesEventInputs,
    PhysicalEventType,
    evaluate_futures_event,
    evaluate_futures_universe,
)


NOW = datetime(2026, 8, 21, 20, 0, tzinfo=timezone.utc)


def contract():
    return FuturesContractSnapshot("OJ-FUT", 5000, Decimal("5000"), False, True, "a" * 64)


def event():
    return FuturesEventInputs(
        "freeze-1", PhysicalEventType.EXTREME_WEATHER,
        NOW - timedelta(minutes=2), NOW - timedelta(minutes=1),
        Decimal("1000"), Decimal("400"), Decimal("100"), Decimal("50"),
        Decimal("50"), "b" * 64, "c" * 64,
    )


class FuturesEventTests(unittest.TestCase):
    def test_nonfinite_event_edge_cannot_rank(self) -> None:
        with self.assertRaisesRegex(ValueError, "finite"):
            evaluate_futures_event(
                contract(),
                replace(event(), modeled_gross_impact_per_contract=Decimal("Infinity")),
                NOW,
                Decimal("10"),
            )

    def test_universe_ranks_residual_edge_and_never_authorizes(self) -> None:
        stronger = replace(
            event(), event_id="shipping-strong",
            event_type=PhysicalEventType.SHIPPING_DISRUPTION,
            modeled_gross_impact_per_contract=Decimal("1200"),
        )
        result = evaluate_futures_universe(
            (
                FuturesEventCandidate(contract(), event()),
                FuturesEventCandidate(contract(), stronger),
            ),
            NOW,
            Decimal("300"),
        )
        self.assertEqual(result.candidates[0].event_id, "shipping-strong")
        self.assertFalse(result.trade_authorized)
        self.assertTrue(all(not item.trade_authorized for item in result.candidates))

    def test_universe_returns_no_trade_when_events_are_priced(self) -> None:
        priced = replace(event(), curve_priced_impact_per_contract=Decimal("900"))
        result = evaluate_futures_universe(
            (FuturesEventCandidate(contract(), priced),), NOW, Decimal("100")
        )
        self.assertEqual(result.disposition, "NO_TRADE")
        self.assertIn("EVENT_EDGE_BELOW_SAFETY_BUFFER", result.rejected_events[0][1])

    def test_residual_event_edge_is_cost_and_curve_aware_but_research_only(self) -> None:
        result = evaluate_futures_event(contract(), event(), NOW, Decimal("300"))
        self.assertEqual(result.residual_edge_per_contract, Decimal("400"))
        self.assertEqual(result.disposition, "EVENT_RESEARCH_CANDIDATE")
        self.assertFalse(result.trade_authorized)
        self.assertEqual(result.environment, "paper")

    def test_known_event_can_be_fully_priced_and_become_no_trade(self) -> None:
        priced = replace(event(), curve_priced_impact_per_contract=Decimal("800"))
        result = evaluate_futures_event(contract(), priced, NOW, Decimal("100"))
        self.assertEqual(result.disposition, "NO_TRADE")
        self.assertIn("EVENT_EDGE_BELOW_SAFETY_BUFFER", result.reason_codes)

    def test_physical_delivery_and_late_evidence_fail_closed(self) -> None:
        physical = replace(contract(), physically_deliverable=True)
        late = replace(event(), received_at=NOW + timedelta(seconds=1))
        result = evaluate_futures_event(physical, late, NOW, Decimal("100"))
        self.assertIn("PHYSICAL_DELIVERY_DISABLED", result.reason_codes)
        self.assertIn("EVENT_NOT_POINT_IN_TIME", result.reason_codes)


if __name__ == "__main__":
    unittest.main()
