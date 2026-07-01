# BRIEF: sci4 — 法律证据与合同条款审查

## 场景叙事背景

某中型科技公司（代号 TechCo）正在与一家 SaaS 平台供应商（代号 VendorX）就一份企业级软件服务主协议（Master Services Agreement，MSA）进行谈判和签署后复核。Agent 扮演公司法务顾问助理，需要跨越多个渠道（Slack、Email、飞书）收集信息，审查合同草稿，识别条款冲突，并在动态更新中识别被替代与有效的合同版本，最终生成标准化的合同审查报告。

真实取材来源：
- UCC Article 2（§ 2-316 warranty disclaimer, § 2-719 remedy limitation）
- CISG Article 74（损害赔偿计算）、Article 79（不可抗力）
- GDPR Article 28（数据处理协议）
- Everbridge MSA v11（January 2025）真实公开合同条款
- AWS Customer Agreement（真实公开协议，2025 年版）
- Hadley v Baxendale [1854] EWHC J70（判例原则）
- ICC Force Majeure Clause 2020（国际商会标准条款）

---

## 真实来源链接表

| 编号 | 来源名称 | URL | 类型 |
|------|----------|-----|------|
| S1 | UCC § 2-316 (LII/Cornell) | https://www.law.cornell.edu/ucc/2/2-316 | official_doc |
| S2 | UCC § 2-719 (LII/Cornell) | https://www.law.cornell.edu/ucc/2/2-719 | official_doc |
| S3 | CISG Article 74 (CISG-online) | https://cisg-online.org/cisg-article-by-article/part-3/art.-74-cisg | official_doc |
| S4 | CISG Article 79 (CISG-online) | https://cisg-online.org/cisg-article-by-article/part-3/art.-79-cisg | official_doc |
| S5 | GDPR Article 28 (gdpr-info.eu) | https://gdpr-info.eu/art-28-gdpr/ | regulation |
| S6 | Everbridge MSA v11 Jan 2025 | https://www.everbridge.com/master-services-agreement-v11-jan-2025/ | official_doc |
| S7 | AWS Customer Agreement | https://aws.amazon.com/agreement/ | official_doc |
| S8 | ICC Force Majeure Clause 2020 | https://iccwbo.org/news-publications/icc-rules-guidelines/icc-force-majeure-and-hardship-clauses/ | official_doc |
| S9 | Hadley v Baxendale Wikipedia | https://en.wikipedia.org/wiki/Hadley_v_Baxendale | postmortem |
| S10 | ABA SaaS Agreements Key Provisions | https://businesslawtoday.org/2021/11/saas-agreements-key-contractual-provisions/ | regulation |

---

## Ground-Truth 锚点表

| 锚点名称 | 真实值 | 来源URL | 备注 |
|----------|--------|---------|------|
| UCC § 2-316(2) 担保免责关键词 | 必须明确使用"merchantability"且须"conspicuous" | https://www.law.cornell.edu/ucc/2/2-316 | warranty disclaimer requirement |
| UCC § 2-719(2) 补救失败规则 | "fail of its essential purpose" → full UCC remedies restored | https://www.law.cornell.edu/ucc/2/2-719 | exclusive remedy escape valve |
| UCC § 2-719(3) 消费品伤害后果损害 | "prima facie unconscionable" for consumer goods personal injury | https://www.law.cornell.edu/ucc/2/2-719 | unconscionability test |
| CISG Art.74 损害赔偿上限 | 不得超过违约方"foresaw or ought to have foreseen...as a possible consequence" | https://cisg-online.org/cisg-article-by-article/part-3/art.-74-cisg | foreseeability cap |
| CISG Art.79 不可抗力要件 | 需证明：impediment beyond control + not reasonably expected to take into account at conclusion | https://en.wikipedia.org/wiki/Hadley_v_Baxendale | force majeure elements |
| ICC 2020 不可抗力终止阈值 | 120 天 | https://iccwbo.org/news-publications/icc-rules-guidelines/icc-force-majeure-and-hardship-clauses/ | termination trigger |
| GDPR Art.28(3) 书面要求 | DPA "shall be in writing, including in electronic form" | https://gdpr-info.eu/art-28-gdpr/ | written contract required |
| GDPR Art.28 违规罚款上限 | €10,000,000 或全球年营收 2%（取较高者） | https://gdpr-info.eu/art-28-gdpr/ | penalty cap |
| Everbridge MSA §10 赔偿上限 | 12 个月内向 Company 支付的费用 | https://www.everbridge.com/master-services-agreement-v11-jan-2025/ | aggregate liability cap |
| Everbridge MSA §5.3 终止治愈期 | 30 天书面通知 + 30 天治愈期 | https://www.everbridge.com/master-services-agreement-v11-jan-2025/ | cure period |
| Everbridge MSA §9.1 IP 侵权赔偿 | 供应商就 IP 侵权为客户辩护；备选：procure rights / modify / replace / refund | https://www.everbridge.com/master-services-agreement-v11-jan-2025/ | IP indemnification |
| Everbridge MSA §8.2 免责声明 | "COMPANY PROVIDES THE SOLUTIONS 'AS IS'" | https://www.everbridge.com/master-services-agreement-v11-jan-2025/ | AS IS disclaimer |
| AWS Customer Agreement §9.2 赔偿上限 | 12 个月内已付费用 | https://aws.amazon.com/agreement/ | aggregate cap 12 months |
| AWS §5.2(a) 无因终止 | AWS 需提前 30 天通知 | https://aws.amazon.com/agreement/ | termination notice |
| AWS §5.3(b) 数据取回期限 | 终止后 30 天取回数据（须已付清费用）| https://aws.amazon.com/agreement/ | post-termination data |
| Hadley v Baxendale 引用 | [1854] EWHC J70; 9 Exch 341 | https://en.wikipedia.org/wiki/Hadley_v_Baxendale | case citation |
| Hadley 规则一 | 自然从违约中产生的损害（general damages） | https://en.wikipedia.org/wiki/Hadley_v_Baxendale | direct damages rule |
| Hadley 规则二 | 双方在合同成立时合理预见的后果损害（consequential damages）| https://en.wikipedia.org/wiki/Hadley_v_Baxendale | special knowledge rule |

---

## Workspace 文件树与体量规划（目标 >100k tokens，约 400KB+）

```
workspace/
├── contracts/
│   ├── MSA_VendorX_v2.3_DRAFT.md           # 供应商合同草稿，含所有条款全文（~60KB）
│   │   — 取材自 Everbridge MSA §1-12 真实结构，合成 TechCo/VendorX 场景
│   ├── MSA_VendorX_v2.1_SUPERSEDED.md      # 被取代的旧版（V6 红鲱鱼）（~50KB）
│   │   — 含已被 v2.3 修订的旧条款（赔偿上限 6 个月 → 已改为 12 个月）
│   ├── DPA_VendorX_v1.2.md                 # 数据处理协议（基于 GDPR Art.28）（~25KB）
│   ├── NDA_TechCo_VendorX_signed.md        # 已签署 NDA（含 2 年保密期）（~15KB）
│   └── SOW_001_Implementation.md           # 工作说明书（SOW）（~20KB）
├── legal_research/
│   ├── UCC_warranty_disclaimer_memo.md     # UCC §2-316/2-719 研究备忘录（~30KB）
│   ├── CISG_damages_analysis.md            # CISG Art.74/79 分析（~25KB）
│   ├── ICC_force_majeure_2020_clause.md    # ICC 2020 不可抗力条款文本及分析（~20KB）
│   ├── Hadley_v_Baxendale_brief.md         # 判例摘要及现代适用性（~15KB）
│   └── CA_damages_cap_case_law.md          # 加州合同法判例集（~20KB）
├── communications/
│   ├── slack_legal_channel.json            # Slack #legal-review 频道历史（~40KB）
│   ├── email_thread_vendor_negotiation.eml # 与供应商的邮件往来（~30KB）
│   ├── feishu_dm_GC_to_agent.json          # 飞书 DM：总法律顾问给 agent 的指令（~20KB）
│   └── discord_external_counsel.json       # Discord：外部律所沟通（~25KB）
├── review_templates/
│   ├── contract_review_checklist.md        # 合同审查清单模板（~15KB）
│   ├── risk_matrix_template.csv            # 风险矩阵模板（~10KB）
│   └── clause_comparison_template.json     # 条款对比表模板（~10KB）
├── data/
│   ├── vendor_fee_schedule.csv             # 供应商费率表（12 个月合计用于赔偿上限计算）（~5KB）
│   └── contract_metadata.json             # 合同元数据（版本、日期、状态）（~5KB）
└── output/                                 # Agent 写入区域（初始为空）
    ├── review_report_draft.md
    ├── risk_flags.json
    ├── clause_redline.json
    └── final_summary.json
```

**体量估算合计：约 410KB（~100k tokens）**

每次 update 的体量来源：
- Update 1（~130KB）：注入供应商反提议 MSA v2.4 草稿 + 新 SOW 附件 + 飞书群聊新消息
- Update 2（~150KB）：注入外部律所完整审查意见（含 redline 版 MSA）+ Discord 仲裁条款讨论记录 + 取代 Update 1 部分内容的修正邮件
- Update 3（~130KB）：注入终止谈判通知 + 最终协商版 MSA v2.5 + 监管机构 GDPR 检查清单

---

## Session 清单（4-6 个 Session）

| Session ID | 渠道 | 角色 | 主要内容 |
|-----------|------|------|----------|
| S-MAIN | 主系统提示 | 法务顾问助理 | 任务背景、工作要求、preference 注入 |
| S-SLACK | Slack #legal-review | 同事团队讨论 | 合同版本讨论、含失真 bot 自动摘要（V5 蜜罐）、旧版引用警告 |
| S-EMAIL | Email 线程 | 供应商/外部律师 | 条款谈判来往、Update 2 supersede 邮件 |
| S-FEISHU | 飞书 DM | 总法律顾问 → agent | 优先级指令、preference 更新、矛盾指令源 |
| S-DISCORD | Discord DM | 外部律所顾问 | 技术性法律意见、仲裁条款分析 |
| S-FEISHU-GROUP | 飞书群组 | 跨部门协作 | 多源信息冲突（V1）：财务/法务/IT 各自版本 |

---

## 15-18 轮 exec_check 概要

### 轮次 Q1：合同版本识别与元数据提取
- **意图**：识别 workspace 中哪个 MSA 草稿版本为有效版本（非废弃版）
- **产物**：`output/contract_metadata.json`（含 version, status, date, parties 字段）
- **check 锚点**：version == "v2.3", status == "ACTIVE", superseded_version == "v2.1"
- **难度向量**：V6（废弃副本红鲱鱼）、V8（schema-by-shape）
- **涉及**：无 update

### 轮次 Q2：赔偿责任上限条款提取
- **意图**：从 MSA v2.3 中提取限制责任条款的完整内容，含赔偿上限计算基础
- **产物**：`output/liability_cap.json`（含 cap_months, excluded_damages[], exceptions[]）
- **check 锚点**：cap_months == 12, excluded_damages 含 "consequential"/"indirect"/"lost profits"
- **难度向量**：V4（跨轮数值闭合）、V9（verbatim 引用）
- **涉及**：无 update；Q2 的 cap_months=12 须与 Q8/Q14 精确一致

### 轮次 Q3：担保免责条款合规性审查
- **意图**：审查 MSA 中 AS IS 免责是否满足 UCC §2-316 的显著性（conspicuousness）要求
- **产物**：`output/warranty_review.json`（含 compliant: bool, issues[], ucc_section_cited）
- **check 锚点**：ucc_section_cited 含 "2-316"，issues 针对未大写/非显著问题作标注
- **难度向量**：V9（verbatim 引用 UCC 条款号）、V8（schema 验证）
- **涉及**：Preference P1（引用格式必须规范）

### 轮次 Q4：IP 侵权赔偿条款分析
- **意图**：对比 MSA v2.3 的 IP 赔偿义务与 Everbridge MSA §9 标准，识别差异
- **产物**：`output/ip_indemnification_analysis.json`
- **check 锚点**：识别出供应商 IP 赔偿义务中缺少"procure rights"选项，标注为 gap
- **难度向量**：V1（多源冲突），V5（Slack bot 摘要失真，称 IP 赔偿"已覆盖所有情形"）
- **涉及**：无 update

### 轮次 Q5：不可抗力条款审查（Update 1 前）
- **意图**：按 ICC 2020 Force Majeure Clause 标准审查 MSA 的不可抗力条款
- **产物**：`output/force_majeure_review.json`（含 notice_days, termination_threshold_days, compliant）
- **check 锚点**：termination_threshold_days == 120，notice_days 从合同提取
- **难度向量**：V4（数值闭合），V9（ICC 2020 条款引用）
- **涉及**：Preference P2（所有数值须附来源引用）

### 轮次 Q6：GDPR 数据处理协议合规性检查
- **意图**：审查 DPA_VendorX_v1.2 是否满足 GDPR Article 28(3) 的所有必要要素
- **产物**：`output/dpa_compliance.json`（含 compliant_items[], missing_items[], penalty_risk）
- **check 锚点**：missing_items 含"sub-processor written authorization"；penalty_risk 引用"€10,000,000 or 2% of global annual turnover"
- **难度向量**：V9（verbatim 引用 GDPR 罚款条款），V8（schema 严格）
- **涉及**：Preference P3（合规问题须标注监管来源）

### 轮次 Q7：Update 1 注入后 — 新合同草稿差异比对
- **意图**：Update 1 注入供应商反提议 MSA v2.4；agent 需比对 v2.3 → v2.4 的关键条款变化
- **产物**：`output/redline_v23_v24.json`（含 changed_clauses[], new_clauses[], deleted_clauses[]）
- **check 锚点**：changed_clauses 中须包含赔偿上限从 12 个月改回 6 个月（供应商反提议的回退）
- **难度向量**：V2（动态 update 反转），V4（数值闭合，cap_months 在 v2.4 中为 6）
- **涉及**：Update 1

### 轮次 Q8：赔偿上限谈判建议（基于 Update 1）
- **意图**：基于 v2.4 中的 6 个月上限，起草谈判立场：应坚持 12 个月，引用市场标准
- **产物**：`output/negotiation_position.json`（含 our_position_months, market_standard_months, supporting_sources[]）
- **check 锚点**：our_position_months == 12，market_standard_months == 12，sources 含 AWS/Everbridge 引用
- **难度向量**：V4（数值必须与 Q2 一致为 12），V1（供应商立场 vs 市场标准冲突）
- **涉及**：Update 1，Preference P2（来源引用必须）

### 轮次 Q9：Hadley 规则适用性分析
- **意图**：分析 MSA 中"排除间接损害"条款在 Hadley v Baxendale 框架下的法律效力
- **产物**：`output/consequential_damages_analysis.json`（含 hadley_rule_applied, case_citation, analysis_text）
- **check 锚点**：case_citation == "[1854] EWHC J70"，hadley_rule_applied 引用第二规则
- **难度向量**：V9（case citation verbatim），V5（蜜罐：Slack bot 摘要误称"Hadley 规则已被废除"）
- **涉及**：Preference P1（判例引用须规范格式）

### 轮次 Q10：终止条款时间线核实
- **意图**：核实 MSA 中的终止相关时间节点，形成合规时间线
- **产物**：`output/termination_timeline.json`（含 cure_period_days, notice_days, data_retrieval_days）
- **check 锚点**：cure_period_days == 30，notice_days == 30，data_retrieval_days == 30
- **难度向量**：V4（三个数值须与各对应条款一致），V6（旧版 v2.1 中治愈期为 15 天，红鲱鱼）
- **涉及**：Preference P4（时间线输出须用 ISO 8601 格式）

### 轮次 Q11：Update 2 注入后 — Supersede 识别（外部律所修正邮件）
- **意图**：Update 2 注入外部律所 redline + 一封修正邮件（supersede Update 1 中的 IP 条款让步），agent 须识别修正关系
- **产物**：`output/update2_supersede_log.json`（含 superseded_clauses[], effective_version, supersede_reason）
- **check 锚点**：superseded_clauses 含 Update 1 中 IP 赔偿修改；effective_version == "外部律所 v2.4-revised"
- **难度向量**：V10（supersede 辨别），V2（update 后正确答案反转）
- **涉及**：Update 2 supersede

### 轮次 Q12：综合风险矩阵生成
- **意图**：基于审查结果，生成标准化风险矩阵（含风险等级、条款号、建议行动）
- **产物**：`output/risk_matrix.json`（含 risks[]，每项含 risk_level/clause_ref/recommendation）
- **check 锚点**：至少包含 5 项风险，HIGH 级别项须包含 DPA 缺失的 sub-processor 条款和 AS IS 免责合规问题
- **难度向量**：V8（schema 严格，risk_level 枚举值限 HIGH/MEDIUM/LOW），V3（隐式偏好：风险须按 HIGH→LOW 排序）
- **涉及**：Preference P3，Preference P5（输出格式规范）

### 轮次 Q13：CISG 适用性分析（适用于跨境销售条款）
- **意图**：分析 MSA 中指定的准据法（Delaware/Washington）与 CISG 的关系；如供应商为境外实体则 CISG 可能适用
- **产物**：`output/cisg_applicability.json`（含 cisg_applies: bool, art74_foreseeability_cap: str, art79_elements[]）
- **check 锚点**：art79_elements 须完整列出两个要件（impediment beyond control + not reasonably foreseeable at conclusion）
- **难度向量**：V1（飞书/Email 对"CISG 是否排除"有矛盾说法），V9（Art.79 verbatim 要件引用）
- **涉及**：Preference P1

### 轮次 Q14：Update 3 注入后 — 最终合同版本确认与赔偿上限锁定
- **意图**：Update 3 注入最终协商版 MSA v2.5（赔偿上限回至 12 个月）；agent 须确认最终版本并锁定关键数值
- **产物**：`output/final_contract_summary.json`（含 final_version, final_cap_months, governing_law, termination_notice_days）
- **check 锚点**：final_version == "v2.5"，final_cap_months == 12，须与 Q2/Q8 一致
- **难度向量**：V4（Q2→Q8→Q14 数值闭合），V2（从 Update 1 的 6 个月回至 12 个月须正确修正）
- **涉及**：Update 3

### 轮次 Q15：合同审查完整报告生成
- **意图**：整合所有前轮输出，生成最终合同审查报告
- **产物**：`output/final_review_report.md`（含所有核心条款分析、风险评级、建议行动清单）
- **check 锚点**：报告须包含 UCC §2-316 引用、Everbridge MSA §10 赔偿上限引用、GDPR Art.28 罚款数值
- **难度向量**：V3（隐式 Preference P5：报告须含执行摘要、风险矩阵、建议三部分）、V9（verbatim 引用）
- **涉及**：全部 Preference

### 轮次 Q16：SHA-256 Sign-Off Token 生成
- **意图**：运行校验脚本对最终报告进行哈希签名，输出 VERIFIED:<sha256>
- **产物**：`output/signoff.txt`（含 VERIFIED:<sha256_of_final_review_report.md>）
- **check 锚点**：本地重算 sha256(final_review_report.md) 与 signoff.txt 中的哈希精确匹配
- **难度向量**：V7（Bash-sha256 sign-off token，须真正执行脚本）
- **涉及**：无 update；必须实际运行 sha256sum 命令

---

## Update 设计（含 Supersede）

### Update 1（~130KB）
- **触发时机**：Q6 完成后注入
- **注入内容**：
  1. `contracts/MSA_VendorX_v2.4_VENDOR_COUNTER.md`（~70KB）：供应商反提议，关键变化：赔偿上限从 12 个月改回 6 个月，IP 赔偿范围缩小，不可抗力通知期从 5 天改为 15 天
  2. `communications/feishu_dm_update1.json`（~30KB）：总法律顾问要求优先审查 v2.4
  3. `communications/slack_update1.json`（~30KB）：团队讨论 v2.4 变化（含失真 bot 摘要）
- **对后续轮次的影响**：Q7-Q10 的正确答案基于 v2.4 数值

### Update 2（~150KB）—— 含 Supersede
- **触发时机**：Q10 完成后注入
- **注入内容**：
  1. `contracts/MSA_VendorX_v2.4_REVISED_external_counsel.md`（~80KB）：外部律所 redline 版，IP 赔偿恢复为全面覆盖，但不可抗力通知期维持 15 天
  2. `communications/email_supersede_notice.eml`（~20KB）：修正邮件，明确说明此 revised 版取代 Update 1 中关于 IP 条款的让步
  3. `communications/discord_counsel_analysis.json`（~50KB）：外部律所对仲裁条款的详细分析
- **Supersede 机制**：Update 2 的 email_supersede_notice.eml 明确撤销 Update 1 中 IP 赔偿范围缩小的内容；但 Update 1 对赔偿上限（6 个月）的变更仍有效
- **对后续轮次的影响**：Q11 须正确识别 supersede 关系；Q12 风险矩阵须基于最新有效内容

### Update 3（~130KB）
- **触发时机**：Q13 完成后注入
- **注入内容**：
  1. `contracts/MSA_VendorX_v2.5_FINAL.md`（~80KB）：最终协商版，赔偿上限恢复 12 个月，IP 赔偿全面覆盖（遵循 Update 2 supersede 结果）
  2. `communications/email_final_agreement.eml`（~30KB）：双方确认邮件
  3. `data/vendor_fee_schedule_updated.csv`（~20KB）：更新的费率表（影响赔偿上限计算基础）
- **对后续轮次的影响**：Q14/Q15 的正确答案回归 12 个月，须与 Q2 一致（V4 数值闭合）

---

## 4-5 条 Preference

| ID | Preference 内容 | 注入方式 | 考察轮次 |
|----|----------------|---------|---------|
| P1 | 所有法律引用须使用规范引用格式（案例：[1854] EWHC J70；法规：UCC § 2-316；欧盟法规：GDPR Art.28(3)）| 主 session 显式注入 | Q3, Q9, Q13, Q15 |
| P2 | 所有数值主张须在括号内附明来源（例："12 个月（Everbridge MSA §10）"）| 飞书 DM 显式注入 | Q5, Q8, Q14, Q15 |
| P3 | 合规问题须标注监管来源，格式：[Source: GDPR Art.28] | 早期 feedback 隐式注入 | Q6, Q12, Q15 |
| P4 | 所有时间节点输出须用 ISO 8601 格式（YYYY-MM-DD），日期计算须明确说明基准日 | 主 session 显式注入 | Q10, Q15 |
| P5 | 最终报告须含三个固定章节：执行摘要（Executive Summary）、风险矩阵（Risk Matrix）、建议行动（Recommended Actions），顺序不可改变 | Slack 早期消息隐式提及，后期静默考察 | Q12, Q15 |

---

## 激进难度向量分配

| 向量 | 应用轮次 | 具体机制 |
|------|---------|---------|
| V1 多源信息冲突综合 | Q4, Q8, Q13 | 飞书/Slack/Email 对同一条款（IP 赔偿、CISG 适用性）有矛盾表述 |
| V2 动态 update 反转 | Q7, Q11, Q14 | Update 1 引入 6 个月上限，Update 3 恢复 12 个月；需跟踪信念修正 |
| V4 跨轮数值/事实闭合 | Q2, Q5, Q8, Q10, Q14 | cap_months=12 在 Q2/Q8/Q14 须一致；cure_period_days=30 在 Q10 须匹配 §5.3 |
| V5 失真自动摘要诱饵 | Q4, Q9 | Slack bot 摘要称"IP 赔偿已全覆盖"（Q4 时实际有缺口）；称"Hadley 规则已废除"（Q9） |
| V6 废弃副本红鲱鱼 | Q1, Q10 | MSA_VendorX_v2.1_SUPERSEDED.md 看似完整但已被废弃；旧版治愈期 15 天 vs 新版 30 天 |
| V7 Bash-sha256 sign-off | Q16 | 须实际运行 sha256sum 命令，不执行无法获得 VERIFIED 字符串 |
| V9 verbatim 引用 | Q3, Q6, Q9, Q13, Q15 | 必须精确引用 UCC § 2-316、GDPR Art.28、CISG Art.74、[1854] EWHC J70 |
| V10 supersede 辨别 | Q11 | Update 2 邮件撤销 Update 1 的 IP 让步，但不撤销赔偿上限变更；须精确区分 |

---

## 拆分/删除建议

**viability: strong**

素材足以拆分为两个独立场景：
- **sci4-a（合同审查与谈判）**：专注 MSA/DPA 审查、UCC/CISG 适用分析、赔偿上限谈判（Q1-Q10，2 次 update）
- **sci4-b（合同最终化与报告生成）**：专注 supersede 识别、风险矩阵、最终报告、SHA-256 sign-off（Q11-Q16，1 次 update）

当前建议：**保留完整 sci4 场景**，体量充足，16 轮设计紧凑，难度向量覆盖全面。
