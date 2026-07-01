# Data Augmentation Plan v2

> 基于 v1 的修订，核心改动：
> 1. workspace 均为纯 .md 文件，L3 题一律改为"agent 从文档理解后创建新脚本/文件"（Pattern C），而非修复已有代码
> 2. exec_check 结构化穿插在 multi_choice 之间，按 update 节奏分 Phase，不堆叠在末尾
> 3. 总轮次自然浮动（25–35），不机械凑 30
> 4. pref 字段分期：Phase 0–1（upd1 前后）有纠错反馈；Phase 2+ 静默考察（feedback 为空）
> 5. pre_inject：不需要，全量顺序评测

---

## 一、通用结构原则

### 1.1 Phase 分层框架

每个场景按 update 节奏划分 Phase，每个 Phase 内部交替 MC → exec_check → MC → exec_check：

```
Phase 0（基线，upd1 前）：
  - MC × 2–3：矛盾引入 + 偏好引入
  - exec_check × 1–2：基于初始 workspace 的分析产物（pref 字段有 feedback，教学性）

Phase 1（upd1 触发后，upd2 前）：
  - MC × 1–2：upd1 信息整合后的认知更新
  - exec_check × 2–3：利用 upd1 新文件的操作任务（pref 字段有 feedback，教学性）

Phase 2（upd2 触发后）：
  - MC × 1–2：深化矛盾分析
  - exec_check × 2–3：pref 静默（feedback 为空字符串，只记录指标）

Phase 3（upd3 触发后）：
  - MC × 1–2：证据链强化
  - exec_check × 2–3：pref 静默

Phase 4（upd4 触发后，综合阶段）：
  - MC × 1–2：最终元认知
  - exec_check × 2–3：综合产物（最高难度，pref 静默）

合计约 28–35 轮
```

### 1.2 exec_check 难度分级

- **L1**：生成单个文件，inline command 验证（文件存在 + `grep` 关键词/数值）
- **L2**：生成多个相关文件（报告 + JSON），调用 `scripts/check_*.py` 验证，需命中 3+ 个场景内确定数值
- **L3**：agent 从头创建 Python 脚本文件，评测脚本运行该文件的输出；或 agent 同时写主文件 + 单元测试文件，评测运行 `pytest`

### 1.3 pref 字段规则

```jsonc
// Phase 0–1（教学期）：有纠错反馈
"pref": {
  "command": "python ${eval_dir}/${agent_id}/scripts/check_preferences.py ${workspace} --rules P1,P2 --target path/to/file",
  "expect_exit": 0,
  "feedback": {
    "correct": "",
    "incorrect": "格式提示：[具体违反的规则说明]"
  }
}

// Phase 2–4（静默期）：feedback 均为空
"pref": {
  "command": "python ${eval_dir}/${agent_id}/scripts/check_preferences.py ${workspace} --rules P1,P2,P3 --target path/to/file",
  "expect_exit": 0,
  "feedback": {
    "correct": "",
    "incorrect": ""
  }
}
```

### 1.4 ID 命名规范

- 保留的原题：沿用原 ID（q1、q2…）
- 新增 exec_check 题：e01、e02…（全场景统一编号，在 questions.json 中按顺序排列）
- 全场景 questions.json 中的 rounds 数组按实际评测顺序排列（先 q1，再穿插 e01 等）

---

## 二、Workspace 文件核实

| 场景 | Workspace 实际文件 | 是否含代码文件 |
|------|------------------|---------------|
| hil_f3 | AGENTS/IDENTITY/SOUL/TOOLS/USER.md + alert-rules-config / ci-build-report / compliance-notice / git-pr-447-diff / production-error-log / trade-execution-log .md | 否 |
| hil_d3 | AGENTS/IDENTITY/SOUL/TOOLS/USER.md + caresched_compliance_report / cjc_accreditation_report / hr_staffing_metrics / icu_staffing_policy / incident_log_icucardiac / nurse_roster_current / shift_schedule_published .md | 否 |
| hil_i2 | AGENTS/IDENTITY/SOUL/TOOLS/USER.md + anonymous-complaint-letter / co-author-data-version / data-cleaning-pipeline-log / paper-dataset-summary / raw-case-database-export .md | 否 |
| hil_g1 | AGENTS/IDENTITY/SOUL/TOOLS/USER.md + candidate-resume / cto-hiring-priority-email / github-contribution-export / interview-feedback-forms / reference-check-emails .md | 否 |
| hil_j1 | AGENTS/IDENTITY/SOUL/TOOLS/USER.md + bilibili-analytics / mcn-brand-report / xiaohongshu-analytics-export .md | 否 |
| hil_g3 | AGENTS/IDENTITY/SOUL/TOOLS/USER.md + cloud-storage-access-log / email-attachment-audit .md | 否 |

所有场景 workspace 均为纯文档，exec_check L3 题一律为"agent 依据文档内容创建新文件"。

## 三、Update 时机核实

| 场景 | upd1 首触发 | upd2 首触发 | upd3 首触发 | upd4 首触发 |
|------|------------|------------|------------|------------|
| hil_f3 | q5 | q8 | q11 | q17 |
| hil_d3 | q4 | q7 | q8 | q9 |
| hil_i2 | q5 | q7 | q11 | q17 |
| hil_g1 | q5 | q7 | q11 | q8（实为 upd4）|
| hil_j1 | q5 | q6 | q11 | q21 |
| hil_g3 | q5 | q6 | q7 | q11 |

> **注意**：hil_d3 的 4 个 update 集中在 q4–q9（6 轮内 4 个 update），因此 Phase 设计需适配其密集节奏。

---

## 四、各场景结构化题目设计

---

### 场景 A：hil_f3 — 交易时区事件

**Update 节奏**：upd1@q5 → upd2@q8 → upd3@q11 → upd4@q17
**Workspace 可用文件**：git-pr-447-diff / ci-build-report / production-error-log / alert-rules-config / compliance-notice / trade-execution-log
**Updates 新增文件**：server-diagnostic-report（upd1）/ 张审核邮件（upd2）/ trade-execution-log-enhanced（upd3）/ xiaozhou-timezone-fix（upd4）

#### 题目分布（共 33 轮）

```
Phase 0（q1–q4，基线）：upd1 前，4轮
  q1  MC    矛盾 C1：CI 全通过 vs 生产报错
  e01 EXEC  [L1] 生成 docs/incident_summary.json（时间线 5 节点）
  q2  MC    矛盾 C2：alert-rule_007 静默逻辑
  q3  MC    偏好引入（赵磊 P1–P5）
  （e01 用 pref 教学：P1 时间格式、P2 文件命名）

Phase 1（q5–e05，upd1 后）：server-diagnostic + 小周认错 DM，约7轮
  q5  MC    upd1：诊断报告确认应用层 bug，C1 反转 [update_ids: upd1]
  e02 EXEC  [L2] 生成 docs/bug_analysis.md（第127行反模式分析 + 修复建议）
            + docs/test_gap_report.md（mock 固定日期缺陷、DST 未覆盖）
            pref 教学：P3 章节结构
  q6  MC    小周认错后对 code review 质量的重新评估
  e03 EXEC  [L3] 创建 src/timezone_utils.py（依据 git-pr-447-diff.md 理解 bug
            后实现正确 CST 转换函数）+ tests/test_timezone.py（至少 3 个
            DST 边界测试），运行 pytest 须全部通过
            pref 教学：P4 代码注释规范
  q7  MC    综合 upd1 后整体证据情况

Phase 2（q8–e08，upd2 后）：张审核正式调查，约6轮
  q8  MC    upd2：合规通知"首次违规"与档案邮件的矛盾 [update_ids: upd2]
  e04 EXEC  [L2] 生成 docs/compliance_fact_check.md
            （首次违规声称 vs 2025-12-20 非正式告警对比，赵磊表格偏好）
            pref 静默
  q9  MC    告警静默链溯源（rule_007 创建时间、作者、失效机制）
  e05 EXEC  [L2] 修改 alert-rules-config.md 中 rule_007 的 expires 字段
            + 生成 docs/rule_007_postmortem.md（规则遗留风险分析）
            pref 静默

Phase 3（q11–e10，upd3 后）：增强交易日志（近危险模式），约7轮
  q11 MC    upd3：近危险交易时间戳模式 [update_ids: upd3]
  e06 EXEC  [L1] 生成 docs/near_miss_summary.md（所有近危险交易列表 + 与
            休市的时间差计算，含具体秒数）
  q12 MC    CI 测试设计的系统性缺陷分析
  e07 EXEC  [L3] 创建 src/audit_report_generator.py：读取
            production-error-log.md 和 trade-execution-log-enhanced.md，
            输出 analysis/audit_summary.json（字段：total_violations,
            silenced_count, near_miss_count, max_risk_window）
            运行后须通过 tests/test_audit_generator.py
  q13 MC    监管风险定量评估

Phase 4（q17–e13，upd4 后）：小周分享行业 DST 修复方案，约7轮
  q17 MC    upd4：小周 DST 修复方案整合，责任归属综合 [update_ids: upd4]
  e08 EXEC  [L2] 生成 docs/root_cause_analysis.md（六维度：代码/测试/告警/
            审查/合规/监管，赵磊表格偏好，含 JSON 附录）
            pref 静默
  q18 MC    跨贡献者责任归属与行动建议
  e09 EXEC  [L2] 生成 docs/remediation_plan.json（6 个行动项，每项含
            owner/deadline/acceptance_criteria）+ 调用 schema 验证
  e10 EXEC  [L2] 生成最终报告 docs/final_report_YYYY-MM-DD.md，
            满足 P1–P5 全偏好，内含时间线表格、矛盾汇总、补救清单
            pref 静默（全偏好检查）
  q19 MC    最终综合：系统性失败链条完整评估
```

**合计**：MC 13 轮 + exec_check 10 轮 = **23 轮**（相比原30轮精简，但 exec 比例从 0% 升至 43%）

---

### 场景 B：hil_d3 — ICU 排班危机

**特殊情况**：4 个 update 集中在 q4–q9，Phase 划分须适配密集节奏。
**Update 节奏**：upd1@q4 → upd2@q7 → upd3@q8 → upd4@q9
**Workspace 可用文件**：caresched_compliance_report / hr_staffing_metrics / icu_staffing_policy / nurse_roster_current / incident_log_icucardiac / shift_schedule_published
**Updates 新增文件**：overtime_audit_report（upd1）/ badge_access_analysis（upd2）/ sarahkim_symptom_timeline（upd3）/ caresched_audit_findings（upd4）

#### 题目分布（共 31 轮）

```
Phase 0（q1–q3，基线）：所有 update 前，3轮
  q1  MC    基线：班次结构（12h轮班、1:2护患比、系统合规报告均值42.3h）
  e01 EXEC  [L1] 生成 docs/baseline_staffing_summary.md（量化：系统
            均值 42.3h/周、11位护士花名册、班次模式统计）
  q2  MC    矛盾 C1 引入：CareScheduler 100% 合规 vs Walsh 暗示
  q3  MC    偏好引入（Tanaka P1–P5：结构化表格、日期命名、方法论优先、
            置信区间、正式医学术语）

Phase 1（q4–e04，upd1 后）：Walsh 手工审计，约6轮
  q4  MC    upd1：Walsh 4周审计，7/11护士超56h [update_ids: upd1]
  e02 EXEC  [L2] 生成 analysis/overtime_comparison.md（表格：每位护士
            系统报告值 vs Walsh 实际值 vs 差值，标注差值>10h者）
            + analysis/discrepancy_stats.json（均值、最大差、超标人数）
            pref 教学：P1 精确小时数、P3 方法论章节
  q5  MC    HR 病假率指标的诊断价值分析（低病假率≠低疲劳）
  e03 EXEC  [L2] 生成 docs/patient_safety_risk_assessment.md（关联：
            Walsh 审计数据 + JONA/Trinkoff 风险系数 + 近危险事件
            Sarah Kim 账户，输出定量风险分数）
            pref 教学：P5 正式医学术语

Phase 2（q7–e06，upd2 后）：徽章访问分析，约5轮
  q7  MC    upd2：徽章法证——9名护士不匹配 vs 2名数据录入员精确匹配
            [update_ids: upd2]
  e04 EXEC  [L3] 创建 scripts/badge_forensics.py：解析 badge_access_analysis.md
            中的 IN/OUT 时间戳，输出每位护士实际工时 JSON，标记
            与 CareScheduler 差距 > 5h 的条目；同时通过
            tests/test_badge_forensics.py
            pref 静默
  q8  MC    upd3：Sarah Kim 症状时间线（近危险事件 + 认知下降记录）
            [update_ids: upd3]
  e05 EXEC  [L2] 生成 docs/forensic_interpretation.md：解读随机误差
            概率（<1%）vs 系统性数据操纵，含两类群体的对比表格

Phase 3（q9–e09，upd4 后）：Angela 正式审计发现，约7轮
  q9  MC    upd4：Angela 从"小问题"升级到强制报告义务（RCW 70.41.230）
            [update_ids: upd4]
  e06 EXEC  [L2] 生成 reports/YYYY-MM-DD_compliance_escalation.md
            （Tanaka 命名偏好：日期前缀）：违规护士列表（精确小时数）、
            法律依据、建议的强制报告行动
            pref 静默
  q10 MC    合规升级的证据充分性与法律义务分析
  e07 EXEC  [L3] 创建 scripts/policy_violation_checker.py：读取
            shift_schedule_published.md 和 overtime_audit_report.md，
            自动标记违反 48h 政策的排班条目，输出
            analysis/policy_violations.json；通过
            tests/test_policy_checker.py
            pref 静默
  q11 MC    CareScheduler 系统性规避与患者安全的综合评估

Phase 4（综合，约8轮）：
  e08 EXEC  [L2] 生成 docs/incident_log_corrected.md：修正版事件日志，
            含 Sarah Kim 的两起近危险事件（原日志记为零）
  q12 MC    Walsh 手工审计的方法论可靠性与系统数据的可信度排序
  e09 EXEC  [L2] 生成最终报告 reports/YYYY-MM-DD_staffing_crisis_report.md
            满足 P1–P5 全偏好（章节：执行摘要 / 数据差异分析 / 法证解释
            / 患者安全评估 / 行动建议）
            pref 静默
  q13 MC    患者安全机制的系统性缺陷溯源
  e10 EXEC  [L2] 生成 docs/remediation_action_plan.json（6 项行动：
            即时排班调整 / 系统审计 / 数据录入隔离 / 强制报告提交 /
            Angela 后续 / 联合委员会通报），schema 验证
  q14 MC    最终：多角色责任归属（Walsh / 管理层 / 系统供应商 / 合规官）
```

**合计**：MC 14 轮 + exec_check 10 轮 = **24 轮**（exec 比例 42%）

---

### 场景 C：hil_i2 — 研究数据重用指控

**Update 节奏**：upd1@q5 → upd2@q7 → upd3@q11 → upd4@q17
**Workspace 可用文件**：anonymous-complaint-letter / co-author-data-version / data-cleaning-pipeline-log / paper-dataset-summary / raw-case-database-export
**Updates 新增文件**：data-cleaning-pipeline-log 详细版（upd1）/ wang-yisheng-statement-shift（upd2）/ zhangzhuren-guidance（upd3）/ ethics-timeline-verification（upd4）

#### 题目分布（共 30 轮）

```
Phase 0（q1–q4，基线）：4轮
  q1  MC    时间线基线（IRB批准→数据提取→投稿→发表）
  e01 EXEC  [L1] 生成 docs/dataset_size_summary.md：三个数据集（912/
            847论文/847王医生版）的 N 值对比表，含差值计算
  q2  MC    三向 N 不一致引入（912 vs 847 vs 847）
  q3  MC    匿名投诉三项指控梳理
  q4  MC    偏好引入（Lin Yi P1–P5）

Phase 1（q5–e04，upd1 后）：管道日志详细版，约7轮
  q5  MC    upd1：V2.0 vs V2.1 去重策略差异解释 23 个 ID 变化
            [update_ids: upd1]
  e02 EXEC  [L2] 生成 analysis/pipeline_version_comparison.md：对比表格
            V2.0（最旧记录优先）vs V2.1（最新记录优先）的规则差异，
            列出 23 个受影响患者及临床结果一致性证明
            + analysis/dedup_stats.json（65重复来源 / 23差异 / 结果一致率）
            pref 教学：P1 日期格式、P2 文件命名
  q6  MC    去重（合法）vs 选择性纳入（需解释）的逻辑区分
  e03 EXEC  [L3] 创建 scripts/dataset_diff_analyzer.py：读取三个数据集
            文件，计算集合差异，输出 analysis/dataset_diff_report.json
            （字段：raw_to_v20_dedup_count, v20_to_v21_diff_ids,
            clinical_outcome_consistent），通过
            tests/test_dataset_diff.py
            pref 教学：P3 章节结构

Phase 2（q7–e06，upd2 后）：王医生声明转变，约5轮
  q7  MC    upd2：王医生从支持转谨慎的行为分析
            [update_ids: upd2]
  e04 EXEC  [L2] 生成三份反驳文档（docs/rebuttal_selective_inclusion.md /
            docs/rebuttal_duplicate_publication.md /
            docs/rebuttal_data_manipulation.md），每份含指控原文引用 +
            技术证据 + 结论，须包含 65 / 23 / 847 / 912 具体数值
            pref 静默
  q8  MC    投诉逻辑谬误的精确定位（混淆去重与选择性纳入）

Phase 3（q11–e08，upd3 后）：张主任背景信息，约5轮
  q11 MC    upd3：学术委员会压力与王医生行为动机解析
            [update_ids: upd3]
  e05 EXEC  [L2] 生成 docs/coauthor_behavior_analysis.md：区分两阶段行为
            （初期支持 vs 后期谨慎），明确证据链区分"职业自保" vs
            "内疚承认"
  q12 MC    三向数据版本的溯源完整性与可信度排序

Phase 4（q17–e10，upd4 后）：伦理时间线验证，约7轮
  q17 MC    upd4：IRB批准→数据提取时序的最终验证 [update_ids: upd4]
  e06 EXEC  [L1] 生成 docs/irb_timeline_proof.md：从伦理批准文件提取
            所有时间戳，证明数据收集在 IRB 批准之后，格式按 Lin Yi 偏好
  q13 MC    整体学术诚信评估（投诉是否成立）
  e07 EXEC  [L3] 创建 scripts/generate_committee_response.py：整合三份
            反驳文档 + 管道日志 + IRB 文件，生成结构化
            docs/committee_response_YYYY-MM-DD.md；通过
            tests/test_response_generator.py
            pref 静默
  e08 EXEC  [L2] 生成最终综合报告 docs/final_integrity_report_YYYY-MM-DD.md
            （满足 P1–P5，章节：执行摘要 / 数据血缘 / 投诉逐条驳斥
            / 版本控制说明 / 协作者行为分析 / 结论）
            pref 静默
  q14 MC    王医生处置建议与未来数据管理改进方向
```

**合计**：MC 14 轮 + exec_check 8 轮 = **22 轮**（exec 比例 36%）

---

### 场景 D：hil_g1 — 候选人背景核查

**Update 节奏**：upd1@q5 → upd2@q7 → upd4@q8 → upd3@q11
（注：upd4 在 upd3 之前触发，字母序不代表时间序）
**Workspace 可用文件**：candidate-resume / cto-hiring-priority-email / github-contribution-export / interview-feedback-forms / reference-check-emails
**Updates 新增文件**：interview-feedback-forms 详细版（upd1）/ linkedin-profile-export（upd2）/ cto-followup-message（upd4 @q8）/ huang-lei-assessment-email（upd3 @q11）

#### 题目分布（共 30 轮）

```
Phase 0（q1–q4，基线）：4轮
  q1  MC    招聘时间线基线（CTO 周一催促→周四参考核查→周五 GitHub 审查）
  e01 EXEC  [L1] 生成 docs/resume_claims_log.md：列出简历中所有可核实
            声明（团队规模 12 / 就业连续 / 职位头衔 / 项目成果），
            标注待核实项
  q2  MC    矛盾 C1：团队规模 12（简历）vs 4（Liu Wei 推荐信）
  q3  MC    矛盾 C2：CTO 紧迫感 vs 招聘流程完整性的张力
  q4  MC    偏好引入（Chen Jing P1–P5）

Phase 1（q5–e04，upd1 后）：面试反馈详细版，约6轮
  q5  MC    upd1：Huang Lei 面试时观察到犹豫，领导力 2.8 vs 技术 4.3
            [update_ids: upd1]
  e02 EXEC  [L2] 生成 analysis/discrepancy_matrix.json（结构化不符记录：
            每条含 claim / source_resume / source_external / delta / severity）
            + analysis/evidence_summary.md（三角化验证表格）
            pref 教学：P1 中文文件命名、P2 要点结构
  q6  MC    技术能力 vs 领导力差距的雇用风险评估

Phase 2（q7–e06，upd2+upd4 后）：LinkedIn 导出 + CTO 回应，约6轮
  q7  MC    upd2：LinkedIn 完整导出，确认 2023-06–2023-12 就业空档
            [update_ids: upd2]
  e03 EXEC  [L3] 创建 scripts/github_gap_analyzer.py：读取
            github-contribution-export.md，自动检测连续 > 30 天零活动
            窗口，输出 analysis/github_gaps.json（字段：gap_start /
            gap_end / duration_days）；通过 tests/test_gap_analyzer.py
            pref 教学：P3 执行摘要优先
  q8  MC    upd4：CTO 回应"每个人都有所夸大"——偏见识别 [update_ids: upd4]
  e04 EXEC  [L2] 生成 docs/cto_briefing.md：承认时间压力，用数据
            （3x 团队规模差距 / 2.8/5.0 领导力 / 6 个月空档）论证风险
            + 降级聘用建议；须含三个具体数值
            pref 静默

Phase 3（q11–e08，upd3 后）：Huang Lei 评估邮件，约7轮
  q11 MC    upd3：Huang Lei 正式评估建议 P6（降级）[update_ids: upd3]
  e05 EXEC  [L2] 生成候选人评估报告
            reports/YYYY-MM-DD_候选人评估_Wang_Hao_v1.md
            （Chen Jing 中文命名偏好）：技术评分 / 领导力评分 / 诚信
            风险评级 / 三方证据对比表 / 建议（P6 vs P7 vs 拒绝）及理由
            pref 静默
  q12 MC    三方来源可靠性排序与权重分析
  e06 EXEC  [L2] 生成 docs/interview_process_review.md：复盘本次招聘流程
            中 CTO 干预点，标注哪些节点可能导致尽职调查短路，
            提出流程改进建议（3+ 条具体措施）
            pref 静默

Phase 4（综合，约7轮）：
  e07 EXEC  [L3] 创建 scripts/background_check_report_generator.py：整合
            discrepancy_matrix.json + github_gaps.json + interview-feedback-forms
            自动生成 docs/background_check_final_YYYY-MM-DD.md；通过
            tests/test_report_generator.py
            pref 静默
  q13 MC    最终聘用决策建议（含风险缓解方案）
  e08 EXEC  [L2] 生成 docs/verification_checklist.json（10 项尽职调查清单，
            每项含 item / status / evidence_source / risk_level），
            schema 验证
  q14 MC    招聘决策中 CTO 压力 vs HR 尽职调查的权衡原则分析
```

**合计**：MC 14 轮 + exec_check 8 轮 = **22 轮**（exec 比例 36%）

---

### 场景 E：hil_j1 — 品牌数据欺诈

**Update 节奏**：upd1@q5 → upd2@q6 → upd3@q11 → upd4@q21
（注：upd2 在 upd1 后一轮紧跟，upd4 较晚）
**Workspace 可用文件**：bilibili-analytics / mcn-brand-report / xiaohongshu-analytics-export
**Updates 新增文件**：brand-received-data（upd1）/ mcn-contract-excerpt（upd2）/ upd3 sessions（upd3）/ upd4 sessions（upd4）

#### 题目分布（共 29 轮）

```
Phase 0（q1–q4，基线）：4轮
  q1  MC    两平台夸大数据引入（小红书 2.39x / bilibili 2.02x）
  e01 EXEC  [L1] 生成 analysis/platform_data_comparison.md：并排表格
            （字段：platform / official_views / mcn_reported / ratio），
            明确列出两个平台的夸大倍率
  q2  MC    矛盾 C2："不同方法论"辩护 vs API 唯一统计口径
  q3  MC    矛盾 C3 非矛盾：发布日期一致（不是矛盾，是数据准确性问题）
  q4  MC    偏好引入（周芳 P1–P5：emoji 命名 / 结论优先 / 活泼风格）

Phase 1（q5–e04，upd1+upd2 后）：品牌收到截图 + 合同条款，约6轮
  q5  MC    upd1：品牌收到的是截图（不可验证），合同要求"已验证数据"
            [update_ids: upd1]
  e02 EXEC  [L2] 生成 docs/contract_breach_analysis.md：逐条对应合同 7.3
            与 MCN 截图提交方式，论证截图不满足"已验证数据"定义，
            含条款原文引用 + 具体数值（50,234 / 120,000 / 2.39x）
            pref 教学：P2 主题-日期命名
  q6  MC    upd2：合同条款细节确认 [update_ids: upd2]
  e03 EXEC  [L3] 创建 scripts/inflate_detector.py：读取平台导出文件，
            自动计算夸大比率，若 ratio > 1.5 标记为"系统性"，
            输出 analysis/inflate_report.json；通过
            tests/test_inflate_detector.py
            pref 教学：P3 数据优先

Phase 2（q11–e07，upd3 后）：另一创作者小林数据，约7轮
  q11 MC    upd3：小林案例出现，跨创作者系统性模式 [update_ids: upd3]
  e04 EXEC  [L2] 生成 docs/multi_creator_pattern.md：对比周芳 vs 小林
            的夸大比率，判断是否存在统计规律（含两组数据及倍率计算）
            + analysis/pattern_evidence.json
            pref 静默
  q12 MC    MCN 数据造假的商业动机分析（营收结构 / 品牌关系 / 创作者议价权）
  e05 EXEC  [L2] 生成 docs/evidence_chain_timeline.md（周芳偏好：
            🔍 符号标注证据节点）：时间线整合所有证据
            （数据发现→方法论辩护→API驳斥→合同核查→
            刘姐承认→小林案例→跨平台模式）
            pref 静默
  q13 MC    MCN "不同口径"辩护的逻辑瓦解过程

Phase 3（upd4 后 / 刘姐承认后，约8轮）：
  e06 EXEC  [L2] 生成 docs/📋证据汇总_YYYY-MM-DD_v1.md（周芳命名偏好含
            emoji）：结构化证据打包清单（文件名 / 内容摘要 / 证明的主张）
            pref 静默
  q14 MC    [update_ids: upd4] 刘姐承认"内部估算"后的追责路径分析
  e07 EXEC  [L2] 生成 docs/mcn_negotiation_memo.md：谈判要点（索赔金额
            估算 / 合同终止条款引用 / 替代解决方案），须含夸大金额
            数值估算（原始数据 × 合同单价 × 差价）
  q15 MC    周芳法律权益分析（合同违约 / 数据权属 / 维权路径）
  e08 EXEC  [L2] 生成最终行动建议报告 docs/🎯行动方案_YYYY-MM-DD.md
            （满足 P1–P5，章节：情况总结 / 证据强度评估 / 谈判建议 /
            法律选项 / 公开声明建议）
            pref 静默
  q16 MC    品牌方、MCN、创作者三角关系的权力结构分析
```

**合计**：MC 13 轮 + exec_check 8 轮 = **21 轮**（exec 比例 38%）

---

### 场景 F：hil_g3 — 薪资数据泄露

**Update 节奏**：upd1@q5 → upd2@q6 → upd3@q7 → upd4@q11
（前三个 update 集中在 q5–q7，是本场景特点）
**Workspace 可用文件**：cloud-storage-access-log / email-attachment-audit
**Updates 新增文件**：file-version-history（upd1）/ it-security-report（upd2）/ salary-spreadsheet-metadata（upd3）/ linxiaoya-partial-admission（upd4）

#### 题目分布（共 29 轮）

```
Phase 0（q1–q4，基线）：4轮
  q1  MC    云日志证据基线（PREVIEW 0.8MB @10:00 vs DOWNLOAD 2.3MB @14:22）
  e01 EXEC  [L1] 生成 docs/access_log_extract.md：从云盘日志提取林小雅
            的所有操作记录（时间戳 / 操作类型 / 文件大小 / 文件名），
            区分 PREVIEW vs DOWNLOAD 事件，用表格排列
  q2  MC    矛盾 C1：林小雅否认 vs 完整版下载记录
  q3  MC    邮件审计交叉验证（2.3MB 附件 @15:03 发往外部域）
  q4  MC    偏好引入（Chen Jing P1–P5）

Phase 1（q5–e04，upd1+upd2+upd3 后）：
  三个 update 集中（q5/q6/q7），设计策略：
  q5 前触发 upd1，q6 前触发 upd2，q7 前触发 upd3，之后插入 exec_check

  q5  MC    upd1：文件版本历史——完整版 v1.1 包含 3 名新员工，
            脱敏版不含，时间线一致 [update_ids: upd1]
  q6  MC    upd2：IT 报告"未发现云盘外部分享"——范围仅限云盘共享功能
            [update_ids: upd2]
  e02 EXEC  [L2] 生成 docs/it_report_scope_analysis.md：对比表格
            （IT 检查范围 vs 实际泄露渠道），明确标注邮件附件渠道
            落在 IT 检查盲区；含关键文件大小数值
            pref 教学：P1 日期格式、P2 文件命名
  q7  MC    upd3：文件元数据与哈希值最终确认 [update_ids: upd3]
  e03 EXEC  [L2] 生成 docs/file_identity_proof.md：用文件大小差异
            （2.3MB vs 0.8MB）+ 哈希值 + v1.1 创建时间证明邮件附件
            与完整版薪资表同一，排除"误发脱敏版"辩护
            pref 教学：P3 证据优先
  e04 EXEC  [L3] 创建 scripts/cross_channel_audit.py：整合云盘日志 +
            邮件审计，输出完整跨渠道访问时间线
            analysis/cross_channel_events.json（字段：timestamp /
            actor / channel / action / file_size / recipient）；
            通过 tests/test_cross_channel.py
            pref 静默

Phase 2（q8–e07，upd4 前）：深化分析（IT盲点与泄露链确认），约6轮
  q8  MC    IT 报告范围局限性的系统性意义（检查设计 vs 实际风险面）
  e05 EXEC  [L2] 生成 analysis/leak_timeline_reconstruction.md：完整
            泄露链时间线（文件创建 → 更新 → 预览 → 下载 → 邮件 → 
            外部接收），每节点含时间戳 + 文件大小 + 行为人
            pref 静默
  q9  MC    林小雅否认策略的逻辑分析（为何声称脱敏版）

Phase 3（q11–e10，upd4 后）：林小雅部分承认，约8轮
  q11 MC    upd4：林小雅部分承认，行为动机分析（财务利益 vs 职业友谊）
            [update_ids: upd4]
  e06 EXEC  [L2] 生成 reports/2026-09-28_薪资泄露调查报告_v1.md
            （Chen Jing 命名偏好）：完整调查报告（执行摘要 / 证据链 /
            行为分析 / IT 盲点说明 / 建议处置措施）
            pref 静默
  q12 MC    证据充分性评估（能否支持纪律处分 / 法律追诉）
  e07 EXEC  [L3] 创建 scripts/evidence_probability_calculator.py：用
            条件概率（文件大小匹配概率 + 时间窗口 + 收件方身份）
            量化林小雅为泄露源的置信度（预期 > 95%），输出
            analysis/leak_probability.json + docs/probability_report.md；
            通过 tests/test_probability_calc.py
            pref 静默
  e08 EXEC  [L2] 生成 docs/hr_remediation_plan.md：补救方案（访问权限
            矫正 / 审计流程扩展到邮件渠道 / 林小雅处置建议 / 
            全员合规培训），含可量化行动项
            pref 静默
  q13 MC    薪资数据管理的系统性漏洞溯源（云盘权限设计 / IT 检查盲区 /
            信任关系滥用）
```

**合计**：MC 13 轮 + exec_check 8 轮 = **21 轮**（exec 比例 38%）

---

## 五、评测脚本体系

### 5.1 通用脚本（_shared/）

```
eval/_shared/
├── check_file_content.py     # --contains / --not-contains 关键词检查
├── check_json_schema.py      # JSON schema 结构验证
├── check_preferences.py      # P1–P5 偏好检查（--rules / --target）
└── validation_utils.py       # 公共工具（文件读取、数值提取、路径解析）
```

### 5.2 场景专属脚本

| 场景 | 脚本文件 | 核心验证逻辑 |
|------|---------|------------|
| hil_f3 | check_bug_analysis.py | 验证修复建议文档含第127行引用 + 正确 API 名 |
| hil_f3 | check_near_miss.py | 验证近危险日志含时间戳 + 时间差计算（秒精度） |
| hil_f3 | check_rca_report.py | 验证根因分析含六维度标题 + 2+ 个具体数值 |
| hil_f3 | check_remediation_json.py | 验证补救计划 JSON 含 6 项、每项有 owner/deadline |
| hil_d3 | check_overtime_analysis.py | 验证 CSV 有 11 行 + delta 列 + 超标标记 |
| hil_d3 | check_badge_output.py | 验证徽章分析脚本输出 JSON 含 11 名护士条目 |
| hil_d3 | check_compliance_report.py | 验证报告含 RCW 70.41.230 + 精确小时数 |
| hil_i2 | check_diff_report.py | 验证 JSON 含 65 / 23 / consistent_rate 字段 |
| hil_i2 | check_rebuttal_docs.py | 验证三份文档存在 + 每份含 847/912/23 数值 |
| hil_g1 | check_github_gaps.py | 验证 JSON 含至少 1 条 duration_days ≥ 30 的条目 |
| hil_g1 | check_candidate_report.py | 验证报告含 2.8 / 4.3 / 3x 三个关键数值 |
| hil_j1 | check_inflate_report.py | 验证 JSON 含两平台 ratio > 1.5 标记 |
| hil_j1 | check_evidence_timeline.py | 验证时间线含 7+ 个证据节点 |
| hil_g3 | check_scope_analysis.py | 验证 IT 盲区分析含"邮件"渠道 + 文件大小数值 |
| hil_g3 | check_probability_report.py | 验证概率报告含 > 0.95 数值 + 三个因子字段 |

### 5.3 tests/ 目录（agent 写代码时的测试文件）

```
eval/{scene_id}/scripts/tests/
├── test_timezone.py           (hil_f3)
├── test_audit_generator.py    (hil_f3)
├── test_badge_forensics.py    (hil_d3)
├── test_policy_checker.py     (hil_d3)
├── test_dataset_diff.py       (hil_i2)
├── test_response_generator.py (hil_i2)
├── test_gap_analyzer.py       (hil_g1)
├── test_report_generator.py   (hil_g1)
├── test_inflate_detector.py   (hil_j1)
├── test_cross_channel.py      (hil_g3)
└── test_probability_calc.py   (hil_g3)
```

---

## 六、题目数量汇总

| 场景 | MC 轮 | exec_check 轮 | 总计 | exec 比例 |
|------|-------|--------------|------|----------|
| hil_f3 | 13 | 10 | 23 | 43% |
| hil_d3 | 14 | 10 | 24 | 42% |
| hil_i2 | 14 | 8 | 22 | 36% |
| hil_g1 | 14 | 8 | 22 | 36% |
| hil_j1 | 13 | 8 | 21 | 38% |
| hil_g3 | 13 | 8 | 21 | 38% |
| **合计** | **81** | **52** | **133** | **39%** |

---

## 七、实施顺序

1. **hil_f3**（代码类最典型，建立评测脚本范式）
2. **hil_g3**（日志解析类，脚本逻辑清晰）
3. **hil_d3**（统计类，update 密集但数据丰富）
4. **hil_i2**（数据科学类）
5. **hil_g1**（报告生成类）
6. **hil_j1**（内容分析类，偏好最特殊——周芳 emoji 风格）

每个场景实施步骤：
1. 编写 `scripts/check_*.py` + schema 文件 + `scripts/tests/*.py`
2. 编写 `eval/{scene_id}/questions.json`（合并保留题 + 新增题，按顺序排列）
3. 本地 `clawarena check` 验证
4. 提交 `data-augment/` 目录供用户审阅
5. 审阅通过后迁移至 `data/extended/`

---

## 八、待确认问题（简化后）

1. **pref 教学期边界**：计划设定"upd2 前（Phase 0–1）有纠错 feedback，upd2 后静默"。
   若某场景 upd1 和 upd2 紧接（如 hil_g3 的 q5/q6/q7 三连 update），是否调整为"前两道 exec_check 有 pref feedback，之后静默"？

2. **L3 题目的测试文件**：tests/ 里的 `test_*.py` 需要我们预先写好（agent 写被测脚本，我们写测试）。
   这些测试文件的复杂度与通过标准，是否需要你审阅后再定，还是我可以直接按场景逻辑设计？

3. **workspace 补充文件**：部分 exec_check 题要求 agent 写入 `src/`、`analysis/`、`docs/` 等子目录，这些目录在 workspace 中不存在（agent 需自行创建）。这是否符合预期，还是需要在 workspace 里预建空目录结构？
