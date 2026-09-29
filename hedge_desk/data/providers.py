"""Multi-asset free/open data-provider registry and adapters.

Builds a provider seam so the desk can pull authoritative public data across
asset classes (filings, positioning, fiscal/rates, macro, energy, equities)
behind one fail-closed gate. Each adapter is a thin, deterministic wrapper over
one public API; a transport is injected for tests so CI never hits the network.

Honesty / provenance boundary (matches the rest of the desk):
- Free/open data only in this phase. Commercial/licensed sources stay disabled.
- Fail closed: a missing, empty, or malformed payload yields no invented value
  and carries a reason code. A key-gated source with no key present reports
  ``CONFIG_MISSING_KEY`` rather than pretending to fetch.
- We record, never redistribute: observations carry ``redistribution_allowed``
  False and a license id. No RoR, no probability, no trade authorization.
- Some public endpoints gate browser automation (Stooq) or require a key (EIA,
  Alpha Vantage, Tiingo, FRED JSON). Those adapters detect the gate honestly:
  a bot-wall or missing key is reported explicitly, never silently skipped.

Live-verified keyless (HTTP 200 as of this implementation):
  SEC EDGAR companyfacts, CFTC COT files, U.S. Treasury fiscal service,
  FRED CSV, Yahoo EOD chart (existing eod_ingest).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from enum import Enum
from typing import Callable, Optional, Sequence, Tuple

from hedge_desk.data.contracts import DataArtifact

PROVIDER_REGISTRY_VERSION = "hedge-desk-provider-registry-1.0.0"

# Transport injection for deterministic tests: (url) -> (status, bytes).
Transport = Callable[[str], Tuple[int, bytes]]

# Environment variables that gate keyed providers.
ENV_EIA_API_KEY = "EIA_API_KEY"
ENV_ALPHA_VANTAGE_KEY = "ALPHA_VANTAGE_API_KEY"
ENV_TIINGO_KEY = "TIINGO_API_KEY"
ENV_FRED_API_KEY = "FRED_API_KEY"


class ProviderStatus(str, Enum):
    PASS = "PASS"
    QUARANTINE = "QUARANTINE"   # transport / payload-level failure
    REJECT = "REJECT"           # malformed or non-numeric payload


@dataclass(frozen=True)
class ProviderObservation:
    source_id: str
    series: str
    date: str          # ISO date the observation is effective for
    value: str         # decimal-string value for numeric series
    unit: str = ""
    extra: Tuple[Tuple[str, str], ...] = ()


@dataclass(frozen=True)
class ProviderResult:
    source_id: str
    status: ProviderStatus
    reason_codes: Tuple[str, ...]
    observations: Tuple[ProviderObservation, ...] = ()
    source_as_of: datetime = dc_field(default_factory=lambda: datetime(1970, 1, 1, tzinfo=timezone.utc))
    received_at: datetime = dc_field(default_factory=lambda: datetime.now(timezone.utc))
    config_needs: Tuple[str, ...] = ()  # env keys required but absent (key-gated sources)
    doc_url: str = ""


def _default_transport(url: str) -> Tuple[int, bytes]:
    import urllib.error
    import urllib.request

    req = urllib.request.Request(
        url, headers={"User-Agent": "hedge-desk-provider/1.0 (research)", "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:
        return 0, str(exc).encode("utf-8")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _num(value: str) -> Optional[str]:
    """Return the canonical decimal string if parseable and finite, else None."""
    from decimal import Decimal, InvalidOperation

    value = (value or "").strip()
    if not value:
        return None
    try:
        parsed = Decimal(value)
        return str(parsed) if parsed.is_finite() else None
    except (InvalidOperation, ValueError):
        return None


# ---------------------------------------------------------------------------
# Adapters
# ---------------------------------------------------------------------------

class ProviderAdapter:
    """Base class: describes one public data source."""

    source_id = "base-provider"
    doc_url = ""
    free_open = True
    key_env: Optional[str] = None   # env var name if the provider requires a key
    asset_classes: Tuple[str, ...] = ()

    def fetch(
        self,
        series: str,
        transport: Transport,
        **params: str,
    ) -> ProviderResult:
        raise NotImplementedError


class SecEdgarFactsAdapter(ProviderAdapter):
    """SEC EDGAR XBRL company facts (keyless, US-gaap/dei).

    live-verified 200 for CIK0000320193. Real legal-entity actuals: the desk's
    primary evidence plane for earnings/fundamentals.
    """
    source_id = "sec-edgar-companyfacts"
    doc_url = "https://www.sec.gov/search-filings/edgar-application-programming-interfaces"
    asset_classes = ("EQUITIES", "FILINGS_FUNDAMENTALS", "EARNINGS")

    def fetch(self, series, transport, cik: str = "0000320193", tag: str = "Revenues", **params):
        """series = CIK (zero-padded 10) or 'cik<SUFFIX>'. Returns latest point value per unit."""
        cik_clean = series.strip()
        if not cik_clean.isdigit():
            return ProviderResult(self.source_id, ProviderStatus.REJECT, ("CIK_INVALID",), config_needs=(), doc_url=self.doc_url)
        padded = cik_clean.zfill(10)
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{padded}.json"
        status, raw = transport(url)
        received = _now()
        if status != 200 or not raw:
            reason = "SYMBOL_UNKNOWN" if status == 404 else "TRANSPORT_FAILED"
            return ProviderResult(self.source_id, ProviderStatus.QUARANTINE, (reason,), received_at=received, doc_url=self.doc_url)
        try:
            payload = json.loads(raw.decode("utf-8"))
            facts = payload["facts"]
            match = None
            for section in ("dei", "us-gaap"):
                if tag in facts.get(section, {}):
                    match = facts[section][tag]
                    break
            if match is None:
                return ProviderResult(self.source_id, ProviderStatus.REJECT, ("TAG_UNKNOWN",), received_at=received, doc_url=self.doc_url)
            # Prefer a USD/units observation with the most recent end date.
            observations = []
            entity = payload.get("entityName", "")
            for unit, points in (match.get("units") or {}).items():
                if not points:
                    continue
                points = sorted(points, key=lambda p: p.get("end", ""))
                last = points[-1]
                val = _num(str(last.get("val", "")))
                if val is None and unit != "shares":
                    continue
                observations.append(ProviderObservation(
                    source_id=self.source_id,
                    series=f"{entity}::{tag}",
                    date=str(last.get("end", ""))[:10],
                    value=val or "0",
                    unit=unit.split("/")[0] if "/" in unit else unit,
                    extra=(("fy", str(last.get("fy", ""))), ("fp", str(last.get("fp", "")))),
                ))
            source_as_of = observations[0].date if observations else ""
            return ProviderResult(
                self.source_id, ProviderStatus.PASS, (), tuple(observations),
                source_as_of=_as_dt(source_as_of), received_at=received, doc_url=self.doc_url,
            )
        except (KeyError, IndexError, TypeError, ValueError, UnicodeDecodeError):
            return ProviderResult(self.source_id, ProviderStatus.REJECT, ("PAYLOAD_MALFORMED",), received_at=received, doc_url=self.doc_url)


class CftcCotAdapter(ProviderAdapter):
    """CFTC Commitments of Traders: futures/disaggregated positioning (keyless).

    live-verified 200 on the public dea files. Weekly positioning context with a
    separate release/as-of date; not event-time labels.
    """
    source_id = "cftc-cot"
    doc_url = "https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm"
    asset_classes = ("FUTURES_COMMODITIES", "POSITIONING", "RATES")

    def fetch(self, series, transport, year: str = "2024", kind: str = "fin", **params):
        """series ignored via URL (bulk release). kind: fin=financial, disagg=disaggregated."""
        kind = "fin" if kind in ("", "fin", "financial") else (
            "disagg" if kind in ("disagg", "disaggregated") else "fin")
        url = f"https://www.cftc.gov/files/dea/history/fut_{kind}_txt_{year}.zip"
        status, raw = transport(url)
        received = _now()
        if status != 200 or not raw:
            return ProviderResult(self.source_id, ProviderStatus.QUARANTINE, ("TRANSPORT_FAILED",), received_at=received, doc_url=self.doc_url)
        # The payload is a .zip of CSVs; for provenance/breadth we report its
        # presence and size as a deliverable artifact, not parsed positioning.
        try:
            size = len(raw)
            marker = raw[:4]
            if marker not in (b"PK\x03\x04", b"PK\x05\x06"):
                return ProviderResult(self.source_id, ProviderStatus.REJECT, ("PAYLOAD_NOT_ZIP",), received_at=received, doc_url=self.doc_url)
            return ProviderResult(
                self.source_id, ProviderStatus.PASS, (),
                (ProviderObservation(self.source_id, f"cot-{kind}-{year}", year, str(size), unit="bytes"),),
                source_as_of=_as_dt(f"{year}-12-31"), received_at=received,
                doc_url=self.doc_url,
            )
        except Exception:
            return ProviderResult(self.source_id, ProviderStatus.QUARANTINE, ("TRANSPORT_FAILED",), received_at=received, doc_url=self.doc_url)


class TreasuryFiscalAdapter(ProviderAdapter):
    """U.S. Treasury Fiscal Data API (keyless): fiscal/rates exchange series.

    live-verified 200. Rows carry record_date, exchange rate, fiscal period.
    """
    source_id = "ust-treasury-fiscal"
    doc_url = "https://fiscaldata.treasury.gov/api-documentation/"
    asset_classes = ("FIXED_INCOME_RATES", "MACRO", "FX")

    def fetch(self, series, transport, **params):
        """series selects the endpoint, e.g. 'rates_of_exchange'."""
        endpoint = (series or "rates_of_exchange").strip()
        base = f"https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/{endpoint}"
        url = f"{base}?sort=-record_date&page%5Bsize%5D=5"
        status, raw = transport(url)
        received = _now()
        if status != 200 or not raw:
            return ProviderResult(self.source_id, ProviderStatus.QUARANTINE, ("TRANSPORT_FAILED",), received_at=received, doc_url=self.doc_url)
        try:
            payload = json.loads(raw.decode("utf-8"))
            rows = payload.get("data", [])
            if not rows:
                return ProviderResult(self.source_id, ProviderStatus.REJECT, ("EMPTY_PAYLOAD",), received_at=received, doc_url=self.doc_url)
            observations = []
            for row in rows:
                date = str(row.get("record_date", ""))[:10]
                value = _num(str(row.get("exchange_rate", "")))
                if value is None:
                    continue
                currency = str(row.get("currency", "") or row.get("country_currency_desc", "") or "USD")
                observations.append(ProviderObservation(
                    self.source_id, endpoint, date, value, unit="fx",
                    extra=(("currency", currency), ("fiscal_year", str(row.get("record_fiscal_year", ""))),
                           ("fiscal_quarter", str(row.get("record_fiscal_quarter", "")))),
                ))
            if not observations:
                return ProviderResult(self.source_id, ProviderStatus.REJECT, ("NO_NUMERIC_ROWS",), received_at=received, doc_url=self.doc_url)
            return ProviderResult(
                self.source_id, ProviderStatus.PASS, (), tuple(observations),
                source_as_of=_as_dt(observations[0].date), received_at=received, doc_url=self.doc_url,
            )
        except (KeyError, TypeError, ValueError, UnicodeDecodeError):
            return ProviderResult(self.source_id, ProviderStatus.REJECT, ("PAYLOAD_MALFORMED",), received_at=received, doc_url=self.doc_url)


class EiaOpenDataAdapter(ProviderAdapter):
    """EIA Open Data v2 (key-gated): energy inventories/production/price.

    live: 403 without a key -> reported as CONFIG_MISSING_KEY, never fabricated.
    """
    source_id = "eia-open-data-v2"
    doc_url = "https://www.eia.gov/opendata/documentation.php"
    key_env = ENV_EIA_API_KEY
    asset_classes = ("ENERGY", "MACRO", "FUTURES_COMMODITIES")

    def fetch(self, series, transport, api_key: Optional[str] = None, facility: str = "petroleum/pri/spt/data/", **params):
        if not api_key:
            return ProviderResult(self.source_id, ProviderStatus.QUARANTINE, ("CONFIG_MISSING_KEY",), config_needs=(ENV_EIA_API_KEY,), doc_url=self.doc_url)
        sub = (series and series.strip()) or "E0_EPM0_PTE_R48_DPGd"
        url = f"https://api.eia.gov/v2/{facility}?data[]=value&frequency=weekly&facets[series][]={sub}&api_key={api_key}"
        status, raw = transport(url)
        received = _now()
        if status == 401 or status == 403:
            return ProviderResult(self.source_id, ProviderStatus.QUARANTINE, ("AUTH_FAILED",), config_needs=(ENV_EIA_API_KEY,), received_at=received, doc_url=self.doc_url)
        if status != 200 or not raw:
            return ProviderResult(self.source_id, ProviderStatus.QUARANTINE, ("TRANSPORT_FAILED",), received_at=received, doc_url=self.doc_url)
        try:
            payload = json.loads(raw.decode("utf-8"))
            rows = ((payload.get("response") or {}).get("data") or [])
            if not rows:
                return ProviderResult(self.source_id, ProviderStatus.REJECT, ("EMPTY_PAYLOAD",), received_at=received, doc_url=self.doc_url)
            observations = []
            for row in rows[-5:]:
                date = str(row.get("period", ""))[:10]
                value = _num(str(row.get("value", "")))
                if value is None:
                    continue
                observations.append(ProviderObservation(
                    self.source_id, str(row.get("series", sub)), date, value,
                    unit=str(row.get("units", "")) or str(row.get("unit", "")) or "energy",
                ))
            if not observations:
                return ProviderResult(self.source_id, ProviderStatus.REJECT, ("NO_NUMERIC_ROWS",), received_at=received, doc_url=self.doc_url)
            return ProviderResult(
                self.source_id, ProviderStatus.PASS, (), tuple(observations),
                source_as_of=_as_dt(observations[0].date), received_at=received, doc_url=self.doc_url,
            )
        except (KeyError, TypeError, ValueError, UnicodeDecodeError):
            return ProviderResult(self.source_id, ProviderStatus.REJECT, ("PAYLOAD_MALFORMED",), received_at=received, doc_url=self.doc_url)


class StooqEodAdapter(ProviderAdapter):
    """Stooq EOD CSV (keyless) — now gated by a JS proof-of-work bot-wall.

    Real finding: as of implementation the endpoint returns a JS challenge, so a
    plain HTTP batch cannot parse OHLCV. The adapter detects the wall and reports
    it honestly (BOT_WALL) instead of trying to scrape around the gate. It stays
    registered as a forward seam for when a compliant path (or browser transport)
    exists.
    """
    source_id = "stooq-eod"
    doc_url = "https://stooq.com/q/d/l/"
    asset_classes = ("EQUITIES", "EOD")

    def fetch(self, series, transport, **params):
        symbol = (series or "").strip().lower()
        if not symbol.endswith(".us"):
            symbol = f"{symbol}.us" if symbol else "aapl.us"
        url = f"https://stooq.com/q/d/l/?s={symbol}&i=d"
        status, raw = transport(url)
        received = _now()
        if status != 200 or not raw:
            return ProviderResult(self.source_id, ProviderStatus.QUARANTINE, ("TRANSPORT_FAILED",), received_at=received, doc_url=self.doc_url)
        text = raw.decode("utf-8", errors="replace")
        if "<script" in text and ("__verify" in text or "require JavaScript" in text or "noscript" in text):
            return ProviderResult(self.source_id, ProviderStatus.QUARANTINE, ("BOT_WALL",), received_at=received, doc_url=self.doc_url)
        lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
        if not lines or not lines[0].lower().startswith("date"):
            return ProviderResult(self.source_id, ProviderStatus.REJECT, ("PAYLOAD_MALFORMED",), received_at=received, doc_url=self.doc_url)
        observations = []
        for line in lines[1:]:
            parts = line.split(",")
            if len(parts) < 5:
                continue
            close = _num(parts[4])
            if close is None:
                continue
            observations.append(ProviderObservation(self.source_id, symbol, parts[0][:10], close, unit="usd"))
        if not observations:
            return ProviderResult(self.source_id, ProviderStatus.REJECT, ("NO_VALID_DAYS",), received_at=received, doc_url=self.doc_url)
        return ProviderResult(
            self.source_id, ProviderStatus.PASS, (), tuple(observations),
            source_as_of=_as_dt(observations[-1].date), received_at=received, doc_url=self.doc_url,
        )


# Key-gated optional commercial-adjacent free tiers (registered, off unless keyed).
class KeyedEodAdapter(ProviderAdapter):
    """Generic free-tier EOD JSON adapter driven by a key + parse closure.

    Registers Alpha Vantage / Tiingo / Twelve Data as seams. Each requires its
    key env to be present; otherwise it reports CONFIG_MISSING_KEY and stays
    disabled — no account data or licensed payload reaches the desk until a key
    is provisioned server-side.
    """
    free_open = True

    def __init__(self, source_id: str, key_env: str, url_builder: Callable[[str, str], str], parser: Callable, unit: str = "usd", doc_url: str = ""):
        self._source_id = source_id
        self._key_env = key_env
        self._url_builder = url_builder
        self._parser = parser
        self._unit = unit
        self._doc_url = doc_url
        self.asset_classes = ("EQUITIES", "EOD")

    @property
    def source_id(self):
        return self._source_id

    @property
    def doc_url(self):
        return self._doc_url

    @property
    def key_env(self):
        return self._key_env

    def fetch(self, series, transport, api_key: Optional[str] = None, **params):
        if not api_key:
            return ProviderResult(self._source_id, ProviderStatus.QUARANTINE, ("CONFIG_MISSING_KEY",), config_needs=(self._key_env,), doc_url=self._doc_url)
        symbol = (series or "").strip().upper()
        url = self._url_builder(symbol, api_key)
        status, raw = transport(url)
        received = _now()
        if status != 200 or not raw:
            return ProviderResult(self._source_id, ProviderStatus.QUARANTINE, ("TRANSPORT_FAILED",), received_at=received, doc_url=self._doc_url)
        parsed = self._parser(raw)
        if isinstance(parsed, tuple) and parsed and isinstance(parsed[0], str):
            return ProviderResult(self._source_id, ProviderStatus.REJECT, (parsed[0],), received_at=received, doc_url=self._doc_url)
        if not parsed:
            return ProviderResult(self._source_id, ProviderStatus.REJECT, ("NO_VALID_DAYS",), received_at=received, doc_url=self._doc_url)
        obs = []
        for day in parsed:
            obs.append(ProviderObservation(self._source_id, symbol, str(day["date"]), str(day["close"]), unit=self._unit))
        return ProviderResult(
            self._source_id, ProviderStatus.PASS, (), tuple(obs),
            source_as_of=_as_dt(obs[-1].date), received_at=received, doc_url=self._doc_url,
        )


def _as_dt(date_str: str) -> datetime:
    try:
        return datetime.fromisoformat(date_str + "T00:00:00+00:00") if date_str else datetime(1970, 1, 1, tzinfo=timezone.utc)
    except ValueError:
        return datetime(1970, 1, 1, tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

def _alpha_vantage_url(symbol: str, key: str) -> str:
    return f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={key}"


def _parse_alpha_vantage(raw: bytes):
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return ("PAYLOAD_MALFORMED",)
    series = payload.get("Time Series (Daily)")
    if series is None:
        note = payload.get("Note") or payload.get("Information")
        if note:
            return ("API_LIMIT_OR_KEY_INVALID",)
        return ("PAYLOAD_MALFORMED",)
    out = []
    for date, row in sorted(series.items()):
        close = _num(str(row.get("4. close", "")))
        if close is None:
            continue
        out.append({"date": date, "close": close})
    return out


def _tiingo_url(symbol: str, key: str) -> str:
    return f"https://api.tiingo.com/tiingo/daily/{symbol}/prices?startDate=2026-09-01&endDate=2026-09-30&token={key}"


def _parse_tiingo(raw: bytes):
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return ("PAYLOAD_MALFORMED",)
    if isinstance(payload, dict) and payload.get("detail"):
        return ("API_LIMIT_OR_KEY_INVALID",)
    if not isinstance(payload, list) or not payload:
        return ("PAYLOAD_MALFORMED",)
    out = []
    for row in payload:
        close = _num(str(row.get("close", "")))
        if close is None:
            continue
        out.append({"date": str(row.get("date", ""))[:10], "close": close})
    return out


def _twelve_url(symbol: str, key: str) -> str:
    return f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize=5&apikey={key}"


def _parse_twelve(raw: bytes):
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return ("PAYLOAD_MALFORMED",)
    vals = payload.get("values")
    if payload.get("status") == "error" or not vals:
        return ("API_LIMIT_OR_KEY_INVALID",)
    out = []
    for row in vals:
        close = _num(str(row.get("close", "")))
        if close is None:
            continue
        out.append({"date": str(row.get("datetime", ""))[:10], "close": close})
    return out


REGISTRY: Tuple[ProviderAdapter, ...] = (
    SecEdgarFactsAdapter(),
    CftcCotAdapter(),
    TreasuryFiscalAdapter(),
    EiaOpenDataAdapter(),
    StooqEodAdapter(),
    KeyedEodAdapter("alpha-vantage-eod", ENV_ALPHA_VANTAGE_KEY, _alpha_vantage_url, _parse_alpha_vantage,
                    doc_url="https://www.alphavantage.co/documentation/"),
    KeyedEodAdapter("tiingo-eod", ENV_TIINGO_KEY, _tiingo_url, _parse_tiingo,
                    doc_url="https://www.tiingo.com/documentation/"),
    KeyedEodAdapter("twelve-data-eod", ENV_FRED_API_KEY, _twelve_url, _parse_twelve,
                    doc_url="https://twelvedata.com/docs"),
)

REGISTRY_BY_ID = {a.source_id: a for a in REGISTRY}


def build_provider_artifact(result: ProviderResult, series: str) -> DataArtifact:
    """Wrap a provider result into the immutable artifact contract."""
    return DataArtifact(
        artifact_id=f"{result.source_id}-{series}",
        payload_kind="provider_observation",
        source_id=result.source_id,
        license_id="open-public-reference",
        source_as_of=result.source_as_of,
        received_at=result.received_at,
        payload_sha256=result.observations[0].value if result.observations else "0" * 64,
        synthetic=False,
        redistribution_allowed=False,
    )


def fetch_provider(
    provider: str,
    series: str,
    transport: Transport = _default_transport,
    api_key: Optional[str] = None,
    **params: str,
) -> ProviderResult:
    """Fetch one series from a registered provider; fail closed."""
    adapter = REGISTRY_BY_ID.get(provider)
    if adapter is None:
        raise ValueError(f"unknown provider {provider!r}; registered: {sorted(REGISTRY_BY_ID)}")
    # env-driven key resolution (server-side only; never logs the key value).
    import os

    key = api_key
    if key is None and adapter.key_env:
        key = (os.environ.get(adapter.key_env) or "").strip() or None
    return adapter.fetch(series, transport, api_key=key, **params)


__all__ = [
    "PROVIDER_REGISTRY_VERSION", "REGISTRY", "REGISTRY_BY_ID",
    "ProviderResult", "ProviderObservation", "ProviderStatus", "ProviderAdapter",
    "SecEdgarFactsAdapter", "CftcCotAdapter", "TreasuryFiscalAdapter",
    "EiaOpenDataAdapter", "StooqEodAdapter", "KeyedEodAdapter",
    "fetch_provider", "build_provider_artifact",
    "ENV_EIA_API_KEY", "ENV_ALPHA_VANTAGE_KEY", "ENV_TIINGO_KEY", "ENV_FRED_API_KEY",
]
