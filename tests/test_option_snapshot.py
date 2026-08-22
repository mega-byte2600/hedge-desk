from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from hedge_desk.options import parse_option_snapshot


def snapshot():
    return {
        "schema_version": "hedge-desk-option-snapshot-1.0.0",
        "underlying_quote": {
            "symbol": "TEST",
            "bid": "99.99",
            "ask": "100.01",
            "quoted_at": "2026-08-21T12:00:00Z",
        },
        "option_quotes": [
            {
                "contract_id": "TEST260918P00095000",
                "underlying": "TEST",
                "option_type": "put",
                "strike": "95",
                "expiration": "2026-09-18",
                "bid": "2.00",
                "ask": "2.10",
                "bid_size": 25,
                "ask_size": 30,
                "quoted_at": "2026-08-21T12:00:00Z",
                "open_interest": 1000,
                "volume": 500,
            }
        ],
    }


class OptionSnapshotTests(unittest.TestCase):
    def _parse(self, value):
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "snapshot.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            return parse_option_snapshot(path, "licensed-source")

    def test_canonical_snapshot_parses_exact_decimal_quotes(self) -> None:
        result = self._parse(snapshot())
        self.assertEqual(result.underlying_quote.symbol, "TEST")
        self.assertEqual(str(result.option_quotes[0].bid), "2.00")
        self.assertEqual(result.option_quotes[0].source_id, "licensed-source")

    def test_float_price_and_unknown_model_field_fail_closed(self) -> None:
        value = snapshot()
        value["option_quotes"][0]["bid"] = 2.0
        with self.assertRaisesRegex(ValueError, "decimal string"):
            self._parse(value)
        value = snapshot()
        value["option_quotes"][0]["agent_probability"] = "0.99"
        with self.assertRaisesRegex(ValueError, "fields unknown"):
            self._parse(value)

    def test_crossed_quotes_and_symbol_mismatch_fail_closed(self) -> None:
        crossed = snapshot()
        crossed["option_quotes"][0]["bid"] = "2.20"
        with self.assertRaisesRegex(ValueError, "crossed"):
            self._parse(crossed)
        mismatch = snapshot()
        mismatch["option_quotes"][0]["underlying"] = "OTHER"
        with self.assertRaisesRegex(ValueError, "symbols must match"):
            self._parse(mismatch)

    def test_duplicate_contracts_and_naive_time_fail_closed(self) -> None:
        duplicate = snapshot()
        duplicate["option_quotes"].append(deepcopy(duplicate["option_quotes"][0]))
        with self.assertRaisesRegex(ValueError, "identities must be unique"):
            self._parse(duplicate)
        naive = snapshot()
        naive["underlying_quote"]["quoted_at"] = "2026-08-21T12:00:00"
        with self.assertRaisesRegex(ValueError, "include a timezone"):
            self._parse(naive)


if __name__ == "__main__":
    unittest.main()
