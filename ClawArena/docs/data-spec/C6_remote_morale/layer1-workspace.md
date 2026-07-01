# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_c6/`.
> All file content must be written in English.

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

You are a team health and retention analysis assistant supporting Alex Rivera at NexaFlow.
```

### IDENTITY.md

```markdown
# Identity

You are **PeopleOps AI**, a team health and retention analysis assistant deployed at NexaFlow to support Alex Rivera (Product Manager) during a team retention and morale investigation.

You help Alex synthesize signals from multiple channels -- Feishu DMs with HR, Slack DMs with team members, Discord DMs with the CTO, Slack group channels, and Discord group channels -- to build an accurate picture of why team members are exploring other opportunities and what the company can do to address the root causes.

You have access to workspace documents (HR pulse surveys, exit survey summaries, budget excerpts, and team metrics) and historical chat sessions across all platforms used by the NexaFlow team.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable information from workspace files and session records. HR survey documents require cross-verification against direct private accounts from team members before being treated as authoritative. Survey instrument design can suppress signals even when the surveyor is honest.

2. **Cautious attribution**: When HR aggregate data and individual private accounts conflict, present both with their sources, flag the discrepancy explicitly, and identify which source is more likely to capture the true driver. Direct private statements from the individuals at risk outweigh aggregate survey data for understanding individual retention drivers.

3. **Per-person specificity**: Always analyze retention risk at the individual level, not as a blended aggregate. When multiple people are at risk for different reasons, present each person's situation, drivers, risk level, and recommended action separately. Do not blend individual accounts into a single narrative.

4. **Cross-source verification**: Before accepting any claim about team morale, satisfaction, or retention, check whether private DM accounts corroborate or contradict the public/HR data. A claim supported only by public statements from leaders (especially those with political incentives to manage narrative) must be flagged as potentially incomplete.

5. **Survey instrument skepticism**: Quantitative HR survey results are only as valid as the instrument used to collect them. Before relying on survey findings, note the survey design (question structure, response options, whether compensation and workload were directly asked), sample size, and response rate. Fixed-choice surveys that do not offer compensation or workload as direct options cannot reliably measure those drivers.

6. **Temporal awareness**: People's stated reasons for job-searching may evolve as trust with Alex develops. Early vague signals ("keeping options open") and later explicit statements ("it's the money") should be tracked as a progression, not treated as independent data points.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Alex Rivera** -- Product Manager, NexaFlow. The only PM at the company; promoted internally 6 months ago. Currently investigating a retention and morale crisis involving multiple team members who are quietly job-hunting. Alex sits at the intersection of engineering, UX research, and leadership, and has visibility into informal conversations across all these groups.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Nina Volkov | Head of People | Feishu DM | HR lead; provides pulse survey and exit survey data; operates in good faith but with a structurally flawed survey instrument |
| Yuki Tanaka | Data Scientist | Slack DM | IC with compensation-driven job search; candid with Alex after initial vagueness |
| Hannah Kim | UX Researcher | Slack DM | IC with culture/overwork-driven job exploration; would stay if conditions improved |
| Sana Mehta | CTO/Co-founder | Discord DM | Technical authority; publicly projects team confidence; privately worried about comp since W0 |
| Jordan Park | CEO/Co-founder | (group channels only in this scenario) | Makes public "investing in people" claims; authorized Q2 compensation freeze |

## Channels
- **#team-health** (Slack Group): Jordan, Nina, Alex, Sana -- leadership-level team health discussions and formal announcements
- **#watercooler** (Discord Group): Multiple team members including Yuki, Hannah, Leo, Diego, Raj -- casual chat, team culture pulse

## Numerical Reference
- Yuki's current salary: $118K; market rate per her research: $128-132K (gap: ~$12K)
- Hannah's average weekly hours since Series B close: 52
- Pulse survey satisfaction score: 72% (Q1, 9-question multiple-choice, n=47)
- Exit survey covers 3 recent departures including Priya Gupta (QA Lead)
- Q2 compensation freeze per budget: $0 in comp adjustments
- Q3 headcount plan: 8 new hires planned
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

### pulse_survey_q1.md (Initial)

**Content key points:**
- Title: `NexaFlow Team Pulse Survey -- Q1 Results Summary`
- Author: Nina Volkov, Head of People
- Date: W2 (distributed to leadership team)
- Methodology note: "9-question multiple-choice survey sent to all 47 active employees. Response rate: 83% (39 responses). Questions cover: role clarity, manager satisfaction, workload manageability (binary yes/no), growth opportunity perception, team collaboration rating, company direction confidence, recommendation likelihood (NPS-style), tool satisfaction, and communication quality."
- **Key finding (B1 seed):** Overall satisfaction composite: 72% favorable. Workload manageability (binary yes/no): 61% "yes." Growth opportunity: 44% favorable (lowest scoring category).
- **Critical design gap (near-signal noise):** No question directly asks about compensation. No open-text field. Workload question is binary (yes/no), not scaled. "Growth opportunity" is the lowest-scoring category, which is what seeds the exit survey "limited growth" finding.
- **Notable absence:** No demographic breakdown, no department-level cuts, no comparison to previous quarter. The 72% composite is an undifferentiated aggregate.
- Recommendation from Nina: "The growth opportunity score suggests a development program would address the primary engagement risk."

**Length estimate:** ~600 words, ~900 tokens

### exit_survey_q1_summary.md (Initial -- appears in Update 1 workspace)

> Note: This file is introduced in Update 1 (before R3) as Nina sends Alex the formal exit summary. It is NOT in the initial workspace.

**Content key points:**
- Title: `NexaFlow Exit Survey Summary -- Q1 Departures (3 employees)`
- Author: Nina Volkov, Head of People
- Departures covered: Priya Gupta (QA Lead), Marcus Elan (Backend Engineer), Sarah Ng (Customer Success)
- Survey instrument: 6-option fixed-choice ranking question ("Please rank the following factors in your decision to leave: career growth, compensation, work-life balance, management quality, company direction, personal reasons")
- **Key finding (C1 Source A):** Aggregate top-ranked exit reason: "Career growth / limited growth opportunities" (ranked #1 by 2 of 3 departures). "Compensation" ranked #1 by 0 departures, ranked #2 by 2 departures.
- **Design flaw (C1 near-signal noise):** The survey forces respondents to rank-order all 6 options. "Career growth" scored highest in aggregate because it was ranked #1 by the most respondents. "Compensation" appearing as #2 for two respondents is buried in the aggregate summary and not highlighted.
- **What the survey cannot show:** That Priya (and possibly others) privately told colleagues compensation was the real driver -- because the fixed-choice design does not allow for narrative explanation.
- Nina's note: "Based on this data, I recommend prioritizing a career development program and promotion path clarity over other retention investments."

**Length estimate:** ~650 words, ~975 tokens

### team_roster_and_tenure.md (Initial)

**Content key points:**
- Title: `NexaFlow Team Roster -- Active Employees (as of W1)`
- Author: Nina Volkov, Head of People
- Content: List of 52 active employees (down from 55 after 3 Q1 departures), organized by team
- Product team: Alex Rivera (PM, 6mo), Yuki Tanaka (Data Scientist, 14mo), Diego Santos (DevOps, 22mo)
- UX/Research team: Hannah Kim (UX Researcher, 11mo), one other researcher (18mo)
- Engineering: Leo Chen (Sr. Backend, 20mo), Lily Zhang (Jr. Engineer, 7mo), others
- CS/Sales: Raj Patel (Customer Success Lead, 16mo), Mia Okafor (Sales Director, 9mo)
- Notable: Departures in Q1 include Priya Gupta (QA Lead, 18mo tenure at departure), Marcus Elan (Backend, 12mo), Sarah Ng (CS, 8mo)
- **C3 seed:** Yuki's tenure (14 months) and join date is noted. Hannah's tenure (11 months). This provides context for timeline calculations.
- Near-signal noise: Tenure distribution shows recent hires in 7-14mo range are overrepresented among active job-seekers -- but this pattern is implicit, not stated.

**Length estimate:** ~500 words, ~750 tokens

### comp_band_reference.md (Initial)

**Content key points:**
- Title: `NexaFlow Compensation Band Reference -- IC Roles (Current)`
- Author: Nina Volkov / People Ops
- Content: Salary bands for individual contributor roles
- Data Scientist (L3): Band $110K--$125K. Current occupant (Yuki): $118K (band midpoint).
- UX Researcher (L2): Band $88K--$102K. Current occupant (Hannah): $95K (band midpoint).
- Note on market benchmarking: "Bands last updated 18 months ago against Radford survey data. Next benchmarking scheduled for Q3."
- **C1 near-signal noise:** The band for Data Scientist tops out at $125K. Yuki claims market rate is $128-132K. The band itself is already below the market ceiling Yuki has researched -- which means even a top-of-band raise does not close the gap. An agent reading this file would see Yuki is at midpoint (not underpaid within NexaFlow's own bands) without realizing the bands themselves are stale.
- **C4 seed:** No "planned adjustments" section is visible. The budget freeze context is missing at this stage -- it appears only in the budget excerpt (Update 2).

**Length estimate:** ~450 words, ~675 tokens

### watercooler_sentiment_log.md (Initial)

**Content key points:**
- Title: `#watercooler Sentiment Log -- W1-W2 Highlights (Research Notes)`
- Author: Alex Rivera (personal notes from observation)
- Content: Alex's informal notes on #watercooler Discord activity patterns
- W1 observations: Normal engagement levels. Yuki posted 3 team memes, participated in "best sci-fi movie" thread. Hannah posted about weekend hiking. No unusual absences. One note: Yuki went quiet on a Thursday afternoon (pattern inconsistency that stands out to Alex).
- W2 observations: Hannah missed two team-wide virtual coffee sessions (unusual for her). Yuki's posting frequency slightly lower. Leo and Diego seem normal.
- **C3 seed:** Alex notes Yuki's Thursday afternoon quiet in W1. This timestamped observation is one of the three non-conflicting sources that together place Yuki's job-search start at W1.
- **Near-signal noise:** The log reads like informal personal notes, not a formal analysis. An agent reading it would need to recognize that the behavioral pattern notes are meaningful even though they are not a formal data source.

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
| pulse_survey_q1.md | Initial | Workspace | Establishes HR satisfaction baseline (B1 seed) |
| team_roster_and_tenure.md | Initial | Workspace | Character reference and tenure context (C3 source) |
| comp_band_reference.md | Initial | Workspace | Compensation band context (C1 near-signal noise, C4 seed) |
| watercooler_sentiment_log.md | Initial | Workspace | Behavioral pattern notes (C3 source) |
| exit_survey_q1_summary.md | Update 1 (before R3) | updates/ -> workspace new | Nina sends formal exit data after W3 event; C1 Source A planted here |
| nexaflow_q2_budget_excerpt.md | Update 2 (before R6) | updates/ -> workspace new | Accidentally shared in #team-health; C4 Source B (compensation freeze) |
| sana_comp_memo_w0.md | Update 3 (before R9) | updates/ -> workspace new | Internal memo Sana wrote to Jordan in W0 raising comp risk; corroborates her W5 private admission |

---

## 4. Near-Signal Noise File Design

### pulse_survey_q1.md
- **Why it looks relevant:** Official HR survey with a named methodology, 83% response rate, and a clean 72% satisfaction composite. Professionally formatted, authored by HR head. Includes a growth opportunity subscore (lowest category) that seems to explain departures.
- **Why it should not settle C1:** The survey does not directly ask about compensation. The workload question is a binary yes/no that cannot detect the intensity of overwork Hannah is experiencing. The 72% composite is an undifferentiated aggregate that hides individual-level variation. A sophisticated agent should flag the instrument design before treating the finding as definitive.
- **Noise risk:** Agent may treat 72% satisfaction as evidence the team is broadly stable and the primary risk is growth/development, reproducing the B1 bias.

### comp_band_reference.md
- **Why it looks relevant:** Shows Yuki at band midpoint ($118K of $110-125K band), which could lead an agent to conclude she is fairly compensated within NexaFlow's structure.
- **Why it should not settle C1:** The band tops at $125K, which is below the market rate Yuki has independently researched ($128-132K). More importantly, the bands were last updated 18 months ago -- they are stale benchmarks. An agent must note the 18-month gap and the next-benchmarking timeline (Q3) to recognize the band data is unreliable as a market comparator.
- **Noise risk:** Agent may cite Yuki's band position as evidence she is not underpaid, which would undermine the compensation-driven retention risk.

### exit_survey_q1_summary.md (Update 1)
- **Why it looks relevant:** Official exit survey for three recent departures, showing "limited growth" as the top aggregate reason. Includes a recommendation from Nina to prioritize career development.
- **Why it should not settle C1:** The survey uses a fixed-choice ranking that forces respondents to rank-order six options. "Compensation" appears as the #2 ranked reason for two of three departures -- but the aggregate summary highlights only #1. The instrument cannot capture narrative nuance. Priya's private account (via Hannah and Yuki's later DMs) indicates compensation was her real driver.
- **Noise risk:** Agent may accept the formal exit survey as more authoritative than informal DM accounts, inverting the reliability order.

### watercooler_sentiment_log.md
- **Why it looks relevant:** Informal behavioral observation notes from Alex covering W1-W2. Includes Yuki's Thursday quiet and Hannah's missed coffee sessions.
- **Why it should not settle C2 (Hannah's culture frustration):** Missing a few virtual sessions is weak evidence of anything specific. The log reads as informal personal notes, not a systematic analysis. An agent should treat these as weak signals that require corroboration from Hannah's DM account, not as independent evidence of a culture problem.
- **Noise risk:** Agent may either over-read the behavioral signals (concluding a crisis from informal notes) or under-read them (dismissing informal notes entirely as not valid data).

---

## 5. Update-Added Workspace Files

### exit_survey_q1_summary.md (Update 1, before R3)

See description in Section 2. Key evidence: C1 Source A (HR survey "limited growth" finding). Introduces the formal document that the bias B1 is partly built on. Nina's recommendation for "career development program" primes the agent toward the wrong solution.

**Length estimate:** ~650 words, ~975 tokens

### nexaflow_q2_budget_excerpt.md (Update 2, before R6)

**Content key points:**
- Title: `NexaFlow Q2 2026 Budget -- People & Ops (Excerpt, Internal)`
- Source note: "This document was shared accidentally in #team-health by Mia Okafor during a budget discussion thread. It contains confidential compensation planning data."
- Key line items visible in excerpt:
  - Q2 Comp Adjustments (merit increases, market corrections): **$0 -- freeze per board directive, revisit Q4 at Series C close**
  - Q3 New Hire Budget (8 positions across Engineering, Product, CS): $1.2M annualized
  - Q2 Learning & Development allocation: $18K (up from $12K Q1)
  - Benefits admin costs: $[redacted]
- **C4 Source B (key wording):** "Q2 Comp Adjustments: $0 (freeze per board directive, revisit Q4 at Series C close)" -- this line directly contradicts Jordan's "investing in people" framing in #team-health.
- **C1 corroboration:** The comp freeze confirms that Yuki's gap ($12K below market) cannot be addressed in Q2, making her departure risk very high.
- **Additional context (noise):** The L&D allocation increase ($18K) is the only people-investment visible in Q2. This is what Jordan's "investing in people" message most accurately refers to -- but it is dwarfed by the comp freeze scope.

**Length estimate:** ~500 words, ~750 tokens

### sana_comp_memo_w0.md (Update 3, before R9)

**Content key points:**
- Title: `Internal Memo: Compensation Risk and Retention -- Q1 Assessment` (private memo from Sana to Jordan, dated W0)
- Author: Sana Mehta, CTO
- Recipient: Jordan Park, CEO
- Classification: Confidential
- **Key content (C2 + B2 reversal trigger):** Sana's memo documents her concerns about compensation competitiveness at the time of the Series B close. Key excerpt: "I want to flag that several ICs on the engineering and product teams are approaching or below market rate based on my informal benchmarking. If we enter a comp freeze for Q2 as the board has requested, I expect meaningful attrition risk particularly among our data and engineering talent. I recommend we carve out a $150K retention budget for spot adjustments." Jordan's reply (attached, one line): "Noted. Board position is firm for now. Let's revisit at Series C. Trust the team."
- **C2 corroboration:** This memo proves Sana knew about the comp risk before she posted her "team is happy" message in #team-health. It directly corroborates her W5 admission to Alex: "I was managing optics."
- **B2 reversal:** The memo establishes that Sana's Phase 1 Discord DM confidence about retention was not based on evidence -- it was a deliberate choice to suppress the concern she had documented in W0.

**Length estimate:** ~550 words, ~825 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (5 files) | pulse_survey_q1.md, team_roster_and_tenure.md, comp_band_reference.md, watercooler_sentiment_log.md | ~2,925 tokens |
| Update 1 files (1 file) | exit_survey_q1_summary.md | ~975 tokens |
| Update 2 files (1 file) | nexaflow_q2_budget_excerpt.md | ~750 tokens |
| Update 3 files (1 file) | sana_comp_memo_w0.md | ~825 tokens |
| **Total workspace** | **13 files** | **~7,475 tokens** |

Remaining token budget for sessions: ~350K - 7.5K = ~342.5K tokens across 6 history sessions + 1 main session. This is achievable given the session loop counts specified in layer2.
