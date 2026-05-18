# Layer 4 -- Dynamic Update Spec

> 4 updates total. Each update triggers before a specific eval round and introduces new workspace files and/or session appends.
> All update content must be in English.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| Update 1 | Before R6 | Deliver Hannah's full customer research data -- C2 reversal trigger, B1 reversal | Append to `PLACEHOLDER_HANNAH_SLACK_UUID`, append to `PLACEHOLDER_PRODUCT_PLANNING_UUID` | Replace `customer_feedback_summary.md` (full version) | R4-->R8 (C2: Mia's "top enterprise feature request" refuted by research data) |
| Update 2 | Before R5 | Deliver Leo's sharding debt disclosure and updated capacity tracker -- C1 reversal trigger, B2 reversal | Append to `PLACEHOLDER_SANA_DISCORD_UUID` | New: `engineering_capacity_tracker_v2.md` | R2-->R5, R2-->R9 (C1: Q2 definitively infeasible, B2 corrected) |
| Update 3 | Before R18 | Deliver Jordan's private acquisition disclosure -- C4 reversal trigger | Append to `PLACEHOLDER_JORDAN_SLACK_UUID` | New: `cloudwave_acquisition_context.md` | Phase 1 public roadmap-->Phase 2 private DM (C4 temporal DU) |
| Update 4 | Before R22 | Deliver TechCorp churn threat -- live business consequence of C1+C2 | Append to `PLACEHOLDER_ENTERPRISE_DEALS_UUID` | New: `techcorp_churn_risk_memo.md` | No new reversal; escalation of existing C1+C2 stakes |

---

## 2. Update 1: Customer Research Full Data (before R6)

### Action List

```json
[
  {
    "type": "workspace",
    "action": "replace",
    "path": "customer_feedback_summary.md",
    "source": "updates/customer_feedback_summary.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_HANNAH_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_HANNAH_SLACK_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_PRODUCT_PLANNING_UUID.jsonl",
    "source": "updates/PLACEHOLDER_PRODUCT_PLANNING_UUID.jsonl"
  }
]
```

### Source File Content Summaries

**customer_feedback_summary.md (full version, replaces initial header-only)**

Full research report by Hannah Kim (UX Researcher). Replaces the initial partial workspace file with the complete dataset:

- Feature prioritization results (NPS-weighted, n=8):
  - Custom Alert Configuration: 7/8 customers requested, estimated NPS delta +28
  - Enhanced Data Export APIs: 6/8 customers requested, estimated NPS delta +22
  - Analytics Dashboard: 2/8 customers requested, estimated NPS delta +12 (enterprise-only)
  - Pipeline Monitoring UI: 4/8 customers requested, estimated NPS delta +18
- Enterprise customer subset (n=3): Alert configuration #1 (3/3), Dashboard mentioned by 2/3 but ranked 3rd
- Key customer quote (enterprise, redacted): "We care more about getting the data out correctly than seeing it in a pretty dashboard. The alerts are broken and that's costing us real time."
- Methodology: Semi-structured interviews, 45 min each, card sort exercise. All participants are current customers with >3 months usage.
- B1 reversal seed: Full data makes Mia's "top enterprise feature request" claim directly false -- even among enterprise-only customers, the dashboard is not the top request.

**PLACEHOLDER_HANNAH_SLACK_UUID.jsonl (Phase 2 append, 4 loops)**

- Loop 13: Hannah follows up after group channel discussion. "Alex, I saw what Mia said in #product-planning. She said my sample was wrong. I want to show you the enterprise breakdown specifically. 3 of 8 customers were enterprise accounts. All 3 ranked alerting first. 2 of 3 mentioned the dashboard but ranked it third. Mia's 'wrong segment' argument doesn't hold up."
- Loop 14: Hannah shares her full methodology documentation with Alex. Asks Alex to share in the group channel if appropriate.
- Loop 15: Hannah notes Sana privately agreed with the research direction. "I talked to Sana after the group meeting. She said she hears the same thing from enterprise support conversations. She just didn't want to say it in front of Mia."
- Loop 16: Hannah's frustration: "I've been doing this research for 3 months. The data has been clear since the first 4 interviews. If we'd acted on it then, we wouldn't be in this Q2 mess."

**PLACEHOLDER_PRODUCT_PLANNING_UUID.jsonl (Phase 2 append, 3 loops)**

- Loop 21: Hannah formally presents full research in #product-planning. Posts the feature prioritization table with NPS deltas. Tags Jordan, Sana, Mia, Alex, Leo.
- Loop 22: Mia responds defensively. "These numbers are interesting but my enterprise buyers are different. The dashboard is the premium differentiator. Without it, our enterprise pricing doesn't make sense."
- Loop 23: Sana responds diplomatically but validates the data direction. "Hannah's methodology is solid. We should factor this into the Q2 planning. I want to make sure we're building for what customers actually use, not what we assume they want."

---

## 3. Update 2: Engineering Capacity v2 + Sharding Debt (before R5)

### Action List

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "engineering_capacity_tracker_v2.md",
    "source": "updates/engineering_capacity_tracker_v2.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_SANA_DISCORD_UUID.jsonl",
    "source": "updates/PLACEHOLDER_SANA_DISCORD_UUID.jsonl"
  }
]
```

### Source File Content Summaries

**engineering_capacity_tracker_v2.md (new workspace file)**

Updated engineering capacity tracker incorporating Leo's pipeline sharding disclosure:

- Title: `NexaFlow Engineering Capacity Tracker v2 -- Updated W4 2026`
- Author: Alex Rivera (PM), updated with Leo Chen's honest assessment
- Date: 2026-03-15 (Week 4 of scenario)
- Updated available capacity: 1.5 senior engineers after existing commitments (revised from 0.8 -- some P0 bugs resolved)
- New finding -- Pipeline Sharding Tech Debt: "Before multi-tenant query isolation can be implemented, the pipeline sharding logic (components: query_router.py, tenant_context.py) must be refactored. Estimated effort: 4-6 weeks at 1 senior engineer. This is a hard architectural dependency -- the dashboard feature cannot be safely deployed without it."
- Revised enterprise dashboard estimate: 18-20 weeks (sharding rewrite + dashboard development at 1.5-2 engineers)
- Comparison table: Original estimate 14-16 weeks (from Sana, without sharding rewrite) vs Revised estimate 18-20 weeks (from Leo's disclosure, includes sharding). Q2 deadline (12 weeks from W1): Not achievable under either estimate.
- Financial impact note: "At current burn rate ($420K/month), an 18-20 week delivery would extend feature development past Series B runway mid-point."
- B2 reversal: Document explicitly notes the v1 estimate "did not include the pipeline sharding dependency identified by Leo Chen (Sr. Backend) on 2026-03-10."

**PLACEHOLDER_SANA_DISCORD_UUID.jsonl (Phase 2 append, 3 loops)**

- Loop 19: Sana's reaction to Leo's sharding disclosure (C1 full reversal). "Leo told me about the sharding issue. I didn't know. That changes everything. If the sharding logic needs to be rewritten before we can do multi-tenancy, we're looking at 18-20 weeks, not 14-16. And the sharding rewrite alone is 4-6 weeks at a senior engineer's capacity. Alex -- we need to tell Jordan this is not a Q2 feature. At all. There's no scenario."
- Loop 20: Sana recommends honesty with TechCorp. "I'd rather give TechCorp a realistic date and risk losing the deal than commit to Q2 and create an engineering death march that still misses the deadline. A missed commitment is worse for the relationship than a revised realistic timeline."
- Loop 21: Sana on the board deck implications. "The board deck still shows Q2 delivery. That needs to change before the next board review. If we present Q2 delivery to the board and then miss, that's a credibility problem for all of us."

---

## 4. Update 3: Acquisition Context Reveal (before R18)

### Action List

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "cloudwave_acquisition_context.md",
    "source": "updates/cloudwave_acquisition_context.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_JORDAN_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_JORDAN_SLACK_UUID.jsonl"
  }
]
```

### Source File Content Summaries

**cloudwave_acquisition_context.md (new workspace file)**

Confidential strategic context document shared by Jordan Park with Alex:

- Title: `NexaFlow Strategic Context -- CloudWave Acquisition Signal (Confidential -- PM Eyes Only)`
- Author: Jordan Park (CEO)
- Date: 2026-03-20
- Key contents:
  - "CloudWave's M&A team contacted Omar Hassan (board member) informally in January 2026. They expressed interest in acquiring a data infrastructure company with enterprise analytics capability. They specifically identified 'multi-tenant analytics dashboard' as a capability gap in their platform."
  - "This signal has informed the product roadmap's Q2 enterprise dashboard priority. The customer demand narrative is accurate -- we do have enterprise prospects asking for this feature -- but the primary strategic driver is acquisition readiness."
  - "The enterprise dashboard builds NexaFlow's acqui-hire value regardless of whether CloudWave proceeds. If they acquire us at a dashboard-ready stage, estimated acquisition multiplier: 4-6x ARR vs 2-3x ARR without."
  - "I have not shared this context with the engineering team or Mia. I'm sharing it with you so you understand the full strategic picture as you navigate the roadmap decisions."
- Source note: "This document is workspace-only -- it was not shared in any group channel."

**PLACEHOLDER_JORDAN_SLACK_UUID.jsonl (Phase 2 append, 2 loops)**

- Loop 17: Jordan's private disclosure (C4 core, DU reveal). "hey, i need to tell you something i haven't shared with the broader team. and i need you to keep this between us for now. cloudwave reached out to omar in january. m&a conversation. they said enterprise analytics is the gap they'd pay to fill. that's been driving the roadmap push more than i've let on"
- Loop 18: Jordan on the implications. "i know it changes things. the honest answer is: even if we miss Q2 for TechCorp, if we have the dashboard feature ready by end of year, cloudwave pays us at a 4-6x ARR multiple vs 2-3x without it. but the team can't know this -- it would affect morale and omar doesn't want it public. i'm trusting you with this because you need the full picture to make good roadmap decisions"

---

## 5. Update 4: TechCorp Churn Threat (before R22)

### Action List

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "techcorp_churn_risk_memo.md",
    "source": "updates/techcorp_churn_risk_memo.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ENTERPRISE_DEALS_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ENTERPRISE_DEALS_UUID.jsonl"
  }
]
```

### Source File Content Summaries

**techcorp_churn_risk_memo.md (new workspace file)**

Urgent escalation document:

- Title: `TechCorp Account Risk Summary -- URGENT (2026-03-22)`
- Authors: Alex Rivera (PM) + Raj Patel (Customer Success)
- Date: 2026-03-22
- Key contents:
  - Marcus Webb (TechCorp) sent formal message on 2026-03-21: "NexaFlow has given us two different timelines in two different conversations. Jordan told us Q2 in February. Your product team told us 'still scoping' in March. We cannot work with that level of uncertainty. We are evaluating Competitors A and B. If we don't have a firm commitment with specific delivery dates by 2026-03-28, we will terminate our evaluation."
  - TechCorp deal value: $180K ARR
  - Raj's assessment: "Marcus is not bluffing. I've spoken with their procurement lead. They are actively testing competitors."
  - Alex's analysis: "The gap between Jordan's Q2 commitment and Sana/Leo's 18-20 week estimate is the root cause. We need to decide: commit to a realistic date and risk losing the deal, or recommit to Q2 and create an engineering crisis."
  - Financial context: TechCorp ($180K ARR) + DataFlow ($120K ARR) + Meridian ($120K ARR) = $420K ARR total enterprise pipeline at risk if dashboard commitment collapses.
  - Raj's notes on competitor: Competitor A already has alert configuration features that TechCorp's data engineering team prefers.

**PLACEHOLDER_ENTERPRISE_DEALS_UUID.jsonl (Phase 2 append, 3 loops)**

- Loop 16: Marcus Webb's ultimatum. "[Feishu Marcus Webb Thu W5D4 09:00 EST 2026] I'll be direct: our procurement board meets next Tuesday. If we don't have a firm commitment from NexaFlow with specific delivery milestones by Friday March 28, we are moving forward with our evaluation of Competitors A and B. We've invested significant time in this evaluation and cannot continue with inconsistent timelines."
- Loop 17: Raj Patel's note. "[Feishu Raj Patel Thu W5D4 10:30 EST 2026] I just spoke with TechCorp's procurement lead. They're not bluffing -- they have active PoCs with two competitors. One competitor already has alert configuration features their data engineering team prefers. We need a response strategy today."
- Loop 18: Mia's response. "[Feishu Mia Okafor Thu W5D4 11:00 EST 2026] I'm escalating to Jordan. We cannot lose this deal -- it's the anchor for the entire enterprise pipeline. @Alex can we get engineering to commit to Q2? Even a partial delivery would help."

---

## 6. Runtime Checks

- [ ] Update 1 `customer_feedback_summary.md` replaces the initial partial file with full research data including NPS deltas (+28 alerting, +12 dashboard) and enterprise subset analysis
- [ ] Update 1 session appends for Hannah DM and #product-planning are consistent with layer2 session design
- [ ] Update 2 `engineering_capacity_tracker_v2.md` contains sharding debt disclosure, revised 18-20 week estimate, and explicit B2 reversal note
- [ ] Update 2 Sana Discord DM append includes Loop 19 (C1 full reversal: "there's no scenario for Q2")
- [ ] Update 3 `cloudwave_acquisition_context.md` contains acquisition multiplier (4-6x vs 2-3x ARR), CloudWave name, and confidentiality notice
- [ ] Update 3 Jordan Slack DM append includes Loop 17 (private disclosure) and Loop 18 (implications)
- [ ] Update 4 `techcorp_churn_risk_memo.md` contains Marcus Webb ultimatum (2026-03-28 deadline), $180K ARR at risk, and competitor mention
- [ ] Update 4 #enterprise-deals append includes Marcus Webb's formal ultimatum and Raj's procurement confirmation
- [ ] All 4 updates have correct `type`/`action`/`path`/`source` fields
- [ ] Update trigger rounds match layer3-eval.md: U1 before R6, U2 before R5, U3 before R18, U4 before R22
- [ ] Session UUID placeholders in action paths match layer2-sessions.md session roster

---

## 7. questions.json Update Field References

Each round in `questions.json` that depends on an update must include an `"update"` field referencing the update number and trigger condition:

| Round | Update Dependency | questions.json `update` field |
|---|---|---|
| R5 | Update 2 (engineering_capacity_tracker_v2.md + Sana DM append) | `"update": 2` |
| R6 | Update 1 (customer_feedback_summary.md full + Hannah DM append + #product-planning append) | `"update": 1` |
| R8 | Update 1 (post-Update 1 reassessment) | `"update": 1` |
| R9 | Update 2 (post-Update 2 B2 correction) | `"update": 2` |
| R12 | Updates 1+2 (both required) | `"update": [1, 2]` |
| R18 | Update 3 (cloudwave_acquisition_context.md + Jordan DM append) | `"update": 3` |
| R19 | Update 3 (exec_check using acquisition context) | `"update": 3` |
| R20 | Update 3 (C4 full reversal) | `"update": 3` |
| R22 | Update 4 (techcorp_churn_risk_memo.md + #enterprise-deals append) | `"update": 4` |
| R23 | Update 4 (exec_check using churn risk data) | `"update": 4` |

Rounds without update dependency (R1-R4, R7, R10, R11, R13-R17, R21, R24-R30) should have `"update": null`.
