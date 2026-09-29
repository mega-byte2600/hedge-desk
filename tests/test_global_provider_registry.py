import unittest

from hedge_desk.data.providers import (
    missing_auth_env,
    provider,
    provider_console_rows,
    providers_for_asset_class,
    providers_for_capability,
)


class GlobalProviderRegistryTests(unittest.TestCase):
    def test_new_global_sources_are_registered_keyless_and_public(self):
        for provider_id in (
            "imf-datamapper",
            "oecd-cli",
            "eurostat",
            "usgs-earthquakes",
            "nasa-eonet",
        ):
            spec = provider(provider_id)
            self.assertEqual(spec.authority, "official")
            self.assertTrue(spec.public_without_key)
            self.assertIsNone(missing_auth_env(provider_id, {}))

    def test_new_capabilities_are_queryable(self):
        self.assertEqual(
            {item.provider_id for item in providers_for_capability("leading_indicator")},
            {"oecd-cli"},
        )
        self.assertIn(
            "eurostat",
            {item.provider_id for item in providers_for_capability("hicp")},
        )
        physical = {item.provider_id for item in providers_for_asset_class("physical_events")}
        self.assertTrue({"usgs-earthquakes", "nasa-eonet"}.issubset(physical))

    def test_console_surfaces_new_sources_without_credentials(self):
        rows = {row["source_id"]: row for row in provider_console_rows()}
        for provider_id in (
            "imf-datamapper",
            "oecd-cli",
            "eurostat",
            "usgs-earthquakes",
            "nasa-eonet",
        ):
            self.assertIn(provider_id, rows)
            self.assertEqual(rows[provider_id]["status"], "PASS")
            self.assertTrue(rows[provider_id]["public_without_key"])
            self.assertIn("no fabricated values", rows[provider_id]["controls"])


if __name__ == "__main__":
    unittest.main()
