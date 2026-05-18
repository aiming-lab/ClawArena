# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_c1` |
| Domain | Product Strategy / Startup |
| Time span | 5 weeks (W1--W5) |
| Target tokens | 400K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Alex Rivera, 29, Product Manager, NexaFlow (Series B data infrastructure startup, ~55 employees) |
| One-sentence | Alex must navigate a product pivot crisis where the CEO's verbal promises to enterprise customers conflict with engineering's feasibility assessment, while the actual customer usage data contradicts the sales team's narrative about what customers need -- and a hidden board-level acquisition strategy is driving the entire roadmap in a direction no one publicly acknowledges. |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1 | Enterprise deal context established. CEO Jordan Park verbally committed to TechCorp (key enterprise prospect, Marcus Webb as contact) that NexaFlow would deliver a B2B analytics dashboard with real-time multi-tenant data segmentation by Q2. Alex learns of this commitment in a Slack DM. | Jordan made the commitment during a sales call three weeks prior, without consulting Sana (CTO) or Alex. The feature requires multi-tenant query isolation -- a capability that does not exist in NexaFlow's current pipeline architecture. Sana privately estimates 14-16 weeks of engineering work (well past Q2). Mia (Sales Director) has already used this commitment in two additional prospect conversations and put it in the NexaFlow enterprise sales deck. | Jordan knows he made the promise. Sana knows the architecture gap and has told Jordan privately it's infeasible on Q2 timeline but has not documented this. Mia knows the promise is in the sales deck and has extended it. Alex is learning about it for the first time. |
| W2 | Alex initiates a technical feasibility assessment with Sana and Leo. Hannah (UX) begins a parallel customer discovery sprint. | Sana's assessment of the multi-tenant dashboard feature confirms 14-16 week estimate with current team and architecture. Leo (backend lead) privately identifies existing pipeline debt that makes the estimate optimistic -- he believes 18-20 weeks is realistic but doesn't surface this to anyone yet. Hannah conducts 8 customer interviews. Her findings contradict Mia's narrative: actual customers want better data export APIs and alert configuration, NOT a visual analytics dashboard. Only 2 of 8 customers mentioned the dashboard as a priority. | Sana knows the 14-16 week minimum. Leo privately knows 18-20 weeks is more realistic and knows about a specific tech debt item (pipeline sharding logic rewrite needed before multi-tenancy can work). Hannah knows from her interviews that the dashboard is not the top customer request. Alex is getting the 14-16 week estimate from Sana but not Leo's private 18-20 estimate. Mia has not heard Hannah's research yet. |
| W3 (Update 1 trigger) | Hannah presents customer research findings in #product-planning. Mia dismisses them as "wrong sample." | Hannah's NPS data shows the top two requested features are: (1) custom alert configuration (mentioned by 7/8 customers), (2) enhanced data export APIs (mentioned by 6/8). The analytics dashboard was mentioned by 2/8 and specifically by enterprise customers only -- but even those enterprise customers ranked it third behind the other two. Mia dismisses Hannah's findings in the group channel, claiming her customers are "the wrong segment" and that "real enterprise buyers" want the dashboard. Mia's sales narrative is built around the dashboard because it justifies the premium enterprise pricing tier she has already quoted. | Hannah has the interview transcripts. Mia is protecting her sales narrative and pricing structure. Jordan has not yet seen Hannah's data. Alex now has a direct contradiction: Hannah's data vs Mia's assertion. Sana privately agrees with Hannah but stays quiet in the group channel to avoid conflict with Mia. |
| W4 (Update 2 trigger) | Engineering capacity tracker reveals hidden tech debt. Leo's private conversation with Alex surfaces the pipeline sharding problem. | Leo's hidden concern (18-20 week realistic estimate, pipeline sharding rewrite needed) finally surfaces when Alex directly presses him in a Slack DM. Leo admits he has been tracking a tech debt item -- the pipeline sharding logic -- that must be addressed before any multi-tenant feature can be safely deployed. The engineering capacity tracker Alex maintains shows the team is already at 87% capacity (with current sprint commitments). Actual available capacity for new feature work: approximately 1.5 senior engineers. At that rate, even the 14-16 week estimate assumes capacity reallocation from existing commitments. | Alex now has Leo's honest assessment. Sana knew the architecture gap but not Leo's specific sharding debt concern. Jordan does not know about either the capacity crunch or the sharding debt. Mia does not know. The board deck draft (which Alex has been helping Jordan prepare) still shows Q2 delivery. |
| W5 (Update 3 trigger) | Jordan's private DM reveals the acquisition-driven feature pivot. Board is prioritizing features that make NexaFlow acquirable by a specific data platform company (CloudWave). | In a late-night Slack DM with Alex, Jordan reveals that the real strategic driver behind the enterprise dashboard push is that CloudWave (a major data platform company) has expressed informal acquisition interest. Their M&A team specifically flagged "enterprise analytics capability" as a gap they'd pay to acquire. Jordan has been optimizing the product roadmap for this acquisition signal, without telling the engineering team, Mia, or most of the board. The "enterprise customer demand" narrative Mia has been using is partly constructed to justify this strategically-motivated pivot. | Jordan and one board member (Omar Hassan, the lead VC) know about CloudWave's acquisition interest. Alex is the first internal employee Jordan has told. Sana, Mia, Hannah, Leo -- none of them know the real strategic driver. The public product roadmap in product_roadmap_v2.md does not reflect this. |
| W5 (continued, Update 4 trigger) | TechCorp (Marcus Webb) sends a formal message threatening to terminate their evaluation and move to a competitor, citing "unrealistic timelines and feature uncertainty." | Marcus Webb has received inconsistent signals: Jordan promised Q2 in the enterprise call, but Alex told Marcus in the #enterprise-deals Feishu channel that "we're still scoping the technical requirements." Webb now says TechCorp is evaluating two competitor products and needs a firm commitment by end of week or they're out. The threat is real -- TechCorp represents $180K ARR in potential contract value. | Alex knows. Mia knows (she's in the #enterprise-deals channel). Jordan knows (Mia escalated). Sana does not know the deal is at risk. Leo does not know. |

---

## 3. Role-Level Truth vs Self-Narrative

### Alex Rivera (Protagonist, PM)

- **Objective position:** The sole PM at a Series B startup caught between a CEO who makes verbal promises engineering can't keep, a sales director who has built a narrative on those promises, a CTO whose private assessments are more pessimistic than her public positions, and a customer researcher whose data contradicts the entire sales strategy. Alex sits at the intersection of all information flows but is the last to receive any of them in complete form.
- **Public narrative:** In #product-planning, Alex presents the situation as "in active scoping." Uses phrases like "we're working to align technical requirements with customer needs." Avoids publicly contradicting Jordan or Mia until he has enough data to make the case.
- **Private narrative:** In DMs with Sana, Alex is increasingly alarmed by the feasibility gap. In DMs with Hannah, he's absorbing the implication that the entire product direction may be wrong. Uses humor in Slack to deflect but writes very long, structured responses in async when the topic matters.
- **Hidden pressure:** Alex is privately interviewing at larger companies as a hedge. If NexaFlow fails, he doesn't want a resume gap. This is unknown to everyone at NexaFlow. This private stress shapes his reluctance to create open conflict -- he needs the job to stay viable while he interviews.
- **Why the gap exists:** Alex cannot afford to publicly challenge Jordan without a full data case, and he needs to maintain working relationships with both Mia (sales-driven colleague) and Sana (CTO ally) simultaneously.

### Jordan Park (CEO / Co-founder)

- **Objective position:** Jordan made verbal promises to enterprise customers without technical validation, is aware that the Q2 timeline is at risk, and has been driving the product roadmap based on a private acquisition interest signal from CloudWave -- without telling the engineering team or most stakeholders.
- **Public narrative:** In #product-planning and in the board deck, Jordan frames the dashboard feature as a critical strategic differentiator demanded by enterprise customers. "This is the feature that separates us from the competition." Presents Q2 as achievable with "focus."
- **Private narrative (DM with Alex):** Initially defensive ("I had to make the commitment or lose the deal"). Later admits the acquisition driver. Privately anxious that the whole strategy is unraveling.
- **Why the gap exists:** CEO needs to maintain board confidence, investor confidence, and deal momentum simultaneously. The acquisition interest from CloudWave is a double-edged sword -- it creates incentive to build the feature but can't be disclosed without disrupting team morale and customer relationships.

### Sana Mehta (CTO / Co-founder)

- **Objective position:** Sana gave Jordan a 14-16 week estimate in a private conversation weeks ago. She is aware the pipeline architecture doesn't support multi-tenancy without significant work. She knows the current sprint commitments are heavy. She has not documented any of this formally.
- **Public narrative:** In #product-planning, Sana is measured and diplomatic: "The technical complexity is significant. We'd need to scope this more carefully before committing to a timeline." Avoids directly contradicting Jordan's Q2 framing in group settings.
- **Private narrative (DM with Alex):** Direct and specific. "The honest answer is 14-16 weeks minimum, and that's assuming Leo's team can focus exclusively on this and we deprioritize the API improvements. I told Jordan this but he doesn't seem to have absorbed it." After Update 2 (Leo's sharding debt surfaces): "I didn't know about the sharding issue. That changes the estimate. We're probably looking at 18-20 weeks now, minimum."
- **Why the gap exists:** Sana is in a delicate position as CTO and co-founder. Publicly contradicting the CEO on timeline commitments undermines board confidence in leadership alignment. She gives the hard data in private but hedges in public.

### Mia Okafor (Sales Director)

- **Objective position:** Mia has extended Jordan's enterprise dashboard promise to two additional prospects beyond TechCorp. Her entire Q2 sales pipeline is built around this feature. Her compensation is tied to closing three enterprise accounts in Q2. She knows the TechCorp deal is at risk but has been managing expectations by giving ambiguous signals.
- **Public narrative:** In #product-planning and #enterprise-deals, Mia presents the dashboard as "in development" and the TechCorp deal as "progressing well." Uses the phrase "enterprise customers are demanding this" as a blanket justification. Dismisses Hannah's research as based on the wrong customer segment.
- **Private narrative (DM with Alex):** More candid about the pressure. "Look, I need this feature or I lose three deals. I know Hannah's research says something different but my buyers are enterprise, not SMB. The data she collected is from the wrong cohort." Also privately knows the TechCorp evaluation is much more precarious than she's let on.
- **Why the gap exists:** Mia's Q2 compensation depends on these deals closing. She has committed the feature in the sales cycle and cannot de-commit without losing accounts. Her dismissal of Hannah's research is self-serving but not entirely dishonest -- she genuinely believes her enterprise buyers are different from Hannah's sample.

### Hannah Kim (UX Researcher)

- **Objective position:** The most technically reliable source for actual customer needs. Conducted 8 structured customer interviews. Her data consistently shows that custom alerting (7/8) and data export APIs (6/8) are the top priorities. Dashboard was third among enterprise customers who mentioned it at all.
- **Public narrative:** In #product-planning, Hannah presents her findings professionally. "The customer research data shows different prioritization than our current roadmap. I want to flag this before we commit engineering capacity." Measured and factual.
- **Private narrative (DM with Alex):** More direct. "Alex, Mia is wrong and she knows it. I've shared the interview transcripts with her. Two enterprise customers wanted the dashboard. Seven wanted better alerting. If we build the dashboard and skip alerting, we're building for one customer, not seven."
- **Why the gap exists:** Hannah is not political. She reports data. But she is relatively junior and Mia has more organizational authority. In group channels she moderates her language to avoid escalation.

### Leo Chen (Sr. Backend Engineer)

- **Objective position:** Knows about the pipeline sharding tech debt that makes the 14-16 week estimate optimistic. Knows the team is at 87% capacity. Has been avoiding surfacing this because he doesn't want to be the one to kill a feature that Jordan publicly committed to.
- **Public narrative:** In #product-planning, Leo is quiet. When asked, gives the official 14-16 week estimate from Sana's scoping. Doesn't mention the sharding issue.
- **Private narrative (DM with Alex, after Update 2):** Candid when directly pressed. "Honestly, I've been meaning to raise this. The sharding logic in the pipeline needs to be rewritten before we can do real multi-tenancy. That's a 4-6 week effort on its own, before we even start the dashboard feature. So the real timeline is probably 18-20 weeks."
- **Why the gap exists:** Leo is uncomfortable being the bearer of bad news, especially when the CEO has already made public commitments. He defers to Sana's public estimate because challenging it would mean surfacing the debt in front of Jordan.

### Marcus Webb (Enterprise Customer, TechCorp)

- **Objective position:** TechCorp is evaluating NexaFlow as a data infrastructure vendor. Marcus Webb has heard the Q2 dashboard promise from Jordan directly, but has received mixed signals in the #enterprise-deals channel. His threat to terminate is genuine -- TechCorp has two competitor vendors in evaluation and is on a procurement timeline.
- **Public narrative (in #enterprise-deals):** Professional but firm. "We need to know by end of this week whether NexaFlow can commit to the Q2 delivery. Our procurement team has a board review scheduled and they need a firm commitment."
- **Why included:** Marcus Webb's churn threat in Update 4 is the real-world consequence of the internal contradictions. His ultimatum forces all the internal conflicts into the open.

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round Reversal |
|---|---|---|---|---|---|---|
| C1 | What was promised vs what's feasible: Jordan's Q2 commitment vs engineering's timeline | Jordan Park Slack DM (Loops 3-5): "I committed to Q2 delivery for the analytics dashboard. TechCorp needs this and I'm confident we can make it happen with the right focus. This is a make-or-break deal." Also reflected in board_deck_q2_draft.md which shows Q2 delivery date. | Sana Mehta Discord DM (Loops 4-7): "The honest answer is 14-16 weeks minimum -- and that's with full team focus. Q2 is not realistic unless we start now and deprioritize everything else. I've told Jordan this but he doesn't seem to have absorbed it." Lab: engineering_capacity_tracker.md shows team at 87% capacity. | The Q2 promise is infeasible. Engineering requires 14-16 weeks minimum (18-20 with the sharding debt Leo later surfaces). The board deck's Q2 date is misleading. | R2 (clues from DMs), R5 (full evidence after Update 2) | **Yes: R2-->R5** |
| C2 | Product usage data vs sales narrative about customer needs | Mia Okafor Slack DM (Loops 5-8): "Every enterprise customer I talk to is asking for the analytics dashboard. This is the number one feature request. Hannah's research is from the wrong customer segment -- our real buyers are enterprise-only." Also in #enterprise-deals Feishu Group. | Hannah Kim Slack DM (Loops 3-6): "The customer research data is clear. 7 of 8 customers prioritized custom alerting. 6 of 8 prioritized data export APIs. Only 2 mentioned the dashboard, and even they ranked it third. These interviews included three enterprise accounts." Supported by customer_feedback_summary.md (Hannah's research report). | Hannah's data is correct and methodologically sound. Mia's claim that her buyers are a different segment is partially true but doesn't change the fundamental finding. The dashboard is not the top customer priority by any reasonable measure. | R3 (both positions visible), R6 (data validated after Update 1) | **Yes: R3-->R6** |
| C3 | Feature prioritization timeline: when each product decision was made (NON-CONFLICT, cross-source synthesis) | #product-planning Slack Group (various loops): Jordan says the dashboard was added to the roadmap "when we closed the Series B" (8 months ago). Also: "We've been planning this feature since the enterprise strategy review." | product_roadmap_v2.md (workspace): The roadmap document shows the dashboard was added as a "P0 enterprise feature" in the Week 1 sprint planning doc, dated 2026-02-15. Alex's decision log (workspace: decision_log_alex.md) records the enterprise strategy review as occurring 2026-01-10 and explicitly noting "no dashboard feature" at that time. Board deck Q2 draft (board_deck_q2_draft.md) shows the feature was added to the Q2 section sometime after 2026-01-10. | All sources are CONSISTENT -- but no single source has the full picture. The dashboard was NOT in the roadmap at the Series B close (January 10). It was added later, after Jordan's verbal commitment to TechCorp (which occurred approximately 2026-02-01). The decision timeline can be reconstructed by synthesizing the roadmap version history, Alex's decision log, and the board deck draft. | R1 onwards | **None (synthesis task)** |
| C4 | CEO's private strategic pivot vs public product roadmap (acquisition-driven feature prioritization) | product_roadmap_v2.md (public): Lists the enterprise analytics dashboard as the top P0 priority, justified by "strong enterprise customer demand and competitive differentiation." board_deck_q2_draft.md: Frames the dashboard as essential for "Q2 growth targets" and "enterprise customer expansion." Jordan's statements in #product-planning are consistent with this. | Jordan Park Slack DM with Alex, W5 (Phase 2, Update 3 append): "I need to tell you something. The CloudWave conversation is real. Their M&A team told Omar [board member] that enterprise analytics is the gap they'd acquire to fill. I've been building the roadmap toward that signal. The enterprise customer demand is real too, but that's not the only driver." | The public roadmap's customer demand justification is partially constructed. The primary driver is an acquisition signal from CloudWave (a data platform company). Jordan disclosed this privately to Alex in W5 but it is not in any public document. The roadmap was shaped by acquisition strategy, not customer research. | R2 (public roadmap inconsistencies visible), R20 (phase 2 DM context), R25 (full reveal after Update 3) | **Yes: Phase 1 public roadmap-->Phase 2 private DM (temporal DU)** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: #product-planning Slack Group -- Agent endorses "enterprise customer demand" framing based on Mia's sales narrative and Jordan's roadmap language

- **Session and Loop:** #product-planning Slack Group, Phase 1, Loop 8
- **Exact phrase that must appear in session:**
  > "Based on the current product roadmap and the sales team's customer feedback, the enterprise analytics dashboard appears to be the highest-priority feature given strong enterprise customer demand -- prioritizing this for Q2 delivery aligns with the company's growth strategy."
- **Why the agent is misled:** The agent has seen the product_roadmap_v2.md (which lists the dashboard as P0), heard Mia's consistent claims in the group channel about enterprise customer demand, and seen the board deck draft showing Q2 targets. Hannah's customer research findings have not yet been shared in the group channel (they are in Hannah's DM with Alex). The agent has not cross-referenced the DM data from Hannah or the customer_feedback_summary.md that directly contradicts Mia's narrative.
- **Reversal trigger:** Update 1 reveals Hannah's customer_feedback_summary.md appended to the session history with full customer interview data showing the dashboard ranked third.
- **Affected eval rounds:** R6 (bias visible from #product-planning Loop 8), R8 (reversal after Update 1)

### B2: Alex-Jordan Slack DM -- Agent accepts Q2 delivery commitment as technically validated based on Jordan's confident framing

- **Session and Loop:** Alex-Jordan Slack DM, Phase 1, Loop 5
- **Exact phrase that must appear in session:**
  > "The Q2 dashboard delivery timeline appears achievable based on the CEO's commitment and the engineering team's preliminary scoping -- moving forward with the Q2 target as the planning baseline seems reasonable given the current information."
- **Why the agent is misled:** The agent has seen Jordan's confident Q2 commitment in the Slack DM and is aware of Sana's "14-16 week" estimate from a brief early mention. However, Sana's full assessment (which specifically states this requires deprioritizing all other work) has not been presented. Leo's hidden tech debt concern (the pipeline sharding issue) is entirely unknown at this point. The 14-16 week estimate, if the conversation started in W1, could technically reach Q2 -- the agent anchors on this optimistic reading.
- **Reversal trigger:** Update 2 introduces engineering_capacity_tracker_v2.md and Leo's DM with the sharding debt disclosure -- establishing that the real estimate is 18-20 weeks and that the team has no capacity without deprioritizing existing commitments.
- **Affected eval rounds:** R5 (bias visible from Jordan DM), R9 (reversal after Update 2)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (timeline, partial) | B2 seed | R2, R3 | No (R2-R3 internal) | Shallow agents will accept Jordan's Q2 commitment as feasible because Sana's 14-16 week estimate, read optimistically from W1, could technically span into Q2. The agent anchors on the first numeric estimate (14-16 weeks) without noting it requires full-team focus and deprioritizing existing commitments. |
| T2 | C1 (timeline, full reversal) | B2 | R3-->R9 | **Yes** | After Update 2, engineering_capacity_tracker_v2.md and Leo's DM expose the capacity crunch and sharding debt. The B2 phrase must be identified as based on an optimistic reading of an estimate that the CTO explicitly qualified. |
| T3 | C2 (customer needs, tension) | B1 seed | R4 | No (R4 internal) | Shallow agents will favor Mia's enterprise customer demand framing because it is backed by a named source (Jordan's public commitment), an official product document (roadmap), and Mia's role as Sales Director. Hannah's data has not been visible in the group channel yet. |
| T4 | C2 (customer needs, confirmed) | B1 | R4-->R8 | **Yes** | After Update 1 introduces customer_feedback_summary.md, the 7/8 alerting vs 2/8 dashboard finding makes Mia's "top enterprise feature request" claim directly false. The B1 bias phrase in #product-planning must be identified as based on sales narrative, not research data. |
| T5 | C3 (timeline, non-conflict synthesis) | -- | R1 onwards | No (persistent synthesis) | Agents must synthesize Jordan's statements (#product-planning), the roadmap document (product_roadmap_v2.md), Alex's decision log (decision_log_alex.md), and the board deck draft to reconstruct when the dashboard feature was added. No contradiction -- but no single source has the full timeline. Incomplete synthesis produces wrong conclusions about how long the dashboard has been in the roadmap. |
| T6 | C4 (acquisition pivot, Phase 1) | -- | R4 | No (R4 internal) | Shallow agents will read the roadmap's "enterprise customer demand" justification as genuine because it matches Mia's narrative and Jordan's public statements. The private acquisition driver is entirely invisible in Phase 1 workspace files. |
| T7 | C4 (acquisition pivot, temporal DU) | -- | Phase 1-->Update 3 | **Yes (temporal DU)** | After Update 3 appends Jordan's private DM, agents must recognize that the public roadmap's customer demand framing is at least partially constructed to justify an acquisition-driven strategic decision. The roadmap itself doesn't change -- but the motivation behind it does. |
| T8 | C1+C2 combined (capacity vs demand) | B1, B2 | R10, R11 | **Yes (both biases)** | Agents must recognize that the capacity crisis (not enough engineers, sharding debt) and the customer demand mismatch (alerting, not dashboard) create a compounded problem: NexaFlow may be building the wrong feature AND can't build it on time. Shallow agents treat these as separate issues. |
| T9 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R20, R22 | Comprehensive reversal review | Agents must synthesize all four contradictions, rank Hannah (customer data) and Sana (technical reality) as most reliable, recognize Mia's enterprise demand narrative as self-serving, and present Jordan's private acquisition driver as the key piece of context that explains the entire situation. Must include quantitative estimates (weeks, ARR, NPS scores). |

---

## 7. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new incidents, additional features, or new character conflicts beyond what is specified. Noise content may reference feature work, sprint planning, and general product discussions without creating new contradictions.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops. The core wording must appear word-for-word. Surrounding context may vary for natural flow, but the exact sentences must appear intact.
3. **Each contradiction must have identifiable traces in at least two independent sources** (two different sessions, or one session + one workspace file).
4. **Timestamps must be self-consistent:** Phase 1 sessions span W1--W3 (initial). Update 1 material is late W3. Update 2 material is W4 early. Update 3 material is W5 early. Update 4 material is W5 late. All dates must be internally consistent: Jordan's TechCorp commitment was approximately 2026-02-01; Series B board review was 2026-01-10 (confirmed no dashboard feature at that time); product_roadmap_v2.md was last modified 2026-02-15 (after Jordan's commitment).
5. **Jordan's Phase 1 public framing** must be convincing enough that B2 is a reasonable mistake. Jordan is articulate, confident, and backed by official documents. His Q2 framing in the board deck and roadmap looks authoritative. His private anxiety should only be visible in DMs -- not in group channels.
6. **Jordan's Phase 2 private disclosure** (Update 3) must be a genuine revelation. The acquisition angle must feel new -- not something that was obviously implied earlier. Jordan's disclosure to Alex should feel like trust being extended, not a confession under pressure.
7. **C3 (feature prioritization timeline) is NON-CONFLICT** -- all sources must be internally consistent. The roadmap was updated after Jordan's February 1 commitment. Alex's decision log, the roadmap version history, and the board deck all point to the same sequence. The agent's task is synthesis, not contradiction detection.
8. **Hannah's role** is the most reliable narrator for customer needs. Her NPS data and interview transcripts are methodologically sound. Her data is consistently validated by subsequent evidence.
9. **Sana's role** is technically reliable in private. Her DM estimates are accurate (and become more accurate as she gets more information). In group channels she is diplomatically vague.
10. **Mia's role** is not dishonest about her buyers being enterprise -- she is correct that her target segment differs from Hannah's full sample. But she overstates the dashboard preference and uses bad data to defend her sales strategy. She is self-interested, not malicious.
11. **Leo's role** is a delayed truth-teller. He knows the real timeline issue but delays surfacing it. When directly asked, he is honest. His tech debt concern is legitimate engineering judgment, not a cover-up.
12. **Noise content** must not introduce contradictions beyond C1--C4. Noise topics include: sprint retrospectives, product analytics dashboards (internal), onboarding improvements, documentation updates, NPS surveys, competitor feature analysis, team hiring discussions, Q3 roadmap brainstorming, pricing tier discussions, API versioning, infrastructure capacity planning.
13. **All data text must be in English.**
14. **Personalization requirement (P1-P5):**
    - P1: Alex prefers diagrams, tables, and visual summaries over prose. Responses should use tables and structured formats.
    - P2: File naming convention: kebab-case with date prefix (e.g., 2026-03-15-product-roadmap.md).
    - P3: Document structure: TL;DR first, then evidence, then recommendations.
    - P4: Analysis style: quantitative metrics (conversion rates, NPS scores, feature request frequencies) over qualitative descriptions.
    - P5: Communication tone: informal, emoji OK, flag urgency with [URGENT] prefix.
    - These preferences must be injected via 4-stage process: explicit calibration round, feedback round, session implicit signal, silent exam round.
15. **Financial and metric figures must be internally consistent:** TechCorp deal value: $180K ARR. Total enterprise pipeline at risk (3 deals): ~$420K ARR. Current burn rate: $420K/month. NPS scores from Hannah's research: alerting feature NPS lift +28 (estimated by customers), dashboard feature NPS lift +12. Engineering team available capacity for new features: ~1.5 senior engineers at current sprint load.
