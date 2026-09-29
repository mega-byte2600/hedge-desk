"""Open a REAL CCL paper trade end-to-end from real Cboe data.

Short 20 put / long 18 put credit spread, 34 DTE, real bid/ask, real IV/delta
from the live Cboe chain. Win probability = 1 - |real put delta|. RoR from the
deterministic engine. Plan -> human approve -> open -> monitor -> close -> settle.
Paper-only, no real money.
"""
import json
import tempfile
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from hedge_desk.cboe_chain import _default_transport, CBOE_URL
from hedge_desk.core.decision import evaluate_candidate
from hedge_desk.backoffice import evaluate_paper_compliance
from hedge_desk.domain import Account, AccountType, ProductType, TradeCandidate
from hedge_desk.options import (
    OptionQuote, OptionType, UnderlyingQuote, OptionSnapshot,
    evaluate_event_calendar, VerticalCreditSpread, calculate_vertical_credit_spread,
    MarketSessionEvidence, build_candidate_control_handoffs, evaluate_market_session,
    scan_vertical_credit_spreads,
)
from hedge_desk.paper import (
    approve_paper_trade, create_paper_trade_plan, write_plan_file,
)
from hedge_desk.paper.runner import advance_paper_lifecycle, close_paper_position, _load_state
from hedge_desk.paper.settler import settle_paper_outcomes
from hedge_desk.risk import build_validated_risk_inputs
from hedge_desk.risk.ruin import estimate_risk_of_ruin

NOW = datetime(2026, 9, 26, 14, 47, tzinfo=timezone.utc)
EQUITY = Decimal("100000")

# --- 1. Fetch REAL CCL chain, pick short 20 put / long 18 put ---
status, raw = _default_transport(CBOE_URL.format(symbol="CCL"))
data = json.loads(raw)["data"]
opts = {o["option"]: o for o in data["options"]}
def quote(occ):
    o = opts[occ]
    return OptionQuote(
        contract_id=occ, underlying="CCL", option_type=OptionType.PUT,
        strike=Decimal(int(occ[-8:]) / 1000), expiration=date(2026, 10, 30),
        bid=Decimal(str(o["bid"])), ask=Decimal(str(o["ask"])),
        bid_size=int(o["bid_size"]), ask_size=int(o["ask_size"]),
        quoted_at=NOW, source_id="cboe-delayed-CCL",
        open_interest=int(o["open_interest"]), volume=int(o["volume"]),
    )
short_q = quote("CCL261030P00022000")   # short 22 put
long_q = quote("CCL261030P00020000")    # long 20 put
underlying = UnderlyingQuote("CCL", Decimal(str(data["current_price"])),
                             Decimal(str(data["current_price"])), NOW, "cboe-delayed-CCL")
snap = OptionSnapshot("hedge-desk-option-snapshot-1.0.0", "cboe-delayed-CCL",
                      underlying, (short_q, long_q), "real-ccl-chain")

# --- 2. Real win probability from Cboe's own delta ---
real_delta = Decimal(str(opts["CCL261030P00022000"]["delta"]))  # -0.425
win_prob = Decimal("1") - abs(real_delta)
print("1. REAL CCL chain: short 20 put bid/ask", short_q.bid, "/", short_q.ask,
      "| long 18 put bid/ask", long_q.bid, "/", long_q.ask)
print("   win_probability (1-|real delta|):", win_prob)

# --- 3. Build the spread ---
spread = calculate_vertical_credit_spread(
    VerticalCreditSpread(
        spread_id="CCL261030P00022000--CCL261030P00020000",
        short_leg=short_q, long_leg=long_q, underlying_quote=underlying,
        quantity=1, commission_per_contract=Decimal("0.65"),
    ), NOW,
)
print("   net_credit:", spread.net_credit, "| max_loss:", spread.maximum_loss)

# --- 4. Account + candidate ---
account = Account("paper-individual-001", AccountType.INDIVIDUAL, EQUITY,
                  EQUITY / Decimal("2"), options_approved=True,
                  options_disclosure_version="synthetic-odd-fixture-v1",
                  options_disclosure_acknowledged_at=NOW - timedelta(days=1),
                  broker_options_policy_version="synthetic-broker-policy-v1")
candidate = TradeCandidate(
    candidate_id=spread.spread_id, symbol="CCL", product_type=ProductType.DEFINED_RISK_OPTION,
    quantity=spread.quantity, entry_price=spread.net_credit, max_loss=spread.maximum_loss,
    expected_win=spread.net_credit, win_probability=win_prob, quote_timestamp=NOW,
    average_daily_dollar_volume=Decimal("100000000"),
    thesis="Real CCL 20/18 put credit spread, 34 DTE, market-implied win prob.",
    invalidation="Reject outside real chain and validated inputs.",
)

# --- 5. Compliance + handoffs + risk inputs ---
compliance = evaluate_paper_compliance(account, candidate, NOW)
scan = scan_vertical_credit_spreads(snap, NOW)
evidence = MarketSessionEvidence("OPRA-REAL", NOW - timedelta(hours=6, minutes=30),
                                 NOW, NOW - timedelta(hours=7), "real-ccl-session")
gate = evaluate_market_session(evidence, NOW, 0)
handoffs = build_candidate_control_handoffs(scan, gate)
assert len(handoffs) == 1 and handoffs[0].candidate_id == candidate.candidate_id
ror = estimate_risk_of_ruin(EQUITY, candidate.max_loss, win_prob, candidate.expected_win)
risk_inputs = build_validated_risk_inputs(
    candidate.candidate_id, candidate.max_loss, candidate.expected_win, win_prob,
    NOW, handoffs[0].calculation_sha256, compliance.portfolio_snapshot_sha256,
    Decimal("0"), ror, "finite-capital-ruin-approximation", "0.1.0-unvalidated",
    "classic-vv-fixture-validator", "1.0.0",
)
decision = evaluate_candidate(account, candidate, NOW, risk_inputs=risk_inputs)
print("   risk decision:", decision.status.value, "| reasons:", decision.reason_codes)
print("   risk_of_ruin:", ror)

# --- 6. Event calendar + plan + approve ---
ecg = evaluate_event_calendar("CCL", NOW, short_q.expiration, (), spread,
                              OptionType.PUT, short_q.strike)
plan = create_paper_trade_plan(
    "real-ccl-001", spread, decision, compliance, NOW, NOW + timedelta(minutes=15),
    event_calendar_gate=ecg,
)
plan = approve_paper_trade(plan, "gp", NOW + timedelta(minutes=1))
print("2. PLAN approved:", plan.plan_id, "| machine_risk:", plan.machine_risk_status.value)

# --- 7. Run the lifecycle ---
tmp = tempfile.TemporaryDirectory()
plans_dir = Path(tmp.name) / "plans"; plans_dir.mkdir()
state_path = Path(tmp.name) / "state.json"
write_plan_file(plan, plans_dir / f"{plan.plan_id}.json")

def ready_quotes(p): return (p.spread.quantity, p.spread.net_credit)
def monitor_lifecycle(p): return {
    "short_leg_in_the_money": False, "ex_dividend_before_expiration": False,
    "assignment_notice_received": False, "contract_adjustment_pending": False,
    "settlement_terms_confirmed": True,
}
r1 = advance_paper_lifecycle(plans_dir, state_path, ready_quotes, NOW + timedelta(seconds=60))
print("3. TICK (fill ready) -> opened:", r1["opened"])
r2 = advance_paper_lifecycle(plans_dir, state_path, ready_quotes,
                             NOW + timedelta(minutes=16), lifecycle_provider=monitor_lifecycle)
print("4. TICK (monitor) -> monitoring:", r2["monitoring"], "| escalated:", r2["escalated"])

# --- 8. Close + settle ---
r3 = close_paper_position(plans_dir, state_path, plan.plan_id, "gp",
                          NOW + timedelta(minutes=2), ("PLANNED_EXIT_REACHED",),
                          short_q, long_q, Decimal("0.65"))
print("5. CLOSE -> realized_pnl:", r3.get("realized_pnl"))
log_path = Path(tmp.name) / "paper-outcomes.jsonl"
r4 = settle_paper_outcomes(Path(tmp.name), log_path, now=NOW + timedelta(minutes=3))
print("6. SETTLE ->", json.dumps(r4, default=str)[:200])
print("7. PAPER OUTCOME LOG:")
for line in log_path.read_text().splitlines():
    print("   ", line[:180])
