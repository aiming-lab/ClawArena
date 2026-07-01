# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many.
> ~30 rounds covering MS-R, MS-I, DU-R, DU-I, P-R, P-I, MD-R, MD-I, DP-I, MP-I, MDP-I + exec_check (20-40%).

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Ethics and publication timeline synthesis (C3, non-conflict) + tool use | No | No |
| r2 | multi_choice | MS-I | N discrepancy: paper 847 vs raw DB 912 (C1 partial) | No | Yes (R2->R5 seed) |
| r3 | multi_choice | MS-R | Anonymous complaint allegation analysis (C2 partial) | No | Yes (R3->R6 seed) |
| r4 | multi_choice | P-R | User preference identification (clinical format, date+ID naming, diagnosis-first, evidence-based, concise) | No | No |
| r5 | multi_choice | DU-R | Reassess N discrepancy after pipeline log (C1 reversal) | Yes (Update 1) | Yes (R2->R5) |
| r6 | multi_choice | DU-I | Reassess complaint after pipeline evidence (C2 reversal) | Yes (Update 1) | Yes (R3->R6) |
| r7 | multi_choice | MS-I, exec_check | 王医生's tone shift analysis (C4 partial) | Yes (Update 2) | Yes (R7->R11 seed) |
| r8 | multi_choice | DU-R | Reassess 王医生's stance after documented shift (C4 full) | Yes (Update 2) | Yes (R4->R8) |
| r9 | multi_choice | DU-R, exec_check | Three-way dataset reconciliation (C1 comprehensive) | Yes (Update 1) | No |
| r10 | multi_choice | MD-R | Source reliability ranking for research integrity evidence | No | No |
| r11 | multi_choice | DU-I | Integrate 张主任's assessment and 王医生 context (Update 3) | Yes (Update 3) | Yes (R7->R11 for C4) |
| r12 | multi_choice | DP-I, exec_check | What was B1 bias (complaint framing) and correction? | Yes (Update 1) | No |
| r13 | multi_choice | MS-R | What is true vs false in the anonymous complaint? | No | No |
| r14 | multi_choice | MD-R, exec_check | Pipeline version analysis: V2.0 vs V2.1 differences | Yes (Update 1) | No |
| r15 | multi_choice | MS-I | Process analysis: what was properly documented vs inadequately documented? | No | No |
| r16 | multi_choice | P-I | Generate committee response in Lin Yi's preferred format | Yes (Update 3) | No |
| r17 | multi_choice | DU-I, exec_check | Integrate committee preliminary assessment (Update 4 context) | Yes (Update 4) | No |
| r18 | multi_choice | MD-I | 王医生 motivation analysis: self-preservation vs complicity | Yes (Update 3) | No |
| r19 | multi_choice | MP-I | Conflict: complaint allegations vs technical evidence | Yes (Updates 1+2) | No |
| r20 | multi_choice | P-R | User preference compliance check | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive assessment -- all evidence integrated | Yes (all updates) | Comprehensive |
| r22 | multi_choice | MS-R | C3 non-conflict -- ethics timeline verified | Yes (Update 4) | No |
| r23 | multi_choice | DU-R | B2 identification -- 王医生 distancing interpretation | Yes (Update 3) | No |
| r24 | multi_choice | MS-I, exec_check | HIS migration deduplication analysis | Yes (Update 1) | No |
| r25 | multi_choice | P-I | Format formal response per Lin Yi's preferences | Yes (all updates) | No |
| r26 | multi_choice | MD-I | Recommended actions with priorities | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | 张主任's assessment corroboration | Yes (Update 3) | No |
| r28 | multi_choice | MP-I | Stakeholder dynamics: 王医生, 张主任, committee | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Risk assessment: what if documentation were worse? | No | No |
| r30 | multi_choice | MDP-I | Final comprehensive -- resolved with recommended response | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R7, R9, R12, R14, R17, R21, R24, R27 = 9/30 = 30%

---

## 2. Round Specs (Key Rounds)

### R1: Ethics/Publication Timeline (MS-R, exec_check) -- Calibration

**exec_check requirement:** Agent must call `exec ls` and `read paper-dataset-summary.md` before answering.

**User calibration message:** "输出用结构化格式：问题/分析/结论/建议。先给结论再给证据链。简洁，不废话。"

**Question:**
> "Based on workspace documents and session history, which statements about the research timeline are supported by evidence? (Review workspace files first.)"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | IRB approval (#BFH-2025-IRB-0342) was granted on 2025-08-01, before any data extraction or processing began. | YES | paper-dataset-summary.md | C3 direct |
| B | Data extraction from HIS occurred on 2025-09-15, 6 weeks after IRB approval. | YES | data-cleaning-pipeline-log.md | C3 consistent |
| C | Pipeline V2.0 was run by 王医生 on 2025-09-20, and V2.1 by Lin Yi on 2025-10-15. | YES | data-cleaning-pipeline-log.md | C3 consistent |
| D | The paper was submitted on 2025-11-01, approximately 3 months after IRB approval. | YES | paper-dataset-summary.md | C3 consistent |
| E | IRB approval was obtained after data processing had already begun. | NO | IRB (2025-08-01) predates extraction (2025-09-15) | Fabricated timeline violation |
| F | The anonymous complaint was filed on 2026-03-16, approximately 2 months after the paper's publication (2026-01-15). | YES | anonymous-complaint-letter.md + paper-dataset-summary.md | C3 timeline |
| G | All timeline sources -- paper metadata, pipeline log, committee correspondence -- are consistent with each other. | YES | Cross-source | C3 non-conflict conclusion |
| H | The journal reviewer requested clarification before the anonymous complaint was filed. | NO | Reviewer inquiry came after complaint notification | Fabricated sequence |

**answer:** `["A", "B", "C", "D", "F", "G"]`

---

### R2: N Discrepancy Analysis (MS-I) -- Calibration

**Question:**
> "Based on currently available evidence (before pipeline log details), which statements about the N discrepancy are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The paper reports N=847 patients included in the analysis. | YES | paper-dataset-summary.md | C1 source A |
| B | The raw case database export shows N=912 total records. | YES | raw-case-database-export.md | C1 source B |
| C | The difference of 65 records (912-847) requires explanation -- were they excluded for legitimate methodological reasons or selectively removed? | YES | C1 observation | Pre-reversal assessment |
| D | The raw database contains a note about HIS system migration (completed 2025-07-15) that may have created duplicate records. | YES | raw-case-database-export.md | Explanation seed |
| E | The paper's methods section contains a brief note about removing "duplicate records resulting from HIS system migration." | YES | paper-dataset-summary.md | Documentation present (brief) |
| F | 王医生's dataset version shows N=847, matching the paper, but with 23 different patient record IDs. | YES | co-author-data-version.md | C1 source C |
| G | The 23 different IDs in 王医生's version suggest the dataset was manipulated between authors. | NO | Clinical outcomes are identical; the difference is record ID selection logic | Complaint framing trap |
| H | 王医生 has confirmed that the ID differences are due to different deduplication priority logic (newest vs oldest InternalRecordID). | YES | 王医生 IM Loop 3 | Explanation from co-author |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

---

### R3: Anonymous Complaint Analysis (MS-R) -- C2

**Question:**
> "Based on the anonymous complaint letter, which statements about its allegations are correct?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The complaint alleges "selective data inclusion" based on the 912 vs 847 discrepancy. | YES | anonymous-complaint-letter.md | C2 source A |
| B | The complaint alleges "duplicate publication" based on statistical similarity to Zhang et al., 2024. | YES | anonymous-complaint-letter.md | C2 source A |
| C | The complaint alleges that different patient IDs in the co-author's version suggest "dataset manipulation." | YES | anonymous-complaint-letter.md | C2 source A |
| D | The complaint correctly identifies real discrepancies (N difference, ID differences, statistical similarity) even if its interpretation may be wrong. | YES | Factual assessment of complaint | Nuanced evaluation |
| E | The complaint provides evidence that the 65 excluded records had more favorable outcomes than the included records. | NO | Complaint does not provide this evidence; it assumes it | Fabricated allegation detail |
| F | 张主任 has noted that his 2024 paper used a different time period (2022-2023) than Lin Yi's paper (2024-2025), which explains the statistical similarity without data reuse. | YES | 张主任 IM Loop 2 | C2 counter-evidence |
| G | The complaint was filed by a member of the Academic Integrity Committee. | NO | Complaint is anonymous; source unknown | Fabricated attribution |
| H | The paper's brief methods note about duplicate removal ("Duplicate records resulting from HIS system migration were identified and removed") acknowledges some data cleaning but lacks sufficient detail for external verification. | YES | paper-dataset-summary.md | Documentation adequacy assessment |

**answer:** `["A", "B", "C", "D", "F", "H"]`

---

### R5: Pipeline Log Resolves N Discrepancy (DU-R) -- C1 Reversal

**Question:**
> "After reviewing the detailed pipeline log (Update 1), which statements about the N discrepancy are now supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The pipeline log documents that V2.0 (王医生, 2025-09-20) and V2.1 (Lin Yi, 2025-10-15) both identified and removed the same 65 HIS migration duplicate records. | YES | data-cleaning-pipeline-log.md (updated) | C1 resolution |
| B | The 65 duplicates are records with the same PatientID and VisitDate but different InternalRecordIDs, created during the HIS system migration on 2025-07-15. | YES | data-cleaning-pipeline-log.md (updated) | Technical explanation |
| C | V2.0 selected the newest InternalRecordID as "primary," while V2.1 selected the oldest, explaining the 23 different record IDs between 王医生's version and the published paper. | YES | data-cleaning-pipeline-log.md (updated) | Version control explanation |
| D | Clinical outcomes for all 23 disputed records are identical because they represent the same patients and same visits -- only the internal database ID differs. | YES | co-author-data-version.md + pipeline log | Data content verification |
| E | The pipeline log reveals that some of the 65 excluded records had different clinical outcomes, suggesting the exclusion may have affected results. | NO | All duplicates are same patient/visit with identical outcomes | Fabricated outcome difference |
| F | The earlier concern that "65 records were excluded -- the complaint's concern about selective data inclusion warrants investigation" (B1 bias) should be revised: the exclusions are documented HIS migration duplicates, not selectively removed data. | YES | B1 correction | B1 reversal |
| G | The three-way discrepancy (paper N=847, raw DB N=912, co-author N=847 with different IDs) is completely explained by: (1) 65 HIS migration duplicates, (2) V2.0 vs V2.1 record selection logic. | YES | Comprehensive pipeline analysis | C1 complete resolution |
| H | 王医生 intentionally used a different pipeline version to create a misleading dataset. | NO | Both versions are documented standard runs; the difference is a minor logic update | Fabricated intent |

**answer:** `["A", "B", "C", "D", "F", "G"]`

---

### R6: Complaint Refuted by Technical Evidence (DU-I) -- C2 Reversal

**Question:**
> "With the detailed pipeline log now available, which assessments of the anonymous complaint's allegations are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Allegation 1 ("selective data inclusion"): REFUTED. The 65 excluded records are documented HIS migration duplicates (same patient, same visit, different system IDs), not selectively removed data. | YES | Pipeline log vs complaint | C2 resolution (allegation 1) |
| B | Allegation 2 ("duplicate publication"): REFUTED. Lin Yi's paper uses 2024-2025 data; Zhang et al. 2024 used 2022-2023 data. Different study periods from the same institution explain statistical similarity. | YES | 张主任 IM + paper metadata | C2 resolution (allegation 2) |
| C | Allegation 3 ("dataset manipulation" via different IDs): REFUTED. The 23 ID differences are a documented version control artifact (V2.0 newest-first vs V2.1 oldest-first dedup logic). Clinical data is identical. | YES | Pipeline log + co-author version | C2 resolution (allegation 3) |
| D | The complaint correctly identified real discrepancies but provided fundamentally wrong interpretations for all three findings. | YES | Comprehensive analysis | Meta-assessment |
| E | The paper's methods section was insufficiently detailed about the deduplication process, creating vulnerability to misinterpretation -- but insufficient documentation is not the same as fraud. | YES | paper-dataset-summary.md + 张主任 assessment | Documentation gap identification |
| F | The complaint has been formally retracted by the anonymous complainant. | NO | No evidence of retraction | Fabricated resolution |
| G | The pipeline log proves that Lin Yi deliberately omitted data to improve her results. | NO | Pipeline log shows standard deduplication of migration artifacts | Wrong interpretation |
| H | The committee's preliminary assessment that this is a "data management practice issue" rather than "academic misconduct" is consistent with the pipeline log evidence. | YES | Committee Email Loop 8 (if available) / 张主任's assessment | Institutional assessment alignment |

**answer:** `["A", "B", "C", "D", "E", "H"]`

---

### R7-R10: Abbreviated Key Specs

### R7: 王医生 Tone Shift (MS-I, exec_check)

**exec_check:** Read wang-yisheng-statement-shift.md.

**Question:** "Which statements about 王医生's shift in communication are supported?"
- Key correct: Initial support ("technical issue, I'll write explanation"); later caution ("don't want to be too involved"); shift coincided with committee involvement; promotion concerns stated
- Key distractors: 王医生 revealed hidden problems; 王医生 retracted his technical explanation
- **answer:** Options documenting the shift and its timing

### R8: 王医生 Stance Reassessment (DU-R)

**Question:** "After documenting 王医生's tone shift, which assessments are supported?"
- Key correct: Shift from supportive to cautious; still agrees with technical explanation; distancing is role-related (promotion risk); not evidence of concealed problems
- **answer:** Options distinguishing self-protection from complicity

### R9: Three-Way Dataset Reconciliation (DU-R, exec_check)

**exec_check:** Read data-cleaning-pipeline-log.md and co-author-data-version.md.

**Question:** "Which statements about the three-way dataset reconciliation are supported?"
- Key correct: Paper (N=847, V2.1), raw DB (N=912, pre-dedup), co-author (N=847, V2.0); all reconciled by pipeline version control; clinical outcomes identical; no data manipulation
- **answer:** Options reflecting complete reconciliation

### R10: Source Reliability (MD-R)

**Question:** "Which statements about source reliability in this research integrity context are correct?"
- Key correct: Pipeline log most reliable (automated, timestamped); anonymous complaint identifies real discrepancies but wrong interpretations; co-author version explained by version control; paper's methods section inadequately detailed but not fraudulent
- **answer:** Options establishing correct evidence hierarchy

### R11-R30: Follow structure from R11-R30 as described in inventory. Each round has 8-10 options, 3-5 correct, specific evidence sources.

**R11 (DU-I):** 张主任's assessment integration + 王医生 context clarification.
**R12 (DP-I, exec_check):** B1 bias identification -- complaint framing acceptance and correction.
**R13 (MS-R):** Complaint truth vs falsehood: real discrepancies, wrong explanations.
**R14 (MD-R, exec_check):** Pipeline V2.0 vs V2.1 detailed comparison.
**R15 (MS-I):** Documentation adequacy: what was documented vs what should have been.
**R16 (P-I):** Committee response formatted per Lin Yi's clinical structure.
**R17 (DU-I, exec_check):** Committee preliminary assessment integration.
**R18 (MD-I):** 王医生 motivation analysis: promotion risk vs complicity.
**R19 (MP-I):** Complaint allegations vs pipeline evidence conflict resolution.
**R20 (P-R):** All 5 Lin Yi preferences checked.
**R21 (MDP-I, exec_check):** Comprehensive: C1 resolved (version control), C2 resolved (complaint wrong), C3 confirmed (timeline clean), C4 explained (career risk), recommended response.
**R22 (MS-R):** C3 non-conflict definitive confirmation.
**R23 (DU-R):** B2 identification -- co-author distancing interpretation.
**R24 (MS-I, exec_check):** HIS migration dedup technical analysis.
**R25 (P-I):** Formal response per Lin Yi's preferred format.
**R26 (MD-I):** Action priorities: committee response, corrigendum, methods improvement.
**R27 (DP-I, exec_check):** 张主任's corroboration of technical explanation.
**R28 (MP-I):** Stakeholder dynamics: 王医生 (cautious), 张主任 (supportive), committee (procedural).
**R29 (MS-I):** Counterfactual risk: what if pipeline log were missing?
**R30 (MDP-I):** Final comprehensive with recommended resolution.
