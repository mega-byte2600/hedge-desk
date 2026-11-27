[fix] Close the RoR-substitution escape in scripts/

Thursday's risk audit (GAP 1): the architecture-boundary test scanned only
hedge_desk/ for estimate_risk_of_ruin calls, so scripts/real_nke_paper_trade.py
and scripts/real_ccl_paper_trade.py called it, wrapped the result in
build_validated_risk_inputs, and approved a paper-trade plan — the forbidden
pattern end to end, untested. Both scripts even claimed "RoR from the
deterministic engine" in their docstrings.

This branch: the boundary test now scans scripts/ too (with a test pinning
that coverage); both scripts use a new demo-only helper
(hedge_desk.demo.build_demo_risk_inputs) that passes an explicit 0
placeholder in the RoR slots, labeled unvalidated — the same posture as the
frozen reference demo. No RoR is computed anywhere outside
hedge_desk/risk/ruin.py anymore. The scripts' decisions now reflect only the
non-RoR gates; they remain lifecycle mechanics demos, not risk approvals.

Verified (2026-11-27): full suite pytest 1,416 tests, 0 failures; focused
risk suites 102 passed; node test set 60 passed, 0 failed; negative control
— the two extended boundary tests FAIL on the old scripts and pass with the
fix. No RoR value was calculated or modified by this change. Risk-control
change: independent authorized approval required before merge.
