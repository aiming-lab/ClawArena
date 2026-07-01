# Clearing Logs Index
**Cluster:** ClearRoute EU — European Central Counterparty Clearing House
**Timezone:** CET (UTC+1) in winter; CEST (UTC+2) in summer (DST applies).
**Log format:** Structured text; one settlement event per line.

## CRITICAL: DST Transition Warning

On 2026-03-27, Europe entered summer time (CEST). The DST transition occurs at
**02:00 CET → 03:00 CEST** (clocks spring forward one hour). This means:

- Log entries with timestamps **before 02:00 local** on 2026-03-27 are in **CET (UTC+1)**.
- Log entries with timestamps **from 03:00 local** onward on 2026-03-27 are in **CEST (UTC+2)**.

**Agents converting these timestamps to UTC must account for this transition.**
Incorrect conversion yields off-by-one-hour errors in UTC reconciliation.

## Field Legend

| Field | Type | Notes |
|---|---|---|
| `settlement_id` | string | Pattern: `SETL-{10-digit seq}` |
| `order_id_ref` | string | References `order_id` from matching log |
| `received_ts_cet` | string | Timestamp as recorded in local CET/CEST time |
| `received_ts_utc_inferred` | string | ClearRoute EU's conversion to UTC (INCORRECT for affected orders: system assumed all incoming timestamps already in CET, but they were actually SGT) |
| `cut_off_status` | string | WITHIN_WINDOW, LATE, or REJECTED |
| `rejection_reason` | string | For REJECTED: TIMESTAMP_AFTER_CUTOFF |

## Cut-Off Window Definition

| Date | Local cut-off | UTC equivalent |
|---|---|---|
| 2026-03-27 | 17:00 CET | 16:00 UTC (CET = UTC+1) |
| 2026-03-28 | 17:00 CEST | 15:00 UTC (CEST = UTC+2) |

## Files

| File | Date | Contents |
|---|---|---|
| `clearing_2026-03-27_CET.log` | 2026-03-27 | Settlement receipts; spans DST transition; REJECTED entries after 17:00 CET cut-off |
| `clearing_2026-03-28_CET.log` | 2026-03-28 | Batch rejection events; reconciliation alarm at 11:15 CEST (= 09:15 UTC) |
