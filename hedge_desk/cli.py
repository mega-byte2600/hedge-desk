"""Command-line entry point for the frozen paper-only vertical slice."""

import argparse
import json
from pathlib import Path

from hedge_desk.demo import run_reference_demo
from hedge_desk.overnight import current_morning_report
from hedge_desk.projects import MVP_PROJECTS
from hedge_desk.wargames import build_war_game_report
from hedge_desk.reporting import render_morning_markdown
from hedge_desk.artifacts import build_artifact_bundle_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--morning-markdown",
        action="store_true",
        help="render the validated paper morning evaluation as Markdown",
    )
    parser.add_argument(
        "--war-games",
        action="store_true",
        help="run every declared synthetic premium-spread stress scenario",
    )
    parser.add_argument(
        "--overnight-report",
        action="store_true",
        help="run all four paper evaluations and emit the morning JSON report",
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
    args = parser.parse_args()
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
    if args.approve and not args.human_id.strip():
        parser.error("--human-id is required with --approve")
    print(json.dumps(run_reference_demo(args.approve, args.human_id), indent=2))


if __name__ == "__main__":
    main()
