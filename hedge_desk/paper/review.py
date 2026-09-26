"""In-memory human review queue for paper-trade plans.

This module is the production caller hook for the paper-trade approval loop.
The intended flow is::

    plan = create_paper_trade_plan(...)      # machine side: risk + compliance + calendar
    queue = submit_plan_for_review(plan)     # hand the PENDING plan to a human
    queue.pending()                          # review surface: plan_id, hash, expiry, risk status
    queue.decide(plan_id, human_id, decided_at, approve=True)
    # or: queue.decide(plan_id, human_id, decided_at, approve=False,
    #                    reason_codes=("THESIS_INVALIDATED",))

``decide`` routes to :func:`approve_paper_trade` or
:func:`reject_paper_trade` in :mod:`hedge_desk.paper.workflow`, so every guard
defined there applies unchanged: plan-hash integrity, human identity,
timezone-aware timestamps, the approval window, PENDING-only decisions, and —
on the approve path — no override of a machine risk rejection or a Back
Office compliance block. A rejection only ever says no, so the machine and
compliance gates are approval-side only; the reject path keeps the same audit
guards (integrity, identity, window, PENDING) plus mandatory reason codes.

Paper-trade plans can cross a process boundary as plan files. A plan file is
a JSON envelope::

    {"schema_version": "paper-plan-file-1.0.0",
     "environment": "paper",
     "plan": { ... }}

``environment`` must be ``"paper"``; anything else is refused. Use
:func:`write_plan_file` to emit one from a live plan and
:func:`load_plan_file` to rebuild the plan (the plan-hash integrity check in
the workflow functions still verifies the file was not tampered with).
The CLI wires these files to the queue via ``--paper-review`` and
``--paper-decide``.

The queue is in-memory and deterministic: pending plans are listed in
submission order. It is a review surface, not a durable store.
"""

from __future__ import annotations

import dataclasses
import json
import typing
from dataclasses import is_dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from hedge_desk.paper.workflow import (
    HumanAuthorizationStatus,
    PaperTradePlan,
    approve_paper_trade,
    reject_paper_trade,
)

PLAN_FILE_SCHEMA_VERSION = "paper-plan-file-1.0.0"
PLAN_FILE_ENVIRONMENT = "paper"


class PaperReviewQueue:
    """Deterministic in-memory queue of plans awaiting a human decision."""

    def __init__(self) -> None:
        self._plans: Dict[str, PaperTradePlan] = {}

    def submit(self, plan: PaperTradePlan) -> PaperTradePlan:
        """Add a PENDING plan to the review queue."""
        if plan.plan_id in self._plans:
            raise ValueError(f"duplicate plan_id in review queue: {plan.plan_id}")
        if plan.authorization.status is not HumanAuthorizationStatus.PENDING:
            raise ValueError(
                f"only PENDING plans can enter review: {plan.plan_id} is "
                f"{plan.authorization.status.value}"
            )
        self._plans[plan.plan_id] = plan
        return plan

    def get(self, plan_id: str) -> PaperTradePlan:
        """Return the stored plan (PENDING or already decided)."""
        try:
            return self._plans[plan_id]
        except KeyError:
            raise KeyError(f"unknown plan_id in review queue: {plan_id}") from None

    def pending(self) -> List[Dict[str, Any]]:
        """List PENDING plans in submission order for the review surface."""
        return [
            {
                "plan_id": plan.plan_id,
                "plan_hash": plan.plan_hash,
                "approval_expires_at": plan.approval_expires_at.isoformat(),
                "machine_risk_status": plan.machine_risk_status.value,
            }
            for plan in self._plans.values()
            if plan.authorization.status is HumanAuthorizationStatus.PENDING
        ]

    def decide(
        self,
        plan_id: str,
        human_id: str,
        decided_at: datetime,
        approve: bool,
        reason_codes: Iterable[str] = (),
    ) -> PaperTradePlan:
        """Record a human decision, routing to approve or reject.

        ``reason_codes`` is required when ``approve`` is False and ignored
        when True. A second decision on the same plan is refused by the
        workflow's PENDING-only guard.
        """
        plan = self.get(plan_id)
        decided = (
            approve_paper_trade(plan, human_id, decided_at)
            if approve
            else reject_paper_trade(plan, human_id, decided_at, tuple(reason_codes))
        )
        self._plans[plan_id] = decided
        return decided


def submit_plan_for_review(plan: PaperTradePlan) -> PaperReviewQueue:
    """Convenience hook: create a queue with one PENDING plan submitted."""
    queue = PaperReviewQueue()
    queue.submit(plan)
    return queue


def _json_value(value: Any) -> Any:
    """Convert immutable records to stable JSON-compatible values.

    Local copy of the demo serializer so this module never imports the demo
    fixtures (demo imports hedge_desk.paper).
    """
    if is_dataclass(value):
        return {key: _json_value(item) for key, item in dataclasses.asdict(value).items()}
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


def _parse_hint(hint: Any, value: Any, path: str) -> Any:
    """Rebuild one typed value from its JSON form using the type hint."""
    if value is None:
        origin = typing.get_origin(hint)
        if origin is typing.Union and type(None) in typing.get_args(hint):
            return None
        raise ValueError(f"missing value for {path}")
    origin = typing.get_origin(hint)
    if origin is typing.Union:
        args = [a for a in typing.get_args(hint) if a is not type(None)]
        if len(args) == 1:
            return _parse_hint(args[0], value, path)
        raise ValueError(f"unsupported union at {path}")
    if isinstance(hint, type) and issubclass(hint, Enum):
        return hint(value)
    if hint is Decimal:
        return Decimal(str(value))
    if hint is datetime:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            raise ValueError(f"timezone-aware timestamp required at {path}")
        return parsed
    if hint is date:
        return date.fromisoformat(value)
    if hint is bool:
        if not isinstance(value, bool):
            raise ValueError(f"boolean required at {path}")
        return value
    if hint in (str, int, float):
        return hint(value)
    if origin in (tuple, list):
        args = typing.get_args(hint)
        items = list(value)
        if origin is tuple and len(args) == 2 and args[1] is Ellipsis:
            return tuple(_parse_hint(args[0], item, f"{path}[{i}]") for i, item in enumerate(items))
        if len(items) != len(args):
            raise ValueError(f"wrong arity at {path}")
        parsed_items = [_parse_hint(arg, item, f"{path}[{i}]") for i, (arg, item) in enumerate(zip(args, items))]
        return tuple(parsed_items) if origin is tuple else parsed_items
    if isinstance(hint, type) and is_dataclass(hint):
        return _record_from_dict(hint, value, path)
    raise ValueError(f"unsupported type at {path}: {hint!r}")


def _record_from_dict(cls: Any, data: Dict[str, Any], path: str) -> Any:
    hints = typing.get_type_hints(cls)
    kwargs = {}
    for field in dataclasses.fields(cls):
        field_path = f"{path}.{field.name}"
        if field.name not in data:
            if field.default is not dataclasses.MISSING or field.default_factory is not dataclasses.MISSING:
                continue
            raise ValueError(f"missing field {field_path}")
        kwargs[field.name] = _parse_hint(hints[field.name], data[field.name], field_path)
    return cls(**kwargs)


def write_plan_file(plan: PaperTradePlan, path: Any) -> Path:
    """Write a paper plan file that the review queue and CLI can load."""
    target = Path(path)
    envelope = {
        "schema_version": PLAN_FILE_SCHEMA_VERSION,
        "environment": PLAN_FILE_ENVIRONMENT,
        "plan": _json_value(plan),
    }
    target.write_text(json.dumps(envelope, indent=2, sort_keys=True), encoding="utf-8")
    return target


def load_plan_file(path: Any) -> PaperTradePlan:
    """Rebuild a PaperTradePlan from a plan file; refuses non-paper files.

    The returned plan still passes through the workflow's plan-hash integrity
    check on approve/reject, so a tampered file cannot produce a decision.
    """
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if raw.get("schema_version") != PLAN_FILE_SCHEMA_VERSION:
        raise ValueError(
            f"unsupported plan file schema: {raw.get('schema_version')!r}"
        )
    if raw.get("environment") != PLAN_FILE_ENVIRONMENT:
        raise ValueError(
            f"refusing non-paper plan file (environment={raw.get('environment')!r})"
        )
    plan_data = raw.get("plan")
    if not isinstance(plan_data, dict):
        raise ValueError("plan file is missing its plan payload")
    return _record_from_dict(PaperTradePlan, plan_data, "plan")


__all__ = [
    "PLAN_FILE_ENVIRONMENT",
    "PLAN_FILE_SCHEMA_VERSION",
    "PaperReviewQueue",
    "load_plan_file",
    "submit_plan_for_review",
    "write_plan_file",
]
