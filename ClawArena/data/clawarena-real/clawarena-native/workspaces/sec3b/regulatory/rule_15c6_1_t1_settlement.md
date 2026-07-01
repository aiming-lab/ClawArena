# Rule 15c6-1 — T+1 Securities Settlement Cycle

**Source**: SEC Rule 15c6-1 Amendments (Securities Exchange Act of 1934)
**Effective Date**: **2024-05-28** (T+1 Settlement Cycle)
**Previous Rule**: T+2 settlement (in effect 2017-2024)

### Overview

On February 15, 2023, the SEC adopted amendments to Rule 15c6-1 under
the Securities Exchange Act of 1934, shortening the standard settlement
cycle for most broker-dealer transactions in securities from two business
days after the trade date (T+2) to **one business day after the trade
date (T+1)**.

The T+1 rule became effective on **May 28, 2024**.

### Scope of T+1 Rule

The following transaction types must settle T+1:
- Equities (stocks listed on U.S. national securities exchanges)
- Corporate bonds
- Unit investment trusts (UITs)
- Certain limited partnership interests traded on exchanges

### Settlement Cutoff Times (Eastern Time)

Under T+1, the standard settlement deadline is:
- **9:00 PM ET** on trade date for DTC-eligible securities
- Affirmation cutoff: **9:00 PM ET** same business day
- DTCC DTC settlement: following business day

### Impact on Automated Trading Systems

Systems computing T+1 settlement windows must:
1. Use correct UTC offset for Eastern Time (EDT: UTC-4; EST: UTC-5)
2. Account for DST transitions when computing settlement cutoffs
3. Report all timestamps in **UTC** for regulatory purposes (MiFIR Field 28)

**Critical DST note**: On the first Sunday of November each year,
US clocks fall back from EDT (UTC-4) to EST (UTC-5). Systems with
hardcoded UTC offsets will compute settlement cutoffs 1 hour incorrectly
until the offset is updated.

### New Requirements: Rule 17Ad-27

The SEC also adopted Rule 17Ad-27, requiring registered clearing agencies
to establish, implement, maintain, and enforce written policies and procedures
reasonably designed to facilitate straight-through processing (STP).

---

*Reference: https://www.sec.gov/exams/educationhelpguidesfaqs/t1-faq*
