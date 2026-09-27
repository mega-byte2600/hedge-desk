import json

import pytest

from hedge_desk.data.open_market_feeds import (
    cftc_cot,
    eia_v2,
    finra_fixed_income,
    sec_companyfacts,
    sec_submissions,
    treasury_latest_auctions,
)


def _transport(payload, status=200, seen=None):
    raw = json.dumps(payload).encode("utf-8")

    def fetch(url):
        if seen is not None:
            seen.append(url)
        return status, raw

    return fetch


def test_treasury_auctions_uses_official_endpoint_and_rows():
    seen = []
    result = treasury_latest_auctions(
        limit=2,
        transport=_transport(
            {"data": [{"cusip": "912TEST01"}, {"cusip": "912TEST02"}]},
            seen=seen,
        ),
    )
    assert result.provider_id == "treasury-fiscaldata"
    assert result.row_count == 2
    assert "api.fiscaldata.treasury.gov" in seen[0]
    assert "auctions_query" in seen[0]
    assert "page%5Bsize%5D=2" in seen[0]


def test_finra_public_fixed_income_dataset_is_allowlisted():
    seen = []
    result = finra_fixed_income(
        "corporateMarketBreadth",
        limit=5,
        transport=_transport([{"advances": 100, "declines": 80}], seen=seen),
    )
    assert result.provider_id == "finra"
    assert result.dataset == "corporateMarketBreadth"
    assert result.row_count == 1
    assert "api.finra.org/data/group/fixedIncomeMarket/name/corporateMarketBreadth" in seen[0]
    with pytest.raises(ValueError, match="unsupported FINRA"):
        finra_fixed_income("arbitraryDataset", transport=_transport([]))


def test_cftc_tff_uses_official_public_reporting_api():
    seen = []
    result = cftc_cot(
        "tff_futures_only",
        limit=3,
        transport=_transport([{"market_and_exchange_names": "TEST"}], seen=seen),
    )
    assert result.provider_id == "cftc-cot"
    assert result.row_count == 1
    assert "publicreporting.cftc.gov/resource/gpe5-46if.json" in seen[0]
    assert "%24limit=3" in seen[0]


def test_eia_requires_key_and_does_not_return_it_in_result(monkeypatch):
    monkeypatch.delenv("EIA_API_KEY", raising=False)
    with pytest.raises(ValueError, match="EIA_API_KEY"):
        eia_v2("petroleum/stoc/wstk", transport=_transport({}))

    seen = []
    result = eia_v2(
        "petroleum/stoc/wstk",
        data=("value",),
        limit=4,
        api_key="secret-test-key",
        transport=_transport({"response": {"data": [{"value": "1"}]}}, seen=seen),
    )
    assert result.provider_id == "eia-open-data"
    assert result.dataset == "petroleum/stoc/wstk"
    assert "secret-test-key" not in repr(result)
    assert "api_key=secret-test-key" in seen[0]


def test_sec_submissions_normalizes_cik():
    seen = []
    payload = {"cik": "320193", "name": "Example"}
    result = sec_submissions(320193, transport=_transport(payload, seen=seen))
    assert result["cik"] == "320193"
    assert seen[0].endswith("CIK0000320193.json")


def test_sec_companyfacts_requires_facts():
    seen = []
    result = sec_companyfacts(
        "0000320193",
        transport=_transport({"facts": {"us-gaap": {}}}, seen=seen),
    )
    assert "facts" in result
    assert "/api/xbrl/companyfacts/CIK0000320193.json" in seen[0]
    with pytest.raises(ValueError, match="malformed"):
        sec_companyfacts(320193, transport=_transport({"entityName": "Example"}))


def test_open_feed_adapters_fail_closed_on_bad_http_and_json():
    with pytest.raises(ValueError, match="status 503"):
        treasury_latest_auctions(transport=lambda _url: (503, b"down"))
    with pytest.raises(ValueError, match="malformed JSON"):
        cftc_cot(transport=lambda _url: (200, b"not-json"))


def test_limits_and_routes_are_validated_before_network():
    with pytest.raises(ValueError, match="limit"):
        treasury_latest_auctions(limit=0, transport=_transport({"data": []}))
    with pytest.raises(ValueError, match="invalid EIA route"):
        eia_v2("../secret", api_key="x", transport=_transport({}))
