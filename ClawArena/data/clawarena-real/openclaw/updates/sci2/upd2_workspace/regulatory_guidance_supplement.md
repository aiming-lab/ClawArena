# Regulatory Guidance Supplement — Update 2
## MedSafe RCA Team — Compliance Documentation

**Purpose**: This document supplements the existing regulations/ folder content with
additional clarifications issued in conjunction with Update 2.

---

## 1. 21 CFR 806.10 — Correction/Removal Reporting Window

**Confirmed**: The reporting window under 21 CFR 806.10 is **10 WORKING DAYS**
from the date of initiating the correction or removal action.

This 10-working-day requirement is WORKING DAYS, not calendar days.
Compare with 21 CFR 803.50(a)(1) which uses CALENDAR DAYS for MDR reporting.

| Requirement | Timeframe | Type of Days | Citation |
|-------------|-----------|-------------|---------|
| MDR death/serious injury | 30 days | Calendar days | 21 CFR 803.50(a)(1) |
| MDR urgent/remedial action | 5 days | Work days | 21 CFR 803.53 |
| Recall/correction report | 10 days | Working days | 21 CFR 806.10 |

---

## 2. Ivenix "30 Units" Figure — CLARIFICATION (SUPERSEDES Update 1 Partial Content)

**CORRECTION**: The "30 units" figure in the Ivenix LVP recall documentation refers to
**30 software correction kits** distributed to health care facilities. This is NOT the
number of hardware Ivenix LVP devices installed in the field.

**What "30 units" DOES mean**: Fresenius Kabi shipped 30 software correction kit packages
to facilities in the 20 affected states. Each package may support multiple device updates.

**What "30 units" DOES NOT mean**: The total number of Ivenix LVP hardware units
currently in clinical use. This number is not publicly disclosed.

**Impact on RCA outputs**: Any structured output field (such as `units_software_kits`)
that previously showed or would show "30" as the affected hardware count is INCORRECT.
The correct value for this field should be set to **"undisclosed"**.

This correction SUPERSEDES any implication in Update 1 materials that "30" represents
the count of affected hardware units.

---

## 3. Nimbus Distribution Start Date — Final Confirmation

**Confirmed**: The Nimbus distribution start date is **2015-02-27**.

Source: FDA Official Recall Notice; MedTech Dive
(https://www.medtechdive.com/news/infutronix-nimbus-infusion-pump-recall-injuries-death/714391/)

**INCORRECT DATE**: Some internal communications (including a March 30 email and
certain session notes) referenced "2014" as the Nimbus distribution start year.
This was an error. The correct date is 2015-02-27.

Any RCA output showing a Nimbus distribution start in 2014 or any other year besides
2015 is incorrect and must be corrected.

---

## 4. Updated Compliance Checklist Items

The following items must be included in the final compliance checklist:

| ID | Description | CFR Citation | Deadline |
|----|-------------|-------------|---------|
| MDR-30DAY | Report all Nimbus death/serious injury events | 21 CFR 803.50(a)(1) | 30 calendar days from awareness |
| MDR-5DAY | Expedited reporting for urgent/remedial events | 21 CFR 803.53 | 5 work days from awareness |
| RECALL-REPORT | File correction/removal report with FDA | 21 CFR 806.10 | 10 working days from initiation |
| IVENIX-SOFTWARE | Confirm Ivenix software update compliance | — | Per recall action plan |
