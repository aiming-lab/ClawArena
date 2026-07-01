# L2 SLA Revert Impact Analysis and Post-Revert Operations Guide
**Prepared by:** Dave Park (Compliance) + Alice Wong (Support Ops)
**Date:** 2026-04-06
**Subject:** Impact of reverting L2 from 90 min back to 120 min

**Ref:** FEISHU-PRD4-L2-REVERT

## 1. Background

Following the issuance of management notice FEISHU-PRD4-L2-REVERT on 2026-04-06,
the L2 response SLA has been reverted from 90 minutes (introduced in sla_matrix_v2,
effective 2025-02-01) back to 120 minutes (the original Atlassian Enterprise baseline).

This document:
1. Explains the supersede chain and the authoritative interpretation
2. Provides re-analysis guidance for Q4 2024 breach calculations
3. Documents the data patch requirements (tickets_patch_001.json)
4. Provides the final v3 breach analysis methodology

---

## 2. Supersede Chain Summary

The following sequence of policy changes applies:

```
[v1] L2 = 120 min (effective 2024-01-01)
  ↓ superseded by:
[v2] L2 = 90 min (effective 2025-02-01, via sla_matrix_v2.json)
  ↓ superseded by:
[FEISHU-PRD4-L2-REVERT] L2 = 120 min (effective immediately, via feishu notice)
```

**Current status:** L2 = 120 minutes. The v2 change has been superseded.

**Key principle:** When calculating SLA compliance, use the policy version in force
AT THE TIME OF THE TICKET CREATION, not the current policy version.

Since all Q4 2024 and Q1 2025 tickets were created before the v2 update (2025-02-01),
they should use v1 (L2=120min) for the primary analysis.
After FEISHU-PRD4-L2-REVERT, revert any v2-based analyses back to 120min.

---

## 3. Data Patch Application (tickets_patch_001.json)

Simultaneously with the L2 revert, `tickets_patch_001.json` corrects 15 tickets
in the Q4 2024 batch that had data entry errors in `first_response_at`.

### 3.1 Patch Summary

- 15 tickets patched
- 5 tickets corrected from breach → compliant status
- 10 tickets have corrected timestamps but remain in breach

### 3.2 Patched Ticket Analysis

After applying patches:

| Category | Before Patch | After Patch | Delta |
|---|---|---|---|
| Q4 Total breaches (v1/v3) | 28 | 23 | -5 |
| Q4 Total tickets | 200 | 200 | 0 |
| Q4 Compliance rate | 86.00% | 88.50% | +2.50% |

### 3.3 Breach Tickets v3 Format

The output `breach_tickets_Q4_v3.json` must:
1. Apply the data corrections from tickets_patch_001.json
2. Use L2=120min (v3/reverted — same as v1)
3. Recalculate breach status for all 15 patched tickets
4. Include only tickets that REMAIN in breach after patches

---

## 4. Q4 v3 Expected Breach Counts

After applying both the L2 revert (back to 120min) and the data patch:

| Severity | Total Tickets | Breaches (v1, pre-patch) | After Patch (v3) |
|---|---|---|---|
| L1 | ~50 | 10 | 5 (5 were data errors, now corrected) |
| L2 | ~55 | 8 | 8 (no patch corrections apply to L2 breaches >120min) |
| L3 | ~56 | 6 | 6 |
| L4 | ~43 | 4 | 4 |
| **Total** | **200** | **28** | **23** |

Note: The 5 corrections are from the first 5 entries in tickets_patch_001.json.
Verify the exact ticket IDs against the patch file.

---

## 5. Validation Requirements for v3 Analysis

### 5.1 script validate_ticket_sla.py

Use `scripts/validate_ticket_sla.py` to validate breach_tickets_Q4_v3.json:

```bash
python scripts/validate_ticket_sla.py output/breach_tickets_Q4_v3.json
```

Expected output structure:
```json
{
  "validated_count": <int>,
  "error_count": 0,
  "invalid_ticket_ids": []
}
```

- `validated_count + error_count = total tickets in breach file`
- `error_count` should be 0 if all patches applied correctly

### 5.2 Arithmetic Closure Checks

For each breach ticket entry:
- `breach_delta_min = actual_response_min - expected_response_min`
- `expected_response_min` for L2 tickets = **120** (NOT 90)
- `actual_response_min` must match the corrected value from patch where applicable

---

## 6. Combined Summary Impact

### 6.1 Effect on Q10 Combined Breach Summary

After all corrections and reverts, the combined Q4+Q1 summary must reflect:

| Metric | Value |
|---|---|
| Q4 total tickets | 200 |
| Q4 breaches (v3, post-patch) | 23 |
| Q1 total tickets | 150 |
| Q1 breaches (v1 = same as v3) | 19 |
| **Combined total tickets** | **350** |
| **Combined total breaches** | **42** |
| **Combined breach_pct** | **12.00%** |

### 6.2 Effect on November 2024 Monthly Report

The formal escalation report for November 2024 covers only the Q4 batch tickets
from that month. The exact ticket count and breach count will differ from the full
Q4 batch totals. See `reports/monthly_sla_report_2024_11.md` for the November subset.

---

## 7. Policy Update Communication History

### 7.1 Official Communication Log

| Date | From | To | Subject | Key Message |
|---|---|---|---|---|
| 2025-02-01 | Alice Wong | All Support | sla_matrix_v2 effective | L2 changes to 90min |
| 2026-04-02 | Alice Wong | Bob Chen (DM) | L2 proposal discussion | Still proposal, use v1 |
| 2026-04-06 | Dave Park | Feishu group | FEISHU-PRD4-L2-REVERT | L2 reverts to 120min |

### 7.2 Session Evidence References

| Session | Ref | Content |
|---|---|---|
| Slack DM Alice-Bob | 2026-04-02T14:35Z | Alice confirms v1 applies until v2 officially issued |
| Feishu #support-ops-management | FEISHU-PRD4-L2-REVERT | Official revert notice |

---

## Appendix A: Full Comparison Table — v1/v2/v3

| Field | v0 (ARCHIVED) | v1 | v2 (interim) | v3/reverted |
|---|---|---|---|---|
| L1 | 60 min ERROR | 30 min | 30 min | **30 min** |
| L2 | 120 min | 120 min | 90 min (superseded) | **120 min** |
| L3 | 480 min | 480 min | 480 min | **480 min** |
| L4 | 1440 min | 1440 min | 1440 min | **1440 min** |
| Status | ARCHIVED | Superseded by v2 | Superseded by revert | **CURRENT** |

---

## Appendix B: Re-analysis Checklist

For engineers re-running breach analysis after the L2 revert:

- [ ] Confirm you have read FEISHU-PRD4-L2-REVERT notice
- [ ] Confirm L2 threshold = 120 min (not 90 min)
- [ ] Apply tickets_patch_001.json corrections before running analysis
- [ ] For each patched ticket, use corrected_response_minutes (not original)
- [ ] Re-evaluate breach status for all 15 patched tickets
- [ ] Output breach_tickets_Q4_v3.json (not _v2)
- [ ] Verify: total_tickets_in_v3 = correct count (not all 200)
- [ ] Verify arithmetic: breach_delta_min = actual - expected for each entry

---

## Appendix C: tickets_patch_001 Application Worked Example

### Original Ticket (before patch)

```json
{
  "ticket_id": "Q4-L1-BREACH-001",
  "severity": "L1",
  "created_at": "2024-10-01T08:00:00Z",
  "first_response_at": "2024-10-01T08:40:00Z",
  "response_minutes": 40,
  "sla_threshold": 30
}
```

### Patch Entry

```json
{
  "ticket_id": "Q4-L1-BREACH-001",
  "patch_reason": "data_entry_correction",
  "original_first_response_at": "2024-10-01T08:40:00Z",
  "corrected_first_response_at": "2024-10-01T08:25:00Z",
  "original_response_minutes": 40,
  "corrected_response_minutes": 25
}
```

### After Patch Application

```json
{
  "ticket_id": "Q4-L1-BREACH-001",
  "severity": "L1",
  "created_at": "2024-10-01T08:00:00Z",
  "first_response_at": "2024-10-01T08:25:00Z",
  "response_minutes": 25,
  "sla_threshold": 30,
  "sla_status": "PASS"  // Was BREACH before patch
}
```

This ticket is now COMPLIANT (25 min < 30 min threshold) and should be EXCLUDED
from breach_tickets_Q4_v3.json.

---

*End of L2 SLA Revert Impact Analysis*
*Reference: FEISHU-PRD4-L2-REVERT*
*Next review: Upon next policy update*

## Appendix D: Historical Ticket Impact Traces
The following traces document the analysis path for key tickets across all policy versions.

### Trace 001: L4 ticket, response=37min
- Created: 2024-11-01T13:00:00Z
- Response: 37 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 002: L4 ticket, response=64min
- Created: 2024-11-12T00:00:00Z
- Response: 64 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 003: L3 ticket, response=195min
- Created: 2024-10-16T08:00:00Z
- Response: 195 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 004: L3 ticket, response=134min
- Created: 2024-10-04T10:00:00Z
- Response: 134 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 005: L1 ticket, response=152min
- Created: 2024-12-17T14:00:00Z
- Response: 152 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 006: L2 ticket, response=39min
- Created: 2024-10-05T22:00:00Z
- Response: 39 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **PASS**
- v3 (120min threshold, same as v1): **PASS**

### Trace 007: L3 ticket, response=171min
- Created: 2024-12-06T00:00:00Z
- Response: 171 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 008: L3 ticket, response=119min
- Created: 2024-10-25T09:00:00Z
- Response: 119 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 009: L4 ticket, response=40min
- Created: 2024-10-05T13:00:00Z
- Response: 40 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 010: L4 ticket, response=117min
- Created: 2024-11-24T18:00:00Z
- Response: 117 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 011: L3 ticket, response=40min
- Created: 2024-12-06T10:00:00Z
- Response: 40 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 012: L2 ticket, response=94min
- Created: 2024-10-06T05:00:00Z
- Response: 94 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **PASS**
  → This ticket changes status between v1 and v2!

### Trace 013: L3 ticket, response=141min
- Created: 2024-10-26T07:00:00Z
- Response: 141 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 014: L2 ticket, response=105min
- Created: 2024-10-08T10:00:00Z
- Response: 105 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **PASS**
  → This ticket changes status between v1 and v2!

### Trace 015: L1 ticket, response=37min
- Created: 2024-11-03T14:00:00Z
- Response: 37 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 016: L3 ticket, response=142min
- Created: 2024-11-24T11:00:00Z
- Response: 142 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 017: L2 ticket, response=99min
- Created: 2024-10-06T16:00:00Z
- Response: 99 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **PASS**
  → This ticket changes status between v1 and v2!

### Trace 018: L3 ticket, response=188min
- Created: 2024-11-21T12:00:00Z
- Response: 188 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 019: L3 ticket, response=63min
- Created: 2024-10-06T10:00:00Z
- Response: 63 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 020: L3 ticket, response=198min
- Created: 2024-12-16T03:00:00Z
- Response: 198 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 021: L3 ticket, response=98min
- Created: 2024-11-15T18:00:00Z
- Response: 98 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 022: L3 ticket, response=76min
- Created: 2024-11-09T22:00:00Z
- Response: 76 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 023: L2 ticket, response=179min
- Created: 2024-11-02T15:00:00Z
- Response: 179 minutes
- v1 (120min threshold): **BREACH**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **BREACH**

### Trace 024: L2 ticket, response=98min
- Created: 2024-11-05T22:00:00Z
- Response: 98 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **PASS**
  → This ticket changes status between v1 and v2!

### Trace 025: L1 ticket, response=198min
- Created: 2024-10-21T10:00:00Z
- Response: 198 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 026: L1 ticket, response=123min
- Created: 2024-11-05T03:00:00Z
- Response: 123 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 027: L4 ticket, response=56min
- Created: 2024-11-04T09:00:00Z
- Response: 56 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 028: L2 ticket, response=198min
- Created: 2024-10-26T18:00:00Z
- Response: 198 minutes
- v1 (120min threshold): **BREACH**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **BREACH**

### Trace 029: L4 ticket, response=75min
- Created: 2024-11-12T21:00:00Z
- Response: 75 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 030: L3 ticket, response=92min
- Created: 2024-10-27T17:00:00Z
- Response: 92 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 031: L2 ticket, response=169min
- Created: 2024-10-15T13:00:00Z
- Response: 169 minutes
- v1 (120min threshold): **BREACH**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **BREACH**

### Trace 032: L3 ticket, response=29min
- Created: 2024-10-29T14:00:00Z
- Response: 29 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 033: L1 ticket, response=164min
- Created: 2024-10-07T12:00:00Z
- Response: 164 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 034: L2 ticket, response=49min
- Created: 2024-10-08T06:00:00Z
- Response: 49 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **PASS**
- v3 (120min threshold, same as v1): **PASS**

### Trace 035: L3 ticket, response=159min
- Created: 2024-10-09T12:00:00Z
- Response: 159 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 036: L2 ticket, response=48min
- Created: 2024-11-03T09:00:00Z
- Response: 48 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **PASS**
- v3 (120min threshold, same as v1): **PASS**

### Trace 037: L2 ticket, response=164min
- Created: 2024-11-01T04:00:00Z
- Response: 164 minutes
- v1 (120min threshold): **BREACH**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **BREACH**

### Trace 038: L4 ticket, response=133min
- Created: 2024-12-03T17:00:00Z
- Response: 133 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 039: L4 ticket, response=135min
- Created: 2024-11-11T04:00:00Z
- Response: 135 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 040: L4 ticket, response=21min
- Created: 2024-10-02T14:00:00Z
- Response: 21 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 041: L4 ticket, response=172min
- Created: 2024-10-27T23:00:00Z
- Response: 172 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 042: L3 ticket, response=65min
- Created: 2024-12-21T01:00:00Z
- Response: 65 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 043: L2 ticket, response=50min
- Created: 2024-12-09T21:00:00Z
- Response: 50 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **PASS**
- v3 (120min threshold, same as v1): **PASS**

### Trace 044: L2 ticket, response=148min
- Created: 2024-10-13T21:00:00Z
- Response: 148 minutes
- v1 (120min threshold): **BREACH**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **BREACH**

### Trace 045: L1 ticket, response=147min
- Created: 2024-11-11T20:00:00Z
- Response: 147 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 046: L3 ticket, response=145min
- Created: 2024-10-24T21:00:00Z
- Response: 145 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 047: L4 ticket, response=127min
- Created: 2024-11-04T05:00:00Z
- Response: 127 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 048: L3 ticket, response=199min
- Created: 2024-12-16T00:00:00Z
- Response: 199 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 049: L2 ticket, response=48min
- Created: 2024-11-05T02:00:00Z
- Response: 48 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **PASS**
- v3 (120min threshold, same as v1): **PASS**

### Trace 050: L4 ticket, response=88min
- Created: 2024-10-12T18:00:00Z
- Response: 88 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 051: L3 ticket, response=187min
- Created: 2024-10-04T07:00:00Z
- Response: 187 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 052: L2 ticket, response=106min
- Created: 2024-12-22T04:00:00Z
- Response: 106 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **PASS**
  → This ticket changes status between v1 and v2!

### Trace 053: L3 ticket, response=103min
- Created: 2024-12-16T17:00:00Z
- Response: 103 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 054: L4 ticket, response=123min
- Created: 2024-11-19T08:00:00Z
- Response: 123 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 055: L3 ticket, response=85min
- Created: 2024-10-21T09:00:00Z
- Response: 85 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 056: L2 ticket, response=153min
- Created: 2024-10-16T20:00:00Z
- Response: 153 minutes
- v1 (120min threshold): **BREACH**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **BREACH**

### Trace 057: L2 ticket, response=169min
- Created: 2024-11-20T05:00:00Z
- Response: 169 minutes
- v1 (120min threshold): **BREACH**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **BREACH**

### Trace 058: L3 ticket, response=157min
- Created: 2024-11-26T08:00:00Z
- Response: 157 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 059: L3 ticket, response=33min
- Created: 2024-12-22T02:00:00Z
- Response: 33 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 060: L1 ticket, response=123min
- Created: 2024-10-06T08:00:00Z
- Response: 123 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 061: L3 ticket, response=170min
- Created: 2024-11-09T13:00:00Z
- Response: 170 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 062: L1 ticket, response=123min
- Created: 2024-12-26T11:00:00Z
- Response: 123 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 063: L3 ticket, response=153min
- Created: 2024-11-01T19:00:00Z
- Response: 153 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 064: L2 ticket, response=160min
- Created: 2024-12-09T06:00:00Z
- Response: 160 minutes
- v1 (120min threshold): **BREACH**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **BREACH**

### Trace 065: L2 ticket, response=86min
- Created: 2024-11-02T12:00:00Z
- Response: 86 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **PASS**
- v3 (120min threshold, same as v1): **PASS**

### Trace 066: L3 ticket, response=169min
- Created: 2024-10-29T13:00:00Z
- Response: 169 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 067: L1 ticket, response=152min
- Created: 2024-11-01T00:00:00Z
- Response: 152 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 068: L2 ticket, response=84min
- Created: 2024-11-08T00:00:00Z
- Response: 84 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **PASS**
- v3 (120min threshold, same as v1): **PASS**

### Trace 069: L1 ticket, response=157min
- Created: 2024-10-21T14:00:00Z
- Response: 157 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 070: L3 ticket, response=68min
- Created: 2024-12-22T05:00:00Z
- Response: 68 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 071: L1 ticket, response=178min
- Created: 2024-10-30T00:00:00Z
- Response: 178 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 072: L3 ticket, response=135min
- Created: 2024-12-05T22:00:00Z
- Response: 135 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 073: L4 ticket, response=34min
- Created: 2024-10-11T07:00:00Z
- Response: 34 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 074: L4 ticket, response=106min
- Created: 2024-10-18T01:00:00Z
- Response: 106 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 075: L3 ticket, response=190min
- Created: 2024-10-23T14:00:00Z
- Response: 190 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 076: L1 ticket, response=150min
- Created: 2024-11-25T12:00:00Z
- Response: 150 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 077: L4 ticket, response=27min
- Created: 2024-10-26T08:00:00Z
- Response: 27 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 078: L4 ticket, response=88min
- Created: 2024-10-08T11:00:00Z
- Response: 88 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 079: L2 ticket, response=118min
- Created: 2024-11-02T14:00:00Z
- Response: 118 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **PASS**
  → This ticket changes status between v1 and v2!

### Trace 080: L3 ticket, response=54min
- Created: 2024-10-29T00:00:00Z
- Response: 54 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 081: L4 ticket, response=30min
- Created: 2024-11-06T18:00:00Z
- Response: 30 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 082: L4 ticket, response=33min
- Created: 2024-10-27T14:00:00Z
- Response: 33 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 083: L3 ticket, response=153min
- Created: 2024-12-03T01:00:00Z
- Response: 153 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 084: L2 ticket, response=65min
- Created: 2024-12-21T14:00:00Z
- Response: 65 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **PASS**
- v3 (120min threshold, same as v1): **PASS**

### Trace 085: L4 ticket, response=36min
- Created: 2024-10-09T05:00:00Z
- Response: 36 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 086: L2 ticket, response=200min
- Created: 2024-12-17T18:00:00Z
- Response: 200 minutes
- v1 (120min threshold): **BREACH**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **BREACH**

### Trace 087: L1 ticket, response=67min
- Created: 2024-12-19T03:00:00Z
- Response: 67 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 088: L1 ticket, response=159min
- Created: 2024-10-14T02:00:00Z
- Response: 159 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 089: L2 ticket, response=20min
- Created: 2024-11-09T01:00:00Z
- Response: 20 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **PASS**
- v3 (120min threshold, same as v1): **PASS**

### Trace 090: L2 ticket, response=79min
- Created: 2024-12-16T17:00:00Z
- Response: 79 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **PASS**
- v3 (120min threshold, same as v1): **PASS**

### Trace 091: L2 ticket, response=108min
- Created: 2024-11-27T06:00:00Z
- Response: 108 minutes
- v1 (120min threshold): **PASS**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **PASS**
  → This ticket changes status between v1 and v2!

### Trace 092: L3 ticket, response=163min
- Created: 2024-10-10T22:00:00Z
- Response: 163 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 093: L1 ticket, response=58min
- Created: 2024-10-23T15:00:00Z
- Response: 58 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 094: L1 ticket, response=70min
- Created: 2024-11-09T21:00:00Z
- Response: 70 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 095: L4 ticket, response=139min
- Created: 2024-11-24T20:00:00Z
- Response: 139 minutes
- v1 (1440min threshold): **PASS**
- v2 (1440min threshold): **PASS**
- v3 (1440min threshold, same as v1): **PASS**

### Trace 096: L1 ticket, response=175min
- Created: 2024-10-16T00:00:00Z
- Response: 175 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 097: L3 ticket, response=34min
- Created: 2024-12-06T20:00:00Z
- Response: 34 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 098: L3 ticket, response=73min
- Created: 2024-11-12T14:00:00Z
- Response: 73 minutes
- v1 (480min threshold): **PASS**
- v2 (480min threshold): **PASS**
- v3 (480min threshold, same as v1): **PASS**

### Trace 099: L1 ticket, response=35min
- Created: 2024-12-29T04:00:00Z
- Response: 35 minutes
- v1 (30min threshold): **BREACH**
- v2 (30min threshold): **BREACH**
- v3 (30min threshold, same as v1): **BREACH**

### Trace 100: L2 ticket, response=159min
- Created: 2024-10-20T11:00:00Z
- Response: 159 minutes
- v1 (120min threshold): **BREACH**
- v2 (90min threshold): **BREACH**
- v3 (120min threshold, same as v1): **BREACH**

---
*End of Appendix D*
