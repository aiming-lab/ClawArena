# DTCC T+1 Settlement Conversion Guide (March 2024 Update)

**Source**: DTCC, "The Move to T+1: Conversion Guide," March 2024
**Reference URL**: https://www.dtcc.com/-/media/Files/PDFs/T2/T1-Conversion-Document-March-2024.pdf

---

## Overview

The US securities settlement cycle shortened from T+2 to T+1 effective
**May 28, 2024** under SEC Rule 15c6-1 (amended February 15, 2023).

## Key Metrics Post-T+1 Transition

| Metric | Pre-T+1 | Post-T+1 (YTD Dec 2024) |
|--------|---------|------------------------|
| Same-day affirmation rate | ~73% | **97%** |
| Fails rate | Baseline | Significantly reduced |
| Settlement cycle | T+2 | T+1 |

## Scope of T+1 Rule

Transactions that must now settle T+1:
- Exchange-listed equities (NYSE, NASDAQ, etc.)
- Corporate debt securities
- Unit investment trusts (UITs)
- Certain limited partnership interests traded on exchanges

Excluded from T+1 (remain T+2 or longer):
- Government securities (already T+1)
- Municipal bonds (separate Rule 15c6-1 provision)
- OTC derivatives

## Settlement Cutoff Times Under T+1

| Milestone | Time (ET) | Impact on UTC calculation |
|-----------|-----------|--------------------------|
| Trade execution | During market hours | Must use correct UTC-4/UTC-5 per season |
| Affirmation cutoff | 21:00 ET same day | UTC = 21:00 + abs(offset) |
| DTC settlement | 16:00 ET next business day | Settlement completion |

**DST impact on cutoff UTC**:
- EDT period (UTC-4): 21:00 ET cutoff = 01:00 UTC next calendar day
- EST period (UTC-5): 21:00 ET cutoff = 02:00 UTC next calendar day

Systems must account for DST transitions when computing settlement cutoffs.
The 1-hour difference between EDT and EST cutoff UTC times can cause orders
to be classified as T+1 vs T+2 incorrectly.

## Rule 17Ad-27 — Straight-Through Processing

The SEC also adopted Rule 17Ad-27, requiring registered clearing agencies
to maintain policies for straight-through processing (STP). DTCC's Target
STP rate post-T+1: maintain ≥97% same-day affirmation.

---

## Relevance to AROS v4.2 Incident

The 2024-11-03 AROS v4.2 incident occurred on the first day of the
post-DST EST period, approximately 5 months after T+1 became effective.
Systems that had adapted for T+1 but did not implement DST-aware UTC
computation faced precisely this scenario: correct T+1 logic but with
1-hour offset in the UTC cutoff calculation.

Reference settlement calculations:
- Trade date: 2024-11-03
- T+1 settlement date: 2024-11-04
- T+1 cutoff (correct, UTC-5 EST): 2024-11-04T02:00:00Z
- T+1 cutoff (wrong, UTC-4 bug): 2024-11-04T01:00:00Z
- Orders submitted between 01:00-02:00 UTC on 2024-11-04: missed T+1 window
  (were classified as T+1 by system, but are actually T+2 under correct calculation)
