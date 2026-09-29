import json

import pytest

from hedge_desk.data.institutional_feeds import (
    BIS_GLOBAL_LIQUIDITY_SERIES,
    FINRA_EQUITY_DATASETS,
    bis_global_liquidity,
    coinbase_product_trades,
    finra_equity,
)


def test_bis_global_liquidity_parses_csv_and_uses_official_endpoint():
    seen = []
    payload = (
        "FREQ,CURRENCY,BORROWERS_CTY,TIME_PERIOD,OBS_VALUE\n"
        "Q,USD,3P,2025-Q4,7.2\n"
        "Q,USD,3P,2026-Q1,6.8\n"
    ).encode()

    def transport(url):
        seen.append(url)
        return 200, payload

    result = bis_global_liquidity(limit=2, transport=transport)
    assert result.provider_id == "bis"
    assert result.row_count == 2
    assert result.rows[-1]["TIME_PERIOD"] == "2026-Q1"
    assert result.rows[-1]["OBS_VALUE"] == "6.8"
    assert result.rows[-1]["series_alias"] == "usd_credit_nonbanks_ex_us_yoy"
    assert seen and seen[0].startswith(
        "https://stats.bis.org/api/v2/data/dataflow/BIS/WS_GLI/1.0/"
    )
    assert "lastNObservations=2" in seen[0]
    assert "format=csv" in seen[0]


def test_bis_global_liquidity_fails_closed_on_bad_inputs_and_payloads():
    with pytest.raises(ValueError, match="unsupported BIS"):
        bis_global_liquidity("not-a-series", transport=lambda _url: (200, b"x"))
    with pytest.raises(ValueError, match="limit"):
        bis_global_liquidity(limit=0, transport=lambda _url: (200, b"x"))
    with pytest.raises(ValueError, match="required fields"):
        bis_global_liquidity(transport=lambda _url: (200, b"TIME_PERIOD,OTHER\n2026-Q1,1\n"))
    assert "usd_credit_nonbanks_ex_us_yoy" in BIS_GLOBAL_LIQUIDITY_SERIES


def test_coinbase_product_trades_parses_public_trade_tape():
    seen = []
    payload = json.dumps(
        [
            {
                "time": "2026-09-29T12:00:00.000Z",
                "trade_id": 123,
                "price": "65000.25",
                "size": "0.125",
                "side": "sell",
            }
        ]
    ).encode()

    def transport(url):
        seen.append(url)
        return 200, payload

    result = coinbase_product_trades("btc-usd", limit=1, transport=transport)
    assert result.provider_id == "coinbase-exchange"
    assert result.dataset == "spot-trades:BTC-USD"
    assert result.rows[0]["product_id"] == "BTC-USD"
    assert result.rows[0]["price"] == "65000.25"
    assert seen == ["https://api.exchange.coinbase.com/products/BTC-USD/trades?limit=1"]


def test_coinbase_product_trades_rejects_malformed_requests_and_rows():
    with pytest.raises(ValueError, match="product id"):
        coinbase_product_trades("https://evil.example", transport=lambda _url: (200, b"[]"))
    with pytest.raises(ValueError, match="limit"):
        coinbase_product_trades(limit=1001, transport=lambda _url: (200, b"[]"))
    with pytest.raises(ValueError, match="trade row"):
        coinbase_product_trades(
            transport=lambda _url: (200, json.dumps([{"price": "1"}]).encode())
        )


def test_finra_equity_uses_vetted_dataset_and_bearer_token():
    seen = []

    def request_transport(request):
        seen.append(request)
        return 200, json.dumps(
            [
                {
                    "tradeReportDate": "2026-09-28",
                    "securitiesInformationProcessorSymbolIdentifier": "AAPL",
                    "shortParQuantity": 100,
                    "totalParQuantity": 250,
                }
            ]
        ).encode()

    result = finra_equity(
        "reg_sho_daily",
        limit=1,
        request_transport=request_transport,
        access_token="test-token",
    )
    assert result.provider_id == "finra"
    assert result.dataset == "reg_sho_daily"
    assert result.row_count == 1
    assert seen[0].full_url == (
        "https://api.finra.org/data/group/otcMarket/name/regShoDaily?limit=1"
    )
    assert seen[0].headers["Authorization"] == "Bearer test-token"
    assert "consolidated_short_interest" in FINRA_EQUITY_DATASETS


def test_finra_equity_fails_closed_for_unknown_dataset():
    with pytest.raises(ValueError, match="unsupported FINRA equity"):
        finra_equity("not-a-dataset", access_token="x")
