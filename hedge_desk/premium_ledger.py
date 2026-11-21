"""Paper Outcome Ledger for the premium-selling score (GP brief 2026-11-20).

Closes the loop: every eligible Desk-call candidate is recorded once, on the
night it first appears, in an append-only JSONL ledger. When the structure
expires, it is settled from the underlying's REAL closing price on the
expiration date (hold-to-expiry, the simplest honest rule; no mid-life quotes
are assumed). The summary answers the one question that matters for the
score's weights: do higher-scored structures actually do better?

Rules (SOUL / AGENTS / CarpeDATA):
* Paper only. Nothing here is an order or a performance claim; every row
  carries ``trade_authorized: False`` and ``basis: PAPER_HOLD_TO_EXPIRY``.
* Real data only: entries come from the nightly's real Cboe-derived
  structures; settlement uses real EOD closes already fetched by the nightly.
  No new API calls. A missing close leaves the entry OPEN (never guessed).
* Money in ``Decimal``. Deterministic: callers pass the date; no wall clock.
* Append-only: a settled outcome is a NEW line referencing the entry id;
  existing lines are never rewritten.

P&L at expiry (per contract set, USD):
    net_credit (already after opening commissions, executable bid/ask)
  - min(width, max(0, value of the short leg minus value of the long leg)) x 100 x qty
  - closing commissions (2 legs) only if the spread finished in the money
"""
from __future__ import annotations

import json
from datetime import date
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

SCHEMA_VERSION = "hedge-desk-premium-ledger-1.0.0"
BASIS = "PAPER_HOLD_TO_EXPIRY"
MULTIPLIER = Decimal(100)
COMMISSION_PER_CONTRACT = Decimal("0.65")
CENT = Decimal("0.01")


def _d(x: Any) -> Decimal:
    return Decimal(str(x))


def _parse_leg(occ: str) -> Dict[str, Any]:
    s = occ.strip().upper()
    return {"type": s[-9], "strike": Decimal(int(s[-8:])) / Decimal(1000), "expiry": "20" + s[-15:-9]}


def entry_id(contract_id: str) -> str:
    return f"{contract_id}"


def read_ledger(path: Path | str) -> List[Dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return []
    rows = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def _append(path: Path | str, rows: Iterable[Mapping[str, Any]]) -> int:
    rows = list(rows)
    if not rows:
        return 0
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    return len(rows)


def new_entries(eligible: Iterable[Mapping[str, Any]], existing: List[Mapping[str, Any]],
                as_of: date, context: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """Entry rows for eligible structures not already in the ledger."""
    seen = {r["entry_id"] for r in existing if r.get("kind") == "ENTRY"}
    out = []
    for s in eligible:
        p = s.get("premium") or {}
        if not p.get("eligible"):
            continue
        eid = entry_id(s["contract_id"])
        if eid in seen:
            continue
        seen.add(eid)
        short_id, long_id = s["contract_id"].split("--")
        short, long_ = _parse_leg(short_id), _parse_leg(long_id)
        out.append({
            "kind": "ENTRY", "schema_version": SCHEMA_VERSION, "basis": BASIS,
            "entry_id": eid, "entry_date": as_of.isoformat(),
            "underlying": s.get("underlying", "SPY"), "contract_id": s["contract_id"],
            "option_type": short["type"], "short_strike": str(short["strike"]), "long_strike": str(long_["strike"]),
            "expiration": s.get("expiration") or f"{short['expiry'][:4]}-{short['expiry'][4:6]}-{short['expiry'][6:8]}",
            "days_to_expiration": s.get("days_to_expiration"),
            "net_credit": str(_d(s["net_credit"])), "maximum_loss": str(_d(s["maximum_loss"])),
            "spread_width": str(_d(s.get("spread_width") or abs(short["strike"] - long_["strike"]))),
            "quantity": 1,
            "premium_score": p.get("premium_score"), "components": p.get("components"),
            "inputs": {k: (p.get("inputs") or {}).get(k) for k in (
                "short_leg_abs_delta", "variance_risk_premium", "return_on_collateral_30d",
                "realized_vol_21d_annual", "vol_edge_benchmark_iv")},
            "context": dict(context), "trade_authorized": False,
        })
    return out


def settle(entry: Mapping[str, Any], close_on_expiry: Decimal) -> Dict[str, Any]:
    """Outcome row for one entry given the underlying's close on expiration."""
    k_s, k_l = _d(entry["short_strike"]), _d(entry["long_strike"])
    width, qty = _d(entry["spread_width"]), Decimal(entry.get("quantity", 1))
    if entry["option_type"] == "P":
        intrinsic = max(Decimal(0), k_s - close_on_expiry) - max(Decimal(0), k_l - close_on_expiry)
    else:
        intrinsic = max(Decimal(0), close_on_expiry - k_s) - max(Decimal(0), close_on_expiry - k_l)
    intrinsic = min(width, max(Decimal(0), intrinsic))
    settle_cost = intrinsic * MULTIPLIER * qty
    closing_commission = COMMISSION_PER_CONTRACT * 2 * qty if intrinsic > 0 else Decimal(0)
    pnl = (_d(entry["net_credit"]) - settle_cost - closing_commission).quantize(CENT, ROUND_HALF_EVEN)
    collateral = _d(entry["net_credit"]) + _d(entry["maximum_loss"])
    return {
        "kind": "OUTCOME", "schema_version": SCHEMA_VERSION, "basis": BASIS,
        "entry_id": entry["entry_id"], "settled_on": entry["expiration"],
        "underlying_close": str(close_on_expiry), "expired_worthless": intrinsic == 0,
        "pnl_usd": str(pnl),
        "return_on_collateral": str((pnl / collateral).quantize(Decimal("0.0001"), ROUND_HALF_EVEN))
        if collateral > 0 else None,
        "premium_score": entry.get("premium_score"), "trade_authorized": False,
    }


def due_outcomes(rows: List[Mapping[str, Any]], closes: Mapping[str, Any], today: date) -> List[Dict[str, Any]]:
    """Outcome rows for every OPEN entry whose expiration has a real close.
    An entry stays OPEN when the expiry close is not available (never guessed)."""
    settled = {r["entry_id"] for r in rows if r.get("kind") == "OUTCOME"}
    out = []
    for r in rows:
        if r.get("kind") != "ENTRY" or r["entry_id"] in settled:
            continue
        exp = r["expiration"]
        if date.fromisoformat(exp) > today:
            continue
        c = closes.get(exp)
        if c is None:
            continue
        out.append(settle(r, _d(c)))
    return out


def summarize(rows: List[Mapping[str, Any]]) -> Dict[str, Any]:
    """Track record by score band: the calibration signal for the weights."""
    entries = {r["entry_id"]: r for r in rows if r.get("kind") == "ENTRY"}
    outcomes = [r for r in rows if r.get("kind") == "OUTCOME"]
    bands = {"score >= 70": lambda s: s >= 70, "55-70": lambda s: 55 <= s < 70, "< 55": lambda s: s < 55}

    def stats(items):
        if not items:
            return {"n": 0, "win_rate": None, "avg_pnl_usd": None, "avg_return_on_collateral": None}
        pnl = [_d(o["pnl_usd"]) for o in items]
        roc = [_d(o["return_on_collateral"]) for o in items if o.get("return_on_collateral") is not None]
        return {"n": len(items),
                "win_rate": str((Decimal(sum(1 for p in pnl if p > 0)) / len(pnl)).quantize(Decimal("0.001"))),
                "avg_pnl_usd": str((sum(pnl) / len(pnl)).quantize(CENT)),
                "avg_return_on_collateral": str((sum(roc) / len(roc)).quantize(Decimal("0.0001"))) if roc else None}

    by_band = {name: stats([o for o in outcomes if o.get("premium_score") is not None and f(float(o["premium_score"]))])
               for name, f in bands.items()}
    return {"schema_version": SCHEMA_VERSION, "basis": BASIS,
            "entries": len(entries), "open": len(entries) - len(outcomes), "settled": len(outcomes),
            "overall": stats(outcomes), "by_score_band": by_band,
            "note": ("Paper, hold-to-expiry outcomes of eligible premium-score candidates, settled on the "
                     "underlying's real expiry close. Not performance, not advice, not an order. "
                     "Sample sizes are small until several expirations have passed."),
            "trade_authorized": False}


def update_ledger(path: Path | str, eligible: Iterable[Mapping[str, Any]], closes: Mapping[str, Any],
                  as_of: date, context: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
    """Nightly step: append new entries and due outcomes; return the summary."""
    rows = read_ledger(path)
    entries = new_entries(eligible, rows, as_of, context or {})
    added = _append(path, entries)
    rows = read_ledger(path)
    outcomes = due_outcomes(rows, closes, as_of)
    settled = _append(path, outcomes)
    summary = summarize(read_ledger(path))
    summary.update({"entries_added_tonight": added, "outcomes_settled_tonight": settled,
                    # Tonight's appended rows ride inside the dated nightly report,
                    # which the batch commit always includes. The full ledger can
                    # be rebuilt from committed reports (rebuild_from_reports) even
                    # if the .jsonl itself is never committed.
                    "appended_rows": entries + outcomes})
    return summary


def rebuild_from_reports(report_paths: Iterable[Path | str]) -> List[Dict[str, Any]]:
    """Reconstruct the ledger from committed dated reports (oldest first),
    de-duplicating by (kind, entry_id)."""
    seen, rows = set(), []
    for rp in sorted(Path(x) for x in report_paths):
        try:
            led = json.loads(Path(rp).read_text(encoding="utf-8")).get("premium_ledger") or {}
        except (OSError, ValueError):
            continue
        for r in led.get("appended_rows") or []:
            key = (r.get("kind"), r.get("entry_id"))
            if key not in seen:
                seen.add(key)
                rows.append(r)
    return rows


LINK_WINDOW_DAYS = 3


def link_yellow_sheets(sheets: Iterable[Mapping[str, Any]], rows: List[Mapping[str, Any]]) -> Dict[str, Any]:
    """Connect GP Yellow Sheets (decision documents) to ledger outcomes.

    Read-only: Yellow Sheets are hashed, append-only decision records and are
    never modified. A CREDIT_SPREAD sheet links to the ledger entry with the
    same underlying and short strike, entered within LINK_WINDOW_DAYS of the
    sheet; when the sheet records a DTE, the entry's expiration must also be
    within LINK_WINDOW_DAYS of (recorded date + DTE). Ambiguity is reported,
    never resolved by guessing.
    """
    from datetime import timedelta
    entries = [r for r in rows if r.get("kind") == "ENTRY"]
    outcomes = {r["entry_id"]: r for r in rows if r.get("kind") == "OUTCOME"}
    linked = []
    for sh in sheets:
        if sh.get("strategy") != "CREDIT_SPREAD" or sh.get("strike") is None:
            continue
        try:
            rec = date.fromisoformat(str(sh.get("recorded_at"))[:10])
            strike = _d(sh["strike"])
        except (ValueError, TypeError, ArithmeticError):
            continue
        matches = []
        for e in entries:
            if e.get("underlying", "").upper() != str(sh.get("symbol", "")).upper():
                continue
            if _d(e["short_strike"]) != strike:
                continue
            if abs((date.fromisoformat(e["entry_date"]) - rec).days) > LINK_WINDOW_DAYS:
                continue
            if sh.get("dte") is not None:
                want = rec + timedelta(days=int(sh["dte"]))
                if abs((date.fromisoformat(e["expiration"]) - want).days) > LINK_WINDOW_DAYS:
                    continue
            matches.append(e)
        row = {"yellow_sheet_seq": sh.get("seq"), "yellow_sheet_sha256": sh.get("entry_sha256"),
               "symbol": sh.get("symbol"), "strike": str(strike), "decision": sh.get("decision"),
               "thesis": sh.get("thesis"), "invalidation": sh.get("invalidation")}
        if len(matches) != 1:
            row.update({"link": "AMBIGUOUS" if matches else "NO_LEDGER_MATCH",
                        "candidates": [m["entry_id"] for m in matches]})
        else:
            e = matches[0]
            o = outcomes.get(e["entry_id"])
            row.update({"link": "LINKED", "entry_id": e["entry_id"], "premium_score": e.get("premium_score"),
                        "status": "SETTLED" if o else "OPEN"})
            if o:
                row.update({"pnl_usd": o["pnl_usd"], "return_on_collateral": o.get("return_on_collateral"),
                            "expired_worthless": o.get("expired_worthless"),
                            "thesis_held": _d(o["pnl_usd"]) > 0})
        linked.append(row)
    settled = [r for r in linked if r.get("status") == "SETTLED"]
    return {"schema_version": SCHEMA_VERSION, "basis": BASIS,
            "sheets_considered": len(linked),
            "linked": sum(1 for r in linked if r["link"] == "LINKED"),
            "settled": len(settled),
            "thesis_held": sum(1 for r in settled if r.get("thesis_held")),
            "rows": linked,
            "note": ("Yellow Sheets (GP decisions) joined read-only to paper hold-to-expiry outcomes. "
                     "Not performance, not advice."),
            "trade_authorized": False}


__all__ = ["update_ledger", "rebuild_from_reports", "link_yellow_sheets", "summarize", "settle", "due_outcomes", "new_entries", "read_ledger",
           "SCHEMA_VERSION", "BASIS"]
