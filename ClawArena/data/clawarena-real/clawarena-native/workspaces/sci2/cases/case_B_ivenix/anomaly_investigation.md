# Software Anomaly Root Cause Investigation
## Fresenius Kabi Ivenix LVP — Internal Investigation Report

**Document Reference**: IVX-RCA-2025-001
**Investigation Lead**: Software Safety Team
**Status**: Final

---

## Anomaly 1 Root Cause: Battery State-of-Charge Reporting

### Observed Failure
Battery remaining capacity displayed as 85% when actual remaining capacity was below 20%.
Device subsequently shut down during active infusion without prior low-battery alarm.

### 5-Why Analysis

| Why # | Question | Finding |
|-------|----------|---------|
| Why 1 | Why did the device shut down unexpectedly? | Battery was depleted below minimum operating voltage |
| Why 2 | Why was the battery depleted without warning? | Low-battery alarm did not trigger at the appropriate threshold |
| Why 3 | Why did the alarm fail to trigger? | State-of-charge calculation algorithm returned inaccurate values |
| Why 4 | Why was the algorithm inaccurate? | Coulomb counting offset error accumulated over charge-discharge cycles |
| Why 5 | Why was the cumulative error not detected? | Verification testing used fresh batteries only; aged-battery test scenarios not included in V&V protocol |

### Root Cause
Software defect in battery state-of-charge algorithm (version 5.10.1 and earlier):
coulomb counting function did not account for battery impedance changes with aging.
Batteries with health below 70% exhibited the most severe reporting errors.

---

## Anomaly 2 Root Cause: Dual-Zero Rate Entry Freeze

### Observed Failure
Entry of "0010" for a 10 mL/hr rate, followed by pressing Back or OK, causes UI to
freeze in fail-stop alarm state. Device requires power cycle to recover.

### 5-Why Analysis

| Why # | Question | Finding |
|-------|----------|---------|
| Why 1 | Why does the UI freeze? | State machine enters unrecoverable error state |
| Why 2 | Why does the state machine fail? | Input parser does not handle leading-zero numeric strings correctly |
| Why 3 | Why is the parsing error fatal? | Exception handler calls fail-stop routine instead of input validation reset |
| Why 4 | Why does the exception handler escalate? | Defensive programming assumption violated: input validation was expected to prevent this path |
| Why 5 | Why was this path not prevented? | Integration testing did not include boundary cases with leading zeros in rate entry |

### Root Cause
Input validation gap in the rate-entry state machine: leading-zero numeric strings bypass
the range validation and trigger an unhandled parser exception that invokes fail-stop.
Present in software version 5.10.1 and earlier.

---

## Corrective Action Summary

| Action | Target | Owner | Status |
|--------|--------|-------|--------|
| Update LVP software to v5.10.2 | All affected units | Software Team | Complete |
| Update IMS to v5.2.2 | All affected units | Integration Team | Complete |
| Replace batteries with health < 70% | Affected devices | Field Service | In Progress |
| Revise V&V protocol to include aged-battery and boundary-case test scenarios | V&V Team | Quality | In Progress |
