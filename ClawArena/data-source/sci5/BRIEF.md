# BRIEF: sci5 — HR 违规解雇与 PIP 纠纷

## 场景叙事背景

HelixDyne Software（一家位于加利福尼亚州、员工规模约 320 人的中型 SaaS 公司）的 People Operations 团队正面临一场多线并发的 HR 合规危机。

**主线一（PIP 纠纷）：** 工程师 Marcus Webb（42 岁）被直属经理以"持续绩效不达标"为由启动了 PIP，PIP 文件仅设定 21 天观察期。PIP 结束后第 3 天，Marcus 收到解雇通知书。Marcus 随即联系公司 HR 负责人声称：（1）PIP 期限不足行业惯例 30 天最低标准；（2）他曾在 PIP 启动前第 6 天申请了 FMLA 假期，解雇时 FMLA 保护期尚未届满；（3）公司实际将他的岗位外包给承包商，并非绩效原因，构成伪装性解雇（pretextual termination）。

**主线二（WARN Act 合规）：** 同期，公司董事会批准了一项"组织效能重组"计划：在 30 天内裁员 58 名全职员工，关闭圣地亚哥办公室（当地有 47 名全职员工）。新任 General Counsel 提交了一份内部法律备忘录，声称此次裁员"低于联邦 WARN Act 500 人阈值，无需提前通知"，但忽视了加州 Cal-WARN Act 的更严格要求（75 名员工覆盖、50 名员工触发、60 天通知期），以及纽约办公室同期离职员工与是否构成联邦 33% 规则的问题。

**Agent 的角色：** Agent 扮演公司 People Operations 专员（同时掌握 HR 合规与法律政策知识），须在多个 session（Slack、Email、飞书、HR 系统导出文件）中核查文件、计算合规窗口、起草合规通知、识别法律风险，最终输出一套可由 shell 脚本精确校验的结构化合规报告与法律文件。

---

## 真实来源链接表

| # | 来源标题 | URL | 类型 |
|---|---------|-----|------|
| S1 | WARN Act 29 U.S.C. § 2101 — Definitions (Cornell LII) | https://www.law.cornell.edu/uscode/text/29/2101 | official_doc |
| S2 | WARN Act Overview — Thomson Reuters Legal | https://legal.thomsonreuters.com/en/insights/articles/what-is-the-warn-act | regulation |
| S3 | Cal-WARN Act — CA DIR Official Page | https://www.dir.ca.gov/dlse/cal-warnact.html | official_doc |
| S4 | California WARN Act Thresholds — Shouse Law | https://www.shouselaw.com/ca/labor/wrongful-termination/warn-act/ | regulation |
| S5 | New York WARN Act FAQ — NY DOL Official | https://dol.ny.gov/warn-businesses-frequently-asked-questions | official_doc |
| S6 | NY WARN Act 2023 Amendments — Cooley Law | https://www.cooley.com/news/insight/2023/2023-08-03-new-york-state-amends-its-warn-act-regulations | regulation |
| S7 | SHRM: PIPs — Write, Implement and Time Them Precisely | https://www.shrm.org/topics-tools/employment-law-compliance/pips-write-implement-time-precisely | dataset |
| S8 | EEOC: Time Limits for Filing a Charge | https://www.eeoc.gov/time-limits-filing-charge | official_doc |
| S9 | EEOC: OWBPA Severance Waiver Q&A | https://www.eeoc.gov/laws/guidance/qa-understanding-waivers-discrimination-claims-employee-severance-agreements | official_doc |
| S10 | 5 CFR § 432.105 — Federal PIP Performance Action (Cornell LII) | https://www.law.cornell.edu/cfr/text/5/432.105 | regulation |
| S11 | OPM: Performance Improvement Period Guide | https://www.opm.gov/policy-data-oversight/employee-relations/reference-materials/the-performance-improvement-period.pdf | official_doc |
| S12 | DOL Plant Closings — WARN Act Topic Page | https://www.dol.gov/general/topic/termination/plantclosings | official_doc |
| S13 | FMLA Eligibility 29 CFR 825.110 — Cornell LII | https://www.law.cornell.edu/cfr/text/29/825.110 | regulation |
| S14 | ADEA Statute — EEOC Official Page | https://www.eeoc.gov/statutes/age-discrimination-employment-act-1967 | official_doc |
| S15 | Montana WDEA § 39-2-904 — MT Legislature | https://mca.legmt.gov/bills/mca/title_0390/chapter_0020/part_0090/section_0040/0390-0020-0090-0040.html | official_doc |

---

## Ground-Truth 锚点表

| 锚点 ID | 锚点名称 | 精确值 | 来源 URL | 备注 |
|--------|---------|-------|---------|------|
| A1 | 联邦 WARN Act 雇主覆盖阈值 | 100 名全职员工（或总工时 ≥4,000 小时/周） | S1/S2 | 29 U.S.C. § 2101 |
| A2 | 联邦 WARN Act 植物关闭触发数 | 50 名员工（30 天内），不含兼职 | S1/S2 | 植物关闭定义 |
| A3 | 联邦 WARN Act 大规模裁员 33% 规则 | ≥33% 全职员工 且 ≥50 人，或 ≥500 人 | S1/S2 | mass layoff 双重阈值 |
| A4 | 联邦 WARN Act 通知期 | 60 个日历日 | S2 | 提前书面通知 |
| A5 | 联邦 WARN Act 地方政府违规罚款 | $500/天（3 周内补发薪资可免） | S2 | civil penalty |
| A6 | Cal-WARN Act 雇主覆盖阈值 | 75 名员工（过去 12 个月内任一时点） | S3/S4 | Labor Code § 1400-1408 |
| A7 | Cal-WARN Act 大规模裁员触发数 | 30 天内裁员 ≥50 名员工 | S3/S4 | 不需要 33% 比例要求 |
| A8 | Cal-WARN Act 通知期 | 60 天 | S3/S4 | 与联邦相同天数，但触发门槛更低 |
| A9 | NYS WARN Act 雇主覆盖阈值 | 50 名全职员工（纽约州内） | S5/S6 | 2023 修正后含远程工 |
| A10 | NYS WARN Act 植物关闭触发数 | ≥25 名员工（30 天内） | S5 | 低于联邦 50 人门槛 |
| A11 | NYS WARN Act 通知期 | 90 天 | S6 | 超过联邦 60 天 |
| A12 | PIP 行业惯例最短持续期 | 30 天（30–90 天范围） | S7 | SHRM 建议，非法定 |
| A13 | EEOC 申诉标准时限 | 180 天（有州机构则 300 天） | S8 | Title VII / ADA / ADEA |
| A14 | FMLA 雇主覆盖阈值 | 50 名员工（20 个或以上工作周） | S13 | 29 CFR § 825.110 |
| A15 | FMLA 员工资格：工龄 | ≥12 个月（可不连续） | S13 | |
| A16 | FMLA 员工资格：工时 | ≥1,250 小时（过去 12 个月） | S13 | |
| A17 | FMLA 员工资格：地理 | 75 英里范围内 ≥50 名员工 | S13 | |
| A18 | FMLA 带薪/无薪假期上限 | 12 周/年 | S13 | 无薪但岗位保护 |
| A19 | ADEA 保护年龄 | ≥40 岁 | S14 | 29 U.S.C. § 631 |
| A20 | ADEA 雇主覆盖阈值 | 20 名员工（连续 20 个工作周） | S14 | |
| A21 | OWBPA 个人解雇考虑期 | 21 天 | S9 | ADEA 豁免协议 |
| A22 | OWBPA 集体解雇考虑期 | 45 天 | S9 | group termination program |
| A23 | OWBPA 撤销期 | 7 天（不可缩短） | S9 | 签署后 7 天内可撤回 |
| A24 | 5 CFR § 432.105 提前通知期（联邦雇员） | 30 天（最长可延至 60 天） | S10 | 联邦机构 PIP 制度 |

---

## Workspace 文件树与体量规划（目标 >100k tokens）

```
workspace/
├── company/
│   ├── employee_roster.csv           # 320 行员工数据（含姓名/年龄/岗位/工龄/工时/工资），约 40KB
│   ├── hr_policy_handbook.md         # 公司 HR 手册全文（PIP 政策、渐进式纪律、解雇流程），约 80KB
│   ├── org_chart.json                # 组织架构 JSON（部门/汇报线/办公室位置），约 15KB
│   └── payroll_summary_Q1Q2.csv      # 薪资汇总表（按员工/月/部门），约 35KB
├── legal/
│   ├── warn_act_federal_summary.md   # 联邦 WARN Act 条文摘要（含所有阈值、豁免条款、通知模板），约 50KB
│   ├── cal_warn_act_memo.md          # Cal-WARN 内部法律备忘录（含 75 人/50 人/60 天分析），约 30KB
│   ├── nys_warn_act_memo.md          # NYS WARN Act 分析（含 90 天通知期、25 人门槛），约 25KB
│   ├── gc_layoff_memo_v1.md          # General Counsel 原始备忘录（含"500 人阈值"错误结论），约 20KB ← 诱饵文件 V5
│   ├── gc_layoff_memo_v2.md          # GC 修订备忘录（更正 Cal-WARN 分析，部分撤回 v1），约 18KB
│   ├── owbpa_waiver_template.md      # OWBPA 豁免协议模板（含 21/45 天条款、7 天撤销期），约 15KB
│   └── eeoc_filing_guide.md          # EEOC 申诉流程指南（180/300 天规则，申诉表格），约 20KB
├── pip_case/
│   ├── marcus_webb_pip_v1.md         # Marcus Webb PIP 原件（21 天期限，错误版本），约 12KB ← 旧版本红鲱鱼 V6
│   ├── marcus_webb_pip_v2.md         # HR 修订后的 PIP（30 天期限，合规版本）—— Update 1 注入，约 12KB
│   ├── marcus_webb_personnel_file.md # Marcus 人事档案（雇佣记录、工龄、工时、FMLA 申请记录），约 25KB
│   ├── performance_review_2023.md    # 2023 年度绩效考核报告（含评分、反馈记录），约 18KB
│   ├── performance_review_2024.md    # 2024 年度绩效考核报告（含 Q3 下滑记录），约 18KB
│   └── contractor_engagement_log.md  # 外包承包商参与日志（时间线与 Marcus 岗位重叠证据），约 15KB
├── layoff/
│   ├── restructuring_plan_v1.md      # 重组计划草案（裁员 58 人，含办公室明细），约 20KB
│   ├── restructuring_plan_v2.md      # 重组计划修订版（裁员人数调整），约 18KB ← Update 2 注入
│   ├── warn_notice_draft_federal.md  # 联邦 WARN 通知草案（致受影响员工），约 10KB
│   ├── warn_notice_draft_cal.md      # Cal-WARN 通知草案（致加州 EDD 和受影响员工），约 10KB
│   ├── affected_employees_list.csv   # 受裁员影响员工列表（含年龄/工资/岗位/办公室），约 20KB
│   └── severance_matrix.csv          # 遣散费矩阵（按工龄/年龄/岗位计算），约 15KB
├── sessions/
│   ├── slack_general_hr.jsonl        # #hr-compliance Slack 频道历史（含 tool call 痕迹），约 50KB
│   ├── slack_dm_marcus.jsonl         # Marcus 与 HR 的 Slack DM 记录，约 20KB
│   ├── email_thread_gc_layoff.eml    # GC 与 HR 关于裁员合规的 Email 线程，约 30KB
│   ├── feishu_pip_discussion.jsonl   # 飞书 HR 团队内部关于 PIP 的群聊记录，约 25KB
│   └── discord_legal_ops.jsonl       # Legal Ops Discord DM（律师与 HR BP 交流），约 20KB
└── reports/
    ├── compliance_audit_template.json # 合规审计输出模板（JSON schema 定义），约 8KB
    └── risk_matrix_template.csv       # 风险矩阵模板，约 5KB
```

**体量估算总计：** 约 620KB 文本 ≈ 155,000–200,000 tokens（大幅超过 100k 要求）

---

## Session 清单（6 个）

| Session ID | 渠道 | 参与方 | 主要内容 |
|-----------|------|-------|---------|
| S-MAIN | HR 系统 / Agent 工作台 | HR 专员（Agent）⟷ HR 系统 | 主工作 session，所有文件操作与报告输出均在此执行 |
| S-SLACK-HR | Slack #hr-compliance | HR BP、GC、People Ops VP | 裁员合规讨论，GC 误判 WARN Act 的原始对话，含 bot 自动摘要诱饵（V5） |
| S-SLACK-DM | Slack DM | Marcus Webb ⟷ HR 专员 | Marcus 的 PIP 申诉、FMLA 申请时间线记录、怀疑遭预谋解雇的陈述 |
| S-EMAIL | Email 线程 | GC ⟷ HR Director | 内部法律邮件，v1 备忘录发送（含错误分析），v2 撤回部分内容（Update 2 supersede） |
| S-FEISHU | 飞书群聊 | HR Team（3 人） | PIP 内部讨论，对 21 天 vs 30 天的分歧，最终决定修订 PIP（Update 1 来源） |
| S-DISCORD | Discord DM | Outside Counsel ⟷ HR BP | OWBPA 豁免协议合规性审查，EEOC 申诉期计算讨论 |

---

## 15–18 轮 exec_check 概要

### Q1 — 员工资格核查：FMLA 覆盖判定
- **目标意图：** 判定 HelixDyne 是否为 FMLA 覆盖雇主，Marcus 是否满足 FMLA 员工资格三要件
- **产物：** `reports/fmla_eligibility_check.json`（字段：`employer_covered: bool`、`employee_eligible: bool`、`weeks_entitled: int`、`reasons: []`）
- **check 锚点：** `employer_covered = true`（320 > 50）、`employee_eligible = true`（工龄 4.5 年 > 12 月，工时 1,310 > 1,250）、`weeks_entitled = 12`
- **难度向量：** V8（JSON schema 精确字段/类型校验）、V4（工时数字贯穿后续轮次）
- **相关 preference：** P1（JSON 输出必须含 `reasoning` 字段）

### Q2 — PIP 合规性分析
- **目标意图：** 对比 marcus_webb_pip_v1.md（21 天）与行业最低标准，判定是否合规
- **产物：** `reports/pip_compliance.json`（字段：`duration_days: int`、`compliant: bool`、`minimum_recommended_days: int`、`deficiencies: []`）
- **check 锚点：** `duration_days = 21`、`compliant = false`、`minimum_recommended_days = 30`
- **难度向量：** V6（pip_v1 是被废弃的旧版，pip_v2 才是 Update 1 后的合规版本，需辨别）、V8
- **update 关联：** Update 1 注入 pip_v2，后续轮次须引用 v2

### Q3 — FMLA 保护期与解雇时间线分析
- **目标意图：** 计算 Marcus FMLA 申请日期 + 保护期是否与解雇日期冲突
- **产物：** `reports/fmla_timeline.json`（字段：`fmla_start_date`、`fmla_end_date`、`termination_date`、`in_protection_window: bool`、`risk_level: str`）
- **check 锚点：** `in_protection_window = true`（解雇日在 FMLA 保护 12 周内）、`risk_level = "HIGH"`
- **难度向量：** V4（日期从 Q1 数据链路延续），V1（Slack DM 与人事档案日期有微小差异，须以人事档案为准）

### Q4 — 解雇原因真实性核查（pretextual termination）
- **目标意图：** 对比绩效考核记录与承包商参与日志，判断是否存在伪装性解雇迹象
- **产物：** `reports/pretext_risk_assessment.json`（字段：`contractor_overlap_days: int`、`performance_rating_2024_q3`、`pretext_indicators: []`、`risk_score: int (0-100)`）
- **check 锚点：** `contractor_overlap_days ≥ 14`、`risk_score ≥ 70`，至少 2 条 `pretext_indicators`
- **难度向量：** V1（GC 备忘录与承包商日志时间线相互矛盾），V5（Slack bot 摘要错误声称"承包商于 Marcus 离职后才参与"）

### Q5 — 联邦 WARN Act 适用性分析
- **目标意图：** 判断 HelixDyne 裁员 58 人是否触发联邦 WARN Act，区分 mass layoff 与 plant closing
- **产物：** `reports/warn_federal.json`（字段：`employer_qualifies: bool`、`event_type: str`、`threshold_met: bool`、`employees_affected: int`、`notice_days_required: int`、`applicable_rule: str`）
- **check 锚点：** `employer_qualifies = true`（320 > 100）、`threshold_met = true`（58 > 50 且 SD 47 人关闭）、`notice_days_required = 60`、`applicable_rule` 含 "plant closing"
- **难度向量：** V5（GC v1 备忘录声称"低于 500 人无需通知"是诱饵错误）、V9（必须逐字引用 "50 or more employees" 条文）

### Q6 — Cal-WARN Act 合规分析
- **目标意图：** 在联邦 WARN 之外，分析 Cal-WARN Act 附加义务
- **产物：** `reports/warn_california.json`（字段：`applies: bool`、`employer_threshold: int`、`trigger_threshold: int`、`notice_days: int`、`additional_obligations: []`）
- **check 锚点：** `applies = true`（320 > 75）、`employer_threshold = 75`、`trigger_threshold = 50`、`notice_days = 60`
- **难度向量：** V9（数字必须来自 Cal-WARN Labor Code § 1400-1408 条文），V4（50/75 数字后续 Q14 终产物须一致）

### Q7 — NYS WARN Act 分析（Update 1 前）
- **目标意图：** 分析纽约办公室裁员是否触发 NYS WARN（首轮：基于重组计划 v1）
- **产物：** `reports/warn_nys_v1.json`（字段：`applies: bool`、`ny_employees_affected: int`、`threshold: int`、`notice_days: int`、`triggered: bool`）
- **check 锚点（v1 数据）：** `notice_days = 90`、`threshold = 25`
- **难度向量：** V2（Update 2 后裁员人数变化，此轮答案将被 supersede）

### Q8 — ADEA / OWBPA 合规性核查
- **目标意图：** 确认 Marcus（42 岁）受 ADEA 保护；起草遣散协议须包含 OWBPA 合规条款
- **产物：** `reports/adea_compliance.json`（字段：`employee_age: int`、`adea_protected: bool`、`employer_threshold_met: bool`、`individual_termination: bool`、`consideration_days: int`、`revocation_days: int`）
- **check 锚点：** `adea_protected = true`、`consideration_days = 21`（个人解雇非集体）、`revocation_days = 7`
- **难度向量：** V8（精确数值 21/7 必须正确），V1（Slack 对话中有人误引"45 天"，需识别应为 21 天）

### Q9 — EEOC 申诉期计算
- **目标意图：** 计算 Marcus 若提起 EEOC 申诉的截止日期（加州有 DFEH，适用 300 天）
- **产物：** `reports/eeoc_deadline.json`（字段：`state_agency_exists: bool`、`filing_deadline_days: int`、`deadline_date: str (ISO8601)`、`statute_basis: str`）
- **check 锚点：** `filing_deadline_days = 300`（加州 DFEH 存在）、`statute_basis` 含 "Title VII" 与 "ADEA"
- **难度向量：** V4（解雇日期从 Q3 延续，deadline_date 须精确计算），V9（必须引用 Title VII / 42 U.S.C. § 2000e）

### Q10 — 起草联邦 WARN 通知（Update 1 后）
- **目标意图：** 在确认联邦 WARN 触发后，起草符合要求的书面通知
- **产物：** `warn_notice_federal_final.md`（含雇主信息、触发事件类型、受影响员工数、预计生效日期、工会/非工会状态）
- **check 锚点：** 文件须包含 "60" 天通知期字样、受影响员工数 ≥50、事件类型为 "plant closing" 或 "mass layoff"
- **难度向量：** V3（P3 要求所有对外通知须在 header 注明版本号和日期），V9（通知文本须引用 29 U.S.C. § 2102）

### Q11 — 起草 Cal-WARN 通知（同步）
- **目标意图：** 按 Cal-WARN 要求起草额外通知（须同时发给 CA EDD 和受影响员工）
- **产物：** `warn_notice_cal_final.md`（含加州特有附加要求）
- **check 锚点：** 文件须包含 "California Employment Development Department"（字面量）、通知期 60 天、触发人数 50
- **难度向量：** V9（verbatim 引用 EDD 名称），V3（P3 版本号格式）

### Q12 — Update 2 注入：重组计划修订（supersede）
- **目标意图：** 处理 Update 2 注入的 restructuring_plan_v2.md（裁员人数从 58 人调整为 31 人，SD 办公室保留）；判断此修订是否撤销 Q7 的 NYS WARN 结论
- **产物：** `reports/warn_nys_v2.json`（更新后的 NYS 分析）与 `reports/supersede_log.json`（记录哪些先前结论被修订）
- **check 锚点：** `warn_nys_v2.json` 中 `triggered = false`（31 人 > 25 但 SD 已保留，联邦 plant closing 不再触发）；`supersede_log.json` 中须记录 Q7 结论被 Q12 替代
- **难度向量：** V2（update 反转：裁员缩减后部分 WARN 义务消失），V10（supersede 辨别，不能简单叠加）

### Q13 — 综合风险矩阵输出
- **目标意图：** 汇总所有法律风险，输出机器可校验的风险矩阵 CSV
- **产物：** `reports/risk_matrix_final.csv`（列：`risk_id, law, risk_description, severity, status, recommended_action`）
- **check 锚点：** 至少包含 6 行（FMLA 风险、ADEA 风险、联邦 WARN 风险、Cal-WARN 风险、PIP 风险、pretext 风险）；severity 字段仅允许 `HIGH/MEDIUM/LOW`；FMLA 和 Cal-WARN 条目 severity = "HIGH"
- **难度向量：** V4（数字引用须与 Q1-Q12 一致），V3（P5 要求 CSV 使用 UTF-8 with BOM 编码）

### Q14 — OWBPA 豁免协议起草
- **目标意图：** 为 Marcus 的遣散协议起草符合 OWBPA 的豁免条款
- **产物：** `legal/owbpa_waiver_marcus.md`（含 21 天考虑期、7 天撤销期、ADEA 权利声明、律师咨询建议）
- **check 锚点：** 文件须包含 "21 days"、"7 days"（字面量）、"Age Discrimination in Employment Act"（全称）
- **难度向量：** V9（verbatim 引用法律全称），V3（P2 要求正式文件使用特定文件头格式）

### Q15 — EEOC 申诉表草稿（Marcus 视角）
- **目标意图：** 基于 Marcus 的陈述，起草 EEOC 投诉摘要（不代表真实提交，属内部风险评估文件）
- **产物：** `legal/eeoc_complaint_draft.json`（字段：`complainant`、`respondent`、`bases_of_discrimination: []`、`date_of_harm`、`filing_deadline`、`claims: []`）
- **check 锚点：** `bases_of_discrimination` 须含 `"age"` 和 `"FMLA retaliation"`；`filing_deadline` 须与 Q9 输出一致
- **难度向量：** V4（日期闭合），V8（JSON 结构校验）

### Q16 — 最终合规 SHA-256 校验令牌
- **目标意图：** 运行校验脚本，对 `reports/risk_matrix_final.csv` 计算 SHA-256，并将结果写入 `reports/signoff.txt`
- **产物：** `reports/signoff.txt`（格式：`VERIFIED:<sha256hex>`）
- **check 锚点：** check 脚本独立重算 SHA-256 并比对，格式须精确匹配 `VERIFIED:[a-f0-9]{64}`
- **难度向量：** V7（必须真正运行 Bash `sha256sum` 命令，无法凭空编造哈希值）

---

## Update 设计（含 supersede）

### Update 1（Q2/Q3 之后注入）
- **触发时机：** Q2 完成后（PIP 合规分析结果已出）
- **注入内容：** 飞书群聊新消息（S-FEISHU 追加）+ `pip_case/marcus_webb_pip_v2.md`（修订后 30 天 PIP）+ HR Director 邮件确认修订
- **体量：** ≈ 35KB（pip_v2 文档 12KB + 飞书历史追加 15KB + 邮件 8KB）
- **影响：** Q3 之后所有对 Marcus PIP 的引用须改为 v2（30 天合规版本）；Q2 中 `compliant = false` 的结论针对 v1 仍成立，但后续行动计划须基于 v2
- **supersede 性质：** 无（Update 1 属于补充新文件，非撤回）

### Update 2（Q7/Q8 之后注入，含 supersede）— 核心 supersede
- **触发时机：** Q8 完成后（ADEA/OWBPA 分析已出）
- **注入内容：**
  - `layoff/restructuring_plan_v2.md`（裁员从 58 人降至 31 人，SD 办公室保留，改为仅关闭 NYC 一处）
  - GC 邮件（v2 备忘录）撤回 v1 中"无需通知"的结论，但新增"NYC 裁员是否触发 NYS WARN"问题
  - `layoff/affected_employees_list_v2.csv`（更新后名单）
- **体量：** ≈ 45KB（plan_v2 18KB + 邮件 10KB + 名单 v2 17KB）
- **supersede 性质：** **是**（GC v2 邮件明确撤回 v1 中"low federal threshold"判断；Q7 的 `triggered: true` 结论被 Q12 的 `triggered: false` 替代）
- **影响：** Q12 须识别此 supersede 关系并记录，而非将 v1 与 v2 结论简单叠加

### Update 3（Q13 之后注入）
- **触发时机：** Q13 综合风险矩阵输出后
- **注入内容：** Outside Counsel（S-DISCORD）发送新 DM，补充指出：Marcus 的遣散协议初稿缺少 "written advice to consult an attorney" 条款（OWBPA 必要元素），要求 24 小时内修订
- **体量：** ≈ 32KB（Discord DM 追加 8KB + 修订版 OWBPA 模板 18KB + 法律意见书 6KB）
- **影响：** Q14 须在豁免协议中明确加入律师咨询建议条款

---

## 4-5 条 Preference 规则

| ID | 内容 | 注入方式 | 静默考察轮次 |
|----|------|---------|------------|
| P1 | 所有 JSON 输出必须包含顶层字段 `"reasoning": "..."` 用于解释判断依据，不得省略 | Q1 前用户显式说明 | Q5、Q8、Q15 |
| P2 | 正式法律文件（WARN 通知、OWBPA 协议）须在文件最顶部包含格式固定的 header：`Document: [名称] | Version: [n.n] | Date: [YYYY-MM-DD] | Status: [DRAFT/FINAL]` | Q10 前 feedback 注入 | Q11、Q14 |
| P3 | 所有对外通知草稿（warn_notice_*.md）须在 footer 注明：`Prepared by: People Operations | Review required before distribution` | Q10 前显式说明 | Q11 |
| P4 | 引用法律条款时必须使用完整 citation 格式（如 `29 U.S.C. § 2101(a)(2)`），不得仅写法律名称 | Q5 前显式说明 | Q6、Q9、Q14 |
| P5 | CSV 文件须使用 UTF-8 with BOM 编码（`﻿` 开头），字段用英文逗号分隔，首行为 header | Q13 前 feedback 注入 | Q13、Q16 校验阶段 |

---

## 难度向量汇总（绑定轮次）

| 向量 | 描述 | 绑定轮次 |
|-----|------|---------|
| V1 | 多源信息冲突综合 | Q3（DM vs 档案日期）、Q4（bot 摘要 vs 日志）、Q8（Slack 误引 45 天） |
| V2 | 动态 update 反转 | Q12（Update 2 裁员缩减反转 NYS WARN 触发结论） |
| V3 | 隐式 preference 静默考察 | Q11（P2/P3）、Q13（P5）、Q14（P2） |
| V4 | 跨轮数值/事实闭合 | Q3（工时 1310 延续）、Q9（解雇日期延续）、Q13（数值一致性）、Q15（deadline 闭合）|
| V5 | 失真自动摘要诱饵 | Q4（Slack bot 摘要错误声称承包商时间线）、Q5（GC v1 备忘录"500 人"错误结论） |
| V6 | 废弃副本红鲱鱼 | Q2（pip_v1 是废弃版，Update 1 后不得再引用 pip_v1 作为现行 PIP） |
| V7 | Bash SHA-256 sign-off | Q16（必须运行 sha256sum，写入 VERIFIED:<hex>） |
| V8 | schema-by-shape 严格 check | Q1、Q2、Q8、Q15 |
| V9 | 真实来源字段 verbatim 引用 | Q5（29 U.S.C. § 2101 条文）、Q6（Labor Code § 1400）、Q9（Title VII 全称）、Q11（EDD 全名）、Q14（ADEA 全名） |
| V10 | supersede 辨别 | Q12（须记录 Q7 被替代，不得叠加） |

---

## 拆分建议

本场景素材极其丰富，理论上可拆分为两个独立场景：

**方案 A — sci5a：PIP 与 FMLA/ADEA 个人纠纷**（Q1-Q9 + Q14-Q16）
**方案 B — sci5b：WARN Act 多州合规与大规模裁员**（Q5-Q7 + Q10-Q13 + Q16）

但由于两条主线的数据（员工名单、工资单、公司规模）高度重合，建议作为单一场景保留，通过 6 个 session 和三次 update 充分展现交叉复杂度。

---

## 可行性说明

- **素材充足度：** Strong — 联邦/州级劳动法条文、EEOC 官方指南、SHRM 最佳实践、OPM 法规均为公开真实文档，锚点数值可回溯至具体 URL
- **体量可行：** 员工名单（320 行）、薪资表、5 份法律备忘录、多渠道聊天历史，合成后远超 100k tokens
- **主要风险：** PIP "30 天最低标准"属行业惯例（SHRM 建议），非法定强制要求，须在场景叙事中将其锚定为"公司 HR 手册政策承诺"，使违反成为可检验的合同/政策违规而非纯法律违规
