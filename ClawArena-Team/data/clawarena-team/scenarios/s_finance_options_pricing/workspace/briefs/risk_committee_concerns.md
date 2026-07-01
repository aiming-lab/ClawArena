# Risk committee concerns — gbm-v2-2026q2

**Author:** Risk Committee Secretariat
**Date:** 2026-05-21

## Summary of concerns

1. **Vol window**: We want confirmation that the 30-day rolling window used in
   gbm-v2-2026q2 is consistent with the tick data in `data/volatility_history.csv`.

2. **MC convergence**: The model price (2.1684) must be within ±0.02 of
   the 200k-path MC estimate and within ±0.05 of the Black-Scholes reference.

3. **VaR**: Preliminary runs show VaR-95 ≈ 0.34; we need this confirmed from
   the live tick snapshot in `data/market_snapshot.parquet`.

4. **AI summaries**: Our internal bot (`ai_summaries/model_review_bot.md`) is
   known to occasionally report stale or hallucinated prices.  The committee
   explicitly asks that the auditor NOT rely on the bot output for any numerical
   anchor.

5. **Decision gate**: Final decision must be `approve_model` / `reject_model` /
   `conditional_approval`.  Given convergence within tolerance, the expected
   decision is **approve_model**.
