# Rule 15c6-1 — T+1 Settlement Cycle (Amended)
## SEC FAQ: Shortening the Securities Transaction Settlement Cycle

**Amendment effective date**: May 28, 2024
**Prior standard**: T+2 (two business days)
**New standard**: T+1 (one business day)

---

## Overview

The SEC amended Rule 15c6-1 under the Securities Exchange Act of 1934 to require that
most broker-dealer transactions be settled within one business day of the trade date (T+1),
replacing the prior T+2 settlement cycle effective May 28, 2024.

## Scope

Rule 15c6-1 (as amended, effective 2024-05-28) applies to:
- Equity securities transactions
- Corporate debt transactions
- Municipal securities transactions
- Unit investment trust transactions

## Key Deadlines

Under T+1, the standard settlement date is T+1 (the business day following trade date).
For institutional trades, affirmation of trade details must occur by the end of trade date (T)
to ensure timely T+1 settlement.

## Impact of Timezone Errors on T+1 Settlement

The transition to T+1 settlement increased the criticality of accurate timestamp management:

- **Settlement deadline calculation**: With T+2, a 1-hour timestamp error had limited practical
  impact. Under T+1, a 1-hour error in settlement deadline calculation can cause a trade to
  miss the settlement cutoff, triggering a settlement fail.

- **UTC standardisation**: All settlement deadline calculations should use UTC as the reference
  timezone to avoid EDT/EST confusion. A system configured at UTC-4 (EDT) that has not
  transitioned to UTC-5 (EST) will calculate settlement deadlines as 1 hour later than correct,
  potentially causing T+1 settlement fails.

## New Rule 17Ad-27

The amended framework also includes new Rule 17Ad-27, requiring clearing agencies to
establish, implement, maintain, and enforce written policies and procedures reasonably
designed to facilitate straight-through processing (STP) of securities transactions.

---

*Source: https://www.sec.gov/exams/educationhelpguidesfaqs/t1-faq*
