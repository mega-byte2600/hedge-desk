"""The disclosures surface: versioned, present, and scanned.

Disclosures are a domain unit rather than a footnote, so they are a versioned artifact on
the shipped surface. These tests keep them versioned, keep the language inside the claim
rules (the claim guard in tests/test_public_claims.py scans this file automatically), and
keep the renderer following the console's hardened enhancement conventions.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
REQUIRED_IDS = {
    "paper-only",
    "synthetic-fixtures",
    "not-advice",
    "risk-of-ruin-unvalidated",
    "no-performance-claim",
    "broker-read-only",
    "tier-boundaries",
    "not-an-offering",
    "no-registration-claimed",
    "reproducibility",
}


class DisclosuresPayloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads((WEB / "disclosures.json").read_text(encoding="utf-8"))

    def test_payload_is_versioned(self):
        self.assertEqual(self.payload["schema_version"], "emporion-disclosures-1")
        self.assertTrue(str(self.payload["disclosure_version"]).strip(), "disclosures need a version")
        self.assertTrue(str(self.payload["effective"]).strip(), "disclosures need an effective date")

    def test_every_required_disclosure_is_present(self):
        ids = {d["id"] for d in self.payload["disclosures"]}
        self.assertTrue(REQUIRED_IDS.issubset(ids), f"missing: {sorted(REQUIRED_IDS - ids)}")

    def test_ids_are_unique_and_text_is_present(self):
        seen = set()
        for d in self.payload["disclosures"]:
            self.assertNotIn(d["id"], seen, f"duplicate disclosure id {d['id']}")
            seen.add(d["id"])
            self.assertTrue(d["title"].strip(), d["id"])
            self.assertGreater(len(d["text"].strip()), 40, f"{d['id']} text is too thin to be a disclosure")

    def test_the_boundary_disclosures_are_specific(self):
        # The paper-only and no-offering statements are the ones a visitor relies on, so
        # their wording is pinned rather than left to drift.
        by_id = {d["id"]: d for d in self.payload["disclosures"]}
        self.assertIn("does not place orders", by_id["paper-only"]["text"])
        # Assert the meaning, not one phrasing: "Nothing produced here is investment
        # advice" and "not investment advice" both disclaim, and pinning one wording
        # would fail on a legitimate reword.
        self.assertRegex(by_id["not-advice"]["text"], r"(?i)(not|nothing)[^.]{0,60}investment advice")
        self.assertRegex(by_id["not-an-offering"]["text"], r"(?i)(not an offer|not an offer to sell)")
        self.assertIn("tamper-evident", by_id["reproducibility"]["text"])
        self.assertRegex(by_id["paper-only"]["text"], r"(?i)does not (place|route|execute)")


class DisclosuresWiringTests(unittest.TestCase):
    def test_index_html_loads_the_disclosures_module(self):
        html = (WEB / "index.html").read_text(encoding="utf-8")
        self.assertIn('src="./disclosures.js"', html)
        self.assertIn('type="module"', html.split('src="./disclosures.js"')[0][-40:])

    def test_renderer_follows_the_hardened_enhancement_conventions(self):
        src = (WEB / "disclosures.js").read_text(encoding="utf-8")
        self.assertIn("requestAnimationFrame", src, "observer work must be deferred")
        self.assertRegex(src, r"if \(document\.getElementById\(MOUNT_ID\)\) return;", "must be idempotent")
        # The check must be repeated after the await, or two renders can race.
        self.assertGreaterEqual(src.count("getElementById(MOUNT_ID)"), 2)

    def test_fetch_failure_does_not_fabricate_content(self):
        src = (WEB / "disclosures.js").read_text(encoding="utf-8")
        self.assertRegex(src, r"catch\s*\{[\s\S]{0,240}?\}", "a failed load must be handled, not invented")
        self.assertNotIn("lorem", src.lower())

    def test_escaping_is_applied_to_payload_text(self):
        src = (WEB / "disclosures.js").read_text(encoding="utf-8")
        self.assertIn("escapeText(", src)
        self.assertRegex(src, r"replace\(/\[&<>\"'\]/g")


if __name__ == "__main__":
    unittest.main()
