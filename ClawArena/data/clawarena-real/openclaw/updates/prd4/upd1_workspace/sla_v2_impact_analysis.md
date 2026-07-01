# SLA Policy v2 Impact Analysis Report
**Prepared by:** Support Operations Team
**Date:** 2025-02-01
**Subject:** Impact Analysis of L2 Response Time Change (120min → 90min)

## Executive Summary

This document analyses the operational impact of tightening the L2 response time SLA
from 2 hours (120 minutes) to 90 minutes under `sla_matrix_v2.json`, effective 2025-02-01.

**Key Finding:** The change from L2=120min to L2=90min will reclassify tickets whose
actual response time falls between 91 and 120 minutes from "compliant" to "breach" status.
This analysis quantifies this impact using historical Q4 2024 data.

**IMPORTANT:** This analysis is prepared for the Q7 round of analysis. At this point,
`sla_matrix_v2.json` is in force. However, a subsequent management notice (FEISHU-PRD4-L2-REVERT)
may supersede this change. Always check for the most recent policy update before applying.

---

## Section 1: Policy Change Summary

### 1.1 Change Details

| Field | Old Value (v1) | New Value (v2) | Delta |
|---|---|---|---|
| L2 response_minutes | 120 | **90** | -30 minutes |
| L2 coverage | 24/7 | 24/7 | Unchanged |
| All other levels | Unchanged | Unchanged | — |

### 1.2 Rationale

The tightening of the L2 SLA from 2 hours to 90 minutes was approved as part of
NebulaTech's customer commitment upgrade program (Q4 2024 roadmap item #17).

Rationale:
- Customer satisfaction surveys indicated L2 responses between 90-120 minutes
  were perceived as "slow" by 73% of affected customers
- Competitive analysis shows most Enterprise-tier competitors have L2 SLAs ≤ 90 minutes
- Support team capacity analysis (September 2024) indicated 90-minute compliance
  was achievable at 94% rate with current staffing

---

## Section 2: Q4 2024 Historical Impact Analysis

### 2.1 Tickets in the 91-120 Minute Range (L2 Only)

Under v1 (L2=120min), tickets with L2 response between 91-120 minutes were COMPLIANT.
Under v2 (L2=90min), these same tickets become BREACHED.

The following Q4 2024 L2 tickets are affected by this reclassification:

| Ticket ID | Created | Response (min) | v1 Status | v2 Status |
|---|---|---|---|---|
| Q4-L2-NEARV2-001 | (see batch file) | 91-119 | PASS | BREACH |
| Q4-L2-NEARV2-002 | (see batch file) | 91-119 | PASS | BREACH |
| Q4-L2-NEARV2-003 | (see batch file) | 91-119 | PASS | BREACH |

**Impact on Q4 L2 Breach Count:**
- Under v1: 8 L2 breaches (response > 120 min)
- Under v2: 11 L2 breaches (response > 90 min; includes the 3 near-threshold tickets)
- Net increase: **+3 breach tickets** due to threshold tightening

**Impact on Q4 Total Breach Count:**
- Under v1: 28 total breaches
- Under v2: 31 total breaches

### 2.2 Compliance Rate Impact

| Metric | v1 (L2=120min) | v2 (L2=90min) | Change |
|---|---|---|---|
| Q4 Total breaches | 28 | 31 | +3 |
| Q4 L2 compliance | 86.78% (48/55 compliant) | 81.82% (45/55 compliant) | -4.96% |
| Q4 Overall compliance | 86.00% | 84.50% | -1.50% |

### 2.3 Forward-Looking Q1 2025 Analysis

For Q1 2025 tickets, the v2 threshold applies from the start of the quarter.
Estimated Q1 L2 compliance under v2: see breach_tickets_Q1.json after analysis.

---

## Section 3: Operational Impact Assessment

### 3.1 Staffing Requirements

Based on Q4 2024 data, achieving 90-minute L2 response at 95% compliance rate requires:

| Shift | Current Coverage | Required Coverage | Gap |
|---|---|---|---|
| Business hours (09:00-18:00) | 8 engineers | 8 engineers | None |
| Evening (18:00-00:00) | 3 engineers | 5 engineers | -2 |
| Overnight (00:00-09:00) | 2 engineers | 4 engineers | -2 |
| Weekend days | 4 engineers | 6 engineers | -2 |
| Weekend nights | 1 engineer | 3 engineers | -2 |

**Staffing gap:** 8 additional FTE-equivalent coverage slots required.

**NOTE:** This gap analysis is the basis for the subsequent management decision
to revert the L2 change (ref: FEISHU-PRD4-L2-REVERT). The 90-minute target
could not be met with existing staffing levels.

### 3.2 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| L2 breach rate increase | High (due to staffing gap) | High (SLA penalties) | Revert to 120min |
| Customer dissatisfaction at 90min target | Low | Medium | Monitor CSAT |
| Escalation rate increase | Medium | Medium | Auto-escalation at 75min |

---

## Section 4: Detailed Ticket Analysis by Severity

### 4.1 L1 Tickets (Q4 2024 — No Change Under v2)

L1 threshold remains 30 minutes. All L1 analysis unchanged.

| Metric | Q4 2024 Value |
|---|---|
| Total L1 tickets | 50 (approx.) |
| L1 breaches | 10 |
| L1 compliance rate | 80.00% |
| Worst L1 breach (min) | 87-90 min (approx.) |

### 4.2 L2 Tickets (Q4 2024 — Affected by v2)

| Category | Count | Notes |
|---|---|---|
| L2 breaches under v1 (>120min) | 8 | Clear breaches regardless of version |
| L2 near-threshold (91-120min) | 3 | Compliant under v1; breach under v2 |
| L2 compliant under v2 (<91min) | 45 | Compliant under both versions |
| **Total L2 breaches under v2** | **11** | |

### 4.3 L3 Tickets (Q4 2024 — No Change Under v2)

L3 threshold remains 480 minutes (8 hours).

| Metric | Q4 2024 Value |
|---|---|
| Total L3 tickets | 56 (approx.) |
| L3 breaches | 6 |
| L3 compliance rate | 89.29% |

### 4.4 L4 Tickets (Q4 2024 — No Change Under v2)

L4 threshold remains 1440 minutes (24 hours).

| Metric | Q4 2024 Value |
|---|---|
| Total L4 tickets | 43 (approx.) |
| L4 breaches | 4 |
| L4 compliance rate | 90.70% |

---

## Section 5: Q1 2025 Forward Projection (Under v2)

### 5.1 Expected Breach Counts

Based on Q4 2024 patterns and staffing constraints:

| Severity | Q1 Total (est.) | Q1 Breach (est.) | Rate |
|---|---|---|---|
| L1 | 45 | 5 | 88.89% |
| L2 | 55 | 10-12 | 78-82% |
| L3 | 30 | 4 | 86.67% |
| L4 | 20 | 3 | 85.00% |

### 5.2 Year-over-Year Comparison

| Quarter | Total Tickets | Total Breaches | Compliance |
|---|---|---|---|
| Q3 2024 (v1) | 185 | 22 | 88.11% |
| Q4 2024 (v1) | 200 | 28 | 86.00% |
| Q1 2025 (v2) | 150 | ~22 | ~85.33% |

---

## Appendix A: Per-Ticket Analysis Detail (Q4 2024 L2)

The following lists all Q4 2024 L2 tickets with their response times and
status under both v1 and v2 policies:

### L2 Breach Tickets Under v1 (>120 min)
| Q4-L2-BREACH-001 | 178 | BREACH (v1) | BREACH (v2) | delta=58 (v1), delta=88 (v2) |
| Q4-L2-BREACH-002 | 218 | BREACH (v1) | BREACH (v2) | delta=98 (v1), delta=128 (v2) |
| Q4-L2-BREACH-003 | 126 | BREACH (v1) | BREACH (v2) | delta=6 (v1), delta=36 (v2) |
| Q4-L2-BREACH-004 | 229 | BREACH (v1) | BREACH (v2) | delta=109 (v1), delta=139 (v2) |
| Q4-L2-BREACH-005 | 230 | BREACH (v1) | BREACH (v2) | delta=110 (v1), delta=140 (v2) |
| Q4-L2-BREACH-006 | 227 | BREACH (v1) | BREACH (v2) | delta=107 (v1), delta=137 (v2) |
| Q4-L2-BREACH-007 | 163 | BREACH (v1) | BREACH (v2) | delta=43 (v1), delta=73 (v2) |
| Q4-L2-BREACH-008 | 234 | BREACH (v1) | BREACH (v2) | delta=114 (v1), delta=144 (v2) |

### L2 Near-Threshold Tickets (91-120 min)
| Q4-L2-NEARV2-001 | 102 | PASS (v1) | BREACH (v2) | delta=N/A (v1), delta=12 (v2) |
| Q4-L2-NEARV2-002 | 97 | PASS (v1) | BREACH (v2) | delta=N/A (v1), delta=7 (v2) |
| Q4-L2-NEARV2-003 | 99 | PASS (v1) | BREACH (v2) | delta=N/A (v1), delta=9 (v2) |

### L2 Compliant Tickets Under Both Policies (<91 min)
| Q4-L2-OK-001 | 82 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-002 | 65 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-003 | 30 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-004 | 57 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-005 | 25 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-006 | 65 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-007 | 43 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-008 | 81 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-009 | 32 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-010 | 88 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-011 | 80 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-012 | 33 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-013 | 55 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-014 | 21 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-015 | 77 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-016 | 62 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-017 | 84 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-018 | 74 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-019 | 31 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-020 | 28 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-021 | 36 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-022 | 19 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-023 | 34 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-024 | 53 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-025 | 51 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-026 | 13 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-027 | 68 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-028 | 53 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-029 | 13 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-030 | 75 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-031 | 63 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-032 | 10 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-033 | 10 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-034 | 30 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-035 | 84 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-036 | 32 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-037 | 46 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-038 | 22 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-039 | 63 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-040 | 23 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-041 | 83 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-042 | 33 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-043 | 58 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-044 | 39 | PASS (v1) | PASS (v2) | |
| Q4-L2-OK-045 | 77 | PASS (v1) | PASS (v2) | |

---

## Appendix B: Policy Version Comparison Table

| Field | v0 (ARCHIVED) | v1 (Effective 2024-01-01) | v2 (Effective 2025-02-01) | v2-reverted |
|---|---|---|---|---|
| L1 response | 60 min (ERROR) | **30 min** | 30 min | 30 min |
| L2 response | 120 min | 120 min | **90 min** | **120 min (reverted)** |
| L3 response | 480 min | 480 min | 480 min | 480 min |
| L4 response | 1440 min | 1440 min | 1440 min | 1440 min |
| L2 coverage | 24/7 | 24/7 | 24/7 | 24/7 |

Notes:
- v0 L1=60min was an ERROR. Do not reference v0 for any current analysis.
- v2 L2=90min was approved but subsequently REVERTED by management notice FEISHU-PRD4-L2-REVERT.
- After the revert, L2=120min (same as v1) applies.

---

## Appendix C: SLA Calculation Reference Tables

### Response Time Thresholds (All Versions)

| Severity | v1 | v2 | v2-reverted |
|---|---|---|---|
| L1 | 30 | 30 | 30 |
| L2 | **120** | **90** | **120** |
| L3 | 480 | 480 | 480 |
| L4 | 1440 | 1440 | 1440 |

### Credit Tiers (Atlassian Enterprise — Unchanged Across All Versions)

| Uptime | Credit |
|---|---|
| 99.90%–99.95% | 5% |
| 99.00%–99.90% | 10% |
| 95.00%–99.00% | 25% |
| < 95.00% | 50% |

---

## Appendix D: Staffing Analysis Detail

### Current vs Required Coverage (per 4-hour block)

| Time Block | Day | Current | Required | Gap |
|---|---|---|---|---|
| 00:00-04:00 | Mon-Fri | 2 | 4 | -2 |
| 04:00-08:00 | Mon-Fri | 2 | 3 | -1 |
| 08:00-12:00 | Mon-Fri | 8 | 8 | 0 |
| 12:00-16:00 | Mon-Fri | 8 | 8 | 0 |
| 16:00-20:00 | Mon-Fri | 5 | 7 | -2 |
| 20:00-24:00 | Mon-Fri | 3 | 5 | -2 |
| 00:00-12:00 | Sat-Sun | 2 | 4 | -2 |
| 12:00-24:00 | Sat-Sun | 2 | 4 | -2 |

**Total coverage gap: equivalent to 8-10 additional FTEs**

Conclusion: Without additional hiring or shift adjustments, the 90-minute L2 SLA
target is not achievable at the required 95% compliance rate. This is the primary
driver for the management decision to revert L2 to 120 minutes.

---

*End of SLA Policy v2 Impact Analysis Report*
*Prepared by: Support Operations Team, NebulaTech*
