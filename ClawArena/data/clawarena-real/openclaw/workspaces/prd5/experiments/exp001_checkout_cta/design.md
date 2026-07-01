# exp001: Checkout CTA Button Color — Experiment Design

## Objective
Test whether changing the checkout CTA button from gray to orange increases checkout conversion rate.

## Hypothesis
H₀: There is no difference in checkout conversion rate between the control (gray) and treatment (orange).
H₁: The orange button has a higher checkout conversion rate than the gray button.

## Metrics
- **Primary**: checkout_conversion_rate
- **Secondary**: revenue_per_user, cart_abandonment_rate, page_time_on_page,
  add_to_cart_rate, session_duration, bounce_rate, repeat_visit_rate (total: 8 metrics)

## Design Parameters
- Traffic split: 50/50
- Target sample size: 10,000 per variant
- Alpha: 0.05 (two-sided)
- Power: 0.80
- Baseline conversion rate: ~8%
- Minimum detectable effect: 1.5 percentage points

## SRM Check
- Expected ratio: 1.00
- Actual ratio: 9823/9791 = 1.0033 (within acceptable range, no SRM detected)

## Notes
- Experiment ran 89 days (Aug 1 – Oct 29, 2023)
- No peeking protocol enforced during experiment run
