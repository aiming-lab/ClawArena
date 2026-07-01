# exp002 Analysis Report — v2

## Summary
Experiment: Onboarding Flow Redesign
Status: ENDED
Analysis Date: 2023-11-05

## SRM Check
Chi-squared test performed on final sample allocation:
- Control: 5,234 users (expected: 5,062.5)
- Treatment: 4,891 users (expected: 5,062.5)
- chi2_stat = 11.83
- p_value = 0.0006

This p-value is below 0.01 (Statsig threshold for SRM investigation).
⚠️ SRM DETECTED — results are unreliable pending investigation.

## CUPED Analysis
CUPED adjustment applied with theta = 0.31.
However, this theta was manually configured rather than computed as:
  θ = Cov(Y, X) / Var(X)

Recalculation needed using the correct Statsig formula.

Pre-experiment covariance (Cov(activation_rate, previous_week_logins)): 0.0412
Pre-experiment variance (Var(previous_week_logins)): 0.1456
Correct theta = 0.0412 / 0.1456 = 0.2829

Reported theta (0.31) vs. correct theta (0.2829): error = 9.6%

## Primary Metric Result
activation_rate: control=0.342, treatment=0.371
p-value (unadjusted): 0.038 (significant at alpha=0.05)
p-value (CUPED adjusted): 0.029

## Conclusion
**Results INVALID due to SRM.** CUPED theta was also misconfigured.
Investigation required before any conclusions drawn.
