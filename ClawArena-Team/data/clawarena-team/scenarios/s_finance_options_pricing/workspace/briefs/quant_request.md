# Audit request — gbm-v2-2026q2

**From:** Priya Mehta, Quant Research
**Date:** 2026-05-20
**Model:** gbm-v2-2026q2  (GBM-based options pricer, v2 candidate for Q2 2026)
**Underlying:** RTSP-2030  (fictitious synthetic equity)
**Contract:** European call, K=52.5, T=0.25 yr (3-month)

Hi team,

We're going through the quarterly model-review cycle. gbm-v2-2026q2 is our
refreshed GBM pricer that updates the vol surface more aggressively. Before
we promote it to the production risk system, the model risk committee needs
a written sign-off with four deliverables:

1. Structured review plan.
2. Evidence that the MC simulation (200 k paths) converges to within ±0.02
   of the Black-Scholes reference.
3. A VaR-95 estimate from the tick data.
4. A final compliance-stamped decision JSON.

Full data package is in `data/`; model code in `code/`. The MC animation
(`reports/mc_convergence_anim.mp4`) shows the path-count convergence visually —
the **video frames** carry the numerical anchor, not any narration.

Please use the same data-analysis subagent session across turns where possible
(the parquet file is large; re-loading wastes time).

— Priya
