"""Validate a Muse research-findings file against the intake schema.

Muse (a meta agent app) contributes research findings to the desk via the GitHub
API — it writes a dated findings JSON into docs/research/muse/ and opens a PR.
This validator is the CI gate on that path: it enforces the intake contract so a
finding can never silently become a candidate or a trade.

Contract (mirrors docs/research/muse/README.md):
- Findings are RESEARCH INPUT, never trusted desk output. They become candidates
  or Yellow Sheets only after independent review.
- Every claim must cite a public https source. No fabricated numbers.
- No probability/RoR claims on delayed data, no trade authorization, no secrets/PII.
- A finding cannot relax a risk gate or the paper-only boundary.

Usage:
    python scripts/validate_muse_findings.py docs/research/muse/2026-09-25.json
Exits 0 and prints a JSON verdict on success; raises a named error code on failure.
"""

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs" / "research" / "muse" / "findings.schema.json"

ALLOWED_KINDS = {"fundamental_brief", "competitive", "event_watch", "risk_flag"}
ALLOWED_SYMBOLS = {"MARKET", "PRODUCT"}
# Standing firewall: these must never appear as a claim in a finding.
FORBIDDEN_CLAIMS = (
    "probability", "prob of", "risk of ruin", "ror", "trade_authorized",
    "guaranteed", "certain", "no risk", "risk-free",
)
# Secret/PII redaction guard: flag obvious credential/identity leaks.
SECRET_PATTERNS = (
    re.compile(r"(?i)\b(api[_-]?key|secret|token|password|bearer)\b\s*[:=]"),
    re.compile(r"\bgh[opsu]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b"),  # SSN
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),  # email
)


def _load_schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_findings(payload):
    if not isinstance(payload, dict):
        raise ValueError("MUSE_FINDINGS_NOT_OBJECT")
    if payload.get("schema_version") != "muse-findings-1.0.0":
        raise ValueError("MUSE_FINDINGS_VERSION_INVALID")
    if payload.get("author") != "muse":
        raise ValueError("MUSE_FINDINGS_AUTHOR_INVALID")
    session = payload.get("session")
    if not isinstance(session, str) or not session.strip():
        raise ValueError("MUSE_FINDINGS_SESSION_INVALID")
    findings = payload.get("findings")
    if not isinstance(findings, list) or not findings:
        raise ValueError("MUSE_FINDINGS_EMPTY")

    ids = []
    for finding in findings:
        if not isinstance(finding, dict):
            raise ValueError("MUSE_FINDING_NOT_OBJECT")
        fid = finding.get("id")
        if not isinstance(fid, str) or not re.match(r"^[a-z0-9-]+$", fid):
            raise ValueError("MUSE_FINDING_ID_INVALID")
        ids.append(fid)
        if finding.get("kind") not in ALLOWED_KINDS:
            raise ValueError("MUSE_FINDING_KIND_INVALID")
        symbol = finding.get("symbol")
        if not isinstance(symbol, str) or not (
            symbol in ALLOWED_SYMBOLS or re.match(r"^[A-Z]{1,5}$", symbol)
        ):
            raise ValueError("MUSE_FINDING_SYMBOL_INVALID")
        for field in ("title", "summary"):
            if not isinstance(finding.get(field), str) or not finding[field].strip():
                raise ValueError("MUSE_FINDING_VALUE_INVALID")
        sources = finding.get("sources")
        if not isinstance(sources, list) or not sources:
            raise ValueError("MUSE_FINDING_SOURCES_EMPTY")
        for url in sources:
            if not isinstance(url, str):
                raise ValueError("MUSE_FINDING_SOURCE_NOT_STRING")
            parsed = urlparse(url)
            if parsed.scheme != "https" or not parsed.netloc:
                raise ValueError("MUSE_FINDING_SOURCE_URL_INVALID")

        # Standing firewall: no forbidden claims, no secrets/PII.
        blob = " ".join(
            str(finding.get(k, "")) for k in ("title", "summary", "catalysts", "risk_flags")
        ).lower()
        for claim in FORBIDDEN_CLAIMS:
            if claim in blob:
                raise ValueError("MUSE_FINDING_FORBIDDEN_CLAIM_%s" % claim.upper().replace(" ", "_"))
        for pattern in SECRET_PATTERNS:
            if pattern.search(blob):
                raise ValueError("MUSE_FINDING_SECRET_OR_PII")

    if len(ids) != len(set(ids)):
        raise ValueError("MUSE_FINDING_ID_DUPLICATE")

    return {
        "schema_version": payload["schema_version"],
        "session": session,
        "finding_count": len(findings),
        "kinds": sorted({f["kind"] for f in findings}),
        "symbols": sorted({f["symbol"] for f in findings}),
        "status": "VALID",
        "note": "Research input only. Not a candidate, not a trade, not reviewed.",
    }


def main():
    if len(sys.argv) != 2:
        print("usage: python scripts/validate_muse_findings.py <findings.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "INVALID", "error": "MUSE_FINDINGS_UNREADABLE", "detail": str(exc)}))
        return 1
    try:
        verdict = validate_findings(payload)
    except ValueError as exc:
        print(json.dumps({"status": "INVALID", "error": str(exc)}))
        return 1
    print(json.dumps(verdict, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
