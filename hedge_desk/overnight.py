"""Deterministic paper-only overnight evaluation and morning report."""

from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import os
from typing import Any, Dict, Tuple

from hedge_desk.data import DataArtifact, validate_data_artifact
from hedge_desk.data import SourceBatchResult, SourceBatchStatus, build_batch_manifest
from hedge_desk.data import NewsObservation, NewsTransport, evaluate_news_batch
from hedge_desk.data.contracts import sha256_text
from hedge_desk.demo import (
    FIXTURE_AS_OF,
    FIXTURE_ID,
    FIXTURE_OPTION_PAYLOAD_SHA256,
    FIXTURE_OPTION_SOURCE_ID,
    build_reference_option_snapshot,
    build_reference_market_session_gate,
    build_reference_plan,
    json_value,
)
from hedge_desk.evaluation import (
    Disposition,
    EvaluationLayer,
    EvaluationStatus,
    LayerEvaluation,
    ProjectEvaluation,
)
from hedge_desk.paper import HumanAuthorizationStatus, MachineRiskStatus
from hedge_desk.backoffice import (
    BackOfficeStatus,
    evaluate_paper_reconciliation,
    serialize_paper_reconciliation,
)
from hedge_desk.projects import MVP_PROJECTS, validate_project_registry
from hedge_desk.wargames import build_war_game_report
from hedge_desk.replay import build_replay_evaluation
from hedge_desk.reporting import finalize_report
from hedge_desk.audit import build_audit_evaluation
from hedge_desk.stat_evaluation import build_stat_evaluation
from hedge_desk.portfolio_stress import build_portfolio_stress_report
from hedge_desk.models import (
    ModelTeam,
    build_synthetic_reference_quorum,
    build_synthetic_training_gate,
    build_synthetic_split_gate,
)
from hedge_desk.off_exchange import (
    OtcWeeklyObservation,
    evaluate_otc_weekly_observation,
)
from hedge_desk.earnings import (
    EarningsConsensus,
    EarningsEventInput,
    EarningsRelease,
    evaluate_earnings_surprise,
    evaluate_earnings_universe,
)
from hedge_desk.earnings_experiment import assign_earnings_experiment
from hedge_desk.arbitrage import (
    ArbitrageLeg,
    ArbitragePackage,
    LegSide,
    evaluate_arbitrage_package,
    evaluate_arbitrage_universe,
)
from hedge_desk.dividends import (
    AnnualPayoutObservation,
    CapeObservation,
    DividendCapeInput,
    DividendCompanyHistory,
    evaluate_dividend_cape_universe,
    evaluate_dividend_history,
    evaluate_dividend_universe,
)
from hedge_desk.futures_events import (
    FuturesContractSnapshot,
    FuturesEventCandidate,
    FuturesEventInputs,
    PhysicalEventType,
    evaluate_futures_event,
    evaluate_futures_universe,
)
from hedge_desk.options import (
    build_candidate_control_handoffs,
    evaluate_option_universe,
    evaluate_premium_cadence,
    serialize_premium_cadence,
    scan_vertical_credit_spreads,
)
from hedge_desk.release import build_reference_release_readiness
from hedge_desk.strategic_allocation import (
    AllocationWeight,
    AssetClass,
    evaluate_strategic_allocation,
)


OVERNIGHT_RUNNER_VERSION = "1.0.0"


def _reference_artifact() -> DataArtifact:
    return DataArtifact(
        artifact_id="synthetic-option-chain-v1",
        payload_kind="option_chain",
        source_id=FIXTURE_OPTION_SOURCE_ID,
        license_id="repository-synthetic-fixture",
        source_as_of=FIXTURE_AS_OF,
        received_at=FIXTURE_AS_OF,
        payload_sha256=FIXTURE_OPTION_PAYLOAD_SHA256,
        synthetic=True,
        redistribution_allowed=True,
    )


def _reference_batch() -> Any:
    artifact = _reference_artifact()
    source_hashes = {
        "synthetic-option-chain": artifact.payload_sha256,
        "synthetic-underlying-quote": sha256_text("synthetic-underlying-quote-v1"),
        "synthetic-corporate-events": sha256_text("synthetic-corporate-events-v1"),
        "synthetic-earnings-consensus": "e" * 64,
        "synthetic-earnings-release": "f" * 64,
        "synthetic-arbitrage-legs": sha256_text("synthetic-arbitrage-legs-v1"),
        "synthetic-dividend-history": sha256_text("synthetic-dividend-history-v1"),
        "synthetic-model-governance": sha256_text("synthetic-model-governance-v1"),
        "synthetic-off-exchange": "0" * 63 + "1",
        "synthetic-futures-contract": "5" * 64,
        "synthetic-futures-event": sha256_text("synthetic-futures-event-v1"),
    }
    return build_batch_manifest(
        "synthetic-reference-batch-v1",
        tuple(source_hashes),
        tuple(
            SourceBatchResult(
                source_id,
                SourceBatchStatus.PASS,
                artifact_hash,
            )
            for source_id, artifact_hash in source_hashes.items()
        ),
        sha256_text("paper-source-policy-1.0.0"),
    )


def _model_lab_evaluation(evaluated_at: datetime) -> ProjectEvaluation:
    quorum = build_synthetic_reference_quorum(evaluated_at)
    quant_training = build_synthetic_training_gate(ModelTeam.QUANT)
    ai_training = build_synthetic_training_gate(ModelTeam.AI)
    split_gate = build_synthetic_split_gate(evaluated_at)
    otc = evaluate_otc_weekly_observation(
        OtcWeeklyObservation(
            "synthetic-finra-week", "TEST", "T1", date(2026, 6, 29),
            100000, 1000, evaluated_at - timedelta(days=1),
            evaluated_at - timedelta(days=1), 14, "1" * 64,
        ),
        evaluated_at,
    )
    layers = (
        LayerEvaluation(
            EvaluationLayer.OBSERVED, EvaluationStatus.PASS, (),
            {
                "source": "synthetic_fixture",
                "otc_delayed_aggregate_admissible": str(otc.admissible).lower(),
                "otc_average_shares_per_trade": str(otc.average_shares_per_trade),
                "otc_live_hidden_order_visibility": str(
                    otc.live_hidden_order_visibility
                ).lower(),
            },
            quorum.model_artifact_ids + ("1" * 64,),
        ),
        LayerEvaluation(
            EvaluationLayer.STAT, EvaluationStatus.NOT_REQUIRED,
            ("RESEARCH_LABELS_ONLY",), {},
        ),
        LayerEvaluation(
            EvaluationLayer.BIG, EvaluationStatus.PASS, (),
            {
                "disposition": quorum.disposition,
                "label": quorum.label.value,
                "authoritative_risk_input": str(quorum.authoritative_risk_input).lower(),
                "quant_training_manifest_admissible": str(
                    quant_training.admissible
                ).lower(),
                "ai_training_manifest_admissible": str(
                    ai_training.admissible
                ).lower(),
                "training_trade_authorized": "false",
                "purged_split_admissible": str(split_gate.admissible).lower(),
                "purged_split_artifact": split_gate.artifact_sha256,
                "purged_split_authoritative_risk_input": str(
                    split_gate.authoritative_risk_input
                ).lower(),
                "purged_split_trade_authorized": str(
                    split_gate.trade_authorized
                ).lower(),
                "otc_directional_signal_authorized": str(
                    otc.directional_signal_authorized
                ).lower(),
            },
            quorum.model_artifact_ids + (split_gate.artifact_sha256,),
        ),
        LayerEvaluation(
            EvaluationLayer.DETERMINISTIC_RISK, EvaluationStatus.BLOCKED,
            ("AUTHORITATIVE_RISK_INPUT_ABSENT",), {},
        ),
        LayerEvaluation(
            EvaluationLayer.DETERMINISTIC_COMPLIANCE, EvaluationStatus.NOT_REQUIRED,
            ("RESEARCH_ONLY_NO_TRADE",), {},
        ),
        LayerEvaluation(
            EvaluationLayer.HUMAN, EvaluationStatus.NOT_REQUIRED,
            ("RESEARCH_ONLY_NO_TRADE",), {},
        ),
    )
    return ProjectEvaluation(
        "open-quant-ai-model-lab", evaluated_at, Disposition.NO_TRADE, layers
    )


def _earnings_evaluation(evaluated_at: datetime) -> ProjectEvaluation:
    consensus = EarningsConsensus(
        "TEST", "2026Q2", Decimal("1.00"), Decimal("1000"), 8,
        evaluated_at - timedelta(hours=2), "e" * 64,
    )
    release = EarningsRelease(
        "TEST", "2026Q2", Decimal("1.10"), Decimal("1020"),
        evaluated_at - timedelta(minutes=2),
        evaluated_at - timedelta(minutes=1), "f" * 64,
    )
    result = evaluate_earnings_surprise(consensus, release, evaluated_at)
    universe = evaluate_earnings_universe(
        (
            EarningsEventInput("base-aligned", consensus, release),
            EarningsEventInput(
                "stronger-aligned",
                EarningsConsensus(
                    "STRONG", "2026Q2", Decimal("1.00"), Decimal("1000"), 10,
                    evaluated_at - timedelta(hours=2), "1" * 64,
                ),
                EarningsRelease(
                    "STRONG", "2026Q2", Decimal("1.20"), Decimal("1050"),
                    evaluated_at - timedelta(minutes=2),
                    evaluated_at - timedelta(minutes=1), "2" * 64,
                ),
            ),
            EarningsEventInput(
                "mixed-rejected",
                EarningsConsensus(
                    "MIXED", "2026Q2", Decimal("1.00"), Decimal("1000"), 7,
                    evaluated_at - timedelta(hours=2), "3" * 64,
                ),
                EarningsRelease(
                    "MIXED", "2026Q2", Decimal("1.10"), Decimal("990"),
                    evaluated_at - timedelta(minutes=2),
                    evaluated_at - timedelta(minutes=1), "4" * 64,
                ),
            ),
        ),
        evaluated_at,
    )
    experiment = assign_earnings_experiment(
        "synthetic-earnings-four-arm-v1",
        universe.candidates[0].event_id,
        release.published_at - timedelta(hours=1),
        release.published_at,
        "5" * 64,
    )
    layers = (
        LayerEvaluation(
            EvaluationLayer.OBSERVED,
            EvaluationStatus.PASS if result.admissible else EvaluationStatus.BLOCKED,
            result.reason_codes,
            {
                "source": "synthetic_fixture",
                "eps_surprise_fraction": str(result.eps_surprise_fraction),
                "revenue_surprise_fraction": str(result.revenue_surprise_fraction),
                "surprise_alignment": result.surprise_alignment,
                "universe_candidate_count": str(len(universe.candidates)),
                "universe_rejected_count": str(len(universe.rejected_events)),
                "top_ranked_event": universe.candidates[0].event_id,
                "locked_experiment_arm": experiment.assigned_arm.value,
                "experiment_plan_sha256": experiment.plan_sha256,
            },
            (consensus.source_artifact_sha256, release.source_artifact_sha256),
        ),
        LayerEvaluation(
            EvaluationLayer.STAT, EvaluationStatus.NOT_REQUIRED,
            ("OUT_OF_SAMPLE_REACTION_MODEL_ABSENT",), {},
        ),
        LayerEvaluation(
            EvaluationLayer.BIG, EvaluationStatus.BLOCKED,
            ("PRICE_REACTION_NOT_OBSERVED",),
            {
                "directional_trade_authorized": "false",
                "universe_directional_trade_authorized": str(
                    universe.directional_trade_authorized
                ).lower(),
                "experiment_trade_authorized": str(
                    experiment.trade_authorized
                ).lower(),
            },
        ),
        LayerEvaluation(
            EvaluationLayer.DETERMINISTIC_RISK, EvaluationStatus.BLOCKED,
            ("AUTHORITATIVE_RISK_INPUT_ABSENT",), {},
        ),
        LayerEvaluation(
            EvaluationLayer.DETERMINISTIC_COMPLIANCE, EvaluationStatus.NOT_REQUIRED,
            ("RESEARCH_ONLY_NO_TRADE",), {},
        ),
        LayerEvaluation(
            EvaluationLayer.HUMAN, EvaluationStatus.NOT_REQUIRED,
            ("RESEARCH_ONLY_NO_TRADE",), {},
        ),
    )
    return ProjectEvaluation(
        "earnings-event-desk", evaluated_at, Disposition.NO_TRADE, layers
    )


def _arbitrage_evaluation(evaluated_at: datetime) -> ProjectEvaluation:
    settlement = date(2026, 9, 18)
    legs = (
        ArbitrageLeg("buy-a", LegSide.BUY, Decimal("1.9"), Decimal("2.0"), 5, evaluated_at, settlement, "1" * 64),
        ArbitrageLeg("sell-b", LegSide.SELL, Decimal("1.5"), Decimal("1.6"), 5, evaluated_at, settlement, "2" * 64),
        ArbitrageLeg("sell-c", LegSide.SELL, Decimal("1.2"), Decimal("1.3"), 5, evaluated_at, settlement, "3" * 64),
        ArbitrageLeg("buy-d", LegSide.BUY, Decimal("0.7"), Decimal("0.8"), 5, evaluated_at, settlement, "4" * 64),
    )
    result = evaluate_arbitrage_package(
        legs, 1, 100, Decimal("100"), Decimal("5"), Decimal("5"),
        Decimal("5"), Decimal("20"),
    )
    universe = evaluate_arbitrage_universe(
        (
            ArbitragePackage(
                "synthetic-parity-strong", legs, 1, 100, Decimal("100"),
                Decimal("5"), Decimal("5"), Decimal("5"), Decimal("20"),
            ),
            ArbitragePackage(
                "synthetic-parity-erased", legs, 1, 100, Decimal("30"),
                Decimal("5"), Decimal("5"), Decimal("5"), Decimal("20"),
            ),
        )
    )
    layers = (
        LayerEvaluation(
            EvaluationLayer.OBSERVED,
            EvaluationStatus.PASS if result.admissible else EvaluationStatus.BLOCKED,
            result.reason_codes,
            {
                "source": "synthetic_fixture",
                "executable_entry_cashflow": str(result.executable_entry_cashflow),
                "net_edge": str(result.net_edge),
                "universe_candidate_count": str(len(universe.candidates)),
                "top_ranked_package": universe.candidates[0].package_id,
            },
            tuple(leg.source_artifact_sha256 for leg in legs),
        ),
        LayerEvaluation(
            EvaluationLayer.STAT, EvaluationStatus.NOT_REQUIRED,
            ("SYNTHETIC_IDENTITY_CHECK_ONLY",), {},
        ),
        LayerEvaluation(
            EvaluationLayer.BIG, EvaluationStatus.PASS, (),
            {
                "disposition": result.disposition,
                "trade_authorized": str(result.trade_authorized).lower(),
                "universe_trade_authorized": str(universe.trade_authorized).lower(),
            },
        ),
        LayerEvaluation(
            EvaluationLayer.DETERMINISTIC_RISK, EvaluationStatus.BLOCKED,
            ("AUTHORITATIVE_RISK_INPUT_ABSENT",), {},
        ),
        LayerEvaluation(
            EvaluationLayer.DETERMINISTIC_COMPLIANCE, EvaluationStatus.NOT_REQUIRED,
            ("RESEARCH_ONLY_NO_TRADE",), {},
        ),
        LayerEvaluation(
            EvaluationLayer.HUMAN, EvaluationStatus.NOT_REQUIRED,
            ("RESEARCH_ONLY_NO_TRADE",), {},
        ),
    )
    return ProjectEvaluation(
        "arbitrage-observer", evaluated_at, Disposition.NO_TRADE, layers
    )


def _dividend_evaluation(evaluated_at: datetime) -> ProjectEvaluation:
    history = tuple(
        AnnualPayoutObservation(
            2016 + index,
            Decimal("1") + Decimal(index) / Decimal("10"),
            Decimal("4"), Decimal("50"), Decimal("100"), Decimal("25"),
            Decimal("10000"),
            evaluated_at - timedelta(days=365 * (10 - index)),
            format(index + 1, "x") * 64,
        )
        for index in range(10)
    )
    result = evaluate_dividend_history(history, evaluated_at)
    efficient_history = tuple(
        AnnualPayoutObservation(
            item.fiscal_year,
            item.dividends_per_share * Decimal("1.2"),
            Decimal("8"),
            item.average_share_price,
            item.buybacks,
            item.issuance,
            item.market_cap,
            item.available_at,
            item.source_artifact_sha256,
        )
        for item in history
    )
    universe = evaluate_dividend_universe(
        (
            DividendCompanyHistory("TEST", history),
            DividendCompanyHistory("TEST-EFFICIENT", efficient_history),
        ),
        evaluated_at,
    )
    cape_universe = evaluate_dividend_cape_universe(
        (
            DividendCapeInput(
                DividendCompanyHistory("TEST", history),
                CapeObservation(
                    "TEST", Decimal("30"), evaluated_at - timedelta(days=1),
                    evaluated_at, "a" * 64,
                ),
            ),
            DividendCapeInput(
                DividendCompanyHistory("TEST-EFFICIENT", efficient_history),
                CapeObservation(
                    "TEST-EFFICIENT", Decimal("15"),
                    evaluated_at - timedelta(days=1), evaluated_at, "b" * 64,
                ),
            ),
        ),
        evaluated_at,
    )
    layers = (
        LayerEvaluation(
            EvaluationLayer.OBSERVED,
            EvaluationStatus.PASS if result.admissible else EvaluationStatus.BLOCKED,
            result.reason_codes,
            {
                "source": "synthetic_fixture",
                "ten_year_average_dividend_yield": str(result.ten_year_average_dividend_yield),
                "ten_year_average_payout_ratio": str(result.ten_year_average_payout_ratio),
                "ten_year_average_net_shareholder_yield": str(result.ten_year_average_net_shareholder_yield),
                "dividend_cut_count": str(result.dividend_cut_count),
                "universe_candidate_count": str(len(universe.candidates)),
                "top_ranked_symbol": universe.candidates[0].symbol,
                "ranking_basis": "ten_year_yield_per_payout_ratio",
                "cape_candidate_count": str(len(cape_universe.candidates)),
                "cape_top_ranked_symbol": cape_universe.candidates[0].symbol,
                "cape_ranking_basis": "yield_per_payout_ratio_divided_by_cape",
            },
            tuple(item.source_artifact_sha256 for item in history),
        ),
        LayerEvaluation(
            EvaluationLayer.STAT, EvaluationStatus.NOT_REQUIRED,
            ("CROSS_SECTIONAL_OUT_OF_SAMPLE_MODEL_ABSENT",), {},
        ),
        LayerEvaluation(
            EvaluationLayer.BIG, EvaluationStatus.PASS, (),
            {
                "long_call_cash_dividend_entitlement": str(
                    result.long_call_cash_dividend_entitlement
                ),
                "trade_authorized": str(result.trade_authorized).lower(),
                "universe_trade_authorized": str(universe.trade_authorized).lower(),
                "cape_trade_authorized": str(cape_universe.trade_authorized).lower(),
            },
        ),
        LayerEvaluation(
            EvaluationLayer.DETERMINISTIC_RISK, EvaluationStatus.BLOCKED,
            ("AUTHORITATIVE_RISK_INPUT_ABSENT",), {},
        ),
        LayerEvaluation(
            EvaluationLayer.DETERMINISTIC_COMPLIANCE, EvaluationStatus.NOT_REQUIRED,
            ("RESEARCH_ONLY_NO_TRADE",), {},
        ),
        LayerEvaluation(
            EvaluationLayer.HUMAN, EvaluationStatus.NOT_REQUIRED,
            ("RESEARCH_ONLY_NO_TRADE",), {},
        ),
    )
    return ProjectEvaluation(
        "dividend-opportunity-desk", evaluated_at, Disposition.NO_TRADE, layers
    )


def _futures_event_evaluation(evaluated_at: datetime) -> ProjectEvaluation:
    news = evaluate_news_batch(
        (
            NewsObservation(
                "synthetic-shipping-news",
                "synthetic-public-agency",
                "https://example.com/synthetic/shipping-event",
                "repository-synthetic-fixture",
                NewsTransport.PUBLIC_AGENCY_FEED,
                evaluated_at - timedelta(minutes=3),
                evaluated_at - timedelta(minutes=2),
                "d" * 64,
                True,
                True,
            ),
        ),
        evaluated_at,
        300,
    )
    contract = FuturesContractSnapshot(
        "CASH-SETTLED-SYNTHETIC-FUT", 5000, Decimal("5000"), False, True,
        "5" * 64,
    )
    event = FuturesEventInputs(
        "synthetic-shipping-disruption",
        PhysicalEventType.SHIPPING_DISRUPTION,
        evaluated_at - timedelta(minutes=2),
        evaluated_at - timedelta(minutes=1),
        Decimal("1000"), Decimal("400"), Decimal("100"), Decimal("50"),
        Decimal("50"), "6" * 64, "7" * 64,
    )
    result = evaluate_futures_event(
        contract, event, evaluated_at, Decimal("300")
    )
    universe = evaluate_futures_universe(
        (
            FuturesEventCandidate(contract, event),
            FuturesEventCandidate(
                contract,
                FuturesEventInputs(
                    "synthetic-weather-priced",
                    PhysicalEventType.EXTREME_WEATHER,
                    evaluated_at - timedelta(minutes=3),
                    evaluated_at - timedelta(minutes=1),
                    Decimal("700"), Decimal("600"), Decimal("50"),
                    Decimal("25"), Decimal("25"), "8" * 64, "9" * 64,
                ),
            ),
        ),
        evaluated_at,
        Decimal("300"),
    )
    layers = (
        LayerEvaluation(
            EvaluationLayer.OBSERVED,
            EvaluationStatus.PASS if result.admissible else EvaluationStatus.BLOCKED,
            result.reason_codes,
            {
                "source": "synthetic_fixture",
                "event_type": event.event_type.value,
                "residual_edge_per_contract": str(result.residual_edge_per_contract),
                "universe_candidate_count": str(len(universe.candidates)),
                "universe_rejected_count": str(len(universe.rejected_events)),
                "top_ranked_event": universe.candidates[0].event_id,
                "news_evidence_admissible": str(news.admissible).lower(),
                "news_research_evidence_only": str(
                    news.research_evidence_only
                ).lower(),
            },
            (
                contract.source_artifact_sha256,
                event.source_artifact_sha256,
                event.impact_model_artifact_sha256,
            ),
        ),
        LayerEvaluation(
            EvaluationLayer.STAT, EvaluationStatus.NOT_REQUIRED,
            ("OUT_OF_SAMPLE_EVENT_MODEL_ABSENT",), {},
        ),
        LayerEvaluation(
            EvaluationLayer.BIG, EvaluationStatus.PASS, (),
            {
                "disposition": result.disposition,
                "trade_authorized": str(result.trade_authorized).lower(),
                "universe_trade_authorized": str(universe.trade_authorized).lower(),
                "news_trade_authorized": str(news.trade_authorized).lower(),
            },
        ),
        LayerEvaluation(
            EvaluationLayer.DETERMINISTIC_RISK, EvaluationStatus.BLOCKED,
            ("FUTURES_RISK_AND_MARGIN_ARTIFACT_ABSENT",), {},
        ),
        LayerEvaluation(
            EvaluationLayer.DETERMINISTIC_COMPLIANCE, EvaluationStatus.BLOCKED,
            ("FUTURES_PAPER_RESEARCH_ONLY",), {},
        ),
        LayerEvaluation(
            EvaluationLayer.HUMAN, EvaluationStatus.NOT_REQUIRED,
            ("RESEARCH_ONLY_NO_TRADE",), {},
        ),
    )
    return ProjectEvaluation(
        "event-futures-desk", evaluated_at, Disposition.NO_TRADE, layers
    )


def evaluate_reference_projects() -> Tuple[ProjectEvaluation, ...]:
    """Evaluate every registered project without inventing unbuilt strategies."""
    validate_project_registry()
    artifact = _reference_artifact()
    data_gate = validate_data_artifact(artifact, FIXTURE_AS_OF, maximum_age_seconds=0)
    plan = build_reference_plan()
    scan = scan_vertical_credit_spreads(build_reference_option_snapshot(), FIXTURE_AS_OF)
    handoffs = build_candidate_control_handoffs(
        scan, build_reference_market_session_gate()
    )
    base_snapshot = build_reference_option_snapshot()
    stronger_snapshot = replace(
        base_snapshot,
        underlying_quote=replace(base_snapshot.underlying_quote, symbol="STRONG"),
        option_quotes=tuple(
            replace(
                item,
                underlying="STRONG",
                bid=item.bid + (Decimal("1") if index == 0 else Decimal("0")),
                ask=item.ask + (Decimal("1") if index == 0 else Decimal("0")),
            )
            for index, item in enumerate(base_snapshot.option_quotes)
        ),
        source_artifact_sha256="c" * 64,
    )
    option_universe = evaluate_option_universe(
        (base_snapshot, stronger_snapshot),
        FIXTURE_AS_OF,
        build_reference_market_session_gate(),
    )
    strategic_allocation = evaluate_strategic_allocation(
        (
            AllocationWeight(AssetClass.US_EQUITY, Decimal("0.25")),
            AllocationWeight(AssetClass.INTERNATIONAL_EQUITY, Decimal("0.20")),
            AllocationWeight(AssetClass.FIXED_INCOME, Decimal("0.25")),
            AllocationWeight(AssetClass.REAL_ASSET, Decimal("0.20")),
            AllocationWeight(AssetClass.CASH, Decimal("0.10")),
        ),
        Decimal("35"),
    )
    cadence = evaluate_premium_cadence(
        FIXTURE_AS_OF, FIXTURE_AS_OF - timedelta(days=30)
    )
    observed = LayerEvaluation(
        EvaluationLayer.OBSERVED,
        EvaluationStatus.PASS if data_gate.admissible else EvaluationStatus.BLOCKED,
        data_gate.reason_codes,
        {
            "synthetic": "true",
            "net_credit": str(plan.spread.net_credit),
            "maximum_loss": str(plan.spread.maximum_loss),
            "break_even": str(plan.spread.break_even),
            "days_to_expiration": str(plan.spread.days_to_expiration),
            "planned_exit_date": plan.spread.planned_exit_date.isoformat(),
            "event_calendar_complete_through": plan.event_calendar_gate.complete_through.isoformat(),
            "enumerated_vertical_pairs": str(scan.pair_count),
            "admissible_vertical_pairs": str(scan.admissible_count),
            "underlying_universe_candidate_count": str(
                len(option_universe.candidates)
            ),
            "top_ranked_underlying": option_universe.candidates[0].symbol,
            "underlying_ranking_basis": option_universe.ranking_basis,
        },
        (
            artifact.artifact_id,
            artifact.payload_sha256,
            plan.event_calendar_gate.calendar_sha256,
        ),
    )
    # No statistical inference is claimed by this executable-side reference case.
    stat = LayerEvaluation(
        EvaluationLayer.STAT,
        EvaluationStatus.NOT_REQUIRED,
        ("REFERENCE_ECONOMICS_ONLY",),
        {},
    )
    big = LayerEvaluation(
        EvaluationLayer.BIG,
        EvaluationStatus.PASS if cadence.new_entry_evaluation_allowed
        else EvaluationStatus.BLOCKED,
        cadence.reason_codes,
        {
            "proposal": "defined-risk synthetic put credit spread",
            "candidate_handoff_count": str(len(handoffs)),
            "handoff_next_action": handoffs[0].next_action,
            "handoff_trade_authorized": str(handoffs[0].trade_authorized).lower(),
            "handoff_calculation_artifact": handoffs[0].calculation_sha256,
            "underlying_universe_probability_inferred": str(
                option_universe.probability_inferred
            ).lower(),
            "underlying_universe_trade_authorized": str(
                option_universe.trade_authorized
            ).lower(),
            "monthly_new_entry_evaluation_allowed": str(
                cadence.new_entry_evaluation_allowed
            ).lower(),
            "continuous_monitoring_allowed": str(
                cadence.monitoring_allowed
            ).lower(),
            "cadence_trade_authorized": str(cadence.trade_authorized).lower(),
            "cadence_artifact": cadence.artifact_sha256,
        },
        (FIXTURE_ID, handoffs[0].handoff_sha256, cadence.artifact_sha256),
    )
    risk_pass = (
        plan.machine_risk_status is MachineRiskStatus.PASS
        and strategic_allocation.admissible
    )
    risk = LayerEvaluation(
        EvaluationLayer.DETERMINISTIC_RISK,
        EvaluationStatus.PASS if risk_pass else EvaluationStatus.BLOCKED,
        plan.reason_codes,
        {
            "risk_artifact": plan.plan_hash,
            "risk_input_artifact": plan.risk_decision.risk_input_sha256,
            "risk_source_artifact": plan.risk_decision.risk_source_artifact_sha256,
            "risk_of_ruin": str(plan.risk_decision.risk_of_ruin_after),
            "risk_model_id": plan.risk_decision.risk_model_id,
            "risk_model_version": plan.risk_decision.risk_model_version,
            "strategic_allocation_admissible": str(
                strategic_allocation.admissible
            ).lower(),
            "strategic_allocation_artifact": strategic_allocation.artifact_sha256,
            "strategic_allocation_cape": str(strategic_allocation.cape_ratio),
            "strategic_allocation_trade_authorized": str(
                strategic_allocation.trade_authorized
            ).lower(),
        },
        (
            plan.risk_decision.risk_input_sha256,
            plan.plan_hash,
            strategic_allocation.artifact_sha256,
        ),
    )
    reconciliation = evaluate_paper_reconciliation(
        plan.plan_hash,
        plan.compliance_decision.portfolio_snapshot_sha256,
        plan.compliance_decision.portfolio_snapshot_sha256,
        Decimal("100000"),
        Decimal("100000"),
        0,
        0,
        FIXTURE_AS_OF,
    )
    compliance_pass = (
        plan.compliance_decision.status is BackOfficeStatus.PASS
        and reconciliation.status is BackOfficeStatus.PASS
    )
    compliance = LayerEvaluation(
        EvaluationLayer.DETERMINISTIC_COMPLIANCE,
        EvaluationStatus.PASS if compliance_pass else EvaluationStatus.BLOCKED,
        tuple(sorted(set(
            plan.compliance_decision.reason_codes + reconciliation.reason_codes
        ))),
        {
            "policy_version": plan.compliance_decision.policy_version,
            "regulatory_traceability_sha256": (
                plan.compliance_decision.policy_decision.regulatory_traceability_sha256
            ),
            "paper_reconciliation_status": reconciliation.status.value,
            "paper_reconciliation_artifact": reconciliation.artifact_sha256,
            "paper_reconciliation_positions_artifact": (
                reconciliation.internal_positions_sha256
            ),
            "paper_reconciliation_live_release_eligible": str(
                reconciliation.live_release_evidence_eligible
            ).lower(),
        },
        (
            plan.plan_hash,
            plan.compliance_decision.policy_decision.regulatory_traceability_sha256,
            reconciliation.artifact_sha256,
        ),
    )
    human_pending = plan.authorization.status is HumanAuthorizationStatus.PENDING
    human = LayerEvaluation(
        EvaluationLayer.HUMAN,
        EvaluationStatus.PENDING if human_pending else EvaluationStatus.BLOCKED,
        ("HUMAN_AUTHORIZATION_REQUIRED",) if human_pending else (),
        {},
        (plan.plan_hash,),
    )
    premium = ProjectEvaluation(
        MVP_PROJECTS[0].project_id,
        FIXTURE_AS_OF,
        Disposition.HUMAN_REVIEW
        if data_gate.admissible and risk_pass and compliance_pass
        else Disposition.NO_TRADE,
        (observed, stat, big, risk, compliance, human),
    )
    return (
        (
            premium,
            _earnings_evaluation(FIXTURE_AS_OF),
            _arbitrage_evaluation(FIXTURE_AS_OF),
            _dividend_evaluation(FIXTURE_AS_OF),
        )
        + (
            _model_lab_evaluation(FIXTURE_AS_OF),
            _futures_event_evaluation(FIXTURE_AS_OF),
        )
    )


def build_morning_report(
    generated_at: datetime, code_commit: str = "LOCAL_UNSPECIFIED"
) -> Dict[str, Any]:
    if generated_at.tzinfo is None:
        raise ValueError("report timestamp must be timezone-aware")
    if not code_commit:
        raise ValueError("report code commit identity is required")
    evaluations = evaluate_reference_projects()
    human_review = sum(
        evaluation.disposition is Disposition.HUMAN_REVIEW
        for evaluation in evaluations
    )
    no_trade = sum(
        evaluation.disposition is Disposition.NO_TRADE for evaluation in evaluations
    )
    report = {
        "report_type": "paper_hypothetical_morning_evaluation",
        "runner_version": OVERNIGHT_RUNNER_VERSION,
        "code_commit": code_commit,
        "generated_at": generated_at.isoformat(),
        "environment": "paper",
        "complete": True,
        "live_orders_enabled": False,
        "real_money_pnl": "0",
        "real_trades_executed": 0,
        "summary": {
            "projects_evaluated": len(evaluations),
            "human_review": human_review,
            "no_trade": no_trade,
        },
        "limitations": [
            "Synthetic fixtures only; no current market opportunity is claimed.",
            "Hypothetical paper output is not investment advice or a performance guarantee.",
            "Research-only foundations correctly return NO_TRADE without validated risk inputs.",
        ],
        "projects": json_value(evaluations),
        "data_batch": json_value(_reference_batch()),
        "war_games": build_war_game_report(),
        "chronological_replay": build_replay_evaluation(),
        "audit_chain": build_audit_evaluation(),
        "back_office_reconciliation": serialize_paper_reconciliation(
            evaluate_paper_reconciliation(
                evaluations[0].layers[3].metrics["risk_artifact"],
                evaluations[0].layers[4].metrics[
                    "paper_reconciliation_positions_artifact"
                ],
                evaluations[0].layers[4].metrics[
                    "paper_reconciliation_positions_artifact"
                ],
                Decimal("100000"),
                Decimal("100000"),
                0,
                0,
                FIXTURE_AS_OF,
            )
        ),
        "premium_cadence": serialize_premium_cadence(
            evaluate_premium_cadence(
                FIXTURE_AS_OF, FIXTURE_AS_OF - timedelta(days=30)
            )
        ),
        "stat_evaluation": build_stat_evaluation(),
        "portfolio_stress": build_portfolio_stress_report(),
        "release_readiness": json_value(build_reference_release_readiness()),
    }
    return finalize_report(report)


def current_morning_report() -> Dict[str, Any]:
    return build_morning_report(
        datetime.now(timezone.utc),
        os.environ.get("HEDGE_DESK_CODE_COMMIT", "LOCAL_UNSPECIFIED"),
    )
