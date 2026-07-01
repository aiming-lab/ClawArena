# Alignment Table — hil_s1 (pilot)

`exec_check` 题之 question-workspace-eval 三角对齐分析。每行：题中所列值 → workspace 真源 → eval 检查 → 处理决策。

**Round 可见性**：q2,q3=initial · q7,q8,q9=upd1 · q11-q14=upd2 · q16-q18=upd3 · q21-q24=upd4

**保全清单（任题不可动）**：输出路径、输出 JSON 字段名、文件名前缀规则（YYYY-MM-DD_*_v<N>.ext）、枚举值约束（status, data_sensitivity 等）、P1-P5 规则编号本身。

---

## q2 — milestones.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| (无具体日期，已让 agent 自己找) | meeting_notes.md（kickoff 2025-03-03、interim 2025-03-12、deliver 2025-03-14）+ USER.md | check_deadline_file.py: 三日期硬编码相等 | 仅改语气；原题已不漏值 |

输出 schema 字段名 (`final_deadline`, `interim_review`, `kickoff_date`) 须 verbatim 留。

## q3 — metrics_definitions.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| "30-day" 阈值（feedback 中） | data_dictionary.md L174,461; old_q4_report.md 多处 | grep "30.day\|30 day\|threshold" + grep "churn" | STRIP — agent 读 data_dict 即得 |
| P1 例 "51,203" | style_guide.md（且实为数据集行数） | P1 校验 | STRIP — 转引 style_guide |
| P1 例 "2025-03-03T09:00:00Z" | style_guide.md | P1 校验 | STRIP — 转引 style_guide |

## q7 — data_dictionary update + versioned copy

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| "channel" 列 | upd1 schema_changelog.md, transactions_v2.csv 表头 | grep "channel" | STRIP — agent 读 changelog 自得 |
| "YYYY-MM-DD_data_dictionary_v2.md" 格式 | style_guide.md (P2) | check_preferences --expect-versioned-copy "data_dictionary" | KEEP — eval 直接 grep 文件名词根 "data_dictionary"，须 verbatim |

## q8 — clean_data.py for v2

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 输入 `transactions_v2.csv` | 即 upd1 新增之文件 | （无显式检查；输出有 channel 即视为 v2） | STRIP — 改用"新版数据"语义指代 |
| "channel" 列保留 | 同 q7 | 输出 CSV 含 channel | STRIP |
| 清洗规则细节 | 应见于已有 clean_data.py（v1 版） | 输出非空 | STRIP — 改作"沿用现行清洗逻辑" |
| 输出路径 `data/processed/transactions_v2_clean.csv` | — | test -f 该路径 | KEEP verbatim |

## q9 — action_items_u1.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 完整 JSON schema | check_schema.py 之 action_items schema | check_schema --schema action_items | KEEP（包以更自然之引语：legal/triage 工具吃这格式） |
| `"update": "update1"` | — | check_schema 验此字段 | KEEP，但缩 |
| "≥4 items" | — | python assert ≥4 | KEEP |
| status 枚举集 | — | schema 验枚举 | KEEP |
| "such as: re-running analysis…" 样例 bullet | — | 无强检查 | STRIP（agent 自填即可）|

## q11 — test_analysis.py

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 函数名 `analyze_churn_correlation()` | upd2 analysis_v2.py 中之函数 | pytest 实调此函数 | KEEP（agent 须知名；可改作"the correlation function in analysis_v2.py"）|
| dict 键 `correlation/p_value/method` | analysis_v2.py 返回值结构 | pytest assert keys | STRIP — agent 读 analysis_v2.py 自得 |
| `method == 'spearman'` | analysis_v2.py + 上轮 q10 多选已揭示 | pytest assert | STRIP — 改作"the corrected method we landed on" |
| 相关系数 `-1..1` | 数学常识 | assert range | STRIP |
| P4 细节（type hints/docstrings） | style_guide.md | check_preferences P4 | STRIP — 转引 P4 |

## q12 — corrected analysis report

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 文件名 `YYYY-MM-DD_<topic>_v<N>.md` | style_guide.md P2 | check_preferences P2,P3 | KEEP（pattern 须述）|
| 必含 sections (Summary/Details/Action Items) | style_guide.md P3 | P3 校验 | STRIP — 引 P3 即可 |
| 内容 bullets（why Spearman, recommendations…）| — | 仅 P2/P3 结构检查 | STRIP — 留意图勿强加目录 |

## q13 — progress_update_v1.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 文件名 `*_progress_update_v1.md` | — | ls 该 pattern | KEEP verbatim |
| P5 三约束（≤20 词首句 / [UNVERIFIED] / source citations） | style_guide.md | check_preferences P5 | STRIP — 引 P5 |
| 内容 bullets | — | grep "spearman\|correla" + 状态词 | KEEP "提到 Spearman 修正" 一条线索（隐蔽些）|

## q14 — README update (mid)

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| "channel" 列 | 见 q7 | grep channel | STRIP |
| section 名 "Project Status" | — | grep "Project Status" 字面 | KEEP（section 字面被 grep）|
| P1/P3 规则 | style_guide.md | P1,P3 | STRIP — 引规则编号 |

## q16 — contamination_log entry

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 检测日 `2025-03-12` | upd3 alex_slack.md "Contamination discovered 2025-03-12" | grep "2025-03-12" 字面 | STRIP — agent 读 slack 即得，但因 grep 字面，可靠性降低；建议保留隐性指代"今日（参 alex slack 中提及）"|
| 11,777 / 23.0% / 动作文本 | contamination_log.csv 头注 + alex slack | 仅 grep 日期 + P1 日期格式 | STRIP — 已可读 |

> 风险：日期 `2025-03-12` 之 grep 字面检查使此题脆弱。Agent 若挑别的格式或别的日期会败。建议**保留**该日期为题中明示，以稳妥。改"strip"→"KEEP"。

## q17 — impact_assessment_v1.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 文件名 pattern | — | ls + P5 | KEEP pattern |
| P5 | style_guide.md | P5 校验 | STRIP - 引 P5 |
| 内容（无具体数值在题中） | — | 无 | n/a |

## q18 — quality_check.py

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 1-4 必做项（dup/date/threshold/JSON stdout） | — | 实只检 stdout JSON 含 `churn_threshold` 键 + P4 | 可放宽——只需保证 agent 输出含 churn_threshold；其余可作语义指代 |
| "30 days" 阈值 | data_dictionary, old_q4_report | 无具体值检查（仅键存在） | STRIP — 自查阈值 |
| `churn_threshold` 字段名 | — | json 含此键 | KEEP |
| 路径 `project/src/quality_check.py` | — | 必检 | KEEP |

## q21 — run_final_pipeline.py

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `transactions_v3.csv` | upd3 文件存在 | 无显式检查输入 | STRIP — 用"latest/clean dataset" |
| Spearman | analysis_final.py (upd4) + 多处会话 | 输出 JSON lower 含 "spearman" | STRIP — 用"the agreed method" |
| 30-day | 同 q18 | 输出 JSON 字符串含 "30" | STRIP — 阈值自查；但因 grep "30" 较脆弱（任何 30 都过），保留亦无碍 |
| 输出路径 `data/processed/final_results.json` | — | 必检 | KEEP |

## q22 — README final update

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| `39,426` | contamination_log.csv 头注 + transactions_v3.csv 行数 | grep "39,426" 字面 | KEEP——P1 要求带逗号，agent 须写出此精确数；强制其读源后回填即可，可不在题中明示，但要给指针 → STRIP，依赖 agent 已知 P1 + 自数 v3 行数 |
| Spearman | 同 q21 | grep "spearman\|Spearman" | STRIP |
| 30-day | — | （非此题 grep）| STRIP |
| P1/P3 | — | 校验 | STRIP — 引 P1/P3 |

> 注：q22 之 39,426 之 grep 字面检查使此题脆弱。若 agent 形如 `~39k records` 即败。**为保稳妥，q22 中保留 "39,426"，但以 P1 thousands-sep 为由说明，使其自然。**

## q23 — project_summary_v1.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 文件名 pattern | — | ls + P5 | KEEP |
| P5 | — | P5 | STRIP - 引 |

## q24 — decision_log.md

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 4 reversal 具体值 (Pearson→Spearman / 45→30 / v2→v3 / 9.1%→8.3%) | 各 upd 文件 + sessions | check_scope_diff --required-topics method_change threshold_fix data_version baseline_recalc | 关键词性 grep（method/spearman/threshold/45/30/v2/v3/baseline/9.1/8.3 等族）。STRIP 具体值，但保 4 主题之**语义指代**（"the method change, the threshold correction, the dataset version switch, the Q4 baseline recalc"），让 agent 自填值 |

---

## 总体处理总结

- **完全 STRIP 具体值**之题：q3, q7, q8, q9 部分, q11, q14 部分, q17, q18, q21, q23
- **保留具体值（因 grep 字面脆弱）**：q14 之 "Project Status"、q16 之 `2025-03-12`、q22 之 `39,426`
- **schema 字段名 verbatim 留**：q2, q9, q11, q18
- **文件名 pattern verbatim 留**：q12, q13, q17, q23

接下来按上表执行 rephrase。
