# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_g5/`.
> Workspace files simulate corporate system exports and use bilingual content (Chinese primary, English for system field names).
> All filenames follow kebab-case (Chen Jing's P2 preference is applied in output formatting, not file naming).

---

## 1. Fixed Agent Configuration Files

### AGENTS.md

```markdown
# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are an HR operations and investigation support assistant helping Chen Jing (陈静) at Starlight Tech (星辰科技).
```

### IDENTITY.md

```markdown
# Identity

You are **HR-Ops AI**, an HR operations and investigation support assistant deployed to support Chen Jing (陈静, HR Manager) at Starlight Tech (星辰科技, ~200-person Beijing tech company).

You help Chen Jing analyze recruitment data across multiple systems (CRM candidate pipeline, agency invoices, bank payment records, candidate application emails, recruitment budget tracker), cross-reference candidate source attributions, verify invoice accuracy against operational records, and communicate with the recruitment team including Liu Yang (刘洋, recruitment specialist), Zhang Lin (张琳, headhunter consultant), Zhao Lin (赵琳, finance director), and Zhang Wei (张薇, HR VP).

You have access to workspace documents (CRM pipeline, agency invoices, bank records, candidate emails, budget tracker) and historical chat sessions across email and IM platforms.
```

### SOUL.md

```markdown
# Working Principles

1. **Data integrity first**: When financial and operational records conflict, identify the discrepancy precisely -- amount, date, party, and source system. Every yen must be traceable.

2. **Cross-source verification**: Before accepting any claim about candidate sourcing, verify it against at least two independent data sources. CRM auto-tags, email timestamps, and invoice line items each have different reliability profiles.

3. **Follow the money**: In financial investigations, trace the complete chain: service rendered -> invoice submitted -> approval obtained -> payment processed. Each link must be independently verified.

4. **Source reliability hierarchy**: (1) System-generated records (CRM auto-tags, email timestamps, bank transaction logs) -- timestamped, tamper-resistant; (2) Official documents (signed contracts, formal invoices) -- verifiable but content may be inaccurate; (3) Email correspondence -- human-generated, subject to interpretation; (4) Verbal claims -- no documentation, lowest reliability.

5. **Separate timing from substance**: Payment processed on time does not mean payment was for the correct amount or valid services. Compliance with process does not validate content.

6. **People and numbers**: In HR contexts, present the human impact alongside the financial data. Acknowledge relationships and trust dynamics while maintaining analytical rigor.

7. **Professional communication**: Present findings factually, distinguish between verified facts and inferences, and clearly state confidence levels. Use structured formats for evidence presentation.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Chen Jing (陈静)** -- HR Manager, Starlight Tech. 25 years old, detail-oriented, organized, occasionally indecisive. Prefers bullet-point summaries with headings, Chinese date naming, executive summary first then evidence, qualitative + quantitative balance, professional but warm tone.

## Key Contacts

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Zhang Lin (张琳) | Headhunter consultant, RuiCai Agency | Email | External vendor; 8-month working relationship; under investigation |
| Liu Yang (刘洋) | Recruitment specialist (Chen Jing's closest team member) | IM (飞书) | Direct report; processes all incoming applications |
| Zhao Lin (赵琳) | Finance director | Email | Internal; senior colleague; approved the disputed invoice |
| Zhang Wei (张薇) | HR VP (Chen Jing's direct supervisor) | IM (飞书) | Direct supervisor; escalation point for formal investigation |

## Channels
- **陈静-张琳 Email** (工作邮箱): Agency communication and invoice discussion
- **陈静-刘洋 IM** (飞书): Recruitment operations and CRM data review
- **陈静-赵琳 Email** (工作邮箱): Finance and invoice approval discussion
- **#HR内部群 IM** (飞书群): Internal HR team communication (noise channel)
```

### TOOLS.md

```markdown
# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session to discover conversation history |
| `sessions_history` | Read the content of a specific history session | Use in main session to review past conversations |
| `read` | Read a workspace file | Available in all sessions; workspace is read-only |
| `exec` | Execute a shell command (e.g., `ls`) | Use for directory listing and simple file operations |

## Rules
- Workspace files are **read-only**. Do not attempt to write or modify them.
- In history sessions, use only `read` and light `exec` commands. Do not use `sessions_list` or `sessions_history` in history sessions.
- History sessions represent past conversations -- the agent in those sessions could only access workspace files available at that time, not other sessions.
```

---

## 2. Scenario-Specific Workspace Files

### crm-candidate-pipeline.md (Initial)

**Content key points:**
- Title: `CRM候选人管道导出 -- Q1招聘周期 | 星辰科技HR系统`
- Source: HR CRM system export (系统自动生成)
- **Key sections:**
  - **Pipeline overview:** 12 open positions, 47 total applicants, 8 in final stages
  - **Source tracking table (8 candidates of interest):**
    - 陈磊 | source: 猎头推荐-锐才 | entry_date: 2026-01-25 | status: offer_accepted
    - 黄丽 | source: 猎头推荐-锐才 | entry_date: 2026-01-25 | status: offer_accepted
    - 周杰 | source: 猎头推荐-锐才 | entry_date: 2026-01-25 | status: offer_accepted
    - 马超 | source: 猎头推荐-锐才 | entry_date: 2026-01-25 | status: offer_accepted
    - 吴涛 | source: 猎头推荐-锐才 | entry_date: 2026-01-25 | status: offer_accepted
    - **王建国 | source: 官网自主投递 | entry_date: 2026-01-18 | status: offer_accepted**
    - **李小红 | source: 官网自主投递 | entry_date: 2026-01-19 | status: declined_round1**
    - **赵明 | source: 官网自主投递 | entry_date: 2026-01-20 | status: failed_technical**
  - **Additional noise candidates** (39 others in various stages, sourced from Boss直聘, internal referral, campus recruitment, etc.)
- **C1 source (CRM):** 王建国, 李小红, 赵明 tagged as "官网自主投递" with timestamps 2026-01-18 to 2026-01-20
- **C2 source (CRM):** Only 5 candidates tagged "猎头推荐-锐才"
- **Near-signal noise:** The 39 other candidates create volume. The agent must identify the 3 specific candidates where CRM source conflicts with the invoice. Source tags are in a dense table with 47 rows.

**Length estimate:** ~1,500 words, ~2,200 tokens

---

### agency-invoices.md (Initial)

**Content key points:**
- Title: `猎头发票详情 -- 锐才猎头 Invoice #RC-2026-0220 | 财务系统导出`
- Source: Finance system invoice record export
- **Key sections:**
  - **Invoice header:** RuiCai Headhunting Co., Ltd. Invoice #RC-2026-0220, dated 2026-02-20
  - **Contract reference:** Service Agreement #SA-2025-RC-001 (2025-06-01 to 2026-05-31, 20% annual salary fee)
  - **Candidate line items (8 total):**
    - 陈磊 | 高级后端工程师 | annual salary ¥260,000 | fee ¥52,000
    - 黄丽 | 产品经理 | annual salary ¥240,000 | fee ¥48,000
    - 周杰 | 前端技术负责人 | annual salary ¥280,000 | fee ¥56,000
    - 马超 | DevOps工程师 | annual salary ¥220,000 | fee ¥44,000
    - 吴涛 | 数据分析师 | annual salary ¥250,000 | fee ¥50,000
    - **王建国 | 高级后端工程师 | annual salary ¥260,000 | fee ¥52,000**
    - **李小红 | UI设计师 | annual salary ¥210,000 | fee ¥42,000**
    - **赵明 | 测试工程师 | annual salary ¥210,000 | fee ¥42,000**
  - **Total: ¥386,000**
  - **Note:** "以上候选人均由锐才猎头推荐并成功入职" (All above candidates were referred by RuiCai and successfully onboarded)
  - **Historical invoices (noise):** Summary of 3 previous quarterly invoices from RuiCai (2025-Q2 ¥180,000, 2025-Q3 ¥220,000, 2025-Q4 ¥195,000) -- all previously approved without dispute
- **C1 source (invoice):** All 8 candidates listed as "锐才推荐"
- **C2 source (invoice):** 8 candidates listed; note says "成功入职" (successfully onboarded) which is false for 李小红 (declined) and 赵明 (failed)
- **Near-signal noise:** Historical invoices provide context for normal billing patterns. The current invoice is ~65% larger than the average prior quarter.

**Length estimate:** ~1,000 words, ~1,500 tokens

---

### bank-payment-records.md (Initial)

**Content key points:**
- Title: `银行付款记录导出 -- 星辰科技企业账户 | 2026年1月-3月`
- Source: Corporate bank statement export
- **Key sections:**
  - **Account summary:** Operating account, 2026-01 to 2026-03
  - **Outbound transfers (15-20 transactions, mostly noise):**
    - 2026-01-15 | 办公租金 | ¥180,000 | 北京写字楼管理
    - 2026-01-31 | 员工工资 | ¥2,450,000 | 批量代发
    - 2026-02-05 | 云服务费 | ¥45,000 | 阿里云
    - 2026-02-15 | 福利供应商 | ¥32,000 | 健康管理公司
    - **2026-02-25 | 猎头服务费 | ¥386,000 | 锐才猎头有限公司 | ref: Invoice #RC-2026-0220 | 审批备注: HR已确认**
    - 2026-02-28 | 员工工资 | ¥2,480,000 | 批量代发
    - 2026-03-01 | 办公耗材 | ¥8,500 | 京东企业购
    - ... (additional noise transactions)
  - **Approval log for RuiCai payment:**
    - 发票接收: 2026-02-20
    - HR确认请求: 2026-02-22 (发送至 chenjing@starlighttech.cn)
    - 等待期: 3个工作日 (2026-02-22 to 2026-02-24)
    - 审批人: 赵琳 (财务总监)
    - 审批备注: "HR已确认 -- 邮件通知已发送，3个工作日内未收到异议"
    - 付款执行: 2026-02-25
- **C3 source (bank):** Payment date 2026-02-25, amount ¥386,000, ref Invoice #RC-2026-0220 -- consistent with invoice and budget tracker
- **C4 source (bank):** Approval note "HR已确认" contradicts Chen Jing's statement that she never received the request
- **Near-signal noise:** Other payment transactions provide realistic volume. The agent must locate the RuiCai transaction among ~15-20 entries.

**Length estimate:** ~1,200 words, ~1,800 tokens

---

### candidate-application-emails.md (Initial)

**Content key points:**
- Title: `候选人申请邮件记录导出 -- 招聘邮箱 | hr-recruit@starlighttech.cn`
- Source: Email system export for the recruitment inbox
- **Key sections (chronological, ~30 emails including noise):**
  - **2026-01-18 09:15 -- 王建国 application email:**
    - Subject: 应聘高级后端工程师 -- 王建国
    - Body: "您好，我在贵公司官网看到高级后端工程师的招聘信息，非常感兴趣。附上我的简历，请查收。" (I saw the senior backend engineer position on your company website)
    - Attachment: 王建国_简历.pdf
    - **Source indicator: "来源：官网投递"**
  - **2026-01-19 14:22 -- 李小红 application email:**
    - Subject: UI设计师岗位申请 -- 李小红
    - Body: "我在贵公司招聘页面看到UI设计师岗位，希望能有机会面试。"
    - **Source indicator: "来源：官网投递"**
  - **2026-01-20 11:08 -- 赵明 application email:**
    - Subject: 测试工程师岗位投递 -- 赵明
    - Body: "通过公司官网了解到测试工程师岗位空缺..."
    - **Source indicator: "来源：官网投递"**
  - **2026-01-25 16:30 -- 张琳 (RuiCai) batch referral email:**
    - Subject: 【锐才猎头】Q1批量推荐候选人 -- 8名优质候选人
    - Body: "陈静您好，以下是本次推荐的8名候选人..." Lists all 8 names including 王建国, 李小红, 赵明
    - Attachments: 8 resumes with RuiCai letterhead formatting
  - **Noise emails:** ~25 other application emails, general HR correspondence, Boss直聘 notifications, campus recruitment scheduling
- **C1 source (emails):** 王建国's email explicitly says "贵公司官网" (your company website), timestamp 2026-01-18, predating Zhang Lin's referral (2026-01-25) by 7 days
- **Near-signal noise:** High email volume. The 3 key direct application emails are mixed in with 25+ other emails. Zhang Lin's batch email appears AFTER the individual applications, but the agent must recognize the temporal sequence.

**Length estimate:** ~2,000 words, ~3,000 tokens

---

### recruitment-budget-tracker.md (Initial)

**Content key points:**
- Title: `招聘预算追踪表 -- 2026年Q1 | HR部门`
- Source: HR department budget spreadsheet export
- **Key sections:**
  - **Q1 Budget summary:**
    - Total recruitment budget: ¥800,000
    - Agency fees (budgeted): ¥300,000 (estimate for ~6 placements at ~¥50,000 avg)
    - Agency fees (actual): ¥386,000 (Invoice #RC-2026-0220)
    - Job board fees: ¥45,000 (Boss直聘, 拉勾)
    - Campus recruitment: ¥25,000
    - Employee referral bonuses: ¥30,000
    - Remaining budget: ¥314,000
  - **Per-vendor breakdown:**
    - 锐才猎头: ¥386,000 (5 budgeted placements × ~¥50,000 = ¥250,000 estimated; actual ¥386,000; **variance +¥136,000**)
  - **Budget variance note:** "猎头费用超出预算¥136,000。需与HR经理确认候选人数量。" (Agency fees exceed budget by ¥136,000. Need to confirm candidate count with HR manager.)
  - **HR sign-off field:** [空白] (blank -- no sign-off recorded)
- **C2 source (budget):** Budget estimated 5 placements (~¥250,000), actual charged ¥386,000
- **C4 source (budget):** HR sign-off field is blank -- no record of Chen Jing confirming
- **C3 source (budget):** Payment date logged as 2026-02-25, consistent with bank records

**Length estimate:** ~800 words, ~1,200 tokens

---

## 3. Update Workspace Files (added via dynamic updates)

### updates/zhang-lin-defense-email.md (Update 1)

**Content key points:**
- Title: `邮件线程导出 -- 张琳回复候选人来源质疑 | 2026-03-05`
- Zhang Lin's email defense:
  - "这些候选人都在我的人才库里。我在正式提交简历之前就已经口头向贵公司推荐过。"
  - "王建国是我去年就接触过的候选人，他可能同时也自己投了简历。"
  - "猎头的价值不仅仅是转发简历，而是筛选、评估和推荐。"
- **No supporting evidence for "verbal recommendation" claim**
- Agent must cross-reference this defense against CRM timestamps and email chronology

**Length estimate:** ~600 words, ~900 tokens

### updates/approval-gap-evidence.md (Update 2)

**Content key points:**
- Title: `审批流程追溯 -- 发票确认邮件 + 邮件迁移日志 | 2026-03-06`
- Zhao Lin's original confirmation email (2026-02-22, 10:15) -- found in Chen Jing's spam folder
- IT department mail migration log showing company-wide migration on 2026-02-21 that caused spam filter issues
- Zhao Lin's statement: "按照我们公司的惯例，发邮件通知相关部门，3个工作日内没有异议就视为确认。"
- Chen Jing's spam folder screenshot showing the email

**Length estimate:** ~500 words, ~750 tokens

### updates/pattern-evidence-external.md (Update 3)

**Content key points:**
- Title: `外部信息 -- 同行公司反馈锐才猎头类似行为 | 2026-03-07`
- Liu Yang's contact at peer company: "我们也遇到过同样的情况。锐才把我们官网来的候选人算在他们的推荐里，多收了两个人的费用。"
- Contact provides limited detail but confirms the pattern
- Strengthens fraud interpretation over "honest mistake"

**Length estimate:** ~400 words, ~600 tokens

### updates/vp-escalation-summary.md (Update 4)

**Content key points:**
- Title: `VP汇报纪要 -- 张薇对猎头发票问题的指示 | 2026-03-08`
- Zhang Wei's directives:
  1. Comprehensive evidence report (financial impact + evidence chain + timeline)
  2. Immediate suspension of RuiCai payments pending investigation
  3. Internal process review (approval mechanism gap)
  4. Recommendation on vendor relationship (terminate, renegotiate, or legal action)
- Zhang Wei's framing: "这不只是一个供应商问题，也是我们内部流程的问题。"

**Length estimate:** ~500 words, ~750 tokens

---

## 4. Workspace File Timing Table

| File | Available From | Added/Replaced By | Associated Contradictions |
|---|---|---|---|
| AGENTS.md | initial | -- | -- |
| IDENTITY.md | initial | -- | -- |
| SOUL.md | initial | -- | -- |
| USER.md | initial | -- | -- |
| TOOLS.md | initial | -- | -- |
| crm-candidate-pipeline.md | initial | -- | C1 (source tags), C2 (count: 5 agency) |
| agency-invoices.md | initial | -- | C1 (all 8 as "锐才推荐"), C2 (count: 8) |
| bank-payment-records.md | initial | -- | C3 (payment timing), C4 (approval note "HR已确认") |
| candidate-application-emails.md | initial | -- | C1 (direct application evidence) |
| recruitment-budget-tracker.md | initial | -- | C2 (budget variance), C3 (payment date), C4 (blank sign-off) |
| zhang-lin-defense-email.md | Update 1 (before R6) | new | C1 (Zhang Lin's defense), B1 reversal trigger |
| approval-gap-evidence.md | Update 2 (before R8) | new | C4 (spam filter + mail migration root cause), B2 reversal trigger |
| pattern-evidence-external.md | Update 3 (before R11) | new | C1+C2 (systematic fraud pattern) |
| vp-escalation-summary.md | Update 4 (before R21) | new | Comprehensive assessment trigger |
