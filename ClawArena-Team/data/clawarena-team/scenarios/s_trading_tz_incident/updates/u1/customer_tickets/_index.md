# Customer Tickets Index (Updated — Post-u1)

This directory contains incident tickets filed by five customers affected by the
FinClear Asia timezone misconfiguration incident on 2026-03-27/28, plus three
supplemental tickets delivered with the u1 update (attached to q4).

## Original Tickets (Pre-u1)

| Ticket ID | File | Customer | Timezone Used | Orders | Notes |
|---|---|---|---|---|---|
| CUST-INC-2026-0001 | ticket_CX-001.md | Customer Alpha (institutional) | HKT (UTC+8) | 312 | Correctly converts HKT→UTC |
| CUST-INC-2026-0002 | ticket_CX-002.md | Customer Beta (retail) | SGT (UTC+8) | 147 | Correctly states SGT |
| CUST-INC-2026-0003 | ticket_CX-003.md | Customer Gamma (institutional) | **Claims UTC** | 203 | **WARNING: false UTC claim; data is EDT** |
| CUST-INC-2026-0004 | ticket_CX-004.md | Customer Delta (retail) | JST (UTC+9) | 89 | Correctly converts JST→UTC |
| CUST-INC-2026-0005 | ticket_CX-005.md | Customer Epsilon (institutional) | CET/CEST | 178 | Correctly handles DST transition |

## Supplemental Tickets (u1)

| Ticket ID | File | Customer | Key Content |
|---|---|---|---|
| CUST-INC-2026-0003b | ticket_CX-003b.md | Customer Gamma (institutional) | **Again claims UTC; EDT pattern repeats; 4 high-value orders for priority resubmit** |
| CUST-INC-2026-0004b | ticket_CX-004b.md | Customer Delta (retail) | 12 additional disputed orders NOT in affected_orders CSV; correctly stated JST timestamps |
| CUST-INC-2026-0005b | ticket_CX-005b.md | Customer Epsilon (institutional) | DST clarification; confirms ClearRoute EU handled DST correctly; total loss USD 143,680.25 confirmed |

## Timezone Disclaimer

**dispatch_tz_stated may not be reliable.** Customer Gamma (CX-003) has now filed
TWO tickets (original and 003b) both claiming UTC. However, the systematic gap between
`fill_ts_utc` and stated event times is consistently −4 hours, confirming EDT.

The updated SOP v2.0 (in regulatory_templates/sop_timezone_normalization.md, also updated
with u1) explicitly codifies the EDT normalization rule:

> Section 4.3 (NEW in v2.0): EDT (Eastern Daylight Time, UTC-4): all incoming timestamps
> labeled UTC but exhibiting systematic -4h offset from confirmed UTC fill timestamps must
> be treated as mislabeled EDT and corrected by adding 4 hours.

The SOP v2.0 confirms that the q2 analysis applying EDT correction to CX-003 was correct.

## Note on CX-004b Additional Orders

The 12 additional orders in ticket_CX-004b.md do NOT appear in the affected_orders CSV
(which was frozen at the time of the original investigation). These orders should be
noted as "under investigation — not included in q2/q4 totals" in the updated loss summary.
Do NOT add these 12 orders to the FAILED settlement count or total loss figure.

## Grand Total (Unchanged by u1)

| Customer | Failed Orders | Loss (USD) |
|---|---|---|
| CX-001 | 312 | 247,850.40 |
| CX-002 | 147 | 98,320.75 |
| CX-003 | 203 | 162,440.00 (EDT-corrected; not UTC as claimed) |
| CX-004 | 89 | 71,205.60 |
| CX-005 | 178 | 143,680.25 |
| **TOTAL** | **929** | **723,497.00** |

Note: The 12 additional CX-004 orders from ticket_CX-004b are not included in the above total.
