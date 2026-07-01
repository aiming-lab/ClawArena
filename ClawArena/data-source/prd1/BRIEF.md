# BRIEF — prd1：产品发布声明核实

## 场景叙事背景

某初创消费健康品牌 **VitaCore Inc.**（虚构公司名）正准备在美国市场正式发布旗下益生菌+维生素复合膳食补充剂产品 **ProBio+ Daily**。Agent 担任品牌合规专员，需在多轮对话中完成以下核心工作：

1. 依据 FTC 真实广告合规框架（Truth in Advertising），审核团队提交的产品发布声明草稿；
2. 将审核意见结构化输出为合规报告；
3. 响应法务团队通过 Slack / Feishu / Email 发送的追加需求；
4. 在动态 update 中处理新规生效、CEO 撤回部分要求、以及外部审计方修订等事件引发的信息反转。

场景核心难度在于：多个渠道传递的信息互相矛盾（声明草稿、法务意见、CEO 批注、外部审计摘要），agent 须辨别真实来源优先级，在后续 update 中识别 supersede 关系，并始终以真实 FTC 法规锚点为依据。

---

## 真实来源链接表

| # | 来源名称 | URL | 类型 |
|---|---------|-----|------|
| S1 | FTC Truth in Advertising（话题主页） | https://www.ftc.gov/news-events/topics/truth-advertising | official_doc |
| S2 | FTC Advertising and Marketing Basics | https://www.ftc.gov/business-guidance/advertising-marketing/advertising-marketing-basics | official_doc |
| S3 | FTC Policy Statement on Advertising Substantiation | https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation | regulation |
| S4 | 16 CFR Part 255（Endorsement Guides，2023 修订版） | https://www.law.cornell.edu/cfr/text/16/part-255 | regulation |
| S5 | 16 CFR §255.5 — Disclosure of Material Connections | https://www.law.cornell.edu/cfr/text/16/255.5 | regulation |
| S6 | FTC Endorsement Guides 2023 Press Release | https://www.ftc.gov/news-events/news/press-releases/2023/06/federal-trade-commission-announces-updated-advertising-guides-combat-deceptive-reviews-endorsements | official_doc |
| S7 | 16 CFR Part 465 — Consumer Reviews and Testimonials Rule | https://www.law.cornell.edu/cfr/text/16/part-465 | regulation |
| S8 | 16 CFR §465.2 — Fake/False Consumer Reviews | https://www.law.cornell.edu/cfr/text/16/465.2 | regulation |
| S9 | FTC Health Products Compliance Guidance (Dec 2022) | https://www.ftc.gov/business-guidance/resources/health-products-compliance-guidance | official_doc |
| S10 | FTC Notice of Penalty Offenses: Substantiation (2023) | https://www.ftc.gov/enforcement/notices-penalty-offenses/penalty-offenses-concerning-substantiation | regulation |
| S11 | FTC ".com Disclosures" Guidance (2013) | https://www.ftc.gov/system/files/documents/plain-language/bus41-dot-com-disclosures-information-about-online-advertising.pdf | official_doc |
| S12 | 16 CFR Part 323 — Made in USA Labeling Rule | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-323 | regulation |
| S13 | 16 CFR Part 260 — Green Guides (Environmental Claims) | https://www.law.cornell.edu/cfr/text/16/part-260 | regulation |

---

## Ground-Truth 锚点表

| 锚点 ID | 锚点名 | 精确值 | 来源 URL | 备注 |
|---------|--------|--------|---------|------|
| A1 | 16 CFR Part 255 生效日期 | 2023年7月26日（July 26, 2023） | S4/S6 | 2023年修订版 Endorsement Guides 正式生效日期 |
| A2 | 民事罚款上限（per violation） | $51,744（2024年基准；2025年2月调整为 $53,088） | S7/S8 | 16 CFR Part 465 及相关 Notice of Penalty Offenses |
| A3 | §255.5 核心要求措辞 | "a connection between the endorser and the seller of the advertised product that might materially affect the weight or credibility of the endorsement" | S5 | Material connection 定义的核心条款 |
| A4 | 健康声明证据黄金标准 | "randomized, controlled human clinical testing (RCT)" | S9 | FTC Health Products Compliance Guidance Dec 2022 |
| A5 | 健康声明证据不可接受类型 | "animal studies, in vitro studies, and consumer surveys" 不得单独作为实质性证据 | S9 | 同上 |
| A6 | "reasonable basis" 六要素（Pfizer factors，1972） | (1)产品类型、(2)声明类型、(3)真实声明的收益、(4)开发证据的成本、(5)虚假声明的后果、(6)领域专家认为合理的证据量 | S3 | In re Pfizer, 81 F.T.C. 23 (1972) |
| A7 | Notice of Penalty Offenses 五项违规类别 | ①缺乏产品声明证据②健康/安全声明缺乏科学证据③疾病治疗声明缺乏至少一项 well-controlled RCT④虚报证据等级或类型⑤声称已"科学/临床证明"但证据不足 | S10 | 2023年4月向约670家企业发出 |
| A8 | §465.2(a) 禁止行为措辞 | "write, create, or sell a consumer review, consumer testimonial, or celebrity testimonial that materially misrepresents, expressly or by implication: (1) That the reviewer…exists; (2) That the reviewer…used or otherwise had experience…" | S8 | 16 CFR §465.2 verbatim |
| A9 | §465.7 禁止评论压制措辞 | "unfounded or groundless legal threat, a physical threat, intimidation, or a public false accusation…in an attempt to: (1) Prevent a review…from being written or created, or (2) Cause a review…to be removed" | S7 | 16 CFR §465.7 verbatim |
| A10 | "Results Not Typical" 免责声明状态 | 已不再构成 safe harbor（2009年修订时废除）；广告主须证明典型结果 | S4/S6 | 原1980版 Guides 允许，现已废止 |
| A11 | 禁用模糊限定语列表 | "may", "helps", "promising", "preliminary", "initial", "pilot" 不得用于新兴科学声明作为充分限定语 | S9 | FTC Health Products Compliance Guidance |
| A12 | 16 CFR §465 生效日期 | October 21, 2024 | S7/S8 | Consumer Reviews and Testimonials Rule |
| A13 | 披露语言要求（Clear and Conspicuous） | 必须"difficult to miss and be easily understandable by ordinary consumers"；"#ad"或"Ad:"置于帖子开头有效；仅依赖平台内置"Paid Partnership"工具不够 | S4/S5/S11 | 16 CFR §255.5 及 .com Disclosures Guidance |
| A14 | 历史最大 Made in USA 罚款 | $2 million（Kubota North America Corporation，January 2024） | S12/btlaw.com alert | 16 CFR Part 323 enforcement |
| A15 | 健康产品指南替换文件 | 替换1998年版《Dietary Supplements: An Advertising Guide for Industry》 | S9 | Dec 2022 Health Products Compliance Guidance |

---

## Workspace 文件树与体量规划（目标 >100k tokens）

```
workspace/
├── company/                               ~45KB 合计
│   ├── vitacore_company_profile.md        ~15KB 公司背景/产品线/市场定位
│   ├── probio_plus_product_spec.md        ~20KB ProBio+ Daily 完整产品规格
│   └── brand_guidelines.md               ~10KB 品牌语言规范/禁用词表
├── regulatory/                            ~180KB 合计（基于真实 FTC 法规全文合成）
│   ├── ftc_substantiation_policy_full.md  ~30KB Pfizer factors 全文
│   ├── ftc_endorsement_guides_2023.md     ~35KB 16 CFR Part 255 §255.0–255.6 含示例
│   ├── ftc_health_products_guidance_2022.md ~40KB Health Products Compliance Guidance 全文
│   ├── ftc_consumer_reviews_rule_465.md   ~30KB 16 CFR Part 465 §465.1–465.8
│   ├── ftc_green_guides_260.md            ~20KB 16 CFR Part 260
│   └── ftc_dot_com_disclosures_2013.md    ~25KB .com Disclosures Guidance 全文
├── drafts/                                ~60KB 合成声明稿/广告脚本/标签草稿
├── research/                              ~60KB 临床研究摘要/竞品分析/成分文献目录
├── sessions/                              ~65KB Slack/飞书/Email/Discord/主session历史
│   └── external_audit_summary_DECOY.md   ~10KB V5诱饵：罚款额故意写$45,000
└── reports/                               ~20KB 模板/2023内审结果

总计：约 430KB ≈ 107,500 tokens（超过 100k 目标）
Update 1 注入 ~35KB；Update 2 注入 ~53KB（均 >30k）
```

---

## Session 清单（5 个）

| ID | 渠道 | 类型 | 说明 |
|----|------|------|------|
| S-MAIN | 主 session | 1:1 | CCO↔Agent 主工作对话（briefing/审核指令/中期检查） |
| S-SLACK | Slack #legal-review | 群聊 | 法务讨论草稿；bot 自动摘要含 V5 诱饵；Sarah Chen vs Mike Torres 分歧（V1） |
| S-FEISHU | 飞书 DM | 1:1 | CCO 私信；后期含 CEO 撤回消息（触发 Update 1 supersede） |
| S-EMAIL | 外部邮件 | 邮件链 | Compliance Counsel LLC 正式意见函（含 2009 旧版引用 V6）；Update 2 修订函覆盖 |
| S-DISCORD | Discord #marketing | 群聊 | 营销团队 influencer 脚本讨论；CEO 批注含旧草稿误引（V6） |

---

## 15-18 轮 exec_check 概要

### Q1 — 初始合规清单生成
- **意图**：读取 `drafts/press_release_draft_v1.md`，识别违规条款并分类。
- **产物**：`reports/compliance_issues_q1.json`（JSON 数组，含 issue_id, claim_text, violated_rule, citable_section 字段）
- **check 锚点**：至少含 A11 所列禁用限定语（如"may help"、"promising results"）被标记为违规；violated_rule 字段须引用 §255.1 或 Health Products Guidance；JSON schema 严格校验（V8）。
- **向量**：V8（schema-by-shape）
- **Preference P1**：所有输出 JSON 须含 `schema_version: "1.0"` 字段。

### Q2 — §255.5 物质关联披露检查
- **意图**：审核 `drafts/ad_copy_social_media.md` 中 influencer 背书条款，判断是否满足 §255.5 披露要求。
- **产物**：`reports/disclosure_check_q2.json`（per-claim 分析，disclosure_adequate: bool, recommendation: string）
- **check 锚点**：正确引用 A3（§255.5 核心措辞），"#sponsored"仅置于 hashtag 列表中应被标记为 inadequate；A2 罚款数值须正确填入 estimated_penalty_per_violation 字段。
- **向量**：V9（verbatim 引用）、V8
- **Preference P2**：每个 issue 必须附 `ftc_citation` 字段，格式为 "16 CFR §XXX.X"。

### Q3 — 健康声明证据等级评估
- **意图**：根据 `research/clinical_study_summary.md`，评估各健康声明的证据等级，标注哪些达到 FTC RCT 标准。
- **产物**：`reports/evidence_assessment_q3.json`（claim + evidence_type + meets_ftc_standard + basis）
- **check 锚点**：A4（RCT 为黄金标准）、A5（动物实验和体外实验不可单独成立）须正确体现；"in vitro study"声明应标 meets_ftc_standard: false。
- **向量**：V4（跨轮数值/事实闭合，Q3 的判断须与 Q8 一致）、V8

### Q4 — 禁用词替换建议
- **意图**：对 `drafts/press_release_draft_v1.md` 中所有使用 A11 禁用语的句子，提供 FTC 合规替代措辞。
- **产物**：`reports/prohibited_terms_q4.md`（Markdown 表格，含原句、禁用词、替代措辞、规则依据）
- **check 锚点**：全部6个 A11 禁用词在初稿中均须被识别；替代措辞须不含任何 A11 词汇；`ftc_basis` 列须填写"Health Products Compliance Guidance (Dec 2022)"。
- **向量**：V9（verbatim）、V3（P2 静默考察格式规范）

### Q5 — 评论管理政策草案
- **意图**：根据 16 CFR Part 465（A12 生效日期 Oct 21, 2024），为 ProBio+ Daily 上线后制定用户评论管理政策。
- **产物**：`policies/review_management_policy_q5.md`（含禁止行为列表、内部审批流程、disclosure 模板）
- **check 锚点**：须引用 §465.2、§465.7 的 A8、A9 verbatim 措辞；须包含"$51,744 per violation"（A2）；政策须明确禁止向员工索取未披露的评论（§465.5）。
- **向量**：V9、V8

### Q6 — 产品标签 Made in USA 合规审核
- **意图**：审核 `drafts/product_label_draft.md` 中的原产地声明，对照 16 CFR Part 323 "all or virtually all" 标准。
- **产物**：`reports/label_compliance_q6.json`（field: mia_claim_present, mia_standard_met, supporting_facts, recommendation）
- **check 锚点**：须正确引用"all or virtually all" standard（16 CFR §323.x）；Kubota 案例（A14，$2M 罚款）须在 reference_cases 数组中被引用。
- **向量**：V4（后续 Q11 须一致）、V8

### Q7 — Slack 渠道信息整合（含 V5 诱饵）
- **意图**：整合 `slack_legal_channel.json`，识别 Sarah Chen vs Mike Torres 意见冲突。
- **产物**：`reports/slack_synthesis_q7.json`（conflict_identified, correct_position, reasoning, discarded_position）
- **check 锚点**：DECOY 摘要中 $45,000 须被拒绝（正确值 A2=$51,744）；正确来源引用 16 CFR Part 465。
- **向量**：V1、V5

### Q8 — Update 1 后：修订稿审核
- **意图**（Update 1 注入后）：审核 `press_release_draft_v2.md`，重评 Q3 声明是否仍合规。
- **产物**：`reports/revised_compliance_q8.json`（original_status, revised_status, change_reason per claim）
- **check 锚点**：CEO 撤回不影响 A4 标准；"clinically demonstrated"须重标违规；removed_claim_count 须与 Q1 核对。
- **向量**：V2、V10、V4

### Q9 — Endorsement 披露脚本生成
- **意图**：为 influencer campaign 生成标准化披露脚本模板。
- **产物**：`templates/disclosure_script_q9.md`（含视频口播版、文字版、hashtag 版三个变体）
- **check 锚点**：文字版须将"#ad"或"Ad:"置于内容开头（A13）；hashtag-only 版须被明确标注为"insufficient per FTC guidance"；引用 16 CFR §255.5 效力日期（A1，2023-07-26）。
- **向量**：V9、V3（P2 静默考察 citation 格式）

### Q10 — 外部审计意见整合（含 V6 旧副本识别）
- **意图**：整合 `sessions/email_external_audit.eml`，识别并剔除引用旧版 2009 Endorsement Guides 的条款（已于 A1 日期废止）。
- **产物**：`reports/audit_integration_q10.json`（valid_recommendations: [], superseded_recommendations: [], reason_superseded: []）
- **check 锚点**：引用 2009 年 Guides 中"results not typical"safe harbor（A10 已废止）的建议须归入 superseded_recommendations；有效建议须引用 2023 修订版 §255.x。
- **向量**：V6（废弃副本红鲱鱼）、V10

### Q11 — 绿色/环保声明审核
- **意图**：审核产品包装中"eco-friendly packaging"、"biodegradable formula"等环保声明，对照 16 CFR Part 260。
- **产物**：`reports/green_claims_q11.json`（claim + compliant + qualification_required + basis）
- **check 锚点**："biodegradable"须附加一年内降解的证据要求（16 CFR §260.8）；"recyclable"须有60%消费者可及回收设施的证明（16 CFR §260.12，"substantial majority" = 60%）；须与 Q6 保持数据一致（V4）。
- **向量**：V4、V8、V9

### Q12 — Update 2 后：修订合规报告（supersede 识别）
- **意图**（Update 2 注入后）：外部审计机构发送修订函，撤回第一封邮件中对某条"医生推荐"声明的许可意见，改为标注违规。Agent 须识别该 supersede 关系并更新报告。
- **产物**：`reports/final_compliance_q12.json`（superseded_items: [], active_items: [], update_source: "email_revised_audit_v2"）
- **check 锚点**：update_source 须精确为"email_revised_audit_v2"；"doctor recommended"声明（类比 A3/Health Guidance 中的"cardiologist recommended"隐含声明警告）须被重新标注为 requires_substantiation: true。
- **向量**：V2（Update 反转）、V10（supersede）、V1

### Q13 — 合规培训材料生成
- **意图**：生成面向营销团队的内部培训摘要（一页纸规则卡片）。
- **产物**：`training/ad_compliance_card_q13.md`（含：5条关键规则、禁用词表、披露语言样板）
- **check 锚点**：禁用词须完整包含 A11 全部6个词汇；披露语言样板须包含"Ad:"前置格式；须注明 16 CFR Part 255 生效日期（A1）。
- **向量**：V3（Preference P3/P4 静默考察）、V9

### Q14 — CEO 声明格式最终审定
- **意图**：将所有修订后条款汇总入最终发布声明文件，按 CCO 偏好格式输出。
- **产物**：`final/press_release_final_q14.md`（含 compliance_reviewed_by、review_date、ftc_basis_summary 段落）
- **check 锚点**：所有 Q1-Q12 标注的违规条款不得出现；compliance_reviewed_by 须为 agent 当前会话 ID；review_date 须为场景内置日期（ISO 8601 格式）。
- **向量**：V4（跨轮闭合）、V3（P5 静默考察文件命名规范）

### Q15 — SHA-256 Sign-off Token 生成
- **意图**：对 `final/press_release_final_q14.md` 文件内容运行 `sha256sum`，将结果写入 sign-off 文件。
- **产物**：`final/signoff_q15.txt`（格式：`VERIFIED:<sha256_hex>:<filename>`）
- **check 锚点**：check 脚本本地重算 sha256sum 与 signoff 文件对比；不实际运行 bash 命令无法得到正确 hash（V7）。
- **向量**：V7（Bash-sha256 sign-off token）

### Q16 — 最终 JSON 合规摘要（严格 schema 校验）
- **意图**：将所有轮次结论汇总为机器可读的最终合规摘要 JSON。
- **产物**：`final/compliance_summary_q16.json`
- **check 锚点**：strict JSON schema 校验（V8）：须含 `total_violations_identified`（integer）、`violations_resolved`（integer）、`active_penalty_risk_usd`（number，须为 $51,744 的倍数）、`governing_regulations`（array，须含 "16 CFR Part 255"、"16 CFR Part 465"）、`schema_version: "1.0"`（P1）。
- **向量**：V8、V4、V9

### Q17 — 跨渠道时间线重建
- **意图**：整合所有 session 中与产品发布声明审核相关的决策事件，按时间顺序输出事件日志。
- **产物**：`reports/decision_timeline_q17.json`（events 数组，含 timestamp, channel, actor, decision, supersedes_event_id）
- **check 锚点**：Update 1 的 supersede 事件须在 supersedes_event_id 字段中正确引用被覆盖的 Q1 事件 ID（V10）；Q12 的 Update 2 supersede 亦须体现；时间线须满足 V4 跨轮数据闭合。
- **向量**：V4、V10、V1

---

## 2-4 次 Update 设计

### Update 1（Q7 后、Q8 前，~35KB）
- **触发**：CEO 飞书撤回"clinically demonstrated to support immune function"，称不知名律所建议允许"supports immune health"+"based on our proprietary blend"；Sarah Chen 在 Slack 确认 §465.2 已生效，2009 Guides "results not typical" safe harbor 已废止。
- **文件**：`feishu_ceo_update1.json`（~25KB）+ `slack_legal_update1.json`（~10KB）。
- **supersede**：撤销 Q1 对"clinically demonstrated"的暂时许可，Q8 须重标为违规（V10）。

### Update 2（Q11 后、Q12 前，~53KB，关键双层 supersede）
- **触发**：外部审计机构 Compliance Counsel LLC 发修订函 v2，撤回第一封对"Doctor-formulated"的条件许可，改为要求 "substantial competent scientific evidence"（对照 A4），并新增"biodegradable"须附独立检测报告要求。
- **文件**：`ftc_enforcement_cases_2024.md`（~30KB）+ `email_revised_audit_v2.eml`（~8KB）+ `green_claims_test_reports.md`（~15KB）。
- **supersede（V10双层）**：既撤回第一封外部审计函的条件许可，又间接否定 Update 1 中 CEO 的非正式合规建议（无法律效力，FTC 规则优先）。Agent 须识别两层均被 Update 2 覆盖。

---

## 4-5 条 Preference 规则

| ID | Preference 内容 | 注入方式 | 考察轮次 |
|----|----------------|---------|---------|
| P1 | 所有 JSON 输出文件须含顶层字段 `"schema_version": "1.0"` | 显式（Q1 briefing 文档中明确说明） | Q1, Q5, Q6, Q12, Q16 |
| P2 | 每个合规问题条目须含 `"ftc_citation"` 字段，格式严格为 `"16 CFR §XXX.X"` | 显式（Q2 时 CCO 明确要求） | Q2, Q5, Q8, Q12 |
| P3 | Markdown 报告文件中的标题层级：H1 = 文件名，H2 = 声明类别，H3 = 具体条款 | 经 feedback 注入（Q4 完成后 CCO 反馈） | Q9, Q13, Q14 |
| P4 | 禁用词替换表须包含 `"severity"` 列（取值 high/medium/low），严重程度对应 FTC 执行优先级 | 经 feedback 注入（Q4 完成后） | Q13 静默考察 |
| P5 | 所有 `final/` 目录下的输出文件命名须遵循 `{document_type}_final_YYYYMMDD.{ext}` 格式 | 显式（session_main_brief.md 中规定） | Q14, Q15 |

---

## 难度向量绑定汇总

| 向量 | 绑定轮次 | 说明 |
|------|---------|------|
| V1 多源信息冲突 | Q7, Q12 | Slack Sarah vs Mike 分歧；Update 2 vs Update 1 CEO 声明冲突 |
| V2 动态 Update 反转 | Q8, Q12 | Update 1 撤回"clinically demonstrated"许可；Update 2 撤回"Doctor-formulated"条件许可 |
| V3 隐式 Preference 静默 | Q9, Q13, Q14 | P3 heading 层级、P4 severity 列不再提示 |
| V4 跨轮数值闭合 | Q3→Q8, Q6→Q11, Q14→Q16 | 证据等级/Made in USA 结论/违规条款数须前后一致 |
| V5 失真摘要诱饵 | Q7 | DECOY 摘要罚款写 $45,000（正确 A2=$51,744） |
| V6 废弃副本红鲱鱼 | Q10 | 外部邮件引用 2009 旧版 Guides 已废止的 safe harbor |
| V7 SHA-256 sign-off | Q15 | 须实际运行 sha256sum 命令 |
| V8 schema-by-shape | Q1, Q2, Q5, Q12, Q16 | JSON 字段名/类型/枚举值严格匹配 |
| V9 verbatim 引用 | Q2, Q5, Q9, Q10, Q11 | §255.5/§465.2/§465.7 原文须精确引用 |
| V10 supersede 辨别 | Q8, Q10, Q12, Q17 | Update 1→Q1；Update 2→Update 1 CEO声明+旧审计函（双层） |

## 拆分建议

素材丰富，可拆分：**prd1-core**（健康声明证据实质性）+ **prd1-reviews**（16 CFR Part 465 评论规则 + Part 255 endorsement 披露）。当前单一场景保留，素材支撑充足。
