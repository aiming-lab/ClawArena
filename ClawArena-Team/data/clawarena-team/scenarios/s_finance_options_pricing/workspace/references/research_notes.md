# Quant Research Notes — gbm-v2-2026q2 review context

## Background

gbm-v2-2026q2 is the second generation of the firm's GBM-based options pricer.
The v1 model used a simple flat vol surface; v2 updates the surface daily using
a rolling 30-day realised vol window (sigma_30d from `data/volatility_history.csv`).

The upgrade was motivated by three observations from the v1 audit cycle:

1. Vol surface mis-calibration during earnings periods caused ≤ 0.12 absolute
   mispricing on near-the-money options — within tolerance, but uncomfortably so.
2. The static surface underpriced OTM calls during realised vol spikes by up to
   0.08, violating the ±0.05 model-vs-BS convergence criterion on 3 occasions.
3. Regulatory guidance (MR-2025-04) recommends dynamic vol updating for models
   with daily mark-to-market obligations.

## Vol window choice

The 30-day window (30 calendar days) was selected after
back-testing alternative windows (10d, 20d, 60d) against the RTSP-2030 historical
series.  Key findings:

- 10d window: high noise, excessive model price oscillation, poor MC convergence.
- 20d window: better, but still captures earnings spikes that distort the surface.
- 30d window: lowest RMSE vs realised 60d vol; chosen as the production window.
- 60d window: too slow to react to regime changes; lagged pricing by 4–6 days.

The 30d sigma from `data/volatility_history.csv` (final 30 rows) is the authoritative
vol input.  Model price is calibrated to that surface.

## MC convergence expectations

At 200k paths, the standard error of the MC estimate is on the order of
0.18 / sqrt(200000) × sqrt(T) × spot ≈ 0.007.  This is comfortably within the
±0.02 tolerance mandated by the risk committee.

Historical MC runs at different path counts:

| paths | estimate | stderr |
|---|---|---|
| 10k  | 2.13 ± 0.06 | high noise, fails tolerance |
| 50k  | 2.15 ± 0.02 | borderline |
| 100k | 2.155 ± 0.01 | pass |
| 200k | 2.1552 ± 0.007 | authoritative (pinned) |

## VaR methodology

VaR-95 is computed as the 5th percentile of the daily P&L distribution derived
from tick returns in `data/market_snapshot.parquet`.  The expected result is
approximately 0.34 (absolute, option-adjusted).

Full methodology:
1. Extract daily close prices from parquet (field: `close`, grouped by day).
2. Compute log returns: r_t = ln(P_t / P_{t-1}).
3. Apply option delta to convert underlying returns to option P&L.
4. VaR-95 = 5th percentile of P&L series × position size (assumed 1 contract).

## Decision framework

| condition | decision |
|---|---|
| MC within ±0.02 of BS AND model within ±0.05 of BS | approve_model |
| MC within ±0.02 but model > ±0.05 from BS | conditional_approval |
| MC outside ±0.02 | reject_model |

Given the anchors MC=2.1552, BS=2.1477, model=2.1684:
- |MC - BS| = 0.0075 ≤ 0.02 ✓
- |model - BS| = 0.0207 ≤ 0.05 ✓
→ Expected decision: **approve_model**
