# Fresenius Kabi Ivenix LVP Software Recall
## FDA Recall Number: Z-0885-2026

**Product**: Ivenix Large Volume Pump (LVP) — Software Only
**Product Code**: LVP-SW-0005
**Classification**: Class I
**Enforcement Date**: December 16, 2025
**Recall Number**: Z-0885-2026

---

## Affected Product

**Software Version**: 5.10.1 and earlier
**Product Code**: LVP-SW-0005
**Units Affected**: 30 software correction kits distributed
**Distribution States**: CA, CO, FL, GA, ID, IL, MD, MI, MN, MS, NE, NJ, NV, OK, OR, SC, TX, VA, WA, WI

---

## Reason for Recall — Two Software Anomalies

### Anomaly 1: Battery State-of-Charge Reporting Error
The battery management software in version 5.10.1 and earlier contains a
defect causing the battery's state-of-charge (remaining capacity) to be inaccurately displayed.
This results in the device displaying higher remaining charge than is actually available,
leading to unexpected device shutdown during infusion without adequate warning.

**Clinical consequence**: Unexpected mid-infusion pump shutdown may cause under-dosing,
therapy interruption, or in critical care contexts, patient harm.

### Anomaly 2: Dual-Zero Rate Entry Interface Freeze
When a clinician enters an infusion rate with two leading zeros (e.g., entering "0010" for
10 mL/hr), followed by pressing the Back or OK button, the pump's user interface freezes in
a fail-stop alarm state. The device cannot be operated until power-cycled.

**Clinical consequence**: Interface freeze during rate programming may delay or prevent
medication administration in time-critical situations.

---

## Adverse Events (as of November 18, 2025)

| Category | Count |
|----------|-------|
| Serious Injuries | 2 |
| Deaths | 0 |

---

## Corrective Action

1. Update Infusion Management Software (IMS) to version 5.2.2
2. Update LVP software to version 5.10.2
3. Replace battery if health is below 70%

**Source**: https://www.softwarecpr.com/2025/12/fda-recall-software-anomalies-can-cause-serious-harm-or-death/
**Source**: https://manufacturingchemist.com/fda-class-i-recall-fresenius-kabi-ivenix-infusion
