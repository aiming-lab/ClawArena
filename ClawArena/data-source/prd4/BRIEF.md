# BRIEF: prd4 — 客服工单升级与 SLA 合规

## 一、场景叙事背景

某中型 SaaS 企业（"NebulaTech"）使用 Jira Service Management 管理客户支持工单，并在 AWS 和 Atlassian Cloud 上运营核心产品。公司内部制定了一套参照 AWS Enterprise Support 与 Atlassian Cloud Enterprise SLA 条款的支持政策（SLA 矩阵）。

Agent 的角色为「支持运维工程师」，需在多个 session 中：
1. 解析传入的工单数据（JSON 格式），按 SLA 政策计算是否违约；
2. 生成升级报告（escalation report）并提交结构化归档；
3. 随着 update 注入政策修订、工单补丁，需辨别哪些 SLA 条款被撤销/更新；
4. 跑脚本生成 SHA-256 sign-off 以核验最终归档完整性。

真实 SLA 锚点来源：
- Atlassian Cloud SLA（Premium/Enterprise 可用性承诺、信用比例）
- Atlassian Support Offerings（L1–L4 响应时限）
- AWS Support Plans（Critical/Urgent/High/Normal/Low 分级及响应时间）
- AWS EC2 SLA（Region 99.99% / Instance 99.5%，信用层级）
- AWS Lambda SLA（99.95%，信用层级）
- Google Cloud TSSG（P0–P4 分级，Standard/Enhanced/Premium 响应时间）

---

## 二、真实来源链接表

| # | 来源 | 类型 | URL |
|---|------|------|-----|
| S1 | Atlassian Cloud SLA（Premium/Enterprise 可用性与信用） | 官方 SLA 文档 | https://www.atlassian.com/legal/sla |
| S2 | Atlassian Support Offerings（L1–L4 响应时限表） | 官方支持文档 | https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html |
| S3 | AWS Support Plans 响应时间对比表 | 官方支持页面 | https://aws.amazon.com/premiumsupport/plans/ |
| S4 | AWS Support API SeverityLevel（code/name 映射） | 官方 API 文档 | https://docs.aws.amazon.com/awssupport/latest/APIReference/API_SeverityLevel.html |
| S5 | Amazon EC2 SLA（区域 99.99% / 实例 99.5%，信用层级） | 官方 SLA 文档 | https://aws.amazon.com/ec2/sla/ |
| S6 | AWS Lambda SLA（99.95%，信用层级） | 官方 SLA 文档 | https://aws.amazon.com/lambda/sla/ |
| S7 | Google Cloud Technical Support Services Guidelines（P0–P4） | 官方 TSSG | https://cloud.google.com/terms/tssg |
| S8 | Salesforce 支持工单严重级别定义（L1–L4） | 官方帮助文档 | https://help.salesforce.com/s/articleView?id=000382814&language=en_US&type=1 |

---

## 三、Ground-Truth 锚点表

| 锚点名 | 精确值 | 来源 URL | 备注 |
|--------|--------|----------|------|
| A01_atl_premium_uptime | 99.90% | https://www.atlassian.com/legal/sla | Atlassian Premium 月度可用性承诺 |
| A02_atl_enterprise_uptime | 99.95% | https://www.atlassian.com/legal/sla | Atlassian Enterprise 月度可用性承诺 |
| A03_atl_premium_credit_tier1 | 10%（99.00%–99.90% 区间） | https://www.atlassian.com/legal/sla | Premium 信用第一档 |
| A04_atl_premium_credit_tier2 | 25%（95.00%–99.00% 区间） | https://www.atlassian.com/legal/sla | Premium 信用第二档 |
| A05_atl_premium_credit_tier3 | 50%（< 95.00%） | https://www.atlassian.com/legal/sla | Premium 信用第三档 |
| A06_atl_enterprise_credit_tier0 | 5%（99.90%–99.95% 区间） | https://www.atlassian.com/legal/sla | Enterprise 专属额外档位 |
| A07_atl_downtime_minute_def | error rate > 5% per minute | https://www.atlassian.com/legal/sla | Downtime Minute 定义 |
| A08_atl_claim_deadline | 15 天（calendar month 结束后） | https://www.atlassian.com/legal/sla | 信用申请截止期 |
| A09_atl_enterprise_L1_response | 30 分钟（24/7） | https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html | Enterprise L1 响应时限 |
| A10_atl_enterprise_L2_response | 2 小时（24/7） | https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html | Enterprise L2 响应时限 |
| A11_atl_enterprise_L3_response | 8 小时（工作日） | https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html | Enterprise L3 响应时限 |
| A12_atl_enterprise_L4_response | 24 小时（工作日） | https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html | Enterprise L4 响应时限 |
| A13_atl_premium_L1_response | 1 小时（24/7） | https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html | Premium L1 响应时限 |
| A14_atl_standard_L1_response | 2 个工作日小时（9/5） | https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html | Standard L1 响应时限 |
| A15_aws_critical_enterprise | < 15 分钟 | https://aws.amazon.com/premiumsupport/plans/ | AWS Enterprise：Business-critical system down |
| A16_aws_critical_business_plus | < 30 分钟 | https://aws.amazon.com/premiumsupport/plans/ | AWS Business+：Business-critical system down |
| A17_aws_urgent_response | < 1 小时 | https://aws.amazon.com/premiumsupport/plans/ | Production system down（所有计划） |
| A18_aws_high_response | < 4 小时 | https://aws.amazon.com/premiumsupport/plans/ | Production system impaired |
| A19_aws_severity_code_critical | code="critical", name="Business-critical system down" | https://docs.aws.amazon.com/awssupport/latest/APIReference/API_SeverityLevel.html | API 映射 |
| A20_aws_severity_code_urgent | code="urgent", name="Production system down" | https://docs.aws.amazon.com/awssupport/latest/APIReference/API_SeverityLevel.html | API 映射 |
| A21_aws_severity_code_high | code="high", name="Production system impaired" | https://docs.aws.amazon.com/awssupport/latest/APIReference/API_SeverityLevel.html | API 映射 |
| A22_aws_ec2_region_uptime | 99.99% | https://aws.amazon.com/ec2/sla/ | EC2 区域级可用性承诺 |
| A23_aws_ec2_instance_uptime | 99.5% | https://aws.amazon.com/ec2/sla/ | EC2 实例级可用性承诺 |
| A24_aws_ec2_credit_tier1 | 10%（99.0%–99.99%） | https://aws.amazon.com/ec2/sla/ | EC2 信用第一档 |
| A25_aws_ec2_credit_tier2 | 30%（95.0%–99.0%） | https://aws.amazon.com/ec2/sla/ | EC2 信用第二档 |
| A26_aws_ec2_credit_tier3 | 100%（< 95.0%） | https://aws.amazon.com/ec2/sla/ | EC2 信用第三档 |
| A27_aws_lambda_uptime | 99.95% | https://aws.amazon.com/lambda/sla/ | Lambda 月度可用性承诺 |
| A28_aws_lambda_credit_tier1 | 10%（99.0%–99.95%） | https://aws.amazon.com/lambda/sla/ | Lambda 信用第一档 |
| A29_aws_lambda_credit_tier2 | 25%（95.0%–99.0%） | https://aws.amazon.com/lambda/sla/ | Lambda 信用第二档 |
| A30_aws_lambda_credit_tier3 | 100%（< 95.0%） | https://aws.amazon.com/lambda/sla/ | Lambda 信用第三档 |
| A31_aws_lambda_error_def | 500 或 503 状态码（不含函数自定义生成的） | https://aws.amazon.com/lambda/sla/ | Lambda Error 定义 |
| A32_aws_lambda_interval | 5 分钟 | https://aws.amazon.com/lambda/sla/ | Lambda 可用性计算粒度 |
| A33_aws_ec2_auto_credit_trigger | 6 分钟（每 clock hour 内） | https://aws.amazon.com/ec2/sla/ | EC2 免申请自动信用触发阈值 |
| A34_aws_credit_claim_deadline | 第二个 billing cycle 结束前 | https://aws.amazon.com/ec2/sla/ | EC2 信用申请截止期 |
| A35_gcp_p1_premium_response | 15 分钟 | https://cloud.google.com/terms/tssg | GCP Premium P1 响应时限 |
| A36_gcp_p2_premium_response | 2 小时 | https://cloud.google.com/terms/tssg | GCP Premium P2 响应时限 |
| A37_gcp_p1_def | Critical Impact – Service Unusable in Production | https://cloud.google.com/terms/tssg | GCP P1 定义 |
| A38_gcp_p0_def | Impact to operating environments provisioned to support Mission Critical Services | https://cloud.google.com/terms/tssg | GCP P0 定义 |

---

## 四、Workspace 文件树与体量规划（目标 > 100k tokens）

```
workspace/
├── policy/
│   ├── sla_matrix_v1.json          # NebulaTech 内部 SLA 矩阵（基于 Atlassian Enterprise + AWS Enterprise）~8k tokens
│   ├── sla_matrix_v2.json          # Update-1 修订版（调整 L2 响应时限）~8k tokens
│   ├── escalation_policy.md        # 升级政策全文（响应时限、信用申请流程）~6k tokens
│   └── ARCHIVED_sla_matrix_v0.json # 废弃的旧版（红鲱鱼，含错误的 L1=1h）~5k tokens
├── tickets/
│   ├── tickets_batch_2024Q4.json   # 2024Q4 工单批次（200 条，含 severity/created_at/first_response_at/resolved_at/status）~40k tokens
│   ├── tickets_batch_2025Q1.json   # 2025Q1 工单批次（150 条）~30k tokens
│   └── tickets_patch_001.json      # Update-2 注入的工单补丁（修正 15 条工单的字段）~5k tokens
├── reports/
│   ├── escalation_summary_template.json  # 升级报告 JSON Schema 模板 ~3k tokens
│   └── monthly_sla_report_2024_11.md     # 2024 年 11 月已有月报（示范格式）~10k tokens
├── sessions/
│   ├── slack_channel_support-ops.json    # Slack #support-ops 频道历史（含 tool call 痕迹）~15k tokens
│   ├── slack_dm_alice_bob.json           # Slack DM：Alice（工程师）↔ Bob（产品）~8k tokens
│   ├── email_thread_sla_review.json      # Email 线程（SLA 政策讨论，含错误摘要诱饵）~10k tokens
│   ├── feishu_group_incident.json        # 飞书群聊（P1 事件响应记录）~8k tokens
│   └── discord_dm_charlie.json           # Discord DM（外部合作方咨询）~5k tokens
├── scripts/
│   ├── validate_ticket_sla.py       # 工单 SLA 合规检查脚本骨架 ~3k tokens
│   └── generate_report.py           # 报告生成脚本骨架 ~3k tokens
└── reference/
    ├── atlassian_sla_excerpt.md     # Atlassian 官方 SLA 关键条款摘录（verbatim）~5k tokens
    ├── aws_severity_mapping.json    # AWS severity code/name 映射表 ~2k tokens
    └── gcp_tssg_excerpt.md          # GCP TSSG P0–P4 定义摘录 ~3k tokens
```

**体量估算合计：约 178k tokens（约 700KB 文本），满足 > 100k 要求。**

每次 update 体量（> 30k tokens）：
- Update-1：注入修订版 sla_matrix_v2.json + 新 escalation_policy.md（修订章节）+ 30 条新 ticket 数据 ≈ 45k tokens
- Update-2：注入 tickets_patch_001.json（补丁）+ feishu 新群消息（撤销 Update-1 对 L2 响应时限的部分修订）+ 新月报草稿 ≈ 35k tokens

---

## 五、Session 清单（1 主 + 5 多渠道）

| Session ID | 类型 | 内容概述 |
|-----------|------|----------|
| main | Agent 主 session | 工单分析、SLA 计算、报告生成、脚本执行、sign-off |
| slack_support_ops | Slack 频道 #support-ops | 团队讨论 SLA 政策更新、工具调用痕迹（create_ticket、update_priority 等） |
| slack_dm_alice_bob | Slack DM | Alice 与 Bob 讨论 L2 响应时限争议（信息冲突：Alice 引用旧版 2h，Bob 引用新版 1h） |
| email_sla_review | Email 线程 | 法务/产品/支持三方 Email 讨论，含一封自动摘要邮件（蜜罐：将 L1 响应时限误写为 1h，与 Enterprise 30min 矛盾） |
| feishu_incident | 飞书群聊 | 真实 P1 事件响应记录（时间戳完整），含 Update-2 时的撤销通知 |
| discord_dm | Discord DM | 外部合作方（Charlie）询问 SLA 赔偿计算方式，含错误理解示例 |

---

## 六、15–18 轮 exec_check 概要

### Round 1（Q1）
- **意图**：解析 sla_matrix_v1.json，输出内部 SLA 政策摘要文件
- **产物**：`output/policy_summary.json`（含各 severity 级别 + 响应时限 + 信用档位）
- **Check 锚点**：A09（L1=30min）、A10（L2=2h）、A02（enterprise_uptime=99.95%）、A06（enterprise_credit_tier0=5%）
- **向量**：V8（schema 严格校验字段名、类型、数值范围）
- **Preference**：P1（JSON 字段名采用 snake_case）

### Round 2（Q2）
- **意图**：识别 ARCHIVED_sla_matrix_v0.json 为废弃副本，在 output/archive_audit.json 中标记其失效原因
- **产物**：`output/archive_audit.json`（含 `is_superseded: true`、失效日期、与 v1 的差异字段列表）
- **Check 锚点**：A09 vs 旧文件中错误的 L1=1h（必须标记为废弃值）
- **向量**：V6（废弃副本红鲱鱼识别）、V1（多源信息冲突）
- **Preference**：P1（snake_case）、P2（报告顶部附 metadata 块）

### Round 3（Q3）
- **意图**：从 tickets_batch_2024Q4.json 中筛出所有 first_response_at 超出 SLA 的工单（按 severity 对应响应时限），写入 `output/breach_tickets_Q4.json`
- **产物**：`output/breach_tickets_Q4.json`（含 ticket_id、severity、expected_response_min、actual_response_min、breach_delta_min）
- **Check 锚点**：A09–A12（各级响应时限），违约判断精确到分钟
- **向量**：V4（数值闭合：breach_delta_min = actual - expected）、V8（字段类型精确）
- **Preference**：P3（时间字段统一 ISO 8601 格式）

### Round 4（Q4）
- **意图**：读取 email_sla_review 中的自动摘要邮件，识别其中 L1 响应时限（1h）与官方来源（30min）的矛盾，在 `output/email_audit.json` 中记录蜜罐标记
- **产物**：`output/email_audit.json`（含 `honeypot_detected: true`、`claimed_value: "1h"`、`correct_value: "30min"`、`authoritative_source: "atlassian-support-offerings"`）
- **Check 锚点**：A09（L1=30min，Enterprise），`honeypot_detected` 必须为 true
- **向量**：V5（失真自动摘要蜜罐）、V1（多源冲突）
- **Preference**：P1（snake_case）、P2（metadata 块）

### Round 5（Q5）
- **意图**：计算 2024Q4 批次中各 severity 级别的 SLA 达标率（%），写入 `output/sla_compliance_Q4.json`
- **产物**：`output/sla_compliance_Q4.json`（含每个 severity 级别的 total_count、breach_count、compliance_rate，精确到小数点后两位）
- **Check 锚点**：compliance_rate 与 breach_tickets 数量闭合（A04 轮中写的 breach 数量 × 100 / total = 1 - compliance_rate）
- **向量**：V4（跨轮数值闭合：Q3 的 breach 数量必须与此处一致）、V8（数值范围 0.00–100.00）
- **Preference**：P4（数值保留两位小数）

### Round 6（Q6）
- **意图**：计算 Atlassian Enterprise 月度可用性低于 99.95% 时应赔付的信用比例，给定场景月度可用性为 99.92%
- **产物**：`output/credit_calc_atlassian.json`（含 actual_uptime、applicable_tier、credit_pct、credit_amount_usd）
- **Check 锚点**：A06（99.90%–99.95% → 5% credit for Enterprise），credit_pct 必须等于 5
- **向量**：V9（verbatim 引用条款名），V8（精确数值）
- **Preference**：P4（两位小数）

### Round 7（Q7）— UPDATE-1 注入（sla_matrix_v2 + escalation_policy 修订）
- **意图**：读取 Update-1 注入的 sla_matrix_v2.json（L2 响应时限从 2h 改为 90min），重新计算 Q4 批次中 L2 违约工单，更新 `output/breach_tickets_Q4_v2.json`
- **产物**：`output/breach_tickets_Q4_v2.json`
- **Check 锚点**：L2 响应时限须为 90min（v2 新值），而非 2h（v1 旧值）；违约工单数量会变化
- **向量**：V2（动态 update 反转：正确答案从 2h 变为 90min）、V4（数值闭合）
- **Preference**：P1、P3、P4

### Round 8（Q8）
- **意图**：从 slack_dm_alice_bob 中提取双方关于 L2 响应时限的争议，在 `output/conflict_resolution.json` 中记录信息来源评级与最终采信值
- **产物**：`output/conflict_resolution.json`（含 alice_claimed、bob_claimed、adopted_value、source_authority）
- **Check 锚点**：adopted_value 必须为 "90min"（来自 v2，非 v1 的 "2h"），source_authority 引用 "sla_matrix_v2"
- **向量**：V1（多源冲突综合）、V2（update 后修正）、V10（supersede 辨别）
- **Preference**：P2（metadata 块）、P1（snake_case）

### Round 9（Q9）
- **意图**：检查 2025Q1 批次工单，按 sla_matrix_v2 计算违约，生成 `output/breach_tickets_Q1.json`
- **产物**：`output/breach_tickets_Q1.json`
- **Check 锚点**：L1=30min（A09）、L2=90min（v2 更新值，V2 已验证）、L3=8h（A11）、L4=24h（A12）
- **向量**：V3（隐式 preference 考察：无人提示是否保持 snake_case 和 ISO 8601）、V4（数值一致性）
- **Preference**：P1、P3（静默考察）

### Round 10（Q10）
- **意图**：生成跨 Q4+Q1 的合并违约统计，写入 `output/combined_breach_summary.json`，并与各 session 聊天记录中提及的数字比对
- **产物**：`output/combined_breach_summary.json`（含 total_tickets、total_breaches、breach_pct、by_severity 细分）
- **Check 锚点**：total_breaches = Q4 违约数 + Q1 违约数（跨轮闭合），breach_pct 精确计算
- **向量**：V4（跨轮数值闭合）、V8（字段完整性）
- **Preference**：P4（两位小数）

### Round 11（Q11）— UPDATE-2 注入（tickets_patch_001 + feishu 撤销通知）
- **意图**：应用 tickets_patch_001.json 对已有违约计算结果打补丁（修正 15 条工单的 first_response_at），并依据飞书撤销通知将 L2 响应时限恢复为 2h（撤销 v2 对 L2 的修订），重新输出 `output/breach_tickets_Q4_v3.json`
- **产物**：`output/breach_tickets_Q4_v3.json`
- **Check 锚点**：L2 响应时限须恢复为 2h（A10，原始 Enterprise 值）；15 条补丁工单的计算须基于修正后的时间戳
- **向量**：V10（supersede：Update-2 撤销 Update-1 的 L2 修订，考察辨别替代而非叠加）、V2（信念修正）
- **Preference**：P1、P3、P4（静默考察）

### Round 12（Q12）
- **意图**：生成正式的月度升级报告（November 2024），严格按 escalation_summary_template.json Schema 填写，写入 `output/escalation_report_2024_11.json`
- **产物**：`output/escalation_report_2024_11.json`（含 report_metadata、sla_policy_version、breach_summary、top_breached_tickets[]、credit_recommendations[]）
- **Check 锚点**：sla_policy_version 必须为 "v1"（11 月适用 v1，v2 是后来修订的）；credit_recommendations 中的 credit_pct 与 A03–A06 精确匹配
- **向量**：V9（verbatim 引用条款字段名）、V8（Schema 严格校验）、V4（与 Q3/Q5 数字闭合）
- **Preference**：P2（metadata 块）、P5（报告正文附审核人签名字段）

### Round 13（Q13）
- **意图**：从 feishu_group_incident.json 提取 P1 事件的时间线（issue_detected_at、first_response_at、resolved_at），计算 MTTD、MTTR，写入 `output/incident_timeline.json`
- **产物**：`output/incident_timeline.json`（含 incident_id、severity="L1"、mttd_min、mttr_min、sla_breach: bool）
- **Check 锚点**：A09（L1=30min，用于判断 sla_breach）；mttd/mttr 精确到分钟
- **向量**：V4（数值闭合：resolved_at - first_response_at = mttr_min × 60）、V3（隐式格式 preference）
- **Preference**：P3（ISO 8601，静默考察）

### Round 14（Q14）
- **意图**：运行 validate_ticket_sla.py 脚本（需 agent 补全关键逻辑），对 output/breach_tickets_Q4_v3.json 执行脚本级验证，将结果写入 `output/validation_result.json`
- **产物**：`output/validation_result.json`（含 validated_count、error_count、invalid_ticket_ids[]）
- **Check 锚点**：validated_count + error_count = total tickets in v3；脚本须实际运行（Bash exec），不能只填写
- **向量**：V7 前置步骤（需真实跑脚本），V8（Schema 校验）
- **Preference**：P1、P4

### Round 15（Q15）
- **意图**：计算 AWS EC2 在给定月度（实际可用性 98.5%）下的信用比例，并给出信用申请截止日期（假设月份为 2024-11），写入 `output/aws_credit_calc.json`
- **产物**：`output/aws_credit_calc.json`（含 service="ec2"、actual_uptime_pct=98.5、credit_pct=30、claim_deadline="2025-01-31"）
- **Check 锚点**：A24/A25（98.5% 落在 95.0%–99.0% → 30% credit）；A34（第二 billing cycle 结束前）
- **向量**：V9（verbatim 条款值引用）、V8（数值精确）
- **Preference**：P4（两位小数）

### Round 16（Q16）
- **意图**：汇总并对比 Atlassian Enterprise 与 AWS Enterprise 的 SLA 关键指标，生成对比表文件 `output/sla_comparison.json`（数组，每项含 vendor、metric_name、value、source_url）
- **产物**：`output/sla_comparison.json`
- **Check 锚点**：A01（Atlassian Premium 99.90%）、A02（Enterprise 99.95%）、A22（EC2 Region 99.99%）、A27（Lambda 99.95%）；source_url 须与真实 URL 精确匹配
- **向量**：V9（verbatim URL 引用）、V4（与前序各轮数值闭合）
- **Preference**：P1、P2、P5

### Round 17（Q17）— Bash SHA-256 Sign-off
- **意图**：运行 SHA-256 校验脚本，计算 output/ 目录下所有 JSON 文件的综合 checksum（脚本由 agent 编写并执行），将结果写入 `output/signoff.txt`，格式为 `VERIFIED:<sha256_hex>`
- **产物**：`output/signoff.txt`
- **Check 锚点**：check 脚本本地重算比对，格式严格为 `VERIFIED:` + 64 位十六进制；不跑 Bash 拿不到
- **向量**：V7（Bash-sha256 sign-off token，终轮）
- **Preference**：P1–P5 全量静默考察（命名、格式、metadata）

---

## 七、Update 设计

### Update-1（注入于 Q7 前）
- **内容**：
  1. `sla_matrix_v2.json`：L2 响应时限从 2h 修改为 90min（企业内部政策收紧）
  2. `escalation_policy.md`（修订版）：新增"L2 升级触发阈值"章节（90min 内无首次响应即自动升级）
  3. 30 条新 ticket 数据（用于 Q9）
- **体量**：约 45k tokens
- **Supersede 标记**：非 supersede（这是新增修订）

### Update-2（注入于 Q11 前）—含 supersede
- **内容**：
  1. `tickets_patch_001.json`：修正 15 条工单的 first_response_at（数据录入错误修正）
  2. 飞书群消息（新增）：管理层通知撤销 Update-1 中对 L2 响应时限的修订（恢复为 2h，因客服团队人力不足，无法满足 90min SLA）
  3. 更新 2024-11 月报草稿
- **体量**：约 35k tokens
- **Supersede 标记**：是（Update-2 的飞书通知撤销了 Update-1 中 L2=90min 的修订，恢复 L2=2h）

---

## 八、4–5 条 Preference

| ID | 规则 | 注入方式 | 考察轮次 |
|----|------|----------|---------|
| P1 | 所有 JSON 输出字段名使用 snake_case（不得使用 camelCase 或连字符） | Q1 显式说明 | Q1–Q17 全程 |
| P2 | 每份报告文件顶部附 metadata 块（含 generated_at、agent_id、schema_version 字段） | Q2 显式反馈 | Q2–Q17 |
| P3 | 所有时间字段统一使用 ISO 8601 格式（YYYY-MM-DDTHH:MM:SSZ） | Q3 显式说明 | Q3–Q17 |
| P4 | 数值字段（百分比、分钟数、金额）保留两位小数（0.00 格式） | Q5 显式说明 | Q5–Q17 |
| P5 | 报告文件末尾附 reviewer_signature 字段（值可为空字符串，但字段必须存在） | Q12 显式注入 | Q12–Q17 |

---

## 九、难度向量分配汇总

| 向量 | 绑定轮次 | 说明 |
|------|---------|------|
| V1 多源信息冲突综合 | Q2、Q4、Q8 | 废弃副本 vs 现行版、蜜罐邮件 vs 官方文档、Slack DM 双方说法不一 |
| V2 动态 update 反转 | Q7、Q8、Q11 | Update-1 修改 L2，Update-2 撤销；信念须随 update 修正 |
| V4 跨轮数值/事实闭合 | Q5、Q7、Q10、Q13、Q17 | 违约数、compliance_rate、MTTR、SHA-256 均须与前轮一致 |
| V5 失真自动摘要蜜罐 | Q4 | Email 中的自动摘要将 L1=1h，官方为 30min，须识别并标记 |
| V6 废弃副本红鲱鱼 | Q2 | ARCHIVED_sla_matrix_v0.json 含错误 L1=1h，引用即判错 |
| V7 Bash-sha256 sign-off | Q14（前置）、Q17（终轮） | 须真实运行脚本，不跑拿不到 VERIFIED 串 |
| V8 schema-by-shape 严格 check | Q1、Q3、Q5、Q6、Q12、Q15 | JSON 字段类型/范围/精确值三层校验 |
| V9 真实来源字段 verbatim 引用 | Q4、Q6、Q12、Q15、Q16 | source_url、条款名、credit_pct 须与官方来源精确一致 |
| V10 supersede 辨别 | Q8、Q11 | Update-2 撤销 Update-1 的 L2 修订；须辨别"替代"而非"叠加" |
| V3 隐式 preference 静默考察 | Q9、Q13、Q17 | snake_case、ISO 8601、两位小数无人提示时是否坚持 |

---

## 十、可行性与拆分建议

**Viability**：strong。素材极为丰富：Atlassian（L1–L4 × 3 tier）、AWS（5 级 × 3 plan）、GCP（P0–P4 × 3 tier）提供大量可查锚点；工单数据体量可合成至 > 100k tokens；多渠道 session 天然支持信息冲突设计。

**拆分建议**：若需拆分，可按以下方向拆为两个独立场景：
1. **prd4a**：纯 Atlassian JSM 环境的 SLA 计算与工单分级合规（聚焦 Atlassian L1–L4 矩阵）
2. **prd4b**：多云（AWS + GCP）支持工单的 severity 映射与跨平台 SLA 信用计算（聚焦 AWS severity code/name 映射 + GCP P0–P4 跨厂商对比）

当前规划已足够作为一个完整场景，建议保持合并。
