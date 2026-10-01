"""Weekly options-seed refresh (run by .github/workflows/options-seed.yml).

Fetches the real Cboe delayed SPY chain, selects the ~30-DTE put seed, and
writes derived analytics to artifacts/options-seed-latest.json. The workflow
force-adds that file (artifacts/ is gitignored; tracked generated files use
git add -f, same as am-report-latest.json).

Compliance, in order:
  * only derived analytics are ever written — the raw 5.9MB chain payload is
    parsed in memory and discarded, never committed;
  * on fetch/select failure the last-good file is preserved: only its
    ``refresh`` block is updated to fetch_failed with the reason, and every
    contract field stays byte-identical (never synthetic);
  * if no last-good file exists there is nothing honest to serve: write
    nothing and exit 1 so the workflow fails closed. The endpoint then 404s
    with artifact_missing instead of inventing data.

Exit codes: 0 = seed refreshed or last-good preserved; 1 = no data at all.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from hedge_desk import cboe_chain
from hedge_desk.options_seed import SEED_SCHEMA_VERSION, seed_to_dict, select_seed_put

SYMBOL = "SPY"
REPO_ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = REPO_ROOT / "artifacts" / "options-seed-latest.json"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _read_last_good() -> Dict[str, Any] | None:
    try:
        return json.loads(SEED_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _mark_failed(last_good: Dict[str, Any], reason: str) -> None:
    last_good["refresh"] = {
        "status": "fetch_failed",
        "refreshed_at": _now().isoformat(),
        "reason": reason,
        "previous_as_of": last_good.get("as_of"),
    }
    SEED_PATH.write_text(json.dumps(last_good, indent=2) + "\n", encoding="utf-8")


def refresh(transport: cboe_chain.Transport | None = None) -> int:
    now = _now()
    fetch = transport or cboe_chain._default_transport
    try:
        status, raw = fetch(cboe_chain.CBOE_URL.format(symbol=SYMBOL))
        if status != 200 or not raw:
            raise ValueError(f"cboe fetch failed (status {status})")
        seed = select_seed_put(raw, SYMBOL, now)
        payload_top = json.loads(raw.decode("utf-8"))["data"]
    except Exception as exc:  # noqa: BLE001 - failure path must never raise
        reason = f"{type(exc).__name__}: {exc}"
        last_good = _read_last_good()
        if last_good is None:
            print(f"options-seed: no data and no last-good file: {reason}", file=sys.stderr)
            return 1
        _mark_failed(last_good, reason)
        print(f"options-seed: fetch failed, last-good preserved: {reason}")
        return 0
    payload = seed_to_dict(
        seed,
        SYMBOL,
        payload_top,
        now,
        {"status": "ok", "refreshed_at": now.isoformat(), "reason": None},
    )
    assert payload["schema_version"] == SEED_SCHEMA_VERSION
    SEED_PATH.parent.mkdir(parents=True, exist_ok=True)
    SEED_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"options-seed: refreshed {payload['contract_id']} "
        f"dte={payload['days_to_expiration']} as_of={payload['as_of']}"
    )
    return 0


def main() -> None:
    sys.exit(refresh())


if __name__ == "__main__":
    main()
