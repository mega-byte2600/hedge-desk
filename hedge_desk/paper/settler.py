"""Read-only market-data settler for paper outcomes (automation track, Move #3).

Closes the feedback loop opened by the paper lifecycle runner
(:mod:`hedge_desk.paper.runner`): after a human closes a paper position, or an
OPEN plan reaches expiration, this module derives the OBSERVED outcome from
read-only market data (or from the recorded human close) and appends it to the
paper outcome log (:mod:`hedge_desk.paper_log`).

Outcome mapping (deterministic, no inference):
- CLOSED plan with a close artifact: CLOSED_GAIN if the recorded
  realized_pnl > 0, CLOSED_LOSS if < 0, and STOPPED with reason code
  ZERO_PNL_CLOSE if exactly zero.
- OPEN plan at/past expiration, observed via the injected market-data
  provider: EXPIRED_WORTHLESS when the short leg expired OTM (observed short
  intrinsic is zero), ASSIGNED when the short leg expired ITM (observed short
  intrinsic is positive).
- Anything unverifiable: UNKNOWN, never a guess.

Honesty and safety:
- Read-only market data only: the provider is an injected callable and the
  default provider returns all-None, so the settler records UNKNOWN rather
  than guessing when market data is absent.
- Outcomes for CLOSED plans come from the recorded human PaperClose, never
  from a model.
- Idempotent: a (plan_id, outcome) pair already present in the paper log is
  never recorded twice.
- Paper only: the runner state and every artifact are refused unless stamped
  ``environment == "paper"``. This module never touches live orders,
  brokerage credentials, or the authoritative Risk of Ruin.
- Money stays in :class:`~decimal.Decimal`; every settlement keeps reason
  codes and provenance.
"""

from __future__ import annotations

import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple

from hedge_desk import paper_log
from hedge_desk.paper.runner import (
    RUNNER_ENVIRONMENT,
    STATUS_CLOSED,
    STATUS_OPEN,
    _load_state,
)
from hedge_desk.paper.review import load_plan_file
from hedge_desk.paper.workflow import PaperTradePlan

SETTLER_SCHEMA_VERSION = "paper-settler-1.0.0"

# Layout inside the state directory: the runner state file, the plan files the
# runner ticks, and the human close artifacts.
STATE_FILE_NAME = "state.json"
PLANS_SUBDIR = "plans"
CLOSES_SUBDIR = "closes"

# The paper workflow only ever produces vertical credit spreads, so the
# paper-log strategy label for a settled plan is this fixed, documented
# mapping — not an inference about the trade.
PAPER_LOG_STRATEGY = "CREDIT_SPREAD"

#: Observed expiration data for one plan. ``underlying_close`` is the
#: observed underlying close at expiration; ``short_intrinsic`` is the
#: observed intrinsic value of the short leg at expiration. ``None`` means
#: unverifiable — the settler records UNKNOWN, never a guess.
MarketDataProvider = Callable[
    [PaperTradePlan], Optional[Mapping[str, Any]]
]


def _default_market_data_provider(
    plan: PaperTradePlan,
) -> Mapping[str, None]:
    """Fail-closed default: no market data is observed, all fields None."""
    return {"underlying_close": None, "short_intrinsic": None}


def _require_tz_aware(moment: datetime, label: str) -> datetime:
    if moment.tzinfo is None:
        raise ValueError(f"{label} must be timezone-aware")
    return moment


def _outcome_for_realized_pnl(
    realized_pnl: Decimal,
) -> Tuple[str, Tuple[str, ...]]:
    """Map a recorded paper-close P&L to its outcome, deterministically."""
    if realized_pnl > 0:
        return "CLOSED_GAIN", ("REALIZED_PNL_GAIN",)
    if realized_pnl < 0:
        return "CLOSED_LOSS", ("REALIZED_PNL_LOSS",)
    return "STOPPED", ("ZERO_PNL_CLOSE",)


def _observed_decimal(value: Any) -> Optional[Decimal]:
    """Coerce an observed market-data value to Decimal; None when unusable."""
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, Decimal):
        return value if value.is_finite() else None
    if isinstance(value, (int, float)):
        try:
            parsed = Decimal(str(value))
        except InvalidOperation:
            return None
        return parsed if parsed.is_finite() else None
    return None


def _observe_expiration_outcome(
    market_data: Optional[Mapping[str, Any]],
) -> Tuple[str, Tuple[str, ...], Dict[str, str]]:
    """Derive the expiration outcome from observed data only.

    EXPIRED_WORTHLESS when the short leg expired OTM (observed short
    intrinsic is zero); ASSIGNED when the short leg expired ITM (observed
    short intrinsic is positive); UNKNOWN whenever the observation is
    missing, malformed, or physically impossible (negative intrinsic).
    """
    if not isinstance(market_data, Mapping):
        return "UNKNOWN", ("MARKET_DATA_PROVIDER_INVALID",), {}
    underlying_close = _observed_decimal(market_data.get("underlying_close"))
    short_intrinsic = _observed_decimal(market_data.get("short_intrinsic"))
    if underlying_close is None or short_intrinsic is None:
        return "UNKNOWN", ("MARKET_DATA_UNAVAILABLE",), {}
    if short_intrinsic < 0:
        # Intrinsic value cannot be negative; a negative reading is malformed
        # provider data, so fail closed to UNKNOWN rather than guessing.
        return "UNKNOWN", ("NEGATIVE_SHORT_INTRINSIC",), {}
    observed = {
        "underlying_close": str(underlying_close),
        "short_intrinsic": str(short_intrinsic),
    }
    if short_intrinsic == 0:
        return "EXPIRED_WORTHLESS", ("SHORT_LEG_EXPIRED_OTM",), observed
    return "ASSIGNED", ("SHORT_LEG_EXPIRED_ITM",), observed


def _load_plan(
    plans_dir: Path, plan_id: str, entry: Mapping[str, Any]
) -> Tuple[Optional[PaperTradePlan], Optional[str]]:
    """Load the plan file for a state entry; return (plan, failure_code)."""
    plan_path = plans_dir / f"{plan_id}.json"
    if not plan_path.is_file():
        return None, "PLAN_FILE_NOT_FOUND"
    try:
        plan = load_plan_file(plan_path)
    except (ValueError, KeyError, json.JSONDecodeError):
        return None, "PLAN_FILE_LOAD_FAILED"
    if plan.plan_hash != entry.get("plan_hash"):
        return None, "STATE_PLAN_HASH_MISMATCH"
    return plan, None


def _parse_optional_datetime(value: Any) -> Tuple[Optional[datetime], bool]:
    """Parse an ISO-8601 timestamp; (None, False) when unparseable."""
    if not isinstance(value, str):
        return None, False
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None, False
    if parsed.tzinfo is None:
        return None, False
    return parsed, True


def _already_settled(
    paper_log_path: Path, plan_id: str, outcome: str
) -> bool:
    """Idempotency gate: never record the same (plan_id, outcome) twice."""
    for existing in paper_log.read_log(paper_log_path):
        if (
            existing.get("candidate_id") == plan_id
            and existing.get("outcome") == outcome
        ):
            return True
    return False


def _record_once(
    *,
    paper_log_path: Path,
    plan_id: str,
    symbol: str,
    outcome: str,
    reason_codes: Tuple[str, ...],
    provenance: Dict[str, Any],
    entered_at: Optional[datetime],
    exit_price: Optional[str],
    premium_received: Optional[str],
    now: datetime,
    report: Dict[str, List[Dict[str, Any]]],
) -> None:
    """Append one outcome to the paper log unless already recorded."""
    if _already_settled(paper_log_path, plan_id, outcome):
        report["skipped"].append(
            {
                "plan_id": plan_id,
                "outcome": outcome,
                "reason_codes": ["ALREADY_SETTLED"],
            }
        )
        return
    logged = paper_log.append_outcome(
        paper_log_path,
        candidate_id=plan_id,
        symbol=symbol,
        strategy=PAPER_LOG_STRATEGY,
        outcome=outcome,
        entered_at=entered_at,
        exit_price=exit_price,
        premium_received=premium_received,
        recorded_at=now,
        provenance=provenance,
    )
    bucket = "unknown" if outcome == "UNKNOWN" else "settled"
    report[bucket].append(
        {
            "plan_id": plan_id,
            "outcome": outcome,
            "reason_codes": list(reason_codes),
            "log_seq": logged["seq"],
            "entry_sha256": logged["entry_sha256"],
        }
    )


def _skipped(
    report: Dict[str, List[Dict[str, Any]]],
    plan_id: str,
    reason_code: str,
    outcome: Optional[str] = None,
) -> None:
    entry: Dict[str, Any] = {"plan_id": plan_id, "reason_codes": [reason_code]}
    if outcome is not None:
        entry["outcome"] = outcome
    report["skipped"].append(entry)


def _settle_closed_plan(
    *,
    state_dir: Path,
    plans_dir: Path,
    plan_id: str,
    entry: Mapping[str, Any],
    paper_log_path: Path,
    now: datetime,
    report: Dict[str, List[Dict[str, Any]]],
) -> None:
    """Settle a CLOSED plan from its recorded human close artifact."""
    artifact_path = state_dir / CLOSES_SUBDIR / f"{plan_id}.json"
    if not artifact_path.is_file():
        _skipped(report, plan_id, "CLOSE_ARTIFACT_MISSING", outcome=None)
        return
    try:
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        _skipped(report, plan_id, "CLOSE_ARTIFACT_UNREADABLE")
        return
    if artifact.get("environment") != RUNNER_ENVIRONMENT:
        _skipped(report, plan_id, "NON_PAPER_CLOSE_ARTIFACT")
        return
    close = artifact.get("close")
    decision = artifact.get("decision")
    if not isinstance(close, dict) or not isinstance(decision, dict):
        _skipped(report, plan_id, "CLOSE_ARTIFACT_MALFORMED")
        return
    if close.get("plan_id") != plan_id:
        _skipped(report, plan_id, "CLOSE_ARTIFACT_PLAN_MISMATCH")
        return
    try:
        realized_pnl = Decimal(str(close["realized_pnl"]))
    except (KeyError, InvalidOperation, ValueError):
        _skipped(report, plan_id, "CLOSE_PNL_UNPARSEABLE")
        return
    plan, failure = _load_plan(plans_dir, plan_id, entry)
    if failure is not None:
        _skipped(report, plan_id, failure)
        return
    assert plan is not None
    outcome, reason_codes = _outcome_for_realized_pnl(realized_pnl)

    open_record = entry.get("open") or {}
    entered_at, entered_ok = _parse_optional_datetime(open_record.get("opened_at"))
    codes = list(reason_codes)
    if not entered_ok:
        codes.append("OPENED_AT_UNPARSEABLE")
    provenance: Dict[str, Any] = {
        "settler": SETTLER_SCHEMA_VERSION,
        "settled_at": now.isoformat(),
        "source": "recorded-human-paper-close",
        "plan_id": plan_id,
        "plan_hash": entry.get("plan_hash"),
        "close_sha256": close.get("close_sha256"),
        "exit_evaluation_sha256": close.get("exit_evaluation_sha256"),
        "human_id": decision.get("human_id"),
        "decided_at": decision.get("decided_at"),
        "reason_codes": list(decision.get("reason_codes") or []),
    }
    _record_once(
        paper_log_path=paper_log_path,
        plan_id=plan_id,
        symbol=plan.spread.underlying,
        outcome=outcome,
        reason_codes=tuple(codes),
        provenance=provenance,
        entered_at=entered_at,
        exit_price=close.get("exit_debit"),
        premium_received=open_record.get("entry_credit"),
        now=now,
        report=report,
    )


def _settle_open_plan(
    *,
    plans_dir: Path,
    plan_id: str,
    entry: Mapping[str, Any],
    market_data_provider: MarketDataProvider,
    paper_log_path: Path,
    now: datetime,
    report: Dict[str, List[Dict[str, Any]]],
) -> None:
    """Settle an OPEN plan at/past expiration from observed market data."""
    plan, failure = _load_plan(plans_dir, plan_id, entry)
    if failure is not None:
        _skipped(report, plan_id, failure)
        return
    assert plan is not None
    expiration = plan.spread.expiration_date
    if now.date() < expiration:
        _skipped(report, plan_id, "NOT_AT_EXPIRATION")
        return
    try:
        market_data = market_data_provider(plan)
    except Exception:
        outcome, reason_codes, observed = (
            "UNKNOWN",
            ("MARKET_DATA_PROVIDER_FAILED",),
            {},
        )
    else:
        outcome, reason_codes, observed = _observe_expiration_outcome(market_data)

    open_record = entry.get("open") or {}
    entered_at, entered_ok = _parse_optional_datetime(open_record.get("opened_at"))
    codes = list(reason_codes)
    if not entered_ok:
        codes.append("OPENED_AT_UNPARSEABLE")
    provenance: Dict[str, Any] = {
        "settler": SETTLER_SCHEMA_VERSION,
        "settled_at": now.isoformat(),
        "source": "observed-market-data-at-expiration",
        "plan_id": plan_id,
        "plan_hash": plan.plan_hash,
        "expiration_date": expiration.isoformat(),
        "underlying": plan.spread.underlying,
        **observed,
    }
    _record_once(
        paper_log_path=paper_log_path,
        plan_id=plan_id,
        symbol=plan.spread.underlying,
        outcome=outcome,
        reason_codes=tuple(codes),
        provenance=provenance,
        entered_at=entered_at,
        exit_price=None,
        premium_received=open_record.get("entry_credit"),
        now=now,
        report=report,
    )


def settle_paper_outcomes(
    state_dir: Any,
    paper_log_path: Any,
    market_data_provider: Optional[MarketDataProvider] = None,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """Settle paper outcomes from the runner state into the paper outcome log.

    ``state_dir`` is the runner lifecycle directory holding ``state.json``,
    ``plans/`` (the plan files the runner ticks), and ``closes/`` (the human
    close artifacts). For each plan:

    - CLOSED with a close artifact: derive the outcome from the recorded
      PaperClose (CLOSED_GAIN / CLOSED_LOSS / STOPPED on exactly-zero P&L).
    - OPEN at/past expiration: observe expiration market data through
      ``market_data_provider(plan)`` (EXPIRED_WORTHLESS / ASSIGNED / UNKNOWN).
    - Anything else (pending plans, OPEN plans before expiration, missing
      artifacts or plan files, already-settled outcomes) is reported in
      ``skipped`` with reason codes — never settled.

    Returns a settlement report ``{"settled", "unknown", "skipped",
    "environment", "settler"}``. Every outcome is recorded through
    :func:`hedge_desk.paper_log.append_outcome` with full provenance.
    """
    if now is None:
        raise ValueError("a timezone-aware `now` is required")
    _require_tz_aware(now, "settlement timestamp")
    provider = market_data_provider or _default_market_data_provider

    root = Path(state_dir)
    state_path = root / STATE_FILE_NAME
    if not state_path.is_file():
        raise ValueError(f"runner state file not found: {state_path}")
    # Validates the schema version and refuses non-paper state.
    state = _load_state(state_path)

    plans_dir = root / PLANS_SUBDIR
    log_path = Path(paper_log_path)

    report: Dict[str, Any] = {
        "settled": [],
        "unknown": [],
        "skipped": [],
        "environment": RUNNER_ENVIRONMENT,
        "settler": SETTLER_SCHEMA_VERSION,
    }
    plans = state.get("plans")
    if not isinstance(plans, dict):
        raise ValueError("runner state is missing its plans map")
    for plan_id in sorted(plans):
        entry = plans[plan_id]
        if not isinstance(entry, dict):
            _skipped(report, plan_id, "STATE_ENTRY_MALFORMED")
            continue
        status = entry.get("status")
        if status == STATUS_CLOSED:
            _settle_closed_plan(
                state_dir=root,
                plans_dir=plans_dir,
                plan_id=plan_id,
                entry=entry,
                paper_log_path=log_path,
                now=now,
                report=report,
            )
        elif status == STATUS_OPEN:
            _settle_open_plan(
                plans_dir=plans_dir,
                plan_id=plan_id,
                entry=entry,
                market_data_provider=provider,
                paper_log_path=log_path,
                now=now,
                report=report,
            )
        else:
            _skipped(report, plan_id, "PLAN_NOT_OPEN_OR_CLOSED")
    return report


__all__ = [
    "SETTLER_SCHEMA_VERSION",
    "PAPER_LOG_STRATEGY",
    "settle_paper_outcomes",
]
