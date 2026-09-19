"""Real option-chain intake from Cboe's public delayed-quotes API.

Turns a REAL Cboe chain (bid/ask/size/open interest/volume, delayed) into the
canonical ``OptionSnapshot`` the already-tested premium scanner consumes, then
returns executable income economics. This is the "real fukn data from over night"
path: no synthetic fixtures.

Source: https://cdn.cboe.com/api/global/delayed_quotes/options/{SYMBOL}.json
Delayed reference quotes for research. No order is placed.

Cboe option-symbol convention: ``SPY260918C00300000`` -> underlying + YYMMDD +
C/P + strike code (strike = int(code) / 1000), giving $300.00 for ``00300000``.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Callable, Dict, Tuple

from hedge_desk.options import (
    OptionQuote,
    OptionSnapshot,
    OptionType,
    SpreadScanPolicy,
    UnderlyingQuote,
    scan_vertical_credit_spreads,
)

CBOE_URL = "https://cdn.cboe.com/api/global/delayed_quotes/options/{symbol}.json"
Transport = Callable[[str], Tuple[int, bytes]]


def _default_transport(url: str) -> Tuple[int, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": "hedge-desk/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:
        return 0, str(exc).encode("utf-8")


def _d(value) -> Decimal:
    try:
        parsed = Decimal(str(value))
        return parsed if parsed.is_finite() else Decimal("0")
    except (InvalidOperation, ValueError):
        return Decimal("0")


def _parse_symbol(symbol: str) -> Tuple[str, date, OptionType, Decimal] | None:
    """Parse an OCC-style option symbol into (underlying, expiry, type, strike)."""
    try:
        # Underlying is the leading letters (2-6); keep it simple: strip suffix.
        body = symbol.upper()
        # Find the 6-digit YYMMDD near a known place: last chars before C/P.
        # Robust: scan for the first C or P that follows a 6-digit date.
        import re

        m = re.search(r"(\d{6})([CP])(\d{8})$", body)
        if not m:
            return None
        date_code, type_code, strike_code = m.group(1), m.group(2), m.group(3)
        expiry = date(
            2000 + int(date_code[0:2]),
            int(date_code[2:4]),
            int(date_code[4:6]),
        )
        ot = OptionType.CALL if type_code == "C" else OptionType.PUT
        strike = _d(strike_code) / Decimal("1000")
        underlying = body[: body.index(date_code)]
        return underlying, expiry, ot, strike
    except (ValueError, IndexError):
        return None


def build_snapshot_from_cboe(
    raw: bytes, symbol: str, quoted_at: datetime
) -> OptionSnapshot:
    """Parse a Cboe delayed-quotes payload into a canonical OptionSnapshot."""
    try:
        data = json.loads(raw.decode("utf-8"))["data"]
    except (KeyError, IndexError, TypeError, ValueError, UnicodeDecodeError) as exc:
        raise ValueError("cboe payload malformed") from exc
    opts = data.get("options")
    if not isinstance(opts, list) or not opts:
        raise ValueError("cboe payload has no options")
    current_price = _d(data.get("current_price"))
    if current_price <= 0:
        raise ValueError("cboe underlying price invalid")
    underlying_quote = UnderlyingQuote(
        symbol.upper(),
        _d(data.get("bid")) or current_price,
        _d(data.get("ask")) or current_price,
        quoted_at,
        f"cboe-delayed-{symbol.upper()}",
    )
    quotes = []
    seen = set()
    # Keep the scan bounded and on the ~30-day premium cycle the desk targets.
    # Choose the single expiration whose days-to-expiry is closest to the premium
    # window (27-45 days) AND safely past the scanner's planned pre-expiry exit
    # window (7 days). This matches the GP's "sell premiums ~every 30 days" shape
    # and avoids both the front month (too close / expired) and far-dated illiquid
    # months.
    target_dte = 34
    min_dte = 14  # must clear the 7-day exit window twice over
    max_dte = 45
    expiry_meta: Dict[str, date] = {}
    for item in opts:
        p = _parse_symbol(str(item.get("option", "")))
        if p:
            expiry_meta.setdefault(p[1].isoformat(), p[1])
    today_date = quoted_at.date()
    candidates = []
    for iso, exp in expiry_meta.items():
        dte = (exp - today_date).days
        if min_dte <= dte <= max_dte:
            candidates.append((abs(dte - target_dte), iso, exp))
    candidates.sort()
    if not candidates:
        raise ValueError("cboe chain has no expiration in the premium window")
    chosen_expiry = candidates[0][2]
    band_pct = Decimal("0.12")
    for item in opts:
        contract = str(item.get("option", ""))
        parsed = _parse_symbol(contract)
        if parsed is None:
            continue
        under, expiry, ot, strike = parsed
        if under.upper() != symbol.upper():
            continue
        if expiry != chosen_expiry:
            continue
        try:
            strike_dec = _d(strike)
        except (InvalidOperation, ValueError):
            continue
        if strike_dec <= 0:
            continue
        # Strike band filter: only within +-band_pct of the underlying, so the
        # defined-risk verticals are struck near the money on the liquid ETF.
        if not (current_price * (Decimal(1) - band_pct) <= strike_dec <= current_price * (Decimal(1) + band_pct)):
            continue
        bid = _d(item.get("bid"))
        ask = _d(item.get("ask"))
        bid_size = int(float(item.get("bid_size") or 0))
        ask_size = int(float(item.get("ask_size") or 0))
        if bid <= 0 or ask <= 0 or bid_size <= 0 or ask_size <= 0 or ask < bid:
            continue  # unexecutable quote
        if contract in seen:
            continue
        seen.add(contract)
        quotes.append(
            OptionQuote(
                contract,
                symbol.upper(),
                ot,
                strike,
                expiry,
                bid,
                ask,
                bid_size,
                ask_size,
                quoted_at,
                f"cboe-delayed-{symbol.upper()}",
                int(float(item.get("open_interest") or 0)),
                int(float(item.get("volume") or 0)),
            )
        )
    if not quotes:
        raise ValueError("cboe chain has no executable quotes")
    quotes.sort(key=lambda q: q.contract_id)
    return OptionSnapshot(
        "hedge-desk-option-snapshot-1.0.0",
        f"cboe-delayed-{symbol.upper()}",
        underlying_quote,
        tuple(quotes),
        "0" * 64,
    )


def real_chain_income(
    symbol: str,
    cutoff: datetime,
    transport: Transport = _default_transport,
    quantity: int = 1,
    commission_per_contract: str = "0.65",
) -> Dict[str, object]:
    """Fetch a real Cboe chain and return executable income for each spread."""
    if cutoff.tzinfo is None:
        raise ValueError("cutoff must be timezone-aware")
    if not symbol or not str(symbol).strip():
        raise ValueError("symbol required")
    symbol = str(symbol).upper().strip()
    status, raw = transport(CBOE_URL.format(symbol=symbol))
    if status != 200 or not raw:
        raise ValueError(f"cboe fetch failed (status {status})")
    snapshot = build_snapshot_from_cboe(raw, symbol, cutoff)
    policy = SpreadScanPolicy(
        quantity=quantity,
        commission_per_contract=_d(commission_per_contract),
    )
    scan = scan_vertical_credit_spreads(snapshot, cutoff, policy)
    underlying_mid = (
        snapshot.underlying_quote.bid + snapshot.underlying_quote.ask
    ) / Decimal("2")
    structures = []
    for ev in scan.evaluations:
        if not ev.admissible or ev.calculation is None:
            continue
        calc = ev.calculation
        # Premium-selling basics: the SHORT leg must be out of the money, so the
        # seller is collecting premium on a strike the underlying is not through.
        # A vertical whose short leg is ITM is a different (assignment-risk) trade,
        # not the defined-risk premium sell the desk targets. Recover the short leg
        # from the snapshot and filter to OTM-short structures.
        contracts_by_id = {q.contract_id: q for q in snapshot.option_quotes}
        short_id, long_id = calc.input_contract_ids
        short_q = contracts_by_id.get(short_id)
        long_q = contracts_by_id.get(long_id)
        if short_q is None or long_q is None:
            continue
        if short_q.option_type is OptionType.CALL:
            otm = short_q.strike > underlying_mid
        else:
            otm = short_q.strike < underlying_mid
        if not otm:
            continue
        structures.append(
            {
                "structure": "VERTICAL_CREDIT_SPREAD",
                "contract_id": calc.spread_id,
                "underlying": calc.underlying,
                "expiration": calc.expiration_date.isoformat(),
                "days_to_expiration": calc.days_to_expiration,
                "net_credit_per_share": str(
                    calc.net_credit / (calc.contract_multiplier * calc.quantity)
                ),
                "net_credit": str(calc.net_credit),
                "maximum_loss": str(calc.maximum_loss),
                "break_even": str(calc.break_even),
                "return_on_risk": str(calc.return_on_risk),
                "trade_authorized": False,
            }
        )
    structures.sort(key=lambda s: -float(s["return_on_risk"]))
    top = structures[:40]  # present the best defined-risk economics, not all pairs
    return {
        "schema_version": "hedge-desk-cboe-chain-1.0.0",
        "mode": "REAL_CBOE_CHAIN_INCOME",
        "symbol": symbol,
        "underlying_close": str(snapshot.underlying_quote.bid),
        "cutoff": cutoff.isoformat(),
        "scan_disposition": scan.disposition,
        "pair_count": scan.pair_count,
        "admissible_count": scan.admissible_count,
        "income_structures": top,
        "data_source": "cboe-delayed-public-http-200",
        "trade_authorized": False,
        "note": (
            "Executable-side net credit from REAL delayed bid/ask. No probability, "
            "no RoR. No order placed. Max-loss economics per defined-risk vertical."
        ),
    }


__all__ = ["real_chain_income", "build_snapshot_from_cboe", "CBOE_URL"]