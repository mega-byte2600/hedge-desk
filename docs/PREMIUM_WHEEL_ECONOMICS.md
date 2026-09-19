# Premium wheel economics — measured on real data (2026-09-19)

Findings from the cash-secured-put scanner (`hedge_desk/csp_scan.py`) across 24+
liquid names, real Cboe delayed chains, 30-45 DTE. This resolves what "max ~2%
per trade" means and whether the wheel premise holds.

## Two different "2%"s (the key reconciliation)

1. return_on_capital = net_credit / collateral = **0.013% - 0.065% per month**
   measured near-the-money across F/T/BAC/CLF/SOFI/PLUG/NIO/RIVN/KO/SPY. This is
   the yield on the FULL capital deployed (the cash securing the put). It is
   SMALL because the collateral is the whole strike.

2. premium yield = net_credit / strike = **1.3% - 3% per month** (e.g. F 0.39/13
   = 3.0%, RIVN 0.92/15 = 6.1%, SPY 9.91/762 = 1.3%). This is premium as a
   fraction of the notional strike, which is what "sell premium every 30 days"
   intuitively means.

The GP's "max 2% per trade" is conventional for the PREMIUM YIELD (metric 2),
NOT the return-on-capital-deployed (metric 1). The wheel does NOT make 2% of
collateral per month; it makes ~2% of the strike in premium per month against
risk of assignment. Confusing the two overstates the economics ~40x.

## What the wheel actually earns (honest, real, per 30-45d)
- Near-the-money cash-secured put: ~1-3% of strike in collected premium.
- that premium is income if the option expires; the assigned position then owns
  the stock at ~strike. Return is NOT 2% of the cash used.
- Deep 10% OTM puts buy little (F ~0.10, KO ~0.01): premium near zero — the
  "sell puts way OTM" version pays almost nothing on most names.

## Practical consequences for the product
- The <$5k capital filter is good for a starting account, but combined with 1-3%
  premium yield means <$5k x ~2% = ~$50-150 of premium per position per month —
  real but modest; transaction costs matter.
- The scanner's `RETURN_NOT_IN_GP_BAND` reason fired on LOW returns (0.0xxx%),
  i.e. real data says metric 1 in 0.5-2% band is unachievable for CSP. If the
  GP's 2% is the premium yield, the rule basis must be premium/strike, not
  premium/collateral. This is a flag for the GP to confirm which basis — do not
  assume; do not silently repoint.

## Status / V&V
- VERIFIED (measured): the numbers above are from real Cboe bid/ask, reproducible
  by re-running the scanner.
- LEARN: the strategy economics must be stated as premium yield on strike, and
  the "2%" basis must be confirmed with the GP before the rule is relied upon.
- NOT YET: no decision (survivability INDETERMINATE without a real account);
  no order. Nothing is trade_authorized.