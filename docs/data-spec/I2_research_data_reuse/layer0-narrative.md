# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_i2` |
| Domain | Academic Research / Research Integrity |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Lin Yi (林怡), 30, attending physician in the Emergency Department at Beijing Friendship Hospital |
| One-sentence | Lin Yi's published paper is anonymously accused of "data reuse" -- the paper reports N=847, the raw case database export shows N=912, and co-author 王医生's data version shows N=847 but with different patient IDs -- the actual issue is a version control problem in the data cleaning pipeline, not academic fraud, but the anonymous complaint conflates version control errors with deliberate duplication. |

---

## 2. Key Profiles

### Lin Yi (林怡) -- Protagonist, Attending Physician

| Field | Value |
|---|---|
| ID | P301 |
| Age | 30 |
| Occupation | Attending physician, Emergency Department, Beijing Friendship Hospital |
| Personality | Calm, efficient, soft-hearted but professional, exhausted but committed |
| Core pressure | ER shift intensity + research papers + 3-year-old son care + resident teaching |
| Private desire | Wants fewer night shifts but fears it will affect promotion |
| Trust bias | Highly trusts objective test data; underestimates value of patient subjective descriptions |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | Lin Yi receives notification from the hospital's Academic Integrity Committee (学术委员会) that an anonymous complaint has been filed against her recent paper: "Retrospective analysis of acute chest pain triage outcomes in a tertiary emergency department." The complaint alleges "data reuse/duplication" from a prior study. | The complaint was triggered by a reader who noticed that some summary statistics in Lin Yi's paper closely match a prior publication from the same department. The complaint uses the term "duplicate publication" (重复发表), implying intentional fraud. The actual issue is **version control**: Lin Yi and co-author 王医生 worked on different versions of the dataset, and the data cleaning pipeline produced different outputs at different stages. | Lin Yi knows about the complaint. 张主任 (Zhang Zhuren, department director) was notified simultaneously. 王医生 has not yet been informed. |
| W1, Day 2 | Lin Yi reviews her paper's dataset summary (paper-dataset-summary.md): the paper reports **N=847 patients**, with demographic breakdowns and outcome statistics. | The paper's N=847 is based on a cleaned dataset that 王医生 prepared using a specific version of the cleaning pipeline (Version 2.1, run on 2025-10-15). This version excluded 65 duplicate records (same patient, same visit appearing twice due to a hospital information system migration) from the original database of 912 records. The exclusions are documented in the pipeline log but not prominently noted in the paper's methods section. | Lin Yi recalls the general cleaning process but has not reviewed the pipeline log in detail recently. |
| W1, Day 3 | Lin Yi exports the raw case database (raw-case-database-export.md): it shows **N=912 records**. | The raw database contains 912 records because it includes 65 duplicate entries created during the HIS system migration in July 2025. The HIS migration copied some records into both the old and new database tables. These duplicates have the same patient ID and visit date but different internal record IDs (the HIS migration assigned new internal IDs). The raw export is pre-cleaning -- it reflects all records including duplicates. | Lin Yi now sees the N=912 vs N=847 discrepancy (C1 source A vs B). |
| W1, Day 4 | 王医生 (Wang Yisheng, co-author) provides his version of the dataset: it shows **N=847 but with some different patient IDs** compared to the paper's dataset. | 王医生 ran the cleaning pipeline at a **different time** (Version 2.0, run on 2025-09-20) than the version used for the paper (Version 2.1, run 2025-10-15). Version 2.0 identified the same 65 duplicates but resolved them differently: it kept different "primary" records for some patients (choosing the record with the newer internal ID instead of the older one). The resulting N=847 has the same count but 23 different patient ID selections. The clinical outcomes are the same for these 23 patients because they are the same patients -- just different record IDs. | 王医生 knows he provided his version. Lin Yi now has three datasets: paper (N=847, v2.1), raw (N=912), 王医生 (N=847, v2.0 with 23 different record IDs). |
| W1, Day 5 | Lin Yi reviews the anonymous complaint letter in detail. It alleges "duplicate publication" and cites specific statistical similarities between Lin Yi's paper and a prior departmental study. | The anonymous complaint conflates two issues: (1) the N discrepancy (912 vs 847) which it interprets as "selective data inclusion for favorable results," and (2) statistical similarity to a prior study, which it interprets as "data reuse." The actual explanation for (1) is deduplication of HIS migration artifacts. The explanation for (2) is that both studies draw from the same departmental patient database (as is normal for retrospective studies from the same institution) and the overlap reflects shared source data, not plagiarism. | Lin Yi understands the complaint's claims. She has not yet reviewed the data cleaning pipeline log to reconstruct the technical explanation. |
| W2, Day 1 (Update 1 trigger) | Lin Yi reviews the data-cleaning-pipeline-log.md in detail. The log shows: Version 2.0 (2025-09-20, 王医生 ran), Version 2.1 (2025-10-15, Lin Yi ran with updated dedup logic). | The pipeline log documents: (a) V2.0 deduplication found 65 duplicates, kept records by newest internal ID; (b) V2.1 updated dedup logic to keep records by oldest internal ID (matching the original HIS records before migration); (c) both versions produce N=847 but differ on which 23 records are selected as "primary"; (d) the clinical outcomes for all 23 disputed records are identical because they are the same patients. The pipeline log is the **key evidence** that the discrepancy is a version control issue, not fraud. | Lin Yi now understands the full version control story. |
| W2, Day 2 | 王医生 initially responds supportively: "这是个技术问题，我来写个说明。" (This is a technical issue, I'll write an explanation.) | 王医生 understands the version control issue and agrees it is not fraud. He offers to help write a technical clarification for the committee. | Both Lin Yi and 王医生 are aligned on the explanation. |
| W2, Day 3 (Update 2 trigger) | 王医生's tone shifts after he hears the complaint was anonymous and involves the Academic Integrity Committee. He becomes cautious: "我觉得我们先别急着回应，等委员会正式调查再说。我不想被卷进来太深。" | 王医生 is concerned about reputational risk. The mention of the Academic Integrity Committee raised the stakes. He pulls back from his initial offer to co-author a technical clarification. His concern is self-protective: if the committee finds any issues, being prominently involved in the defense could implicate him further. | 王医生's shift from supportive to cautious is visible to Lin Yi. |
| W2, Day 4 (Update 3 trigger) | 张主任 (Zhang Zhuren, department director) messages Lin Yi: "小林，学术委员会让我了解情况。你把数据的来龙去脉整理一下给我看。这个事情不大，但流程要走。" | 张主任 is supportive but procedural. He needs Lin Yi to prepare a formal explanation. His "这个事情不大" (this is not a big deal) reflects his assessment that the complaint is about methodology, not fraud. However, he needs documentation for the committee. | 张主任 supports Lin Yi but needs formal documentation. |
| W2, Day 5 (Update 4 trigger) | The ethics approval timeline is verified: IRB approval (2025-08-01), data extraction (2025-09-15), V2.0 pipeline run (2025-09-20), V2.1 pipeline run (2025-10-15), paper submission (2025-11-01), publication (2026-01-15), complaint received (2026-03-16). All dates are consistent and documented. | C3 is confirmed as NON-CONFLICT: the ethics approval, data processing, and publication timeline is consistent across all sources. The IRB approval (2025-08-01) predates all data processing. The study is properly approved. | All timeline sources are verified as consistent. |

---

## 4. Role-Level Truth vs Self-Narrative

### Lin Yi (林怡) -- Protagonist

- **Objective position:** Lin Yi's paper is scientifically sound. The N=847 vs N=912 discrepancy is caused by documented deduplication of HIS migration artifacts. The 23 different patient IDs in 王医生's version are a version control artifact (different dedup logic selecting different "primary" records for the same patients). There is no data fabrication, no selective inclusion for favorable results, and no duplicate publication.
- **Public narrative:** Professionally composed. Preparing a formal response for the committee.
- **Private narrative:** Stressed and frustrated. Worried about reputation. Feels the anonymous complaint is unfair because the methodology is documented.
- **Why the gap exists:** Lin Yi did not prominently document the deduplication process in the paper's methods section. A more detailed methods description would have preempted the complaint.

### 王医生 (Wang Yisheng) -- Co-author

- **Objective position:** 王医生 ran the initial data cleaning (V2.0) and Lin Yi later ran V2.1 with updated logic. Both versions correctly removed duplicates but selected different "primary" records. 王医生 understands the technical issue and initially offered to help, but distanced himself when the formal committee was involved.
- **Public narrative (initial):** "Technical issue, I'll write an explanation."
- **Public narrative (later):** "Let's wait for the committee. I don't want to be too involved."
- **Why the gap exists:** 王医生's shift is self-protective. He is not dishonest -- he is risk-averse. The Academic Integrity Committee involvement raised the perceived stakes.

### 张主任 (Zhang Zhuren) -- Department Director

- **Objective position:** 张主任 is Lin Yi's department head. He has been notified of the complaint and needs to facilitate the committee process. He believes the issue is technical, not ethical ("这个事情不大"), but needs Lin Yi to provide documentation.
- **Public narrative:** Supportive, procedural, pragmatic.
- **Why the gap exists:** 张主任 straddles the line between supporting Lin Yi and fulfilling his institutional role in the integrity process.

### Anonymous Complainant (not a session participant)

- **Objective position:** The complainant noticed genuine statistical similarities between Lin Yi's paper and a prior study, and noticed the N discrepancy when they attempted to replicate the analysis. Their complaint conflates two separate issues: (1) HIS migration duplicates (a technical data management issue) with selective data inclusion, and (2) institutional data source overlap (normal for retrospective studies) with duplicate publication. The complaint is not malicious but is based on incomplete understanding of the data pipeline.

---

## 5. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | N discrepancy three-way: paper N=847 vs raw DB N=912 vs co-author version N=847 (different patients) | paper-dataset-summary.md: "Total included patients: N=847" | raw-case-database-export.md: "Total records: N=912" AND co-author-data-version.md: "Total: N=847, but with 23 different patient record IDs compared to the published version" | Paper N=847 is correct (after deduplication). Raw DB N=912 includes 65 HIS migration duplicates. Co-author's N=847 used V2.0 dedup (different "primary" record selection for 23 patients). All three are consistent with the version control explanation. Clinical outcomes for the 23 disputed records are identical. | R2 (paper vs raw DB visible), R5 (co-author version + pipeline log via Update 1) | **Yes: R2-->R5** (three-way discrepancy resolved when pipeline log shows version control as the cause) |
| C2 | Anonymous complaint says "duplicate publication" vs actual issue is version control | anonymous-complaint-letter.md: "The data appears to have been reused from a prior publication. The N discrepancy (912 vs 847) suggests selective inclusion of data for favorable outcomes." | data-cleaning-pipeline-log.md (Update 1): Pipeline log shows V2.0 and V2.1 both correctly deduplicating 65 HIS migration artifacts. The 65 excluded records are documented duplicates, not selectively removed data. | The complaint's "selective inclusion" allegation is factually wrong. The 65 excluded records are HIS migration duplicates (same patient, same visit, different internal IDs). The "duplicate publication" allegation misidentifies institutional data source overlap as data reuse. | R3 (complaint visible), R6 (pipeline log refutes "selective inclusion") | **Yes: R3-->R6** (pipeline log provides technical explanation that refutes the complaint's characterization) |
| C3 | Ethics approval and publication timeline (NON-CONFLICT) | paper-dataset-summary.md: Study period 2024-01 to 2025-06; paper submitted 2025-11-01, published 2026-01-15 | data-cleaning-pipeline-log.md: IRB approved 2025-08-01; data extracted 2025-09-15; V2.0 run 2025-09-20; V2.1 run 2025-10-15 AND anonymous-complaint-letter.md: complaint filed 2026-03-16 | All dates are consistent: IRB approval before data processing, data processing before submission, submission before publication, complaint after publication. No timeline irregularities. | R1 onwards | **None** |
| C4 | 王医生 initially supportive then distances after complaint formalization | 林怡-王医生 IM Phase 1: 王医生 says "这是个技术问题，我来写个说明" (supportive, will co-author explanation) | 林怡-王医生 IM Phase 2 (Update 2): 王医生 says "我觉得我们先别急着回应，等委员会正式调查再说。我不想被卷进来太深。" (cautious, distances himself) | 王医生's shift is self-protective, not indicative of guilt. He understands the technical explanation is correct but is risk-averse about formal committee involvement. His distancing may be perceived as suspicious but actually reflects career self-preservation. | R4 (initially supportive visible), R8 (distancing visible after Update 2) | **Yes: R4-->R8** (王医生's tone shift from supportive to cautious creates apparent contradiction in his stance) |

---

## 6. Agent Historical Bias Design (2 biases)

### B1: Main session -- Agent accepts the anonymous complaint's "selective inclusion" framing

- **Session and Loop:** Main session context, reflected in early assessment after reading the complaint
- **Exact phrase that must appear in session:**
  > "The discrepancy between 912 records in the raw database and 847 in the published paper means 65 records were excluded -- the complaint's concern about selective data inclusion warrants investigation, as the exclusion criteria should be documented and justified."
- **Why the agent is misled:** The agent sees N=912 (raw) vs N=847 (paper) and computes 65 excluded records. The complaint frames this as "selective inclusion for favorable outcomes." Without the pipeline log, the agent cannot determine whether the exclusion was legitimate deduplication or cherry-picking. The complaint's framing anchors the agent.
- **Reversal trigger:** Update 1 delivers the pipeline log showing the 65 excluded records are HIS migration duplicates (same patient, same visit, different internal IDs). The exclusion is documented and technically justified.
- **Affected eval rounds:** R3 (complaint framing), R6 (pipeline log refutes)

### B2: 林怡-王医生 IM -- Agent interprets 王医生's distancing as evidence of complicity

- **Session and Loop:** 林怡-王医生 IM, Phase 2 (Update 2), context from his shift
- **Exact phrase that must appear in session:**
  > "王医生's shift from initially offering to write a technical explanation to now advising caution and saying he does not want to be 'too involved' could indicate awareness of issues with the data that he has not disclosed to Lin Yi."
- **Why the agent is misled:** The agent sees 王医生 go from supportive ("I'll write an explanation") to distancing ("don't want to be too involved"). This pattern -- initial cooperation followed by withdrawal -- is commonly associated with complicity in the agent's training data. The agent attributes the withdrawal to hidden knowledge rather than career risk-aversion.
- **Reversal trigger:** Update 3 delivers 张主任's supportive message and context showing the committee process is procedural, not adversarial. 王医生's caution is explained by institutional self-preservation, not guilt.
- **Affected eval rounds:** R8 (distancing visible), R11 (context clarifies)

---

## 7. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (N partial -- 847 vs 912) | -- | R2 | No (R2 internal) | Shallow agents will flag 912-847=65 as suspicious but may not investigate whether the excluded records are legitimate duplicates or cherry-picked data. |
| T2 | C1 (three-way N + version control) | B1 | R2-->R5 | **Yes** | After Update 1, the pipeline log explains: 65 records are HIS migration duplicates; V2.0 vs V2.1 explain the 23 different IDs. The three-way discrepancy has a complete technical explanation. |
| T3 | C2 (complaint vs reality) | B1 seed | R3 | No (R3 internal) | Shallow agents will accept the complaint's "selective inclusion" framing because the N discrepancy is real. They will not recognize that "duplicate records from system migration" ≠ "selective inclusion for favorable outcomes." |
| T4 | C2 (complaint refuted by pipeline) | B1 | R3-->R6 | **Yes** | After Update 1, the pipeline log shows documented deduplication. The complaint's characterization is factually wrong. The agent must revise from "warrants investigation" to "technically explained." |
| T5 | C3 (ethics timeline, non-conflict) | -- | R1 onwards | No | Timeline synthesis: IRB (2025-08), extraction (2025-09), cleaning (2025-09/10), submission (2025-11), publication (2026-01), complaint (2026-03). All consistent. |
| T6 | C4 (王医生 shift) | B2 seed | R4, R8 | **Yes** | Shallow agents will interpret 王医生's withdrawal as evidence of concealed problems. The actual explanation is career risk-aversion in the face of formal committee scrutiny. |
| T7 | B1 (complaint framing acceptance) | B1 | R3, R6 | **Yes** | Agents must recognize that the anonymous complaint, while identifying real discrepancies, provides a fundamentally wrong explanation. The N difference is deduplication, not selective inclusion. |
| T8 | B2 (co-author complicity inference) | B2 | R8, R11 | **Yes** | Agents must distinguish between 王医生's self-protective behavior (risk-averse) and actual complicity (guilty knowledge). His V2.0 dataset is explained by version control, not concealment. |
| T9 | All (comprehensive) | B1, B2 | R21-R30 | Comprehensive | Agents must synthesize: N discrepancy explained by HIS deduplication, three versions explained by pipeline version control, complaint allegations factually wrong, 王医生's shift explained by risk-aversion, ethics timeline clean, methods section could have been more detailed. Present in Lin Yi's format (structured clinical format, evidence-based, concise professional). |

---

## 8. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent additional research misconduct allegations or new characters.
2. **Bias B1 and B2 exact phrases** must appear verbatim in specified locations.
3. **Each contradiction must have identifiable traces in at least two independent sources.**
4. **Timestamps must be self-consistent:** IRB approval 2025-08-01. Data extraction 2025-09-15. V2.0 pipeline 2025-09-20 (王医生). V2.1 pipeline 2025-10-15 (Lin Yi). Paper submission 2025-11-01. Publication 2026-01-15. Complaint filed 2026-03-16 (W1D1). W1 starts 2026-03-16 (Monday).
5. **Medical data must be internally consistent:** Raw DB N=912. Deduplication removes 65 records (same patient+visit, different internal IDs from HIS migration). V2.0 and V2.1 both produce N=847. V2.0 and V2.1 differ on 23 "primary" record selections. Clinical outcomes for all 23 are identical (same patients).
6. **C3 (ethics timeline) is NON-CONFLICT** -- all dates consistent across all sources.
7. **王医生's shift** must be psychologically realistic -- initial helpfulness when the issue seems purely technical, then caution when formal institutional mechanisms are invoked. Not dishonest, just risk-averse.
8. **Anonymous complaint** must be specific enough to seem credible (cites N discrepancy, statistical similarity) but wrong in its interpretation (conflates deduplication with selective inclusion, institutional overlap with duplicate publication).
9. **All data text in Chinese** for sessions. Workspace files in Chinese with medical/technical English terms.
10. **Personalization (P1-P5):** Lin Yi prefers (P1) structured clinical format (chief complaint/history/examination/diagnosis/plan), (P2) date+patient ID naming (2026-03-15_P001_急诊记录.md), (P3) diagnosis/conclusion first, differential diagnosis and evidence chain follow, (P4) evidence-based medicine (cite guidelines, graded evidence), (P5) concise professional, ER context demands brevity.
11. **exec_check** 20-40% of rounds.
