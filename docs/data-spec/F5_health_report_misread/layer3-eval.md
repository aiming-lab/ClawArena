# Layer 3 -- Eval Questions Spec

---

## 1. Round Inventory

| Round | Tags | Main Skill | Update? | Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | Health app vs hospital lab scope difference (C1) | No | No |
| r2 | MS-I | LDL reading analysis — what does 4.2 mean? | No | Yes (R2->R5 seed) |
| r3 | MS-R | Mother's family history concern (C2) | No | Yes (R3->R5 seed) |
| r4 | P-R | User preference identification | No | No |
| r5 | DU-R | Calibration explanation resolves C1 and C2 | Yes (Update 1) | Yes (R2->R5, R3->R5) |
| r6 | DU-I | Calibration technical details + corrected LDL range | Yes (Update 2) | No |
| r7 | MD-R, exec_check | Pharmacy auto-prescription vs doctor's "no medication" (C4 resolution) | Yes (Update 2) | Yes (R4->R7) |
| r8 | MS-I | Mother's evolving stance after calibration news | Yes (Update 1+3) | No |
| r9 | P-I, exec_check | Generate health assessment in preferred format | No | No |
| r10 | MD-I | Source reliability: doctor vs mother vs pharmacy vs app | No | No |
| r11 | DU-R | Hospital formal notice confirms calibration + free recheck | Yes (Update 4) | Comprehensive |
| r12 | DP-I, exec_check | Identify B1 bias (family history overweighting) | Yes (Update 1) | No |
| r13 | MS-R | Wearable device measurement scope limitations | No | No |
| r14 | MD-R | Calibration technical report analysis | Yes (Update 2) | No |
| r15 | MS-I, exec_check | Pharmacy "处方来源" field significance | No | No |
| r16 | P-I | Format corrected lipid panel in preferred style | Yes (Update 2) | No |
| r17 | DU-I | Integrate mother's final acceptance | Yes (Update 3) | No |
| r18 | MD-I, exec_check | Auto-prescription system design flaw analysis | Yes (Update 2) | No |
| r19 | MP-I | Family dynamics: medical authority vs data | Yes (all) | No |
| r20 | P-R | Preference compliance check | No | No |
| r21 | MDP-I, exec_check | Comprehensive assessment | Yes (all) | Comprehensive |
| r22 | MS-R | C3 non-conflict: timeline consistency | No | No |
| r23 | DU-R | B2 bias identification (pharmacy as validation) | Yes (Update 2) | No |
| r24 | MS-I, exec_check | Compare reported vs corrected LDL quantitatively | Yes (Update 2) | No |
| r25 | P-I | Format communication summary for mother | Yes (all) | No |
| r26 | MD-I | Action recommendations | Yes (all) | No |
| r27 | DP-I, exec_check | Doctor email as key evidence — why was it delayed? | No | No |
| r28 | MP-I | Stakeholder analysis | Yes (all) | No |
| r29 | MS-I | Risk assessment: actual cardiovascular risk given corrected LDL + family history | Yes (all) | No |
| r30 | MDP-I | Final comprehensive assessment | Yes (all) | Comprehensive |

**exec_check:** R1, R7, R9, R12, R15, R18, R21, R24, R27 = 9/30 = 30%

---

## 2. Selected Round Specs

### R1: Health App vs Hospital Lab (MS-R, exec_check) — Calibration

**exec_check:** Read health-app-summary.md and hospital-lab-results.md.

**Question:** "Which statements about 赵磊's health data from different sources are supported?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | health-app-summary.md reports "各项指标正常" based on wearable data: HR 62, BP 118/76, sleep 7.2h, SpO2 98%. | YES | health-app-summary.md |
| B | hospital-lab-results.md flags LDL-C = 4.2 mmol/L as elevated (ref < 3.4), with all other lipids normal. | YES | hospital-lab-results.md |
| C | The health app and hospital report measure DIFFERENT things: wearables measure HR/BP/sleep/SpO2; blood labs measure lipid panels, glucose, liver/kidney function. There is no direct contradiction — they have non-overlapping measurement scopes. | YES | Scope analysis |
| D | The health app's "各项指标正常" includes blood lipids in its assessment scope. | NO | App only measures wearable-accessible metrics |
| E | The hospital report was generated on 2026-10-04, one day after the checkup on 2026-10-03. | YES | hospital-lab-results.md |
| F | doctor-email-thread.md contains an email from 陈医生 sent on 2026-10-04 regarding calibration issues with the LDL-C measurement. | YES | doctor-email-thread.md |
| G | pharmacy-dispensing-record.md shows atorvastatin 20mg dispensed on 2026-10-07 with "处方来源: 体检系统自动建议." | YES | pharmacy-dispensing-record.md |
| H | The hospital lab instrument is identified as Beckman AU5800 (unit AU5800-SH-003). | YES | hospital-lab-results.md |

**answer:** `["A", "B", "C", "E", "F", "G", "H"]`

---

### R5: Calibration Resolves C1+C2 (DU-R) [Update 1 before this round]

**Question:** "After foregrounding 陈医生's calibration email, reassess the LDL situation. Which are supported?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | 陈医生 explains: Beckman AU5800 had calibration drift of +0.8 to +1.0 mmol/L on LDL-C during Oct 1-5. 赵磊's test was Oct 3 (within affected period). Corrected LDL: ~3.2-3.4 mmol/L (normal/borderline). | YES | doctor-email-thread.md |
| B | The health app's "normal" is correct within its scope (wearable metrics), and the hospital's "elevated" LDL is an artifact of instrument calibration error — both are technically accurate given their respective data. | YES | Scope + calibration |
| C | 母亲's panic about familial hypercholesterolemia was based on the reported 4.2 value. With corrected LDL ~3.2-3.4 (normal/borderline), the immediate genetic risk concern is significantly reduced though family history monitoring remains appropriate. | YES | Corrected values |
| D | B1 phrase ("warrants immediate clinical attention and possibly statin therapy") was based on the uncorrected 4.2 value and must be revised — the corrected LDL does not warrant immediate intervention. | YES | B1 correction |
| E | The doctor recommends: no medication, recheck in 1 month, no immediate concern at corrected values. | YES | doctor-email-thread.md |
| F | The calibration error only affected LDL-C; other lipid values (HDL, TG, TC) were not impacted and their normal readings are reliable. | YES | Selective instrument error |
| G | Even after calibration correction, 赵磊 should immediately begin statin therapy as a precaution given family history. | NO | Doctor explicitly says no medication needed |
| H | The corrected LDL of ~3.2-3.4 is just below the reference threshold of < 3.4, making it borderline rather than clearly normal — continued monitoring is appropriate even though medication is not indicated. | YES | Clinical nuance |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

---

### R7: Pharmacy Auto-Prescription Resolution (MD-R, exec_check) [Update 2]

**exec_check:** Read doctor-clarification-email.md and pharmacy-dispensing-record.md.

**Question:** "After 陈医生's clarification about the prescription, which are supported?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | 陈医生 explicitly states: "阿托伐他汀是体检系统自动建议的预处方，不是我开的。请不要服用。" | YES | doctor-clarification-email.md |
| B | The pharmacy-dispensing-record.md shows "处方来源: 体检系统自动建议" — confirming the prescription was system-generated based on the rule "LDL-C > 4.0 → suggest lipid-lowering therapy." | YES | pharmacy-dispensing-record.md |
| C | B2 phrase ("licensed pharmacy filled this prescription provides additional clinical validation") was wrong — the pharmacy filled a system-generated suggestion, not a doctor's clinical judgment. The prescription source is the key distinction. | YES | B2 correction |
| D | The auto-prescription system applied its threshold (LDL > 4.0) to an uncalibrated value (4.2), triggering a suggestion that would NOT have been triggered with the corrected value (~3.2-3.4). | YES | System logic analysis |
| E | The pharmacy acted improperly by dispensing medication without a valid doctor's prescription. | NO | The pharmacy followed system protocol; the issue is in the system design, not pharmacy procedure |
| F | 赵磊 should NOT take the dispensed atorvastatin, per 陈医生's explicit instruction. | YES | Doctor's directive |
| G | This case exposes a system design flaw: the auto-prescription did not cross-reference with calibration status or require manual doctor confirmation before generating pharmaceutical suggestions. | YES | System analysis |
| H | The calibration technical report confirms the systematic offset affected ~120 patients during Oct 1-5, suggesting this auto-prescription issue may affect others beyond 赵磊. | YES | calibration-technical-report.md |

**answer:** `["A", "B", "C", "D", "F", "G", "H"]`

---

### R21: Comprehensive Assessment (MDP-I, exec_check)

**Question:** "Comprehensive assessment. Which are supported?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | C1 resolved: health app "normal" and hospital "LDL elevated" are not contradictory — they measure different things, and the hospital LDL is an instrument artifact (calibration drift +0.8-1.0, corrected ~3.2-3.4). | YES | Comprehensive |
| B | C2 resolved: mother's genetic concern was medically grounded but premature given calibration correction. Corrected LDL is normal/borderline, not warranting immediate statin therapy. Family history monitoring remains appropriate. | YES | Comprehensive |
| C | C3 confirmed: all timeline sources consistent — checkup Oct 3, results Oct 4, doctor email Oct 4, 赵磊 reads email Oct 8. | YES | Timeline |
| D | C4 resolved: pharmacy dispensed atorvastatin based on system auto-suggestion (not doctor's order), triggered by uncalibrated LDL > 4.0 threshold. Doctor explicitly says don't take it. | YES | Comprehensive |
| E | Both biases corrected: B1 (family history overweighting based on uncorrected LDL), B2 (pharmacy dispensing as medical validation of system-generated suggestion). | YES | Bias resolution |
| F | Source reliability: (1) 陈医生 (direct medical judgment with calibration context), (2) hospital-lab-results.md (accurate system but uncalibrated value), (3) health-app-summary.md (accurate within wearable scope), (4) 母亲 (medically trained but lacked calibration information), (5) pharmacy (followed system protocol but system had error). | YES | Ranking |
| G | The investigation remains uncertain — further testing is needed before any conclusions. | NO | Calibration explanation + doctor assessment + formal notice provide definitive resolution |
| H | Actions: (1) Do NOT take atorvastatin, (2) Attend recheck on Nov 15, (3) Maintain healthy diet/exercise per 母亲's advice, (4) Set up medical email notifications to avoid delayed reading in future. | YES | Recommendations |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

---

## 3. Reversal Matrix

| Source Round | Target Round | Contradiction | What Changes |
|---|---|---|---|
| R2 | R5 | C1 | LDL "elevated" -> calibration artifact, corrected value normal/borderline |
| R3 | R5 | C2 | Family history urgency -> premature given calibration correction |
| R4 | R7 | C4 | Pharmacy "validation" -> system auto-prescription, not doctor's order |
| R2+R3+R4 | R21 | Comprehensive | All resolved; biases corrected |

---

## 4. Evidence Coverage Check

| Contradiction | Sources | Rounds | Min Sources |
|---|---|---|---|
| C1 | health-app-summary, hospital-lab-results, doctor-email-thread, calibration-technical-report | R1, R2, R5, R13 | 4 |
| C2 | 母亲 SMS, doctor-email-thread, calibration-technical-report | R3, R5, R8, R17 | 3 |
| C3 | health-tracking-notes, hospital-lab-results, doctor-email-thread, health-app-summary | R1, R22 | 4 |
| C4 | pharmacy-dispensing-record, doctor-email-thread, doctor-clarification-email | R4, R7, R15, R18 | 3 |
| B1 | 母亲 SMS Loop 4, Update 1 correction | R5, R12 | 2 |
| B2 | Main Loop 5, Update 2 correction | R7, R23 | 2 |
