"""Automated scorecard against docs/SCORING_RUBRIC.md (VERIFIED items only).

Every machine-checkable rubric item runs in seconds so each change is
measured immediately. VALIDATED (GP expectations) stays a human judgement.

    python scripts/scorecard.py [--full]   # --full also runs the whole test suite (~3 min)
Exit 0 when every check passes.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable


def _run(cmd):
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def _read(rel):
    p = ROOT / rel
    return p.read_text() if p.exists() else ""


def checks(full: bool) -> list[dict]:
    out = []

    def add(dim, item, ok, detail=""):
        out.append({"dimension": dim, "item": item, "pass": bool(ok), "detail": detail})

    rc, txt = _run(["ruff", "check", "hedge_desk", "tests", "scripts", "-q"])
    add("Code quality", "ruff gating set clean (E9,F,B,FA102)", rc == 0, txt.strip()[:100])
    ci = _read(".github/workflows/ci.yml")
    add("Code quality", "CI runs pytest + ruff + 3.9/3.11/3.13", "pytest" in ci and "ruff check" in ci
        and all(v in ci for v in ('"3.9"', '"3.11"', '"3.13"')))
    tests = ["tests/test_premium_score.py", "tests/test_win_probability.py", "tests/test_desk_call.py",
             "tests/test_feed_retries.py", "tests/test_console_last_good.py"]
    cmd = [PY, "-m", "pytest", "-q", "-o", "addopts="] + ([] if full else tests)
    rc, txt = _run(cmd)
    m = re.search(r"(\d+) passed", txt)
    add("Code quality", "tests pass" + (" (full suite)" if full else " (core subset)"),
        rc == 0, f"{m.group(1) if m else 0} passed")

    add("API & data health", "Cboe + EOD fetch through with_retries",
        "_default_transport = with_retries(" in _read("hedge_desk/cboe_chain.py")
        and "_default_transport = with_retries(" in _read("hedge_desk/data/eod_ingest.py"))
    srv = _read("hedge_desk/server.py")
    add("API & data health", "stale-labelled last-good report (no synthetic)", "load_last_good_console" in srv
        and '"status": "STALE"' in srv)
    add("API & data health", "options-seed freshness vs SLA", "options_seed_freshness" in srv)
    add("API & data health", "prices quantized at ingest", "def _px(" in _read("hedge_desk/data/eod_ingest.py"))

    demo = _read("artifacts/am-demo.html")
    add("UI/UX", "vendored plotly first (offline)", "/vendor/plotly-2.35.2.min.js" in demo
        and (ROOT / "web/vendor/plotly-2.35.2.min.js").exists())
    add("UI/UX", "desk call header above fold", 0 <= demo.find("class='deskcall") < demo.find("class='ts'"))
    add("UI/UX", "premium panel shows real scored rows + eligibility + wheel",
        "meet the GP bands" in demo and "Why / warnings" in demo and "GP wheel" in demo
        and "next nightly run" not in demo)

    ps = _read("hedge_desk/premium_score.py")
    add("Insight", "premium score: 4 sourced components", all(k in ps for k in (
        "Carr & Wu", "vol_edge", "entry_window", "strike_placement", "time_value")))
    wp = _read("hedge_desk/risk/win_probability.py")
    add("Rigor", "exact BSM N(d2) w/ r,q (model 2.0.0)", 'MODEL_VERSION = "2.0.0"' in wp and "dividend_yield" in wp)
    add("Rigor", "Hull reference cases", "Example 17.1" in _read("tests/test_win_probability.py"))
    add("Rigor", "delta consistent with r,q", "dividend_yield" in ps and "rate - dividend_yield" in ps)
    # Behaviour, not strings: run the tests that pin the GP brief's hard rules.
    rc, txt = _run([PY, "-m", "pytest", "-q", "-o", "addopts=",
                    "tests/test_premium_score.py::test_out_of_band_or_no_edge_can_never_rank_first",
                    "tests/test_premium_score.py::test_time_value_is_return_on_collateral",
                    "tests/test_premium_score.py::test_missing_rv_is_flagged_not_invented_and_ranking_is_by_score",
                    "tests/test_desk_call.py::test_shortlist_dedupes_short_leg_ranks_eligible_first_and_sizes_under_2pct"])
    add("Rigor", "behaviour: brief bands enforced, RoC, no unearned credit, 2% sizing", rc == 0, txt.strip()[-80:])
    dc = _read("hedge_desk/desk_call.py")
    add("Actionability", "desk call: action, shortlist, invalidation, exits",
        all(k in dc for k in ("NO_TRADE", "invalidation_underlying_through", "take_profit_at_credit_captured",
                              "stop_at_loss", "premium_score")))
    add("Actionability", "21-DTE time exit per candidate", "time_exit_dte" in ps)
    return out


def main() -> int:
    rows = checks("--full" in sys.argv)
    if "--json" in sys.argv:
        print(json.dumps(rows, indent=1))
    else:
        dims: dict = {}
        for r in rows:
            dims.setdefault(r["dimension"], []).append(r)
        print("| Dimension | VERIFIED checks passing | Failing |\n|---|---|---|")
        for d, rs in dims.items():
            bad = [r["item"] + (f" ({r['detail']})" if r["detail"] else "") for r in rs if not r["pass"]]
            print(f"| {d} | {sum(r['pass'] for r in rs)}/{len(rs)} | {'; '.join(bad) or '—'} |")
    return 0 if all(r["pass"] for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
