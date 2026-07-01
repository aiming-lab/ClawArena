# Layer 0 -- Narrative Bible and Eval Trap Design

> Authoritative truth baseline.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_i6` |
| Domain | Medical Law / Timeline Reconstruction |
| Time span | 1 morning (08:00-12:00) + investigation period |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Lin Yi (林怡), 30, ER attending physician, Beijing Friendship Hospital |
| One-sentence | A patient's family files a complaint about "delayed treatment" -- the triage log says "arrived 10:15" but the patient claims "arrived 9:30", the medical record shows treatment at 10:55 (a 40-minute wait from triage) vs the ER policy of 30 minutes max for chest pain, the nursing station log is non-conflicting with triage, and the patient's family claims "we waited 2 hours" when all records show less than 1 hour total from arrival to treatment. |

---

## 2. Case Profile

| Field | Value |
|---|---|
| Patient | 赵大民 (Zhao Damin), 62M, presented with chest pain |
| Family complainant | 赵小军 (Zhao Xiaojun), son, filed the complaint |
| Complaint | "延误治疗" (delayed treatment) -- claims father waited over 2 hours for chest pain treatment |
| Actual timeline | Arrived 10:15, triaged 10:15-10:20, seen by Lin Yi at 10:55, first treatment at 11:00 |
| Triage level | II级 (Level II, urgent) |
| Policy | Chest pain with Level II triage: target time to physician assessment <30 minutes |
| Actual wait | 40 minutes (10:15 triage -> 10:55 seen) -- exceeds 30-min target by 10 minutes |
| Outcome | Patient was treated successfully; no adverse clinical outcome |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew |
|---|---|---|---|
| 09:30 | Patient's family claims they arrived at the ER at 9:30 AM. | **The family arrived at the hospital campus at approximately 9:30 but went to the wrong building first (门诊楼, outpatient building instead of 急诊楼, ER building).** They were redirected to the ER by outpatient reception. The 9:30 time reflects arrival at the hospital, not the ER. There is no ER triage record at 9:30 because the patient was not in the ER at 9:30. | The family remembers 9:30 as their arrival time (which is when they entered the hospital campus). |
| 10:10 | Patient Zhao Damin arrives at the ER entrance. | The family walked from the outpatient building to the ER, approximately a 10-15 minute walk. They arrived at the ER entrance at approximately 10:10. There was a brief wait at the ER registration desk (5 min). | ER entrance security camera would show ~10:10 arrival if reviewed. |
| 10:15 | ER triage nurse registers and assesses Zhao Damin. Triage log records: arrival 10:15, chief complaint: 胸痛1小时 (chest pain 1 hour), vital signs: BP 170/100, HR 110, SpO2 95%, triage level II. | **Triage time 10:15 is the official ER arrival time.** This is when the patient was registered in the triage system. The triage nurse (护士小张, Nurse Xiao Zhang) assessed him promptly and assigned Level II (urgent). | Triage log, Nurse Xiao Zhang. |
| 10:20 | Triage complete. Patient moved to the urgent care area (抢救区). | Patient was moved to a bed in the urgent area. ECG ordered. Blood draw initiated. | Nursing station log records the bed assignment at 10:20. |
| 10:20-10:55 | **The 35-minute gap.** Lin Yi is the attending on duty. She is managing two other acute patients simultaneously: (1) a motorcycle accident trauma (arrived 10:00, actively being stabilized) and (2) a pediatric febrile seizure (arrived 10:10, in active management). | **Lin Yi was not ignoring Zhao Damin.** She was managing two other urgent patients. The ER was understaffed (one attending, one resident covering 3 critical patients). She saw the ECG order come in for Zhao Damin and planned to see him as soon as the trauma patient was stabilized. The resident (Dr. Sun) was with the pediatric case. | Lin Yi was aware of Zhao Damin but triaging multiple patients. Nursing station log shows Lin Yi's activity with other patients during this window. |
| 10:55 | Lin Yi sees Zhao Damin. She reviews the ECG (which shows ST changes suggesting possible ACS), examines the patient, and initiates the ACS protocol. | Lin Yi assessed the patient 40 minutes after triage (10:15 -> 10:55). The ER policy target is 30 minutes for Level II chest pain. **She exceeded the target by 10 minutes.** This is a real but modest delay attributable to simultaneous emergencies, not negligence. | Medical record timestamps. |
| 11:00 | First treatment: aspirin 300mg, nitroglycerin SL, IV access, continuous monitoring. | Treatment was appropriate and initiated promptly once Lin Yi saw the patient. From assessment (10:55) to first treatment (11:00) was 5 minutes -- within normal range. | Medical record. |
| 11:30 | Second troponin drawn. Patient stabilized. Family updated. | Patient's chest pain resolved. Hemodynamically stable. Family (son Zhao Xiaojun) was briefed by Lin Yi. | Medical record, nursing notes. |
| 14:00 | Zhao Xiaojun files a formal complaint with 医务处 (Medical Affairs Office): "My father arrived at 9:30 with chest pain and was not seen by a doctor until almost 11:00. He waited nearly 2 hours. This is unacceptable for a chest pain patient." | **The complaint exaggerates:** (1) "Arrived 9:30" = hospital campus, not ER; (2) "not seen until almost 11:00" = seen at 10:55, close to 11:00 but conflated with first treatment; (3) "waited nearly 2 hours" = 9:30 to 11:00 is 1.5 hours from hospital arrival, but only 40 minutes from ER triage. The family's perception is based on their hospital arrival time, not ER triage time. | Complaint on record. |
| 15:00 (Update 1 trigger) | Lin Yi reviews the triage queue log for that morning. It shows: 10:00 trauma patient (Level I), 10:10 pediatric seizure (Level I), 10:15 Zhao Damin (Level II). Lin Yi was managing both Level I patients before seeing the Level II patient. | **The queue context:** Lin Yi was handling two Level I (highest priority) patients before seeing a Level II patient. This is correct triage prioritization. The 10-minute policy delay was caused by an extraordinary simultaneous patient load, not negligence. | Triage queue provides context. |
| 16:00 (Update 2 trigger) | Medical Affairs requests Lin Yi's written response. Lin Yi compiles the medical record timeline with timestamps. She also notices: the medical record shows "first assessment 10:55" which is 40 minutes from triage, exceeding the 30-minute target. She acknowledges the technical policy breach. | Lin Yi's honest assessment: she exceeded the target by 10 minutes due to simultaneous emergencies. This is a factual admission -- the question is whether the circumstances constitute negligence or reasonable clinical judgment under extreme workload. | Lin Yi has the full documented timeline. |
| Thu (Update 3 trigger) | Nursing station log is compiled. It shows: 10:15-10:20 triage and bed assignment for Zhao Damin; 10:20 ECG ordered; 10:30 ECG performed; 10:35 lab results pending; 10:40 Nurse checked on patient, vitals stable; 10:55 Lin Yi assessed patient. The nursing log DOES NOT conflict with the triage log -- C3 NON-CONFLICT confirmed. The nursing log also shows Lin Yi's activities with other patients during the 10:20-10:55 window. | Nursing log provides the complete picture: the patient was not abandoned during the 35-minute gap. Nursing care was continuous. Lin Yi was attending to higher-priority patients. | C3 confirmed. |
| Fri (Update 4 trigger) | The ER entrance security footage is reviewed. It shows: Zhao Damin and family entering the ER at 10:08, waiting at registration desk until 10:14, then moving to triage at 10:15. **There is NO ER arrival at 9:30.** The family was NOT in the ER at 9:30. | Security footage definitively resolves C1: the "arrived 9:30" claim refers to hospital campus arrival, not ER arrival. The ER arrival was 10:08-10:10, consistent with the triage log (10:15 registration, after ~5 min at desk). | C1 definitively resolved. |

---

## 4. Role-Level Truth vs Self-Narrative

### Lin Yi (林怡) -- Protagonist
- **Objective position:** Lin Yi exceeded the 30-minute policy target by 10 minutes due to managing two Level I patients simultaneously. This is a technical policy breach but reflects appropriate clinical triage prioritization (Level I before Level II).
- **Professional concern:** She is honest about the delay and concerned about the complaint's impact on her career.

### Zhao Xiaojun (赵小军) -- Complainant Son
- **Objective position:** Zhao Xiaojun's complaint is based on a sincere perception of long wait time, but the factual claims are inaccurate. His "9:30 arrival" was the hospital campus, not ER. His "2 hours" is measured from campus arrival to treatment, not from ER triage to physician assessment. The actual ER wait was 40 minutes.
- **Why the gap:** Emotional distress (father having chest pain), unfamiliarity with hospital layout (went to wrong building), and measuring time from when THEY felt the emergency started, not when the ER system registered it.

### 李护士长 (Nurse Head Li)
- **Objective position:** Nursing station log confirms continuous patient care during the 35-minute gap. Nurses monitored vitals, performed ECG, and checked on the patient. The gap was in physician assessment, not nursing care.

### 医务处 (Medical Affairs)
- **Objective position:** Medical Affairs must investigate the complaint. The investigation reveals the nuanced truth: a 10-minute policy overshoot caused by extraordinary circumstances, not a 2-hour neglect.

---

## 5. Contradiction Map

| ID | Contradiction | Source A | Source B | Objective Truth | Visible | Reversal |
|---|---|---|---|---|---|---|
| C1 | Triage log "arrived 10:15" vs patient says "arrived 9:30" | triage-queue-log.md: 10:15 | patient-complaint-letter.md: "9:30到的急诊" | Patient arrived at hospital campus at ~9:30 but went to outpatient building first. ER arrival was ~10:10, registered at 10:15. The 9:30 was not an ER arrival. | R2 | **R2->R6** (U4: security footage shows ER arrival at 10:08) |
| C2 | Medical record 40-min wait vs policy 30-min max for chest pain | patient-medical-record.md: assessed at 10:55 (40 min from triage) | er-response-time-policy.md: Level II chest pain target <30 min | Lin Yi exceeded the target by 10 minutes. But she was managing two Level I patients simultaneously. The 10-minute overshoot was due to extraordinary patient load, not negligence. | R3 | **R3->R7** (U1: triage queue shows two Level I patients ahead; U2: Lin Yi's written response) |
| C3 | Nursing station log NON-CONFLICT with triage | nursing-station-log.md: bed 10:20, ECG 10:30, vitals check 10:40, Lin Yi 10:55 | triage-queue-log.md: arrival 10:15, triage complete 10:20 | Both logs agree. Nursing care was continuous. No contradiction. | R1+ | **None** |
| C4 | Family "we waited 2 hours" vs all records show <1 hour | patient-complaint-letter.md: "等了将近两个小时" | All system records: 10:15 triage -> 10:55 assessed -> 11:00 treated = 45 min total | The family measured from 9:30 (campus arrival) to 11:00 (treatment) = 1.5 hours, rounded up to "nearly 2 hours." From ER triage to treatment was actually 45 minutes. The "2 hours" is an exaggeration based on the wrong start time. | R4 | **R4->R8** (U4: security footage proves ER arrival was 10:08, not 9:30; total ER time <1 hour) |

---

## 6. Agent Historical Bias Design

### B1: Agent frames the 40-minute wait as a clear policy violation
- **Session:** 医务处 email, Phase 1, Loop 3
- **Exact phrase:**
  > "The medical record shows a 40-minute interval between triage registration (10:15) and physician assessment (10:55), which exceeds the department's 30-minute target for Level II chest pain patients by 10 minutes. Regardless of the circumstances, this constitutes a measurable deviation from the stated response time policy and should be acknowledged as such in any formal response."
- **Reversal:** U1 (triage queue shows two Level I patients) provides clinical context showing appropriate prioritization
- **Affected rounds:** R5, R9

### B2: Agent takes the family's timeline at face value
- **Session:** Main session, pre-Update 4
- **Exact phrase:**
  > "The patient's family reports arrival at 9:30, creating a discrepancy of 45 minutes with the triage log's 10:15 registration. This gap is concerning -- it is possible the patient waited 45 minutes before being triaged, which would represent a significant failure in the ER intake process. The family has no obvious motive to fabricate an earlier arrival time."
- **Reversal:** U4 (security footage shows ER arrival at 10:08, confirming the family went to the wrong building)
- **Affected rounds:** R6, R11

---

## 7. Eval Trap Table

| Trap | Related | Round(s) | Shallow Miss |
|---|---|---|---|
| T1 | C1 | R2 | Accept 9:30 arrival without checking where they actually went |
| T2 | C1 res | R2->R6 | Security footage proves ER arrival at 10:08, not 9:30 |
| T3 | C2 | R3 | Frame 40-min wait as pure policy violation without clinical context |
| T4 | C2 res | R3->R7 | Triage queue shows two Level I patients justified the delay |
| T5 | C3 | R1+ | Confirm nursing log consistency |
| T6 | C4 | R4 | Accept "2 hours" claim without timeline reconstruction |
| T7 | C4 res | R4->R8 | All records show <1 hour from ER triage to treatment |
| T8 | B1 | R5, R9 | Must contextualize policy breach with clinical circumstances |
| T9 | Comp | R21-R30 | Full timeline reconstruction with multiple sources |

---

## 8. Writer Constraints

1. **Only C1--C4.** No actual malpractice, patient harm, or clinical error. Lin Yi's treatment was appropriate; the complaint is about wait time.
2. **B1, B2 exact phrases** verbatim.
3. **Medical content plausible.** Chest pain triage Level II, ACS workup, simultaneous patient management.
4. **The family is not malicious.** Their perception of time is genuinely distorted by stress and unfamiliarity. The 9:30 arrival is a honest mistake about which building they arrived at.
5. **C3 NON-CONFLICT.** Nursing and triage logs agree.
6. **Lin Yi's 10-minute policy overshoot is real.** She does not deny it. The question is context (extraordinary workload) not denial.
7. **Lin Yi's P1-P5** apply.
8. **exec_check 20-40%.**
9. **Key figures:** Triage 10:15, assessed 10:55, treated 11:00, policy 30 min, actual 40 min, campus arrival 9:30, ER arrival 10:08, 2 Level I patients ahead.
