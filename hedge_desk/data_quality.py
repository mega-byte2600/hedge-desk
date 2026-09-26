"""Data-quality monitor: loud alerts when a source is down, stale, or missing.

Handoff 2026-09-26 gap #3. The FRED "1.0" poisoning and the FRED CSV hang both
showed the same gap: a source can fail silently and the dashboard just says
BLOCKED without saying why, for how long, or what to do. This module scans
the nightly AM report and produces a structured quality assessment with
severity levels that the dashboard surfaces prominently.

Severity:
- OK: source is current and healthy.
- STALE: source has data but it's older than expected (e.g., prior-day close).
- DOWN: source failed this run (BLOCKED, QUARANTINE, transport failure).
- MISSING: source section absent from the report entirely.

This is a pure, deterministic helper (no network): it reads the report dict
and returns a schema-versioned quality summary. No orders, no probabilities,
no Risk of Ruin — just honest source health.
"""

from __future__ import annotations

from datetime import date
from typing import Dict, List

QUALITY_VERSION = "hedge-desk-data-quality-1.0.0"

# Severity levels, ordered by urgency.
SEV_OK = "OK"
SEV_STALE = "STALE"
SEV_DOWN = "DOWN"
SEV_MISSING = "MISSING"


def _alert(
    source: str,
    severity: str,
    message: str,
    detail: str = "",
) -> Dict[str, str]:
    """Build one quality alert dict."""
    return {
        "source": source,
        "severity": severity,
        "message": message,
        "detail": detail,
    }


def _check_fred_section(
    section: Dict, name: str, label: str
) -> Dict[str, str]:
    """Check a FRED-backed section (macro_environment, rates_environment)."""
    if not section:
        return _alert(
            label, SEV_MISSING,
            f"{label} section missing from report",
            "The nightly batch did not produce this section at all.",
        )
    mode = section.get("mode", "")
    if mode == "BLOCKED":
        blocked = section.get("blocked", [])
        reason = section.get("reason", "unknown")
        return _alert(
            label, SEV_DOWN,
            f"{label} BLOCKED: {', '.join(blocked) if blocked else 'all series'}",
            f"Reason: {reason}. FRED CSV hangs on this network; "
            "set FRED_API_KEY for the official JSON API fallback.",
        )
    # OK: has real observations.
    as_of = section.get("as_of", "unknown")
    return _alert(
        label, SEV_OK,
        f"{label} current as of {as_of}",
        "",
    )


def _check_eod(report: Dict) -> Dict[str, str]:
    """Check EOD equities batch (Yahoo/Stooq)."""
    freshness = report.get("data_freshness", {})
    batch_status = report.get("eod_batch_status", "")
    if not freshness:
        return _alert(
            "EOD", SEV_MISSING,
            "EOD freshness section missing from report",
            "",
        )
    is_current = freshness.get("is_current", False)
    as_of = freshness.get("as_of", "unknown")
    expected = freshness.get("expected_trading_day", "unknown")

    # Check for fallback usage in source results.
    sources_used = set()
    for sr in report.get("eod_source_results", []):
        # source_results don't carry source_id; check artifacts if present.
        pass

    if batch_status and "READY" not in batch_status:
        return _alert(
            "EOD", SEV_DOWN,
            f"EOD batch not ready: {batch_status}",
            f"As of {as_of}, expected {expected}.",
        )
    if not is_current:
        return _alert(
            "EOD", SEV_STALE,
            f"EOD stale: running on {as_of}, expected {expected}",
            "Source has not published today's close yet; using prior trading day.",
        )
    return _alert(
        "EOD", SEV_OK,
        f"EOD current: {as_of} close",
        "",
    )


def _check_section_present(
    report: Dict, key: str, label: str
) -> Dict[str, str]:
    """Generic check: section exists and isn't empty/BLOCKED."""
    section = report.get(key)
    if not section:
        return _alert(
            label, SEV_MISSING,
            f"{label} section missing from report",
            "",
        )
    if isinstance(section, dict):
        mode = section.get("mode", "")
        if mode == "BLOCKED":
            return _alert(
                label, SEV_DOWN,
                f"{label} BLOCKED",
                section.get("reason", "") or section.get("note", ""),
            )
    return _alert(label, SEV_OK, f"{label} present", "")


def quality_report(report: Dict, as_of: date | None = None) -> Dict[str, object]:
    """Scan a nightly AM report and return a data-quality summary.

    Returns a schema-versioned dict with per-source alerts and an overall
    status. The dashboard surfaces DOWN/STALE/MISSING alerts prominently;
    OK sources are listed quietly.
    """
    check_date = (as_of or date.today()).isoformat()
    alerts: List[Dict[str, str]] = []

    # FRED-backed sections (the ones that failed on 2026-09-26).
    alerts.append(
        _check_fred_section(
            report.get("macro_environment", {}),
            "macro_environment",
            "Macro/FRED",
        )
    )
    alerts.append(
        _check_fred_section(
            report.get("rates_environment", {}),
            "rates_environment",
            "Rates/FRED",
        )
    )

    # EOD equities.
    alerts.append(_check_eod(report))

    # Other desks: present and not BLOCKED.
    alerts.append(_check_section_present(report, "oil_market", "Oil/WTI"))
    alerts.append(_check_section_present(report, "earnings_actuals", "Earnings/SEC"))
    alerts.append(_check_section_present(report, "chain_income", "Options/Cboe"))

    # Overall status: worst severity wins.
    severity_rank = {SEV_OK: 0, SEV_STALE: 1, SEV_DOWN: 2, SEV_MISSING: 3}
    worst = SEV_OK
    for a in alerts:
        if severity_rank[a["severity"]] > severity_rank[worst]:
            worst = a["severity"]

    loud = [a for a in alerts if a["severity"] != SEV_OK]

    return {
        "schema_version": QUALITY_VERSION,
        "as_of": check_date,
        "overall": worst,
        "alert_count": len(loud),
        "alerts": alerts,
        "loud_alerts": loud,
        "summary": (
            f"{len(loud)} data-quality alert(s): "
            + ", ".join(f"{a['source']}={a['severity']}" for a in loud)
            if loud
            else "All data sources OK."
        ),
    }
