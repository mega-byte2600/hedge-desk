"""Canonical content manifest for uploaded overnight evaluation artifacts."""

import json
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Tuple


BUNDLE_MANIFEST_VERSION = "overnight-artifact-bundle-1.0.0"


def build_artifact_bundle_manifest(paths: Tuple[Path, ...]) -> Dict[str, Any]:
    if not paths:
        raise ValueError("at least one artifact path is required")
    names = [path.name for path in paths]
    if len(names) != len(set(names)):
        raise ValueError("artifact filenames must be unique")
    files = []
    for path in sorted(paths, key=lambda item: item.name):
        if not path.is_file():
            raise ValueError(f"artifact file is missing: {path.name}")
        payload = path.read_bytes()
        files.append(
            {
                "name": path.name,
                "sha256": sha256(payload).hexdigest(),
                "size_bytes": len(payload),
            }
        )
    manifest = {"version": BUNDLE_MANIFEST_VERSION, "files": files}
    manifest["bundle_sha256"] = sha256(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return manifest


def verify_artifact_bundle_manifest(
    manifest: Dict[str, Any], root: Path
) -> Tuple[str, ...]:
    reasons = []
    if manifest.get("version") != BUNDLE_MANIFEST_VERSION:
        reasons.append("BUNDLE_VERSION_INVALID")
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        reasons.append("BUNDLE_FILES_MISSING")
        return tuple(sorted(set(reasons)))
    names = [item.get("name") for item in files if isinstance(item, dict)]
    if len(names) != len(files) or len(names) != len(set(names)):
        reasons.append("BUNDLE_FILE_IDENTITIES_INVALID")
    for item in files:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            reasons.append("BUNDLE_FILE_IDENTITIES_INVALID")
            continue
        if Path(item["name"]).name != item["name"]:
            reasons.append("BUNDLE_FILE_PATH_INVALID")
            continue
        path = root / item["name"]
        if not path.is_file():
            reasons.append(f"BUNDLE_FILE_MISSING:{item['name']}")
            continue
        payload = path.read_bytes()
        if sha256(payload).hexdigest() != item.get("sha256"):
            reasons.append(f"BUNDLE_FILE_HASH_INVALID:{item['name']}")
        if len(payload) != item.get("size_bytes"):
            reasons.append(f"BUNDLE_FILE_SIZE_INVALID:{item['name']}")
    without_hash = {
        key: value for key, value in manifest.items() if key != "bundle_sha256"
    }
    expected = sha256(
        json.dumps(without_hash, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if manifest.get("bundle_sha256") != expected:
        reasons.append("BUNDLE_MANIFEST_HASH_INVALID")
    return tuple(sorted(set(reasons)))
