# exp003: Pricing Page Layout — Experiment Design

## Objective
Test three pricing page variants to maximize paid conversion.

## Variants
- **control**: Current pricing page layout
- **v1_simplified**: Simplified 3-plan layout, less information
- **v2_social_proof**: Adds customer testimonials and trust signals

## Metrics
- **Primary**: paid_conversion_rate
- **Secondary**: revenue_per_visitor, plan_selection_distribution, time_on_pricing_page,
  support_chat_initiated, free_trial_signups, page_scroll_depth, cta_click_rate
  (total: 8 secondary metrics; with primary = 24 total pairwise tests for 3 variants)

## Design Parameters
- Traffic split: 34/33/33
- Target sample size: 15,000 per variant
- Duration: 57 days (Sept 15 – Nov 10)
- Alpha: 0.05, Power: 0.80

## Statistical Testing Plan
- 3 variants × 8 metrics = 24 tests requiring multiple comparison correction
- Planned: Benjamini-Hochberg (BH) correction

## Notes
- Bot traffic contamination discovered post-experiment in control group
- Approximately 12% of control users flagged as bot traffic
- This will require re-analysis with contaminated users removed
