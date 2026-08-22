"""Strict canonical option-snapshot schema for validated local data."""

import json
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, Tuple

from .spreads import OptionQuote, OptionType, UnderlyingQuote


OPTION_SNAPSHOT_SCHEMA_VERSION = "hedge-desk-option-snapshot-1.0.0"
_ROOT_FIELDS = frozenset({"schema_version", "underlying_quote", "option_quotes"})
_UNDERLYING_FIELDS = frozenset({"symbol", "bid", "ask", "quoted_at"})
_OPTION_FIELDS = frozenset(
    {
        "contract_id",
        "underlying",
        "option_type",
        "strike",
        "expiration",
        "bid",
        "ask",
        "bid_size",
        "ask_size",
        "quoted_at",
        "open_interest",
        "volume",
    }
)


@dataclass(frozen=True)
class OptionSnapshot:
    schema_version: str
    source_id: str
    underlying_quote: UnderlyingQuote
    option_quotes: Tuple[OptionQuote, ...]
    source_artifact_sha256: str = "0" * 64


def _exact_fields(value: Any, expected: frozenset, label: str) -> Dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    missing = sorted(expected - set(value))
    unknown = sorted(set(value) - expected)
    if missing:
        raise ValueError(f"{label} fields missing: " + ",".join(missing))
    if unknown:
        raise ValueError(f"{label} fields unknown: " + ",".join(unknown))
    return value


def _decimal(value: Any, field: str) -> Decimal:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a decimal string")
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{field} must be a valid decimal string") from exc
    if not parsed.is_finite():
        raise ValueError(f"{field} must be finite")
    return parsed


def _integer(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field} must be an integer")
    return value


def _datetime(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO-8601 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be valid ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include a timezone")
    return parsed


def _date(value: Any, field: str) -> date:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO date string")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be a valid ISO date") from exc


def parse_option_snapshot(
    path: Path, source_id: str, source_artifact_sha256: str = "0" * 64
) -> OptionSnapshot:
    if not source_id:
        raise ValueError("validated source identity is required")
    try:
        hash_valid = len(source_artifact_sha256) == 64 and int(
            source_artifact_sha256, 16
        ) >= 0
    except ValueError:
        hash_valid = False
    if not hash_valid:
        raise ValueError("validated source artifact hash is required")
    try:
        root = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("option snapshot must be readable UTF-8 JSON") from exc
    root = _exact_fields(root, _ROOT_FIELDS, "option snapshot")
    if root["schema_version"] != OPTION_SNAPSHOT_SCHEMA_VERSION:
        raise ValueError("option snapshot schema version is not supported")
    underlying = _exact_fields(
        root["underlying_quote"], _UNDERLYING_FIELDS, "underlying quote"
    )
    if not isinstance(underlying["symbol"], str):
        raise ValueError("underlying symbol must be a string")
    underlying_quote = UnderlyingQuote(
        underlying["symbol"],
        _decimal(underlying["bid"], "underlying bid"),
        _decimal(underlying["ask"], "underlying ask"),
        _datetime(underlying["quoted_at"], "underlying quoted_at"),
        source_id,
    )
    if not isinstance(root["option_quotes"], list) or not root["option_quotes"]:
        raise ValueError("option_quotes must be a non-empty array")
    quotes = []
    for index, item in enumerate(root["option_quotes"]):
        quote = _exact_fields(item, _OPTION_FIELDS, f"option quote {index}")
        for field in ("contract_id", "underlying", "option_type"):
            if not isinstance(quote[field], str):
                raise ValueError(f"option quote {index} {field} must be a string")
        try:
            option_type = OptionType(quote["option_type"])
        except ValueError as exc:
            raise ValueError(f"option quote {index} option_type is unsupported") from exc
        parsed = OptionQuote(
            quote["contract_id"],
            quote["underlying"],
            option_type,
            _decimal(quote["strike"], f"option quote {index} strike"),
            _date(quote["expiration"], f"option quote {index} expiration"),
            _decimal(quote["bid"], f"option quote {index} bid"),
            _decimal(quote["ask"], f"option quote {index} ask"),
            _integer(quote["bid_size"], f"option quote {index} bid_size"),
            _integer(quote["ask_size"], f"option quote {index} ask_size"),
            _datetime(quote["quoted_at"], f"option quote {index} quoted_at"),
            source_id,
            _integer(quote["open_interest"], f"option quote {index} open_interest"),
            _integer(quote["volume"], f"option quote {index} volume"),
        )
        if parsed.underlying != underlying_quote.symbol:
            raise ValueError("option and underlying symbols must match")
        quotes.append(parsed)
    contract_ids = [quote.contract_id for quote in quotes]
    if len(contract_ids) != len(set(contract_ids)):
        raise ValueError("option contract identities must be unique")
    return OptionSnapshot(
        OPTION_SNAPSHOT_SCHEMA_VERSION,
        source_id,
        underlying_quote,
        tuple(sorted(quotes, key=lambda item: item.contract_id)),
        source_artifact_sha256,
    )
