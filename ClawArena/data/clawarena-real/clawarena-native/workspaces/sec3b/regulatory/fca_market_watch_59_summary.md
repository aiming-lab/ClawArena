# FCA Market Watch 59 — MiFIR Transaction Reporting Observations

**Source**: Financial Conduct Authority, Market Watch Newsletter Issue 59
**Publication Date**: April 2019
**Reference URL**: https://www.fca.org.uk/publication/newsletters/market-watch-59.pdf

---

## Overview

Market Watch 59 sets out the FCA's observations on common errors in
MiFIR (Markets in Financial Instruments Regulation) transaction reporting.
The newsletter specifically addresses **UTC and DST timestamp compliance issues**
that were identified as a systemic problem across multiple firms.

---

## Field 28: Trading Date and Time — Key Requirements

**Field 28** (trading date & time) is one of the most frequently mis-reported
fields in MiFIR transaction reports submitted to the FCA.

### Mandatory Requirements for Field 28

1. **UTC mandatory**: Field 28 must be reported in **Coordinated Universal Time
   (UTC)**, not in local time. This requirement replaced the MiFID I approach
   of reporting in local time.

2. **ISO 8601 format**: The timestamp must be expressed in ISO 8601 format
   with UTC designator, e.g. `2024-11-03T21:00:00Z`.

3. **DST awareness**: During British Summer Time (BST, UTC+1), firms must
   **subtract 1 hour** from their local UK timestamps to convert to UTC
   before reporting. During GMT (UTC+0), local time equals UTC.
   Similarly, US-based firms must account for EDT (UTC-4) vs EST (UTC-5)
   transitions when computing UTC for Field 28.

4. **Precision**: Timestamps must include at minimum **second-level precision**;
   microsecond precision is required for high-frequency trading venues.

### Common DST Errors Identified by FCA

The FCA identified the following systemic errors in Field 28 reporting:

| Error Type | Description | Frequency |
|------------|-------------|-----------|
| BST/GMT confusion | Reporting BST local time as if it were UTC (1-hour error) | Most common |
| Hardcoded UTC offset | Systems with static UTC offset that does not update on DST switch | Common |
| Local time submission | Submitting local exchange time without UTC conversion | Moderate |
| Microsecond truncation | Reporting seconds-only when microseconds required for HFT | Moderate |

### Regulatory Consequence

Firms that report Field 28 with incorrect timestamps (e.g. local time instead
of UTC, or with wrong DST offset) are in breach of:
- **Article 26 of MiFIR** (transaction reporting obligation)
- **RTS 22** (regulatory technical standards on transaction reporting)

The FCA may issue data quality warnings, require resubmission, and in
repeated/serious cases, initiate supervisory action.

---

## MiFIR RTS 22 Field 28 Technical Specification

Per RTS 22 (Commission Delegated Regulation (EU) 2017/590):

- Field number: **28**
- Field name: **Trading date and time**
- Field description: Date and time when the transaction was executed
- Format: ISO 8601 date-time in UTC — `{YYYY}-{MM}-{DD}T{hh}:{mm}:{ss}[.{mmm}]Z`
- Applicability: All reportable transactions under Article 26 MiFIR

---

## Remediation Guidance

FCA Market Watch 59 recommends the following remediation steps for firms
with Field 28 compliance issues:

1. **Audit existing reporting infrastructure** for hardcoded UTC offsets
2. **Implement automatic DST detection** using OS-level timezone libraries
   (e.g. `pytz`, `zoneinfo`, `dateutil`) rather than static offsets
3. **Backfill corrected reports** for the affected reporting period
4. **Test UTC conversion logic** specifically around DST transition days
5. **Document the fix** in the firm's compliance testing procedures
