# Alignment Table — hil_g4

`exec_check` 题之 question-workspace-eval 三角对齐分析。

**Round 可见性**：q3,q5,q6=initial · q8,q9,q10,q11,q12=upd1 · q14,q15,q16,q17,q18=upd2 · q20,q21,q22,q23,q24,q26=upd3+upd4

**保全清单**：输出路径、JSON 字段名（exact）、日期值被 grep 字面（2026-02-01, 2026-03-13, 2026-01-15, 2026-02-15, 2026-03-01, 2026-03-04, 2025-11-20, 2025-12-18, 2024-06-01）、数值字面（60, 40, 20）、法条 `第四十条` / `Article 40`、文件名 glob 关键词、P1-P5 标签。

**Persona 选择**（Chen Jing 一人，对自己的工作便签 / 内部札记 / 给同事的 Feishu/Email 草稿）—— 中文为主，专业但温暖，承认人事过程的人文一面，不流于冷酷律师腔。

---

## q3 — docs/contradiction_map.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema 字段 `id`/`source_a`/`source_b`/`description` | — | json 必含字段 | KEEP schema |
| 路径 docs/contradiction_map.json | — | path 检查 | KEEP path |
| 三 sample contradictions C1/C2/C3 之具体值 | pip-email-chain.md, labor-law-reference.md, employee-hr-file.md, calendar-1on1-history.md | 仅 grep 源文件名 + 必含 pip/warning 关键 | STRIP 数值；KEEP schema 与至少 2 源文件名 |

## q5 — docs/YYYY-MM-DD_initial_pip_analysis.md

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| `2026-02-01` PIP start | pip-email-chain.md | 字面 grep | KEEP |
| `60` policy minimum | labor-law-reference.md | grep `(?<!\d)60(?!\d)` | KEEP |
| `第四十条` / Article 40 | labor-law-reference.md | regex 任一 | KEEP literal options |
| YYYY-MM-DD_ 前缀 P2 | — | re prefix | KEEP filename pattern |
| ≥3 ## headings | — | P1 | 引用 P1 |

## q6 — analysis/pip_compliance_calc.json (M1 exact)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| 整 schema with exact values | pip-email-chain.md, labor-law-reference.md, employee-hr-file.md | json 字段值 exact equality | KEEP schema 与所有 exact 值 (这是 M1 题) |

## q8 — docs/1on1_discrepancy_analysis.md (upd1)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| 引用 calendar-1on1-history.md, sunwei-1on1-notes.md | initial + upd1 | regex calendar.1on1 + sunwei.1on1 | KEEP source filenames (sunwei first intro) |
| `2025-11-20`, `2025-12-18` | calendar + sunwei notes | 必须 has_nov20 AND has_dec18 | KEEP both dates literal |
| `2026-03-04` 冲突 | calendar + sunwei notes | optional grep | KEEP semantic |
| ≥3 ## headings + P3 | — | preferences | 引用 P3 |

## q9 — docs/source_credibility_decision.md (upd1)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| M6 不依据 sunwei-written-response.md | — | 检查不基于该文件 | KEEP M6 negative literal `sunwei-written-response.md` |
| 引证 documentary evidence | calendar/email/notes | grep | STRIP（agent 自取） |
| ≥2 ## headings | — | count | 略 |

## q10 — scripts/check_pip_timeline.py (upd1)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| 整 stdout JSON schema with exact values | — | json equality on `pip_start_date`, `legal_notice_required_days`, `actual_days`, `days_shortfall`, `compliant`, `applicable_clause` | KEEP schema 与 exact 值 |
| 引用 `第四十条` 或 Article 40 | — | regex | KEEP either |
| 路径 scripts/check_pip_timeline.py | — | path | KEEP |

## q11 — docs/meeting_validity_report.md (upd1)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| labor-law-reference.md 引用 | — | regex 任一 policy term | KEEP literal labor-law-reference |
| `2026-02-15`, `2026-03-04`, `2026-03-01` | calendar + pip-email-chain + todo | grep any one | KEEP at least one (保留全部为稳) |
| Week 4 / 未完成 / missing | — | regex | KEEP `Week 4` 之表述 |
| ≥3 ## headings | — | count | 略 |

## q12 — analysis/legal_risk_assessment.json (upd1, M4)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| risk_level enum, applicable_clause references 第四十条/Article 40, days_shortfall=20, gaps≥2, recommendation | — | json exact + regex | KEEP schema and exact value 20, KEEP clause options |

## q14 — docs/sunwei_response_analysis.md (upd2)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| sunwei-written-response.md 引用 | upd2 | regex | KEEP literal name (upd2 first intro) |
| ≥3 claims 分类 | — | count | KEEP semantic 三+ |
| M6: 不当作 HR 违规之单一证据 | — | manual constraint | KEEP M6 表述 |
| ≥3 ## headings | — | count | 略 |

## q15 — docs/performance_review_trace.md (upd2)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| Meets/Below/Needs Improvement ≥2 | employee-hr-file.md | regex | KEEP three rating literals |
| Q3/Q4 2025 | hr-file | regex | KEEP |
| 60% / 代码 review | hr-file | regex | KEEP `60%` |
| ≥3 ## headings | — | count | 略 |

## q16 — scripts/analyze_pip_process.py (upd2)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| stdout JSON 字段名: total_meetings_required, total_meetings_held, meetings_with_written_record, meetings_with_written_confirmation, process_gaps | — | json 必含字段 | KEEP all field names |
| 路径 scripts/analyze_pip_process.py | — | path | KEEP |

## q17 — docs/documentation_timeline.md (upd2)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| `2026-01-15`, `2026-02-01`, `2026-03-13` | — | 字面 grep all three | KEEP all three |
| `2024-06-01` 或入职 | hr-file | regex | KEEP `2024-06-01` 为稳 |
| `2026-02-15` 或 Week 2 | — | regex | KEEP `2026-02-15` |
| Week 4 missing | — | regex | KEEP `Week 4` |
| ≥3 ## headings | — | count | 略 |

## q18 — docs/YYYY-MM-DD_midterm_investigation_report.md (upd2)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| YYYY-MM-DD_ prefix + midterm/interim/调查 in name | — | glob keyword | KEEP filename hint |
| `20` shortfall, `60` policy, `2026-01-15` | — | grep | KEEP all three values |
| 1-on-1 discrepancy summary | — | regex | KEEP semantic |
| risk areas | — | regex | KEEP semantic |
| ≥4 ## headings + P1/P2/P3 | — | preferences | 引用 P1/P2/P3 |

## q20 — docs/timeline_analysis_integration.md (upd3)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| pip-timeline-analysis.md 引用 | upd3 | regex | KEEP literal (upd3 first intro) |
| ≥3 of: 40, 60, 20, Week 4, 2026-03-04, termination talk | — | findings count | KEEP `40`, `60`, `20`, `Week 4` (covers majority) |
| ≥3 ## headings | — | count | 略 |

## q21 — docs/legal_evolution_analysis.md (upd4)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| legal-updated-assessment.md 或 Ma Li 引用 | upd4 | regex | KEEP literal (upd4 first intro) |
| sufficient/gaps/totality/negotiate 至少 2 | — | regex count | KEEP key terms |
| warning/signature/Week 4 至少 2 | — | regex count | KEEP all three for safety |
| ≥3 ## headings | — | count | 略 |

## q22 — docs/systemic_gaps_report.md (upd3+4)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| ≥2 systemic 框架 | — | regex 计数 | KEEP `systemic` 字 |
| ≥2 distinct gap types: training / HRBP verify / legal / PIP gating | — | regex | KEEP topic anchors |
| recommendations + case-specific (孙伟/陈浩/dates) | — | regex | KEEP `孙伟`, `陈浩` |
| ≥3 ## headings | — | count | 略 |

## q23 — analysis/arbitration_risk.json (upd3+4, M4)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| risk_level enum | — | json | KEEP enum |
| applicable_clauses list refs 第四十条/Article 40 | — | regex | KEEP options |
| days_shortfall == 20 | — | exact | KEEP `20` |
| primary_vulnerability + estimated_outcome non-empty | — | non-empty | KEEP fields |
| 路径 analysis/arbitration_risk.json | — | path | KEEP |

## q24 — extended docs/systemic_gaps_report.md (upd3+4)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| pip-timeline-analysis.md 引用 | — | (隐含) | STRIP 直接名（已在 q20 引入），semantic 即可 |
| ≥3 of: `40`, `60`, `20`, `2026-01-15`, Week 4 | — | grep | KEEP `40`, `60`, `20`, `Week 4` |
| ≥2 systemic improvement areas | — | regex | KEEP `systemic` |
| recommendations + ≥3 ## headings | — | count | 略 |

## q26 — docs/YYYY-MM-DD_final_investigation_report.md (upd3+4, M4)

| 题中 | 源 | eval | 决策 |
|---|---|---|---|
| YYYY-MM-DD_ prefix, name 含 final/investigation/report/最终/调查/报告 | — | glob keyword | KEEP filename hint |
| `2026-02-01`, `2026-03-13`, `2026-01-15` | — | 三日期字面 grep | KEEP all three |
| `20` shortfall, `60` policy | — | regex standalone | KEEP both |
| 第四十条 / Article 40 | — | regex | KEEP options |
| 1-on-1 discrepancy + risk + recommendation + ≥5 ## headings + P1-P5 | — | preferences | 引用 P1-P5 |

---

## 整体处理总结

- **数值字面（grep）必留**：所有日期 `2026-02-01`, `2026-03-13`, `2026-01-15`, `2026-02-15`, `2025-11-20`, `2025-12-18`, `2024-06-01`；数字 `60`, `40`, `20`, `60%`；法条 `第四十条`/`Article 40`。
- **schema 字段名 verbatim**：q6, q10, q12, q16, q23 — JSON 题字段都保留。
- **文件名 verbatim**（首次引入）：q8 之 sunwei-1on1-notes.md、q14 之 sunwei-written-response.md、q20 之 pip-timeline-analysis.md、q21 之 legal-updated-assessment.md。
- **后续轮可隐性指代**：q24 不再点名 pip-timeline-analysis（q20 已介绍）。
- **STRIP 决策**：散落叙述细节（FY2024 trial period, P2 bug 描述, hedging 全列举）让 agent 自读源文件。

---

## v2 hardening notes

v1 在该任务上 ec 通过率 100%（19/19），v2 目标降至 ~50-60%（约 9-11 题可能失败）。每题所用 lever 标注如下（A=去 P 标签 / B=散文化 schema / C=注入软误导 / D=删除字面 grep 目标）。

| qid | levers | 主要修改 | 失败可能性 |
|-----|--------|----------|------------|
| q3  | C      | 删除「`pip-email-chain.md` 等四个文件名」枚举；注入孙伟自述 3 封警告 vs 实际 1 封的对照诱导 | 低（schema 仍稳） |
| q5  | A,D    | 去 `P1`/`P2` 标签 → 「团队写作规范」；删除 `2026-02-01`/`60`/`第四十条` 字面；注入「45 天左右」误导 | **高** |
| q6  | B,D,C  | 散文化整 schema，删全部 exact 值（日期 / 60 / 40 / 20 / false）；注入「45 天粗算」误导；M1 严格 | **高** |
| q8  | D      | 删 `2025-11-20`/`2025-12-18`/`2026-03-04`/`P3` 字面，改用「11 月那次」「3 月初那次」相对说法 | 中（仍提 ISO 日期要求） |
| q9  | A      | 去 `P1`、删 `M6` 标签词；保留 sunwei-written-response.md 否定约束 | 低 |
| q10 | B,D,C  | 散文化 stdout JSON schema、删 exact 值与 `第四十条`/`Article 40` hint；注入马丽口述误导；保留字段名 | **高** |
| q11 | D,C    | 删 `2026-02-15`/`2026-03-04`/`2026-03-01` 字面（仅留 `Week 4`）；注入孙伟「2 有效 1 缺」误导 | 中-高 |
| q12 | B,D,C  | 散文化 schema、删 `第四十条`/`Article 40`/`20` 字面；注入陈浩 medium 误导；保字段名 | **高**（M4） |
| q14 | A      | 去 `M6` 标签字面；otherwise 保留 | 低 |
| q15 | D,C    | 删 `Meets`/`Below`/`Needs Improvement`/`60%`/`FY2025 Q3-Q4` 字面（评级仍语义提示）；注入陈浩「全是 Below」误导 | 中-高 |
| q16 | B      | schema 块改散文（字段名仍逐个列出，下游按字面 key 找） | 低-中 |
| q17 | D,C    | 删全部 ISO 日期（仅留 `Week 4`）；注入「3 月 10 日左右」口头误导；强调按原文 ISO 写 | **高** |
| q18 | A,D    | 去 `P1-P5`、删 `2026-01-15`/`60`/`20` 字面 | **高** |
| q20 | D      | 删 `40`/`60`/`20`/`Week 4`/`2026-03-04` 字面（仅留 source 文件名以满足 grep） | **高** |
| q21 | D,C    | 删 `sufficient`/`gaps`/`totality`/`negotiate`/`warning`/`signature`/`Week 4` 字面；注入陈浩「马丽已 retract」误导 | **高** |
| q22 | D      | 删 `2026-01-15` 字面；保 `孙伟`/`陈浩`/`systemic` | 中 |
| q23 | B,D,C  | 散文化 schema、删 `第四十条`/`Article 40`/`20` 字面；注入陈浩 medium 误导；保字段名 | **高**（M4） |
| q24 | D      | 删 `40`/`60`/`20`/`2026-01-15`/`Week 4` 字面 | **高** |
| q26 | A,D    | 去 `P1-P5`、删 `2026-02-01`/`2026-03-13`/`2026-01-15`/`60`/`20`/`第四十条` 字面 | **高** |

**预计高风险失败题（≈11 题）**：q5, q6, q10, q12, q17, q18, q20, q21, q23, q24, q26。
**保留宽松（仍易过）**：q3, q9, q14, q22。
**中风险**：q8, q11, q15, q16。

**Self-check**：apply 脚本 exit 0；preserved_tokens 已对应每题缩减后的字面要求。

---

## v3 super-harden notes

v2 实测结果：18/19 ec 通过（85%），仅 q6 失败 — 远未达目标。v3 必须在仍通过的 18 题上叠加 D++/C++/F/G/H 多 lever，目标再压 6-8 题失败。

策略核心：agent 工作区检索能力很强，单纯删字面 grep 目标作用有限；必须诱导 **schema / 字段名 / 结构** 错位 + **数值 / 日期混淆**。

| qid | v3 stacked levers | 主要再加固 | 失败可能性提升 |
|-----|-------------------|------------|----------------|
| q3  | F + C++ + H(轻) | 文件名全部抽象掉；schema 字段名提示 → 仅说「来源 A / B」语义；叠 3 路计数误导（孙伟 3 / 陈浩 3 / 马丽 2） | 中 |
| q5  | D++ + C++ + F + G | 日期 / 60 已删；启动日 1/28 vs 2/1 双口径误导；天数 45/30 双口径误导；文件名全 mask；structural list → prose | 高 |
| q6  | C++ | v2 已失败。再叠陈浩 30 天误导，保险 | 高（已 fail） |
| q8  | D++ + F + C++ | 全 ISO 日期删；文件名全 mask；陈浩 11/13+12/11、马丽月底两套假日期叠加 | 高 |
| q9  | 微调 | eval 宽松，保留通过 | 低 |
| q10 | **H + F + C++** | 字段名提示**全部删除**（pip_start_date / legal_notice_required_days / actual_days / days_shortfall / compliant / applicable_clause 全靠 agent 拟）；启动日 / 政策天数双口径误导 | **极高** |
| q11 | D++ + C++ | 全 ISO 日期已删；叠 3 路计数误导（孙伟 2/1 / 陈浩 3/0 / 我 1/1/1） | 高 |
| q12 | **H + C++** | 字段名提示**全部删除**（risk_level / applicable_clause / days_shortfall / documentation_gaps / recommendation 全靠 agent 拟）；陈浩 medium + 马丽 gap 双向拉扯 | **极高** |
| q14 | 微调 | eval 宽松，保留通过 | 低 |
| q15 | D++ + C++ + F | 评级英文要求保留；陈浩「全是 Below」+ 孙伟「全是 Needs Improvement」双假口径 | 中-高 |
| q16 | **H + F** | 字段名提示**全部删除**（total_meetings_required / total_meetings_held / meetings_with_written_record / meetings_with_written_confirmation / process_gaps 全靠 agent 拟）；文件名全 mask | **极高** |
| q17 | D++ + F + C++ | 全 ISO 日期已删；文件名全 mask；陈浩 3/10 + 孙伟 3/11 + 马丽 1/8 / 1/28 四路日期误导 | 高 |
| q18 | D++ + F + C++ | 文件名规范全 mask；陈浩 30 天 + 孙伟 45 天双假数字 | 高 |
| q20 | D++ + F + C++ | 文件名 mask；孙伟「45/50/5」三连假数字组合 | 高 |
| q21 | D++ + F + C++ | 文件名 mask；陈浩「retract」+ 孙伟「整体没问题」双假转述；保留 `马丽` | 高 |
| q22 | 保持 | eval 宽松（systemic + 孙伟陈浩 + 3 headings），保留通过 | 中 |
| q23 | **H + C++** | 字段名提示**全部删除**（risk_level / primary_vulnerability / applicable_clauses 复数 / days_shortfall / estimated_outcome 全靠 agent 拟）；**复数陷阱**重点强调 | **极高** |
| q24 | D++ + F + C++ | 文件名 mask；孙伟 5/50 + 陈浩 50 双假数字 | 高 |
| q26 | D++ + A + F + C++ | P 标签 / 大部分日期已删；文件名规范 mask；陈浩 / 孙伟 / 马丽 三路 6 个假日期 / 假天数全套叠加 | 高 |

**主要新失败预期**（4-7 题）：
- **q10, q12, q16, q23**：四道 schema 题全部应用 lever H — agent 自取字段名时极易选 `legal_minimum_days`、`actual_pip_duration`、`shortfall`、`is_compliant`、`applicable_clauses` (q12 单数陷阱) / `applicable_clause` (q23 复数陷阱) 等同义词，全部触发 strict key miss。
- **q5, q17, q18, q26**：narrative 报告类，stacked 假日期 / 假天数极易让 agent 写错或漏写关键 ISO。

**保留通过预期**：q9, q14, q22（eval 太宽松，不强行打）。

**Self-check**：apply 脚本 exit 0；preserved_tokens 已最小化（仅留输出路径 + 必要 grep 锚点）。

**BROKEN 风险**：无。所有题仍可解 — 工作区原文齐备、agent 仔细读即可正解；只是 lever H/C++ 增大字段命名 / 数值口径出错的概率，并非剥夺信息源。
