# BRIEF: sci2 — 医疗器械安全事件根本原因分析（RCA）

## 场景叙事背景

某医疗器械安全合规团队（MedSafe RCA Team）正就三起真实 FDA Class I / Class II 器械召回事件开展根本原因分析（Root Cause Analysis, RCA）。Agent 扮演资深质量工程师，在多 session 环境中：
- 从 FDA MAUDE 数据库、Recall 数据库、Field Safety Notice 中提取真实锚点数据；
- 撰写结构化 RCA 报告（含 fishbone 分析、5-Why、CAPA 条目）；
- 维护跨 session 的数值一致性（流速偏差、受影响单位数、召回等级）；
- 应对动态注入的修订通知（update supersede 机制），辨别旧版内容并以最新版为准；
- 全程遵守团队工作偏好规范。

核心真实素材围绕以下三起 FDA 真实召回：

**召回 A（主线）：InfuTronix Nimbus / Nimbus II 系列输液泵**
- 事件：2024 年 Class I 召回（FDA 公告日期 2024-04-25）
- 原因：多模式失效（电池故障、上游堵塞、系统错误、药液泄漏、流速偏高/低、外壳损坏）
- 规模：52,328 台输液泵，分发时间段 2015-02-27 至 2024-02-29
- 不良事件：3,698 份投诉、6 例严重伤害、1 例死亡
- Nimbus 主泵 UDI：00817170020000
- 后果：设备于 2024-06-20 停止支持，厂商需完整重新设计并重新申请 510(k)

**召回 B（辅线 / 对比参照）：Fresenius Kabi Ivenix LVP 软件**
- 事件：2025-2026 年 Class I 召回（Z-0885-2026，enforcement 日期 2025-12-16）
- 原因：软件版本 5.10.1 及更早版本存在双重异常：
  (1) 电池剩余电量显示错误 → 意外关机；
  (2) 输入以双零开头的速率（如 0010）后按 Back/OK → 界面冻结于 fail-stop 报警态
- 受影响软件产品码：LVP-SW-0005；分发州：CA, CO, FL, GA, ID, IL, MD, MI, MN, MS, NE, NJ, NV, OK, OR, SC, TX, VA, WA, WI（共 30 台 software update kits）
- 不良事件：2 例严重伤害，0 例死亡
- 纠正措施：更新 IMS 至 v5.2.2，更新 LVP 软件至 v5.10.2；电池健康低于 70% 须更换

**召回 C（红鲱鱼 / 参考基线）：Medtronic SynchroMed II 植入式输液泵**
- 事件：2019 年 Class I 召回（December 2019，FDA 分级）
- 原因：制造过程中异物颗粒导致齿轮卡顿 → 电机失速 → 无法输药
- 受影响型号：8637-20 和 8637-40（约 11,299 台）
- 不良事件：5 例电机失速报告（制造至 2019-04 的最后一批），无死亡
- 注意：此事件为旧案（2019），作为场景中"废弃副本"红鲱鱼使用（V6）

---

## 真实来源链接表

| # | 来源名称 | URL | 类型 |
|---|----------|-----|------|
| S1 | InfuTronix Nimbus 召回 - FDA 官方页面 | https://www.fda.gov/medical-devices/medical-device-recalls/infutronix-llc-recalls-nimbus-and-nimbus-ii-infusion-pump-systems-multiple-device-failures-may-cause | official_doc |
| S2 | Nimbus 召回 - MedTech Dive 深度报道 | https://www.medtechdive.com/news/infutronix-nimbus-infusion-pump-recall-injuries-death/714391/ | news |
| S3 | Nimbus 召回 - HPN Online 含 52,328 台数据 | https://www.hpnonline.com/surgical-critical-care/news/55036575/infutronix-recalls-52328-infusion-pump-systems-due-to-multiple-potential-failure-modes | news |
| S4 | Nimbus 召回 - Drug Delivery Business（含 1 例死亡） | https://www.drugdeliverybusiness.com/fda-infutronix-infusion-pump-recall-1-death/ | news |
| S5 | Ivenix LVP 软件召回 - SoftwareCPR（Z-0885-2026 确认） | https://www.softwarecpr.com/2025/12/fda-recall-software-anomalies-can-cause-serious-harm-or-death/ | postmortem |
| S6 | Ivenix 软件召回 - AABB 监管更新 | https://www.aabb.org/news-resources/news/article/2026/03/04/regulatory-update--class-i-recall-issued-for-fresenius-kabi-ivenix-large-volume-pump-software | regulation |
| S7 | Ivenix 软件召回 - Manufacturing Chemist（技术细节） | https://manufacturingchemist.com/fda-class-i-recall-fresenius-kabi-ivenix-infusion | news |
| S8 | MAUDE 数据库入口 | https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/search.cfm | dataset |
| S9 | FDA MAUDE Avanos AMBIT 泵不良事件（流速异常案例） | https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=20464324&pc=MEA | dataset |
| S10 | PMC 输液泵 Class I 召回失效模式分析（70 例统计） | https://pmc.ncbi.nlm.nih.gov/articles/PMC6524450/ | dataset |
| S11 | 21 CFR Part 803 MDR 报告要求 - eCFR | https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-803 | regulation |
| S12 | Medtronic SynchroMed II 2019 Class I 召回 - MedTech Dive | https://www.medtechdive.com/news/fda-grades-new-medtronic-synchromed-ii-recall-as-class-i-event/568509/ | news |

---

## Ground-Truth 锚点表

| 锚点名 | 值 | 来源 URL | 备注 |
|--------|-----|----------|------|
| nimbus_units_recalled | 52,328 | S3 | 美国境内受影响输液泵总台数 |
| nimbus_complaints | 3,698 | S1/S2/S4 | 投诉总数（截至 2024-04-25）|
| nimbus_serious_injuries | 6 | S2/S4 | 严重伤害报告数 |
| nimbus_deaths | 1 | S4 | 死亡报告数 |
| nimbus_distribution_end | 2024-02-29 | S2 | 最后分发日期 |
| nimbus_distribution_start | 2015-02-27 | S2 | 首次分发日期 |
| nimbus_support_cutoff | 2024-06-20 | S2/S4 | 设备支持截止日 |
| nimbus_udi_main | 00817170020000 | S3（HPN 含 UDI 字段） | Nimbus 主泵 UDI |
| nimbus_recall_class | Class I | S1 | FDA 召回等级 |
| ivenix_recall_number | Z-0885-2026 | S5 | FDA 执行报告号 |
| ivenix_software_affected | 5.10.1 及更早 | S6/S7 | 受影响软件版本 |
| ivenix_software_fixed | 5.10.2 | S6/S7 | 修复目标版本 |
| ivenix_ims_fixed | 5.2.2 | S6 | IMS 更新目标版本 |
| ivenix_product_code | LVP-SW-0005 | S5/S7 | FDA 产品码 |
| ivenix_injuries | 2 | S7 | 严重伤害数（2025-11-18 为止）|
| ivenix_battery_threshold | 70% | S6 | 需更换电池的健康度下限 |
| ivenix_anomaly_1 | 电池剩余电量显示错误导致意外关机 | S7 | 第一技术异常描述 |
| ivenix_anomaly_2 | 双零开头速率输入后界面冻结 | S7 | 第二技术异常描述 |
| mdr_30day_requirement | 21 CFR 803，30 calendar days | S11 | 制造商 MDR 报告时限 |
| mdr_5day_requirement | 21 CFR 803，5 work days | S11 | 紧急 MDR 报告时限 |
| pump_failure_energy_pct | 67% (47/70) | S10 | 能量危害类失效占比（PMC 研究） |
| pump_failure_underdose_pct | 55% (36/66) | S10 | 低剂量伤害事件占比 |
| synchromed_model_affected | 8637-20, 8637-40 | S12 | SynchroMed II 受影响型号（旧案/红鲱鱼）|
| synchromed_units | 11,299 | S12 | SynchroMed II 受影响台数（旧案）|
| 806_report_deadline | 10 working days | S11/21 CFR 806 | 21 CFR 806 纠正/移除报告提交时限 |

---

## Workspace 文件树与体量规划（>100k tokens）

```
workspace/
├── cases/
│   ├── case_A_nimbus/
│   │   ├── recall_notice_official.md         # 5,000 tokens：FDA 召回公告全文（含失效模式、UDI、分发信息）
│   │   ├── complaint_log_2019_2023.csv        # 25,000 tokens：虚构但围绕真实锚点的 3,698 条投诉条目
│   │   │                                      # 字段：date,model,lot,failure_mode,outcome,mdr_submitted
│   │   ├── maude_reports_sample.jsonl         # 15,000 tokens：基于真实 MAUDE MDR 格式的 50 条样本报告
│   │   ├── field_safety_notice_v1.md          # 3,000 tokens：初始 FSN（含 V2 反转内容，后被 update 修订）
│   │   ├── rca_draft_fishbone.md              # 4,000 tokens：待完善的鱼骨图草稿（含蓄意失真的 bot 摘要诱饵）
│   │   └── engineering_test_data.csv          # 8,000 tokens：模拟电池测试、流速偏差测试数据（含容差阈值）
│   ├── case_B_ivenix/
│   │   ├── software_recall_Z0885.md           # 3,000 tokens：Ivenix Z-0885-2026 召回技术通报
│   │   ├── anomaly_investigation.md           # 4,000 tokens：两个软件异常的根因分析草稿
│   │   ├── software_changelog.md              # 3,000 tokens：v5.10.1 → v5.10.2 变更日志
│   │   └── hospital_impact_report.md          # 3,000 tokens：受影响医院清单及风险评估
│   └── case_C_synchromed_legacy/
│       ├── ARCHIVED_recall_2019.md            # 2,000 tokens：2019 年 SynchroMed II 召回存档（红鲱鱼）
│       └── NOTE_superseded.md                 # 500 tokens：明确标注已废弃的说明文件
├── regulations/
│   ├── 21cfr_803_mdr_requirements.md          # 5,000 tokens：21 CFR Part 803 关键条款摘录（含 5-day/30-day）
│   ├── 21cfr_806_recall_report.md             # 4,000 tokens：21 CFR Part 806 纠正/移除报告要求
│   ├── ifu_infusion_pump_lifecycle_fda.md     # 6,000 tokens：FDA 输液泵全生命周期监管指南摘要
│   └── iec60601_accuracy_requirements.md      # 3,000 tokens：IEC 60601-2-24 流速精度要求概述
├── templates/
│   ├── rca_report_template.md                 # 4,000 tokens：标准 RCA 报告模板（含 CAPA 字段）
│   ├── maude_mdr_form_3500a.md                # 3,000 tokens：MedWatch Form 3500A 字段说明
│   ├── capa_tracking_template.xlsx.md         # 3,000 tokens：CAPA 追踪表格（Markdown 表格格式）
│   └── fda_806_report_template.md             # 2,500 tokens：21 CFR 806 报告模板
├── sessions/
│   ├── slack_channel_safety_team.jsonl        # 8,000 tokens：Slack #safety-alerts 频道记录
│   │                                          # 含真实讨论：Nimbus 投诉数、召回等级判定、MDR 截止日
│   ├── feishu_group_rca_wip.jsonl             # 6,000 tokens：飞书群组「RCA 工作进展」聊天记录
│   │                                          # 含 V1 信息冲突：一条消息误引 3,800 条投诉（失真）
│   ├── email_thread_regulatory.eml            # 5,000 tokens：与 FDA 对接的邮件线程（含 Z-0885-2026 引用）
│   ├── discord_dm_engineer.jsonl              # 4,000 tokens：工程师 DM 记录（含技术参数讨论）
│   └── bot_summary_HONEYPOT.md                # 2,000 tokens：自动 bot 摘要（V5：蓄意错误 — 将 Ivenix 伤害数写为 5，
│                                              # 将 Nimbus 支持截止日写为 2024-08-31，均有明面反证）
├── rca_outputs/
│   ├── .gitkeep                               # Agent 将在此目录产出最终 RCA 文件
│   └── README.md                              # 产出规范说明（含格式要求）
└── scripts/
    └── verify_recall_data.py                  # SHA-256 校验脚本（V7 终轮使用）
```

**体量估算总计：约 130,000 tokens**（各文件含合理的真实背景素材填充）

---

## Session 清单（4-6 个 Session）

| Session ID | 渠道 | 参与者 | 核心内容 | 注入时间 |
|------------|------|--------|----------|----------|
| sess-01 | Slack (#safety-alerts) | Safety Team 群组 | Nimbus 召回初始通报，含投诉数讨论（V1 冲突：3698 vs 3800）| 初始 workspace |
| sess-02 | Feishu 群组（RCA 工作进展）| RCA 团队 | 分配任务、case_A/B 并行分析、技术参数讨论 | 初始 workspace |
| sess-03 | Email（工程师 → 监管专员）| Engineer + Regulatory | 引用 Z-0885-2026，讨论 Ivenix 软件版本，初期版本号 5.10.0（Update 1 后修正为 5.10.1）| 初始 workspace |
| sess-04 | Discord DM（资深工程师）| Lead Engineer | 详细技术分析，电池阈值、MDR 法规引用 | 初始 workspace |
| sess-05 | Feishu 群组（更新注入）| 团队负责人 | Update 1：发布修订 FSN，修正 Ivenix 受影响软件版本描述 | Update 1 注入 |
| sess-06 | Email（监管跟进）| Regulatory + FDA | Update 2：撤销 Update 1 的部分错误更正，并补充 Nimbus 新分发日期范围 | Update 2 注入 |

---

## 15-18 轮 exec_check 概要

### 轮次 Q01
**意图：** 提取并结构化 Nimbus 召回核心元数据  
**产物：** `rca_outputs/nimbus_recall_metadata.json`  
**字段：** `{"manufacturer","recall_class","units_recalled","complaints","serious_injuries","deaths","distribution_start","distribution_end","support_cutoff","udi_main"}`  
**check 锚点：** units_recalled=52328, complaints=3698, deaths=1, udi_main="00817170020000"  
**难度向量：** V8（schema-by-shape 精确值校验）  
**涉及：** 初始 workspace，sess-01/sess-02

### 轮次 Q02
**意图：** 识别 bot 摘要（HONEYPOT）中的失真内容并标记  
**产物：** `rca_outputs/honeypot_flags.json`  
**字段：** `{"flagged_errors": [{"field","honeypot_value","correct_value","evidence_source"}]}`  
**check 锚点：** 必须标记 ivenix_injuries(5→2) 和 nimbus_cutoff("2024-08-31"→"2024-06-20")  
**难度向量：** V5（失真摘要诱饵）  
**涉及：** bot_summary_HONEYPOT.md vs S4/S7

### 轮次 Q03
**意图：** 撰写 Nimbus 召回 5-Why 分析  
**产物：** `rca_outputs/nimbus_5why.md`  
**格式要求：** 标准 Markdown 五层表格，最终根因必须点名电池设计缺陷与无菌屏障失效  
**check 锚点：** 文件存在 + 包含"battery"+"sterile barrier"+"occlusion"关键词 + 字数 ≥ 400  
**难度向量：** V3（preference：5-Why 必须用表格格式，非 prose）  
**涉及：** preference P1

### 轮次 Q04
**意图：** 映射监管报告义务（MDR 与 806 要求）  
**产物：** `rca_outputs/regulatory_obligations.json`  
**字段：** `{"mdr_30day_cfr","mdr_5day_cfr","recall_report_cfr","recall_report_deadline_days"}`  
**check 锚点：** mdr_30day_cfr="21 CFR 803.50(a)(1)", recall_report_deadline_days=10  
**难度向量：** V9（真实来源条款号 verbatim 引用）  
**涉及：** regulations/ 文件夹

### 轮次 Q05
**意图：** 生成 Nimbus 案例鱼骨图（Ishikawa）结构化输出  
**产物：** `rca_outputs/nimbus_fishbone.json`  
**字段：** `{"categories":{"Man","Machine","Material","Method","Environment","Measurement"}, "root_causes":[]}`  
**check 锚点：** Machine 类别须含"battery_failure"和"occlusion_sensor"；Material 类别须含"sterile_barrier"  
**难度向量：** V8（schema-by-shape）、V3（preference P2：JSON 鱼骨图必须用六 M 分类）  
**涉及：** preference P2

### 轮次 Q06
**意图：** 汇总投诉数据统计，输出失效模式频次表  
**产物：** `rca_outputs/failure_mode_stats.csv`  
**字段：** `failure_mode,count,pct_of_total`（pct 保留 2 位小数）  
**check 锚点：** 总 count=3698，battery_failure 行 pct 在合理范围内（由 complaint_log 推算）  
**难度向量：** V4（跨轮数值闭合：Q06 的 total count 必须与 Q01 的 complaints 字段一致）  
**涉及：** cases/case_A_nimbus/complaint_log_2019_2023.csv

### 轮次 Q07（Update 1 注入前最后一轮）
**意图：** 基于初始 FSN v1 撰写 Ivenix 软件召回技术摘要  
**产物：** `rca_outputs/ivenix_tech_summary_v1.md`  
**check 锚点：** 记录 affected_version="5.10.0"（初始 session 03 email 中的版本号，Update 1 前的状态）  
**难度向量：** V2 预布（为 update 后反转做铺垫）  
**涉及：** sess-03 email

---

**[UPDATE 1 注入]** — 新增文件 `sessions/feishu_update1_fsn_revision.jsonl`（~35k tokens）  
内容：修订 FSN，将 Ivenix 受影响软件版本从 "5.10.0" 修正为 "5.10.1 及更早版本"；同时明确 LVP-SW-0005 产品码；补充 Z-0885-2026 召回号确认。

---

### 轮次 Q08（Update 1 注入后）
**意图：** 基于修订 FSN 更新 Ivenix 召回元数据  
**产物：** `rca_outputs/ivenix_recall_metadata.json`  
**字段：** `{"recall_number","affected_software_version","product_code","fixed_version","ims_fixed_version","injuries","battery_threshold_pct","anomaly_1","anomaly_2"}`  
**check 锚点：** affected_software_version 须含"5.10.1"（不得为"5.10.0"）；recall_number="Z-0885-2026"；battery_threshold_pct=70  
**难度向量：** V2（动态 update 反转：必须采纳新版本号，不能保留旧版）、V9（Z-0885-2026 verbatim）  
**涉及：** Update 1

### 轮次 Q09
**意图：** 对比 Nimbus（硬件失效）与 Ivenix（软件异常）两类根因的 CAPA 差异  
**产物：** `rca_outputs/capa_comparison.json`  
**字段：** `{"case_A":{"root_cause_category","capa_actions":[]},"case_B":{"root_cause_category","capa_actions":[]}}`  
**check 锚点：** case_A.root_cause_category="hardware_design"; case_B.root_cause_category="software_anomaly"  
**难度向量：** V4（case_B 的 CAPA 行动必须包含更新至 v5.10.2 的 verbatim 描述）  
**涉及：** 跨 case 数值闭合

### 轮次 Q10
**意图：** 检查 case_C legacy 文件夹，识别 SynchroMed II 2019 召回为废弃旧案  
**产物：** `rca_outputs/case_C_assessment.json`  
**字段：** `{"status","reason","should_include_in_current_rca","affected_models","units"}`  
**check 锚点：** status="ARCHIVED_LEGACY"; should_include_in_current_rca=false  
**难度向量：** V6（废弃副本红鲱鱼：旧案不得引入当前 RCA 作为有效依据）  
**涉及：** case_C_synchromed_legacy/

### 轮次 Q11
**意图：** 撰写 Nimbus 召回 MAUDE MDR 报告摘要（模拟厂商视角）  
**产物：** `rca_outputs/nimbus_mdr_summary.md`  
**格式：** 按 Form 3500A 字段结构填写（包含 Section A-G）  
**check 锚点：** 文件含"3500A"+"B3"(事件严重程度)+"30 calendar days"；字数 ≥ 600  
**难度向量：** V9（Form 3500A 字段名 verbatim）、V3（preference P3：MDR 文档必须按 FDA 标准 Section 编号）  
**涉及：** preference P3, templates/

---

**[UPDATE 2 注入]** — 新增文件 `sessions/email_update2_supersede.eml`（~32k tokens）  
内容：  
(1) **Supersede Update 1 部分内容**：声明 Update 1 中"30 units software kits"的描述有误，实际该数字指硬件 LVP 单元，不可用于推断软件安装量，相关字段应删除或标注为"undisclosed"；  
(2) **新增 Nimbus 信息**：补充 Nimbus 分发时间段起始日期应为 2015-02-27（之前一些 session 中错误引用的 2014 年数据不可信）；  
(3) 补充 21 CFR 806 的 10-working-day 报告窗口明确说明。

---

### 轮次 Q12（Update 2 注入后）
**意图：** 处理 supersede 修订，更新 Ivenix 元数据中受影响字段  
**产物：** `rca_outputs/ivenix_recall_metadata_v2.json`（覆盖 Q08 版本）  
**check 锚点：** units_software_kits 字段值为"undisclosed"（不能保留 "30"）  
**难度向量：** V10（supersede 辨别：必须识别 Update 2 撤销了 Update 1 的 "30 units" 字段）  
**涉及：** Update 2 supersede

### 轮次 Q13
**意图：** 验证 Nimbus 分发起始日期，解决多 session 信息冲突  
**产物：** `rca_outputs/distribution_timeline.json`  
**字段：** `{"manufacturer","distribution_start","distribution_end","support_cutoff","evidence_source","conflicts_resolved":[{"session","claimed_value","resolution"}]}`  
**check 锚点：** distribution_start="2015-02-27"（不得为 2014 年的任何日期）  
**难度向量：** V1（多源冲突综合：session 中有 2014 年错误引用，须以 Update 2 修正版为准）  
**涉及：** sess-01 冲突 vs Update 2 正确值

### 轮次 Q14
**意图：** 生成统一的 RCA 执行摘要（Executive Summary）  
**产物：** `rca_outputs/executive_summary.md`  
**check 锚点：** 文件须含以下精确字符串或其等价：  
- "52,328" 或 "52328"（Nimbus 台数）  
- "3,698" 或 "3698"（Nimbus 投诉数）  
- "Z-0885-2026"（Ivenix 召回号）  
- "2015-02-27"（Nimbus 分发起始）  
- "2024-06-20"（Nimbus 支持截止）  
**难度向量：** V4（跨轮数值闭合，所有关键数字与 Q01/Q08/Q13 一致）、V3（preference P4：Executive Summary 须含结构化摘要块，格式 YAML frontmatter）  
**涉及：** preference P4

### 轮次 Q15
**意图：** 静默考察 preference P5：输出文件命名规范  
**产物：** `rca_outputs/final_rca_report_YYYYMMDD.md`（日期替换为实际日期）  
**check 锚点：** 文件名匹配正则 `final_rca_report_\d{8}\.md`；文件含"Class I"出现次数 ≥ 2  
**难度向量：** V3（preference P5 静默考察：命名规范从未在此轮明确重申）  
**涉及：** preference P5

### 轮次 Q16
**意图：** 运行数据验证脚本，生成 SHA-256 校验令牌  
**产物：** `rca_outputs/verification_token.txt`  
**格式：** `VERIFIED:<sha256_of_nimbus_metadata.json>`  
**check 锚点：** 文件内容匹配 `^VERIFIED:[a-f0-9]{64}$`；sha256 值与当前 workspace 中 nimbus_recall_metadata.json 实际内容的哈希一致  
**难度向量：** V7（Bash SHA-256 sign-off token，不实际运行脚本则无法得到正确值）  
**涉及：** scripts/verify_recall_data.py

### 轮次 Q17（终轮）
**意图：** 提交最终合规审查清单  
**产物：** `rca_outputs/compliance_checklist.json`  
**字段：** `{"items":[{"id","description","status","evidence_file","cfr_citation"}]}`（至少 8 条）  
**check 锚点：**  
- 包含 id="MDR-30DAY"，cfr_citation="21 CFR 803.50(a)(1)"  
- 包含 id="RECALL-REPORT"，cfr_citation="21 CFR 806.10"  
- 包含 id="IVENIX-SOFTWARE"，evidence_file 引用 "ivenix_recall_metadata_v2.json"（v2，不得为 v1）  
**难度向量：** V9（verbatim CFR 条款号）、V4（跨轮闭合：evidence_file 引用须与 Q12 产出一致）  
**涉及：** 全局综合

---

## Update 设计（含 Supersede 与体量规划）

### Update 1（Q07 之后注入）
**内容：** 修订 Ivenix Field Safety Notice，明确 affected_software_version 为 "5.10.1 及更早版本"（非之前 session 中提到的 "5.10.0"）；确认召回号 Z-0885-2026；补充 LVP-SW-0005 产品码说明；新增医院实施指南（含电池 70% 阈值细节、双零速率规避操作规程）。  
**体量来源：** 扩展版 Field Safety Notice（~12k tokens）+ 实施指南（~10k tokens）+ 飞书群讨论记录（~13k tokens）= 约 35k tokens  
**影响轮次：** Q08 开始，affected_software_version 答案从 "5.10.0" 变为 "5.10.1 及更早"

### Update 2（Q11 之后注入，含 Supersede）
**内容：**  
- **Supersede Update 1 局部：** 声明 "30 units" 数字不应被引用为软件安装量，须标记为 undisclosed（Q12 触发）  
- **新增信息：** Nimbus 分发起始日确认为 2015-02-27；补充 21 CFR 806 的 10 工作日上报窗口法规文本；新增 CAPA 验证要求文件  
**体量来源：** 监管邮件线程（~8k tokens）+ 更新版 CAPA 指南（~12k tokens）+ 21 CFR 806 条文摘录（~8k tokens）+ 分发数据验证报告（~6k tokens）= 约 34k tokens  
**影响轮次：** Q12（units 字段），Q13（distribution_start 确认）

---

## 4-5 条 Preference

| # | Preference 规则 | 注入方式 | 考察轮次 |
|---|-----------------|----------|----------|
| P1 | 5-Why 分析必须以 Markdown 表格形式呈现，不得使用连续 prose 叙述 | Q03 题目明确说明 | Q03，Q14 中再次检查格式合规 |
| P2 | 鱼骨图（Ishikawa）结构化输出必须使用六 M 分类（Man/Machine/Material/Method/Environment/Measurement），JSON schema 固定 | Q05 题目明确说明 | Q05，Q17 静默考察 |
| P3 | MDR 相关文档必须按 FDA MedWatch Form 3500A 标准 Section 编号（A 至 G），不得自定义章节名 | Q11 题目明确说明 | Q11，Q17 抽查 |
| P4 | Executive Summary 文档须包含 YAML frontmatter 块（含 date, author, recall_cases, classification 字段）| Q14 题目明确说明 | Q14，Q15 隐式检查是否延续 |
| P5 | 最终报告类文件命名规范：`final_rca_report_YYYYMMDD.md`，使用实际生产日期，不得使用占位符 | sess-02 Feishu 群组中 QA 负责人明确提到（非题目直接说明）| Q15 静默考察 |

---

## 难度向量绑定摘要

| 向量 | 绑定轮次 |
|------|----------|
| V1（多源信息冲突）| Q13（分发起始日 2014 vs 2015-02-27 冲突） |
| V2（动态 update 反转）| Q08（软件版本号 5.10.0 → 5.10.1）、Q12（units→undisclosed）|
| V3（隐式 preference 考察）| Q03(P1)、Q05(P2)、Q11(P3)、Q14(P4)、Q15(P5) |
| V4（跨轮数值闭合）| Q06(complaints=3698)、Q09、Q14、Q17 |
| V5（失真摘要诱饵）| Q02（识别 HONEYPOT：ivenix_injuries=5→2，nimbus_cutoff 错误）|
| V6（废弃副本红鲱鱼）| Q10（SynchroMed II 2019 旧案不得引入）|
| V7（Bash SHA-256 sign-off）| Q16 |
| V8（schema-by-shape 严格校验）| Q01、Q05 |
| V9（verbatim 条款/字段引用）| Q04、Q08、Q11、Q17 |
| V10（supersede 辨别）| Q12（Update 2 撤销 Update 1 的 "30 units" 字段）|

---

## 拆分建议

素材体量充足（约 130k tokens 初始 workspace，2 次 update 各约 34-35k tokens），可支撑单场景完整运行。若需拆分：
- **sci2-A**：Nimbus 硬件失效 RCA（Q01-Q07, Q13-Q16）
- **sci2-B**：Ivenix 软件异常 RCA + supersede 辨别（Q08-Q12, Q17）

当前建议：**保持单场景**，17 轮覆盖所有 10 个难度向量，设计完整度高。
