# STAT inference V&V boundary

`hedge_desk.stat_inference` is conventional deterministic software, not an
agent opinion. It implements a one-sided exact binomial test of directional hit
rate against a declared null and a 95% Wilson score interval.

- The hypothesis-test significance threshold is `alpha = 0.005`.
- The interval coverage target is separately `confidence_level = 0.95`.
- Inference is withheld below 100 observations by default.
- Inputs must be resolved point-in-time outcomes from a frozen, non-overlapping
  evaluation set. The function does not establish that requirement by itself.
- A significant result is not profitability, causal evidence, strategy
  approval, or trade authorization. Costs, calibration, multiple testing,
  dependence, regime drift, capacity, and tail loss remain separate gates.
- `trade_authorized` is structurally always false.

The test suite locks an exact `Binomial(100, 0.5)` tail vector, Wilson interval
containment, the significance boundary, insufficient-sample withholding, and
malformed-input rejection. Any method or confidence-level change requires a new
version and independent V&V vectors.
