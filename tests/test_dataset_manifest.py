from datetime import datetime, timezone
import unittest

from hedge_desk.data.manifest import (
    DATASET_MANIFEST_SCHEMA_VERSION,
    DatasetValidationStatus,
    build_dataset_manifest,
    dataset_manifest_sha256,
    parse_dataset_manifest,
)


NOW = datetime(2026, 9, 8, 21, 0, tzinfo=timezone.utc)
CHECKSUM = "a" * 64


def manifest_payload():
    manifest = build_dataset_manifest(
        dataset_id="us_equity_daily",
        source="provider_name",
        created_at=NOW,
        min_timestamp="2000-01-01",
        max_timestamp="2026-09-08",
        row_count=100,
        storage_path="data/normalized/equities/venue=NASDAQ/symbol=AAPL/year=2026/month=09/part-000.parquet",
        partitioning=("venue", "symbol", "year", "month"),
        validation_status=DatasetValidationStatus.PASSED,
        checksum_sha256=CHECKSUM,
    )
    return {
        "checksum_sha256": manifest.checksum_sha256,
        "created_at": manifest.created_at.isoformat(),
        "dataset_id": manifest.dataset_id,
        "format": manifest.format,
        "manifest_sha256": manifest.manifest_sha256,
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


class DatasetManifestTests(unittest.TestCase):
    def test_parquet_manifest_round_trips_with_canonical_hash(self) -> None:
        payload = manifest_payload()
        parsed = parse_dataset_manifest(payload)

        self.assertEqual(parsed.schema_version, DATASET_MANIFEST_SCHEMA_VERSION)
        self.assertEqual(parsed.format, "parquet")
        self.assertEqual(parsed.storage_path.split("/", 2)[:2], ["data", "normalized"])
        self.assertEqual(parsed.manifest_sha256, dataset_manifest_sha256(parsed))

    def test_manifest_rejects_database_storage_and_non_parquet_bulk_data(self) -> None:
        payload = manifest_payload()
        payload["storage_path"] = "postgres://market_observations"
        payload["manifest_sha256"] = "b" * 64
        with self.assertRaisesRegex(ValueError, "approved data zone"):
            parse_dataset_manifest(payload)

        payload = manifest_payload()
        payload["format"] = "json"
        with self.assertRaisesRegex(ValueError, "parquet"):
            parse_dataset_manifest(payload)

    def test_manifest_rejects_unknown_fields_and_secret_metadata(self) -> None:
        payload = manifest_payload()
        payload["api_token"] = "nope"
        with self.assertRaisesRegex(ValueError, "schema invalid"):
            parse_dataset_manifest(payload)

    def test_manifest_rejects_non_parquet_path_and_nonstring_lineage(self) -> None:
        payload = manifest_payload()
        payload["storage_path"] = "data/normalized/equities/part-000.csv"
        payload["manifest_sha256"] = "b" * 64
        with self.assertRaisesRegex(ValueError, "parquet file"):
            parse_dataset_manifest(payload)

        payload = manifest_payload()
        payload["parent_dataset_id"] = 123
        payload["manifest_sha256"] = "b" * 64
        with self.assertRaisesRegex(ValueError, "lineage"):
            parse_dataset_manifest(payload)

    def test_manifest_rejects_overpartitioning_and_tampered_hash(self) -> None:
        with self.assertRaisesRegex(ValueError, "over-specified"):
            build_dataset_manifest(
                dataset_id="too_many_parts",
                source="provider",
                created_at=NOW,
                min_timestamp="2026-01-01",
                max_timestamp="2026-09-08",
                row_count=1,
                storage_path="data/features/market/source=x/asset_class=equity/venue=NASDAQ/symbol=AAPL/year=2026/month=09/part-000.parquet",
                partitioning=("source", "asset_class", "venue", "symbol", "year"),
                validation_status=DatasetValidationStatus.PASSED,
                checksum_sha256=CHECKSUM,
            )

        payload = manifest_payload()
        payload["row_count"] = 101
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            parse_dataset_manifest(payload)

    def test_passed_manifest_must_have_rows(self) -> None:
        with self.assertRaisesRegex(ValueError, "must contain rows"):
            build_dataset_manifest(
                dataset_id="empty_pass",
                source="provider",
                created_at=NOW,
                min_timestamp="2026-01-01",
                max_timestamp="2026-09-08",
                row_count=0,
                storage_path="data/research/candidates/year=2026/part-000.parquet",
                partitioning=("year",),
                validation_status=DatasetValidationStatus.PASSED,
                checksum_sha256=CHECKSUM,
            )


if __name__ == "__main__":
    unittest.main()
