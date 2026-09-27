"""Deterministic tests for the Finnhub adapter (no network)."""

import json
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from hedge_desk import finnhub_desk
from hedge_desk.finnhub_desk import fetch_quotes, quote_summary

_CLI_OUT = json.dumps(
    {
        "AAPL": {
            "c": 341.07,
            "h": 341.67,
            "l": 334.53,
            "o": 336.04,
            "pc": 335.92,
            "t": 1790366400,
        },
        "BOGUS": {"error": "no quote (unknown symbol?)"},
    }
)


class FakeProc:
    returncode = 0
    stderr = ""

    def __init__(self, stdout):
        self.stdout = stdout


class FinnhubDeskTest(unittest.TestCase):
    def _patch_cli(self, stdout=_CLI_OUT):
        return patch.object(
            finnhub_desk, "_skill_cli_path", return_value=Path("/fake/cli.py")
        ), patch(
            "subprocess.run", return_value=FakeProc(stdout)
        )

    def test_fetch_parses_quote(self):
        p1, p2 = self._patch_cli()
        with p1, p2:
            quotes = fetch_quotes(["AAPL"])
        q = quotes["AAPL"]
        self.assertEqual(q.current, Decimal("341.07"))
        self.assertEqual(q.prev_close, Decimal("335.92"))
        self.assertEqual(q.change(), Decimal("341.07") - Decimal("335.92"))

    def test_error_symbol_omitted(self):
        p1, p2 = self._patch_cli()
        with p1, p2:
            quotes = fetch_quotes(["BOGUS"])
        self.assertNotIn("BOGUS", quotes)

    def test_cli_missing_raises(self):
        with patch.object(finnhub_desk, "_skill_cli_path", return_value=None):
            with self.assertRaises(ValueError):
                fetch_quotes(["AAPL"])

    def test_summary_marks_blocked_symbol(self):
        p1, p2 = self._patch_cli()
        with p1, p2:
            s = quote_summary(["AAPL", "BOGUS"])
        by_sym = {r["symbol"]: r for r in s["quotes"]}
        self.assertEqual(by_sym["AAPL"]["mode"], "REAL_FINNHUB_QUOTE")
        self.assertEqual(by_sym["BOGUS"]["mode"], "BLOCKED")

    def test_summary_blocked_when_cli_fails(self):
        with patch.object(finnhub_desk, "_skill_cli_path", return_value=None):
            s = quote_summary(["AAPL"])
        self.assertEqual(s["mode"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
