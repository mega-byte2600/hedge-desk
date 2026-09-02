"""Command-line entry point for the frozen paper-only vertical slice."""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256

from hedge_desk.demo import json_value, run_reference_demo
from hedge_desk.overnight import current_morning_report
from hedge_desk.projects import MVP_PROJECTS
from hedge_desk.wargames import build_war_game_report
from hedge_desk.reporting import build_control_summary, render_morning_markdown
from hedge_desk.artifacts import (
    build_artifact_bundle_manifest,
    verify_artifact_bundle_manifest,
)
from hedge_desk.audit import build_reference_audit
from hedge_desk.audit_store import initialize_audit_journal, read_audit_journal
from hedge_desk.operational_health import evaluate_paper_run_health
from hedge_desk.option_universe_intake import validate_local_option_universe
from hedge_desk.scheduler import (
    ScheduledRunRequest,
    execute_scheduled_run,
    validate_serialized_scheduled_run_receipt,
)
from hedge_desk.stat_inference import evaluate_directional_hits
from hedge_desk.data import (
    evaluate_options_data_stack,
    parse_data_stack_manifest,
    validate_local_observation,
)
from hedge_desk.options import (
    build_candidate_control_handoffs,
    parse_option_snapshot,
    parse_market_session_evidence,
    evaluate_market_session,
    scan_vertical_credit_spreads,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--evaluate-directional-outcomes",
        metavar="FILE",
        help="evaluate strict local boolean outcomes at alpha .005 and 95% CI",
    )
    parser.add_argument(
        "--validate-option-universe-manifest",
        metavar="FILE",
        help="validate and rank multiple local option snapshots without copying them",
    )
    parser.add_argument(
        "--verify-run-health",
        metavar="DIRECTORY",
        help="verify latest report, receipt, journal, freshness, and paper boundary",
    )
    parser.add_argument(
        "--maximum-run-age-seconds",
        type=int,
        default=900,
        help="maximum report age used by --verify-run-health",
    )
    parser.add_argument(
        "--health-evaluated-at",
        help="optional injected ISO-8601 clock for reproducible health checks",
    )
    parser.add_argument(
        "--audit-journal",
        metavar="FILE",
        help="create a new fail-closed local JSONL paper audit journal",
    )
    parser.add_argument(
        "--verify-audit-journal",
        metavar="FILE",
        help="independently read and verify a local JSONL paper audit journal",
    )
    parser.add_argument(
        "--validate-data-stack",
        metavar="FILE",
        help="validate a strict subscription capability manifest",
    )
    parser.add_argument(
        "--validate-data-envelope",
        metavar="FILE",
        help="validate a local BYO-data envelope against --payload",
    )
    parser.add_argument(
        "--payload",
        metavar="FILE",
        help="local payload used with --validate-data-envelope; never copied",
    )
    parser.add_argument(
        "--validate-option-snapshot",
        action="store_true",
        help="also enforce the canonical option snapshot schema",
    )
    parser.add_argument(
        "--scan-vertical-spreads",
        action="store_true",
        help="enumerate admissible verticals from a validated option snapshot",
    )
    parser.add_argument(
        "--market-session-evidence",
        metavar="FILE",
        help="strict exchange-session evidence required for candidate handoff",
    )
    parser.add_argument(
        "--minimum-seconds-before-close",
        type=int,
        default=900,
        help="entry cutoff buffer used with --market-session-evidence",
    )
    parser.add_argument(
        "--decision-cutoff",
        help="timezone-aware ISO-8601 cutoff for local data validation",
    )
    parser.add_argument(
        "--max-age-seconds",
        type=int,
        default=0,
        help="maximum data age for local validation (default: 0)",
    )
    parser.add_argument(
        "--morning-markdown",
        action="store_true",
        help="render the validated paper morning evaluation as Markdown",
    )
    parser.add_argument(
        "--control-summary",
        action="store_true",
        help="emit validated paper/real, war-game, stress, and release headlines",
    )
    parser.add_argument(
        "--war-games",
        action="store_true",
        help="run every declared synthetic premium-spread stress scenario",
    )
    parser.add_argument(
        "--overnight-report",
        action="store_true",
        help="run all six paper evaluations and emit the morning JSON report",
    )
    parser.add_argument(
        "--projects",
        action="store_true",
        help="print the machine-readable MVP project registry",
    )
    parser.add_argument(
        "--approve",
        action="store_true",
        help="simulate an explicit human approval for this frozen paper fixture",
    )
    parser.add_argument(
        "--yellow-sheet-rationale",
        action="store_true",
        help="show the active Yellow Sheet WHY and gate result for each candidate",
    )
    parser.add_argument(
        "--human-id",
        default="",
        help="required human identity when --approve is supplied",
    )
    parser.add_argument(
        "--report-input",
        help="render --morning-markdown from this exact finalized JSON report",
    )
    parser.add_argument(
        "--bundle-manifest",
        nargs="+",
        metavar="FILE",
        help="emit a canonical SHA-256 manifest for artifact files",
    )
    parser.add_argument(
        "--verify-bundle-manifest",
        metavar="FILE",
        help="verify an artifact bundle manifest against files beside it",
    )
    parser.add_argument(
        "--scheduled-receipt",
        action="store_true",
        help="emit a scheduler receipt bound to --report-input",
    )
    parser.add_argument(
        "--verify-scheduled-receipt",
        metavar="FILE",
        help="independently verify a serialized scheduler receipt",
    )
    parser.add_argument(
        "--idempotency-key",
        help="stable run identity required with --scheduled-receipt",
    )
    args = parser.parse_args()
    if args.evaluate_directional_outcomes:
        try:
            payload = json.loads(
                Path(args.evaluate_directional_outcomes).read_text(encoding="utf-8")
            )
            expected_fields = {
                "schema_version", "dataset_sha256", "source_id", "model_id",
                "model_version", "observations",
            }
            if not isinstance(payload, dict) or set(payload) != expected_fields:
                raise ValueError("directional outcome schema is invalid")
            identities = (
                payload["source_id"], payload["model_id"], payload["model_version"]
            )
            if any(not isinstance(value, str) or not value for value in identities):
                raise ValueError("directional outcome identities are required")
            dataset_hash = payload["dataset_sha256"]
            try:
                valid_hash = (
                    isinstance(dataset_hash, str)
                    and len(dataset_hash) == 64
                    and int(dataset_hash, 16) > 0
                )
            except ValueError:
                valid_hash = False
            if not valid_hash:
                raise ValueError("directional outcome dataset hash is invalid")
            observations = payload["observations"]
            if not isinstance(observations, list):
                raise ValueError("directional observations must be a list")
            if any(
                not isinstance(item, dict)
                or set(item) != {"observation_id", "outcome"}
                or not isinstance(item["observation_id"], str)
                or not item["observation_id"]
                or type(item["outcome"]) is not bool
                for item in observations
            ):
                raise ValueError("directional observation schema is invalid")
            observation_ids = [item["observation_id"] for item in observations]
            if len(observation_ids) != len(set(observation_ids)):
                raise ValueError("directional observation identities must be unique")
            observed_hash = sha256(
                json.dumps(
                    observations, sort_keys=True, separators=(",", ":")
                ).encode("utf-8")
            ).hexdigest()
            if dataset_hash != observed_hash:
                raise ValueError("directional outcome dataset hash mismatch")
            if payload["schema_version"] != "directional-outcomes-1.1.0":
                raise ValueError("directional outcome schema version is invalid")
            result = evaluate_directional_hits(
                tuple(item["outcome"] for item in observations)
            )
            output = {
                "label": "STAT",
                "schema_version": payload["schema_version"],
                "dataset_sha256": dataset_hash,
                "source_id": payload["source_id"],
                "model_id": payload["model_id"],
                "model_version": payload["model_version"],
                "evaluation": json_value(result),
            }
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            parser.error(str(exc))
        print(json.dumps(output, indent=2))
        return
    if args.control_summary:
        if not args.report_input:
            parser.error("--control-summary requires --report-input")
        try:
            report = json.loads(Path(args.report_input).read_text(encoding="utf-8"))
            summary = build_control_summary(report)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            parser.error(str(exc))
        print(json.dumps(summary, indent=2))
        return
    if args.validate_option_universe_manifest:
        try:
            result = validate_local_option_universe(
                Path(args.validate_option_universe_manifest)
            )
        except ValueError as exc:
            parser.error(str(exc))
        print(json.dumps(json_value(result), indent=2))
        return
    if args.verify_run_health:
        root = Path(args.verify_run_health)
        try:
            report = json.loads((root / "morning-report.json").read_text(encoding="utf-8"))
            receipt = json.loads((root / "run-receipt.json").read_text(encoding="utf-8"))
            journal = read_audit_journal(root / "audit-journal.jsonl")
            evaluated_at = (
                datetime.fromisoformat(args.health_evaluated_at.replace("Z", "+00:00"))
                if args.health_evaluated_at
                else datetime.now(timezone.utc)
            )
            result = evaluate_paper_run_health(
                report,
                receipt,
                len(journal),
                journal[-1].event_hash if journal else "0" * 64,
                evaluated_at,
                args.maximum_run_age_seconds,
                os.environ.get("HEDGE_DESK_CODE_COMMIT", report.get("code_commit", "")),
            )
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            print(json.dumps({"status": "BLOCKED", "reason_codes": [str(exc).split(":", 1)[0]]}, indent=2))
            raise SystemExit(1)
        print(json.dumps(json_value(result), indent=2))
        if result.status != "HEALTHY_PAPER":
            raise SystemExit(1)
        return
    if args.verify_audit_journal:
        try:
            chain = read_audit_journal(Path(args.verify_audit_journal))
        except ValueError as exc:
            print(json.dumps({"valid": False, "reason_codes": [str(exc).split(":", 1)[0]]}, indent=2))
            raise SystemExit(1)
        print(json.dumps({
            "valid": True,
            "event_count": len(chain),
            "head_hash": chain[-1].event_hash if chain else "0" * 64,
            "reason_codes": [],
        }, indent=2))
        return
    if args.audit_journal:
        result = initialize_audit_journal(
            Path(args.audit_journal), build_reference_audit()
        )
        print(json.dumps(json_value(result), indent=2))
        if result.status != "INITIALIZED":
            raise SystemExit(1)
        return
    if args.validate_data_stack:
        try:
            payload = json.loads(Path(args.validate_data_stack).read_text(encoding="utf-8"))
            budget, subscriptions = parse_data_stack_manifest(payload)
            result = evaluate_options_data_stack(subscriptions, budget)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            parser.error(str(exc))
        print(json.dumps(json_value(result), indent=2))
        if not result.ready_for_internal_options_research:
            raise SystemExit(2)
        return
    if args.verify_scheduled_receipt:
        try:
            receipt = json.loads(
                Path(args.verify_scheduled_receipt).read_text(encoding="utf-8")
            )
            reasons = validate_serialized_scheduled_run_receipt(receipt)
        except (OSError, UnicodeError, json.JSONDecodeError):
            reasons = ("SCHEDULER_RECEIPT_SCHEMA_INVALID",)
        print(json.dumps({"valid": not reasons, "reason_codes": list(reasons)}, indent=2))
        if reasons:
            raise SystemExit(1)
        return
    if args.validate_data_envelope:
        if not args.payload or not args.decision_cutoff:
            parser.error(
                "--validate-data-envelope requires --payload and --decision-cutoff"
            )
        try:
            cutoff = datetime.fromisoformat(
                args.decision_cutoff.replace("Z", "+00:00")
            )
            result = validate_local_observation(
                Path(args.validate_data_envelope),
                Path(args.payload),
                cutoff,
                args.max_age_seconds,
            )
        except ValueError as exc:
            parser.error(str(exc))
        output = json_value(result)
        if args.scan_vertical_spreads and not args.validate_option_snapshot:
            parser.error("--scan-vertical-spreads requires --validate-option-snapshot")
        if args.validate_option_snapshot:
            if result.artifact.payload_kind != "option_chain":
                parser.error(
                    "--validate-option-snapshot requires payload_kind option_chain"
                )
            try:
                snapshot = parse_option_snapshot(
                    Path(args.payload),
                    result.artifact.source_id,
                    result.artifact.payload_sha256,
                )
            except ValueError as exc:
                parser.error(str(exc))
            output["option_snapshot"] = {
                "schema_version": snapshot.schema_version,
                "source_id": snapshot.source_id,
                "symbol": snapshot.underlying_quote.symbol,
                "contract_count": len(snapshot.option_quotes),
                "contract_ids": [
                    quote.contract_id for quote in snapshot.option_quotes
                ],
            }
            if args.scan_vertical_spreads:
                scan = scan_vertical_credit_spreads(snapshot, cutoff)
                output["vertical_spread_scan"] = json_value(scan)
                if args.market_session_evidence:
                    try:
                        session_payload = json.loads(
                            Path(args.market_session_evidence).read_text(encoding="utf-8")
                        )
                        evidence = parse_market_session_evidence(session_payload)
                        session_gate = evaluate_market_session(
                            evidence, cutoff, args.minimum_seconds_before_close
                        )
                    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
                        parser.error(str(exc))
                    output["market_session_gate"] = json_value(session_gate)
                    output["control_handoffs"] = json_value(
                        build_candidate_control_handoffs(scan, session_gate)
                    )
                    output["handoff_reason_codes"] = list(session_gate.reason_codes)
                else:
                    output["control_handoffs"] = []
                    output["handoff_reason_codes"] = [
                        "MARKET_SESSION_EVIDENCE_REQUIRED"
                    ]
        print(json.dumps(output, indent=2))
        if not result.gate.admissible:
            raise SystemExit(2)
        return
    if args.verify_bundle_manifest:
        manifest_path = Path(args.verify_bundle_manifest)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        reasons = verify_artifact_bundle_manifest(manifest, manifest_path.parent)
        print(json.dumps({"valid": not reasons, "reason_codes": list(reasons)}, indent=2))
        if reasons:
            raise SystemExit(1)
        return
    if args.scheduled_receipt:
        if not args.report_input or not args.idempotency_key:
            parser.error(
                "--scheduled-receipt requires --report-input and --idempotency-key"
            )
        report = json.loads(Path(args.report_input).read_text(encoding="utf-8"))
        scheduled_for = datetime.fromisoformat(report["generated_at"])
        receipts = execute_scheduled_run(
            ScheduledRunRequest(args.idempotency_key, scheduled_for),
            (),
            lambda _: report,
        )
        print(json.dumps(json_value(receipts[-1]), indent=2))
        return
    if args.bundle_manifest:
        manifest = build_artifact_bundle_manifest(
            tuple(Path(item) for item in args.bundle_manifest)
        )
        print(json.dumps(manifest, indent=2))
        return
    if args.projects:
        print(json.dumps([project.__dict__ for project in MVP_PROJECTS], indent=2))
        return
    if args.overnight_report:
        print(json.dumps(current_morning_report(), indent=2))
        return
    if args.morning_markdown:
        report = (
            json.loads(Path(args.report_input).read_text(encoding="utf-8"))
            if args.report_input
            else current_morning_report()
        )
        print(render_morning_markdown(report), end="")
        return
    if args.report_input:
        parser.error("--report-input requires --morning-markdown")
    if args.war_games:
        print(json.dumps(build_war_game_report(), indent=2))
        return
    if args.yellow_sheet_rationale:
        plan = run_reference_demo(False, "")["plan"]
        sheet = plan["yellow_sheet"]
        print(json.dumps({
            "candidate_id": plan["risk_decision"]["candidate_id"],
            "plan_hash": plan["plan_hash"],
            "yellow_sheet_id": sheet["yellow_sheet_id"],
            "yellow_sheet_version": sheet["version"],
            "disposition": plan["proposal_disposition"],
            "reason_codes": plan["yellow_sheet_gate"]["reason_codes"],
            "why": sheet["decision_rationale"],
        }, indent=2))
        return
    if args.approve and not args.human_id.strip():
        parser.error("--human-id is required with --approve")
    print(json.dumps(run_reference_demo(args.approve, args.human_id), indent=2))


if __name__ == "__main__":
    main()
