# hil_i2 Sub-Plan: Research Data Reuse Accusation Response

> Scene: ER physician Dr. Lin Yi responds to an anonymous complaint accusing her research
> team of data reuse, selective exclusion, and potential duplicate publication.

---

## 一、场景概要

- **Scene ID**: hil_i2
- **User/Persona**: Lin Yi (林怡), ER physician / researcher
- **Language**: **English** (original questions.json is English)
- **Total rounds**: 30 (8 MC + 22 EC = 73.3% EC)
- **Updates**: 4 updates, spaced at q5, q10, q16, q22

---

## 二、Lin Yi 偏好规则 (P1–P5)

| Rule | Description | Check logic |
|------|------------|-------------|
| P1 | Problem / Assessment / Plan structure (clinical decision framework) | Document has "Problem" AND "Assessment" AND "Plan" sections (or functional equivalents) |
| P2 | Date + patient-ID or date + topic naming convention (e.g., 2026-03-27_committee_response.md) | ≥1 file in docs/ with `YYYY-MM-DD_` prefix |
| P3 | Conclusion / diagnosis first, then supporting evidence chain | First substantial section contains conclusions or findings, not just intro |
| P4 | Evidence-based references: cite pipeline versions, IRB numbers, specific dates | Contains "IRB" and "#BFH-2025-IRB-0342" or specific pipeline versions "V2.0" / "V2.1" |
| P5 | Concise ER professional style — direct, no filler phrases; quantify everything | No "it is worth noting that" or similar filler; avg sentence length signals (hard to check directly) — use: ≥3 specific numbers in doc |

check_preferences.py P rules:
- P1: ("Problem" or "Issue") AND ("Assessment" or "Analysis") AND ("Plan" or "Recommendation") in headings
- P2: ≥1 file in docs/ matching `^\d{4}-\d{2}-\d{2}_`
- P3: first `##` section heading appears within first 400 chars of content
- P4: "IRB" present AND ("V2.0" or "V2.1" or "pipeline") present
- P5: ≥3 numeric values in document (`\b\d+\b` at least 3 distinct occurrences)

---

## 三、关键数值（Ground Truth）

| Fact | Value | Source |
|------|-------|--------|
| Raw database N | **912** | raw-case-database-export.md |
| Published paper N | **847** | paper-dataset-summary.md |
| Difference | **65 records** | calculated: 912 - 847 |
| Source of 65 duplicates | 100% from HIS migration (2025-07-15) | data-cleaning-pipeline-log.md |
| Pipeline V2.0 date | **2025-09-20** | data-cleaning-pipeline-log.md |
| Pipeline V2.0 operator | Wang Yisheng (co-author) | data-cleaning-pipeline-log.md |
| Pipeline V2.0 tiebreaker | newest InternalRecordID | data-cleaning-pipeline-log.md |
| Pipeline V2.1 date | **2025-10-15** | data-cleaning-pipeline-log.md |
| Pipeline V2.1 operator | Lin Yi | data-cleaning-pipeline-log.md |
| Pipeline V2.1 tiebreaker | oldest InternalRecordID | data-cleaning-pipeline-log.md |
| Records with ID-only diff | **23** (out of 65) | co-author-data-version.md |
| Clinical data diff among 23 | **0** (all identical: age, sex, triage, 30d-MACE) | co-author-data-version.md |
| IRB approval number | **#BFH-2025-IRB-0342** | paper-dataset-summary.md |
| IRB approval date | **2025-08-01** | paper-dataset-summary.md |
| Data extraction date | **2025-09-15** | raw-case-database-export.md |
| Paper submission date | **2025-11-01** | paper-dataset-summary.md |
| Paper publication date | **2026-01-15** | paper-dataset-summary.md |
| Complaint receipt date | **2026-03-16** | anonymous-complaint-letter.md |
| Days from publication to complaint | **61 days** | calculated |
| IRB → data extraction interval | **45 days** (Aug 1 → Sep 15) | calculated |
| Zhang Zhuren 2024 paper period | 2022–2023 | zhangzhuren-guidance.md (upd3) |
| Lin Yi paper period | 2024–2025 | paper-dataset-summary.md |
| Committee initial judgment | "documentation gap, not academic misconduct" | committee_email.md (upd4) |
| Committee decision date | **2026-03-27** | committee_email.md (upd4) |

---

## 四、矛盾（C1–C4）

- **C1**: Complaint claims "selective exclusion" (65 records removed) — pipeline log proves 100% of 65 are HIS migration duplicates, standard deduplication procedure
- **C2**: Complaint claims "duplicate publication" (statistical similarity to Zhang 2024) — Zhang paper covers 2022–2023; Lin paper covers 2024–2025; no data period overlap
- **C3**: Wang Yisheng's V2.0 and Lin Yi's V2.1 produce different 23 record IDs — tiebreaker logic differs (newest vs oldest ID); 0 clinical data differences; not data manipulation
- **C4**: Wang Yisheng initially supportive, then became evasive (self-protection due to ongoing promotion review) — does NOT indicate guilt, only personal career risk

---

## 五、Update 触发设计

| Update ID | Trigger Round | Files | What it reveals |
|-----------|--------------|-------|----------------|
| upd1_workspace | q5 | data-cleaning-pipeline-log.md | Detailed V2.0 vs V2.1 comparison: 65 = HIS migration duplicates; 23 ID-only differences, 0 clinical differences; tiebreaker logic explained |
| upd2_sessions, upd2_workspace | q10 | wangyisheng_im.md, wang-yisheng-statement-shift.md | Wang Yisheng's attitude shift from collaborative to self-protective; motivation is promotion risk, not guilt |
| upd3_sessions, upd3_workspace | q16 | zhangzhuren_im.md, zhangzhuren-guidance.md | Zhang Zhuren confirms: his 2024 paper covers 2022–2023 (no overlap); recommends 3-page P/A/P response + pipeline log attachment |
| upd4_sessions, upd4_workspace | q22 | committee_email.md, ethics-timeline-verification.md | Committee independently verifies 8 timeline events; preliminary judgment: documentation gap, not misconduct; recommend corrigendum not retraction |

---

## 六、题目序列设计（30 轮）

### Phase 1: 初始证据 (q1–q4)

**q1** [MC]
- Topic: Research timeline consistency
- Based on: paper-dataset-summary.md + raw-case-database-export.md
- Question: "Based on available workspace documents, which statements about the research timeline are supported by evidence?"
- Answer: IRB approved 2025-08-01 before data extraction 2025-09-15; N difference (912 vs 847) documented

**q2** [MC]
- Topic: N discrepancy initial assessment
- Question: "Before reviewing the detailed pipeline log, which statements about the N=912 vs N=847 discrepancy are supported?"
- Answer: 65-record difference documented; HIS migration on 2025-07-15 is potential cause; co-author data version shows 23 ID-only differences; final determination requires pipeline log

**q3** [EC, L2, pref:P1,P3]
- Task: Create `analysis/n_discrepancy_preliminary.md` — initial analysis of the N discrepancy using available workspace docs; structure as Problem / Assessment / Plan
- check_n_discrepancy_prelim.py: validates "912" AND "847" AND "65" present, P/A/P structure (Problem OR Issue) AND (Assessment OR Analysis), ≥3 ## headings

**q4** [MC]
- Topic: Lin Yi's communication preferences (P1–P5 identification)
- Question: "Based on Lin Yi's communication patterns and explicit preferences, which statements about her preferred output format are accurate?"
- Answer: Problem/Assessment/Plan structure, date+ID naming, conclusion-first, IRB citation style, ER-concise

### Phase 2: upd1 후 — 管道日志详情 (q5–q9)

**q5** [MC, update_ids: upd1_workspace]
- Topic: Detailed pipeline log reveals
- Question: "After reviewing the detailed data-cleaning pipeline log (Update 1), which statements are now supported?"
- Answer: 65 records are ALL HIS migration duplicates; V2.0 and V2.1 differ by tiebreaker (newest vs oldest ID); 23 records have different IDs but 0 clinical differences

**q6** [EC, L2]
- Task: Create `analysis/deduplication_verification.md` — document the deduplication process: 912 raw → 847 after removing 65 HIS migration duplicates; explain tiebreaker logic for V2.0 vs V2.1
- check_dedup_verification.py: validates "912" AND "847" AND "65" present, "HIS" AND "migration" present, "tiebreaker" OR "V2.0" AND "V2.1" present, "23" present (ID-only diff)

**q7** [EC, L2]
- Task: Create `analysis/version_difference_table.md` — Markdown table comparing V2.0 and V2.1: operator, date, tiebreaker logic, resulting IDs (for 23 affected records), clinical outcomes
- check_version_table.py: validates "V2.0" AND "V2.1" present, "Wang" or "Wang Yisheng" (V2.0 operator) present, "2025-09-20" or "September 20" present, "2025-10-15" or "October 15" present, "23" present, "0" clinical differences mentioned

**q8** [EC, L2, pref:P4]
- Task: Create `analysis/complaint_rebuttal_point_by_point.md` — structured rebuttal of the anonymous complaint's 3 allegations (selective exclusion, duplicate publication, data manipulation); must cite IRB number and pipeline version
- check_rebuttal.py: validates 3 allegations addressed ("Allegation 1" or "C1" structure), "#BFH-2025-IRB-0342" or "IRB-0342" present, "V2.1" present, "0" clinical differences stated, ≥4 ## headings

**q9** [EC, L2]
- Task: Create `analysis/timeline_verification_matrix.json` — JSON of 8 key events: event, date, verified_by, significance; must include IRB approval, data extraction, V2.0 run, V2.1 run, submission, publication, complaint
- check_timeline_matrix.py: validates JSON, ≥7 events, "2025-08-01" (IRB) AND "2025-09-15" (extraction) present, events in chronological order, all dates are before or same as submission (no pre-IRB data processing)

### Phase 3: upd2 후 — Wang Yisheng 态度转变 (q10–q15)

**q10** [MC, update_ids: upd2_sessions, upd2_workspace]
- Topic: Wang Yisheng's stance shift
- Question: "After reviewing Wang Yisheng's communications and statement shift (Update 2), which statements are supported?"
- Answer: Wang initially collaborative; shifted to self-protective after committee involvement; motivation is promotion review risk; technical position unchanged; shift does not indicate guilt

**q11** [EC, L2]
- Task: Create `analysis/wang_yisheng_motivation_analysis.md` — analyze Wang Yisheng's attitude evolution: cooperative (W1D3) → self-protective (W2D3); identify career risk as driver; distinguish self-protection from complicity
- check_wang_motivation.py: validates "Wang" present with timeline of attitude shift, "promotion" or "career" or "self-protect" present, "complicity" or "guilt" distinguished from career risk, ≥3 ## headings

**q12** [EC, L2]
- Task: Create `analysis/coauthor_technical_position.md` — document Wang's technical contributions: ran V2.0 with newest-ID tiebreaker; this was valid but not the final version (Lin Yi updated to V2.1); no data manipulation occurred
- check_coauthor_position.py: validates "V2.0" AND Wang as operator, "V2.1" AND Lin Yi as operator, "tiebreaker" explained, "valid" or "legitimate" approach mentioned, ≥3 ## headings

**q13** [EC, L2, pref:P3,P4]
- Task: Create `docs/YYYY-MM-DD_committee_response_draft.md` — draft response for committee; must: conclusion first (P3), cite IRB and pipeline versions (P4), use P/A/P structure (P1)
- check_committee_response.py: validates docs/ date-prefixed file, "#BFH-2025-IRB-0342" or "IRB" number present, "V2.1" present, "65" AND "912" AND "847" present, ≥4 ## headings

**q14** [EC, L2]
- Task: Create `analysis/evidence_credibility_assessment.md` — assess credibility of each evidence source: anonymous complaint (low), pipeline log (high), IRB records (highest), Wang's IM messages (medium — attitude-driven)
- check_credibility.py: validates ≥4 evidence sources with credibility levels, "anonymous" complaint rated lower, "IRB" or "pipeline" rated highest, ≥3 ## headings

**q15** [EC, L3]
- Task: Create `scripts/verify_timeline_sequence.py` — Python script reading workspace documents to verify that IRB approval date < data extraction date < pipeline run dates < submission date; outputs JSON with verification results per event
- eval.command: `cd ${workspace} && python scripts/verify_timeline_sequence.py 2>&1 | python3 -c "import sys, json; d=json.load(sys.stdin); sys.exit(0 if d.get('irb_before_extraction') and d.get('extraction_before_pipeline') and d.get('pipeline_before_submission') else 1)"`
- eval.timeout: 30

### Phase 4: upd3 후 — Zhang Zhuren 指导 (q16–q21)

**q16** [MC, update_ids: upd3_sessions, upd3_workspace]
- Topic: Zhang Zhuren's clarification and guidance
- Question: "After receiving Zhang Zhuren's guidance (Update 3), which statements are now supported?"
- Answer: Zhang 2024 paper covers 2022–2023 (no temporal overlap with Lin Yi's 2024–2025); statistical similarity is normal for same population cohort across years; Zhang recommends P/A/P response with pipeline attachment

**q17** [EC, L2]
- Task: Create `analysis/duplicate_publication_rebuttal.md` — rebut the duplicate publication allegation specifically: compare time periods (2022-2023 vs 2024-2025), explain why statistical similarity in cardiology is expected for different-year cohorts
- check_dup_pub_rebuttal.py: validates "2022" AND "2023" (Zhang period) present, "2024" AND "2025" (Lin period) present, "no overlap" or "different period" or "independent cohort" present, statistical similarity explained as normal, ≥3 ## headings

**q18** [EC, L2]
- Task: Create `analysis/methods_documentation_gap.md` — identify the actual root problem: the paper's methods section was too brief on deduplication details; recommend supplementary methods addition for future papers
- check_methods_gap.py: validates "methods" section and "insufficient" or "brief" or "lacking detail" present, "supplementary" or "future" improvement mentioned, "deduplication" described, ≥3 ## headings

**q19** [EC, L2]
- Task: Create `analysis/b2_bias_risk.md` — document B2 bias risk: anchoring to complaint framing ("if N differs, there's a problem") rather than "does the N difference have a valid explanation?"
- check_bias_risk.py: validates bias framing explained (anchoring or complaint-framing), correct reframe stated (difference with valid explanation ≠ problem), ≥2 ## headings

**q20** [EC, L2]
- Task: Create `docs/YYYY-MM-DD_zhang_zhuren_guidance_summary.md` — summarize Zhang Zhuren's guidance and incorporate into formal response strategy; note his confirmation about 2022–2023 period
- check_zhang_summary.py: validates docs/ date-prefixed file, "Zhang" present with guidance content, "2022" or "2023" confirmed period, P/A/P recommendation mentioned, ≥3 ## headings

**q21** [EC, L2, pref:P1,P2,P5]
- Task: Create `docs/YYYY-MM-DD_formal_committee_response.md` — formal response to academic committee; P/A/P structure, date-prefixed (P2), concise ER style with all numbers (P5)
- check_formal_response.py: validates docs/ date-prefixed file, "Problem" AND "Assessment" AND "Plan" headings, all 3 allegations addressed, "IRB" number present, "65" and "912" and "847" present, ≥5 ## headings

### Phase 5: upd4 후 — 委员会初步判断 (q22–q30)

**q22** [MC, update_ids: upd4_sessions, upd4_workspace]
- Topic: Committee initial assessment
- Question: "After receiving the committee's preliminary assessment (Update 4), which statements are supported?"
- Answer: committee independently verified 8 timeline events; judgment: documentation gap not misconduct; recommend corrigendum not retraction; IRB procedure confirmed correct

**q23** [EC, L2]
- Task: Create `analysis/committee_verification_summary.md` — document the 8 events the committee independently verified; highlight that IRB → extraction sequence confirmed; final judgment summary
- check_committee_verification.py: validates ≥7 events mentioned with dates, "documentation gap" or "not misconduct" judgment, "corrigendum" or "not retraction" mentioned, "2026-03-27" or "March 27" date present, ≥4 ## headings

**q24** [EC, L2]
- Task: Create `analysis/resolution_pathway.json` — JSON documenting recommended resolution steps: corrigendum content, supplementary methods content, future prevention measures
- check_resolution_pathway.py: validates JSON, "corrigendum" key or entry, "supplementary" method addition, ≥3 resolution steps

**q25** [EC, L2]
- Task: Create `analysis/full_case_timeline.md` — comprehensive chronological table from HIS migration (2025-07-15) through committee judgment (2026-03-27), including all key events
- check_full_timeline.py: validates "2025-07-15" or "July 15" (HIS migration) present, "2025-08-01" or "August 1" (IRB) present, "2026-03-27" or "March 27" (committee) present, ≥8 events in table or list

**q26** [EC, L2]
- Task: Create `docs/YYYY-MM-DD_case_closure_memo.md` — closure memo summarizing entire investigation: 4 allegations addressed, committee verdict, next steps (corrigendum), lessons learned
- check_closure_memo.py: validates docs/ date-prefixed file, 4 allegations/contradictions addressed, "corrigendum" present, "lesson" or "future" improvement present, ≥5 ## headings

**q27** [EC, L2]
- Task: Create `analysis/wang_yisheng_exoneration_note.md` — document that Wang Yisheng's self-protective behavior was career-motivated, not evidence of guilt; technical contributions (V2.0) were valid; both researchers acted professionally
- check_wang_exoneration.py: validates "Wang" AND ("exonerat" or "not at fault" or "valid" or "career motivation"), ≥2 ## headings, "promotion" or "career" as motivation mentioned

**q28** [MC]
- Topic: B2 bias post-mortem
- Question: "Which statements about the analytical bias risk in this investigation are supported?"
- Answer: B2 (anchoring to complaint framing) was a risk; systematic pipeline evidence overcame it; Wang Yisheng's defensiveness could have been misread as guilt; structured timeline analysis was key to correct assessment

**q29** [EC, L2]
- Task: Create `docs/YYYY-MM-DD_final_response_package.md` — final comprehensive response; P1–P5 compliant: P/A/P structure, date-prefixed, conclusion-first, IRB + pipeline citations, concise with ≥3 specific numbers
- eval.command: `python ${eval_dir}/scripts/check_preferences.py ${workspace} --rules P1,P2,P3,P4,P5 --target docs/ && python ${eval_dir}/scripts/check_final_response.py ${workspace}`
- check_final_response.py: validates docs/ date-prefixed file, "#BFH-2025-IRB-0342" or "IRB" present, "V2.0" AND "V2.1" present, "65" AND "912" AND "847" present, "corrigendum" or "committee" resolution mentioned, ≥5 ## headings, ≥800 chars

**q30** [MC]
- Topic: Final overall assessment
- Question: "Which statements represent the most accurate final assessment of the research integrity case?"
- Answer: no misconduct found; documentation gap was root cause; corrigendum appropriate; IRB timeline fully compliant; Wang Yisheng's behavior understandable given career risk

---

## 七、评测脚本清单

| Script | What to validate | Key checks |
|--------|-----------------|-----------|
| check_n_discrepancy_prelim.py | analysis/n_discrepancy_preliminary.md | 912, 847, 65 present; P/A/P structure |
| check_dedup_verification.py | analysis/deduplication_verification.md | 912, 847, 65, HIS migration, tiebreaker, 23 |
| check_version_table.py | analysis/version_difference_table.md | V2.0+Wang+2025-09-20, V2.1+Lin Yi+2025-10-15, 23, 0 clinical diff |
| check_rebuttal.py | analysis/complaint_rebuttal_point_by_point.md | 3 allegations, IRB-0342, V2.1, 0 clinical diff |
| check_timeline_matrix.py | analysis/timeline_verification_matrix.json | JSON, ≥7 events, 2025-08-01, 2025-09-15 |
| check_wang_motivation.py | analysis/wang_yisheng_motivation_analysis.md | Wang + attitude shift, promotion/career motivation |
| check_coauthor_position.py | analysis/coauthor_technical_position.md | V2.0+Wang, V2.1+Lin Yi, tiebreaker |
| check_committee_response.py | docs/YYYY-MM-DD_committee_response_draft.md | date-prefixed, IRB-0342, V2.1, 65+912+847 |
| check_credibility.py | analysis/evidence_credibility_assessment.md | ≥4 sources, anonymous low, IRB/pipeline high |
| (inline) | scripts/verify_timeline_sequence.py | JSON with 3 sequence flags all true |
| check_dup_pub_rebuttal.py | analysis/duplicate_publication_rebuttal.md | 2022-2023 vs 2024-2025, no overlap, normal similarity |
| check_methods_gap.py | analysis/methods_documentation_gap.md | methods insufficient, supplementary improvement |
| check_bias_risk.py | analysis/b2_bias_risk.md | anchoring/complaint framing, correct reframe |
| check_zhang_summary.py | docs/YYYY-MM-DD_zhang_zhuren_guidance_summary.md | date-prefixed, Zhang, 2022-2023 period |
| check_formal_response.py | docs/YYYY-MM-DD_formal_committee_response.md | date-prefixed, P/A/P, 3 allegations, IRB, 65+912+847 |
| check_committee_verification.py | analysis/committee_verification_summary.md | ≥7 events, "not misconduct", corrigendum, 2026-03-27 |
| check_resolution_pathway.py | analysis/resolution_pathway.json | JSON, corrigendum, supplementary, ≥3 steps |
| check_full_timeline.py | analysis/full_case_timeline.md | 2025-07-15, 2025-08-01, 2026-03-27, ≥8 events |
| check_closure_memo.py | docs/YYYY-MM-DD_case_closure_memo.md | date-prefixed, 4 allegations, corrigendum, lessons |
| check_wang_exoneration.py | analysis/wang_yisheng_exoneration_note.md | Wang exonerated, career motivation, V2.0 valid |
| check_final_response.py | docs/YYYY-MM-DD_final_response_package.md | IRB-0342, V2.0+V2.1, 65+912+847, corrigendum |
| check_preferences.py | docs/ | P1–P5 rules (scene-specific, see §二) |

---

## 八、特别注意事项

1. **q15 (L3)**: verify_timeline_sequence.py must output JSON parseable by eval.command; test it handles missing files gracefully
2. **pref rounds**: q3 (P1,P3), q8 (P4), q13 (P3,P4), q21 (P1,P2,P5)
3. **q29 full scoring**: --rules P1,P2,P3,P4,P5
4. **IRB number format**: "#BFH-2025-IRB-0342" — check scripts should look for "IRB-0342" as substring
5. **check_preferences.py P2**: "at least one file in docs/ has YYYY-MM-DD_ prefix"
