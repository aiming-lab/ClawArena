# GrowthCo Statistical Methodology for A/B Experiments

Version: 2.1 (Current)
Last Updated: 2023-10-01
Approved By: Data Science Lead

## 1. Significance Threshold

All experiments use a two-sided significance threshold of **alpha = 0.05** (95% confidence level).
This is the industry standard referenced by Optimizely's Stats Engine:
https://www.optimizely.com/insights/blog/statistics-for-the-internet-age-the-story-behind-optimizelys-new-stats-engine/

## 2. Statistical Power

Default power target: **0.80 (80%)**.
Source: Evan Miller A/B Sample Size Calculator (https://www.evanmiller.org/ab-testing/sample-size.html)

## 3. Sample Size Formula (Two-Proportion Z-Test)

For binary metrics (e.g., conversion rates), use the two-sample z-test formula:

  **n = (z_α/2 + z_β)² × [p1(1-p1) + p2(1-p2)] / (p1 - p2)²**

Where:
- z_α/2 = **1.96** for alpha=0.05, two-sided (97.5th percentile of standard normal)
- z_β  = **0.84** for power=0.80 (80th percentile of standard normal)
- p1 = baseline proportion
- p2 = expected proportion under treatment
- (p1 - p2) = minimum detectable effect

Reference: https://en.wikipedia.org/wiki/Two-proportion_Z-test

## 4. Peeking and Sequential Testing

**Warning**: Continuously monitoring experiment results and stopping early when significance
is reached dramatically inflates the false positive rate.

Per Optimizely's Stats Engine research
(https://www.optimizely.com/insights/blog/statistics-for-the-internet-age-the-story-behind-optimizelys-new-stats-engine/):

- Checking after **every visitor**: actual false positive rate = **57%** (vs nominal 5%)
- Checking after every **500 visitors**: actual false positive rate = **26%**
- Ratio (every-visitor): 57% / 5% = 11.4× inflation

**Policy**: Experiments must run to pre-planned sample size. No early stopping.

## 5. Sample Ratio Mismatch (SRM)

SRM occurs when actual traffic allocation differs significantly from the configured split.

SRM detection thresholds:
- **Statsig**: p < 0.01 (chi-squared test)
  Source: https://docs.statsig.com/stats-engine/methodologies/srm-checks
- **Microsoft ExP**: p < 0.0005 (conservative threshold)
  Source: https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/

Note: These two platforms use different thresholds. Using Statsig's p < 0.01 for this project.

SRM frequency: Approximately **6% of A/B experiments** exhibit SRM (Microsoft & Booking.com research).

## 6. CUPED (Controlled-experiment Using Pre-Experiment Data)

CUPED reduces variance by controlling for pre-experiment covariates.

**Theta formula (Statsig implementation)**:
  **θ = Cov(Y, X) / Var(X)**

Where Y is the post-experiment outcome metric, X is the pre-experiment covariate.

Adjusted metric:
  Y_adjusted = Y - θX + θ·E[X]

Source: https://docs.statsig.com/stats-engine/methodologies/cuped

**Activation conditions (Statsig)**:
- Must have > 100 units with pre-experiment data
- Pre-experiment data coverage must be > 5% of total units
- Pre-experiment window: **7 days prior to first exposure** (Statsig Cloud default)

**Expected variance reduction**:
- Netflix (2016): ~40% reduction in key engagement metrics
  (Source: https://docs.growthbook.io/statistics/cuped)
- Microsoft ExP: R²=0.4 → 1.66× effective traffic multiplier
  (Source: https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/deep-dive-into-variance-reduction/)

## 7. Multiple Comparison Correction

When testing multiple metrics simultaneously, apply correction to control family-wise error rate.

**Available methods**:
- **Benjamini-Hochberg (BH)**: Controls False Discovery Rate (FDR)
- **Bonferroni**: Divides alpha by number of tests (more conservative)

Default for this project: **Bonferroni** correction.
(Note: A VP email requested BH correction on 2023-11-01, but this was subsequently
rescinded per CFO office correction notice dated 2023-11-15.)

Probability of ≥1 false positive with 20 independent tests at alpha=0.05: **~64%**
Source: https://docs.growthbook.io/using/experimentation-problems

## 8. Twyman's Law

Per GrowthBook documentation (https://docs.growthbook.io/using/experimentation-problems):

**"Any figure that looks interesting or different is usually wrong."**

Extremely large positive results (e.g., >20% lift on a mature metric) should be investigated
before being acted upon. Standard diagnostic steps:
1. Check instrumentation and event tracking
2. Check for SRM (if experiment is ongoing)
3. Check for novelty effects
4. Check for bot/spam traffic contamination
5. Validate metric calculation code

## 9. New Experiment Requirements

All new experiments must:
1. Document expected effect size and justify baseline conversion rate
2. Calculate sample size using the formula in Section 3
3. Enable SRM checks from day 1
4. Pre-register primary and secondary metrics
5. Use Bonferroni correction for secondary metrics (Section 7)
