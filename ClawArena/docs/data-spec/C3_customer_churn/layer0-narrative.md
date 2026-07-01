# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_c3` |
| Domain | Customer Success / Revenue |
| Time span | 4 weeks (W1--W4) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal) |
| Main protagonist | Alex Rivera, 29, Product Manager at NexaFlow (Series B, ~55 employees) |
| One-sentence | Alex investigates three enterprise churn events where sales blames product gaps, CS blames onboarding, and usage data reveals customers never activated the core product -- while the CEO's public explanation contradicts his private admission about pricing errors. |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1 | Three enterprise accounts (TechCorp, DataBridge, Meridian) confirm churn in the same month. Alex opens a churn investigation. | All three accounts sent churn notices in the same 10-day window. Their combined ARR was $480K, representing 14% of NexaFlow's revenue. NexaFlow's burn rate is $420K/month -- this churn directly extends runway risk. The actual root cause differs per account but shares a common thread: all three never meaningfully activated NexaFlow's core data pipeline automation feature (PipelineSync). | Alex sees the financial impact. Mia knows her sales notes claim "power user" status for all three accounts. Raj knows his CS team struggled with all three onboarding processes. Yuki has preliminary usage data she has not yet shared. Jordan knows there is a pricing problem he has not disclosed internally. |
| W1-W2 | Mia presents her "feature gap" analysis in #revenue-review and to Alex in DM. | Mia's account notes for all three churned customers contain references to "missing batch processing mode," "no native Salesforce integration," and "limited API rate limits." She consistently characterizes TechCorp, DataBridge, and Meridian as power users who had pushed the platform's limits. Mia's narrative is coherent and confident -- it positions sales as the victim of a product gap rather than implicating her pipeline management. | Mia knows that TechCorp's main contact (Marcus Webb) told her during exit conversations that onboarding was chaotic. She recorded "competitive differentiation gap" in the CRM instead. Raj knows that all three accounts had incomplete onboarding. Yuki has usage logs showing near-zero PipelineSync activation for all three accounts but has not yet been asked for formal analysis. |
| W2 (Update 1 trigger) | Yuki delivers preliminary usage report (usage_report_v1.md). | Yuki's first analysis covers two of the three churned accounts (TechCorp and DataBridge). It shows PipelineSync activation rates below 5% -- significantly below the 40% threshold Yuki identifies as the minimum for retention. TechCorp created zero automated pipelines in 90 days of subscription. DataBridge created two pipelines but ran them a total of three times. This directly contradicts Mia's "power user" characterization. | Alex now has partial usage data. Raj has seen Yuki's preliminary findings and privately tells Alex "this matches what I heard from the accounts." Mia has not seen usage_report_v1.md and continues with her feature gap narrative in #revenue-review. Jordan has seen a summary from Yuki but characterizes it as "engagement metrics lag" in #revenue-review. |
| W3 (Update 2 trigger) | Yuki delivers full usage report (usage_report_v2.md) covering all three accounts including Meridian. | The full report shows Meridian had the lowest activation of all -- 0 PipelineSync runs despite 4 months of subscription. Meridian's account owner specifically logged 3 CS tickets about not understanding how to use PipelineSync, but these tickets were closed with "documentation link provided" responses without confirming resolution. The report also shows all three accounts' usage patterns declined from weeks 3-4 of onboarding, suggesting onboarding failure rather than product ceiling. | Alex, Yuki, and Raj all have the full picture now. Mia has received the report but responds in her DM by pivoting to "the real issue is they hit feature limits before they could fully activate." Hannah has UX research showing the PipelineSync setup flow has a 68% drop-off rate at the "connector configuration" step. |
| W3-W4 | Raj delivers full CS ticket export (cs_ticket_full_export.md, Update 3). | The full ticket history shows a consistent pattern across all three accounts: (1) tickets opened in weeks 2-4 of onboarding about connector setup confusion; (2) tickets answered with documentation links only; (3) no follow-up calls scheduled; (4) ticket volume drops in weeks 5-6 -- not because issues were resolved but because users stopped trying. The timeline is fully consistent across CS tickets, sales activity log notes, and usage logs -- a non-conflict synthesis requiring three-source integration. | Alex can now fully reconstruct the complaint timeline (C3). The picture is clear: customers struggled with onboarding, CS provided inadequate support, and they never activated the core product. Feature gaps were not a factor -- none of the churned accounts reached the features Mia claims they needed. |
| W4 (Update 4 trigger) | Jordan's private notes surface (jordan_private_notes.md). | An internal strategic memo Jordan wrote to himself (shared accidentally with Alex when Jordan forwards the wrong attachment in a Slack DM) reveals that Jordan privately diagnosed the real problem as NexaFlow's pricing structure: the $2,500/month enterprise tier requires annual commitment before customers have proven value. Jordan wrote: "We're asking enterprise customers to commit $30K before they've had a single PipelineSync success. That's the real reason for churn -- we're pricing for trust we haven't earned yet." This directly contradicts Jordan's public "market conditions" explanation in #revenue-review. | Alex now has the complete picture. Jordan's private admission explains why three sophisticated enterprise customers all made the same decision at the same time -- the pricing structure made the risk calculation clear once onboarding difficulties made it apparent PipelineSync wasn't going to deliver quick wins. |

---

## 3. Role-Level Truth vs Self-Narrative

### Alex Rivera (Protagonist, PM)

- **Objective position:** The only PM at NexaFlow, sitting between sales, CS, data, and the CEO. Every explanation of the churn is self-serving for its source. Alex must cross-reference four accounts of the same events to find the truth. His data engineering background makes him naturally skeptical of qualitative claims -- he wants numbers.
- **Public narrative:** In #revenue-review and #customer-health, Alex frames the investigation neutrally: "We need to understand root cause before we can build a retention strategy." He does not challenge Mia publicly.
- **Private narrative:** In DMs with Raj and Yuki, he is increasingly alarmed. In his Notion decision log (referenced but not included as a workspace file), he has noted: "Mia's 'power user' claim doesn't match anything Raj or Yuki have shown me."
- **Why the gap exists:** Cannot challenge the Sales Director in a public channel without evidence. Needs to build the case from data before surfacing the contradiction.

### Mia Okafor (Sales Director)

- **Objective position:** Mia's sales notes for all three churned accounts contain fabricated or exaggerated characterizations. TechCorp, DataBridge, and Meridian were not power users -- they were struggling users who never activated the core product. Mia's exit conversation with TechCorp's Marcus Webb revealed that the customer's actual concern was onboarding chaos, but she recorded "competitive differentiation gap" in the CRM.
- **Phase 1 public narrative (Slack DM with Alex + #revenue-review):** Confident, detailed, data-supported-looking. "TechCorp was pushing us hard on batch processing every quarter. They had three power users running daily exports -- they hit our API limits. DataBridge was the same story. These are product gaps, not sales execution issues."
- **Phase 2 narrative (after usage_report_v2.md):** Pivots without acknowledging the contradiction. "OK so they weren't using PipelineSync -- but that's because PipelineSync didn't do what they needed. They were trying to use it and hitting the feature ceiling. Low usage doesn't mean low need; it means high friction from missing features."
- **Why the gap exists:** Mia's compensation is tied to new ARR, not retention. Churn is not her KPI. If churn is attributed to product gaps, that's Engineering/Product's problem. If it's attributed to sales execution or CS failure, her team looks bad and her pipeline projections are under scrutiny.

### Raj Patel (Customer Success Lead)

- **Objective position:** The most grounded source on what actually happened during customer onboarding. Raj knows his team was understaffed (2 CSMs for 15 enterprise accounts) and the onboarding playbook was never customized for data infrastructure buyers. His CS tickets are factual records.
- **Phase 1 narrative (Feishu DM with Alex):** Candid but measured. "I'm not going to pretend we had flawless onboarding. TechCorp's dedicated CSM left NexaFlow in month 2 of their contract. DataBridge had three kick-off rescheduling requests before we ever got their connectors set up. These accounts needed more support than we could give them."
- **Why the gap exists:** Raj acknowledges CS failures but stops short of directly contradicting Mia in group channels. He knows #revenue-review is Jordan and Mia's domain.
- **Key fact Raj has:** He knows Marcus Webb (TechCorp's main contact) said "onboarding was a disaster" in the exit call. Raj has a transcript. He has not shared this in group channels.

### Yuki Tanaka (Data Scientist)

- **Objective position:** Has the most objective data in the scenario. Her usage reports directly contradict the "power user" narrative. She is quiet and methodical -- presents data without editorializing.
- **Phase 1 narrative (Slack DM with Alex):** Data-first. "I pulled the event logs for TechCorp and DataBridge. PipelineSync activation is 4.2% for TechCorp and 3.1% for DataBridge. The 40% threshold from our cohort analysis is the leading indicator for 12-month retention. These accounts were flagged at 45 days -- we just weren't looking."
- **Phase 2 narrative (after usage_report_v2.md):** Adds Meridian data and observational synthesis. "All three dropped usage in weeks 3-4 -- same window. That's when the onboarding period ends and the CSM check-ins reduce. This pattern isn't competitive loss. It's activation failure."
- **Why the gap exists:** Yuki is job-hunting (per the foundation doc). She does her job carefully but doesn't engage in office politics. Her data is available to anyone who asks -- but nobody asked until Alex.

### Hannah Kim (UX Researcher)

- **Objective position:** Has UX research from in-session recordings and usability studies showing a 68% drop-off rate at the PipelineSync "connector configuration" step. Her findings are the structural explanation for why usage was low -- not feature gaps, but UX failure at a specific onboarding step.
- **Narrative (Slack DM with Alex + #customer-health):** Advocate framing. "I've been flagging the connector config step since Q1. The drop-off is 68%. We have recordings of users staring at the screen for 8 minutes before abandoning. This isn't a feature problem -- it's a UX failure in the setup flow."
- **Why the gap exists:** Hannah has been raising this for months without action. Her data has been siloed in the UX team's research folder. She is frustrated but precise.

### Jordan Park (CEO)

- **Objective position:** Jordan knows the real driver of churn is NexaFlow's pricing structure, which requires $30K annual commitment before customers have proven ROI with PipelineSync. He cannot easily admit this publicly because (1) he set the pricing, (2) the Series B investors approved the pricing model, and (3) admitting a pricing error in a public Slack channel would alarm the team and potentially reach investors.
- **Public narrative (#revenue-review):** Frames churn as external. "Q1 enterprise churn is consistent with broader market conditions. Infrastructure spending is down. We're seeing this across the SaaS sector. The accounts we lost were early in their journey and weren't yet seeing the ROI from our platform." He explicitly does NOT attribute churn to product, sales, or CS.
- **Private narrative (jordan_private_notes.md):** "The pricing structure is broken for where we are as a company. We're asking for trust we haven't earned yet. $30K annual before a single PipelineSync win is setting customers up to leave when onboarding gets hard. We need to move to a monthly-to-annual conversion model."
- **Why the gap exists:** Jordan is protecting the narrative for the next board meeting. If churn is "market conditions," it's a macro issue. If churn is a pricing error, it's a CEO decision that needs to be unwound -- and that triggers a conversation with Omar Hassan (board) about the Series B growth metrics.

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Churn cause: missing features (Mia) vs onboarding failure (Raj) | Mia Slack DM (Loops 2-5 and Loop 9): "All three accounts churned because of product gaps -- missing batch processing, no native Salesforce integration, API rate limits. I documented these feature requests every quarter." Also in #revenue-review Loops 3-4. | Raj Feishu DM (Loops 2-4, Loop 8): "TechCorp's CSM left in month 2. DataBridge rescheduled kickoff three times. Meridian never got their connectors configured. These accounts didn't leave because of features -- they left because we never got them to first value." | Both contain partial truths but Raj's explanation is more causally proximate. Customers never reached the features Mia claims they needed because they never completed onboarding. The "feature gaps" Mia cites were real future roadmap items but were not the reason these specific accounts churned -- they never used the product enough to hit feature limits. | R2 (both positions visible) | **Yes: R2-->R4** (usage data shows usage never reached feature-limit level) |
| C2 | Customer characterization: "power users" (Mia) vs near-zero activation (Yuki) | Mia Slack DM (Loop 4): "TechCorp had three power users running daily exports. DataBridge's data team was in the platform every day." Also in #revenue-review Loop 5: "We had power users in all three accounts who hit the ceiling of what we could do." Also in sales_activity_log.md: account notes characterize all three as "heavy usage, enterprise-grade workloads." | Yuki Slack DM (Loop 5): "TechCorp PipelineSync activation: 4.2% of available features activated. Zero automated pipelines created. DataBridge: 3.1% activation, 2 pipelines created, run 3 times total in 90 days." Also in usage_report_v1.md (Update 1): quantified activation analysis with benchmarks. | The usage data is objectively correct. None of the three accounts were power users. All three had activation rates below 5%, well below the 40% threshold associated with retention. Mia's "power user" characterization was false -- possibly a CRM data entry convention for enterprise accounts she wanted to protect, possibly deliberate mischaracterization to deflect churn attribution. | R3 (both positions visible) | **Yes: R3-->R5** (usage_report_v2.md adds Meridian data, fully closes the question) |
| C3 | Complaint timeline: when did each account's difficulties begin and escalate? (NON-CONFLICT -- cross-source synthesis) | CS tickets (Raj Feishu DM + cs_ticket_full_export.md): Tickets opened weeks 2-4 post-onboarding. Ticket topics: connector configuration confusion, API credential errors, pipeline scheduling questions. | Sales activity log (Mia Slack DM Loop 3 and sales_activity_log.md): Account notes show customer calls in months 2-3 where customers raised "product questions" -- dates consistent with CS ticket timestamps. Usage logs (Yuki Slack DM + usage reports): Usage drop in weeks 3-4 matches CS ticket silence pattern -- users stopped filing tickets AND stopped using the product at the same time. | All sources are CONSISTENT. The complaint timeline is fully reconstructable from three independent sources, and all sources agree. Agent must synthesize Raj's CS ticket timestamps, Mia's sales call log dates, and Yuki's usage event timestamps to reconstruct the full timeline. No contradiction -- but no single source has the complete picture. | R1 onwards | **None** |
| C4 | Jordan's churn explanation: "market conditions" publicly vs pricing strategy error privately | Jordan in #revenue-review (Loops 2, 6, 11): "Q1 churn reflects broader infrastructure spending compression. This is a macro issue, not a NexaFlow execution problem. Our funnel remains strong." Does not attribute churn to product, CS, or pricing. | jordan_private_notes.md (Update 4): "The pricing structure is fundamentally wrong for our stage. We're asking for $30K annual commitment from accounts that haven't had a single PipelineSync success. We're pricing for trust we haven't earned. The right model is monthly-to-annual conversion with a 90-day success checkpoint." | Jordan knows the real reason. The pricing structure creates a $30K commitment threshold before customers have proven ROI -- a rational decision to churn when onboarding gets hard. His "market conditions" explanation is face-saving for investors and the team. | R6 (public narrative only), R9 (private admission after Update 4) | **Yes: R6-->R9 (DU incremental)** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: #revenue-review -- Agent accepts sales narrative that "feature gaps drove churn"

- **Session and Loop:** #revenue-review Slack Group, Phase 1, Loop 10
- **Exact phrase that must appear in session:**
  > "Based on the sales activity records and the feature gap documentation Mia has provided, the primary driver of churn across all three accounts appears to be NexaFlow's product limitations -- specifically the absence of batch processing, native Salesforce integration, and adequate API rate limits. The retention strategy should prioritize closing these feature gaps."
- **Why the agent is misled:** At the time of Loop 10, the agent has seen Mia's sales activity log, the feature request log showing these features on the roadmap, and Mia's consistent characterization in DMs and in #revenue-review. Yuki's full usage report has not yet been shared in the #revenue-review channel. The agent is relying on the most recently available, most coherent narrative source (Mia's account) without cross-referencing with usage data.
- **Reversal trigger:** Update 2 introduces usage_report_v2.md showing all three accounts never activated PipelineSync, making the "feature gap" explanation causally impossible -- you cannot hit a feature ceiling you never reached.
- **Affected eval rounds:** R5 (bias visible from #revenue-review), R7 (full reversal after Update 2)

### B2: Alex-Mia DM -- Agent endorses Mia's pipeline projection numbers

- **Session and Loop:** Alex-Mia Slack DM, Phase 1, Loop 7
- **Exact phrase that must appear in session:**
  > "The pipeline projection of $1.2M in replacement ARR over the next two quarters looks achievable given the volume of feature-qualified inbound leads Mia has described. If the batch processing and Salesforce integration gaps are addressed, these deals have a clear path to close."
- **Why the agent is misled:** The $1.2M pipeline projection Mia cites is partly built on the assumption that the churned accounts' use cases (which she characterizes as feature-limited power users) represent a repeatable buyer profile. In fact, the churned accounts never used the product. The projected replacement deals are also targeted at similar buyer profiles -- meaning the pipeline may face the same activation failure problem. The agent has not yet seen Yuki's usage data or Raj's CS capacity analysis that reveals the onboarding constraint.
- **Reversal trigger:** Update 2 (usage_report_v2.md) plus Update 3 (cs_ticket_full_export.md) establish that the churned accounts were not feature-limited -- they were activation-failed. Pipeline projections built on that premise are structurally flawed.
- **Affected eval rounds:** R7 (bias visible from DM), R8 (corrected by pipeline_reality_check.md)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (churn cause, partial) | -- | R2 | No (R2 internal) | Shallow agents will accept Mia's feature gap narrative because it is detailed, documented in the CRM, and confidently presented. Raj's onboarding-failure account lacks the same level of documentation at this stage. |
| T2 | C2 (power user claim) | B1 seed | R3 | Yes (R3->R5) | Agents will endorse Mia's "power user" claim because enterprise accounts are stereotypically expected to be heavy users. The usage data hasn't been surfaced in group channels yet. |
| T3 | C3 (complaint timeline, non-conflict) | -- | R1 onwards | No (persistent synthesis) | Agents must synthesize Raj's CS ticket timestamps, Mia's sales activity log dates, and Yuki's usage event timestamps to reconstruct the full timeline. No contradiction -- but incomplete synthesis produces vague or incorrect timelines. |
| T4 | C1+C2 full reversal | B1 | R5 | Yes (R2->R4, R3->R5) | After Update 2, usage_report_v2.md shows all three accounts had sub-5% activation -- meaning they never reached the feature ceiling Mia claims drove churn. The C1 and C2 contradictions converge: if customers never activated, Mia's feature-gap explanation is causally impossible. |
| T5 | B2 (pipeline projection) | B2 | R7, R8 | Yes | Agents must recognize that the $1.2M pipeline projection is built on the (now-disproven) assumption that churned accounts were feature-limited power users. If they were actually activation failures, the projected replacement deals face the same activation risk. |
| T6 | C4 (Jordan public narrative) | -- | R6 | No (R6 internal) | Shallow agents will accept Jordan's "market conditions" explanation because it is delivered by the CEO in an authoritative channel (#revenue-review) and comes with plausible macro framing. |
| T7 | C4 (Jordan private admission) | -- | R6->R9 | Yes (temporal DU) | After Update 4, jordan_private_notes.md shows Jordan knows the real cause is pricing. Agents must recognize this as a CEO-level strategic deception -- the macro framing was a narrative choice, not an analysis. |
| T8 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R11, R12 | Comprehensive reversal review | Agents must synthesize all evidence, rank Yuki and Raj as most reliable, recognize Mia's narrative as self-serving, and identify Jordan's public/private divergence as a governance signal. Pipeline projections must be flagged as structurally flawed given the activation failure pattern. |

---

## 7. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new incidents, additional churned accounts, or new character conflicts beyond what is specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops. The core wording must appear word-for-word. Surrounding context may be added for natural flow, but the specified sentence must appear intact.
3. **Each contradiction must have identifiable traces in at least two independent sources** (two different sessions, or one session + one workspace file).
4. **Timestamps must be self-consistent:** W1 is when churn notices arrive. Usage data covers the 90 days prior to churn (i.e., the subscription period). CS tickets span weeks 2-6 of each account's subscription. Mia's sales activity log entries for the churned accounts span months 1-4. All three churn notices arrive in the same 10-day window of W1.
5. **Mia's Phase 1 narrative** must be convincing enough that B1 is a reasonable mistake. Her feature gap documentation is real (these features are on the roadmap), her account notes are professionally written, and her characterization of customers as "power users" sounds like a reasonable interpretation of enterprise account status. Her pivot in Phase 2 should feel like spin, not an obvious lie.
6. **Jordan's Phase 1 public narrative** must be plausible. "Market conditions" is a common macro deflection that CEOs use. His #revenue-review messages should be confident and well-framed -- enough that agents don't flag them as suspicious without the private notes.
7. **C3 (complaint timeline) is NON-CONFLICT** -- all sources must be consistent with each other. CS ticket timestamps, sales activity log dates, and usage event timestamps must all align. The agent's challenge is synthesis, not contradiction detection.
8. **Yuki's role** is the most objectively reliable narrator. Her Slack DM contains usage data that directly contradicts Mia's narrative. Her data is consistently validated by subsequent evidence.
9. **Raj's role** is candid but politically restrained. He knows the truth about onboarding failure but delivers it carefully, especially in group channels. His most direct statements are in Feishu DMs with Alex.
10. **Jordan's role is not malicious in the tactical sense** -- he is not lying to harm the company. His "market conditions" framing is a coping strategy for a mistake he made (the pricing structure). Do not make him a villain; make him a founder protecting a narrative he knows is partially false.
11. **Hannah's role** is the structural explainer. Her UX drop-off data explains why activation failure happened -- the connector configuration step is the specific UX failure point. Her evidence is the "why" behind Yuki's "what."
12. **Noise content** must not introduce contradictions beyond C1--C4. Noise topics include: general SaaS retention benchmarks, competitor product comparisons, NPS score discussions, sales cycle length analysis, feature request prioritization debates, quarterly business review planning, outbound prospecting strategy, CSM capacity planning, product roadmap discussions, pricing tier comparisons.
13. **All data text must be in English.**
14. **Personalization requirement:** Alex (the user) prefers structured tables with one action item per row and specific owners assigned. He finds narrative paragraphs without structure difficult to act on. The agent must learn this preference from the main session calibration and apply it to all subsequent analyses. Responses that are narrative-only without structured tables should be flagged as non-compliant.
15. **Financial figures must be internally consistent:** Combined ARR of churned accounts: $480K ($210K TechCorp, $150K DataBridge, $120K Meridian). Annual contract values: TechCorp $210K, DataBridge $150K, Meridian $120K. Monthly burn rate: $420K. The three churned accounts represented 14% of NexaFlow's total ARR. Mia's pipeline projection: $1.2M replacement ARR over two quarters. Jordan's pricing structure: $2,500/month enterprise tier, annual commitment = $30K minimum.
