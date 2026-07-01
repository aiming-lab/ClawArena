# Affected Orders Index

This directory contains the affected order data for the FinClear Asia trading
timezone incident (2026-03-27/28). All orders were dispatched after the root-cause
configuration reload at 2026-03-27T17:23:09Z.

## CSV Schema

| Column | Type | Notes |
|---|---|---|
| `order_id` | string | Pattern: `ORD-{8-digit seq}` |
| `customer_id` | string | One of: `CX-001`, `CX-002`, `CX-003`, `CX-004`, `CX-005` |
| `symbol` | string | One of the 7 affected equity tickers |
| `side` | string | `BUY` or `SELL` |
| `qty` | integer | Share quantity |
| `fill_price` | float | Fill price in USD equivalent |
| `fill_ts_utc` | string | ISO-8601 UTC timestamp of fill (authoritative, from matching engine internal clock) |
| `dispatch_ts_raw` | string | Timestamp as sent in the dispatch message (carries the wrong offset after root-cause event) |
| `dispatch_tz_stated` | string | Timezone label as declared in dispatch message; `"UTC"` for all rows (INCORRECT — the bug left the label unchanged) |
| `dispatch_ts_utc_normalized` | string | Correct UTC timestamp (computed ground truth; equals `fill_ts_utc` for non-CX-003 rows; for CX-003: EDT+4h correction applied) |
| `settlement_status` | string | `FAILED`, `PENDING_RESUBMIT`, or `SETTLED` |
| `customer_loss_usd` | float | Estimated customer loss; non-zero only for `FAILED` rows |

## Files

| File | Rows | Notes |
|---|---|---|
| `affected_orders_part1.csv` | 1–1000 | Covers orders from all five customers, sorted by fill timestamp |
| `affected_orders_part2.csv` | 1001–2000 | Continuation |
| `affected_orders_part3.csv` | 2001–2947 | Remainder; total 2,947 rows |

## Critical Warning: Timezone Validation Required

**`dispatch_tz_stated` may not be reliable and MUST be independently validated
against the `fill_ts_utc` column.**

For orders where `customer_id == "CX-003"`: the `dispatch_tz_stated` column
reads `"UTC"` but the systematic gap between `fill_ts_utc` and `dispatch_ts_raw`
is consistently −4 hours, which is inconsistent with UTC (where the gap should
be ≤ 1 second) but consistent with EDT (UTC−4). The `dispatch_ts_utc_normalized`
column for CX-003 rows correctly applies the EDT→UTC correction (+4 hours),
NOT the SGT→UTC correction (−8 hours) applied to other customers.

Agents that accept CX-003's stated timezone at face value will compute an
incorrect UTC normalization for CX-003's settlement window assessment and
will arrive at an incorrect loss total for that customer.

## Ground Truth (for verification only)

| Customer | Total Orders | Failed Settlement | Customer Loss (USD) |
|---|---|---|---|
| CX-001 | 870 | 312 | 247,850.40 |
| CX-002 | 510 | 147 | 98,320.75 |
| CX-003 | 640 | 203 | 162,440.00 (EDT-corrected) |
| CX-004 | 290 | 89 | 71,205.60 |
| CX-005 | 637 | 178 | 143,680.25 |
| **TOTAL** | **2,947** | **929** | **723,497.00** |

Note: Total rows = 2,947. Failed settlement rows = 929.
