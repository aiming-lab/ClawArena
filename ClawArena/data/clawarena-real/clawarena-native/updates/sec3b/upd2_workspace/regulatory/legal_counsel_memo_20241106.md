# Legal Counsel Memorandum — ArtemisQ Capital
## Re: SEC Preliminary Inquiry — Field Specification Revision
## Date: 2024-11-06

**From**: ArtemisQ Capital Legal Counsel (external)
**To**: Elena Vasquez, Chief Compliance Officer
**Re**: Revision to SEC Inquiry Response Field Specification

---

## URGENT — SUPERSEDES PRIOR INSTRUCTION

This memorandum **SUPERSEDES** the field specification in the SEC's
preliminary inquiry letter of 2024-11-05 regarding the calculation method
for price differentials.

### Background

Further review of the SEC preliminary inquiry letter (2024-11-05) confirms:
1. The letter is a **preliminary inquiry notice**, NOT a formal investigation order
2. The "price_diff_usd" field specified in the inquiry should be revised
   to use **VWAP (Volume Weighted Average Price) basis** rather than
   end-of-day closing price, as VWAP provides a more accurate representation
   of execution quality in automated market-making contexts

### Supersede Rule — CRITICAL

**Effective immediately, the field `price_diff_usd` is REPLACED by
`price_diff_vwap_usd` in all affected order reports.**

| Old Field (SUPERSEDED) | New Field (REQUIRED) | Basis |
|------------------------|---------------------|-------|
| `price_diff_usd` | `price_diff_vwap_usd` | VWAP, not closing price |

**Any report using `price_diff_usd` after receipt of this memo is NON-COMPLIANT
with our revised submission specification.**

### Revised Required Fields

For the order-level difference report (Round 11 deliverable), use:
```
order_id, expected_settlement_utc, actual_settlement_utc, price_diff_vwap_usd
```

NOT the old specification:
```
order_id, expected_settlement_utc, actual_settlement_utc, price_diff_usd  ← SUPERSEDED
```

### VWAP Calculation Basis

Price differentials should be calculated as:
`price_diff_vwap_usd = (execution_price - vwap_reference) * quantity`

Where `vwap_reference` is the 5-minute VWAP at the time of the affected order.
For the purposes of this regulatory submission, VWAP values are provided in
the revised field specification document.

---

Legal Counsel
ArtemisQ Capital
2024-11-06T10:00:00Z
