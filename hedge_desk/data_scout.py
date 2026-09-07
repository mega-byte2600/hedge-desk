"""Discover public/open finance datasets and research repositories.

This module is discovery-only. It does not download restricted datasets, bypass
licenses, or treat repository availability as permission for commercial use.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import quote_plus
from urllib.request import Request, urlopen


DEFAULT_QUERIES = (
    "finance dataset trading language:Python",
    "financial markets dataset hedge fund",
    "options dataset volatility surface",
    "earnings dataset financial NLP",
    "futures commodities dataset",
    "quantitative finance dataset",
    "financial news dataset",
    "SEC filings dataset finance",
    "macro economics dataset trading",
    "DeepSeek finance dataset",
    "FinGPT dataset finance",
)

LICENSE_ALLOWLIST = {
    "mit",
    "apache-2.0",
    "bsd-2-clause",
    "bsd-3-clause",
    "cc0-1.0",
    "unlicense",
}

DATA_HINTS = re.compile(
    r"\b(dataset|data set|csv|parquet|jsonl|hugging ?face|kaggle|wrds|crsp|compustat|ibes|"
    r"optionmetrics|taq|sec|edgar|fred|treasury|futures|options|earnings|filings|news)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class DatasetCandidate:
    repo: str
    url: str
    description: str
    stars: int
    updated_at: str
    license_spdx: str | None
    open_license: bool
    dataset_signal: bool
    commercial_use_status: str
    discovered_at: str
    query: str


def _github_json(url: str, token: str | None = None) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "hedge-desk-data-scout/1.0",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=20) as response:
        return json.load(response)


def search_github(query: str, *, token: str | None = None, per_page: int = 20) -> list[DatasetCandidate]:
    payload = _github_json(
        f"https://api.github.com/search/repositories?q={quote_plus(query)}&sort=updated&order=desc&per_page={per_page}",
        token,
    )
    now = datetime.now(timezone.utc).isoformat()
    out: list[DatasetCandidate] = []
    for item in payload.get("items", []):
        license_obj = item.get("license") or {}
        spdx = license_obj.get("spdx_id")
        desc = item.get("description") or ""
        name = item.get("full_name") or ""
        combined = f"{name} {desc}"
        open_license = bool(spdx and spdx.lower() in LICENSE_ALLOWLIST)
        dataset_signal = bool(DATA_HINTS.search(combined))
        if open_license:
            commercial = "OPEN_LICENSE_REVIEW_STILL_REQUIRED"
        elif spdx:
            commercial = "LICENSE_REVIEW_REQUIRED"
        else:
            commercial = "NO_LICENSE_METADATA_DO_NOT_USE"
        out.append(
            DatasetCandidate(
                repo=name,
                url=item.get("html_url") or "",
                description=desc,
                stars=int(item.get("stargazers_count") or 0),
                updated_at=item.get("updated_at") or "",
                license_spdx=spdx,
                open_license=open_license,
                dataset_signal=dataset_signal,
                commercial_use_status=commercial,
                discovered_at=now,
                query=query,
            )
        )
    return out


def discover(queries: Iterable[str] = DEFAULT_QUERIES, *, token: str | None = None) -> dict:
    seen: dict[str, DatasetCandidate] = {}
    errors: list[dict[str, str]] = []
    for query in queries:
        try:
            for candidate in search_github(query, token=token):
                current = seen.get(candidate.repo)
                if current is None or candidate.stars > current.stars:
                    seen[candidate.repo] = candidate
        except Exception as exc:  # discovery must fail soft per query
            errors.append({"query": query, "error": type(exc).__name__})
    ranked = sorted(
        seen.values(),
        key=lambda x: (x.dataset_signal, x.open_license, x.stars, x.updated_at),
        reverse=True,
    )
    return {
        "schema_version": "hedge-desk-data-scout-1.0.0",
        "purpose": "OPEN_PUBLIC_DATASET_DISCOVERY_ONLY",
        "commercial_use_assumed": False,
        "candidates": [asdict(x) for x in ranked],
        "errors": errors,
    }


def main() -> None:
    output = Path(os.getenv("DATA_SCOUT_OUTPUT", "artifacts/data-scout.json"))
    output.parent.mkdir(parents=True, exist_ok=True)
    result = discover(token=os.getenv("GITHUB_TOKEN"))
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(result['candidates'])} candidates to {output}")


if __name__ == "__main__":
    main()
