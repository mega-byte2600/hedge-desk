"""Drive the full paper lifecycle end-to-end to prove the machinery works.

plan -> human approve -> open (fill-check) -> monitor -> human close -> settle.
Uses the frozen reference fixture (TEST symbol, $100k account) exactly as the
test suite does, so this is deterministic and paper-only. No real money.
"""
import json
import tempfile
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from hedge_desk.demo import build_reference_plan, build_reference_option_snapshot
from hedge_desk.paper import (
    approve_paper_trade,
    create_paper_trade_plan,
    write_plan_file,
)
from hedge_desk.paper.runner import (
    advance_paper_lifecycle,
    close_paper_position,
    _load_state,
)
from hedge_desk.paper.settler import settle_paper_outcomes

FIXTURE_AS_OF = datetime(2026, 7, 28, 20, 0, tzinfo=timezone.utc)
TICK = FIXTURE_AS_OF + timedelta(seconds=60)
DECIDED = FIXTURE_AS_OF + timedelta(minutes=1)
CLOSED = FIXTURE_AS_OF + timedelta(minutes=2)

tmp = tempfile.TemporaryDirectory()
plans_dir = Path(tmp.name) / "plans"; plans_dir.mkdir()
state_path = Path(tmp.name) / "state.json"

# 1. Build + approve the plan
base = build_reference_plan()
plan = create_paper_trade_plan(
    "paper-demo-001", base.spread, base.risk_decision, base.compliance_decision,
    base.created_at, base.approval_expires_at,
    event_calendar_gate=base.event_calendar_gate,
)
plan = approve_paper_trade(plan, "gp", DECIDED)
write_plan_file(plan, plans_dir / f"{plan.plan_id}.json")
print("1. PLAN built + human-approved:", plan.plan_id, "| spread:", plan.spread.spread_id)

# 2. Tick with ready quotes -> opens
def ready_quotes(p): return (p.spread.quantity, p.spread.net_credit)
def monitor_lifecycle(p): return {
    "short_leg_in_the_money": False, "ex_dividend_before_expiration": False,
    "assignment_notice_received": False, "contract_adjustment_pending": False,
    "settlement_terms_confirmed": True,
}
r1 = advance_paper_lifecycle(plans_dir, state_path, ready_quotes, TICK)
print("2. TICK (fill ready) -> opened:", r1["opened"], "| pending:", r1["still_pending"])

# 3. Monitor tick -> stays open
r2 = advance_paper_lifecycle(plans_dir, state_path, ready_quotes, TICK + timedelta(minutes=15),
                             lifecycle_provider=monitor_lifecycle)
print("3. TICK (monitor) -> monitoring:", r2["monitoring"], "| escalated:", r2["escalated"])

# 4. Human close
snap = build_reference_option_snapshot()
q = {q.contract_id: q for q in snap.option_quotes}
short_q = q["TEST260821P00095000"]; long_q = q["TEST260821P00090000"]
r3 = close_paper_position(plans_dir, state_path, plan.plan_id, "gp", CLOSED,
                          ("PLANNED_EXIT_REACHED",), short_q, long_q, Decimal("0.65"))
print("4. CLOSE -> realized_pnl:", r3.get("realized_pnl"), "| close_sha256:", r3.get("close_sha256","")[:16])

# 5. Settle into the paper outcome log
log_path = Path(tmp.name) / "paper-outcomes.jsonl"
r4 = settle_paper_outcomes(Path(tmp.name), log_path, now=CLOSED + timedelta(minutes=1))
print("5. SETTLE ->", json.dumps(r4, default=str)[:300])

# 6. Show the paper outcome log
print("6. PAPER OUTCOME LOG:")
for line in log_path.read_text().splitlines():
    print("   ", line[:200])
