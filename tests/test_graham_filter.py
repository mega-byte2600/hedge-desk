"""Deterministic tests for the Graham Filter engine.

Every verdict branch, every fail-closed path, the adapter boundary, and the
UI contract. Same inputs -> same verdict, every run.

Run:  python3 tests/test_engine.py
"""

import math
from hedge_desk.graham_filter.engine import (
    Assessment, Candidate, Standards, assess, assess_all, market_regime,
    PROTOTYPE_STANDARDS,
)
from hedge_desk.graham_filter.adapter import adapt, adapt_assess
from hedge_desk.graham_filter.contract import (
    DEFAULT_FILTER, FILTER_MODES, VERDICTS,
    apply_filter, to_batch, to_dict,
)

# Explicit standards — every threshold stated, nothing defaulted.
STD = Standards(
    margin_strong=5.0,
    margin_adequate=2.0,
    margin_thin=0.5,
    manic_vix=30.0,
    complacent_vix=14.0,
    manic_margin_bump=2.0,
    default_hurdle=15.0,
    per_symbol_hurdles={},
    label="test",
)


def good_candidate(**kw):
    base = dict(
        symbol="SPY", spot=600.0, strike=570.0, premium=6.0, dte=30,
        timestamp="2026-10-04T12:00:00Z", source="test",
    )
    base.update(kw)
    return Candidate(**base)


def good_payload(**kw):
    base = dict(
        symbol="SPY", spot=600.0, strike=570.0, premium=6.0, dte=30,
        timestamp="2026-10-04T12:00:00Z", source="Yahoo Finance",
    )
    base.update(kw)
    return base


passed = failed = 0

def check(name, cond):
    global passed, failed
    if cond:
        passed += 1
        print("PASS " + name)
    else:
        failed += 1
        print("FAIL " + name)


def check_raises(name, fn, exc=ValueError):
    try:
        fn()
    except exc:
        check(name, True)
    except Exception:
        check(name, False)
    else:
        check(name, False)


# --- Verdict branches -------------------------------------------------------

# INVESTMENT: margin adequate+, return clears, own-it yes
a = assess(good_candidate(), vix=16.0, own_it=True, std=STD, hurdle_override=10.0)
check("investment verdict", a.verdict == "INVESTMENT")
# margin: price cushion (600-570)/600=5% + premium 6/570=1.05% -> STRONG
check("margin strong", a.margin_rating == "STRONG")
# return: 6/570*100 * 365/30 = 12.8% >= 10 hurdle
check("clears hurdle", a.clears_hurdle is True)

# SPECULATION via own-it No (even with great numbers)
a = assess(good_candidate(), vix=16.0, own_it=False, std=STD, hurdle_override=10.0)
check("speculation via own-it no", a.verdict == "SPECULATION" and "Own-it" in a.reason)

# SPECULATION via margin NONE (deep ITM put, no cushion)
a = assess(good_candidate(spot=500.0, strike=570.0, premium=75.0),
           vix=16.0, own_it=True, std=STD, hurdle_override=10.0)
# price cushion (500-570)/500 = -14%, premium 75/570 = 13.16% -> total -0.84% -> NONE
check("margin none", a.margin_rating == "NONE")
check("speculation via margin none", a.verdict == "SPECULATION")

# NEEDS-YOU via own-it unanswered
a = assess(good_candidate(), vix=16.0, own_it=None, std=STD, hurdle_override=10.0)
check("needs-you via own-it unset", a.verdict == "NEEDS-YOU")

# NEEDS-YOU via inadequate return (NOT speculation — deliberate distinction)
a = assess(good_candidate(), vix=16.0, own_it=True, std=STD, hurdle_override=50.0)
check("needs-you via inadequate return", a.verdict == "NEEDS-YOU")
check("inadequate return wording", "Inadequate return" in a.reason)
check("not labeled speculation", a.verdict != "SPECULATION")

# missing symbol is data unavailable
a = assess(good_candidate(symbol=None), vix=16.0, own_it=True, std=STD)
check("data unavailable: symbol=None",
      a.verdict == "DATA-UNAVAILABLE" and "symbol" in a.reason)

# --- Fail closed: data unavailable ------------------------------------------

for field, bad in [
    ("spot", None), ("strike", None), ("premium", None),
    ("dte", None), ("timestamp", None), ("source", None),
    ("spot", 0), ("strike", -5), ("dte", 0), ("premium", -1.0),
    ("timestamp", ""), ("source", ""),
]:
    kw = {field: bad}
    a = assess(good_candidate(**kw), vix=16.0, own_it=True, std=STD)
    check(f"data unavailable: {field}={bad!r}",
          a.verdict == "DATA-UNAVAILABLE" and "data unavailable" in a.reason)

# --- Missing configuration fails fast (never silently defaulted) -----------

check_raises("assess without standards raises",
             lambda: assess(good_candidate(), vix=16.0, own_it=True))
check_raises("market_regime without standards raises",
             lambda: market_regime(16.0))
check_raises("assess_all without standards raises",
             lambda: assess_all([good_candidate()], 16.0, {}, None))
check("prototype standards labeled unapproved",
      PROTOTYPE_STANDARDS.label == "PROTOTYPE — UNAPPROVED")
check("prototype carries invented per-symbol hurdles",
      PROTOTYPE_STANDARDS.per_symbol_hurdles.get("TSLA") == 25)

# --- Mr. Market: VIX bump ----------------------------------------------------

# Candidate with thin margin that passes at VIX 16...
thin = good_candidate(spot=580.0, strike=570.0, premium=2.0)  # ~1.72+0.35 = 2.07% ADEQUATE
a_calm = assess(thin, vix=16.0, own_it=True, std=STD, hurdle_override=1.0)
check("adequate when calm", a_calm.margin_rating == "ADEQUATE")
# ...but the MANIC bump (+2%) pushes the bar above it -> THIN, still not NONE
a_manic = assess(thin, vix=35.0, own_it=True, std=STD, hurdle_override=1.0)
check("manic regime detected", a_manic.regime == "MANIC")
check("manic bump applied", a_manic.margin_bar_pct == 2.0)
check("manic lowers rating", a_manic.margin_rating == "THIN")

# Regime boundaries
check("regime manic", market_regime(30.1, STD) == "MANIC")
check("regime normal high", market_regime(30.0, STD) == "NORMAL")
check("regime complacent", market_regime(13.9, STD) == "COMPLACENT")
check("regime normal low", market_regime(14.0, STD) == "NORMAL")

# --- Batch + filter ----------------------------------------------------------

cands = [good_candidate(symbol="A"), good_candidate(symbol="B")]
answers = {"A": True, "B": False}
res = assess_all(cands, vix=16.0, own_it_answers=answers, std=STD,
                 hurdle_override=10.0, filter_speculation=True)
check("filter drops speculation", len(res) == 1 and res[0].symbol == "A")
res = assess_all(cands, vix=16.0, own_it_answers=answers, std=STD,
                 hurdle_override=10.0, filter_speculation=False)
check("filter off keeps all", len(res) == 2)

# --- Determinism --------------------------------------------------------------

a1 = assess(good_candidate(), vix=16.0, own_it=True, std=STD, hurdle_override=10.0)
a2 = assess(good_candidate(), vix=16.0, own_it=True, std=STD, hurdle_override=10.0)
check("deterministic", a1 == a2)

# --- Adapter ------------------------------------------------------------------

c = adapt(good_payload())
check("adapter builds candidate",
      c.symbol == "SPY" and c.spot == 600.0 and c.dte == 30)

c = adapt(good_payload(extra_key="ignored", bid=1.0, iv=0.4))
check("adapter ignores extras", c.symbol == "SPY" and c.spot == 600.0)

for label, payload in [
    ("non-dict", [1, 2, 3]),
    ("none", None),
    ("empty", {}),
    ("bool numeric", good_payload(spot=True)),
    ("nan", good_payload(premium=float("nan"))),
    ("inf", good_payload(strike=float("inf"))),
    ("blank strings", good_payload(timestamp="   ", source="")),
    ("wrong types", good_payload(dte="30", spot="600")),
]:
    a = adapt_assess(payload, vix=16.0, own_it=True, std=STD)
    check(f"adapter fail-closed: {label}",
          a.verdict == "DATA-UNAVAILABLE" and "data unavailable" in a.reason)

a = adapt_assess(good_payload(), vix=16.0, own_it=True, std=STD,
                 hurdle_override=10.0)
check("adapter end-to-end investment", a.verdict == "INVESTMENT")

for label, vix in [("missing vix", None), ("zero vix", 0), ("neg vix", -3),
                   ("nan vix", float("nan")), ("str vix", "16")]:
    a = adapt_assess(good_payload(), vix=vix, own_it=True, std=STD)
    check(f"adapter fail-closed: {label}",
          a.verdict == "DATA-UNAVAILABLE" and "vix" in a.reason)

a = adapt_assess(good_payload(), vix=16.0, own_it="yes", std=STD,
                 hurdle_override=10.0)
check("adapter coerces bad own_it to unanswered",
      a.verdict == "NEEDS-YOU" and a.own_it is None)

check_raises("adapt_assess without standards raises",
             lambda: adapt_assess(good_payload(), vix=16.0, own_it=True))

# --- Contract -------------------------------------------------------------------

a = assess(good_candidate(), vix=16.0, own_it=True, std=STD, hurdle_override=10.0)
row = to_dict(a, standards_label=STD.label, standards_approved=False)
check("contract verdict literal", row["verdict"] in VERDICTS)
check("contract margin block",
      row["margin"]["rating"] == "STRONG" and row["margin"]["breakeven"] == 564.0)
check("contract return block",
      row["return"]["clears_hurdle"] is True and row["return"]["hurdle_pct"] == 10.0)
check("contract standards provenance",
      row["standards"] == {"label": "test", "approved": False})
check("contract assessed_at present", bool(row["assessed_at"]))
check("contract data_unavailable_fields empty", row["data_unavailable_fields"] == [])

a = assess(good_candidate(premium=None), vix=16.0, own_it=True, std=STD)
row = to_dict(a, standards_label=STD.label, standards_approved=False)
check("contract null blocks when unavailable",
      row["margin"] is None and row["return"] is None)
check("contract lists missing fields", row["data_unavailable_fields"] == ["premium"])
check("contract reason literal", "data unavailable" in row["reason"])

rows = [
    {"verdict": "INVESTMENT"}, {"verdict": "SPECULATION"},
    {"verdict": "NEEDS-YOU"}, {"verdict": "DATA-UNAVAILABLE"},
]
check("filter on hides only speculation",
      [r["verdict"] for r in apply_filter(rows, "hide_speculation")] ==
      ["INVESTMENT", "NEEDS-YOU", "DATA-UNAVAILABLE"])
check("filter off keeps all", len(apply_filter(rows, "all")) == 4)
check("default filter is hide_speculation", DEFAULT_FILTER == "hide_speculation")
check_raises("bad filter mode raises",
             lambda: apply_filter(rows, "bogus"))

a1 = assess(good_candidate(), vix=16.0, own_it=True, std=STD, hurdle_override=10.0)
a2 = assess(good_candidate(), vix=16.0, own_it=False, std=STD, hurdle_override=10.0)
batch = to_batch([a1, a2], standards_label="test", standards_approved=False)
check("batch shape",
      batch["filter"] == "hide_speculation" and batch["count"] == 1
      and len(batch["rows"]) == 1)

print(f"\n{passed} passed, {failed} failed.")
if failed:
    raise SystemExit(1)
print("All Graham Filter engine tests passed.")
