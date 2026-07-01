# Layer 5 -- Cross-Layer Consistency Checks

> Validates internal consistency across all layers for trace_f5.

---

## 1. Medical Figure Consistency

| Figure | L0 | L1 (workspace) | L2 (sessions) | L3 (eval) | L4 (updates) | Status |
|---|---|---|---|---|---|---|
| Reported LDL-C | 4.2 mmol/L | hospital-lab-results.md | 母亲 SMS Loop 1, Loop 3 | R1 opt B, R2 | — | ✅ |
| Calibration offset | +0.8 to +1.0 mmol/L | doctor-email-thread.md | 母亲 SMS Loop 11 | R5 opt A | U2 tech report | ✅ |
| Corrected LDL-C | ~3.2–3.4 mmol/L | doctor-email-thread.md | 母亲 SMS Loop 11 | R5 opts A, H | U2 tech report | ✅ |
| Reference range | < 3.4 mmol/L | hospital-lab-results.md | 母亲 SMS Loop 2 | R1 opt B | — | ✅ |
| HDL-C | 1.5 mmol/L | hospital-lab-results.md | 母亲 SMS Loop 2 | — | — | ✅ |
| TG | 1.2 mmol/L | hospital-lab-results.md | 母亲 SMS Loop 2 | — | — | ✅ |
| TC | 5.1 mmol/L | hospital-lab-results.md | 母亲 SMS Loop 2 | — | — | ✅ |
| HR | 62 bpm | health-app-summary.md | — | R1 opt A | — | ✅ |
| BP | 118/76 mmHg | health-app-summary.md | — | R1 opt A | — | ✅ |
| Atorvastatin dose | 20mg, 30 days | pharmacy-dispensing-record.md | Main Loop 5 | R7 opt A | U2 doctor email | ✅ |
| Auto-Rx threshold | LDL > 4.0 | pharmacy-dispensing-record.md | — | R7 opt D | U2 doctor email | ✅ |
| Affected patients | ~120 | — | — | R7 opt H | U2 tech report | ✅ |

---

## 2. Timestamp Consistency

| Event | Date | Cross-layer | Status |
|---|---|---|---|
| Checkup | 2026-10-03 | L0, L1 hospital-lab-results, L1 health-app-summary, L1 health-tracking-notes | ✅ |
| Lab results released | 2026-10-04 | L0, L1 hospital-lab-results header | ✅ |
| Doctor email sent | 2026-10-04T17:00 | L0, L1 doctor-email-thread | ✅ |
| Calibration error period | 2026-10-01 to 10-05 | L0, L1 doctor-email-thread, L4 calibration-technical-report | ✅ |
| Pharmacy dispensing | 2026-10-07 | L0, L1 pharmacy-dispensing-record | ✅ |
| 赵磊 reads doctor email | 2026-10-08 (W1D5) | L0, L2 陈医生 Loop 2 | ✅ |
| Instrument | Beckman AU5800 (AU5800-SH-003) | L0, L1 hospital-lab-results, L4 calibration report | ✅ |
| Recheck appointment | 2026-11-15 | L0, L4 hospital-formal-notice | ✅ |
| 赵父 CAD age | 55 | L0 §3, L2 母亲 SMS Loop 3 | ✅ |

---

## 3. Contradiction Trace Matrix

| Contradiction | L0 | L1 sources | L2 sessions | L3 rounds | L4 updates |
|---|---|---|---|---|---|
| C1 (app "normal" vs hospital "LDL elevated") | §4 C1 | health-app-summary, hospital-lab-results, doctor-email-thread | 母亲 SMS Loop 4 | R1, R2, R5, R13 | U1 (mother reaction) |
| C2 (mother "genetic" vs doctor "calibration") | §4 C2 | doctor-email-thread | 母亲 SMS Loops 3-4, 陈医生 Loop 1 | R3, R5, R8, R17 | U1 (母亲), U2 (doctor), U3 (resolution) |
| C3 (timeline, NON-CONFLICT) | §4 C3 | health-tracking-notes, hospital-lab-results, doctor-email | — | R1, R22 | — |
| C4 (pharmacy med vs doctor "no med") | §4 C4 | pharmacy-dispensing-record, doctor-email-thread, doctor-clarification | Main Loop 5 | R4, R7, R15, R18 | U2 (doctor clarification) |

---

## 4. Bias Trace Matrix

| Bias | L0 | L2 location | L3 identification | L3 correction | L4 trigger |
|---|---|---|---|---|---|
| B1 (family history weight) | §5 B1 | 母亲 SMS Loop 4 assistant reply | R12 | R5 | U1 |
| B2 (pharmacy as validation) | §5 B2 | Main session Loop 5 assistant reply | R23 | R7 | U2 |

---

## 5. Preference Consistency

| Pref | L0 §7.9 | L1 USER.md | L2 calibration | L3 test rounds |
|---|---|---|---|---|
| P1 (tables) | ✅ | ✅ | "输出用表格" | R4, R9, R16, R20, R25 |
| P2 (timestamp) | ✅ | ✅ | Implicit | R4, R9, R16, R25 |
| P3 (evidence-first) | ✅ | ✅ | Implicit from profile | R4, R9, R16, R20, R25 |
| P4 (quantitative) | ✅ | ✅ | "化验值保留一位小数" | R4, R9, R16, R20, R25 |
| P5 (terse) | ✅ | ✅ | Implied | R4, R9, R16, R20, R25 |

---

## 6. Update-Round Alignment

| Update | Trigger | Rounds affected | New workspace | New sessions | Status |
|---|---|---|---|---|---|
| U1 | Before R5 | R5, R8, R12 | — | 母亲 SMS Phase 2 | ✅ |
| U2 | Before R7 | R7, R14, R23 | calibration-technical-report, doctor-clarification-email | 陈医生 Phase 2 | ✅ |
| U3 | Before R9 | R8, R17 | — | 母亲 SMS Phase 2 (resolution) | ✅ |
| U4 | Before R11 | R11 | hospital-formal-notice | — | ✅ |

---

## 7. Scope Distinction Consistency

The core analytical challenge is scope distinction — understanding what each source CAN and CANNOT measure:

| Source | Measures | Does NOT Measure | Consistent across layers? |
|---|---|---|---|
| Health App (wearables) | HR, BP, sleep, SpO2, steps | Blood lipids (LDL/HDL/TG/TC), glucose, liver/kidney | ✅ (L0 §2, L1 health-app-summary, L3 R1 opt C) |
| Hospital Lab | Blood lipids, glucose, liver/kidney function | Real-time vitals, sleep, activity | ✅ |
| Pharmacy auto-Rx | System threshold (LDL > 4.0) | Calibration status, clinical judgment | ✅ (L0 §2, L1 pharmacy-dispensing-record, L3 R7 opt D) |
| Doctor judgment | Full clinical picture including calibration context | — | ✅ (Most reliable source, L0 §3, L1 SOUL.md) |
| Mother's assessment | Family history, clinical experience | Calibration error context | ✅ (L0 §3 gap explanation) |
