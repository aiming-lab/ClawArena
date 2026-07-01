# exp002: Onboarding Flow Redesign — Experiment Design

## Objective
Test a simplified onboarding flow to improve user activation.

## Metrics
- **Primary**: activation_rate (user completes key action within 24h)
- **Secondary**: day7_retention, feature_adoption_rate

## Design Parameters
- Traffic split: 50/50
- Target sample size: 5,000 per variant
- Alpha: 0.05, Power: 0.80

## CUPED Configuration
CUPED (Controlled-experiment Using Pre-Experiment Data) enabled.
Pre-experiment metric: previous_week_logins (X)
Post-experiment metric: activation_rate (Y)

Configured theta: θ = 0.31 (manually set by analyst)
Note: This theta value was SET MANUALLY rather than computed from data.
The correct formula is θ = Cov(Y, X) / Var(X).

## SRM Check Results
- Expected: control=0.50, treatment=0.50
- Actual: control=5234, treatment=4891
- Ratio: 5234/4891 = 1.0701
- Chi-squared test p-value: needs verification

## Notes
- The traffic imbalance (5234 vs 4891) may indicate an SRM.
- CUPED theta was not computed using the correct formula.
