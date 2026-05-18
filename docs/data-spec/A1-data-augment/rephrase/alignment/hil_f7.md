# Alignment Table — hil_f7

`exec_check` 题之 question-workspace-eval 三角对齐分析。每行：题中所列值 → workspace 真源 → eval 检查 → 处理决策。

**Round 可见性**：
- 初始 (q1–q6, q8–q12): order-history-618.md, package-tracking-log.md, payment-records.md, product-listing-screenshot.md, return-policy.md, USER.md
- upd1 (q7 起): product-listing-screenshot-append.md（截图2）
- upd2 (q13 起): payment-detail-export.md
- upd3 (q19 起): courier-evidence.md
- upd4 (q25 起): seller-response-email.md

需要 rephrase 之 exec_check 题：q3, q5, q6, q8, q9, q10, q11, q12, q14, q15, q16, q17, q18, q20, q21, q22, q23, q24, q26（共 19 题）。multi_choice (q1, q2, q4, q7, q13, q19, q25, q27) 不动。

**保全清单（多题共用）**：
- 文件路径：`docs/contradiction_map.json`, `docs/timeline.json`, `analysis/evidence_schema.json`, `scripts/parse_delivery.py`, `scripts/parse_payment.py`, `scripts/cross_validate.py` 等
- 订单号 `JD-618-2026-7891234`、SKU `GPU-A100-80G` / `GPU-A40-48G`、RMA `RMA-2026-0620-001`、退款流水 `2026062709300012345`
- 时间戳 `2026-06-18 10:02:33`, `10:02:45`, `2026-06-19 08:30:00`, `2026-06-20 11:45:00`, `2026-06-20 14:15:00`
- 三个运单尾号 `88761`, `88922`, `89103`
- 金额 `72,999`, `32,000`, `40,999`, `74,999`, `79,999`, `7299900`, `7999900`, `3200000`, `4099900`
- 政策 `v3.2`, 日期 `2026-01-15`, 章节 `4.2`
- 法律 `12315`, P1–P5 编号
- 货品代码 `NVIDIA 专业显卡`、`A100缺货`、`口头`、`独立`、`12 second`、TL;DR

---

## q3 — docs/contradiction_map.json

| 题中所列 | workspace 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema 字段 contradictions/id/title/source_a/evidence_a/source_b/evidence_b/resolved | — | json key 检查 | KEEP verbatim |
| C1/C2/C3 题目 (SKU/policy/refund) | order-history, package-tracking, product-listing, payment-records | grep `GPU-A100-80G\|A100`, `GPU-A40-48G\|A40`, 文件名 | KEEP A100/A40 二字符串；C1/C2/C3 编号必留 |
| `resolved=false` | — | 全部为 false | KEEP |
| 三大矛盾具体值（72,999 vs 32,000 等） | 全在初始 workspace | 仅检查 SKU 字符串 | STRIP — 改作语义指代 |

## q5 — docs/YYYY-MM-DD_initial_analysis.md

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| 文件名 `YYYY-MM-DD_*.md` 前缀 | P2 | glob | KEEP pattern |
| 订单号 `JD-618-2026-7891234` | order-history | grep | KEEP |
| 金额 `72,999` | payment-records | grep `72[,.]?999` | STRIP — agent 自查 |
| 日期 `2026-06-19` | package-tracking | grep | STRIP — 自查 |
| ≥3 ## headings | — | 数 heading | KEEP "三段以上" 之意 |

## q6 — docs/timeline.json

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema `events`, `event`, `timestamp` | — | json keys | KEEP |
| 八条事件示例 + 四个硬编码时间戳 | order/payment/package/RMA | grep 字面 `2026-06-18T10:02:33`, `10:02:45`, `2026-06-19T08:30:00`, `2026-06-20T14:15:00` | KEEP（grep 字面，强相关） |
| ISO `+08:00` | — | grep `T10:02:33` 含 T | KEEP "ISO 8601 +08:00" 提示 |
| ≥6 entries | — | len 检查 | KEEP "至少六条" |

## q8 — docs/spec_comparison.md

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| 文件 `docs/spec_comparison.md` | — | exists | KEEP |
| `72,999`、`74,999` 双价 | screenshot1/2 | grep 字面 | STRIP（agent 自查二截图）— 但因 grep 字面，**保留**为稳妥 → KEEP |
| 表头 `Field|Screenshot1_Value|Screenshot2_Value|Changed` | — | grep `^\|.+\|` | KEEP 表结构提示，列名可松 |
| 五字段（price/stock_status/...） | screenshots | 仅检查 stock + table | STRIP — agent 自填 |
| 有货/in stock | screenshots | grep `有货\|in.stock\|库存` | STRIP — 自查即得 |
| ≥2 ## | — | 数 | KEEP |
| P3 evidence-first | style | check_preferences P3 | STRIP — 以 P3 引之 |

## q9 — docs/source_decision.md (M6 negative assertion)

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| 截图1 `2026-06-18 10:00:15` | product-listing-screenshot.md | grep `2026-06-18`, `10:00:15\|截图\s*1` | KEEP `2026-06-18`、`10:00:15` |
| 截图2 时间 `2026-06-25` | append | — | STRIP — 自查 |
| 2分18秒间隔 | — | 无显式检查 | STRIP |
| **negative assertion**（截图2 不可作购买参照） | — | regex `(screenshot\s*2\|截图\s*2).*?(not\|cannot\|不得\|不能\|不适用\|不作为\|无效\|后来\|retroactive)` | KEEP — 必明示"截图2 不能作为购买时参照"之否定语 |
| ≥2 ## | — | 数 | KEEP |

## q10 — scripts/parse_delivery.py

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 `scripts/parse_delivery.py` | — | bash 运行 | KEEP |
| stdout schema (node_count/nodes/dispatch_time/receipt_time/transit_hours/all_internal_codes) | — | json 字段名硬检查 | KEEP verbatim |
| `node_count==3`, transit_hours `27.25` | package-tracking | 检查值 | KEEP `27.25` 验证目标 |
| dispatch/receipt 时间格式 `2026-06-19T08:30:00`, `2026-06-20T11:45:00` | — | grep 字面 in stdout | KEEP — 输出含此值 |
| `all_internal_codes` = `["GPU-A40-48G"]*3` | — | 字面比对 | KEEP `GPU-A40-48G` |
| 第一/二/三次发货分节 | package-tracking | — | STRIP — 自读 |

## q11 — docs/timeline_consistency_report.md

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| 三时间戳 `10:02:33`, `10:02:45`, `2026-06-19` | 各源 | grep 字面 | KEEP 三字面值 |
| `12 second` 间隔 | — | regex `12.*?(second\|秒)` | KEEP `12` + `second\|秒` |
| `22.46 hours` | 派生值 | 无强检查 | STRIP |
| ≥3 ## | — | 数 | KEEP |
| order→payment→dispatch 序 | — | 无 | KEEP 语义 |

## q12 — analysis/evidence_schema.json

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| 字段 `order_id`, `product_sku_ordered`, `product_sku_received`, `payment_amount_fen`, `rma_id`, `fraud_type` | — | json 字段硬检查 | KEEP verbatim |
| 各字段值 `JD-618-2026-7891234`, `GPU-A100-80G`, `GPU-A40-48G`, `7299900`, `RMA-2026-0620-001` | 各源 | == 比较 | KEEP（agent 须填确切值） |
| 枚举 `product_substitution\|description_mismatch\|both` | — | 集合校验 | KEEP |

## q14 — docs/financial_damage_report.md

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| `72,999`, `32,000`, `40,999` | payment-records, payment-detail-export | grep `72[,.]?999`, `32[,.]?000`, `40[,.]?999` | STRIP（自查）— 因 grep 字面，**保留**为稳妥 → KEEP（金额三件） |
| 退款流水 `2026062709300012345` | payment-detail-export | grep | KEEP |
| 表 `Item | Amount (CNY)` | — | grep `^\|.+\|` | KEEP 表结构 |
| 原价 `79,999`, 政策 `4.2` | — | 无检查 | STRIP |
| ≥3 ## | — | 数 | KEEP |

## q15 — docs/return_policy_analysis.md

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| 政策 `v3.2`, 日期 `2026-01-15` | return-policy.md | grep | KEEP |
| 章节 `2.2`, `4.2`, `4.3` | return-policy | regex `2\.2\|4\.2\|4\.3` | KEEP — 须列章节号 |
| 618 special terms 30 天 | return-policy | 无 | STRIP |
| 否定断言（无替换条款） | — | regex 否定 | KEEP "无 substitution clause" 之意 |
| ≥3 ## | — | 数 | KEEP |

## q16 — scripts/parse_payment.py

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 `scripts/parse_payment.py` | — | 运行 | KEEP |
| stdout schema (listed_price_fen/promotional_price_fen/refund_amount_fen/damage_fen/refund_transaction_id/refund_initiator/reconciled) | — | 字段硬检查 | KEEP verbatim |
| 期望值 7999900, 7299900, 3200000, 4099900 | 计算 | == | KEEP（数学约束） |
| 流水 `2026062709300012345` | export | == | KEEP |
| `merchant`, `reconciled=true` | — | == | KEEP |

## q17 — docs/seller_behavior_pattern.md

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| 三运单尾号 88761/88922/89103 | package-tracking | grep | KEEP 三号 |
| `NVIDIA 专业显卡` 标签 | package-tracking | grep `专业显卡\|vague` | KEEP `专业显卡` |
| `GPU-A40-48G` | package-tracking | grep | KEEP |
| 退款 `32,000` | payment-detail-export | grep | KEEP |
| RMA `RMA-2026-0620-001` | order-history | grep | KEEP |
| ≥3 ## | — | 数 | KEEP |

## q18 — docs/YYYY-MM-DD_midterm_evidence_report.md

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| 日期前缀 + `midterm/evidence/report` 文件名词 | — | glob | KEEP pattern + 词根 `midterm` |
| 订单号、72,999/32,000/40,999、运单流水 | 各源 | grep 字面 | KEEP（grep 字面） |
| ≥4 ## | — | 数 | KEEP |

## q20 — docs/courier_investigation_analysis.md

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| `GPU-A40-48G` | courier-evidence | grep | KEEP |
| `A100 缺货 / 库存` | courier-evidence | regex `A100.*?(缺货\|库存\|inventory\|zero)` | KEEP `A100` + `缺货` |
| `主管口头同意发A40替代` | courier-evidence | regex `口头\|oral\|verbal` | KEEP `口头`（更稳） |
| 日期 `2026-06-29` | courier-evidence | grep | KEEP |
| 三运单尾号 | courier-evidence | grep | KEEP |
| C1/C4 标签 | — | 无显式检查 | STRIP |
| ≥3 ## | — | 数 | KEEP |

## q21 — scripts/cross_validate.py

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| 路径 `scripts/cross_validate.py` | — | 运行 | KEEP |
| stdout 字段 `order_id_matches`, `amount_consistent`, `timeline_consistent`, `discrepancies` | — | 字段硬检查 | KEEP verbatim |
| 期望值（三 true + discrepancies 含 a40/a100） | — | == 与 substring | KEEP `GPU-A40-48G` 与 `GPU-A100-80G`（discrepancy 中要含 a40 或 a100） |

## q22 — docs/evidence_reliability_ranking.md

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| 排名顺序 5 类 | — | 仅检查 courier 高 + seller 低 + independent | STRIP 部分；KEEP "courier 最高、seller/CS 最低、independent third party" 三个语义钩 |
| `independent / 独立 / third party / 第三方` | — | regex | KEEP `independent` 或 `独立` |
| ≥4 ## | — | 数 | KEEP |

## q23 — analysis/complete_evidence_chain.json

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| schema (fraud_evidence/seller_claims/conclusion + 子字段) | — | 字段硬检查 | KEEP verbatim |
| 至少 4 fraud_evidence、含 courier-evidence.md | — | substring `courier` | KEEP `courier-evidence.md` 之提示 |
| 至少 2 seller_claims，全 `supported_by_evidence=false` | — | 全 false | KEEP `false` |
| reliability 枚举 high/medium/low | — | 集合 | KEEP |

## q24 — docs/legal_complaint_draft.md

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| 法律名 `消费者权益保护法` (or English) | — | grep | KEEP |
| Article 55 三倍赔偿 | — | 无（仅检查法名） | STRIP — 法常识 |
| 金额 `72,999` | — | grep | KEEP |
| `GPU-A100-80G` 与 `GPU-A40-48G` (or A100/A40) | — | grep `A100`, `A40` | KEEP A100/A40 |
| 章节 `4.2` | — | grep | KEEP |
| `12315` | — | grep | KEEP |
| ≥4 ## | — | 数 | KEEP |
| 时间线（2026-06-18 / 19/22/25 / 27） | — | 无具体检查 | STRIP |

## q26 — docs/YYYY-MM-DD_final_complaint.md (P1–P5 综合)

| 题中所列 | 源 | eval 检查 | 决策 |
|---|---|---|---|
| YYYY-MM-DD 前缀 + 含 `final/complaint` 之文件名 | — | glob + name regex | KEEP `YYYY-MM-DD_` + `final_complaint` 词 |
| `## TL;DR` | — | regex `## TL;DR` | KEEP `TL;DR` 字面 |
| TL;DR 内含 `JD-618-2026-7891234`, `72,999`, `40,999`, `A40` | — | grep 在 TL;DR 段 | KEEP 四值 |
| `72,999`, `40,999`, `32,000` | — | grep | KEEP |
| Clause `7.3` 反驳 | seller-email | grep `7\.3` | KEEP `7.3` |
| `消费者权益` | — | grep | KEEP |
| `12315` | — | grep | KEEP |
| markdown 表 | — | grep `^\|` | KEEP 表结构 |
| ≥5 ## | — | 数 | KEEP |
| 7-layer evidence chain | — | 无具体检查 | STRIP — agent 自串 |
| P1–P5 | check_preferences | — | KEEP P1-P5 编号 |

---

## 总体处理总结

- **STRIP 多者**：q3 矛盾细节、q5 部分日期金额、q8 双价（让位 grep 字面安全）、q14 原价、q22 排名细节
- **KEEP（grep 字面脆弱故）**：q5/q14/q18 之 `72,999/32,000/40,999`、q11 `12 second`、q20 `口头\|A100缺货`、q9 `截图2 否定`、q26 `TL;DR / 7.3 / final_complaint`
- **schema 字段名 verbatim**：q3, q6, q10, q12, q16, q21, q23
- **文件名/路径 verbatim**：所有题之路径

人物声口选择（多视赵磊本人独白；亦可借客服小刘/张师傅/老韩之转述）：
- q3, q5, q6: 赵磊自陈，简洁数据流（"我先把矛盾盘一下"）
- q8, q9: 赵磊比对截图，怀疑商家做手脚
- q10, q16, q21: 偏脚本工具自动化，赵磊量化交易员本色
- q11, q12, q14, q15: 证据规整，文档化
- q17, q18, q20, q22, q23: 中后期累积，老韩/张师傅旁证语融
- q24, q26: 法律维权，更正式

---

## v2 hardening notes

v1 太松，gpt-5.4 19/19 全过。v2 按四杠杆（A 去 P 标签 / B prose 化 schema / C 误导性 hedged distractor / D 删字面 grep 目标）逐题加压，目标 9–11 题易挂。

| 题号 | 主用杠杆 | 关键删除/改写 |
|---|---|---|
| q3 | B + D | schema 范例代码块改 prose；删 C1/C2/C3 强制编号、`A100`/`A40` 字面、`false` 字面、`>=3` 条要求；加 hedged distractor「应该是两条吧」 |
| q5 | A + D | 删 P1/P2/P3 标签、订单号字面、`72,999`、`2026-06-19`、`3 ##` 阈值；加 hedged「6 月 21 那天」误导日期 |
| q6 | B + D | 删示例 4 条 timestamp（`10:02:33` 等四值）、删 `+08:00` 字面、`order_placed` 等枚举值；加 hedged「10:02 整、几秒之后」 |
| q8 | A + D | 删 `72,999`/`74,999`/`有货`/P3 标签/列名英文 verbatim；改为「A100 在售/有库存」让 agent 自抄 |
| q9 | D | 删时间戳 `2026-06-18`/`10:00:15` 字面、删「截图 2 不能」预写否定句——agent 须自己组合「截图 2」+ 否定动词（被动认不出） |
| q10 | B + D | schema 改 prose；删 `27.25`/`GPU-A40-48G`/两个 timestamp 字面；加错误 hedged「三次都不一样」 |
| q11 | A + D | 删 P3 标签、`10:02:33`/`10:02:45`/`2026-06-19`/`12`/`秒` 字面；规则改「N 秒」抽象 |
| q12 | B | schema 整段 prose 化；保 `payment_amount_fen`（unconventional 单位）+ enum 三值；删 `JD-...`/`GPU-A100-80G`/`GPU-A40-48G`/`7299900`/`RMA-...` 字面 |
| q14 | A + D | 删 `72,999`/`32,000`/`40,999`/`2026062709300012345`/`4.2`/P4/`Item|Amount` 表头；加误导「12 位」位数提示 |
| q15 | A + D | 删 `v3.2`/`2026-01-15`/`2.2`/`4.2`/`4.3`/P3 字面；加误导「v3.5 左右」 |
| q16 | B | schema prose 化；保 7 个 unconventional 字段名（含 `_fen` 单位）；删 `7999900`/`7299900`/`3200000`/`4099900`/`merchant`/`true`/P4 |
| q17 | D | 删三运单尾号 `88761`/`88922`/`89103`、`专业显卡`、`GPU-A40-48G`、`32,000`、`RMA-...`、P3；加误导「总共四张运单」 |
| q18 | A + D | 删订单号、三金额、退款流水、P2/P5 字面；保 `midterm` 词根 |
| q20 | D | 删运单尾号、`GPU-A40-48G`、`A100缺货`、`口头`、`2026-06-29` 字面；改为指代「关于库存判断那个短语」/「授权方式那个限定词」 |
| q21 | B | schema prose；删 SKU 字面 `GPU-A40-48G`/`GPU-A100-80G`/`true` |
| q22 | A + D | 删 `independent`/`第三方` 字面；只留 SOUL.md 提示路径 |
| q23 | B | schema 部分 prose（保 unconventional 字段 `fraud_evidence`/`source_file`/`evidence_type`/`reliability`/`key_finding`/`seller_claims`/`supported_by_evidence`/`conclusion` + enum `high`/`medium`/`low`）；删 `false` 字面、`courier-evidence.md` 字面 |
| q24 | A + C + D | 删 `4.2`/`12315`/A100/A40/`72,999`/P5；加 hedged 错误「12345 那条线？」误导热线号 |
| q26 | A + D | 删 `JD-...`/`72,999`/`40,999`/`32,000`/A40/A100/`7.3`/`12315`/P1–P5；保 `## TL;DR`、`final_complaint` 词根；改「捏造的章节号」抽象指代 |

**预期挂题（≥9）**：q5（漏数字 grep）、q9（否定句结构错）、q10（错信「三次不一样」hedged）、q11（漏「秒」字面）、q14（漏退款流水/4.2/12 位 hedged）、q15（漏 `v3.2`/`2026-01-15`/章节号）、q17（漏 vague-label 中文短语）、q20（漏「口头」/「A100 缺货」）、q22（漏 `independent`/`第三方`）、q24（错抄热线号 12345 / 漏 4.2）、q26（漏 7.3 / 漏 12315 / 漏 A40 in TL;DR）。

**保留 verbatim（不能再松）**：所有路径、`payment_amount_fen` 等单位字段、`final_complaint` 词根、`midterm` 词根、`## TL;DR`、`fraud_type` 三个 enum 值、`high`/`medium`/`low` enum、各 schema 中 unconventional 字段名（reducer 硬索引）。

---

## v3 super-harden notes

v2 实测 81%（27 题挂 5：ec q10/q12/q22 + mc q2/q13），ec 还有 16 题 PASS。v3 选 5 题（q11/q14/q17/q18/q24）按 D++/C++/F/G 杠杆叠加加压，目标再挂 3–5 题。

| 题号 | v3 叠加杠杆 | 关键改动 |
|---|---|---|
| q11 | D++ + G + C++ | 删「下单到付款之间的间隔以「N 秒」明写」直白指令；改为要求一段「完整小句子表达"相隔了多少 + 单位"」抽象描述（agent 易写「instantaneously」/「立刻」漏「秒」单位）；加 hedged「立刻就过了——大概一两秒之间」「6 月 20 礼拜五」（错日期：实际 06-19）多重误导 |
| q14 | D++ + G + C++ | 把三笔金额从 enum 列表稀释为叙述「实际掏了多少、退回来了多少、净亏多少、原标价多少」一段散文；流水号叠加 3 重 hedged 误导（12 位/带 R 前缀/19 位左右）；章节号也虚化为「自己去翻 schema/policy 文件」 |
| q17 | G + C++ | 三件并排清单稀释为长段叙述；加 hedged「四张运单」+ 张师傅说「两张就够」干扰；面单短语加 hedged「专业级算力卡之类的」（错短语：实际「专业显卡」），易让 agent 照口述写 |
| q18 | G + C++ | 删金额三连 enum，改成段落「围绕这单各方资金流的几笔具体数额（实际付出去的、商家事后部分退回来的、净亏的——三笔要在正文里都能找到）」；订单号、运单号、流水号也稀释；加双重错误口述（"四万出头" / "三万多"）|
| q24 | F + C++ + G | 删 `return-policy.md` 文件名直引，改「`ls` workspace 自己找」；热线号叠加双重 hedged 误导（12345 政务线 + 12365 质监线）；章节号也只口述「按原文章节号引」无具体数字提示 |

**v3 预期新增挂题（目标 3–5 个）**：
- q11：漏「秒」/「second」字面（最易挂——抽象描述诱导 agent 用副词）
- q14：流水号位数被三重 hedged 误导写错；或漏其中一个金额
- q17：照口述写「专业级算力卡」漏「专业显卡」字面；或漏 RMA 完整编号
- q24：照 12345/12365 hedged 写错热线号；或找不到正确文件名漏 4.2 章节号
- q18：受口述误导写错损失金额，或漏其中一个数字（midterm 要求 4 ## 比 v2 q5 严）

**保留 verbatim**：所有路径、所有 schema 字段（`payment_amount_fen`/`fraud_type` 三 enum/`high|medium|low`/JSON 顶层 key 等 reducer 硬索引项）、`midterm` 词根、`final_complaint` 词根、`## TL;DR`。

**BROKEN 风险**：q24 的「workspace 里有材料明确写出该热线号」需 agent 实际能找到 12315 的字面出处（USER.md/退换货政策里应有）；若 workspace 无任何文件提及 12315，agent 必挂——但这与 eval 期望一致，属可接受。
