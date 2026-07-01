# exp001 Analysis Report — DRAFT

## Summary
Experiment: Checkout CTA Button Color
Status: ENDED
Analysis Date: 2023-11-01

## Key Finding
The treatment (orange button) showed a **+45% lift** in checkout_conversion_rate
(control: 8.2%, treatment: 11.9%, p=0.00001).

⚠️ **NOTE**: This +45% lift is highly unusual compared to historical experiments
(typical range: 2-8%). This should be investigated per Twyman's Law:
"Any figure that looks interesting or different is usually wrong."

## Statistical Issues Identified

### Issue 1: Peeking (Early Stopping)
The experiment was monitored daily. Analysis logs show statistical significance was
first reached on Day 12 with p=0.041. However, the experiment continued running.
Multiple looks at the data inflate the actual false positive rate far above 5%.

According to Optimizely's Stats Engine analysis:
- Checking after every visitor: **actual false positive rate = 5%** (incorrectly stated)
- This is a known peeking problem that needs correction.

### Issue 2: Multiple Comparisons
8 secondary metrics were tested simultaneously. With alpha=0.05, the probability of
at least one false positive across 8 metrics is approximately 1 - (0.95)^8 ≈ 34%.

### Issue 3: Anomalous Primary Metric Lift
The +45% lift on checkout_conversion_rate is statistically significant but practically
implausible. Historical experiments have shown lifts of 2-8% for UX changes.

## Conclusion
**Inconclusive** — the +45% lift is flagged as suspicious per Twyman's Law and requires
diagnostic investigation before any rollout decision.

## Recommendation
1. Run Twyman diagnostic checklist on checkout_conversion_rate
2. Apply BH correction to secondary metrics
3. Investigate potential instrumentation issues

_This draft report has been flagged for peer review._
