"""Versioned regulatory-source traceability for deterministic paper controls."""

import json
from dataclasses import dataclass
from hashlib import sha256
from typing import Tuple


TRACEABILITY_VERSION = "regulatory-traceability-1.0.0"


@dataclass(frozen=True)
class RegulatoryRequirement:
    requirement_id: str
    authority: str
    source_url: str
    applicability: str
    reason_codes: Tuple[str, ...]
    test_module: str
    counsel_approved_for_live: bool = False


REFERENCE_REQUIREMENTS: Tuple[RegulatoryRequirement, ...] = (
    RegulatoryRequirement(
        "finra-options-account-controls", "FINRA",
        "https://www.finra.org/finramanual/rules/r2360",
        "options approval, disclosure, diligence, and account controls",
        ("OPTIONS_APPROVAL_REQUIRED", "OPTIONS_DISCLOSURE_ACKNOWLEDGEMENT_REQUIRED"),
        "tests.test_account_gate",
    ),
    RegulatoryRequirement(
        "occ-options-risk-disclosure", "OCC",
        "https://www.theocc.com/company-information/documents-and-archives/options-disclosure-document",
        "current options disclosure acknowledgement evidence",
        ("OPTIONS_DISCLOSURE_ACKNOWLEDGEMENT_REQUIRED",),
        "tests.test_account_gate",
    ),
    RegulatoryRequirement(
        "sec-automated-adviser-boundary", "SEC",
        "https://www.sec.gov/newsroom/press-releases/2017-52",
        "automated securities advice remains subject to adviser analysis",
        ("PAPER_ONLY_VIOLATION",),
        "tests.test_backoffice",
    ),
    RegulatoryRequirement(
        "cftc-hypothetical-results", "CFTC",
        "https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/fraudadv_tradingsystem.html",
        "hypothetical results require conspicuous limitations",
        ("HYPOTHETICAL_LABEL_REQUIRED",),
        "tests.test_reporting",
    ),
    RegulatoryRequirement(
        "finra-books-records", "FINRA",
        "https://www.finra.org/rules-guidance/key-topics/books-records",
        "future regulated retention requires external recordkeeping analysis",
        ("AUDIT_JOURNAL_CORRUPT",),
        "tests.test_audit_store",
    ),
)


def validate_traceability_registry(
    requirements: Tuple[RegulatoryRequirement, ...] = REFERENCE_REQUIREMENTS,
) -> Tuple[str, ...]:
    reasons = []
    identities = [item.requirement_id for item in requirements]
    if not requirements or len(identities) != len(set(identities)):
        reasons.append("REGULATORY_REQUIREMENT_ID_INVALID")
    allowed_hosts = ("https://www.finra.org/", "https://www.sec.gov/", "https://www.cftc.gov/", "https://www.theocc.com/")
    for item in requirements:
        if not item.requirement_id or not item.authority or not item.applicability:
            reasons.append("REGULATORY_REQUIREMENT_INCOMPLETE")
        if not item.source_url.startswith(allowed_hosts):
            reasons.append("REGULATORY_SOURCE_NOT_AUTHORITATIVE")
        if not item.reason_codes or item.reason_codes != tuple(sorted(set(item.reason_codes))):
            reasons.append("REGULATORY_REASON_MAPPING_INVALID")
        if not item.test_module.startswith("tests.test_"):
            reasons.append("REGULATORY_TEST_REFERENCE_INVALID")
    return tuple(sorted(set(reasons)))


def traceability_sha256(
    requirements: Tuple[RegulatoryRequirement, ...] = REFERENCE_REQUIREMENTS,
) -> str:
    reasons = validate_traceability_registry(requirements)
    if reasons:
        raise ValueError("regulatory traceability registry invalid")
    payload = {
        "version": TRACEABILITY_VERSION,
        "requirements": [
            {
                "requirement_id": item.requirement_id,
                "authority": item.authority,
                "source_url": item.source_url,
                "applicability": item.applicability,
                "reason_codes": list(item.reason_codes),
                "test_module": item.test_module,
                "counsel_approved_for_live": item.counsel_approved_for_live,
            }
            for item in requirements
        ],
    }
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
