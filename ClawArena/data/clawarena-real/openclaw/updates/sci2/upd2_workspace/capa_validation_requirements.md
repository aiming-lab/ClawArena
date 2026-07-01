# CAPA Validation Requirements — Update 2 Supplement
## MedSafe RCA Team — Ivenix LVP Cases

**Document Reference**: CAPA-VALID-2026-001
**Issued**: April 2026 (Update 2)

---

## Purpose

This document establishes the validation requirements for confirming CAPA effectiveness
following the Ivenix LVP software recall (Z-0885-2026).

---

## CAPA Validation Matrix

### CAPA-004 & CAPA-005: LVP Software Update v5.10.2

| Test ID | Scenario | Expected Result | Status |
|---------|----------|----------------|--------|
| TV-001 | Battery health 100%, SOC at 50% | SOC reported within ±3% | Passed |
| TV-002 | Battery health 80%, SOC at 50% | SOC reported within ±3% | Passed |
| TV-003 | Battery health 70%, SOC at 50% | SOC reported within ±3% | Passed |
| TV-004 | Battery health 60%, SOC at 50% | SOC reported within ±3% | Passed |
| TV-005 | Battery health 50%, SOC at 20% | SOC reported within ±3% | Passed |
| TV-006 | Rate entry "0010" → OK | Rate set to 10.0 mL/hr, no freeze | Passed |
| TV-007 | Rate entry "0010" → BACK | Returns to prior screen, no freeze | Passed |
| TV-008 | Rate entry "00" → OK | Rate invalid: prompt re-entry | Passed |
| TV-009 | Low battery alarm at 20% actual SOC | Alarm triggered at ≤20% | Passed |
| TV-010 | Aged battery (250 cycles) SOC accuracy | SOC within ±3% | Passed |

**CAPA-004 and CAPA-005 validation: COMPLETE**

---

### CAPA-006: V&V Protocol Revision

| Deliverable | Status |
|-------------|--------|
| Aged battery test matrix (50-300 cycles) | In Progress |
| Temperature × cycle × health matrix | In Progress |
| Leading-zero input boundary test cases | Complete |
| V&V protocol formal review | Pending |

**CAPA-006 target completion**: Q1 2026

---

## Battery Replacement Effectiveness (CAPA-004 supplemental)

Facilities that replaced batteries with health < 70% report:
- Zero unexpected shutdowns post-replacement
- SOC accuracy within ±3% confirmed in post-service audits
- Patient safety incidents: 0 reported post-update

---

## Ivenix CAPA Summary

| CAPA | Description | Validation Status |
|------|-------------|-----------------|
| CAPA-004 | LVP software update v5.10.2 | COMPLETE |
| CAPA-005 | LVP software update v5.10.2 (input fix) | COMPLETE |
| CAPA-006 | V&V protocol revision | IN PROGRESS |

*Note on "30 units software kits": As clarified in Update 2, this figure represents
software correction kits distributed, NOT hardware LVP units. The total hardware
installation count for effectiveness measurement is tracked separately by Fresenius
Kabi's field service team and is not publicly disclosed.*
