# Risk of Ruin trust boundary

The agentic decision runtime never calculates, estimates, repairs, or fills in
Risk of Ruin (RoR). It accepts only a content-addressed validation artifact with
both `risk_of_ruin_before` and `risk_of_ruin_after`, the conventional model ID
and version, validator identity and version, source hash, portfolio snapshot
hash, candidate economics, and as-of time. Missing, mismatched, future-dated,
or corrupt artifacts fail closed.

`hedge_desk/risk/ruin.py` contains the isolated conventional reference
implementation and its hard comparison gate. Its numerical implementation is
covered by locked golden vectors and an independent rational-arithmetic oracle.
The orchestration layer does not call that calculator; it preserves the exact
validator-issued output and can only route its existing result through policy.

The checked-in reference implementation remains explicitly unvalidated and
paper-only. It is not production authority. Production requires an independent
classic software-development V&V release, separately controlled artifact
issuer, approved model/version allowlist, and immutable signed input/output
lineage. No agent or agent quorum may issue, alter, approve, or override it.
