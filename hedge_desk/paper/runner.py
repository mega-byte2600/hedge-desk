"""Fail-closed paper lifecycle runner for the 15-minute cadence.

The runner chains the paper lifecycle on an injected clock: each tick it scans
a directory of approved paper plan files, advances PENDING_OPEN plans to OPEN
when the fill check passes, and monitors OPEN plans through
``evaluate_plan_lifecycle``. The runner only ever opens and monitors — it
never auto-closes and never auto-acts on an escalation. Only a human closes,
via :func:`close_paper_position`.

Determinism rules:
- No wall-clock reads except the explicitly passed ``now``.
- Money stays in :class:`~decimal.Decimal`; serialization writes Decimals as
  strings and datetimes as ISO-8601.
- Every decision keeps reason codes; every failure path fails closed.

Paper boundary:
- The state file and every artifact are refused unless stamped with
  ``environment == "paper"``. This module never touches live orders,
  brokerage credentials, or the authoritative Risk of Ruin.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from hedge_desk.options import OptionQuote, OptionType
from hedge_desk.paper.review import load_plan_file
from hedge_desk.paper.workflow import (
    HumanAuthorizationStatus,
    PaperClose,
    PaperOpen,
    PaperTradePlan,
    close_paper_trade,
    execute_paper_open,
    evaluate_paper_fill,
    evaluate_plan_lifecycle,
)

RUNNER_STATE_SCHEMA_VERSION = "paper-runner-state-1.0.0"
RUNNER_ESCALATION_SCHEMA_VERSION = "paper-runner-escalations-1.0.0"
RUNNER_ENVIRONMENT = "paper"

STATUS_PENDING_OPEN = "PENDING_OPEN"
STATUS_OPEN = "OPEN"
STATUS_CLOSED = "CLOSED"

_MONITOR_ACTION = "MONITOR"

# Actions that need a human; the runner records them but never acts on them.
_ESCALATION_ACTIONS = {
    "CLOSE_REVIEW_REQUIRED",
    "BLOCK_AND_ESCALATE",
    "ASSIGNMENT_RECONCILIATION_REQUIRED",
    "EXPIRATION_RECONCILIATION_REQUIRED",
}


def _json_value(value: Any) -> Any:
    """Local JSON serializer mirroring the paper review envelope style."""
    if hasattr(value, "__dataclass_fields__"):
        return {
            key: _json_value(getattr(value, key))
            for key in value.__dataclass_fields__
        }
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_value(item) for item in value]
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def _require_tz_aware(moment: datetime, label: str) -> datetime:
    if moment.tzinfo is None:
        raise ValueError(f"{label} must be timezone-aware")
    return moment


def _open_to_dict(opened: PaperOpen) -> Dict[str, Any]:
    return _json_value(opened)


def _close_to_dict(closed: PaperClose) -> Dict[str, Any]:
    return _json_value(closed)


def _open_from_dict(data: Dict[str, Any]) -> PaperOpen:
    return PaperOpen(
        plan_id=str(data["plan_id"]),
        plan_hash=str(data["plan_hash"]),
        spread_id=str(data["spread_id"]),
        opened_at=_require_tz_aware(
            datetime.fromisoformat(data["opened_at"]), "paper-open timestamp"
        ),
        entry_credit=Decimal(str(data["entry_credit"])),
        quantity=int(data["quantity"]),
        environment=str(data.get("environment", "paper")),
    )


def _close_from_dict(data: Dict[str, Any]) -> PaperClose:
    return PaperClose(
        plan_id=str(data["plan_id"]),
        plan_hash=str(data["plan_hash"]),
        closed_at=_require_tz_aware(
            datetime.fromisoformat(data["closed_at"]), "paper-close timestamp"
        ),
        exit_debit=Decimal(str(data["exit_debit"])),
        exit_commission=Decimal(str(data["exit_commission"])),
        realized_pnl=Decimal(str(data["realized_pnl"])),
        exit_evaluation_sha256=str(data["exit_evaluation_sha256"]),
        close_sha256=str(data["close_sha256"]),
        environment=str(data.get("environment", "paper")),
    )


def parse_option_quote(data: Dict[str, Any]) -> OptionQuote:
    """Rebuild an OptionQuote from its JSON form (used by the CLI close path)."""
    return OptionQuote(
        contract_id=str(data["contract_id"]),
        underlying=str(data["underlying"]),
        option_type=OptionType(str(data["option_type"])),
        strike=Decimal(str(data["strike"])),
        expiration=date.fromisoformat(data["expiration"]),
        bid=Decimal(str(data["bid"])),
        ask=Decimal(str(data["ask"])),
        bid_size=int(data["bid_size"]),
        ask_size=int(data["ask_size"]),
        quoted_at=_require_tz_aware(
            datetime.fromisoformat(data["quoted_at"]), "quote timestamp"
        ),
        source_id=str(data["source_id"]),
        open_interest=int(data["open_interest"]),
        volume=int(data["volume"]),
    )


def _default_state() -> Dict[str, Any]:
    return {
        "schema_version": RUNNER_STATE_SCHEMA_VERSION,
        "environment": RUNNER_ENVIRONMENT,
        "plans": {},
    }


def _load_state(state_path: Path) -> Dict[str, Any]:
    if not state_path.exists():
        return _default_state()
    raw = json.loads(state_path.read_text(encoding="utf-8"))
    if raw.get("schema_version") != RUNNER_STATE_SCHEMA_VERSION:
        raise ValueError(
            f"unsupported runner state schema: {raw.get('schema_version')!r}"
        )
    if raw.get("environment") != RUNNER_ENVIRONMENT:
        raise ValueError(
            f"refusing non-paper runner state (environment={raw.get('environment')!r})"
        )
    plans = raw.get("plans")
    if not isinstance(plans, dict):
        raise ValueError("runner state is missing its plans map")
    return raw


def _write_state(state_path: Path, state: Dict[str, Any]) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(state, indent=2, sort_keys=True), encoding="utf-8"
    )


def _new_entry(plan: PaperTradePlan) -> Dict[str, Any]:
    return {
        "status": STATUS_PENDING_OPEN,
        "plan_hash": plan.plan_hash,
        "open": None,
        "close": None,
        "escalations": [],
    }


def _entry_for(state: Dict[str, Any], plan: PaperTradePlan) -> Dict[str, Any]:
    entry = state["plans"].get(plan.plan_id)
    if entry is None:
        entry = _new_entry(plan)
        state["plans"][plan.plan_id] = entry
    return entry


def _require_state_plan_hash(entry: Dict[str, Any], plan: PaperTradePlan) -> bool:
    """Confirm the durable state entry is still bound to the approved plan."""
    return entry.get("plan_hash") == plan.plan_hash


def _lifecycle_defaults() -> Dict[str, bool]:
    return {
        "short_leg_in_the_money": False,
        "ex_dividend_before_expiration": False,
        "assignment_notice_received": False,
        "contract_adjustment_pending": False,
        "settlement_terms_confirmed": False,
    }


def _default_quotes_provider(plan: PaperTradePlan) -> Tuple[int, Optional[Decimal]]:
    """Nothing executable — fail closed unless a real provider is injected."""
    return (0, None)


def _default_lifecycle_provider(plan: PaperTradePlan) -> Dict[str, bool]:
    """Conservative baseline: all flags False.

    Note this means ``settlement_terms_confirmed`` is False, which the
    lifecycle control treats as BLOCK_AND_ESCALATE (unconfirmed settlement
    terms fail closed). The runner therefore never assumes a quiet market;
    callers that want MONITOR must inject a provider asserting confirmed
    settlement terms.
    """
    return _lifecycle_defaults()


QuotesProvider = Callable[[PaperTradePlan], Tuple[int, Optional[Decimal]]]
LifecycleProvider = Callable[[PaperTradePlan], Dict[str, bool]]


def advance_paper_lifecycle(
    plans_dir: Any,
    state_path: Any,
    quotes_provider: Optional[QuotesProvider] = None,
    now: Optional[datetime] = None,
    lifecycle_provider: Optional[LifecycleProvider] = None,
) -> Dict[str, Any]:
    """Advance the paper lifecycle one tick on the 15-minute cadence.

    Only APPROVED plans are considered. Each tick:
    - PENDING_OPEN plans are fill-checked with ``quotes_provider(plan)``; a
      ready fill is opened via ``execute_paper_open``. Any unready condition
      (stale quotes, insufficient size, worse credit, unavailable quotes,
      expired approval, or a refused open) keeps the plan PENDING_OPEN with
      reason codes — fail closed.
    - OPEN plans are lifecycle-checked with ``lifecycle_provider(plan)``.
      MONITOR keeps them open; any other action appends an escalation to the
      plan's escalation list and the human-escalation manifest. The runner
      never auto-closes and never auto-acts.
    - CLOSED plans are left alone.

    Returns a tick report ``{"opened", "still_pending", "monitoring",
    "escalated", "skipped", "environment"}``. ``plans_dir`` absent or empty
    is a strict no-op returning an empty report.
    """
    if now is None:
        raise ValueError("a timezone-aware `now` is required")
    _require_tz_aware(now, "tick timestamp")
    if quotes_provider is None:
        quotes_provider = _default_quotes_provider
    if lifecycle_provider is None:
        lifecycle_provider = _default_lifecycle_provider

    report: Dict[str, Any] = {
        "opened": [],
        "still_pending": [],
        "monitoring": [],
        "escalated": [],
        "skipped": [],
        "environment": RUNNER_ENVIRONMENT,
    }
    plans_path = Path(plans_dir)
    if not plans_path.is_dir():
        return report
    plan_files = sorted(plans_path.glob("*.json"))
    if not plan_files:
        return report

    state_path = Path(state_path)
    state = _load_state(state_path)
    ticked = False

    for plan_file in plan_files:
        try:
            plan = load_plan_file(plan_file)
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            report["skipped"].append(
                {
                    "plan_file": str(plan_file),
                    "reason_codes": ["PLAN_FILE_LOAD_FAILED"],
                }
            )
            continue
        if plan.authorization.status is not HumanAuthorizationStatus.APPROVED:
            continue
        entry = _entry_for(state, plan)
        ticked = True

        if not _require_state_plan_hash(entry, plan):
            escalation = {
                "action": "BLOCK_AND_ESCALATE",
                "reason_codes": ["PLAN_HASH_MISMATCH"],
                "checked_at": now.isoformat(),
                "status": "PENDING_HUMAN",
            }
            entry["escalations"].append(escalation)
            report["escalated"].append(
                {
                    "plan_id": plan.plan_id,
                    "action": escalation["action"],
                    "reason_codes": list(escalation["reason_codes"]),
                    "checked_at": escalation["checked_at"],
                }
            )
            continue

        status = entry.get("status", STATUS_PENDING_OPEN)
        if status == STATUS_PENDING_OPEN:
            _tick_pending_open(plan, entry, now, quotes_provider, report)
        elif status == STATUS_OPEN:
            _tick_open(plan, entry, now, lifecycle_provider, report)
        elif status == STATUS_CLOSED:
            continue
        else:
            report["skipped"].append(
                {
                    "plan_id": plan.plan_id,
                    "reason_codes": ["UNKNOWN_PLAN_STATUS"],
                }
            )

    if ticked:
        _write_state(state_path, state)
        _write_escalation_manifest(state_path, state)
    return report


def _tick_pending_open(
    plan: PaperTradePlan,
    entry: Dict[str, Any],
    now: datetime,
    quotes_provider: QuotesProvider,
    report: Dict[str, Any],
) -> None:
    """Try to open one PENDING_OPEN plan; fail closed on any unready cause."""
    if now > plan.approval_expires_at:
        report["still_pending"].append(
            {"plan_id": plan.plan_id, "reason_codes": ["APPROVAL_EXPIRED"]}
        )
        return
    try:
        available_combo_size, current_net_credit = quotes_provider(plan)
    except Exception:
        report["still_pending"].append(
            {"plan_id": plan.plan_id, "reason_codes": ["QUOTES_PROVIDER_FAILED"]}
        )
        return
    if current_net_credit is None:
        report["still_pending"].append(
            {
                "plan_id": plan.plan_id,
                "reason_codes": ["QUOTE_UNAVAILABLE", "INSUFFICIENT_COMBO_SIZE"],
            }
        )
        return
    if not isinstance(current_net_credit, Decimal) or not isinstance(
        available_combo_size, int
    ):
        report["still_pending"].append(
            {"plan_id": plan.plan_id, "reason_codes": ["QUOTE_PROVIDER_TYPE_ERROR"]}
        )
        return
    fill = evaluate_paper_fill(
        plan, available_combo_size, current_net_credit, now
    )
    if not fill.ready:
        report["still_pending"].append(
            {"plan_id": plan.plan_id, "reason_codes": list(fill.reason_codes)}
        )
        return
    try:
        opened = execute_paper_open(plan, now)
    except (PermissionError, ValueError):
        report["still_pending"].append(
            {"plan_id": plan.plan_id, "reason_codes": ["OPEN_REFUSED"]}
        )
        return
    entry["status"] = STATUS_OPEN
    entry["open"] = _open_to_dict(opened)
    report["opened"].append(
        {
            "plan_id": plan.plan_id,
            "plan_hash": plan.plan_hash,
            "opened_at": opened.opened_at.isoformat(),
            "entry_credit": str(opened.entry_credit),
            "quantity": opened.quantity,
        }
    )


def _tick_open(
    plan: PaperTradePlan,
    entry: Dict[str, Any],
    now: datetime,
    lifecycle_provider: LifecycleProvider,
    report: Dict[str, Any],
) -> None:
    """Monitor one OPEN plan; record escalations but never auto-act."""
    try:
        opened = _open_from_dict(entry["open"])
    except (KeyError, TypeError, ValueError):
        escalation = {
            "action": "BLOCK_AND_ESCALATE",
            "reason_codes": ["OPEN_RECORD_CORRUPT"],
            "checked_at": now.isoformat(),
            "status": "PENDING_HUMAN",
        }
        entry["escalations"].append(escalation)
        report["escalated"].append(
            {
                "plan_id": plan.plan_id,
                "action": escalation["action"],
                "reason_codes": list(escalation["reason_codes"]),
                "checked_at": escalation["checked_at"],
            }
        )
        return
    if opened.plan_hash != plan.plan_hash:
        escalation = {
            "action": "BLOCK_AND_ESCALATE",
            "reason_codes": ["OPEN_PLAN_HASH_MISMATCH"],
            "checked_at": now.isoformat(),
            "status": "PENDING_HUMAN",
        }
        entry["escalations"].append(escalation)
        report["escalated"].append(
            {
                "plan_id": plan.plan_id,
                "action": escalation["action"],
                "reason_codes": list(escalation["reason_codes"]),
                "checked_at": escalation["checked_at"],
            }
        )
        return
    try:
        lifecycle_inputs = lifecycle_provider(plan)
    except Exception:
        lifecycle_inputs = dict(_lifecycle_defaults())
        lifecycle_inputs["contract_adjustment_pending"] = True
        lifecycle_inputs["settlement_terms_confirmed"] = False
    check = evaluate_plan_lifecycle(
        plan,
        now,
        short_leg_in_the_money=bool(lifecycle_inputs.get("short_leg_in_the_money")),
        ex_dividend_before_expiration=bool(
            lifecycle_inputs.get("ex_dividend_before_expiration")
        ),
        assignment_notice_received=bool(
            lifecycle_inputs.get("assignment_notice_received")
        ),
        contract_adjustment_pending=bool(
            lifecycle_inputs.get("contract_adjustment_pending")
        ),
        settlement_terms_confirmed=bool(
            lifecycle_inputs.get("settlement_terms_confirmed")
        ),
    )
    if check.action == _MONITOR_ACTION:
        report["monitoring"].append(
            {"plan_id": plan.plan_id, "checked_at": check.checked_at.isoformat()}
        )
        return
    if check.action not in _ESCALATION_ACTIONS:
        # Unknown action from a newer lifecycle revision: fail closed by
        # escalating rather than guessing what it means.
        escalation_action = "BLOCK_AND_ESCALATE"
        reason_codes = ["UNKNOWN_LIFECYCLE_ACTION"] + list(check.reason_codes)
    else:
        escalation_action = check.action
        reason_codes = list(check.reason_codes)
    escalation = {
        "action": escalation_action,
        "reason_codes": reason_codes,
        "checked_at": check.checked_at.isoformat(),
        "status": "PENDING_HUMAN",
    }
    entry["escalations"].append(escalation)
    report["escalated"].append(
        {
            "plan_id": plan.plan_id,
            "action": escalation_action,
            "reason_codes": reason_codes,
            "checked_at": escalation["checked_at"],
        }
    )


def _escalation_manifest_path(state_path: Path) -> Path:
    return state_path.parent / "escalations.json"


def _closes_dir(state_path: Path) -> Path:
    return state_path.parent / "closes"


def _write_escalation_manifest(state_path: Path, state: Dict[str, Any]) -> None:
    """Write the human-escalation manifest next to the state file."""
    manifest = {
        "schema_version": RUNNER_ESCALATION_SCHEMA_VERSION,
        "environment": RUNNER_ENVIRONMENT,
        "escalations": {
            plan_id: list(entry.get("escalations", []))
            for plan_id, entry in state["plans"].items()
            if entry.get("escalations")
        },
    }
    _write_state(_escalation_manifest_path(state_path), manifest)


def _validate_human_decision(
    human_id: str,
    decided_at: datetime,
    reason_codes: Tuple[str, ...],
) -> Tuple[str, datetime, Tuple[str, ...]]:
    if not human_id.strip():
        raise ValueError("human identity is required")
    _require_tz_aware(decided_at, "close decision timestamp")
    codes = tuple(reason_codes)
    if not codes or any(not code.strip() for code in codes):
        raise ValueError("close requires at least one reason code")
    return human_id.strip(), decided_at, codes


def _find_plan_file(plans_dir: Path, plan_id: str) -> Path:
    for plan_file in sorted(plans_dir.glob("*.json")):
        try:
            if load_plan_file(plan_file).plan_id == plan_id:
                return plan_file
        except (ValueError, KeyError, json.JSONDecodeError):
            continue
    raise ValueError(f"no paper plan file found for plan_id: {plan_id}")


def close_paper_position(
    plans_dir: Any,
    state_path: Any,
    plan_id: str,
    human_id: str,
    decided_at: datetime,
    reason_codes: Tuple[str, ...],
    short_quote: OptionQuote,
    long_quote: OptionQuote,
    exit_commission_per_contract: Decimal,
) -> Dict[str, Any]:
    """Record a human close of an OPEN paper position.

    Requires the plan to be OPEN in the runner state, a named human, a
    timezone-aware decision timestamp, and at least one reason code. The
    PaperClose artifact is written next to the state file under
    ``closes/<plan_id>.json`` for the later market-data settler. A plan that
    is not OPEN is refused — the runner itself never closes.
    """
    human_id, decided_at, codes = _validate_human_decision(
        human_id, decided_at, tuple(reason_codes)
    )
    if not isinstance(exit_commission_per_contract, Decimal):
        raise ValueError("exit commission must be a Decimal")
    plans_path = Path(plans_dir)
    plan = load_plan_file(_find_plan_file(plans_path, plan_id))
    state_path = Path(state_path)
    state = _load_state(state_path)
    entry = state["plans"].get(plan_id)
    if entry is None:
        raise PermissionError(f"plan has no lifecycle state: {plan_id}")
    if entry.get("status") != STATUS_OPEN:
        raise PermissionError(
            f"only an OPEN paper position can be closed: {plan_id} is "
            f"{entry.get('status')}"
        )
    if entry.get("plan_hash") != plan.plan_hash:
        raise PermissionError("state entry is not bound to the approved plan")
    opened = _open_from_dict(entry["open"])
    closed = close_paper_trade(
        opened,
        plan,
        short_quote,
        long_quote,
        exit_commission_per_contract,
        decided_at,
    )
    entry["status"] = STATUS_CLOSED
    entry["close"] = _close_to_dict(closed)
    entry["close_decision"] = {
        "human_id": human_id,
        "decided_at": decided_at.isoformat(),
        "reason_codes": list(codes),
    }
    closes = _closes_dir(state_path)
    closes.mkdir(parents=True, exist_ok=True)
    artifact = {
        "schema_version": RUNNER_STATE_SCHEMA_VERSION,
        "environment": RUNNER_ENVIRONMENT,
        "decision": entry["close_decision"],
        "close": entry["close"],
    }
    artifact_path = closes / f"{plan_id}.json"
    artifact_path.write_text(
        json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8"
    )
    _write_state(state_path, state)
    _write_escalation_manifest(state_path, state)
    return {
        "plan_id": plan_id,
        "plan_hash": plan.plan_hash,
        "status": "closed",
        "human_id": human_id,
        "decided_at": decided_at.isoformat(),
        "reason_codes": list(codes),
        "closed_at": closed.closed_at.isoformat(),
        "exit_debit": str(closed.exit_debit),
        "exit_commission": str(closed.exit_commission),
        "realized_pnl": str(closed.realized_pnl),
        "close_sha256": closed.close_sha256,
        "close_artifact": str(artifact_path),
        "environment": RUNNER_ENVIRONMENT,
    }


def list_pending_escalations(state_path: Any) -> Dict[str, Any]:
    """List every escalation awaiting a human (the runner never auto-resolves)."""
    state = _load_state(Path(state_path))
    pending: List[Dict[str, Any]] = []
    for plan_id, entry in state["plans"].items():
        for escalation in entry.get("escalations", []):
            if escalation.get("status") == "PENDING_HUMAN":
                pending.append({"plan_id": plan_id, **escalation})
    return {"pending_escalations": pending, "environment": RUNNER_ENVIRONMENT}


__all__ = [
    "RUNNER_ENVIRONMENT",
    "RUNNER_ESCALATION_SCHEMA_VERSION",
    "RUNNER_STATE_SCHEMA_VERSION",
    "STATUS_CLOSED",
    "STATUS_OPEN",
    "STATUS_PENDING_OPEN",
    "advance_paper_lifecycle",
    "close_paper_position",
    "list_pending_escalations",
    "parse_option_quote",
]
