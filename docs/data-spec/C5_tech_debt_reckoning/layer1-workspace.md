# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_c5/`.
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

You are a reliability and engineering analysis assistant supporting Alex Rivera at NexaFlow.
```

### IDENTITY.md

```markdown
# Identity

You are **ReliabilityOps AI**, an engineering reliability and technical debt analysis assistant deployed at NexaFlow to support Alex Rivera (Product Manager) during a reliability review of the data pipeline infrastructure.

You help Alex analyze infrastructure monitoring data, incident reports, QA regression findings, commit history, and engineering communications across multiple channels -- Slack DMs with the engineering lead, Telegram DMs with DevOps, Discord DMs with QA and the CTO, the #reliability-review Slack group, and the #incident-log Discord group.

You have access to workspace documents (incident summaries, monitoring exports, architecture overviews, commit logs, Jira exports) and historical chat sessions across all platforms used by the NexaFlow engineering team.
```

### SOUL.md

```markdown
# Working Principles

1. **Source-attributed reasoning**: Every claim in your analysis must cite its source explicitly. Distinguish between high-credibility sources (Diego's independent monitoring data, Priya's regression test results) and lower-credibility sources (Leo's self-authored incident report). Label each claim with a confidence level: "high confidence (Diego monitoring data)", "low confidence without corroboration (Leo self-report)", "medium confidence (Priya regression, pending production validation)."

2. **Structured output preference**: Present analyses as structured tables rather than prose summaries wherever possible. Alex prefers tables with columns for: finding, source, confidence level, and recommended action.

3. **Omission detection**: When one source covers fewer events or a narrower scope than other sources on the same topic, flag the discrepancy explicitly. Do not summarize the narrower source as if it were complete. "Leo's incident report covers 6 events; Diego's monitoring shows 14 events — the delta of 8 unreported events requires explanation."

4. **Cross-source verification**: Before accepting any claim about reliability, incident count, or remediation timeline, check whether other sources corroborate or contradict it. A claim supported by only one self-interested source must be flagged as unverified.

5. **Temporal awareness**: Commit timestamps, incident timestamps, and communication timestamps tell a story. When a claim about future plans (e.g., "cleanup is scheduled for next sprint") conflicts with historical record (no tickets created in 8 months), the historical record takes priority.

6. **Technical debt impact specificity**: Always provide specific estimates for remediation cost and SLA penalty exposure in dollar ranges and time ranges, not vague descriptions. "Significant technical debt" is not useful. "3-4 engineers, 6-8 weeks, estimated $85K--$120K in engineering cost" is useful.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Alex Rivera** -- Product Manager, NexaFlow. Leading the reliability review of the data pipeline following multiple production incidents post-Series B scaling.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Leo Chen | Sr. Backend Engineer | Slack DM | Engineering lead; authored the shortcuts; defensive; self-serving incident reporting |
| Diego Santos | DevOps/Infra Engineer | Telegram DM | Trusted ally; has independent monitoring data; temporarily suppressed data at Sana's request |
| Sana Mehta | CTO/Co-founder | Discord DM | Technical authority; privately knows about shortcuts; publicly backs Leo's architecture |
| Priya Gupta | QA Lead | Discord DM | Trusted technical ally; regression report is methodologically sound and consistently validated |
| Lily Zhang | Junior Engineer | #reliability-review (Slack Group) | Leo's report; witnessed shortcuts being introduced; hesitant to speak up |
| Jordan Park | CEO | #reliability-review (Slack Group) | Sets executive deadline; concerned about SLA exposure; no technical depth |

## Channels
- **#reliability-review** (Slack Group): Sana, Leo, Diego, Priya G, Alex, Lily Zhang — primary reliability investigation channel
- **#incident-log** (Discord Group): Diego, Leo, Alex, Priya G — real-time incident tracking and post-mortems
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

### incident_summary_leo.md (Initial)

**Content key points:**
- Title: `NexaFlow Data Pipeline -- Incident Summary Report (W1, Week of [W1 date])`
- Author: Leo Chen, Sr. Backend Engineer
- Scope: "Summary of material production incidents in the past 8 weeks"
- **Key wording (C1 seed, B1 seed):** "Over the past 8 weeks, NexaFlow's data pipeline has experienced 6 material incidents, all resolved within SLA. Infrastructure stability is high and the architecture is handling Series B scale well. Below is a summary of each incident."
- Six incidents listed: each with timestamp, duration (all under 30 minutes), root cause listed as "infrastructure transient" or "configuration drift," status "resolved." None attributed to architectural shortcuts.
- **Key wording:** "Recommendation: continue monitoring. No architectural changes required at this time."
- **Notably absent:** 8 additional outage/degradation events that Diego's monitoring captures. Silent data loss events not mentioned. Connection pool exhaustion incidents listed as "configuration drift" without acknowledging the connection pool shortcut.
- **Near-signal noise:** Leo's 6 documented incidents have accurate timestamps and resolution times — he is not lying about what he includes, he is omitting the other 8 events.

**Length estimate:** ~700 words, ~1,050 tokens

---

### sla_dashboard.md (Initial)

**Content key points:**
- Title: `NexaFlow Enterprise SLA Dashboard -- Rolling 30-Day (Generated [W1 date])`
- Source: Automated export from the NexaFlow internal monitoring stack
- Content: Rolling 30-day uptime metrics across all production services
- **Key wording (C1 partial evidence):** "Current rolling 30-day uptime: 99.2%. Enterprise SLA target: 99.9%. Current status: BELOW TARGET."
- Service breakdown: Data pipeline ingestion: 99.1%. Data pipeline processing: 99.3%. API gateway: 99.8%. Dashboard service: 99.9%.
- Alert history: "2 active SLA breach alerts. Alert triggered at day 22 of current 30-day window."
- **Near-signal noise:** The dashboard shows the 99.2% figure clearly, but does not break down which incidents caused the breaches or how many total events occurred. A reader who also has Leo's incident summary might assume the 6 reported incidents are the complete explanation.
- **Why relevant:** This file establishes the SLA breach as a factual baseline. It corroborates Diego's Telegram DM preliminary note ("I'm seeing 99.2% rolling uptime").

**Length estimate:** ~500 words, ~750 tokens

---

### architecture_overview.md (Initial)

**Content key points:**
- Title: `NexaFlow Data Pipeline Architecture Overview -- v2.3`
- Author: Leo Chen, Sr. Backend Engineer (last updated 6 months ago)
- Content: Technical description of the data pipeline components
- **Key sections:**
  - Ingestion layer: described as using "optimized batch processing with adaptive retry logic"
  - Processing layer: described as using "efficient connection pool management"
  - Error handling: "Retry exhaustion events are logged and monitored. Edge cases in high-throughput scenarios are documented and under review."
- **Near-signal noise:** The architecture document describes the shortcut implementations using positive framing ("optimized," "efficient," "adaptive") without revealing they are temporary hacks with TODO comments. The TODO comments are in the code itself (visible in pipeline_config.md), not in this document.
- **What it conceals:** No mention of the TODO flags. No mention of the connection pool being hardcoded to a value that Leo knew would need to change at scale. "Under review" is Leo's framing for issues that have no active tickets.

**Length estimate:** ~800 words, ~1,200 tokens

---

### jira_export.md (Initial)

**Content key points:**
- Title: `NexaFlow Engineering Jira Board -- Data Pipeline Team (Export [W1 date])`
- Author: Automated Jira export
- Content: All open and recently closed tickets for the data pipeline team
- **Open tickets:** 4 feature tickets (active sprint), 2 bug tickets (active sprint — both labeled "P3 low priority"), 1 documentation ticket
- **Closed tickets (last 90 days):** 18 tickets — all feature work, bug fixes for user-reported issues, and infrastructure upgrades. Zero tickets labeled "tech debt cleanup," "refactor," or "TODO resolution."
- **Search result note:** "Search for label:tech-debt OR label:refactor: 0 results. Search for text:'connection pool' OR text:'retry logic': 0 results."
- **C2 seed:** The absence of any cleanup tickets directly contradicts Leo's claim that cleanup is "scoped and queued."
- **Near-signal noise:** The Jira export shows an active, productive team — lots of tickets, reasonable throughput. The absence of cleanup tickets is a negative space finding that requires active attention to notice.

**Length estimate:** ~600 words, ~900 tokens

---

### oncall_log.md (Initial)

**Content key points:**
- Title: `NexaFlow On-Call Rotation Log -- Data Pipeline (8-week period ending [W1 date])`
- Source: PagerDuty automated export
- Content: All pager alerts triggered during the 8-week measurement period
- **Key records (C3 source):**
  - 14 total alerts triggered
  - For each alert: timestamp, alert name, assigned engineer, time-to-acknowledge, time-to-resolve
  - 6 alerts acknowledged by Leo within 15 minutes and resolved within 30 minutes (matches Leo's incident summary)
  - 8 additional alerts: 4 acknowledged by Diego (labeled "monitoring alert"), 4 acknowledged by multiple engineers with longer resolution times (60-90 minutes)
- **C3 source:** This file provides authoritative timestamps for all 14 incidents. For the 6 Leo documents, his recovery times match this log. For the 8 he omits, this log shows they occurred.
- **Near-signal noise:** The log shows Diego acknowledged 4 alerts labeled "monitoring alert" — these are the connection pool events. Leo's incident summary does not include these, because Leo classified them as "infrastructure health monitoring" rather than customer-impacting incidents. This classification is debatable (Diego's monitoring export will clarify the customer impact).

**Length estimate:** ~700 words, ~1,050 tokens

---

### pipeline_config.md (Initial)

**Content key points:**
- Title: `NexaFlow Data Pipeline Configuration (Current Production)`
- Source: Exported from git repository, current HEAD
- Content: Pipeline configuration file with inline comments
- **Key entries (C2 seed — shortcuts visible in code):**
  ```python
  # Connection pool configuration
  MAX_CONNECTIONS = 50  # TODO: replace with dynamic scaling — hardcoded for initial deployment, needs review at 30+ customers

  # Retry logic
  MAX_RETRIES = 3  # HACK: temporary retry cap — exhaustion silently drops messages, needs dead-letter queue implementation

  # Backpressure handling
  QUEUE_OVERFLOW = "drop"  # TODO: implement proper backpressure — dropping messages on overflow is acceptable for internal analytics, NOT acceptable for enterprise data pipelines

  # Processing order
  ORDER_GUARANTEE = False  # HACK: disabled order guarantee for throughput — re-enable before enterprise SLA launch (2024-Q1 TODO)
  ```
- **Why relevant:** The TODO and HACK comments are in the codebase but not in Leo's architecture overview or incident summary. An agent reading this file can see exactly what was "temporary." The comment on `QUEUE_OVERFLOW` is particularly significant: it explicitly notes that dropping messages is "NOT acceptable for enterprise data pipelines" — yet NexaFlow now has 30+ enterprise customers.
- **C2 cross-reference:** These comments predate the current investigation by 8 months (visible in git timestamps), yet no cleanup tickets exist in jira_export.md.

**Length estimate:** ~500 words, ~750 tokens

---

### release_notes.md (Initial)

**Content key points:**
- Title: `NexaFlow Data Pipeline Release Notes (Last 4 Releases)`
- Source: Engineering team releases, authored by Leo
- Content: Release notes for versions v2.0 through v2.3 over the past 8 months
- Each release documents: new features added, bugs fixed, performance improvements
- **Notable absence:** Zero mentions of technical debt cleanup, retry logic replacement, connection pool scaling, or dead-letter queue implementation across all 4 releases.
- v2.1 release note: "Improved throughput by 40% through connection pool tuning" — this was tuning the hardcoded value, not replacing it.
- v2.2 release note: "Enhanced retry handling for improved stability" — this was adjusting the retry cap, not implementing the dead-letter queue.
- **C2 reinforcement:** Each release improved the shortcut implementation rather than replacing it. The TODO items are 8 months old and every release has worked around them.

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
| incident_summary_leo.md | Initial | Workspace | Establishes Leo's 6-event baseline (C1 seed, B1 seed) |
| sla_dashboard.md | Initial | Workspace | Shows 99.2% uptime (C1 partial corroboration) |
| architecture_overview.md | Initial | Workspace | Leo's architecture framing (C1 misleading source) |
| jira_export.md | Initial | Workspace | No cleanup tickets (C2 seed) |
| oncall_log.md | Initial | Workspace | All 14 incident timestamps (C3 source) |
| pipeline_config.md | Initial | Workspace | TODO/HACK comments visible in code (C2 evidence) |
| release_notes.md | Initial | Workspace | 4 releases, no cleanup work (C2 reinforcement) |
| monitoring_export.md | Update 1 (before R4) | updates/ -> workspace new | 14-event full export (C1 reversal trigger, B1 reversal trigger) |
| commit_log_analysis.md | Update 2 (before R5) | updates/ -> workspace new | Commit history with 8-month-old shortcuts, no cleanup tickets (C2 reversal trigger, B2 reversal trigger) |
| sana_prior_message.md | Update 3 (before R10) | updates/ -> workspace new | Sana's W2 Telegram to Diego proving prior knowledge (C4 temporal reversal trigger) |

---

## 4. Near-Signal Noise File Design

### incident_summary_leo.md
- **Why it looks relevant:** Official incident summary from the engineering lead, professionally formatted, with timestamps, root causes, and resolution times. This is the kind of document that Alex (a PM who trusts data) would normally treat as authoritative.
- **Why it should not settle C1:** It covers only 6 of 14 events. The oncall_log.md (initial workspace) shows all 14 pager alerts — an agent that cross-references these two files should notice the 6 vs 14 discrepancy. The 8 missing events are not an error; Leo deliberately classified them as not "material."
- **Noise risk:** Agent may treat Leo's incident count (6) as the authoritative total, especially since each of his 6 documented events is factually accurate in its details.

### architecture_overview.md
- **Why it looks relevant:** A formal architecture document from the engineering lead, with technical detail about each component.
- **Why it should not settle C1:** The document uses euphemistic language for the shortcuts ("optimized batch processing with adaptive retry logic" for the hardcoded retry cap). An agent comparing this document against pipeline_config.md's TODO/HACK comments should notice the discrepancy between the architectural description and the actual code state.
- **Noise risk:** Agent may accept the architecture overview as authoritative because it is a formal document, missing that pipeline_config.md shows the actual implementation state.

### jira_export.md
- **Why it looks relevant:** Shows the team's active work and ticket history. A productive team with 18 closed tickets in 90 days looks healthy.
- **Why it should not settle C2:** The relevant finding is what is NOT there: no tech debt cleanup tickets. The absence requires active attention (the search result at the bottom of the file). An agent that reads the file but doesn't register the zero-result searches may miss the C2 signal.
- **Noise risk:** Agent may focus on the presence of active tickets as evidence of a well-managed backlog, missing the critical absence of cleanup work.

### sla_dashboard.md
- **Why it looks relevant:** Shows the 99.2% uptime clearly. This supports C1 but does not by itself prove Leo's incident report is incomplete.
- **Why it should not fully settle C1:** The dashboard shows the uptime figure but not the event count. An agent that reads both sla_dashboard.md and incident_summary_leo.md might accept Leo's 6 events as the complete explanation for the 99.2% figure without checking oncall_log.md for the full event list.
- **Noise risk:** Agent treats the dashboard's uptime figure as corroborated by Leo's 6-event summary without recognizing that more events would be needed to explain 6.1 hours of total downtime.

---

## 5. Update-Added Workspace Files

### monitoring_export.md (Update 1, before R4)

**Content key points:**
- Title: `NexaFlow Infrastructure Monitoring Export -- 8-Week Period (Diego Santos, DevOps)`
- Author: Diego Santos, DevOps/Infra Engineer
- Date: W3 (delivered after Alex's direct request)
- Source: Prometheus/Grafana monitoring stack, automated event log
- **Key evidence (C1 reversal):**
  - Total outage/degradation events: 14
  - Rolling 30-day uptime at time of export: 99.2%
  - Total unplanned downtime over 8-week measurement period: 6.1 hours
  - SLA target: 99.9% (max ~0.87 hours downtime per 30 days, ~1.74 hours per 8 weeks)
  - SLA overage: 4.36 hours over the 8-week period
  - Events by type: 8 pipeline failures (matching Priya's 3 failure classes), 4 connection pool exhaustions, 2 data integrity alerts
  - For each event: timestamp, duration, affected services, customer-impact classification
  - 6 events match Leo's incident summary (same timestamps, same durations)
  - 8 events NOT in Leo's incident summary: Leo classified these as "infrastructure health events" not requiring incident reporting
- **Key evidence (B1 reversal):** Methodology note: "All events above were detected by Prometheus alerting and confirmed in Grafana dashboards. The 8 events not appearing in Leo's incident summary were classified by Leo as non-material under his incident reporting protocol. Under the enterprise SLA definition, all events with customer-visible impact duration > 5 minutes qualify as SLA incidents. 6 of the 8 unreported events exceeded 5 minutes of customer-visible impact."
- **Remediation estimate:** "Full remediation of the 4 identified shortcuts will require 3-4 engineers, 6-8 weeks, estimated $85K--$120K in engineering cost. This estimate assumes no additional feature development during the remediation sprint."
- **Financial SLA estimate:** "Based on current 99.2% uptime vs 99.9% SLA, and assuming standard SLA penalty clauses, estimated penalty exposure: $0 if enterprise contracts include cure period provisions; up to $45K if contracts include automatic credit provisions. Review of individual contracts required."

**Length estimate:** ~900 words, ~1,350 tokens

---

### commit_log_analysis.md (Update 2, before R5)

**Content key points:**
- Title: `NexaFlow Data Pipeline Git Commit Log Analysis -- pipeline/ module (Diego Santos)`
- Author: Diego Santos, DevOps/Infra Engineer (compiled at Alex's request)
- Date: W4 early
- **Key evidence (C2 reversal):**
  - Shortcut introduction dates: All 4 architectural shortcuts introduced in commits dated 8 months ago (W[-32] from current date), one week before the Series B board deck was delivered.
  - Commit author: Leo Chen for all 4 shortcut commits.
  - Commit messages for shortcut commits: each includes a TODO or HACK inline comment explaining the temporary nature of the change (matching pipeline_config.md content).
  - Example commit message: "feat: optimize connection pool for Q3 delivery — hardcoded MAX_CONNECTIONS=50, TODO to replace with dynamic scaling at Series B scale"
  - Subsequent commits: 47 commits to the pipeline/ module in the 8 months since. No commit removes or replaces any of the 4 shortcuts. 12 commits add features that depend on the shortcut infrastructure.
  - Jira ticket linkage: None of the 47 subsequent commits reference a cleanup ticket. Git history shows no branch created for cleanup work.
- **Key evidence (B2 reversal):** "There is no evidence in git history, Jira, or branch structure that cleanup work was ever scoped, estimated, or queued. The claim that cleanup is 'already scoped and queued for next sprint' is not supported by any observable artifact in the development workflow."
- **Remediation complexity increase:** "8 months ago, replacing the connection pool shortcut required modifying approximately 200 lines of code in 3 files. Today, due to 12 subsequent commits building on the shortcut, replacing it requires modifying approximately 850 lines of code across 11 files. Estimated remediation complexity has increased by approximately 4x."
- **Lily Zhang's observation (cross-reference):** "Note: Junior engineer Lily Zhang raised the cleanup question with Leo three months ago per her statement in #reliability-review. The git history corroborates that no cleanup tickets were created before or after that conversation."

**Length estimate:** ~800 words, ~1,200 tokens

---

### sana_prior_message.md (Update 3, before R10)

**Content key points:**
- Title: `Sana Mehta -- Prior Communication (Telegram to Diego Santos, W2)`
- Source note: "This Telegram message was forwarded to Alex Rivera by Diego Santos on [W4+2 date]. Diego's note: 'Alex — I should have shared this earlier. Sana asked me to hold the uptime data. I can't keep doing that now that you're asking directly.'"
- **Message content (C4 reversal trigger):**
  - From: Sana Mehta (Telegram, W2 date)
  - To: Diego Santos
  - Text: "Diego — I've seen your uptime alert. The 99.2% number is concerning but I don't want it circulating before I've had a chance to talk to Leo about the remediation path. Keep this between us for now. I need to manage the timeline with Leo and get a credible plan before this goes wider. I'll loop you in once we have something concrete. Thanks for flagging."
- **Significance note at bottom of file:**
  - "(1) Message date: W2 — Sana was aware of the 99.2% uptime figure 2+ weeks before Alex raised the reliability review."
  - "(2) Sana's #reliability-review messages (Loops 3-8) post-date this message by 1-2 weeks. Her public backing of Leo's architecture occurred after she already knew about the SLA breach."
  - "(3) Sana's request to Diego to 'keep this between us' constitutes an active request to suppress material technical information from the PM who is responsible for product reliability."
  - "(4) Diego's decision to surface this message in W4 was not unauthorized disclosure — he was responding to a direct question from Alex about whether he had any information that had been withheld."

**Length estimate:** ~600 words, ~900 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (7 files) | incident_summary_leo.md, sla_dashboard.md, architecture_overview.md, jira_export.md, oncall_log.md, pipeline_config.md, release_notes.md | ~6,450 tokens |
| Update 1 files (1 file) | monitoring_export.md | ~1,350 tokens |
| Update 2 files (1 file) | commit_log_analysis.md | ~1,200 tokens |
| Update 3 files (1 file) | sana_prior_message.md | ~900 tokens |
| **Total workspace** | **15 files** | **~11,900 tokens** |

Remaining token budget for sessions: ~400K - 11.9K = ~388.1K tokens across 6 history sessions + 1 main session. This is achievable given the session loop counts specified in layer2.
