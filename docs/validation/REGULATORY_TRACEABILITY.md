# Regulatory traceability register

`hedge_desk.compliance.traceability` maps each implemented paper control to an
official FINRA, SEC, CFTC, or OCC source, its applicability, deterministic
reason codes, and a test module. The canonical registry hash is embedded in the
independent compliance decision and therefore in the human plan hash, audit
lineage, and morning report.

The register is source traceability, not legal approval. Every reference entry
currently has `counsel_approved_for_live=false`; changing that flag is not
sufficient to enable live operation because the separate release gate also
requires all other signed evidence and a separate authorization architecture.
Rules and broker requirements can change and must be reviewed by qualified
counsel and the relevant broker before live use.
