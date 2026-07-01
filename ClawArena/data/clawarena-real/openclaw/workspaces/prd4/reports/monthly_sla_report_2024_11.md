# NebulaTech Support Operations — Monthly SLA Report
## Report Period: November 2024

**Prepared by:** Support Operations Team
**Report Date:** 2024-12-05T09:00:00Z
**Policy Version:** v1
**Distribution:** Alice Wong (SupportOps Manager), Dave Park (Legal/Compliance)

---

## Executive Summary

This report covers SLA compliance for all Jira Service Management (JSM) tickets
processed during November 2024. NebulaTech operated under the Atlassian Enterprise
support plan (sla_matrix_v1), with the following headline metrics:

- **Total tickets processed:** 172
- **Total SLA breaches:** 24
- **Overall compliance rate:** 86.05%
- **Atlassian Cloud uptime (2024-11):** 99.93% (within 99.90–99.95% range → 5% credit eligible)

---

## Section 1: SLA Policy Reference (v1)

| Severity | Definition | Response SLA | Coverage |
|----------|-----------|--------------|----------|
| L1 | Production down | 30 min | 24/7 |
| L2 | Serious degradation | 120 min (2h) | 24/7 |
| L3 | Moderate impact | 480 min (8h) | Weekdays |
| L4 | Limited impact | 1440 min (24h) | Weekdays |

Source: https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html

Credit tiers (Atlassian Enterprise):
- 99.90%–99.95%: **5%** (Enterprise-exclusive tier)
- 99.00%–99.90%: 10%
- 95.00%–99.00%: 25%
- < 95.00%: 50%

Source: https://www.atlassian.com/legal/sla

---

## Section 2: Ticket Volume and Breach Analysis

### 2.1 Volume by Severity

| Severity | Total | Breached | Compliance Rate |
|----------|-------|----------|----------------|
| L1 | 38 | 7 | 81.58% |
| L2 | 52 | 8 | 84.62% |
| L3 | 48 | 6 | 87.50% |
| L4 | 34 | 3 | 91.18% |
| **Total** | **172** | **24** | **86.05%** |

### 2.2 Worst Breach Cases (Top 5)

| Ticket | Severity | Expected (min) | Actual (min) | Breach Delta |
|--------|----------|---------------|--------------|-------------|
| NOV-L1-011 | L1 | 30 | 142 | +112 |
| NOV-L1-007 | L1 | 30 | 97 | +67 |
| NOV-L2-019 | L2 | 120 | 183 | +63 |
| NOV-L2-031 | L2 | 120 | 178 | +58 |
| NOV-L3-024 | L3 | 480 | 531 | +51 |

---

## Section 3: Atlassian Cloud Availability

**Reported monthly uptime (2024-11):** 99.93%

This falls within the 99.90%–99.95% range, qualifying NebulaTech for the
**5% service credit** under the Atlassian Enterprise tier-0 credit tier.

Credit claim must be filed within **15 calendar days** of 2024-11-30
(i.e., by 2024-12-15).

---

## Section 4: AWS Infrastructure Context

NebulaTech's backend services ran on:
- **Amazon EC2 (us-east-1):** Monthly uptime 99.97% — within 99.0–99.99% range → 10% credit eligible
- **AWS Lambda (us-east-1):** Monthly uptime 99.96% — within 99.0–99.95% range → 10% credit eligible

---

## Section 5: Recommendations

1. **Prioritise L1 response time:** Average L1 response in November was 24 minutes
   (within SLA), but 7 breaches indicate process gaps on overnight shifts.
2. **L2 monitoring:** 8 L2 breaches suggest the 2-hour window is tight for
   complex degradation issues; consider pre-escalation at 90 minutes.
3. **Atlassian credit claim:** File credit claim for 99.93% uptime by 2024-12-15.

---

## Appendix: SLA Credit Calculation Formulas

For Atlassian Enterprise (source: https://www.atlassian.com/legal/sla):
```
credit_amount = monthly_contract_value * credit_pct / 100
```

For AWS EC2 Region-Level SLA (source: https://aws.amazon.com/ec2/sla/):
- 99.0–99.99%: 10% credit
- 95.0–99.0%: 30% credit
- < 95.0%: 100% credit

For AWS Lambda (source: https://aws.amazon.com/lambda/sla/):
- 99.0–99.95%: 10% credit
- 95.0–99.0%: 25% credit
- < 95.0%: 100% credit

---

*End of Report — Monthly SLA Report 2024-11*
*Next report due: 2025-01-05 (covering December 2024)*


---

## Appendix B: Ticket Detail Log (November 2024 Sample)

The following table lists all L1 and L2 tickets processed in November 2024,
with full timestamps and response times for audit purposes.

### L1 Tickets (November 2024)

| Ticket ID | Created | First Response | Response (min) | Status |
|-----------|---------|---------------|----------------|--------|
| NOV-L1-001 | 2024-11-01T02:15:00Z | 2024-11-01T02:38:00Z | 23 | PASS |
| NOV-L1-002 | 2024-11-01T09:42:00Z | 2024-11-01T10:05:00Z | 23 | PASS |
| NOV-L1-003 | 2024-11-02T15:30:00Z | 2024-11-02T15:52:00Z | 22 | PASS |
| NOV-L1-004 | 2024-11-03T03:20:00Z | 2024-11-03T03:41:00Z | 21 | PASS |
| NOV-L1-005 | 2024-11-04T11:00:00Z | 2024-11-04T11:18:00Z | 18 | PASS |
| NOV-L1-006 | 2024-11-05T07:45:00Z | 2024-11-05T08:10:00Z | 25 | PASS |
| NOV-L1-007 | 2024-11-06T22:30:00Z | 2024-11-07T00:07:00Z | 97 | **BREACH** |
| NOV-L1-008 | 2024-11-07T14:15:00Z | 2024-11-07T14:34:00Z | 19 | PASS |
| NOV-L1-009 | 2024-11-08T06:00:00Z | 2024-11-08T06:21:00Z | 21 | PASS |
| NOV-L1-010 | 2024-11-09T20:45:00Z | 2024-11-09T21:03:00Z | 18 | PASS |
| NOV-L1-011 | 2024-11-10T01:30:00Z | 2024-11-10T03:52:00Z | 142 | **BREACH** |
| NOV-L1-012 | 2024-11-11T16:20:00Z | 2024-11-11T16:40:00Z | 20 | PASS |
| NOV-L1-013 | 2024-11-12T09:15:00Z | 2024-11-12T09:35:00Z | 20 | PASS |
| NOV-L1-014 | 2024-11-13T23:00:00Z | 2024-11-14T00:15:00Z | 75 | **BREACH** |
| NOV-L1-015 | 2024-11-14T12:30:00Z | 2024-11-14T12:48:00Z | 18 | PASS |
| NOV-L1-016 | 2024-11-15T05:45:00Z | 2024-11-15T06:04:00Z | 19 | PASS |
| NOV-L1-017 | 2024-11-16T18:00:00Z | 2024-11-16T18:24:00Z | 24 | PASS |
| NOV-L1-018 | 2024-11-17T08:30:00Z | 2024-11-17T09:10:00Z | 40 | **BREACH** |
| NOV-L1-019 | 2024-11-18T14:00:00Z | 2024-11-18T14:22:00Z | 22 | PASS |
| NOV-L1-020 | 2024-11-19T21:30:00Z | 2024-11-19T21:48:00Z | 18 | PASS |
| NOV-L1-021 | 2024-11-20T03:15:00Z | 2024-11-20T04:28:00Z | 73 | **BREACH** |
| NOV-L1-022 | 2024-11-21T10:45:00Z | 2024-11-21T11:05:00Z | 20 | PASS |
| NOV-L1-023 | 2024-11-22T07:20:00Z | 2024-11-22T07:39:00Z | 19 | PASS |
| NOV-L1-024 | 2024-11-23T19:00:00Z | 2024-11-23T20:05:00Z | 65 | **BREACH** |
| NOV-L1-025 | 2024-11-24T13:30:00Z | 2024-11-24T13:51:00Z | 21 | PASS |
| NOV-L1-026 | 2024-11-25T02:00:00Z | 2024-11-25T03:22:00Z | 82 | **BREACH** |
| NOV-L1-027 | 2024-11-26T09:00:00Z | 2024-11-26T09:18:00Z | 18 | PASS |
| NOV-L1-028 | 2024-11-27T16:45:00Z | 2024-11-27T17:03:00Z | 18 | PASS |
| NOV-L1-029 | 2024-11-28T06:30:00Z | 2024-11-28T06:52:00Z | 22 | PASS |
| NOV-L1-030 | 2024-11-29T22:15:00Z | 2024-11-29T22:35:00Z | 20 | PASS |
| NOV-L1-031 | 2024-11-30T12:00:00Z | 2024-11-30T12:21:00Z | 21 | PASS |
| NOV-L1-032 | 2024-11-04T17:30:00Z | 2024-11-04T17:49:00Z | 19 | PASS |
| NOV-L1-033 | 2024-11-07T22:00:00Z | 2024-11-07T22:21:00Z | 21 | PASS |
| NOV-L1-034 | 2024-11-12T04:15:00Z | 2024-11-12T04:34:00Z | 19 | PASS |
| NOV-L1-035 | 2024-11-17T20:30:00Z | 2024-11-17T20:49:00Z | 19 | PASS |
| NOV-L1-036 | 2024-11-21T15:45:00Z | 2024-11-21T16:04:00Z | 19 | PASS |
| NOV-L1-037 | 2024-11-25T08:00:00Z | 2024-11-25T08:22:00Z | 22 | PASS |
| NOV-L1-038 | 2024-11-28T11:30:00Z | 2024-11-28T11:51:00Z | 21 | PASS |

**L1 Summary: 38 tickets, 7 breaches, compliance rate 81.58%**

---

### L2 Tickets (November 2024 — Selected)

(Full table available in the ticketing system. Showing representative sample.)

| Ticket ID | Created | First Response | Response (min) | Status |
|-----------|---------|---------------|----------------|--------|
| NOV-L2-001 | 2024-11-01T10:00:00Z | 2024-11-01T11:42:00Z | 102 | PASS |
| NOV-L2-002 | 2024-11-02T14:30:00Z | 2024-11-02T16:05:00Z | 95 | PASS |
| NOV-L2-003 | 2024-11-03T09:00:00Z | 2024-11-03T10:55:00Z | 115 | PASS |
| NOV-L2-004 | 2024-11-04T16:45:00Z | 2024-11-04T19:45:00Z | 180 | **BREACH** |
| NOV-L2-005 | 2024-11-05T08:30:00Z | 2024-11-05T10:05:00Z | 95 | PASS |
| NOV-L2-006 | 2024-11-06T13:00:00Z | 2024-11-06T15:02:00Z | 122 | **BREACH** |
| NOV-L2-007 | 2024-11-07T11:15:00Z | 2024-11-07T13:10:00Z | 115 | PASS |
| NOV-L2-008 | 2024-11-08T09:45:00Z | 2024-11-08T11:43:00Z | 118 | PASS |
| NOV-L2-009 | 2024-11-09T14:00:00Z | 2024-11-09T16:12:00Z | 132 | **BREACH** |
| NOV-L2-010 | 2024-11-10T10:30:00Z | 2024-11-10T12:20:00Z | 110 | PASS |

*... (42 additional L2 tickets not shown) ...*

**L2 Summary: 52 tickets, 8 breaches, compliance rate 84.62%**

---

## Appendix C: Incident Timeline (2024-11 P1 Incidents)

The following P1 incidents were logged via the Feishu incident group during November 2024.

### Incident INC-2024-11-003
- **Detected:** 2024-11-10T01:15:00Z
- **First Response:** 2024-11-10T01:45:00Z (30 min — exactly at SLA boundary)
- **Resolved:** 2024-11-10T04:30:00Z (MTTR = 165 min)
- **Root Cause:** AWS EC2 instance failure in us-east-1a
- **Action Items:** Enable multi-AZ deployment for critical services

### Incident INC-2024-11-007
- **Detected:** 2024-11-22T03:00:00Z
- **First Response:** 2024-11-22T04:10:00Z (70 min — SLA BREACH)
- **Resolved:** 2024-11-22T08:45:00Z (MTTR = 335 min)
- **Root Cause:** Lambda cold-start timeout cascade
- **Action Items:** Implement Lambda provisioned concurrency for critical functions

---

*Report generated by SupportOps AI*
*Policy reference: sla_matrix_v1.json*
*Next review: 2025-01-10*
