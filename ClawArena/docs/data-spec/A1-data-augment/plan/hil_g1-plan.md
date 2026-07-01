# hil_g1 Sub-Plan: Candidate Background Check Discrepancy

> Scene: Chen Jing (HR Manager) conducts a background check on P7-level candidate
> Wang Hao, uncovering team size inflation (12 vs 4) and a concealed 6-month employment gap.

---

## 一、场景概要

- **Scene ID**: hil_g1
- **User/Persona**: Chen Jing (陈静), HR Manager
- **Language**: **English** (original questions.json is English)
- **Total rounds**: 30 (8 MC + 22 EC = 73.3% EC)
- **Updates**: 4 updates, spaced at q5, q10, q17, q23

---

## 二、Chen Jing 偏好规则 (P1–P5)

| Rule | Description | Check logic |
|------|------------|-------------|
| P1 | Bullet-point summaries with section headings — avoid dense prose paragraphs | ≥3 `##` headings AND at least 3 bullet/list items (`^- ` or `^* `) |
| P2 | Chinese-style naming convention with date prefix (e.g., `2026-03-19_背调报告.md` or `2026-03-19_background_check.md`) | ≥1 file in docs/ with `YYYY-MM-DD_` prefix |
| P3 | Executive summary or conclusion first — lead with the answer, then evidence | `## Executive Summary` or `## Summary` or `## Conclusion` heading appears before evidence sections |
| P4 | Balance qualitative (behavioral observations) with quantitative (exact numbers) | Both: a number like "12" or "4" or "4.3" AND a behavioral description ("hesitated" or "leadership" or "observed") |
| P5 | Professional but warm tone — acknowledge candidate's genuine technical skills even while flagging discrepancies | Technical strengths acknowledged in same document as discrepancies |

check_preferences.py P rules:
- P1: count `^## ` ≥3 AND `^[-*] ` ≥3
- P2: ≥1 file in docs/ matching `^\d{4}-\d{2}-\d{2}_`
- P3: first `##` heading contains "Summary" or "Conclusion" or "Executive" or "Finding"
- P4: `\b1[02]\b` (12) or `\b4[-–]5\b` (4-5) AND ("hesitat" or "leadership" or "observed" or "behavioral") present
- P5: ("technical" or "engineering") AND ("skill" or "ability" or "strength") present alongside discrepancy mention

---

## 三、关键数值（Ground Truth）

| Fact | Value | Source |
|------|-------|--------|
| Resume: team size claimed | **12 engineers** (cross-functional) | candidate-resume.md |
| Reference check: team size | **"about 4 engineers"** (Liu Wei, former director) | reference-check-emails.md |
| Interview observation | **"4–5 direct reports"** (candidate self-corrected after hesitation) | interview-feedback-forms.md (upd1) |
| Team size discrepancy ratio | **3x inflation** (12 ÷ 4 = 3) | calculated |
| Employment gap start | **2023-06** (June 2023, departed StarBridge) | linkedin-profile-export.md (upd2) |
| Employment gap end | **2024-01** (January 2024, returned to StarBridge) | linkedin-profile-export.md (upd2) |
| Gap duration | **7 months** (June 2023 – January 2024) | calculated |
| GitHub zero contribution period | **2023-06 to 2023-12** (6 months) | github-contribution-export.md |
| Resume claim about gap period | continuous employment + "active open-source contributions throughout" | candidate-resume.md |
| Technical score (Huang Lei) | **4.3/5.0** | huang-lei-assessment-email.md (upd3) |
| Leadership score (Huang Lei) | **2.8/5.0** | huang-lei-assessment-email.md (upd3) |
| Huang Lei recommendation | P6 IC, NOT P7 team lead | huang-lei-assessment-email.md (upd3) |
| Other interviewers (Chen Wei, Li Min) | 4.0–4.3 tech, "Hire" recommendation | interview-feedback-forms.md (upd1) |
| CTO hiring deadline pressure | Q2 business-critical, board visibility | cto-hiring-priority-email.md |
| HR VP stance | "background check findings go on record; no shortcuts" | vp_zhangwei_feishu.md (upd4) |
| CTO response to discrepancy | "everyone inflates their resume" — seeks to minimize | cto_liqiang_feishu.md (upd4) |

---

## 四、矛盾（C1–C4）

- **C1**: Resume claims 12-person team; reference check says "about 4"; interview observation catches candidate self-correcting to "4–5 direct reports" after hesitation — 3x inflation, candidate aware of the discrepancy
- **C2**: Resume claims "maintained active open-source contributions throughout tenure"; GitHub export shows zero contributions June–December 2023 (6 months) — directly contradicted by public record
- **C3**: Resume implies continuous employment 2018–2025; LinkedIn profile (candidate's own) shows departure June 2023, return January 2024 — deliberate concealment, not omission
- **C4**: CTO dismisses discrepancies as "normal resume polishing" and pushes for P7 offer; HR VP insists on following process; organizational pressure vs. process integrity conflict

---

## 五、Update 触发设计

| Update ID | Trigger Round | Files | What it reveals |
|-----------|--------------|-------|----------------|
| upd1_workspace | q5 | interview-feedback-forms.md | Huang Lei's full feedback: candidate hesitated on team size, self-corrected to "4–5 direct reports"; tech 4.3/5 but leadership 2.8/5; recommend P6 not P7 |
| upd2_sessions, upd2_workspace | q10 | recruiter_liuyang_im.md, linkedin-profile-export.md | Liu Yang found LinkedIn profile showing departure June 2023 / return January 2024 — confirms C3 (employment gap) and C2 (zero GitHub during gap) |
| upd3_sessions, upd3_workspace | q17 | tl_huanglei_email.md, huang-lei-assessment-email.md | Huang Lei's formal written assessment: P6 IC conditional offer (if candidate explains honestly), explicitly NOT P7; leadership concerns based on behavioral interview |
| upd4_sessions, upd4_workspace | q23 | cto_liqiang_feishu.md, vp_zhangwei_feishu.md | CTO pushback ("everyone inflates") vs Zhang Wei (HR VP) support for process; CTO agrees to candidate confrontation session before final decision |

---

## 六、题目序列设计（30 轮）

### Phase 1: 初始信号 (q1–q4)

**q1** [MC]
- Topic: Initial evidence from workspace docs
- Based on: candidate-resume.md + reference-check-emails.md + cto-hiring-priority-email.md
- Question: "Based on available workspace documents, which statements about the background check findings are supported?"
- Answer: reference check (Liu Wei) says ~4 engineers vs resume claims 12; CTO urgency email noted; tech skills from resume appear genuine

**q2** [MC]
- Topic: Team size discrepancy (pre-interview data only)
- Question: "Based on current evidence (before interview feedback), which statements about the team size discrepancy are supported?"
- Answer: 3x gap between resume (12) and reference (4); single source (Liu Wei); independent confirmation needed

**q3** [EC, L2, pref:P1,P3]
- Task: Create `analysis/initial_discrepancy_summary.md` — document the C1 team size discrepancy with available evidence; structure with Executive Summary first
- check_initial_discrepancy.py: validates "12" AND "4" present, "## Summary" or "## Executive Summary" or "## Finding" heading before other ##s, "3x" or "three times" or "ratio" present, ≥3 ## headings

**q4** [EC, L2]
- Task: Create `analysis/cto_urgency_context.md` — document CTO's hiring timeline pressure (Q2 business-critical, board visibility) and analyze potential bias risk: urgency pressure may compromise background check integrity
- check_cto_urgency.py: validates "Q2" or "business-critical" or "board" present, "pressure" or "urgency" or "timeline" present, bias or integrity risk mentioned, ≥2 ## headings

### Phase 2: upd1 후 — 面试观察 (q5–q9)

**q5** [MC, update_ids: upd1_workspace]
- Topic: Interview feedback (Huang Lei) reveals
- Question: "After reviewing Huang Lei's interview feedback (Update 1), which statements about the candidate's self-presentation are supported?"
- Answer: candidate hesitated when asked about team size, then self-corrected to "4–5 direct reports" — aware of discrepancy; tech 4.3/5, leadership 2.8/5; Huang Lei recommends P6 not P7

**q6** [EC, L2]
- Task: Create `analysis/interview_behavioral_analysis.md` — analyze the behavioral signals in Huang Lei's interview: hesitation + self-correction on team size indicates awareness; leadership score (2.8/5) vs technical score (4.3/5) gap significance for P7 role
- check_interview_behavioral.py: validates "hesitat" OR "self-correct" present, "4.3" AND "2.8" present, "P7" AND ("not recommend" or "P6" or "risk") present, ≥3 ## headings

**q7** [EC, L2, pref:P4]
- Task: Create `analysis/github_contribution_analysis.md` — analyze GitHub contribution export; document the 6-month zero-contribution gap (June–December 2023); compare to resume claim of "active contributions throughout tenure"
- check_github_analysis.py: validates "2023" AND "June" or "Jun" or "2023-06" present, "zero" or "0" contributions AND "6 months" or "six months" present, resume claim directly contradicted, ≥3 ## headings

**q8** [EC, L2]
- Task: Create `analysis/three_source_corroboration.md` — document how 3 independent sources confirm C1: (1) reference check Liu Wei (4 engineers), (2) interview hesitation + self-correction (4–5 direct), (3) candidate's own interview statement
- check_three_source.py: validates "Liu Wei" present, "hesitat" or "self-correct" present, "three" or "3" sources mentioned, ≥2 ## headings, corroboration/convergence language

**q9** [EC, L2]
- Task: Create `analysis/discrepancy_severity_assessment.md` — assess severity of C1: 3x inflation for team lead role (P7 requires demonstrated team management); distinguish from acceptable "polishing"
- check_severity.py: validates "3x" or "300%" or "12" vs "4" ratio, "P7" requirements vs leadership score gap, "inflat" or "exaggerat" present, ≥2 ## headings

### Phase 3: upd2 후 — LinkedIn 就业缺口 (q10–q16)

**q10** [MC, update_ids: upd2_sessions, upd2_workspace]
- Topic: LinkedIn profile reveals employment gap
- Question: "After reviewing the LinkedIn profile discovery (Update 2), which statements are supported?"
- Answer: LinkedIn shows departure June 2023, return January 2024 (7 months); candidate's own profile contradicts resume; GitHub zero contributions corroborate gap; this is resume fraud (not omission)

**q11** [EC, L2]
- Task: Create `analysis/employment_gap_verification.md` — document C3 gap: LinkedIn shows 2023-06 departure, 2024-01 return (7 months); GitHub shows 6 months zero (June–December); both public sources confirm
- check_employment_gap.py: validates "2023-06" or "June 2023" AND "2024-01" or "January 2024" present, "7 months" or "seven months" or "6 months" present, "LinkedIn" AND "GitHub" both mentioned as confirming sources, ≥3 ## headings

**q12** [EC, L2]
- Task: Create `analysis/discrepancy_matrix.md` — 3-column table: Claim (resume), Reality (evidence), Discrepancy Type, Source; covering C1 (team size), C2 (open-source activity), C3 (employment continuity)
- check_discrepancy_matrix.py: validates "12" vs "4" row present, "0" contributions or "zero" gap period row, employment continuity row, ≥3 data rows in table format

**q13** [EC, L2]
- Task: Create `analysis/fraud_vs_polish_distinction.md` — distinguish between acceptable resume polishing (slight exaggeration, context-dependent) vs actionable misrepresentation; assess C1 (3x inflation) and C3 (active concealment of gap) against this standard
- check_fraud_polish.py: validates "polish" or "exaggerat" vs "fraud" or "misrepresent" distinction, C1 (12 vs 4, 3x) classified as actionable, C3 gap classified as active concealment, ≥3 ## headings

**q14** [EC, L2, pref:P2]
- Task: Create `docs/YYYY-MM-DD_background_check_findings_memo.md` — formal findings memo for HR records; must use date-prefix (P2), cover C1–C3
- check_bc_memo.py: validates docs/ date-prefixed file, "C1" or "team size" discrepancy present, "C2" or "GitHub" or open-source gap present, "C3" or "employment gap" or LinkedIn present, ≥4 ## headings

**q15** [EC, L2]
- Task: Create `analysis/cto_bias_risk_analysis.md` — analyze CTO pressure as B1 bias source: "everyone inflates" minimization narrative; organizational dynamics vs process integrity
- check_cto_bias.py: validates CTO's minimization discussed, "bias" or "pressure" present, HR process integrity mentioned, ≥2 ## headings

**q16** [EC, L2]
- Task: Create `scripts/score_background_check.py` — Python script that reads candidate-resume.md, reference-check-emails.md, and github-contribution-export.md from workspace; outputs JSON scoring: team_size_discrepancy_ratio (float), gap_months (int), github_zero_months (int)
- eval.command: `cd ${workspace} && python scripts/score_background_check.py 2>&1 | python3 -c "import sys, json; d=json.load(sys.stdin); sys.exit(0 if abs(d.get('team_size_discrepancy_ratio', 0) - 3.0) <= 0.5 else 1)"`
- eval.timeout: 30

### Phase 4: upd3 후 — 黄磊正式评估 (q17–q22)

**q17** [MC, update_ids: upd3_sessions, upd3_workspace]
- Topic: Huang Lei's formal written assessment
- Question: "After reviewing Huang Lei's formal written assessment (Update 3), which statements are now supported?"
- Answer: Technical ability solid (P6 level, 4.3/5); leadership evidence insufficient for P7 (2.8/5, textbook answers only); conditional P6 offer appropriate; P7 premature without honest explanation

**q18** [EC, L2]
- Task: Create `analysis/level_assessment_comparison.md` — compare P6 vs P7 requirements against candidate data; for P7: needs demonstrated 8+ person team management — evidence only shows 4–5 at best
- check_level_assessment.py: validates "P6" AND "P7" compared, "4.3" (tech) AND "2.8" (leadership) present, ≥2 requirements for P7 listed vs candidate gap, ≥3 ## headings

**q19** [EC, L2]
- Task: Create `analysis/conditional_offer_rationale.md` — document rationale for conditional P6 offer: technical ability confirmed (IC level), leadership claims unverified (P7 not justified), honest explanation as condition
- check_conditional_offer.py: validates "P6" recommended AND "P7" not recommended with reasoning, "condition" or "conditional" present, ≥2 ## headings

**q20** [EC, L2]
- Task: Create `analysis/behavioral_interview_gap.md` — analyze why Huang Lei scored leadership 2.8/5: candidate gave "textbook" answers without real-world specifics; in context of C1, this makes sense — limited actual management experience
- check_behavioral_gap.py: validates "2.8" AND "leadership" AND Huang Lei present, "textbook" or "generic" or "no specifics" interview observation present, C1 connection made (explains why generic), ≥3 ## headings

**q21** [EC, L2, pref:P1,P3,P4]
- Task: Create `docs/YYYY-MM-DD_recommendation_report.md` — formal recommendation report with conclusion first (P3): P6 conditional offer; bullet structure (P1); quantitative support (P4: scores, ratios)
- check_recommendation_report.py: validates docs/ date-prefixed file, P6 recommendation stated, "## Summary" or "## Recommendation" or "## Conclusion" first heading, "4.3" AND "2.8" AND "12" AND "4" present, ≥5 ## headings

**q22** [EC, L2]
- Task: Create `analysis/evidence_convergence_summary.md` — document how 4+ independent sources converge on C1: (1) Liu Wei reference, (2) Huang Lei interview observation, (3) GitHub gap, (4) LinkedIn gap; all consistent
- check_convergence.py: validates ≥4 sources listed, "converge" or "consistent" or "independent" confirmation language, ≥3 ## headings

### Phase 5: upd4 후 — 组织压力与决策 (q23–q30)

**q23** [MC, update_ids: upd4_sessions, upd4_workspace]
- Topic: CTO vs HR VP divergence
- Question: "After receiving CTO and HR VP messages (Update 4), which statements about organizational dynamics are supported?"
- Answer: CTO minimizes ("everyone inflates") seeking P7 offer; Zhang Wei (HR VP) insists on process integrity; CTO agrees to confrontation session; tension documented

**q24** [EC, L2]
- Task: Create `analysis/organizational_dynamics_analysis.md` — document CTO vs HR VP divergence; analyze why CTO minimization is itself a risk (endorsing misrepresentation sets precedent); HR VP's position is correct
- check_org_dynamics.py: validates "CTO" AND ("Zhang Wei" or "HR VP") with opposing positions, precedent/risk of minimization argued, ≥3 ## headings

**q25** [EC, L2]
- Task: Create `analysis/confrontation_session_framework.md` — framework for the planned candidate confrontation session: what to ask, what constitutes honest explanation, what constitutes evasion; decision criteria for P6 vs rejection
- check_confrontation_framework.py: validates confrontation questions or criteria listed, "P6" vs rejection criteria stated, "honest explanation" condition present, ≥3 ## headings

**q26** [EC, L2]
- Task: Create `docs/YYYY-MM-DD_hr_risk_register.md` — HR risk register documenting C1–C4 as risks; for each: description, severity, evidence, recommended action, owner
- check_risk_register.py: validates docs/ date-prefixed file, ≥4 risk entries, each has severity/action/evidence, C4 (CTO pressure) included as process risk, ≥4 ## headings or table rows

**q27** [EC, L2]
- Task: Create `analysis/decision_tree_final.md` — decision tree for candidate outcome: if honest explanation → P6 offer; if evasive/denies → reject; if CTO overrides → escalate to HR VP; document the tree and Chen Jing's role
- check_decision_tree.py: validates decision tree structure (at least 2 branches with conditions), "P6" offer branch AND rejection branch present, "escalate" or "Zhang Wei" as override path, ≥3 ## headings

**q28** [MC]
- Topic: B1 and B2 bias risks in the investigation
- Question: "Which statements about analytical bias risks in this background check are supported?"
- Answer: B1 (anchoring to CTO urgency framing), B2 (assuming technical skill implies leadership skill); evidence-based approach with multiple independent sources mitigates both

**q29** [EC, L2]
- Task: Create `docs/YYYY-MM-DD_final_background_check_report.md` — comprehensive final report following all P1–P5: bullet structure + headings (P1), date-prefixed (P2), recommendation/conclusion first (P3), quantitative + behavioral (P4), professional-warm acknowledging tech strengths (P5)
- eval.command: `python ${eval_dir}/scripts/check_preferences.py ${workspace} --rules P1,P2,P3,P4,P5 --target docs/ && python ${eval_dir}/scripts/check_final_bgcheck.py ${workspace}`
- check_final_bgcheck.py: validates docs/ date-prefixed file, "12" AND "4" present (C1), employment gap "2023" present (C3), "P6" recommendation present, "4.3" AND "2.8" scores present, ≥5 ## headings, ≥800 chars

**q30** [MC]
- Topic: Final comprehensive assessment
- Question: "Which statements represent the most accurate final assessment of Wang Hao's candidacy?"
- Answer: Technical ability P6-solid; P7 not justified based on evidence; P6 conditional offer correct path; CTO pressure does not override documented discrepancies

---

## 七、评测脚本清单

| Script | What to validate | Key checks |
|--------|-----------------|-----------|
| check_initial_discrepancy.py | analysis/initial_discrepancy_summary.md | "12"+"4", exec summary first, 3x ratio |
| check_cto_urgency.py | analysis/cto_urgency_context.md | Q2/board urgency, bias risk |
| check_interview_behavioral.py | analysis/interview_behavioral_analysis.md | "hesitat"/"self-correct", 4.3+2.8, P6 not P7 |
| check_github_analysis.py | analysis/github_contribution_analysis.md | 2023-06, zero/6 months, resume contradicted |
| check_three_source.py | analysis/three_source_corroboration.md | Liu Wei, hesitat/self-correct, 3 sources |
| check_severity.py | analysis/discrepancy_severity_assessment.md | 3x/300%, P7 leadership gap |
| check_employment_gap.py | analysis/employment_gap_verification.md | 2023-06+2024-01, 7 months, LinkedIn+GitHub |
| check_discrepancy_matrix.py | analysis/discrepancy_matrix.md | 12 vs 4, zero gap, employment row |
| check_fraud_polish.py | analysis/fraud_vs_polish_distinction.md | polish vs fraud distinction, C1+C3 classified |
| check_bc_memo.py | docs/YYYY-MM-DD_background_check_findings_memo.md | date-prefixed, C1+C2+C3 mentioned |
| check_cto_bias.py | analysis/cto_bias_risk_analysis.md | CTO minimization, bias/pressure, process integrity |
| (inline) | scripts/score_background_check.py | JSON team_size_discrepancy_ratio ≈ 3.0 |
| check_level_assessment.py | analysis/level_assessment_comparison.md | P6+P7 compared, 4.3+2.8, requirements vs gap |
| check_conditional_offer.py | analysis/conditional_offer_rationale.md | P6 recommended, P7 not, condition present |
| check_behavioral_gap.py | analysis/behavioral_interview_gap.md | 2.8+leadership+Huang Lei, textbook/generic |
| check_recommendation_report.py | docs/YYYY-MM-DD_recommendation_report.md | date-prefixed, P6, exec summary first, 4.3+2.8+12+4 |
| check_convergence.py | analysis/evidence_convergence_summary.md | ≥4 sources, convergence language |
| check_org_dynamics.py | analysis/organizational_dynamics_analysis.md | CTO vs HR VP positions, precedent risk |
| check_confrontation_framework.py | analysis/confrontation_session_framework.md | questions/criteria, P6 vs reject conditions |
| check_risk_register.py | docs/YYYY-MM-DD_hr_risk_register.md | date-prefixed, ≥4 risks, C4 CTO risk included |
| check_decision_tree.py | analysis/decision_tree_final.md | ≥2 branches, P6+reject+escalate |
| check_final_bgcheck.py | docs/YYYY-MM-DD_final_background_check_report.md | 12+4, 2023 gap, P6, 4.3+2.8, ≥5 ## |
| check_preferences.py | docs/ | P1–P5 rules (scene-specific, see §二) |

---

## 八、特别注意事项

1. **q16 (L3)**: score_background_check.py reads workspace files; team_size_discrepancy_ratio = 12/4 = 3.0
2. **pref rounds**: q3 (P1,P3), q7 (P4), q14 (P2), q21 (P1,P3,P4) — non-scoring educational
3. **q29 full scoring**: --rules P1,P2,P3,P4,P5
4. **Employment gap**: LinkedIn shows 7 months (June 2023 – January 2024), but GitHub only shows 6 months zero (June–December 2023); both are valid but document both figures accurately in check scripts
5. **P2 naming**: the original workspace has Chinese naming convention (2026年03月_主题.md) but since questions.json is English, the file naming in tasks can be English date prefix format (YYYY-MM-DD_topic.md)
