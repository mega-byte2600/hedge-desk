"""Fail-closed local JSONL persistence for paper audit chains."""

import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Tuple

from hedge_desk.audit import AuditEvent, verify_audit_chain


AUDIT_JOURNAL_VERSION = "paper-audit-journal-1.0.0"


@dataclass(frozen=True)
class AuditJournalResult:
    status: str
    event_count: int
    head_hash: str
    reason_codes: Tuple[str, ...]


def _event_payload(event: AuditEvent):
    return {
        "sequence": event.sequence,
        "run_id": event.run_id,
        "stage": event.stage,
        "occurred_at": event.occurred_at.isoformat(),
        "artifact_id": event.artifact_id,
        "candidate_id": event.candidate_id,
        "input_sha256": event.input_sha256,
        "output_sha256": event.output_sha256,
        "component_version": event.component_version,
        "policy_version": event.policy_version,
        "reason_codes": list(event.reason_codes),
        "previous_hash": event.previous_hash,
        "event_hash": event.event_hash,
    }


def _parse_event(value) -> AuditEvent:
    fields = {
        "sequence", "run_id", "stage", "occurred_at", "artifact_id",
        "candidate_id", "input_sha256", "output_sha256", "component_version",
        "policy_version", "reason_codes", "previous_hash", "event_hash",
    }
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError("audit journal event schema invalid")
    if type(value["sequence"]) is not int or not isinstance(value["reason_codes"], list):
        raise ValueError("audit journal event types invalid")
    return AuditEvent(
        value["sequence"], str(value["run_id"]), str(value["stage"]),
        datetime.fromisoformat(str(value["occurred_at"])), str(value["artifact_id"]),
        str(value["candidate_id"]), str(value["input_sha256"]),
        str(value["output_sha256"]), str(value["component_version"]),
        str(value["policy_version"]), tuple(str(item) for item in value["reason_codes"]),
        str(value["previous_hash"]), str(value["event_hash"]),
    )


def read_audit_journal(path: Path) -> Tuple[AuditEvent, ...]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        events = tuple(_parse_event(json.loads(line)) for line in lines if line)
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise ValueError("AUDIT_JOURNAL_CORRUPT") from exc
    reasons = verify_audit_chain(events)
    if reasons:
        raise ValueError("AUDIT_JOURNAL_CORRUPT:" + ",".join(reasons))
    return events


def initialize_audit_journal(path: Path, chain: Tuple[AuditEvent, ...]) -> AuditJournalResult:
    reasons = verify_audit_chain(chain)
    if reasons:
        return AuditJournalResult("BLOCKED", len(chain), "", reasons)
    payload = "".join(
        json.dumps(_event_payload(event), sort_keys=True, separators=(",", ":")) + "\n"
        for event in chain
    )
    try:
        with path.open("x", encoding="utf-8") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError:
        return AuditJournalResult("BLOCKED", 0, "", ("AUDIT_JOURNAL_ALREADY_EXISTS",))
    return AuditJournalResult(
        "INITIALIZED", len(chain), chain[-1].event_hash if chain else "0" * 64, ()
    )


def append_audit_journal(path: Path, event: AuditEvent) -> AuditJournalResult:
    try:
        chain = read_audit_journal(path)
    except ValueError:
        return AuditJournalResult("BLOCKED", 0, "", ("AUDIT_JOURNAL_CORRUPT",))
    if chain and event.event_hash == chain[-1].event_hash:
        return AuditJournalResult("DUPLICATE_SUPPRESSED", len(chain), chain[-1].event_hash, ())
    proposed = chain + (event,)
    reasons = verify_audit_chain(proposed)
    if reasons:
        return AuditJournalResult("BLOCKED", len(chain), chain[-1].event_hash if chain else "0" * 64, reasons)
    line = json.dumps(_event_payload(event), sort_keys=True, separators=(",", ":")) + "\n"
    try:
        with path.open("a", encoding="utf-8") as stream:
            stream.write(line)
            stream.flush()
            os.fsync(stream.fileno())
    except OSError:
        return AuditJournalResult("BLOCKED", len(chain), chain[-1].event_hash if chain else "0" * 64, ("AUDIT_JOURNAL_WRITE_FAILED",))
    return AuditJournalResult("APPENDED", len(proposed), event.event_hash, ())
