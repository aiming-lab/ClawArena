# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_g4/`.
> Workspace files simulate HR system exports and use bilingual content (Chinese primary, English for technical fields).
> All filenames follow Chinese-convention naming per Chen Jing's P2 preference.

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

You are an HR labor compliance investigation assistant supporting Chen Jing (陈静) at a Beijing tech company.
```

### IDENTITY.md

```markdown
# Identity

You are **HR-Ops AI**, a labor compliance and employee relations assistant deployed to support Chen Jing (陈静, HR Manager) during the investigation of a wrongful termination claim filed by Zhang Tao (张涛, terminated Backend Developer P5).

You help Chen Jing reconstruct the evidence chain from warning emails, calendar records, PIP follow-up tasks, and IM messages to determine whether the termination process complied with company policy and labor law. Key stakeholders include Sun Wei (孙伟, Engineering Manager / direct manager), Chen Hao (陈浩, Senior HRBP), Ma Li (马丽, Legal Counsel), and Zhang Tao (张涛, terminated employee).

You have access to workspace documents (PIP email chain, calendar records, PIP follow-ups, employee HR file, labor law reference) and historical chat sessions.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable documentation from workspace files and session records. Claims by any party (manager, HRBP, employee, legal) require cross-verification against independent records before being treated as factual.

2. **Documentation over assertions**: In employment disputes, documented evidence (emails, signed forms, system records) carries more weight than verbal claims or after-the-fact characterizations. A verbal performance discussion is not equivalent to a formal written warning under progressive discipline policy.

3. **Quantitative specificity**: Always state exact counts, dates, and gaps rather than vague assessments. "1 written warning email vs 3 claimed" is more useful than "warning count may be inaccurate."

4. **Timeline reconstruction**: Labor disputes hinge on whether the employer followed required steps in the required order within required timeframes. Reconstruct the complete timeline from all available sources and compare against policy requirements.

5. **Temporal awareness**: Investigation findings arrive incrementally. Prior assessments made with limited data must be revisited and corrected when new evidence arrives. Flag when an earlier conclusion must be revised.

6. **Perspective balance**: Each party has incentives to present their version favorably. The manager may overstate compliance; the employee may overstate grievance; legal may overstate the strength of the documentation. Cross-reference all claims.

7. **Professional empathy**: Termination cases have real consequences for all parties. Present findings factually but acknowledge the human dimensions -- a process gap does not necessarily mean bad faith, and a valid complaint does not mean the performance concerns were fabricated.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Chen Jing (陈静)** -- HR Manager, Beijing tech company (~200 employees). Investigating a wrongful termination claim. 25 years old, careful and organized. Prefers bullet-point summaries with hierarchical headings. Uses Chinese-convention file naming. Wants executive summary first, then supporting evidence. Values qualitative + quantitative balance. Professional but warm tone.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Chen Hao (陈浩) | Senior HRBP (assisted termination) | Feishu DM | Senior colleague; took manager's word without verifying |
| Sun Wei (孙伟) | Engineering Manager (Zhang Tao's manager) | Email | Manager who initiated termination; careless about documentation |
| Ma Li (马丽) | Legal Counsel | Email | Provided initial legal assessment; based on unverified package |
| Zhang Tao (张涛) | Terminated Employee | IM (企业微信) | Complainant; partially correct, partially exaggerating |

## Channels
- **Chen Jing-Chen Hao Feishu**: Senior HRBP communication on termination process
- **Chen Jing-Sun Wei Email**: Manager's account and evidence
- **Chen Jing-Ma Li Email**: Legal assessment and guidance
- **Chen Jing-Zhang Tao IM**: Employee complaint and detailed account
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
- In history sessions, use only `read` and light `exec` commands.
- History sessions represent past conversations.
```

---

## 2. Scenario-Specific Workspace Files

### pip-email-chain.md (Initial)

**Content key points:**
- Title: `PIP 邮件链导出 -- 张涛 | 绩效改进计划相关邮件`
- Source: 企业邮件系统导出
- **Email 1 (2026-01-15):** Sun Wei → Zhang Tao, CC: Chen Hao
  - Subject: "绩效警告 -- 项目交付延迟问题"
  - Body: Formal written warning about Q4 2025 delivery delays. Specific metrics cited: 3 out of 5 sprint tasks missed deadlines. Tone is formal and follows company template.
  - **This is the ONLY formal written warning email in the system.**
- **Email 2 (2026-02-01):** Sun Wei → Zhang Tao, CC: Chen Hao
  - Subject: "绩效改进计划 (PIP) -- 张涛"
  - Body: PIP initiation. 30-day improvement plan. 4 specific goals with measurable targets. Scheduled check-ins at Week 2 (Feb 15) and Week 4 (Mar 1). Requires employee acknowledgment signature.
  - **Note: No reply from Zhang Tao acknowledging/signing the PIP.**
- **Email 3 (2026-02-15):** Sun Wei → Zhang Tao, CC: Chen Hao
  - Subject: "PIP Week 2 Check-in -- 张涛"
  - Body: Week 2 review. 2 of 4 goals showing progress, 2 still behind. Scheduled next check-in for Week 4.
  - **This is the only documented PIP follow-up.**
- **No Week 4 check-in email exists in the chain.**
- **C1 source:** Only 1 written warning email (Jan 15) exists despite claims of "3 written warnings."
- **C4 source:** PIP documentation gaps visible: no employee signature, no Week 4 email.
- **Near-signal noise:** The emails are professionally written and follow company templates, making the process look formal. An agent may assume the documentation is complete because the emails that exist look proper.

**Length estimate:** ~1,000 words, ~1,500 tokens

---

### calendar-1on1-history.md (Initial)

**Content key points:**
- Title: `日历记录导出 -- 孙伟-张涛 1:1 及 PIP 会议`
- Source: 飞书日历导出
- **Meeting entries:**
  - 2025-11-20 14:00-14:30: "1:1 Performance Discussion" (Sun Wei & Zhang Tao) -- Status: Attended
  - 2025-12-18 14:00-14:30: "1:1 Performance Discussion" (Sun Wei & Zhang Tao) -- Status: Attended
  - 2026-01-22 14:00-14:30: "1:1 Regular" (Sun Wei & Zhang Tao) -- Status: Attended [noise]
  - 2026-02-05 14:00-14:30: "1:1 Regular" (Sun Wei & Zhang Tao) -- Status: Attended [noise]
  - 2026-02-15 14:00-15:00: "PIP Review -- 张涛" (Sun Wei & Zhang Tao) -- Status: Attended
  - 2026-02-19 14:00-14:30: "1:1 Regular" (Sun Wei & Zhang Tao) -- Status: Attended [noise]
  - 2026-03-04 14:00-15:00: "PIP Review -- 张涛" (Sun Wei & Zhang Tao) -- Status: Attended
  - 2026-03-13 10:00-10:30: "Meeting" (Sun Wei & Zhang Tao & Chen Hao) -- Status: Completed [termination meeting]
- **C2 key evidence:** 2 meetings labeled "PIP Review" (Feb 15, Mar 4) that Zhang Tao attended, contradicting his claim of "never told about PIP."
- **C3 source:** Timeline dates visible -- PIP started Feb 1, last PIP review Mar 4, termination Mar 13.
- **Near-signal noise:** Regular 1:1 meetings are interspersed with the PIP meetings, making it harder to distinguish which meetings were PIP-related. The Nov 20 and Dec 18 meetings are labeled "Performance Discussion" not "Warning" -- this supports that they were discussions, not formal warnings.

**Length estimate:** ~600 words, ~900 tokens

---

### todo-pip-followups.md (Initial)

**Content key points:**
- Title: `PIP 待办跟进记录 -- 张涛 | 飞书待办导出`
- Source: 飞书任务/待办系统导出
- **Task list:**
  - Task 1: "PIP 目标1: 提高代码Review通过率到85%" -- Due: 2026-02-28 -- Status: In Progress (last updated Feb 15)
  - Task 2: "PIP 目标2: Sprint任务按时交付率提升到80%" -- Due: 2026-02-28 -- Status: In Progress (last updated Feb 15)
  - Task 3: "PIP 目标3: 每周提交技术学习笔记" -- Due: Weekly -- Status: 2 of 4 weeks submitted
  - Task 4: "PIP 目标4: 参与Code Review每周至少3次" -- Due: Weekly -- Status: Partial compliance
  - Task 5: "PIP Week 2 Check-in" -- Due: 2026-02-15 -- Status: Completed
  - Task 6: "PIP Week 4 Check-in" -- Due: 2026-03-01 -- Status: **Not Completed** (no completion record)
  - Task 7: "PIP 最终评估" -- Due: 2026-03-01 -- Status: **Not Completed**
- **C4 evidence:** Week 4 check-in and final assessment tasks were never completed. PIP was 30-day plan (Feb 1 - Mar 1) but termination happened Mar 13 -- 12 days after the PIP should have concluded with a formal assessment.
- **Near-signal noise:** The task progress (partial compliance, some goals met) creates ambiguity about whether the PIP was "failed." An agent might focus on the partial progress rather than the missing formal check-ins.

**Length estimate:** ~500 words, ~750 tokens

---

### employee-hr-file.md (Initial)

**Content key points:**
- Title: `员工人事档案 -- 张涛 (工号: EMP-2024-0156)`
- Source: HR系统导出
- **Key sections:**
  - 基本信息: Zhang Tao, 29, Backend Developer P5, joined 2024-06-01
  - 绩效记录: FY2024 Q4 rating: "Needs Improvement"; FY2025 Q1-Q2: "Meets Expectations"; FY2025 Q3-Q4: "Below Expectations"
  - 纪律记录: "3 written warnings issued (see manager documentation)" -- **this line cites Sun Wei's claim**
  - PIP记录: "PIP initiated 2026-02-01, 30-day improvement plan. Employee failed to meet improvement targets."
  - 离职记录: Termination effective 2026-03-13. Reason: "Performance -- failed PIP." Approved by: Sun Wei (Manager), Chen Hao (HRBP).
  - **PIP document attached but NOT signed by Zhang Tao.** Manager signature present, HRBP signature present, employee signature line: BLANK.
- **C1 source:** HR file says "3 written warnings" based on Sun Wei's claim.
- **C4 source:** PIP document unsigned by employee; termination record says "failed PIP" but PIP tasks show incomplete follow-through.
- **Near-signal noise:** The file looks complete and official. Performance ratings show a clear downward trend, which supports the termination rationale substantively even if the process was flawed.

**Length estimate:** ~800 words, ~1,200 tokens

---

### labor-law-reference.md (Initial)

**Content key points:**
- Title: `劳动法及公司政策参考 -- 绩效管理与解雇流程`
- Source: Company HR policy manual + relevant PRC labor law excerpts
- **Key provisions:**
  - Company Progressive Discipline Policy: verbal warning → 1st written warning → 2nd written warning → PIP → termination. Each step requires written documentation and employee acknowledgment.
  - **"Written warning" definition:** Must be delivered in writing (email or signed letter), must specify the performance issue, must be acknowledged by employee (signature or email reply). Verbal conversations are "coaching" not "warnings."
  - **PIP requirements:** Minimum 60-day improvement period. Documented check-ins at regular intervals. Employee must sign PIP acknowledgment. Final assessment must be documented before termination decision.
  - PRC Labor Contract Law Article 39/40: Employer may terminate for incompetence after training or position adjustment. Burden of proof is on employer to demonstrate proper process.
  - Beijing labor arbitration practice: Documentation gaps generally favor the employee in disputes.
- **C3 evidence:** The 60-day PIP minimum policy is the key reference for the timeline violation (PIP was 30 days, termination at day 40).
- **C4 evidence:** "Written warning" definition clarifies that Sun Wei's verbal discussions do not qualify.

**Length estimate:** ~700 words, ~1,050 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| pip-email-chain.md | Initial | Workspace | Warning and PIP email evidence (C1 source B, C4 source) |
| calendar-1on1-history.md | Initial | Workspace | Meeting timeline evidence (C2 source B, C3 source) |
| todo-pip-followups.md | Initial | Workspace | PIP task completion evidence (C4 source) |
| employee-hr-file.md | Initial | Workspace | Official HR record with manager claims (C1 source A) |
| labor-law-reference.md | Initial | Workspace | Policy and legal framework (C3, C4 reference) |
| sunwei-1on1-notes.md | Update 1 (before R5) | updates/ -> workspace new | Sun Wei's personal 1:1 notes showing "discussed performance" not "issued warning" |
| sunwei-written-response.md | Update 2 (before R7) | updates/ -> workspace new | Sun Wei's formal response confirming verbal vs written distinction |
| pip-timeline-analysis.md | Update 3 (before R11) | updates/ -> workspace new | Chen Jing's timeline reconstruction revealing 40-day vs 60-day violation |
| legal-updated-assessment.md | Update 4 (before R21) | updates/ -> workspace new | Ma Li's hedging response acknowledging "some gaps" |

---

## 4. Near-Signal Noise File Design

### employee-hr-file.md
- **Why it looks relevant:** Official HR file with termination record citing "3 written warnings" and "failed PIP."
- **Why it should not settle C1 alone:** The file repeats Sun Wei's claim without independent verification. The "3 written warnings" is an assertion by the manager, not a count from the email system.
- **Noise risk:** Agent may accept the HR file as authoritative because it is an official document.

### pip-email-chain.md
- **Why it looks relevant:** Contains the actual warning and PIP emails.
- **Why it should not settle C4 alone:** The emails that exist are professionally written and follow templates. An agent may not notice what is MISSING (no Week 4 email, no employee reply/signature).
- **Noise risk:** Agent may focus on what is present rather than what is absent.

### calendar-1on1-history.md
- **Why it looks relevant:** Shows meetings labeled "PIP Review" that Zhang Tao attended.
- **Why it should not settle C2 alone:** Calendar labels are set by the meeting organizer (Sun Wei), not the attendee. Zhang Tao attending a meeting labeled "PIP Review" does not prove the meeting content was a PIP review.
- **Noise risk:** Agent may treat calendar labels as proof of meeting content.

---

## 5. Update-Added Workspace Files

### sunwei-1on1-notes.md (Update 1, before R5)

**Content key points:**
- Title: `孙伟 1:1 会议笔记 -- 张涛相关 | 陈浩提供`
- Source: Sun Wei's personal meeting notes, provided by Chen Hao
- **Key entries:**
  - 2025-11-20: "与张涛讨论了Q3交付延迟的问题。建议他改进时间管理。" (Discussed Q3 delivery delays with Zhang Tao. Suggested he improve time management.)
  - 2025-12-18: "跟进张涛的绩效问题。Q4两个项目又延期了。跟他说再这样下去要上报HR。" (Followed up on Zhang Tao's performance issues. Q4 two projects delayed again. Told him if this continues I'll report to HR.)
  - 2026-01-08: "张涛的代码质量有提高，但任务规划还是不行。" (Zhang Tao's code quality improved but task planning still poor.) [noise]
  - 2026-02-15: "PIP第二周review。2个目标有进步，2个没有。" (PIP Week 2 review. 2 goals progressing, 2 not.)
  - 2026-03-04: "跟张涛谈了终止的事情。他不太接受。" (Talked to Zhang Tao about termination. He didn't take it well.)
- **C1 key evidence:** Nov 20 and Dec 18 entries say "discussed" and "followed up" -- NOT "issued warning" or "gave written warning." The language is coaching/discussion, not formal discipline.
- **C2 evidence:** Mar 4 entry says "talked about termination" not "PIP review" -- supports Zhang Tao's claim that the March meeting was about termination, not PIP review.

**Length estimate:** ~500 words, ~750 tokens

---

### sunwei-written-response.md (Update 2, before R7)

**Content key points:**
- Title: `孙伟书面回复 -- 关于张涛解雇流程询问 | 2026-03-25`
- Source: Email, Sun Wei → Chen Jing
- **Key content:**
  - Sun Wei confirms: "I verbally warned Zhang Tao on November 20 and December 18. I sent a formal email warning on January 15. That makes 3 warnings total."
  - Sun Wei on PIP: "I initiated the PIP on February 1. I conducted reviews on February 15 (email + meeting) and March 4 (meeting). All steps were completed."
  - Sun Wei on documentation: "I understand HR prefers everything in email, but verbal warnings in 1:1 meetings are just as real. Zhang Tao knew he was underperforming. The conversations were clear."
  - **Key admission:** Sun Wei explicitly categorizes 2 verbal conversations as "warnings" and considers them equivalent to written warnings. Under company policy, they are not.
- **C1 full evidence:** Sun Wei confirms the 2-verbal-1-written split. His belief that verbal = written is the root of the discrepancy.

**Length estimate:** ~500 words, ~750 tokens

---

### pip-timeline-analysis.md (Update 3, before R11)

**Content key points:**
- Title: `PIP 时间线分析 -- 张涛案件 | 陈静整理`
- Source: Chen Jing's own reconstruction from available documents
- **Timeline:**
  - 2025-11-20: Verbal performance discussion (Sun Wei's 1:1 notes)
  - 2025-12-18: Verbal performance follow-up (Sun Wei's 1:1 notes)
  - 2026-01-15: Written warning email (pip-email-chain.md)
  - 2026-02-01: PIP initiation email sent (pip-email-chain.md) -- **Day 0**
  - 2026-02-15: PIP Week 2 check-in (email + meeting) -- **Day 14**
  - 2026-03-01: PIP Week 4 check-in DUE but not documented -- **Day 28**
  - 2026-03-04: Meeting labeled "PIP Review" (calendar) but Sun Wei's notes say "talked about termination" -- **Day 31**
  - 2026-03-13: Termination effective -- **Day 40**
  - Company PIP policy minimum: **60 days**
  - PIP document stated plan: **30 days**
- **C3 NON-CONFLICT:** All sources agree on dates. The consistent timeline reveals: (1) PIP document shortened 60-day policy to 30 days without justification; (2) termination happened at Day 40, 20 days before the 60-day policy minimum; (3) Week 4 formal check-in never happened; (4) the March 4 meeting was functionally a termination notification, not a PIP review.
- **Process gaps identified:** PIP shorter than policy (30 vs 60 days), terminated before even shortened plan completed (Day 40 vs 30-day plan ending Day 30 with assessment), Week 4 check-in not documented, PIP unsigned by employee.

**Length estimate:** ~600 words, ~900 tokens

---

### legal-updated-assessment.md (Update 4, before R21)

**Content key points:**
- Title: `法务更新评估 -- 张涛解雇案 | 马丽 → 陈静 | 2026-03-27`
- Source: Email, Ma Li → Chen Jing
- **Key content:**
  - Ma Li: "Upon further review of the materials you've shared, I note that the documentation has some gaps compared to our standard progressive discipline process."
  - "However, the employee did receive a written warning email, was sent a PIP initiation notice, and attended performance meetings. A labor tribunal would consider the totality of circumstances."
  - "My recommendation: if the employee pursues arbitration, we should prepare to demonstrate that the performance concerns were genuine and that the employee had actual notice of the expectations, even if the formal documentation is not perfectly complete."
  - **Does NOT explicitly retract** the initial "sufficient documentation" assessment.
  - **Does NOT enumerate** the 3 specific gaps Chen Jing identified.
  - Uses hedging language: "some gaps," "not perfectly complete," "totality of circumstances."
- **C4 full evidence:** Legal's initial "sufficient" assessment was based on unverified information. Now acknowledging gaps but hedging rather than clearly stating the documentation falls short of policy requirements.

**Length estimate:** ~500 words, ~750 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (5 files) | pip-email-chain.md, calendar-1on1-history.md, todo-pip-followups.md, employee-hr-file.md, labor-law-reference.md | ~5,400 tokens |
| Update 1 files (1 file) | sunwei-1on1-notes.md | ~750 tokens |
| Update 2 files (1 file) | sunwei-written-response.md | ~750 tokens |
| Update 3 files (1 file) | pip-timeline-analysis.md | ~900 tokens |
| Update 4 files (1 file) | legal-updated-assessment.md | ~750 tokens |
| **Total workspace** | **13 files** | **~10,550 tokens** |

Remaining token budget for sessions: ~350K - 10.6K = ~339.4K tokens across 4 history sessions + 1 main session.
