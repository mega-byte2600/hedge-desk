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

    assert provider("sec-edgar").public_without_key is True
    assert provider("nyfed-markets").public_without_key is True
    assert provider("treasury-fiscaldata").public_without_key is True
    assert provider("cftc-cot").public_without_key is True


def test_capability_and_asset_class_queries():
    option_ids = {item.provider_id for item in providers_for_asset_class("options")}
    assert {"cboe", "cme", "schwab", "polygon"}.issubset(option_ids)

    positioning_ids = {item.provider_id for item in providers_for_capability("positioning")}
    assert positioning_ids == {"cftc-cot"}

    sofr_ids = {item.provider_id for item in providers_for_capability("sofr")}
    assert sofr_ids == {"nyfed-markets"}


def test_auth_requirements_fail_closed_without_keys():
    assert missing_auth_env("polygon", {}) == "POLYGON_API_KEY"
    assert missing_auth_env("polygon", {"POLYGON_API_KEY": "x"}) is None
    assert missing_auth_env("eia-open-data", {}) == "EIA_API_KEY"
    assert missing_auth_env("sec-edgar", {}) is None
    assert missing_auth_env("fred", {}) is None


def test_unknown_provider_is_rejected():
    try:
        provider("not-a-provider")
    except KeyError as exc:
        assert "unknown provider" in str(exc)
    else:
        raise AssertionError("unknown provider should fail closed")
