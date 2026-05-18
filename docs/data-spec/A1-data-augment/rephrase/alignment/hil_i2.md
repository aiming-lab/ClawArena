# Alignment Table — hil_i2

`exec_check` 题之 question-workspace-eval 三角对齐分析。林怡（ER 主治医师）应对匿名学术不端投诉，AI 助手协作。

**Round 可见性**：
- initial（q1–q4 visible）：paper-dataset-summary.md、raw-case-database-export.md、co-author-data-version.md、anonymous-complaint-letter.md、message_logs/wangyisheng_im.md（W1D1-D2）、USER.md
- upd1（q5+ 起）：data-cleaning-pipeline-log.md（V2.0/V2.1 详细审计）
- upd2（q10+ 起）：wang-yisheng-statement-shift.md、upd2_sessions/wangyisheng_im.md（W1D3 转向）
- upd3（q17+ 起）：zhangzhuren-guidance.md、upd3_sessions/zhangzhuren_im.md
- upd4（q23+ 起）：ethics-timeline-verification.md、upd4_sessions/committee_email.md

**保全清单（任题不可动）**：
- 输出路径：`analysis/<...>.json|md`、`docs/YYYY-MM-DD_*.md`、`scripts/<...>.py`
- IRB 号 `#BFH-2025-IRB-0342`（多题 grep "BFH-2025-IRB-0342" 字面）
- 关键日期 `2025-09-20`（V2.0）、`2025-10-15`（V2.1）、`2025-08-01`（IRB）、`2025-09-15`（提取）、`2025-11-01`（投稿）、`2025-07-15`（HIS 迁移）—— 部分题字面 grep
- 数字 `912`、`847`、`65`、`23`、`4`（被字面 grep word-boundary）
- pipeline 版本号 `V2.0`、`V2.1`
- 中文姓名 `王逸生`、`林依`、`张主任`、`zhangzhuren`
- JSON 字段名（schema）—— 全部 verbatim
- 枚举值/常量字符串：`HIS_migration_duplicates`、`no_selective_exclusion`、`responded`、`confirmed`、`acknowledged_not_misconduct`、`committee_clarification`、`misconduct_not_supported`、`HIS_migration_dedup`
- P1–P5 规则编号（被 check_preferences 验）

---

## q3 — n_discrepancy_preliminary.md + research_timeline.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `912/847/65` | paper-dataset-summary.md + raw-case-database-export.md | grep `\b912\b` `\b847\b` `\b65\b` | STRIP（agent 读两文件即得）|
| 各日期 | 同上 | json 字段 `irb_date == "2025-08-01"` etc. | KEEP schema 字段名 verbatim；STRIP 题中冗余复述 |
| `#BFH-2025-IRB-0342` | paper-dataset-summary.md | json `irb_number` contains 'BFH-2025-IRB-0342' | KEEP（schema 中 verbatim）|
| Problem/Assessment/Plan 结构、≥3 ## headings | — | check_q3 + P1/P3 | KEEP（"##"/"Problem"/"Assessment"/"Plan"）|
| HIS / migration | raw-case-database-export.md | grep 'HIS\|migration' | STRIP（agent 自读）|

## q4 — verify_irb_timeline.py

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 `scripts/verify_irb_timeline.py` | — | cd workspace && python scripts/verify_irb_timeline.py | KEEP |
| IRB 行字面 `| 伦理审批 | 2025-08-01, ..., #BFH-2025-IRB-0342 |` | paper-dataset-summary.md L16 | grep BFH | STRIP 重复列举（让 agent 读源文件）|
| `2025-09-15` 提取日 | raw-case-database-export.md / paper-dataset-summary.md | days_difference > 0 | STRIP |
| JSON output schema 字段 | — | shell pipeline 校验 | KEEP（字段名 verbatim）|

## q6 — deduplication_verification.json（schema 严格）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 全 schema 字段 + enum | data-cleaning-pipeline-log.md | check_q6 严格匹配 `total_raw==912` `excluded_count==65` `pipeline_author=='王逸生'` `pipeline_date=='2025-09-20'` `exclusion_cause=='HIS_migration_duplicates'` etc. | KEEP 整 schema verbatim（含枚举值串），措辞改为人话；STRIP "<float>" 这类细节描述 |

## q7 — compute_exclusion_stats.py

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 输出 schema | — | shell `total_raw==912 excluded_count==65 clinical_diffs_in_excluded==0` | KEEP（schema verbatim）|
| Parsing guidance | data-cleaning-pipeline-log.md | — | STRIP（让 agent 自看）|
| `HIS_migration_duplicate` 枚举 | — | 题面建议；非硬检 | KEEP-LITERAL（保此串以稳）|

## q8 — pipeline_authorship_analysis.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `V2.0`/`王逸生`/`2025-09-20` | data-cleaning-pipeline-log.md | grep V2.0+王逸生 同段；V2.1+林依 | KEEP 这几词；STRIP 日期重复 |
| `V2.1`/`林依`/`2025-10-15` | 同上 | grep | KEEP V2.1+林依 |
| `field rename` 或 `minor` | — | grep `field\s+rename\|minor` | KEEP-LITERAL（一选其一）|
| ≥3 ## headings | — | check_q8 | KEEP |

## q9 — co_author_discrepancy.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `847`/`912`/`23` 三数 | co-author-data-version.md + raw-case-database-export.md + paper-dataset-summary.md | grep `\b847\b` `\b912\b` `\b23\b` | KEEP-LITERAL（务必题中明示三数标准独立形）|
| REC-NEW-* / REC-OLD-* 区分逻辑 | raw-case-database-export.md 重复记录示例 | check_q9 检测 `keep_old.*new` 之类语义 | STRIP 实现细节；保"两版本同 N、ID 选取不同"语义即可 |
| V2.1 authoritative | — | grep `V2\.1.*authoritative\|V2\.1.*standard\|published.*V2\.1\|V2\.1.*correct` | KEEP "V2.1" 词根 + authoritative/published 语义 |

## q11 — coauthor_behavior_analysis.md + contradiction_registry.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `王逸生` | upd2 文件 | grep 王逸生 | KEEP |
| co-sign / distanced 语义 | wang-yisheng-statement-shift.md | grep | KEEP-LITERAL "co-sign\|co-author" 之一 + "distanc" 之一（题文中明示之）|
| contemporaneous/pre-complaint contrast | — | grep | KEEP "pre-complaint" 或 "contemporaneous" |
| JSON c1/c2/c3 schema | — | check_q11 schema | KEEP 字段名 c1/c2/c3 + claim/evidence/resolved_by |

## q12 — analyze_timeline_consistency.py

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 三文件读取 | 已知 | shell pipeline | STRIP 文件名详列；提示 agent "across IRB/pipeline/co-author shift docs" |
| schema | — | shell `irb_before_extraction==true` etc. | KEEP（字段名 verbatim）|
| 推理逻辑步骤 | — | — | STRIP（agent 应自读日期）|

## q13 — committee_response_draft.md（docs/，date-prefix）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `912/847/65` | check_q13 grep word-boundary | KEEP-LITERAL 三数（强 grep）|
| `BFH-2025-IRB-0342` | grep | KEEP-LITERAL |
| `V2.0` 或 `王逸生` | grep | KEEP-LITERAL |
| 投诉 refutation 语义 (M6) | grep `complaint.*not.{0,40}support\|allege.*however\|refut\|反驳\|不成立\|disprove\|complaint.*unfound` | KEEP "complaint" + "refute/not support" 语义指示 |
| ≥4 ## headings | — | grep | KEEP |
| 文件路径模板 `docs/YYYY-MM-DD_committee_response_draft.md` | — | check 文件名 | KEEP `committee_response_draft` 词根 + `YYYY-MM-DD` |

## q14 — adverse_outcome_comparison.md + adverse_outcome_rates.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `65/847` | data-cleaning-pipeline-log.md | grep word-boundary | KEEP-LITERAL |
| consistent / not significantly different 语义 | — | grep | KEEP |
| selective-exclusion refute 语义 | — | grep | KEEP |
| JSON 字段+`no_selective_exclusion` 串 | — | strict | KEEP-LITERAL 该串 |

## q15 — generate_defense_summary.py

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema 字段 | — | shell strict | KEEP verbatim |
| 三参考文件 | — | — | STRIP 列举（让 agent 自定）|

## q16 — zhang_zhuren_guidance_analysis.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `张主任` 或 `zhangzhuren` | upd3 zhangzhuren-guidance.md | grep | KEEP-LITERAL（任一）|
| `standard` 或 `pre-registered` | — | grep | KEEP-LITERAL（任一）|
| 投诉 vs 张主任 contrast | — | grep | KEEP 对比语义 |
| ≥3 ## headings | — | — | KEEP |

## q18 — irb_compliance_audit.json + complaint_rebuttal_matrix.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema | — | strict | KEEP |
| MD 4 列表头 / 4 行 / pipeline 或 HIS 字 | — | grep | KEEP "Allegation\|Evidence" 列名 + ≥4 行 + pipeline/HIS |

## q19 — build_irb_compliance_report.py

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema | — | shell strict `allegations_refuted==4 allegations_supported==0 overall_verdict contains "not_supported"` | KEEP（字段名 + `not_supported` 子串）|
| 4 大指控之列举 | anonymous-complaint-letter.md | — | STRIP 列举（agent 自读投诉信）|

## q20 — methodological_defense.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `V2.0` | — | grep | KEEP |
| `BFH-2025-IRB-0342` 或 `BFH` | — | grep | KEEP-LITERAL |
| `HIS` + `migration` | — | grep 各自 | KEEP-LITERAL 两词 |
| 投诉 vs 证据两 framing 对比 | — | grep | KEEP |

## q21 — four_contradiction_analysis.md + contradiction_resolution_v2.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| C1–C4 全部 | 各 upd | grep `C1\|C2\|C3\|C4`（headings）| KEEP-LITERAL "C1" "C2" "C3" "C4" |
| ≥4 ## headings | — | — | KEEP |
| JSON c1–c4 + favors_defense=true | — | strict | KEEP |

## q22 — pipeline_audit_trail.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `V2.0` + `2025-09-20` | data-cleaning-pipeline-log.md | substring | KEEP-LITERAL |
| `V2.1` + `2025-10-15` | 同上 | substring | KEEP-LITERAL |
| `field rename` 或 `minor` | — | grep | KEEP-LITERAL |
| `pre-submission` / `not post-hoc` 语义 | — | grep | KEEP "pre-submission" 或 "post-hoc" 词 |

## q24 — formal_ethics_response.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 全 schema + 枚举值（`responded`/`confirmed`/`acknowledged_not_misconduct`/`committee_clarification`/`#BFH-2025-IRB-0342`/`["V2.0","V2.1"]`）| — | strict | KEEP verbatim |

## q25 — generate_final_defense.py

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema | — | shell strict bool | KEEP |
| 文件读取建议 | — | — | STRIP |

## q26 — coauthor_resolution_strategy.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `王逸生` | — | grep | KEEP-LITERAL |
| contemporaneous vs post-complaint contrast | — | grep | KEEP "pre-complaint"/"contemporaneous" |
| `pipeline` 独立证据 | — | grep `pipeline.*independent\|independent.*pipeline\|timestamp` | KEEP "pipeline" + "independent/timestamped" 语义 |
| ≥2 ## headings | — | — | KEEP |

## q27 — final_committee_response.md + response_evidence_checklist.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 文件名 `docs/YYYY-MM-DD_final_committee_response.md` | — | glob | KEEP `final_committee_response` 词根 + `YYYY-MM-DD` |
| `BFH` 或 `#BFH-2025-IRB-0342` | — | grep | KEEP-LITERAL |
| ≥5 ## headings | — | — | KEEP |
| JSON 全 bool 字段 + irb_number contains BFH | — | strict | KEEP schema |

## q29 — final_research_integrity_report.md（P1–P5 全检）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `912/847/65` | — | grep | KEEP-LITERAL |
| `#BFH-2025-IRB-0342` | — | grep | KEEP-LITERAL |
| `V2.0`/`王逸生`、`V2.1`/`林依` | — | grep | KEEP-LITERAL 全部 |
| adverse rate 一致性 / 4 allegations refuted 语义 | — | grep | KEEP 语义 |
| 文件名 `docs/YYYY-MM-DD_final_research_integrity_report.md` | — | glob + P2 prefix | KEEP `final_research_integrity_report` 词根 + `YYYY-MM-DD` |
| ≥5 ## headings、≥800 chars | — | — | KEEP 数字提示 |
| P1（Problem/Assessment/Plan headings）、P3（first ## ≤500 chars）、P4（IRB+pipeline）、P5（≥3 distinct numbers）| — | check_preferences | KEEP P1/P3/P4/P5 引用 |

---

## 总体策略

- **整体语气**：林怡是急诊主治，文言/英文混用，简洁、临床式（"problem/assessment/plan"），偶 ER brevity 缩写；同事/委员会场景换正式语调
- **首次出现的源文件名**：q3/q4 可保留 `paper-dataset-summary.md` `raw-case-database-export.md`（initial 轮，定位用）；后续轮只指代（"Wang's V2.0 audit log"、"Zhang 主任的 guidance memo"、"upd3 的 director note"）
- **distractor**：每题 ≥1 句 tangential 加味——如 "Casey 那边 promotion deadline 在压"、"committee 周四例会前要交"、"reviewer 还在等 corrigendum"、"晚班结束前要收"
- **persona variation**：q3/q4/q6（自我笔记，clinical brevity）；q13/q27（formal committee tone）；q11/q26（lab-mate 私下侧写）；q15/q19/q25（脚本写代码 task voice）
- **STRIP 不确之处**：
  - q9 中"23"是关键 word-boundary，必 keep；其叙事可以让 agent 自读 co-author-data-version.md
  - q3/q14 中 `912/847/65` 字面 grep，必 keep
  - q22 中两 ISO 日期 substring grep，必 keep
- **不强字面而保 KEEP**：所有 schema 字段名 / 枚举常量字符串 / 路径 / IRB 号 / pipeline 版本号
