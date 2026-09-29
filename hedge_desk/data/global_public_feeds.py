"""Keyless global macro and physical-event research feeds.

These adapters extend the desk's read-only public data plane with international
macro indicators and physical-event context. They use narrow allowlists,
bounded queries, existing retry/backoff helpers, and fail closed on malformed
or unavailable upstream data.

No function in this module places an order, authorizes a trade, or computes
Risk of Ruin.
"""

from __future__ import annotations

import csv
import io
import json
import re
import urllib.parse
from datetime import date, timedelta
from typing import Mapping, Sequence, Tuple

from .open_market_feeds import (
    OpenFeedResult,
    Transport,
    _default_transport,
    _fetch_bytes,
    _fetch_json,
)

IMF_DATAMAPPER_URL = "https://www.imf.org/external/datamapper/api/v2/{indicator}/{entities}"
OECD_CLI_URL = (
    "https://sdmx.oecd.org/public/rest/data/"
    "OECD.SDD.STES,DSD_STES@DF_CLI,4.1/{area}.M.LI...AA...H"
)
EUROSTAT_HICP_URL = (
    "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
    "prc_hicp_minr"
)
USGS_EVENT_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
NASA_EONET_URL = "https://eonet.gsfc.nasa.gov/api/v3/events"

IMF_INDICATORS = frozenset(
    {
        "NGDP_RPCH",     # real GDP growth, percent change
        "PCPIPCH",       # consumer price inflation, percent change
        "LUR",           # unemployment rate
        "GGXWDG_NGDP",   # general government gross debt, percent GDP
        "GGXCNL_NGDP",   # general government net lending/borrowing, percent GDP
        "BCA_NGDPD",     # current account balance, percent GDP
    }
)
IMF_ENTITIES = frozenset({"USA", "CHN", "DEU", "JPN", "GBR", "FRA", "IND", "BRA"})
OECD_CLI_AREAS = frozenset({"USA", "CHN", "DEU", "JPN", "GBR", "FRA", "IND", "BRA", "G7", "G20"})
EUROSTAT_HICP_GEOS = frozenset({"EA20", "EU27_2020", "DE", "FR", "IT", "ES", "NL"})

_PERIOD_RE = re.compile(r"^\d{4}-\d{2}$")


def _bounded_int(value: int, minimum: int, maximum: int, name: str) -> int:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{name} must be an integer from {minimum} to {maximum}")
    return value


def imf_datamapper(
    indicator: str = "NGDP_RPCH",
    entities: Sequence[str] = ("USA", "CHN", "DEU", "JPN", "GBR"),
    periods: Sequence[int] | None = None,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch an allowlisted IMF DataMapper v2 time series (no key required)."""
    normalized_indicator = indicator.strip().upper()
    if normalized_indicator not in IMF_INDICATORS:
        raise ValueError(f"unsupported IMF DataMapper indicator: {indicator}")
    normalized_entities = tuple(str(item).strip().upper() for item in entities)
    if not normalized_entities or len(normalized_entities) > 12:
        raise ValueError("IMF entities must contain from 1 to 12 items")
    if any(item not in IMF_ENTITIES for item in normalized_entities):
        raise ValueError("unsupported IMF DataMapper entity")

    url = IMF_DATAMAPPER_URL.format(
        indicator=urllib.parse.quote(normalized_indicator, safe=""),
        entities="/".join(urllib.parse.quote(item, safe="") for item in normalized_entities),
    )
    if periods is not None:
        normalized_periods = tuple(int(item) for item in periods)
        if not normalized_periods or len(normalized_periods) > 20:
            raise ValueError("IMF periods must contain from 1 to 20 years")
        if any(item < 1900 or item > 2200 for item in normalized_periods):
            raise ValueError("IMF period is outside the supported year range")
        url = f"{url}?{urllib.parse.urlencode({'periods': ','.join(str(item) for item in normalized_periods)})}"

    payload = _fetch_json(url, "imf-datamapper", transport)
    if not isinstance(payload, dict):
        raise ValueError("imf-datamapper payload is malformed")
    values = payload.get("values")
    by_indicator = values.get(normalized_indicator) if isinstance(values, dict) else None
    if not isinstance(by_indicator, dict):
        raise ValueError("imf-datamapper payload has no requested indicator")

    rows = []
    for entity in normalized_entities:
        observations = by_indicator.get(entity)
        if observations is None:
            continue
        if not isinstance(observations, dict):
            raise ValueError("imf-datamapper entity observations are malformed")
        for period, value in observations.items():
            if value is None:
                continue
            rows.append(
                {
                    "indicator": normalized_indicator,
                    "entity": entity,
                    "period": str(period),
                    "value": value,
                }
            )
    if not rows:
        raise ValueError("imf-datamapper payload has no observations")
    rows.sort(key=lambda item: (item["entity"], item["period"]))
    return OpenFeedResult("imf-datamapper", normalized_indicator, tuple(rows))


def oecd_composite_leading_indicator(
    area: str = "USA",
    start_period: str | None = None,
    limit: int = 18,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch OECD's harmonised monthly Composite Leading Indicator."""
    normalized_area = area.strip().upper()
    if normalized_area not in OECD_CLI_AREAS:
        raise ValueError(f"unsupported OECD CLI reference area: {area}")
    limit = _bounded_int(limit, 1, 120, "limit")
    if start_period is not None and not _PERIOD_RE.fullmatch(start_period):
        raise ValueError("start_period must use YYYY-MM")

    query = {
        "dimensionAtObservation": "AllDimensions",
        "format": "csvfilewithlabels",
    }
    if start_period:
        query["startPeriod"] = start_period
    url = f"{OECD_CLI_URL.format(area=normalized_area)}?{urllib.parse.urlencode(query)}"
    raw = _fetch_bytes(url, "oecd-cli", transport)
    try:
        reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
        rows = list(reader)
    except (UnicodeDecodeError, csv.Error) as exc:
        raise ValueError("oecd-cli returned malformed CSV") from exc
    if not rows:
        raise ValueError("oecd-cli payload has no observations")

    required = {"REF_AREA", "TIME_PERIOD", "OBS_VALUE"}
    normalized = []
    for row in rows:
        if not required.issubset(row):
            raise ValueError("oecd-cli payload is missing required columns")
        if row.get("REF_AREA") != normalized_area:
            continue
        if not row.get("TIME_PERIOD") or row.get("OBS_VALUE") in (None, ""):
            continue
        normalized.append(
            {
                "reference_area": row["REF_AREA"],
                "time_period": row["TIME_PERIOD"],
                "value": row["OBS_VALUE"],
                "unit_measure": row.get("UNIT_MEASURE", ""),
                "measure": row.get("MEASURE", "LI"),
            }
        )
    if not normalized:
        raise ValueError("oecd-cli payload has no matching observations")
    normalized.sort(key=lambda item: item["time_period"])
    return OpenFeedResult("oecd-cli", "composite-leading-indicator", tuple(normalized[-limit:]))


def _jsonstat_positions(category_index: object) -> list[tuple[str, int]]:
    if isinstance(category_index, dict):
        pairs = []
        for code, position in category_index.items():
            if not isinstance(position, int):
                raise ValueError("eurostat category index is malformed")
            pairs.append((str(code), position))
        return sorted(pairs, key=lambda item: item[1])
    if isinstance(category_index, list):
        return [(str(code), position) for position, code in enumerate(category_index)]
    raise ValueError("eurostat category index is malformed")


def eurostat_hicp_inflation(
    geo: str = "EA20",
    periods: int = 12,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch current monthly all-items HICP annual inflation from Eurostat."""
    normalized_geo = geo.strip().upper()
    if normalized_geo not in EUROSTAT_HICP_GEOS:
        raise ValueError(f"unsupported Eurostat HICP geography: {geo}")
    periods = _bounded_int(periods, 1, 60, "periods")
    query = urllib.parse.urlencode(
        {
            "format": "JSON",
            "lang": "EN",
            "freq": "M",
            "unit": "RCH_A",
            "coicop": "CP00",
            "geo": normalized_geo,
            "lastTimePeriod": str(periods),
        }
    )
    payload = _fetch_json(f"{EUROSTAT_HICP_URL}?{query}", "eurostat-hicp", transport)
    if not isinstance(payload, dict):
        raise ValueError("eurostat-hicp payload is malformed")
    ids = payload.get("id")
    sizes = payload.get("size")
    dimension = payload.get("dimension")
    values = payload.get("value")
    if not isinstance(ids, list) or not isinstance(sizes, list) or not isinstance(dimension, dict):
        raise ValueError("eurostat-hicp dataset structure is malformed")
    if "time" not in ids or len(ids) != len(sizes):
        raise ValueError("eurostat-hicp time dimension is missing")
    time_index = ids.index("time")
    if any(int(size) != 1 for idx, size in enumerate(sizes) if idx != time_index):
        raise ValueError("eurostat-hicp query returned unexpected extra dimensions")
    time_dim = dimension.get("time")
    category = time_dim.get("category") if isinstance(time_dim, dict) else None
    index = category.get("index") if isinstance(category, dict) else None
    positions = _jsonstat_positions(index)
    if not positions:
        raise ValueError("eurostat-hicp payload has no time positions")

    rows = []
    for time_code, position in positions:
        if isinstance(values, list):
            value = values[position] if position < len(values) else None
        elif isinstance(values, dict):
            value = values.get(str(position))
        else:
            raise ValueError("eurostat-hicp values are malformed")
        if value is None:
            continue
        rows.append(
            {
                "geo": normalized_geo,
                "time_period": time_code,
                "value": value,
                "unit": "RCH_A",
                "coicop": "CP00",
            }
        )
    if not rows:
        raise ValueError("eurostat-hicp payload has no observations")
    return OpenFeedResult("eurostat", "prc_hicp_minr", tuple(rows))


def usgs_material_earthquakes(
    days: int = 7,
    min_magnitude: float = 5.5,
    limit: int = 50,
    as_of: date | None = None,
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch recent material earthquakes from the USGS FDSN Event API."""
    days = _bounded_int(days, 1, 30, "days")
    limit = _bounded_int(limit, 1, 500, "limit")
    try:
        magnitude = float(min_magnitude)
    except (TypeError, ValueError) as exc:
        raise ValueError("min_magnitude must be numeric") from exc
    if not 0.0 <= magnitude <= 10.0:
        raise ValueError("min_magnitude must be from 0 to 10")
    end = as_of or date.today()
    start = end - timedelta(days=days)
    query = urllib.parse.urlencode(
        {
            "format": "geojson",
            "starttime": start.isoformat(),
            "endtime": end.isoformat(),
            "minmagnitude": f"{magnitude:g}",
            "limit": str(limit),
            "orderby": "time",
            "eventtype": "earthquake",
        }
    )
    payload = _fetch_json(f"{USGS_EVENT_URL}?{query}", "usgs-earthquakes", transport)
    if not isinstance(payload, dict) or not isinstance(payload.get("features"), list):
        raise ValueError("usgs-earthquakes payload is malformed")
    rows = []
    for feature in payload["features"]:
        if not isinstance(feature, dict):
            raise ValueError("usgs-earthquakes feature is malformed")
        properties = feature.get("properties")
        geometry = feature.get("geometry")
        coords = geometry.get("coordinates") if isinstance(geometry, dict) else None
        if not isinstance(properties, dict) or not isinstance(coords, list) or len(coords) < 2:
            raise ValueError("usgs-earthquakes feature is missing required fields")
        rows.append(
            {
                "event_id": str(feature.get("id", "")),
                "time": properties.get("time"),
                "updated": properties.get("updated"),
                "magnitude": properties.get("mag"),
                "place": properties.get("place"),
                "alert": properties.get("alert"),
                "tsunami": properties.get("tsunami"),
                "significance": properties.get("sig"),
                "status": properties.get("status"),
                "url": properties.get("url"),
                "longitude": coords[0],
                "latitude": coords[1],
                "depth_km": coords[2] if len(coords) > 2 else None,
            }
        )
    return OpenFeedResult("usgs-earthquakes", "fdsn-material-events", tuple(rows))


def nasa_eonet_events(
    days: int = 30,
    limit: int = 50,
    status: str = "open",
    transport: Transport = _default_transport,
) -> OpenFeedResult:
    """Fetch current natural-event context from NASA EONET v3."""
    days = _bounded_int(days, 1, 365, "days")
    limit = _bounded_int(limit, 1, 500, "limit")
    normalized_status = status.strip().lower()
    if normalized_status not in {"open", "closed", "all"}:
        raise ValueError("EONET status must be open, closed, or all")
    query = urllib.parse.urlencode(
        {"status": normalized_status, "limit": str(limit), "days": str(days)}
    )
    payload = _fetch_json(f"{NASA_EONET_URL}?{query}", "nasa-eonet", transport)
    if not isinstance(payload, dict) or not isinstance(payload.get("events"), list):
        raise ValueError("nasa-eonet payload is malformed")
    rows = []
    for event in payload["events"]:
        if not isinstance(event, dict) or not event.get("id") or not event.get("title"):
            raise ValueError("nasa-eonet event is malformed")
        categories = event.get("categories") or []
        sources = event.get("sources") or []
        geometries = event.get("geometry") or []
        if not isinstance(categories, list) or not isinstance(sources, list) or not isinstance(geometries, list):
            raise ValueError("nasa-eonet event collections are malformed")
        latest_geometry = geometries[-1] if geometries else {}
        if latest_geometry and not isinstance(latest_geometry, dict):
            raise ValueError("nasa-eonet geometry is malformed")
        rows.append(
            {
                "event_id": str(event["id"]),
                "title": str(event["title"]),
                "closed": event.get("closed"),
                "categories": [
                    {"id": item.get("id"), "title": item.get("title")}
                    for item in categories
                    if isinstance(item, dict)
                ],
                "sources": [item.get("id") for item in sources if isinstance(item, dict)],
                "event_date": latest_geometry.get("date"),
                "geometry_type": latest_geometry.get("type"),
                "coordinates": latest_geometry.get("coordinates"),
                "magnitude_value": event.get("magnitudeValue"),
                "magnitude_unit": event.get("magnitudeUnit"),
            }
        )
    return OpenFeedResult("nasa-eonet", "natural-events-v3", tuple(rows))


__all__ = [
    "EUROSTAT_HICP_GEOS",
    "IMF_ENTITIES",
    "IMF_INDICATORS",
    "OECD_CLI_AREAS",
    "eurostat_hicp_inflation",
    "imf_datamapper",
    "nasa_eonet_events",
    "oecd_composite_leading_indicator",
    "usgs_material_earthquakes",
]
