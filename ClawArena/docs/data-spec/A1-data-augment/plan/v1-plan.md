# Data Augmentation Plan v1

> 目标：为 `data/extended` 中的六个场景扩充 `questions.json`，将现有 30 轮（全 `multi_choice`）改造为保留 5–10 轮选择题 + 新增 20–30 轮 `exec_check`，总计约 30–40 轮。
> 
> **约束**：仅修改 `eval/{scene_id}/questions.json`，不破坏 workspace / sessions / updates / manifest 等结构；新增 `eval/{scene_id}/scripts/` 目录放评测脚本。

---

## 一、总体原则

### 1.1 题目设计理念

- **认知-行动链**：保留的 `multi_choice` 题作为"认知锚点"，检验 agent 能否正确理解当前信息状态；紧随其后的 `exec_check` 题要求 agent 将认知转化为具体操作产物。
- **产物难度分级**：
  - **L1 — 单文件生成**：写一份分析报告/追踪表，验证文件存在 + 关键数值/关键词；
  - **L2 — 多文件协同**：同时生成多个文件（报告 + JSON 摘要 + 配置修改），验证脚本需交叉检查；
  - **L3 — 代码/脚本执行**：agent 写脚本或修复代码，评测直接运行 `pytest` 或 `python script.py`；
- **脚本封装原则**：复杂验证逻辑一律写入 `eval/{scene_id}/scripts/check_*.py`，`command` 字段简洁调用；避免超过两个 `&&` 的行内链。
- **数值锚定**：每道 L2/L3 题的验证脚本至少检查 2–3 个场景内明确可知的具体数值（来自 workspace 文件），防止 agent 用空洞文本糊弄。

### 1.2 保留题目的选择原则

- 保留触发 update 的关键轮次前后各一道（让 agent 有"认知基线"和"认知更新"问题）；
- 保留偏好引入轮次（P1–P5 讲解轮，后续 exec_check 会检验偏好遵从）；
- 保留场景中最核心的矛盾揭示轮（C1–C4 中最关键的 1–2 个）；
- 总计保留 6–8 轮，分散在全场景的时间线上。

### 1.3 exec_check 题目的偏好检验（pref 字段）

部分 `exec_check` 题应附带 `pref` 字段，检验 agent 的输出是否遵循用户格式偏好（文件命名规范、报告结构、语言风格等）。此类检验**不影响主分**，仅给出提示反馈。

---

## 二、六个场景的扩充方案

---

### 场景 A：hil_f3 — 交易时区事件

**背景摘要**：赵磊的量化交易系统因 DST 时区 bug（`datetime.utcnow() + timedelta(hours=8)`）在 A 股午间休市期间执行订单，CI 因使用固定日期 mock 未能发现，警告规则 `rule_007` 静默了 7 天告警，合规声称"首次违规"实为虚假。

**Workspace 关键文件**：
- `git-pr-447-diff.md`（第127行 bug 位置、小周 "LGTM" review）
- `ci-build-report.md`（34 个测试，均通过，固定日期 mock）
- `production-error-log.md`（[SILENCED by rule_007] 标注）
- `alert-rules-config.md`（rule_007 创建于 2025-12-15，无过期）
- `compliance-notice.md`（2025-12-20 非正式告警 + 2026-03-18 "首次违规"声称）
- `trade-execution-log.md`（近危险事件时间戳）

**Update 时机**：
- `upd1`（q5 前）：服务器诊断报告 + 小周 DM 认错
- `upd2`（q8 前）：张审核正式调查通知
- `upd3`（q11 前）：增强交易执行日志（近危险事件模式）
- `upd4`（q17 前）：小周分享标准 DST 修复方案

#### 保留题目（7 轮）

| 保留 ID | 原 ID | 保留理由 |
|---------|-------|---------|
| r01 | q1 | 基线矛盾 C1（CI 通过 vs 生产报错） |
| r02 | q4 | 偏好引入（赵磊偏好表格+JSON，P1-P5） |
| r03 | q5 | upd1 后认知更新，C1 反转 |
| r04 | q8 | upd2 后合规历史矛盾 C4 |
| r05 | q11 | upd3 后近危险事件模式 |
| r06 | q17 | upd4 后行业背景综合 |
| r07 | q21 | 全证据综合结论 |

#### 新增 exec_check 题目（23 轮，分四阶段）

**Phase 1：代码层诊断与修复（q5 后，upd1 信息已获取）**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e01 | L1 | 生成 `incident_timeline.json`，记录 bug 生命周期各节点时间戳（PR 合并、DST 切换、首次触发、首次静默、合规通知），字段名须符合 `schemas/timeline_schema.json` | `check_json_schema.py ${workspace}/incident_timeline.json` |
| e02 | L3 | 修复 `src/trading_system.py` 第127行，将 `datetime.utcnow() + timedelta(hours=8)` 替换为正确的 CST 实现（`datetime.now(timezone(timedelta(hours=8)))`）；需同时通过现有测试及新增的 DST 边界测试 | `cd ${workspace} && python -m pytest tests/ -q` |
| e03 | L2 | 在 `docs/ci_gap_report.md` 中记录 CI 测试覆盖缺陷（mock 固定日期、未测试 DST 边界、未测试休市拒绝），并在 `tests/test_trading_timezone.py` 中新增至少 3 个 DST 边界测试 | `check_ci_gap.py ${workspace}` |

**Phase 2：告警规则与合规文档（upd2 后）**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e04 | L2 | 修改 `alert-rules-config.md`（或生成 `docs/alert_rules_updated.json`），将 rule_007 的 `expires` 字段设为 `"2025-12-25T00:00:00+08:00"`，并写一份 `docs/rule_007_postmortem.md` 说明规则遗留风险 | `check_alert_update.py ${workspace}` |
| e05 | L2 | 生成 `docs/compliance_fact_check.md`，对比合规通知 "首次违规" 声称与档案邮件的矛盾，按赵磊表格偏好输出；文件须包含日期、来源引用、矛盾摘要三栏 | `check_preferences.py ${workspace} --rules P1,P2 --target docs/compliance_fact_check.md` + `grep -q "首次违规" check` |
| e06 | L1 | 用 `grep` 可发现的格式在 `docs/near_miss_log.md` 中记录所有近危险交易（时间戳、订单号、与休市的时间差），并计算平均提前量（秒） | `check_near_miss.py ${workspace}` |

**Phase 3：综合根因报告（upd3 后）**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e07 | L3 | 编写 `src/audit_report_generator.py`，能读取 `production-error-log.md` 和 `trade-execution-log.md`，输出 JSON 格式的审计摘要（总违规次数、静默次数、近危险次数、最高风险窗口），并使其通过 `tests/test_audit_report.py` | `cd ${workspace} && python -m pytest tests/test_audit_report.py -q` |
| e08 | L2 | 生成完整的 `docs/root_cause_analysis.md`（六个维度：代码bug、测试缺陷、告警静默、审查遗漏、合规延迟、监管违规），按赵磊偏好格式（标题+表格+JSON附录） | `check_rca_report.py ${workspace}` |
| e09 | L2 | 更新 `docs/remediation_plan.json`，包含六个行动项（每项含负责人、截止日、验收标准），schema 须通过 `schemas/remediation_schema.json` 验证 | `check_json_schema.py ${workspace}/docs/remediation_plan.json --schema ${eval_dir}/${agent_id}/schemas/remediation_schema.json` |

**Phase 4：偏好合规全量检验（upd4 后，综合阶段）**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e10 | L3 | 生成最终的 `docs/final_report_YYYY-MM-DD.md`（文件名用实际日期），综合全部证据，满足 P1（ISO 时间格式）、P2（文件命名）、P3（章节结构：摘要、时间线、矛盾分析、根因、补救、结论）、P4（代码块正确标记）、P5（不确定内容加 [UNVERIFIED]） | `check_preferences.py ${workspace} --rules P1,P2,P3,P4,P5 --target docs/final_report_*.md` |

*此阶段另补 8–10 道类似难度题（通知邮件草稿生成、测试覆盖率报告、配置差异 JSON 等），确保 exec_check 达 20 道以上。待细化。*

---

### 场景 B：hil_d3 — ICU 排班危机

**背景摘要**：CareScheduler 显示 100% 合规（均值 42.3h/周），Walsh 手工记录显示 7/11 护士实超 56h/周，徽章日志法证分析揭示数据录入者准确但其余 9 人均不准确（系统性造假）。Sarah Kim 的症状时间线记录两起近危险用药事件，Angela 的审计从"小问题"升级为"强制报告"。

**Workspace 关键文件**：
- `caresched_compliance_report.md`（系统报告，100% 合规）
- `hr_staffing_metrics.md`（HR 数据，病假率低于医院均值）
- `icu_staffing_policy.md`（JONA 2010 / Trinkoff 2011 研究引用）
- `nurse_roster_current.md`（11 名护士花名册）
- `incident_log_icucardiac.md`（正式日志，Q1 零近危险事件）
- `shift_schedule_published.md`（已发布班次）

**Update 时机**：
- `upd1`（q4 前）：Walsh 手工审计（`overtime_audit_report.md`）
- `upd2`（q7 前）：徽章访问分析（`badge_access_analysis.md`）
- `upd3`（q5 前）：Sarah Kim 症状时间线（`sarahkim_symptom_timeline.md`）
- `upd4`（q9 前）：Angela 正式审计发现（`caresched_audit_findings.md`）

#### 保留题目（6 轮）

| 保留 ID | 原 ID | 保留理由 |
|---------|-------|---------|
| r01 | q1 | 基线：班次结构与护患比 |
| r02 | q2 | 矛盾 C1 引入（系统 vs Walsh） |
| r03 | q3 | 矛盾 C2 引入（HR 指标 vs Sarah Kim） |
| r04 | q5 | 偏好引入（Tanaka 偏好 P1-P5） |
| r05 | q4 → upd1 后 | Walsh 审计后认知更新 |
| r06 | upd4 后 | Angela 审计升级后法律义务判断 |

#### 新增 exec_check 题目（24 轮）

**Phase 1：数据交叉验证（upd1 后，Walsh 审计可用）**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e01 | L2 | 生成 `analysis/overtime_comparison.csv`（11 行，字段：nurse_name, caresched_hours, actual_hours, delta, policy_breach），并在 `analysis/discrepancy_summary.md` 中计算：超标护士数、最大差值、系统均值 vs 实际均值 | `check_overtime_analysis.py ${workspace}` |
| e02 | L1 | 在 `docs/sarah_kim_risk_assessment.md` 中关联：连续班次时长 + JONA/Trinkoff 风险倍增系数 + 两起近危险事件，输出定量患者安全风险评分 | `check_file_content.py ${workspace} docs/sarah_kim_risk_assessment.md --contains "19" --contains "3" --contains "Trinkoff"` |

**Phase 2：徽章数据法证（upd2 后）**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e03 | L3 | 编写 `scripts/badge_forensics.py`：读取徽章日志，输出每位护士的实际工时（基于 IN/OUT 时间戳差值），与 CareScheduler 报告对比，标记差异 > 5h 的条目；运行后输出标准格式 CSV | `cd ${workspace} && python scripts/badge_forensics.py && python ${eval_dir}/${agent_id}/scripts/check_badge_output.py ${workspace}` |
| e04 | L2 | 生成 `docs/data_integrity_report.md`：量化两类群体（数据录入员 2 人 vs 其余 9 人）的误差模式，计算随机概率 < 1%，引用法证定义"系统性" vs "随机"误差 | `check_data_integrity.py ${workspace}` |

**Phase 3：合规与患者安全报告（upd4 后）**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e05 | L2 | 生成 `reports/YYYY-MM-DD_compliance_escalation.md`（Tanaka 命名偏好），包含：违规护士列表（含小时数）、Angela 审计升级依据（RCW 70.41.230）、建议的强制报告行动 | `check_preferences.py ${workspace} --rules P1,P2,P3 --target reports/` + `check_compliance_report.py ${workspace}` |
| e06 | L3 | 编写 `scripts/policy_check.py`：比对 `shift_schedule_published.md` 与 `overtime_audit_report.md`，自动标记所有违反 48h/周政策的排班条目，输出结构化 JSON；同时运行并通过 `tests/test_policy_check.py` | `cd ${workspace} && python -m pytest tests/test_policy_check.py -q` |
| e07 | L2 | 更新 `docs/incident_log_corrected.md`（正式日志 Q1 零事件与 Sarah Kim 时间线矛盾的修正版），按 Tanaka 偏好包含：事件日期、护士身份（匿名）、班次时长、风险等级 | `check_incident_log.py ${workspace}` |

*另补 7–9 道类似题（排班算法 bug 追踪报告、护士当前建议排班表修正、联合委员会汇报摘要等）。*

---

### 场景 C：hil_i2 — 研究数据重用指控

**背景摘要**：去重管道 V2.0 vs V2.1 对 23 名患者选择了不同"主记录"（临床结果不变），导致论文与王医生版本的患者 ID 集合有 23 个不同。投诉混淆了去重与数据选择性纳入；王医生从支持转为谨慎源于学术委员会压力下的职业自保，而非内疚。

**Workspace 关键文件**：
- 论文 N=847 数据集摘要
- 原始数据库导出（N=912）
- 王医生版本（N=847，23 个不同 ID）
- `pipeline-log.md`（V2.0 vs V2.1 去重规则差异）
- IRB 批准文件
- 发表时间线

**Update 时机**：
- `upd1`（q5 前）：详细管道日志（V2.0 vs V2.1 差异）
- `upd2`（q7 前）：王医生邮件演变（支持→谨慎）
- `upd3`（q6 前）：张主任背景信息
- `upd4`（q11 前）：学术委员会邮件

#### 保留题目（6 轮）

| 保留 ID | 原 ID | 保留理由 |
|---------|-------|---------|
| r01 | q1 | 时间线基线（IRB→提取→提交） |
| r02 | q2 | N 不一致引入（912/847/847） |
| r03 | q3 | 投诉三项指控 |
| r04 | q4 | 偏好引入（Lin Yi P1-P5） |
| r05 | q5 → upd1 后 | 管道日志解释三向 N 差异 |
| r06 | upd4 后 | 王医生行为动机综合判断 |

#### 新增 exec_check 题目（22 轮）

**Phase 1：数据集三向比对（upd1 管道日志可用后）**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e01 | L3 | 编写 `scripts/dataset_diff.py`：接收三个患者 ID 列表文件，计算：原始 DB → V2.0 的 65 条去重、V2.0 vs V2.1 的 23 个 ID 差异、临床结果一致性；输出 `analysis/dataset_diff_report.json` | `cd ${workspace} && python scripts/dataset_diff.py && python ${eval_dir}/${agent_id}/scripts/check_diff_report.py ${workspace}` |
| e02 | L2 | 生成 `docs/pipeline_version_comparison.md`：对比 V2.0（最旧记录优先）vs V2.1（最新记录优先）的去重策略差异，用表格列出 23 个受影响患者的 ID 变化及临床结果一致性证明 | `check_pipeline_comparison.py ${workspace}` |

**Phase 2：投诉反驳文档（upd2 后）**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e03 | L2 | 为每条投诉指控生成独立反驳文档 `docs/rebuttal_{claim}.md`（3 个文件），每份含：指控原文引用、技术证据链、结论；文件须包含具体数字（65、23、847、912） | `check_rebuttal_docs.py ${workspace}` |
| e04 | L1 | 生成 `docs/irb_timeline_verification.md`：从 IRB 批准文件提取所有时间戳，证明数据收集在 IRB 批准之后；格式按 Lin Yi 偏好（结论优先、日期标注） | `check_file_content.py ${workspace} docs/irb_timeline_verification.md --contains "2025-08-01" --contains "2025-09-15"` |

**Phase 3：学术委员会回应（upd4 后）**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e05 | L3 | 编写 `scripts/generate_committee_response.py`：整合反驳文档 + 管道日志 + IRB 文件，自动生成结构化 `docs/committee_response_YYYY-MM-DD.md`；脚本须通过 `tests/test_response_generator.py` | `cd ${workspace} && python -m pytest tests/test_response_generator.py -q` |
| e06 | L2 | 生成 `docs/wang_behavior_analysis.md`：区分王医生两阶段行为（初期支持 vs 后期谨慎），明确证据区分"职业自保"与"内疚承认"，按 Lin Yi 偏好格式化 | `check_wang_analysis.py ${workspace}` |

*另补 6–8 道（数据溯源图生成、去重算法实现验证、期刊投稿记录时间线等）。*

---

### 场景 D：hil_g1 — 候选人背景核查

**背景摘要**：Wang Hao 简历两处不符（12 人团队→实 4 人、连续就业→6 个月空档），CTO 因董事会压力推动快录，Huang Lei 技术面打分领导力仅 2.8/5.0 vs 技术 4.3/5.0，HR VP 支持尽职调查。

**Workspace 关键文件**：
- `candidate-resume.md`（声称12人+连续就业）
- `reference-check-emails.md`（Liu Wei：4人）
- `github-contribution-export.md`（6 个月零活动）
- `linkedin-profile-export.md`（就业空档日期）
- `interview-feedback-forms.md`（Huang Lei：领导力 2.8、技术 4.3）
- `cto-initial-message.md`（董事会压力）

#### 保留题目（7 轮）

| 保留 ID | 原 ID | 保留理由 |
|---------|-------|---------|
| r01 | q1 | 时间线基线 |
| r02 | q2 | C1 引入（团队规模 12 vs 4） |
| r03 | q3 | C2 引入（CTO 压力 vs 实际评估） |
| r04 | q4 | 偏好引入（Chen Jing P1-P5） |
| r05 | q5 → upd1 后 | Huang Lei 面试深化验证 |
| r06 | upd2 后 | LinkedIn 完整导出确认空档 |
| r07 | upd4 后 | CTO 回应与决策权衡 |

#### 新增 exec_check 题目（21 轮）

**Phase 1：证据三角化**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e01 | L2 | 生成 `analysis/discrepancy_matrix.json`：结构化记录每处不符（字段：claim, source_resume, source_external, delta, severity），并生成 `analysis/discrepancy_summary.md` 汇总表格（按 Chen Jing 偏好） | `check_json_schema.py ${workspace}/analysis/discrepancy_matrix.json --schema ${eval_dir}/${agent_id}/schemas/discrepancy_schema.json` |
| e02 | L3 | 编写 `scripts/github_gap_analyzer.py`：读取 GitHub 贡献导出，自动检测连续 > 30 天零活动的时间窗口，输出 `analysis/github_gaps.json`（字段：gap_start, gap_end, duration_days） | `cd ${workspace} && python scripts/github_gap_analyzer.py && python ${eval_dir}/${agent_id}/scripts/check_github_gaps.py ${workspace}` |
| e03 | L1 | 生成 `docs/reference_verification.md`：对比 Liu Wei 推荐信 vs 简历中关于团队规模的说法，计算倍增系数（12/4=3x），格式按 Chen Jing 偏好（要点+摘要优先） | `check_file_content.py ${workspace} docs/reference_verification.md --contains "3" --contains "2.8" --contains "4.3"` |

**Phase 2：多维度评估报告**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e04 | L2 | 生成 `reports/YYYY-MM-DD_候选人评估_Wang_Hao_v1.md`（中文文件名，Chen Jing 命名偏好）：包含技术评分、领导力评分、诚信风险评级、三方证据对比表、建议（P6 vs P7 vs 拒绝）及理由 | `check_preferences.py ${workspace} --rules P1,P2,P3 --target reports/` + `check_candidate_report.py ${workspace}` |
| e05 | L2 | 生成 `docs/cto_briefing.md`：专为 CTO 李强准备，承认其时间压力，但用数据（3x 团队规模不符 + 2.8/5.0 领导力 + 6 个月空档）论证风险；须包含三个具体数值和一个降级聘用建议 | `check_cto_briefing.py ${workspace}` |

**Phase 3：后续流程**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e06 | L3 | 生成 `docs/verification_checklist.json`（10 项尽职调查清单，每项含：item, status, evidence_source, risk_level）并通过 schema 验证 | `check_json_schema.py ${workspace}/docs/verification_checklist.json --schema ${eval_dir}/${agent_id}/schemas/checklist_schema.json` |
| e07 | L2 | 生成 `docs/background_check_protocol.md`：为 HR 部门起草标准背景核查流程（含防 CTO 过度干预的节点），包含 Wang Hao 案例中的具体失误示例 | `check_protocol_doc.py ${workspace}` |

*另补 4–6 道题（决策矩阵生成、邮件回复草稿、背景核查摘要 JSON 等）。*

---

### 场景 E：hil_j1 — 品牌数据欺诈

**背景摘要**：MCN 星芒传媒在两个平台（小红书 2.39x、bilibili 2.02x）系统性夸大周芳数据，"不同衡量方法论"辩护被 API 文档单一口径定义驳斥，合同条款 7.3 要求"已验证数据"，刘姐最终承认"内部估算"。

**Workspace 关键文件**：
- `xiaohongshu-backend-export.md`（50,234 浏览）
- `mcn-brand-report.md`（报告 120,000）
- `bilibili-data-export.md`（32,178 vs MCN 65,000）
- `brand-contract-excerpt.md`（条款 7.3"已验证数据"）
- `xiaolin-creator-report.md`（另一创作者数据）

#### 保留题目（6 轮）

| 保留 ID | 原 ID | 保留理由 |
|---------|-------|---------|
| r01 | q1 | 基线：两平台夸大倍率 |
| r02 | q2 | C2 引入（方法论辩护 vs API 口径） |
| r03 | q3 | C3 非矛盾确认（发布日期一致） |
| r04 | q4 | 偏好引入（周芳 P1-P5） |
| r05 | upd1 后 | 品牌收到截图证据后 |
| r06 | upd2 后 | 刘姐承认"内部估算"后 |

#### 新增 exec_check 题目（22 轮）

**Phase 1：数据量化分析**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e01 | L2 | 生成 `analysis/data_discrepancy_table.csv`（字段：platform, official_views, mcn_reported, inflation_ratio, contract_requirement_met）及 `analysis/📊夸大分析_YYYY-MM-DD.md`（按周芳命名偏好含 emoji） | `check_discrepancy_table.py ${workspace}` |
| e02 | L3 | 编写 `scripts/inflate_detector.py`：读取多个平台导出文件，自动计算夸大比率，若比率 > 1.5 标记为"系统性"，输出 `analysis/inflate_report.json`；运行后须通过 `tests/test_inflate_detector.py` | `cd ${workspace} && python -m pytest tests/test_inflate_detector.py -q` |
| e03 | L1 | 生成 `docs/api_definition_evidence.md`：引用 API 文档中的"唯一统计口径"条款，驳斥"不同方法论"辩护，列出两平台夸大数字及倍率 | `check_file_content.py ${workspace} docs/api_definition_evidence.md --contains "2.39" --contains "2.02" --contains "唯一"` |

**Phase 2：合同合规与证据链**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e04 | L2 | 生成 `docs/contract_breach_analysis.md`：逐条对应合同 7.3 与 MCN 截图提交方式，论证截图不满足"已验证数据"定义；须含条款原文引用 | `check_contract_analysis.py ${workspace}` |
| e05 | L2 | 生成 `reports/📋证据汇总_YYYY-MM-DD_v1.md`（周芳命名偏好）：时间线形式整合所有证据节点（数据不符首发现→方法论辩护→API文档驳斥→合同核查→刘姐承认），每节点含来源引用 | `check_preferences.py ${workspace} --rules P1,P2,P4 --target reports/` |
| e06 | L3 | 生成 `docs/xiaolin_parallel_analysis.md`：对比小林案例与周芳案例的夸大比率，用统计方法（皮尔逊/斯皮尔曼）检验两创作者数据的模式一致性，输出 `analysis/pattern_stats.json` | `check_parallel_analysis.py ${workspace}` |

**Phase 3：后续行动方案（刘姐承认后）**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e07 | L2 | 生成 `docs/mcn_negotiation_memo.md`：以周芳视角起草与 MCN 的谈判要点（索赔金额计算、合同终止条款引用、替代解决方案），须包含夸大金额的数值估算 | `check_negotiation_memo.py ${workspace}` |
| e08 | L2 | 生成 `docs/brand_disclosure_draft.md`：向品牌方说明数据造假情况的正式通知草稿；须使用正式语气（区别于周芳日常活泼风格），并记录原始数据来源 | `check_brand_disclosure.py ${workspace}` |

*另补 4–6 道（平台 API 使用报告、证据打包清单 JSON、致粉丝透明声明等）。*

---

### 场景 F：hil_g3 — 薪资数据泄露

**背景摘要**：云盘日志显示林小雅 14:22 下载完整版（2.3MB）、10:00 仅预览脱敏版（0.8MB），15:03 邮件转发 2.3MB 附件给外部猎头；IT 报告仅覆盖云盘分享功能（范围盲点），不含邮件渠道；文件版本历史确认完整版包含 3 名新员工而脱敏版不包含。

**Workspace 关键文件**：
- `cloud-storage-access-log.md`（PREVIEW vs DOWNLOAD 时间戳）
- `email-attachment-audit.md`（2.3MB 附件发往外部域）
- `it-security-report.md`（范围限于云盘，未含邮件）
- `salary-spreadsheet-metadata.md`（文件大小/哈希）

#### 保留题目（6 轮）

| 保留 ID | 原 ID | 保留理由 |
|---------|-------|---------|
| r01 | q1 | 云日志证据基线 |
| r02 | q2 | C1 引入（林小雅否认 vs 完整版下载记录） |
| r03 | q3 | 邮件审计与文件大小交叉验证 |
| r04 | q4 | 偏好引入（Chen Jing P1-P5） |
| r05 | upd1 后 | 版本历史确认完整版身份 |
| r06 | upd2 后 | IT 报告范围盲点揭示 |

#### 新增 exec_check 题目（22 轮）

**Phase 1：日志解析与证据提取**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e01 | L3 | 编写 `scripts/log_parser.py`：解析云盘访问日志，提取 DOWNLOAD 事件（含文件大小、时间戳、用户），输出 `analysis/download_events.json`；运行后须通过 `tests/test_log_parser.py` | `cd ${workspace} && python -m pytest tests/test_log_parser.py -q` |
| e02 | L2 | 生成 `analysis/timeline_reconstruction.md`：按时间顺序重建泄露链（文件创建→更新→预览→下载→邮件发送），每事件含：时间戳、操作类型、文件大小、参与方，格式按 Chen Jing 偏好 | `check_timeline.py ${workspace}` |
| e03 | L1 | 生成 `docs/file_identity_proof.md`：用文件大小差异（2.3MB vs 0.8MB）+ 哈希值 + 版本历史证明邮件附件与完整版薪资表同一，排除"误发脱敏版"辩护 | `check_file_content.py ${workspace} docs/file_identity_proof.md --contains "2.3" --contains "0.8" --contains "v1.1"` |

**Phase 2：IT 报告盲点分析**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e04 | L2 | 生成 `docs/it_report_scope_analysis.md`：明确 IT 报告覆盖范围（云盘共享功能）vs 未覆盖范围（邮件附件），用对比表格展示，并标注哪条泄露证据落在 IT 盲区 | `check_it_scope_analysis.py ${workspace}` |
| e05 | L3 | 编写 `scripts/cross_channel_audit.py`：整合云盘日志 + 邮件审计，生成完整的跨渠道访问时间线 `analysis/cross_channel_events.json`；脚本须通过 `tests/test_cross_channel.py` | `cd ${workspace} && python -m pytest tests/test_cross_channel.py -q` |

**Phase 3：调查报告（upd4 林小雅部分承认后）**

| 新 ID | 难度 | 任务描述 | 验证方式 |
|-------|------|---------|---------|
| e06 | L2 | 生成 `reports/2026-09-28_薪资泄露调查报告_v1.md`（Chen Jing 命名偏好）：完整调查报告，含执行摘要、证据链、嫌疑人行为分析、IT 报告局限性、建议处置措施 | `check_preferences.py ${workspace} --rules P1,P2,P3 --target reports/` + `check_investigation_report.py ${workspace}` |
| e07 | L2 | 生成 `docs/hr_remediation_plan.md`：针对此次泄露的 HR 补救方案（访问权限矫正、审计流程覆盖邮件渠道、林小雅处置建议），须包含可量化的行动项 | `check_remediation_plan.py ${workspace}` |
| e08 | L3 | 生成 `docs/leak_probability_report.md`：用条件概率（文件大小匹配概率 + 时间窗口匹配概率 + 收件方身份概率）量化林小雅为泄露源的置信度（须 > 95%），以 JSON + Markdown 双格式输出 | `check_probability_report.py ${workspace}` |

*另补 4–6 道题（证据打包清单、向林小雅的询问提纲、外部猎头通知草稿等）。*

---

## 三、评测脚本体系设计

### 3.1 通用工具（可跨场景复用）

```
eval/
├── _shared/
│   ├── check_file_content.py      # 检查文件含关键词
│   ├── check_json_schema.py       # JSON schema 验证
│   ├── check_file_exists.py       # 文件存在 + 非空
│   ├── check_preferences.py       # 通用偏好检查（P1-P5）
│   └── validation_utils.py        # 公共工具函数
└── {scene_id}/
    ├── questions.json
    └── scripts/
        ├── check_*.py             # 场景专属检查脚本
        ├── tests/
        │   └── test_*.py          # 测试 agent 写的代码
        └── schemas/
            └── *.json             # JSON schema 定义
```

### 3.2 场景专属脚本清单

| 场景 | 脚本 | 主要功能 |
|------|------|---------|
| hil_f3 | check_ci_gap.py | 验证测试缺陷报告 + DST 测试存在 |
| hil_f3 | check_rca_report.py | 验证根因分析六维度 + 数值 |
| hil_f3 | check_near_miss.py | 验证近危险日志时间戳格式 |
| hil_d3 | check_overtime_analysis.py | 验证 overtime_comparison.csv 字段与数值 |
| hil_d3 | check_badge_output.py | 验证徽章分析脚本输出 CSV 格式 |
| hil_d3 | check_compliance_report.py | 验证合规报告含强制报告依据 |
| hil_i2 | check_diff_report.py | 验证三向数据集比对 JSON |
| hil_i2 | check_pipeline_comparison.py | 验证 V2.0 vs V2.1 对比表格 |
| hil_i2 | check_rebuttal_docs.py | 验证三份反驳文档存在 + 关键数字 |
| hil_g1 | check_github_gaps.py | 验证 GitHub 空白窗口 JSON |
| hil_g1 | check_candidate_report.py | 验证评估报告含三项关键数值 |
| hil_j1 | check_discrepancy_table.py | 验证 CSV 字段与比率计算 |
| hil_j1 | check_parallel_analysis.py | 验证统计分析输出 |
| hil_g3 | check_timeline.py | 验证时间线重建完整性 |
| hil_g3 | check_investigation_report.py | 验证调查报告结构 + 数值 |

---

## 四、题目数量汇总

| 场景 | 保留 multi_choice | 新增 exec_check | 总计 |
|------|------------------|----------------|------|
| hil_f3（时区事件） | 7 | ~23 | ~30 |
| hil_d3（排班危机） | 6 | ~24 | ~30 |
| hil_i2（数据重用） | 6 | ~22 | ~28 |
| hil_g1（背景核查） | 7 | ~21 | ~28 |
| hil_j1（品牌欺诈） | 6 | ~22 | ~28 |
| hil_g3（薪资泄露） | 6 | ~22 | ~28 |
| **合计** | **38** | **~134** | **~172** |

---

## 五、实施顺序建议

1. **优先启动 hil_f3**（代码修复类，验证逻辑最客观，可作为后续场景的模板）
2. **次优先 hil_d3**（统计脚本类，覆盖 Pattern C+D，工作区数据最丰富）
3. **然后 hil_i2**（数据管道类，天然适合 Pattern C+G）
4. **最后三个**（hil_g1 / hil_j1 / hil_g3）主要偏报告生成 + JSON 输出，Pattern A+B+G 为主

每个场景的实施步骤：
1. 确认 workspace 文件与 data-spec 一致（如缺少文件需补充）
2. 编写评测脚本（`scripts/check_*.py` + schema 文件）
3. 编写 `questions.json`（保留题 + 新增题）
4. 本地用 `clawarena check` 验证
5. 提交审阅

---

## 六、待确认问题

以下问题需与用户确认后才能推进：

1. **workspace 文件补充**：六个场景的 workspace 目前主要含 AGENTS/IDENTITY/SOUL/USER/TOOLS 五个配置文件 + 场景文件。部分 exec_check 题（如 hil_f3 的代码修复）需要 workspace 中存在 `src/trading_system.py`、`tests/` 等目录结构。**问题：这些代码文件是否需要新建到 workspace，还是只用现有的 .md 文件作为工作产物来源？**

2. **hil_d3 的 workspace**：spec 中描述的文件与 extended 目录中的实际文件是否一致？需确认 `badge_access_analysis.md` 等 update 文件是否已存在。

3. **题目 ID 命名**：保留的原题是否沿用原 ID（q1、q4 等），新增题用什么 ID 规范（如 `e01`、`exec_01`、或直接续号 `q31`）？

4. **`pre_inject` 字段**：新增的 exec_check 题是否需要配 `pre_inject` 文件？（如 exec 题在靠后的轮次，跳过前面多道选择题时需要注入上下文）

5. **偏好检查覆盖度**：每个场景中，`pref` 字段附加检查是否要达到特定比例（如 30%）？
