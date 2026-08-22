from pathlib import Path
import tempfile
import unittest

from hedge_desk.supply_chain import validate_github_action_pins


ROOT = Path(__file__).resolve().parents[1]


class CiSupplyChainTests(unittest.TestCase):
    def test_every_repository_action_is_pinned_to_a_full_sha(self) -> None:
        root = ROOT / ".github" / "workflows"
        workflows = tuple(sorted(tuple(root.glob("*.yml")) + tuple(root.glob("*.yaml"))))
        self.assertTrue(workflows)
        self.assertEqual(validate_github_action_pins(workflows), ())

    def test_mutable_or_missing_action_revisions_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mutable = root / "mutable.yml"
            mutable.write_text(
                "steps:\n  - uses: actions/checkout@v4\n  - uses: owner/action\n",
                encoding="utf-8",
            )
            reasons = validate_github_action_pins((mutable,))
        self.assertEqual(len(reasons), 2)
        self.assertTrue(any("ACTION_NOT_PINNED_TO_SHA" in item for item in reasons))
        self.assertTrue(any("ACTION_REFERENCE_MISSING_REVISION" in item for item in reasons))


if __name__ == "__main__":
    unittest.main()
