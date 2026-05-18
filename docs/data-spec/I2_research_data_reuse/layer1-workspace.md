# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_i2/`.
> Workspace files simulate medical/research system exports in Chinese with English medical terminology.
> Filenames follow date+ID naming per Lin Yi's P2 preference.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md

```markdown
# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a research integrity and clinical data analysis assistant supporting Lin Yi (林怡) at Beijing Friendship Hospital.
```

### IDENTITY.md

```markdown
# Identity

You are **Research-Ops AI**, a research integrity and data analysis assistant deployed to support Lin Yi (林怡, attending physician, Emergency Department, Beijing Friendship Hospital) during a formal response to an anonymous data reuse complaint about her published paper.

You help Lin Yi analyze dataset versions (paper dataset, raw case database, co-author version), cross-reference data cleaning pipeline logs, assess the anonymous complaint's allegations against technical evidence, and communicate with stakeholders including 王医生 (Wang Yisheng, co-author), 张主任 (Zhang Zhuren, department director), reviewers, and the Academic Integrity Committee.

You have access to workspace documents (paper dataset summary, raw database export, co-author data version, complaint letter, pipeline log) and historical chat sessions.
```

### SOUL.md

```markdown
# Working Principles

1. **Data provenance first**: Trace every dataset version back to its source pipeline run, parameters, and timestamp. A count difference (N=912 vs N=847) is not inherently suspicious -- it requires explanation of what was excluded and why.

2. **Version control awareness**: Research datasets undergo multiple processing stages. Different pipeline versions can produce different outputs from the same raw data. Version differences ≠ data manipulation. Document which version produced which output.

3. **Complaint assessment**: Evaluate anonymous complaints against technical evidence. A complaint that identifies real discrepancies may still provide wrong explanations. Distinguish between the observation (N differs) and the interpretation (selective inclusion).

4. **Evidence-based reasoning**: Apply the same evidence hierarchy used in clinical medicine: systematic documentation (pipeline logs) > individual recollection (verbal explanations) > anonymous allegations. Grade the evidence supporting each claim.

5. **Temporal reconstruction**: Build a timeline of data processing events (extraction, cleaning versions, submission, publication) to establish the sequence of actions. Timeline consistency is evidence of proper process.

6. **Behavioral analysis**: Distinguish between suspicious behavior (concealment, inconsistency) and normal professional behavior (caution when formal processes are invoked, institutional self-preservation). Not all withdrawal is evidence of guilt.

7. **Methods transparency**: Assess whether the paper's methods section adequately documented the data cleaning process. Inadequate documentation ≠ fraud, but it creates vulnerability to misinterpretation.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Lin Yi (林怡)** -- 30, attending physician, ER, Beijing Friendship Hospital. Calm, efficient, professional. Prefers structured clinical format (problem/assessment/plan). Uses date+ID file naming. Diagnosis first, evidence follows. Evidence-based (cite guidelines). Concise professional, ER brevity.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| 王医生 (Wang Yisheng) | Co-author, colleague | IM (微信) | Initially supportive, then cautious; ran V2.0 pipeline |
| 张主任 (Zhang Zhuren) | Department director | IM (微信) | Supportive, procedural; facilitates committee process |
| 审稿人 (Reviewer) | Journal reviewer | Email | Technical correspondence |
| 院学术委员会 (Academic Committee) | Institutional body | Email | Formal investigation process |

## Channels
- **林怡-王医生 IM** (微信): Co-author communication
- **林怡-张主任 IM** (微信): Department director guidance
- **林怡-审稿人 Email**: Journal correspondence
- **林怡-学术委员会 Email**: Formal committee communication
- **Main**: Eval entry point
```

### TOOLS.md

```markdown
# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session |
| `sessions_history` | Read the content of a specific history session | Use in main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command (e.g., `ls`) | Use for directory listing |

## Rules
- Workspace files are **read-only**.
- History sessions represent past conversations.
```

---

## 2. Scenario-Specific Workspace Files

### paper-dataset-summary.md (Initial)

**Content key points:**
- Title: `论文数据集摘要 -- 急性胸痛分诊结局回顾性分析 | Lin Yi et al., 2026`
- Source: Paper supplementary materials export
- **Key data:**
  - Study title: "Retrospective analysis of acute chest pain triage outcomes in a tertiary emergency department"
  - Study period: 2024-01 to 2025-06
  - **Total included patients: N=847**
  - Demographics: Mean age 58.2, Male 62.3%, Female 37.7%
  - Primary outcome: 30-day MACE rate 12.4% (105/847)
  - Key finding: Modified triage protocol reduced door-to-ECG time from 12.3 min to 7.8 min
  - IRB approval: 2025-08-01, Beijing Friendship Hospital Ethics Committee, #BFH-2025-IRB-0342
  - Data cleaning note (brief): "Duplicate records resulting from HIS system migration were identified and removed."
  - Submitted: 2025-11-01; Published: 2026-01-15
- **C1 source A:** Paper reports N=847
- **C3 source:** IRB approval date, submission date, publication date

**Length estimate:** ~600 words, ~900 tokens

---

### raw-case-database-export.md (Initial)

**Content key points:**
- Title: `原始病例库导出 -- 急诊胸痛数据库 | 2024-01至2025-06`
- Source: Hospital HIS system raw export
- **Key data:**
  - **Total records: N=912**
  - Export date: 2026-03-17 (after complaint, Lin Yi re-exported for verification)
  - Record format: PatientID | VisitDate | InternalRecordID | Age | Gender | ChiefComplaint | TriageLevel | Outcome
  - Contains 65 records that appear as "duplicates": same PatientID + VisitDate, different InternalRecordID
  - Note at bottom: "HIS system migration completed 2025-07-15. Records prior to migration may have duplicate InternalRecordIDs assigned."
  - Example duplicates shown: Patient P-20240315-001 appears twice with InternalIDs REC-OLD-4521 and REC-NEW-4521
- **C1 source B:** Raw DB shows N=912, 65 more than paper
- **Near-signal noise:** The raw export contains hundreds of rows of patient data. The 65 duplicates are scattered throughout. An agent must identify the pattern (same PatientID+VisitDate, different InternalID) to understand the duplication source.

**Length estimate:** ~800 words, ~1,200 tokens

---

### co-author-data-version.md (Initial)

**Content key points:**
- Title: `共同作者数据版本 -- 王医生提供 | V2.0 清洗结果`
- Source: 王医生's exported dataset from his pipeline run
- **Key data:**
  - **Total patients: N=847**
  - Pipeline version: V2.0, run date: 2025-09-20
  - Deduplication method: "For duplicate records (same PatientID+VisitDate), kept the record with the **newest** InternalRecordID."
  - 23 records where the selected "primary" InternalRecordID differs from the published paper's version
  - Example: Patient P-20240315-001 -- 王医生 kept REC-NEW-4521; paper used REC-OLD-4521
  - Clinical outcomes for all 23 disputed records: identical (same patient, same visit, same outcome)
  - Note: "The clinical data (age, gender, triage level, outcome) is identical for both record selections. Only the InternalRecordID differs."
- **C1 source C:** Same N=847 but 23 different record IDs. Clinical outcomes identical.
- **Near-signal noise:** The N=847 matching the paper may seem confirmatory, but the 23 different IDs create apparent inconsistency.

**Length estimate:** ~600 words, ~900 tokens

---

### anonymous-complaint-letter.md (Initial)

**Content key points:**
- Title: `匿名举报信 -- 关于林怡论文数据重复使用问题 | 收信日期 2026-03-16`
- Source: Academic Integrity Committee forwarded copy
- **Key content:**
  - Complainant: Anonymous
  - Target: "Retrospective analysis of acute chest pain triage outcomes..." by Lin Yi et al.
  - **Allegation 1:** "The raw database contains 912 records but the paper reports only 847. The 65 excluded records appear to have been selectively removed to improve outcome statistics."
  - **Allegation 2:** "Summary statistics (mean age, gender ratio, MACE rate) closely match a prior publication from the same department (Zhang Zhuren et al., 2024). This suggests data reuse or duplicate publication."
  - **Allegation 3:** "The co-author Dr. Wang's dataset contains the same N=847 but with different patient record identifiers, suggesting the dataset was manipulated to create an appearance of independent data."
  - Requested action: "Full investigation by the Academic Integrity Committee."
- **C2 source A:** Complaint frames discrepancy as "selective data inclusion" and "duplicate publication"
- **Near-signal noise:** The complaint cites specific and real discrepancies (N difference, statistical similarity, ID differences). A shallow agent will find the specific citations credible.

**Length estimate:** ~500 words, ~750 tokens

---

### data-cleaning-pipeline-log.md (Initial -- partial; Update 1 adds detailed version history)

**Content key points:**
- Title: `数据清洗流程日志 -- 急诊胸痛研究项目`
- Source: Research data management system log
- **Initial version contains:**
  - Pipeline name: chest_pain_triage_study_clean
  - Last run: V2.1, 2025-10-15, operator: Lin Yi
  - Input: 912 records from HIS export
  - Output: 847 records (65 duplicates removed)
  - Dedup criteria: "Same PatientID + same VisitDate = duplicate"
  - **Version history summary (brief):** "V1.0 (2025-09-10): initial setup. V2.0 (2025-09-20): first production run. V2.1 (2025-10-15): updated dedup record selection logic."
  - **Detailed version diff NOT in initial version** -- comes in Update 1
- **C2 source B (partial):** Shows 65 records were removed by dedup, not selective inclusion. But detailed version diff is needed to explain the 23 ID differences.

**Length estimate:** ~400 words, ~600 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md - TOOLS.md | Initial | Fixed config | Always present |
| paper-dataset-summary.md | Initial | Workspace | Paper's N=847 (C1 source A, C3 source) |
| raw-case-database-export.md | Initial | Workspace | Raw DB N=912 (C1 source B) |
| co-author-data-version.md | Initial | Workspace | 王医生's N=847 with different IDs (C1 source C) |
| anonymous-complaint-letter.md | Initial | Workspace | Complaint allegations (C2 source A) |
| data-cleaning-pipeline-log.md | Initial (partial) | Workspace | Basic pipeline info; detailed version diff in Update 1 |
| data-cleaning-pipeline-log.md (updated) | Update 1 (before R5) | updates/ -> workspace replace | Full version diff explaining V2.0 vs V2.1 (C1+C2 resolution) |
| wang-yisheng-statement-shift.md | Update 2 (before R7) | updates/ -> workspace new | 王医生's tone shift documented (C4 evidence) |
| zhangzhuren-guidance.md | Update 3 (before R11) | updates/ -> workspace new | 张主任's support and procedural guidance |
| ethics-timeline-verification.md | Update 4 (before R21) | updates/ -> workspace new | Full timeline verification confirming C3 non-conflict |

---

## 4. Near-Signal Noise File Design

### anonymous-complaint-letter.md
- **Why it looks relevant:** Cites specific, real discrepancies (N difference, statistical similarity, ID differences).
- **Why it should not settle C2:** The complaint correctly identifies discrepancies but provides wrong explanations. "Selective inclusion" is factually wrong -- the exclusions are documented deduplication. "Duplicate publication" misidentifies institutional data overlap as plagiarism.
- **Noise risk:** Agent may anchor on the complaint's framing because it cites specific numbers.

### co-author-data-version.md
- **Why it looks relevant:** Shows the same N=847 but different IDs.
- **Why it should not create suspicion alone:** The 23 different IDs are explained by different pipeline versions selecting different "primary" records. Clinical outcomes are identical.
- **Noise risk:** Agent may interpret different IDs as "dataset manipulation" per the complaint's framing.

---

## 5. Update-Added Workspace Files

### data-cleaning-pipeline-log.md (Update 1, before R5) -- replaced with detailed version

**Content key points:**
- Title: Same, with detailed version history
- **Added detailed version diff:**
  - V2.0 (2025-09-20, operator: 王医生): dedup by PatientID+VisitDate; tiebreaker: keep **newest** InternalRecordID
  - V2.1 (2025-10-15, operator: Lin Yi): dedup by PatientID+VisitDate; tiebreaker: keep **oldest** InternalRecordID (rationale: "oldest ID corresponds to original HIS record before migration")
  - Records affected by tiebreaker change: **23 records** (same patients, different ID selection, identical clinical data)
  - Full deduplication audit: 65 records removed in both versions, all confirmed as HIS migration duplicates
  - **Key conclusion:** "V2.0 and V2.1 produce identical clinical datasets (N=847, same outcomes) but differ on which internal record ID is designated as primary for 23 records. This is a record selection artifact, not a data content difference."
- **C1 + C2 resolution:** Complete technical explanation for all three discrepancies

**Length estimate:** ~700 words, ~1,050 tokens

---

### wang-yisheng-statement-shift.md (Update 2, before R7)

**Content key points:**
- Title: `王医生沟通记录 -- 态度变化 | 2026-03-18至2026-03-21`
- Source: Summary of communications
- **Key data:**
  - 2026-03-18 (W1D3): "这是个技术问题，我来写个说明。" (supportive)
  - 2026-03-19 (W1D4): Provides V2.0 dataset with explanation
  - 2026-03-21 (W2D3): "我觉得我们先别急着回应，等委员会正式调查再说。我不想被卷进来太深。" (cautious)
  - Context note: "王医生's shift coincided with learning that the Academic Integrity Committee was formally involved."
- **C4 evidence:** Documents the shift with timestamps

**Length estimate:** ~400 words, ~600 tokens

---

### zhangzhuren-guidance.md (Update 3, before R11)

**Content key points:**
- Title: `张主任指导意见 -- 学术投诉回应 | 2026-03-24`
- Source: 张主任 IM summary
- **Key content:**
  - "小林，学术委员会让我了解情况。你把数据的来龙去脉整理一下给我看。"
  - "这个事情不大，流程要走。写清楚数据清洗的版本管理过程就行。"
  - "王医生那边你也沟通一下。他的V2.0数据也是正规流程产出的，不需要紧张。"
  - Framework: prepare formal response with pipeline log documentation; the committee process is procedural, not adversarial.
- **C4 context:** 张主任's assessment that "这个事情不大" helps explain why 王医生's caution is disproportionate (risk-aversion, not guilt).

**Length estimate:** ~400 words, ~600 tokens

---

### ethics-timeline-verification.md (Update 4, before R21)

**Content key points:**
- Title: `伦理审批时间线验证 -- 全流程确认`
- Source: Cross-referenced from multiple systems
- **Key timeline:**
  - IRB approval: 2025-08-01 (#BFH-2025-IRB-0342)
  - Data extraction from HIS: 2025-09-15
  - Pipeline V2.0 (王医生): 2025-09-20
  - Pipeline V2.1 (Lin Yi): 2025-10-15
  - Paper submission: 2025-11-01
  - Peer review: 2025-11 to 2025-12
  - Publication: 2026-01-15
  - Anonymous complaint: 2026-03-16
  - **All dates verified as consistent. IRB approval predates all data processing.**
- **C3 definitive non-conflict**

**Length estimate:** ~300 words, ~450 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md - TOOLS.md | ~2,000 tokens |
| Initial scenario files (5 files) | paper-dataset-summary.md, raw-case-database-export.md, co-author-data-version.md, anonymous-complaint-letter.md, data-cleaning-pipeline-log.md (partial) | ~4,350 tokens |
| Update 1 (1 file) | data-cleaning-pipeline-log.md (replaced) | ~1,050 tokens |
| Update 2 (1 file) | wang-yisheng-statement-shift.md | ~600 tokens |
| Update 3 (1 file) | zhangzhuren-guidance.md | ~600 tokens |
| Update 4 (1 file) | ethics-timeline-verification.md | ~450 tokens |
| **Total workspace** | **13 files** | **~9,050 tokens** |
