"""Strict local multi-underlying option-universe intake orchestration."""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Tuple

from hedge_desk.data import validate_local_observation
from hedge_desk.options import (
    OptionUniverseEvaluation,
    evaluate_market_session,
    evaluate_option_universe,
    parse_market_session_evidence,
    parse_option_snapshot,
)


OPTION_UNIVERSE_MANIFEST_VERSION = "hedge-desk-option-universe-1.0.0"


@dataclass(frozen=True)
class OptionUniverseIntake:
    source_count: int
    symbols: Tuple[str, ...]
    evaluation: OptionUniverseEvaluation
    raw_payloads_copied: bool = False


def validate_local_option_universe(manifest_path: Path) -> OptionUniverseIntake:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("option universe manifest unreadable") from exc
    expected = {
        "schema_version", "decision_cutoff", "maximum_age_seconds",
        "minimum_seconds_before_close", "market_session_evidence", "snapshots",
    }
    if not isinstance(manifest, dict) or set(manifest) != expected:
        raise ValueError("option universe manifest schema invalid")
    if manifest["schema_version"] != OPTION_UNIVERSE_MANIFEST_VERSION:
        raise ValueError("option universe manifest version unsupported")
    try:
        decision_time = datetime.fromisoformat(
            manifest["decision_cutoff"].replace("Z", "+00:00")
        )
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("option universe decision time invalid") from exc
    maximum_age = manifest["maximum_age_seconds"]
    minimum_before_close = manifest["minimum_seconds_before_close"]
    if type(maximum_age) is not int or type(minimum_before_close) is not int:
        raise ValueError("option universe timing policies must be integers")
    rows = manifest["snapshots"]
    if not isinstance(rows, list) or not rows:
        raise ValueError("option universe snapshots required")
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"envelope", "payload"}:
            raise ValueError("option universe snapshot reference invalid")
        if (
            not isinstance(row["envelope"], str)
            or not row["envelope"]
            or not isinstance(row["payload"], str)
            or not row["payload"]
        ):
            raise ValueError("option universe snapshot paths invalid")
    root = manifest_path.parent
    try:
        session_payload = json.loads(
            (root / manifest["market_session_evidence"]).read_text(encoding="utf-8")
        )
        session = parse_market_session_evidence(session_payload)
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise ValueError("option universe session evidence invalid") from exc
    session_gate = evaluate_market_session(session, decision_time, minimum_before_close)
    if not session_gate.admissible:
        raise ValueError("option universe session blocked:" + ",".join(session_gate.reason_codes))
    snapshots = []
    for row in rows:
        envelope_path = root / row["envelope"]
        payload_path = root / row["payload"]
        try:
            intake = validate_local_observation(
                envelope_path, payload_path, decision_time, maximum_age
            )
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
            raise ValueError("option universe snapshot unreadable") from exc
        if not intake.gate.admissible:
            raise ValueError(
                "option universe snapshot blocked:" + ",".join(intake.gate.reason_codes)
            )
        if intake.artifact.payload_kind != "option_chain":
            raise ValueError("option universe payload kind must be option_chain")
        try:
            snapshots.append(parse_option_snapshot(
                payload_path, intake.artifact.source_id, intake.artifact.payload_sha256
            ))
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
            raise ValueError("option universe option snapshot invalid") from exc
    evaluation = evaluate_option_universe(
        tuple(snapshots), decision_time, session_gate
    )
    return OptionUniverseIntake(
        len(snapshots),
        tuple(sorted(item.underlying_quote.symbol for item in snapshots)),
        evaluation,
        False,
    )
