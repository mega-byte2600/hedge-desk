"""Filesystem-first dataset manifest contract for Emporion research data."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from hashlib import sha256
import json
from pathlib import PurePosixPath
from typing import Any, Mapping, Optional, Tuple


DATASET_MANIFEST_SCHEMA_VERSION = "emporion-dataset-manifest-1.0.0"
ALLOWED_DATA_ZONES = (
    "raw",
    "normalized",
    "features",
    "research",
    "backtests",
    "models",
    "snapshots",
    "quarantine",
)
ALLOWED_PARTITIONS = (
    "asset_class",
    "venue",
    "symbol",
    "year",
    "month",
    "source",
)
SENSITIVE_FIELD_HINTS = ("secret", "token", "password", "oauth", "credential")


class DatasetValidationStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    QUARANTINED = "quarantined"
    PENDING = "pending"


@dataclass(frozen=True)
class DatasetManifest:
    dataset_id: str
    schema_version: str
    source: str
    created_at: datetime
    min_timestamp: str
    max_timestamp: str
    row_count: int
    format: str
    storage_path: str
    partitioning: Tuple[str, ...]
    validation_status: DatasetValidationStatus
    checksum_sha256: str
    parent_dataset_id: Optional[str]
    transformation: Optional[str]
    manifest_sha256: str


def _valid_hash(value: str) -> bool:
    try:
        return isinstance(value, str) and len(value) == 64 and int(value, 16) > 0
    except (TypeError, ValueError):
        return False


def _parse_utc_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("manifest timestamps must be timezone aware")
    return parsed


def _canonical_payload(manifest: DatasetManifest) -> Mapping[str, Any]:
    return {
        "checksum_sha256": manifest.checksum_sha256,
        "created_at": manifest.created_at.isoformat(),
        "dataset_id": manifest.dataset_id,
        "format": manifest.format,
        "max_timestamp": manifest.max_timestamp,
        "min_timestamp": manifest.min_timestamp,
        "parent_dataset_id": manifest.parent_dataset_id,
        "partitioning": list(manifest.partitioning),
        "row_count": manifest.row_count,
        "schema_version": manifest.schema_version,
        "source": manifest.source,
        "storage_path": manifest.storage_path,
        "transformation": manifest.transformation,
        "validation_status": manifest.validation_status.value,
    }


def parse_dataset_manifest(payload: Mapping[str, Any]) -> DatasetManifest:
    """Parse a strict manifest without trusting its claimed manifest hash."""
    expected = set(_canonical_payload(
        DatasetManifest(
            dataset_id="_",
            schema_version=DATASET_MANIFEST_SCHEMA_VERSION,
            source="_",
            created_at=datetime.fromtimestamp(0).astimezone(),
            min_timestamp="_",
            max_timestamp="_",
            row_count=0,
            format="parquet",
            storage_path="data/raw/_/part-000.parquet",
            partitioning=(),
            validation_status=DatasetValidationStatus.PENDING,
            checksum_sha256="1" * 64,
            parent_dataset_id=None,
            transformation=None,
            manifest_sha256="1" * 64,
        )
    ))
    expected.add("manifest_sha256")
    if set(payload) != expected:
        raise ValueError("dataset manifest schema invalid")

    if any(hint in key.lower() for key in payload for hint in SENSITIVE_FIELD_HINTS):
        raise ValueError("dataset manifest must not contain secret-bearing fields")
    if payload["schema_version"] != DATASET_MANIFEST_SCHEMA_VERSION:
        raise ValueError("dataset manifest version unsupported")
    if payload["format"] != "parquet":
        raise ValueError("material research datasets must be stored as parquet")
    if not _valid_hash(str(payload["checksum_sha256"])):
        raise ValueError("dataset checksum invalid")

    row_count = payload["row_count"]
    if type(row_count) is not int or row_count < 0:
        raise ValueError("dataset row count must be a nonnegative integer")

    partitioning = tuple(str(item) for item in payload["partitioning"])
    if len(set(partitioning)) != len(partitioning) or any(
        item not in ALLOWED_PARTITIONS for item in partitioning
    ):
        raise ValueError("dataset partitioning is invalid")
    if len(partitioning) > 4:
        raise ValueError("dataset partitioning is over-specified")

    storage_path = PurePosixPath(str(payload["storage_path"]))
    parts = storage_path.parts
    if len(parts) < 3 or parts[0] != "data" or parts[1] not in ALLOWED_DATA_ZONES:
        raise ValueError("dataset storage path must be under an approved data zone")
    if any(part in ("", ".", "..") for part in parts):
        raise ValueError("dataset storage path must be normalized")
    if storage_path.suffix != ".parquet":
        raise ValueError("dataset storage path must reference a parquet file")
    if str(storage_path).startswith("data/manifests/"):
        raise ValueError("dataset files cannot live inside the manifest catalog")
    for optional_field in ("parent_dataset_id", "transformation"):
        value = payload[optional_field]
        if value is not None and not isinstance(value, str):
            raise ValueError("dataset lineage fields must be strings or null")

    created_at = _parse_utc_datetime(str(payload["created_at"]))
    status = DatasetValidationStatus(str(payload["validation_status"]))
    manifest = DatasetManifest(
        dataset_id=str(payload["dataset_id"]),
        schema_version=str(payload["schema_version"]),
        source=str(payload["source"]),
        created_at=created_at,
        min_timestamp=str(payload["min_timestamp"]),
        max_timestamp=str(payload["max_timestamp"]),
        row_count=row_count,
        format=str(payload["format"]),
        storage_path=str(storage_path),
        partitioning=partitioning,
        validation_status=status,
        checksum_sha256=str(payload["checksum_sha256"]),
        parent_dataset_id=payload["parent_dataset_id"],
        transformation=payload["transformation"],
        manifest_sha256=str(payload["manifest_sha256"]),
    )
    if not manifest.dataset_id or not manifest.source:
        raise ValueError("dataset identity and source are required")
    if (
        manifest.validation_status is DatasetValidationStatus.PASSED
        and manifest.row_count == 0
    ):
        raise ValueError("passed datasets must contain rows")
    expected_hash = dataset_manifest_sha256(manifest)
    if manifest.manifest_sha256 != expected_hash:
        raise ValueError("dataset manifest hash mismatch")
    return manifest


def dataset_manifest_sha256(manifest: DatasetManifest) -> str:
    payload = _canonical_payload(manifest)
    return sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def build_dataset_manifest(
    *,
    dataset_id: str,
    source: str,
    created_at: datetime,
    min_timestamp: str,
    max_timestamp: str,
    row_count: int,
    storage_path: str,
    partitioning: Tuple[str, ...],
    validation_status: DatasetValidationStatus,
    checksum_sha256: str,
    parent_dataset_id: Optional[str] = None,
    transformation: Optional[str] = None,
) -> DatasetManifest:
    candidate = DatasetManifest(
        dataset_id=dataset_id,
        schema_version=DATASET_MANIFEST_SCHEMA_VERSION,
        source=source,
        created_at=created_at,
        min_timestamp=min_timestamp,
        max_timestamp=max_timestamp,
        row_count=row_count,
        format="parquet",
        storage_path=storage_path,
        partitioning=partitioning,
        validation_status=validation_status,
        checksum_sha256=checksum_sha256,
        parent_dataset_id=parent_dataset_id,
        transformation=transformation,
        manifest_sha256="0" * 64,
    )
    manifest = DatasetManifest(
        **{**candidate.__dict__, "manifest_sha256": dataset_manifest_sha256(candidate)}
    )
    parse_dataset_manifest({
        **_canonical_payload(manifest),
        "manifest_sha256": manifest.manifest_sha256,
    })
    return manifest
