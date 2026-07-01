# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_i1` |
| Domain | Emergency Medicine / Patient Safety |
| Time span | 1 night shift + morning handoff (~12 hours, 20:00--08:00) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Lin Yi (林怡), 30, ER attending physician at Beijing Friendship Hospital (北京友谊医院) |
| One-sentence | A chest-pain patient's critical handoff information is inconsistent across three systems (HIS electronic medical record, nursing handoff sheet, doctor verbal handoff notes) -- drug dosage, onset time, and prior allergy history each differ, and the discrepancies lead to a divergence in the subsequent treatment plan. |

---

## 2. Patient Profile (Clinical Object)

| Field | Value |
|---|---|
| Patient name | Zhang Guoqiang (张国强) |
| Patient ID | P20260315-0042 |
| Age / Sex | 58 / Male |
| Chief complaint | 胸痛2小时（chest pain for 2 hours） |
| Arrival time | 2026-03-15 20:35 |
| Triage level | II级（急诊优先） |
| Admitted by | Dr. Wang (王医生, 夜班前半段主治) |
| Handoff to | Dr. Lin Yi (林怡, 夜班后半段主治, 02:00 接班) |
| Key history | 高血压10年，糖尿病5年，冠心病3年，**青霉素过敏** |
| Initial presentation | Substernal crushing chest pain, diaphoresis, BP 165/95, HR 98, SpO2 96% |
| Working diagnosis | Acute coronary syndrome (ACS) rule-out, NSTEMI vs unstable angina |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| 20:35 | Patient Zhang Guoqiang arrives at ER via ambulance. Triage nurse Li Mei (李梅) performs initial assessment: BP 165/95, HR 98, SpO2 96%, chest pain rated 7/10. Triage level II. | Patient arrived with crushing substernal chest pain of 2 hours duration. **Actual onset was 18:30** (patient told the ambulance crew "about 6:30 PM"). Patient is diaphoretic and anxious. He mentions penicillin allergy to the triage nurse. | Triage nurse Li Mei documented onset time as "约2小时前" (approximately 2 hours ago) in the nursing triage sheet. Ambulance crew verbal report said "18:30发病" (onset 18:30). Patient told triage nurse about penicillin allergy. |
| 20:45 | Dr. Wang (王医生) sees the patient. Orders initial workup: 12-lead ECG, troponin, CBC, BMP, coagulation panel. Starts IV access. | Dr. Wang examined the patient and documented in HIS. He entered the onset time as "approximately 18:00" based on the patient saying "dinner time, around 6" during his exam (patient was less precise with Dr. Wang than with the ambulance crew). Dr. Wang ordered aspirin 300mg loading dose and noted it in HIS. He also ordered **nitroglycerin 0.5mg sublingual** and documented this in HIS. Dr. Wang recorded the penicillin allergy in the HIS allergy field. | Dr. Wang's HIS entry has onset "约18:00." Nursing triage sheet says "约2小时前" (which at 20:35 implies ~18:35). Ambulance crew report (verbal, not in any system) said 18:30. |
| 21:00 | ECG shows ST depression in leads V3-V6 and T-wave inversions. Dr. Wang's clinical impression: NSTEMI likely. Orders heparin drip. | Dr. Wang orders unfractionated heparin (UFH) with a bolus of 60 units/kg followed by infusion at 12 units/kg/hr. Patient weight estimated at 75kg. **Dr. Wang wrote the bolus as "4500 units" in HIS** (60 x 75 = 4500, correct). Nurse Li Mei administered the bolus and started the drip. | Dr. Wang, Nurse Li Mei, and the patient. Heparin order is in HIS. |
| 21:15 | First troponin result: 0.08 ng/mL (elevated, normal <0.04). Confirms NSTEMI diagnosis. Dr. Wang adjusts assessment in HIS. | Troponin confirms myocardial injury. Dr. Wang updates HIS diagnosis to "NSTEMI" and notes the troponin trend should be followed in 3 hours. He also adds clopidogrel 300mg loading dose to the medication orders. | Lab result in HIS. Dr. Wang documents the troponin and updated diagnosis. |
| 22:00 | Nurse shift change. Nurse Li Mei hands off to Nurse Chen Hong (陈红). Li Mei fills out the nursing handoff sheet. | **Nurse Li Mei fills out the handoff sheet hurriedly during a busy shift change.** She writes the nitroglycerin dose as **"0.5mg x 2" (meaning two sublingual doses were given)** but in the handoff sheet's medication column she abbreviates it as **"硝酸甘油 1mg"** (total dose, not per-dose). She also writes the heparin bolus as **"4000 units"** (rounding error from memory; actual was 4500 in HIS). She copies the onset time from her triage sheet as **"20:30左右"** (around 20:30) -- she confused the arrival time (20:35) with the onset time. **She does NOT include the penicillin allergy on the handoff sheet** because the allergy field on the paper handoff form was on the back side and she forgot to flip it. | Nurse Chen Hong now has the handoff sheet with: NTG "1mg", heparin bolus "4000u", onset "20:30左右", NO allergy notation. HIS has: NTG "0.5mg SL", heparin bolus "4500u", onset "约18:00", allergy "青霉素过敏." |
| 00:30 | Second troponin result: 0.45 ng/mL (rising trend). Repeat ECG shows persistent ST changes. Patient's pain is now 4/10 after nitroglycerin and morphine. | The troponin trend confirms significant myocardial injury. Dr. Wang considers whether the patient needs urgent catheterization or can be medically managed overnight. He decides to continue medical management and discuss with cardiology in the morning. | Lab result in HIS. Dr. Wang documents his reasoning. |
| 01:30 | Dr. Wang prepares verbal handoff notes for Lin Yi. He writes quick notes on a personal notepad (not in HIS). | **Dr. Wang is tired (end of a 14-hour shift). His verbal handoff notes record:** "chest pain patient, onset about 19:00" (splitting the difference between what he remembered -- he had earlier written 18:00 in HIS but now misremembers). He writes the heparin bolus correctly as "4500u" but notes the nitroglycerin as **"NTG 0.5mg x 1"** (he forgot the second dose that Nurse Li Mei gave at 21:30). He mentions "no significant allergy" in his notes -- he had entered the penicillin allergy in HIS but forgot it in his hurried handoff notes. | Dr. Wang's verbal notes: onset "约19:00", NTG "0.5mg x1", heparin "4500u", allergy "无特殊" (nothing significant). HIS: onset "约18:00", NTG "0.5mg SL", heparin "4500u", allergy "青霉素过敏." Nursing handoff: onset "20:30左右", NTG "1mg", heparin "4000u", allergy not recorded. |
| 02:00 | Lin Yi takes over the night shift. She receives verbal handoff from Dr. Wang (who is exhausted and leaves quickly) and reviews the nursing handoff sheet. She has not yet opened the patient's full HIS record. | Lin Yi now has two conflicting information sources: Dr. Wang's verbal notes and the nursing handoff sheet. She has not yet cross-checked against HIS. The discrepancies are: (C1) NTG dose: verbal "0.5mg x1" vs nursing "1mg"; (C2) onset time: verbal "约19:00" vs nursing "20:30左右"; (C4) allergy: verbal "无特殊" vs nursing "not recorded" -- both sources fail to mention the penicillin allergy that IS in HIS. | Lin Yi, Dr. Wang (leaving), Nurse Chen Hong (who is working from Li Mei's handoff sheet). |
| 02:30 | Lin Yi reviews the patient. BP 148/88, HR 86, pain 3/10. She considers the treatment plan going forward. | Lin Yi examines the patient. The patient is stable but she notices the information gaps. She asks Nurse Chen Hong about the medications and gets the nursing handoff sheet information. She has not yet opened HIS. | Lin Yi, Nurse Chen Hong. |
| 03:00 | Lin Yi opens HIS to review the full electronic record. She discovers the discrepancies. | **This is the key moment.** Lin Yi cross-references HIS (onset ~18:00, NTG 0.5mg SL, heparin 4500u, penicillin allergy documented) with nursing handoff (onset ~20:30, NTG 1mg, heparin 4000u, no allergy) and verbal notes (onset ~19:00, NTG 0.5mg x1, heparin 4500u, no significant allergy). She realizes the three sources are inconsistent on multiple critical data points. | Lin Yi now has all three sources and can see the discrepancies. |
| 03:30 (Update 1 trigger) | Third troponin result: 0.89 ng/mL (continuing rise). Lab results timeline now shows the full 3-point troponin trend. | The troponin trend (0.08 -> 0.45 -> 0.89) over ~6 hours is significant. Lin Yi cross-references the lab timeline with the onset time discrepancy -- if onset was 18:00 (HIS), the troponin curve is consistent with a 9-hour evolution; if onset was 20:30 (nursing), the rise is alarmingly fast for just 7 hours. **The lab timeline is internally consistent and does NOT contradict any source** -- it provides objective anchor points. | Lin Yi, lab system. |
| 04:00 | Lin Yi messages the #急诊科群 about antibiotic selection for a concurrent patient. Nurse Chen Hong mentions in passing that "this chest pain patient's allergy list seems empty on my sheet." | Lin Yi is now alerted to check the allergy status more carefully. She looks at HIS again and sees "青霉素过敏" in the allergy field. She realizes neither the verbal notes nor the nursing handoff mentioned this. | Lin Yi, Nurse Chen Hong. |
| 05:00 (Update 2 trigger) | Nurse Li Mei (previous shift) calls back to correct an error -- she realized she wrote the wrong onset time on the handoff sheet. "I confused the arrival time with the onset time. He said chest pain started around dinner time, about 6:30." | Li Mei's correction aligns with the ambulance crew's verbal report (18:30) and is close to Dr. Wang's HIS entry (18:00). This resolves the onset time discrepancy (C2) -- the nursing handoff's "20:30" was a mistake confusing arrival with onset. | Lin Yi, Nurse Li Mei (via phone). Dr. Wang's verbal note "19:00" remains an outlier but is explained by fatigue-related misremembering. |
| 06:00 (Update 3 trigger) | Lin Yi messages Dr. Sun (孙医生, resident) to review the medication administration record (MAR) in detail. The MAR shows: NTG 0.5mg SL at 20:50, NTG 0.5mg SL at 21:30 (repeat dose for persistent pain). Total NTG = 1mg. | The MAR resolves the NTG dose discrepancy (C1): Dr. Wang's original order was 0.5mg SL; a second 0.5mg dose was given 40 minutes later for persistent pain (also ordered by Dr. Wang in HIS). Nurse Li Mei's handoff "1mg" was the total; Dr. Wang's verbal note "0.5mg x1" missed the second dose; HIS records both individual orders. Heparin: HIS says 4500u (correct), nursing handoff says 4000u (Li Mei's rounding error from memory). | Lin Yi, Dr. Sun, MAR system. |
| 06:30 | Lin Yi discusses findings with Nurse Head Li (李护士长) about the allergy documentation gap. Li confirms the paper handoff form's allergy field is on the back and is frequently missed. | The allergy omission (C4) is explained: it is a systemic design flaw in the paper handoff form, not malicious omission. The allergy IS in HIS (entered by Dr. Wang) but was not carried over to the nursing handoff sheet or Dr. Wang's verbal notes. | Lin Yi, Nurse Head Li. |
| 07:00 (Update 4 trigger) | Dr. Zhang (张主任, department chief) arrives for morning rounds. Lin Yi presents the case including the handoff discrepancies. Zhang orders a review of the handoff process and asks Lin Yi to write a formal incident analysis. | Zhang pushes Lin Yi to formalize the findings. This prompts the comprehensive assessment that eval rounds R21-R30 will test. | Lin Yi, Dr. Zhang, morning rounds team. |

---

## 4. Role-Level Truth vs Self-Narrative

### Lin Yi (林怡) -- Protagonist, ER Attending Physician

- **Objective position:** Lin Yi took over the night shift at 02:00 and received inconsistent information from three sources: HIS, nursing handoff sheet, and doctor verbal notes. She methodically cross-referenced the sources and identified the discrepancies. Her trust bias (over-trusts objective test data like labs; underestimates subjective history details) initially led her to focus on the troponin trend rather than reconciling the onset time and medication dose discrepancies.
- **Public narrative:** In group communications (#急诊科群), Lin Yi presents clinical findings concisely and asks operational questions. She does not blame colleagues publicly.
- **Private narrative:** In DMs with Wang (colleague) and Li Nurse Head, she is concerned about the handoff quality and worried that the allergy omission could have led to a serious adverse event if penicillin-class antibiotics had been ordered for a concurrent infection.
- **Why the gap exists:** As a 30-year-old attending in a high-pressure ER, Lin Yi navigates a culture where questioning senior colleagues' handoff quality is sensitive. She documents discrepancies factually rather than assigning blame.

### Wang Yifan (王一凡, 王医生) -- Outgoing Night Shift Attending

- **Objective position:** Dr. Wang worked a 14-hour shift (12:00--02:00) and was exhausted at handoff. His HIS documentation was accurate (onset ~18:00, NTG 0.5mg SL, heparin 4500u, penicillin allergy recorded). However, his verbal handoff notes were sloppy: onset became "约19:00" (misremembered), NTG became "0.5mg x1" (forgot the repeat dose), and allergy became "无特殊" (omitted penicillin allergy from verbal notes despite recording it in HIS).
- **Public narrative:** Dr. Wang is a competent physician whose HIS documentation was correct. His verbal notes were hurried but he would argue "the record is in the system."
- **Private motivation:** Exhausted and wanting to go home. Not negligent, just fatigued.
- **Why the gap exists:** The gap between his accurate HIS entries and inaccurate verbal notes illustrates the system-dependent nature of medical handoffs -- critical information exists in the electronic system but may not be communicated verbally.

### Nurse Li Mei (李梅) -- Outgoing Triage/Bedside Nurse

- **Objective position:** Li Mei performed the initial triage accurately (BP, HR, SpO2 all correct) and administered medications correctly (NTG 0.5mg SL x2, heparin 4500u bolus). However, her handoff sheet had three errors: (1) NTG written as "1mg" total instead of "0.5mg x2"; (2) heparin bolus rounded to "4000u" from memory instead of "4500u"; (3) onset time confused with arrival time ("20:30" instead of "~18:30"); (4) penicillin allergy omitted because of the paper form's back-page design.
- **Public narrative:** Li Mei acknowledges her handoff sheet had errors when she calls back at 05:00 to correct the onset time. She is apologetic and professional.
- **Private motivation:** The ER was extremely busy during shift change. She was handling two other critical patients simultaneously.
- **Why the gap exists:** Nursing handoff sheets are paper-based and filled out from memory during chaotic shift changes, leading to transcription errors that would not occur if nurses referenced the electronic system directly.

### Nurse Chen Hong (陈红) -- Incoming Night Nurse

- **Objective position:** Chen Hong received the handoff sheet from Li Mei and is working from that sheet's information. She did not independently verify the sheet against HIS. She notices the allergy field is empty and mentions it in passing in the group chat.
- **Public narrative:** Professional and task-focused. She flags the empty allergy field when it becomes relevant.
- **Why the gap exists:** Chen Hong trusts the handoff sheet as the authoritative bedside document. Cross-checking every patient's handoff sheet against HIS is not standard practice during a busy night shift.

### Nurse Head Li (李护士长) -- Nursing Department Head

- **Objective position:** Li knows about the paper handoff form design flaw (allergy field on back page). She has previously flagged this to hospital administration but the forms have not been updated. She supports Lin Yi's investigation and confirms the systemic nature of the allergy documentation gap.
- **Public narrative:** Supportive of process improvement. Acknowledges the form design issue.
- **Why the gap exists:** The paper form design is a known issue that has not been prioritized for redesign.

### Dr. Sun (孙医生) -- Resident (Lin Yi's trainee)

- **Objective position:** Dr. Sun is a PGY-2 resident learning under Lin Yi. He helps review the medication administration record and verify the NTG dosing timeline. He provides detailed MAR data that resolves C1.
- **Public narrative:** Eager, thorough, learning from Lin Yi's systematic approach.
- **Why the gap exists:** As a resident, Dr. Sun follows Lin Yi's lead and provides data support.

### Dr. Zhang (张主任) -- Department Chief

- **Objective position:** Zhang arrives for morning rounds and learns about the handoff discrepancies. He takes the situation seriously and asks Lin Yi to formalize the analysis. He is concerned about patient safety implications but also wants to use this as a process improvement opportunity, not a blame exercise.
- **Public narrative:** Authoritative, process-oriented, patient-safety-focused.
- **Why the gap exists:** Zhang operates at the department leadership level. He wants documented analysis that can drive systemic improvements.

---

## 5. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Source C (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|---|
| C1 | Drug dosage discrepancy: HIS records NTG 0.5mg SL (x2 orders), nursing handoff says "1mg", doctor verbal notes say "0.5mg x1". Heparin bolus: HIS says 4500u, nursing says 4000u, verbal says 4500u. | his-patient-record.md (initial workspace): "硝酸甘油0.5mg 舌下含服" x2 orders (20:50 and 21:30); "肝素钠 4500u 静推" | nursing-handoff-sheet.md (initial workspace): "硝酸甘油 1mg"; "肝素 4000u" | doctor-verbal-notes.md (initial workspace): "NTG 0.5mg x1"; "heparin 4500u" | NTG: Two separate 0.5mg SL doses were given (total 1mg). Nursing handoff wrote the total; verbal notes missed the second dose; HIS has both individual orders. Heparin: HIS is correct at 4500u; nursing handoff's 4000u is a rounding error from memory. | R2 (three-source NTG discrepancy visible) | **Yes: R2-->R6** (MAR from Update 3 resolves: two individual 0.5mg doses, total 1mg; heparin was 4500u per HIS and MAR) |
| C2 | Onset time differs across 3 sources: HIS says "约18:00", nursing handoff says "20:30左右", doctor verbal notes say "约19:00" | his-patient-record.md: "发病时间：约18:00" | nursing-handoff-sheet.md: "发病时间：20:30左右" | doctor-verbal-notes.md: "onset about 19:00" | Actual onset was approximately 18:30 (patient told ambulance crew "about 6:30 PM"). HIS "18:00" is close (Dr. Wang documented from patient's vaguer statement "dinner time, around 6"). Nursing "20:30" confuses arrival time (20:35) with onset. Verbal "19:00" is Dr. Wang's fatigued misremembering at handoff. | R3 (three-source onset discrepancy visible) | **Yes: R3-->R7** (Nurse Li Mei's callback in Update 2 confirms onset ~18:30, resolving nursing error; verbal "19:00" explained by fatigue) |
| C3 | Lab result timeline -- NON-CONFLICT: troponin trend (0.08 -> 0.45 -> 0.89), ECG findings, and vital signs are consistent across all sources | lab-results-timeline.md (initial workspace): Troponin 21:15 = 0.08, 00:30 = 0.45; ECG timestamps consistent | his-patient-record.md: Same troponin values and timestamps in HIS records | medication-administration-record.md (Update 3): Timestamps for medication administration consistent with lab draws | All sources agree on lab values, ECG findings, vital sign trends, and their timestamps. No contradictions in the objective clinical data. Agent must synthesize the troponin trend across sources. | R1 onwards | **None** |
| C4 | Prior medical history (penicillin allergy) missing from nursing handoff and verbal notes but present in HIS | his-patient-record.md: "过敏史：青霉素过敏" (in the allergy field, entered by Dr. Wang) | nursing-handoff-sheet.md: Allergy field is **blank** (Li Mei forgot to flip to the back page of the form) | doctor-verbal-notes.md: "过敏：无特殊" (Dr. Wang forgot to mention it in verbal handoff despite recording it in HIS) | Patient IS allergic to penicillin. Dr. Wang correctly documented it in HIS. It was omitted from both the nursing handoff (paper form design flaw -- allergy field on back page) and verbal notes (fatigue-related omission). If a penicillin-class antibiotic had been ordered, this omission could have caused a serious adverse event. | R4 (allergy absent from 2 of 3 sources) | **Yes: R4-->R8** (Nurse Head Li confirms paper form design flaw in Update 3 context; HIS is definitive source; systemic issue identified) |

---

## 6. Agent Historical Bias Design (2 biases)

### B1: 林怡-王医生 IM -- Agent trusts Dr. Wang's verbal notes over nursing handoff because doctor-to-doctor communication is perceived as more reliable

- **Session and Loop:** 林怡-王医生 IM, Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "Since Dr. Wang's verbal handoff represents physician-to-physician communication and is based on his direct clinical assessment of the patient, his noted dosages and timeline should generally be given more weight than the nursing handoff sheet, which may contain transcription approximations."
- **Why the agent is misled:** The agent has seen the verbal notes (NTG 0.5mg x1, onset ~19:00, no significant allergy) and the nursing handoff (NTG 1mg, onset ~20:30, no allergy). Without checking HIS, the agent defaults to trusting the doctor's verbal notes as more authoritative because SOUL.md emphasizes evidence-based medicine and the physician's clinical assessment. The agent treats the nursing handoff as a "transcription approximation."
- **Reversal trigger:** Update 3 delivers MAR data showing two NTG doses (matching nursing total of 1mg, not verbal's single dose). HIS review confirms heparin was 4500u (matching verbal but not nursing's 4000u). The verbal notes are partially right and partially wrong -- just as the nursing notes are. Neither source is systematically more reliable than the other; HIS + MAR are the definitive records.
- **Affected eval rounds:** R5 (bias visible from Wang IM), R9 (full reversal after Update 3 MAR data)

### B2: 林怡-李护士长 IM -- Agent dismisses the allergy omission as a low-priority clerical issue

- **Session and Loop:** 林怡-李护士长 IM, Phase 1, Loop 3
- **Exact phrase that must appear in session:**
  > "The missing allergy notation on the nursing handoff sheet appears to be a minor documentation gap rather than a clinically significant omission -- the patient's primary presentation is cardiac, so penicillin-class antibiotics are unlikely to be part of the immediate treatment plan."
- **Why the agent is misled:** The agent correctly identifies that the current treatment plan (ACS management with heparin, aspirin, clopidogrel, nitroglycerin) does not involve penicillin-class antibiotics. The agent therefore treats the allergy omission as a documentation issue rather than a patient safety risk. It does not consider that ER patients frequently develop concurrent conditions (e.g., aspiration pneumonia, urinary tract infection) that may require antibiotics, and the allergy information must be available for any future ordering decision.
- **Reversal trigger:** Update 3/4 context reveals that Nurse Head Li confirms the paper form design flaw is a systemic issue that has caused near-miss events before. The allergy omission is not "minor" -- it is a patient safety gap that could lead to anaphylaxis if antibiotics are ordered by a covering physician who only checks the bedside handoff sheet and not HIS. Dr. Zhang (morning rounds, Update 4) specifically flags this as the most concerning finding.
- **Affected eval rounds:** R8 (bias visible from Li Nurse Head IM), R11 (full reversal after Update 3+4 combined evidence)

---

## 7. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (NTG dose partial) | -- | R2, R3 | No (R2-R3 internal) | Shallow agents will see three different NTG dose representations and may not realize they can all be reconciled: 0.5mg x2 individual doses = 1mg total. The nursing sheet wrote the total; the verbal notes missed a dose; HIS has both individual orders. |
| T2 | C1 (NTG dose full resolution) | B1 seed | R2-->R6 | **Yes** | After Update 3, the MAR confirms two separate 0.5mg doses at 20:50 and 21:30. The nursing handoff's "1mg" was the correct total, and the verbal notes' "0.5mg x1" was incomplete. Agents who trusted the verbal notes over the nursing sheet (B1) must revise. |
| T3 | C2 (onset time partial) | -- | R3 | No (R3 internal) | Shallow agents will see three different onset times (18:00, 19:00, 20:30) and may average them or pick the "most authoritative" source. The correct approach is to identify that 20:30 confuses arrival with onset, 19:00 is fatigue-related misremembering, and 18:00 is closest to truth. |
| T4 | C2 (onset time full resolution) | -- | R3-->R7 | **Yes** | After Update 2, Nurse Li Mei's callback confirms onset ~18:30 (aligned with ambulance crew report). The nursing handoff "20:30" is definitively a clerical error (arrival vs onset confusion). HIS "18:00" is the closest documented estimate. |
| T5 | C3 (lab timeline, non-conflict) | -- | R1 onwards | No (persistent synthesis) | Agents must synthesize the troponin trend (0.08 -> 0.45 -> 0.89) across time and correlate it with onset time to assess the clinical trajectory. The lab data is the objective anchor. No single source has the complete lab-clinical-timeline synthesis. |
| T6 | C4 (allergy omission partial) | B2 seed | R4 | No (R4 internal) | Shallow agents will note the allergy is missing from handoff sources but present in HIS, and may dismiss it as a documentation issue since the current treatment doesn't involve penicillin. They will miss the patient safety implications for concurrent or future conditions. |
| T7 | C4 (allergy omission full) | B2 | R4-->R8 | **Yes** | After Update 3+4, the systemic nature of the paper form design flaw is revealed. The allergy omission is a patient safety gap, not a clerical inconvenience. Dr. Zhang flags this as the most concerning finding. |
| T8 | B1 (verbal note trust) | B1 | R5, R9 | **Yes** | Agents must recognize that trusting verbal notes over nursing handoff is not evidence-based -- both sources had errors. HIS + MAR are the definitive records. The correct approach is to always cross-reference bedside documents against the electronic system. |
| T9 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R21-R30 | Comprehensive reversal review | Agents must synthesize all evidence: NTG dose reconciliation (two 0.5mg doses = 1mg total), onset time resolution (~18:30 via callback), lab timeline correlation (troponin curve consistent with ~18:00-18:30 onset), allergy omission as systemic patient safety issue. Must present in Lin Yi's preferred format (structured case format, diagnosis first, evidence-based, concise professional). |

---

## 8. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new discrepancies, additional patients, or new character conflicts beyond what is specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops. The core wording must appear word-for-word. Surrounding context may be added for natural flow, but the specified sentence must appear intact.
3. **Each contradiction must have identifiable traces in at least two independent sources** (two different sessions, or one session + one workspace file).
4. **Timestamps must be self-consistent:** Patient arrival 20:35. Dr. Wang sees patient 20:45. ECG/orders 21:00. First troponin 21:15. Nurse shift change 22:00. Second troponin 00:30. Dr. Wang verbal handoff prep 01:30. Lin Yi takes over 02:00. Lin Yi reviews HIS 03:00. Third troponin 03:30. Li Mei callback 05:00. MAR review 06:00. Morning rounds 07:00.
5. **Medical content must be clinically plausible.** NSTEMI management with aspirin, clopidogrel, heparin, and nitroglycerin is standard. Troponin trend (0.08 -> 0.45 -> 0.89) is realistic for NSTEMI. Vital signs and ECG findings must be internally consistent.
6. **Dr. Wang's documentation gap** should be understandable (14-hour shift fatigue) but not negligent. His HIS documentation was accurate; his verbal notes were sloppy.
7. **C3 (lab result timeline) is NON-CONFLICT** -- all sources must be consistent on lab values, ECG findings, and vital sign timestamps. The challenge is synthesis across multiple sources, not contradiction detection.
8. **Nurse Li Mei's handoff errors** should be understandable (busy shift change, paper form design) but clinically significant.
9. **The penicillin allergy omission (C4)** is the most safety-critical finding. It exists in HIS but was omitted from both the nursing handoff and verbal notes through independent mechanisms (paper form design flaw + fatigue).
10. **Noise content** must not introduce contradictions beyond C1--C4. Noise topics include: other ER patients, staffing discussions, equipment issues, supply requests, scheduling, teaching cases, administrative announcements.
11. **All data text must be in Chinese** for session messages (reflecting the Chinese hospital context) and in a mix of Chinese and English for workspace files (reflecting medical system exports that contain bilingual content -- medical terminology often uses English abbreviations). Agent responses and eval questions are in English.
12. **Personalization requirement (P1-P5):** Lin Yi prefers (P1) structured case format (主诉/现病史/查体/辅助检查/诊断/处理), (P2) date+patientID naming (2026-03-15_P001_急诊记录.md), (P3) diagnosis/conclusion first then differential diagnosis and evidence chain, (P4) evidence-based medicine (cite guidelines, graded evidence), (P5) concise and professional -- ER context means no unnecessary words. These preferences must be introduced progressively in 4 injection stages in the main session calibration and tested in P-I eval rounds.
13. **exec_check questions** must constitute 20-40% of total rounds. These rounds test whether the agent correctly uses workspace tools (exec ls, read, sessions_history) before answering.
14. **Factual figures must be internally consistent:** NTG: 0.5mg SL x2 doses (total 1mg); first dose 20:50, second dose 21:30. Heparin bolus: 4500 units (60 units/kg x 75kg). Troponin: 0.08 (21:15), 0.45 (00:30), 0.89 (03:30). Patient weight: ~75kg. BP on arrival: 165/95. HR: 98. SpO2: 96%.
