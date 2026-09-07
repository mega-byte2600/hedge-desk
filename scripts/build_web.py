"""Export an engine-validated synthetic report for the read-only web console."""
import argparse
import json
import sys
import shutil
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hedge_desk.overnight import current_morning_report
from hedge_desk.projects import MVP_PROJECTS
from hedge_desk.reporting import build_control_summary, render_morning_markdown, validate_report
from hedge_desk.data import PWB_DAILY_NEWS_DATASET
from hedge_desk.candidates import build_candidate_feed


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
        "candidate_feed": build_candidate_feed(),
        "owner": {
            "display_name": "mbolton",
            "linkedin_url": "https://www.linkedin.com/in/bolton-2600/",
        },
        "research_data_sources": [
            {
                "source_id": "papers-with-backtest",
                "dataset": PWB_DAILY_NEWS_DATASET,
                "status": "ADAPTER_READY",
                "mode": "LICENSED_RESEARCH_ONLY",
                "feeds": ["earnings-event-desk", "open-quant-ai-model-lab", "event-futures-desk"],
                "controls": [
                    "point-in-time embargo",
                    "explicit source timezone",
                    "entitlement identifier",
                    "content hashes",
                    "no vendor text retention",
                    "no trade authorization",
                ],
            }
        ],
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
    if args.output.resolve() == (ROOT / "web").resolve():
        distribution = ROOT / "dist"
        distribution.mkdir(exist_ok=True)
        for filename in (
            "index.html",
            "styles.css",
            "app.js",
            "core.mjs",
            "professional.js",
            "yellow-sheet.css",
            "yellow-sheet.js",
            "acknowledgements.js",
            "brand-logo.js",
            "emporion-mark.svg",
            "report.json",
        ):
            shutil.copyfile(ROOT / "web" / filename, distribution / filename)
        shutil.copyfile(ROOT / "README_PUBLIC.md", distribution / "README_PUBLIC.md")
    print("Validated console report exported to", args.output)
