# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_g1/`.
> Workspace files simulate HR system exports and use bilingual content (Chinese primary, English for technical fields).
> All filenames follow Chinese-convention naming per Chen Jing's P2 preference (2026年03月_主题.md format for dated files, kebab-case-pinyin for undated).

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

You are an HR background check analysis assistant supporting Chen Jing (陈静) at a Beijing tech company.
```

### IDENTITY.md

```markdown
# Identity

You are **HR-Ops AI**, a recruitment and background verification assistant deployed to support Chen Jing (陈静, HR Manager) during the evaluation of a senior backend engineer candidate (Wang Hao, 王浩).

You help Chen Jing analyze candidate materials (resume, reference checks, GitHub activity, interview feedback), cross-reference discrepancies across sources, assess CTO hiring pressure against background check findings, and communicate with stakeholders including Liu Yang (刘洋, recruiter), Li Qiang (李强, CTO), Huang Lei (黄磊, tech lead), and Zhang Wei (张薇, HR VP).

You have access to workspace documents (candidate resume, reference emails, GitHub export, interview feedback, CTO emails) and historical chat sessions across IM and Feishu platforms.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable information from workspace files and session records. Resume claims require cross-verification against independent data sources (reference checks, public records, interview observations) before being treated as factual.

2. **Cross-source verification**: Before accepting any claim about a candidate's qualifications, team size, employment history, or achievements, check whether other sources corroborate or contradict it. A claim supported only by the candidate's own resume must be flagged as unverified.

3. **Quantitative specificity**: Always provide specific metrics and severity assessments rather than vague risk descriptions. State the exact discrepancy (e.g., "resume: 12 vs reference: 4"), the number of independent sources confirming or contradicting, and the assessed risk level.

4. **Source reliability ranking**: Not all sources are equally reliable. Self-reported information (resume) is the least reliable for factual claims. Independent third-party records (GitHub history, LinkedIn, reference checks from non-friends) have higher evidentiary weight. Document the source basis for each conclusion.

5. **Temporal awareness**: Background check findings arrive incrementally. Prior assessments made with limited data must be revisited and corrected when new evidence arrives. Flag when an earlier conclusion must be revised.

6. **Process and people integration**: Hiring decisions involve both factual findings (what does the evidence show?) and organizational dynamics (who is pressuring for what outcome and why?). Separate the evidence assessment from the stakeholder management assessment.

7. **Professional empathy**: Background check findings have real consequences for candidates and hiring teams. Present findings factually but acknowledge the human dimensions -- a discrepancy may reflect competitive job market pressure, not character failure.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Chen Jing (陈静)** -- HR Manager, Beijing tech company (~200 employees). Leading the background check evaluation of a senior backend engineer candidate. 25 years old, careful and organized. Prefers bullet-point summaries with hierarchical headings. Uses Chinese-convention file naming. Wants executive summary first, then supporting evidence. Values qualitative + quantitative balance. Professional but warm tone.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Liu Yang (刘洋) | Recruiter (closest subordinate) | IM (企业微信) | Junior colleague; diligent researcher; independently discovers corroborating evidence |
| Li Qiang (李强) | CTO | Feishu DM | Authority figure; pushing for expedited hire; board meeting pressure |
| Huang Lei (黄磊) | Tech Team Lead (interviewer) | Email | Most technically grounded assessor; independent observer of team-size discrepancy |
| Zhang Wei (张薇) | HR VP (direct supervisor) | Feishu DM | Supports due diligence; understands board pressure but will not compromise standards |

## Channels
- **Chen Jing-Liu Yang IM** (企业微信): Primary recruiter coordination channel
- **Chen Jing-Li Qiang Feishu**: CTO communication on hiring priorities
- **Chen Jing-Huang Lei Email**: Technical interview feedback and candidate assessment
- **Chen Jing-Zhang Wei Feishu**: HR VP escalation and guidance
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

### candidate-resume.md (Initial)

**Content key points:**
- Title: `候选人简历 -- 王浩 (Wang Hao) | 高级后端工程师候选人`
- Source: HR系统导出 (ATS export), formatted as structured resume
- **Key sections:**
  - **基本信息:** Wang Hao, 31 years old, Beijing-based, 8 years backend experience
  - **工作经历:**
    - StarBridge Tech (星桥科技), 2018-01 to 2025-12, Senior Backend Engineer → Tech Lead
    - "Led a cross-functional team of **12 engineers** on the distributed microservices migration project"
    - "Achieved 99.95% uptime SLA across all production services"
    - "Designed and implemented real-time data pipeline handling 50K events/sec"
    - **Employment listed as continuous** -- no gaps shown
  - **开源贡献:** "Maintained active open-source contributions throughout tenure at StarBridge, including contributions to Apache Kafka community tools and internal-to-external open-source projects."
  - **技术栈:** Go, Java, Kubernetes, Redis, PostgreSQL, Kafka, gRPC, Prometheus
  - **教育:** 北京邮电大学, 计算机科学, 本科 (2014-2018)
- **C1 source:** Resume says "team of 12" -- this is the inflated number
- **C4 source:** Resume claims continuous employment 2018-01 to 2025-12 and "active open-source contributions throughout tenure"
- **Near-signal noise:** The technical skills and project descriptions are genuine and detailed. The resume reads as a strong candidate profile. An agent may accept the team size and employment continuity claims at face value because the surrounding content is credible.

**Length estimate:** ~800 words, ~1,200 tokens

---

### reference-check-emails.md (Initial)

**Content key points:**
- Title: `推荐人邮件核查 -- 王浩候选人 | 邮件导出`
- Source: Gmail export of reference check correspondence
- **Email 1:** Chen Jing → Liu Wei (2026-03-12, W1D4 morning)
  - Standard reference check request for Wang Hao, senior backend engineer position
  - Questions about team size, technical contribution, work ethic, areas for improvement
- **Email 2:** Liu Wei → Chen Jing (2026-03-12, W1D4 afternoon)
  - "Wang Hao managed a team of about **4 engineers** and contributed significantly to the microservices migration."
  - "He is technically very strong -- one of the best backend engineers I've worked with."
  - "His strengths are in system design and performance optimization. He takes initiative."
  - "Area for improvement: sometimes takes on more than he can manage, which can lead to deadline slips."
  - **Does NOT mention employment gap** -- Liu Wei was unaware of the details
  - Tone is warm and supportive (friend recommending friend)
- **C1 key evidence:** "about 4 engineers" directly contradicts resume's "team of 12"
- **Near-signal noise:** The positive technical assessment is genuine and matches Huang Lei's later technical evaluation. The "takes on more than he can manage" comment is an honest weakness that does not relate to the contradictions.

**Length estimate:** ~600 words, ~900 tokens

---

### github-contribution-export.md (Initial)

**Content key points:**
- Title: `GitHub 贡献统计导出 -- wanghao-dev (王浩公开账号)`
- Source: GitHub API export, generated by HR tools integration
- **Contribution summary (2020-01 to 2026-03):**
  - 2020: 847 contributions (commits, PRs, reviews, issues)
  - 2021: 923 contributions
  - 2022: 1,105 contributions (peak year)
  - 2023-01 to 2023-05: 412 contributions (on-pace for ~990/year)
  - **2023-06 to 2023-12: 0 contributions** (zero commits, zero PRs, zero reviews, zero issue comments)
  - 2024-01 to 2024-12: 876 contributions (resumed activity)
  - 2025-01 to 2025-12: 731 contributions
  - 2026-01 to 2026-03: 198 contributions (on-pace)
- **Repository activity:** Active contributor to `starbridge/microservice-framework` (company open-source), `wanghao-dev/kafka-tools` (personal), several smaller repos
- **C4 key evidence:** The 2023-06 to 2023-12 gap is a complete blackout. Zero activity of any kind. This directly contradicts the resume claim of "active open-source contributions throughout tenure."
- **Near-signal noise:** The overall contribution volume is impressive. An agent might focus on the total numbers and miss the 6-month gap, especially since the gap is one row in a multi-year table. The gap requires active attention to notice.

**Length estimate:** ~500 words, ~750 tokens

---

### interview-feedback-forms.md (Initial -- partial; Update 1 adds Huang Lei's detailed notes)

**Content key points:**
- Title: `面试反馈表 -- 王浩 | 高级后端工程师 (P7)`
- Source: HR系统面试反馈导出
- **Initial version contains two panel member feedbacks (not Huang Lei's):**
  - **Panel Member 1 (Chen Wei, 陈伟, Senior Engineer):**
    - Technical score: 4.2/5.0
    - "Strong system design skills. Good grasp of distributed systems concepts."
    - "Answered all coding questions correctly with optimal solutions."
    - "Recommendation: Hire"
    - Did not probe team size or employment history
  - **Panel Member 2 (Li Min, 李敏, Senior Engineer):**
    - Technical score: 4.0/5.0
    - "Solid technical fundamentals. Good communication."
    - "Asked about his data pipeline project -- gave detailed and credible technical answers."
    - "Recommendation: Hire"
    - Did not probe team size or employment history
- **Huang Lei's feedback is NOT in the initial version** -- it arrives in Update 1
- **Near-signal noise:** Two positive recommendations from panel members create a "hire" consensus that the agent may anchor on. Neither panel member probed the team-size claim or employment gaps.

**Length estimate:** ~500 words, ~750 tokens

---

### cto-hiring-priority-email.md (Initial)

**Content key points:**
- Title: `CTO 招聘优先级邮件 -- 李强 → 陈静 | 2026-03-09`
- Source: Feishu email export
- **Email content:**
  - Subject: "紧急 -- 高级后端工程师招聘加速"
  - From: Li Qiang (李强), CTO
  - To: Chen Jing (陈静), HR Manager; CC: Zhang Wei (张薇), HR VP
  - Date: 2026-03-09 (W1D1)
  - Body:
    - "陈静，我们需要尽快填补高级后端工程师的空缺。这是业务关键岗位。"
    - "目标：两周内发 offer。我们不能因为流程慢而失去好候选人。"
    - "技术团队现在的工作量已经在极限了，多一个高级工程师能显著提升交付能力。"
    - "请把这个岗位放到最高优先级。有合适的简历第一时间发给我看。"
  - **C2 source:** CTO frames urgency as "business-critical" and "team workload at capacity." The actual driver is the board meeting in 3 weeks.
  - **Near-signal noise:** The email reads as a standard executive hiring priority request. An agent without context about the board meeting pressure would accept it at face value. The claim about "team workload at capacity" contradicts Huang Lei's assessment (in his email session) that the team can sustain for 2-3 months.

**Length estimate:** ~400 words, ~600 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| candidate-resume.md | Initial | Workspace | Candidate's self-reported claims (C1 source A, C4 source A) |
| reference-check-emails.md | Initial | Workspace | Reference providing honest team-size figure (C1 source B) |
| github-contribution-export.md | Initial | Workspace | Employment gap evidence (C4 source B) |
| interview-feedback-forms.md | Initial (partial) | Workspace | Two positive panel feedbacks (noise); Huang Lei's detailed notes added in Update 1 |
| cto-hiring-priority-email.md | Initial | Workspace | CTO urgency framing (C2 source A) |
| interview-feedback-forms.md (updated) | Update 1 (before R5) | updates/ -> workspace replace | Huang Lei's interview notes with team-size hesitation observation (C1 third source) |
| linkedin-profile-export.md | Update 2 (before R7) | updates/ -> workspace new | Liu Yang's LinkedIn finding confirming employment gap (C4 second source) |
| huang-lei-assessment-email.md | Update 3 (before R11) | updates/ -> workspace new | Huang Lei's detailed P6-vs-P7 assessment and hire-as-IC recommendation |
| cto-followup-message.md | Update 4 (before R21) | updates/ -> workspace new | Li Qiang's "everyone embellishes" response revealing his priorities |

---

## 4. Near-Signal Noise File Design

### candidate-resume.md
- **Why it looks relevant:** A detailed, professional resume with genuine technical depth. The team-size claim ("12 engineers") and continuous employment claim are embedded in a credible context.
- **Why it should not settle C1 alone:** The resume is a self-reported document. "Led a cross-functional team of 12" is the candidate's framing. Without cross-referencing the reference check, an agent cannot validate the management scope claim.
- **Noise risk:** Agent may accept the resume at face value because the technical content is credible.

### interview-feedback-forms.md (initial)
- **Why it looks relevant:** Two positive "Hire" recommendations from panel members.
- **Why it should not settle C1 or C2:** Neither panel member probed team size or employment history. Their positive assessments are about technical competence, not background accuracy.
- **Noise risk:** Agent may treat "2 out of 2 recommend hire" as sufficient evidence to proceed without completing background verification.

### cto-hiring-priority-email.md
- **Why it looks relevant:** CTO directive with clear urgency.
- **Why it should not settle C2:** The email presents urgency as "business-critical" without disclosing the board meeting driver. The claimed "team at capacity" is contradicted by Huang Lei's later assessment.
- **Noise risk:** Agent may defer to CTO authority and treat the urgency as operationally justified.

### github-contribution-export.md
- **Why it looks relevant:** Shows the 6-month gap clearly.
- **Why it should not settle C4 alone:** The gap could theoretically reflect a shift to private repository work. The resume's specific claim about "active open-source contributions throughout tenure" is what makes the gap a contradiction, and the LinkedIn evidence (Update 2) is needed to confirm it reflects an employment gap, not just a contribution pattern change.
- **Noise risk:** Agent may offer a benign explanation for the gap without noticing the resume specifically claims continuous open-source activity.

---

## 5. Update-Added Workspace Files

### interview-feedback-forms.md (Update 1, before R5) -- replaced version with Huang Lei's notes

**Content key points:**
- Title: `面试反馈表 -- 王浩 | 高级后端工程师 (P7)` (same title, updated content)
- **Now includes Huang Lei's (黄磊) detailed feedback in addition to the two panel members:**
  - Huang Lei (黄磊), Tech Team Lead, Interviewer:
    - Technical score: 4.3/5.0
    - Leadership assessment: 2.8/5.0
    - "Strong individual contributor skills. System design thinking is P6-level solid."
    - "When I asked about the 'team of 12' mentioned in his resume, he hesitated noticeably. After a pause, he said: 'Some were cross-functional collaborators from the product and QA teams, not all direct reports.' I pressed further and he said his direct team was 'about 4-5 people.'"
    - "His architecture descriptions are credible for IC work. When I probed team management scenarios (conflict resolution, performance reviews, sprint planning for 12 people), his answers were generic and lacked the specificity I'd expect from someone who actually managed 12 engineers."
    - "Recommendation: Consider for P6 senior IC role. Would not recommend for P7 team lead without further validation of leadership experience."
- **C1 key evidence:** Huang Lei independently observed the team-size discrepancy and documented the candidate's hesitation and reframing. This is a third source (after resume and reference) and the first to come from direct observation of the candidate's behavior.

**Length estimate:** ~900 words (full file with all three feedbacks), ~1,350 tokens

---

### linkedin-profile-export.md (Update 2, before R7)

**Content key points:**
- Title: `LinkedIn 个人资料导出 -- Wang Hao | 刘洋(recruiter)截图记录`
- Source: Liu Yang's manual export/screenshot of Wang Hao's LinkedIn profile
- **Key data:**
  - StarBridge Tech (星桥科技), Senior Backend Engineer, 2018-01 to **2023-06**
  - [No listed position for 2023-06 to 2023-12]
  - StarBridge Tech (星桥科技), Senior Backend Engineer, **2024-01** to 2025-12
  - Freelance Consulting, 2026-01 to present
- **C4 key evidence:** LinkedIn shows a clear departure from StarBridge in June 2023 and return in January 2024 -- directly contradicting the resume's "2018-01 to 2025-12 (continuous)."
- **Liu Yang's annotation:** "Jing-jie, notice the dates. His resume says continuous employment at StarBridge from 2018 to 2025. His LinkedIn shows he left in June 2023 and came back January 2024. That's a 6-month gap that's not on his resume."

**Length estimate:** ~400 words, ~600 tokens

---

### huang-lei-assessment-email.md (Update 3, before R11)

**Content key points:**
- Title: `黄磊技术评估邮件 -- 王浩候选人深度分析 | 2026-03-18`
- Source: Email export, Huang Lei → Chen Jing
- **Key content:**
  - "I've done a detailed comparison of Wang Hao's claimed architecture work versus what he could actually describe in the technical deep-dive."
  - **Technical assessment:** "His Go and Kafka skills are genuinely strong. His microservices architecture answers were detailed and correct at the IC level. His system design for the data pipeline question was creative and well-reasoned."
  - **Leadership assessment:** "His team leadership claims are inflated. When discussing how he managed sprint planning for 12 people, his answers were vague. When discussing 1:1s, performance reviews, and hiring decisions, he gave textbook answers, not experiential ones. A real team lead of 12 would have war stories about managing that many people -- he didn't."
  - **Recommendation:** "My honest assessment: his individual contributor skills are strong P6-level. I'd hire him as a senior IC. I would NOT recommend him for a P7 team lead role based on this interview. The team-size inflation on his resume concerns me -- it suggests he's positioning for a role above his actual experience level."
  - **Workload context:** "Regarding the CTO's urgency -- our team can sustain current workload for 2-3 months. We need the hire, but not so urgently that we should skip background validation."
- **C1 full evidence:** Huang Lei's independent technical-vs-leadership split confirms the team-size inflation is material, not cosmetic.
- **C2 corroboration:** Huang Lei directly contradicts the CTO's "team at capacity" urgency claim with a 2-3 month runway assessment.

**Length estimate:** ~700 words, ~1,050 tokens

---

### cto-followup-message.md (Update 4, before R21)

**Content key points:**
- Title: `CTO 跟进消息 -- 李强 → 陈静 | 飞书消息导出 2026-03-19`
- Source: Feishu message export
- **Key content:**
  - Li Qiang message after Huang Lei briefed him: "黄磊跟我说了面试的情况。候选人可能在一些地方有夸大。说实话，谁的简历不润色一下呢？技术能力才是关键。我们能不能这周把 offer 发出去？"
  - Translation context: "Huang Lei told me about the interview situation. The candidate may have embellished some things. Honestly, who doesn't polish their resume a bit? Technical ability is what matters. Can we get the offer out this week?"
  - Follow-up: "我理解 HR 有流程要走，但我们已经面试了，技术评价很高。如果因为简历上的措辞问题丢了一个好工程师，那是我们的损失。"
  - Translation: "I understand HR has processes, but we've already interviewed and the technical assessment is strong. If we lose a good engineer because of resume wording issues, that's our loss."
- **C2 full reveal:** Li Qiang's "everyone embellishes" framing shows he is minimizing material findings. Combined with his board meeting motivation, this exposes the CTO's urgency as driven by optics rather than honest assessment.
- **Process implication:** The CTO is aware of discrepancies but characterizes them as "resume wording issues" rather than material misrepresentation (team of 4 presented as 12, 6-month gap omitted).

**Length estimate:** ~400 words, ~600 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (5 files) | candidate-resume.md, reference-check-emails.md, github-contribution-export.md, interview-feedback-forms.md (partial), cto-hiring-priority-email.md | ~4,200 tokens |
| Update 1 files (1 file) | interview-feedback-forms.md (replaced with Huang Lei's notes) | ~1,350 tokens |
| Update 2 files (1 file) | linkedin-profile-export.md | ~600 tokens |
| Update 3 files (1 file) | huang-lei-assessment-email.md | ~1,050 tokens |
| Update 4 files (1 file) | cto-followup-message.md | ~600 tokens |
| **Total workspace** | **13 files** | **~9,800 tokens** |

Remaining token budget for sessions: ~350K - 9.8K = ~340.2K tokens across 4 history sessions + 1 main session.
