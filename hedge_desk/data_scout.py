"""Discover public/open finance datasets and research repositories.

Discovery is data-first and bond-first. This module does not download restricted
payloads, bypass licenses, or treat repository visibility as commercial-use
permission. Model training and trade execution are intentionally out of scope.
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
    # mbolton priority: bonds/rates first because fixed income anchors discounting,
    # financing, macro regime, relative value, and cross-asset research.
    "treasury bond dataset yield curve rates",
    "fixed income bond dataset yields spreads",
    "sovereign bond dataset global yields",
    "corporate bond dataset credit spreads TRACE",
    "municipal bond dataset yields",
    "mortgage backed securities dataset MBS",
    "repo rates dataset SOFR secured financing",
    "interest rate swaps dataset OIS swap curve",
    "Treasury auction dataset debt issuance",
    "central bank rates yield curve dataset",
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
    "financial sentiment dataset huggingface",
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
    r"optionmetrics|taq|sec|edgar|fred|treasury|bond|bonds|yield|curve|trace|sofr|repo|swap|ois|"
    r"futures|options|earnings|filings|news)\b",
    re.IGNORECASE,
)

ASSET_PATTERNS = {
    "FIXED_INCOME_RATES": re.compile(r"\b(treasur(?:y|ies)|bond|bonds|yield curve|rates?|fixed income|sofr|repo|swap|ois)\b", re.I),
    "CREDIT": re.compile(r"\b(corporate bond|credit spread|high yield|investment grade|trace|default|cds)\b", re.I),
    "MUNICIPALS": re.compile(r"\b(municipal|muni|msrb)\b", re.I),
    "MBS_STRUCTURED": re.compile(r"\b(mbs|mortgage.backed|agency mbs|cmbs|abs|structured credit)\b", re.I),
    "SOVEREIGN": re.compile(r"\b(sovereign|government bond|gilt|bund|jgb|treasur(?:y|ies))\b", re.I),
    "EQUITIES": re.compile(r"\b(equity|equities|stock|stocks|shares?)\b", re.I),
    "OPTIONS": re.compile(r"\b(option|options|volatility|vol surface|implied volatility)\b", re.I),
    "FUTURES_COMMODITIES": re.compile(r"\b(futures?|commodit|oil|gas|wheat|corn|gold)\b", re.I),
    "MACRO": re.compile(r"\b(macro|econom|inflation|gdp|employment|central bank|fred)\b", re.I),
    "FILINGS_FUNDAMENTALS": re.compile(r"\b(sec|edgar|filings?|fundamental|earnings|10-k|10-q)\b", re.I),
    "NEWS_NLP": re.compile(r"\b(news|sentiment|nlp|language|headline)\b", re.I),
}

REGION_PATTERNS = {
    "AMERICAS": re.compile(r"\b(us|u\.s\.|usa|american|sec|edgar|fred|treasury|sofr|trace|nasdaq|nyse|canada|brazil)\b", re.I),
    "EUROPE": re.compile(r"\b(europe|european|eu|uk|britain|germany|france|ecb|eurostat|gilt|bund|london)\b", re.I),
    "ASIA_PACIFIC": re.compile(r"\b(china|chinese|japan|jgb|korea|india|singapore|hong kong|asia|australia|deepseek)\b", re.I),
}

BOND_PRIORITY_PATTERNS = (
    re.compile(r"\b(treasur(?:y|ies)|government bond|sovereign|yield curve)\b", re.I),
    re.compile(r"\b(corporate bond|credit spread|trace|cds)\b", re.I),
    re.compile(r"\b(sofr|repo|swap|ois|secured financing)\b", re.I),
    re.compile(r"\b(municipal|muni|msrb|mbs|mortgage.backed)\b", re.I),
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
    asset_classes: tuple[str, ...] = ()
    regions: tuple[str, ...] = ()
    bond_priority: bool = False
    discovery_score: int = 0


def _classify(text: str, patterns: dict[str, re.Pattern]) -> tuple[str, ...]:
    return tuple(name for name, pattern in patterns.items() if pattern.search(text))


def _is_bond_priority(text: str) -> bool:
    return any(pattern.search(text) for pattern in BOND_PRIORITY_PATTERNS)


def _score(*, dataset_signal: bool, open_license: bool, stars: int, asset_classes: tuple[str, ...], regions: tuple[str, ...], bond_priority: bool) -> int:
    score = 0
    if dataset_signal:
        score += 35
    if open_license:
        score += 20
    if bond_priority:
        score += 25
    score += min(stars, 1000) // 50
    score += min(len(asset_classes) * 3, 12)
    score += min(len(regions) * 2, 6)
    return min(score, 100)


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
        combined = f"{name} {desc} {query}"
        open_license = bool(spdx and spdx.lower() in LICENSE_ALLOWLIST)
        dataset_signal = bool(DATA_HINTS.search(combined))
        asset_classes = _classify(combined, ASSET_PATTERNS)
        regions = _classify(combined, REGION_PATTERNS)
        bond_priority = _is_bond_priority(combined)
        stars = int(item.get("stargazers_count") or 0)
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
                stars=stars,
                updated_at=item.get("updated_at") or "",
                license_spdx=spdx,
                open_license=open_license,
                dataset_signal=dataset_signal,
                commercial_use_status=commercial,
                discovered_at=now,
                query=query,
                asset_classes=asset_classes,
                regions=regions,
                bond_priority=bond_priority,
                discovery_score=_score(
                    dataset_signal=dataset_signal,
                    open_license=open_license,
                    stars=stars,
                    asset_classes=asset_classes,
                    regions=regions,
                    bond_priority=bond_priority,
                ),
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
                candidate_rank = (candidate.discovery_score, candidate.stars, candidate.updated_at)
                current_rank = (current.discovery_score, current.stars, current.updated_at) if current else None
                if current is None or candidate_rank > current_rank:
                    seen[candidate.repo] = candidate
        except Exception as exc:  # discovery must fail soft per query
            errors.append({"query": query, "error": type(exc).__name__})
    ranked = sorted(
        seen.values(),
        key=lambda x: (x.bond_priority, x.discovery_score, x.dataset_signal, x.open_license, x.stars, x.updated_at),
        reverse=True,
    )
    return {
        "schema_version": "hedge-desk-data-scout-1.2.0",
        "purpose": "OPEN_PUBLIC_DATASET_DISCOVERY_ONLY",
        "builder": "mbolton",
        "priority": "BONDS_RATES_CREDIT_FIRST",
        "commercial_use_assumed": False,
        "model_training_enabled": False,
        "ranking_note": "Bond/rates/credit datasets are deliberately prioritized, followed by dataset signal, permissive-license metadata, relevance breadth, and repository adoption. Discovery is not legal or data-quality approval.",
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
