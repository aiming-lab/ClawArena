# BRIEF：sec5 — 反欺诈交易调查

## 一、场景叙事背景

**虚构机构**：MeridianPay（一家处理欧洲及北美信用卡与移动支付的中型支付处理商），其合规团队使用内部欺诈分析平台 FraudScope。

**角色**：玩家扮演初级欺诈调查分析师，入职第一周即承接一批待处理可疑交易告警，须完成从原始数据摄取、特征工程、风险评分、案例分类，到 SAR（可疑活动报告）起草，再到监管阈值合规核查的完整调查链路。

**真实素材锚点**：
- 数据集字段取自 ULB 信用卡欺诈数据集（Kaggle/MLG-ULB）与 PaySim 合成移动支付数据集
- 监管规则取自 Visa VAMP 2026、Mastercard ECP/HECM、FinCEN SAR Form 111 官方要求
- 内部 SLA 框架参考行业标准（告警响应 2 小时、案件结案 3 个工作日、ESC≥$50,000 上报高管）

**动态变化**：调查过程中接收两次 update：Update-1 注入一批补充交易日志与初步机器学习模型输出（含错误的自动摘要诱饵）；Update-2 撤销/修订 Update-1 中的部分评分规则（supersede），并追加一个新监管通知要求在 30 天内完成 SAR 归档。

---

## 二、真实来源链接表

| # | 来源名称 | URL | 类型 | 用途 |
|---|---------|-----|------|------|
| S1 | ULB Credit Card Fraud Detection — Kaggle | https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud | dataset | 主数据集字段、欺诈占比、PCA 特征 |
| S2 | PaySim Synthetic Financial Datasets — Kaggle | https://www.kaggle.com/datasets/ealaxi/paysim1 | dataset | 移动支付字段、事务类型、isFlaggedFraud 阈值 |
| S3 | PaySim GitHub (Lopez-Rojas) | https://github.com/EdgarLopezPhD/PaySim | github | PaySim 模拟参数、事务类型定义 |
| S4 | Visa VAMP 2026 Merchant Compliance — Corgi Labs | https://www.corgilabs.ai/insights/vamp-2026-merchant-compliance | regulation | VAMP ratio 公式、150 bps 阈值、$8/event 罚款 |
| S5 | Visa VAMP Rules 2026 — Seamless Chex | https://www.seamlesschex.com/blog/new-visa-vamp-rules-2026 | regulation | April 1 2026 执行日期、TC40+TC15/TC05 公式 |
| S6 | Mastercard ECM Program Thresholds — Chargebacks911 | https://chargebacks911.com/mastercard-chargebacks/mastercard-excessive-fraud-chargeback-monitoring-programs/mastercard-ecm-program-thresholds-tiers/ | regulation | ECM 150 bps、HECM 300 bps、月费阶梯 |
| S7 | Visa & Mastercard Thresholds — HighRiskIntel | https://highriskintel.com/blog/what-is-chargeback-threshold | regulation | VDMP Early Warning 0.65%、Standard 0.9%、Excessive 1.8% |
| S8 | Visa & MC Monitoring Programs — Solidgate | https://solidgate.com/blog/monitoring-programs/ | regulation | VFMP/VDMP 三档阈值、Mastercard EFM 四条件 |
| S9 | FinCEN SAR FAQ — FinCEN.gov | https://www.fincen.gov/resources/frequently-asked-questions-regarding-fincen-suspicious-activity-report-sar | official_doc | SAR 30/60 天期限、$5,000 阈值、Form 111 |
| S10 | FinCEN SAR Filing Requirements — FluxForce | https://www.fluxforce.ai/regulations/us-fincen-suspicious-activity-report-sar | regulation | Form 111 字段、五个 W、可疑活动类型 |
| S11 | Dal Pozzolo et al. 2014 (ULB 数据集论文) | https://www.sciencedirect.com/science/article/abs/pii/S095741741400089X | dataset | 数据集学术引用、DOI 10.1016/j.eswa.2014.02.026 |
| S12 | Fraud Investigation SLA — Hyperbots | https://www.hyperbots.com/glossary/fraud-investigation-sla | regulation | 告警响应 2h、案件 3 日结案、$50k ESC 阈值 |

---

## 三、Ground-Truth 锚点表

| 锚点名 | 值 | 来源 URL | 备注 |
|--------|---|---------|------|
| ULB_total_transactions | 284,807 | https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud | 2013 年 9 月欧洲持卡人两天数据 |
| ULB_fraud_count | 492 | https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud | 欺诈笔数 |
| ULB_fraud_rate | 0.172% | https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud | 类别严重不平衡 |
| ULB_features | V1–V28, Time, Amount, Class | https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud | V1-V28 为 PCA 变换；Time 单位为秒；Amount 单位为 EUR |
| PaySim_tx_types | CASH-IN, CASH-OUT, DEBIT, PAYMENT, TRANSFER | https://www.kaggle.com/datasets/ealaxi/paysim1 | 五类事务 |
| PaySim_isFlaggedFraud_threshold | 200,000 | https://www.kaggle.com/datasets/ealaxi/paysim1 | 系统自动标记金额上限（本地货币） |
| PaySim_fraud_rate | 0.129% (8,213/6,362,620) | https://www.kaggle.com/datasets/ealaxi/paysim1 | isFraud=1 占比 |
| PaySim_simulation_steps | 744 步（30 天，每步 1 小时） | https://github.com/EdgarLopezPhD/PaySim | 模拟时长 |
| VAMP_ratio_formula | (TC40 + TC15) / TC05 | https://www.seamlesschex.com/blog/new-visa-vamp-rules-2026 | 统一欺诈+争议分子；分母为已结算 CNP 交易 |
| VAMP_merchant_threshold_2026 | 150 bps (1.50%) | https://www.corgilabs.ai/insights/vamp-2026-merchant-compliance | 2026-04-01 起美/加/欧/亚太生效 |
| VAMP_enforcement_date | 2026-04-01 | https://www.seamlesschex.com/blog/new-visa-vamp-rules-2026 | 旧阈值 220 bps；CEMEA 仍为 220 bps |
| VAMP_fee_per_event | $8 USD | https://www.corgilabs.ai/insights/vamp-2026-merchant-compliance | 每笔超标欺诈或争议的罚款 |
| VAMP_grace_period | 3 个月 | https://www.corgilabs.ai/insights/vamp-2026-merchant-compliance | 首次违规 12 个月滚动窗口内免罚期 |
| MC_ECM_threshold | 150–299 bps & 100–299 笔/月 | https://chargebacks911.com/mastercard-chargebacks/mastercard-excessive-fraud-chargeback-monitoring-programs/mastercard-ecm-program-thresholds-tiers/ | ECM 起始门槛 |
| MC_HECM_threshold | ≥300 bps & ≥300 笔/月 | https://chargebacks911.com/mastercard-chargebacks/mastercard-excessive-fraud-chargeback-monitoring-programs/mastercard-ecm-program-thresholds-tiers/ | HECM 高级违规 |
| MC_ECP_fee_month_4_6_ECM | €5,000/月 | https://chargebacks911.com/mastercard-chargebacks/mastercard-excessive-fraud-chargeback-monitoring-programs/mastercard-ecm-program-thresholds-tiers/ | 第 4-6 月 ECM 罚款 |
| MC_ECP_fee_month_4_6_HECM | €10,000/月 | https://chargebacks911.com/mastercard-chargebacks/mastercard-excessive-fraud-chargeback-monitoring-programs/mastercard-ecm-program-thresholds-tiers/ | 第 4-6 月 HECM 罚款 |
| SAR_filing_deadline_standard | 30 日历天 | https://www.fincen.gov/resources/frequently-asked-questions-regarding-fincen-suspicious-activity-report-sar | 从首次发现可疑活动起算 |
| SAR_deadline_no_suspect | 60 日历天 | https://www.fincen.gov/resources/frequently-asked-questions-regarding-fincen-suspicious-activity-report-sar | 无法识别嫌疑人时延长至 60 天 |
| SAR_bank_threshold | $5,000 | https://www.fluxforce.ai/regulations/us-fincen-suspicious-activity-report-sar | 银行类机构强制申报下限 |
| SAR_form_number | FinCEN Form 111 | https://www.fluxforce.ai/regulations/us-fincen-suspicious-activity-report-sar | 统一取代旧版多张表格 |
| SLA_alert_response | 2 小时 | https://www.hyperbots.com/glossary/fraud-investigation-sla | 可疑告警初步审核期限 |
| SLA_case_resolution | 3 个工作日 | https://www.hyperbots.com/glossary/fraud-investigation-sla | 已确认案件结案期限 |
| SLA_escalation_threshold | $50,000 | https://www.hyperbots.com/glossary/fraud-investigation-sla | 触发高管上报的损失金额 |
| VDMP_early_warning | 0.65% | https://highriskintel.com/blog/what-is-chargeback-threshold | VDMP 早期预警档 |
| VDMP_standard | 0.9% | https://highriskintel.com/blog/what-is-chargeback-threshold | VDMP 标准监控档 |
| VDMP_excessive | 1.8% | https://highriskintel.com/blog/what-is-chargeback-threshold | VDMP 超标档（+1,000 笔争议） |
| ULB_doi | 10.1016/j.eswa.2014.02.026 | https://www.sciencedirect.com/science/article/abs/pii/S095741741400089X | Dal Pozzolo et al. 2014 学术引用 |

---

## 四、Workspace 文件树与体量规划

目标：初始 workspace > 100k tokens（≈400KB+），每次 update > 30k tokens（≈120KB+）。

```
workspace/
├── data/
│   ├── raw/
│   │   ├── creditcard_sample_10k.csv          # ULB 数据集 10,000 条采样（含 V1-V28, Time, Amount, Class）；~2MB
│   │   ├── paysim_sample_20k.csv              # PaySim 20,000 条采样（10 字段 × 20k 行）；~3MB
│   │   └── README_datasets.md                 # 字段说明、来源 URL、引用信息；~5KB
│   ├── alerts/
│   │   ├── alert_batch_001.json               # 可疑告警批次 1（500 条，JSON 格式，含 alert_id/tx_id/score/rule_id）；~300KB
│   │   ├── alert_batch_002.json               # 告警批次 2（Update-1 注入，300 条）；~180KB（update体量）
│   │   └── alert_schema.json                  # 告警字段 schema；~3KB
│   ├── transactions/
│   │   ├── tx_history_merchant_A.csv          # 商户 A 过去 90 天完整交易历史（~5,000 行）；~800KB
│   │   ├── tx_history_merchant_B.csv          # 商户 B 过去 90 天交易历史（~3,000 行）；~500KB
│   │   └── tx_enriched_with_features.parquet  # 特征工程后宽表（~400 列，2,000 行）；~2MB（说明：合成 parquet 描述文件）
│   └── reference/
│       ├── visa_vamp_thresholds_2026.json     # VAMP 阈值配置（150bps、TC40/TC15/TC05 公式、$8/event）；~5KB
│       ├── mc_ecp_thresholds.json             # Mastercard ECM/HECM 阈值与月费阶梯；~8KB
│       └── sar_form111_template.json          # SAR Form 111 字段模板（五个 W + 必填字段）；~10KB
├── models/
│   ├── fraud_model_v1_report.md               # 初始模型评估报告（含 confusion matrix、AUC=0.982、精度/召回数值）；~20KB
│   ├── fraud_model_v1_config.json             # 模型超参数（threshold=0.5、SMOTE ratio、特征权重）；~5KB
│   ├── fraud_model_v2_report.md               # Update-1 注入：新版模型报告（含故意失真的自动摘要诱饵）；~20KB（update体量）
│   └── feature_importance.csv                 # 特征重要性排名（V14/V10/V17/Amount 等真实字段）；~10KB
├── cases/
│   ├── case_template.json                     # 案件记录模板（case_id/status/assigned_to/sla_deadline/amount/classification）；~3KB
│   ├── open_cases.json                        # 当前待处理案件列表（20 件）；~30KB
│   └── closed_cases_archive.json             # 历史已结案件（50 件，含 resolution/sar_filed/amount）；~60KB
├── regulations/
│   ├── visa_vamp_fact_sheet_summary.md        # VAMP 规则摘要（含真实数值锚点）；~15KB
│   ├── mastercard_ecp_guide.md               # Mastercard ECP/HECM 指南（含费用阶梯表）；~15KB
│   ├── fincen_sar_requirements.md            # FinCEN SAR Form 111 要求（30/60天期限、$5000阈值）；~10KB
│   └── LEGACY_visa_vdmp_old_thresholds.md    # [红鲱鱼] 废弃的旧版 VDMP 阈值文档（220bps），标注 LEGACY；~8KB（V6 红鲱鱼）
├── comms/
│   ├── slack_fraud_team.json                  # Slack #fraud-alerts 频道历史（200 条消息，含 tool call 痕迹）；~50KB
│   ├── email_compliance.eml                   # 合规团队邮件线程（15 封，含 SAR 期限讨论）；~30KB
│   ├── feishu_case_dm.json                    # 飞书 DM：主管与分析师的案件分配对话；~20KB
│   └── discord_risk_ops.json                  # Discord #risk-ops 频道（技术讨论，含阈值配置片段）；~25KB
├── scripts/
│   ├── compute_vamp_ratio.py                  # 计算 VAMP ratio 脚本（TC40+TC15/TC05 公式）；~3KB
│   ├── classify_alerts.py                     # 告警分级脚本（low/medium/high/critical）；~5KB
│   ├── generate_sar_draft.py                  # SAR 起草辅助脚本；~8KB
│   └── check_sla_compliance.py               # SLA 合规检查脚本；~3KB
└── reports/
    ├── weekly_fraud_summary_template.md      # 周报模板；~5KB
    └── incident_report_template.md           # 事件报告模板；~5KB
```

**体量估算**：
- 原始数据文件（CSV/JSON）：~6MB（合成但围绕真实字段）
- 通讯历史（4 渠道）：~125KB
- 法规文档：~48KB
- 模型报告 + 配置：~55KB
- 案件数据：~93KB
- 脚本：~19KB
- **合计初始 workspace**：约 6.4MB 文本 ≈ 1,600k tokens（远超 100k 下限）
- **每次 update 注入量**：约 200KB+（超 30k tokens 下限）

---

## 五、Session 清单（4-6 个）

| Session | 类型 | 渠道 | 内容概要 |
|---------|------|------|---------|
| S-main | 主 session | FraudScope 平台操作界面 | 分析师接收任务、处理告警、写案件记录、计算合规指标、提交 SAR 草稿 |
| S-slack | 多渠道历史 | Slack #fraud-alerts | 团队讨论告警分级规则；含一条自动 bot 摘要（失真诱饵 V5）；同事提及旧版阈值（V6 红鲱鱼） |
| S-email | 多渠道历史 | Email（合规团队） | 法务合规官发邮件明确 SAR 30 天期限；更新 SAR 阈值适用对象 |
| S-feishu | 多渠道历史 | 飞书 DM | 主管 DM 分配优先级、注入 preference（文件命名规范、JSON schema 偏好） |
| S-discord | 多渠道历史 | Discord #risk-ops | 工程团队讨论 VAMP ratio 计算脚本；含一个错误版本（Update-1 supersede 前）与修正版本 |

---

## 六、15-18 轮 exec_check 概要

### Update 节点说明
- **Update-1**（约第 6 轮后注入）：注入新版模型报告（`fraud_model_v2_report.md`）、新增告警批次（`alert_batch_002.json`）、VAMP 配置旧版 JSON（含错误阈值 220bps 作为诱饵）
- **Update-2/supersede**（约第 12 轮后注入）：撤销 Update-1 中的 220bps 旧配置，替换为正确的 150bps；新增 FinCEN 监管通知要求在发现日起 30 天内提交 SAR；撤销 Update-1 中的模型 v2 评分建议（threshold 从 0.3 改回 0.5+SMOTE）

### Preference 注入点
- P1（第 1 轮显式）：所有输出 JSON 文件必须包含 `"schema_version": "1.0"` 字段
- P2（第 3 轮 feishu DM 注入）：案件 ID 格式为 `CASE-YYYYMMDD-NNN`
- P3（第 5 轮 email 注入）：SAR 叙述须按「五个 W」结构（who/what/when/where/why）组织
- P4（第 8 轮静默考察，违规进评分命令）：所有金额字段保留 2 位小数
- P5（第 10 轮静默考察）：监管阈值引用须附 source_url 字段

---

| 轮次 | 目标意图 | 产物 | Check 锚点 | 难度向量 | update/preference |
|------|---------|------|-----------|---------|-------------------|
| Q1 | 加载 ULB 数据集字段说明，输出字段清单 JSON | `output/q1_fields.json`（含 V1-V28, Time, Amount, Class 及描述） | 字段名精确匹配；Class 值域 {0,1}；schema_version="1.0" | V9（verbatim 字段名）、V8（schema 形状） | P1 |
| Q2 | 统计 ULB 欺诈率，计算欺诈笔数与总笔数 | `output/q2_stats.json`（total=284807, fraud=492, fraud_rate=0.00172） | 数值精确匹配（rate 容差 ±0.00001）；JSON 可解 | V8（精确数值）、V4（闭合） | — |
| Q3 | 解析 PaySim 数据集，输出事务类型与 isFlaggedFraud 阈值 | `output/q3_paysim_meta.json`（含5种类型、threshold=200000、case_id格式） | isFlaggedFraud_threshold=200000；types列表完整；case_id格式 CASE-YYYYMMDD-NNN | V9（verbatim字段）、V8 | P2（case_id 格式） |
| Q4 | 对 alert_batch_001.json 进行初步分级，high/critical 告警写入案件记录 | `output/q4_cases_created.json`（≥3件，含case_id/status/amount/sla_deadline） | case_id 格式合规；amount 保留 2 位小数；sla_deadline 在 2 个工作日内 | V8（schema 形状）、V3（P2 隐式） | P2 |
| Q5 | 阅读合规文档，输出 SAR 必填字段与叙述结构说明 | `output/q5_sar_structure.json`（含 who/what/when/where/why 五个 W、filing_threshold、form_number） | form_number="FinCEN Form 111"；threshold=5000；five_ws 字段非空 | V9（Form 111 verbatim）、V8 | P3（SAR 五个 W） |
| Q6 | 基于当前模型 v1 报告，计算三笔告警的风险评分并判定是否超过 threshold=0.5 | `output/q6_risk_scores.json`（3笔，各含 tx_id/score/decision） | 评分决策逻辑正确；**（Update-1 前）** threshold=0.5 | V4（与 Q2/Q3 数值一致）、V1 | — |
| **[Update-1 注入]** | 注入：model_v2_report.md（含失真摘要：threshold 建议改为 0.3）、alert_batch_002.json、VAMP 旧配置 220bps | — | — | — | — |
| Q7 | 读取 model_v2_report，提取关键指标并识别自动摘要与正文的矛盾 | `output/q7_model_comparison.json`（含 v1 vs v2 对比、identified_discrepancy 字段） | identified_discrepancy 非空；正确指出摘要中 threshold=0.3 与正文 threshold=0.5 矛盾 | V5（失真自动摘要诱饵）、V1（信息冲突） | Update-1 |
| Q8 | 计算商户 A 的 VAMP ratio（使用当前配置文件中的公式） | `output/q8_vamp_calc.json`（含 tc40_count/tc15_count/tc05_count/vamp_ratio/threshold_used/is_excessive） | **（Update-1 注入了错误的 220bps）**：若 agent 盲目使用 Update-1 配置则判错；正确答案须回溯到 `visa_vamp_thresholds_2026.json` 原始文件（150bps） | V1（多源冲突）、V6（旧配置红鲱鱼）、V2 | Update-1 |
| Q9 | 检查 LEGACY_visa_vdmp_old_thresholds.md，判断其是否适用于当前合规计算 | `output/q9_legacy_assessment.json`（含 document_status="LEGACY_DO_NOT_USE"、reason、correct_threshold=150） | document_status 字段值精确；correct_threshold=150；reason 非空 | V6（废弃副本识别）、V9 | — |
| Q10 | 对 alert_batch_002 的 high/critical 告警更新案件状态，计算 SLA 剩余时间 | `output/q10_cases_updated.json`（含 sla_remaining_hours、escalation_required 布尔值） | amount 保留 2 位小数；escalation_required=true 当 amount≥50000；source_url 字段存在 | V4（金额闭合）、V3（P4 P5 隐式） | P4、P5 |
| Q11 | 检查商户 B 是否触发 Mastercard ECM/HECM，输出合规状态报告 | `output/q11_mc_compliance.json`（含 monthly_chargebacks/chargeback_ratio_bps/program_tier/monthly_fee_eur） | bps 计算正确（n/prev_month_tx × 10000）；program_tier 为 "ECM"/"HECM"/"none" 之一；fee 与阶梯表精确匹配 | V8（精确数值）、V4（闭合） | — |
| Q12 | 起草 SAR 叙述草稿（针对最高金额告警案件） | `output/q12_sar_draft.json`（含 who/what/when/where/why 五个 W 结构、filing_deadline_days=30、amount_reported） | 五个 W 各非空；filing_deadline_days=30；amount≥5000；form_number="FinCEN Form 111"；source_url 字段 | V9（verbatim 字段）、V3（P3 P5）、V8 | — |
| **[Update-2/supersede 注入]** | 撤销 Update-1 的 220bps 配置 → 确认 150bps；撤销 threshold=0.3 建议 → 恢复 0.5；追加 FinCEN 通知：30 天内提交 SAR | — | — | V10（supersede 辨别） | — |
| Q13 | 重新计算商户 A 的 VAMP ratio（Update-2 后使用正确 150bps），输出修订合规报告 | `output/q13_vamp_revised.json`（含 old_threshold=220/new_threshold=150/revised_is_excessive/update_source="Update-2"） | new_threshold=150 精确；update_source 非空；与 Q8 结果对比字段存在 | V2（update 反转）、V10（supersede）、V4（闭合） | Update-2 |
| Q14 | 重新对 alert_batch_002 应用修订后的 threshold=0.5 评分规则，更新决策 | `output/q14_rescored.json`（含 threshold_applied=0.5、changed_decisions 列表） | threshold_applied=0.5（非 0.3）；changed_decisions 非空；与 Q6 决策一致性校验 | V2（信念修正）、V1（冲突解决）、V4 | Update-2 |
| Q15 | 生成完整周报 JSON（含本周告警数、结案数、VAMP 状态、MC 合规状态、SAR 计划） | `output/q15_weekly_report.json`（含 total_alerts/closed_cases/vamp_ratio/vamp_status/mc_program_tier/sar_to_file_count） | 所有数值与前序轮次一致（V4 全局闭合）；amount 2位小数；schema_version="1.0"；source_url 存在 | V4（跨轮闭合）、V3（P1 P4 P5）、V8 | — |
| Q16 | 生成 SAR 待提交清单并计算每件的截止日期（Update-2 注入的监管通知起算） | `output/q16_sar_deadlines.json`（含 case_id/amount/detection_date/deadline_date/days_remaining） | deadline = detection_date + 30天精确；case_id 格式合规；amount≥5000 | V9（30天deadline）、V2（supersede后新增要求）、V4 | Update-2 |
| Q17 | 运行 compute_vamp_ratio.py 脚本并将输出哈希写入 sign-off 文件 | `output/q17_signoff.txt`（格式：VERIFIED:<sha256>） | sha256 格式为 VERIFIED: 前缀 + 64 位十六进制；须实际运行脚本得到（不可手写伪造） | V7（Bash-sha256 sign-off）、V4 | — |

---

## 七、Update 设计详情

### Update-1（第 6 轮后注入，≥30k tokens）
**新增/修改文件**：
- `data/alerts/alert_batch_002.json`（新增 300 条告警，~180KB）
- `models/fraud_model_v2_report.md`（新版模型报告，~20KB，含**失真自动摘要**：建议 threshold 改为 0.3，正文实验数据显示最优仍为 0.5）
- `data/reference/visa_vamp_config_DRAFT.json`（**故意错误**：threshold=220bps，来自旧版，为红鲱鱼 V6）
- `comms/discord_risk_ops.json`（新增 Update-1 通讯记录，工程师讨论使用 0.3 阈值的争议）

**体量**：~210KB（>30k tokens）

**影响的正确答案**：Q7（识别失真摘要）、Q8（不应盲目采用 220bps）

---

### Update-2/Supersede（第 12 轮后注入，≥30k tokens）
**撤销内容**：
- 明确作废 `visa_vamp_config_DRAFT.json` 中的 220bps，替换为 `visa_vamp_thresholds_2026.json` 中的 150bps
- 撤销 `fraud_model_v2_report.md` 摘要中的 threshold=0.3 建议，恢复 threshold=0.5

**新增内容**：
- `regulations/fincen_notice_20260601.md`（新增 FinCEN 监管通知：自发现日起 30 日历天内提交 SAR）
- `comms/email_compliance_update2.eml`（合规官邮件，明确 supersede Update-1 的配置建议，~50KB）
- `cases/open_cases_updated.json`（更新后的案件列表，含新截止日期，~80KB）

**体量**：~140KB（>30k tokens）

**影响的正确答案**：Q13（150bps）、Q14（threshold=0.5）、Q16（30天SAR截止）

**Supersede 考察点（V10）**：Update-2 明确声明「以下条目替代 Update-1 第 3、5 条」，agent 须辨别是替代而非叠加——若同时引用 220bps 和 150bps 则判错。

---

## 八、4-5 条 Preference 规则

| # | 规则 | 注入方式 | 静默考察轮次 |
|---|------|---------|------------|
| P1 | 所有输出 JSON 文件必须包含顶层字段 `"schema_version": "1.0"` | Q1 显式指令 | Q10, Q15, Q16 |
| P2 | 案件 ID 格式严格为 `CASE-YYYYMMDD-NNN`（8位日期+3位流水号） | 第 3 轮飞书 DM | Q4, Q10, Q16 |
| P3 | SAR 叙述须按 who/what/when/where/why 五段式结构组织 | 第 5 轮 email | Q12, Q16 |
| P4 | 所有涉及金额的字段值须保留恰好 2 位小数（如 1234.56，不可 1234.5 或 1234.567） | 第 8 轮（隐式，前期 feishu 中提过但不强调） | Q10, Q12, Q15 |
| P5 | 引用监管阈值数据时，JSON 中须附 `"source_url"` 字段（值为真实来源 URL） | 第 10 轮（静默，仅在 discord 历史中出现过一次） | Q12, Q13, Q15, Q16 |

---

## 九、拆分建议

当前素材足以支撑单一场景，**无需拆分**。若后续扩展，可考虑：
- **sec5-a**：聚焦数据分析与特征工程链路（Q1-Q8）
- **sec5-b**：聚焦合规计算与 SAR 链路（Q9-Q17）

两者均能独立成章，但作为一个完整调查链路场景，合并更能体现跨领域综合能力。

---

## 十、难度向量绑定总览

| 向量 | 描述 | 绑定轮次 |
|------|------|---------|
| V1 | 多源信息冲突综合 | Q7, Q8, Q14 |
| V2 | 动态 update 反转 | Q13, Q14, Q16 |
| V3 | 隐式 preference 静默考察 | Q8（P4）、Q10（P4/P5）、Q15（P1/P4/P5） |
| V5 | 失真自动摘要诱饵 | Q7（model_v2 摘要 threshold=0.3 vs 正文 0.5） |
| V6 | 废弃副本红鲱鱼 | Q8（DRAFT 220bps）、Q9（LEGACY 文档识别） |
| V7 | Bash-sha256 sign-off token | Q17 |
| V9 | 真实来源字段 verbatim 引用 | Q1, Q3, Q5, Q12 |
| V10 | supersede 辨别 | Q13（Update-2 明确替代 Update-1 第 3、5 条） |

*本场景选用 V1、V2、V5、V6、V7（5 条激进向量，V3/V9/V10 作为辅助覆盖）。*
