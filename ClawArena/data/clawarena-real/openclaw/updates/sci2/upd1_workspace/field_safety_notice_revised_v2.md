# REVISED Field Safety Notice — Fresenius Kabi Ivenix LVP Software
## Version 2.0 (REVISION — Supersedes All Prior Ivenix FSN Versions)

**REVISION NOTICE**: This document supersedes any prior communications regarding
Ivenix LVP software affected version scope. The affected version description
has been corrected.

---

## CRITICAL CORRECTION

**INCORRECT** (prior communications): "Affected software version: 5.10.0"
**CORRECT** (this revision): "Affected software version: **5.10.1 and earlier**"

This means ALL Ivenix LVP software versions from the initial release through
5.10.1 are affected, not only version 5.10.0.

---

## Updated Recall Summary

**Recall Number**: Z-0885-2026
**Product Code**: LVP-SW-0005
**Affected Software Versions**: 5.10.1 and earlier
**Fixed Version**: 5.10.2
**IMS Updated Version**: 5.2.2

---

## Anomaly 1: Battery State-of-Charge Reporting Error

**Root Cause**: The coulomb counting algorithm in versions 5.10.1 and
earlier does not compensate for battery impedance changes associated with aging.
Batteries with health below 70% show the most severe reporting errors.

**Action Required**: Replace any battery with health < 70%.
Install software update 5.10.2 and IMS 5.2.2.

---

## Anomaly 2: Dual-Zero Rate Entry Interface Freeze

**Root Cause**: Input validation gap in the rate-entry state machine allows
leading-zero numeric strings to bypass range validation, triggering an unhandled
parser exception that invokes fail-stop mode.

**Action Required**: Install software update 5.10.2.

---

## Adverse Events (as of November 18, 2025)
- Serious Injuries: 2
- Deaths: 0

---

## Implementation Guide (supplemental)

### Battery Health Assessment Protocol
1. Access device diagnostics menu.
2. Navigate to Battery Health > State of Charge.
3. Record battery health percentage.
4. If health < 70%, schedule immediate battery replacement before software update.
5. If health >= 70%, proceed directly to software update.

### Software Update Procedure
1. Connect device to IMS workstation.
2. Apply IMS update to v5.2.2 first.
3. Apply LVP software update to v5.10.2.
4. Verify update completion via device firmware version screen.
5. Run self-test sequence before returning device to clinical use.

### Dual-Zero Input Risk Avoidance (pre-update)
Clinician guidance: do not enter rates using leading zeros (e.g., use "10" not "0010").
Display "RATE ENTRY NOTE" reminder near pump in affected wards.

---

## Documentation

- Recall Number: Z-0885-2026
- FDA Enforcement Date: 2025-12-16
- Product Code: LVP-SW-0005
- Distribution States: CA, CO, FL, GA, ID, IL, MD, MI, MN, MS, NE, NJ, NV, OK, OR, SC, TX, VA, WA, WI
- Units (software correction kits): 30
  (Note: this figure represents the number of software correction kits distributed,
  not the total number of hardware LVP units in the field.)

**Sources**:
- https://www.softwarecpr.com/2025/12/fda-recall-software-anomalies-can-cause-serious-harm-or-death/
- https://www.aabb.org/news-resources/news/article/2026/03/04/regulatory-update--class-i-recall-issued-for-fresenius-kabi-ivenix-large-volume-pump-software
- https://manufacturingchemist.com/fda-class-i-recall-fresenius-kabi-ivenix-infusion
