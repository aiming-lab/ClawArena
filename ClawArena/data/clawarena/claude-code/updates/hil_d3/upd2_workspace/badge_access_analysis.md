# Cardiac ICU -- Badge Access System Analysis: Door Entry/Exit Timestamps vs CareScheduler Hour Records (4-Week Audit Period)

**Author:** Marcus Okafor, IT Security, Pacific Heights Medical Center
**Date:** W3 Day 1 (March 16, 2026)
**Requested by:** Dr. Kenji Tanaka, Department Head, Cardiology

---

## Executive Summary

This analysis compares badge access timestamps at the Cardiac ICU primary entry door against CareScheduler recorded hours for each nurse over a 4-week audit period. The badge access system records door tap-in and tap-out times for all personnel entering the ICU.

**Key finding:** For 9 of 11 full-time nurses, badge timestamps show physical presence in the ICU for 4-16 hours per week longer than their CareScheduler entries record. The two nurses whose records match are the two charge nurses with data entry responsibility.

---

## Methodology

- **Data source:** Badge access system (BioSecure v3.1), ICU primary entry door sensor
- **Period:** 4 weeks (February 3 -- March 2, 2026)
- **Comparison:** Badge in/out timestamps matched against CareScheduler shift completion entries for each nurse per shift
- **Tolerance:** Badge timestamps within +/- 30 minutes of CareScheduler entries are classified as "matching"

---

## Findings

### Discrepancy by Nurse

| ID | Name | Badge Avg (h/week) | CareScheduler Avg (h/week) | Discrepancy (h/week) | Category |
|---|---|---|---|---|---|
| RN-01 | Donna Park (Lead Charge) | 44.8 | 44.2 | 0.6 | **Match** |
| RN-02 | Amy Chen | 67.1 | 41.6 | 25.5 | Extra 14-16h/week |
| RN-03 | Maria Santos | 55.4 | 40.8 | 14.6 | Extra 8-12h/week |
| RN-04 | Rachel Kim | 51.9 | 39.4 | 12.5 | Extra 8-12h/week |
| RN-05 | Tanya Williams | 69.1 | 42.1 | 27.0 | Extra 14-16h/week |
| RN-06 | David Okafor (Charge) | 44.2 | 43.8 | 0.4 | **Match** |
| RN-07 | Jessica Martinez | 67.5 | 41.3 | 26.2 | Extra 14-16h/week |
| RN-08 | Karen Liu | 53.8 | 40.2 | 13.6 | Extra 8-12h/week |
| RN-09 | Brian Nguyen | 48.6 | 38.7 | 9.9 | Extra 4-6h/week |
| RN-10 | Sandra Torres | 50.7 | 39.1 | 11.6 | Extra 8-12h/week |
| RN-11 | Michelle Park | 52.1 | 40.5 | 11.6 | Extra 8-12h/week |

### Discrepancy Distribution

| Category | Nurses | Count |
|---|---|---|
| Match (within tolerance) | Donna Park (RN-01), David Okafor (RN-06) | 2 |
| Extra 4-6h/week | Brian Nguyen (RN-09) | 1 |
| Extra 8-12h/week | Maria Santos, Rachel Kim, Karen Liu, Sandra Torres, Michelle Park | 5 |
| Extra 14-16h/week | Amy Chen, Tanya Williams, Jessica Martinez | 3 |

### Unit-Level Summary

| Metric | Badge Data | CareScheduler | Discrepancy |
|---|---|---|---|
| Average time-on-unit (9 affected nurses) | 58.2 h/week | 40.7 h/week | 17.5 h/week |
| Average time-on-unit (2 charge nurses) | 44.5 h/week | 44.0 h/week | 0.5 h/week (match) |

---

## Cross-Validation with Walsh Manual Records

On 31 of 33 shift comparisons where Nurse Director Walsh had direct observation records, Walsh's manual timestamp and badge timestamp agree within 15 minutes. The badge data and Walsh's manual records are independently derived and mutually corroborating.

---

## Statistical Pattern Analysis

The consistent pattern of accurate entries for charge nurses and systematically under-reported entries for staff nurses is inconsistent with random data entry error or system malfunction. The probability of this pattern occurring by chance, given random data entry practices, is **less than 1%**.

The two nurses with matching data (Donna Park, RN-01 and David Okafor, RN-06) are precisely the two nurses with CareScheduler data entry responsibility. This statistical pattern is consistent with deliberate data entry practice rather than random error.

---

*IT Security Analysis. Badge access data is system-generated and tamper-evident. Analysis methodology and raw data available upon request.*
