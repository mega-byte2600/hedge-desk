"""Frozen end-to-end fixture for the Overnight Premium Desk MVP."""

from dataclasses import asdict, is_dataclass
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from enum import Enum
from typing import Any, Dict

from hedge_desk.core.decision import evaluate_candidate
from hedge_desk.backoffice import evaluate_paper_compliance
from hedge_desk.domain import Account, AccountType, ProductType, TradeCandidate
from hedge_desk.options import (
    OptionQuote,
    OptionType,
    VerticalCreditSpread,
    calculate_vertical_credit_spread,
)
from hedge_desk.paper import (
    approve_paper_trade,
    close_paper_trade,
    create_paper_trade_plan,
    execute_paper_open,
)


FIXTURE_ID = "overnight-premium-reference-v1"
FIXTURE_AS_OF = datetime(2026, 7, 28, 20, 0, tzinfo=timezone.utc)


def json_value(value: Any) -> Any:
    """Convert immutable domain records into stable JSON-compatible values."""
    if is_dataclass(value):
        return {key: json_value(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): json_value(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_value(item) for item in value]
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def build_reference_plan() -> Any:
    """Build a human-pending plan entirely from a frozen synthetic fixture.

    The 0.85 probability is an explicit fixture input standing in for a
    separately validated model output. This function does not estimate it.
    """
    expiration = date(2026, 8, 21)
    short_quote = OptionQuote(
        contract_id="TEST260821P00095000",
        underlying="TEST",
        option_type=OptionType.PUT,
        strike=Decimal("95"),
        expiration=expiration,
        bid=Decimal("2.00"),
        ask=Decimal("2.10"),
        bid_size=25,
        ask_size=30,
        quoted_at=FIXTURE_AS_OF,
        source_id="synthetic-fixture",
    )
    long_quote = OptionQuote(
        contract_id="TEST260821P00090000",
        underlying="TEST",
        option_type=OptionType.PUT,
        strike=Decimal("90"),
        expiration=expiration,
        bid=Decimal("0.75"),
        ask=Decimal("0.80"),
        bid_size=25,
        ask_size=30,
        quoted_at=FIXTURE_AS_OF,
        source_id="synthetic-fixture",
    )
    spread = calculate_vertical_credit_spread(
        VerticalCreditSpread(
            spread_id="TEST-95-90-PUT-CREDIT",
            short_leg=short_quote,
            long_leg=long_quote,
            quantity=1,
            commission_per_contract=Decimal("0.65"),
        ),
        FIXTURE_AS_OF,
    )
    account = Account(
        account_id="paper-individual-001",
        account_type=AccountType.INDIVIDUAL,
        equity=Decimal("100000"),
        cash=Decimal("50000"),
        options_approved=True,
    )
    candidate = TradeCandidate(
        candidate_id=spread.spread_id,
        symbol="TEST",
        product_type=ProductType.DEFINED_RISK_OPTION,
        quantity=spread.quantity,
        entry_price=spread.net_credit,
        max_loss=spread.maximum_loss,
        expected_win=spread.net_credit,
        win_probability=Decimal("0.85"),
        quote_timestamp=FIXTURE_AS_OF,
        average_daily_dollar_volume=Decimal("100000000"),
        thesis="Synthetic reference case for executable-side premium capture.",
        invalidation="Reject outside the frozen fixture and validated inputs.",
    )
    decision = evaluate_candidate(account, candidate, FIXTURE_AS_OF)
    compliance_decision = evaluate_paper_compliance(account, candidate, FIXTURE_AS_OF)
    return create_paper_trade_plan(
        plan_id=FIXTURE_ID,
        spread=spread,
        risk_decision=decision,
        compliance_decision=compliance_decision,
        created_at=FIXTURE_AS_OF,
        approval_expires_at=FIXTURE_AS_OF + timedelta(minutes=15),
    )


def run_reference_demo(approve: bool = False, human_id: str = "") -> Dict[str, Any]:
    """Run the frozen paper workflow; execution is impossible without approval."""
    plan = build_reference_plan()
    output: Dict[str, Any] = {
        "fixture_id": FIXTURE_ID,
        "mode": "paper",
        "plan": json_value(plan),
    }
    if not approve:
        output["next_action"] = "human_authorization_required"
        return output

    approved = approve_paper_trade(
        plan, human_id=human_id, decided_at=FIXTURE_AS_OF + timedelta(minutes=1)
    )
    opened = execute_paper_open(
        approved, opened_at=FIXTURE_AS_OF + timedelta(minutes=2)
    )
    closed = close_paper_trade(
        opened,
        exit_debit_per_share=Decimal("0.40"),
        exit_commission_per_contract=Decimal("0.65"),
        closed_at=FIXTURE_AS_OF + timedelta(days=1),
    )
    output.update(
        {
            "plan": json_value(approved),
            "paper_open": json_value(opened),
            "paper_close": json_value(closed),
        }
    )
    return output
