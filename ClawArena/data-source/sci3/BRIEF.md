# BRIEF: sci3 — 医疗排班与护患比危机

## 场景叙事背景

Sutter Valley Medical Center（加州虚构综合医院，下称 SVMC）是一家 350 床位的 General Acute Care Hospital，须依照
California Health & Safety Code § 1276.4 及 Cal. Code Regs. Title 22 § 70217 维持法定护患比。
2024 年底，SVMC 多个科室深陷「护士荒」：ICU 编制缺口 3 人（在职护士离职 + FMLA 占用），
医外科（Med/Surg）夜班屡次超过 1:5 上限，CDPH 一次无预告抽查后出具 Statement of Deficiencies。
医院护理总监（CNO）Miranda Chen 聘用 AI scheduling agent 协助：
1. 重新制定各科室未来两周的排班方案，保证合规；
2. 准备 CDPH 报告所需的 staffing log（CSV 格式）；
3. 在两次 update（含一次 supersede）后，根据新增信息修订合规报告与排班策略；
4. 最终产出可提交监管机构的文档包。

场景同时引入多渠道 history（CNO Slack DM、护士工会 Email、CDPH 来函 PDF、
合规顾问飞书群），制造多源信息冲突与时间线诱饵。

---

## 真实来源链接表

| # | 标题 | URL | 类型 |
|---|------|-----|------|
| S1 | Cal. Code Regs. Tit. 22 § 70217 — Nursing Service Staff (LII) | https://www.law.cornell.edu/regulations/california/Cal-Code-Regs-Tit-22-SS-70217 | regulation |
| S2 | California Health & Safety Code § 1276.4 (OneCle) | https://law.onecle.com/california/health/1276.4.html | regulation |
| S3 | California H&SC § 1280.3 — Administrative Penalties (Justia 2024) | https://law.justia.com/codes/california/code-hsc/division-2/chapter-2/article-3/section-1280-3/ | regulation |
| S4 | CDPH AFL-23-27 (Enforcement Guidance, Sep 2023) | https://www.cdph.ca.gov/Programs/CHCQ/LCP/Pages/AFL-23-27.aspx | official_doc |
| S5 | California SB 596 (Nurse Staffing Ratio Penalties, signed Oct 13 2025) | https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260SB596 | regulation |
| S6 | Oregon HB 2697 Enrolled Text (2023 Regular Session) | https://olis.oregonlegislature.gov/liz/2023R1/Downloads/MeasureDocument/HB2697/Enrolled | regulation |
| S7 | Massachusetts MGL c.111 § 231 / 958 CMR 8.00 (HPC page) | https://masshpc.gov/regulations-guidance/icu-nurse-staffing | regulation |
| S8 | PMC — Increased Utilization of Overtime and Agency Nurses and Patient Safety (2024, 70 hospitals) | https://pmc.ncbi.nlm.nih.gov/articles/PMC11966309/ | dataset |
| S9 | NNU — What California Ratios Law Requires | https://www.nationalnursesunited.org/ratios-what-does-california-ratios-law-require | official_doc |
| S10 | Joint Commission NPG 12 — Health Professional Resource Management (eff. Jan 1 2026) | https://aihc-assn.org/nurse-staffing-as-national-performance-goal-12/ | official_doc |
| S11 | CDPH Health Facilities State Enforcement Actions Dataset (CHHS Open Data) | https://data.chhs.ca.gov/dataset/healthcare-facility-state-enforcement-actions | dataset |

---

## Ground-Truth 锚点表

| 锚点名 | 值 | 来源 URL | 备注 |
|--------|----|----------|------|
| A1: ICU 护患比 | 1:2（≤2 patients/nurse）| S1 § 70217(a)(1) | "Critical Care" 含 ICU、burn center、coronary care、acute respiratory、NICU |
| A2: Med/Surg 护患比 | 1:5（effective 2005-01-01）| S1 § 70217(a)(11) | 2004年初始为1:6，2005起收紧 |
| A3: 步降病房（Step-Down）护患比 | 1:3（effective 2008-01-01）| S1 § 70217(a)(9) | Step-down: 中度-重度生理不稳定、需技术支持但非人工生命支持 |
| A4: 遥测（Telemetry）护患比 | 1:4（effective 2008-01-01）| S1 § 70217(a)(10) | 持续心脏监测、稳定状态患者 |
| A5: 急诊科（ED）护患比 | 1:4；重创 1:1（RN only）| S1 § 70217(a)(8) | ED 重创患者仅限注册护士 |
| A6: 精神科（Psychiatric）护患比 | 1:6 | S1 § 70217(a)(13) | 精神专科技术员在精神科可替代 LVN |
| A7: 首次违规罚款 | $15,000 | S3 § 1280.3; CDPH AFL-23-27 (S4) | SB 227（2019年签署）建立此罚款机制 |
| A8: 再次违规罚款 | $30,000/次 | S3 § 1280.3 | 3年内再次违规 = subsequent violation |
| A9: SB 596 关键变化 | 2026-01-01起每日计算为独立违规 | S5; signed 2025-10-13 | 此前同次检查多项违规计为1次 |
| A10: 豁免三要件 | (1)涨动不可预测+不可控；(2)立即采取措施；(3)已穷尽在职 on-call 名单 | S4 AFL-23-27 | 季节性流感高峰等「可预期」情形不自动豁免 |
| A11: Charge Nurse 计入规则 | 仅当从事直接患者护理时计入护患比 | S1 § 70217 interpretive language | 行政督导期间不计入分母 |
| A12: Oregon ICU 比率 | 1:2（HB 2697, eff. 2024-06-01）| S6 | Oregon 第二州强制比率法，ICU与CA相同 |
| A13: Oregon Med/Surg 比率阶段 | 1:5（2024-06-01）→ 1:4（2026-06-01）| S6 | CA仍停留1:5，OR将超越CA |
| A14: Oregon 执法违规罚款上限 | $5,000（重复违规）| S6 / wsna.org (S6衍生) | 远低于CA $15,000/$30,000 |
| A15: 机构护士 agency 超阈值 | 140%超过安全阈值（0.09 HPPD 断点）| S8 PMC11966309 | 跨70家医院2019-2022研究 |
| A16: Massachusetts ICU 比率法 | 1:1或1:2（依病情稳定性 acuity tool）| S7 MGL c.111 § 231; 958 CMR 8.00 | 2015-07-03生效；禁止1:3 |
| A17: Joint Commission NPG 12 | 2026-01-01生效，护士长须指导 staffing plan，24h RN 覆盖 | S10 NPG.12.02.01 | 首次将护患配置纳入认证硬性要求 |
| A18: 记录保存要求 | 逐日逐班次保存实际护士-患者分配记录，至少 1 年 | S1 § 70217(d) | CDPH 抽查时须立即提供 |

---

## Workspace 文件树与体量规划（目标 >100k tokens）

```
workspace/
├── regulations/
│   ├── CA_Title22_§70217_full.txt          # 法规全文逐条翻译+原文，~15k tokens
│   ├── CA_HSC_§1276.4_annotated.txt        # 含修订历史注释，~8k tokens
│   ├── CA_HSC_§1280.3_penalties.txt        # 罚款条款全文，~5k tokens
│   ├── CA_AFL-23-27_enforcement.txt        # CDPH All Facilities Letter，~6k tokens
│   ├── CA_SB596_2025_daily_penalty.txt     # SB 596 立法摘要+条文，~4k tokens
│   ├── OR_HB2697_enrolled.txt              # 俄勒冈 HB 2697 全文，~20k tokens
│   └── MA_ICU_958CMR8.00.txt              # 马萨诸塞 ICU 法规，~8k tokens
├── hospital_data/
│   ├── SVMC_unit_census_oct2024.csv        # 各科室10月日均患者数（合成），~8k tokens
│   ├── SVMC_nurse_roster.csv              # 护士名册（姓名/执照/科室/FTE），~10k tokens
│   ├── SVMC_staffing_log_oct2024.csv      # 已有排班日志（含违规班次），~15k tokens
│   ├── SVMC_on_call_list_current.csv      # 在职 on-call 名单（含 float pool），~5k tokens
│   ├── SVMC_FMLA_leave_schedule.csv       # FMLA/CFRA 请假计划，~3k tokens
│   └── SVMC_travel_nurse_contracts.csv    # 临时/差旅护士合同摘要，~5k tokens
├── communications/
│   ├── slack_cno_dm_history.json          # CNO Miranda Chen 与各部门主管 Slack DM，~12k tokens
│   ├── email_nurse_union_oct2024.mbox     # 护士工会往来邮件（含投诉），~10k tokens
│   ├── feishu_compliance_group.json       # 飞书合规顾问群聊记录（含失真摘要），~8k tokens
│   └── cdph_inspection_letter.txt        # CDPH 检查来函（含 2567 表格引用），~6k tokens
├── reports/
│   ├── SVMC_staffing_deficiency_report_draft.txt  # 当前缺陷报告草稿，~8k tokens
│   └── SVMC_corrective_action_plan_draft.txt      # 纠正措施计划草稿，~6k tokens
└── scripts/
    ├── validate_ratios.py                 # 验证排班方案是否合规，~3k tokens
    └── generate_cdph_log.py               # 生成 CDPH 格式 staffing log，~3k tokens
```

**估算总量：** ~148k tokens（充裕超过 100k 门槛）

---

## Sessions 清单（4-6 个）

| Session | 渠道 | 参与方 | 内容摘要 |
|---------|------|--------|----------|
| S-Main | Claude Code 主对话 | CNO Miranda Chen ↔ Agent | 18 轮主任务，包含所有 exec_check 题 |
| S-Slack | Slack DM + 频道消息 | CNO ↔ ICU 护士长、Med/Surg 护士长 | 关于违规班次的追责讨论，含矛盾说法（ICU 护士长声称排班合规） |
| S-Email | Union Email Thread | 护士工会代表 ↔ CNO ↔ 院方 HR | 工会主张违规从 2023 年 10 月起持续，院方否认；附件含旧版 on-call 名单 |
| S-Feishu | 飞书群「合规应急」 | 合规顾问（3人）+ CNO | 合规顾问 Bot 自动摘要（失真：将 $15,000 写成 $10,000，误称季节性流感可豁免）|
| S-CDPH | 官方往来（Email/Letter） | CDPH 检查员 ↔ 医院 | 正式检查通知、Statement of Deficiencies、整改期限（30 天）|

---

## 15-18 轮 exec_check 概要

### Q1（轮次 1）基线科室护患比合规检查
- **意图：** 提取各科室当前法定最低护患比并写入 JSON 文件
- **产物：** `workspace/output/ratios_baseline.json`（字段：unit, legal_ratio_max_patients, regulation_ref, effective_date）
- **check 锚点：** ICU=2, MedSurg=5, StepDown=3, Telemetry=4, ED=4, Psych=6；regulation_ref 须含 "§ 70217"；ICU effective_date = "2004-01-01"，StepDown/Telemetry effective_date = "2008-01-01"
- **难度向量：** V8（schema-by-shape 精确值校验），V9（verbatim 引用 § 70217 条款号）
- **偏好/update：** 无

### Q2（轮次 2）Charge Nurse 不计入直接护理比核实
- **意图：** 识别 staffing_log 中误将 charge nurse 纳入比率计算的班次，输出违规班次列表
- **产物：** `workspace/output/charge_nurse_violations.csv`（shift_id, unit, date, actual_ratio_excluding_charge, legal_max）
- **check 锚点：** 须正确识别至少 3 个 charge nurse 被错误计入的班次；剔除后该班次比率超过法定上限
- **难度向量：** V1（staffing log 与 roster 信息冲突需综合），V4（前后轮数值闭合）
- **偏好/update：** 无

### Q3（轮次 3）首次违规 vs 再次违规罚款分类
- **意图：** 根据 CDPH AFL-23-27 规则，对检查发现的违规班次分类并计算应缴罚款总额
- **产物：** `workspace/output/penalty_assessment.json`（violation_count_first, violation_count_subsequent, total_penalty_usd）
- **check 锚点：** first_violation_fee = 15000；subsequent_violation_fee = 30000；3 年内重复计为 subsequent；total 须精确（允许 ±0）
- **难度向量：** V5（飞书摘要将 $15,000 写为 $10,000 作为失真诱饵），V8（精确数值），V9（引用 AFL-23-27）
- **偏好：** P1（金额用整数，不带小数点）

### Q4（轮次 4）SB 596 日罚款影响预测
- **意图：** 若 SB 596 已生效（2026-01-01 起），重新计算同一违规周期的罚款总额（每日计为独立违规）
- **产物：** `workspace/output/sb596_penalty_projection.json`（pre_sb596_total, post_sb596_total, diff, effective_date）
- **check 锚点：** effective_date = "2026-01-01"；post_sb596_total > pre_sb596_total；diff 精确
- **难度向量：** V2（时间线 update 改变计算逻辑），V4（与 Q3 数值闭合）
- **偏好：** P1

### Q5（轮次 5）豁免三要件评估报告
- **意图：** 对每个违规班次，依 AFL-23-27 三要件检验是否具备豁免资格，写 Markdown 报告
- **产物：** `workspace/output/exemption_analysis.md`（每班次一节：班次ID/日期/满足/不满足的要件/结论）
- **check 锚点：** 须正确识别"季节性流感不自动豁免"；at least 2 班次因未能穷尽 on-call 名单而不获豁免；第 3 要件引用"immediately used and subsequently exhausted the hospital's on-call list"
- **难度向量：** V5（飞书摘要错误声称流感可豁免），V6（旧版 on-call 名单是红鲱鱼，应使用 current 版本），V9（verbatim 引用三要件语言）
- **偏好：** P2（Markdown 报告每节含三级标题格式）

### Q6（轮次 6）两周排班方案生成（ICU + Step-Down）
- **意图：** 为 ICU（8 名在编+2 名差旅护士）和 Step-Down（12 名在编）生成两周 12-8h 班次排班表，满足 § 70217 要求
- **产物：** `workspace/output/schedule_icu_stepdown.csv`（date, shift, unit, nurse_id, patient_count, ratio_computed）
- **check 锚点：** ICU ratio_computed ≤ 2.0（全班次）；Step-Down ratio_computed ≤ 3.0；每班次 RN 覆盖 24h；charge nurse 时段须同时有其他 RN
- **难度向量：** V4（与后续轮次日志数值闭合），V8（ratio 字段精确到 1 位小数）
- **偏好：** P3（CSV 日期格式 YYYY-MM-DD；ratio 字段两位小数）

### Q7（轮次 7）Med/Surg 夜班超标分析与纠正计划
- **意图：** 分析过去 4 周 Med/Surg 夜班超标班次，输出含根因+纠正措施的结构化报告
- **产物：** `workspace/output/medsurg_night_analysis.json`（violation_shifts[], root_cause, corrective_measures[]）
- **check 锚点：** violation 班次数 ≥ 5（基于 staffing log）；root_cause 必须提及 FMLA/CFRA；corrective_measures 至少包含 float pool 扩充 + on-call 名单更新
- **难度向量：** V1（工会邮件声称违规已持续更长时间，Slack 护士长否认），V4（违规班次数须与 Q2 数据一致）
- **偏好：** P4（JSON 数组字段用蛇形命名 snake_case）

### Q8（轮次 8）CDPH 格式 Staffing Log CSV 生成
- **意图：** 按 Title 22 § 70217(d) 要求，为整改期第 1 周生成可提交 CDPH 的 staffing log
- **产物：** `workspace/output/cdph_staffing_log_week1.csv`（date, shift_start, shift_end, unit, nurse_id, license_type, patient_count, ratio）
- **check 锚点：** 所有班次 ratio ≤ 法定上限；license_type ∈ {RN, LVN, PT}；精神科若出现 PT，须验证科室为 Psychiatric；charge nurse 在行政任务班次中 patient_count = 0
- **难度向量：** V7（终轮 sha256 校验铺垫，此轮产出文件作为后续签名输入），V8（字段类型+范围校验），V9（字段名须与 CDPH 格式一致）
- **偏好：** P3（CSV 编码 UTF-8，字段顺序固定）

---

## **UPDATE 1（注入于 Q9 之前）** — CDPH 补充检查通知

**体量来源：** 补充注入新的 CDPH 来函（~35k tokens）：
- 新增 Statement of Deficiencies 详细表格（涵盖额外 12 个违规班次，主要在 Telemetry 科室）
- 追加 Telemetry 科室历史 census 数据（4 周，CSV）
- 更新后 Telemetry 违规日期落在 SB 596 生效（2026-01-01）之后，触发日罚款模式

**对后续轮次的影响：** Q9-Q12 须将 Telemetry 违规纳入计算，罚款总额大幅上升。

---

### Q9（轮次 9）Telemetry 违规纳入更新后罚款总额
- **意图：** 将 Update 1 新增 Telemetry 违规整合，重新计算罚款（含 SB 596 日罚款）
- **产物：** `workspace/output/penalty_assessment_v2.json`（all_violations[], total_pre_sb596, total_post_sb596, telemetry_daily_violations）
- **check 锚点：** telemetry_daily_violations 数值与 Update 1 注入 CSV 精确匹配；total_post_sb596 > Q4 结果（信念修正）
- **难度向量：** V2（update 反转罚款规模），V4（v2 与前轮数值闭合），V10（supersede 准备）

### Q10（轮次 10）On-Call 名单合规审查
- **意图：** 审查现有 on-call 名单是否符合 SB 596 对 on-call list 的新定义（仅限 scheduled on-call 或 float pool）
- **产物：** `workspace/output/oncall_audit.json`（compliant_nurses[], non_compliant_nurses[], gap_count, recommendation）
- **check 锚点：** non_compliant 须包含未在 schedule 内但被联系的护士名（从 roster 数据可查）；gap_count 精确；recommendation 须引用 SB 596 on-call 定义
- **难度向量：** V6（旧版 on-call 名单 v2023-10 是废弃副本，使用旧版导致错误），V9（引用 SB 596 定义语言）
- **偏好：** P4（JSON 蛇形命名），P5（recommendation 字段不超过 150 字）

---

## **UPDATE 2（注入于 Q11 之前）** — supersede 部分内容 — 工会和解协议

**体量来源：** 注入工会和解备忘录 + 修订排班协议 + 附加历史邮件线程（~40k tokens）：
- 工会与医院签署的和解协议，**撤销** Update 1 中 4 个 Telemetry 违规班次（工会确认这些班次护士实际在岗，时间戳记录错误）
- 新增 2 个此前未发现的 ICU 违规班次（深夜班次数据）
- 修订整改措施：要求 float pool 配置为 ≥ 3 名 ICU 资质护士（原 Update 1 版本无此要求）

**supersede 逻辑：** Update 2 部分撤销 Update 1 的 Telemetry 违规数（-4），同时新增 ICU 违规（+2）；agent 须辨别并非叠加而是修订。

---

### Q11（轮次 11）supersede 后违规台账终版

- **意图：** 依 Update 2 和解协议，最终确定所有违规班次台账（撤销 4 Telemetry + 新增 2 ICU）
- **产物：** `workspace/output/violation_ledger_final.json`（violations[], total_count, superseded_count, newly_added_count）
- **check 锚点：** superseded_count = 4；newly_added_count = 2；total_count = 原有数 − 4 + 2；violations[] 每项含 unit/date/shift/ratio_actual/legal_max
- **难度向量：** V10（supersede 辨别，不能叠加新增而是替换），V4（数值前后闭合）

### Q12（轮次 12）修订后总罚款重算
- **意图：** 以 Q11 最终台账重新计算罚款，区分 SB 596 生效前后的违规
- **产物：** `workspace/output/penalty_final.json`（pre_2026_total, post_2026_total, grand_total）
- **check 锚点：** grand_total 须与 Q11 violations[] 精确匹配（无多余或遗漏）；post_2026_total 按日计算
- **难度向量：** V2（信念修正，低于 Q9 的 total），V8（精确数值）

### Q13（轮次 13）Joint Commission NPG 12 合规差距分析
- **意图：** 对比 SVMC 现有 staffing plan 文档与 NPG 12 各 EP，输出差距矩阵
- **产物：** `workspace/output/npg12_gap_analysis.json`（ep_id, requirement, svmc_current_status, gap, action_required）
- **check 锚点：** EP NPG.12.02.01 须标记 nurse executive 24h RN 覆盖要求；NPG.12.06.01 须标记 QAPI 整合要求；effective_date = "2026-01-01"；至少 6 个 EP 条目
- **难度向量：** V9（EP 编号 verbatim 引用），V8（ep_id 字段精确匹配）

### Q14（轮次 14）Oregon 法规对比报告（含 Phase-in 时间线）
- **意图：** 比较加州（Title 22 § 70217）与俄勒冈（HB 2697）的护患比规则，重点标注 Med/Surg Phase-in 差异
- **产物：** `workspace/output/ca_vs_or_comparison.json`（unit, ca_ratio, or_ratio_2024, or_ratio_2026, or_stricter_by_2026）
- **check 锚点：** ICU 两州均 = 2；Med/Surg CA = 5，OR 2024 = 5，OR 2026 = 4；or_stricter_by_2026 = true（Med/Surg）；or_penalty_max = 5000 vs ca_first_violation = 15000
- **难度向量：** V1（多源规定冲突），V4（数值与 Q1 闭合），V9（HB 2697 条文号引用）

### Q15（轮次 15）整改期第二周 Staffing Log 生成

- **意图：** 生成整改期第 2 周全院 staffing log（含 float pool 扩充后的 ICU 配置），验证合规
- **产物：** `workspace/output/cdph_staffing_log_week2.csv`（同 Q8 schema）
- **check 锚点：** ICU float pool 护士数 ≥ 3（Update 2 要求）；全院所有 unit 无超标班次；CSV 行数与 census 数据一致
- **难度向量：** V4（float pool ≥ 3 源自 Update 2，须与 Q6 排班一致），V8（ratio 字段精确）
- **偏好：** P3（CSV 格式）

### Q16（轮次 16）CDPH 整改提交文档包 Manifest 生成

- **意图：** 生成完整整改文档包的 manifest JSON（列出所有待提交文件、描述、SHA-256 哈希）
- **产物：** `workspace/output/submission_manifest.json`（files[]: path, description, sha256, size_bytes）
- **check 锚点：** 须包含 Q8 产出的 week1 log、Q15 产出的 week2 log、violation_ledger_final.json、penalty_final.json；每个 sha256 须为实际文件内容的正确哈希
- **难度向量：** V7（agent 须运行 sha256sum/hashlib 得到真实哈希，不可伪造）

### Q17（轮次 17）终验：CDPH 提交包 SHA-256 签名校验

- **意图：** 运行校验脚本，对 submission_manifest.json 中每个文件重算 sha256，与 manifest 记录比对
- **产物：** `workspace/output/verification_report.txt`（格式：VERIFIED:<sha256_of_manifest> 或 FAILED:<file>:<reason>）
- **check 锚点：** 输出第一行必须为 `VERIFIED:<sha256>`；sha256 须与实际文件内容一致（脚本本地重算比对）
- **难度向量：** V7（必须实际运行 Bash/Python 才能得到哈希，伪造无效）

---

## Update 设计汇总

| Update | 注入时机 | 内容摘要 | 体量来源 | supersede |
|--------|----------|----------|----------|-----------|
| U1 | Q8 后 | CDPH 补充检查通知 + Telemetry 违规数据（12 班次）+ SB 596 已生效情境 | 新增 CDPH 来函文档 + Telemetry census CSV，共 ~35k tokens | 否 |
| U2 | Q10 后 | 工会和解协议：撤销 4 Telemetry 违规 + 新增 2 ICU 违规 + float pool ≥ 3 要求 | 和解备忘录 + 修订邮件线程 + 历史排班附件，共 ~40k tokens | 是（撤销 U1 中 4 个违规） |

---

## 4-5 条 Preference 规则

| 编号 | 规则 | 注入方式 | 考察轮次 |
|------|------|----------|----------|
| P1 | 所有货币金额以整数美元表示，不带小数点、不带千位符（例：15000，不是 $15,000.00）| Q3 显式说明 | Q4、Q9、Q12 静默考察 |
| P2 | Markdown 报告每个案例/班次用三级标题（`###`）开头，不使用二级标题 | Q5 用户 feedback 纠正 | Q7、Q13 静默考察 |
| P3 | CSV 文件：UTF-8 编码，日期字段格式 YYYY-MM-DD，ratio 字段保留两位小数 | Q6 显式说明 | Q8、Q15 静默考察 |
| P4 | JSON 文件所有字段名使用 snake_case，数组字段以复数命名（violations, files） | Q7 显式说明 | Q10、Q11、Q12、Q16 静默考察 |
| P5 | 所有 recommendation/action 字段纯文本，不嵌套子 JSON，长度不超过 150 字 | Q10 用户 feedback 纠正 | Q13、Q16 静默考察 |

---

## 拆分/删除建议

素材充裕，可考虑拆分为两个子场景：
- **sci3a**：聚焦加州法规合规 + 排班生成 + CDPH 整改文档（Q1-Q8 + Q15-Q17），减少跨州比较
- **sci3b**：聚焦多州护患比政策分析 + 罚款机制演变（含 SB 596）+ 联合委员会 NPG 12（Q3-Q4 + Q9-Q14）

当前方案可作为单一完整场景（17 轮），素材体量与复杂度均充分。

---

## 可行性评估

**Viability：strong**
- 6 个以上真实可查 URL，18 个精确锚点均有明确法规/论文出处
- 合成文件树估算 ~148k tokens，每次 update 体量 35k/40k，满足 >30k 要求
- 所有数值锚点可回溯至具体法规条款号（§ 70217 subsection + H&SC 条文）
