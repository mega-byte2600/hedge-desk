import json
from pathlib import Path
import tempfile
import unittest

from hedge_desk.artifacts import build_artifact_bundle_manifest


class ArtifactBundleTests(unittest.TestCase):
    def test_bundle_is_order_independent_and_content_sensitive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            one = root / "one.json"
            two = root / "two.md"
            one.write_text(json.dumps({"a": 1}), encoding="utf-8")
            two.write_text("paper\n", encoding="utf-8")
            forward = build_artifact_bundle_manifest((one, two))
            reverse = build_artifact_bundle_manifest((two, one))
            self.assertEqual(forward, reverse)
            self.assertEqual(len(forward["bundle_sha256"]), 64)
            two.write_text("changed\n", encoding="utf-8")
            changed = build_artifact_bundle_manifest((one, two))
            self.assertNotEqual(forward["bundle_sha256"], changed["bundle_sha256"])

    def test_missing_or_duplicate_artifact_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "one.json"
            path.write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                build_artifact_bundle_manifest((path, path))
            with self.assertRaises(ValueError):
                build_artifact_bundle_manifest((Path(directory) / "missing",))


if __name__ == "__main__":
    unittest.main()
