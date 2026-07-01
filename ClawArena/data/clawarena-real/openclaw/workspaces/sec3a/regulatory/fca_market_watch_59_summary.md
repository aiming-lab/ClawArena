# FCA Market Watch 59 — MiFIR Transaction Reporting: Key Observations
## Summary for Compliance Reference

**Publication date**: April 2019
**Jurisdiction**: UK / FCA (Financial Conduct Authority)
**Topic**: MiFIR transaction reporting compliance issues, including DST/UTC timestamp errors

---

## Overview

FCA Market Watch 59 documents common compliance failures observed in MiFIR transaction
reporting. A significant proportion of observations relate to the incorrect handling of
timezone offsets — particularly around Daylight Saving Time (DST) transitions.

---

## Critical Finding: Field 28 — Trading Date and Time

### Requirement

**Field 28** of the MiFIR transaction report (the "trading date and time" field) **must be
reported in UTC** (Coordinated Universal Time), not in local time. This requirement is
established by MiFIR Article 26 and the associated Regulatory Technical Standard 22 (RTS 22).

The FCA specifically identified the following recurring error pattern:

> "A number of firms have been found to be reporting timestamps in Field 28 using local time
> (or local time adjusted for DST) rather than UTC. This constitutes a material reporting error
> under MiFIR Article 26 and RTS 22."

### DST Transition Errors

The FCA observed that firms commonly made Field 28 errors during Daylight Saving Time (DST)
transitions, specifically:

1. **British Summer Time (BST) to GMT transition** (UK clocks go back one hour in late October):
   Firms continued to report timestamps at UTC+1 (BST) after the transition to UTC+0 (GMT),
   resulting in a one-hour offset error.

2. **Reverse error at spring transitions**: Firms that had hard-coded UTC offsets failed to
   update them at the spring DST transition.

### Impact and Regulatory Risk

Firms that report Field 28 incorrectly face:
- Regulatory inquiries and formal data quality warnings
- Potential FCA supervisory action under MiFIR Article 26
- Requirement to resubmit corrected transaction reports

---

## Recommended Controls

The FCA recommended that firms:
1. Use NTP-synchronised UTC timestamps directly from exchange matching engines
2. Avoid hard-coding timezone offsets in trading or reporting systems
3. Test timezone handling at each DST transition (both spring and autumn)
4. Implement automated timestamp validation that flags UTC-offset fields

---

## Connection to AROS Incident

The ArtemisQ Capital AROS v4.2 incident of November 3, 2024 exhibits the same error pattern:
a hard-coded UTC-4 offset was not updated when US clocks transitioned from EDT (UTC-4) to
EST (UTC-5), causing Field 28 reports to be submitted with an incorrect one-hour offset.
This falls precisely within the FCA Market Watch 59 category of DST transition errors.

---

*Source: https://www.fca.org.uk/publication/newsletters/market-watch-59.pdf*
