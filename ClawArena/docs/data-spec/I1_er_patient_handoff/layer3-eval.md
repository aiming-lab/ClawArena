# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many (agent determines how many to select).
> Scoring: agent uses `\bbox{A,C,F}` format; exact set match against answer key.
> All question text and option text must be in English.
> ~30 rounds covering MS-R, MS-I, DU-R, DU-I, P-R, P-I, MD-R, MD-I, DP-I, MP-I, MDP-I + exec_check (20-40% of rounds).
> exec_check rounds test whether the agent correctly uses workspace tools before answering.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Lab result timeline cross-source synthesis (C3, non-conflict) + tool use | No | No |
| r2 | multi_choice | MS-I | NTG dose discrepancy inference -- HIS vs nursing vs verbal (C1 partial) | No | Yes (R2->R6 seed) |
| r3 | multi_choice | MS-R | Onset time discrepancy -- three-source comparison (C2) | No | Yes (R3->R7 seed) |
| r4 | multi_choice | MS-I | Allergy omission detection -- HIS vs nursing vs verbal (C4 partial) | No | Yes (R4->R8 seed) |
| r5 | multi_choice | DU-R | Reassess source reliability after troponin update (C3 extended + B1 visible) | Yes (Update 1) | Yes (R5->R9 seed via B1) |
| r6 | multi_choice | DU-R, exec_check | Reassess NTG dose after full MAR data (C1 reversal) | Yes (Update 3) | Yes (R2->R6 via C1) |
| r7 | multi_choice | DU-R | Reassess onset time after nurse callback (C2 reversal) | Yes (Update 2) | Yes (R3->R7 via C2) |
| r8 | multi_choice | DU-I | Reassess allergy omission severity after systemic evidence (C4 reversal) | Yes (Update 3+4) | Yes (R4->R8 via C4) |
| r9 | multi_choice | DU-I, exec_check | Reassess B1 bias -- verbal notes vs nursing handoff reliability (B1 full reversal) | Yes (Update 3) | Yes (R5->R9 via B1) |
| r10 | multi_choice | P-R | User preference identification (structured case format, date+ID naming, diagnosis first, EBM, concise) | No | No |
| r11 | multi_choice | DU-I | Integrate B2 reversal -- allergy omission is systemic safety gap, not minor (B2 full reversal) | Yes (Update 3+4) | No |
| r12 | multi_choice | MD-R, exec_check | Source reliability ranking -- HIS vs MAR vs nursing vs verbal | No | No |
| r13 | multi_choice | MS-R | Heparin dose reconciliation -- which sources agree, which disagree? | No | No |
| r14 | multi_choice | MD-R, exec_check | Nursing handoff error analysis -- what caused each error? | No | No |
| r15 | multi_choice | MS-I | Troponin trend interpretation given corrected onset time | Yes (Update 1+2) | No |
| r16 | multi_choice | P-I | Generate clinical summary in Lin Yi's preferred format (structured case, EBM) | Yes (Update 3) | No |
| r17 | multi_choice | DP-I, exec_check | B1 bias identification -- what was the phrase, where, and what corrected it? | Yes (Update 3) | No |
| r18 | multi_choice | MD-I | Dr. Wang's documentation analysis -- HIS accurate vs verbal sloppy, why? | No | No |
| r19 | multi_choice | MP-I | Handoff process failure analysis -- systemic vs individual factors | Yes (Update 3+4) | No |
| r20 | multi_choice | P-R | User preference compliance check -- does response apply all 5 preferences? | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive handoff discrepancy assessment -- all evidence integrated | Yes (all updates) | Yes (R2+R3+R4 comprehensive) |
| r22 | multi_choice | MS-R | C3 non-conflict synthesis -- confirm all sources consistent on lab values | No | No |
| r23 | multi_choice | DU-R | B2 bias identification -- allergy minimization phrase and systemic correction | Yes (Update 3+4) | No |
| r24 | multi_choice | MS-I, exec_check | Medication reconciliation -- complete dose verification across all sources | Yes (Update 3) | No |
| r25 | multi_choice | P-I | Format the incident analysis report in Lin Yi's preferred style | Yes (Update 4) | No |
| r26 | multi_choice | MD-I | Patient safety risk assessment -- what could have gone wrong? | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | MAR as definitive record -- does it align with HIS, correct nursing, correct verbal? | Yes (Update 3) | No |
| r28 | multi_choice | MP-I | Stakeholder analysis -- Dr. Wang, nurses, Zhang, systemic factors | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Process improvement recommendations -- what changes would prevent recurrence? | Yes (Update 4) | No |
| r30 | multi_choice | MDP-I | Final comprehensive -- all contradictions resolved, all biases corrected, formal analysis | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R6, R9, R12, R14, R17, R21, R24, R27 = 9 out of 30 = 30% (within 20-40% target)

---

## 2. Option Design Principles

| Type | Count per Round | Description |
|---|---|---|
| Truly correct | 3-5 | Clear evidence supports the statement |
| Real material but wrong detail | 2-3 | Event is real but attribution, timing, dose, or mechanism is wrong |
| Single-source unverified | 1-2 | One person said it, no corroboration or active contradiction |
| Fabricated distractor | 1-2 | No corresponding material; wording mimics clinical content |

---

## 3. Round Specs

### R1: Lab Result Timeline Cross-Source Synthesis (MS-R, exec_check) -- Calibration (unscored)

**exec_check requirement:** Agent must call `exec ls` and `read lab-results-timeline.md` before answering. If agent answers without referencing workspace files, exec_check fails.

**User calibration message before R1:** "输出用病例格式：主诉、现病史、查体、辅助检查、诊断、处理。先给诊断结论。"

**Question:**
> "Based on workspace documents and session history, which statements about the patient's lab results and clinical timeline are supported by evidence? (Before answering, make sure you've reviewed the workspace files.)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The first troponin result (0.08 ng/mL) was drawn at 21:15, approximately 45 minutes after the patient was seen by Dr. Wang. | YES | lab-results-timeline.md + his-patient-record.md (Dr. Wang saw patient at 20:45) | Direct fact, C3 synthesis |
| B | The second troponin result (0.45 ng/mL) at 00:30 represents a 5.6-fold increase from the first, consistent with evolving myocardial injury. | YES | lab-results-timeline.md | Direct calculation, C3 |
| C | The ECG showed ST elevation in leads V3-V6, consistent with STEMI. | NO | HIS shows ST depression and T-wave inversion, not ST elevation | Wrong ECG finding (NSTEMI not STEMI) |
| D | The APTT at 00:30 was 65 seconds, which is within the therapeutic range for heparin anticoagulation in ACS management. | YES | lab-results-timeline.md | Direct fact, C3 |
| E | The troponin and ECG results are consistent across all documentation sources -- HIS, nursing handoff, and lab system all report the same values and timestamps. | YES | Cross-source comparison | C3 non-conflict conclusion |
| F | The patient's glucose level of 8.9 mmol/L reflects his known diabetes mellitus, documented in the past medical history. | YES | lab-results-timeline.md + his-patient-record.md | Cross-reference, C3 |
| G | Lab results show the patient was on warfarin with an INR of 2.5 at the time of arrival. | NO | Lab shows INR 1.0, no warfarin use documented | Fabricated medication/lab value |
| H | The coagulation panel (PT 12.5s, APTT 28s pre-heparin, INR 1.0) at baseline was normal, providing a valid baseline before heparin initiation. | YES | lab-results-timeline.md | Direct fact, C3 |

**answer:** `["A", "B", "D", "E", "F", "H"]`

**question_class:** `calibration` (R1 establishes P1 structured case format preference -- agent should respond with clinical structure)

---

### R2: NTG Dose Discrepancy Inference (MS-I) -- Calibration (unscored)

**User calibration message before R2:** "诊断结论先写，鉴别诊断和证据链跟后面。"

**Question:**
> "Based on all currently available evidence (before MAR update), which statements about the nitroglycerin dosage discrepancy are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | HIS records two separate nitroglycerin orders: 0.5mg SL at 20:50 and 0.5mg SL at 21:30 (repeat dose for persistent pain). | YES | his-patient-record.md | Direct fact, C1 HIS source |
| B | The nursing handoff sheet records "硝酸甘油 1mg" without specifying whether this was a single dose or a total of multiple doses. | YES | nursing-handoff-sheet.md | Direct fact, C1 nursing source |
| C | Dr. Wang's verbal handoff notes record "NTG 0.5mg x1 SL," indicating only one dose was given. | YES | doctor-verbal-notes.md | Direct fact, C1 verbal source |
| D | The three sources present three different representations of the NTG administration: HIS shows 0.5mg x2, nursing shows 1mg, verbal shows 0.5mg x1. These could potentially be reconciled (0.5mg x 2 = 1mg total), but the verbal notes' "x1" contradicts HIS's two orders. | YES | Cross-source analysis | C1 discrepancy framing |
| E | The nursing handoff sheet's "1mg" notation could represent the total dose from two 0.5mg administrations, which would be consistent with HIS if the sheet records totals rather than individual doses. | YES | Logical inference | Possible reconciliation |
| F | Dr. Wang confirmed in the IM session that a second NTG dose was given at 21:30 for persistent pain, which he forgot to include in his verbal handoff notes. | YES | Wang Doctor IM Loop 3 | Session evidence |
| G | The nursing handoff sheet explicitly states "硝酸甘油 0.5mg x 2次" (two doses of 0.5mg each). | NO | Nursing sheet says "1mg" without the "x 2" detail | Fabricated nursing notation |
| H | The maximum safe sublingual nitroglycerin dose is 0.4mg, making the "0.5mg" orders in HIS a potential medication error. | NO | Standard NTG SL dose is 0.3-0.6mg; 0.5mg is within range | Fabricated safety concern |

**answer:** `["A", "B", "C", "D", "E", "F"]`

**question_class:** `calibration` (P3 diagnosis-first preference established)

---

### R3: Onset Time Discrepancy -- Three-Source Comparison (MS-R) -- C2

**Question:**
> "Based on all currently available evidence, which statements about the onset time discrepancy are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | HIS records the onset time as "约18:00" (approximately 18:00), based on Dr. Wang's documentation of the patient's statement that chest pain began "at dinner time, around 6." | YES | his-patient-record.md | Direct fact, C2 HIS source |
| B | The nursing handoff sheet records onset time as "20:30左右" (around 20:30), which is suspiciously close to the actual arrival time of 20:35. | YES | nursing-handoff-sheet.md | Direct fact, C2 nursing source |
| C | Dr. Wang's verbal handoff notes record onset as "约19:00," which differs from his own HIS entry of "约18:00." | YES | doctor-verbal-notes.md vs his-patient-record.md | Direct comparison, C2 verbal source |
| D | The nursing handoff's "20:30" onset time likely confuses the patient's arrival time (20:35) with the symptom onset time -- the two times are within 5 minutes of each other, suggesting a transcription mix-up. | YES | Logical inference from arrival time proximity | C2 key inference |
| E | All three sources agree that the onset was sometime in the evening of March 15, 2026, but disagree on the specific hour: 18:00 (HIS), 19:00 (verbal), 20:30 (nursing). | YES | Cross-source synthesis | C2 summary |
| F | The onset time has clinical significance because it affects the interpretation of the troponin trend -- a 0.08 to 0.45 rise over 6.5 hours (from 18:00 onset) has different implications than the same rise over 4 hours (from 20:30 onset). | YES | Clinical reasoning + lab data | Clinical impact of C2 |
| G | Dr. Wang's verbal notes say "约20:00," splitting the difference between the other two sources. | NO | Verbal notes say "约19:00," not "约20:00" | Wrong verbal time |
| H | The ambulance crew documented the onset time as 18:30 in the EMS run sheet, which is available in the workspace. | NO | Ambulance crew verbal report was not documented in any workspace file | Fabricated documentation |

**answer:** `["A", "B", "C", "D", "E", "F"]`

---

### R4: Allergy Omission Detection (MS-I) -- C4 Partial

**Question:**
> "Based on all currently available evidence, which statements about the patient's allergy documentation are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | HIS records "青霉素过敏" (penicillin allergy) in the structured allergy field, entered by Dr. Wang during the initial evaluation. | YES | his-patient-record.md | Direct fact, C4 HIS source |
| B | The nursing handoff sheet's allergy field is blank -- no allergy information was recorded during the nursing shift change. | YES | nursing-handoff-sheet.md | Direct fact, C4 nursing source |
| C | Dr. Wang's verbal handoff notes state "过敏：无特殊" (allergies: nothing significant), omitting the penicillin allergy despite having documented it in HIS. | YES | doctor-verbal-notes.md | Direct fact, C4 verbal source |
| D | The penicillin allergy is documented in exactly one of the three sources (HIS) and absent from the other two (nursing handoff and verbal notes), creating a critical information gap for any clinician relying on the non-HIS sources. | YES | Cross-source comparison | C4 gap analysis |
| E | Dr. Wang confirmed in the IM session that he did record the penicillin allergy in HIS but forgot to mention it in his verbal handoff notes due to fatigue. | YES | Wang Doctor IM Loop 4 | Session evidence |
| F | Nurse Chen Hong mentioned in the #急诊科群 that the allergy field on the handoff sheet appeared empty, alerting Lin Yi to check HIS. | YES | ER Group IM Loop 3/4 context | Session evidence |
| G | The nursing handoff sheet explicitly states "过敏：无" (allergies: none), confirming the patient has no allergies. | NO | The field is blank (empty), not filled with "无" -- blank and "无" have different meanings | Wrong distinction |
| H | The allergy omission has no clinical significance because penicillin-class antibiotics are not part of ACS management. | NO | While true for current treatment, ER patients may develop concurrent conditions requiring antibiotics | Misleading clinical logic (B2 trap) |
| I | Multiple nurses in the #急诊科群 confirmed that the handoff form's allergy field on the back page is frequently missed during busy shifts. | YES | ER Group IM Loop 4 | Systemic evidence |

**answer:** `["A", "B", "C", "D", "E", "F", "I"]`

---

### R5: Reassess Source Reliability After Troponin Update (DU-R) -- C3 Extended + B1 Visible

**Question:**
> "After the third troponin result (Update 1), which statements about source reliability and clinical interpretation are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The three-point troponin trend (0.08 -> 0.45 -> 0.89 over ~6 hours from 21:15 to 03:30) shows a continuing significant rise consistent with evolving NSTEMI. | YES | lab-results-timeline.md (updated) | C3 extended data |
| B | If the onset was ~18:00 (HIS), the troponin trend represents a ~9.5-hour evolution, consistent with moderate NSTEMI kinetics per ACS guidelines. | YES | Clinical reasoning with corrected timeline | C3 + C2 integration |
| C | If the onset was ~20:30 (nursing), the same troponin trend represents only a ~7-hour evolution, suggesting a faster rise that could indicate a larger infarct territory. | YES | Clinical reasoning with nursing timeline | C2 clinical impact |
| D | The lab results are the most objective data source in this case -- they are instrument-generated, timestamped, and consistent across all documentation sources. | YES | Source reliability principle | C3 reliability assessment |
| E | The APTT at 03:30 is 72 seconds (slightly supratherapeutic), suggesting the heparin dose may need adjustment but confirming that heparin is being administered. | YES | lab-results-timeline.md (updated) | Clinical data point |
| F | The troponin trend supports the HIS onset time (~18:00) as more clinically plausible than the nursing onset time (~20:30), because the rate of rise is more consistent with typical NSTEMI kinetics at the earlier onset. | YES | Clinical reasoning | C2 resolution support |
| G | The third troponin result shows a decline to 0.30, suggesting the patient's myocardial injury is resolving. | NO | Troponin is 0.89 (rising), not 0.30 (declining) | Fabricated lab value |
| H | The CK-MB trend (12 -> 28 -> 52) mirrors the troponin trend and independently confirms ongoing myocardial injury. | YES | lab-results-timeline.md (updated) | C3 corroboration |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

---

### R6: Reassess NTG Dose After Full MAR Data (DU-R, exec_check) -- C1 Reversal

**exec_check requirement:** Agent must call `read medication-administration-record.md` before answering.

**Question:**
> "After receiving the full medication administration record (Update 3), which statements about the NTG dosage discrepancy are now supported by evidence? (Please review medication-administration-record.md before answering.)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The MAR confirms two separate NTG 0.5mg SL administrations: first at 20:50, second at 21:30 (repeat for persistent pain), totaling 1mg. | YES | medication-administration-record.md (updated) | C1 definitive resolution |
| B | The nursing handoff sheet's "1mg" was the correct total dose, while Dr. Wang's verbal notes' "0.5mg x1" incorrectly omitted the second dose. | YES | MAR vs nursing vs verbal comparison | C1 reversal conclusion |
| C | The MAR (medication administration record) is the definitive source for what was actually given because it records each individual administration event with timestamp, dose, and administering nurse. | YES | Source reliability principle | MAR authority |
| D | The heparin bolus is confirmed as 4500 units in both HIS and MAR, establishing that the nursing handoff's "4000u" was a memory-based rounding error. | YES | MAR + HIS vs nursing comparison | C1 heparin resolution |
| E | The earlier assessment that gave more weight to Dr. Wang's verbal notes over the nursing handoff (B1 bias) must be revised -- the nursing total was correct while the verbal notes were incomplete. | YES | B1 correction | B1 reversal |
| F | The MAR shows that Nurse Li Mei administered all medications correctly despite the errors in her handoff sheet documentation. | YES | MAR administration records | Important distinction: execution vs documentation |
| G | The MAR confirms that only one NTG dose was given, supporting Dr. Wang's verbal notes over the nursing handoff. | NO | MAR shows two doses | Direct contradiction of MAR evidence |
| H | The MAR shows the heparin bolus was 4000 units, confirming the nursing handoff sheet. | NO | MAR confirms 4500u, not 4000u | Wrong MAR data |

**answer:** `["A", "B", "C", "D", "E", "F"]`

---

### R7: Reassess Onset Time After Nurse Callback (DU-R) -- C2 Reversal

**Question:**
> "After Nurse Li Mei's callback (Update 2), which statements about the onset time discrepancy are now supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Nurse Li Mei confirmed that she confused the patient's arrival time (20:35) with the onset time when filling out the handoff sheet, explaining the "20:30" entry. | YES | nurse-callback-transcript.md | C2 definitive resolution |
| B | Li Mei reported that the ambulance crew told her the onset was "18:30发病" (onset at 18:30), which aligns with HIS's "约18:00" estimate. | YES | nurse-callback-transcript.md | C2 corroboration |
| C | The onset time can now be estimated as approximately 18:00-18:30 based on convergent evidence: HIS (~18:00), ambulance crew report (~18:30 per Li Mei), and Li Mei's correction (~18:30). | YES | Multi-source convergence | C2 resolution |
| D | Dr. Wang's verbal notes' "约19:00" is explained by fatigue-related misremembering at the end of a 14-hour shift -- he had correctly documented "约18:00" in HIS hours earlier. | YES | Context from Wang IM + verbal notes vs HIS | C2 explanation |
| E | The corrected onset time (~18:00-18:30) is consistent with the troponin trend kinetics, confirming the clinical trajectory of a moderate NSTEMI over ~9-10 hours. | YES | Lab data + corrected timeline | C2 + C3 integration |
| F | Li Mei admitted that she filled out the handoff sheet from memory without consulting HIS, explaining all the documentation errors (onset, NTG dose, heparin dose). | YES | nurse-callback-transcript.md | Root cause for nursing errors |
| G | The ambulance crew's run sheet, now available in the workspace, documents the onset time as 18:30. | NO | Ambulance crew report is verbal only; no run sheet in workspace | Fabricated document |
| H | All three sources now agree on the onset time after Li Mei's correction. | NO | Wang's verbal "19:00" remains different; it's explained but not corrected in the document | Oversimplification |

**answer:** `["A", "B", "C", "D", "E", "F"]`

---

### R8: Reassess Allergy Omission Severity After Systemic Evidence (DU-I) -- C4 Reversal

**Question:**
> "After Nurse Head Li's systemic evidence and Dr. Zhang's morning rounds assessment (Updates 3+4), which statements about the allergy omission are now supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Nurse Head Li confirmed that the paper handoff form's allergy field is on the back page and has been a known documentation issue, with prior near-miss events where allergies were missed. | YES | Nurse Head Li IM Phase 2 Loop 10 | C4 systemic evidence |
| B | Dr. Zhang identified the allergy omission as the most safety-critical finding in the handoff discrepancy analysis, specifically citing the risk of a penicillin-class antibiotic being ordered if a clinician relies only on the handoff sheet. | YES | morning-rounds-summary.md + Zhang IM Phase 2 | C4 authority assessment |
| C | The earlier assessment that the allergy omission was "a minor documentation gap" (B2 bias) must be revised -- it is a systemic patient safety gap with documented near-miss history, not a low-priority clerical issue. | YES | B2 correction | B2 reversal |
| D | The allergy omission resulted from two independent failures: (1) the paper form design flaw (allergy on back page) caused the nursing omission, and (2) Dr. Wang's fatigue caused the verbal notes omission. HIS was the only system that correctly captured the allergy. | YES | Multi-factor analysis | C4 root cause |
| E | Nurse Head Li has proposed three concrete improvements: move allergy to front page, require HIS verification at handoff, and implement automatic HIS-to-handoff printing. | YES | Nurse Head Li IM Phase 2 Loop 11 | Process improvement |
| F | The allergy omission directly harmed the patient during this admission. | NO | No adverse event occurred; penicillin was not ordered | Wrong -- latent risk, not realized harm |
| G | Dr. Zhang framed the analysis as a blame exercise targeting Nurse Li Mei for the documentation errors. | NO | Zhang explicitly said "不是追责，是改流程" (not about blame, about fixing process) | Fabricated blame framing |
| H | The penicillin allergy omission could have led to anaphylaxis if a concurrent infection (e.g., aspiration pneumonia) had required antibiotic selection during the night shift, and a covering physician relied only on the bedside handoff sheet. | YES | Clinical reasoning from Zhang + Li assessments | C4 risk quantification |

**answer:** `["A", "B", "C", "D", "E", "H"]`

---

### R9: B1 Bias Full Reversal -- Verbal Notes vs Nursing Handoff (DU-I, exec_check)

**exec_check requirement:** Agent must read session history for Wang Doctor IM before answering.

**Question:**
> "The agent previously stated that Dr. Wang's verbal handoff should 'generally be given more weight than the nursing handoff sheet.' With all evidence now available, which assessments of source reliability are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The B1 bias phrase privileged physician-to-physician communication over nursing documentation, but the MAR showed the nursing total (1mg) was correct while the verbal notes (0.5mg x1) were incomplete. | YES | MAR + B1 analysis | B1 reversal core |
| B | Neither the verbal notes nor the nursing handoff was systematically more reliable -- each had different errors. Verbal missed a dose; nursing rounded the heparin and confused onset with arrival. | YES | Comprehensive error analysis | B1 reversal conclusion |
| C | The correct hierarchy is: HIS/MAR (electronic, timestamped) > nursing documentation (contemporaneous paper) > verbal notes (memory-dependent, end-of-shift fatigue). Neither nursing nor verbal should be unconditionally trusted over the other. | YES | Source reliability principle | Corrected hierarchy |
| D | Dr. Wang's verbal notes were accurate on all data points except the onset time, which was a minor variation. | NO | Verbal notes also missed the second NTG dose and omitted the penicillin allergy | Understates verbal errors |
| E | The nursing handoff sheet was wrong on every data point it reported. | NO | Nursing total NTG (1mg) was correct; aspirin, clopidogrel, morphine doses were correct | Overstates nursing errors |
| F | The key lesson is that bedside documents (whether nursing sheets or verbal notes) should always be cross-referenced against electronic system records (HIS, MAR) before clinical decisions are made. | YES | Synthesis of all evidence | Process conclusion |
| G | After this analysis, verbal handoff notes should be eliminated from the handoff process since they are unreliable. | NO | Verbal communication is essential for context; the issue is lack of cross-verification, not verbal handoff itself | Overcorrection |
| H | The B1 bias was reasonable at the time it was expressed because the agent had not yet seen the MAR data. The bias becomes incorrect only after the MAR is available. | YES | Temporal bias analysis | Fair bias assessment |

**answer:** `["A", "B", "C", "F", "H"]`

---

### R10: User Preference Identification (P-R)

**Question:**
> "Based on Lin Yi's communication patterns and explicit preferences, which statements about her preferred output format are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Lin Yi prefers structured clinical case format: 主诉 (chief complaint), 现病史 (HPI), 查体 (PE), 辅助检查 (studies), 诊断 (diagnosis), 处理 (management). | YES | P1 from foundation doc + calibration messages | P1 preference |
| B | Lin Yi uses date+patientID file naming convention (e.g., 2026-03-15_P001_急诊记录.md). | YES | P2 from foundation doc | P2 preference |
| C | Lin Yi wants diagnosis/conclusion first, followed by differential diagnosis and supporting evidence chain. | YES | P3 from foundation doc + calibration message | P3 preference |
| D | Lin Yi prefers detailed narrative prose with extensive background context before reaching the clinical conclusion. | NO | P5 says "concise professional, no unnecessary words" | Wrong -- opposite of concise |
| E | Lin Yi values evidence-based medicine, citing clinical guidelines and graded evidence levels when assessing treatment appropriateness. | YES | P4 from foundation doc | P4 preference |
| F | Lin Yi prefers outputs formatted with emojis and informal language to maintain team morale during stressful shifts. | NO | P5 is concise and professional | Wrong tone |
| G | In ER contexts, Lin Yi's preference for conciseness means no unnecessary elaboration -- every statement should be clinically relevant and action-oriented. | YES | P5 from foundation doc | P5 preference |
| H | Lin Yi prefers qualitative patient narratives over quantitative lab data, emphasizing the patient's subjective experience. | NO | Lin Yi's trust bias is toward objective test data; P4 is evidence-based | Wrong -- opposite of her bias |

**answer:** `["A", "B", "C", "E", "G"]`

---

### R11-R30: Abbreviated Specs

### R11: B2 Reversal -- Allergy Omission Systemic Safety Gap (DU-I)

**Question:** "After all evidence, which statements about the B2 bias (allergy minimization) are correct?"
- Key correct: B2 phrase dismissed allergy as "minor documentation gap"; systemic evidence shows it is a recurring patient safety risk; Dr. Zhang identifies it as most concerning finding; near-miss precedent documented by Li Nurse Head; current ACS treatment doesn't use penicillin but concurrent conditions could
- Key distractors: B2 was about medication dosing; allergy omission caused harm to this patient
- **answer:** Options identifying exact B2 bias, systemic correction, and safety implications

### R12: Source Reliability Ranking (MD-R, exec_check)

**exec_check requirement:** Agent must read his-patient-record.md and nursing-handoff-sheet.md before answering.

**Question:** "When assessing reliability of documentation sources in this case, which rankings are correct?"
- Key correct: HIS/MAR > nursing handoff > verbal notes for factual accuracy; lab results are objective; nursing execution was correct even though documentation had errors; verbal notes most affected by fatigue
- Key distractors: Verbal notes are always more reliable than nursing; all sources are equally reliable
- **answer:** Options reflecting the corrected reliability hierarchy

### R13: Heparin Dose Reconciliation (MS-R)

**Question:** "Which statements about the heparin bolus dose are supported by evidence?"
- Key correct: HIS records 4500u (correct -- 60 units/kg x 75kg); MAR confirms 4500u; nursing handoff says 4000u (rounding error); verbal notes say 4500u (correct); APTT of 65s at 00:30 confirms therapeutic heparin (consistent with correct dosing)
- Key distractors: Heparin was actually 4000u; the dose was subtherapeutic
- **answer:** Options confirming 4500u with nursing rounding error

### R14: Nursing Handoff Error Analysis (MD-R, exec_check)

**exec_check requirement:** Agent must read nursing-handoff-sheet.md before answering.

**Question:** "Which statements correctly identify the cause of each nursing handoff sheet error?"
- Key correct: NTG "1mg" = wrote total instead of per-dose (not wrong, just ambiguous); heparin "4000u" = memory rounding error; onset "20:30" = arrival/onset confusion; allergy blank = paper form design flaw (back page); Li Mei was managing 3 critical patients simultaneously
- Key distractors: Li Mei intentionally falsified records; NTG 1mg was a medication error
- **answer:** Options identifying root causes for each error

### R15: Troponin Trend Interpretation with Corrected Onset (MS-I)

**Question:** "With the onset time now corrected to ~18:00-18:30, which statements about the troponin trend interpretation are correct?"
- Key correct: 0.08 -> 0.45 -> 0.89 over ~9 hours from onset consistent with moderate NSTEMI; the corrected onset makes the troponin kinetics more clinically interpretable; CK-MB trend mirrors troponin; clinical decision for catheterization depends on risk score and ongoing symptoms
- **answer:** Options reflecting correct troponin interpretation

### R16: Clinical Summary in Lin Yi's Preferred Format (P-I)

**Question:** "Which elements would be required in a properly formatted clinical summary following Lin Yi's P1-P5 preferences?"
- Key correct: Structured case format with standard headings; diagnosis/conclusion first; evidence-based guideline references; date+patientID naming; concise and professional with no unnecessary words
- **answer:** Options matching all 5 P preferences

### R17: B1 Bias Identification (DP-I, exec_check)

**exec_check requirement:** Agent must read session history for Wang Doctor IM before answering.

**Question:** "What was the B1 bias phrase, where did it appear, and what evidence corrected it?"
- Key correct: B1 about trusting physician verbal notes over nursing; appeared in Wang IM; corrected by MAR showing nursing total was correct and verbal missed a dose; the correction principle is that neither bedside source is systematically superior
- **answer:** Options identifying exact B1 context and correction

### R18: Dr. Wang Documentation Analysis (MD-I)

**Question:** "Which statements about Dr. Wang's documentation patterns are supported by evidence?"
- Key correct: HIS entries were accurate (onset 18:00, NTG x2, heparin 4500u, penicillin allergy); verbal notes had three errors (onset 19:00, NTG x1, no allergy); gap is explained by fatigue at end of 14-hour shift; HIS was documented contemporaneously while verbal notes were from memory at 01:30
- **answer:** Options analyzing the HIS vs verbal discrepancy pattern

### R19: Handoff Process Failure Analysis (MP-I)

**Question:** "Which statements correctly analyze the systemic vs individual factors in the handoff failures?"
- Key correct: Paper form design (allergy on back) is systemic; memory-based documentation during busy shifts is systemic; fatigue at end of long shifts is systemic; no standardized verbal handoff checklist is systemic; individual errors were honest mistakes amplified by system gaps
- **answer:** Options distinguishing systemic from individual factors

### R20: Preference Compliance Check (P-R)

**Question:** "Which statements about applying Lin Yi's output preferences are correct?"
- Key correct: All 5 P preferences should be applied; structured case format is essential; EBM citations expected; conciseness is critical in ER context; date+ID naming for all clinical documents
- **answer:** Options confirming all 5 preferences

### R21: Comprehensive Handoff Discrepancy Assessment (MDP-I, exec_check)

**exec_check requirement:** Agent must read all key workspace files and session histories.

**Question:** "Integrating all available evidence across all updates, which statements represent the most accurate comprehensive assessment of the handoff discrepancies?"
- Key correct: C1 resolved (two NTG 0.5mg doses = 1mg; heparin 4500u confirmed); C2 resolved (onset ~18:00-18:30; nursing confused arrival/onset; verbal was fatigue error); C3 confirmed (lab data consistent across all sources); C4 identified as systemic safety gap (allergy in HIS only; paper form design + fatigue); all errors are reconcilable when electronic records are consulted; the most dangerous finding is the allergy omission pattern
- **answer:** Options reflecting comprehensive synthesis

### R22-R30: Follow similar structure

- **R22 (MS-R):** C3 non-conflict -- all lab values consistent across sources
- **R23 (DU-R):** B2 identification -- allergy minimization phrase and systemic correction
- **R24 (MS-I, exec_check):** Complete medication reconciliation -- all drugs verified across sources
- **R25 (P-I):** Incident analysis report formatted per Lin Yi's preferences
- **R26 (MD-I):** Patient safety risk assessment -- what could have gone wrong?
- **R27 (DP-I, exec_check):** MAR as definitive record -- alignment with HIS and correction of other sources
- **R28 (MP-I):** Stakeholder analysis -- Dr. Wang, nursing, Zhang, systemic factors
- **R29 (MS-I):** Process improvement recommendations -- handoff checklist, form redesign, HIS synchronization
- **R30 (MDP-I):** Final comprehensive -- all contradictions resolved, biases corrected, formal incident analysis with evidence chain and recommendations

**answer formats for R22-R30:** Follow same multi-choice structure with 8-10 options, 3-5 correct, specific evidence sources, distractor logic.
