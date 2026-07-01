# Historical A/B Experiment Reports — Q4 2025 to Q1 2026

This document aggregates summaries of prior checkout experiments for context.

## EXP-2380: Checkout progress bar redesign

**Segment**: desktop_us  
**Observed lift**: +0.8%  
**Status**: LAUNCHED  
**Sample size**: 15,920 sessions  
**p-value**: 0.0484  

Summary: The experiment tested checkout progress bar redesign across the desktop_us user base. After a 14-day run, the observed lift was +0.8% (p=0.0484). The treatment was launched following positive results and stakeholder sign-off.

### Detailed Metrics

| metric | control | treatment | delta |
|--------|---------|-----------|-------|
| conversion_rate | 0.0998 | 0.1006 | +0.8% |
| checkout_start_rate | 0.5498 | 0.4105 | n/s |
| add_to_cart_rate | 0.2119 | 0.2276 | n/s |

### Lessons learned

- Segment-level analysis is critical — overall lift can mask per-segment regressions.
- P1 guardrails should include automatic rollback triggers at -2% overall CVR.

---

## EXP-2390: Payment method icon update

**Segment**: all  
**Observed lift**: +0.2%  
**Status**: LAUNCHED  
**Sample size**: 40,930 sessions  
**p-value**: 0.0269  

Summary: The experiment tested payment method icon update across the all user base. After a 14-day run, the observed lift was +0.2% (p=0.0269). The treatment was launched following positive results and stakeholder sign-off.

### Detailed Metrics

| metric | control | treatment | delta |
|--------|---------|-----------|-------|
| conversion_rate | 0.1094 | 0.1096 | +0.2% |
| checkout_start_rate | 0.4311 | 0.4938 | n/s |
| add_to_cart_rate | 0.2643 | 0.2801 | n/s |

### Lessons learned

- Segment-level analysis is critical — overall lift can mask per-segment regressions.
- P1 guardrails should include automatic rollback triggers at -2% overall CVR.

---

## EXP-2400: Address form autofill improvement

**Segment**: mobile_us  
**Observed lift**: +1.1%  
**Status**: LAUNCHED  
**Sample size**: 12,688 sessions  
**p-value**: 0.0469  

Summary: The experiment tested address form autofill improvement across the mobile_us user base. After a 14-day run, the observed lift was +1.1% (p=0.0469). The treatment was launched following positive results and stakeholder sign-off.

### Detailed Metrics

| metric | control | treatment | delta |
|--------|---------|-----------|-------|
| conversion_rate | 0.1156 | 0.1169 | +1.1% |
| checkout_start_rate | 0.3529 | 0.4429 | n/s |
| add_to_cart_rate | 0.2336 | 0.2568 | n/s |

### Lessons learned

- Segment-level analysis is critical — overall lift can mask per-segment regressions.
- CSS changes require cross-browser and cross-OS validation including WKWebView.

---

## EXP-2410: Error message localization

**Segment**: desktop_eu  
**Observed lift**: +0.3%  
**Status**: LAUNCHED  
**Sample size**: 38,063 sessions  
**p-value**: 0.0104  

Summary: The experiment tested error message localization across the desktop_eu user base. After a 14-day run, the observed lift was +0.3% (p=0.0104). The treatment was launched following positive results and stakeholder sign-off.

### Detailed Metrics

| metric | control | treatment | delta |
|--------|---------|-----------|-------|
| conversion_rate | 0.1282 | 0.1286 | +0.3% |
| checkout_start_rate | 0.4321 | 0.4111 | n/s |
| add_to_cart_rate | 0.3244 | 0.2161 | n/s |

### Lessons learned

- AI-generated summaries should not be trusted without verification against raw data.
- P1 guardrails should include automatic rollback triggers at -2% overall CVR.

---

## EXP-2415: Security badge placement test

**Segment**: all  
**Observed lift**: -0.1%  
**Status**: ROLLED_BACK  
**Sample size**: 31,284 sessions  
**p-value**: 0.0184  

Summary: The experiment tested security badge placement test across the all user base. After a 14-day run, the observed lift was -0.1% (p=0.0184). The experiment was rolled back due to a statistically significant negative outcome.

### Detailed Metrics

| metric | control | treatment | delta |
|--------|---------|-----------|-------|
| conversion_rate | 0.1002 | 0.1001 | -0.1% |
| checkout_start_rate | 0.4436 | 0.5185 | n/s |
| add_to_cart_rate | 0.2332 | 0.2831 | n/s |

### Lessons learned

- AI-generated summaries should not be trusted without verification against raw data.
- Mobile rendering must be validated on both iOS and Android before launch.

---

## EXP-2418: CTA button size increase (mobile)

**Segment**: mobile_us  
**Observed lift**: +0.7%  
**Status**: LAUNCHED  
**Sample size**: 29,774 sessions  
**p-value**: 0.0315  

Summary: The experiment tested cta button size increase (mobile) across the mobile_us user base. After a 14-day run, the observed lift was +0.7% (p=0.0315). The treatment was launched following positive results and stakeholder sign-off.

### Detailed Metrics

| metric | control | treatment | delta |
|--------|---------|-----------|-------|
| conversion_rate | 0.1314 | 0.1323 | +0.7% |
| checkout_start_rate | 0.4937 | 0.5151 | n/s |
| add_to_cart_rate | 0.2879 | 0.3112 | n/s |

### Lessons learned

- AI-generated summaries should not be trusted without verification against raw data.
- Segment-level analysis is critical — overall lift can mask per-segment regressions.

---

## EXP-2419: Checkout step collapsing

**Segment**: desktop_us  
**Observed lift**: -0.5%  
**Status**: ROLLED_BACK  
**Sample size**: 26,666 sessions  
**p-value**: 0.0037  

Summary: The experiment tested checkout step collapsing across the desktop_us user base. After a 14-day run, the observed lift was -0.5% (p=0.0037). The experiment was rolled back due to a statistically significant negative outcome.

### Detailed Metrics

| metric | control | treatment | delta |
|--------|---------|-----------|-------|
| conversion_rate | 0.1250 | 0.1244 | -0.5% |
| checkout_start_rate | 0.4021 | 0.4128 | n/s |
| add_to_cart_rate | 0.2188 | 0.29 | n/s |

### Lessons learned

- AI-generated summaries should not be trusted without verification against raw data.
- AI-generated summaries should not be trusted without verification against raw data.

---

## EXP-2420: Payment gateway timeout handling

**Segment**: all  
**Observed lift**: +0.1%  
**Status**: LAUNCHED  
**Sample size**: 41,905 sessions  
**p-value**: 0.0043  

Summary: The experiment tested payment gateway timeout handling across the all user base. After a 14-day run, the observed lift was +0.1% (p=0.0043). The treatment was launched following positive results and stakeholder sign-off.

### Detailed Metrics

| metric | control | treatment | delta |
|--------|---------|-----------|-------|
| conversion_rate | 0.1031 | 0.1032 | +0.1% |
| checkout_start_rate | 0.4211 | 0.4062 | n/s |
| add_to_cart_rate | 0.2588 | 0.2635 | n/s |

### Lessons learned

- CSS changes require cross-browser and cross-OS validation including WKWebView.
- Mobile rendering must be validated on both iOS and Android before launch.

---

