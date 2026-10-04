"""Deterministic tests for the Yahoo hardened transport + options failover.

No network: every test injects a scripted fixture transport.
Run: python3 test_yahoo_failover.py  (or via unittest discovery)
"""

from __future__ import annotations

import json
import sys
import os
import unittest

# repo layout: imports are absolute

from hedge_desk.data.yahoo_transport import YahooBlocked, YahooSession
from hedge_desk.data.options_failover import (
    ChainResult,
    fetch_nasdaq_options,
    fetch_options_chain,
    parse_yahoo_options,
)

CRUMB_A = "crumbAAAA111"
CRUMB_B = "crumbBBBB222"

YAHOO_CHAIN = {
    "optionChain": {
        "result": [{
            "quote": {"regularMarketPrice": 500.0},
            "options": [{
                "expirationDate": 1792000000,
                "calls": [{
                    "strike": 500.0, "bid": 5.0, "ask": 5.4,
                    "volume": 1200, "openInterest": 3400,
                    "impliedVolatility": 0.21,
                }],
                "puts": [{
                    "strike": 490.0, "bid": 4.1, "ask": 4.5,
                    "volume": 800, "openInterest": 2100,
                    "impliedVolatility": 0.23,
                }],
            }],
        }],
        "error": None,
    }
}

CBOE_BODY = json.dumps({
    "data": {"current_price": 500.0, "options": [{"option": "SPY261016C00500000"}]}
}).encode()


class ScriptedTransport:
    """Fixture transport: scripted (status, body) per URL substring, in order."""

    def __init__(self, script):
        # script: list of (url_substring, status, body)
        self.script = list(script)
        self.calls = []

    def __call__(self, url, headers):
        self.calls.append(url)
        for i, (sub, status, body) in enumerate(self.script):
            if sub in url:
                del self.script[i]
                return status, body
        raise AssertionError(f"no scripted response for {url[:80]}")

    def count(self, sub):
        return sum(1 for u in self.calls if sub in u)


def noop_sleep(_):
    pass


class CrumbTests(unittest.TestCase):
    def test_crumb_cached_across_calls(self):
        t = ScriptedTransport([
            ("getcrumb", 200, CRUMB_A.encode()),
            ("v7/finance/options", 200, json.dumps(YAHOO_CHAIN).encode()),
            ("v7/finance/options", 200, json.dumps(YAHOO_CHAIN).encode()),
        ])
        s = YahooSession(transport=t, sleeper=noop_sleep)
        s.get("https://query2.finance.yahoo.com/v7/finance/options/SPY")
        s.get("https://query2.finance.yahoo.com/v7/finance/options/QQQ")
        self.assertEqual(t.count("getcrumb"), 1)  # crumb reused, not refetched

    def test_401_refreshes_crumb_once_then_recovers(self):
        t = ScriptedTransport([
            ("getcrumb", 200, CRUMB_A.encode()),
            ("v7/finance/options", 401, b""),
            ("getcrumb", 200, CRUMB_B.encode()),
            ("v7/finance/options", 200, json.dumps(YAHOO_CHAIN).encode()),  # crumb B works
        ])
        s = YahooSession(transport=t, sleeper=noop_sleep)
        body = s.get("https://query2.finance.yahoo.com/v7/finance/options/SPY")
        self.assertIn(b"optionChain", body)
        events = [e["event"] for e in s.attempts_log]
        self.assertIn("stale_crumb_401", events)

    def test_persistent_401_after_refresh_raises_blocked(self):
        t = ScriptedTransport([
            ("getcrumb", 200, CRUMB_A.encode()),
            ("v7/finance/options", 401, b""),
            ("getcrumb", 200, CRUMB_B.encode()),
            ("v7/finance/options", 401, b""),
            ("v7/finance/options", 401, b""),
        ])
        s = YahooSession(transport=t, sleeper=noop_sleep)
        with self.assertRaises(YahooBlocked):
            s.get("https://query2.finance.yahoo.com/v7/finance/options/SPY")

    def test_crumb_endpoint_401_fails_over_without_hammering(self):
        t = ScriptedTransport([("getcrumb", 401, b"")])
        s = YahooSession(transport=t, sleeper=noop_sleep)
        with self.assertRaises(YahooBlocked):
            s.get("https://query2.finance.yahoo.com/v7/finance/options/SPY")
        self.assertEqual(t.count("getcrumb"), 1)  # exactly one attempt

    def test_transport_error_backs_off_then_succeeds(self):
        sleeps = []
        t = ScriptedTransport([
            ("getcrumb", 200, CRUMB_A.encode()),
            ("v7/finance/options", 0, b""),
            ("v7/finance/options", 0, b""),
            ("v7/finance/options", 200, json.dumps(YAHOO_CHAIN).encode()),
        ])
        s = YahooSession(transport=t, sleeper=sleeps.append)
        body = s.get("https://query2.finance.yahoo.com/v7/finance/options/SPY")
        self.assertIn(b"optionChain", body)
        backoff_waits = [w for w in sleeps if w in (1.0, 2.0, 4.0)]
        self.assertEqual(len(backoff_waits), 2)  # two retries, exponential


class FailoverTests(unittest.TestCase):
    def test_yahoo_healthy_serves_first(self):
        t = ScriptedTransport([
            ("getcrumb", 200, CRUMB_A.encode()),
            ("v7/finance/options", 200, json.dumps(YAHOO_CHAIN).encode()),
        ])
        res = fetch_options_chain("SPY", transport=t, sleeper=noop_sleep)
        self.assertTrue(res.ok)
        self.assertEqual(res.source_id, "yahoo")

    def test_yahoo_401_falls_through_to_cboe(self):
        # Yahoo mitigated (crumb 401), Nasdaq shape-rejects, CBOE serves.
        t = ScriptedTransport([
            ("getcrumb", 401, b""),
            ("nasdaq.com", 200, json.dumps({"status": {"rCode": 400}}).encode()),
            ("cboe.com", 200, CBOE_BODY),
        ])
        res = fetch_options_chain("SPY", transport=t, sleeper=noop_sleep)
        self.assertTrue(res.ok)
        self.assertEqual(res.source_id, "cboe")
        srcs = [a["source"] for a in res.attempts if a["ok"] == "no"]
        self.assertEqual(srcs, ["yahoo", "nasdaq"])  # order = standing order

    def test_yahoo_malformed_payload_fails_over(self):
        t = ScriptedTransport([
            ("getcrumb", 200, CRUMB_A.encode()),
            ("v7/finance/options", 200, b'{"optionChain": {"result": []}}'),
            ("nasdaq.com", 200, json.dumps({"status": {"rCode": 400}}).encode()),
            ("cboe.com", 200, CBOE_BODY),
        ])
        res = fetch_options_chain("SPY", transport=t, sleeper=noop_sleep)
        self.assertTrue(res.ok)
        self.assertEqual(res.source_id, "cboe")

    def test_all_sources_down_returns_data_unavailable(self):
        t = ScriptedTransport([
            ("getcrumb", 401, b""),
            ("nasdaq.com", 404, b""),
            ("cboe.com", 500, b""),
        ])
        res = fetch_options_chain("SPY", transport=t, sleeper=noop_sleep)
        self.assertFalse(res.ok)
        self.assertEqual(res.payload, b"")
        self.assertTrue(res.data_unavailable.startswith("data unavailable:"))
        self.assertIn("yahoo", res.reason)
        self.assertIn("nasdaq", res.reason)
        self.assertIn("cboe", res.reason)
        # never synthetic: no payload, explicit reasons only
        self.assertNotIn("synthetic", res.reason.lower())

    def test_nasdaq_shape_mismatch_is_fail_closed(self):
        t = ScriptedTransport([
            ("nasdaq.com", 200, b'{"data": {"table": {"rows": []}}}'),
        ])
        with self.assertRaises(YahooBlocked):
            fetch_nasdaq_options(t, "SPY")

    def test_parse_yahoo_options_extracts_contracts(self):
        contracts = parse_yahoo_options(json.dumps(YAHOO_CHAIN).encode())
        self.assertEqual(len(contracts), 2)
        call = [c for c in contracts if c["type"] == "call"][0]
        self.assertEqual(call["strike"], 500.0)
        self.assertEqual(call["impliedVolatility"], 0.21)

    def test_parse_yahoo_options_rejects_malformed(self):
        with self.assertRaises(ValueError):
            parse_yahoo_options(b'{"optionChain": {}}')
        with self.assertRaises(ValueError):
            parse_yahoo_options(b'not json')


def main():
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
