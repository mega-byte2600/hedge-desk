from hedge_desk.data.providers import (
    all_providers,
    missing_auth_env,
    provider,
    providers_for_asset_class,
    providers_for_capability,
)


def test_provider_ids_are_unique_and_nonempty():
    ids = [item.provider_id for item in all_providers()]
    assert all(ids)
    assert len(ids) == len(set(ids))


def test_authoritative_public_sources_cover_core_desk_domains():
    assert provider("sec-edgar").authority == "official"
    assert provider("nyfed-markets").authority == "official"
    assert provider("treasury-fiscaldata").authority == "official"
    assert provider("eia-open-data").authority == "official"
    assert provider("cftc-cot").authority == "official"
    assert provider("bis").authority == "official"
    for provider_id in ("imf", "oecd", "eurostat", "usgs", "nasa-eonet"):
        assert provider(provider_id).authority == "official"
        assert provider(provider_id).public_without_key is True
        assert missing_auth_env(provider_id, {}) is None

    assert provider("sec-edgar").public_without_key is True
    assert provider("nyfed-markets").public_without_key is True
    assert provider("treasury-fiscaldata").public_without_key is True
    assert provider("cftc-cot").public_without_key is True
    assert provider("bis").public_without_key is True
    assert provider("coinbase-exchange").public_without_key is True


def test_capability_and_asset_class_queries():
    option_ids = {item.provider_id for item in providers_for_asset_class("options")}
    assert {"cboe", "cme", "schwab", "polygon"}.issubset(option_ids)

    positioning_ids = {item.provider_id for item in providers_for_capability("positioning")}
    assert positioning_ids == {"cftc-cot"}

    sofr_ids = {item.provider_id for item in providers_for_capability("sofr")}
    assert sofr_ids == {"nyfed-markets"}

    liquidity_ids = {item.provider_id for item in providers_for_capability("global_liquidity")}
    assert liquidity_ids == {"bis"}

    short_ids = {item.provider_id for item in providers_for_capability("short_sale_volume")}
    assert short_ids == {"finra"}

    crypto_ids = {item.provider_id for item in providers_for_asset_class("crypto")}
    assert "coinbase-exchange" in crypto_ids


def test_auth_requirements_fail_closed_without_keys():
    assert missing_auth_env("polygon", {}) == "POLYGON_API_KEY"
    assert missing_auth_env("polygon", {"POLYGON_API_KEY": "x"}) is None
    assert missing_auth_env("eia-open-data", {}) == "EIA_API_KEY"
    assert missing_auth_env("finra", {}) == "FINRA_CLIENT_ID"
    assert missing_auth_env("sec-edgar", {}) is None
    assert missing_auth_env("fred", {}) is None
    assert missing_auth_env("bis", {}) is None
    assert missing_auth_env("coinbase-exchange", {}) is None


def test_unknown_provider_is_rejected():
    try:
        provider("not-a-provider")
    except KeyError as exc:
        assert "unknown provider" in str(exc)
    else:
        raise AssertionError("unknown provider should fail closed")


def test_provider_console_rows_surface_all_catalog_providers():
    from hedge_desk.data.providers import provider_console_rows

    rows = provider_console_rows()
    assert len(rows) == len(all_providers()) - 1  # fdic is catalog-only (public-claims gate)
    ids = {r["source_id"] for r in rows}
    assert "fdic" not in ids
    assert {"sec-edgar", "treasury-fiscaldata", "fred", "cftc-cot",
            "nws", "stooq", "alpha-vantage", "bis", "coinbase-exchange",
            "imf", "oecd", "eurostat", "usgs", "nasa-eonet"}.issubset(ids)
    for r in rows:
        # statuses must render under the console statusClass() palette
        assert r["status"] in ("PASS", "PENDING", "REVIEW_REQUIRED")
        assert "no fabricated values" in r["controls"]
    # key-gated vs keyless surfaces correctly
    by_id = {r["source_id"]: r for r in rows}
    assert by_id["sec-edgar"]["status"] == "PASS"
    assert by_id["sec-edgar"]["public_without_key"] is True
    assert by_id["bis"]["status"] == "PASS"
    for provider_id in ("imf", "oecd", "eurostat", "usgs", "nasa-eonet"):
        assert by_id[provider_id]["status"] == "PASS"
    assert by_id["coinbase-exchange"]["status"] == "PASS"
    assert by_id["alpha-vantage"]["status"] == "REVIEW_REQUIRED"


def test_provider_console_rows_never_claims_fabricated_pass():
    # a key-gated provider without a key must not show PASS
    from hedge_desk.data.providers import provider_console_rows

    rows = provider_console_rows()
    keyed = [r for r in rows if r["key_env"] and not r["public_without_key"]]
    assert keyed, "expected at least one key-gated provider"
    for r in keyed:
        assert r["status"] != "PASS"
