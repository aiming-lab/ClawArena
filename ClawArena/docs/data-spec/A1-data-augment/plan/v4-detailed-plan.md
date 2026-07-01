# v4 造数据详细计划

> 基于 v4-plan.md 场景选定 + difficulty-upgrade-guide.md + pitfalls.md 规范。
> 12 场景总轮数目标 **337 轮**（现有 7 场景 204 轮 + 新增 5 场景 **133 轮**）。

---

## 一、轮数分配

| 场景 | 域 | Updates | 总轮数 | MC | EC | EC比例 |
|------|----|---------|--------|----|----|--------|
| hil_f7 | 个人/家庭 | 4 | **27** | 8 | 19 | 70.4% |
| hil_g4 | 法律政策 | 4 | **27** | 8 | 19 | 70.4% |
| hil_c7 | 科技企业 | 4 | **28** | 8 | 20 | 71.4% |
| hil_h3 | 教育科研 | 4 | **27** | 8 | 19 | 70.4% |
| hil_e4 | 非盈利组织 | 3 | **24** | 7 | 17 | 70.8% |
| **合计** | | | **133** | **39** | **94** | **70.7%** |

> 现有6 EC场景均为30轮/8MC/22EC（73.3%）。新场景因轮数略少，EC比例在70–71%，满足≥70%要求。

**轮数推导逻辑**：
- 4-update场景：Phase 0（q1–q6=6轮）+ Phase1–3（各6轮）+ Phase4（q25–q27/28，3–4轮）= 27–28轮
- 3-update场景（e4）：Phase 0（q1–q6=6轮）+ Phase1–3（各6轮）= 24轮，Phase3即最终阶段

---

## 二、Phase结构模板

### 2.1 4-update 场景（f7/g4/c7/h3）

```
Phase 0  q1–q6   update前基线（3 MC + 3 EC）
Phase 1  q7–q12  upd1后         （1 MC + 5 EC）
Phase 2  q13–q18 upd2后         （1 MC + 5 EC）
Phase 3  q19–q24 upd3后         （1 MC + 5 EC）
Phase 4  q25–q27 upd4后收尾     （1 MC + 1 EC + 1 MC）   ← 27轮
         q25–q28 （c7）         （1 MC + 2 EC + 1 MC）   ← 28轮
```

MC布局：q1/q2/q4（基线+偏好）+ q7/q13/q19/q25（update触发）+ q27/q28（最终综合）= 8道

### 2.2 3-update 场景（e4）

```
Phase 0  q1–q6   update前基线（3 MC + 3 EC）
Phase 1  q7–q12  upd1后         （1 MC + 5 EC）
Phase 2  q13–q18 upd2后         （1 MC + 5 EC）
Phase 3  q19–q24 upd3后+综合收尾（1 MC + 4 EC + 1 MC）
```

MC布局：q1/q2/q4（基线+偏好）+ q7/q13/q19（update触发）+ q24（最终综合）= 7道

---

## 三、MC筛选策略

### 3.1 保留类型（从原30道MC中选8道）

| 类别 | 说明 |
|------|------|
| 开篇矛盾建立 | q1–q3中选2–3道：场景核心矛盾C1/C2/C3初判 |
| 偏好引入轮 | 通常q4：呈现P1–P5规则上下文 |
| Update触发轮 | 各update首轮MC：验证agent对新文件的第一反应 |
| 最终综合轮 | 最后一道MC：跨update全局裁决或元认知收尾 |

### 3.2 转EC类型

- "Generate X document, which elements should include" → EC（agent直接产出文件）
- "Format X per preferences" → 合并入EC的pref.command
- 同一Phase内连续两道MC → 保留一道，另一道改为EC

### 3.3 从原questions.json选MC

各场景原有30道（h3=25道）全MC。依据3.1原则：
- 每个update触发位置**必须保留MC**（update_ids非空的轮次优先用MC）
- q1/q2/q4通常直接保留
- 后段中段MC按"元认知/偏见修正"价值取舍

---

## 四、EC每题独立check脚本

**核心原则**（参照现有6个EC场景）：每道EC题对应 **1个专属 `check_*.py`** 脚本。

```
eval.command 典型形式：
  python ${eval_dir}/${agent_id}/scripts/check_xxx.py ${workspace}
  
  或（L3题，agent写脚本）：
  cd ${workspace} && python scripts/parse_xxx.py 2>&1 | python3 -c "
  import sys,json; d=json.load(sys.stdin)
  assert abs(d['field'] - expected) < tol, f'...'
  "
```

两种模式：
1. **evaluator check脚本**（`${eval_dir}/scripts/check_*.py`）：我们预写，验证agent产出的文件内容
2. **agent workspace脚本**（`cd ${workspace} && python scripts/xxx.py`）：agent写，eval直接运行并验证stdout JSON

多个验证需求用 `&&` 串联多个 check 脚本（每题最多2–3个，避免过多）。

**脚本复杂度要求**（对照现有场景）：
- check脚本须做**数值exact match**（`abs(val - expected) < tol`），不能只检查字段存在
- 关键词匹配用 `re.search(r'\bNUM\b', content)` 防假阳性
- 结构类EC须验证 `##` 标题数量（≥N个），防agent用空洞文本糊弄

---

## 五、pref 两段制

| Phase | 轮次 | 模式 | P规则 | 计分 |
|-------|------|------|-------|------|
| 教学期 | Phase 0–1（q1–q12） | pref字段附feedback | P1,P2（q5教学）；P3/P4（q8/q11教学） | 否 |
| 静默期 | Phase 2–4（q13–q27/q24） | 迁入eval.command | P1–P4（q18）；P1–P5（q26/q27最终） | 是 |

**各场景偏好P1–P5**（子计划阶段核实具体规则，参考原questions.json q4轮偏好描述）：

| 场景 | P1 | P2 | P3 | P4 | P5 |
|------|----|----|----|----|----|
| f7 | 时间戳精确格式 | 日期前缀文件命名 | 证据链优先叙事 | 定量精确 | 简洁无冗余 |
| g4 | 法律条款精确引用 | 日期前缀命名 | 结论先行 | 矛盾显式标注 | 风险量化 |
| c7 | ISO时间戳 | 文件命名规范 | 技术精确 | 影响范围量化 | 合规结论明确 |
| h3 | commit引用格式 | 日期前缀命名 | 证据链溯源 | 相似度量化 | 结论简洁 |
| e4 | 货币精确到分 | 日期前缀命名 | 现场优先视角 | 合规差额量化 | 多文件交叉引用 |

> 注：上表为初步分配，子计划阶段须读取各场景实际 workspace + 原 q4 内容后确认。

---

## 六、各场景 EC 题序设计要点

### 6.1 hil_f7 — 27轮，19 EC

**Ground Truth 数值表**（造题前必建，子计划阶段补充具体数值）：

| 事实 | 文件来源 | 精度 |
|------|---------|------|
| 订单金额（原价） | order-history-618.md | 分 |
| 实付款（扣除优惠后） | payment-records.md | 分（需完整还原多层抵扣） |
| 快递首节点时间戳 | package-tracking-log.md | 秒 |
| 商品参数（下单时版本） | product-listing-screenshot.md | 精确规格型号 |
| 商品参数（变更后版本） | product-listing-screenshot-append.md（upd1） | 精确规格型号 |
| 快递官方重量记录 | courier-evidence.md（upd3） | 克/公斤 |
| 支付手续费 | payment-detail-export.md（upd2） | 分 |

**难度机制 → check脚本设计**：

| 轮次 | EC类型 | 核心验证 | check脚本 |
|------|--------|---------|---------|
| q3 | L2 | 初步证据梳理JSON（3个矛盾点×来源文件） | `check_contradiction_map.py`（验证3个矛盾点字段） |
| q5 | L2+pref | [pref P1,P2] 初步分析报告（含订单金额精确值） | `check_initial_analysis.py` + `check_preferences.py` |
| q6 | L2 | 退换货时效计算JSON（下单→收货→申诉各时间差） | `check_timeline_json.py`（exact match时间差） |
| q8 | L2+pref | [pref P3] 产品规格差异分析（引用下单时截图 vs 更新版本） | `check_spec_diff.py` |
| q9 | L2 | M2裁决：下单时截图 vs 更新版截图，agent明确引用下单时版本 | `check_version_decision.py`（验证引用下单时版本+M6负向断言） |
| q10 | L3 | `scripts/parse_delivery.py`：解析快递日志→输出各节点时间差JSON | agent脚本stdout验证（时间差分钟精度） |
| q11 | L2 | M3跨文件一致性：订单时间/支付时间/快递首节点时间三源在维权时间线中一致 | `check_timeline_consistency.py` |
| q12 | L4 schema | M4：维权时间线JSON须含`order_ts`/`payment_ts`/`first_shipment_ts`/`rma_ts`枚举状态字段 | `check_timeline_schema.py` |
| q14 | L2+pref | [pref P4] 财务损失量化报告（原价/实付/差额精确到分） | `check_financial_report.py` |
| q15 | L2 | 消费者权益法适用分析（引用具体法条编号） | `check_legal_analysis.py` |
| q16 | L3 | `scripts/parse_payment.py`：解析支付明细→输出费用分解JSON（原价/优惠/手续费/实付） | agent脚本stdout验证（exact match各字段） |
| q17 | L2 | 卖家行为模式分析（3次发货+1次声明的时序模式） | `check_seller_pattern.py` |
| q18 | L2 | 综合中期报告（P1–P4全量，pref迁入eval.command） | `check_midterm_report.py` + pref |
| q20 | L2 | upd3快递官方调查整合：M6断言卖家声明不得作为商品符合描述依据 | `check_courier_integration.py` |
| q21 | L3 | `scripts/cross_validate.py`：跨文件验证订单/支付/快递三源一致性→输出差异JSON | agent脚本stdout验证 |
| q22 | L2 | 证据可信度排序报告（含快递官方数据 > 卖家声明的明确论证） | `check_evidence_ranking.py` |
| q23 | L2 | M4：完整证据清单JSON（字段：source/type/reliability_score/contradicts） | `check_evidence_schema.py` |
| q26 | L2 | 最终维权文件（P1–P5全量，计入eval.command） | `check_final_complaint.py` + pref全量 |

**M6 负向断言重点**：q9中验证agent未将`seller-response-email`（upd4）的主观声明用作"商品符合描述"结论。

---

### 6.2 hil_g4 — 27轮，19 EC

**Ground Truth 数值表**：

| 事实 | 文件来源 | 精度 |
|------|---------|------|
| PIP启动日期 | pip-email-chain.md | 精确到日 |
| 劳动法规定最短PIP通知期 | labor-law-reference.md | 天数 |
| days_shortfall（实际差额） | 计算值 | 天 |
| 1-on-1会议日期列表（HR版） | calendar-1on1-history.md | 各会议精确日期 |
| 1-on-1会议日期列表（孙伟版） | sunwei-1on1-notes.md（upd1） | 各会议精确日期 |
| 最终仲裁风险评估结论 | legal-updated-assessment.md（upd4） | 枚举值 |

**难度机制 → check脚本设计**：

| 轮次 | EC类型 | 核心验证 | check脚本 |
|------|--------|---------|---------|
| q3 | L2 | 案件矛盾地图JSON（C1:PIP合规/C2:1on1记录/C3:绩效评级各来源） | `check_contradiction_map.py` |
| q5 | L2+pref | [pref P1,P2] 初步PIP合规分析报告（引用lab-law条款编号） | `check_pip_prelim.py` + `check_preferences.py` |
| q6 | L2 | M1：PIP合规计算（实际通知天数 vs 法规要求，days_shortfall精确到天） | `check_pip_compliance_calc.py`（exact match days_shortfall） |
| q8 | L2+pref | [pref P3] upd1整合：1on1记录差异分析（HR版vs孙伟版，逐日期对比） | `check_1on1_diff.py` |
| q9 | L2 | M2裁决：calendar-1on1-history vs sunwei-1on1-notes，agent明确裁决哪个更可信+依据 | `check_1on1_decision.py`（验证裁决方向+M6） |
| q10 | L3 | `scripts/check_pip_timeline.py`：解析pip-email-chain + labor-law → 输出合规检查JSON | agent脚本stdout验证（days_shortfall exact match） |
| q11 | L2 | M3：PIP合规报告须同时引用law条款编号 + hr-file具体日期，check跨文件校验 | `check_cross_reference.py` |
| q12 | L2 | M4：法律风险JSON（`risk_level`枚举high/medium/low，`applicable_clause`字符串，`days_shortfall`数值） | `check_risk_schema.py` |
| q14 | L2+pref | [pref P4] upd2整合：孙伟书面异议分析（M6：异议不得作为HR违规确定性依据） | `check_sunwei_response.py` |
| q15 | L2 | PIP会议有效性分析（会议次数/议题完整性/书面确认记录，精确到次） | `check_meeting_validity.py` |
| q16 | L3 | `scripts/analyze_pip_process.py`：综合多文件分析PIP流程→输出合规差距JSON | agent脚本stdout验证 |
| q17 | L2 | 时间线重建报告（入职→绩效预警→PIP触发→解雇各节点精确日期） | `check_timeline_reconstruction.py` |
| q18 | L2 | 综合中期报告（P1–P4全量） | `check_midterm_report.py` + pref |
| q20 | L2 | upd3时间线分析整合：识别哪个关键节点缺失书面记录 | `check_documentation_gaps.py` |
| q21 | L2 | 利益相关方陈述可信度矩阵（HR经理/孙伟/张涛各陈述的文档支撑） | `check_credibility_matrix.py` |
| q22 | L2 | 系统性程序漏洞识别（至少2处，含具体条款引用） | `check_systemic_gaps.py` |
| q23 | L2 | 仲裁风险评估JSON（M4严格schema） | `check_arbitration_schema.py` |
| q26 | L2 | 最终调查报告（P1–P5全量，含days_shortfall精确数值） | `check_final_report.py` + pref全量 |

**M6**：q14验证agent未将`sunwei-written-response`（主观异议，无文档依据）用作"HR违规已确定"结论。

---

### 6.3 hil_c7 — 28轮，20 EC

**Ground Truth 数值表**：

| 事实 | 文件来源 | 精度 |
|------|---------|------|
| 漏洞首次被利用时间戳 | access_log_analysis.md（upd1） | 秒级 |
| 漏洞修复部署时间戳 | deployment_timeline.md（upd2） | 秒级 |
| 客户通知发送时间戳 | notification_final.md（upd3） | 秒级 |
| 监管通知窗口是否满足72h | 计算值（三时间戳推导） | bool + 小时精度 |
| CVSS评分 | vulnerability_technical_brief.md | float（如9.1） |
| 受影响端点数量 | api_endpoint_register.md | 整数 |
| 初估影响范围（客户数） | disclosure_report_initial.md | 整数（可能偏差） |
| 最终确认受影响客户数 | access_log_analysis.md（upd1后计算） | 整数 |

**难度机制 → check脚本设计**：

| 轮次 | EC类型 | 核心验证 | check脚本 |
|------|--------|---------|---------|
| q3 | L2 | 初步事件影响范围分析JSON（端点数/数据类型/初估客户数） | `check_impact_prelim.py` |
| q5 | L2+pref | [pref P1,P2] 事件时间线JSON（5个关键节点含ISO时间戳） | `check_incident_timeline.py` + `check_preferences.py` |
| q6 | L2 | 三方影响范围来源对比（api_endpoint vs customer_inventory vs disclosure_initial的数字差异） | `check_scope_conflict.py` |
| q8 | L2+pref | [pref P3] upd1整合：访问日志分析→精确暴露时间窗口 | `check_access_analysis.py` |
| q9 | L2 | M2裁决：三个影响范围估算来源，agent明确选定哪个最可信+依据 | `check_scope_decision.py`（验证裁决+M6） |
| q10 | L3 | `scripts/analyze_scope.py`：解析api_endpoint_register + customer_data_inventory → 受影响矩阵JSON | agent脚本stdout验证 |
| q11 | L2 | M3跨文件一致性：disclosure_report使用的数字须与api_endpoint/customer_inventory交叉吻合 | `check_disclosure_consistency.py` |
| q12 | L2 | 事件响应检查清单审计（incident_response_checklist.md逐项完成状态验证） | `check_checklist_audit.py` |
| q14 | L2+pref | [pref P4] upd2整合：部署时间线分析→漏洞引入版本到修复版本的完整追溯 | `check_deployment_trace.py` |
| q15 | L2 | M1：三时间戳计算（漏洞利用→修复→通知），暴露窗口小时数+72h合规判断 | `check_72h_compliance.py`（exact match小时数+bool） |
| q16 | L3 | `scripts/analyze_timeline.py`：解析access_log + deployment_timeline → 时间线JSON | agent脚本stdout验证 |
| q17 | L2 | 通知邮件版本对比（notification_draft_v1 vs notification_final的内容差异） | `check_notification_diff.py` |
| q18 | L2 | 综合中期报告（P1–P4全量） | `check_midterm_report.py` + pref |
| q20 | L2 | upd3整合：最终通知发送后的合规状态总结（含具体时间戳） | `check_compliance_summary.py` |
| q21 | L3 | `scripts/generate_breach_report.py`：综合多文件→输出漏洞报告JSON | agent脚本stdout验证 |
| q22 | L2 | 根因分析报告（含CVSS评分+受影响端点数+漏洞引入版本精确值） | `check_root_cause.py` |
| q23 | L2 | M4：漏洞影响JSON（`cvss_score`float/`affected_endpoints`数组/`notification_compliant`bool/`exposure_hours`float） | `check_breach_schema.py` |
| q24 | L2 | 利益相关方行动时间线（每个角色的关键决策时间戳） | `check_stakeholder_timeline.py` |
| q26 | L2 | 合规改进计划JSON（含具体截止日期） | `check_remediation_plan.py` |
| q27 | L2 | 最终事件报告（P1–P5全量，含所有精确数值） | `check_final_report.py` + pref全量 |

**M6**：q9中验证agent未将`disclosure_report_initial`（初期估算，数据不完整）作为最终客户影响数结论。

---

### 6.4 hil_h3 — 27轮，19 EC

**原场景25轮→扩充至27轮**（新增2道EC在Phase 0和Phase 4）。

**Ground Truth 数值表**：

| 事实 | 文件来源 | 精度 |
|------|---------|------|
| 王明首个相关commit时间戳 | git-commit-history-wangming.md | 分钟 |
| 陈伟GitLab最早相关commit时间戳 | git-commit-history-opponent.md | 分钟 |
| 陈伟GitHub仓库创建时间 | git-commit-history-opponent.md（upd1补充） | 日期时间 |
| 作业截止日期 | course-syllabus-integrity-policy.md | 精确日期时间 |
| MOSS相似度 | plagiarism-detection-report.md | 87% |
| 两提交时间差（分钟） | 计算值 | 分钟 |
| SO可解释相似度占比 | stackoverflow-answer-screenshot.md | 估算% |

**update顺序调整**：原h3 update编号非时序（upd4@q11先于upd3@q14），重排时统一为按时序注入：
- 原upd1 → 新upd1（@q7）；原upd2 → 新upd2（@q13）；原upd4 → 新upd3（@q19）；原upd3 → 新upd4（@q25）

**难度机制 → check脚本设计**：

| 轮次 | EC类型 | 核心验证 | check脚本 |
|------|--------|---------|---------|
| q3 | L2 | 初步证据可信度分类（客观证据vs主观陈述×来源文件） | `check_evidence_classification.py` |
| q5 | L2+pref | [pref P1,P2] 初步案例分析报告（引用MOSS 87%+git时间戳） | `check_case_analysis.py` + `check_preferences.py` |
| q6 | L2 | 两仓库对比JSON（GitLab vs GitHub，相关commit列表+时间戳） | `check_repo_comparison.py` |
| q8 | L2+pref | [pref P3] upd1整合：TA git对比笔记分析 | `check_ta_notes_analysis.py` |
| q9 | L2 | M2：MOSS 87%相似度（算法）vs SO公共解法可解释性（人工），agent裁决哪个解释更充分+量化SO覆盖% | `check_moss_vs_so.py`（验证裁决方向+覆盖百分比） |
| q10 | L3 | `scripts/parse_git_history.py`：解析双方git历史md→输出JSON（各commit时间戳/相似片段首现方/时间差分钟） | agent脚本stdout验证（时间差exact match） |
| q11 | L2 | M1：王明GitLab vs 陈伟对应commit时间差计算（分钟精度），确定谁在前 | `check_commit_timing.py`（exact match时间差） |
| q12 | L2 | 学术诚信政策适用性分析（引用课程政策具体条款） | `check_policy_application.py` |
| q14 | L2+pref | [pref P4] upd2整合：SO参考页面分析（能解释多少%的相似度） | `check_so_analysis.py` |
| q15 | L2 | 抄袭认定标准核查（按课程政策，87%相似+各证据权重） | `check_plagiarism_standard.py` |
| q16 | L3 | `scripts/analyze_similarity.py`：解析MOSS报告+SO截图→输出相似度来源分解JSON | agent脚本stdout验证 |
| q17 | L2 | 陈伟陈述演变分析（Phase1 vs Phase2 IM记录中陈述变化） | `check_chenwei_narrative.py` |
| q18 | L2 | 综合中期报告（P1–P4全量） | `check_midterm_report.py` + pref |
| q20 | L2 | upd3整合：TA解决方案（警告而非零容忍）合理性分析 | `check_resolution_analysis.py` |
| q21 | L2 | M4：`code_provenance_analysis.json`（`commit_owner`/`timestamp` ISO 8601/`source_confidence`枚举） | `check_provenance_schema.py` |
| q22 | L2 | M6负向断言：陈伟GitHub仓库（截止日期后创建）commit不得作为"陈伟先写"证据 | `check_github_exclusion.py` |
| q23 | L2 | 王明申诉建议文件（含git时间戳证据链） | `check_appeal_document.py` |
| q26 | L2 | 最终案例评估报告（P1–P5全量，含两提交时间差精确值） | `check_final_assessment.py` + pref全量 |

---

### 6.5 hil_e4 — 24轮，17 EC

**特殊说明**：e4原始questions.json中`update_ids`几乎每轮都有标注，但实际upd_workspace只有3个（upd1/upd2/upd3）。重排时严格区分：
- **workspace注入点**：仅q7/q13/q19三轮触发新文件到workspace
- **其余引用update_ids的轮次**：只是引用已注入的文件，update_ids字段仍可标注，但不是新注入点

**Ground Truth 数值表**：

| 事实 | 文件来源 | 精度 |
|------|---------|------|
| 各预算类别实际支出（USD） | financial_tracking_Q2.md | 分（$X,XXX.XX） |
| 各预算类别协议上限（USD） | grant_deliverables_annex_C.md | 分 |
| 各类别支出率（%） | 计算值 | 0.1%精度 |
| 人员名单人数 | hr_roster_nairobi.md | 整数 |
| 实际部署人天数 | staff_deployment_Q2.md（upd3） | 人天 |
| 人力成本（实际vs申报） | financial_tracking_Q2.md vs staff_deployment_Q2.md | USD精确到分 |
| 现场叙事活动人次 | nairobi_field_narrative_Q2.md | 整数（定性估算，M6来源） |

**难度机制 → check脚本设计**：

| 轮次 | EC类型 | 核心验证 | check脚本 |
|------|--------|---------|---------|
| q3 | L2 | 合规差异地图JSON（三源：财务追踪/叙事报告/Pemberton看板的数字差异） | `check_discrepancy_map.py` |
| q5 | L2+pref | [pref P1,P2] 初步合规分析报告（引用Annex C条款+财务追踪数字） | `check_compliance_prelim.py` + `check_preferences.py` |
| q6 | L2 | M1：各预算类别支出率计算（actual/approved×100%），精确到0.1% | `check_utilization_rates.py`（exact match各类别支出率） |
| q8 | L2+pref | [pref P3] upd1整合：Petrova初步评估分析（识别人员部署质疑点） | `check_petrova_analysis.py` |
| q9 | L2 | M2裁决：financial_tracking vs nairobi_field_narrative对同一人员活动的数字冲突，agent裁决哪个更可信 | `check_source_decision.py`（验证选财务文件+M6） |
| q10 | L3 | `scripts/analyze_budget.py`：解析financial_tracking_Q2 + grant_deliverables_annex_C → 支出率JSON | agent脚本stdout验证（各类别支出率exact match） |
| q11 | L2 | M3：合规报告须同时引用Annex C条款编号 + financial_tracking具体数字，check跨文件一致性 | `check_cross_reference.py` |
| q12 | L2 | David董事会通信分析（官方解释 vs 实际差异，识别解释中的信息缺口） | `check_board_comm_analysis.py` |
| q14 | L2+pref | [pref P4] upd2整合：waiver申请框架草稿（含具体差额数值） | `check_waiver_framework.py` |
| q15 | L2 | M4：合规状态JSON（`category`/`actual_usd`/`approved_usd`/`utilization_pct`/`compliant`bool） | `check_compliance_schema.py` |
| q16 | L2 | Pemberton官方回应草稿（引用Annex C条款+精确数字） | `check_pemberton_response.py` |
| q18 | L2 | 综合中期报告（P1–P4全量） | `check_midterm_report.py` + pref |
| q20 | L2 | upd3整合：人员部署记录分析（实际部署天数 vs HR名单 vs 财务成本三源交叉） | `check_deployment_analysis.py`（三源数值一致性） |
| q21 | L3 | `scripts/analyze_deployment.py`：综合解析hr_roster + staff_deployment + financial_tracking → 差异JSON | agent脚本stdout验证 |
| q22 | L2 | M6负向断言：nairobi_field_narrative（定性估算）的活动人次不得作为财务核查精确依据 | `check_narrative_exclusion.py` |
| q23 | L2 | 补救时间线JSON（各差异项的整改截止日期） | `check_remediation_timeline.py` |
| q24 | MC | 最终综合（跨update全局裁决） | MC |

---

## 七、脚本汇总（L3 agent脚本，每场景2–3个）

| 场景 | 脚本 | 触发轮 | 输出JSON关键字段 |
|------|------|--------|----------------|
| f7 | `scripts/parse_delivery.py` | q10 | node_times[]/delay_minutes/anomaly_flag |
| f7 | `scripts/parse_payment.py` | q16 | listed_price/coupon_total/platform_fee/actual_paid |
| f7 | `scripts/cross_validate.py` | q21 | order_ts/payment_ts/shipment_ts/consistent |
| g4 | `scripts/check_pip_timeline.py` | q10 | requirements[]/actual_dates/compliant/days_shortfall |
| g4 | `scripts/analyze_pip_process.py` | q16 | meetings_required/meetings_held/documentation_gaps[] |
| c7 | `scripts/analyze_scope.py` | q10 | endpoint_count/affected_records/data_type_matrix |
| c7 | `scripts/analyze_timeline.py` | q16 | exploit_ts/fix_ts/notify_ts/exposure_hours/compliant_72h |
| c7 | `scripts/generate_breach_report.py` | q21 | breach_summary/scope/timeline/compliance |
| h3 | `scripts/parse_git_history.py` | q10 | commits[]/first_appearance_owner/time_diff_minutes |
| h3 | `scripts/analyze_similarity.py` | q16 | moss_pct/so_explainable_pct/unexplained_pct |
| e4 | `scripts/analyze_budget.py` | q10 | categories[]/actual_usd/approved_usd/utilization_pct |
| e4 | `scripts/analyze_deployment.py` | q21 | person_days/labor_cost_actual/labor_cost_reported/discrepancy |

---

## 八、避雷要点（对照pitfalls.md）

1. **eval.command禁止通配符test -f**：文件存在检查移入check脚本内部（pitfalls §1.1）
2. **数值exact match**：`abs(val - expected) < tol`，不能只检查字段存在或"非零"（pitfalls §4.1）
3. **关键词防假阳性**：用`re.search(r'\bNUM\b', content)`（pitfalls §4.2）
4. **P2规则用"至少一个"**：不要求目录下所有文件都有日期前缀（pitfalls §2.1）
5. **L3脚本字段名精确对齐**：题目要求字段名与pytest断言字段名逐字核对（pitfalls §6.1）
6. **update触发轮后紧跟EC**：至少一道EC须明确引用新注入文件（pitfalls §7.2）
7. **workspace核实**：子计划阶段先`ls`实际目录，核实文件名（pitfalls §3.1）
8. **h3 update编号重排**：原upd3/upd4顺序非时序，子计划按实际注入顺序重新编号
9. **e4 update_ids区分**：原questions.json大量误用update_ids字段，子计划只在3个实际注入点设trigger

---

## 九、与现有场景的一致性

| 维度 | 现有6个EC场景 | 新增5个场景 |
|------|-------------|-----------|
| eval命令风格 | `python ${eval_dir}/${agent_id}/scripts/check_xxx.py ${workspace}` | 同上，保持完全一致 |
| L3 agent脚本命令 | `cd ${workspace} && python scripts/xxx.py 2>&1 \| python3 -c "..."` | 同上 |
| MC题type字段 | `"multi_choice"` | 同上 |
| EC题type字段 | `"exec_check"` | 同上 |
| update_ids格式 | `["upd1_sessions","upd1_workspace"]` | 同上 |
| pref字段结构 | `{command, expect_exit, feedback:{correct,incorrect}}` | 同上 |

---

## 十、执行顺序

| 顺序 | 场景 | 优先理由 |
|------|------|---------|
| 1 | hil_f7 | 数值类型最纯粹，建立电商类EC范式 |
| 2 | hil_g4 | 法律文件引用+时间线，难度适中 |
| 3 | hil_c7 | workspace最丰富，72h合规窗口是经典多时间戳验证题 |
| 4 | hil_h3 | git历史脚本最独特，需较多时间设计 |
| 5 | hil_e4 | 财务合规多源交叉最复杂，最后处理 |
