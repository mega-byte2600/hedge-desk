"""Deterministic tests for the account-equity input (no network, no secrets)."""

import os
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from hedge_desk.account import read_account_equity


class AccountEquityTests(unittest.TestCase):
    def test_reads_from_env(self):
        self.assertEqual(read_account_equity(env="25000"), Decimal("25000"))

    def test_reads_from_file_when_env_empty(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "equity.txt"
            p.write_text("50000\n")
            self.assertEqual(read_account_equity(env="", path=p), Decimal("50000"))

    def test_missing_returns_none(self):
        self.assertIsNone(read_account_equity(env=""))
        self.assertIsNone(read_account_equity(env="   "))

    def test_non_numeric_returns_none(self):
        self.assertIsNone(read_account_equity(env="not-a-number"))

    def test_non_positive_returns_none(self):
        self.assertIsNone(read_account_equity(env="0"))
        self.assertIsNone(read_account_equity(env="-100"))


if __name__ == "__main__":
    unittest.main()