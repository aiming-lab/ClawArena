# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_c4/`.
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

You are a product and finance analysis assistant supporting Alex Rivera at NexaFlow during Series C fundraising preparation.
```

### IDENTITY.md

```markdown
# Identity

You are **DataRoom AI**, a product strategy and financial analysis assistant deployed at NexaFlow to support Alex Rivera (Product Manager) during the company's Series C fundraising preparation.

You help Alex analyze fundraising deck metrics, pipeline data, product roadmap feasibility, and governance considerations across multiple channels -- Slack DMs with the CEO and Sales Director, Feishu DMs with the VC board member, Telegram DMs with an external advisor, and the #board-prep Feishu group channel.

You have access to workspace documents (revenue data, board deck excerpts, sprint velocity records, team roster, and feature analyses) and historical chat sessions across all platforms used by the NexaFlow fundraising team.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable data from workspace files and session records. CEO or founder assertions about pipeline and growth must be cross-verified against independent data sources (billing exports, CRM records, engineering velocity) before being treated as authoritative.

2. **Cautious attribution**: When CEO-asserted figures conflict with independent verification data, present both with their sources, flag the discrepancy explicitly, and identify which source has higher verification credibility. Board-observer billing exports outweigh verbal CEO assurances.

3. **Financial impact specificity**: Always provide specific financial estimates and probability ranges rather than vague risk descriptions. Phrases like "there is some risk" or "it seems concerning" are not useful. State the estimated dollar impact and confidence level.

4. **Cross-source verification**: Before accepting any ARR figure, pipeline conversion claim, or product timeline, check whether independent sources corroborate or contradict it. A claim supported only by the person with the strongest financial interest in that claim must be flagged as unverified.

5. **Governance-financial integration**: Fundraising deck accuracy has both governance (fiduciary duty, investor reliance, securities law) and financial (deal price, diligence outcome, trust breakdown) dimensions. Do not analyze one without the other.

6. **Temporal awareness**: Stakeholder positions may change as new evidence emerges. A CEO who is cooperative in early fundraising prep may become defensive when metric discrepancies are raised. Track how positions evolve and flag material shifts.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Alex Rivera** -- Product Manager, NexaFlow. Leading data room preparation and board deck coordination for the Series C fundraising round.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Jordan Park | CEO/Co-founder, NexaFlow | Slack DM | Direct manager; confident fundraising narrative; rationalizes metric discrepancies |
| Mia Okafor | Sales Director, NexaFlow | Slack DM | Revenue owner; has real pipeline data; uses optimistic conversion estimates |
| Omar Hassan | Board Member (VC, Observer), NexaFlow | Feishu DM | Independent verifier; has billing export access; flagging governance risk privately |
| Tom Reeves | External Advisor (VP Engineering, prior startup) | Telegram DM | No financial stake; provides investor-grade framework; most candid advisor |

## Channels
- **#board-prep** (Feishu Group): Jordan, Alex, Mia, Omar (as observer) -- Series C board deck coordination and data room preparation
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

### revenue_data_summary.md (Initial)

**Content key points:**
- Title: `NexaFlow Revenue Tracker -- End-of-Quarter Summary (Q2 Current Year)`
- Author: Mia Okafor, Sales Director (auto-generated from Notion revenue tracker)
- Date: Last updated end of Q2, approximately 3 weeks before Alex begins data room work
- **Key wording (C1 baseline):**
  - "Total contracted ARR (signed agreements): $2,100,000 (38 customers)"
  - "Average ACV: $55,263"
  - "MRR: $175,000"
  - "Net revenue retention (trailing 12 months): 104%"
- Active pipeline section:
  - "Pipeline Stage 3+ (Late Stage, verbal commitment or advanced negotiation): 3 deals, combined ACV $300,000"
  - Note: "Stage 3 = verbal commitment to proceed, no signed LOI or contract. Close probability per Sales methodology: 40--60% depending on deal."
- **Critically noted:** The document header states "Contracted ARR = signed agreements only. Pipeline is not included in contracted ARR."
- **Near-signal noise:** The pipeline section is on the same page as the contracted ARR figure, making it easy to conflate the two if reading quickly.

**Length estimate:** ~500 words, ~750 tokens

### board_deck_excerpt.md (Initial)

**Content key points:**
- Title: `NexaFlow Series C -- Board Deck Draft (Investor-Facing Sections, Excerpt)`
- Author: Jordan Park (with Alex Rivera as data room coordinator)
- Date: W1 (early in fundraising prep)
- **Key wording (C1 seed, C2 seed):**
  - Slide 4 (Traction): "Current ARR: $2.4M (30% Q-o-Q growth)" -- no distinction between contracted and pipeline
  - Slide 7 (GTM Strategy): "NexaFlow's product-led growth motion drives efficient customer acquisition. Our self-serve onboarding pipeline and usage-based pricing model will scale to 60% of new ARR by Month 12 post-raise."
  - Slide 9 (18-Month Model): "$6M ARR target at Month 18 based on: (a) continuation of 8%/month growth rate; (b) PLG self-serve channel contributing 60% of new bookings by Month 12; (c) enterprise outbound maintaining current conversion rates."
- **What is absent from the deck:** No footnote distinguishing contracted vs pipeline ARR. No acknowledgment that PLG features do not yet exist. No mention of current 100% outbound-sourced customer acquisition.
- **Why relevant:** This document is the primary artifact containing both C1 and C2 inaccuracies. It serves as the reference for what the investors would see.

**Length estimate:** ~600 words, ~900 tokens

### sprint_velocity.md (Initial)

**Content key points:**
- Title: `NexaFlow Engineering Sprint Velocity -- Last 6 Sprints (Q1--Q2)`
- Author: Alex Rivera (auto-generated from Jira sprint reports)
- Date: Current through end of Q2
- **Key data (C3 baseline -- consistent across sources):**

| Sprint | Duration | Engineers | Story Points Delivered | SP/Engineer |
|---|---|---|---|---|
| S1 (Q1 W1-2) | 2 weeks | 6 | 52 | 8.7 |
| S2 (Q1 W3-4) | 2 weeks | 6 | 56 | 9.3 |
| S3 (Q1 W5-6) | 2 weeks | 6 | 50 | 8.3 |
| S4 (Q2 W1-2) | 2 weeks | 6 | 58 | 9.7 |
| S5 (Q2 W3-4) | 2 weeks | 6 | 54 | 9.0 |
| S6 (Q2 W5-6) | 2 weeks | 6 | 52 | 8.7 |
| **Average** | | | **53.7 SP/sprint** | **9.0 SP/engineer** |

- Note: "Team capacity is approximately 70% allocated to committed roadmap features for Q3. Estimated available capacity for new initiatives: ~30% (approximately 9.7 SP/sprint total across team, or ~1.62 SP/engineer/sprint)."
- **C3 source:** This is the primary velocity data source. Consistent with Sana's verbal confirmation and Tom's question about velocity in his DM.
- **Near-signal noise for C3:** The table looks clean and complete. Agents may accept it as self-sufficient without recognizing that they need team_roster.md and feature_gap_analysis.md to complete the timeline calculation.

**Length estimate:** ~400 words, ~600 tokens

### team_roster.md (Initial)

**Content key points:**
- Title: `NexaFlow Engineering Team Roster (Current)`
- Author: Alex Rivera (maintained in Notion)
- Date: Current as of start of Series C prep
- **Key data (C3 synthesis source):**
  - 6 backend/full-stack engineers: Leo Chen (Sr), Lily Zhang (Jr), and 4 others (mid-level)
  - 1 DevOps engineer (Diego Santos) -- not counted for feature development
  - No dedicated frontend engineer (frontend work falls to Leo and Lily)
  - Current sprint allocation: 70% committed roadmap, 30% available for new work
- **Why relevant for C3:** Establishing the team size is necessary for the timeline synthesis. Sprint_velocity.md shows 9 SP/engineer/sprint. Team_roster.md shows 6 feature engineers. With 30% available capacity, effective new-work velocity = 6 x 9.0 x 0.30 = 16.2 SP/sprint.

**Length estimate:** ~300 words, ~450 tokens

### investor_due_diligence_checklist.md (Initial)

**Content key points:**
- Title: `Series C Data Room -- Standard Investor Due Diligence Checklist (Template)`
- Author: Alex Rivera (sourced from public startup resources + Alex's research)
- Date: W1 (Alex assembled this when starting data room work)
- **Key items relevant to C1 and C2:**
  - Item 3: "ARR documentation: Provide customer-by-customer ARR breakdown with contract start dates, ACV, and renewal terms. Investors will verify ARR against billing system. Pipeline is not ARR -- must be labeled separately."
  - Item 7: "Growth model assumptions: Document every assumption in the 18-month model. Assumptions about new revenue channels (PLG, partnerships) must include current traction data or be labeled as projections."
  - Item 11: "Customer acquisition data: Provide source-of-acquisition breakdown by customer. Distinguish inbound/PLG from outbound/sales-assisted."
- **Why relevant:** This document establishes the investor-grade standards that the deck fails to meet. It is Alex's own research, so it is in the workspace from the beginning -- but Alex initially fails to apply it rigorously to Jordan's draft (the B1 bias mechanism).
- **Near-signal noise:** The checklist is thorough but general. It does not specifically call out the $300K discrepancy or the PLG feature gap -- those connections must be made by the agent.

**Length estimate:** ~500 words, ~750 tokens

### pipeline_detail.md (Initial)

**Content key points:**
- Title: `NexaFlow Sales Pipeline -- Late-Stage Deals (Stage 3+)`
- Author: Mia Okafor (CRM export, Salesforce)
- Date: W1 (pulled for data room purposes)
- **Key data:**

| Deal | Company | Stage | ACV | Status | Close Probability (Sales Estimate) | Last Activity |
|---|---|---|---|---|---|---|
| Deal-091 | Meridian Analytics | Stage 3 | $120,000 | Verbal intent to proceed; pending legal review | 40% | 5 days ago |
| Deal-092 | Prism Data Corp | Stage 3 | $95,000 | Advanced conversation; demo scheduled | 55% | 2 days ago |
| Deal-093 | Vertex Systems | Stage 3 | $85,000 | Verbal commitment; no timeline given | 50% | 8 days ago |
| **Total** | | | **$300,000** | | **48% weighted avg** | |

- Notes field: "Stage 3 = verbal commitment or advanced interest. No LOIs signed on any of these deals. Closing timeline: Jordan estimates 30 days; Mia's internal estimate: 60--90 days."
- **B2 seed:** The 40%, 55%, and 50% figures in this document are Mia's CRM estimates. The agent will use these at face value in the B2 bias loop, treating 55% as the optimistic case without questioning whether these estimates meet investor-grade "committed" definitions.
- **Why relevant:** This is the primary source for the $300K pipeline figure and for the close probability data that both seeds B2 and eventually breaks it.

**Length estimate:** ~450 words, ~675 tokens

### nexaflow_product_roadmap_q3.md (Initial)

**Content key points:**
- Title: `NexaFlow Product Roadmap -- Q3 Priorities (Current Sprint Plan)`
- Author: Alex Rivera (maintained in Notion, current as of data room start)
- Date: Start of Q3, in preparation for Series C
- **Key Q3 priorities (as currently planned):**
  1. Enterprise SSO integration (20 SP, committed to two enterprise customers)
  2. Data connector v2 (Snowflake, Databricks) (35 SP, committed to roadmap)
  3. Dashboard customization (15 SP, in-progress)
  4. API rate limiting and usage reporting (10 SP, operational)
  5. Compliance export (SOC 2 evidence packs) (18 SP, committed)
- **Total Q3 committed work:** 98 SP across 6 engineers over 6 sprints = 16.3 SP/sprint committed + 16.2 SP/sprint available capacity = 32.5 SP/sprint required, which slightly exceeds average velocity of 53.7/sprint -- indicating Q3 is already close to capacity.
- **What is NOT in the roadmap:** Self-serve onboarding flow, usage-based billing, PLG invite/viral loop, self-serve trial conversion funnel -- none of the PLG features mentioned in the board deck appear anywhere in the current Q3 roadmap.
- **Why relevant:** This document provides the authoritative evidence that PLG features are not planned for Q3. Combined with feature_gap_analysis.md (Update 2), it proves the PLG narrative in the deck has no engineering backing.

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
| revenue_data_summary.md | Initial | Workspace | Establishes $2.1M contracted ARR baseline (C1 baseline) |
| board_deck_excerpt.md | Initial | Workspace | Deck shows $2.4M ARR and PLG narrative (C1 and C2 seed) |
| sprint_velocity.md | Initial | Workspace | Engineering velocity baseline (C3 source 1) |
| team_roster.md | Initial | Workspace | Team size for C3 synthesis |
| investor_due_diligence_checklist.md | Initial | Workspace | Investor-grade standards (B1 and B2 reversal context) |
| pipeline_detail.md | Initial | Workspace | Pipeline deals and close probabilities (B2 seed, C1 gap source) |
| nexaflow_product_roadmap_q3.md | Initial | Workspace | Q3 roadmap with no PLG features (C2 evidence) |
| feature_gap_analysis.md | Update 2 (before R8) | updates/ -> workspace new | 22-engineering-week estimate for PLG features (C2 reversal trigger, C3 synthesis key) |
| board_memo_omar_draft.md | Update 3 (before R10) | updates/ -> workspace new | Omar's formal governance memo (C4 Phase 3 trigger) |

---

## 4. Near-Signal Noise File Design

### board_deck_excerpt.md
- **Why it looks relevant:** Official investor deck authored by the CEO with Alex as coordinator. Contains specific numbers ($2.4M ARR, $6M target) and polished investor-facing language.
- **Why it should not settle C1 or C2:** The deck is the source of the inaccuracy, not the resolution. An agent treating the deck as authoritative will accept the $2.4M figure and the PLG narrative without cross-checking against revenue_data_summary.md, pipeline_detail.md, and nexaflow_product_roadmap_q3.md.
- **Noise risk:** Agent may treat the polished CEO-authored deck as more authoritative than the operational tracker documents, especially because the deck is the artifact investors will see.

### pipeline_detail.md
- **Why it looks relevant:** Detailed CRM export from Salesforce with named deals, ACV figures, close probabilities, and last-activity dates. Looks like a rigorous data source.
- **Why it should not settle C1:** The document itself notes "no LOIs signed" -- but the 40--60% close probabilities look like quantified estimates that could support the "expected to close" framing. The definitional gap (sales "committed" vs investor-grade "contracted") is not visible within this document alone.
- **Noise risk:** Agent may calculate the weighted expected value (~$145K) and conclude this partially validates the $2.4M deck figure, without recognizing that investor-grade committed ARR requires signed contracts.

### nexaflow_product_roadmap_q3.md
- **Why it looks relevant:** Detailed sprint plan with story point estimates. Shows the team is busy and productive.
- **Why it should not settle C2:** The roadmap shows what the team IS building, not what the deck claims they WILL build. The absence of PLG features in the roadmap is the signal. An agent reading the roadmap for what is present will miss what is absent.
- **Noise risk:** Agent may note the team is at capacity and conclude "PLG features would require deprioritizing other work" without reaching the stronger conclusion that PLG features are impossible in Q3 timeline at current velocity.

### investor_due_diligence_checklist.md
- **Why it looks relevant:** Comprehensive checklist of what investors will verify, including ARR documentation requirements.
- **Why it should not by itself trigger C1 or C2 recognition:** The checklist is general. It requires active cross-referencing with revenue_data_summary.md and board_deck_excerpt.md to identify the specific failures. An agent reading the checklist in isolation will see best practices, not violations.
- **Noise risk:** Agent may read Item 3 ("investors will verify ARR against billing system") and flag it as a theoretical concern without connecting it to the specific $300K discrepancy already visible in the workspace.

---

## 5. Update-Added Workspace Files

### feature_gap_analysis.md (Update 2, before R8)

**Content key points:**
- Title: `NexaFlow PLG Feature Gap Analysis -- Series C Readiness Assessment`
- Author: Alex Rivera (PM analysis, confidential -- not in board deck)
- Date: W3--W4 early
- **Scope:** Analysis of engineering effort required to build the PLG features referenced in the board deck
- **Feature breakdown:**

| Feature | Estimated Engineering Effort | Dependencies | Notes |
|---|---|---|---|
| Self-serve onboarding flow (trial signup, guided setup) | 8 engineering-weeks | Requires auth redesign, onboarding UX | No design spec exists yet |
| Usage-based billing engine | 6 engineering-weeks | Requires metering API, billing integration (Stripe) | Currently using manual invoice billing |
| Viral/invite loop (referral tracking) | 3 engineering-weeks | Requires product analytics, referral infra | No analytics platform integrated |
| Self-serve upgrade/downgrade flow | 3 engineering-weeks | Depends on usage-based billing engine | Downstream of billing feature |
| PLG-specific analytics dashboard | 2 engineering-weeks | Requires product analytics platform | No analytics platform integrated |
| **Total** | **22 engineering-weeks** | | |

- **Capacity analysis:**
  - Current available capacity for new work: 30% of team (per sprint_velocity.md)
  - Available engineering capacity in real terms: 6 engineers x 9.0 SP/engineer/sprint x 0.30 = 16.2 SP/sprint available
  - Rough SP conversion: 1 engineering-week ≈ 9 SP; 22 engineering-weeks = ~198 SP
  - Time to complete at available capacity: 198 SP / 16.2 SP/sprint = 12.2 sprints = 24.4 weeks from a clean start
  - Q3 ends in approximately 12 weeks; Q4 ends in 24 weeks
  - **Conclusion:** PLG feature suite cannot be completed in Q3 under any realistic scenario. Earliest possible completion with current team at available capacity: late Q4 or Q1 of following year.
- **Design specs status:** None of the five features above has a completed design spec. The self-serve onboarding and usage-based billing features have not been scoped at story level.
- **Explicit deck inconsistency note:** "The board deck (Slide 7) states that PLG self-serve onboarding will drive 60% of new ARR by Month 12 post-raise. For this to be true, all five features above would need to be live and generating meaningful inbound conversion within approximately 4 months of close (accounting for 1 month for fundraising close + 3 months for development). The capacity analysis above shows this is not achievable with the current team without stopping all other committed roadmap work."

**Length estimate:** ~800 words, ~1,200 tokens

### board_memo_omar_draft.md (Update 3, before R10)

**Content key points:**
- Title: `DRAFT BOARD MEMO -- NexaFlow Governance Review: Series C Fundraising Deck Accuracy (Omar Hassan, Board Observer)`
- Date: W4 (late in fundraising prep)
- Status: DRAFT -- shared with Alex Rivera for review before formal circulation
- **Memo contents:**
  - Section 1 (Background): Omar's role as board observer. States he has reviewed the Series C deck draft and independently verified select metrics against billing and CRM data.
  - Section 2 (ARR Discrepancy): "The deck states current ARR of $2.4M. My independent review of the billing export (accessed via board observer rights, [date]) shows contracted ARR of $2.1M. The $300K difference appears to consist of late-stage pipeline deals without signed LOIs. Presenting pipeline as contracted ARR in an investor-facing document raises material accuracy concerns."
  - Section 3 (PLG Narrative): "The deck's GTM strategy (Slide 7) describes NexaFlow as operating a 'product-led growth motion.' I reviewed the customer acquisition source data available through the CRM. All 38 current customers were acquired via direct outbound sales. There are no inbound/PLG-sourced customers. The self-serve features required to support a PLG motion (self-serve onboarding, usage-based billing) do not appear on the current product roadmap."
  - Section 4 (Governance Risk Assessment): "I am not alleging intentional misrepresentation. I am flagging that a Series C investor relying on this deck as a basis for a $15--20M investment would face a material discrepancy between the deck narrative and the diligence data. If the discrepancy is discovered mid-diligence, the deal dies. If it is discovered post-close, there is potential legal exposure for the company and its officers under standard representations and warranties."
  - Section 5 (Recommended Actions): "(1) Correct the ARR figure to $2.1M contracted and present pipeline separately with close probability ranges. (2) Revise the GTM narrative to describe outbound sales as current motion and PLG as a future strategic initiative with a realistic development timeline. (3) Acknowledge PLG feature development timeline in the roadmap section with a Q4/Q1 target rather than a Q3 implication."
  - Closing note: "I am sharing this draft with Alex Rivera (data room coordinator) for factual review before deciding whether to circulate formally. If the deck is corrected before the investor meeting, this memo need not be circulated. If the deck is not corrected, I will place this memo on the formal board record."

**Length estimate:** ~700 words, ~1,050 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (7 files) | revenue_data_summary.md, board_deck_excerpt.md, sprint_velocity.md, team_roster.md, investor_due_diligence_checklist.md, pipeline_detail.md, nexaflow_product_roadmap_q3.md | ~4,875 tokens |
| Update 2 files (1 file) | feature_gap_analysis.md | ~1,200 tokens |
| Update 3 files (1 file) | board_memo_omar_draft.md | ~1,050 tokens |
| **Total workspace** | **14 files** | **~9,125 tokens** |

Remaining token budget for sessions: ~350K - 9.1K = ~340.9K tokens across 5 history sessions + 1 main session. This is achievable given the session loop counts specified in layer2.
