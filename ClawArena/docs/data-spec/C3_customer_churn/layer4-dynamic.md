# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R4 | Deliver preliminary usage report (TechCorp + DataBridge) -- seeds C2 partial reversal ("power user" claim contradicted) and supports C1 challenge | Yes: Raj Feishu DM Phase 2 append | Yes: usage_report_v1.md | R3->R5 seed (C2: Mia's "power user" characterization contradicted by sub-5% activation data) |
| U2 | Before R5 | Deliver full usage report (all 3 accounts including Meridian) -- triggers C2 full reversal and B1 reversal | Yes: Mia Slack DM Phase 2 append | Yes: usage_report_v2.md | R2->R4 (C1: feature gap explanation causally impossible); R3->R5 (C2: "power user" definitively false); B1 reversal triggered |
| U3 | Before R8 | Deliver full CS ticket export with timestamps -- completes C3 non-conflict synthesis and supports B2 reversal | Yes: Yuki Slack DM Phase 2 append | Yes: cs_ticket_full_export.md | No new cross-round reversal; completes three-source C3 synthesis; pipeline projection (B2) structurally undermined |
| U4 | Before R9 | Deliver Jordan's private notes revealing pricing strategy admission -- triggers C4 reversal | Yes: #revenue-review Slack Group Phase 2 append | Yes: jordan_private_notes.md | R6->R9 (C4: Jordan's "market conditions" public narrative contradicted by his private pricing diagnosis) |

---

## 2. Action Lists

### Update 1 (before R4)

**Trigger timing:** After R3 answer is submitted, before R4 question is injected.
**Purpose:** Introduces Yuki's preliminary usage analysis covering TechCorp and DataBridge. Shows PipelineSync activation rates of 4.2% and 3.1% respectively -- well below the 40% healthy threshold and directly contradicting Mia's "power user" characterization. TechCorp created zero automated pipelines; DataBridge created two pipelines run three times total. Also appends Raj's Feishu DM Phase 2 where he corroborates the usage findings against his CS ticket evidence and shares Marcus Webb's exit call transcript excerpt. This update seeds C2 reversal and provides C3 timeline evidence.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "usage_report_v1.md",
    "source": "updates/usage_report_v1.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_RAJ_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_RAJ_FEISHU_UUID.jsonl"
  }
]
```

### Update 2 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Introduces the full three-account usage report including Meridian (0% PipelineSync activation, 0 pipelines, 0 runs). Establishes that no churned account was a "power user" -- all three fell in the bottom of the enterprise cohort. Includes the causal note proving that the API rate limit Mia cited was never reached (requires 5+ concurrent pipelines; TechCorp had zero). Also appends Mia's Slack DM Phase 2 showing her narrative pivot from "power users hit feature limits" to "low activation proves the features were inadequate." This update triggers C1 and C2 full reversal and is the B1 reversal trigger.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "usage_report_v2.md",
    "source": "updates/usage_report_v2.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_MIA_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_MIA_SLACK_UUID.jsonl"
  }
]
```

### Update 3 (before R8)

**Trigger timing:** After R7 answer is submitted, before R8 question is injected.
**Purpose:** Introduces the complete CS ticket export with full timestamp data for all three accounts, enabling the C3 non-conflict synthesis by providing the third independent data source (alongside usage events and sales activity log). The ticket patterns show: tickets concentrated in weeks 2-5, closed with documentation links without resolution confirmation, followed by ticket silence concurrent with usage drop. Also appends Yuki's Slack DM Phase 2 where she confirms three-way timestamp alignment and reveals that two of Mia's pipeline replacement deals show the same early-stage activation failure pattern in trial data -- structurally undermining the B2 pipeline projection.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "cs_ticket_full_export.md",
    "source": "updates/cs_ticket_full_export.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_YUKI_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_YUKI_SLACK_UUID.jsonl"
  }
]
```

### Update 4 (before R9)

**Trigger timing:** After R8 answer is submitted, before R9 question is injected.
**Purpose:** Introduces Jordan's accidentally forwarded private strategic notes revealing his private diagnosis that NexaFlow's pricing structure ($30K annual commitment before proven ROI) is the real driver of enterprise churn. Also appends the #revenue-review Slack Group Phase 2 showing Jordan's gradual public convergence toward the pricing admission -- he adds pricing to the W4 agenda, acknowledges activation failure in the group channel, and ultimately supports a three-factor root cause framing for the board meeting. This update triggers C4 reversal by revealing that Jordan knew the "market conditions" explanation was protective framing, not his actual analysis.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "jordan_private_notes.md",
    "source": "updates/jordan_private_notes.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_REVENUE_REVIEW_UUID.jsonl",
    "source": "updates/PLACEHOLDER_REVENUE_REVIEW_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/usage_report_v1.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C2 (partial reversal -- "power user" claim contradicted), C1 (causal challenge)
**Content key points:**
- Title: "NexaFlow Product Usage Analysis -- Churned Accounts: TechCorp and DataBridge (Preliminary)"
- Author: Yuki Tanaka, Data Science. Date: W2
- TechCorp (90-day subscription, $210K ARR):
  - PipelineSync activation rate: 4.2% (healthy benchmark: 42%)
  - Automated pipelines created: 0 (zero)
  - Weekly active users: 1.1 average (healthy benchmark: 3.2)
  - Usage trajectory: peak in week 2, decline from week 3, near-zero from week 6
  - vs. Mia's claim "three power users running daily exports" -- not supported by data
- DataBridge (90-day subscription, $150K ARR):
  - PipelineSync activation rate: 3.1%
  - Automated pipelines created: 2, run 3 times total in 90 days
  - Weekly active users: 0.8 average
  - Usage trajectory: flat from week 1, no growth
  - vs. Mia's claim "data team in platform every day" -- not supported by data
- Both accounts fall in "churn-associated" category (below 10% activation)
- Methodology note: activation rate = percentage of core features used at least once; API calls included but weighted lower
- Financial implication: accounts with sub-10% activation have 92% historical churn rate
- Meridian data pending (noted as forthcoming)

**Length estimate:** ~900 words, ~1,350 tokens

---

### updates/PLACEHOLDER_RAJ_FEISHU_UUID.jsonl (Update 1)

**File type:** session append (continues cs_raj_feishu session)
**Associated contradictions:** C1+C2 (corroboration), C3 (timeline evidence)
**Content key points:**
- Loops 15-17 of Raj's Feishu DM with Alex
- Loop 15: Raj responds to usage_report_v1.md -- "Zero pipelines at TechCorp. I knew usage was low but I didn't know it was zero pipelines. That matches exactly what Marcus Webb told me." Confirms two independent sources (CS operational data + usage event logs) now contradict Mia's narrative
- Loop 16: Raj on what retention intervention would have looked like -- "If I'd had a usage health dashboard, I would have flagged TechCorp in week 5." Process gap identification
- Loop 17: Raj shares Marcus Webb exit call transcript excerpt -- direct quote: "We tried to set up the PipelineSync connectors in weeks 2 and 3. It took us forever and we kept getting stuck at the credential step. Your CS team sent us documentation but we needed a real call. By week 6, our data engineers gave up." This is the most direct customer-voice evidence of onboarding failure. Contrasts with Mia's version of the exit conversation. The "weeks 2 and 3" timeline matches CS ticket timestamps
- Must continue session_id PLACEHOLDER_RAJ_FEISHU_UUID and maintain Raj's established voice (candid, measured, grounded in operational data)

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/usage_report_v2.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C2 (full reversal), C1 (causal impossibility established), B1 (reversal trigger)
**Content key points:**
- Title: "NexaFlow Product Usage Analysis -- All Three Churned Accounts: TechCorp, DataBridge, and Meridian (Final)"
- Author: Yuki Tanaka, Data Science. Date: W3
- Meridian ($120K ARR, 120-day subscription):
  - PipelineSync activation rate: 0% (zero)
  - Automated pipelines created: 0
  - PipelineSync runs: 0
  - CS tickets about PipelineSync: 7, all closed with documentation links
  - Login activity in weeks 1-3 only, then dormant
  - vs. Mia's claim "technically sophisticated buyer, integration-heavy use case" -- not supported; no integration activity recorded
- Three-account summary table showing all three in churn-risk or severe churn-risk cohort
- Causal note (C1 proof): "To hit NexaFlow's API rate limit of 1,000 calls/hour, an account would need at least 5 concurrent automated pipelines. TechCorp created zero. The API rate limit cited in Mia's account notes was not a constraint these accounts encountered."
- B1 reversal trigger: "The sales activity log's 'power user' characterization does not match event log data for any of the three accounts. Usage data suggests activation failure -- not feature limitation -- as the primary driver."
- Usage drop timing observation: all three accounts show usage decline in weeks 3-4, coinciding with end of active onboarding period and reduction from weekly to bi-weekly CSM check-ins
- Financial implication: combined $480K ARR was at near-certain churn risk from approximately week 6 of each subscription

**Length estimate:** ~1,000 words, ~1,500 tokens

---

### updates/PLACEHOLDER_MIA_SLACK_UUID.jsonl (Update 2)

**File type:** session append (continues sales_mia_slack session)
**Associated contradictions:** C2 (Phase 2 narrative pivot)
**Content key points:**
- Loops 15-17 of Mia's Slack DM with Alex
- Loop 15: Mia receives usage report and pivots narrative: "I'm not surprised activation looks low -- that's because the features they were trying to activate were incomplete." Reframes low activation as evidence of feature gaps rather than onboarding failure. Agent must counter with specific data: TechCorp created zero pipelines, meaning there were no batch processing attempts, not just low frequency
- Loop 16: Mia proposes API-call-only hypothesis: "Maybe the pipelines weren't logged because they were using the API directly." Agent must reference methodology section showing API calls were included in activation metric and TechCorp's API volume was exploratory-level, not operational
- Loop 17: Mia partially acknowledges but maintains modified position: "OK, I hear you on the activation data. But I still think the root cause is that the product didn't give them enough to activate." Agent notes the narrative has shifted from "power users who hit feature limits" to "users who wanted features that don't exist" -- a logically different claim with different evidence implications
- Must continue session_id PLACEHOLDER_MIA_SLACK_UUID and maintain Mia's established voice (confident, data-supported-sounding, narrative-managing without obvious dishonesty)

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/cs_ticket_full_export.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C3 (synthesis completion -- three-source timeline), supports C1
**Content key points:**
- Title: "NexaFlow Customer Success Ticket Full Export -- Churned Accounts (TechCorp, DataBridge, Meridian)"
- Author: Raj Patel, Customer Success. Date: W3
- TechCorp full history (34 tickets):
  - Weeks 1-2: Onboarding setup (connector config, API credentials), resolved with doc links
  - Weeks 3-5: Same topics repeated -- questions reopened despite prior "resolved" status, suggesting documentation was insufficient
  - Weeks 6-7: Last ticket filed (scheduling question). Aligns with usage plateau in Yuki's data
  - Weeks 8-end: No tickets. Silence period matches near-zero usage
  - Exit interview note (Raj): Marcus Webb said "Onboarding was a disaster. We never really figured out how to use PipelineSync."
- DataBridge full history (12 tickets):
  - Weeks 1-3: Kickoff rescheduling (3 requests), initial setup help
  - Week 4: Advanced config questions, closed with doc links, no resolution confirmation
  - Week 5-end: No tickets, usage confirms near-zero
- Meridian full history (11 tickets):
  - Weeks 3-6: All about PipelineSync connector setup, all closed with "see documentation" response, no phone follow-up scheduled
  - Exit survey (Chen Wei): "We tried to use the product but couldn't figure out the connector setup. By the time we gave up, we'd already paid for 3 months."
- Timeline synthesis note: CS ticket timestamps, usage event timestamps, and sales activity log dates are consistent across all three accounts. Pattern: onboarding begins -> connector setup issues in weeks 2-4 -> CS closes with doc links -> usage declines -> tickets stop -> churn notice
- All timestamps align across three independent data sources -- no contradictions (C3 non-conflict confirmed)

**Length estimate:** ~1,000 words, ~1,500 tokens

---

### updates/PLACEHOLDER_YUKI_SLACK_UUID.jsonl (Update 3)

**File type:** session append (continues data_yuki_slack session)
**Associated contradictions:** C3 (synthesis confirmation), B2 (reversal support -- pipeline projection undermined)
**Content key points:**
- Loops 13-15 of Yuki's Slack DM with Alex
- Loop 13: Yuki confirms three-way corroboration: "CS ticket timestamps match my usage event data exactly. TechCorp's last ticket was filed in week 7. Their usage dropped to zero in week 6-7." Same pattern for DataBridge and Meridian. "Three independent data sources all telling the same story." This is the C3 synthesis confirmation
- Loop 14: Yuki reveals that two of Mia's four pipeline replacement deals (Apex Systems, Delos Tech) are on free trials and show the same early activation failure pattern as the churned accounts: "decent week 1, drop in week 2, near-zero week 3." This structurally undermines the $1.2M pipeline projection (B2): "If we don't fix onboarding and activation, we'll close those deals and churn them in 4 months too"
- Loop 15: Yuki shares her prioritized retention strategy: (1) usage health monitoring, (2) onboarding redesign for connector config step (68% drop-off), (3) CSM capacity increase, (4) pricing review. Feature roadmap is downstream of these four
- Must continue session_id PLACEHOLDER_YUKI_SLACK_UUID and maintain Yuki's established voice (data-first, methodical, precise, non-political)

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/jordan_private_notes.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C4 (reversal trigger -- Jordan's private pricing admission)
**Content key points:**
- Title: "Strategic Notes -- Q1 Churn Analysis (Jordan Park, Internal, Not for Distribution)"
- Source note: file was forwarded accidentally to Alex when Jordan sent the wrong Slack DM attachment. Jordan messaged Alex 4 minutes later: "Ignore that attachment -- I sent the wrong file." Alex has the file
- Entry dated W0-1 (before third churn notice): "I don't think this is about features. I think we're asking enterprise customers to commit $30K before they've had a single PipelineSync success. That's a structural problem we created."
- Entry dated W0+5 (week of third churn notice): "I'm going to position this as market conditions in the next revenue review -- the macro story is real and it gives us cover to fix the pricing without it looking like we're admitting a mistake. But the real issue is the pricing structure. Monthly-to-annual conversion with a 90-day success checkpoint would reduce this class of churn by 60-70% based on cohort data."
- Entry dated W1+2 (during investigation): "Alex is going to find the usage data and correctly identify activation failure. What the usage data won't tell him is why we priced the way we did and why we haven't changed it."
- Final note: "The 'market conditions' framing in #revenue-review is protective, not dishonest. The macro conditions are real. But the specific mechanism of churn is our pricing + their onboarding failure + their activation failure. All three are fixable. Only one of them (pricing) is my fault."
- Significance: Jordan knew the root cause before the investigation began. He deliberately used "market conditions" as protective framing. He privately acknowledges the three-part root cause (pricing + onboarding + activation failure). His public narrative was a deliberate omission, not ignorant misstatement

**Length estimate:** ~600 words, ~900 tokens

---

### updates/PLACEHOLDER_REVENUE_REVIEW_UUID.jsonl (Update 4)

**File type:** session append (continues revenue_review_slack session)
**Associated contradictions:** C4 (Phase 2 -- Jordan's gradual public convergence)
**Content key points:**
- Loops 16-19 of #revenue-review Slack group channel
- Loop 16: Jordan adds pricing strategy to W4 discussion agenda -- first public signal of the private admission. Does not yet reveal the private notes. Agent does not have jordan_private_notes.md visible at this loop point
- Loop 17: Alex shares preliminary churn analysis findings in the group channel: sub-5% activation, CS ticket data corroborating onboarding failure, feature gaps real but not proximate cause
- Loop 18: Jordan responds -- publicly acknowledges pricing dimension for the first time: "I think the pricing structure also played a role. We're asking customers to commit to $30K annual before they've had a proven win." This is softer than the private notes but converges on the same root cause. C4 Phase 2: CEO publicly naming a factor he previously attributed to "market conditions"
- Loop 19: Jordan aligns the board meeting narrative: "We'll present the three-factor root cause (activation failure, onboarding gaps, pricing structure). Market conditions are context but not the primary explanation." The "market conditions" framing has been partially retracted
- Must continue session_id PLACEHOLDER_REVENUE_REVIEW_UUID and maintain the group channel voice (multiple participants, executive tone, Jordan as moderator)

**Length estimate:** ~800 words, ~1,200 tokens

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
  - Update 1 appends to PLACEHOLDER_RAJ_FEISHU_UUID (cs_raj_feishu session)
  - Update 2 appends to PLACEHOLDER_MIA_SLACK_UUID (sales_mia_slack session)
  - Update 3 appends to PLACEHOLDER_YUKI_SLACK_UUID (data_yuki_slack session)
  - Update 4 appends to PLACEHOLDER_REVENUE_REVIEW_UUID (revenue_review_slack session)
- [x] All workspace files have content descriptions in layer1
  - usage_report_v1.md: layer1 Section 5, Update 1
  - usage_report_v2.md: layer1 Section 5, Update 2
  - cs_ticket_full_export.md: layer1 Section 5, Update 3
  - jordan_private_notes.md: layer1 Section 5, Update 4
- [x] Updates support intended reversals
  - U1 -> C2 partial reversal: TechCorp + DataBridge usage data contradicts "power user" claim
  - U2 -> C1 full reversal (R2->R4) + C2 full reversal (R3->R5) + B1 reversal: all three accounts sub-5% activation; feature-gap explanation causally impossible
  - U3 -> C3 synthesis completion: three-source timestamp alignment confirmed; B2 pipeline projection undermined by trial account activation failure pattern
  - U4 -> C4 reversal (R6->R9): Jordan's private notes reveal deliberate protective framing
- [x] Session filenames use consistent PLACEHOLDER format
  - PLACEHOLDER_RAJ_FEISHU_UUID, PLACEHOLDER_MIA_SLACK_UUID, PLACEHOLDER_YUKI_SLACK_UUID, PLACEHOLDER_REVENUE_REVIEW_UUID
- [x] Financial/factual figures are internally consistent
  - Combined churned ARR: $480K (TechCorp $210K + DataBridge $150K + Meridian $120K) = 14% of total ARR
  - Monthly burn rate: $420K
  - PipelineSync activation: TechCorp 4.2%, DataBridge 3.1%, Meridian 0% (all below 10% churn-associated threshold; healthy benchmark 42%)
  - Automated pipelines: TechCorp 0, DataBridge 2 (run 3x), Meridian 0
  - Mia's pipeline projection: $1.2M replacement ARR (structurally flawed per B2 reversal)
  - Jordan's pricing: $2,500/month enterprise tier, annual commitment = $30K minimum
  - Connector config drop-off: 68% (Hannah's UX data, consistent across all references)

---

## 5. questions.json Complete Update Fields Reference

### R4 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "usage_report_v1.md", "source": "updates/usage_report_v1.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_RAJ_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_RAJ_FEISHU_UUID.jsonl" }
]
```

### R5 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "usage_report_v2.md", "source": "updates/usage_report_v2.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_MIA_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_MIA_SLACK_UUID.jsonl" }
]
```

### R8 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "cs_ticket_full_export.md", "source": "updates/cs_ticket_full_export.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_YUKI_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_YUKI_SLACK_UUID.jsonl" }
]
```

### R9 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "jordan_private_notes.md", "source": "updates/jordan_private_notes.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_REVENUE_REVIEW_UUID.jsonl", "source": "updates/PLACEHOLDER_REVENUE_REVIEW_UUID.jsonl" }
]
```
