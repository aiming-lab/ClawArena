# exp005: Dashboard Widget Personalization — Experiment Design

## Objective
Personalize the main dashboard widget based on user behavior patterns.

## CUPED Eligibility Requirements (Statsig standard)
Before enabling CUPED for this experiment, must verify:
1. Units with pre-experiment data: > 100 users
2. Pre-experiment data coverage: > 5% of total users
3. Pre-experiment window: 7 days prior to exposure (Statsig Cloud default)

## Planned Pre-Experiment Metric
- metric: daily_active_usage_score
- window: 7 days before first exposure
- data source: pre_experiment_metrics.csv

## Notes
- CUPED eligibility needs verification from pre_experiment_metrics.csv
- If eligible, theta = Cov(Y, X) / Var(X) must be computed from data
