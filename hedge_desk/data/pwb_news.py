"""Licensed Papers With Backtest daily-news adapter.

The adapter keeps vendor text in memory and emits only content-addressed,
symbol-level research features.  Those features never authorize a trade.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone, tzinfo
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json
import os
from typing import Any, Callable, Iterable, Mapping, Optional, Tuple

from .news import NewsBatchGate, NewsObservation, NewsTransport, evaluate_news_batch


PWB_DAILY_NEWS_DATASET = "All-Daily-News"
PWB_DAILY_NEWS_SOURCE_ID = "papers-with-backtest:All-Daily-News"


@dataclass(frozen=True)
class PwbSymbolNewsFeature:
    symbol: str
    article_count: int
    average_symbol_sentiment: Decimal
    latest_published_at: datetime
    evidence_sha256: Tuple[str, ...]


@dataclass(frozen=True)
class PwbDailyNewsResult:
    dataset_id: str
    source_id: str
    evaluated_at: datetime
    gate: NewsBatchGate
    features: Tuple[PwbSymbolNewsFeature, ...]
    raw_content_retained: bool = False
    trade_authorized: bool = False


def _sequence(value: Any) -> Tuple[Any, ...]:
    if value is None or isinstance(value, (str, bytes, Mapping)):
        return ()
    try:
        return tuple(value)
    except TypeError:
        return ()


def _timestamp(value: Any, source_timezone: Optional[tzinfo]) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    elif hasattr(value, "to_pydatetime"):
        parsed = value.to_pydatetime()
    elif isinstance(value, str) and value.strip():
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    else:
        raise ValueError("PWB_NEWS_DATETIME_INVALID")
    if parsed.tzinfo is None:
        if source_timezone is None:
            raise ValueError("PWB_NEWS_SOURCE_TIMEZONE_REQUIRED")
        parsed = parsed.replace(tzinfo=source_timezone)
    return parsed.astimezone(timezone.utc)


def _decimal(value: Any) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("PWB_NEWS_SENTIMENT_INVALID")
    if not result.is_finite() or result < Decimal("-1") or result > Decimal("1"):
        raise ValueError("PWB_NEWS_SENTIMENT_INVALID")
    return result


def _rows(frame: Any) -> Iterable[Mapping[str, Any]]:
    if hasattr(frame, "to_dict"):
        records = frame.to_dict(orient="records")
    else:
        records = frame
    if not isinstance(records, Iterable):
        raise ValueError("PWB_NEWS_DATASET_INVALID")
    for row in records:
        if not isinstance(row, Mapping):
            raise ValueError("PWB_NEWS_ROW_INVALID")
        yield row


def _canonical_hash(row: Mapping[str, Any], published_at: datetime) -> str:
    symbol_sentiment = []
    for item in _sequence(row.get("symbol_sentiment")):
        if isinstance(item, Mapping):
            symbol_sentiment.append({
                "symbol": str(item.get("symbol", "")).strip().upper(),
                "sentiment_score": str(item.get("sentiment_score", "")),
            })
    payload = {
        "datetime": published_at.isoformat(),
        "source": str(row.get("source", "")).strip(),
        "symbols": sorted(str(value).strip().upper() for value in _sequence(row.get("symbols"))),
        "title": str(row.get("title", "")).strip(),
        "url": str(row.get("url", "")).strip(),
        "symbol_sentiment": sorted(symbol_sentiment, key=lambda value: value["symbol"]),
    }
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def evaluate_pwb_daily_news(
    frame: Any,
    *,
    license_id: str,
    evaluated_at: datetime,
    source_timezone: Optional[tzinfo],
    publication_embargo: timedelta = timedelta(days=1),
    maximum_age_seconds: int = 172800,
) -> PwbDailyNewsResult:
    """Normalize and aggregate PWB news without retaining vendor text.

    The default one-day embargo is deliberately conservative for daily rows
    whose example timestamps may be midnight.  A strategy can shorten it only
    after independently validating the vendor's timestamp semantics.
    """
    if evaluated_at.tzinfo is None:
        raise ValueError("PWB_NEWS_EVALUATED_AT_NOT_TIMEZONE_AWARE")
    if not license_id.strip():
        raise ValueError("PWB_NEWS_LICENSE_ID_REQUIRED")
    if publication_embargo < timedelta(0):
        raise ValueError("PWB_NEWS_EMBARGO_INVALID")

    observations = []
    sentiments = []
    for index, row in enumerate(_rows(frame)):
        published_at = _timestamp(row.get("datetime"), source_timezone)
        available_at = published_at + publication_embargo
        url = str(row.get("url", "")).strip()
        content_hash = _canonical_hash(row, published_at)
        observation_id = f"pwb-news-{content_hash[:20]}-{index}"
        observations.append(NewsObservation(
            observation_id=observation_id,
            source_id=PWB_DAILY_NEWS_SOURCE_ID,
            source_url=url,
            license_id=license_id,
            transport=NewsTransport.LICENSED_API,
            published_at=published_at,
            received_at=available_at,
            content_sha256=content_hash,
            publicly_available=True,
            redistribution_allowed=False,
        ))
        for item in _sequence(row.get("symbol_sentiment")):
            if not isinstance(item, Mapping):
                raise ValueError(f"PWB_NEWS_SYMBOL_SENTIMENT_INVALID:{index}")
            symbol = str(item.get("symbol", "")).strip().upper()
            if not symbol:
                raise ValueError(f"PWB_NEWS_SYMBOL_INVALID:{index}")
            sentiments.append((observation_id, symbol, _decimal(item.get("sentiment_score")), published_at, content_hash))
    if not observations:
        raise ValueError("PWB_NEWS_DATASET_EMPTY")

    gate = evaluate_news_batch(tuple(observations), evaluated_at.astimezone(timezone.utc), maximum_age_seconds)
    admitted = set(gate.admitted_observation_ids)
    grouped = {}
    for observation_id, symbol, sentiment, published_at, content_hash in sentiments:
        if observation_id in admitted:
            grouped.setdefault(symbol, []).append((sentiment, published_at, content_hash))
    features = []
    for symbol, values in sorted(grouped.items()):
        features.append(PwbSymbolNewsFeature(
            symbol=symbol,
            article_count=len(values),
            average_symbol_sentiment=sum((value[0] for value in values), Decimal("0")) / Decimal(len(values)),
            latest_published_at=max(value[1] for value in values),
            evidence_sha256=tuple(sorted(value[2] for value in values)),
        ))
    return PwbDailyNewsResult(
        PWB_DAILY_NEWS_DATASET,
        PWB_DAILY_NEWS_SOURCE_ID,
        evaluated_at.astimezone(timezone.utc),
        gate,
        tuple(features),
    )


def load_pwb_daily_news(loader: Optional[Callable[[str], Any]] = None) -> Any:
    """Load the licensed dataset using PWB's supported client."""
    if not (os.environ.get("PWB_API_KEY") or os.environ.get("HF_ACCESS_TOKEN")):
        raise ValueError("PWB_NEWS_API_CREDENTIAL_REQUIRED")
    if loader is None:
        try:
            from pwb_toolbox import datasets as pwb_datasets
        except ImportError as exc:
            raise RuntimeError("PWB_NEWS_TOOLBOX_NOT_INSTALLED") from exc
        loader = pwb_datasets.load_dataset
    return loader(PWB_DAILY_NEWS_DATASET)
