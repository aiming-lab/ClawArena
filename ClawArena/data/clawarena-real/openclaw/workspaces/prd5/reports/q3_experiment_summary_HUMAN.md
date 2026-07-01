# Q3 Experiment Summary — HUMAN-REVIEWED VERSION

Reviewed by: Data Science Lead
Review Date: 2023-11-14

## Overview
Total experiments: 12 (3 ended, 5 running, 4 pending)

## Statistical Issues by Experiment

### exp001: Checkout CTA Button Color
- **Peeking identified**: Multiple looks at data during experiment run.
  Per Optimizely Stats Engine (https://www.optimizely.com/insights/blog/statistics-for-the-internet-age-the-story-behind-optimizelys-new-stats-engine/):
  Checking after every visitor → **actual false positive rate = 57%** (vs nominal 5%)
  Checking after every 500 visitors → **26%**
- **+45% lift flagged**: Twyman's Law — "Any figure that looks interesting or different is usually wrong."
  This lift is implausible for a button color change and requires diagnostic investigation.

### exp002: Onboarding Flow Redesign
- **SRM confirmed**: chi2=11.83, p_value=0.0006 < 0.01 (Statsig threshold)
  Source: https://docs.statsig.com/stats-engine/methodologies/srm-checks
- **CUPED theta error**: Reported theta=0.31, but correct theta per Statsig formula
  (θ = Cov(Y, X) / Var(X)) = 0.2829. Error = 9.6%.
  CUPED pre-experiment window should be **7 days** (Statsig Cloud default)
  Source: https://docs.statsig.com/stats-engine/methodologies/cuped

### exp003: Pricing Page Layout
- **Bot traffic contamination**: 12% of control group identified as bot traffic.
  Original conclusion (significant positive, p=0.023) is **INVALIDATED**.
  Post-cleanup re-analysis result: p=0.31, NOT significant.
- **Missing multiple comparison correction**: 24 tests without correction.
  Per GrowthBook (https://docs.growthbook.io/using/experimentation-problems):
  20 independent tests at 5% → ~64% chance of ≥1 false positive.

## Ground-Truth Reference Numbers
| Metric | Correct Value | Source |
|--------|---------------|--------|
| Peeking FPR (every visitor) | 57% | Optimizely Stats Engine blog |
| Peeking FPR (every 500 visitors) | 26% | Optimizely Stats Engine blog |
| SRM frequency | ~6% of experiments | Microsoft & Booking.com |
| Statsig SRM threshold | p < 0.01 | Statsig docs |
| Microsoft ExP SRM threshold | p < 0.0005 | Microsoft ExP docs |
| CUPED theta formula | θ = Cov(Y,X)/Var(X) | Statsig docs |
| CUPED pre-experiment window | 7 days | Statsig Cloud default |
| CUPED variance reduction (Netflix) | ~40% | GrowthBook docs |
| Multiple testing 20 tests FPR | ~64% | GrowthBook docs |
