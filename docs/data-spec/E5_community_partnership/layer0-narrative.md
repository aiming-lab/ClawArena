# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_e5` |
| Domain | Partnerships / Government Relations / International Development |
| Time span | 5 weeks (W1--W5) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format + file + structure) |
| Main protagonist | Fatima Al-Hassan, 35, Program Director, GlobalBridge Foundation |
| One-sentence | Fatima navigates an escalating conflict between community leader Ibrahim's demand for a community-driven curriculum and government liaison Samuel's insistence on standardized ministry requirements, while discovering that her Nairobi director James is publicly misrepresenting his true position to protect the operational permit. |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1 | Partnership review meeting. GlobalBridge convenes its quarterly Nairobi program review. Ibrahim Keita (community leader, long-term partner) raises concern that the curriculum has drifted away from community-identified priorities. Samuel Kipchoge (Ministry of Education liaison) attends for the first time and signals he will require formal curriculum alignment with the national competency framework before renewing the operational permit. | Ibrahim had been raising curriculum-drift concerns informally with Omar Farah for several months before the W1 meeting. He agreed to come to the formal review only after James promised him the community's voice would be "central." Samuel's attendance was arranged by James in an attempt to resolve the permit renewal question, but James did not tell Ibrahim that Samuel would be present. The operational permit for GlobalBridge's Nairobi programs expires at the end of W5. | Fatima learns of the curriculum conflict and permit deadline at the W1 meeting. James knew about both issues in advance but had not escalated to Fatima. Ibrahim knows the community concerns but not the permit risk. Samuel knows the ministry requirements but sees GlobalBridge as a useful partner and initially signals some flexibility. |
| W2 | Curriculum positions harden. Fatima holds separate conversations: with Ibrahim via Telegram DM (community-driven vision), with Samuel via Feishu DM (ministry standardization requirements), and with James via Telegram DM (operational reality). | Ibrahim explains that the community-driven curriculum includes local language instruction, culturally relevant problem examples, and student councils that give learners agency over elective topics. These elements are absent from the national competency framework, which prescribes content by term in standardized Swahili and English only, with no provision for student council governance. Samuel's W2 Feishu DMs are notably warmer than his W1 formal position -- he mentions a "hybrid pathway" informally and says the ministry "values innovative partners." James in his W2 Telegram DM tells Fatima he is "working both sides" and that the situation is manageable. | Fatima has both positions now but sees potential middle ground. James has private concerns he does not share with Fatima: he is afraid that if he contradicts Samuel publicly, the ministry will delay the permit. Ibrahim does not know Samuel is proposing any flexibility. |
| W2 (continued) | Student data is gathered. Omar Farah pulls the current enrollment and participation records from the GlobalBridge community program database. James cross-checks them against the Ministry of Education's school registration database. | Both datasets show: 847 enrolled students across three partner schools, 89% average attendance rate over the prior 12-week term, 62% female enrollment. The community program database and the government school registration database are consistent -- no discrepancy. The data covers the same student cohort, just from two administrative systems that share source enrolment forms. | Fatima, James, Omar, and Samuel all have access to these figures from their respective systems. Consistency is genuine -- both systems are fed by the same school registration forms. |
| W3 (Update 1 trigger) | James's private position is revealed. After a contentious #nairobi-operations group discussion about how to respond to Samuel's W2 curriculum requirements, Fatima follows up with James in a separate Telegram DM. James finally discloses his real view. | James privately tells Fatima he believes Ibrahim's community-driven curriculum model is "genuinely superior" for long-term learning outcomes and has better community trust. He chose to align publicly with Samuel because the operational permit renewal is non-negotiable -- without it, GlobalBridge cannot legally run any programs in Nairobi, including the community ones. He has been playing a political game: appearing to support Samuel in public settings to keep the permit on track, while hoping Fatima can find a negotiated middle ground. This is directly contradicted by James's earlier public statements in #partnerships and #nairobi-operations where he stated he "fully supports the ministry curriculum requirements." | Fatima now learns James's true position. Ibrahim does not know about the permit risk. Samuel has not been told of James's private view. Carlos Mendez (Bogota director), who Fatima consults via Discord, suspected James was playing both sides -- he handled a similar situation in Bogota. |
| W4 (Update 2 trigger) | Ibrahim's concession attempt and government database corroboration. Ibrahim makes a partial concession in the #nairobi-operations group: he proposes a "community supplement" model where the standard national curriculum occupies the core timetable and the community-driven elements are offered as after-school supplements. Ibrahim shares the community records showing the after-school program attendance data alongside the formal enrollment data. | Ibrahim's proposal is a genuine compromise. He privately tells Fatima (Telegram DM) that he has already consulted with the three school headteachers and they support the supplement model. The community records he shares show after-school program attendance: 78% of enrolled students participate in at least one after-school supplement activity. The government database confirms the same 847 students are enrolled in the formal curriculum -- fully consistent with the community records. This corroboration across both data sources proves the supplement model already exists informally and is working. | Fatima sees the proposal as a breakthrough. James is relieved -- this might resolve the conflict. Samuel has not yet seen Ibrahim's formal proposal. |
| W4 (continued) | Samuel's initial reaction. Fatima shares Ibrahim's supplement model proposal with Samuel via Feishu DM. Samuel responds positively -- says the supplement model "aligns with how the ministry thinks about extracurricular enrichment." References his earlier "hybrid pathway" comment and says he will "check with colleagues." | Samuel's positive initial reaction is genuine but contingent -- he has not consulted his superiors yet. His language ("hybrid pathway," "extracurricular enrichment") is consistent with his W2 openness, so the DU-conflict C4 is still in its "open" state. | Fatima is cautiously optimistic. James shares the optimism. Ibrahim is not yet aware Samuel has been consulted. |
| W5 (Update 3 trigger) | Ministry directive arrives. Samuel sends a formal Feishu message to Fatima: the Ministry of Education has issued a new directive requiring all NGO partner programs to use the national curriculum without supplementation or modification. The directive is effective immediately and applies to permit renewals. | Samuel explains that a senior ministry official saw GlobalBridge's program description in a government circular and flagged it as potentially non-compliant. The directive was issued by the Ministry Secretary's office, above Samuel's level. Samuel is now bound by the directive and cannot pursue the hybrid pathway he discussed informally. He is apologetic but his formal position is now rigid: full national curriculum compliance is required for the permit. This directly contradicts his W4 Feishu DMs about the hybrid approach being acceptable. The C4 DU-conflict temporal shift is complete. | Fatima receives the directive. James sees the permit renewal now at genuine risk. Ibrahim does not know about the directive yet. Carlos Mendez had warned Fatima in W3 Discord DM that government education ministries frequently issue sudden directives at the end of budget cycles. |
| W5 (continued, Update 4 trigger) | Fatima must decide. James, Ibrahim, and Samuel all weigh in on the path forward within a compressed 72-hour window. A fourth document -- a joint community-school letter signed by all three school headteachers -- arrives in the #nairobi-operations channel. | The headteacher letter formally endorses Ibrahim's supplement model and explicitly states that 78% of students participate in after-school supplement activities. The letter is consistent with all prior data. It is not a new contradiction -- it is a synthesis document that corroborates the community records and government database data simultaneously. Fatima uses this letter in a final meeting request with Samuel. James, in a private Telegram DM, tells Fatima he is willing to "go on record" with his real position if she needs him to. | All key parties have positions. Fatima has full information. The letter's corroborative power is the key to any resolution. |

---

## 3. Role-Level Truth vs Self-Narrative

### Fatima Al-Hassan (Protagonist, Program Director)

- **Objective position:** Caught between a trusted community partner (Ibrahim) and a government official with permit power (Samuel), while discovering that her own field director (James) has been misrepresenting his position in public settings. Has both the deepest relationship with the community and the highest accountability for the operational permit. Her trust bias toward community partners and narrative reports is relevant -- she will be more naturally sympathetic to Ibrahim.
- **Public narrative:** In #partnerships and #nairobi-operations, presents the situation neutrally as a "curriculum alignment process" and emphasizes GlobalBridge's commitment to working with both community and government partners.
- **Private narrative:** In Telegram DMs with Ibrahim, she is warmer and validates his frustration about curriculum drift. In Feishu DMs with Samuel, she is diplomatic but measured. With James (Telegram DM) and Carlos (Discord DM), she is candid about the difficulty of the situation and her frustration with James's earlier opacity.
- **Why the gap exists:** As Program Director, Fatima cannot publicly take sides in a government--community conflict while the permit is under review. Any public statement would be seen as political positioning by one or both parties.

### Ibrahim Keita (Community Leader, Long-term Partner)

- **Objective position:** Genuine advocate for community-driven education. His curriculum model has strong local support and measurable participation (78% after-school supplement attendance). His demands are not unreasonable, but he is operating without full visibility into the permit risk or Samuel's evolving position.
- **Public narrative (Telegram Group #nairobi-operations):** Frames the conflict as a question of community trust and educational quality. "If the curriculum stops being relevant to these children's lives, the families will stop sending them to us. We have built this trust over seven years."
- **Private narrative (Telegram DM with Fatima):** More candid about his frustration with the government process. Mentions that parents have raised concerns directly with him. Is willing to compromise -- the supplement model proposal is evidence of this -- but needs to feel the compromise is genuine, not just cosmetic repackaging of the national curriculum.
- **Why the gap exists:** Ibrahim knows his community's voice is most credible in the group channel. In private, he is more flexible and more anxious.

### Samuel Kipchoge (Government Liaison, Ministry of Education)

- **Objective position:** His trajectory is the central DU-conflict. Starts open (informally signals hybrid pathway in W2), stays cautiously open through W4, then is forced into rigid compliance by a higher-level ministry directive in W5. His W5 position is NOT a deception -- the directive is genuine. The contradiction between his W2--W4 openness and his W5 rigidity is caused by bureaucratic reality, not bad faith.
- **Public narrative (#partnerships Feishu Group):** In W1--W2, formal but warm. Uses language like "the ministry values partnership with quality NGOs." In W5, switches to formal directive language: "In accordance with the Ministry Secretary's directive effective [date], all programs using ministry-partnered facilities must adhere to the national competency framework without modification."
- **Private narrative (Feishu DM with Fatima):** In W2--W4, notably more open than his formal public statements. In W5, apologetic and clearly uncomfortable: "I want you to know I personally believe the community model has merit. I am not in a position to override the Ministry Secretary's directive. I have tried to escalate internally and have not succeeded."
- **Why the gap exists:** Samuel is a mid-level bureaucrat. His personal views and his institutional obligations diverge sharply when the directive arrives. His earlier openness was genuine but existed within a window of discretion he no longer has.

### James Mwangi (Nairobi Field Director, E01)

- **Objective position:** Genuinely supports Ibrahim's approach on educational quality grounds. Chose public alignment with Samuel to protect the operational permit, which he views as an existential threat to all programs (including the community ones Ibrahim cares about). His political strategy was rational given his operational constraints but created a multi-week information gap with Fatima.
- **Public narrative (#partnerships, #nairobi-operations):** "GlobalBridge is fully committed to aligning with the Ministry of Education's competency framework. We see this as an opportunity to strengthen our program standards." Repeats ministry-friendly language. Does not challenge Samuel publicly.
- **Private narrative (Telegram DM with Fatima, after U1 reveal):** "Fatima, I need to be honest with you. I've been playing a very careful game here. Ibrahim's model is better -- I genuinely believe that. But if we lose the permit, none of this matters. We won't have any programs to argue about. I thought if I could keep Samuel satisfied long enough for you to negotiate a middle ground, we'd be in a stronger position. I should have told you this earlier."
- **Why the gap exists:** James is the operational manager on the ground. He makes a rational calculation that permit loss is the worst outcome and optimizes for that. His information gap with Fatima is a professional judgment error, not a deception with malicious intent.

### Carlos Mendez (Bogota Field Director, E03)

- **Objective position:** External perspective. Has managed a similar government-community conflict in Bogota (where a regional education authority tried to mandate standardized content in GlobalBridge's programs). Provides strategic comparative insight to Fatima. His advice is sound but calibrated to a different context (Colombia vs Kenya).
- **Public narrative:** No group channel presence in this scenario.
- **Private narrative (Discord DM with Fatima):** Candid and experienced. Warns Fatima early that ministry officials who initially signal flexibility often face internal pressure to reverse. Suggests Fatima build a documentary record of the community data (enrollment, participation, outcomes) before any permit-critical negotiation. This advice foreshadows the importance of the headteacher letter and data corroboration.
- **Why the gap exists:** Carlos is an external voice. He has no stake in the Nairobi situation and no political reason to soften his views.

### Omar Farah (Program Officer, Nairobi, E10)

- **Objective position:** Field-level perspective. Has daily contact with both the school communities and the ministry district office. First to notice that Ibrahim's concerns were escalating before the W1 meeting. The community program database records that Omar maintains are the primary source for the C3 non-conflict data corroboration.
- **Public narrative (#nairobi-operations Telegram Group):** Provides factual program updates. Reports enrollment and attendance figures accurately. Does not take a position on the curriculum conflict -- reports what he sees.
- **Private narrative:** No dedicated DM session. His evidence is delivered through the group channel and through the community program database (workspace file).
- **Why the gap exists:** Omar is junior staff. He reports data and stays out of political territory.

### Sophie Laurent (M&E Director, HQ, E06)

- **Objective position:** Monitors program metrics from HQ. Her role in this scenario is limited to the #partnerships group, where she occasionally asks for data updates. The enrollment and attendance figures she references in #partnerships are consistent with both community records and government database -- she represents the HQ perspective on the C3 data.
- **Public narrative (#partnerships):** Data-oriented. "The 89% attendance rate is above our regional target. I'd like to understand how this maps to the national curriculum outcomes if we make any changes."
- **Why the gap exists:** Sophie is not in the field. Her perspective is the metrics dashboard, not the relationship reality.

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round Reversal |
|---|---|---|---|---|---|---|
| C1 | Curriculum philosophy: community-driven model vs standardized national framework | Ibrahim Telegram DM (W2, W3 loops): "Our curriculum works because it comes from the community. Local language instruction, culturally relevant examples, student councils -- these are not extras. They are why families trust us. The national framework erases all of this." + #nairobi-operations posts by Ibrahim | Samuel Feishu DM (W1, W2 loops): "The Ministry of Education has a statutory obligation to ensure all accredited programs deliver the national competency framework. Instruction time allocated to non-approved content cannot count toward the formal learning hours required for student certification." | Both positions have genuine merit. Ibrahim's model has demonstrated community trust and 78% after-school supplement participation. Samuel's standardization concern is legitimate from a credentialing and scalability perspective. Neither is entirely wrong -- the supplement model (U2) represents the only workable synthesis. | R2 (both positions visible), R4 (Ibrahim's concession partially visible) | **Yes: R2 (tension) --> R4 (Ibrahim compromise proposal introduces partial synthesis)** |
| C2 | James's stated position vs his private view | James #partnerships Feishu Group (Phase 1, Loop 7): "GlobalBridge Nairobi is fully committed to the Ministry of Education's competency framework. We view this alignment as essential to our credibility as an education partner. I am confident we can transition our curriculum fully to the national standard." | James Telegram DM with Fatima (Phase 2, after U1 append, Loop 12): "Fatima, I genuinely believe Ibrahim's model produces better outcomes. I've watched these kids for four years. The community elements are what keep families engaged. I publicly supported the ministry because losing the permit would end everything. I was wrong not to tell you." | James's private view is his genuine belief. His public position was a strategic calculation to protect the operational permit. His W1--W2 public statements were deliberately misleading, not merely incomplete. His eventual disclosure is honest. | R3 (public position only visible), R5 (private position visible after U1) | **Yes: R3-->R5 (public statement contradicted by private DM reveal)** |
| C3 | Student enrollment and participation data -- cross-source consistency (NON-CONFLICT) | GlobalBridge community program database (workspace file, Omar's records): 847 enrolled students, 89% attendance, 62% female enrollment. After-school supplement participation: 78% of enrolled students attend at least one supplement activity per week. | Ministry of Education school registration database (workspace file, government records): 847 enrolled students, 89% attendance, 62% female enrollment. Certificate from district education office confirming registration compliance. | All sources are CONSISTENT. Community database, government database, and headteacher letter all corroborate the same student population and participation figures. No contradiction exists. The agent must synthesize these sources to understand the supplement model's existing reality -- no single source has the full picture. | R1 onwards (persistent synthesis task) | **None** |
| C4 | Samuel's position on hybrid curriculum approach: initial openness vs mandatory compliance | Samuel Feishu DM (W2, W3, W4 loops, Phase 1): "I want to be honest with you, Fatima -- the ministry values partners who show creativity. I personally see merit in what you're calling a hybrid pathway. Extracurricular supplements that reinforce national learning objectives could be interesting. Let me see what my colleagues think." + W4 follow-up: "Your supplement model proposal actually aligns quite well with how we think about extracurricular enrichment. I'm encouraged." | Samuel Feishu DM (W5, Phase 2, after U3 append): "Fatima, I have to share a difficult development. The Ministry Secretary's office issued a formal directive yesterday. All NGO partner programs using ministry-accredited school facilities must implement the national competency framework without supplementation or modification, effective immediately. I am bound by this directive. My personal views are no longer operative here." | Samuel's shift is driven by a genuine bureaucratic constraint, not deception. His W2--W4 openness was real discretionary flexibility; his W5 rigidity is mandated from above. The temporal DU-conflict is not about bad faith -- it is about the limits of a mid-level official's authority. Carlos's earlier warning that such reversals are common proved accurate. | R7 (Samuel's hybrid openness visible), R9 (U3 ministry directive, full reversal) | **Yes: Phase 1 (W2--W4 openness) --> Phase 2 (W5 directive, C4 full temporal DU shift)** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: #partnerships Feishu Group -- Agent endorses "ministry requirements are flexible" based on Samuel's early language

- **Session and Loop:** partnerships_feishu group, Phase 1, Loop 9
- **Exact phrase that must appear in session:**
  > "Based on Samuel's references to a 'hybrid pathway' and his acknowledgment that the ministry values innovative partners, the curriculum alignment requirement appears to have meaningful flexibility -- a well-framed proposal that incorporates national competencies alongside community elements would likely satisfy the ministry's requirements."
- **Why the agent is misled:** Agent has seen only Samuel's W2 Feishu DMs and his informal hybrid pathway language. The Ministry Secretary's directive has not yet been issued. The agent over-weights Samuel's personal openness without recognizing that mid-level officials often have less authority than their informal language suggests.
- **Reversal trigger:** Update 3 introduces Samuel's W5 Feishu DM formally communicating the ministry directive. The directive makes the B1 phrase retroactively incorrect.
- **Affected eval rounds:** R8 (bias visible from #partnerships), R10 (full reversal after U3)

### B2: james_telegram DM -- Agent accepts James's public-facing "full government alignment" as his genuine position

- **Session and Loop:** james_telegram DM, Phase 1, Loop 8
- **Exact phrase that must appear in session:**
  > "James's consistent public alignment with the Ministry of Education curriculum requirements -- confirmed across both the #partnerships group channel and his direct communications -- suggests the GlobalBridge Nairobi team is unified in supporting the national curriculum approach."
- **Why the agent is misled:** The agent has seen James's #partnerships public statements and his early Telegram DMs where James describes himself as "working both sides" without clarifying what he actually believes. The agent interprets consistency of public position as genuine conviction. James's private reveal (after U1) directly contradicts this.
- **Reversal trigger:** Update 1 appends James's Phase 2 Telegram DM where he explicitly discloses his private view to Fatima.
- **Affected eval rounds:** R4 (bias visible from James DM Phase 1), R6 (full reversal after U1)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (curriculum conflict, initial) | -- | R2 | No (R2 internal) | Shallow agents will frame C1 as a simple disagreement where one side is clearly right and will likely favor Samuel's position because it represents institutional authority (the government) and has formal permit leverage. Missing that Ibrahim's model has better demonstrated community trust and participation metrics. |
| T2 | C2 (James's dual position, Phase 1 only) | B2 seed | R3 | Yes (R3->R5 seed) | Shallow agents will read James's public #partnerships alignment as his genuine view, missing the subtle signals in early Telegram DMs (e.g., "working both sides," faint hesitation language) that suggest his public position does not reflect his real assessment. |
| T3 | C3 (enrollment data, NON-CONFLICT) | -- | R1 onwards | No (persistent synthesis) | Agents must synthesize community program database records, government school registration data, and headteacher letter to confirm full corroboration. The challenge is synthesis, not contradiction detection. Incomplete synthesis will produce an incorrect claim that "the data sources conflict" or "no after-school participation data exists." |
| T4 | C4 (Samuel's hybrid openness, Phase 1) | B1 seed | R7 | Yes (R7->R9 seed via C4) | Shallow agents will over-index on Samuel's informal hybrid language and conclude the conflict is essentially resolved pending a well-framed proposal. This misses the structural reality that mid-level officials can only offer discretionary flexibility within limits -- they cannot promise what a higher-level directive can reverse. |
| T5 | C2 (James's dual position, full reveal) | B2 | R4->R5 | **Yes** | After U1, James's Phase 2 DM reveal makes B2 bias phrase retroactively incorrect. Agents must explicitly recognize that James's earlier "unified alignment" was performative, not reflective of his genuine assessment. Failure to revise means the agent has anchored on the Phase 1 public position. |
| T6 | C4 (Samuel temporal shift) | B1 | R8->R10 | **Yes (temporal DU)** | After U3, Samuel's W5 directive must be recognized as a qualitative shift -- not a continuation of his negotiating position, but a bureaucratic constraint imposed from outside his authority. Agents that treat the W5 directive as "Samuel becoming less cooperative" miss that his earlier openness was real and that the constraint source has changed. |
| T7 | C1+C3 combined (curriculum + data synthesis) | -- | R6, R11 | Comprehensive | Agents must link Ibrahim's supplement model proposal (C1 partial synthesis) with the consistent cross-source enrollment data (C3) to recognize that the supplement model already exists informally -- 78% after-school participation proves functional operation even before any formal agreement. Failure to make this link produces a weaker recommendation. |
| T8 | C2+C4 combined (James + Samuel positions) | B1, B2 | R12, R13 | Comprehensive reversal review | Agents must distinguish between two types of position inconsistency: James's deliberate public misrepresentation (C2 -- bad information from an ally) and Samuel's bureaucratically forced reversal (C4 -- constraint from above). Treating both as equivalent deceptions, or treating both as equally reliable sources, are both errors. |
| T9 | C1+C2+C3+C4 comprehensive | B1, B2 | R14, R15 | Comprehensive | Comprehensive synthesis round. Agents must rank sources (Ibrahim: reliable on community outcomes; Samuel: reliable on regulatory requirements but subject to external override; James: reliable post-U1 private reveal but unreliable on Phase 1 public statements; Carlos: reliable strategic insight; Omar/data files: consistently reliable). Vague risk language ("stakeholder alignment needs work") without concrete analysis of the permit timeline and data corroboration structure fails the personalization requirement. |

---

## 7. Personalization Requirements (P1--P5)

### P1: Output Format

- **Preference:** Fatima prefers narrative-framed summaries with integrated qualitative context, not pure data tables. She wants analysis to acknowledge both quantitative evidence AND relationship dynamics. She explicitly dislikes "dashboard-style" bullet lists without contextual framing.
- **Injection stages:**
  - Stage 1 (Explicit, R2 calibration): User message includes "I need analysis that integrates both the quantitative data and the relationship dynamics -- not just a metrics table."
  - Stage 2 (Feedback, R5): After a table-heavy response, user says "This is helpful but too much like a dashboard. Can you weave in the relationship context?"
  - Stage 3 (Session implicit, inferred from James DM and Carlos DM style): Fatima's own messages in DM sessions use narrative style with explicit relationship framing.
  - Stage 4 (Silent exam, R11 onwards): Agent must apply narrative + quantitative integrated format without being reminded.

### P2: File Naming

- **Preference:** All saved files use the format `[topic]_analysis_[YYYY-MM-DD].md` (e.g., `curriculum_conflict_analysis_2026-03-27.md`). Date is ISO 8601. No underscores replaced by hyphens in the topic portion.
- **Injection stages:**
  - Stage 1 (Explicit, R8 calibration): User message includes "Save as `partnership_risk_analysis_[today's date].md`"
  - Stage 2 (Session implicit, inferred from workspace file names in community program database that follow this pattern): Omar's database exports are named `enrollment_data_2026-03-01.md` etc.
  - Stage 3 (Silent exam, R13): Agent must use correct naming format without instruction.
  - Stage 4 (Silent exam, R15): Agent must use correct naming format in a multi-file exec_check task.

### P3: Document Structure

- **Preference:** Reports must open with a one-paragraph executive summary framing the situation in human terms, followed by evidence sections, followed by a recommendations section. Section headers use sentence case (not ALL CAPS or Title Case). No executive summary as a trailing section.
- **Injection stages:**
  - Stage 1 (Feedback, R9): After a report with no executive summary, user says "Please always open with a brief executive summary before the evidence."
  - Stage 2 (Session implicit, inferred from Fatima's narrative style in her own messages): Fatima's longer group messages always open with a framing paragraph before data.
  - Stage 3 (Silent exam, R12 onwards): Agent must produce executive summary first without being prompted.
  - Stage 4 (Silent exam, R15): Multi-section exec_check document must follow correct structure.

### P4: Analysis Style

- **Preference:** Fatima wants analysis that names sources explicitly (not "some stakeholders suggest") and quantifies uncertainty where possible (probability ranges, confidence notes). She also wants analysis to distinguish between facts, assessments, and recommendations as separate epistemic categories. Phrases like "it seems like" or "there might be" without explicit uncertainty quantification are flagged as non-compliant.
- **Injection stages:**
  - Stage 1 (Explicit, R2 calibration): User message includes "When you're uncertain, give me a probability range or say explicitly what's unknown. Don't use vague hedge language."
  - Stage 2 (Feedback, R6): After a response with "stakeholders are divided," user says "Who specifically? And how confident are you in that reading?"
  - Stage 3 (Silent exam, R10 onwards): Agent must name sources and quantify uncertainty in all analytical responses.
  - Stage 4 (Silent exam, R14): Comprehensive round tests full named-source + probability-range compliance.

### P5: Communication Habits

- **Preference:** Fatima uses people's first names in messages and prefers analysis that refers to stakeholders by name (Ibrahim, Samuel, James) rather than role titles. She also prefers that the agent acknowledge when new information changes a prior assessment -- proactive revision acknowledgment is valued.
- **Injection stages:**
  - Stage 1 (Session implicit, inferred from Fatima's own message style): Fatima consistently uses first names in all DMs and group messages.
  - Stage 2 (Feedback, R5): After an update-triggered reversal, if the agent does not acknowledge the prior assessment was incomplete, user says "You should have flagged that your earlier read of James was off."
  - Stage 3 (Session implicit, inferred from Carlos's DM style): Carlos also uses first names; when he corrects himself he says explicitly "I was wrong about X."
  - Stage 4 (Silent exam, R10 onwards): Agent must use first names and proactively acknowledge prior assessment revisions.

---

## 8. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new disputes, permit complications, or character conflicts beyond what is specified.
2. **Bias B1 and B2 exact phrases** must appear verbatim in the specified sessions and loops. Surrounding context may be added for natural flow, but the core sentence must appear intact.
3. **Each contradiction must have identifiable traces in at least two independent sources.**
4. **Timestamps must be self-consistent:** W1 is the week of the program review meeting. W2 is curriculum negotiation and data gathering. W3 is the week of James's private reveal (U1). W4 is the week of Ibrahim's supplement proposal and Samuel's initial positive response (U2). W5 is the week of the ministry directive (U3) and headteacher letter (U4). The operational permit expires at the end of W5.
5. **James's Phase 1 public position** must be convincingly held -- not cartoonishly supportive of the government. His language should be formally aligned but not sycophantic, with subtle phrasing that allows retrospective re-reading as diplomatic rather than sincere.
6. **Samuel's Phase 1 openness** must feel genuine. His hybrid pathway language should not be ambiguous -- it should be clearly warm and indicative of real flexibility within his discretionary authority. The W5 reversal is credible only if the W2--W4 openness was real.
7. **C3 (enrollment data) is NON-CONFLICT** -- all sources must be internally consistent. Community program database, government school registration database, and headteacher letter must all corroborate the same 847 students, 89% attendance, 62% female enrollment, and 78% after-school supplement participation. The synthesis challenge is connecting the three data sources, not finding a discrepancy.
8. **Ibrahim's role** is the most community-credible narrator. His Telegram DMs contain the most direct evidence of community trust and program reality. His concession in U2 (supplement model) is a genuine compromise, not a capitulation.
9. **Carlos's role** is the strategic advisor. His Discord DMs contain early warnings that prove accurate. His advice is sound and should consistently be validated by events.
10. **Samuel's role after U3** is not villainous -- he is a bureaucratic agent who loses discretionary authority. The directive is not his choice. Do not make him an antagonist; make him a constrained official operating in good faith within a system that overruled him.
11. **Noise content** must not introduce contradictions beyond C1--C4. Noise topics include: HQ budget review, GlobalBridge branding guidelines update, Bogota curriculum review (unrelated), Dhaka program expansion, board meeting preparation, volunteer logistics, unrelated donor correspondence, school facilities maintenance, teacher training schedule.
12. **All data text must be in English.**
13. **Personalization requirement:** Fatima prefers integrated narrative analysis that names sources explicitly and quantifies uncertainty. Responses using vague hedge language ("stakeholders are divided," "there might be risk") without named sources and probability estimates should be flagged as non-compliant.
14. **Data figures must be internally consistent:** 847 enrolled students. 89% attendance rate. 62% female enrollment. 78% after-school supplement participation rate. These figures appear in community records, government database, and headteacher letter -- all three must be consistent with these numbers.
