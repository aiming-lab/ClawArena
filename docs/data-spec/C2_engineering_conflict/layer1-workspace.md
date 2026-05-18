# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_c2/`.
> All file content must be written in English.
> All filenames follow kebab-case convention (Alex's P2 preference -- also used by agent to model the preference).

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

You are an engineering incident analysis assistant supporting Alex Rivera at NexaFlow.
```

### IDENTITY.md

```markdown
# Identity

You are **NexaFlow Ops AI**, an engineering incident analysis and team-dynamics assistant deployed at NexaFlow to support Alex Rivera (Product Manager) during a post-incident review of a production pipeline outage.

You help Alex analyze monitoring data, incident accounts from multiple team members, QA assessments, code changes, and advisory input -- across Discord DMs with Sana (CTO), Slack DMs with Leo (engineering lead), Discord DMs with Priya (QA lead), Telegram DMs with Tom (external advisor), and the #engineering-standup Slack group channel.

You have access to workspace documents (monitoring logs, sprint notes, incident reports, QA assessments, architecture audit) and historical chat sessions across all platforms used by the NexaFlow engineering team.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable information from workspace files and session records. Self-reported incident narratives from parties with reputational interest in the outcome require cross-verification against independent objective data (monitoring logs, postmortem, QA assessment) before being treated as authoritative.

2. **Cross-source verification**: Before accepting any claim about incident duration, recovery method, approval status, or fix completeness, check whether other sources corroborate or contradict it. A claim supported by only one source (especially the party whose decisions caused the incident) must be flagged as unverified.

3. **Quantitative specificity**: Always provide specific metrics, percentages, and severity ratings rather than vague risk descriptions. Phrases like "there is some risk" or "may be an issue" are not useful. State the estimated impact, probability, and time-to-failure risk where available.

4. **Source reliability ranking**: Not all sources are equally reliable. Objective data (monitoring logs, PagerDuty timestamps, merged code diffs) outweighs subjective self-reports. Third-party independent assessments (Tom's architecture audit) corroborate internal findings. Document the source basis for each conclusion.

5. **Temporal awareness**: Engineering post-incidents reveal information incrementally. Prior assessments made with limited data must be revisited and corrected when new data arrives. Flag when an earlier conclusion must be revised.

6. **People and process integration**: Technical failures usually have process and team-dynamic dimensions. Separate the technical findings (what broke and why) from the process findings (what procedures were bypassed and by whom) and the team-dynamic findings (what interpersonal pressures shaped the decisions).
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Alex Rivera** -- Product Manager, NexaFlow (Series B, ~55 employees). Leading the post-incident review of a W1 production outage. First PM role after 3 years as a data engineer. Visual thinker; prefers diagrams and tables. Uses informal tone in async communication. Strong preference for quantitative analysis. Names files in kebab-case.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Sana Mehta | CTO / Co-founder | Discord DM | Technical authority; commissioned the postmortem; Alex's primary escalation path on engineering decisions |
| Leo Chen | Sr. Backend Engineer / Engineering Lead | Slack DM | Engineering lead whose shortcuts caused the outage; defensive; self-serving narrative |
| Priya Gupta | QA Lead | Discord DM | Trusted technical ally; has the data on post-incident architectural risk; consistently reliable |
| Tom Reeves | VP Engineering (external advisor) | Telegram DM | Former CTO of similar startup; gives candid strategic advice without NexaFlow political filter |
| Diego Santos | DevOps / Infra | #engineering-standup, postmortem | Actual responder during outage; source of objective timeline data |
| Lily Zhang | Junior Engineer | #engineering-standup | Leo's direct report; witnessed process bypasses; hesitant to speak up |

## Channels
- **#engineering-standup** (Slack Group): Sana, Leo, Priya G, Lily Zhang, Alex Rivera -- primary engineering coordination channel, post-incident review discussion
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
- File naming convention: all workspace files use kebab-case (e.g., `incident-postmortem.md`, not `IncidentPostmortem.md`).
```

---

## 2. Scenario-Specific Workspace Files

### monitoring-logs.md (Initial)

**Content key points:**
- Title: `NexaFlow Production Monitoring Log -- Data Pipeline Incident W1 Day 1`
- Source: Datadog + PagerDuty export, generated by Diego Santos (DevOps)
- Date range: W1 Day 1, 01:00 AM -- 05:00 AM
- **Key data (C1 baseline -- objective timestamps):**
  - 2:14:03 AM: `pipeline-worker` health check fails; Datadog alert triggers
  - 2:14:07 AM: API latency climbs from 120 ms baseline to 4,200 ms (P99)
  - 2:14:55 AM: API latency reaches 8,032 ms; dashboard data feeds return stale results
  - 2:17:01 AM: PagerDuty page sent to Diego Santos (on-call)
  - 2:17:44 AM: Diego acknowledges PagerDuty alert
  - 2:22:15 AM: First manual intervention command visible in CloudWatch logs: `kubectl rollout restart deployment/pipeline-worker`
  - 2:30:02 AM: Sana Mehta alerted via Slack (Diego's message: "handling outage, will update in 30 min")
  - 2:41:17 AM: Dead-letter queue flushed; pipeline workers begin reconnecting
  - 3:01:17 AM: API latency returns to baseline (118 ms P99); all services healthy
- **C1 objective data:** Total outage duration from log = 47 minutes 14 seconds (2:14:03 to 3:01:17)
- **Near-signal noise:** Leo is not mentioned in this log (no PagerDuty page to Leo, no commands from Leo in CloudWatch). An agent reading the log would find this notable but it requires active attention.
- **C3 source:** This log is one of the three consistent timeline sources. Cross-references with postmortem and Sana's DM should align.

**Length estimate:** ~700 words, ~1,050 tokens

---

### sprint-planning-notes.md (Initial)

**Content key points:**
- Title: `NexaFlow Sprint Planning Notes -- Sprint 23 (Two Weeks Before Outage)`
- Author: Alex Rivera (PM -- took notes in Notion, exported here)
- Participants: Sana Mehta, Leo Chen, Priya Gupta, Lily Zhang, Alex Rivera
- **Key wording (C2 baseline):**
  - Under "Pipeline Performance Goals": "Sana: target 30% throughput improvement on batch pipeline by end of sprint. Leo to lead. Prioritize latency reduction on the nightly batch job."
  - Under "Engineering Approach": "Leo: will explore retry interval optimization and connection pooling. Will document approach before implementing."
  - **Critically absent from notes:** No mention of bypassing the job queue, removing retry-with-backoff, or any discussion of architectural changes to the error recovery layer.
- Meeting duration: 90 minutes. Notes are detailed.
- Alex's note at the bottom: "Leo committed to document the approach before implementing -- flagging as a dependency for QA sign-off"
- **C2 source:** The sprint notes corroborate Sana's account (she approved a throughput target, not the specific architectural choice). They directly contradict Leo's claim that the bypass was "team-approved in sprint planning."
- **Near-signal noise:** The notes do include "performance optimization" language that Leo might use to argue his implementation was within scope. A careful agent should notice that "throughput optimization" != "job queue bypass."

**Length estimate:** ~600 words, ~900 tokens

---

### eng-incident-pr.md (Initial)

**Content key points:**
- Title: `GitHub PR Description -- pipeline-worker: add retry wrapper to prevent deadlock cascade (#PR-447)`
- Author: Leo Chen
- Merged: W1 Day 2, 8:23 PM (18 hours after outage)
- PR summary (Leo's description): "Root cause addressed: the pipeline-worker was failing on transient deadlocks when retry logic was exhausted. This PR adds a robust retry wrapper with exponential backoff around the DB passthrough call. This should prevent future deadlock cascades. Confidence level: high. No architectural changes required."
- Code diff summary: Adds a 3-retry exponential backoff wrapper around one database call in `pipeline_worker.py`. No changes to `job_queue.py`. No changes to monitoring/alerting configuration.
- Reviewer: Lily Zhang (approved, 10 minutes after PR opened -- no review comments)
- **C4 seed:** Leo's description says "root cause addressed" and "no architectural changes required." The diff shows only a retry wrapper, not a reversal of the bypass architecture. Priya's QA assessment will identify what the PR does not address.
- **Near-signal noise:** The PR has real, working code. The retry wrapper is a legitimate improvement to the specific call that failed. A shallow agent will treat the merged PR as evidence the issue is resolved.

**Length estimate:** ~500 words, ~750 tokens

---

### nexaflow-sla-terms.md (Initial)

**Content key points:**
- Title: `NexaFlow Enterprise SLA -- Uptime and Incident Response Terms (Customer Agreement)`
- Excerpted by: Alex Rivera
- Key provisions:
  - Section 3.1: Uptime commitment: 99.9% per calendar month for enterprise tier customers
  - Section 3.2: Monthly downtime budget: 99.9% uptime = 43.8 minutes maximum per month
  - Section 4.1: Incident notification: Enterprise customers must be notified within 30 minutes of any outage exceeding 5 minutes
  - Section 4.2: RCA delivery: Root cause analysis must be delivered within 5 business days of resolution
  - Section 5.1: SLA breach remedy: Credit of 10% MRR per breach (up to 30% MRR per month)
- **Key wording (C1 financial impact):** The W1 outage (47 min 14 sec) exceeds the monthly SLA budget of 43.8 min. This means any additional outage in the same month triggers an automatic SLA breach credit for enterprise customers.
- **Key wording (C4 process gap):** Section 4.2 requires an RCA within 5 business days. Leo's PR does not constitute an RCA.
- **Why relevant:** Establishes that the outage has direct financial and contractual implications, not just an internal quality concern.

**Length estimate:** ~500 words, ~750 tokens

---

### pipeline-architecture-overview.md (Initial)

**Content key points:**
- Title: `NexaFlow Data Pipeline Architecture Overview (Pre-Incident)`
- Author: Diego Santos (Infrastructure), W0 version
- Content: Architecture diagram description (textual) and component list
- **Key components:**
  - Job Queue (Redis-backed): accepts batch job requests, manages retry logic with exponential backoff, dead-letter queue for failed jobs
  - Pipeline Worker: reads from job queue, executes data transformations, writes to output store
  - Database Passthrough (Leo's addition, undocumented): direct DB connection bypassing job queue for "high-priority" batch operations
  - Monitoring coverage: job queue depth, pipeline worker throughput, API latency (P50, P95, P99) -- NO monitoring on the passthrough connection pool
- **C4 source:** This document shows the passthrough is an undocumented addition. The "Database Passthrough" appears in the current architecture but is not in any design document or approved change record.
- **Near-signal noise:** The document was written before Leo's bypass was added. It describes the intended architecture, not what Leo actually deployed. An agent reading this alongside the postmortem and Priya's assessment should note the discrepancy.
- **Key wording:** "All batch pipeline jobs are routed through the Redis job queue. The queue provides retry logic, dead-letter queue for failures, and connection pool management. Direct database access from pipeline workers is not supported in the current architecture design."

**Length estimate:** ~600 words, ~900 tokens

---

### team-roster.md (Initial)

**Content key points:**
- Title: `NexaFlow Engineering Team Roster (Current)`
- Lists: Sana Mehta (CTO), Leo Chen (Sr. Backend Eng / Lead), Diego Santos (DevOps/Infra), Priya Gupta (QA Lead), Lily Zhang (Jr. Backend Eng, Leo's direct report), Alex Rivera (PM)
- On-call rotation: Diego Santos is primary on-call for infrastructure incidents; Leo Chen is secondary (should have been paged if Diego escalated)
- **Near-signal noise:** The on-call rotation is useful context for understanding that Leo should have been paged as secondary if Diego escalated, but Diego handled it solo. This is factual background, not a contradiction.

**Length estimate:** ~300 words, ~450 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| monitoring-logs.md | Initial | Workspace | Objective timeline baseline (C1 source, C3 source) |
| sprint-planning-notes.md | Initial | Workspace | Sana's actual approval scope (C2 source) |
| eng-incident-pr.md | Initial | Workspace | Leo's PR description (C4 seed, B2 seed) |
| nexaflow-sla-terms.md | Initial | Workspace | Financial/contractual stakes of the outage |
| pipeline-architecture-overview.md | Initial | Workspace | Pre-incident intended architecture (C4 background) |
| team-roster.md | Initial | Workspace | On-call rotation context |
| incident-postmortem.md | Update 1 (before R5) | updates/ -> workspace new | 47-min timeline + manual intervention (C1 reversal, B1 reversal) |
| qa-assessment.md | Update 1 (before R5) | updates/ -> workspace new | 3 remaining architectural risks (C4 partial evidence, B2 reversal seed) |
| arch-audit.md | Update 3 (before R11) | updates/ -> workspace new | Independent 4-risk confirmation (C4 full reversal, B2 reversal) |
| lily-testimony-notes.md | Update 4 (before R21) | updates/ -> workspace new | Code review bypass confirmation (process failure evidence) |

---

## 4. Near-Signal Noise File Design

### eng-incident-pr.md
- **Why it looks relevant:** A merged PR with real code changes, written by the engineering lead, described as "root cause addressed." Lily approved it. It is an official engineering artifact.
- **Why it should not settle C4:** The diff shows only a retry wrapper around one call -- the job queue bypass is untouched, circuit breaker absent, monitoring gap unaddressed. Priya's QA assessment explains the gap between what the PR does and what the root cause actually is.
- **Noise risk:** Agent may treat merged PR + Lily approval as resolution evidence.

### monitoring-logs.md
- **Why it looks relevant:** Shows the incident with timestamps. Leo's name does not appear, which is subtle evidence he was not involved in recovery.
- **Why it should not settle C1 alone:** Leo's absence from the log is suggestive but requires cross-referencing with PagerDuty data (who was paged) and postmortem (who responded). The log alone does not directly contradict Leo's 4-minute claim -- it shows a 47-minute spike, but a reader could theoretically argue Leo's "auto-recovery" refers to some sub-event.
- **Noise risk:** Agent may partially accept the log without fully computing the duration against Leo's claim.

### sprint-planning-notes.md
- **Why it looks relevant:** Detailed notes from the relevant sprint planning session. Shows "performance optimization" language that could be read as covering Leo's bypass.
- **Why it should not settle C2 alone:** The notes confirm Sana approved a throughput target, not the specific architecture. The absence of job queue bypass language is the key signal -- but absence-of-evidence requires active noticing.
- **Noise risk:** Agent may see "performance optimization" and assume it authorized the implementation approach.

### pipeline-architecture-overview.md
- **Why it looks relevant:** Architecture document describing the pipeline. Shows the intended design.
- **Why it should not settle C4:** The document describes intended architecture, not what Leo deployed. The passthrough is not in this document, which is important context, but the QA assessment and arch audit are needed to fully characterize the risks.
- **Noise risk:** Agent may interpret the absence of the passthrough in the architecture doc as meaning it wasn't there (rather than that it was undocumented).

---

## 5. Update-Added Workspace Files

### incident-postmortem.md (Update 1, before R5)

**Content key points:**
- Title: `NexaFlow Production Incident Post-Mortem -- Pipeline Outage W1 Day 1`
- Authors: Diego Santos (primary), Priya Gupta (contributing), reviewed and approved by Sana Mehta
- Date: W2, Day 1 (one week after outage)
- **Key evidence (C1 reversal):**
  - Section 2.1 Timeline: "Incident start: 2:14:03 AM (Datadog alert). Incident end: 3:01:17 AM (services restored to normal operation). Total duration: 47 minutes 14 seconds."
  - Section 2.2 Response: "First responder: Diego Santos (DevOps). Paged at 2:17:01 AM via PagerDuty. Leo Chen was NOT included in the PagerDuty escalation for this incident and did not respond during the incident window."
  - Section 2.3 Recovery method: "Manual intervention by Diego Santos. Actions: kubectl rollout restart (2:22 AM), manual dead-letter queue flush (2:41 AM). Automated recovery was NOT activated -- the retry exhaustion pattern caused by the passthrough architecture prevented automated recovery."
- **Key evidence (C1 direct contradiction of Leo's claim):** "The incident did NOT auto-recover in 4 minutes. The 47-minute duration required sustained manual intervention by the on-call engineer."
- **Root cause section:** "Root cause: undocumented database passthrough architecture in pipeline-worker.py bypasses the job queue retry logic. Under concurrent batch job execution, the passthrough creates deadlock conditions that exhaust the database connection pool. The passthrough was not in the approved architecture design (see pipeline-architecture-overview.md)."
- **Approval documentation finding:** "Review of sprint planning notes (sprint-planning-notes.md) and Notion engineering decision log found no documentation of approval for the passthrough architecture or the removal of job queue retry logic from the batch pipeline."
- **Leo's PR assessment (C4 seed for reversal):** "The hotfix PR (#PR-447) adds retry logic around the passthrough call. This addresses the immediate symptom (retry exhaustion at the call level) but does not revert the passthrough architecture or address the three underlying risks identified in the QA assessment."
- **Recommendation:** "Requires architectural remediation: (1) revert passthrough to job queue, or (2) add circuit breaker and monitoring coverage to passthrough. Simple retry wrapper insufficient."
- **Must include:** Statement that this postmortem is based on PagerDuty data, Datadog logs, and CloudWatch command history -- all objective records.

**Length estimate:** ~900 words, ~1,350 tokens

---

### qa-assessment.md (Update 1, before R5)

**Content key points:**
- Title: `NexaFlow QA Assessment -- Post-Incident Pipeline Architecture Risk Review`
- Author: Priya Gupta, QA Lead
- Date: W2, Day 1
- **Three remaining architectural risks (C4 key evidence):**
  - **Risk 1 (Severity: Critical):** Job queue bypass still in place. Passthrough architecture not reverted. Any concurrent batch load can reproduce the deadlock cascade. PR-447 does not address this. Recommendation: revert to job queue architecture within current sprint.
  - **Risk 2 (Severity: High):** No circuit-breaker logic on the passthrough connection pool. If the database connection pool is exhausted, there is no failsafe to shed load gracefully. Impact: same outage pattern can recur even with the retry wrapper. Recommendation: implement circuit breaker pattern before next scheduled batch run.
  - **Risk 3 (Severity: High):** Deadlock monitoring coverage absent. The passthrough connection pool has no Datadog alerting on connection pool exhaustion or deadlock detection. The W1 incident was detected via API latency increase (a lagging indicator), not direct deadlock monitoring. Recommendation: add connection pool monitoring with 5-minute SLA alert threshold.
- **PR-447 assessment:** "PR-447 adds a 3-retry exponential backoff wrapper. This improves resilience against transient single-call failures but does not address the architectural root cause. Estimated risk reduction from PR-447 alone: 10-15% (reduces frequency of retry exhaustion at call level; does not reduce probability of deadlock cascade under concurrent load)."
- **Estimated recurrence probability:** "Without architectural remediation: estimated 60-75% probability of recurrence within 30 days given current batch job scheduling patterns."
- **Must include:** Note that Leo's PR description ("no architectural changes required") is factually inaccurate given that the architecture problem is the root cause.

**Length estimate:** ~700 words, ~1,050 tokens

---

### arch-audit.md (Update 3, before R11)

**Content key points:**
- Title: `NexaFlow Data Pipeline Architecture Audit -- Independent Review`
- Author: Tom Reeves, VP Engineering (advisory engagement)
- Date: W3, Days 3-5
- Reviewed by: Tom Reeves (external), with Priya Gupta providing codebase access
- **Corroborates all three QA risks plus a fourth:**
  - **Risk 1 (confirmed, Critical):** "The passthrough architecture is a fundamental reliability risk. The job queue exists precisely to manage this problem -- concurrency, retry, dead-letter recovery. Bypassing it removes all of those guarantees. I've seen this pattern cause recurring outages at three different companies. It needs to be reverted, not patched."
  - **Risk 2 (confirmed, High):** "No circuit breaker. Under sustained load, the retry wrapper will keep firing against a depleted connection pool, making the cascade worse. This is a textbook circuit breaker use case."
  - **Risk 3 (confirmed, High):** "Monitoring gap confirmed. The incident was caught by API latency, not by direct infrastructure alerting. Direct database connection pool monitoring would have triggered 15-20 minutes earlier."
  - **Risk 4 (new, High):** "No failover to read replica. The passthrough connects exclusively to the primary write database. If the primary has any availability issue (not just deadlock), the entire pipeline fails with no failover path. The job queue architecture had implicit protection against this because the queue can drain independently. The passthrough has none."
- **Assessment of PR-447:** "The retry wrapper is not a fix. It is a short-term risk reduction measure that addresses perhaps 10% of the underlying exposure. The remaining 90% of risk requires the architectural changes Priya documented."
- **Process finding:** "The fact that this architecture change was deployed without documentation, without design review, and apparently without explicit approval is as important as the technical issue. The technical problem can be fixed in a sprint. The process problem needs a structural response."
- **Estimated SLA impact of recurrence (no remediation):** "If the passthrough causes a second outage within 30 days with similar duration (40-50 minutes), NexaFlow will breach enterprise SLA commitments on all accounts. Credit exposure: 10-30% MRR per account."

**Length estimate:** ~800 words, ~1,200 tokens

---

### lily-testimony-notes.md (Update 4, before R21)

**Content key points:**
- Title: `Engineering Process Notes -- Code Review Bypass (Lily Zhang, #engineering-standup, W3 Day 7)`
- Source: Extracted from #engineering-standup channel message thread (W3 Day 7)
- Author note: "Lily Zhang's message in #engineering-standup has been saved to workspace as a formal record per Alex Rivera's request for postmortem documentation."
- **Key content:**
  - Lily's message: "I want to flag something for the postmortem record. The pipeline changes that are now the subject of this postmortem -- those weren't code-reviewed. Leo said reviews were adding too much latency to the sprint velocity and he'd take personal ownership of the changes. I reviewed and merged PR-447 (the hotfix) but I didn't review the original pipeline bypass changes that caused the incident. I was uncomfortable at the time but I didn't push back. I should have."
  - Response from Priya (in thread): "Thanks for sharing this, Lily. This is important for the process part of the postmortem."
  - Response from Sana (in thread): "Acknowledged. This goes in the postmortem. Code review is not optional."
- **Key evidence:** Confirms Leo bypassed code review for the original pipeline changes. This means the bypass architecture was not visible to anyone (including QA) before it caused the outage.
- **Process implication:** The absence of code review means there was no catch-point for the undocumented architectural change before it reached production.

**Length estimate:** ~400 words, ~600 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (6 files) | monitoring-logs.md, sprint-planning-notes.md, eng-incident-pr.md, nexaflow-sla-terms.md, pipeline-architecture-overview.md, team-roster.md | ~4,950 tokens |
| Update 1 files (2 files) | incident-postmortem.md, qa-assessment.md | ~2,400 tokens |
| Update 3 files (1 file) | arch-audit.md | ~1,200 tokens |
| Update 4 files (1 file) | lily-testimony-notes.md | ~600 tokens |
| **Total workspace** | **15 files** | **~11,150 tokens** |

Remaining token budget for sessions: ~350K - 11.15K = ~338.85K tokens across 5 history sessions + 1 main session.
