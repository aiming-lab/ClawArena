# Revised Order-Level Report Field Specification — v2
## ArtemisQ Capital — SEC Response
## Issued: 2024-11-06 (supersedes v1 specification in SEC inquiry letter 2024-11-05)

---

## SUPERSEDE NOTICE

This document **supersedes** the field specification in the SEC preliminary
inquiry letter dated 2024-11-05. The key change is:

- `price_diff_usd` (closing price basis) → **`price_diff_vwap_usd`** (VWAP basis)

---

## Revised CSV Field Specification (v2)

The order-level difference report must use the following column names EXACTLY:

| Column | Type | Description |
|--------|------|-------------|
| `order_id` | string | Unique order identifier |
| `expected_settlement_utc` | ISO 8601 UTC string | Correct T+1 cutoff (UTC-5, EST) |
| `actual_settlement_utc` | ISO 8601 UTC string | System cutoff (UTC-4 bug) |
| `price_diff_vwap_usd` | float | Price difference using VWAP basis (NOT closing price) |

**Column names must be verbatim. `price_diff_usd` is SUPERSEDED.**

---

## Affected Order Count

Total affected orders (from `incident/affected_orders_detail.csv`): **1200**

---

## VWAP Reference Data

VWAP reference prices for the affected period (2024-11-03T14:00:00Z to 2024-11-03T15:00:00Z):

| 5-min Window Start | ESZ4 VWAP | NQZ4 VWAP |
|--------------------|-----------|-----------|
| 14:00:00Z | 4562.50 | 19840.25 |
| 14:05:00Z | 4563.75 | 19842.00 |
| 14:10:00Z | 4561.00 | 19839.50 |
| 14:15:00Z | 4564.25 | 19843.75 |
| 14:20:00Z | 4565.00 | 19845.00 |
| 14:25:00Z | 4562.25 | 19841.25 |
| 14:30:00Z | 4563.50 | 19840.75 |
| 14:35:00Z | 4564.75 | 19842.50 |
| 14:40:00Z | 4565.25 | 19844.25 |
| 14:45:00Z | 4563.00 | 19841.00 |
| 14:50:00Z | 4562.75 | 19840.50 |
| 14:55:00Z | 4564.00 | 19843.00 |

---

*Version: v2 | Issued: 2024-11-06 | Supersedes: v1 (SEC inquiry letter 2024-11-05)*
