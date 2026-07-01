# IEC 60601-2-24 — Infusion Pump Flow Accuracy Requirements
## Summary for RCA Engineering Analysis

**Standard**: IEC 60601-2-24:2012+AMD1:2020
**Scope**: Infusion pumps and controllers (ambulatory, volumetric, syringe)

---

## Section 51.102 — Accuracy of Flow Rate

### General Accuracy Requirements

For ambulatory infusion pumps (such as the Nimbus series):

| Parameter | Requirement |
|-----------|-------------|
| Long-term accuracy | ≤ ±5% of programmed rate (steady state) |
| Short-term accuracy | ≤ ±15% during start-up phase (first 20 minutes) |
| Bolus delivery accuracy | ≤ ±10% of programmed bolus |

### Clinical Significance

Flow rate deviations exceeding ±5% in steady-state infusion are considered clinically
significant for medications with narrow therapeutic windows (e.g., vasoactive agents,
insulin, heparin, opioid analgesics).

For the InfuTronix Nimbus recall, field data indicates flow rate deviations of up to
±15% during battery-degradation events, which exceeds both the steady-state and
short-term limits for extended durations.

---

## Occlusion Detection (Section 51.107)

Infusion pumps must detect upstream and downstream occlusion conditions:
- **Upstream occlusion**: Pump must alarm within [device-specific threshold] when
  upstream resistance exceeds the alarm threshold.
- **Standard practice**: Alarm threshold ≤ 300 mmHg upstream pressure.
  The InfuTronix Nimbus was designed with a 300 mmHg threshold; field reports indicate
  the actual detection was inconsistent for partial occlusions below this threshold.

---

## Electromagnetic Compatibility (Section 36)

Medical electrical equipment must comply with IEC 61000-3-2 and IEC 61000-3-3 for
electromagnetic interference. Battery-powered devices require additional testing under
IEC 60601-1 Clause 8.9 for battery discharge behavior.
