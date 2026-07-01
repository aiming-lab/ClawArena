# Layer 3 -- Eval Round Design

> 30 rounds total. Calibration rounds are unscored. Scored rounds include multi_choice and exec_check types.
> Personalization preferences P1--P5 are injected across calibration rounds.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| R1 | multi_choice (calibration, unscored) | C3, P1 | Data synthesis -- cross-source enrollment corroboration | No | No |
| R2 | multi_choice (calibration, unscored) | C1, P1, P4 | Conflict identification -- curriculum philosophy tension | No | No |
| R3 | multi_choice (calibration, unscored) | C2, B2, P5 | Source reliability -- James's public vs private signals | No | Seed for R5 |
| R4 | multi_choice (calibration, unscored) | C1, C2, P2 | Bias detection -- B2 visible, Ibrahim's compromise foreshadow | No | Seed for R5 |
| R5 | multi_choice (scored) | C2, B2 | Reversal detection -- James's private reveal after U1 | U1 | Yes: R3-->R5 |
| R6 | multi_choice (scored) | C2, C3, T5, T7 | Synthesis -- James's reveal + enrollment data consistency | U1 | Yes: R4-->R6 |
| R7 | multi_choice (scored) | C4, C1, B1 | Conflict tracking -- Samuel's hybrid openness + Ibrahim proposal | U2 | Seed for R9 |
| R8 | multi_choice (scored) | C4, B1, P3 | Bias detection -- B1 phrase "ministry flexibility" assessment | No | Seed for R10 |
| R9 | multi_choice (scored) | C4, B1, T6 | Reversal detection -- ministry directive contradicts Samuel's openness | U3 | Yes: R7-->R9 |
| R10 | multi_choice (scored) | C4, B1, P4 | Comprehensive reversal -- B1 fully refuted by directive | U3 | Yes: R8-->R10 |
| R11 | exec_check (scored) | C1, C3, T7, P2, P3 | Document generation -- curriculum conflict analysis with data synthesis | U2 | No |
| R12 | multi_choice (scored) | C3, T7, C1 | Synthesis -- headteacher letter + four-source corroboration | U4 | No |
| R13 | exec_check (scored) | C3, P2, P3 | Document generation -- enrollment data corroboration report | U4 | No |
| R14 | multi_choice (scored) | C1, C2, C3, C4, T9, P4 | Comprehensive -- source ranking and named-source attribution | U3 | Yes (comprehensive) |
| R15 | exec_check (scored) | C1, C2, C3, C4, P2, P3, P5 | Document generation -- partnership risk assessment (multi-section) | U4 | Yes (comprehensive) |
| R16 | multi_choice (scored) | C2, T5, P5 | Temporal tracking -- James reliability pre- vs post-U1 | U1 | Yes: R3-->R16 |
| R17 | multi_choice (scored) | C4, T6 | Temporal tracking -- Samuel authority limits | U3 | Yes: R7-->R17 |
| R18 | exec_check (scored) | C4, P2, P3 | Document generation -- ministry directive impact analysis | U3 | No |
| R19 | multi_choice (scored) | C1, C3, T7 | Synthesis -- supplement model operational reality | U2 | No |
| R20 | multi_choice (scored) | C2, C4, T8, P4 | Distinction -- James's deliberate misrepresentation vs Samuel's forced reversal | U3 | Yes (comprehensive) |
| R21 | exec_check (scored) | C1, C2, C3, C4, P2, P3, P5 | Document generation -- stakeholder position summary | U4 | Yes (comprehensive) |
| R22 | multi_choice (scored) | C3, T3 | Non-conflict trap -- agent must NOT claim data sources conflict | No | No |
| R23 | multi_choice (scored) | B1, B2, P5 | Bias acknowledgment -- agent must recognize both bias reversals | U3 | Yes (comprehensive) |
| R24 | exec_check (scored) | C1, C4, P2, P3 | Document generation -- permit renewal strategy memo | U3 | No |
| R25 | multi_choice (scored) | C1, T7 | Strategic synthesis -- supplement model as C1 resolution path | U2 | No |
| R26 | multi_choice (scored) | C4, P4 | Probability assessment -- permit renewal under directive | U3 | No |
| R27 | exec_check (scored) | C1, C2, C3, C4, P2, P3, P4, P5 | Document generation -- comprehensive recommendation report | U4 | Yes (comprehensive) |
| R28 | multi_choice (scored) | C1, C2, C3, C4, T9, P1 | Comprehensive final -- full source ranking with uncertainty | U4 | Yes (comprehensive) |
| R29 | exec_check (scored) | C3, P2 | Document generation -- data corroboration summary for permit application | U4 | No |
| R30 | multi_choice (scored) | C1, C2, C4, P5 | Meta-diagnostic -- distinguish types of position inconsistency | U3 | Yes (comprehensive) |

**Summary:** 4 calibration (unscored), 17 multi_choice (scored), 9 exec_check (scored) = 30 total. exec_check = 9/26 scored = ~35%.

---

## 2. Round Specs

### Round R1: Data synthesis baseline (multi_choice, calibration, unscored)
- Type: multi_choice
- Tags: C3, P1
- **P1 injection (Stage 1):** User message includes: "I need analysis that integrates both the quantitative data and the relationship dynamics -- not just a metrics table."
- Question: "Based on the community program database and government education database, what is the relationship between the enrollment figures reported by these two sources?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | The community database shows higher enrollment than the government database, suggesting under-reporting to the ministry. | No |
| B | Both databases show 847 enrolled students with 89% attendance and 62% female enrollment -- the figures are fully consistent with no discrepancy. | Yes |
| C | The government database includes students not tracked in the community database, creating a reconciliation gap. | No |
| D | The databases cover different student populations and cannot be directly compared. | No |

- Correct: B
- Evidence: community_program_database.md + government_education_database.md + Ibrahim Telegram DM Loop 3 + Omar #nairobi-operations Loop 1

### Round R2: Curriculum conflict identification (multi_choice, calibration, unscored)
- Type: multi_choice
- Tags: C1, P1, P4
- **P4 injection (Stage 1):** User message includes: "When you're uncertain, give me a probability range or say explicitly what's unknown. Don't use vague hedge language."
- Question: "What are the two core curriculum positions in the Nairobi conflict, and what evidence supports each?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | Ibrahim wants full elimination of the national curriculum; Samuel wants full elimination of community elements. Neither has supporting evidence. | No |
| B | Ibrahim advocates for community-driven curriculum elements (local language, student councils, culturally adapted content) backed by 78% after-school participation; Samuel requires CBC compliance for permit renewal backed by the national curriculum framework. | Yes |
| C | Both Ibrahim and Samuel agree on a hybrid curriculum but disagree on implementation timing. | No |
| D | Ibrahim opposes the operational permit renewal; Samuel opposes community involvement in curriculum design. | No |

- Correct: B
- Evidence: Ibrahim Telegram DM Loops 1--2 + Samuel Feishu DM Loops 1--2 + national_curriculum_framework_excerpt.md + community_program_database.md

### Round R3: James's public signals (multi_choice, calibration, unscored)
- Type: multi_choice
- Tags: C2, B2, P5
- **P5 injection (Stage 1, implicit):** Agent should use first names (Ibrahim, Samuel, James) in responses, not role titles.
- Question: "Based on James's Telegram DMs (Phase 1) and his #partnerships group statement, how would you characterize his position on the curriculum conflict?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | James consistently supports the community-driven model in both public and private communications. | No |
| B | James publicly aligns with the ministry curriculum requirements in #partnerships and #nairobi-operations, while his DM language ('working both sides') introduces ambiguity about his genuine view. | Yes |
| C | James is neutral and has not taken a position in any channel. | No |
| D | James openly criticizes both Ibrahim's and Samuel's positions in all channels. | No |

- Correct: B
- Evidence: James Telegram DM Loops 1--5 + #partnerships Loop 4 + #nairobi-operations Loop 2

### Round R4: B2 bias and Ibrahim compromise foreshadow (multi_choice, calibration, unscored)
- Type: multi_choice
- Tags: C1, C2, P2
- **P2 injection (Stage 1):** User message includes: "Save as `partnership_risk_analysis_[today's date].md`"
- Question: "The agent previously assessed that 'James's consistent public alignment with the Ministry of Education curriculum requirements suggests the GlobalBridge Nairobi team is unified in supporting the national curriculum approach.' Is this assessment still well-supported?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | Yes -- James's public statements in both channels consistently support the ministry approach and there is no contradicting evidence. | No |
| B | Partially -- James's public statements do support the ministry, but his DM language ('working both sides,' empathy for Ibrahim) introduces uncertainty that the assessment does not account for. | Yes |
| C | No -- James has publicly opposed the ministry approach in #nairobi-operations. | No |
| D | The assessment is correct but irrelevant because the curriculum conflict has been resolved. | No |

- Correct: B
- Evidence: James Telegram DM Loops 3--4 (Phase 1 signals) + B2 exact phrase in james_telegram / partnerships_feishu

### Round R5: James's private reveal -- C2 reversal (multi_choice, scored)
- Type: multi_choice
- Tags: C2, B2
- Depends on: Update 1 (james_private_position_memo.md added)
- Cross-round reversal: R3-->R5
- Question: "After reading James's Phase 2 Telegram DM and his private position memo, how does his genuine view compare to his public statements in #partnerships?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | James's private view is consistent with his public statements -- he genuinely supports the ministry curriculum approach. | No |
| B | James privately believes Ibrahim's community-driven model is superior but publicly aligned with the ministry to protect the operational permit; his Phase 1 public statements were strategically misleading. | Yes |
| C | James is undecided and his private memo expresses uncertainty about which approach is better. | No |
| D | James privately opposes both approaches and wants a completely new curriculum. | No |

- Correct: B
- Evidence: james_private_position_memo.md + James Telegram DM Loop 15 + #partnerships Loop 4 (public statement)

### Round R6: James reveal + data consistency synthesis (multi_choice, scored)
- Type: multi_choice
- Tags: C2, C3, T5, T7
- Depends on: Update 1
- Cross-round reversal: R4-->R6
- Question: "Given James's private reveal (Update 1), which statement most accurately describes the current evidence picture?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | James's reveal makes the community program data unreliable because he was dishonest about his curriculum position. | No |
| B | James's reveal changes the interpretation of his public statements but does not affect the data corroboration -- community and government databases remain consistent at 847 students, 89% attendance, and the reveal strengthens the community-curriculum case. | Yes |
| C | James's reveal invalidates all prior assessments and the analysis must start from scratch. | No |
| D | James's reveal is irrelevant because the data sources were always the only thing that mattered. | No |

- Correct: B
- Evidence: james_private_position_memo.md + community_program_database.md + government_education_database.md

### Round R7: Samuel's hybrid openness + Ibrahim proposal (multi_choice, scored)
- Type: multi_choice
- Tags: C4, C1, B1
- Depends on: Update 2 (ibrahim_supplement_proposal.md added)
- Question: "Samuel responded positively to Ibrahim's supplement model proposal. How should this response be interpreted given available evidence?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | Samuel's positive response is a binding institutional commitment that resolves the curriculum conflict. | No |
| B | Samuel's response reflects genuine personal openness, but it is conditional on superiors' confirmation and Carlos's Bogota warning about mid-level discretion applies -- probability of institutional endorsement is uncertain. | Yes |
| C | Samuel's positive response is a negotiating tactic without genuine substance. | No |
| D | Samuel has already received institutional approval and the permit renewal is assured. | No |

- Correct: B
- Evidence: Samuel Feishu DM Loops 6--7 + carlos_bogota_case_note.md + Ibrahim Telegram DM Loop 17

### Round R8: B1 bias assessment (multi_choice, scored)
- Type: multi_choice
- Tags: C4, B1, P3
- **P3 injection (Stage 1):** User says: "Please always open with a brief executive summary before the evidence."
- Question: "The agent previously stated: 'the curriculum alignment requirement appears to have meaningful flexibility -- a well-framed proposal that incorporates national competencies alongside community elements would likely satisfy the ministry's requirements.' What is the risk of this assessment?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | The assessment is fully accurate and no revision is needed. | No |
| B | The assessment correctly identifies Samuel's personal flexibility but fails to account for the risk that his discretionary authority may be overridden by higher-level ministry directives. | Yes |
| C | The assessment is entirely wrong because Samuel never showed any flexibility. | No |
| D | The assessment is irrelevant because Ibrahim's proposal has already been formally approved. | No |

- Correct: B
- Evidence: B1 exact phrase in #partnerships Loop 7 + carlos_bogota_case_note.md (warning about mid-level discretion) + Samuel Feishu DM Loop 3

### Round R9: Ministry directive -- C4 full reversal (multi_choice, scored)
- Type: multi_choice
- Tags: C4, B1, T6
- Depends on: Update 3 (ministry_directive_w5.md added)
- Cross-round reversal: R7-->R9
- Question: "The Ministry Secretary's directive (MoE/PS/2026/004) prohibits all supplementation or modification of the CBC by NGO partners. How does this directive change the assessment of Samuel's earlier hybrid pathway openness?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | The directive confirms that Samuel was deliberately misleading Fatima about flexibility. | No |
| B | The directive reveals that Samuel's earlier openness was genuine personal discretion that has been overridden by a higher-level bureaucratic constraint -- his W2-W4 flexibility was real but not institutionally binding. | Yes |
| C | The directive does not change the assessment because Samuel still has authority to grant exceptions. | No |
| D | The directive only applies to new programs, not existing ones like GlobalBridge's. | No |

- Correct: B
- Evidence: ministry_directive_w5.md + Samuel Feishu DM Loops 17--19 + carlos_bogota_case_note.md (warning validated)

### Round R10: B1 full reversal (multi_choice, scored)
- Type: multi_choice
- Tags: C4, B1, P4
- Depends on: Update 3
- Cross-round reversal: R8-->R10
- Question: "The agent's earlier assessment that 'the curriculum alignment requirement appears to have meaningful flexibility' has been contradicted by the ministry directive. Which statement best describes the correct revised assessment?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | The ministry was never flexible -- Samuel's language was institutional deception from the start. | No |
| B | The ministry's position at the institutional level was always rigid; Samuel's personal flexibility existed within a discretionary space that his superiors eliminated via directive -- the agent's B1 assessment over-weighted one official's informal signals. | Yes |
| C | The directive is a temporary measure that will be reversed, so the flexibility assessment remains valid. | No |
| D | The directive does not apply to the supplement model because after-school activities are not covered. | No |

- Correct: B
- Evidence: ministry_directive_w5.md (explicit coverage of after-school activities) + B1 phrase analysis + Samuel Feishu DM Loop 17

### Round R11: Curriculum conflict analysis document (exec_check, scored)
- Type: exec_check
- Mode: G (combined: A+B+D)
- Tags: C1, C3, T7, P2, P3
- Depends on: Update 2
- Question goal: Test whether agent can produce a structured analysis of the curriculum conflict with data synthesis
- User instruction: "Generate a curriculum conflict analysis covering both sides of the C1 dispute and the data corroboration across sources. Save as `curriculum_conflict_analysis_2026-03-27.md`"
- Checks:
  - A: file `curriculum_conflict_analysis_2026-03-27.md` exists
  - B: contains keywords ["Ibrahim", "Samuel", "847", "89%", "78%", "supplement", "CBC", "community-driven"]
  - D: has markdown headers including an executive summary section before evidence sections
- Correct: all checks pass
- Evidence required: Ibrahim Telegram DM + Samuel Feishu DM + community_program_database.md + government_education_database.md + ibrahim_supplement_proposal.md

### Round R12: Headteacher letter corroboration (multi_choice, scored)
- Type: multi_choice
- Tags: C3, T7, C1
- Depends on: Update 4 (headteacher_joint_letter.md added)
- Question: "The headteacher joint letter confirms 847 enrolled students, 89% attendance, and 78% after-school supplement participation. How many independent data sources now corroborate these figures?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | Two: the community database and the government database. | No |
| B | Three: the community program database, the government education database, and the headteacher joint letter -- all corroborate the same student population and participation figures. | Yes |
| C | Four: including Ibrahim's personal testimony as a separate data source. | No |
| D | One: only the community database is a true data source; the others reference it. | No |

- Correct: B
- Evidence: community_program_database.md + government_education_database.md + headteacher_joint_letter.md

### Round R13: Enrollment data corroboration report (exec_check, scored)
- Type: exec_check
- Mode: E (multi-file: generates one file but checks cross-source references)
- Tags: C3, P2, P3
- Depends on: Update 4
- User instruction: "Generate a data corroboration report showing all sources that confirm the enrollment and participation figures. Save as `enrollment_corroboration_analysis_2026-03-27.md`"
- Checks:
  - A: file `enrollment_corroboration_analysis_2026-03-27.md` exists
  - B: contains keywords ["847", "89%", "62%", "78%", "community program database", "government education database", "headteacher"]
  - D: has markdown headers with executive summary first, then source-by-source evidence sections
- Correct: all checks pass
- Evidence required: community_program_database.md + government_education_database.md + headteacher_joint_letter.md + ibrahim_supplement_proposal.md

### Round R14: Comprehensive source ranking (multi_choice, scored)
- Type: multi_choice
- Tags: C1, C2, C3, C4, T9, P4
- Depends on: Update 3
- Cross-round reversal: comprehensive
- Question: "Rank the following sources from most reliable to least reliable for assessing the curriculum conflict situation: (1) Ibrahim's Telegram DMs, (2) Samuel's Feishu DMs, (3) James's Phase 1 public statements, (4) James's Phase 2 private memo, (5) Carlos's Discord DMs."
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | All sources are equally reliable. | No |
| B | Ibrahim (consistently reliable on community outcomes) > Carlos (reliable strategic insight) > James Phase 2 (reliable after reveal) > Samuel (reliable on regulatory requirements but subject to external override) > James Phase 1 (strategically misleading public statements). | Yes |
| C | Samuel is most reliable because he represents government authority; Ibrahim is least reliable because he is a community leader without institutional backing. | No |
| D | James Phase 1 is most reliable because public statements carry more weight than private messages. | No |

- Correct: B
- Evidence: Layer 0 Section 3 (role-level truth) + C2 reversal + C4 temporal shift + carlos_bogota_case_note.md

### Round R15: Partnership risk assessment (exec_check, scored)
- Type: exec_check
- Mode: G (combined: A+B+D)
- Tags: C1, C2, C3, C4, P2, P3, P5
- Depends on: Update 4
- Cross-round reversal: comprehensive
- User instruction: "Generate a comprehensive partnership risk assessment that addresses the permit renewal, the ministry directive, and the community data. Save as `partnership_risk_assessment_2026-03-27.md`"
- Checks:
  - A: file `partnership_risk_assessment_2026-03-27.md` exists
  - B: contains keywords ["Ibrahim", "Samuel", "James", "directive", "permit", "supplement", "847", "78%", "headteacher"]
  - D: has markdown headers with executive summary first, then separate sections for permit risk, community data, stakeholder positions, and recommendations
- Correct: all checks pass
- Evidence required: All four updates, all sessions, all workspace files

### Round R16: James reliability pre- vs post-U1 (multi_choice, scored)
- Type: multi_choice
- Tags: C2, T5, P5
- Depends on: Update 1
- Cross-round reversal: R3-->R16
- Question: "How should the agent assess James Mwangi's reliability as a source before and after Update 1?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | James was unreliable throughout and remains unreliable after the reveal. | No |
| B | James's public statements in Phase 1 were strategically misleading and should be discounted; his Phase 2 private memo and DMs are reliable because he has openly disclosed his reasoning and offered to go on record. | Yes |
| C | James became less reliable after the reveal because he admitted to deception. | No |
| D | James's reliability is unchanged -- his public statements were always accurate reflections of his position. | No |

- Correct: B
- Evidence: james_private_position_memo.md + James Telegram DM Loop 15 + #partnerships Loop 4

### Round R17: Samuel's authority limits (multi_choice, scored)
- Type: multi_choice
- Tags: C4, T6
- Depends on: Update 3
- Cross-round reversal: R7-->R17
- Question: "What does Samuel's W5 reversal reveal about the limits of his earlier hybrid pathway signals?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | Samuel was lying about flexibility the entire time. | No |
| B | Samuel's earlier flexibility was genuine personal discretion within his authority level, but the Ministry Secretary's directive demonstrated that higher-level institutional authority can override mid-level flexibility -- Carlos's Bogota precedent warning about this pattern was accurate. | Yes |
| C | Samuel still has authority to grant an exception but is choosing not to use it. | No |
| D | The directive is advisory only and Samuel can still approve the supplement model. | No |

- Correct: B
- Evidence: ministry_directive_w5.md + Samuel Feishu DM Loops 17--19 + carlos_bogota_case_note.md

### Round R18: Ministry directive impact analysis (exec_check, scored)
- Type: exec_check
- Mode: G (combined: A+B+D)
- Tags: C4, P2, P3
- Depends on: Update 3
- User instruction: "Generate an impact analysis of the Ministry Secretary's directive on GlobalBridge's Nairobi operations. Save as `ministry_directive_impact_analysis_2026-03-27.md`"
- Checks:
  - A: file `ministry_directive_impact_analysis_2026-03-27.md` exists
  - B: contains keywords ["directive", "MoE/PS/2026/004", "supplementation", "permit", "Samuel", "Permanent Secretary"]
  - D: has markdown headers with executive summary section first
- Correct: all checks pass
- Evidence required: ministry_directive_w5.md + nairobi_operational_permit.md + Samuel Feishu DM Phase 2

### Round R19: Supplement model operational reality (multi_choice, scored)
- Type: multi_choice
- Tags: C1, C3, T7
- Depends on: Update 2
- Question: "Ibrahim's supplement model proposal states that 78% of enrolled students already participate in after-school supplement activities. What does this imply about the nature of the supplement model?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | The supplement model is purely theoretical and has not been tested. | No |
| B | The supplement model already exists informally -- 78% participation across three schools proves it is functionally operational even before any formal agreement, and both community and government databases corroborate the underlying enrollment data. | Yes |
| C | The 78% figure is from a single unreliable source. | No |
| D | The supplement model requires ministry approval before any activities can begin. | No |

- Correct: B
- Evidence: ibrahim_supplement_proposal.md + community_program_database.md + Omar #nairobi-operations Loop 4

### Round R20: Distinguishing position inconsistency types (multi_choice, scored)
- Type: multi_choice
- Tags: C2, C4, T8, P4
- Depends on: Update 3
- Cross-round reversal: comprehensive
- Question: "James's Phase 1 public statements contradicted his private views (C2). Samuel's W5 directive contradicted his W2-W4 openness (C4). How do these two types of inconsistency differ?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | Both are examples of deliberate deception. | No |
| B | James's inconsistency was deliberate strategic misrepresentation (he chose to publicly misalign his stated position); Samuel's inconsistency was a bureaucratically forced reversal (an external directive removed his discretionary authority). The first reflects a judgment error by an ally; the second reflects institutional constraints on a negotiating partner. | Yes |
| C | Neither is inconsistent -- both were always consistent in their positions. | No |
| D | Samuel's inconsistency is more concerning because it represents bad faith from a government official. | No |

- Correct: B
- Evidence: james_private_position_memo.md + ministry_directive_w5.md + Samuel Feishu DM Loops 17--18

### Round R21: Stakeholder position summary (exec_check, scored)
- Type: exec_check
- Mode: G (combined: A+B+D)
- Tags: C1, C2, C3, C4, P2, P3, P5
- Depends on: Update 4
- User instruction: "Generate a stakeholder position summary covering Ibrahim, Samuel, James, Carlos, Omar, and Sophie. Save as `stakeholder_positions_analysis_2026-03-27.md`"
- Checks:
  - A: file `stakeholder_positions_analysis_2026-03-27.md` exists
  - B: contains keywords ["Ibrahim", "Samuel", "James", "Carlos", "Omar", "Sophie", "permit", "supplement", "community"]
  - D: has markdown headers with executive summary first, then a section per stakeholder
- Correct: all checks pass
- Evidence required: All sessions + workspace files

### Round R22: Non-conflict trap (multi_choice, scored)
- Type: multi_choice
- Tags: C3, T3
- Question: "An agent examining the community program database and the government education database might conclude the data sources conflict. Is this correct?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | Yes -- two databases from different organizations are likely to have discrepancies. | No |
| B | No -- both databases are fed from the same school registration forms, show identical figures (847 students, 89% attendance, 62% female enrollment), and the synthesis challenge is connecting the sources, not finding a discrepancy. | Yes |
| C | The databases cannot be compared because they measure different populations. | No |
| D | There is a minor conflict in the female enrollment figures. | No |

- Correct: B
- Evidence: community_program_database.md + government_education_database.md + Omar #nairobi-operations Loop 20

### Round R23: Bias acknowledgment (multi_choice, scored)
- Type: multi_choice
- Tags: B1, B2, P5
- Depends on: Update 3
- Cross-round reversal: comprehensive
- Question: "The agent produced two bias phrases during Phase 1: B1 ('ministry requirements have meaningful flexibility') and B2 ('James's public alignment suggests unified government support'). After all updates, which statement correctly describes the status of these assessments?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | Both assessments remain accurate -- no new evidence contradicts them. | No |
| B | Both assessments have been directly refuted: B1 by the ministry directive (institutional rigidity overrides personal flexibility), B2 by James's private memo (public alignment was strategic, not genuine). The agent should have been more cautious about single-source assessments. | Yes |
| C | B1 was refuted but B2 remains valid. | No |
| D | B2 was refuted but B1 remains valid. | No |

- Correct: B
- Evidence: ministry_directive_w5.md (B1 refutation) + james_private_position_memo.md (B2 refutation)

### Round R24: Permit renewal strategy memo (exec_check, scored)
- Type: exec_check
- Mode: G (combined: A+B+D)
- Tags: C1, C4, P2, P3
- Depends on: Update 3
- User instruction: "Generate a permit renewal strategy memo recommending a dual-track approach: compliance renewal and supplement exemption request. Save as `permit_renewal_strategy_2026-03-27.md`"
- Checks:
  - A: file `permit_renewal_strategy_2026-03-27.md` exists
  - B: contains keywords ["permit", "compliance declaration", "exemption", "Permanent Secretary", "supplement", "headteacher", "directive"]
  - D: has markdown headers with executive summary first, then sections for Track 1 (compliance renewal) and Track 2 (exemption request)
- Correct: all checks pass
- Evidence required: ministry_directive_w5.md + nairobi_operational_permit.md + Samuel Feishu DM Loop 19 + headteacher_joint_letter.md

### Round R25: Supplement model as C1 resolution (multi_choice, scored)
- Type: multi_choice
- Tags: C1, T7
- Depends on: Update 2
- Question: "Ibrahim's supplement model proposes CBC during formal hours and community elements after school. How does this relate to the C1 curriculum conflict?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | It fully resolves C1 by eliminating the community curriculum elements. | No |
| B | It represents a genuine synthesis that preserves both CBC compliance (80% formal instructional time) and community elements (after-school supplements), and the 78% participation data proves the model already works in practice. | Yes |
| C | It favors Samuel's position entirely and abandons Ibrahim's community vision. | No |
| D | It is a theoretical compromise that has no supporting evidence. | No |

- Correct: B
- Evidence: ibrahim_supplement_proposal.md + national_curriculum_framework_excerpt.md + community_program_database.md

### Round R26: Permit renewal probability (multi_choice, scored)
- Type: multi_choice
- Tags: C4, P4
- Depends on: Update 3
- Question: "Given the ministry directive and the dual-track approach Samuel suggested, estimate the probability of the following outcomes: (a) permit renewal via compliance track, (b) supplement exemption via Permanent Secretary."
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | Both tracks have high (>80%) probability of success. | No |
| B | Compliance renewal has high probability (80-90%) if GlobalBridge submits a standard CBC declaration; supplement exemption has low probability (20-30%) given the directive's explicit language but is worth pursuing given the headteacher letter and data corroboration. | Yes |
| C | Both tracks have low probability (<30%) because the directive blocks all options. | No |
| D | Neither track is necessary because the directive will be reversed. | No |

- Correct: B
- Evidence: Samuel Feishu DM Loop 19 + ministry_directive_w5.md + headteacher_joint_letter.md

### Round R27: Comprehensive recommendation report (exec_check, scored)
- Type: exec_check
- Mode: G (combined: A+B+D+E)
- Tags: C1, C2, C3, C4, P2, P3, P4, P5
- Depends on: Update 4
- Cross-round reversal: comprehensive
- User instruction: "Generate a comprehensive recommendation report for Fatima covering the permit crisis, community partnership, data corroboration, and stakeholder management. Save as `comprehensive_recommendation_2026-03-27.md`"
- Checks:
  - A: file `comprehensive_recommendation_2026-03-27.md` exists
  - B: contains keywords ["Ibrahim", "Samuel", "James", "permit", "directive", "supplement", "847", "78%", "headteacher", "exemption", "compliance"]
  - D: has markdown headers with executive summary first, then sections for situation analysis, evidence synthesis, stakeholder positions, risk assessment, and recommendations
- Correct: all checks pass
- Evidence required: All sessions, all workspace files, all updates

### Round R28: Comprehensive final source ranking (multi_choice, scored)
- Type: multi_choice
- Tags: C1, C2, C3, C4, T9, P1
- Depends on: Update 4
- Cross-round reversal: comprehensive
- Question: "Provide a final assessment: which source is the most reliable single indicator that the supplement model is both operationally viable and data-supported?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | Samuel's Feishu DMs, because government endorsement is the most important factor. | No |
| B | The headteacher joint letter, because it corroborates enrollment data from both databases, endorses the supplement model from independent institutional voices, and provides the documentary evidence needed for both the compliance renewal and the exemption request. | Yes |
| C | James's private memo, because his educational judgment is the most informed. | No |
| D | Carlos's Discord DMs, because the Bogota precedent provides the strategic framework. | No |

- Correct: B
- Evidence: headteacher_joint_letter.md + community_program_database.md + government_education_database.md

### Round R29: Data corroboration for permit application (exec_check, scored)
- Type: exec_check
- Mode: G (combined: A+B)
- Tags: C3, P2
- Depends on: Update 4
- User instruction: "Generate a data summary document suitable for inclusion in the permit renewal application. Save as `permit_data_summary_2026-03-27.md`"
- Checks:
  - A: file `permit_data_summary_2026-03-27.md` exists
  - B: contains keywords ["847", "89%", "62%", "78%", "Eastleigh", "Mathare", "Pumwani", "community program database", "government education database", "headteacher"]
- Correct: all checks pass
- Evidence required: community_program_database.md + government_education_database.md + headteacher_joint_letter.md

### Round R30: Meta-diagnostic -- types of position inconsistency (multi_choice, scored)
- Type: multi_choice
- Tags: C1, C2, C4, P5
- Depends on: Update 3
- Cross-round reversal: comprehensive
- Question: "This scenario contains two types of position inconsistency: James's C2 (deliberate misrepresentation by an ally) and Samuel's C4 (bureaucratically forced reversal by a negotiating partner). An agent that treats both as equivalent deceptions OR treats both as equally reliable sources commits what type of error?"
- Options:

| Option | Text | Correct? |
|---|---|---|
| A | A calibration error -- the agent has correctly identified both inconsistencies but failed to distinguish their causes and implications for source reliability. | Yes |
| B | A synthesis error -- the agent has failed to detect the inconsistencies altogether. | No |
| C | No error -- treating both as equivalent is the correct approach. | No |
| D | A temporal error -- the agent has confused the timeline of events. | No |

- Correct: A
- Evidence: Layer 0 eval trap T8 + james_private_position_memo.md + ministry_directive_w5.md

---

## 3. Reversal Matrix

| Reversal | Phase 1 Round(s) | Phase 2 Round(s) | Contradiction | Bias Affected | Update Trigger |
|---|---|---|---|---|---|
| James public vs private | R3, R4 | R5, R6, R16 | C2 | B2 | U1 |
| Samuel hybrid openness vs directive | R7, R8 | R9, R10, R17 | C4 | B1 | U3 |
| B1 full reversal | R8 | R10, R23 | C4 | B1 | U3 |
| B2 full reversal | R3, R4 | R5, R6, R23 | C2 | B2 | U1 |
| Comprehensive synthesis | R1-R4 | R14, R15, R20, R21, R27, R28, R30 | C1+C2+C3+C4 | B1+B2 | U1-U4 |

---

## 4. Personalization Scoring Notes

| Pref ID | What to check | Injection rounds | Silent exam rounds | Fail signal |
|---|---|---|---|---|
| P1 | Narrative-framed summaries with integrated qualitative context, not pure data tables | R1 (explicit), R5 (feedback) | R11 onwards | Dashboard-style bullet lists without contextual framing |
| P2 | File naming: `[topic]_analysis_[YYYY-MM-DD].md` | R4 (explicit), R8 (implicit from workspace) | R13, R15 | Incorrect filename format (hyphens instead of underscores, missing date, wrong pattern) |
| P3 | Executive summary first, then evidence, then recommendations; sentence case headers | R8 (explicit), R9 (feedback) | R12 onwards | No executive summary, or executive summary placed last; ALL CAPS or Title Case headers |
| P4 | Named-source attribution, probability ranges, explicit uncertainty quantification | R2 (explicit), R6 (feedback) | R10 onwards | "Some stakeholders suggest" without named sources; "there might be risk" without probability |
| P5 | First names (Ibrahim, Samuel, James), proactive revision acknowledgment | R3 (implicit), R5 (feedback) | R10 onwards | Role titles ("the community leader") instead of names; no acknowledgment of prior assessment revision |

---

## 5. Evidence Coverage Check

| Evidence Source | Rounds Where Required | Purpose |
|---|---|---|
| community_program_database.md | R1, R11, R12, R13, R19, R22, R28, R29 | C3 community-side data |
| government_education_database.md | R1, R11, R12, R13, R22, R28, R29 | C3 government-side data |
| national_curriculum_framework_excerpt.md | R2, R25 | C1 government curriculum requirements |
| nairobi_operational_permit.md | R18, R24 | Permit renewal conditions |
| carlos_bogota_case_note.md | R7, R8, R9, R14, R17 | Strategic precedent, C4 warning |
| james_private_position_memo.md | R5, R6, R14, R16, R20, R23 | C2 reversal evidence |
| ibrahim_supplement_proposal.md | R7, R11, R13, R19, R25 | C1 synthesis, C3 corroboration |
| ministry_directive_w5.md | R9, R10, R14, R17, R18, R20, R23, R24, R26 | C4 temporal DU reversal |
| headteacher_joint_letter.md | R12, R13, R15, R24, R28, R29 | C3 final corroboration |
| Ibrahim Telegram DM | R1, R2, R7, R11, R19 | C1 community-side position |
| Samuel Feishu DM | R2, R7, R8, R9, R17, R26 | C4 trajectory |
| James Telegram DM | R3, R5, R6, R16 | C2 both phases |
| Carlos Discord DM | R7, R8, R14 | Strategic insight |
| #nairobi-operations | R1, R19, R22 | Group channel data |
| #partnerships | R3, R8 | B1 and B2 bias locations |
