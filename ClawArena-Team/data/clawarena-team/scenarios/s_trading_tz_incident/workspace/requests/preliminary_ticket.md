# Preliminary Detection Report: Settlement Reconciliation Alarm
## Batch Reconciliation Job — Automated Alert
**Job ID:** BATCH-RECON-20260328-0001
**Alarm fired:** 2026-03-28T09:15:00Z
**Severity:** P1 — Critical
**Notified:** RISK_OFFICER, MATCHING_ENG_LEAD, CLEARING_LEAD

---

## Detection Event

At 2026-03-28T09:15:00Z, the overnight batch reconciliation job (BATCH-RECON)
completed its daily comparison of dispatched trade confirmations against
ClearRoute EU settlement receipts. The job detected an anomalous rejection rate
and raised a P1 alert.

**Alarm trigger conditions met:**
- Settlement rejection rate: 31.5% (threshold: 2.0%)
- Total rejected settlement instructions: 2,947
- Affected securities: SGEX, HKFIN, JPNBK, AUHLD, TWSMC, KRSEC, CNTECH
- Rejection reason (from ClearRoute EU): TIMESTAMP_AFTER_CUTOFF (all rejections)

---

## Preliminary Findings from Reconciliation Job

The batch reconciliation job's automated analysis identified the following pattern:

1. **All affected orders were dispatched after 17:23 UTC on 2026-03-27.**
   Orders dispatched before 17:23 UTC on 2026-03-27 settled normally (0% rejection).

2. **All rejected settlement instructions carry the same rejection reason:**
   `TIMESTAMP_AFTER_CUTOFF` — ClearRoute EU records that the submitted timestamp
   was after the 17:00 CET daily cut-off window.

3. **The `tz_offset_applied` field in affected dispatch messages reads `+08:00`.**
   This field should always read `+00:00` for production dispatch messages. The
   batch reconciliation job flagged this as the likely root cause parameter.

4. **DST context:** Europe entered summer time (CEST, UTC+2) on 2026-03-27 at
   02:00 CET local time. The ClearRoute EU cut-off on 2026-03-27 was at 17:00 CET
   (= 16:00 UTC), and on 2026-03-28 the cut-off is at 17:00 CEST (= 15:00 UTC).

5. **Customer tickets received:** As of 09:15 UTC 2026-03-28, five customers
   (CX-001 through CX-005) have filed incident tickets via the customer portal.
   Ticket timestamps are in various local timezones; at least one ticket claims
   timestamps are UTC but may be inconsistent with that claim.

---

## Data Available for Analysis

| Data source | Location | Status |
|---|---|---|
| Matching engine logs (2026-03-27, 2026-03-28) | `matching_engine_logs/` | Available |
| ClearRoute EU clearing logs (2026-03-27, 2026-03-28) | `clearing_logs/` | Available |
| Customer incident tickets (CX-001 to CX-005) | `customer_tickets/` | Available |
| Affected orders CSV (2,947 rows, 3 parts) | `affected_orders/` | Available |
| Regulatory report schema | `regulatory_templates/` | Available |
| Internal ops docs (config history, SOPs, runbook) | `internal_ops/` | Available |
| Internal comms (Slack export, regulator email thread) | `comms/` | Available |

---

## Immediate Actions Required

1. Confirm root-cause event in matching engine logs (exact timestamp and config field).
2. Compute confirmed failed-settlement order count and total customer loss (USD).
3. Determine correct UTC normalization for all five customer timezone contexts.
4. File preliminary regulatory incident report before **2026-03-30T09:15:00Z**.

---

## Do NOT Use

The `_archive/migration_jan_2026/` directory contains logs from the January 2026
cross-datacenter migration. Order IDs in those logs use the `MIG-` prefix and are
entirely unrelated to the current settlement incident. Do not cite any MIG- events
in the post-mortem report.
