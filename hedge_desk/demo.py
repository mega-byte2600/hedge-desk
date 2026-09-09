"""Frozen end-to-end fixture for the Overnight Premium Desk MVP."""

from dataclasses import asdict, is_dataclass, replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from enum import Enum
from hashlib import sha256
from typing import Any, Dict

from hedge_desk.core.decision import evaluate_candidate
from hedge_desk.backoffice import evaluate_paper_compliance
from hedge_desk.domain import Account, AccountType, ProductType, TradeCandidate
from hedge_desk.options import (
    OptionQuote,
    OptionType,
    UnderlyingQuote,
    evaluate_event_calendar,
    VerticalCreditSpread,
    calculate_vertical_credit_spread,
    OptionSnapshot,
    MarketSessionEvidence,
    build_candidate_control_handoffs,
    evaluate_market_session,
    scan_vertical_credit_spreads,
)
from hedge_desk.paper import (
    approve_paper_trade,
    close_paper_trade,
    calculate_proposed_plan_hash,
    create_paper_trade_plan,
    execute_paper_open,
)
from hedge_desk.yellow_sheet import (
    CrossMarketContext,
    EvidenceObservation,
    InvalidationCondition,
    TradeAction,
    TradeLogicRule,
    YellowSheetRiskContext,
    YELLOW_SHEET_POLICY_VERSION,
    YELLOW_SHEET_SCHEMA_VERSION,
    build_yellow_sheet,
)
from hedge_desk.risk import build_validated_risk_inputs


FIXTURE_ID = "overnight-premium-reference-v1"
FIXTURE_AS_OF = datetime(2026, 7, 28, 20, 0, tzinfo=timezone.utc)
FIXTURE_OPTION_SOURCE_ID = "synthetic-option-chain"
FIXTURE_OPTION_PAYLOAD_SHA256 = sha256(
    b"TEST260821P00095000--TEST260821P00090000|2026-07-28T20:00:00Z"
).hexdigest()


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


def build_reference_option_snapshot() -> OptionSnapshot:
    """Build the canonical option snapshot used by the frozen reference case."""
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
        source_id=FIXTURE_OPTION_SOURCE_ID,
        open_interest=1000,
        volume=500,
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
        source_id=FIXTURE_OPTION_SOURCE_ID,
        open_interest=1000,
        volume=500,
    )
    underlying_quote = UnderlyingQuote(
        "TEST", Decimal("99.99"), Decimal("100.01"),
        FIXTURE_AS_OF, FIXTURE_OPTION_SOURCE_ID,
    )
    return OptionSnapshot(
        "hedge-desk-option-snapshot-1.0.0",
        FIXTURE_OPTION_SOURCE_ID,
        underlying_quote,
        (short_quote, long_quote),
        FIXTURE_OPTION_PAYLOAD_SHA256,
    )


def build_reference_market_session_gate():
    evidence = MarketSessionEvidence(
        "OPRA-SYNTHETIC",
        FIXTURE_AS_OF - timedelta(hours=6, minutes=30),
        FIXTURE_AS_OF,
        FIXTURE_AS_OF - timedelta(hours=7),
        sha256(b"synthetic-market-session-2026-07-28").hexdigest(),
    )
    return evaluate_market_session(evidence, FIXTURE_AS_OF, 0)


def build_reference_plan() -> Any:
    """Build a human-pending plan entirely from a frozen synthetic fixture.

    The 0.85 probability is an explicit fixture input standing in for a
    separately validated model output. This function does not estimate it.
    """
    snapshot = build_reference_option_snapshot()
    quotes_by_id = {quote.contract_id: quote for quote in snapshot.option_quotes}
    short_quote = quotes_by_id["TEST260821P00095000"]
    long_quote = quotes_by_id["TEST260821P00090000"]
    spread = calculate_vertical_credit_spread(
        VerticalCreditSpread(
            spread_id="TEST260821P00095000--TEST260821P00090000",
            short_leg=short_quote,
            long_leg=long_quote,
            underlying_quote=snapshot.underlying_quote,
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
        options_disclosure_version="synthetic-odd-fixture-v1",
        options_disclosure_acknowledged_at=FIXTURE_AS_OF - timedelta(days=1),
        broker_options_policy_version="synthetic-broker-policy-v1",
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
    compliance_decision = evaluate_paper_compliance(account, candidate, FIXTURE_AS_OF)
    scan = scan_vertical_credit_spreads(snapshot, FIXTURE_AS_OF)
    handoffs = build_candidate_control_handoffs(
        scan, build_reference_market_session_gate()
    )
    if len(handoffs) != 1 or handoffs[0].candidate_id != candidate.candidate_id:
        raise ValueError("reference candidate handoff is incomplete")
    risk_inputs = build_validated_risk_inputs(
        candidate.candidate_id,
        candidate.max_loss,
        candidate.expected_win,
        candidate.win_probability,
        FIXTURE_AS_OF,
        handoffs[0].calculation_sha256,
        compliance_decision.portfolio_snapshot_sha256,
        Decimal("0"),
        Decimal("0"),
        "finite-capital-ruin-approximation",
        "0.1.0-unvalidated",
        "classic-vv-fixture-validator",
        "1.0.0",
    )
    decision = evaluate_candidate(
        account, candidate, FIXTURE_AS_OF, risk_inputs=risk_inputs
    )
    event_calendar_gate = evaluate_event_calendar(
        "TEST",
        FIXTURE_AS_OF,
        short_quote.expiration,
        (),
        spread,
        OptionType.PUT,
        short_quote.strike,
    )
    plan_arguments = dict(
        plan_id=FIXTURE_ID,
        spread=spread,
        risk_decision=decision,
        compliance_decision=compliance_decision,
        event_calendar_gate=event_calendar_gate,
        created_at=FIXTURE_AS_OF,
        approval_expires_at=FIXTURE_AS_OF + timedelta(minutes=15),
    )
    plan_hash = calculate_proposed_plan_hash(
        execution_quote_max_age_seconds=120,
        control_artifact_max_age_seconds=120,
        **plan_arguments,
    )
    evidence_hash = sha256(b"synthetic-yellow-sheet-evidence").hexdigest()
    sheet = build_yellow_sheet(
        schema_version=YELLOW_SHEET_SCHEMA_VERSION,
        yellow_sheet_id="ys-overnight-premium-reference-v1",
        version=1,
        candidate_id=candidate.candidate_id,
        plan_hash=plan_hash,
        interest="Synthetic liquid option premium was observed in the frozen fixture.",
        hypothesis="Executable premium compensates the defined maximum loss in this synthetic case.",
        investigation=(
            "Compared executable option prices, liquidity, event timing, rates, credit, volatility, and alternative no-trade explanations.",
        ),
        evidence=(EvidenceObservation(
            "The synchronized executable quotes produce positive net credit and bounded loss.",
            True, FIXTURE_OPTION_SOURCE_ID, FIXTURE_AS_OF,
            evidence_hash, "vertical-credit-spread-1.0.0",
        ),),
        trade_logic=tuple(
            TradeLogicRule(action, condition) for action, condition in (
                (TradeAction.BUY, "Buy only when an independently approved plan requires a long leg."),
                (TradeAction.SELL, "Sell only as the short leg of the exact approved defined-risk spread."),
                (TradeAction.HOLD, "Hold pending separate risk, compliance, and human authorization."),
                (TradeAction.REDUCE, "Reduce when a deterministic exposure or exit control requires it."),
                (TradeAction.NO_TRADE, "Do not trade if any evidence, risk, compliance, liquidity, hash, or authorization gate fails."),
            )
        ),
        invalidation=(InvalidationCondition(
            "Quotes, event calendar, economics, or control artifacts differ from the bound plan.",
            False, FIXTURE_AS_OF, evidence_hash,
        ),),
        cross_market_context=CrossMarketContext(
            "Synthetic fixture; no adverse bond/yield signal asserted.",
            "Synthetic fixture; curve context recorded but no inference made.",
            "Synthetic fixture; credit-spread context recorded but no inference made.",
            "Underlying quote is synchronized with both option legs.",
            "Executable option prices are used; no volatility forecast is inferred.",
            "Not material to this synthetic equity-option fixture.",
            "Not material to this synthetic USD fixture.",
            "Displayed size, volume, open interest, and bid/ask controls passed.",
        ),
        risk_context=YellowSheetRiskContext(
            str(spread.quantity), str(spread.maximum_loss),
            "Bound to the independently validated portfolio snapshot.",
            "Executable-side liquidity controls passed.",
            "Bound to deterministic symbol and aggregate concentration gates.",
            risk_inputs.artifact_sha256,
            decision.risk_model_id + "@" + decision.risk_model_version,
        ),
        decision_rationale="This exact defined-risk paper proposal is presented because synchronized executable quotes, bounded loss, liquidity, and event controls support human review; it does not authorize execution.",
        input_hashes=tuple(sorted((evidence_hash, risk_inputs.artifact_sha256, handoffs[0].calculation_sha256))),
        policy_version=YELLOW_SHEET_POLICY_VERSION,
        model_version="synthetic-rationale-fixture-1.0.0",
        created_at=FIXTURE_AS_OF,
        prior_yellow_sheet_version=None,
    )
    return create_paper_trade_plan(**plan_arguments, yellow_sheet=sheet)


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
    exit_snapshot = build_reference_option_snapshot()
    closed_at = FIXTURE_AS_OF + timedelta(days=1)
    exit_short = replace(
        exit_snapshot.option_quotes[0],
        bid=Decimal("0.40"), ask=Decimal("0.50"), quoted_at=closed_at,
    )
    exit_long = replace(
        exit_snapshot.option_quotes[1],
        bid=Decimal("0.10"), ask=Decimal("0.20"), quoted_at=closed_at,
    )
    closed = close_paper_trade(
        opened,
        approved,
        exit_short,
        exit_long,
        exit_commission_per_contract=Decimal("0.65"),
        closed_at=closed_at,
    )
    output.update(
        {
            "plan": json_value(approved),
            "paper_open": json_value(opened),
            "paper_close": json_value(closed),
        }
    )
    return output
