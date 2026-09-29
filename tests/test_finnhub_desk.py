"""Deterministic tests for the Finnhub adapter (no network)."""

import json
import os
import unittest
from decimal import Decimal
from pathlib import Path
from urllib.parse import parse_qs, urlparse
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
        ), patch("subprocess.run", return_value=FakeProc(stdout))

    def test_fetch_parses_quote_from_cli_fallback(self):
        p1, p2 = self._patch_cli()
        with patch.dict(os.environ, {}, clear=True), p1, p2:
            quotes = fetch_quotes(["AAPL"])
        q = quotes["AAPL"]
        self.assertEqual(q.current, Decimal("341.07"))
        self.assertEqual(q.prev_close, Decimal("335.92"))
        self.assertEqual(q.change(), Decimal("341.07") - Decimal("335.92"))

    def test_error_symbol_omitted_from_cli_fallback(self):
        p1, p2 = self._patch_cli()
        with patch.dict(os.environ, {}, clear=True), p1, p2:
            quotes = fetch_quotes(["BOGUS"])
        self.assertNotIn("BOGUS", quotes)

    def test_env_key_uses_http_header_not_query_string(self):
        seen = []
        raw = json.dumps(
            {"c": 341.07, "h": 341.67, "l": 334.53, "o": 336.04, "pc": 335.92, "t": 1790366400}
        ).encode("utf-8")

        def transport(request):
            seen.append(request)
            return 200, raw

        with patch.dict(os.environ, {"FINNHUB_API_KEY": "secret-key"}, clear=True):
            quotes = fetch_quotes(["AAPL"], transport=transport)
        self.assertEqual(quotes["AAPL"].current, Decimal("341.07"))
        self.assertEqual(len(seen), 1)
        request = seen[0]
        parsed = urlparse(request.full_url)
        self.assertEqual(parsed.hostname, "finnhub.io")
        self.assertEqual(parsed.path, "/api/v1/quote")
        self.assertEqual(parse_qs(parsed.query)["symbol"], ["AAPL"])
        self.assertNotIn("secret-key", request.full_url)
        self.assertEqual(request.get_header("X-finnhub-token"), "secret-key")

    def test_http_rate_limit_fails_closed_without_leaking_key(self):
        def transport(request):
            return 429, b"limit"

        with patch.dict(os.environ, {"FINNHUB_API_KEY": "secret-key"}, clear=True):
            with self.assertRaisesRegex(ValueError, "rate limit") as ctx:
                fetch_quotes(["AAPL"], transport=transport)
        self.assertNotIn("secret-key", str(ctx.exception))

    def test_cli_missing_raises_when_env_key_absent(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(
            finnhub_desk, "_skill_cli_path", return_value=None
        ):
            with self.assertRaises(ValueError):
                fetch_quotes(["AAPL"])

    def test_summary_marks_blocked_symbol(self):
        p1, p2 = self._patch_cli()
        with patch.dict(os.environ, {}, clear=True), p1, p2:
            summary = quote_summary(["AAPL", "BOGUS"])
        by_sym = {row["symbol"]: row for row in summary["quotes"]}
        self.assertEqual(by_sym["AAPL"]["mode"], "REAL_FINNHUB_QUOTE")
        self.assertEqual(by_sym["BOGUS"]["mode"], "BLOCKED")

    def test_summary_blocked_when_no_transport_is_configured(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(
            finnhub_desk, "_skill_cli_path", return_value=None
        ):
            summary = quote_summary(["AAPL"])
        self.assertEqual(summary["mode"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
