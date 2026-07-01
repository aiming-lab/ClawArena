# sec4 BRIEF — GDPR 数据合规审计

> 场景 ID: sec4 | Family: Security/Compliance/Finance
> 总行数约 210 行（含表格）

---

## 一、场景叙事背景

**企业背景**：VeritasCloud GmbH，总部位于法兰克福，为中型 SaaS 平台（CRM + HR 模块），欧盟境内注册用户约 80 万人，员工 1,200 人。公司近期获得 B 轮融资，投资方要求在 90 天内完成内部 GDPR 合规审计，以便向欧洲监管机构（德国 BayLDA）提交合规证明，同时响应一批积压的数据主体请求。

**Agent 角色**：受雇的外部合规顾问（Data Privacy Consultant），对接内部 DPO（Lena Fischer）。需在多个 session 中：
1. 审计并补全 Article 30 处理活动记录（RoPA）
2. 处理数据主体访问请求（DSAR）积压队列
3. 核查数据泄露事件的 72 小时通报合规性
4. 完成 DPIA 风险矩阵
5. 输出最终合规状态报告（含 Article 83 风险敞口计算）

**Workspace 素材来源**：全部围绕真实 GDPR 条款（Articles 5/12/15/17/30/33/35/37/83）及 CIRCL 开源 JSON schema 合成。

---

## 二、真实来源链接表

| # | 来源名称 | URL | 类型 |
|---|---------|-----|------|
| S1 | GDPR Art. 30 — gdpr-info.eu | https://gdpr-info.eu/art-30-gdpr/ | official_doc |
| S2 | GDPR Art. 83 — gdpr-info.eu | https://gdpr-info.eu/art-83-gdpr/ | official_doc |
| S3 | GDPR Art. 33 — gdpr-info.eu | https://gdpr-info.eu/art-33-gdpr/ | official_doc |
| S4 | GDPR Art. 12 — gdpr-info.eu | https://gdpr-info.eu/art-12-gdpr/ | official_doc |
| S5 | GDPR Art. 15 — gdpr-info.eu | https://gdpr-info.eu/art-15-gdpr/ | official_doc |
| S6 | GDPR Art. 37 — gdpr-info.eu | https://gdpr-info.eu/art-37-gdpr/ | official_doc |
| S7 | GDPR Art. 5 — gdpr-info.eu | https://gdpr-info.eu/art-5-gdpr/ | official_doc |
| S8 | GDPR Art. 35 — gdpr-info.eu | https://gdpr-info.eu/art-35-gdpr/ | official_doc |
| S9 | CIRCL RoPA JSON Schema (GitHub) | https://github.com/CIRCL/compliance/blob/master/gdpr/json-schema/processing-activities-records-schema.json | dataset |
| S10 | EDPB Guidelines 9/2022 v2.0 (Breach Notification) | https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-92022-personal-data-breach-notification-under_en | regulation |
| S11 | EUR-Lex GDPR Full Text (CELEX:32016R0679) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 | official_doc |
| S12 | GDPR Enforcement Tracker (enforcementtracker.com) | https://www.enforcementtracker.com/ | dataset |

---

## 三、Ground-Truth 锚点表

| 锚点名 | 精确值 | 来源 URL | 备注 |
|--------|--------|----------|------|
| A1: DSAR 响应基准时限 | 1 个月（calendar month）| https://gdpr-info.eu/art-12-gdpr/ | Art. 12(3) |
| A2: DSAR 延期上限 | +2 个月（需在初始 1 个月内通知理由）| https://gdpr-info.eu/art-12-gdpr/ | Art. 12(3) |
| A3: 数据泄露通报 SA 时限 | 72 小时（after becoming aware）| https://gdpr-info.eu/art-33-gdpr/ | Art. 33(1) |
| A4: 一级罚款上限（程序性违规）| €10,000,000 或全球年营业额 2%（取高者）| https://gdpr-info.eu/art-83-gdpr/ | Art. 83(4) |
| A5: 二级罚款上限（实质性违规）| €20,000,000 或全球年营业额 4%（取高者）| https://gdpr-info.eu/art-83-gdpr/ | Art. 83(5) |
| A6: Art. 30 记录 4 员工豁免阈值 | 250 人（< 250 人员工可豁免，除非处理高风险/特殊类别数据）| https://gdpr-info.eu/art-30-gdpr/ | Art. 30(5) |
| A7: RoPA 控制者必填字段（controller）| name_and_contact_details, purposes, data_subject_categories, personal_data_categories, recipient_categories, third_country_transfers, retention_periods, security_measures | https://github.com/CIRCL/compliance/blob/master/gdpr/json-schema/processing-activities-records-schema.json | Art. 30(1) |
| A8: Art. 5(1) 六原则名称 | lawfulness_fairness_transparency, purpose_limitation, data_minimisation, accuracy, storage_limitation, integrity_and_confidentiality | https://gdpr-info.eu/art-5-gdpr/ | Art. 5(1)(a-f) |
| A9: Art. 37(1) DPO 强制任命三种情形 | (a) 公共机构 (b) 大规模系统监控 (c) 大规模处理第 9/10 条特殊类别数据 | https://gdpr-info.eu/art-37-gdpr/ | Art. 37(1)(a)(b)(c) |
| A10: Art. 33(3) 通报必含字段 | nature_of_breach, categories_and_number_of_data_subjects, categories_and_number_of_records, DPO_contact, likely_consequences, measures_taken | https://gdpr-info.eu/art-33-gdpr/ | Art. 33(3)(a-d) |
| A11: Art. 35 DPIA 强制触发条件数 | 满足 EDPB 九项标准中的 ≥2 项即须进行 DPIA | https://gdpr-info.eu/art-35-gdpr/ | EDPB Guidelines |
| A12: Art. 83(4) 适用条款范围（一级）| Arts. 8, 11, 25-39, 42-43 | https://gdpr-info.eu/art-83-gdpr/ | Art. 83(4) |
| A13: Art. 15(3) 数据副本条款 | "The controller shall provide a copy of the personal data undergoing processing." | https://gdpr-info.eu/art-15-gdpr/ | Art. 15(3) |

---

## 四、Workspace 文件树与体量规划（初始 > 100k tokens）

```
workspace/
├── company/
│   ├── overview.md                        # 公司背景、业务描述（~2k tokens）
│   ├── org_chart.json                     # 组织架构含 DPO 信息（~1k tokens）
│   └── processing_systems.md              # 系统清单（CRM/HR/Analytics/Billing，~3k tokens）
│
├── ropa/
│   ├── ropa_controller_draft_v1.json      # Art.30 控制者 RoPA 草稿（30 个处理活动，~25k tokens）
│   ├── ropa_controller_legacy_v0.json     # 旧版 RoPA（含故意失真字段，蜜罐，~20k tokens）
│   ├── ropa_processor_draft_v1.json       # Art.30 处理者 RoPA（~10k tokens）
│   └── ropa_schema_reference.json         # CIRCL JSON schema（~5k tokens）
│
├── dsar/
│   ├── dsar_queue.csv                     # 积压 DSAR 列表（50 条，~8k tokens）
│   ├── dsar_response_templates/
│   │   ├── template_access.md             # Art.15 回复模板（~2k tokens）
│   │   ├── template_erasure.md            # Art.17 回复模板（~2k tokens）
│   │   └── template_portability.md        # Art.20 回复模板（~2k tokens）
│   └── dsar_log.json                      # 已处理记录（~5k tokens）
│
├── breach/
│   ├── incident_20250314_report.md        # 数据泄露初始报告（2025-03-14 发现）（~4k tokens）
│   ├── breach_notification_draft.json     # Art.33 通报草稿（~3k tokens）
│   ├── breach_internal_timeline.md        # 内部时间线（~3k tokens）
│   └── breach_risk_assessment.md          # 风险评估（~4k tokens）
│
├── dpia/
│   ├── dpia_hr_analytics_draft.md         # HR Analytics 模块 DPIA 草稿（~8k tokens）
│   ├── dpia_crm_profiling.md              # CRM 大规模分析 DPIA（~8k tokens）
│   └── dpia_template_edpb.md              # EDPB 模板（~4k tokens）
│
├── policies/
│   ├── privacy_policy_v3.md               # 隐私政策正式版（~6k tokens）
│   ├── retention_schedule.csv             # 保留期限表（~4k tokens）
│   └── data_transfer_agreements/
│       ├── scc_us_vendor_A.md             # 标准合同条款（US 供应商 A，~4k tokens）
│       └── scc_us_vendor_B.md             # 标准合同条款（US 供应商 B，~4k tokens）
│
├── audit/
│   ├── audit_checklist_v1.json            # 合规检查清单草稿（~6k tokens）
│   ├── gap_analysis_report_v1.md          # 差距分析报告（~8k tokens）
│   └── findings_log.csv                   # 审计发现记录（~5k tokens）
│
├── sessions/
│   ├── slack_dpo_channel_history.json     # Slack #gdpr-audit 频道历史（~10k tokens）
│   ├── email_thread_investor_due_diligence.md # 投资方尽调邮件链（~6k tokens）
│   ├── feishu_dm_lena_consultant.json     # 飞书 DM（DPO Lena ↔ 顾问）（~5k tokens）
│   └── discord_legal_team.json            # Discord 法务团队群聊（~5k tokens）
│
└── scripts/
    ├── validate_ropa.py                   # RoPA 字段校验脚本（~2k tokens）
    ├── check_dsar_deadlines.py            # DSAR 截止日期检查（~2k tokens）
    └── compute_penalty_exposure.py        # Art.83 罚款敞口计算（~2k tokens）

# 估算合计：约 170k tokens（超过 100k 要求）
```

---

## 五、Session 清单（6 个 Session）

| Session | 渠道 | 参与者 | 内容摘要 |
|---------|------|--------|---------|
| S-main | 主任务 session | Agent ↔ DPO Lena Fischer | 合规审计主线任务，贯穿全部 18 轮 |
| S-slack | Slack #gdpr-audit | Lena, CEO Klaus, Legal Counsel Maria | 关于 RoPA 完整性、泄露事件进展的讨论；含一条失真 bot 摘要（蜜罐） |
| S-email | Email thread | Investor IR team ↔ DPO | 投资方要求提交 Art.30 RoPA 和合规状态；含旧版 RoPA 附件（红鲱鱼） |
| S-feishu | 飞书 DM | DPO Lena ↔ Agent | Art.33 72 小时窗口计算、DSAR 优先级排序的私信讨论 |
| S-discord | Discord #legal-team | Legal Counsel Maria, Compliance Officer Ben | Art.37 DPO 任命资质讨论，含相互矛盾的旧备忘录（信息冲突） |
| S-feishu-group | 飞书群聊 #compliance | 全团队 | update 1 和 update 2 的注入渠道，含 supersede 通知 |

---

## 六、15-18 轮 exec_check 概要

| 轮次 | 目标意图 | 产物（文件/命令） | 检查锚点 | 难度向量 | Update/Pref |
|------|---------|-----------------|---------|---------|-------------|
| Q1 | 解析 RoPA 草稿，识别缺失字段 | `audit/gap_analysis_q1.json` | A7 字段名列表精确匹配（controller 必填 8 字段均到位，≥1 缺失标记 MISSING）| V8 schema-by-shape, V9 verbatim | Pref-1 JSON 格式 |
| Q2 | 修复 RoPA controller 缺失字段 | `ropa/ropa_controller_fixed.json` | Art.30 全部 7 字段存在且非空，retention_periods 为数组 | V8, V4 | Pref-1 |
| Q3 | 按 Art.5(1) 标注每个处理活动的法律原则合规性 | `audit/art5_compliance_map.json` | A8 六原则名称 verbatim 引用（不可简写）| V9, V4 | Pref-2 |
| Q4 | 计算 DSAR 积压队列截止日期（Art.12 一个月规则）| `dsar/dsar_deadlines.csv` | A1 = 30 天（calendar month），逾期标记 OVERDUE；截止日期计算误差 ≤1 天 | V4, V8 | Pref-3 |
| Q5 | 处理高优先级 DSAR（Art.15 数据副本提供，含 Art.15(3) 引用）| `dsar/response_req_042.md` | 响应文件包含 Art.15(3) 条款编号 verbatim，含 "copy of the personal data undergoing processing" | V9, V3 | Pref-2 Pref-3 |
| Q6 | 检查数据泄露通报合规性（72h 窗口）| `breach/notification_compliance_q6.json` | A3 = 72 小时；发现时间 2025-03-14T09:00Z，通报时间读取 breach 文件并计算；status 字段为 "COMPLIANT" 或 "LATE" | V1 多源冲突（飞书 vs Slack 时间戳），V2 | |
| Q7 | 修复 Art.33(3) 通报草稿缺失字段 | `breach/breach_notification_final.json` | A10 通报必含 6 字段全部到位（nature_of_breach, categories_and_number_of_data_subjects, categories_and_number_of_records, DPO_contact, likely_consequences, measures_taken）| V8, V9 | Pref-1 |
| Q8 | 判断 HR Analytics 模块是否须做 DPIA | `dpia/dpia_trigger_assessment.json` | A11：判定触发（满足大规模系统监控 + 特殊类别数据 ≥2 项）；结论字段 required = true | V5 蜜罐（Slack bot 摘要误称"不需要 DPIA"）, V1 | Update-1 前 |
| Q9 | 完成 HR Analytics DPIA 风险矩阵 | `dpia/dpia_hr_analytics_final.json` | 风险矩阵含 likelihood(1-5) × severity(1-5)，high_risk_items 数组含 ≥2 项；residual_risk_score 为数值 | V8, V4 | Update-1 后（新增数据类别）|
| Q10 | 核查 DPO 任命合规性（Art.37）| `audit/dpo_appointment_check.json` | A9 三种情形：公司规模 80 万用户+大规模系统监控 → 符合 37(1)(b)；结论 mandatory = true；依据字段引用 "Art. 37(1)(b)" | V9, V6 旧备忘录红鲱鱼（Discord 旧 memo 称"500 人以下不需要 DPO"为废弃版本）| Pref-4 |
| Q11 | 计算 Art.83 罚款风险敞口（两档）| `audit/penalty_exposure.json` | A4 tier1_max = 10000000，A5 tier2_max = 20000000；营业额字段从 company_financials.json 读取并计算 2% / 4%；最终取两者高值 | V4, V8 | Pref-1 |
| Q12 | 识别并拒绝使用旧版 RoPA（v0 红鲱鱼）| `audit/ropa_version_decision.json` | 产物中 selected_version = "v1"，reason 包含 "legacy" 或 "superseded"；rejected_version = "v0" | V6 红鲱鱼, V10 supersede | Update-2（supersede Update-1 部分内容）|
| Q13 | 更新 RoPA 纳入 Update-2 新增处理活动（AI 推荐引擎）| `ropa/ropa_controller_v2.json` | 新增 processing_activity "ai_recommendation_engine"，purposes 字段含 "personalisation"，legal_ground = "legitimate_interests" | V2 信念修正, V4 | Update-2 |
| Q14 | 生成合规状态摘要报告 | `audit/compliance_summary.json` | 摘要包含 total_processing_activities（数值），dsar_overdue_count，breach_notification_status，dpia_required_modules（数组），dpo_mandatory（布尔）；所有数值与前轮产物一致（跨轮闭合）| V4 跨轮闭合, V8 | Pref-4 Pref-5 |
| Q15 | 按 Art.83 二级罚款条款标注每项合规缺口的法律依据 | `audit/penalty_mapping.json` | 每项缺口条目含 article_violated（精确条款号如 "Art. 5(1)(f)"）和 tier（1 或 2）；至少 3 项 tier-2 缺口 | V9, V4 | Pref-2 |
| Q16 | 运行校验脚本并将 SHA-256 sign-off 写入最终报告 | `audit/final_report_signoff.json` | 执行 `python scripts/compute_sha256_signoff.py workspace/audit/compliance_summary.json` 并将输出写入 signoff 字段；check 脚本本地重算比对，格式 VERIFIED:<sha256hex> | V7 Bash-SHA256 sign-off | Pref-1 |
| Q17 | 根据 Update-2（supersede）修正 DSAR 截止日期（新监管函将 1 个月解释为 30 日历日）| `dsar/dsar_deadlines_v2.csv` | Update-2 supersedes Update-1 的"扩展延期"解释；截止日期采用 30 日历日精确计算，与 Q4 输出相比有变化 | V10 supersede, V2 反转 | Update-2 |
| Q18 | 输出最终 GDPR 合规审计证书（JSON + SHA256）| `audit/gdpr_audit_certificate.json` | 包含 audit_date, company_id, dpo_name, overall_status, article_30_compliant, article_33_compliant, article_37_compliant, article_83_max_exposure；signoff 字段与 Q16 产物一致（跨轮闭合）| V4, V7, V8, V9 | Pref 全部静默考察 |

---

## 七、Update 设计

### Update-1（第 8 轮后注入）
- **触发时机**：Q8 完成后（DPIA 评估已提交）
- **内容**：新注入飞书群消息：CTO 确认 HR Analytics 模块新增了"健康状态预测"字段（special category data，Art.9），同时新增 workspace 文件 `company/hr_analytics_new_feature.md`（~35k tokens：包含技术规格文档、数据字典、API 接口说明、隐私评估初稿）
- **影响**：Q9 DPIA 风险矩阵须纳入新特殊类别数据；DPIA 结论由"高风险"升级为"须咨询 DPO 并提交 SA"
- **体量来源**：技术规格文档 20k + 数据字典 10k + 合同附件 5k = ~35k tokens

### Update-2（第 12 轮后注入，supersede Update-1 部分内容）
- **触发时机**：Q12 完成后
- **Supersede 内容**：新注入邮件（来自监管顾问 Maria）：Update-1 中 CTO 关于"可延期 3 个月回复 DSAR"的内部指引有误，监管函明确要求以 30 日历日计算，不适用于当前积压案例。同时新增 workspace 文件 `legal/supervisory_authority_letter_20250501.md`（~30k tokens：监管函全文、BayLDA 回函、法律备忘录）+ `ropa/ropa_controller_ai_addendum.json`（新增 AI 推荐引擎处理活动，~5k tokens）
- **影响**：Q13 须将 AI 推荐引擎纳入 RoPA；Q17 须用 30 日历日重算 DSAR 截止日期（supersede Q4 的延期逻辑）
- **体量来源**：监管函 15k + 法律备忘录 10k + 附件 5k + RoPA addendum 5k = ~35k tokens

---

## 八、Preference 清单（4-5 条）

| # | 偏好规则 | 注入方式 | 考察轮次 |
|---|---------|---------|---------|
| Pref-1 | 所有结构化产物必须输出为有效 JSON，字段名使用 snake_case，禁止注释 | 主 session 明确说明 | Q1,Q2,Q6,Q7,Q11,Q16,Q18 |
| Pref-2 | 条款引用须使用标准格式 "Art. X(Y)(Z)"（含点号和括号），不可简写为 "Article X" 或 "#X" | 第 3 轮 Lena 飞书 feedback | Q3,Q5,Q10,Q15 |
| Pref-3 | DSAR 响应文件头部必须包含 `case_id`, `request_date`, `response_deadline`, `status` 四个元数据字段 | 主 session 说明 | Q4,Q5 |
| Pref-4 | 所有报告结论字段必须使用大写布尔值字符串 "TRUE"/"FALSE" 而非布尔类型 true/false | 第 10 轮 Lena email feedback | Q10,Q14,Q18 |
| Pref-5 | 最终报告的 overall_status 只允许三个枚举值："COMPLIANT"、"PARTIALLY_COMPLIANT"、"NON_COMPLIANT" | 主 session 合规规范文档 | Q14,Q18 |

---

## 九、难度向量选用

| 向量 | 绑定轮次 | 说明 |
|------|---------|------|
| V1 多源信息冲突 | Q6, Q8 | 飞书与 Slack 对泄露发现时间记录矛盾；Discord 旧 memo 与 GDPR 官方条款冲突 |
| V2 动态 update 反转 | Q9, Q13, Q17 | Update-1 新增特殊类别数据改变 DPIA 结论；Update-2 supersede DSAR 延期逻辑 |
| V4 跨轮数值/事实闭合 | Q4→Q14, Q11→Q18, Q16→Q18 | DSAR 逾期数量、罚款敞口数值、SHA256 sign-off 需跨轮精确一致 |
| V5 失真摘要蜜罐 | Q8 | Slack bot 自动摘要误称"HR Analytics 无需 DPIA"，官方 Art.35 明文反证 |
| V6 废弃副本红鲱鱼 | Q10, Q12 | Discord 旧备忘录称"<500 人不需 DPO"（已废弃逻辑）；ropa_legacy_v0.json 旧版 RoPA |
| V7 Bash-SHA256 sign-off | Q16, Q18 | 须实际运行脚本取得 VERIFIED:<sha256>，不跑 Bash 无法填充 |
| V8 schema-by-shape 严格校验 | Q1,Q2,Q7,Q9,Q11,Q14,Q18 | JSON 结构/类型/枚举值精确校验 |
| V9 verbatim 字段引用 | Q3,Q5,Q7,Q10,Q15,Q18 | 须精确引用官方条款号和字段名 |
| V10 supersede 辨别 | Q12, Q17 | Update-2 撤销 Update-1 中 DSAR 延期解释，须识别替代而非叠加 |

（实际选用 V1/V2/V4/V5/V6/V7/V8/V9/V10 共 9 条，每轮至少绑定 2 条）

---

## 十、拆分建议

素材丰富，可考虑拆分为：
- **sec4a**：Art.30 RoPA 审计 + Art.37 DPO 合规（偏静态文档审计）
- **sec4b**：Art.33 数据泄露通报 + Art.35 DPIA + Art.83 罚款计算（偏动态事件响应）

当前作为单场景亦可行，建议保留单场景以保持叙事连贯性，split_suggestion 留存备用。

---

*BRIEF 版本：1.0 | 生成日期：2026-06-03*
