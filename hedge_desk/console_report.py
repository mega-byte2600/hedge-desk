"""Build the desk-console (desk-console-1) payload from an engine report.

Single source of truth for turning a validated engine report into the exact
JSON the Emporion web console loads. Both the deploy-time exporter
(scripts/build_web.py) and the live-recompute server endpoint
(hedge_desk.server:/api/report) call ``build_console_payload`` so the two can
never drift: a freshly recomputed report on the live site renders through the
same packaging, schema, and registry as the checked-in deploy snapshot.
"""

from dataclasses import asdict

from hedge_desk.candidates import build_candidate_feed
from hedge_desk.data import PWB_DAILY_NEWS_DATASET
from hedge_desk.projects import DESK_ARCHITECTURE
from hedge_desk.reporting import (
    build_control_summary,
    render_morning_markdown,
    validate_report,
)
from hedge_desk.risk.dashboard import build_candidate_risk_dashboard

CONSOLE_SCHEMA = "desk-console-1"


def build_console_payload(report):
    """Wrap a validated engine ``report`` into the desk-console-1 payload.

    Raises ``ValueError`` if the report does not pass the release gate, so a
    non-publishable report is never served to the console.
    """
    decision = validate_report(report)
    if not decision.publishable:
        raise ValueError(
            "Report rejected: " + ", ".join(decision.reason_codes)
        )
    candidate_feed = build_candidate_feed()
    payload = {
        "schema_version": CONSOLE_SCHEMA,
        "report": report,
        "summary": build_control_summary(report),
        "registry": [asdict(project) for project in DESK_ARCHITECTURE],
        "morning_markdown": render_morning_markdown(report),
        "candidate_feed": candidate_feed,
        "risk_dashboard": build_candidate_risk_dashboard(candidate_feed),
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
                "feeds": [
                    "earnings-event-desk",
                    "open-quant-ai-model-lab",
                    "event-futures-desk",
                ],
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
    return payload
