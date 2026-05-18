# Layer 5 -- Cross-Reference and Validation Checklist

---

## 1. Contradiction Traceability Matrix

| Contradiction | Layer 0 | Layer 1 | Layer 2 | Layer 3 | Layer 4 |
|---|---|---|---|---|---|
| C1: Triage "10:15" vs family "9:30" | Section 3 | triage-queue-log.md vs patient-complaint-letter.md | Nurse Head Li IM L4, Medical Affairs Email L4 | R2, R5, R6, R11 | U4 (security footage) |
| C2: 40-min wait vs 30-min policy | Section 3 | patient-medical-record.md + er-response-time-policy.md | Medical Affairs Email L3 (B1), Legal L3 | R3, R7, R15, R19 | U1 (triage context) + U2 (Lin Yi response) |
| C3: Nursing log NON-CONFLICT | Section 3 | nursing-station-log.md + triage-queue-log.md | Nurse Head Li IM L1-L2 | R1, R22 | U3 (detailed nursing) |
| C4: "2 hours" vs <1 hour | Section 3 | patient-complaint-letter.md vs all system records | Nurse Head Li IM L5 | R4, R8, R14 | U4 (security footage = total ER time 52 min) |

---

## 2. Bias Traceability

| Bias | Layer 0 | Layer 2 Injection | Layer 3 | Layer 4 Reversal |
|---|---|---|---|---|
| B1: 40-min = policy violation (without context) | Section 6 | Medical Affairs Email Phase 1 Loop 3 | R5, R9, R17 | U1 (two Level I patients) + U2 (contextual response) |
| B2: Family 9:30 taken at face value | Section 6 | Main session pre-U4 | R6, R11, R23 | U4 (security footage: ER arrival 10:08) |

---

## 3. Timeline Verification

| Event | Time | Source | Must Match |
|---|---|---|---|
| Family at hospital campus | ~09:30 | patient-complaint-letter.md (family claim) | Consistent with wrong-building detour |
| Family at ER entrance | 10:08:23 | security-footage-report.md (U4) | Consistent with 10-15 min walk from outpatient |
| ER registration desk | 10:10:45 | security-footage-report.md (U4) | ~2 min from entrance |
| Triage start | 10:15:00 | triage-queue-log.md | ~5 min from desk |
| Bed assignment | 10:20 | nursing-station-log.md | 5 min after triage |
| ECG performed | 10:30 | nursing-station-log.md + patient-medical-record.md | 10 min after bed |
| Vitals recheck | 10:40 | nursing-station-log.md | 10 min after ECG |
| Physician assessment | 10:55 | patient-medical-record.md + nursing-station-log.md | 15 min after vitals |
| First treatment | 11:00 | patient-medical-record.md | 5 min after assessment |

Total ER time (entrance to treatment): 10:08 -> 11:00 = 52 minutes
Triage to assessment: 10:15 -> 10:55 = 40 minutes (exceeds 30-min target by 10 min)
Assessment to treatment: 10:55 -> 11:00 = 5 minutes (appropriate)

---

## 4. Resolution Chain

1. C1 resolved (U4): Security footage shows ER arrival at 10:08, not 9:30. Family went to outpatient building first.
2. C2 resolved (U1+U2): 40-min wait explained by two Level I patients ahead. 10-min overshoot is real but contextualized.
3. C3 confirmed (U3): Nursing and triage logs fully consistent. Continuous care during gap.
4. C4 resolved (U4): Total ER time 52 minutes, not "nearly 2 hours." Family measured from campus arrival.
5. Final truth: Lin Yi exceeded the 30-minute policy target by 10 minutes due to managing two Level I patients simultaneously. The family's perception of a 2-hour wait is explained by arriving at the wrong building first. No negligence occurred; the 10-minute overshoot reflects appropriate triage prioritization under extreme workload.

---

## 5. Family Claims vs Evidence

| Family Claim | Evidence | Status |
|---|---|---|
| "9:30到的急诊" (arrived at ER 9:30) | Security footage: ER arrival 10:08 | WRONG (arrived at hospital campus, not ER) |
| "等了将近两个小时" (waited ~2 hours) | 10:08 ER arrival -> 11:00 treatment = 52 min | EXAGGERATED (52 min, not 2 hours) |
| "没人管" (no one cared) | Nursing log: continuous monitoring, ECG, vitals | WRONG (nursing care was continuous) |
| "直到接近11点才治疗" (treatment near 11) | Treatment at 11:00, assessment at 10:55 | ACCURATE (treatment was at 11:00, though assessment began at 10:55) |

---

## 6. Token Budget

| Component | Tokens | % |
|---|---|---|
| Workspace | ~5,050 | 1.4% |
| Sessions | ~11,500 | 3.3% |
| Eval (30 rounds) | ~15,000 | 4.3% |
| Noise padding | ~318,500 | 91.0% |
| **Total** | **~350,000** | **100%** |

---

## 7. Eval Coverage

| Skill | Recall | Inference | Total |
|---|---|---|---|
| MS | R1, R3, R13, R22 | R2, R4, R15, R24, R29 | 9 |
| DU | R5, R6, R7 | R8, R9, R11, R23 | 7 |
| P | R10, R20 | R16, R25 | 4 |
| MD | R12, R14 | R18, R26 | 4 |
| DP | -- | R17, R27 | 2 |
| MP | -- | R19, R28 | 2 |
| MDP | -- | R21, R30 | 2 |
| **Total** | **11** | **19** | **30** |

exec_check: 9/30 = 30%
