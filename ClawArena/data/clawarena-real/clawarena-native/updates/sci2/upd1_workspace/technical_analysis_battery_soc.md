# Technical Root Cause Analysis
## Ivenix LVP Battery State-of-Charge (SOC) Algorithm Defect
## Software Versions 5.10.1 and Earlier

**Document Reference**: IVX-TECH-RCA-2025-003
**Prepared by**: Fresenius Kabi Software Safety Engineering
**Review Status**: Final

---

## 1. Technical Background

### Battery Electrochemistry in LVP Devices

Lithium-ion batteries used in the Ivenix LVP system are rated for:
- Nominal capacity: 3,350 mAh at 25°C
- Voltage range: 3.0V (depleted) to 4.2V (fully charged)
- Design life: 300 charge cycles or 3 years, whichever comes first
- Health definition: Actual deliverable capacity / rated capacity × 100%

Batteries with health below 70% show significantly altered
charge-discharge behavior that confounds coulomb counting algorithms.

### Coulomb Counting Algorithm (Defective Implementation)

The SOC algorithm in software version 5.10.1 and earlier used the following approach:

```python
# DEFECTIVE IMPLEMENTATION (v5.10.1 and earlier)
def calculate_soc(initial_charge_mah, current_mah, temperature_c):
    # NOTE: This does not account for battery aging / impedance changes
    soc = (current_mah / initial_charge_mah) * 100
    # Temperature compensation applied (correct)
    if temperature_c < 20:
        soc = soc * 0.97  # 3% correction for cold
    elif temperature_c > 35:
        soc = soc * 0.99  # 1% correction for heat
    return max(0, min(100, soc))
```

**Critical defect**: `initial_charge_mah` is set at manufacturing time and never updated
to reflect actual degraded battery capacity. As batteries age and capacity decreases,
the denominator remains the original rated capacity, causing SOC to be systematically
over-reported.

### Fixed Implementation (v5.10.2)

```python
# CORRECTED IMPLEMENTATION (v5.10.2)
def calculate_soc(current_mah, temperature_c, battery_health_pct):
    # Use measured actual capacity, not rated capacity
    # battery_health_pct obtained from periodic cycle-count measurement
    actual_capacity_mah = 3350 * (battery_health_pct / 100)
    soc = (current_mah / actual_capacity_mah) * 100
    # Temperature compensation (unchanged)
    if temperature_c < 20:
        soc = soc * 0.97
    elif temperature_c > 35:
        soc = soc * 0.99
    return max(0, min(100, soc))
```

---

## 2. Failure Mode Analysis

### Observed Failure Signatures

| Battery Health | SOC Over-Report | Risk |
|---------------|----------------|------|
| 90-100% | < 5% error | Low |
| 80-89% | 5-15% error | Medium |
| 70-79% | 15-25% error | High |
| < 70% | > 25% error | Critical |

A device with 60% battery health and 20% actual remaining charge may display 47% remaining,
causing the clinician and alarm system to believe there is adequate battery reserve when the
device is actually near shutdown threshold.

### Shutdown Event Timeline (Reconstructed from MDR Data)

```
Time 0:00  Device started, battery health = 58%, actual SOC = 22%
           Algorithm reports SOC = 37% (over-report)
           No low-battery alarm triggered (threshold: 10% reported SOC)

Time 0:45  Actual SOC drops to 8%
           Algorithm reports SOC = 14%
           No alarm (above 10% reported threshold)

Time 1:12  Actual SOC drops to 3%
           Algorithm reports SOC = 5%
           Low-battery alarm activates at 5% reported SOC — WARNING
           Clinician sees alarm but believes 5% reported charge
           Actual: already near complete depletion

Time 1:17  Device shuts down unexpectedly
           Patient mid-infusion — dose interrupted
           MDR event triggered
```

---

## 3. Verification and Validation Gap

### Root Cause of V&V Failure

The battery SOC algorithm was validated using:
- New batteries (100% health) at 3 temperatures (15°C, 25°C, 35°C)
- 50 charge-discharge cycles (represents ~6 months of use)
- Accuracy criterion: SOC within ±5% of reference measurement

**Gap identified**: The 50-cycle test represents only 17% of the rated 300-cycle life.
Batteries showing significant impedance changes (typically after 150+ cycles, health < 80%)
were NOT included in the V&V test matrix.

### Corrective V&V Protocol (Preventive CAPA)

Updated protocol (CAPA-006) requires:
- Battery health test matrix: 100%, 90%, 80%, 70%, 60%, 50%
- Cycle count test matrix: 0, 50, 100, 150, 200, 250, 300 cycles
- Temperature matrix: 10°C, 20°C, 25°C, 30°C, 40°C
- Accuracy criterion: SOC within ±3% across all health/cycle/temperature combinations

---

## 4. Dual-Zero Rate Entry Defect (Supplemental)

### Input State Machine Error

The rate entry state machine in versions 5.10.1 and earlier:

```
State: IDLE
  User presses: [0] → State: FIRST_DIGIT
  User presses: [0] → State: SECOND_DIGIT (leading zero)
  User presses: [1] → State: THIRD_DIGIT
  User presses: [0] → State: FOURTH_DIGIT
    Value buffer: "0010"
  User presses: [OK] or [BACK]
    DEFECT: Parser calls int("0010") in strict mode
    Python-style leading-zero check raises ValueError
    Exception handler: triggers fail-stop state
    UI FROZEN — requires power cycle
```

**Fix in v5.10.2**: Input pre-processor strips leading zeros before parsing.
Leading-zero inputs now correctly resolve to their numeric value.

---

## Document History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2025-11-14 | Software Safety Eng | Initial draft |
| 2.0 | 2025-12-16 | Software Safety Eng | Final (post-remediation) |
