# QuantDesk Source Trace

## ML Options Pricing Papers

Local sources verified:

- `/Users/cebu/Library/Mobile Documents/com~apple~CloudDocs/Documents/MBA/Wall$treet/Books/ML_Options_Pricing_JSER.pdf`
- `/Users/cebu/Library/Mobile Documents/com~apple~CloudDocs/Documents/MBA/Wall$treet/Books/OptionPricing_DeepLearning_Stanford.pdf`

Web corroboration:

- DeepOption uses distilled synthetic data from conventional parametric option-pricing methods, then transfer learning on real option data, with a delta branch for hedging.
- Stanford CS230 option-pricing work models option price from contract terms and financial state, compares against Black-Scholes, uses 20-day historical volatility or 20-day price sequences, and highlights bid/ask prediction as useful.

## Implementation Anchor

`hedge_desk/quantdesk/ml_options.py`

- Creates model-ready rows from option quotes.
- Normalizes spot/strike moneyness and option prices by strike.
- Computes 20-day annualized realized volatility.
- Preserves bid, ask, and mid labels instead of collapsing immediately to one theoretical price.
- Generates deterministic baseline labels from Black-Scholes and Cox-Ross-Rubinstein binomial pricing.
- Computes a distilled mean label for future ML pretraining.
- Applies basic liquidity gates using volume, open interest, and relative spread.
- Emits `trade_authorized = false` because QuantDesk research cannot authorize trades.

## Current Boundary

QuantDesk can curate data and produce research features. It cannot:

- approve trades
- override Risk of Ruin
- override Series 7/FINRA/SEC compliance gates
- place Schwab orders
- treat unvalidated ML output as authoritative

## Next Science Build

- Add historical option-chain adapter with source entitlement.
- Add train/validation/test splits with time ordering and embargo.
- Add model-evaluation metrics for bid, ask, mid, and spread error.
- Add delta/gamma research labels after baseline pricing is stable.
