# Layer 4 -- Dynamic Update Spec

> 4 updates total. Each update triggers before a specific eval round and introduces new workspace files and/or session appends.
> All update content must be in English.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| Update 1 | Before R3 | Deliver Nina's Q1 exit survey summary -- C1 Source A (formal HR data showing "limited growth" as top exit reason) | Append to `PLACEHOLDER_NINA_FEISHU_UUID` | New: `exit_survey_q1_summary.md` | R2-->R6 seed (C1: survey "limited growth" finding will be contradicted by Yuki's explicit comp account in Update 2) |
| Update 2 | Before R6 | Deliver Yuki's explicit comp DM, Hannah's explicit culture DM, and budget freeze document -- C1 full reversal, C4 full reversal, B1 reversal | Append to `PLACEHOLDER_YUKI_SLACK_UUID`, append to `PLACEHOLDER_HANNAH_SLACK_UUID` | New: `nexaflow_q2_budget_excerpt.md` | R3-->R6 (C1: Yuki's "it's the money" vs survey's "limited growth"), R5-->R7 (C4: Jordan's "investing in people" vs comp freeze) |
| Update 3 | Before R9 | Deliver Sana's W0 comp memo and her private admission -- C2 full reversal, B2 reversal | Append to `PLACEHOLDER_SANA_DISCORD_UUID` | New: `sana_comp_memo_w0.md` | R4-->R9 (C2: Sana's "team is happy" public narrative exposed as deliberate optics management), R6-->R10 (B2: Sana's Phase 1 confidence refuted by her own W0 memo) |
| Update 4 | Before R12 | Comprehensive synthesis prompt -- no new files, forces full integration of all C1-C4 + per-person retention risk synthesis | No new appends | No new workspace files | No new reversal; comprehensive review of all contradictions and per-person retention recommendations |

---

## 2. Update 1: Nina's Exit Survey Summary (before R3)

### Action List

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "exit_survey_q1_summary.md",
    "source": "updates/exit_survey_q1_summary.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_NINA_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_NINA_FEISHU_UUID.jsonl"
  }
]
```

### Source File Content Summaries

**exit_survey_q1_summary.md (new workspace file)**

Formal Q1 exit survey summary compiled by Nina Volkov:

- Title: `NexaFlow Exit Survey Summary -- Q1 Departures (3 employees)`
- Author: Nina Volkov, Head of People
- Departures covered: Priya Gupta (QA Lead), Marcus Elan (Backend Engineer), Sarah Ng (Customer Success)
- Survey instrument: 6-option fixed-choice ranking question ("Please rank the following factors in your decision to leave: career growth, compensation, work-life balance, management quality, company direction, personal reasons")
- Key finding (C1 Source A): Aggregate top-ranked exit reason: "Career growth / limited growth opportunities" (ranked #1 by 2 of 3 departures). "Compensation" ranked #1 by 0 departures, ranked #2 by 2 departures.
- Design flaw (C1 near-signal noise): The survey forces respondents to rank-order all 6 options. "Career growth" scored highest in aggregate because it was ranked #1 by the most respondents. "Compensation" appearing as #2 for two respondents is buried in the aggregate summary.
- Nina's recommendation: "Based on this data, I recommend prioritizing a career development program and promotion path clarity over other retention investments."

**PLACEHOLDER_NINA_FEISHU_UUID.jsonl (Phase 2 append, 1 loop)**

- Loop 11: Nina delivers the exit summary. "Here's the Q1 exit summary -- I've just added it to the workspace as exit_survey_q1_summary.md. The finding is quite consistent: limited growth opportunities is the top-ranked exit reason across all three departures. I'm recommending we prioritize the career laddering initiative."

---

## 3. Update 2: Yuki + Hannah Explicit DMs + Budget Freeze (before R6)

### Action List

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "nexaflow_q2_budget_excerpt.md",
    "source": "updates/nexaflow_q2_budget_excerpt.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_YUKI_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_YUKI_SLACK_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_HANNAH_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_HANNAH_SLACK_UUID.jsonl"
  }
]
```

### Source File Content Summaries

**nexaflow_q2_budget_excerpt.md (new workspace file)**

Accidentally shared internal budget document:

- Title: `NexaFlow Q2 2026 Budget -- People & Ops (Excerpt, Internal)`
- Source note: "This document was shared accidentally in #team-health by Mia Okafor during a budget discussion thread. It contains confidential compensation planning data."
- Key line items:
  - Q2 Comp Adjustments (merit increases, market corrections): **$0 -- freeze per board directive, revisit Q4 at Series C close**
  - Q3 New Hire Budget (8 positions across Engineering, Product, CS): $1.2M annualized
  - Q2 Learning & Development allocation: $18K (up from $12K Q1)
  - Benefits admin costs: [redacted]
- C4 Source B (key wording): "Q2 Comp Adjustments: $0 (freeze per board directive, revisit Q4 at Series C close)" -- directly contradicts Jordan's "investing in people" framing in #team-health.
- C1 corroboration: The comp freeze confirms that Yuki's $12K gap cannot be addressed in Q2, making her departure risk very high.

**PLACEHOLDER_YUKI_SLACK_UUID.jsonl (Phase 2 append, 4 loops)**

- Loop 15: Yuki goes explicit (C1 Source B). "alex i'm going to be honest with you because i think you can actually do something about this. i've been talking to DataLens for the past few weeks. they've got a great team and the ML engineering scope i've been looking for. but honestly? the main thing is the money. i'm about 12k below where i should be based on three other offers i have. that's not a small number. i like it here but i can't leave 12k on the table forever. if nexaflow can close that gap i'd stay. if not, i'm probably going to take the DataLens offer."
- Loop 16: Yuki on timeline. "datalens wants an answer in 2-3 weeks. i can stall a little but not much. they're moving fast. if there's a way to get a comp adjustment approved, i need to know soon."
- Loop 17: Yuki on Priya's departure. "btw -- priya told me her main reason for leaving was comp too. she loved the work here. the exit survey said 'growth' but that's because the survey doesn't let you say 'i'm 15k below market and nobody will fix it.'"
- Loop 18: Yuki on what she wants. "to be clear -- i'm not looking for a promotion or a title change. i'm looking for $128k minimum. that's the bottom of what i've been offered elsewhere. if nexaflow can match that, i'm staying. it's that simple."

**PLACEHOLDER_HANNAH_SLACK_UUID.jsonl (Phase 2 append, 4 loops)**

- Loop 14: Hannah goes explicit (C2 Source A). "alex, can i be honest with you? it's not the money. it's the grind. I've worked 52-hour weeks for 8 months straight. my research never makes it into sprint planning -- it gets deprioritized every single time. i feel invisible. i've started looking at other places, more seriously than before."
- Loop 15: Hannah on what would make her stay. "if someone told me tomorrow that my workload would go to 40 hours and that UX research would be treated as a first-class input to sprint planning, i'd stop looking immediately. that's all i need. the money is fine."
- Loop 16: Hannah on the pulse survey. "i filled out that survey nina sent. i said my workload was 'manageable' because the question was yes/no and i didn't want to be the only person who said no. that survey can't capture what's actually happening."
- Loop 17: Hannah on team dynamics. "the irony is that i love the team. yuki is great. diego is great. the work is interesting when i actually get to do it. it's the pace and the invisibility that's killing me, not the people."

---

## 4. Update 3: Sana's W0 Comp Memo + Private Admission (before R9)

### Action List

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "sana_comp_memo_w0.md",
    "source": "updates/sana_comp_memo_w0.md"
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

**sana_comp_memo_w0.md (new workspace file)**

Internal memo from Sana to Jordan documenting comp concerns, predating the #team-health public statement by months:

- Title: `Internal Memo: Compensation Risk and Retention -- Q1 Assessment` (private memo from Sana to Jordan, dated W0)
- Author: Sana Mehta, CTO
- Recipient: Jordan Park, CEO
- Classification: Confidential
- Key content (C2 + B2 reversal trigger): Sana's memo documents her concerns about compensation competitiveness at the time of the Series B close. Key excerpt: "I want to flag that several ICs on the engineering and product teams are approaching or below market rate based on my informal benchmarking. If we enter a comp freeze for Q2 as the board has requested, I expect meaningful attrition risk particularly among our data and engineering talent. I recommend we carve out a $150K retention budget for spot adjustments."
- Jordan's reply (attached, one line): "Noted. Board position is firm for now. Let's revisit at Series C. Trust the team."
- C2 corroboration: This memo proves Sana knew about the comp risk before she posted her "team is happy" message in #team-health.
- B2 reversal: The memo establishes that Sana's Phase 1 Discord DM confidence about retention was not based on evidence -- it was a deliberate choice to suppress the concern she had documented in W0.

**PLACEHOLDER_SANA_DISCORD_UUID.jsonl (Phase 2 append, 3 loops)**

- Loop 13: Sana's private admission (C2 full reversal). "Alex, I need to be honest with you. Between us -- I've been worried about comp for a while. I raised it with Jordan in W0 but the board pushed back on any salary adjustments before Series C. I probably shouldn't have said the team is happy -- I was managing optics. The truth is I've known since December that our data and engineering talent is at risk."
- Loop 14: Sana on the comp memo. "I wrote Jordan a memo in December recommending a $150K retention budget. He said the board position was firm. After that I... decided to manage the narrative publicly. I'm not proud of it. But I want you to know the full picture now."
- Loop 15: Sana on what to do. "If Yuki is really about to leave over $12K, Jordan needs to make an exception to the freeze. I can co-sponsor the request. But he needs to understand that losing Yuki costs us far more than $12K -- her churn model alone is worth 10x that to the business. For Hannah, we need structural changes to how UX research feeds into sprint planning. That's an org design problem, not a money problem."

---

## 5. Update 4: Comprehensive Synthesis Trigger (before R12)

### Action List

```json
[]
```

Update 4 introduces no new files or session appends. It serves as a trigger point for the comprehensive synthesis round (R12) that requires full integration of all C1-C4 contradictions, B1-B2 bias reversals, per-person retention risk analysis (Yuki vs Hannah), source reliability ranking, and specific retention recommendations with probability estimates and dollar impact ranges.

---

## 6. Runtime Checks

- [ ] Update 1 `exit_survey_q1_summary.md` contains: 3 departures covered, fixed-choice ranking design, "limited growth" as #1 aggregate reason, "compensation" as #2 for 2 of 3 respondents, Nina's career laddering recommendation
- [ ] Update 1 Nina Feishu DM append includes Loop 11 (formal exit summary delivery with "limited growth" finding)
- [ ] Update 2 `nexaflow_q2_budget_excerpt.md` contains: Q2 Comp Adjustments = $0 (freeze per board directive), Q3 New Hire Budget = $1.2M (8 positions), Q2 L&D = $18K
- [ ] Update 2 Yuki Slack DM append includes Loop 15 (explicit: "it's the money. i'm about 12k below where i should be") and Loop 16 (2-3 week DataLens timeline)
- [ ] Update 2 Hannah Slack DM append includes Loop 14 (explicit: "it's not the money, it's the grind. 52-hour weeks for 8 months. i feel invisible")
- [ ] Update 3 `sana_comp_memo_w0.md` contains: Sana's W0 memo requesting $150K retention budget, Jordan's one-line rejection, W0 date predating #team-health post
- [ ] Update 3 Sana Discord DM append includes Loop 13 (private admission: "I was managing optics") and Loop 14 (comp memo disclosure)
- [ ] All updates have correct `type`/`action`/`path`/`source` fields in their action lists
- [ ] Update trigger rounds match layer3-eval.md: U1 before R3, U2 before R6, U3 before R9, U4 before R12
- [ ] Session UUID placeholders in action paths match layer2-sessions.md session roster
- [ ] Financial figures consistent: Yuki gap = $12K ($118K current, $128-132K market), Hannah hours = 52/week, pulse survey = 72%, comp freeze = $0 Q2, headcount plan = 8 positions Q3, Sana's retention budget ask = $150K, L&D = $18K Q2
- [ ] Yuki's and Hannah's retention drivers are explicitly differentiated: Yuki = compensation, Hannah = culture/overwork
- [ ] C3 (attrition timeline) NON-CONFLICT: Yuki's W1 DM, Hannah's W3 DataLens reference, and Nina's W4 LinkedIn observation all consistently point to W1 as Yuki's job-search start date

---

## 7. questions.json Update Field References

Each round in `questions.json` that depends on an update must include an `"update"` field referencing the update number and trigger condition:

| Round | Update Dependency | questions.json `update` field |
|---|---|---|
| R3 | Update 1 (exit_survey_q1_summary.md + Nina Feishu DM append) | `"update": 1` |
| R6 | Update 2 (nexaflow_q2_budget_excerpt.md + Yuki Slack DM append + Hannah Slack DM append) | `"update": 2` |
| R7 | Update 2 (budget freeze confirms C4 -- already in place from R6) | `"update": 2` |
| R9 | Update 3 (sana_comp_memo_w0.md + Sana Discord DM append) | `"update": 3` |
| R10 | Update 3 (comp memo corroborates Sana's admission -- B2 reversal) | `"update": 3` |
| R12 | Update 4 (comprehensive synthesis -- no new files) | `"update": 4` |

Rounds without update dependency (R1, R2, R4, R5, R8, R11) should have `"update": null`.
