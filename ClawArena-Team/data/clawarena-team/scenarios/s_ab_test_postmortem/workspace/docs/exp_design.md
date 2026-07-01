# Experiment Design — EXP-2421

## Experiment parameters

- Experiment ID: EXP-2421
- Control arm: A (existing checkout, blue button #0055cc)
- Treatment arm: B (redesigned checkout, warm CTA #ff6633)
- Launch date: 2026-04-10
- Expected duration: 28 days (powered for n=40,000 per arm)
- Pre-launch projected lift: +1.5% conversion rate
- Minimum detectable effect (MDE): 0.5% at 80% power, alpha=0.05

## Segment allocation

| Segment       | Control (A) | Treatment (B) | Notes                          |
|---------------|-------------|---------------|-------------------------------|
| desktop_us    | 50%         | 50%           | Largest segment                |
| desktop_eu    | 50%         | 50%           | GDPR notice differences        |
| mobile_us     | 50%         | 50%           | iOS 14 dominant (67%)          |
| mobile_eu     | 50%         | 50%           | Android-heavy (58%)            |

## Analysis plan

Cross-tab analysis per segment: compute conversion rate (converted / total) by variant,
compute lift = (treatment_cvr - control_cvr) / control_cvr, run chi-squared test for
significance (p < 0.05 threshold).

## Known caveats

- iOS 14 WKWebView has a known color rendering issue with certain hex values.
  Specifically, rgba backgrounds with warm hues in the ff6000-ff9000 range may
  display as grey due to compositing layer bug.
- This was flagged in the risk register but mobile simulator testing was incomplete.
