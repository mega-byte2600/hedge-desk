import json
from pathlib import Path
import tempfile
import unittest

from hedge_desk.option_universe_intake import validate_local_option_universe


EXAMPLE = Path(__file__).parents[1] / "examples" / "option-universe.synthetic.json"


class OptionUniverseIntakeTests(unittest.TestCase):
    def test_checked_example_ranks_without_copying_raw_payload(self) -> None:
        result = validate_local_option_universe(EXAMPLE)
        self.assertEqual(result.source_count, 1)
        self.assertEqual(result.symbols, ("TEST",))
        self.assertEqual(result.evaluation.candidates[0].symbol, "TEST")
        self.assertFalse(result.evaluation.trade_authorized)
        self.assertFalse(result.raw_payloads_copied)

    def test_unknown_fields_or_noninteger_timing_fail_strictly(self) -> None:
        payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        payload["maximum_age_seconds"] = "0"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "timing policies"):
                validate_local_option_universe(path)
        payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        payload["extra"] = True
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "schema invalid"):
                validate_local_option_universe(path)

    def test_nonstring_or_empty_snapshot_paths_fail_with_stable_reason(self) -> None:
        for envelope, payload_path in ((None, "quotes.json"), ("", "quotes.json"),
                                       ("envelope.json", 7), ("envelope.json", "")):
            payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))
            payload["snapshots"] = [{"envelope": envelope, "payload": payload_path}]
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "manifest.json"
                path.write_text(json.dumps(payload), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "snapshot paths invalid"):
                    validate_local_option_universe(path)

    def test_missing_snapshot_files_fail_with_stable_reason(self) -> None:
        payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        payload["market_session_evidence"] = str(
            EXAMPLE.parent / "market-session.synthetic.json"
        )
        payload["snapshots"] = [
            {"envelope": "missing-envelope.json", "payload": "missing-quotes.json"}
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "snapshot unreadable"):
                validate_local_option_universe(path)


if __name__ == "__main__":
    unittest.main()
