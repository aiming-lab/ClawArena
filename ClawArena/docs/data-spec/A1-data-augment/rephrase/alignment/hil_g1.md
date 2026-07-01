# Alignment Table — hil_g1

`exec_check` 题之 question-workspace-eval 三角对齐分析。

**任务**：候选人 Wang Hao 背调。四矛盾（C1 团队规模 12→4 / C2 7 月空窗 / C3 GitHub 0 提交 / C4 面试自我修正）。Chen Jing（HR Manager）领导，Liu Yang/Li Qiang/Huang Lei/Zhang Wei 协作。

**Round 可见性**：
- initial(round0): candidate-resume.md, reference-check-emails.md, cto-hiring-priority-email.md, github-contribution-export.md → q3,q4,q7,q8,q9
- upd1: interview-feedback-forms.md → q5,q6
- upd2: linkedin-profile-export.md, recruiter_liuyang_im.md, vp_zhangwei_feishu.md → q10–q16
- upd3: huang-lei-assessment-email.md, tl_huanglei_email.md → q17–q22
- upd4: cto-followup-message.md, cto_liqiang_feishu.md → q23–q30

**保全清单（任题不可动）**：
- 输出路径：`analysis/*.{md,json}`，`scripts/*.py`，`docs/YYYY-MM-DD_*.md`
- JSON 字段名（schema 索引）：`resume_team_size, reference_team_size, discrepancy_ratio, sources_checked, corroboration_needed, reference_name, huang_lei_technical, huang_lei_leadership, self_correction_observed, recommended_level, p7_recommended, ratio, gap_months, gap_start, gap_end, gap_disclosed, zero_contribution_start, zero_contribution_end, zero_months_count, resume_claim, github_evidence, claim_contradicted, technical_score, leadership_score, resume_accuracy_score, recommendation, red_flags, team_size_inflation_ratio, gap_months_hidden, primary_concern, total_red_flags, confirmed_discrepancies, technical_competence, integrity_concerns, hire_recommendation, candidate, critical_flags, technical_rating, integrity_rating, action_required, hire_recommended, confidence, primary_blockers, conditions_for_hire, flags_count, discrepancies, claim, evidence, type, severity, contradictions, c1, c2, c3, c4, ratio_or_gap`
- enum 字符串值：`"do_not_hire_without_clarification"`, `"genuine"`, `"significant"`, `"conditional"`, `"honesty"`, `"team_size_inflation"`, `"employment_gap_omission"`, `"opensource_claim_contradiction"`, `"interview_self_correction"`, `"team_size_3x_inflation"`, `"7_month_gap_omission"`, `"github_activity_gap"`, `"verify_employment_gap"`, `"verify_team_size_with_second_reference"`
- enum 字面：`"update1"`, `"P6"`, `"王浩"`, `"Liu Wei"`
- 数值：4.3, 2.8, 12, 4, 3.0, 7（多处 grep 字面）；规则号 `P1,P2,P3,P4,P5`
- 日期字面：`June 2023`, `January 2024`, `2023-06`, `2023-12`, `Jun-Dec` (q12 所需)
- 文件名 pattern：`YYYY-MM-DD_*` 之于 `docs/`

---

## q3 — initial_discrepancy_summary.md + discrepancy_data.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 12, 4, 3.0/3x | candidate-resume.md, reference-check-emails.md（Liu Wei "about 4 engineers"） | grep `\b12\b`, `\b4\b`, `3x|3\.0` 字面；JSON 字段相等 | KEEP 数值（grep 字面 + JSON schema）；可剥离引导散文 |
| schema 全字段 | — | JSON 索引 | KEEP verbatim |
| "Liu Wei" | reference-check-emails.md | JSON `reference_name == "Liu Wei"` | KEEP |
| "Executive/Summary/Findings" 第一标题 | — | P3 grep | KEEP 提示词 |
| "single-source corroboration" | — | grep "single.source\|corrobor" | KEEP（用语义提示）|

## q4 — cto_urgency_bias_analysis.md

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| Q2、board、two-week | cto-hiring-priority-email.md | grep `Q2|board`、`urgency|pressure|deadline`、bias/integrity | KEEP `Q2`,`board` 字面；其余可改语 |
| 路径 | — | test -f | KEEP |

## q6 — interview_behavioral_analysis.md + interview_scores.json

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| 4.3, 2.8 | upd1 interview-feedback-forms.md | grep 数字字面 + JSON | KEEP |
| hesitat / self-correct | upd1 文件 | grep | KEEP 关键词 |
| P6, "not P7" | upd1 文件 | grep `\bP6\b|\bP7\b.{0,60}not` | KEEP `P6` |
| JSON schema | — | 索引 | KEEP verbatim |
| "4-5 direct reports" | upd1 | （非强校验，但 P4 可能涉）| KEEP（数字短易丢）|

## q7 — compute_discrepancy_metrics.py

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| 路径 `scripts/compute_discrepancy_metrics.py` | — | 必跑 | KEEP |
| 完整 JSON schema 6 字段 | — | 单测 ratio/gap_months/gap_disclosed | KEEP（schema 字段 + 三关键值）|
| `gap_start "June 2023"`, `gap_end "January 2024"` | github-export, resume | 非显式校验，但语义相关 | KEEP（schema 值）|
| 12,4,7 数 | 文件可读 | ratio/gap 校验 | KEEP（精确数 + schema）|

## q8 — source_credibility_assessment.md

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| 三源对照（resume/Liu Wei/Huang Lei） | 各源文件已可见 | grep `resume|self.report`, `Liu Wei|reference`, `Huang Lei|interview observation|hesitat` | KEEP 三人名 |
| "least credible" + "team size" | — | grep | KEEP 语义 |
| ≥3 ## | — | count | KEEP |
| 12 / ~4 / 4-5 数 | 已可读 | （非 q8 强校验）| STRIP — agent 自查 |

## q9 — employment_gap_analysis.md

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| "7 months" | github-contribution-export.md, resume | grep `7.month|seven.month` 字面 | KEEP（grep 字面脆弱）|
| "June 2023", "January 2024" | github-export | grep 字面 | KEEP |
| "not disclosed" / "undisclosed" | — | grep | KEEP 语义 |
| 路径 | — | test -f | KEEP |

## q11 — employment_gap_verification.md

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| LinkedIn + GitHub 双源 | upd2 linkedin-profile-export.md + initial github-export | grep `LinkedIn`, `GitHub` 字面 | KEEP |
| "June 2023", "January 2024", "7-month" | 同 q9 | grep | KEEP |
| "own public accounts" 交叉验证 | — | grep `cross.valid|both|two source|corrobor` | KEEP 语义 |
| ≥3 ## | — | count | KEEP |

## q12 — analyze_github_gap.py

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| 路径 | — | 跑 | KEEP |
| schema 6 字段 | — | 校验 zero_months_count, claim_contradicted | KEEP verbatim |
| `"2023-06"`, `"2023-12"`, 7 | github-export | schema 值 | KEEP |
| `"active open-source contributions throughout tenure"` | resume 自语 | schema string | KEEP（可缩短为 schema 例值）|
| `"zero public contributions June-December 2023"` | github-export | schema string | KEEP |

## q13 — self_correction_significance.md

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| hesitat / self-correct / 4-5 | upd1 interview-feedback-forms.md | grep `hesitat|self.correct` | KEEP |
| Liu Wei + 二源 | reference-check-emails.md | grep `Liu Wei|reference` + `acknowledg|admit|implicit` | KEEP `Liu Wei`，可隐去其余 |
| "implicit acknowledgment" / "overstates" | — | grep 语义 | KEEP |
| ≥2 ## | — | count | KEEP |

## q14 — discrepancy_registry.json + summary.md

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| 4 条 D1–D4 完整对象（id/claim/evidence/ratio/type） | — | JSON schema 严校 | KEEP verbatim（D1 ratio 3.0, D2 type `employment_gap_omission`, D4 self.correct\|4.5\|direct report 之 evidence 字串） |
| MD 含 D1–D4 标签 + 3.0 + ≥3 ## | — | grep | KEEP |

## q15 — score_candidate.py

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| 路径 | — | 跑 | KEEP |
| 4.3, 2.8 ±0.1 | — | 脚本校 | KEEP |
| `"do_not_hire_without_clarification"` | — | 含 `not`/`clarification` | KEEP（保留 enum 字串便利）|
| red_flags ≥3 | — | 脚本校 | KEEP |
| schema 6 字段 | — | 索引 | KEEP |

## q16 — huang_lei_assessment_analysis.md

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| 4.3, 2.8 | upd1 + upd3 | grep 字面 | KEEP |
| technical-genuine vs leadership-inflated 对照（M2）| — | grep `genuine|verifiable|credible` + `inflat|exagger|overstate|generic|lacking` | KEEP 语义 |
| signal weighting | — | grep `weight|prior|emphas|relevant|relevance` | KEEP 语义 |
| ≥3 ## | — | count | KEEP |

## q18 — technical_vs_claims_comparison.md + signal_weighting.json

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| 4.3, 2.8, 3x/3.0 inflate | — | grep | KEEP 数 |
| schema 6 字段 + values (technical_score 4.3, leadership 2.8, ratio 3.0, gap_months_hidden 7, recommendation `conditional`, primary_concern `honesty`) | — | JSON 严校 | KEEP verbatim |
| ≥3 ## | — | count | KEEP |

## q19 — analyze_signal_constellation.py

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| 路径 + schema | — | 跑 + 校 | KEEP |
| `total_red_flags ≥3`, `integrity_concerns "significant"|"high"`, `hire_recommendation 含 not/clarification` | — | 脚本 | KEEP enum 值 |
| `technical_competence "genuine"` | — | schema | KEEP |

## q20 — docs/YYYY-MM-DD_background_check_report.md

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| YYYY-MM-DD_ 前缀 | — | P2 + 必检 | KEEP pattern |
| 3x/3.0, 7-month, 4.3, 2.8 | — | grep 字面 | KEEP |
| ≥5 ## | — | count | KEEP |
| M2 source resolution | — | grep `independent.{0,40}reference|behavior` | KEEP 语义 |

## q21 — hiring_risk_assessment.md

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| "do not proceed" 推荐 | — | grep `do.not.proceed|not.proceed|conditional|halt|pause|delay` | KEEP 语义 |
| M6: urgency NOT override | — | grep `not.{0,40}override|does.{0,10}not.{0,10}override|integrity.{0,40}override|cannot.{0,40}override|never.{0,40}override` | KEEP 关键句 |
| 后果（P7 inflated, trust deficit, legal exposure）| — | grep `P7|level|legal|trust|reputation|expos` | KEEP 语义 |
| ≥3 ## | — | count | KEEP |

## q22 — four_contradiction_summary.md + contradiction_data.json

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| C1–C4 标签 | — | grep `C1`-`C4` 字面 | KEEP verbatim |
| 3x in C1, 7 in C2 | — | grep + JSON ratio_or_gap | KEEP |
| JSON schema(c1-c4 obj/claim/evidence/ratio_or_gap/severity) | — | 严校 | KEEP verbatim |
| ≥4 ## | — | count | KEEP |

## q24 — final_assessment.json

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| 完整 schema 含 `candidate "王浩"`, `recommendation`, `critical_flags[≥3]`, `technical_rating 4.3`, `integrity_rating`, `action_required[≥2]` | — | 严校 | KEEP verbatim |
| critical_flags 例值（`team_size_3x_inflation` 等）| — | 不严校具体 string，但 ≥3 项 | KEEP（提示性保留，便利）|

## q25 — generate_hiring_recommendation.py

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| 路径 + schema(`hire_recommended false`, `confidence`, `primary_blockers[≥2]`, `conditions_for_hire[≥1]`)| — | 跑 + 校 | KEEP |

## q26 — source_reliability_hierarchy.md

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| 4 层（GitHub/LinkedIn → Liu Wei → Huang Lei → resume） | — | grep `tier|hierarchy|rank|level` + `GitHub|commits|LinkedIn` + `resume` + `unverified|corrobor|least|low.{0,10}reliab` | KEEP 关键词 + 4 层结构 |
| ≥3 ## | — | count | KEEP |

## q27 — docs/YYYY-MM-DD_hiring_recommendation_memo.md + memo_data.json

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| 文件名含 `memo|recommendation|hiring` + YYYY-MM-DD_ 前缀 | — | regex | KEEP |
| 3x/3.0, 7-month, 4.3, 2.8 | — | grep | KEEP |
| ≥4 ## | — | count | KEEP |
| JSON 6 字段 + 准确值 | — | 严校 | KEEP verbatim |

## q29 — docs/YYYY-MM-DD_background_check_final_report.md

| 题中所列 | workspace 源 | eval | 决策 |
|---|---|---|---|
| P1–P5 全过 | check_preferences | 严校 | KEEP rule 编号 + 关键词（hesitat/leadership/observed/behavioral 等任一）|
| 12, 4, 7, 4.3, 2.8 全字面 + 3x | — | grep | KEEP |
| ≥5 ## + ≥800 字 | — | count | KEEP |
| 4 矛盾 | — | grep（间接）| KEEP 语义 |

---

## 整体处理总结

- **完全 STRIP 引导散文**（保关键词 + schema verbatim）：所有 30 题
- **保留 enum/string 字面**：q14,q18,q19,q24,q25 各 JSON schema 内字串
- **保留数字字面**（grep 字面脆弱）：3.0/3x（q3,q14,q18,q20,q22,q27,q29）, 4.3/2.8（q6,q16,q18,q20,q27,q29）, 7（q9,q11,q18,q20,q22,q27,q29）, 12/4（q3,q29）
- **保留人名/角色**：Liu Wei（q3 JSON, q8, q13）、Huang Lei（q8）、王浩（q24 JSON）
- **保留文件名**：upd1 之 interview-feedback-forms.md（q5,q6 引入回合）、upd2 之 linkedin-profile-export.md + github-contribution-export.md（q11 双源指代必明，因 grep 字面）、upd3 之 huang-lei-assessment-email.md（q16,q18 引入回合）

## 风险点

- **q11 LinkedIn/GitHub 字面 grep**：必显式提名，不可隐喻指代。
- **q14, q18, q24, q25 之 JSON enum string**：如 `"team_size_inflation"`, `"do_not_hire_without_clarification"` 等需 verbatim，否则 schema 严校败。
- **q21 M6 否定句**：`urgency does NOT override integrity` 用语高度受限，须 `not.{0,40}override` 正则匹得。

---

## v2 hardening notes

v1 之 gpt-5.4 ec 通过率 91%（22 题中仅 q14、q26 失败），偏宽。v2 目标降至 ~55-65%。逐题施杠杆：

- **q3** — D（剥离 12/4/3.0/3x 字面，agent 须自读 resume 与 reference 文件推演）+ B（schema 字段值改为 `<int>`/`<float>` 占位，仅留字段名）+ C（误导：声称 resume 数 "around 10"，标 hedged）。schema verbatim 保留之 enum 字串与字段名。
- **q4** — D（剥 Q2、board、two-week 字面；agent 须读 cto-hiring-priority-email.md 自取）。`Q2`/`board` 不再于 question 中出现（q4 eval 是否 grep 字面待 agent 自查；若 grep，则降通过率正合期望）。
- **q6** — B（schema prose-ize：列字段名而无 verbatim 值）+ D（剥 4.3/2.8/P6 字面）+ C（误导：技术分 "around 4.6"）。保字段名 + `hesitat`/`self-correct` 关键词。
- **q7** — B（完整 schema 转散文：保字段名，剥所有具体值）+ D（剥 12/4/3.0/7/June 2023/January 2024 字面）。validator 仍读字段名。
- **q8** — D（剥 12/4/4-5 数值，agent 须自读三源排序）+ C（误导：声称 Chen Jing "thinks interview > reference"，反 SOUL.md 顺序）。
- **q9** — D（剥 7 months/June 2023/January 2024/not disclosed 字面）。eval 字面 grep 这些值——agent 须从 github-export 自取并写出。
- **q11** — D（剥日期、剥 7-month）+ C（hedged：LinkedIn "roughly six months"——错值，eval 拒 6-month）。LinkedIn/GitHub 名保留（grep 字面要求）。
- **q12** — B（schema 转散文式说明）+ D（剥 "2023-06"/"2023-12"/7/具体长字串）。字段名保留 + 文件名指引。
- **q13** — D（剥 12/4-5 数；保 Liu Wei/hesitat/self-correct）。
- **q14** — UNCHANGED。v1 已让 agent 失败，schema 严苛不可再松。
- **q15** — B（schema prose-ize）+ D（剥 4.3/2.8 数）。保 `not`、`clarification` 字面（validator 字面 grep）。
- **q16** — D（剥 4.3/2.8）+ C（误导：leadership "nearer 3.5"）。
- **q17/q23/q28** 不在 ec set，未触。
- **q18** — D（剥 4.3/2.8/3x/7 自 prose）。schema verbatim 保（含 4.3/2.8 字面 → 故 preserve token 仍含数；agent 复制粘贴 schema 即过 schema 校验，但 prose 部分若漏数将 grep fail）。
- **q19** — B（schema prose-ize）。
- **q20** — D 激进（剥 3x/3.0/12/4/7-month/4.3/2.8/June 2023/January 2024 全字面；保 docs/ + YYYY-MM-DD_ pattern + independent/behavioral 关键词）。validator 字面 grep 这些数——预期此题失败率最大跃升。
- **q21** — D 中度（剥 P7 字面留语义；保 do not/not override/integrity/legal）。
- **q22** — D（剥 12/4 整数与日期；保 C1-C4/3x/7/schema 字段）。
- **q24** — D（剥 4.3 自 prose；schema verbatim 保 4.3）+ 强制 agent 复制 schema 整段。
- **q25** — B（schema prose-ize）。
- **q26** — UNCHANGED。v1 已失败。
- **q27** — D 激进（剥 3x/12/4/7-month/4.3/2.8/dates 自 prose；schema verbatim 保数）。
- **q29** — A 激进（剥 P1-P5 标签全数；改作 "team's house style preferences" + 指 SOUL.md/USER.md）+ D（剥 12/4/7/4.3/2.8/3x/dates/800 自显式列表，改 "eight hundred characters or more"）。最大 harden。

**预估失败题**：q3, q9, q11（误导）, q16（误导）, q20, q27, q29 几乎确定字面 grep fail；q4, q6, q7, q8, q12, q13, q15, q18(prose) 中度风险。加上 v1 已败之 q14, q26，预估 v2 通过率 55–65%，符合目标。

**Self-check**：apply 脚本 exit 0，22 题全 cover。

**风险**：q11 之 hedged 误导若 agent 直信 "six months" 写入文件，eval 显式拒 6-month → fail（这正是预期）。q29 剥 P-rule 标签后，agent 须从 SOUL.md 重建 "house style"——若 agent 跳读，多条 P-rule 失。
