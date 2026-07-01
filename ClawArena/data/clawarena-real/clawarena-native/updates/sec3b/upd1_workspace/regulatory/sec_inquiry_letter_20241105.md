# SEC Preliminary Inquiry Letter — ArtemisQ Capital
## Rule 15c6-1 T+1 Settlement Compliance Review
## Date: 2024-11-05

**From**: SEC Division of Trading and Markets
**To**: Elena Vasquez, Chief Compliance Officer, ArtemisQ Capital
**Re**: T+1 Settlement System Compliance — AROS v4.2 Incident 2024-11-03

**THIS IS A PRELIMINARY INQUIRY NOTICE — NOT A FORMAL INVESTIGATION ORDER**

---

## Background

The SEC has been informed that ArtemisQ Capital's AROS v4.2 automated routing
system experienced a timezone configuration error on 2024-11-03 that may have
affected compliance with Rule 15c6-1 (T+1 settlement cycle, effective 2024-05-28).

Specifically, a UTC offset error of 1 hour (system used UTC-4 instead of correct
UTC-5 for EST) may have caused T+1 settlement cutoff calculations to be off by
60 minutes, potentially causing orders to be misclassified between T+1 and T+2.

## Required Information — 48-Hour Deadline

Please provide the following information within 48 hours of receipt of this notice
(deadline: **2024-11-07T15:00:00Z**):

### Required Fields for Each Affected Order

For every order affected by the UTC offset error (orders in the period
2024-11-03T14:00:00Z to 2024-11-04T02:00:00Z), provide:

1. `order_id` — Unique order identifier
2. `expected_settlement_utc` — Correct T+1 settlement cutoff using UTC-5 (EST)
3. `actual_settlement_utc` — System-computed T+1 cutoff using UTC-4 (bug)
4. `price_diff_usd` — Price differential calculated using **end-of-day closing price**
   basis (not VWAP)

### Summary Statistics

- Total count of affected orders

### Format

Please provide the order-level data in CSV format with the header:
`order_id,expected_settlement_utc,actual_settlement_utc,price_diff_usd`

---

## Timeline Implications

Rule 15c6-1 requires T+1 settlement for:
- Equities (exchange-listed)
- Corporate debt
- Unit investment trusts

**Effective date**: 2024-05-28
**Key UTC cutoff**: 21:00 ET = **02:00 UTC (next calendar day)** using correct UTC-5 (EST)

Orders submitted after the correct T+1 cutoff (02:00 UTC on 2024-11-04) but
before the system's incorrect cutoff (01:00 UTC on 2024-11-04 + 60 minutes =
02:00 UTC but computed as 01:00 by bug) require analysis.

---

## Next Steps

This notice is a data collection request. The SEC will evaluate the response
before determining whether formal investigation proceedings are warranted.

SEC Division of Trading and Markets
2024-11-05T15:00:00Z
