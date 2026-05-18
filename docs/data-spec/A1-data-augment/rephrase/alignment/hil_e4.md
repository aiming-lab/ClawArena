# Alignment Table — hil_e4

`exec_check` 题之 question-workspace-eval 三角对齐分析。每行：题中所列值 → workspace 真源 → eval 检查 → 处理决策。

**Round 可见性**：q3,q5,q6,q9,q10=initial · q8,q11,q12=after upd1 (Petrova 文件可见) · q14,q15,q16,q17,q18=after upd2 (David board) · q20,q21,q22,q23=after upd3 (Sophie deployment)

**Persona 选派**（USER.md）：Fatima（Program Director，主用户）；其余皆她团队。多数 ask 当为 Fatima 自己拟、或她转他人之求；语气随渠道而异：Feishu (#grant-review) 半正式偏机构；Slack DM with Sophie 同侪略松；Telegram with James 现场口语；Discord with Petrova 谨慎。

**保全清单（任题不可动）**：输出路径、JSON schema 字段名、enum 值、Annex C/PEM-XX-01 活动码、Section 6.1/6.3、grep 字面（如 `14` day, `37,000`, `39.4`, `58`, `63`, `409,000`, `0.98`, `47`, `Q2`, `non-compliant`, `over/under/on_track`）。

---

## q3 — docs/compliance_discrepancy_map.json (initial)

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| schema 6 字段 (id/source_a/source_b/field/value_a/value_b/severity) | — | check_q3：indexes by these keys | KEEP |
| severity enum `critical/moderate/minor` | — | enum 校验 | KEEP |
| `>=3 discrepancies` | — | len check | KEEP |
| 至少一 `critical`（暗示 mobilization 超支） | financial_tracking_Q2.md (Line 3) | 必有 critical | KEEP（"Mobilization overspend" hint 留）|
| 不得引 upd 文件 | — | （无显式检查，但题中要求）| 改作 round 限定语 |

## q5 — docs/YYYY-MM-DD_initial_compliance_analysis.md (initial)

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| 文件名 `YYYY-MM-DD_*.md` 在 docs/ | — | regex 校验 | KEEP pattern |
| ≥2 budget categories by name | financial_tracking_Q2.md | 名字 grep | STRIP — 让 agent 读源自填 |
| actual vs approved 数额 | 同上 | grep `409/115/131/178/87`千 | STRIP |
| over/under/on-budget 状态 | — | grep status 词 | KEEP 语义"标注超/欠/在容差内"|
| Annex C 引 | grant_deliverables_annex_C.md | grep `Annex C\|PEM-` | KEEP "Annex C 任一交付类别" |
| ≥3 ## headings | — | count | STRIP（结构由 agent 自决，但 P1/P2 隐含）|
| P1, P2 prefs | — | check_preferences | KEEP（点名 P1/P2 暗示）|

## q6 — analysis/budget_utilization.json (initial) — M1

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| 5 类别精确数 (409/412, 115/148, 131/94, 178/189, 87/90) | financial_tracking_Q2.md | check_q6 严核 util_pct 公差 0.15 | STRIP — 删题中"five categories and exact values"块；让 agent 自读财务表 |
| schema 字段 (name/actual_usd/approved_usd/utilization_pct/status) | — | strict | KEEP |
| status 规则 (>100→over, <90→under, 90-100→on_track) | — | enum 校验 | KEEP |
| 输出路径 `analysis/budget_utilization.json` | — | 必检 | KEEP |

## q8 — docs/petrova_assessment_analysis.md (after upd1)

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| `39 workshops`、`58%`、`63%` | petrova_assessment_prelim.md | grep `39/58/63` 字面 | KEEP at least one literal hint（pilot pattern: 字面 grep 必留）→ 实际可让 agent 自取，但因 grep `\b39\b` `\b58\b` `\b63\b` 字面，**保 "specific findings with exact numbers" 提示语**且**不在题中明示数字**——agent 读 Petrova 报告即得 39/58/63；故 STRIP 数字本身。 |
| Sophie 68-72% 对照 | message_logs/me_sophie_slack.md / USER.md ("~68-72%") | grep `Sophie\|68\|72\|verified` 任一 | STRIP — agent 读 USER.md 自得 |
| Petrova flagged categories | petrova_prelim | 无具体值检查 | STRIP |
| recommendation = use 58% conservative | petrova_prelim | 无字面检查（仅 explain gap）| STRIP |
| ≥3 ## headings | — | count | KEEP "结构 ≥3 ##" |
| P3 pref | — | check_preferences P3 | KEEP P3 标签 |

> 风险：grep 字面 `\b39\b`、`\b58\b`、`\b63\b`。若 agent 漏其一即败。Petrova 文件里这三个数都很显眼，agent 读完应能复述；不强行明示。

## q9 — docs/source_reliability_decision.md (initial) — M2/M6

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| 选 financial vs nairobi_field_narrative_Q2.md | 文件本身 | grep `financial.*reliable\|authoritative` 等 | KEEP 文件名 nairobi_field_narrative_Q2.md（因 grep 字面） |
| M6 negative assertion: 须明言 narrative 非权威 | — | regex 含 not/cannot/excluded | KEEP "explicit negative assertion" 框架 |
| approximate/qualitative 例子 | nairobi_field_narrative_Q2.md ("approximately 200", "85-95%", "680-700") | grep `approximately\|85.95\|680.700\|expect` | STRIP 具体例 — 让 agent 引证 |
| ≥2 ## headings | — | count | STRIP |

## q10 — scripts/analyze_budget.py (initial)

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| 5 类别精确数 | 同 q6 | inline jq-like assert: Mobilization actual=131000/approved=94000/compliant=False, total=920000/933000 | STRIP — agent 读财务表自得；保 `Community Mobilization` 名 |
| schema 字段 (categories/actual_usd/approved_usd/utilization_pct/compliant/overall_compliant/total_actual_usd/total_approved_usd) | — | inline check | KEEP |
| 路径 `scripts/analyze_budget.py` | — | 必检 | KEEP |
| 运行入口 `python scripts/analyze_budget.py` | — | 必检 | KEEP |
| compliant=true if util_pct<=100 | — | inline 假设 Mob=False | KEEP 规则 |

## q11 — docs/cross_reference_report.md (after upd1) — M3

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| 三文件名引：financial_tracking_Q2.md / pemberton_dashboard_Q2.md / pemberton_grant_agreement_excerpt.md | initial | grep 三文件名根 | KEEP 三文件名（grep 字面） |
| 比较具体值（933,000/412,000/148,000/94,000/189,000/90,000/39.4/22.3/45%）| financial_tracking_Q2.md / dashboard | grep 任一 | STRIP — agent 自比 |
| ≥3 ## headings | — | count | KEEP 结构提示 |

## q12 — analysis/compliance_status.json (after upd1) — M4

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| schema (compliance_report/reporting_period/categories/overall_status/petrova_flagged_items + 子字段) | — | 严核 | KEEP 全 schema |
| `reporting_period`=`Q2` | — | 必检 | KEEP "Q2" |
| 5 categories | — | len check | KEEP |
| `overall_status`=`non-compliant` | — | 必检 | KEEP enum + 含此值 |
| Mobilization util ~139.4% | — | 必检 | KEEP 139.4 字面（pilot 之 q22 `39,426` 模式） |
| `petrova_flagged_items` ≥1 | — | len check | KEEP 字段名 |
| enum `compliant/non-compliant/at-risk` | — | enum 校验 | KEEP |

## q14 — docs/board_communication_analysis.md (after upd2)

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| David Ochieng 引 | david_board_communication.md | grep `David\|Ochieng` | KEEP（首次提名后可改间接） — 此为 david 文件主分析，须留人名 |
| `14` calendar days | david_board_communication.md | grep `\b14\b.*day` 字面 | KEEP "14 calendar days" 字面（pilot 同模式） |
| waiver 词 | david_board | grep `waiver` | KEEP |
| 个人 vs 委员会区分 | david 文 Personal Note 段 | regex personal/committee | STRIP — 引导而不明示 |
| ≥3 ## headings | — | count | KEEP |
| P4 pref（隐含；本题 pref=null）| — | — | n/a |

## q15 — docs/waiver_justification_framework.md (after upd2)

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| Section 6.1/6.3 | pemberton_grant_agreement_excerpt.md | grep `Section 6.1\|6.3` 字面 | KEEP（grep 字面）|
| `$37,000` overspend | financial_tracking_Q2.md（131-94=37000）| grep `37[,.]?000\|37,000` | KEEP（pilot 之 39,426 模式：金额字面）|
| `39.4` 或 `39%` | financial_tracking_Q2.md | grep | KEEP `39.4%` 字面 |
| 三 waiver 组件（operational just / enrollment impact / future compliance）| david_board | regex 至少 2 个 | STRIP 具体——引"david 列出之三组件" |
| verbal authorization 不满足 written approval | grant_agreement S6.1 | 无字面检查 | STRIP — 隐含 |
| ≥3 ## headings | — | count | KEEP |

## q16 — analysis/field_narrative_vs_financials.json (after upd2)

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| schema (activity_comparisons/activity/narrative_count/financial_allocation_usd/cost_per_unit_if_calculable) | — | 严核 | KEEP |
| 4 活动详列 + 数字 (47/542/115K/131K/178K/409K) | nairobi_field_narrative_Q2.md + financial_tracking_Q2.md | check_q16: training=115000,mob=131000,training narrative_count==47, ≥1 null | STRIP 详表——让 agent 自读两源；保 schema + 至少一 `null` 之 qualitative 提示 + `47` workshops 字面（因 narrative_count==47 必须）|
| ≥3 entries | — | len check | KEEP |

> 风险：narrative_count==47 字面校验。题中保留 `47` 作为 educator workshops 计数（field_narrative 明文），稳妥。

## q17 — docs/pemberton_formal_response_draft.md (after upd2)

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| Annex C 或 PEM-* | annex_C | grep | KEEP "Annex C" |
| `$37,000` 或 `39.4%` | finance | grep | KEEP 一者 |
| `58` 或 `63` | petrova | grep | KEEP 暗示 Petrova 数 — 但 grep `\b58\b\|\b63\b`，agent 应能从 Petrova 复述；不在题中明示数字，留"Petrova 之核证完成率"指引 |
| waiver | — | grep | KEEP |
| documentation improvement | david_board | grep `documentation.{0,30}(improvement\|plan)` | KEEP "documentation improvement plan" 字面 |
| ≥4 ## headings | — | count | KEEP |
| P1 pref | — | （本题题干言 P1）| KEEP P1 标签 |

## q18 — docs/YYYY-MM-DD_midterm_compliance_report.md (after upd2)

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| 文件名 date prefix 在 docs/ | — | regex | KEEP pattern |
| ≥2 utilization % (99.3/77.7/139.4/94.2/96.7) | analysis/budget_utilization.json (q6 已建) | grep | STRIP 具体——agent 用 q6 输出 |
| `58` and `63` Petrova | petrova | grep both | KEEP 暗示但留"Petrova 数"语义；因 `\b58\b` 与 `\b63\b` 须皆现，**保留 Petrova 范围语义提示** |
| `non-compliant` | — | grep | KEEP `non-compliant` 字面 |
| `14` `day/calendar` | david | grep | KEEP `14 calendar days` |
| ≥4 ## headings | — | count | KEEP |
| P1-P4 prefs | — | 题干提及 | KEEP |

## q20 — docs/deployment_vs_financial.md (after upd3)

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| `14` staff | hr_roster + staff_deployment_Q2.md | grep `\b14\b.{0,30}(staff\|person)` | KEEP `14 staff` 语义 |
| `$409,000` | finance | grep | KEEP `$409,000` 字面 |
| 29,214.29 per-person | derive 409000/14 | grep `29[,.]?214\|per.{0,20}staff` | STRIP 数字——agent 自算 |
| `0.98` workshops/officer/month | staff_deployment_Q2.md | grep `0\.98\|plausib` | KEEP "plausibility calculation" 引；因 `0.98` 字面或 `plausib` 词皆可 |
| Annex C caveat | staff_deployment Important Caveat | regex | KEEP "Annex C documentation caveat" 引 |
| ≥3 ## headings | — | count | KEEP |

## q21 — scripts/analyze_deployment.py (after upd3)

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| 精确常量 (14/14/409000/29214.29/true/true) | hr_roster + deployment + finance | inline assert 全字面 | STRIP "key facts to encode" 块详表——让 agent 读三源、算 29214.29；保 schema + 路径 + 运行入口 |
| schema 6 字段 | — | inline check | KEEP |
| `scripts/analyze_deployment.py` 路径 | — | 必检 | KEEP |
| `python scripts/analyze_deployment.py` 入口 | — | 必检 | KEEP |

## q22 — docs/narrative_exclusion_analysis.md (after upd3) — M6

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| `nairobi_field_narrative_Q2.md` | initial | regex `(field narrative\|nairobi_field_narrative\|narrative).{0,80}(not\|cannot...)` | KEEP "field narrative" 词 |
| 至少 2 例 qualitative 语 ("approximately 200" / "85-95%" / "680-700") | narrative | regex 任 1 即可 | STRIP — 让 agent 自引；但因须 ≥1 例显形，保半显"narrative 中之约略语（"approximately X"、"X-Y%" 类）"提示 |
| `financial` 作权威源 | — | grep `financial` | KEEP |
| M6 negative assertion | — | regex | KEEP 框架 |
| ≥2 ## headings | — | count | KEEP |

## q23 — docs/remediation_action_plan.md (after upd3)

| 题中值 | 源 | eval | 决策 |
|---|---|---|---|
| Section 6 / Annex C / grant agreement | grant_agreement, annex_C | grep | KEEP 引语 |
| ≥1 责任人名 (Fatima/James/Sophie/Rachel/titles) | USER.md / 各 sessions | grep | STRIP — agent 自配 |
| timeline (14 day / 30 day / Year 3) | david_board / annex_C | grep | KEEP "14 calendar days" |
| ≥3 ## headings + ≥3 gaps (mobilization/educator-training/infrastructure) | — | regex | KEEP "三 compliance gaps"（mobilization waiver、educator training documentation、infrastructure co-signatures） |

---

## 总结

- **完全 STRIP 具体值**：q5（金额、类别名）、q6（5 类详值）、q8（39/58/63）、q9（qualitative 例）、q10（5 类详值）、q11（具体比对值）、q15（三组件细节）、q16（4 活动详表）、q18（util %）、q20（29214）、q21（key facts 详表）、q22（具体例）、q23（责任人）
- **KEEP 字面**：q3 schema、q5 P1/P2 + Annex C、q6 schema、q9 nairobi_field_narrative_Q2.md、q10 schema + 入口、q11 三文件名、q12 全 schema + Q2 + non-compliant + 139.4 + petrova_flagged_items、q14 14 calendar days + waiver + David、q15 Section 6.1/6.3 + 37,000 + 39.4%、q16 schema + 47、q17 Annex C + waiver + documentation improvement plan、q18 date pattern + non-compliant + 14 day、q20 14 staff + $409,000 + plausibility、q21 schema + 入口、q22 field narrative + financial + M6、q23 Section 6/Annex C + 14 calendar days + 三 gaps
- **persona 选派**：q3,q5,q6,q9,q10—Fatima 首日自记/给 Sophie 委托（Slack）；q8—Fatima 接 Petrova Discord 后自记，谨慎；q11,q12—#grant-review Feishu 半正式；q14,q15,q17,q18—Fatima 自拟，给 Pemberton 之事，正式；q16—与 Sophie/Rachel Slack；q20,q21—Sophie 协作 M&E 口吻；q22—Fatima 内部立场文；q23—收尾跨人，Feishu。

---

## v2 hardening notes

v1 之 17 ec 题，gpt-5.4 全胜（100%）。v2 加固欲压至 ~50-60%。 levers 用法：

- **A（剥 P-rule 标签）**：q5、q8、q14、q17、q18 — 全删 `P1/P2/P3/P4` 标签，代以"team's house style / framing convention / standard ordering"等模糊语。round.preferences 字段为 None，故 check_preferences 实未触发，标签纯为心理提示——剥之逼 agent 自悟结构。q5/q18 之 `YYYY-MM-DD_` 模式仍保（check_q5/q18 严核 regex）。
- **B（schema 散文化）**：
  - q3：删整个 ```json``` 块；散述 id/source_a/source_b/field/value_a/value_b/severity，亦不直名 `discrepancies` 顶级 key——agent 须凭"plural noun, conventional snake_case"自得。
  - q6：删 schema 块；散述 categories/name/actual_usd/approved_usd/utilization_pct/status；status enum 仍字面（over/under/on_track 须严核）。
  - q10：删 schema 块；散述全字段；`compliant`/`overall_compliant` 字面留（agent 不易自创）+ 入口字面留。
  - q12：删 schema 块；散述大多字段；保 `compliance_report`（顶级 wrapper 不可猜）+ enum 三值 + `petrova_flagged_items`（非常规名）。
  - q16：删 schema 块；散述全字段；保 unconventional 字段名 `activity_comparisons`、`narrative_count`、`financial_allocation_usd`、`cost_per_unit_if_calculable`（agent 难独自得）。
  - q21：保留 schema 散文化但全字段名字面留——皆非常规复合名。
- **C（误导线索）**：q3（Rachel 不确 mobilization 是否最大）、q5（Rachel "60%" 错忆）、q6（Sophie 错称四线 under）、q8（James 错称 Petrova "70%"）、q10（Rachel 错称两线 fail，实仅一）、q11（Rachel 错称 dashboard "8%" 差）、q14（Rachel 错忆 21 天）、q15（Sophie 错忆 email trail）、q16（James 错称 workshop 约 50）、q20（Sophie 错忆 1.2/月）、q21（Rachel 错忆 financial-vs-deployment fail）、q23（Sophie 错忆 21 天）—— 皆 hedged "I think / not sure / might / maybe"。
- **D（删字面 grep target）**：
  - q3：删 `Community Mobilization`、删三文件名（让 agent 自寻）。
  - q5：删类别名详列、删 USD 数（409K/115K/...）。
  - q8：删 `Petrova/Sophie/P3/##` 字面提示——眼前不能直接 hint Petrova 名。
  - q9：删 `nairobi_field_narrative_Q2.md` 字面、`Annex C`字面、`##` 字面——agent 自达。
  - q11：删三文件名 `pemberton_dashboard_Q2.md`/`pemberton_grant_agreement_excerpt.md`/`financial_tracking_Q2.md`、删 `##`。
  - q12：删 `Q2`、`reporting_period`、`categories`、`category` 等字面字段名、删 `non-compliant`/`Community Mobilization` 暗示——agent 须自算 `non-compliant`。
  - q14：删 `David`、`14 calendar days`、`##` 字面——agent 自读 david_board_communication.md。
  - q15：删 `$37,000`、`39.4%`、`Section 6.1`、`Section 6.3`、`pemberton_grant_agreement_excerpt.md`、`##` 字面。
  - q16：删 `47`、`null` 字面、`financial_tracking_Q2.md`。
  - q17：删 `$37,000`、`39.4%`、`Petrova`、`P1`、`Annex C`、`##`、`PEM-` 字面。
  - q18：删 `_midterm_compliance_report.md`、`P1-P4`、`Petrova`、`non-compliant`、`14 calendar days`、`##`。
  - q20：删 `14`、`$409,000`、`financial_tracking_Q2.md`、`Annex C`、`##`。
  - q21：删 `hr_roster_nairobi.md`、`financial_tracking_Q2.md`。
  - q22：删 `nairobi_field_narrative_Q2.md`、`financial`、`Annex C`、`##`。
  - q23：删 `Section 6`、`Annex C`、`14 calendar days`、`##` 字面。

**预期失败方向**：q5（USD 数缺）、q8（Petrova 39/58/63 须自取，加 70% 误导）、q11（具体 dollar 比较易漏 + 8% 误导诱导写错）、q12（散文 schema → 顶层 wrapper 易错；at-risk 误导）、q14（21-day 误导）、q15（37K/39.4 须自算）、q16（narrative_count==47 须读）、q17（多 grep target 累积）、q18（多字面累积+21-day 风险）、q20（29214/0.98 自算+1.2 误导）。 大致 8-10 题易踩雷。

**最重保留**：q3 enum、q12 enum + wrapper 名、q16 unconventional schema、q21 全 schema、各题输出路径。

**风险/可能 BROKEN**：q3 `discrepancies` 顶 key 改作"plural noun for the rows" 散文——若 agent 误起复数同义词（"items"/"differences"），即败 schema 检查。此为 Lever B 内合理冒险。q12 散文 schema 同理。q16 散文虽留四常用字段名字面，仍可能漏某字段（合理冒险）。
