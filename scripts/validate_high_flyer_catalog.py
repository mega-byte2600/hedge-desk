"""Validate the offline High-Flyer/DeepSeek research source catalog."""

import json
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs" / "research" / "high_flyer" / "source_catalog.json"
ALLOWED_KINDS = {
    "code", "code_and_model_index", "dataset", "index", "model", "paper",
    "organization_statement",
}
ALLOWED_STATUSES = {"candidate", "reference"}
ALLOWED_DESKS = {
    "overnight-premium-desk", "earnings-event-desk", "arbitrage-observer",
    "dividend-opportunity-desk", "open-quant-ai-model-lab",
    "event-futures-desk",
}
REQUIRED_SOURCE_FIELDS = {
    "id", "kind", "title", "owner", "url", "license", "intake_status",
    "priority", "desks", "use",
}


def validate_catalog(payload):
    if not isinstance(payload, dict) or set(payload) != {
        "schema_version", "verified_at", "scope", "official_roots",
        "known_unreleased", "sources",
    }:
        raise ValueError("HIGH_FLYER_CATALOG_SCHEMA_INVALID")
    if payload["schema_version"] != "high-flyer-source-catalog-1.0.0":
        raise ValueError("HIGH_FLYER_CATALOG_VERSION_INVALID")
    sources = payload["sources"]
    if not isinstance(sources, list) or not sources:
        raise ValueError("HIGH_FLYER_CATALOG_EMPTY")
    identities = []
    urls = []
    for source in sources:
        if not isinstance(source, dict) or set(source) != REQUIRED_SOURCE_FIELDS:
            raise ValueError("HIGH_FLYER_SOURCE_SCHEMA_INVALID")
        identities.append(source["id"])
        urls.append(source["url"])
        parsed = urlparse(source["url"])
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("HIGH_FLYER_SOURCE_URL_INVALID")
        if source["kind"] not in ALLOWED_KINDS:
            raise ValueError("HIGH_FLYER_SOURCE_KIND_INVALID")
        if source["intake_status"] not in ALLOWED_STATUSES:
            raise ValueError("HIGH_FLYER_SOURCE_STATUS_INVALID")
        if type(source["priority"]) is not int or source["priority"] not in {1, 2, 3}:
            raise ValueError("HIGH_FLYER_SOURCE_PRIORITY_INVALID")
        if not source["desks"] or not set(source["desks"]).issubset(ALLOWED_DESKS):
            raise ValueError("HIGH_FLYER_SOURCE_DESK_INVALID")
        for field in ("id", "title", "owner", "license", "use"):
            if not isinstance(source[field], str) or not source[field].strip():
                raise ValueError("HIGH_FLYER_SOURCE_VALUE_INVALID")
    if len(identities) != len(set(identities)):
        raise ValueError("HIGH_FLYER_SOURCE_ID_DUPLICATE")
    return {
        "schema_version": payload["schema_version"],
        "source_count": len(sources),
        "candidate_count": sum(item["intake_status"] == "candidate" for item in sources),
        "paper_count": sum(item["kind"] == "paper" for item in sources),
        "dataset_count": sum(item["kind"] == "dataset" for item in sources),
        "status": "VALID",
    }


def main():
    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    print(json.dumps(validate_catalog(payload), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
