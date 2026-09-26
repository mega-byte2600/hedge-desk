"""Tests for the Muse research-findings intake validator."""

import unittest

from scripts.validate_muse_findings import validate_findings


def _valid_finding(**overrides):
    finding = {
        "id": "aal-earnings-timing",
        "kind": "risk_flag",
        "symbol": "AAL",
        "title": "AAL earnings falls inside the 33-DTE put window",
        "summary": "AAL next earnings is expected ~2026-10-16, inside the 33-DTE window of the 11.5 put. A gap through the strike turns the credit into a loss on collateral.",
        "sources": ["https://www.example.com/aal-earnings-date"],
        "catalysts": ["earnings 2026-10-16"],
        "risk_flags": ["gap risk through 11.5"],
        "invalidation_threshold": "AAL confirms earnings after the put expires.",
    }
    finding.update(overrides)
    return finding


def _valid_payload(findings=None, **overrides):
    payload = {
        "schema_version": "muse-findings-1.0.0",
        "author": "muse",
        "session": "2026-09-25 (close)",
        "generated_at": "2026-09-25T20:00:00Z",
        "findings": [_valid_finding()] if findings is None else findings,
    }
    payload.update(overrides)
    return payload


class MuseFindingsValidationTests(unittest.TestCase):
    def test_valid_payload_passes(self):
        verdict = validate_findings(_valid_payload())
        self.assertEqual(verdict["status"], "VALID")
        self.assertEqual(verdict["finding_count"], 1)
        self.assertEqual(verdict["symbols"], ["AAL"])

    def test_wrong_author_rejected(self):
        with self.assertRaises(ValueError):
            validate_findings(_valid_payload(author="not-muse"))

    def test_wrong_schema_version_rejected(self):
        with self.assertRaises(ValueError):
            validate_findings(_valid_payload(schema_version="muse-findings-0.9"))

    def test_empty_findings_rejected(self):
        with self.assertRaises(ValueError):
            validate_findings(_valid_payload(findings=[]))

    def test_unsourced_finding_rejected(self):
        with self.assertRaises(ValueError):
            validate_findings(_valid_payload(findings=[_valid_finding(sources=[])]))

    def test_http_source_rejected(self):
        with self.assertRaises(ValueError):
            validate_findings(_valid_payload(findings=[_valid_finding(sources=["http://x.com"])]))

    def test_forbidden_probability_claim_rejected(self):
        with self.assertRaises(ValueError):
            validate_findings(_valid_payload(findings=[_valid_finding(
                summary="There is a 90% probability the put expires worthless.")]))

    def test_secret_leak_rejected(self):
        with self.assertRaises(ValueError):
            validate_findings(_valid_payload(findings=[_valid_finding(
                summary="Use api_key=abc123 to connect.")]))

    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):
            validate_findings(_valid_payload(findings=[
                _valid_finding(), _valid_finding()]))

    def test_bad_symbol_rejected(self):
        with self.assertRaises(ValueError):
            validate_findings(_valid_payload(findings=[_valid_finding(symbol="aa1")]))

    def test_market_and_product_symbols_allowed(self):
        for sym in ("MARKET", "PRODUCT"):
            verdict = validate_findings(_valid_payload(findings=[_valid_finding(symbol=sym)]))
            self.assertEqual(verdict["status"], "VALID")


if __name__ == "__main__":
    unittest.main()
