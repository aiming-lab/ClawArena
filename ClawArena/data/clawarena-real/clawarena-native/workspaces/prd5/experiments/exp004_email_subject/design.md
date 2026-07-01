# exp004: Email Subject Line Optimization — Experiment Design

## Objective
Test personalized email subject lines to improve open rates.

## Parameters
- Baseline open rate (p1): 22% (0.22)
- Expected lift: +3 percentage points (p2 = 0.25)
- Alpha: 0.05 (two-sided)
- Power: 0.80 (80%)

## Sample Size Calculation
Based on two-proportion z-test formula:
  n = (z_alpha/2 + z_beta)^2 × [p1(1-p1) + p2(1-p2)] / (p1-p2)^2

Using z_alpha/2 = 1.96 (alpha=0.05, two-sided)
     z_beta  = 0.84 (power=0.80)

DRAFT calculation (pending verification with corrected script):
  n ≈ 2,400 per group (preliminary estimate)

## Notes
- power_analysis.py uses INCORRECT parameters — needs correction
- The existing script incorrectly uses z_alpha=2.576 (99% CI) and z_beta=1.28 (90% power)
