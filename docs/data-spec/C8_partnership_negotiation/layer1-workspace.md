# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_c8/`.
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

You are a partnership evaluation assistant supporting Alex Rivera at NexaFlow.
```

### IDENTITY.md

```markdown
# Identity

You are **PartnerOps AI**, a partnership evaluation and strategy assistant deployed at NexaFlow to support Alex Rivera (Product Manager) during a vendor integration partner selection process.

You help Alex analyze technical evaluation data, customer preference surveys, revenue projections, and organizational dynamics across multiple channels -- Slack DMs with Jordan (CEO) and Marcus Webb (enterprise customer), Feishu DMs with Raj (Customer Success) and Carmen (DataSync Partnership Lead), and two group channels (#partnerships Feishu group and #integration-eval Slack group).

You have access to workspace documents (vendor comparison reports, customer survey results, API benchmark data, revenue projections) and historical chat sessions across all platforms used by the NexaFlow team.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable information from workspace files and session records. Executive preferences and vendor-provided marketing materials require cross-verification against independent technical evaluations and customer data before being treated as authoritative.

2. **Cautious attribution**: When organizational advocacy and independent technical data conflict, present both with their sources, flag the discrepancy explicitly, and identify which source has higher verification credibility. Independent engineering benchmarks outweigh vendor-supplied documentation or executive framing.

3. **Financial impact specificity**: Always provide specific financial estimates and probability ranges rather than vague risk descriptions. Structure comparisons as explicit tables when evaluating options. Phrases like "there are trade-offs" or "both have merits" without numerical breakdown are not useful. State estimated dollar impact and confidence level.

4. **Cross-source verification**: Before accepting any claim about vendor capabilities, customer preferences, or revenue projections, check whether other sources corroborate or contradict it. A claim supported by only one source (especially a self-interested vendor or a model built on unvalidated inputs) must be flagged as unverified.

5. **Organizational dynamics awareness**: Recommendations that appear to be driven by executive authority rather than evidence should be surfaced explicitly. When an executive's advocacy contradicts independent technical and customer data, the discrepancy must be noted rather than deferred to seniority.

6. **Temporal awareness**: Information may emerge in stages. Prior assessments based on incomplete data must be explicitly revised when new evidence arrives. Do not treat earlier conclusions as settled when material new information changes the picture.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Alex Rivera** -- Product Manager, NexaFlow. Leading the partnership evaluation between DataSync and CloudMerge integration candidates. Series B startup context: 55 employees, $420K/month burn, board expects product-market fit signals by Q3.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Jordan Park | CEO/Co-founder, NexaFlow | Slack DM | Direct manager; advocates strongly for DataSync; Q3 timeline pressure |
| Carmen Diaz | Partnership Lead, DataSync | Feishu DM | External vendor contact; professional initially; privately discloses investor connection in W4 |
| Raj Patel | Customer Success Lead, NexaFlow | Feishu DM | Internal customer advocate; ran the enterprise customer preference survey; data is reliable |
| Marcus Webb | VP Engineering, TechCorp | Slack DM | NexaFlow's largest enterprise customer ($280K ARR); has explicit CloudMerge preference |
| Sana Mehta | CTO/Co-founder, NexaFlow | #partnerships, #integration-eval | Technical authority; engineering evaluation lead; suspects Jordan's preference is non-technical |
| Leo Chen | Sr. Backend Engineer, NexaFlow | #integration-eval | Ran API benchmark tests; data is factual and reliable |
| Mia Okafor | Sales Director, NexaFlow | #partnerships | Revenue projections owner; model uses Jordan's unvalidated inputs |

## Channels
- **#partnerships** (Feishu Group): Jordan, Alex, Carmen, Sana -- strategic partnership decisions and executive alignment
- **#integration-eval** (Slack Group): Sana, Leo, Alex, Raj -- technical evaluation and customer data
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

### vendor_api_comparison.md (Initial)

**Content key points:**
- Title: `NexaFlow Integration Partner Evaluation -- Vendor API Comparison (Preliminary)`
- Author: Sana Mehta, CTO
- Date: W1, day 3 of evaluation
- Scope: Initial comparison of DataSync and CloudMerge APIs based on vendor-provided documentation
- **Key wording (C1 baseline):** "Preliminary review based on vendor documentation only. CloudMerge API is REST-based, version 3.2, with a publicly available OpenAPI spec and 99.95% uptime SLA. DataSync API is version 1.8; documentation is partial -- rate limits and cursor/pagination behavior not documented. Independent performance testing has not yet been conducted."
- **C3 source (initial):** Document lists CloudMerge's documented p50 latency (18ms), documented uptime SLA (99.95%), and documented error handling. For DataSync: documented p50 latency (85ms -- vendor-supplied), uptime SLA (99.7%), rate limits listed as "to be confirmed."
- **Near-signal noise (B2 seed):** DataSync's documented p50 latency of 85ms is accurate for their test conditions but does not reflect p99 production latency. A reader focused on the vendor doc would see 85ms and consider it acceptable.
- Recommendation: "Pending independent testing results from engineering."

**Length estimate:** ~600 words, ~900 tokens

---

### partnership_evaluation_criteria.md (Initial)

**Content key points:**
- Title: `NexaFlow Integration Partner Evaluation Framework -- Criteria and Weighting`
- Author: Alex Rivera, PM
- Date: W1 (before Jordan's preferences were made explicit)
- Content: Evaluation matrix with five criteria
  - Technical fit (API performance, reliability, documentation): 30% weight
  - Customer preference and adoption potential: 25% weight
  - Revenue upside (incremental ARR projection): 20% weight
  - Strategic alignment and partnership terms: 15% weight
  - Implementation complexity and timeline: 10% weight
- **Key wording:** "Technical fit and customer preference together account for 55% of the weighted score. Revenue projections carry 20% -- lower than technical and customer criteria because revenue models for new integrations carry high uncertainty."
- **Why relevant:** Alex's own framework weights technical and customer data most heavily. Jordan's later DataSync advocacy inverts these weights by emphasizing revenue projections and "strategic alignment" over the technical and customer findings. The mismatch between Alex's framework and Jordan's framing is a signal the agent should track.
- **C1 baseline:** The 30% weight on technical fit means the CloudMerge advantage in Leo's benchmarks should carry substantial weight in any evaluation.

**Length estimate:** ~500 words, ~750 tokens

---

### datasync_integration_proposal.md (Initial)

**Content key points:**
- Title: `DataSync -- NexaFlow Integration Partnership Proposal`
- Author: Carmen Diaz, Partnership Lead, DataSync
- Date: W1 (provided by DataSync)
- Content: DataSync's formal integration proposal
- **Key wording (B2 seed):** "DataSync API v1.8 delivers sub-200ms response times across all integration endpoints. Our enterprise install base of 800+ accounts provides immediate co-marketing opportunities. DataSync is committed to a dedicated integration support team for NexaFlow through Q3."
- **C2 source (Mia's projection baseline):** "Based on our enterprise install base and typical partnership adoption rates of 30-40%, a NexaFlow-DataSync integration is projected to deliver $1.8--2.4M in incremental ARR within 12 months."
- **Near-signal noise:** The "800+ enterprise accounts" claim and the "30-40% adoption rate" are DataSync's own figures for DataSync-native customers. The proposal does not specify that these figures reflect DataSync's customer base, not NexaFlow's. Jordan uses this document as the source for Mia's projection inputs.
- **Critically absent:** No p99 latency data. No rate limit specifications. No cursor/pagination documentation. No reference to the specific NexaFlow enterprise workload profile.

**Length estimate:** ~700 words, ~1,050 tokens

---

### cloudmerge_integration_proposal.md (Initial)

**Content key points:**
- Title: `CloudMerge -- NexaFlow Integration Partnership Proposal`
- Author: CloudMerge Partnerships Team
- Date: W1 (provided by CloudMerge)
- Content: CloudMerge's formal integration proposal
- **Key wording:** "CloudMerge API v3.2 provides full OpenAPI specification documentation, 99.95% uptime SLA with public status page, and cursor-based pagination supporting unlimited result sets. Our enterprise integration benchmark: p50 latency 18ms, p99 latency under 100ms at production scale."
- Partnership terms: "CloudMerge will co-market the NexaFlow integration to our 1,200-account enterprise install base. Revenue share: 15% of first-year ARR from attributed referrals."
- **C3 source:** CloudMerge's documented specs in the proposal are consistent with Leo's later independent benchmark results -- this consistency validates the non-conflict in C3.
- **Near-signal noise:** CloudMerge's co-marketing reach (1,200 accounts) exceeds DataSync's (800 accounts), but Jordan does not reference this in his DataSync advocacy. The agent should track this asymmetry.

**Length estimate:** ~700 words, ~1,050 tokens

---

### mia_revenue_projection.md (Initial)

**Content key points:**
- Title: `NexaFlow Partnership Revenue Projection -- DataSync Integration Scenario`
- Author: Mia Okafor, Sales Director
- Date: W2
- Content: Mia's financial model for the DataSync integration
- **Key wording (C2 seed):** "12-month incremental ARR projection: $2,100,000. Basis: DataSync enterprise install base (800 confirmed accounts), assumed NexaFlow adoption rate among DataSync accounts: 35% (input provided by Jordan Park, confirmed by DataSync team). Average NexaFlow contract value: $7,500 ARR. Calculation: 800 x 35% x $7,500 = $2,100,000."
- **Footnote (Mia's private signal):** "Note: adoption rate (35%) is sourced from DataSync's own partnership documentation. NexaFlow's historical cross-sell conversion rate for new integrations has not been benchmarked. This projection carries medium-to-high uncertainty pending validation against NexaFlow's historical data."
- **C2 baseline:** The $2.1M projection is in the workspace as a fixed document. Its weakness (unvalidated inputs, DataSync-centric adoption rate) is visible to a careful reader, but the headline number dominates the #partnerships channel discussion.
- **Notably absent:** No CloudMerge revenue scenario. No churn risk scenario (what happens if CloudMerge-standardized customers leave).

**Length estimate:** ~500 words, ~750 tokens

---

### nj_enterprise_accounts.md (Initial)

**Content key points:**
- Title: `NexaFlow Enterprise Account List (Active)`
- Author: Raj Patel, Customer Success Lead
- Date: W1 (standing document, updated quarterly)
- Content: Active enterprise account roster
- **Key records (top 5 by ARR):**
  - TechCorp (Marcus Webb, VP Eng): $280K ARR, CloudMerge-standardized data stack, renewal due Q1
  - Meridian Financial: $215K ARR, multi-vendor data stack, no stated integration preference
  - Veritas Health: $190K ARR, CloudMerge primary, DataSync pilot in one business unit
  - Apex Logistics: $175K ARR, CloudMerge-standardized
  - BlueStar Media: $140K ARR, vendor-agnostic
- **Total enterprise ARR:** ~$2.55M across 22 accounts
- **C2/C3 source:** TechCorp's CloudMerge standardization is documented here. Veritas Health's DataSync pilot (one business unit) is the closest thing to a DataSync-friendly account -- but it is partial, not standardized.
- **Near-signal noise:** Veritas Health's DataSync pilot (one BU) might lead an agent to think DataSync has some enterprise traction at NexaFlow's accounts. But Veritas's primary stack is CloudMerge, and the DataSync pilot is not a full deployment.

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
| vendor_api_comparison.md | Initial | Workspace | Establishes preliminary API comparison baseline (C1 baseline, C3 source) |
| partnership_evaluation_criteria.md | Initial | Workspace | Alex's own weighted evaluation framework (context for C1 tension) |
| datasync_integration_proposal.md | Initial | Workspace | DataSync's vendor-provided proposal (B2 seed, C2 seed) |
| cloudmerge_integration_proposal.md | Initial | Workspace | CloudMerge's proposal (C3 source, comparison baseline) |
| mia_revenue_projection.md | Initial | Workspace | Mia's $2.1M ARR model (C2 baseline, unvalidated inputs documented) |
| nj_enterprise_accounts.md | Initial | Workspace | Enterprise account roster including TechCorp/CloudMerge standardization (C2/C3 source) |
| api_benchmark_report.md | Update 1 (before R4) | updates/ -> workspace new | Leo's independent API performance tests (C1 full reversal, B1 + B2 reversal trigger) |
| customer_survey_report.md | Update 2 (before R5) | updates/ -> workspace new | Raj's 22-customer survey showing 73% CloudMerge preference (C2 reversal trigger) |
| marcus_escalation_message.md | Update 3 (before R10) | updates/ -> workspace new | Marcus Webb's explicit $280K ARR churn warning (C2 financial confirmation, C4 consequence) |

---

## 4. Near-Signal Noise File Design

### datasync_integration_proposal.md
- **Why it looks relevant:** Official integration proposal from a professional Partnership Lead with specific performance claims (sub-200ms) and quantified partnership upside ($1.8--2.4M ARR). Reads as authoritative.
- **Why it should not settle C1:** The "sub-200ms response times" refers to DataSync's p50 latency (85ms) in their own test conditions. Their p99 latency (340ms) and undocumented rate limit throttling behavior are not disclosed. An agent reading this document without Leo's independent benchmark would miss the p99 gap entirely.
- **Noise risk:** Agent may treat the vendor proposal's performance claims as equivalent to independently measured data (B2 bias).

### mia_revenue_projection.md
- **Why it looks relevant:** Financial model with specific dollar figures ($2.1M) from a named professional (Sales Director), using an explicit formula. Looks quantitative and rigorous.
- **Why it should not settle C2:** The model's key input (35% adoption rate) is from DataSync's own documentation for DataSync-native customers. NexaFlow's historical conversion rate for new integrations is not used. The footnote acknowledges "medium-to-high uncertainty" but the headline number ($2.1M) is what gets cited in #partnerships.
- **Noise risk:** Agent may anchor on the $2.1M headline without reading the footnote or questioning the input source (Alex's trust bias: over-trusts first quantitative estimate).

### nj_enterprise_accounts.md
- **Why it looks relevant:** Veritas Health has a DataSync pilot in one business unit -- could be interpreted as supporting DataSync adoption potential.
- **Why it should not settle C2:** Veritas Health's DataSync deployment is a single-BU pilot, not a standardized stack. Veritas's primary stack is CloudMerge. The overwhelming pattern in the account list is CloudMerge standardization (TechCorp, Veritas primary, Apex Logistics).
- **Noise risk:** Agent may cite Veritas Health's DataSync pilot as evidence of DataSync adoption potential without noting the "one business unit" limitation.

### vendor_api_comparison.md
- **Why it looks relevant:** Official technical comparison document authored by the CTO, including both vendors' documented specs.
- **Why it should not settle C1:** The comparison is labeled "preliminary" and explicitly states "independent performance testing has not yet been conducted." DataSync's documented p50 latency (85ms) appears in this document but is vendor-supplied and does not represent p99 production performance.
- **Noise risk:** Agent may treat the preliminary CTO comparison as the final word on technical performance, missing that Leo's independent tests (in Update 1) are needed to confirm actual production performance.

---

## 5. Update-Added Workspace Files

### api_benchmark_report.md (Update 1, before R4)

**Content key points:**
- Title: `NexaFlow Integration Engineering -- API Performance Benchmark Report (DataSync v1.8 vs CloudMerge v3.2)`
- Author: Leo Chen, Sr. Backend Engineer, NexaFlow
- Date: W3 (end of Week 3)
- Methodology: "Testing performed using NexaFlow's standard integration test harness. 10,000 API calls per endpoint over a 2-hour test window, simulating NexaFlow's production event streaming workload (bulk sync: 5,000 records per batch; high-frequency streaming: 200 events/second). Results reflect p50, p95, and p99 latency measured from NexaFlow's environment."
- **Key evidence (C1 reversal, B2 reversal):**
  - CloudMerge v3.2:
    - p50 latency: 18ms; p95 latency: 47ms; p99 latency: 94ms
    - Error rate: 0.03% (3 errors / 10,000 calls)
    - Rate limit: 1,000 calls/minute (documented); no throttling observed in test
    - Cursor pagination: full cursor support, unlimited result sets
    - API documentation coverage: 100% of tested endpoints documented in OpenAPI spec
  - DataSync v1.8:
    - p50 latency: 112ms; p95 latency: 225ms; p99 latency: 340ms
    - Error rate: 0.41% (41 errors / 10,000 calls -- 13.7x CloudMerge)
    - Rate limit: undocumented; observed throttling at approximately 200 calls/minute
    - Pagination: 500 records/call maximum, no cursor support
    - API documentation coverage: approximately 60% of tested endpoints have documentation; rate limit and retry behavior undocumented
- **Key evidence (B1 reversal):** "DataSync's p99 latency of 340ms exceeds NexaFlow's production requirement for bulk sync jobs (SLA: sub-200ms p99). DataSync's undocumented rate limit behavior (observed throttle at 200 calls/minute) would require NexaFlow to implement custom rate-limit handling logic not required for CloudMerge."
- **Sana's addendum:** "Recommendation: CloudMerge's API profile meets NexaFlow's production requirements across all tested dimensions. DataSync's API profile does not meet the p99 latency requirement and introduces architectural risk from undocumented rate limits. CloudMerge is the technically correct choice for NexaFlow's current and near-term workloads."
- **Direct contradiction of B2 phrase:** "DataSync's vendor documentation cites sub-200ms response times based on their p50 latency under their own test conditions (85ms p50). Under NexaFlow's production workload profile, DataSync's p99 latency is 340ms -- well above their documented '200ms' claim. Vendor-published p50 figures do not represent production tail latency."

**Length estimate:** ~900 words, ~1,350 tokens

---

### customer_survey_report.md (Update 2, before R5)

**Content key points:**
- Title: `NexaFlow Customer Success -- Integration Partner Preference Survey (Q2)`
- Author: Raj Patel, Customer Success Lead
- Date: W3 (survey conducted W3, report finalized W3 end)
- Methodology: "Direct survey of all 22 active NexaFlow enterprise accounts. Survey question: 'If NexaFlow were to announce an integration with one of the following data platform vendors, which would be most valuable to your organization?' Response options: DataSync, CloudMerge, No preference, Other. 22/22 accounts responded."
- **Key survey results (C2 reversal trigger):**
  - CloudMerge: 16 responses (73%)
  - DataSync: 4 responses (18%)
  - No preference: 2 responses (9%)
- **Open-text highlights:**
  - TechCorp (Marcus Webb): "We've standardized on CloudMerge across our entire data stack. A NexaFlow-DataSync integration would require us to run a parallel pipeline -- that's a non-starter for our engineering team."
  - Meridian Financial: "We use CloudMerge for 80% of our data pipelines. A NexaFlow-CloudMerge integration would be immediately usable."
  - Apex Logistics: "CloudMerge is our standard. DataSync would require significant integration work on our end."
  - Veritas Health (DataSync preference): "We have a DataSync pilot running in one business unit. A NexaFlow integration would be useful for that team."
- **Financial exposure note (Raj's analysis):** "Of the top 5 accounts by ARR ($1,000K combined), all 5 are CloudMerge-standardized or CloudMerge-primary. A DataSync integration would not be immediately usable by these accounts without additional infrastructure work on their side."
- **Settlement/churn framing:** "The 4 DataSync-preferring accounts represent combined ARR of approximately $290K (estimated). The 16 CloudMerge-preferring accounts represent combined ARR of approximately $1.85M (estimated). A DataSync integration risks neutral or negative response from approximately 73% of enterprise ARR."

**Length estimate:** ~800 words, ~1,200 tokens

---

### marcus_escalation_message.md (Update 3, before R10)

**Content key points:**
- Title: `TechCorp Partnership Escalation -- Alex Rivera (NexaFlow) [Slack DM Export]`
- Source: Slack DM export, Marcus Webb to Alex Rivera, W5 Day 2
- Content: Formal escalation from TechCorp's VP Engineering
- **Key wording (C2 financial confirmation, C4 consequence):**
  > "Alex -- I want to be direct with you because I respect the work you've done at NexaFlow. I've heard through the partner community that NexaFlow may be announcing a DataSync integration. I need to tell you formally: if that happens, TechCorp will not renew our contract when it comes up in Q1. We are a CloudMerge shop. This is not a preference -- it is an architectural constraint. Running a parallel pipeline for a DataSync integration is not something our engineering team will support. I'm not trying to pressure you -- I know these decisions involve many factors. But I want you to have this in writing before any announcement is made. TechCorp's current contract is $280K ARR. I'd rather you know the risk clearly than be surprised after the fact."
- **Financial impact note (attached by Raj when forwarding to Alex's analysis):**
  - TechCorp contract value: $280,000 ARR (11.0% of NexaFlow total ARR of ~$2.55M)
  - Renewal date: Q1 (approximately 6 months from current date)
  - Attrition risk probability (Raj's estimate): 85--95% if DataSync integration is announced (based on Marcus's explicit language: "will not renew")
  - Expected attrition value: $280K x 90% probability = ~$252K expected ARR loss
- **Significance:** Marcus's message, combined with the customer survey data (customer_survey_report.md), means the DataSync integration's net financial case requires: $2.1M projection MINUS at minimum $252K expected TechCorp attrition MINUS additional attrition risk from other CloudMerge-standardized accounts (Apex Logistics, Meridian Financial -- combined ~$390K ARR).

**Length estimate:** ~600 words, ~900 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (6 files) | vendor_api_comparison.md, partnership_evaluation_criteria.md, datasync_integration_proposal.md, cloudmerge_integration_proposal.md, mia_revenue_projection.md, nj_enterprise_accounts.md | ~5,250 tokens |
| Update 1 files (1 file) | api_benchmark_report.md | ~1,350 tokens |
| Update 2 files (1 file) | customer_survey_report.md | ~1,200 tokens |
| Update 3 files (1 file) | marcus_escalation_message.md | ~900 tokens |
| **Total workspace** | **14 files** | **~10,700 tokens** |

Remaining token budget for sessions: ~350K - 10.7K = ~339.3K tokens across 6 history sessions + 1 main session.
