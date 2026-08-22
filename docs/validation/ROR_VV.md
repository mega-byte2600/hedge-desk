# Risk-of-Ruin V&V boundary

The Risk-of-Ruin value is calculated only by conventional software. Agents do
not create its validated inputs, calculate the authoritative result, approve
the model, or override its blockers.

`tests/fixtures/ror_vv_vectors.json` locks exact outputs for version
`0.1.0-unvalidated`. `tests/test_ror_vv_vectors.py` independently reconstructs
the same finite-capital approximation with rational `Fraction` arithmetic and
checks the production Decimal result within the declared relative tolerance.
This catches formula, argument-order, precision, and regression errors.

Passing these vectors is implementation verification, not empirical model
validation. The model remains prohibited for live capital until an independent
human V&V owner approves the model specification, assumptions, empirical
calibration, failure modes, thresholds, and signed evidence artifact through
the separate release gate.
