"""Deterministic, synthetic war games for paper strategy evaluation."""

from dataclasses import dataclass, replace
from datetime import timedelta
from decimal import Decimal
from hashlib import sha256
import json
from typing import Any, Dict, Tuple

from hedge_desk.demo import (
    FIXTURE_AS_OF,
    build_reference_option_snapshot,
    build_reference_plan,
    json_value,
)
from hedge_desk.paper import (
    approve_paper_trade,
    close_paper_trade,
    evaluate_paper_fill,
    evaluate_paper_lifecycle,
    execute_paper_open,
)
from hedge_desk.metrics import evaluate_pnl_series
from hedge_desk.futures_events import (
    FuturesContractSnapshot,
    FuturesEventInputs,
    PhysicalEventType,
    evaluate_futures_event,
)
from hedge_desk.models import (
    ModelArtifact,
    ModelTeam,
    ResearchLabel,
    ResearchVote,
    evaluate_research_quorum,
)
from hedge_desk.backoffice import (
    BackOfficeStatus,
    evaluate_compliance_policy,
    validate_compliance_policy_artifact,
)
from hedge_desk.domain import Account, AccountType, ProductType, TradeCandidate
from hedge_desk.options import (
    build_candidate_control_handoffs,
    scan_vertical_credit_spreads,
    validate_candidate_control_handoff,
)


WAR_GAME_VERSION = "premium-spread-war-games-1.0.0"
WAR_GAME_FIXTURE_SCHEMA_VERSION = "war-game-fixtures-1.0.0"


@dataclass(frozen=True)
class PremiumWarGame:
    scenario_id: str
    description: str
    exit_debit_per_share: Decimal
    exit_commission_per_contract: Decimal
    additional_operational_cost: Decimal = Decimal("0")


@dataclass(frozen=True)
class PremiumWarGameResult:
    scenario_id: str
    description: str
    entry_credit: Decimal
    exit_debit: Decimal
    exit_commission: Decimal
    additional_operational_cost: Decimal
    net_pnl: Decimal
    profitable: bool
    maximum_loss_reference: Decimal


@dataclass(frozen=True)
class EarningsWarGame:
    scenario_id: str
    start_price: Decimal
    end_price: Decimal
    shares: int
    equity_cost: Decimal
    option_entry_debit: Decimal
    option_exit_credit: Decimal
    option_cost: Decimal
    hedged_gross_pnl: Decimal
    hedged_cost: Decimal


@dataclass(frozen=True)
class ArbitrageWarGame:
    scenario_id: str
    gross_edge: Decimal
    quantity: int
    fees: Decimal
    slippage_reserve: Decimal
    financing_cost: Decimal
    minimum_edge_buffer: Decimal
    quotes_synchronized: bool = True
    depth_available: int = 1
    settlement_compatible: bool = True


@dataclass(frozen=True)
class DividendWarGame:
    scenario_id: str
    start_price: Decimal
    end_price: Decimal
    shares: int
    dividend_per_share_received: Decimal
    share_cost: Decimal
    call_entry_debit: Decimal
    call_exit_credit: Decimal
    call_cost: Decimal


@dataclass(frozen=True)
class ExecutionWarGame:
    scenario_id: str
    available_combo_size: int
    current_net_credit: Decimal
    checked_offset_seconds: int
    contract_adjustment_pending: bool = False


@dataclass(frozen=True)
class LifecycleWarGame:
    scenario_id: str
    planned_exit_reached: bool = False
    expiration_reached: bool = False
    short_leg_in_the_money: bool = False
    ex_dividend_before_expiration: bool = False
    assignment_notice_received: bool = False
    contract_adjustment_pending: bool = False
    settlement_terms_confirmed: bool = True


@dataclass(frozen=True)
class FuturesEventWarGame:
    scenario_id: str
    event_type: PhysicalEventType
    gross_impact: Decimal
    curve_priced: Decimal
    basis_reserve: Decimal
    roll_cost: Decimal
    transaction_cost: Decimal
    physically_deliverable: bool = False
    received_after_decision: bool = False


@dataclass(frozen=True)
class ModelGovernanceWarGame:
    scenario_id: str
    quant_label: ResearchLabel
    ai_label: ResearchLabel
    ai_license: str = "Apache-2.0"


@dataclass(frozen=True)
class ComplianceWarGame:
    scenario_id: str
    attack: str


@dataclass(frozen=True)
class PremiumTimingWarGame:
    scenario_id: str
    days_before_expiration: int
    executable_exit_debit_per_share: Decimal


@dataclass(frozen=True)
class CandidatePipelineWarGame:
    scenario_id: str
    attack: str


PREMIUM_WAR_GAMES: Tuple[PremiumWarGame, ...] = (
    PremiumWarGame(
        "favorable-decay",
        "Premium contracts before the planned exit.",
        Decimal("0.40"),
        Decimal("0.65"),
    ),
    PremiumWarGame(
        "no-edge-after-costs",
        "Gross spread value is unchanged and commissions create a loss.",
        Decimal("1.20"),
        Decimal("0.65"),
    ),
    PremiumWarGame(
        "iv-shock",
        "Implied volatility expands and the spread becomes more expensive.",
        Decimal("2.50"),
        Decimal("0.65"),
    ),
    PremiumWarGame(
        "gap-through-width",
        "Underlying gaps through both strikes and the spread approaches full width.",
        Decimal("5.00"),
        Decimal("0.65"),
    ),
    PremiumWarGame(
        "assignment-operations",
        "Adverse move plus synthetic assignment and operational handling cost.",
        Decimal("5.00"),
        Decimal("0.65"),
        Decimal("25.00"),
    ),
)


EARNINGS_WAR_GAMES: Tuple[EarningsWarGame, ...] = (
    EarningsWarGame(
        "surprise-followthrough", Decimal("100"), Decimal("104"), 10,
        Decimal("4"), Decimal("2.50"), Decimal("4.00"), Decimal("4"),
        Decimal("25"), Decimal("5"),
    ),
    EarningsWarGame(
        "positive-surprise-iv-crush", Decimal("100"), Decimal("101"), 10,
        Decimal("4"), Decimal("4.00"), Decimal("2.00"), Decimal("4"),
        Decimal("5"), Decimal("5"),
    ),
    EarningsWarGame(
        "headline-beat-guidance-reversal", Decimal("100"), Decimal("94"), 10,
        Decimal("4"), Decimal("3.00"), Decimal("0.50"), Decimal("4"),
        Decimal("-20"), Decimal("5"),
    ),
)


ARBITRAGE_WAR_GAMES: Tuple[ArbitrageWarGame, ...] = (
    ArbitrageWarGame(
        "net-edge-survives", Decimal("80"), 1, Decimal("12"), Decimal("15"),
        Decimal("8"), Decimal("20"),
    ),
    ArbitrageWarGame(
        "one-tick-erased-by-costs", Decimal("20"), 1, Decimal("12"),
        Decimal("10"), Decimal("4"), Decimal("5"),
    ),
    ArbitrageWarGame(
        "stale-fourth-leg", Decimal("100"), 1, Decimal("12"), Decimal("15"),
        Decimal("8"), Decimal("20"), quotes_synchronized=False,
    ),
    ArbitrageWarGame(
        "insufficient-depth", Decimal("100"), 2, Decimal("12"), Decimal("15"),
        Decimal("8"), Decimal("20"), depth_available=1,
    ),
    ArbitrageWarGame(
        "settlement-mismatch", Decimal("100"), 1, Decimal("12"), Decimal("15"),
        Decimal("8"), Decimal("20"), settlement_compatible=False,
    ),
)


DIVIDEND_WAR_GAMES: Tuple[DividendWarGame, ...] = (
    DividendWarGame(
        "normal-dividend-entitlement", Decimal("50"), Decimal("52"), 100,
        Decimal("1"), Decimal("4"), Decimal("2"), Decimal("3.50"), Decimal("5"),
    ),
    DividendWarGame(
        "special-dividend", Decimal("50"), Decimal("48"), 100, Decimal("5"),
        Decimal("5"), Decimal("2"), Decimal("1"), Decimal("5"),
    ),
    DividendWarGame(
        "dividend-cut", Decimal("50"), Decimal("48"), 100, Decimal("0.10"),
        Decimal("5"), Decimal("2"), Decimal("0.50"), Decimal("5"),
    ),
    DividendWarGame(
        "yield-trap", Decimal("50"), Decimal("35"), 100, Decimal("0.25"),
        Decimal("4"), Decimal("2"), Decimal("0.10"), Decimal("5"),
    ),
)


EXECUTION_WAR_GAMES: Tuple[ExecutionWarGame, ...] = (
    ExecutionWarGame("approved-terms-available", 1, Decimal("118.70"), 120),
    ExecutionWarGame("stale-entry-quote", 1, Decimal("118.70"), 121),
    ExecutionWarGame("partial-combo-size", 0, Decimal("118.70"), 60),
    ExecutionWarGame("approved-credit-unavailable", 1, Decimal("118.69"), 60),
    ExecutionWarGame(
        "contract-adjustment-pending", 1, Decimal("118.70"), 60, True
    ),
)


LIFECYCLE_WAR_GAMES: Tuple[LifecycleWarGame, ...] = (
    LifecycleWarGame("normal-monitoring"),
    LifecycleWarGame("planned-pre-expiration-exit", planned_exit_reached=True),
    LifecycleWarGame(
        "ex-dividend-early-assignment-risk",
        short_leg_in_the_money=True,
        ex_dividend_before_expiration=True,
    ),
    LifecycleWarGame("assignment-notice", assignment_notice_received=True),
    LifecycleWarGame("expiration-reconciliation", expiration_reached=True),
    LifecycleWarGame(
        "unconfirmed-settlement-terms", settlement_terms_confirmed=False
    ),
)


FUTURES_EVENT_WAR_GAMES: Tuple[FuturesEventWarGame, ...] = (
    FuturesEventWarGame(
        "weather-surprise-edge-survives", PhysicalEventType.EXTREME_WEATHER,
        Decimal("1000"), Decimal("400"), Decimal("100"), Decimal("50"), Decimal("50"),
    ),
    FuturesEventWarGame(
        "weather-event-already-priced", PhysicalEventType.EXTREME_WEATHER,
        Decimal("1000"), Decimal("800"), Decimal("100"), Decimal("50"), Decimal("50"),
    ),
    FuturesEventWarGame(
        "shipping-basis-erases-edge", PhysicalEventType.SHIPPING_DISRUPTION,
        Decimal("1000"), Decimal("300"), Decimal("500"), Decimal("100"), Decimal("150"),
    ),
    FuturesEventWarGame(
        "physical-delivery-contract-disabled", PhysicalEventType.SHIPPING_DISRUPTION,
        Decimal("1000"), Decimal("400"), Decimal("100"), Decimal("50"), Decimal("50"),
        physically_deliverable=True,
    ),
    FuturesEventWarGame(
        "war-event-evidence-arrives-late", PhysicalEventType.WAR_GEOPOLITICAL,
        Decimal("1000"), Decimal("400"), Decimal("100"), Decimal("50"), Decimal("50"),
        received_after_decision=True,
    ),
)


MODEL_GOVERNANCE_WAR_GAMES: Tuple[ModelGovernanceWarGame, ...] = (
    ModelGovernanceWarGame(
        "quant-ai-agree-research-only", ResearchLabel.POSITIVE, ResearchLabel.POSITIVE
    ),
    ModelGovernanceWarGame(
        "quant-ai-disagree", ResearchLabel.POSITIVE, ResearchLabel.NEGATIVE
    ),
    ModelGovernanceWarGame(
        "ai-artifact-license-blocked", ResearchLabel.POSITIVE,
        ResearchLabel.POSITIVE, "proprietary",
    ),
)


COMPLIANCE_WAR_GAMES: Tuple[ComplianceWarGame, ...] = (
    ComplianceWarGame("live-environment-request", "LIVE_ENVIRONMENT"),
    ComplianceWarGame("compliance-artifact-tamper", "HASH_TAMPER"),
    ComplianceWarGame("agent-compliance-pass-override", "PASS_OVERRIDE"),
    ComplianceWarGame("options-disclosure-missing", "MISSING_ODD"),
    ComplianceWarGame("options-disclosure-after-candidate", "LATE_ODD"),
)


PREMIUM_TIMING_WAR_GAMES: Tuple[PremiumTimingWarGame, ...] = (
    PremiumTimingWarGame("timing-21-dte", 21, Decimal("1.00")),
    PremiumTimingWarGame("timing-8-dte", 8, Decimal("0.60")),
    PremiumTimingWarGame("timing-planned-exit-7-dte", 7, Decimal("0.40")),
    PremiumTimingWarGame("timing-adverse-1-dte", 1, Decimal("4.80")),
    PremiumTimingWarGame("timing-expiration", 0, Decimal("5.00")),
)


CANDIDATE_PIPELINE_WAR_GAMES: Tuple[CandidatePipelineWarGame, ...] = (
    CandidatePipelineWarGame("candidate-awaits-validated-risk", "MISSING_RISK"),
    CandidatePipelineWarGame("candidate-thin-market", "THIN_MARKET"),
    CandidatePipelineWarGame("candidate-handoff-economics-tamper", "TAMPER"),
    CandidatePipelineWarGame("candidate-front-office-authorization", "AUTHORIZE"),
)


def _reference_account(
    options_approved: bool = True,
    disclosure_present: bool = True,
    disclosure_late: bool = False,
) -> Account:
    return Account(
        "paper-individual-001",
        AccountType.INDIVIDUAL,
        Decimal("100000"),
        Decimal("50000"),
        options_approved=options_approved,
        options_disclosure_version=(
            "synthetic-odd-fixture-v1" if disclosure_present else None
        ),
        options_disclosure_acknowledged_at=(
            FIXTURE_AS_OF + timedelta(microseconds=1)
            if disclosure_late
            else (FIXTURE_AS_OF - timedelta(days=1) if disclosure_present else None)
        ),
        broker_options_policy_version="synthetic-broker-policy-v1",
    )


def _reference_candidate(plan: Any) -> TradeCandidate:
    return TradeCandidate(
        plan.risk_decision.candidate_id,
        "TEST",
        ProductType.DEFINED_RISK_OPTION,
        plan.spread.quantity,
        plan.spread.net_credit,
        plan.spread.maximum_loss,
        plan.spread.net_credit,
        Decimal("0.85"),
        FIXTURE_AS_OF,
        Decimal("100000000"),
        "Synthetic compliance war-game candidate.",
        "Reject outside the frozen compliance fixture.",
    )


def run_premium_war_games() -> Tuple[PremiumWarGameResult, ...]:
    """Replay every declared scenario; no scenario selection is permitted."""
    plan = build_reference_plan()
    approved = approve_paper_trade(plan, "war-game-human", FIXTURE_AS_OF)
    opened = execute_paper_open(approved, FIXTURE_AS_OF + timedelta(minutes=1))
    results = []
    for index, scenario in enumerate(PREMIUM_WAR_GAMES, start=1):
        closed = close_paper_trade(
            opened,
            scenario.exit_debit_per_share,
            scenario.exit_commission_per_contract,
            FIXTURE_AS_OF + timedelta(days=index),
        )
        net_pnl = closed.realized_pnl - scenario.additional_operational_cost
        results.append(
            PremiumWarGameResult(
                scenario.scenario_id,
                scenario.description,
                opened.entry_credit,
                closed.exit_debit,
                closed.exit_commission,
                scenario.additional_operational_cost,
                net_pnl,
                net_pnl > 0,
                plan.spread.maximum_loss,
            )
        )
    return tuple(results)


def run_earnings_war_games() -> Tuple[Dict[str, str], ...]:
    results = []
    for scenario in EARNINGS_WAR_GAMES:
        equity = (
            (scenario.end_price - scenario.start_price) * Decimal(scenario.shares)
            - scenario.equity_cost
        )
        option = (
            (scenario.option_exit_credit - scenario.option_entry_debit) * Decimal("100")
            - scenario.option_cost
        )
        hedged = scenario.hedged_gross_pnl - scenario.hedged_cost
        arms = {"EQUITY": equity, "DEFINED_RISK_OPTION": option, "HEDGED_EQUITY": hedged, "NO_TRADE": Decimal("0")}
        selected = max(sorted(arms), key=lambda arm: arms[arm])
        results.append(
            {
                "scenario_id": scenario.scenario_id,
                "equity_net_pnl": str(equity),
                "option_net_pnl": str(option),
                "hedged_equity_net_pnl": str(hedged),
                "no_trade_net_pnl": "0",
                "best_hindsight_arm": selected,
            }
        )
    return tuple(results)


def run_arbitrage_war_games() -> Tuple[Dict[str, str], ...]:
    results = []
    for scenario in ARBITRAGE_WAR_GAMES:
        reasons = []
        if not scenario.quotes_synchronized:
            reasons.append("QUOTES_NOT_SYNCHRONIZED")
        if scenario.depth_available < scenario.quantity:
            reasons.append("INSUFFICIENT_DEPTH")
        if not scenario.settlement_compatible:
            reasons.append("SETTLEMENT_MISMATCH")
        net_edge = (
            scenario.gross_edge * Decimal(scenario.quantity)
            - scenario.fees
            - scenario.slippage_reserve
            - scenario.financing_cost
        )
        if net_edge < scenario.minimum_edge_buffer:
            reasons.append("EDGE_BELOW_SAFETY_BUFFER")
        results.append(
            {
                "scenario_id": scenario.scenario_id,
                "gross_edge": str(scenario.gross_edge * Decimal(scenario.quantity)),
                "net_edge": str(net_edge),
                "disposition": "NO_TRADE" if reasons else "NET_EDGE_CANDIDATE",
                "reason_codes": ",".join(sorted(reasons)),
            }
        )
    return tuple(results)


def run_dividend_war_games() -> Tuple[Dict[str, str], ...]:
    results = []
    for scenario in DIVIDEND_WAR_GAMES:
        share_pnl = (
            (scenario.end_price - scenario.start_price) * Decimal(scenario.shares)
            + scenario.dividend_per_share_received * Decimal(scenario.shares)
            - scenario.share_cost
        )
        call_pnl = (
            (scenario.call_exit_credit - scenario.call_entry_debit) * Decimal("100")
            - scenario.call_cost
        )
        arms = {"SHARES": share_pnl, "LONG_CALL": call_pnl, "NO_TRADE": Decimal("0")}
        selected = max(sorted(arms), key=lambda arm: arms[arm])
        results.append(
            {
                "scenario_id": scenario.scenario_id,
                "share_net_pnl": str(share_pnl),
                "call_net_pnl": str(call_pnl),
                "call_dividend_received": "0",
                "no_trade_net_pnl": "0",
                "best_hindsight_arm": selected,
            }
        )
    return tuple(results)


def run_execution_war_games() -> Tuple[Dict[str, Any], ...]:
    plan = approve_paper_trade(build_reference_plan(), "war-game-human", FIXTURE_AS_OF)
    results = []
    for scenario in EXECUTION_WAR_GAMES:
        check = evaluate_paper_fill(
            plan,
            scenario.available_combo_size,
            scenario.current_net_credit,
            FIXTURE_AS_OF + timedelta(seconds=scenario.checked_offset_seconds),
            scenario.contract_adjustment_pending,
        )
        results.append(
            {
                "scenario_id": scenario.scenario_id,
                "disposition": "READY_FOR_PAPER_OPEN" if check.ready else "NO_TRADE",
                "reason_codes": list(check.reason_codes),
            }
        )
    return tuple(results)


def run_lifecycle_war_games() -> Tuple[Dict[str, Any], ...]:
    results = []
    for scenario in LIFECYCLE_WAR_GAMES:
        check = evaluate_paper_lifecycle(
            FIXTURE_AS_OF + timedelta(days=1),
            scenario.planned_exit_reached,
            scenario.expiration_reached,
            scenario.short_leg_in_the_money,
            scenario.ex_dividend_before_expiration,
            scenario.assignment_notice_received,
            scenario.contract_adjustment_pending,
            scenario.settlement_terms_confirmed,
        )
        results.append(
            {
                "scenario_id": scenario.scenario_id,
                "action": check.action,
                "reason_codes": list(check.reason_codes),
            }
        )
    return tuple(results)


def run_futures_event_war_games() -> Tuple[Dict[str, Any], ...]:
    results = []
    for scenario in FUTURES_EVENT_WAR_GAMES:
        contract = FuturesContractSnapshot(
            "SYNTHETIC-FUT", 5000, Decimal("5000"),
            scenario.physically_deliverable, True, "8" * 64,
        )
        received_at = FIXTURE_AS_OF + (
            timedelta(seconds=1)
            if scenario.received_after_decision
            else -timedelta(minutes=1)
        )
        event = FuturesEventInputs(
            scenario.scenario_id, scenario.event_type,
            FIXTURE_AS_OF - timedelta(minutes=2), received_at,
            scenario.gross_impact, scenario.curve_priced, scenario.basis_reserve,
            scenario.roll_cost, scenario.transaction_cost, "9" * 64, "a" * 64,
        )
        evaluation = evaluate_futures_event(
            contract, event, FIXTURE_AS_OF, Decimal("300")
        )
        results.append(
            {
                "scenario_id": scenario.scenario_id,
                "event_type": scenario.event_type.value,
                "residual_edge_per_contract": str(
                    evaluation.residual_edge_per_contract
                ),
                "disposition": evaluation.disposition,
                "reason_codes": list(evaluation.reason_codes),
                "trade_authorized": evaluation.trade_authorized,
            }
        )
    return tuple(results)


def run_model_governance_war_games() -> Tuple[Dict[str, Any], ...]:
    results = []
    for scenario in MODEL_GOVERNANCE_WAR_GAMES:
        artifacts = tuple(
            ModelArtifact(
                f"{team.value.lower()}-war-model", team, "open-war-model", "1.0.0",
                "https://huggingface.co/example/open-war-model",
                scenario.ai_license if team is ModelTeam.AI else "Apache-2.0",
                "b" * 64, "deadbeef",
                FIXTURE_AS_OF - timedelta(days=100), "c" * 64, "d" * 64,
            )
            for team in (ModelTeam.QUANT, ModelTeam.AI)
        )
        votes = (
            ResearchVote(
                scenario.scenario_id, ModelTeam.QUANT, "quant-war-model",
                scenario.quant_label, FIXTURE_AS_OF, "e" * 64,
            ),
            ResearchVote(
                scenario.scenario_id, ModelTeam.AI, "ai-war-model",
                scenario.ai_label, FIXTURE_AS_OF, "f" * 64,
            ),
        )
        evaluation = evaluate_research_quorum(votes, artifacts)  # type: ignore[arg-type]
        results.append(
            {
                "scenario_id": scenario.scenario_id,
                "disposition": evaluation.disposition,
                "label": evaluation.label.value,
                "reason_codes": list(evaluation.reason_codes),
                "authoritative_risk_input": evaluation.authoritative_risk_input,
            }
        )
    return tuple(results)


def run_compliance_war_games() -> Tuple[Dict[str, Any], ...]:
    plan = build_reference_plan()
    results = []
    for scenario in COMPLIANCE_WAR_GAMES:
        account = _reference_account(
            disclosure_present=scenario.attack != "MISSING_ODD",
            disclosure_late=scenario.attack == "LATE_ODD",
        )
        decision = evaluate_compliance_policy(
            account=account,
            candidate=_reference_candidate(plan),
            evaluated_at=FIXTURE_AS_OF,
            environment="live" if scenario.attack == "LIVE_ENVIRONMENT" else "paper",
        )
        if scenario.attack == "HASH_TAMPER":
            decision = replace(decision, artifact_sha256="f" * 64)
        elif scenario.attack == "PASS_OVERRIDE":
            blocked = evaluate_compliance_policy(
                _reference_account(options_approved=False),
                _reference_candidate(plan),
                FIXTURE_AS_OF,
            )
            decision = replace(blocked, status=BackOfficeStatus.PASS)
        reasons = validate_compliance_policy_artifact(decision)
        if decision.status is BackOfficeStatus.BLOCK:
            reasons = tuple(sorted(set(reasons + decision.reason_codes)))
        results.append(
            {
                "scenario_id": scenario.scenario_id,
                "disposition": "NO_TRADE",
                "reason_codes": list(reasons),
                "human_override_allowed": False,
            }
        )
    return tuple(results)


def run_premium_timing_war_games() -> Tuple[Dict[str, Any], ...]:
    """Evaluate declared executable marks against the immutable exit policy."""
    plan = build_reference_plan()
    results = []
    for scenario in PREMIUM_TIMING_WAR_GAMES:
        check = evaluate_paper_lifecycle(
            FIXTURE_AS_OF + timedelta(days=1),
            planned_exit_reached=(
                scenario.days_before_expiration
                <= plan.spread.planned_exit_days_before_expiration
            ),
            expiration_reached=scenario.days_before_expiration <= 0,
            short_leg_in_the_money=False,
            ex_dividend_before_expiration=False,
            assignment_notice_received=False,
            contract_adjustment_pending=False,
            settlement_terms_confirmed=True,
        )
        exit_debit = (
            scenario.executable_exit_debit_per_share
            * Decimal(plan.spread.contract_multiplier)
            * Decimal(plan.spread.quantity)
        )
        exit_commission = Decimal("0.65") * Decimal("2")
        results.append(
            {
                "scenario_id": scenario.scenario_id,
                "days_before_expiration": scenario.days_before_expiration,
                "executable_exit_debit": str(exit_debit),
                "exit_commission": str(exit_commission),
                "net_pnl_if_closed": str(
                    plan.spread.net_credit - exit_debit - exit_commission
                ),
                "lifecycle_action": check.action,
                "reason_codes": list(check.reason_codes),
            }
        )
    return tuple(results)


def run_candidate_pipeline_war_games() -> Tuple[Dict[str, Any], ...]:
    base_snapshot = build_reference_option_snapshot()
    results = []
    for scenario in CANDIDATE_PIPELINE_WAR_GAMES:
        snapshot = base_snapshot
        if scenario.attack == "THIN_MARKET":
            thin_quotes = tuple(
                replace(quote, volume=0) for quote in snapshot.option_quotes
            )
            snapshot = replace(snapshot, option_quotes=thin_quotes)
        scan = scan_vertical_credit_spreads(snapshot, FIXTURE_AS_OF)
        handoffs = build_candidate_control_handoffs(scan)
        reasons = []
        if not handoffs:
            reasons.append("NO_ADMISSIBLE_CANDIDATE")
        else:
            handoff = handoffs[0]
            if scenario.attack == "TAMPER":
                handoff = replace(handoff, maximum_win="999999")
            elif scenario.attack == "AUTHORIZE":
                handoff = replace(handoff, trade_authorized=True)
            reasons.extend(validate_candidate_control_handoff(handoff))
            if scenario.attack == "MISSING_RISK":
                reasons.append("VALIDATED_RISK_INPUT_REQUIRED")
        results.append(
            {
                "scenario_id": scenario.scenario_id,
                "disposition": "NO_TRADE",
                "scan_disposition": scan.disposition,
                "reason_codes": sorted(set(reasons)),
                "trade_authorized": False,
            }
        )
    return tuple(results)


def build_war_game_manifest() -> Dict[str, Any]:
    """Content-address every declared scenario input using canonical JSON."""
    fixtures = {
        "premium": json_value(PREMIUM_WAR_GAMES),
        "earnings": json_value(EARNINGS_WAR_GAMES),
        "arbitrage": json_value(ARBITRAGE_WAR_GAMES),
        "dividend": json_value(DIVIDEND_WAR_GAMES),
        "execution": json_value(EXECUTION_WAR_GAMES),
        "lifecycle": json_value(LIFECYCLE_WAR_GAMES),
        "futures_events": json_value(FUTURES_EVENT_WAR_GAMES),
        "model_governance": json_value(MODEL_GOVERNANCE_WAR_GAMES),
        "compliance_controls": json_value(COMPLIANCE_WAR_GAMES),
        "premium_timing": json_value(PREMIUM_TIMING_WAR_GAMES),
        "candidate_pipeline": json_value(CANDIDATE_PIPELINE_WAR_GAMES),
    }
    scenario_ids = [
        scenario["scenario_id"]
        for group in fixtures.values()
        for scenario in group
    ]
    if len(scenario_ids) != len(set(scenario_ids)):
        raise ValueError("war-game scenario identities must be globally unique")
    payload = {
        "schema_version": WAR_GAME_FIXTURE_SCHEMA_VERSION,
        "fixtures": fixtures,
    }
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    report = {
        "schema_version": WAR_GAME_FIXTURE_SCHEMA_VERSION,
        "scenario_count": len(scenario_ids),
        "scenario_ids": scenario_ids,
        "fixture_sha256": sha256(canonical).hexdigest(),
    }
    return report


def build_war_game_report() -> Dict[str, Any]:
    results = run_premium_war_games()
    earnings = run_earnings_war_games()
    arbitrage = run_arbitrage_war_games()
    dividend = run_dividend_war_games()
    execution = run_execution_war_games()
    lifecycle = run_lifecycle_war_games()
    futures_events = run_futures_event_war_games()
    model_governance = run_model_governance_war_games()
    compliance_controls = run_compliance_war_games()
    premium_timing = run_premium_timing_war_games()
    candidate_pipeline = run_candidate_pipeline_war_games()
    pnls = tuple(result.net_pnl for result in results)
    wins = sum(result.profitable for result in results)
    premium_metrics = evaluate_pnl_series(pnls)
    earnings_arm_metrics = {
        "EQUITY": evaluate_pnl_series(
            tuple(Decimal(item["equity_net_pnl"]) for item in earnings)
        ),
        "DEFINED_RISK_OPTION": evaluate_pnl_series(
            tuple(Decimal(item["option_net_pnl"]) for item in earnings)
        ),
        "HEDGED_EQUITY": evaluate_pnl_series(
            tuple(Decimal(item["hedged_equity_net_pnl"]) for item in earnings)
        ),
        "NO_TRADE": evaluate_pnl_series(
            tuple(Decimal("0") for _ in earnings)
        ),
    }
    dividend_arm_metrics = {
        "SHARES": evaluate_pnl_series(
            tuple(Decimal(item["share_net_pnl"]) for item in dividend)
        ),
        "LONG_CALL": evaluate_pnl_series(
            tuple(Decimal(item["call_net_pnl"]) for item in dividend)
        ),
        "NO_TRADE": evaluate_pnl_series(
            tuple(Decimal("0") for _ in dividend)
        ),
    }
    arbitrage_policy_pnls = tuple(
        Decimal(item["net_edge"])
        if item["disposition"] == "NET_EDGE_CANDIDATE"
        else Decimal("0")
        for item in arbitrage
    )
    no_trade_controls = (
        sum(item["best_hindsight_arm"] == "NO_TRADE" for item in earnings)
        + sum(item["disposition"] == "NO_TRADE" for item in arbitrage)
        + sum(item["best_hindsight_arm"] == "NO_TRADE" for item in dividend)
        + sum(item["disposition"] == "NO_TRADE" for item in execution)
        + sum(item["disposition"] == "NO_TRADE" for item in futures_events)
        + sum(item["disposition"] == "NO_TRADE" for item in model_governance)
        + sum(item["disposition"] == "NO_TRADE" for item in compliance_controls)
        + sum(item["disposition"] == "NO_TRADE" for item in candidate_pipeline)
    )
    report = {
        "report_type": "synthetic_hypothetical_war_games",
        "version": WAR_GAME_VERSION,
        "environment": "paper",
        "source": "synthetic_fixture",
        "all_declared_scenarios_included": True,
        "fixture_manifest": build_war_game_manifest(),
        "summary": {
            "total_scenario_count": (
                len(results) + len(earnings) + len(arbitrage) + len(dividend)
                + len(execution)
                + len(lifecycle)
                + len(futures_events)
                + len(model_governance)
                + len(compliance_controls)
                + len(premium_timing)
                + len(candidate_pipeline)
            ),
            "scenario_count_by_mvp": {
                "overnight-premium-desk": len(results),
                "earnings-event-desk": len(earnings),
                "arbitrage-observer": len(arbitrage),
                "dividend-opportunity-desk": len(dividend),
                "execution-controls": len(execution),
                "lifecycle-controls": len(lifecycle),
                "event-futures-desk": len(futures_events),
                "open-quant-ai-model-lab": len(model_governance),
                "compliance-controls": len(compliance_controls),
                "premium-timing-controls": len(premium_timing),
                "candidate-pipeline-controls": len(candidate_pipeline),
            },
            "no_trade_control_count": no_trade_controls,
            "premium_fixed_trade": {
                "profitable_scenarios": wins,
                "losing_scenarios": len(results) - wins,
                "mean_pnl": str(sum(pnls, Decimal("0")) / Decimal(len(pnls))),
                "worst_pnl": str(min(pnls)),
                "best_pnl": str(max(pnls)),
                "descriptive_metrics": json_value(premium_metrics),
                "sequence_label": "declared_synthetic_stress_order_not_time_series",
                "statistical_significance_computed": False,
            },
            "earnings_fixed_arm_metrics": json_value(earnings_arm_metrics),
            "arbitrage_policy_metrics": json_value(
                evaluate_pnl_series(arbitrage_policy_pnls)
            ),
            "dividend_fixed_arm_metrics": json_value(dividend_arm_metrics),
            "premium_timing_metrics": json_value(
                evaluate_pnl_series(
                    tuple(
                        Decimal(item["net_pnl_if_closed"])
                        for item in premium_timing
                    )
                )
            ),
        },
        "premium": json_value(results),
        "earnings": earnings,
        "arbitrage": arbitrage,
        "dividend": dividend,
        "execution_controls": execution,
        "lifecycle_controls": lifecycle,
        "futures_events": futures_events,
        "model_governance": model_governance,
        "compliance_controls": compliance_controls,
        "premium_timing": premium_timing,
        "candidate_pipeline": candidate_pipeline,
        "limitations": [
            "These are deterministic synthetic stresses, not historical or live results.",
            "A profitable scenario does not establish strategy expectancy.",
            "Assignment cost is a declared synthetic reserve, not a broker quote.",
        ],
    }
    report["war_game_report_sha256"] = sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return report
