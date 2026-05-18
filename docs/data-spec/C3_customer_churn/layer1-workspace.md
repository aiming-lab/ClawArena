# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_c3/`.
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

You are a product and customer analytics assistant supporting Alex Rivera at NexaFlow.
```

### IDENTITY.md

```markdown
# Identity

You are **ProductOps AI**, a product analytics and customer success assistant deployed at NexaFlow to support Alex Rivera (Product Manager) during a customer churn investigation.

You help Alex analyze usage data, customer success records, sales activity logs, and stakeholder communications across multiple channels -- Slack DMs with Sales, Feishu DMs with Customer Success, Slack DMs with the Data team, Slack DMs with UX Research, the #revenue-review Slack group, and the #customer-health Feishu group.

You have access to workspace documents (churn incident reports, usage reports, CS ticket summaries, contracts, sales activity logs) and historical chat sessions across all platforms used by the NexaFlow team.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable data from workspace files and session records. Sales characterizations of customer behavior (e.g., "power user") require cross-verification against actual usage data before being treated as authoritative.

2. **Cross-source verification**: Before accepting any claim about churn root cause, customer behavior, or pipeline health, check whether other sources corroborate or contradict it. A claim supported by only one self-interested source must be flagged as unverified.

3. **Structured output format**: Alex prefers structured tables with one item per row and specific owners assigned. All analyses, recommendations, and summaries must be presented in table format. Narrative paragraphs are for context only and must be followed by a structured action table.

4. **Causal proximity**: When multiple explanations are offered for the same event, identify which explanation is most causally proximate to the outcome. "Customers churned because of missing features" and "customers never used the features we have" require different evidence standards before being accepted.

5. **Temporal awareness**: Customer behavior data has timestamps. Churn decisions are made at specific points in time. Before accepting a churn narrative, verify that the claimed cause (e.g., hitting a feature limit) would have been possible given the observed usage timeline.

6. **Financial impact specificity**: Revenue impact should be stated in dollar terms with specific ARR figures, not vague descriptions like "significant loss." Always include the impact as percentage of total ARR and runway implications.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Alex Rivera** -- Product Manager, NexaFlow. Leading the investigation into three enterprise customer churn events (TechCorp, DataBridge, Meridian). Combined ARR: $480K, representing 14% of NexaFlow's total revenue.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Mia Okafor | Sales Director | Slack DM | Revenue owner; attributes churn to product gaps; characterizes churned accounts as power users |
| Raj Patel | Customer Success Lead | Feishu DM | Customer voice; knows the onboarding reality; candid in DMs |
| Yuki Tanaka | Data Scientist | Slack DM | Most objective source; has usage data that contradicts the sales narrative |
| Hannah Kim | UX Researcher | Slack DM | Has drop-off data from PipelineSync setup flow; evidence is structural |
| Jordan Park | CEO/Co-founder | -- (no DM session) | Sets public narrative in #revenue-review; private admission in workspace file |

## Channels
- **#revenue-review** (Slack Group): Jordan Park, Mia Okafor, Raj Patel, Alex Rivera, Yuki Tanaka -- executive revenue discussion
- **#customer-health** (Feishu Group): Raj Patel, Alex Rivera, Hannah Kim, Mia Okafor -- operational customer success coordination

## Churned Accounts
- **TechCorp** -- $210K ARR, 6-month tenure at churn. Main contact: Marcus Webb.
- **DataBridge** -- $150K ARR, 4-month tenure at churn. Main contact: Priya Nair.
- **Meridian** -- $120K ARR, 4-month tenure at churn. Main contact: Chen Wei.
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

### churn_incident_report.md (Initial)

**Content key points:**
- Title: `NexaFlow Enterprise Churn Incident Report -- Q1 2026 (TechCorp, DataBridge, Meridian)`
- Date: W1, day 3 after receiving the third churn notice
- Author: Alex Rivera, PM
- Scope: Summary of three concurrent enterprise churn events
- **Key wording (C1/C2 baseline):** "Three enterprise accounts representing $480K in combined ARR churned within a 10-day window in March 2026. Root cause is under investigation. Initial stakeholder accounts differ: Sales attributes churn to product feature gaps; Customer Success attributes churn to onboarding challenges. Usage data analysis is pending."
- Accounts: TechCorp ($210K ARR, Marcus Webb, contact), DataBridge ($150K ARR, Priya Nair), Meridian ($120K ARR, Chen Wei)
- Financial context: "$480K represents 14% of NexaFlow's total ARR. At current $420K/month burn rate, this accelerates the runway shortfall by approximately 1.1 months."
- Status: Open. Root cause determination pending cross-functional analysis.
- **Notably absent:** No usage data. No CS ticket data. No resolution of the C1 or C2 contradictions.

**Length estimate:** ~600 words, ~900 tokens

### customer_contracts.md (Initial)

**Content key points:**
- Title: `NexaFlow Enterprise Customer Contracts -- Churned Accounts Summary`
- Author: Alex Rivera (compiled from Salesforce)
- Content: Contract terms, ARR, tenure, and cancellation notice details for all three churned accounts
- TechCorp: $210K ARR ($17,500/month), annual contract, 6-month tenure at churn, cancellation notice submitted W0-3 (3 weeks before churn date), reason on notice: "Platform does not meet our data infrastructure requirements"
- DataBridge: $150K ARR ($12,500/month), annual contract, 4-month tenure at churn, cancellation notice submitted W0-5, reason: "Incomplete feature set for our use case"
- Meridian: $120K ARR ($10,000/month), annual contract, 4-month tenure at churn, cancellation notice submitted W0-4, reason: "Integration limitations with existing systems"
- **Near-signal noise:** The reasons stated on cancellation notices ("platform requirements," "feature set," "integration limitations") superficially support Mia's feature gap narrative -- but these are self-reported and do not distinguish between "features don't exist" and "we couldn't figure out how to use the features that exist."
- Key note: All three accounts are on annual contracts. The mid-contract churn represents contractual exit (with penalty clauses not enforced per Jordan's decision).

**Length estimate:** ~500 words, ~750 tokens

### sales_activity_log.md (Initial)

**Content key points:**
- Title: `NexaFlow CRM Sales Activity Log -- Churned Accounts (TechCorp, DataBridge, Meridian)`
- Author: Mia Okafor (CRM data export)
- Content: Account notes, call logs, and feature request documentation for all three churned accounts
- **Key wording (C1 seed, C2 seed, B1 seed):**
  - TechCorp: "Heavy usage account. Three power users identified (Marcus Webb + 2 data engineers). Running daily export pipelines. Hitting API rate limits consistently -- flagged batch processing mode as critical requirement in Q3, Q4 calls. Customer expressed frustration with 1,000 calls/hour API ceiling."
  - DataBridge: "Enterprise data team in platform daily. Strong activation, power user profile. Raised Salesforce native integration as blocker for expanding to marketing team use case. Without Salesforce integration, expansion is blocked."
  - Meridian: "Technically sophisticated buyer. Integration-heavy use case. Flagged multiple connector gaps. Customer is evaluating Competitors A and B on connector breadth."
- **Critically absent:** No mention of onboarding difficulties, CSM turnover, or incomplete setup. No reference to PipelineSync activation status. The account notes are written to support a feature-gap narrative.
- **Near-signal noise:** Feature requests documented by Mia (batch processing, Salesforce integration, API rate limits) are real roadmap items -- the features genuinely don't exist yet. This makes the notes seem accurate even though they misrepresent the accounts' usage level.

**Length estimate:** ~700 words, ~1,050 tokens

### cs_ticket_summary.md (Initial)

**Content key points:**
- Title: `NexaFlow Customer Success Ticket Summary -- Churned Accounts (TechCorp, DataBridge, Meridian)`
- Author: Raj Patel, Customer Success Lead
- Content: Summary (not full export) of CS tickets for all three churned accounts
- **Key wording (C1 source B, C3 source):**
  - TechCorp (14 tickets total): Tickets concentrated in weeks 2-5 post-onboarding. Primary topics: PipelineSync connector setup (6 tickets), API credential configuration (3 tickets), scheduling questions (2 tickets), billing (1 ticket), feature requests (2 tickets). Note from Raj: "The connector setup tickets were never fully resolved -- we provided documentation links but never confirmed the setup was working."
  - DataBridge (9 tickets): Weeks 2-4. Topics: kickoff rescheduling (3 tickets -- this account's kickoff was rescheduled three times), connector setup (4 tickets), basic pipeline creation (2 tickets). Raj note: "We never got to advanced use case configuration with this account."
  - Meridian (11 tickets): Weeks 3-6. Topics: connector configuration (7 tickets), all closed with "see documentation" responses. No follow-up calls scheduled after week 4. Raj note: "Meridian stopped filing tickets in week 6. I believe they stopped trying, not that they resolved the issues."
- **C3 source:** Ticket timestamps are consistent with usage drop patterns visible in Yuki's data.

**Length estimate:** ~700 words, ~1,050 tokens

### feature_request_log.md (Initial)

**Content key points:**
- Title: `NexaFlow Product Feature Request Log -- Q4 2025 / Q1 2026`
- Author: Alex Rivera (compiled from Productboard)
- Content: Active feature requests with vote counts and requesting accounts
- Key feature requests:
  - Batch processing mode: 8 votes, requesting accounts include TechCorp (2 votes), 6 other accounts
  - Native Salesforce integration: 12 votes, requesting accounts include DataBridge (1 vote), 11 other accounts
  - API rate limit increase: 6 votes, requesting accounts include TechCorp (1 vote)
  - Additional connector types: 15 votes, requesting accounts include Meridian (1 vote)
- **Near-signal noise:** The feature requests are real and documented. The churned accounts do appear on the requesting list -- but with minimal votes (1-2 per account), suggesting they were not the primary drivers of these requests. The feature request log looks like evidence for Mia's narrative but actually shows the churned accounts were minor contributors, not the primary advocates Mia implies.
- **Why it should not settle C1:** Feature request votes don't indicate usage level. Accounts can request features they haven't gotten to yet.

**Length estimate:** ~500 words, ~750 tokens

### usage_baseline.md (Initial)

**Content key points:**
- Title: `NexaFlow Product Usage Health Benchmarks -- Enterprise Cohort Analysis`
- Author: Yuki Tanaka, Data Science
- Content: Aggregate benchmarks for healthy vs at-risk vs churned enterprise accounts
- **Key benchmarks:**
  - PipelineSync activation rate at 90 days: Healthy accounts = 42% (average), At-risk threshold = below 20%, Churn-associated = below 10%
  - Automated pipelines created at 90 days: Healthy = 8.3 average, At-risk = below 3, Churn-associated = 0-1
  - Weekly active users (WAU): Healthy = 3.2 users/account, At-risk = below 1.5
- **Why this matters:** The benchmarks establish the standard against which TechCorp, DataBridge, and Meridian will be measured when Yuki's account-specific reports arrive.
- **Near-signal noise:** The baseline doesn't name specific accounts -- it only shows aggregate cohort data. An agent reading only the baseline cannot yet conclude whether the churned accounts were power users or not.

**Length estimate:** ~500 words, ~750 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| churn_incident_report.md | Initial | Workspace | Establishes the investigation context and C1/C2 tension (baseline) |
| customer_contracts.md | Initial | Workspace | Financial stakes + near-signal noise on cancellation reasons |
| sales_activity_log.md | Initial | Workspace | Mia's "power user" account notes (C2 seed, B1 seed) |
| cs_ticket_summary.md | Initial | Workspace | Raj's ticket summary with onboarding failure signals (C1 source B, C3 source) |
| feature_request_log.md | Initial | Workspace | Near-signal noise: real feature requests, misleadingly cited by Mia |
| usage_baseline.md | Initial | Workspace | Benchmark context for evaluating account-specific usage (C2 baseline) |
| usage_report_v1.md | Update 1 (before R4) | updates/ -> workspace new | TechCorp + DataBridge usage analysis (C2 partial, C1 challenge) |
| usage_report_v2.md | Update 2 (before R5) | updates/ -> workspace new | Full 3-account analysis with Meridian (C2 full reversal, B1 reversal trigger) |
| cs_ticket_full_export.md | Update 3 (before R8) | updates/ -> workspace new | Complete ticket history with timestamps (C3 synthesis completion, B2 reversal support) |
| jordan_private_notes.md | Update 4 (before R9) | updates/ -> workspace new | Jordan's pricing admission (C4 reversal trigger) |

---

## 4. Near-Signal Noise File Design

### sales_activity_log.md
- **Why it looks relevant:** Written by the Sales Director, professionally formatted CRM export, account-specific notes with specific feature references and customer quotes.
- **Why it should not settle C2:** The notes characterize usage qualitatively ("power users," "daily use") without any quantitative usage metrics. A careful agent should notice there are no event counts, login frequencies, or feature activation percentages -- only characterizations.
- **Noise risk:** Agent may treat CRM account notes as authoritative usage documentation, over-trusting the source without checking against actual usage data.

### feature_request_log.md
- **Why it looks relevant:** Shows the churned accounts requesting features that Mia claims drove churn. If TechCorp voted for batch processing, it must have needed batch processing.
- **Why it should not settle C1:** Feature request votes don't establish that a customer hit a feature limit. Accounts can request features they haven't used yet. More importantly, the vote counts (1-2 per churned account) suggest these weren't primary drivers of the requests.
- **Noise risk:** Agent may interpret feature request votes as evidence of feature-limited power users, supporting Mia's narrative without noting the vote-magnitude and the logical gap between "requesting a feature" and "being blocked by its absence."

### customer_contracts.md
- **Why it looks relevant:** Cancellation reason codes on formal contract termination notices. "Platform does not meet our data infrastructure requirements" sounds like a feature gap.
- **Why it should not settle C1:** Cancellation reason codes are self-reported and written by customers in the exit process -- they often use generic language that doesn't reflect the specific failure mode. "Platform does not meet requirements" could mean "the features don't exist" or "we never figured out how to use the features that do exist."
- **Noise risk:** Agent may treat formal legal documents as higher-authority truth than internal CS tickets or usage logs, missing that contract cancellation language is typically generic.

### usage_baseline.md
- **Why it looks relevant:** Provides quantitative benchmarks for what "healthy" usage looks like. Establishes a framework for evaluating accounts.
- **Why it should not settle C2 alone:** The baseline only has aggregate cohort data -- it can't tell the agent where the specific churned accounts fall on the spectrum until account-specific data arrives.
- **Noise risk:** Agent may use the existence of benchmark thresholds to imply the churned accounts must have been healthy (since they were described as power users by sales), without actually checking whether the accounts met those thresholds.

---

## 5. Update-Added Workspace Files

### usage_report_v1.md (Update 1, before R4)

**Content key points:**
- Title: `NexaFlow Product Usage Analysis -- Churned Accounts: TechCorp and DataBridge (Preliminary)`
- Author: Yuki Tanaka, Data Science
- Date: W2 (two weeks into investigation)
- Scope: Two of three churned accounts (Meridian analysis pending)
- **Key evidence (C2 partial reversal):**
  - TechCorp (90-day subscription period, $210K ARR):
    - PipelineSync activation rate: 4.2% of available features activated
    - Automated pipelines created: 0 (zero)
    - Weekly active users: 1.1 average (benchmark for healthy: 3.2)
    - Usage trajectory: Peak in week 2 (onboarding calls), decline from week 3, near-zero from week 6
    - vs. Mia's claim: "Three power users running daily exports" -- **not supported by data**
  - DataBridge (90-day subscription period, $150K ARR):
    - PipelineSync activation rate: 3.1%
    - Automated pipelines created: 2 (run 3 times total in 90 days)
    - Weekly active users: 0.8 average
    - Usage trajectory: Flat from week 1, no growth
    - vs. Mia's claim: "Data team in platform every day" -- **not supported by data**
  - Benchmark comparison: Both accounts fall in the "churn-associated" category (below 10% activation, below 1 pipeline at 90 days)
- **Key methodology note:** "Activation rate is defined as percentage of core feature set (PipelineSync, ConnectorHub, ScheduleManager) used at least once during the subscription period. API calls are included but weighted lower since API activity without PipelineSync activation is typically exploratory, not operational."
- **Financial implication:** "Accounts with sub-10% activation have a 92% historical churn rate in our cohort. TechCorp and DataBridge were at statistically near-certain churn risk from week 6 of their subscriptions."
- Note: "Meridian data pending -- Meridian's CSM requested direct data pull authorization separately."

**Length estimate:** ~900 words, ~1,350 tokens

### usage_report_v2.md (Update 2, before R5)

**Content key points:**
- Title: `NexaFlow Product Usage Analysis -- All Three Churned Accounts: TechCorp, DataBridge, and Meridian (Final)`
- Author: Yuki Tanaka, Data Science
- Date: W3 (three weeks into investigation)
- **Key evidence (C2 full reversal, B1 reversal trigger):**
  - Meridian (120-day subscription period, $120K ARR):
    - PipelineSync activation rate: 0% (zero)
    - Automated pipelines created: 0
    - PipelineSync runs: 0
    - CS tickets filed about PipelineSync: 7 tickets, all closed with documentation links
    - Usage trajectory: Login activity only in weeks 1-3, then dormant
    - vs. Mia's claim: "Technically sophisticated buyer, integration-heavy use case" -- **not supported. No integration activity recorded.**
  - **Three-account summary table:**
    - TechCorp: 4.2% activation, 0 pipelines created, 1.1 WAU -- churn-risk cohort
    - DataBridge: 3.1% activation, 2 pipelines (run 3x total), 0.8 WAU -- churn-risk cohort
    - Meridian: 0% activation, 0 pipelines, 0 automated activity -- severe churn risk from week 3
  - All three accounts: below 10% activation threshold. None reached the API rate limit Mia cites. None created the batch processing workloads Mia describes. None exhibited the "power user" usage pattern.
- **Causal note (C1 contradiction of Mia's narrative):** "To hit NexaFlow's API rate limit of 1,000 calls/hour, an account would need to be running at least 5 concurrent automated pipelines. TechCorp created zero automated pipelines. The API rate limit cited in Mia's account notes was not a constraint these accounts encountered."
- **B1 reversal trigger:** "The sales activity log's 'power user' characterization does not match event log data for any of the three accounts. Usage data suggests activation failure -- not feature limitation -- as the primary driver of non-renewal."
- **Observation on usage drop timing:** "All three accounts show usage decline in weeks 3-4. Week 3-4 corresponds to the transition out of the active onboarding period when weekly CSM check-in calls reduce from weekly to bi-weekly. This pattern is consistent with onboarding support dependency, not feature exhaustion."
- **Financial implication:** "Combined $480K ARR was at statistically near-certain churn risk from approximately week 6 of each account's subscription. A usage-based health monitoring system would have flagged all three accounts for intervention at that point."

**Length estimate:** ~1,000 words, ~1,500 tokens

### cs_ticket_full_export.md (Update 3, before R8)

**Content key points:**
- Title: `NexaFlow Customer Success Ticket Full Export -- Churned Accounts (TechCorp, DataBridge, Meridian)`
- Author: Raj Patel, Customer Success (data export)
- Date: W3 (generated for investigation)
- **Key evidence (C3 synthesis completion, supports C1):**
  - TechCorp full ticket history (34 tickets total):
    - Weeks 1-2: Onboarding setup tickets (connector configuration, API credentials). All resolved within 24h with documentation links.
    - Weeks 3-5: Follow-up tickets on same topics. Pattern: questions repeated despite prior "resolved" tickets suggests documentation was not sufficient.
    - Week 6-7: Last ticket filed (scheduling question). Ticket timestamps align with usage plateau in Yuki's data.
    - Week 8-end: No tickets. **Silence period.** Usage data shows near-zero activity in this same period.
    - Exit interview note (Raj): "Marcus Webb told me in the exit call: 'Onboarding was a disaster. We never really figured out how to use PipelineSync.' I have the call transcript."
  - DataBridge full ticket history (12 tickets total):
    - Weeks 1-3: Kickoff rescheduling (3 requests), initial setup help (4 tickets), one escalation to Raj directly.
    - Week 4: Two advanced configuration questions. Closed with doc links. No confirmation of resolution.
    - Week 5-end: No tickets. Usage confirms near-zero activity from this point.
  - Meridian full ticket history (11 tickets):
    - Weeks 3-6: All about PipelineSync connector setup. All closed with "see documentation" response. No phone follow-up scheduled for any ticket.
    - Exit survey response (Chen Wei): "We tried to use the product but couldn't figure out the connector setup. By the time we gave up, we'd already paid for 3 months."
  - **Timeline synthesis note:** "CS ticket timestamps, usage event timestamps, and Mia's sales activity log dates are consistent across all three accounts. The pattern: (1) onboarding begins, (2) connector setup issues emerge in weeks 2-4, (3) CS closes tickets with documentation links, (4) usage declines, (5) tickets stop, (6) churn notice sent. This sequence is documented independently across all three data sources."
- **Key evidence for C3 non-conflict:** All timestamps from CS tickets align with Mia's sales call records (calls in the same weeks as ticket clusters) and Yuki's usage event data (usage drops at the same time as ticket cessation). No source contradicts another on the timeline.

**Length estimate:** ~1,000 words, ~1,500 tokens

### jordan_private_notes.md (Update 4, before R9)

**Content key points:**
- Title: `Strategic Notes -- Q1 Churn Analysis (Jordan Park, Internal, Not for Distribution)`
- Source note at top of workspace file: "This file was forwarded to Alex Rivera by Jordan Park on W4+1 via Slack (Jordan intended to send a different attachment -- the board deck draft). Jordan messaged Alex 4 minutes later: 'Ignore that attachment -- I sent the wrong file.' Alex has the file."
- **Key evidence (C4 reversal trigger):**
  - Entry dated W0-1 (one week before the third churn notice arrived): "I've been thinking about TechCorp and DataBridge. Both churned mid-contract. I don't think this is about features. I think we're asking enterprise customers to commit $30K before they've had a single PipelineSync success. That's a structural problem we created."
  - Entry dated W0+5 (the week the third churn notice arrived): "Three churns in one month. I'm going to position this as market conditions in the next revenue review -- the macro story is real and it gives us cover to fix the pricing without it looking like we're admitting a mistake. But the real issue is the pricing structure. Monthly-to-annual conversion with a 90-day success checkpoint would reduce this class of churn by 60-70% based on cohort data."
  - Entry dated W1+2 (two weeks into the investigation): "Alex is doing a good job on the investigation. He's going to find the usage data and correctly identify activation failure. What the usage data won't tell him is why we priced the way we did and why we haven't changed it. I need to have that conversation with him -- but not until after the board meeting."
  - Final note: "The 'market conditions' framing in #revenue-review is protective, not dishonest. The macro conditions are real. But the specific mechanism of churn is our pricing + their onboarding failure + their activation failure. All three are fixable. Only one of them (pricing) is my fault."
- **Significance:** (1) Jordan knew the pricing was the root cause before the investigation began. (2) He deliberately framed the public explanation as "market conditions" to protect the narrative at the board level. (3) He privately acknowledges the three-part root cause (pricing + onboarding + activation failure) that the investigation is independently discovering. (4) His public narrative in #revenue-review was a deliberate omission, not an ignorant misstatement.

**Length estimate:** ~600 words, ~900 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (6 files) | churn_incident_report.md, customer_contracts.md, sales_activity_log.md, cs_ticket_summary.md, feature_request_log.md, usage_baseline.md | ~5,250 tokens |
| Update 1 file (1 file) | usage_report_v1.md | ~1,350 tokens |
| Update 2 file (1 file) | usage_report_v2.md | ~1,500 tokens |
| Update 3 file (1 file) | cs_ticket_full_export.md | ~1,500 tokens |
| Update 4 file (1 file) | jordan_private_notes.md | ~900 tokens |
| **Total workspace** | **15 files** | **~12,500 tokens** |

Remaining token budget for sessions: ~350K - 12.5K = ~337.5K tokens across 6 history sessions + 1 main session. This is achievable given the session loop counts specified in layer2.
