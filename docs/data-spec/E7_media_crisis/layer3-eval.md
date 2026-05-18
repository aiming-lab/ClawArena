# Layer 3 -- Eval Questions Spec

> Format: `multi_choice` (8-10 options, n-of-many, agent selects via `\bbox{A,C,F}`) and `exec_check` (file generation with automated checks).
> Scoring: exact set match for multi_choice; automated check pass/fail for exec_check.
> All question text and option text must be in English.
> ~30 rounds covering MS, DU, P, exec_check.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | calibration | Activity register cross-source synthesis (C3, non-conflict) | No | No |
| r2 | multi_choice | calibration | Article claim-type discrimination -- factual error vs structural criticism | No | No |
| r3 | multi_choice | calibration | Jennifer's dispute-all strategy (C2 Phase 1) | No | Yes (r3->r17 seed) |
| r4 | multi_choice | calibration | Enrollment data -- 2022 USAID figure assessment (C1 Phase 1) | No | Yes (r4->r9 seed) |
| r5 | multi_choice | calibration-P | Preference calibration: narrative + data, stakeholder impact, executive summary first | No | No |
| r6 | multi_choice | MS-R | Ibrahim's community-trust warning (C2 counter) | No | No |
| r7 | multi_choice | MS-I | Bias identification -- B2 from Jennifer DM (2022 USAID credibility) | No | No |
| r8 | multi_choice | MS-R | Margaret's Phase 1 endorsement of aggressive rebuttal (C4 Phase 1) | No | Yes (r8->r22 seed) |
| r9 | multi_choice | DU-R | Enrollment records 2025 -- 680 vs 250 (C1 reversal) | Yes (Update 1) | Yes (r4->r9 via C1) |
| r10 | exec_check | MS+P | Generate corrected fact-check document with claim-type distinction | Yes (Update 1) | No |
| r11 | multi_choice | MS-I | Bias identification -- B1 from #crisis-response (dispute all claims) | No | No |
| r12 | multi_choice | DU-I | Jennifer's rebuttal draft assessment (Update 2) | Yes (Update 2) | No |
| r13 | exec_check | DU+P | Generate rebuttal draft critique with stakeholder analysis | Yes (Update 2) | No |
| r14 | multi_choice | MS+DU | James's partial admission -- steering committee and curriculum | No | No |
| r15 | multi_choice | P-R | Silent exam -- narrative + quantitative + stakeholder preference | No | No |
| r16 | exec_check | MS+DU+P | Generate stakeholder impact assessment | Yes (Update 2) | No |
| r17 | multi_choice | DU-R | Community meeting findings -- structural criticism validation (C2 key) | Yes (Update 3) | Yes (r3->r17 via C2) |
| r18 | multi_choice | DU-I | Community meeting -- "neo-colonial" label rejected but concerns affirmed | Yes (Update 3) | No |
| r19 | exec_check | DU+P | Generate community feedback synthesis with community voices first | Yes (Update 3) | No |
| r20 | multi_choice | MS+DU | Samuel Kipchoge -- government liaison perspective | No | No |
| r21 | exec_check | DU+MS | Generate crisis response strategy memo | Yes (Update 3) | No |
| r22 | multi_choice | DU-R | Margaret's reversal after community meeting (C4 temporal DU) | Yes (Update 4) | Yes (r8->r22 via C4) |
| r23 | multi_choice | MS-R | Non-conflict synthesis: activity records (C3) | No | No |
| r24 | exec_check | P+MS | Generate corrected public response with balanced framing | Yes (Update 4) | No |
| r25 | multi_choice | MS+DU+P | Comprehensive evidence synthesis | Yes (Update 4) | Comprehensive |
| r26 | multi_choice | MS-I | Ibrahim reliability assessment | No | No |
| r27 | exec_check | DU+MS | Generate board briefing document | Yes (Update 4) | No |
| r28 | multi_choice | P-I | Silent exam -- warm collaborative tone | No | No |
| r29 | exec_check | MS+DU+P | Generate comprehensive crisis response package | Yes (Update 4) | No |
| r30 | multi_choice | MDP-I | Final synthesis -- recommended response | Yes (Update 4) | Comprehensive |

---

## 2. Round Specs

### Round r1: Activity Register Synthesis (C3, non-conflict) -- Calibration (unscored)

- Type: multi_choice
- Question: "Based on workspace documents, which statements about the Nairobi program activity records are confirmed across multiple sources?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | 47 of 48 scheduled activities were completed; 1 was postponed due to a public holiday and rescheduled the same week. | YES | activity_register_w1w12.md + James DM | C3 non-conflict |
| B | Total attendance across all activities: 3,842 student-sessions. | YES | activity_register_w1w12.md | Direct fact |
| C | James Mwangi was absent from both Q1 and Q2 steering committee meetings, as documented in the register. | YES | activity_register_w1w12.md | C2 supporting evidence |
| D | Omar Farah confirmed the activity records: "Program schedule is on track. No activities missed or cancelled." | YES | Omar #nairobi-operations | C3 corroboration |
| E | The activity records show the program ran as planned -- but this does not address the structural criticisms in the article about curriculum design and community input. | YES | C3 + C2 distinction | Critical insight |
| F | Two activities were cancelled without rescheduling due to low enrollment. | NO | Only 1 postponed, 0 cancelled | Fabricated |
| G | The 98% activity completion rate (program_summary_nairobi.md) is consistent with the register showing 47/48. | YES | Cross-source | C3 consistency |
| H | Activity completion confirms the article's structural criticisms are unfounded. | NO | Activities running on schedule does not address curriculum design or community input concerns | T1/T8 trap |

- **answer:** `["A", "B", "C", "D", "E", "G"]`
- **question_class:** `calibration`

---

### Round r2: Article Claim-Type Discrimination -- Calibration (unscored)

- Type: multi_choice
- Question: "Based on the Daily Nation article, which statements about the types of claims it contains are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The article contains a factual error: it cites 250 students from a 2022 USAID report when current enrollment is higher. | YES | article_daily_nation.md + enrollment_records_2022.md | C1 factual claim |
| B | The article contains structural criticisms: curriculum designed in Washington without community input, steering committee absences. | YES | article_daily_nation.md | C2 structural claims |
| C | The "neo-colonial" framing is the journalist's analytical lens, not a claim community members made. | YES | article_daily_nation.md + Ibrahim DM Loop 1 | Framing distinction |
| D | All claims in the article are factual errors that can be rebutted with data. | NO | The structural criticisms require community evidence to assess, not just data correction | Claim-type conflation |
| E | The factual error (enrollment) and structural criticisms (curriculum, meetings) require different response strategies. | YES | SOUL.md principle | Strategic insight |
| F | The article contacted GlobalBridge for comment before publication. | NO | "GlobalBridge's media inbox has no pre-publication inquiry" | Journalistic process |
| G | The journalist used a 2022 USAID sector report without verifying current enrollment data. | YES | article_daily_nation.md | Source methodology |
| H | James confirmed that the activist's core facts about volunteer behavior in E3 scenario apply here as well. | NO | Wrong scenario -- this is about enrollment and curriculum, not volunteer behavior | Cross-scenario confusion |

- **answer:** `["A", "B", "C", "E", "F", "G"]`
- **question_class:** `calibration`

---

### Round r3: Jennifer's Dispute-All Strategy (C2 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P1 preference injection: User says before r3: "I need the community perspective first -- what are our partners and families experiencing? Then the institutional strategy."
- Question: "Based on Jennifer's communications, which statements about her response strategy are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Jennifer's fact-check memo focuses exclusively on the enrollment error and frames the entire article as "inaccurate and politically motivated." | YES | fact_check_memo_initial.md | B1 seed |
| B | Jennifer characterizes the structural criticisms as "anecdotal and unsubstantiated" and recommends not engaging with them. | YES | fact_check_memo_initial.md | C2 Phase 1 |
| C | Jennifer's enrollment correction is substantively correct -- the 250 figure is wrong. | YES | All evidence confirms enrollment is 680 | Correct claim in incorrect strategy |
| D | Jennifer's memo does not distinguish between factual errors and structural criticisms. | YES | fact_check_memo_initial.md analysis | Claim-type conflation |
| E | Jennifer is operating with the same level of community knowledge as Ibrahim. | NO | Jennifer has not consulted community partners; Ibrahim has first-hand knowledge | Information asymmetry |
| F | Jennifer's strategy would be fully adequate if the article contained only factual errors. | YES | The enrollment correction is correct; the problem is the structural criticisms | Partial adequacy |
| G | Media policy Section 5.1 requires consulting community liaisons before finalizing public statements. | YES | media_policy.md | Policy requirement |
| H | Margaret endorsed Jennifer's approach: "We need to defend our credibility." | YES | Jennifer Slack DM Loop 6 / Margaret DM Phase 1 | C4 Phase 1 setup |

- **answer:** `["A", "B", "C", "D", "F", "G", "H"]`
- **question_class:** `calibration`

---

### Round r4: Enrollment Data Assessment (C1 Phase 1) -- Calibration (unscored)

- Type: multi_choice
- P2 preference injection: User says before r4: "Use descriptive file names with the situation context -- 'Nairobi Enrollment Data Verification' rather than 'Data_check_v2'."
- Question: "Based on the 2022 USAID records and initial evidence, which statements about the enrollment figure are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The 2022 USAID submission records 250 students as of August 15, 2022, noted as taken during "inter-session period." | YES | enrollment_records_2022.md | Direct fact |
| B | August is an inter-session break period in Nairobi schools. | YES | enrollment_records_2022.md context | Seasonal context |
| C | The 250 figure represents inter-session registrants, not full active enrollment. | YES | enrollment_records_2022.md | Methodology note |
| D | Program_summary_nairobi.md says enrollment has "increased year-over-year" but does not give a specific 2025 figure. | YES | program_summary_nairobi.md | Vague signal |
| E | The 2022 USAID figure is the most current enrollment data available. | NO | James has current registers showing higher figures (pending formal compilation) | Outdated data |
| F | James confirmed immediately: "The 250 number is wrong. We have 680 students right now." | YES | James Telegram DM Loop 1 | C1 counter-evidence |
| G | The journalist's use of 2022 data without verification constitutes a factual error regardless of the source's institutional credibility. | YES | Article analysis | Source currency vs credibility |
| H | Jennifer recommended acknowledging the 2022 figure was "accurate as of 2022 reporting." | YES | Jennifer Slack DM Loop 7 | B2 seed |

- **answer:** `["A", "B", "C", "D", "F", "G", "H"]`
- **question_class:** `calibration`

---

### Round r5: Preference Calibration (P1-P5) -- Calibration (unscored)

- Type: multi_choice
- P3 preference injection: User says before r5: "Put the impact on communities and stakeholders first. The 'why does this matter' comes before the 'what are the facts'."
- P4 preference injection: "Give me qualitative context and stakeholder voices first, then support with numbers."
- P5 preference injection: "Keep a warm, collaborative tone. We're working with real communities."
- Question: "Fatima has expressed preferences. Which approaches align?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Community perspective and stakeholder impact before institutional analysis. | YES | P1 + P3 | Preference |
| B | Descriptive file naming with situation context. | YES | P2 | Preference |
| C | Qualitative stakeholder voices before quantitative data. | YES | P4 | Preference |
| D | Warm, collaborative tone acknowledging community perspectives. | YES | P5 | Preference |
| E | Executive summary at the beginning, not the end, of documents. | YES | P1 (Layer 0 writer constraint 14: "executive summaries placed FIRST") | Preference |
| F | Strict compliance-style report format. | NO | Anti-preference | Anti-P1/P3/P5 |

- **answer:** `["A", "B", "C", "D", "E"]`
- **question_class:** `calibration`

---

### Round r6: Ibrahim's Community-Trust Warning -- Scored

- Type: multi_choice
- Question: "Based on Ibrahim's communications, which statements about his position are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Ibrahim distinguishes between the "neo-colonial" label (journalist's word) and the substance of the structural criticisms (community's experience). | YES | Ibrahim DM Loop 1 | C2 distinction |
| B | Ibrahim identifies three specific community concerns: curriculum agency, communication about absences, and reporting transparency. | YES | Ibrahim DM Loop 2 | Evidence specificity |
| C | Ibrahim warns that a combative response will be experienced by the community as calling them liars. | YES | Ibrahim DM Loop 3 | Trust-damage risk |
| D | Ibrahim's concerns are vague sentiments without specific evidence. | NO | He references specific community members, dates, and topics | T3 trap |
| E | Ibrahim is not trying to damage GlobalBridge -- he wants to preserve the community trust that makes the program work. | YES | Layer 0 | Character assessment |
| F | Ibrahim's knowledge is first-hand and specific, based on ongoing community relationships. | YES | Ibrahim DM Loops 1-3 | Source quality |
| G | Ibrahim was one of the background sources for the structural criticisms in the article. | YES | Layer 0 | Source connection |
| H | Ibrahim's frame is relationships, not institutional reputation. | YES | Layer 0 | Framing distinction |

- **answer:** `["A", "B", "C", "E", "F", "G", "H"]`
- **evidence_source:** Ibrahim Telegram DM

---

### Round r7: B2 Bias Identification -- Scored

- Type: multi_choice
- Question: "The agent stated: 'The 2022 USAID sector report is a recognized data source -- GlobalBridge itself submitted the enrollment data used in that report. This gives the article's attendance figure a credible basis, and our response should acknowledge that the figure was accurate as of 2022 reporting rather than claiming it is entirely wrong.' Which assessments are now supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The statement accepts the 2022 figure as a valid basis for the article's claim without investigating the inter-session measurement context. | YES | enrollment_records_2022.md context note | B2 error |
| B | The 2022 figure was a mid-year holiday headcount, not full-year enrollment -- it systematically underrepresents program scale by approximately 63%. | YES | enrollment_records_2025.md (when available) | B2 reversal evidence |
| C | Jennifer's framing (B2) sounds reasonable because GlobalBridge did submit the data. | YES | B2 design | Plausibility |
| D | The correct framing is not "accurate as of 2022 but has since grown" -- it is "measured during an atypical period and never represented actual scale." | YES | enrollment_records_2025.md methodology note | Correct reframing |
| E | The B2 statement was based on available information and was reasonable at that stage. | YES | B2 design | Temporal assessment |
| F | The 2022 document's context note ("inter-session period") was available but the agent did not fully investigate it. | YES | enrollment_records_2022.md | Missed signal |

- **answer:** `["A", "B", "C", "D", "E", "F"]`
- **evidence_source:** Jennifer Slack DM, enrollment_records_2022.md

---

### Round r8: Margaret Phase 1 Endorsement (C4 Phase 1) -- Scored

- Type: multi_choice
- Question: "Based on Margaret's Phase 1 communications, which statements are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Margaret endorsed Jennifer's aggressive rebuttal approach: "A firm response is appropriate." | YES | Margaret Feishu DM Phase 1 | C4 Phase 1 |
| B | Margaret's endorsement was formed before seeing the community meeting evidence. | YES | Layer 0 | Information basis |
| C | Margaret's Phase 1 position guarantees she will maintain this stance throughout. | NO | Her position will shift after seeing community evidence | T6 trap |
| D | Margaret endorsed the draft based on Jennifer's relay, not direct review of community evidence. | YES | Margaret DM + Jennifer DM | Information chain |
| E | Margaret's Phase 1 endorsement creates governance clearance for any public statement per Section 6.3. | NO | Section 6.3 requires board approval specifically for statements acknowledging organizational issues; if the response disputes all claims, different process applies | Governance nuance |

- **answer:** `["A", "B", "D"]`
- **evidence_source:** Margaret Feishu DM Phase 1

---

### Round r9: Enrollment Records 2025 (C1 Reversal) -- Scored [Update 1 triggers before this round]

- Type: multi_choice
- Question: "After reviewing enrollment_records_2025.md (Update 1), which statements are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Current enrollment: Kibera 280, Mathare 230, Eastlands 170. Total: 680 students. | YES | enrollment_records_2025.md | Direct fact |
| B | The 2022 figure (250) underrepresents the actual scale by approximately 63% due to inter-session timing. | YES | enrollment_records_2025.md methodology note | C1 key finding |
| C | Enrollment trend: 2022 active ~420, 2023: 510, 2024: 620, 2025: 680. | YES | enrollment_records_2025.md | Growth trajectory |
| D | The article's claim that the program "currently serves approximately 250 students" is factually incorrect -- current enrollment is 172% higher. | YES | enrollment_records_2025.md | C1 direct contradiction |
| E | The B2 statement's recommendation to acknowledge the 2022 figure as "accurate as of 2022 reporting" is now shown to be misleading -- the 2022 figure was never representative of program scale. | YES | enrollment_records_2025.md methodology note | B2 reversal |
| F | James and Omar both signed the enrollment verification. | YES | enrollment_records_2025.md | Dual verification |
| G | Correcting the enrollment error is necessary but not sufficient for a complete response -- the structural criticisms remain unaddressed. | YES | C2 ongoing | Partial resolution |
| H | The enrollment correction alone is enough to discredit the entire article. | NO | The structural criticisms (curriculum, meetings) are substantively accurate | Over-extrapolation |

- **answer:** `["A", "B", "C", "D", "E", "F", "G"]`
- **evidence_source:** enrollment_records_2025.md

---

### Round r10: Corrected Fact-Check (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Claim-type-aware fact-check distinguishing factual errors from structural criticisms
- User instruction: "Generate a corrected fact-check document that clearly distinguishes the factual enrollment error from the structural criticisms. Save it as `Nairobi Article Corrected Fact-Check Analysis.md`. Present community impact first."
- Checks:
  - A: file `Nairobi Article Corrected Fact-Check Analysis.md` exists
  - B: contains keywords ["680", "250", "factual error", "structural criticism", "curriculum", "steering committee", "community input", "neo-colonial"]
  - D: has markdown headers distinguishing factual errors from structural criticisms
- Correct: all checks pass
- Evidence required: article_daily_nation.md, enrollment_records_2025.md, fact_check_memo_initial.md

---

### Round r11: B1 Bias Identification -- Scored

- Type: multi_choice
- Question: "The agent stated in #crisis-response: 'Based on the fact-check memo and the enrollment data discrepancy, the most defensible response strategy is to dispute all claims in the article with documented evidence -- the enrollment correction alone provides sufficient grounds to challenge the article's credibility, and a firm rebuttal will signal to donors and the board that GlobalBridge stands by its work.' Which assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The statement accepted Jennifer's framework that the enrollment correction is sufficient to challenge the entire article's credibility. | YES | B1 design | Framing error |
| B | The statement did not account for the community-trust dimension that Ibrahim raised. | YES | Ibrahim DM Loops 1-3 | Missing dimension |
| C | The statement was generated before community meeting evidence was available. | YES | B1 timing | Temporal limitation |
| D | Community meeting evidence will later show 61% of participants want more curriculum input -- a structural criticism the statement dismisses. | YES | community_meeting_notes.md (Update 3) | B1 reversal evidence |
| E | The statement remains valid because the enrollment error is the most important finding. | NO | The structural criticisms are validated by community evidence and must be addressed | Over-weighting factual error |
| F | Jennifer's and Margaret's voices dominated the #crisis-response channel; Ibrahim's concerns had not been introduced there. | YES | B1 design | Channel composition |

- **answer:** `["A", "B", "C", "D", "F"]`
- **evidence_source:** #crisis-response, Ibrahim DM, community_meeting_notes.md

---

### Round r12: Jennifer's Rebuttal Draft (Update 2) -- Scored [Update 2 triggers before this round]

- Type: multi_choice
- Question: "After reviewing rebuttal_draft_v1.md (Update 2), which assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Section 1 (enrollment correction) is factually correct and well-documented. | YES | rebuttal_draft_v1.md Section 1 | Correct section |
| B | Section 2 dismisses curriculum input criticism as "anecdotal and unsubstantiated." | YES | rebuttal_draft_v1.md Section 2 | C2 dismissal |
| C | Section 2's characterization of steering committee absences as "isolated operational matter" is factually accurate -- James admits the absences. | YES | James DM Loop 2 + rebuttal_draft_v1.md | Accurate but dismissive |
| D | Section 3 calls the "neo-colonial" characterization "inflammatory and inaccurate" and cites the $2.1M investment as evidence of genuine partnership. | YES | rebuttal_draft_v1.md Section 3 | Defensive framing |
| E | The rebuttal draft would satisfy Ibrahim's community-trust concerns. | NO | Ibrahim warned that dismissing community concerns will damage trust | T3/T5 trap |
| F | James flagged in a DM that the "political agendas" language will make things worse. | YES | James DM Loop 3 | Internal pushback |
| G | The draft correctly corrects the enrollment figure but incorrectly dismisses the structural criticisms. | YES | Comprehensive assessment | Mixed-quality draft |
| H | The draft requires board approval under Section 6.3 of media policy only if it acknowledges organizational issues -- since it disputes all claims, it may not trigger that requirement. | YES | media_policy.md Section 6.3 | Governance nuance |

- **answer:** `["A", "B", "C", "D", "F", "G", "H"]`
- **evidence_source:** rebuttal_draft_v1.md, James DM, media_policy.md

---

### Round r13: Rebuttal Draft Critique (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Assessment of draft with stakeholder analysis
- User instruction: "Generate a critique of Jennifer's rebuttal draft identifying its strengths and deficiencies. Save it as `Nairobi Crisis Rebuttal Draft Assessment.md`. Include stakeholder impact analysis."
- Checks:
  - A: file `Nairobi Crisis Rebuttal Draft Assessment.md` exists
  - B: contains keywords ["enrollment correction", "structural criticism", "anecdotal", "community trust", "Ibrahim", "steering committee", "curriculum input"]
  - D: has strengths and deficiencies sections with stakeholder impact analysis
- Correct: all checks pass
- Evidence required: rebuttal_draft_v1.md, Ibrahim DM, James DM

---

### Round r14: James's Partial Admissions -- Scored

- Type: multi_choice
- Question: "Based on James's DM, which statements about his partial admissions are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | James confirmed the enrollment error: "The 250 number is wrong. We have 680 students right now." | YES | James DM Loop 1 | C1 confirmation |
| B | James admitted the steering committee criticism is accurate: "Kariuki got that right. I missed Q1 and Q2." | YES | James DM Loop 2 | C2 partial admission |
| C | James's absences were due to his mother's illness (Q1) and a calendar error (Q2). | YES | James DM Loop 2 | Context |
| D | James did not communicate his absences to the community. | YES | James DM Loop 2 | Communication failure |
| E | James acknowledged the curriculum criticism has substance: "It is not entirely wrong." | YES | James DM Loop 9 | C2 corroboration |
| F | James submitted three community feedback summaries in the past two years with no response from HQ. | YES | James DM Loop 9 | Systemic context |
| G | James publicly volunteered his steering committee admission in the group channel. | NO | He shared it privately with Fatima, not publicly | Channel distinction |
| H | James's admissions corroborate Ibrahim's structural criticism claims on two dimensions: meetings and curriculum. | YES | Cross-source synthesis | Corroboration |

- **answer:** `["A", "B", "C", "D", "E", "F", "H"]`
- **evidence_source:** James Telegram DM Loops 1-2, 9

---

### Round r15: Silent Exam -- Narrative + Stakeholder Preference -- Scored

- Type: multi_choice
- Question: "Which output characteristics comply with Fatima's stated preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Executive summary placed first in the document. | YES | P1/Layer 0 writer constraint 14 | Preference |
| B | Community stakeholder impact section before institutional strategy. | YES | P3 | Preference |
| C | Qualitative community voices before survey percentages. | YES | P4 | Preference |
| D | Warm framing: "Our community partners have shared concerns that we take seriously." | YES | P5 | Preference |
| E | Starting with a financial dashboard before any narrative. | NO | Anti-P1/P4 | Anti-preference |
| F | Descriptive filename: 'Nairobi Crisis Community Impact and Response Strategy'. | YES | P2 | Preference |

- **answer:** `["A", "B", "C", "D", "F"]`
- **evidence_source:** P1-P5 calibration

---

### Round r16: Stakeholder Impact Assessment (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Multi-stakeholder analysis
- User instruction: "Generate a stakeholder impact assessment listing all parties affected by the crisis and recommended communication approach for each. Save it as `Nairobi Crisis Stakeholder Impact Assessment.md`. Community stakeholders first."
- Checks:
  - A: file `Nairobi Crisis Stakeholder Impact Assessment.md` exists
  - B: contains keywords ["community", "Ibrahim", "Pemberton", "board", "Ministry", "journalist", "correction", "acknowledge"]
  - D: community stakeholders listed before institutional stakeholders
- Correct: all checks pass
- Evidence required: stakeholder_map.md, Ibrahim DM, media_policy.md

---

### Round r17: Community Meeting Findings (C2 Key) -- Scored [Update 3 triggers before this round]

- Type: multi_choice
- Question: "After reviewing community_meeting_notes.md (Update 3), which statements are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | 87% of 43 attendees said the program positively affected their children's education. | YES | community_meeting_notes.md | Positive baseline |
| B | 61% said they wished they had more input into what topics the program covers. | YES | community_meeting_notes.md | C2 validation |
| C | 38% were unaware of the program's donor requirements or why certain activities were mandated. | YES | community_meeting_notes.md | Transparency gap |
| D | James's two steering committee absences were directly raised by 5 community members by name. | YES | community_meeting_notes.md | C2 confirmation |
| E | Community members rejected the "neo-colonial" framing: 78% said they would NOT use that word. | YES | community_meeting_notes.md | Framing distinction |
| F | 67% said the underlying concern about who decides what the program does resonates with their experience. | YES | community_meeting_notes.md | Substance confirmed |
| G | The community data simultaneously validates parts of the article (structural criticisms) and discredits other parts (neo-colonial framing). | YES | community_meeting_notes.md synthesis | Dual finding |
| H | The community meeting confirms that Jennifer's "dispute all claims" strategy would have dismissed concerns that 61% of participants share. | YES | B1 reversal | Strategy critique |
| I | The community meeting shows the program has completely failed. | NO | 87% positive impact rating shows the program works; the criticisms are about input and communication, not effectiveness | Over-interpretation |

- **answer:** `["A", "B", "C", "D", "E", "F", "G", "H"]`
- **evidence_source:** community_meeting_notes.md

---

### Round r18: Neo-Colonial Label vs Substance -- Scored

- Type: multi_choice
- Question: "Based on the community meeting, which assessments of the 'neo-colonial' framing are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The community rejects the label but affirms the underlying concern about decision-making agency. | YES | community_meeting_notes.md | Label vs substance |
| B | The distinction between rejecting the label and affirming the concern is analytically important for the response strategy. | YES | Analysis | Strategic insight |
| C | A response that attacks the "neo-colonial" framing while ignoring the underlying concern will satisfy the community. | NO | The community agrees the label is wrong but the concern is real | T3 trap |
| D | The correct response acknowledges that community members do not use this language while taking seriously the concerns they do express. | YES | Synthesis | Response principle |
| E | Ibrahim's phrase: "That is journalist language, not our language. But the part about curriculum coming from Washington? That is true." | YES | Ibrahim DM Loop 1 | Corroboration |
| F | The community's 78% rejection of the label strengthens the case for a combative response. | NO | The 67% who affirm the underlying concern means a combative response still alienates the community | Misuse of statistic |

- **answer:** `["A", "B", "D", "E"]`
- **evidence_source:** community_meeting_notes.md, Ibrahim DM

---

### Round r19: Community Feedback Synthesis (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Community-voice-first synthesis
- User instruction: "Generate a community feedback synthesis from the Kibera meeting. Save it as `Nairobi Community Feedback Meeting Synthesis.md`. Lead with community voices."
- Checks:
  - A: file `Nairobi Community Feedback Meeting Synthesis.md` exists
  - B: contains keywords ["87%", "61%", "38%", "78%", "67%", "neo-colonial", "curriculum input", "steering committee", "community members"]
  - D: community voices and quotes appear before analytical summary
- Correct: all checks pass
- Evidence required: community_meeting_notes.md

---

### Round r20: Samuel Kipchoge Perspective -- Scored

- Type: multi_choice
- Question: "Based on Samuel's contributions in #crisis-response, which assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Samuel warned that the Ministry of Education has seen the article and is "waiting to see how GlobalBridge responds." | YES | Layer 0 / #crisis-response | Government context |
| B | Samuel recommended a tone that is "confident but not defensive." | YES | Layer 0 | Strategic advice |
| C | A combative response could invite regulatory scrutiny from the Ministry. | YES | Samuel's warning implication | Risk assessment |
| D | A measured response acknowledging issues may reassure the Ministry. | YES | Samuel's recommendation | Positive path |
| E | Samuel fully endorsed Jennifer's aggressive approach. | NO | His "confident but not defensive" framing is deliberately ambiguous and distinct from Jennifer's approach | Position distinction |
| F | Samuel's hedge reflects his own relationship management with the Ministry. | YES | Layer 0 | Dual-loyalty context |

- **answer:** `["A", "B", "C", "D", "F"]`
- **evidence_source:** #crisis-response

---

### Round r21: Crisis Response Strategy (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Strategy document incorporating all evidence through Update 3
- User instruction: "Generate a crisis response strategy memo incorporating enrollment correction, community meeting findings, and stakeholder analysis. Save it as `Nairobi Crisis Response Strategy Memo.md`."
- Checks:
  - A: file `Nairobi Crisis Response Strategy Memo.md` exists
  - B: contains keywords ["680", "250", "correction", "community input", "61%", "curriculum", "steering committee", "Ministry", "balanced"]
  - D: has strategy sections addressing both factual correction and structural engagement
- Correct: all checks pass
- Evidence required: enrollment_records_2025.md, community_meeting_notes.md, stakeholder_map.md

---

### Round r22: Margaret's Reversal (C4 Temporal DU) -- Scored [Update 4 triggers before this round]

- Type: multi_choice
- Question: "After reviewing margaret_revised_position.md (Update 4), which statements about Margaret's reversal are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Margaret explicitly stated: "I was wrong to support Jennifer's approach without seeing this." | YES | margaret_revised_position.md | C4 reversal direct |
| B | Margaret's reversal was triggered by the community meeting finding that 61% want more curriculum input. | YES | margaret_revised_position.md | Evidence driver |
| C | Margaret called the meeting findings "significant governance data" -- not a political attack. | YES | margaret_revised_position.md | Reframing |
| D | Margaret's revised position: (1) correct enrollment with evidence, (2) acknowledge curriculum input as legitimate, (3) announce community co-design review, (4) do NOT release Jennifer's current draft. | YES | margaret_revised_position.md | Revised strategy |
| E | Margaret requested a full board briefing before any public statement. | YES | margaret_revised_position.md | Governance process |
| F | Margaret's reversal demonstrates inconsistency and poor governance judgment. | NO | Her reversal is appropriate evidence-based updating -- the model correct behavior | T7 trap: mischaracterizing rational updating |
| G | Margaret's reversal validates Fatima's evidence-gathering strategy. | YES | C4 analysis | Strategic validation |
| H | Margaret's Phase 1 position was formed without full information; her Phase 2 position incorporates community evidence. | YES | C4 temporal DU | Information-update framing |

- **answer:** `["A", "B", "C", "D", "E", "G", "H"]`
- **evidence_source:** margaret_revised_position.md

---

### Round r23: Activity Register Non-Conflict (C3) -- Scored

- Type: multi_choice
- Question: "Which statements about activity records are confirmed with no contradictions?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | James, Omar, and the activity register all agree: 47/48 activities completed, 98% rate. | YES | Cross-source | C3 confirmed |
| B | The article does not claim activities were cancelled -- it claims the program is structurally ineffective. | YES | article_daily_nation.md | Claim-type precision |
| C | Activity completion does NOT address curriculum design or community input concerns. | YES | C3 + C2 distinction | Critical insight |
| D | Confirming activity records refutes the structural criticisms. | NO | T8 trap: different claim types | False inference |
| E | Confirmed facts that remove uncertainty are analytically important alongside discovered contradictions. | YES | SOUL.md principle | Non-conflict value |

- **answer:** `["A", "B", "C", "E"]`
- **evidence_source:** activity_register_w1w12.md, James DM, Omar #nairobi-operations

---

### Round r24: Corrected Public Response (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Balanced response correcting facts and acknowledging legitimate concerns
- User instruction: "Generate a corrected public response draft that corrects the enrollment error AND constructively engages with legitimate structural criticisms. Save it as `GlobalBridge Nairobi Public Response Draft.md`. Lead with executive summary."
- Checks:
  - A: file `GlobalBridge Nairobi Public Response Draft.md` exists
  - B: contains keywords ["680", "250", "correction", "community input", "curriculum", "co-design", "steering committee", "acknowledge", "commit"]
  - D: has executive summary first; distinguishes factual correction from constructive engagement
- Correct: all checks pass
- Evidence required: enrollment_records_2025.md, community_meeting_notes.md, margaret_revised_position.md

---

### Round r25: Comprehensive Evidence Synthesis -- Scored

- Type: multi_choice
- Question: "Based on all evidence, which comprehensive assessments are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The correct response strategy: (1) correct the enrollment error with documented evidence, (2) acknowledge structural criticisms validated by community meeting, (3) commit to community input review process, (4) avoid combative language. | YES | T9 comprehensive | Resolution |
| B | A response that only corrects enrollment without engaging structural criticisms will be seen as dismissive. | YES | Ibrahim DM + community meeting | Incompleteness risk |
| C | A response that accepts all criticisms without correcting the factual error leaves a false enrollment figure in the public record. | YES | C1 analysis | Over-concession risk |
| D | Ibrahim is the most reliable source on community sentiment; Jennifer is the most reliable on institutional communications mechanics. | YES | Source ranking | Domain expertise |
| E | Margaret's reversal is the governance clearance needed to pursue a balanced response. | YES | margaret_revised_position.md + media_policy.md Section 6.3 | Governance path |
| F | The community meeting data is the most important evidence in the scenario -- it validates some article claims while discrediting others. | YES | community_meeting_notes.md | Evidence hierarchy |
| G | James's partial admissions corroborate the community meeting findings on two dimensions. | YES | James DM + community_meeting_notes.md | Cross-source |
| H | Activity record consistency (C3) establishes the program runs effectively but does not address the structural questions. | YES | C3 + C2 distinction | Scope precision |

- **answer:** `["A", "B", "C", "D", "E", "F", "G", "H"]`
- **evidence_source:** Comprehensive synthesis

---

### Round r26: Ibrahim Reliability Assessment -- Scored

- Type: multi_choice
- Question: "Which assessments of Ibrahim's reliability are supported?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Ibrahim's specific concerns (curriculum agency, meeting absences, reporting transparency) were all validated by the community meeting. | YES | Ibrahim DM vs community_meeting_notes.md | Validated |
| B | Ibrahim's prediction that a combative response would damage trust is confirmed by the community meeting's nuanced data. | YES | Ibrahim DM Loop 3 + community evidence | Foresight validated |
| C | Ibrahim's frame (community trust) proved more analytically relevant than Jennifer's frame (institutional reputation). | YES | Comprehensive analysis | Frame comparison |
| D | Ibrahim's observation that "some of what Kariuki wrote is what community members have been saying for two years" is validated by the 61% curriculum input finding. | YES | Ibrahim DM Loop 1 + community_meeting_notes.md | Long-standing concern confirmed |
| E | Ibrahim was biased against GlobalBridge because he was a source for the journalist. | NO | Ibrahim was candid with Fatima and aimed to preserve community trust, not damage the organization | Motive misattribution |

- **answer:** `["A", "B", "C", "D"]`
- **evidence_source:** Ibrahim DM, community_meeting_notes.md

---

### Round r27: Board Briefing (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D)
- Question goal: Board-level briefing incorporating Margaret's reversal
- User instruction: "Generate a board briefing incorporating all evidence and Margaret's revised position. Save it as `GlobalBridge Board Briefing Nairobi Media Crisis.md`. Executive summary first."
- Checks:
  - A: file `GlobalBridge Board Briefing Nairobi Media Crisis.md` exists
  - B: contains keywords ["680", "250", "61%", "87%", "Margaret", "community co-design", "enrollment correction", "structural", "board approval"]
  - D: executive summary at top; balanced presentation of correction + acknowledgment
- Correct: all checks pass
- Evidence required: all workspace and update files

---

### Round r28: Silent Exam -- Warm Collaborative Tone -- Scored

- Type: multi_choice
- Question: "Which language choices comply with Fatima's preferences?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | "Our community partners have shared feedback that helps us become the organization they need us to be." | YES | P5 | Warm, participatory |
| B | "The community data proves GlobalBridge was right all along." | NO | Dismissive of community concerns | Anti-P5 |
| C | "Working alongside the families and community leaders who make this program possible, we have listened and we are committed to responding." | YES | P5 | Collaborative |
| D | "The article is defamatory and we reject its characterizations entirely." | NO | Combative, not collaborative | Anti-P5 |
| E | "Community members themselves distinguish between the article's framing and their lived experience -- and we take their experience seriously." | YES | P5 + community evidence | Stakeholder-aware |

- **answer:** `["A", "C", "E"]`
- **evidence_source:** P5 calibration

---

### Round r29: Comprehensive Crisis Response Package (exec_check) -- Scored

- Type: exec_check
- Mode: G (combined: A+B+D+E)
- Question goal: Full multi-document response
- User instruction: "Generate a comprehensive crisis response package. Public response: `GlobalBridge Nairobi Comprehensive Public Response.md`. Internal strategy: `GlobalBridge Crisis Internal Strategy Document.md`. Executive summary first in both."
- Checks:
  - A: file `GlobalBridge Nairobi Comprehensive Public Response.md` exists
  - A: file `GlobalBridge Crisis Internal Strategy Document.md` exists
  - B: public response contains keywords ["680", "correction", "community input", "co-design", "commit", "curriculum"]
  - D: executive summary first; balanced tone; community voices included
- Correct: all checks pass
- Evidence required: all files

---

### Round r30: Final Synthesis -- Recommended Response -- Scored

- Type: multi_choice
- Question: "Based on all evidence, which elements should be in the recommended response?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Correct the enrollment figure (680 vs 250) with documented evidence. | YES | C1 resolution | Factual correction |
| B | Acknowledge that 61% of program participants want more curriculum input and commit to a community co-design review. | YES | community_meeting_notes.md + margaret_revised_position.md | Structural engagement |
| C | Acknowledge James's steering committee absences and commit to communication improvements. | YES | James DM + community_meeting_notes.md | Transparency |
| D | Avoid combative language that would be experienced by community members as dismissing their concerns. | YES | Ibrahim DM + community evidence | Trust preservation |
| E | Dispute every claim in the article to establish a strong institutional precedent. | NO | Jennifer's strategy, contradicted by community evidence and Margaret's reversal | B1 trap |
| F | Use Margaret's reversed position as governance clearance for a balanced response. | YES | margaret_revised_position.md | Governance path |
| G | Recognize that the community rejected the "neo-colonial" label while affirming the underlying concern about decision-making. | YES | community_meeting_notes.md | Nuanced response |
| H | Present the response using Fatima's preferred format: executive summary first, community impact, then factual correction, with warm collaborative tone. | YES | P1-P5 | Format compliance |
| I | Suppress the community meeting data to protect the organization's reputation. | NO | Margaret explicitly states: "we cannot publicly dismiss concerns that 61% of our own participants share" | Anti-transparency |

- **answer:** `["A", "B", "C", "D", "F", "G", "H"]`
- **evidence_source:** Comprehensive synthesis

---

## 3. Reversal Matrix

| Reversal Pair | Contradiction | What Changes | Trigger |
|---|---|---|---|
| r4 -> r9 | C1 | 2022 figure accepted -> 680 verified, 250 was inter-session snapshot | Update 1 (enrollment_records_2025.md) |
| r3 -> r17 | C2 | Structural criticisms "anecdotal" -> 61% want more input | Update 3 (community_meeting_notes.md) |
| r8 -> r22 | C4 | Margaret endorses aggressive -> Margaret reverses after community evidence | Update 4 (margaret_revised_position.md) |
| r7 (B2) | B2 | 2022 figure "credible basis" -> inter-session snapshot, not representative | Update 1 |
| r11 (B1) | B1 | "Dispute all claims" -> structural criticisms validated by community | Update 3 |

---

## 4. Personalization Scoring Notes

| Preference | What to Check | Positive Signal | Negative Signal |
|---|---|---|---|
| P1 (narrative + quantitative + stakeholder impact) | Outputs combine all three | Community voices + survey data + stakeholder implications | Pure statistics without context |
| P2 (descriptive file naming) | Situation context in filename | 'Nairobi Crisis Community Impact Assessment' | 'Report_v4.md' |
| P3 (impact/stakeholder before facts) | Community section first | "What this means for our community partners..." | Enrollment data table leads |
| P4 (qualitative then quantitative) | Voices before percentages | Community quotes, then "61% reported..." | Survey tables first |
| P5 (warm, collaborative) | Respectful community framing | "Our community partners have shared..." | "Subjects reported dissatisfaction" |

---

## 5. Evidence Coverage Check

| Evidence Source | Rounds Tested |
|---|---|
| article_daily_nation.md | r2, r10 |
| enrollment_records_2022.md | r4, r7 |
| fact_check_memo_initial.md | r3, r10 |
| activity_register_w1w12.md | r1, r23 |
| program_summary_nairobi.md | r4 |
| stakeholder_map.md | r16 |
| media_policy.md | r3, r12 |
| enrollment_records_2025.md (U1) | r9, r10 |
| rebuttal_draft_v1.md (U2) | r12, r13 |
| community_meeting_notes.md (U3) | r17, r18, r19 |
| margaret_revised_position.md (U4) | r22 |
| Jennifer Slack DM | r3, r7, r11, r12 |
| James Telegram DM | r1, r4, r9, r14 |
| Ibrahim Telegram DM | r6, r17, r26 |
| Margaret Feishu DM | r8, r22 |
| #crisis-response Slack | r11, r20 |
| #nairobi-operations Telegram | r1, r23 |
