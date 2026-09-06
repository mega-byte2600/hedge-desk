"""Export an engine-validated synthetic report for the read-only web console."""
import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hedge_desk.overnight import current_morning_report
from hedge_desk.projects import MVP_PROJECTS
from hedge_desk.reporting import build_control_summary, render_morning_markdown, validate_report


def export_report(report, destination):
    decision = validate_report(report)
    if not decision.publishable:
        raise ValueError("Report rejected: " + ", ".join(decision.reason_codes))
    payload = {
        "schema_version": "desk-console-1",
        "report": report,
        "summary": build_control_summary(report),
        "registry": [asdict(project) for project in MVP_PROJECTS],
        "morning_markdown": render_morning_markdown(report),
    }
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    temporary = destination / "report.json.tmp"
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(destination / "report.json")
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, help="Existing finalized report; validated before export")
    parser.add_argument("--output", type=Path, default=ROOT / "web")
    args = parser.parse_args()
    report = json.loads(args.report.read_text()) if args.report else current_morning_report()
    export_report(report, args.output)
    print("Validated console report exported to", args.output)
