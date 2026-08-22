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
