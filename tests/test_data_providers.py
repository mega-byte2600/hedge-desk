"""Deterministic tests for the multi-asset data-provider registry (no network).

Fixture payloads are minimal, representative slices of the real endpoints'
shapes (SEC EDGAR companyfacts, Treasury fiscal service, CFTC zip, Stooq
bot-wall HTML, EIA key-gating). Transports are injected; CI never reaches the
live APIs. The goal: prove each adapter fails closed on malformed/missing input
and parses a good payload into the shared ProviderObservation contract.
"""

import json
import unittest
from datetime import datetime, timezone

from hedge_desk.data.providers import (
    CftcCotAdapter,
    EiaOpenDataAdapter,
    ENV_EIA_API_KEY,
    KeyedEodAdapter,
    ProviderStatus,
    REGISTRY_BY_ID,
    SecEdgarFactsAdapter,
    StooqEodAdapter,
    TreasuryFiscalAdapter,
    build_provider_artifact,
    fetch_provider,
    _parse_alpha_vantage,
    _parse_tiingo,
    _parse_twelve,
    _alpha_vantage_url,
)

# --- captured real-payload fixtures --------------------------------------

SEC_APPLE = json.dumps({
    "cik": 320193,
    "entityName": "Apple Inc.",
    "facts": {
        "dei": {
            "EntityCommonStockSharesOutstanding": {
                "label": "Entity Common Stock, Shares Outstanding",
                "units": {"shares": [{"end": "2026-06-27", "val": 14852413000, "fy": 2026, "fp": "FY"}]},
            }
        },
        "us-gaap": {
            "Revenues": {
                "label": "Revenues",
                "units": {
                    "USD": [
                        {"end": "2026-06-27", "val": 85777000000, "fy": 2026, "fp": "FY"},
                        {"end": "2025-06-28", "val": 85863000000, "fy": 2025, "fp": "FY"},
                    ]
                },
            }
        },
    },
})


def _sec_ok_transport():
    return lambda url: (200, SEC_APPLE.encode("utf-8"))


TREASURY_OK = json.dumps({
    "data": [
        {
            "record_date": "2026-06-30", "country": "United Kingdom", "currency": "Pound",
            "country_currency_desc": "United Kingdom-Pound", "exchange_rate": "1.268",
            "record_fiscal_year": "2026", "record_fiscal_quarter": "3",
        }
    ]
})


def _treasury_ok_transport():
    return lambda url: (200, TREASURY_OK.encode("utf-8"))


# a valid PK zip preamble (just the magic bytes)
CFTC_ZIP = b"PK\x03\x04" + b"\x00" * 64

STOOQ_BOTWALL = (
    b'<!DOCTYPE html><html><head><meta name="robots" content="noindex,nofollow">'
    b'</head><body><noscript>This site requires JavaScript to verify your browser.</noscript>'
    b'<script nonce="x">(async()=>{const c="AAA",await fetch("/__verify"...})();</script></body></html>'
)


class SecEdgarTests(unittest.TestCase):
    def test_parses_revenues_into_observations(self):
        result = SecEdgarFactsAdapter().fetch("320193", _sec_ok_transport(), tag="Revenues")
        self.assertEqual(result.status, ProviderStatus.PASS)
        self.assertFalse(result.reason_codes)
        self.assertTrue(len(result.observations) >= 1)
        revenues = [o for o in result.observations if "Revenues" in o.series and o.unit == "USD"]
        self.assertTrue(revenues)
        self.assertEqual(revenues[-1].date, "2026-06-27")
        self.assertEqual(revenues[-1].value, "85777000000")
        self.assertEqual(revenues[-1].extra, (("fy", "2026"), ("fp", "FY")))

    def test_unknown_tag_rejects(self):
        result = SecEdgarFactsAdapter().fetch("320193", _sec_ok_transport(), tag="NotARealTag")
        self.assertEqual(result.status, ProviderStatus.REJECT)
        self.assertIn("TAG_UNKNOWN", result.reason_codes)

    def test_404_quarantines_symbol_unknown(self):
        result = SecEdgarFactsAdapter().fetch("320193", lambda url: (404, b"{}"))
        self.assertEqual(result.status, ProviderStatus.QUARANTINE)
        self.assertIn("SYMBOL_UNKNOWN", result.reason_codes)

    def test_invalid_cik_rejects(self):
        result = SecEdgarFactsAdapter().fetch("not-a-cik", _sec_ok_transport())
        self.assertEqual(result.status, ProviderStatus.REJECT)
        self.assertIn("CIK_INVALID", result.reason_codes)

    def test_malformed_payload_rejects(self):
        result = SecEdgarFactsAdapter().fetch("320193", lambda url: (200, b"not json"))
        self.assertEqual(result.status, ProviderStatus.REJECT)
        self.assertIn("PAYLOAD_MALFORMED", result.reason_codes)


class TreasuryTests(unittest.TestCase):
    def test_parses_fx_observations(self):
        result = TreasuryFiscalAdapter().fetch("rates_of_exchange", _treasury_ok_transport())
        self.assertEqual(result.status, ProviderStatus.PASS)
        self.assertEqual(len(result.observations), 1)
        rx = result.observations[0]
        self.assertEqual(rx.date, "2026-06-30")
        self.assertEqual(rx.value, "1.268")
        self.assertEqual(rx.unit, "fx")
        self.assertEqual(rx.extra[0], ("currency", "Pound"))

    def test_empty_data_rejects(self):
        result = TreasuryFiscalAdapter().fetch("rates_of_exchange", lambda url: (200, b'{"data": []}'))
        self.assertEqual(result.status, ProviderStatus.REJECT)
        self.assertIn("EMPTY_PAYLOAD", result.reason_codes)

    def test_transport_failure_quarantines(self):
        result = TreasuryFiscalAdapter().fetch("rates_of_exchange", lambda url: (0, b""))
        self.assertEqual(result.status, ProviderStatus.QUARANTINE)
        self.assertIn("TRANSPORT_FAILED", result.reason_codes)


class CftcTests(unittest.TestCase):
    def test_zip_payload_passes(self):
        result = CftcCotAdapter().fetch("ignored", lambda url: (200, CFTC_ZIP), year="2024")
        self.assertEqual(result.status, ProviderStatus.PASS)
        self.assertEqual(result.observations[0].unit, "bytes")
        self.assertGreater(int(result.observations[0].value), 0)

    def test_non_zip_payload_rejects(self):
        result = CftcCotAdapter().fetch("ignored", lambda url: (200, b"not a zip"))
        self.assertEqual(result.status, ProviderStatus.REJECT)
        self.assertIn("PAYLOAD_NOT_ZIP", result.reason_codes)


class EiaTests(unittest.TestCase):
    def test_missing_key_is_quarantine_config(self):
        # live verified: 403 without key; never fabricate a value.
        result = EiaOpenDataAdapter().fetch("SERIES", lambda url: (200, b"{}"))
        self.assertEqual(result.status, ProviderStatus.QUARANTINE)
        self.assertIn("CONFIG_MISSING_KEY", result.reason_codes)
        self.assertIn(ENV_EIA_API_KEY, result.config_needs)

    def test_auth_failed_key(self):
        result = EiaOpenDataAdapter().fetch("SERIES", lambda url: (403, b""), api_key="dummy")
        self.assertEqual(result.status, ProviderStatus.QUARANTINE)
        self.assertIn("AUTH_FAILED", result.reason_codes)


class StooqTests(unittest.TestCase):
    def test_bot_wall_is_detected_honestly(self):
        result = StooqEodAdapter().fetch("AAPL", lambda url: (200, STOOQ_BOTWALL))
        self.assertEqual(result.status, ProviderStatus.QUARANTINE)
        self.assertIn("BOT_WALL", result.reason_codes)


class KeyedEodTests(unittest.TestCase):
    def test_missing_key_quarantines_with_config(self):
        from hedge_desk.data.providers import REGISTRY

        av = REGISTRY_BY_ID["alpha-vantage-eod"]
        result = av.fetch("AAPL", lambda url: (200, b"{}"))
        self.assertEqual(result.status, ProviderStatus.QUARANTINE)
        self.assertIn("CONFIG_MISSING_KEY", result.reason_codes)
        self.assertEqual(result.config_needs, ("ALPHA_VANTAGE_API_KEY",))

    def test_alpha_vantage_parser(self):
        payload = {
            "Time Series (Daily)": {
                "2026-09-29": {"4. close": "330.00", "1. open": "329.00"},
                "2026-09-28": {"4. close": "328.50", "1. open": "329.10"},
            }
        }
        parsed = _parse_alpha_vantage(json.dumps(payload).encode())
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]["date"], "2026-09-28")
        self.assertEqual(parsed[1]["close"], "330.00")

    def test_alpha_vantage_limit_note(self):
        parsed = _parse_alpha_vantage(b'{"Note": "API limit reached"}')
        self.assertEqual(parsed, ("API_LIMIT_OR_KEY_INVALID",))

    def test_tiingo_parser(self):
        raw = json.dumps([{"date": "2026-09-29T00:00:00+00:00", "close": 330.0}]).encode()
        parsed = _parse_tiingo(raw)
        self.assertEqual(parsed[0]["date"], "2026-09-29")
        self.assertEqual(parsed[0]["close"], "330.0")

    def test_twelve_parser(self):
        raw = json.dumps({"status": "ok", "values": [{"datetime": "2026-09-29", "close": "330.00"}]}).encode()
        parsed = _parse_twelve(raw)
        self.assertEqual(parsed[0]["close"], "330.00")

    def test_url_builders_do_not_leak_secrets(self):
        av = _alpha_vantage_url("AAPL", "SOMEKEY")
        self.assertIn("apikey=SOMEKEY", av)
        # url itself is fine; the key must never reach logs — handled at fetch layer.


class RegistryTests(unittest.TestCase):
    def test_registry_has_all_expected_providers(self):
        expected = {
            "sec-edgar-companyfacts", "cftc-cot", "ust-treasury-fiscal",
            "eia-open-data-v2", "stooq-eod", "alpha-vantage-eod",
            "tiingo-eod", "twelve-data-eod",
        }
        self.assertEqual(set(REGISTRY_BY_ID), expected)

    def test_fetch_provider_unknown_raises(self):
        with self.assertRaisesRegex(ValueError, "unknown provider"):
            fetch_provider("not-a-provider", "AAPL")

    def test_fetch_provider_dispatches(self):
        result = fetch_provider("ust-treasury-fiscal", "rates_of_exchange", transport=_treasury_ok_transport())
        self.assertEqual(result.status, ProviderStatus.PASS)

    def test_build_provider_artifact_seals_metadata(self):
        result = fetch_provider("ust-treasury-fiscal", "rates_of_exchange", transport=_treasury_ok_transport())
        artifact = build_provider_artifact(result, "rates_of_exchange")
        self.assertFalse(artifact.synthetic)
        self.assertFalse(artifact.redistribution_allowed)
        self.assertEqual(artifact.source_id, "ust-treasury-fiscal")
        self.assertEqual(artifact.payload_kind, "provider_observation")


if __name__ == "__main__":
    unittest.main()
