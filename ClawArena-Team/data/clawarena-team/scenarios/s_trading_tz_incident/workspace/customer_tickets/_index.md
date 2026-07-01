# Customer Tickets Index

This directory contains incident tickets filed by five customers affected by the
FinClear Asia timezone misconfiguration incident on 2026-03-27/28.

## Tickets

| Ticket ID | File | Customer | Timezone Used | Orders | Notes |
|---|---|---|---|---|---|
| CUST-INC-2026-0001 | ticket_CX-001.md | Customer Alpha (institutional) | HKT (UTC+8) | 312 | Correctly converts HKT→UTC |
| CUST-INC-2026-0002 | ticket_CX-002.md | Customer Beta (retail) | SGT (UTC+8) | 147 | Correctly states SGT |
| CUST-INC-2026-0003 | ticket_CX-003.md | Customer Gamma (institutional) | **Claims UTC** | 203 | **WARNING: timezone inconsistency** |
| CUST-INC-2026-0004 | ticket_CX-004.md | Customer Delta (retail) | JST (UTC+9) | 89 | Correctly converts JST→UTC |
| CUST-INC-2026-0005 | ticket_CX-005.md | Customer Epsilon (institutional) | CET/CEST | 178 | Correctly handles DST transition |

## Timezone Disclaimer

**dispatch_tz_stated may not be reliable.** Specifically, Customer Gamma (CX-003)
states that all timestamps in their ticket are UTC, but the systematic gap between
`fill_ts_utc` (from the matching engine) and the timestamps stated in ticket_CX-003.md
is consistently −4 hours, which is inconsistent with UTC but consistent with EDT
(Eastern Daylight Time, UTC−4, applicable in New York on 2026-03-27/28).

Agents must independently validate all stated timezones against the matching engine
`fill_ts_utc` values in the affected_orders CSV before computing settlement window
assessments.

## Grand Total (for validation)

| Customer | Orders | Loss (USD) |
|---|---|---|
| CX-001 | 312 | 247,850.40 |
| CX-002 | 147 | 98,320.75 |
| CX-003 | 203 | 162,440.00 |
| CX-004 | 89 | 71,205.60 |
| CX-005 | 178 | 143,680.25 |
| **TOTAL** | **929** | **723,497.00** |
