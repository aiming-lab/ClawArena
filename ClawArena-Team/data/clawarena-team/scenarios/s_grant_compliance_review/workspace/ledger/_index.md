# Ledger — Index

## File: `reimbursements_fy2025.csv`

**Rows:** 310
**Period:** FY2025 (1 January 2025 — 31 December 2025)

### Column Schema

| Column | Type | Description |
|---|---|---|
| `txn_id` | string | Transaction ID; format `{GRANTOR_PREFIX}-{4-digit seq}`; prefixes: GRA (Grantor A / Halcyon), GRB (Grantor B / Nordic), GRC (Grantor C / Opal City) |
| `grantor_id` | string | One of: `halcyon`, `nordic`, `opal_city` |
| `date` | string | ISO date `YYYY-MM-DD` |
| `vendor` | string | Vendor or supplier name |
| `category` | string | Expenditure category code (see legend below) |
| `amount_usd` | float | USD equivalent amount |
| `receipt_ref` | string | Receipt image reference (RCP-001 through RCP-008, or RCP-NONE) |
| `approval_flag` | string | `approved`, `pending`, or `flagged` |
| `notes` | string | Free-text justification or contextual note |

### Category Codes

| Code | Description |
|---|---|
| `travel_intl` | International travel (flights, etc.) |
| `travel_domestic` | Domestic travel |
| `accommodation` | Hotel and per diem accommodation |
| `training` | Training events, materials, facilitation |
| `equipment` | Equipment and hardware purchases |
| `stationery` | Stationery and office consumables |
| `catering` | Event catering and hospitality |
| `entertainment` | Entertainment (note: may be ineligible under some grants) |
| `indirect_admin` | Indirect / overhead cost recovery |
| `venue_hire` | Venue hire for workshops and meetings |
| `audit_fees` | External audit fees |

### Currency Note

All amounts are expressed in USD equivalent, converted at the prevailing mid-market rate on the date of expenditure. NOK-denominated transactions have been converted at the applicable Bank of Norway reference rate.
