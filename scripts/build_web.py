"""Export an engine-validated synthetic report for the read-only web console."""
import argparse
import json
import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hedge_desk.overnight import current_morning_report

# Static console assets copied verbatim from web/ into the deploy bundle.
# build_web.py FAILS if index.html references a local asset not listed here,
# so a file can never silently drop out of the deployment (ror-positioning.js
# was once referenced but not shipped, breaking the ES-module loader on deploy).
CONSOLE_ASSETS = (
    "index.html",
    "iphone-preview.html",
    "styles.css",
    "public-surface.js",
    "app.js",
    "candidate-context.js",
    "scenario-lab.js",
    "core.mjs",
    "professional.js",
    "ror-positioning.js",
    "yellow-sheet.css",
    "yellow-sheet.js",
    "acknowledgements.js",
    "brand-logo.js",
    "ui-polish.js",
    "resources.js",
    "desk-architecture.js",
    "multi-agent-desk.mjs",
    "timeline.json",
    "navigation-stability.js",
    "disclosures.js",
    "disclosures.json",
    "emporion-institutional-seal.svg",
    "account.js",
    "report.json",
)


def _index_html_local_assets(web_root: Path) -> set[str]:
    """Return local assets (./name) referenced by index.html as src/href."""
    index = (web_root / "index.html").read_text(encoding="utf-8")
    assets = set()
    for token in ('src="./', 'href="./'):
        start = 0
        while True:
            pos = index.find(token, start)
            if pos == -1:
                break
            end = index.find('"', pos + len(token))
            if end == -1:
                break
            assets.add(index[pos + len(token):end])
            start = end + 1
    return assets


def _verify_console_assets(web_root: Path) -> None:
    """Fail the build if index.html references a local asset not in CONSOLE_ASSETS
    or missing from disk. Prevents deploy-time module/MIME failures."""
    referenced = _index_html_local_assets(web_root)
    on_disk = {f.name for f in web_root.glob("*") if f.is_file()}
    missing_from_list = sorted(referenced - set(CONSOLE_ASSETS))
    if missing_from_list:
        raise SystemExit(
            "build_web.py FAILED: index.html references assets not in CONSOLE_ASSETS: "
            + ", ".join(missing_from_list)
        )
    missing_from_disk = sorted(referenced - on_disk)
    if missing_from_disk:
        raise SystemExit(
            "build_web.py FAILED: index.html references missing web/ files: "
            + ", ".join(missing_from_disk)
        )


def export_report(report, destination):
    from hedge_desk.console_report import build_console_payload

    payload = build_console_payload(report)
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
        _verify_console_assets(ROOT / "web")
        for filename in CONSOLE_ASSETS:
            shutil.copyfile(ROOT / "web" / filename, distribution / filename)
        shutil.copyfile(ROOT / "README_PUBLIC.md", distribution / "README_PUBLIC.md")
    print("Validated console report exported to", args.output)