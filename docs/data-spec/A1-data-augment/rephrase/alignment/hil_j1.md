# Alignment Table — hil_j1

`exec_check` 题之 question-workspace-eval 三角对齐分析。22 道执行题（q3, q4, q6-q9, q11-q16, q18-q22, q24-q27, q29）。

**轮次可见性**：
- 初始（round 0）：xiaohongshu-analytics-export.md（已含 API 文档 v3.2 摘录）、bilibili-analytics.md、mcn-brand-report.md、USER.md
- upd1（q5 起）：upd1_sessions/zhoufang_zhaomin_wechat.md、upd1_workspace/brand-received-data.md
- upd2（q6 起）：upd2_workspace/mcn-contract-excerpt.md（合同条款 7.3、9.1、4.2、8.1）
- upd3（q15 起）：upd3_sessions/zhoufang_liujie_wechat.md（"内部估算"原话）
- upd4（q21 起）：upd4_sessions/zhoufang_zhaomin_wechat.md（小林 30K vs 70K）

**保全清单**：
- 输出路径（含中文）：analysis/<name>.md / analysis/<name>.json / scripts/<name>.py / docs/YYYY-MM-DD_<topic>.md
- JSON 字段名（snake_case 全部 verbatim）
- 关键 grep 字面量：`50,234` `120,000` `32,178` `65,000` `3,812` `8,500` `2.39` `2.02` `2.23` `2.33` `30,000` `70,000` `2.386` `内部估算` `刘姐` `7.3` `9.1` `4.2`
- P 规则：P1（表格+emoji）、P2（日期前缀）、P3（结论先行）、P4（数据+故事）、P5（活泼亲切）

---

## q3 — 数据差异初步分析（initial round）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 50,234 / 120,000 / 2.39 / 2.386 | xiaohongshu-analytics-export.md / mcn-brand-report.md | grep + JSON==50234 / 120000 / ratio≈2.386 | KEEP（grep 字面量；eval 同时 grep MD 与 JSON 严格相等）|
| schema 字段（xiaohongshu_official, _mcn, _ratio, bilibili_*） | — | JSON 严格相等 | KEEP verbatim |
| 路径 analysis/数据差异初步分析.md / .json | — | test -f 与读取 | KEEP |
| "结论"或"发现" | — | first ## 含此词 | KEEP（P3 grep）|
| 文件名 xiaohongshu-analytics-export.md / mcn-brand-report.md | initial 文件 | 无强 grep | KEEP（首次出现作命名锚点）|

## q4 — compute_data_ratios.py（initial round）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 scripts/compute_data_ratios.py | — | 必检 | KEEP |
| schema (xiaohongshu_ratio, bilibili_ratio, max_ratio, systematic_inflation) | — | JSON | KEEP |
| 数值精度 ±0.1 | — | abs check | STRIP（agent 自算即可，但保留语义提示）|
| 表格中数字含逗号需解析 | MD 表格事实 | — | STRIP（实现细节）|

## q6 — 品牌方材料分析 + 数据来源对比 JSON（upd2 起）

注：q6 的 update_ids=["upd2_workspace"] 但题文也涉及 brand-received-data.md（upd1）。两文件均可见。

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| brand-received-data.md / mcn-contract-excerpt.md 文件名 | upd1/upd2 | 无 grep | STRIP（首次提及——upd1 在 q5 多选已现，upd2 此为首次）→ 保 mcn-contract-excerpt 名以助 orient；brand 用语义指代 |
| "截图（PNG）" | brand-received-data.md | grep "截图"/"screenshot"/"PNG" | STRIP（agent 读即得） |
| 合同条款 7.3 / 9.1 | mcn-contract-excerpt.md | grep "7.3" / "9.1" | KEEP verbatim（grep 字面）|
| 路径 analysis/品牌方材料分析.md / 数据来源对比.json | — | test -f | KEEP |
| schema mcn_submitted/contract_required/compliant/xiaohongshu_official/.. | — | JSON 严格 | KEEP |
| 50234 / 120000 / 32178 / 65000 | — | JSON 严格相等 | KEEP（schema 数值）|

## q7 — multi_platform_stats.py

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 三个 MD 文件名 | initial files | 无 grep（脚本自读） | STRIP（文件已在 q3 命名）|
| schema 全套 | — | JSON 严格 | KEEP |
| 50234 / 32178 / all_above_2x | — | 严格相等 | KEEP |

## q8 — 系统性夸大一致性分析

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 50,234 / 120,000 / 32,178 / 65,000 / 3,812 / 8,500 | initial files | grep 全部字面 | KEEP verbatim（grep 严格） |
| 2.39 / 2.02 / 2.23 | — | grep 字面 | KEEP |
| "系统性"判断 | — | grep 关键词族 | STRIP（语义即可，关键词族广）|
| >= 3 ## 标题 | — | 计数 | KEEP（结构要求）|

## q9 — 互动数据比率分析

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 3,812 / 8,500 | XHS 后台 / MCN 报告 | grep 字面 | KEEP |
| 2.23x / 2.25x / 2.51x | 自算 | 仅 grep 2.23 family（abs<0.05）| KEEP 2.23；其余 STRIP（无强检查）|
| 收藏 1,423 vs 3,200（注释中 1,684 误） | — | 无 grep | STRIP（agent 自查）|
| 互动率 3.7% / 9.3% | — | 无 grep | STRIP |

## q11 — 口径辨析报告（M2）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 analysis/口径辨析报告.md | — | test -f | KEEP |
| "刘姐" / "API"/"官方" / "口径" | initial 文件 + USER.md | grep 全部 | KEEP（grep 字面）|
| 50,234 / 120,000 | — | grep | KEEP |
| 判断结论语 | — | grep 关键词族 | STRIP（语义）|

## q12 — verify_ratio_consistency.py

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema 字段 | — | JSON 严格 | KEEP |
| explanation_api_consistent==false | — | 严格 false | KEEP |
| likes_ratio ≈2.23 | — | abs<0.1 | KEEP |

## q13 — 刘姐解释反驳（M6）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 analysis/刘姐解释反驳.md | — | test -f | KEEP |
| "刘姐" | — | grep | KEEP |
| 否定词族（"不能"/"无法"...） | — | grep 关键词族 | STRIP（语义足以触发）|
| 50,234 / 120,000 | — | grep | KEEP |

## q14 — 数据欺诈证据矩阵 + 欺诈证据.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 四维度（小红书播放/B站/点赞/收藏） | initial | grep 关键词族 | STRIP 之具体值；KEEP 维度名以确保覆盖 |
| 2.39 / 2.02 | — | grep 字面 | KEEP |
| schema {dimension, official, mcn_report, ratio, exceeds_2x} | — | JSON 严格 | KEEP |
| 第一元素 ratio∈[2.3,2.5] | 小红书事实 | 严格 | STRIP 具体值（agent 自填）；保留"第一元素对应小红书"指针 |

## q15 — analyze_admission_evidence.py（upd3 起）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 scripts/analyze_admission_evidence.py | — | 必检 | KEEP |
| "内部估算" key_quote | upd3 wechat | grep + key_quote 包含 | KEEP verbatim（脚本须输出此字符串）|
| 文件名指针（含 liujie/刘姐） | message_logs/upd3 | 脚本读取 | KEEP（首次提及 upd3 文件需指引位置）|
| schema | — | JSON 严格 | KEEP |

## q16 — 承认记录分析

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 analysis/承认记录分析.md | — | test -f | KEEP |
| "内部估算"精确字符串 | upd3 | grep | KEEP verbatim |
| "刘姐" | — | grep | KEEP |
| 矛盾分析关键词 | — | grep 族 | STRIP |

## q18 — 矛盾演化时间线 + 矛盾注册.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| C1-C4 标签或等价描述 | — | 优先 grep "C1".."C4"，否则 fallback 关键词族 | KEEP C1-C4 标签（最稳）|
| "内部估算" | — | grep | KEEP |
| schema {id, claim, evidence, resolution, favors_fraud_claim} | — | JSON 仅查 favors_fraud_claim | KEEP favors_fraud_claim（其余 STRIP 字段细节）|

## q19 — build_fraud_case.py

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema 字段 | — | JSON 部分 | KEEP（evidence_count, admissions, legal_action_recommended）|
| key_evidence 数组示例 | — | 无强检查 | STRIP（仅 schema 提示）|

## q20 — 合同违约分析

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 7.3 / 9.1 / 4.2 | mcn-contract-excerpt.md | grep 字面 | KEEP verbatim |
| 互动率 3.7% / 9.3% | initial files | 无 grep | STRIP |
| 路径 analysis/合同违约分析.md | — | test -f | KEEP |

## q21 — 小林报酬差异分析（upd4 起）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 30,000 / 70,000 | upd4 wechat | grep 字面 | KEEP（grep 严格）|
| 2.33x | 自算 | parse_ratio abs<0.05 | KEEP "2.33"（避免 agent 写 2.3 或 2.4 不通过——等等：abs<0.05 之内浮点 2.3, 2.33 都过）→ STRIP，但保留指针让 agent 自算 |
| 路径 analysis/小林报酬差异分析.md | — | test -f | KEEP |
| 创作者小林 30,000 vs MCN 70,000 来源指针 | upd4_sessions/zhoufang_zhaomin_wechat.md | — | KEEP（首次出现 upd4 文件，需指引）|

## q22 — 四重矛盾总结 + case_strength.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 analysis/四重矛盾总结.md / case_strength.json | — | test -f | KEEP |
| 四矛盾覆盖 | — | grep 关键词族 | STRIP 细节，保维度名 |
| schema (allegations_supported==4, data_manipulation_ratio≈2.386, recommended_action=="legal_proceedings") | — | JSON 严格 | KEEP verbatim 三字段值 |

## q24 — 欺诈证据清单.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 analysis/欺诈证据清单.json | — | test -f | KEEP |
| schema {case_id, parties{...}, evidence_items[...], financial_damage{contract_amount, actual_billed, overcharge_ratio}, legal_threshold_met} | — | JSON 严格 financial_damage + items 数 | KEEP financial 字段值；evidence_items >=3 含 id/type/description/verified | KEEP schema 关键 |
| 30000 / 70000 / 2.33 | upd4 | 严格相等 | KEEP |
| parties 内容（赵敏/星芒传媒/周芳） | — | 无强检查 | STRIP（schema 列出即可）|

## q25 — compute_financial_damage.py

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 scripts/compute_financial_damage.py | — | 必检 | KEEP |
| schema (contract_amount==30000, amount_billed_to_brand==70000, overcharge_amount==40000, overcharge_ratio≈2.333) | — | JSON 严格 | KEEP verbatim |

## q26 — 诉讼证据强度评估

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 analysis/诉讼证据强度评估.md | — | test -f | KEEP |
| 四类证据 | — | grep 关键词族（每类四个备选） | STRIP 具体陈述，保覆盖说明 |
| "承认"或"内部估算" | — | grep | KEEP "内部估算" |
| 强度排序语 | — | grep 族 | STRIP（语义足够）|
| M2 最关键证据判断 | — | strength keyword grep | STRIP |

## q27 — 诉讼证据汇总报告（docs/ + JSON）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 docs/YYYY-MM-DD_诉讼证据汇总报告.md | — | glob date prefix + 文件名含"诉讼/证据/汇总/报告" | KEEP pattern |
| 数值 50,234 / 32,178 / 30,000 / 70,000 | — | grep | KEEP（皆 grep 字面）|
| "2.39"或"2.386" | — | grep | KEEP |
| "内部估算" | — | grep | KEEP |
| 路径 analysis/报告数据核对.json | — | test -f | KEEP |
| schema (xiaohongshu_ratio≈2.386, contract_amount==30000, billed_amount==70000) | — | JSON 严格 | KEEP |
| P2 规则 | — | check_preferences P2 | KEEP "P2" 引用 |

## q29 — 最终欺诈调查报告（P1-P5 全检）

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 docs/YYYY-MM-DD_最终欺诈调查报告.md | — | glob | KEEP pattern |
| P1-P5 五规则 | style_guide？无独立 style_guide，规则在 USER.md+check_preferences 实现 | 全部 5 规则 grep | KEEP "P1"…"P5" |
| 50,234 / 120,000 / 32,178 / 65,000 / 内部估算 / 30,000 / 70,000 | — | 全部 grep | KEEP verbatim |
| 法律行动关键词族 | — | grep（法律/诉讼/起诉/维权/法务/追责/索赔/赔偿）| STRIP（族广）|
| >= 5 ## / >= 800 chars | — | 计数 | KEEP 结构要求 |
| P5 之"我"/"差距"/"明显"/"离谱" | check_preferences P5 | grep | STRIP（"P5" 已 KEEP，让 agent 读 P5 定义 in workspace？无 style_guide 文件）→ KEEP 提示活泼语气词样本 |

---

## 总体处理总结

- **完全 STRIP 具体值**：q4（精度提示）、q9（除 3,812/8,500/2.23）、q14（除 2.39/2.02）、q19（key_evidence 列表细节）、q20（互动率细节）、q21（2.33 由 agent 自算）、q24（parties 内容）、q26（强度排序细节）
- **保留具体值（grep 字面脆弱）**：q3, q6, q8（七数齐保）、q9（3,812/8,500）、q11, q13, q14（2.39/2.02）、q15/q16（"内部估算"）、q18（C1-C4+内部估算）、q20（7.3/9.1/4.2）、q21（30,000/70,000）、q27, q29（全数）
- **schema verbatim**：q3, q4, q6, q7, q12, q14, q18, q19, q22, q24, q25, q27
- **文件路径 verbatim**：所有题
- **P 规则编号 verbatim**：q3（P1, P3）、q27（P2）、q29（P1-P5）

接下来按上表执行 rephrase。

---

## v2 hardening notes

v1 在 gpt-5.4 下 ec 全 22 题 100% 通过，过于宽松，故按 `prompts/v2_harden_template.md` 四杠杆重写。

**总体策略**
- 杠杆 D（删字面）：尽量剥离工作区可查得的数值/条款编号/原话——播放量、点赞、收藏、合同条款 7.3/9.1/4.2、互动率 3.7%/9.3%、刘姐承认的"内部估算"原话，全部交还由 agent 自行回源文件抓。
- 杠杆 A（剥 P 标签）：q27 的 "P2"、q29 的 "P1–P5" 整段删除，改为指向 USER.md 段落、用散文化描述（"主题-日期命名格式 / 视觉对比表格 + emoji / 结论先行 / 数据+故事 / 活泼亲切语气"）。q29 不再列 P-code，也不再罗列具体 emoji 选项与"我/差距/明显/离谱"关键字示例。
- 杠杆 B（散文化 schema）：q4/q7/q8/q9/q11/q13/q14/q19/q20/q22/q24/q25/q27 多数 schema 块改写为字段命名 + 取值规则的中文散文，仅保留 snake_case 字段名 verbatim；非常规字段（如 `liu_jie_admitted_estimate`/`favors_fraud_claim`/`all_above_2x`/`explanation_api_consistent`/`recommended_action` 枚举）保留代码块或字段名 verbatim。
- 杠杆 C（含糊误导分心句）：≥ 半数题加入 hedged-but-wrong 干扰：q3 "粉丝姐姐说算出来 1.8 倍左右"；q4 "赵敏猜大概只有小红书一个平台有问题"；q6 "她说主要是 PDF"；q8 "MCN 报的点赞是 7,500"；q9 "她记得收藏官方 1,684 vs MCN 3,000"；q15 "粉丝姐姐转述记得是\"内部数据\""；q21 "她模糊记得是 3 万 vs 6 万"。所有干扰均以"我不太确认/她记错了/源文件以工作区为准"包装。

**逐题杠杆映射**
- q3：B + C + D（删 50,234/120,000/2.39/2.386，植入 1.8 倍误导）
- q4：B + C + D（删 systematic_inflation 强制 true，引入"赵敏说只有小红书"）
- q6：B + C + D（删 7.3/9.1，删 screenshot/api_export_or_certified_third_party、PDF 误导）
- q7：B + D（schema 散文化，删四个具体整数与 all_above_2x 强制 true）
- q8：C + D（删全部数字，仅保结构与判断要求；植入点赞 7,500 误导）
- q9：C + D（删 3,812/8,500/2.23 全部；收藏数字误导）
- q11：D（删 50,234/120,000）
- q12：B + D（schema 散文化，删 explanation_api_consistent 强制 false 与 likes_ratio≈2.23）
- q13：D（删 50,234/120,000）
- q14：B + D（删 2.39/2.02 与首元素 ratio 范围）
- q15：A 形态 + C + D（删 stdout 代码块里 "内部估算" / "internal_estimate_not_platform_data" / "high"，全部由 agent 从聊天记录抠；植入"内部数据"误导）
- q16：D（删 "内部估算" 字面）
- q18：B + D（schema 散文化，删 "内部估算" 与四节点显式键短语，仅保 C1-C4 标签）
- q19：B + D（删 evidence_count≥3/admissions≥1 强制约束 → 改为软指引）
- q20：D（删 7.3 / 9.1 / 4.2 与 3.7%/9.3%）
- q21：C + D（删 30,000 / 70,000，植入 3 万/6 万误导）
- q22：B + D（删 4 / 2.386 / "legal_proceedings" 字面，转为"按枚举 snake_case 写"）
- q24：B + D（删 30000/70000/2.33 与 case_id 取值 hil_j1_mcn_fraud）
- q25：B + D（删全部数字 30000/70000/40000/2.333）
- q26：D（删 "内部估算"）
- q27：A + B + D（删 P2 / 2.39 / 2.386 / 50,234 / 32,178 / 30,000 / 70,000 / "内部估算" / 文件名硬模板"诉讼证据汇总报告"，仅保 docs/ 与 JSON 字段）
- q29：A + D（删 P1-P5 标签与全部数字字面与 "内部估算"，仅保 docs/ 与 "法律"）

**未保留 v1 不变的题**：无。22 题全部加压。

**自检**：apply 脚本 exit 0；diff 重新生成完毕。

**风险提示（可能 BROKEN 的边界）**
- q15/q16/q18/q26/q27/q29 全部要求 agent 从 upd3 的 zhoufang_liujie_wechat.md 里精确抠出"内部估算"四字。若 agent 读不到 upd3 文件 / 没意识到要查聊天记录，这几题会连环 fail。这正是设计意图，但若 round 可见性配置出问题则会 broken。
- q22 的 `recommended_action` 删除字面 `legal_proceedings`，agent 须自行推断后端枚举命名；这是可接受难度，但属偏激进。
- q29 删除 P1-P5 全部标签，依赖 agent 主动读 USER.md 才能恢复 5 条偏好；若不读则 check_preferences 必挂，是预期失败之一。

预计失败题：q3、q8、q9、q11、q15、q16、q18、q21、q22、q27、q29 等约 11–13 题，目标 ec ~ 50% 通过率。

