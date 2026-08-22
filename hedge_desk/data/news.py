"""Point-in-time news/RSS evidence contracts; transport is not a license."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Tuple


class NewsTransport(str, Enum):
    RSS = "RSS"
    LICENSED_API = "LICENSED_API"
    PUBLIC_FILING = "PUBLIC_FILING"
    PUBLIC_AGENCY_FEED = "PUBLIC_AGENCY_FEED"


@dataclass(frozen=True)
class NewsObservation:
    observation_id: str
    source_id: str
    source_url: str
    license_id: str
    transport: NewsTransport
    published_at: datetime
    received_at: datetime
    content_sha256: str
    publicly_available: bool
    redistribution_allowed: bool


@dataclass(frozen=True)
class NewsBatchGate:
    admissible: bool
    admitted_observation_ids: Tuple[str, ...]
    rejected_observations: Tuple[Tuple[str, Tuple[str, ...]], ...]
    research_evidence_only: bool = True
    trade_authorized: bool = False
    raw_content_commit_allowed: bool = False


def _valid_hash(value: str) -> bool:
    try:
        return isinstance(value, str) and len(value) == 64 and int(value, 16) > 0
    except ValueError:
        return False


def evaluate_news_batch(
    observations: Tuple[NewsObservation, ...],
    decision_time: datetime,
    maximum_age_seconds: int,
) -> NewsBatchGate:
    if decision_time.tzinfo is None:
        raise ValueError("news decision time must be timezone-aware")
    if type(maximum_age_seconds) is not int or maximum_age_seconds < 0:
        raise ValueError("news maximum age must be a nonnegative integer")
    if not observations:
        raise ValueError("news batch cannot be empty")
    identities = [item.observation_id for item in observations]
    if any(not item for item in identities) or len(identities) != len(set(identities)):
        raise ValueError("news observation identities must be unique and nonempty")
    seen_content = set()
    seen_urls = set()
    admitted = []
    rejected = []
    for item in sorted(observations, key=lambda value: value.observation_id):
        reasons = []
        if not item.source_id or not item.license_id:
            reasons.append("NEWS_PROVENANCE_OR_LICENSE_MISSING")
        if not item.source_url.startswith("https://"):
            reasons.append("NEWS_SOURCE_URL_INVALID")
        if not item.publicly_available:
            reasons.append("NEWS_NOT_PUBLICLY_AVAILABLE")
        if (
            type(item.publicly_available) is not bool
            or type(item.redistribution_allowed) is not bool
        ):
            reasons.append("NEWS_ENTITLEMENT_FLAGS_INVALID")
        if not _valid_hash(item.content_sha256):
            reasons.append("NEWS_CONTENT_HASH_INVALID")
        if item.published_at.tzinfo is None or item.received_at.tzinfo is None:
            reasons.append("NEWS_TIMESTAMP_NOT_TIMEZONE_AWARE")
        else:
            if item.received_at < item.published_at:
                reasons.append("NEWS_RECEIVED_BEFORE_PUBLICATION")
            if item.received_at > decision_time:
                reasons.append("NEWS_POINT_IN_TIME_VIOLATION")
            elif (decision_time - item.received_at).total_seconds() > maximum_age_seconds:
                reasons.append("NEWS_STALE")
        if item.content_sha256 in seen_content or item.source_url in seen_urls:
            reasons.append("NEWS_DUPLICATE_EVIDENCE")
        seen_content.add(item.content_sha256)
        seen_urls.add(item.source_url)
        reason_codes = tuple(sorted(set(reasons)))
        if reason_codes:
            rejected.append((item.observation_id, reason_codes))
        else:
            admitted.append(item.observation_id)
    return NewsBatchGate(
        bool(admitted), tuple(admitted), tuple(rejected), True, False, False
    )
