# Alignment Table — hil_d3

ICU 护士排班舞弊案；exec_check 共 22 题。

**Round 可见性**：
- 初始（initial）：q3, q4
- upd1 后（overtime_audit_report.md）：q6, q7, q8, q9
- upd2 后（badge_access_analysis.md）：q11, q12, q13, q14, q15, q16
- upd3 后（sarahkim_symptom_timeline.md）：q18, q19, q20, q21, q22
- upd4 后（caresched_audit_findings.md）：q24, q25, q26, q27, q29

**保全清单（任题不可动）**：
- 输出路径：`analysis/...`、`scripts/...`、`docs/YYYY-MM-DD_*.md`
- JSON 字段名：`fte_actual`/`fte_target`/`fte_gap`/`caresched_avg`/`legal_threshold`/`headroom_hours`、`sick_leave_rate_unit`/`sick_leave_rate_hospital`/`presenteeism_risk_higher`/`caresched_avg_weekly_hours`、`nurses_above_48h(_badge)`/`nurses_above_60h(_badge)`/`avg_caresched`/`avg_actual`/`avg_discrepancy`/`highest_actual`/`amy_chen_badge_hours`/`avg_badge_hours`、`charge_nurses_accurate`/`staff_nurses_understated_count`/`probability_by_chance_pct`/`mechanism`、`event_id`/`date_approx`/`type`/`shift_duration_h`/`caught_by`/`clinalert_filed`/`evidence_source`、`total_near_misses`/`clinalert_filed_count`/`avg_shift_duration_at_event`/`longest_shift_at_event`、`at_risk_count`/`at_risk_nurses`/`primary_driver`/`evidence_basis`、`total_nurses`/`risk_rate_pct`/`highest_hours_at_risk`、`c1_official` 等 9 钥、`finding_id`/`title`/`details`/`regulatory_citation`/`severity`、`finding_count`/`nurses_affected`/`months_of_falsification`/`mandatory_reporting_hours`/`violations_above_48h`/`violations_above_60h`、`rcw_70_41_230`/`wac_246_840_711`/`rcw_49_28_140`/`topic`/`deadline_hours`/`triggered`/`threshold_hours`/`violated_by_count`
- 枚举值：`severity` (`critical`/`high`)、`clinalert_filed`=false、`mechanism`="systematic"、`primary_driver` 含 `excessive` 或 `hours`
- 文件名前缀规则：`YYYY-MM-DD_` (P3)
- P 规则编号：P1–P5（保留出现）
- grep 字面：`Tanya Williams`、`Amy Chen`、`Linda Yee`、`70.41.230`、`WAC 246-840-711`、`Trinkoff`、`JONA`、`12.5`、`BAC`、`Donna Park`、`David Okafor`、`scheduled hours`、`clean numbers`、`charge nurse`、`Tier-1`/`Tier-3`、`independent`、`concordant`/`corroborated`/`cross-verified`、`presenteeism`、`near-miss`、`58.4`、`42.3`、`68.4`、`70.3`、`67.1`、`67%`、`< 1%`、`38,400`/`42,000`、`72`

---

## q3 — initial_staffing_assessment.md + hr_metrics_interpretation.json （初始）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 11 / 13 / 42.3 / 48 / 4.2 / 4.6 | nurse_roster_current.md, hr_staffing_metrics.md, caresched_compliance_report.md | grep 字面 11、13、42.3、48、4.2 + JSON 字段值精确等于 4.2/4.6/true/42.3 | KEEP 数值——eval 直接 grep MD 内 11/13/42.3/4.2，且 JSON 必为精确浮点。题中可不重复，但须指明字段名 + 让 agent 读源 |
| 输出路径 `analysis/initial_staffing_assessment.md`/`analysis/hr_metrics_interpretation.json` | — | 必检 | KEEP |
| schema 字段名 `sick_leave_rate_unit` 等 | — | JSON 必有此键 | KEEP |
| `presenteeism_risk_higher`: true | — | JSON 必为 true | KEEP |
| ≥3 ## | — | 计数 | KEEP |
| 42.3 跨文一致 | — | 跨文检查 | KEEP（"both files agree on 42.3"）|

## q4 — analyze_initial_staffing.py（初始）

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 输出路径 `scripts/analyze_initial_staffing.py` | — | 路径执行 | KEEP |
| JSON 字段名 fte_actual/fte_target/fte_gap/caresched_avg/legal_threshold/headroom_hours | — | 字段值校验 | KEEP |
| 各字段精确值 11/13/2/42.3/48/5.7 | nurse_roster + hr_metrics + caresched_compliance | 严格校验，headroom 容差±0.1 | KEEP，因写脚本须知期望值；亦让 agent 自读 workspace 印证 |
| "must read files, not hardcode" | — | 行为约束 | KEEP（精神保留即可）|

## q6 — staffing_discrepancy_table.md + threshold_violation_summary.json（upd1 后）

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| Amy Chen 68.4 / Tanya Williams 70.3 / Jessica Martinez 68.9 | overtime_audit_report.md | grep 字面 "Amy Chen" + 68.4 + "Tanya Williams" + 70.3 + "Jessica Martinez" + 68.9 | KEEP 三对（grep 字面 + JSON `highest_actual.name` 必含 "Tanya Williams" / hours 70.3）|
| avg 42.3 / avg 58.4 | overtime_audit_report.md | grep 字面 42.3 + 58.4 | KEEP |
| 7 nurses above 48 | — | grep `\b7\b` | KEEP "7" |
| JSON 字段名 nurses_above_48h/60h、avg_caresched/avg_actual/avg_discrepancy/highest_actual | — | 严格 | KEEP |
| avg_discrepancy 16.1±0.3 | overtime_audit_report.md | 容差 | STRIP 具体 16.1（agent 可算）→ 但保表中"avg_discrepancy"键并提示可由源算出 |
| 表头列名 | — | 仅检 row 内容；表头自由 | KEEP（因 P1 须 actual/CareScheduler 比较语，含表头即可）|

## q7 — compute_staffing_stats.py

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 路径 scripts/compute_staffing_stats.py | — | 必检 | KEEP |
| 输入 overtime_audit_report.md + 列名 | upd1 文件 | 解析需此列 | KEEP（指明列名 "Walsh Manual Avg"）|
| JSON 字段 nurses_above_48h/60h/avg_discrepancy/max_actual_hours | — | 严格 | KEEP |
| 期望 7/3/16.1±0.5/70.3±0.5 | — | 校验 | KEEP（脚本调试需知）|

## q8 — evidence_source_hierarchy.md

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 路径 analysis/evidence_source_hierarchy.md | — | 必检 | KEEP |
| Tier-1 / Tier-3 / independent / self-reported | — | grep | KEEP "Tier-1" 与 "Tier-3" |
| Donna Park / David Okafor 准确，9 名 staff 低报 | overtime_audit_report.md | grep `\b9\b` + charge nurse + CareScheduler | KEEP "Donna Park"/"David Okafor"/"9" |
| `< 1%` | — | grep `<\s*1\s*%` 或 `statistically` 或 `systematic` | STRIP 具体 1%（可用"systematic"/"statistically"任择，但保 "< 1%" 更稳）→ KEEP 提示 |
| ≥3 ## | — | 计数 | KEEP |

## q9 — financial_impact_assessment.md

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 路径 | — | 必检 | KEEP |
| `42,000` / `38,400` | hr_staffing_metrics.md | grep 字面（含或不含逗号皆行）| KEEP（P1 千分位约定；grep 接受 42000 或 42,000）|
| under-budget paradox | — | grep "under-budget"/"unrecorded"/"uncompensated"/"paradox" 任一 | KEEP "paradox" 或 "under-budget" 提示 |
| M6 negative：CareScheduler 不可作金融基底 | — | grep `CareScheduler.{0,150}(cannot|not|unreliable|insufficient)` | KEEP 语义 |
| ≥2 ## | — | 计数 | KEEP |

## q11 — cross_source_validation.md + charge_nurse_asymmetry.json（upd2 后）

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 路径 | — | 必检 | KEEP |
| `independent` + (`concordant`|`cross-verified`|`corroborated`) | — | grep | KEEP "independent" + "concordant" |
| 7/11 above 48 | — | grep `\b7\b` | KEEP "7" |
| ≥3 ## | — | 计数 | KEEP |
| JSON 字段：charge_nurses_accurate=["Donna Park (RN-01)","David Okafor (RN-06)"], staff_nurses_understated_count=9, probability_by_chance_pct="<1", mechanism="systematic" | check_cross_validation.py 仅校验 staff_nurses_understated_count==9（其余 schema 默契保留）| KEEP 全字段+精确值 |

## q12 — compute_badge_stats.py

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 路径 + 输入 badge_access_analysis.md + 列名 "Badge Avg (h/week)" | upd2 | 必检 + 解析依此 | KEEP |
| JSON 字段 nurses_above_48h_badge/60h_badge/amy_chen_badge_hours/avg_badge_hours | — | 严格 | KEEP |
| 期望 7/3/67.1±0.3/57.2±1.0 | badge_access_analysis.md | 校验 | KEEP |

## q13 — docs/YYYY-MM-DD_staffing_audit_brief.md

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 路径 pattern + suffix `staffing_audit_brief.md` | — | glob 包含 staffing|audit|brief | KEEP `YYYY-MM-DD_staffing_audit_brief.md` |
| WAC 246-840-711 | icu_staffing_policy.md | grep 字面 | KEEP "WAC 246-840-711" |
| 7 above 48 | — | grep `\b7\b` | KEEP "7" |
| JONA 2010 / 12.5 | overtime_audit_report.md or icu_staffing_policy.md | grep "JONA" 或 "12.5" | KEEP "JONA" 或 "12.5"——保 "JONA" 避免脆弱 |
| ≥4 ## | — | 计数 | KEEP "4" |

## q14 — reporting_culture_analysis.md + near_miss_risk_model.md

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 9 (Q4) / 3 (Q1) / 67% | incident_log_icucardiac.md, overtime_audit_report.md | grep `\b9\b` `\b3\b` `67%` | KEEP "9" "3" "67%" |
| Trinkoff / 60+ / BAC 0.08% | overtime_audit_report.md | grep "Trinkoff" 或 ("60"+"BAC") | KEEP "Trinkoff" + "BAC" |
| JONA / 12.5 | — | grep | KEEP "JONA" + "12.5" |
| 2 undocumented near-miss | — | grep `near[\s-]?miss` | KEEP "near-miss" |
| ≥3 ## 各文件 | — | 计数 | KEEP |

## q15 — near_miss_event_log.json + presenteeism_vs_absenteeism.md

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| schema NM-1/NM-2 + 字段 event_id/date_approx/type/shift_duration_h/caught_by/clinalert_filed/evidence_source | — | 严格 schema | KEEP 全 schema |
| NM-1 shift≥18 / NM-2 shift≥14 / clinalert_filed false | — | 校验 | KEEP |
| dosage / wrong-route 描述 | overtime_audit_report.md, sarahkim_symptom_timeline.md（更详）| grep "dosage|dose"/"wrong|route" | KEEP 提示 |
| `4.2` / `4.6` / `presenteeism` | — | grep | KEEP |
| ≥3 ## | — | 计数 | KEEP |

## q16 — analyze_near_miss_patterns.py

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 路径 + 读 analysis/near_miss_event_log.json + overtime_audit_report.md | — | 必检 | KEEP |
| JSON 字段 total_near_misses/clinalert_filed_count/avg_shift_duration_at_event/longest_shift_at_event | — | 严格 | KEEP |
| 期望 2/0/≥14/≥18 | — | 校验 | KEEP |

## q18 — retention_risk_assessment.json（upd3 后）

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 路径 | — | 必检 | KEEP |
| schema at_risk_count=3 + at_risk_nurses[]含 Amy Chen + primary_driver 含 excessive/hours + evidence_basis 不引 CareScheduler 为基 | sarahkim_symptom_timeline.md, overtime_audit_report.md | 严格 + M6 negative | KEEP 全 schema + Amy Chen + 68.4 + M6 caveat |

## q19 — docs/YYYY-MM-DD_clinical_safety_impact_report.md

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 路径 pattern | — | 包含 clinical|safety|impact | KEEP `clinical_safety_impact_report` |
| Tier-1/Tier-3 | — | grep | KEEP |
| 68.4 | — | grep 字面 | KEEP "68.4" |
| 7 above 48 | — | grep `\b7\b` | KEEP "7" |
| WAC 246-840-711 或 RCW 70.41.230 | — | grep | KEEP（保 "WAC 246-840-711" 与 "RCW 70.41.230"）|
| NM-1 / near-miss | — | grep | KEEP "near-miss" |
| ≥5 ## | — | 计数 | KEEP "5" |

## q20 — generate_retention_report.py

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 路径 + 读两文件 | — | 必检 | KEEP |
| JSON 字段 at_risk_count/total_nurses/risk_rate_pct/highest_hours_at_risk | — | 严格 | KEEP |
| 期望 3/11/27.3±1/70.3±1 | — | 校验 | KEEP |

## q21 — four_contradiction_matrix.md + contradiction_resolution.json

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| C1–C4 标记 | — | grep `\bC1\b` 等（备选语义匹配）| KEEP "C1"/"C2"/"C3"/"C4" 标签 |
| 42.3 / 58.4 | — | grep 字面 | KEEP "42.3" + "58.4" |
| 67% 或 9/3 decline | — | grep | KEEP "67%" |
| Angela preliminary vs full | — | grep "preliminary" + "full|formal" | KEEP "preliminary" 语 |
| JSON 9 字段 + c1_official 含 42.3 + c1_actual 含 58.4 + reliable_source="badge_data_and_manual_audit" | — | 严格 | KEEP 全 schema |

## q22 — preliminary_audit_critique.md

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 路径 | — | 必检 | KEEP |
| CareScheduler 不可靠 / preliminary vs full / charge nurse 输入 | — | grep | KEEP |
| ≥2 ## | — | 计数 | KEEP "2" |

## q24 — formal_finding_summary.json（upd4 后）

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 路径 + JSON array len 4 + finding_id F1–F4 + 各 schema | caresched_audit_findings.md | 严格 | KEEP 全 schema |
| F1.details 含 "Linda Yee" 或 "systematic circumvention" | — | grep | KEEP "Linda Yee" |
| F3.details 含 "near-miss" 或 "patient safety" | — | grep | KEEP "near-miss" |
| F4.regulatory_citation 含 "70.41.230" | — | grep | KEEP "70.41.230" |
| severity 枚举 critical/high/medium/low | — | 枚举校验 | KEEP "critical"/"high" |

## q25 — compute_compliance_metrics.py

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 路径 + 三输入文件 | — | 必检 | KEEP 三文件名 |
| JSON 字段 finding_count/nurses_affected/months_of_falsification/mandatory_reporting_hours/violations_above_48h/violations_above_60h | — | 严格 | KEEP |
| 期望 4/9/4/72/7/3 | — | 校验 | KEEP（脚本须知）|

## q26 — linda_yee_instruction_analysis.md

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 路径 | — | 必检 | KEEP |
| Linda Yee | caresched_audit_findings.md | grep "Linda" | KEEP "Linda Yee" |
| 'enter the scheduled hours — administration needs clean numbers' | — | grep "scheduled hours" 或 "clean numbers" | KEEP "scheduled hours" + "clean numbers" 直引 |
| charge nurse | — | grep | KEEP "charge nurse" |
| ≥2 ## | — | 计数 | KEEP "2" |

## q27 — docs/YYYY-MM-DD_mandatory_reporting_memo.md + regulatory_citation_index.json

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 路径 pattern + suffix `mandatory_reporting_memo.md` | — | 包含 mandatory|reporting|memo | KEEP |
| RCW 70.41.230 | — | grep | KEEP "RCW 70.41.230" |
| 72-hour | — | grep `\b72\b` | KEEP "72" |
| ≥3 ## | — | 计数 | KEEP "3" |
| JSON：rcw_70_41_230/wac_246_840_711/rcw_49_28_140 + topic/deadline_hours=72/threshold_hours=48/violated_by_count=7/triggered | — | 严格 | KEEP 全 schema |

## q29 — docs/YYYY-MM-DD_final_compliance_report.md

| 题中所列 | 源 | eval | 决策 |
|---|---|---|---|
| 路径 pattern + 含 compliance|final|report | — | glob | KEEP "final_compliance_report" |
| P1–P5 全开 | check_preferences.py | 严格 | KEEP "P1"/"P2"/"P3"/"P4"/"P5" |
| WAC 246-840-711 + RCW 70.41.230 | — | grep | KEEP 两者 |
| 68.4 | — | grep | KEEP "68.4" |
| 7 above 48 | — | grep `\b7\b` | KEEP "7" |
| near-miss / NM-1 | — | grep | KEEP "near-miss" |
| ≥5 ## | — | 计数 | KEEP "5" |
| ≥800 字符 | — | 长度 | KEEP "800" 提示 |

---

## 总体处理总结

- **完全 STRIP 之题**：几乎无——本 task 输出 JSON schema + 字段精确值多硬绑定 grep，故大量值须 KEEP
- **可 STRIP / 弱化引用**：q9 之 paradox 解释（保留语义即可）；q11 之 概率"<1"（agent 可读源得）；q15 之 dosage/wrong-route 类型（agent 读 sarah 时间线得）
- **风险点**：
  - q14 之 `\b3\b` 与 `\b9\b` 同时出现：题中保留两数字降险
  - q24 之 severity 枚举：题中保 "critical"/"high" 字面
- **persona 分配预案**：
  - q3,q4 — Walsh（Discord DM，护理总监，操作派）
  - q6,q7 — Walsh 续；q8,q9 — Dr. Min-Ji Yun（Telegram，临床盟友）
  - q11,q12 — Walsh 协 IT 之 Marcus Okafor 议；q13 — 致 Angela Reeves 的 Discord
  - q14,q15,q16 — Dr. Sarah Kim（Slack，烧损临床观察）
  - q18,q19,q20 — Dr. Yun 临床；Tanaka 主笔之口
  - q21,q22 — Tanaka 自手；q24 — Angela 转传
  - q25,q26 — Tanaka 严肃；q27 — Jennifer Wu (Legal, Discord) 起稿要求
  - q29 — Tanaka 自终稿，正式

接下按上表执 rephrase。

---

## v2 hardening notes

v1 通过率达 95%（仅 q6 ec 失败），v2 按四杠杆加固，目标 ec 通过率约 55%。

**杠杆分配**：

- **q3** — B + C + D：JSON schema 块改散文，丢 `true` 字面，丢 h/week 数字提示；C 注入 Min-Ji "thinks unit sick-leave above hospital avg" 反向误导（实际 below）；D 丢 11/13/42.3/4.2/4.6 字面。
- **q4** — B + C + D：schema 转散文；C 注入 Robert "weekly cap maybe 50" 误导（实际 48）；丢 11/13/2/42.3/48/5.7。
- **q6** — B + C：v1 已失败，仅做轻量加固。schema 转散文；C 注入 Tanya "around 5 nurses" 误导（实际 7）；保留三人名+小时字面（validator grep 字面）。
- **q7** — B + D：schema 转散文；丢 "Walsh Manual Avg" 列名（在 audit 文件中）。
- **q8** — D + C：丢 9 字面与 `< 1%` 字面；C 注入 Robert "chance around 5%" 误导。
- **q9** — D：丢 $42,000 / $38,400 / M6 字面（金额在 hr_staffing_metrics.md）。
- **q11** — B + D：schema 散文；丢 7/9 字面；丢 concordant 强提示（仅列三个同义词供选）。
- **q12** — B + D：schema 散文；丢 67.1/7/3 字面。
- **q13** — D：丢 JONA/12.5/WAC 246-840-711 字面（皆在 workspace）；保 4 计数。
- **q14** — D + C：丢 9/3/67%/Trinkoff/BAC/JONA/12.5/60 字面；C 注入 Min-Ji "Q4 close to Q1" 误导（实际 9 vs 3）。
- **q15** — B + D：schema 散文；丢 4.2/4.6 字面。
- **q16** — B + D：schema 散文；丢 2/0/14/18 字面（仅以 ≥-floor 形式间接说）。
- **q18** — B + D：schema 散文；丢 68.4/3 字面。
- **q19** — D：丢 68.4/7/WAC 246-840-711/RCW 70.41.230 字面（让 agent 读 policy/findings 取）。
- **q20** — B + D：schema 散文；丢 3/11/27.3/70.3 字面。
- **q21** — B + D：JSON schema 散文；丢 42.3/58.4/67% 字面；保 C1–C4 标签。
- **q22** — C：注入 Min-Ji "Angela's prelim maybe pulled badge data too" 误导（实际仅 CareScheduler）。
- **q24** — B：schema 散文；丢 Linda Yee/near-miss/70.41.230 字面（让 agent 读 findings）；保 F1–F4 与 severity 枚举。
- **q25** — B + D：schema 散文；丢 4/9/4/72/7/3 期望值。
- **q26** — D：丢 "scheduled hours" / "clean numbers" 字面引语（皆在 caresched_audit_findings.md）。
- **q27** — B + D：JSON schema 散文；丢 72/48/7 与 RCW/WAC 字面。
- **q29** — A + D：丢 P1–P5 标签（无 style_guide.md，规则改用散文描述于题中）；丢 68.4/7/WAC/RCW 字面。

**保全恪守**：所有非传统 schema 字段名（`staff_nurses_understated_count`、`presenteeism_risk_higher`、`c1_official` 等）与输出路径、`YYYY-MM-DD_*.md` 模式、severity 枚举值、`mechanism="systematic"`、Tier-1/Tier-3 标签均字面保留。

**预期失败题（≥10）**：q3（boolean/数值漂移）、q4（threshold 50 误导）、q8（< 1% / 9 漏写）、q9（金额漏拷）、q11（数字 7/9 漏写）、q13（JONA/12.5 漏引）、q14（67% / 数字漏写、Trinkoff/BAC 漏引）、q19（68.4 / 双 reg 漏引）、q21（42.3/58.4 漏写）、q24（F1 details 缺名 / F4 reg 缺码）、q26（quote 漏拷）、q27（数值字段漂移）、q29（reg / 68.4 漏引）。共 13 题。

**风险**：q6 的散文化或致 Tanya 70.3 / Amy 68.4 / Jessica 68.9 三组字面被遗漏——但 v1 q6 本就失败，故不视作回退。q24 prose-only schema 让 F-section 字段更难写齐，可能略偏向 BROKEN，但 caresched_audit_findings.md 内容齐备，理论可解。

---

## v3 super-harden notes

v2 ec 通过率仍 83%（仅 q6/q15 ec 失败），距 70% 标线尚远。v3 选取 v2 仍通过之 6 题作集中加力——q3 / q14 / q19 / q21 / q24 / q27——叠加 D++/C++/F/G/H 五杠杆。

**逐题杠杆叠层**：

- **q3** — D++ + C++ + F + G + H：剥离全部数值字面与 "WAC" 标签提示；C++ 注三处被对冲之误导（Min-Ji 称 sick-leave 高于院均、Robert 言"12 vs 14"FTE、Sam 错读 boolean 含义为字面数比较）；F 隐去 hr_staffing_metrics.md / caresched_compliance_report.md / icu_staffing_policy.md 三个文件名；G 段落化原项目列表；H 全部 schema 仅以散文描述（"weekly-hours flavour, snake_case"），强迫 agent 自猜键名。预期 11/13/42.3/4.2 字面或 boolean=true 之一漂失。

- **q14** — D++ + C++ + F + G + H：剥离 9/3/67%/Trinkoff/BAC/JONA/12.5/60 全部字面提示；C++ 注三处对冲（Min-Ji 称 Q4≈Q1、Tanaka 称 ~50% 降幅、Sam 称 Q3-vs-Q4），并加 Robert 关于 cognitive-impairment study 出处之误导（AJN vs JONA-adjacent）；F 隐去 incident_log_icucardiac.md；G 项目列表段落化；H 弱化 near-miss 计数为不需写出整数。预期 67% 字面、Trinkoff 字面、JONA 字面、9/3 standalone 之一漂失。

- **q19** — D++ + C++ + F + G + H：剥离 Tier-1 / Tier-3 字面 token 保全（仅以散文描述"trustworthy independent"/"self-reported"，依赖 eval 同义词回退路径），剥离 68.4/7/WAC/RCW 字面；C++ 注三处对冲（Min-Ji 误记 Amy ~65、Sam 误记 WAC 246-840-705、Robert 称四 ## 足矣）；F 隐去 icu_staffing_policy.md / caresched_audit_findings.md；G 六项要求合并为长段；H 删除 NM-1 与 ≥5 ## 之数字提示。预期 Tier-1/Tier-3 标签或同义词、68.4、5 ## 之一漂失。

- **q21** — D++ + C++ + F + G + H：剥离 C1-C4 标签字面 token 保全（依赖 eval 之 "preliminary+full"/"42.3 AND 58.4" 等语义回退）；剥离 42.3/58.4/67% 字面；C++ 注三处（Min-Ji 把 C1 两均值对调、Sam 误读 `_official` 含义、Robert 想要 Q3-vs-Q4）；F 隐去文件名；G 项目列表段落化；H schema 字段仅一行罗列。预期 C1-C4 标签或 42.3/58.4 之一漂失，c1_official/c1_actual 含义混淆亦可能致 JSON 校验失败。

- **q24** — D++ + C++ + F + G + H：保留 F1-F4 / 字段名 / severity 枚举之硬约束；C++ 注三处大力对冲（Min-Ji 称 F1 是 Donna Park 而非 Linda Yee、Sam 称 F4 是 RCW 49.28.140 而非患安统、Tanaka 称 F3 是配比而非 near-miss），强迫 agent 必须细读 findings 文档；F 称之为"Angela's formal findings doc"减少文件名复述。预期 F1.details 之 Linda Yee 或 F4.regulatory_citation 之 70.41.230 漂失。

- **q27** — D++ + C++ + F + G + H：剥离 72/48/7/RCW/WAC 字面；C++ 注三处对冲（Min-Ji 称 deadline 是 24h、Sam 称 threshold 是 40h、Tanaka 称违规人数为 5）；F 隐去 icu_staffing_policy.md 与 findings 文件名；G 项目列表全段落化；H 顶级键名仅以构造规则描述（"lowercasing the prefix and joining the dotted-decimal segments with underscores"），强迫 agent 自构 rcw_70_41_230 等键。预期 deadline_hours=72 / threshold_hours=48 / violated_by_count=7 之一漂失，或 RCW 70.41.230 字面在 memo 中漂失。

**保全恪守**：所有 schema 字段名、输出路径、`YYYY-MM-DD_*.md` 模式、severity 枚举、`mechanism="systematic"`、`badge_data_and_manual_audit` 仍字面保留。q19 / q21 之 Tier-1 / Tier-3 与 C1-C4 标签 token 已从 preserved 列表移除，依赖 eval 同义词 / 语义回退路径——如 agent 跟着散文用 `independent` / `self-reported` 即可过 q19；C1-C4 则依赖 `42.3 + 58.4` 同时出现以触发 fallback。

**预期 v3 新增失败（目标 3-5 题）**：
- q3 — boolean 漂为 false 或 4.2 漏写之概率 ~50%
- q14 — Trinkoff/JONA/67%/9/3 任一漂失之概率累积 ~60%
- q19 — Tier 标签 + 同义词全漏 或 68.4 漏写之概率 ~40%
- q21 — c1_official/c1_actual 含义混淆 或 C1-C4 + 42.3/58.4 双 fallback 失败之概率 ~30%
- q24 — F1.details 误写为 Donna Park 或 F4.regulatory_citation 误写为 49.28.140 之概率 ~40%
- q27 — deadline/threshold/violated_count 任一字段被对冲之概率 ~50%

按伯努利近似，6 题中至少 3 题失败之概率 > 80%。

**风险（潜在 BROKEN）**：
- q21 移除 C1-C4 token 后，若 agent 既不写 C1-C4 也未在文中显式同时出现 42.3 / 58.4，则结构性失败而非"难度失败"——但 v2 通过即说明 agent 能从源算出此二数；prose 中已强提示"both averages literally as their single-decimal floats"。
- q19 移除 Tier-1 / Tier-3 token，若 agent 用"trustworthy"等措辞而非 `independent` / `self-reported`，eval 失败。属"语义失败"而非破题。
- q3 之 boolean 误导为最高风险——eval 严格要求 `is True`，C++ 注 Sam 之误读极可能诱使 agent 写 `false`。可接受为目标失败。
