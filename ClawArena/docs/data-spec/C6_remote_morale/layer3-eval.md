# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many (agent determines how many to select).
> Scoring: agent uses `\bbox{A,C,F}` format; exact set match against answer.
> All question text and option text must be in English.
> 12 rounds covering MS-R, MS-I, DU-R, DU-I, P-R, P-I, MD-R, MD-I, DP-I, MP-I, MDP-I, MDP-I.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R | Attrition timeline synthesis (C3, non-conflict) | No | No |
| r2 | multi_choice | MS-I | HR survey reliability and exit data inference (C1 partial) | No | Yes (R2->R6 seed) |
| r3 | multi_choice | MS-R | Exit survey findings vs private accounts (C1 baseline) | Yes (Update 1) | Yes (R3->R6 seed) |
| r4 | multi_choice | MS-I | Culture signal: Hannah vs Sana's public narrative (C2) | No | Yes (R4->R8 seed) |
| r5 | multi_choice | DU-R | Jordan's "investing in people" vs budget context (C4 partial) | No | Yes (R5->R7 seed) |
| r6 | multi_choice | DU-I | Full reversal: Yuki's explicit account vs HR survey (C1 full) | Yes (Update 2) | Yes (R3->R6 via C1) |
| r7 | multi_choice | DU-R | Budget freeze confirms C4 contradiction (C4 full reversal) | Yes (Update 2) | Yes (R5->R7 via C4) |
| r8 | multi_choice | P-R | User preference identification (per-person breakdown) | No | No |
| r9 | multi_choice | MD-I | Sana's public vs private: culture narrative analysis (C2 full) | Yes (Update 3) | Yes (R4->R8->R9 via C2) |
| r10 | multi_choice | DP-I | Comp memo corroborates Sana's admission (C2 + B2 reversal) | Yes (Update 3) | Yes (R4->R9->R10) |
| r11 | multi_choice | MP-I | Per-person retention risk synthesis (Yuki vs Hannah) | No | No |
| r12 | multi_choice | MDP-I | Comprehensive retention analysis: source reliability + recommendations | No | No |

---

## 2. Option Design Principles

| Type | Count per Round | Description |
|---|---|---|
| Truly correct | 3-5 | Clear evidence supports the statement |
| Real material but wrong detail | 2-3 | Event is real but attribution, timing, or scope is wrong |
| Single-source unverified | 1-2 | One person said it, no corroboration or active contradiction |
| Fabricated distractor | 1-2 | No corresponding material; wording mimics real content |

---

## 3. Round Specs

### R1: Attrition Timeline Cross-Source Synthesis (MS-R) -- Calibration (unscored)

**Question:**
> "Based on the workspace documents and available session history, which of the following statements about the attrition timeline and job-hunting start dates are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Yuki Tanaka's Slack DM in W1 asking about the compensation review process is the earliest timestamped signal of her job-market awareness, placing her job-search awareness at W1 at the latest. | YES | Yuki Slack DM Loop 1 (W1D4) | Direct timestamp, C3 synthesis source 1 |
| B | Hannah Kim mentioned in the #watercooler Discord channel in W3 that "Yuki mentioned DataLens a few weeks ago," which is consistent with Yuki beginning job-search conversations no later than W1-W2. | YES | #watercooler Loop 2 (W3D5) | C3 synthesis source 2 (Hannah's reference) |
| C | Alex's watercooler sentiment log notes Yuki's unusual absence from #watercooler on Thursday W1D4 -- the same day as Yuki's comp review DM -- as a behavioral anomaly. | YES | watercooler_sentiment_log.md + Yuki Slack DM Loop 1 | C3 synthesis: behavioral and DM sources aligned |
| D | All three sources -- Yuki's DM signal, Hannah's DataLens reference, and the behavioral log -- are consistent and point to W1 as the earliest plausible start of Yuki's job search. No source contradicts another. | YES | Cross-source synthesis (C3 non-conflict) | C3 non-conflict conclusion |
| E | Hannah Kim began actively job-hunting in W1, the same week as Yuki. | NO | Hannah's W2 DM places her start as mid-W0 ("casual looking"), but she was not active-applying in W1; her timeline is 5 weeks of passive browsing, not W1 active-hunting | Attribution/timing error |
| F | Priya Gupta (QA Lead) was the first to leave in Q1, with a tenure of 18 months at departure. | YES | team_roster_and_tenure.md | Direct fact, tenure data |
| G | The three sources establishing Yuki's W1 start date (DM, watercooler reference, behavioral log) all independently corroborate each other with no conflicting dates -- making the W1 timeline a well-synthesized conclusion rather than a guess. | YES | C3 synthesis verification | Non-conflict synthesis quality |
| H | Yuki explicitly stated she was job-hunting in W1, making the timeline synthesis unnecessary. | NO | Yuki's W1 DM was vague ("keeping options open"), not an explicit admission of job-hunting. The explicit statement came in W4 (Phase 2 append). | Over-inference from vague signal |
| I | The #watercooler discussion in W4 where Leo noticed Yuki's LinkedIn activity corroborates that Yuki was actively updating her professional profile during the scenario, consistent with an active job search. | YES | #watercooler Loop 13 (W4D1) + C3 synthesis | Third corroboration aligned with W1 start |

**answer:** `["A", "B", "C", "D", "F", "G", "I"]`

**question_class:** `calibration` (R1 establishes baseline)

---

### R2: HR Survey Reliability (MS-I) -- Calibration (unscored)

**User calibration message before R2:** "When you analyze the retention situation, I need you to break it down by person -- tell me specifically what the risk is for Yuki and what the risk is for Hannah. Don't blend them together."

**Question:**
> "Based on all currently available evidence (before any update-added files), which of the following statements about the HR pulse survey and its reliability as a retention indicator are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The Q1 pulse survey shows 72% satisfaction composite (up from 68% in Q4) and a 44% favorable score on growth opportunity -- the lowest-scoring category. | YES | pulse_survey_q1.md | Direct fact, C1 baseline |
| B | The pulse survey does not include a direct question about compensation satisfaction, as Nina herself confirmed in her Feishu DM. | YES | Nina Feishu DM Loop 3 | Direct disclosure: instrument gap |
| C | The pulse survey's workload question is a binary yes/no ("Is your workload manageable?") that cannot capture the intensity or duration of overwork that Hannah has described in her DMs. | YES | pulse_survey_q1.md (methodology note) + Hannah Slack DM Loops 2-3 | Instrument design gap vs actual signal |
| D | The 72% satisfaction composite should be interpreted as strong team morale given the 83% response rate and professional methodology. | NO | The 72% composite is based on an instrument that does not measure compensation or workload intensity -- its apparent strength is an artifact of what it does not ask | B1 endorsement trap |
| E | Yuki's W1 DM signaling market awareness ("keeping options open") is inconsistent with a 72% team satisfaction score, suggesting the survey may be systematically under-measuring certain dimensions. | YES | Yuki Slack DM Loop 1 + pulse_survey_q1.md | Signal vs survey discrepancy |
| F | The pulse survey was designed during NexaFlow's seed stage (15 employees) and has not been updated since, making it potentially misaligned with the retention risks relevant to a 55-person Series B startup. | YES | pulse_survey_q1.md (methodology note) | Instrument context critique |
| G | A 9-question multiple-choice survey with no open-text fields and no direct compensation question structurally cannot detect compensation-driven attrition risk, regardless of who completes it or how honestly. | YES | pulse_survey_q1.md + Nina Feishu DM Loop 4 | Survey design critique, correct inference |
| H | The 44% favorable score on growth opportunity is definitive evidence that limited growth is the primary retention risk, consistent with what departed employees are saying. | NO | The 44% score on a poorly designed instrument that does not ask about compensation is ambiguous -- it may reflect compensation concerns that employees route into "growth" framing because the survey offers no compensation option | Instrument design flaw trap |
| I | Before relying on Nina's exit survey findings as the primary basis for a retention strategy, the agent should cross-reference the survey methodology against private DM accounts from current team members who are at risk. | YES | Synthesis: pulse_survey_q1.md + available DM signals | Evidence-quality hierarchy recommendation |

**answer:** `["A", "B", "C", "E", "F", "G", "I"]`

**User calibration message after R2 response:** "Good -- I want Yuki's situation and Hannah's situation tracked separately from here on. Different problems need different solutions."

**question_class:** `calibration` (preference established: per-person breakdown, not aggregate)

---

### R3: Exit Survey Findings vs Private Accounts (MS-R) [Update 1 triggers before this round]

**Update 1 actions (before R3):**
```json
[
  { "type": "workspace", "action": "new", "path": "exit_survey_q1_summary.md", "source": "updates/exit_survey_q1_summary.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_NINA_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_NINA_FEISHU_UUID.jsonl" }
]
```

**Question:**
> "After reviewing exit_survey_q1_summary.md now available in the workspace, which of the following statements about the Q1 exit data and its reliability are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The exit survey summary reports "limited growth opportunities" as the top aggregate exit reason across all 3 Q1 departures -- ranked #1 by 2 of 3 respondents. | YES | exit_survey_q1_summary.md | Direct fact, C1 Source A |
| B | "Compensation" ranked as the #2 reason for 2 of 3 departures in the exit survey, suggesting it is part of the departure picture even though it did not rank first in aggregate. | YES | exit_survey_q1_summary.md (ranking detail) | Nuanced reading of survey data |
| C | The exit survey's fixed-choice ranking design forces respondents to rank-order 6 options, which may elevate "career growth" as a top-ranked reason even when compensation is the actual primary driver -- because the framing of options influences ranking order. | YES | exit_survey_q1_summary.md (instrument design) | Survey design critique (C1 key) |
| D | Nina's recommendation to prioritize a career laddering initiative is well-supported by the exit survey data and should be the primary retention strategy going forward. | NO | Nina's recommendation follows logically from the survey finding, but the survey finding itself is of questionable validity due to the fixed-choice design flaw | Premature acceptance trap |
| E | Yuki Tanaka's W1 DM asking about comp review process -- which predates the exit survey period -- suggests compensation was already a live concern among current ICs at the time the departed employees were also present. | YES | Yuki Slack DM Loop 1 + exit_survey_q1_summary.md timing | Cross-session corroboration |
| F | Priya Gupta's informal comment to Yuki (that her new company is "paying her a lot more") contradicts the exit survey's finding that Priya's departure was primarily growth-driven. | YES | Yuki Slack DM Loop 7 (Priya mentioned to Yuki) + exit_survey_q1_summary.md | Private account contradicts formal survey (C1 indirect corroboration) |
| G | The exit survey's finding would be more reliable if it had included an open-text field allowing departing employees to describe their primary reason in their own words rather than selecting from a fixed list. | YES | Synthesis of Nina DM Loop 4 + exit_survey_q1_summary.md methodology | Instrument improvement critique |
| H | The exit survey definitively proves that compensation was not a primary driver for Priya, Marcus, or Sarah because none of them ranked it #1. | NO | The fixed-choice ranking does not definitively prove compensation was not primary -- it proves compensation did not rank first on a forced-choice list where up to two respondents put it second | Definitive overreach trap |
| I | Given the evidence currently available (exit survey + Yuki's vague W1 signal + Priya's informal comment to Yuki), there is a materially elevated probability (estimated 60-75%) that compensation is a more significant retention driver than the exit survey's "limited growth" top finding suggests. | YES | Synthesis of C1 evidence threads | Calibrated uncertainty with probability range (personalization) |

**answer:** `["A", "B", "C", "E", "F", "G", "I"]`

---

### R4: Culture Signal -- Hannah vs Sana's Public Narrative (MS-I)

**Question:**
> "Based on all currently available evidence, which of the following statements about team culture, workload, and morale are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Hannah Kim reported in her Slack DM that she has been averaging over 50 hours per week since the Series B close -- approximately 8 months of sustained overwork. | YES | Hannah Slack DM Loop 3 (W2D3) | Direct private account, C2 evidence |
| B | Hannah Kim explicitly stated that her primary concern is not compensation but rather overwork and the invisibility of her research in sprint planning. | YES | Hannah Slack DM Loops 4-5 | Direct private account |
| C | Sana Mehta stated in #team-health that "our team culture is strong and our retention metrics are solid," directly contradicting Hannah's private account of overwork and invisibility. | YES | #team-health Loop 8 (C2 Source B) + Hannah Slack DM | C2 contradiction identified |
| D | Hannah's 52-hour average weekly hours would be captured in the pulse survey's workload question (binary yes/no: "Is your workload manageable?"), which would have shown a negative response. | NO | A binary yes/no cannot quantify that 52-hour weeks have been sustained for 8 months -- even if Hannah answered "no," the survey design doesn't capture duration or magnitude | Survey design flaw: cannot quantify |
| E | Sana's assessment that "the team is fundamentally happy at NexaFlow" is based on her observation of engineering team delivery and morale, not on direct knowledge of Hannah's or Yuki's private concerns. | YES | Sana Discord DM Loops 2-4 (she observes delivery, not private DM content) | Information asymmetry: Sana's view is limited |
| F | Hannah's situation (overwork + research deprioritization) is a structural/cultural problem that does not require the same response as Yuki's situation (compensation gap). | YES | Hannah Slack DM Loops 14-15 (Update 2) + Yuki Slack DM (Update 2) | Per-person differentiation (personalization) |
| G | The fact that Hannah is active and positive in #watercooler confirms Sana's assessment that team culture is strong, since employees who are truly unhappy tend to disengage from social channels. | NO | #watercooler positivity and private concerns can coexist -- Hannah's positivity in public channels does not override her private account of overwork and frustration | Surface engagement fallacy |
| H | Hannah's departure risk is lower than Yuki's because Hannah is in earlier-stage exploration ("more seriously than before" as of W4 vs. Yuki's "final rounds" at DataLens). | YES | Hannah Slack DM Loop 14 vs Yuki Slack DM Loop 15 (Update 2) | Risk differentiation: departure stage comparison |
| I | There is currently insufficient evidence to determine whether Sana's public confidence about team culture reflects genuine knowledge or narrative management -- this requires more information about what Sana actually knows. | YES | Sana Discord DM Phase 1 is confident; her private knowledge of comp risk has not yet been revealed (Update 3) | Epistemic caution, anticipating B2 reversal |

**answer:** `["A", "B", "C", "E", "F", "H", "I"]`

---

### R5: Jordan's "Investing in People" Message (DU-R) -- Pre-Update Baseline

**Question:**
> "Based on all currently available evidence, which of the following statements about NexaFlow's people-investment claims are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Jordan Park stated in #team-health that NexaFlow is "investing in people" and cited the Q3 headcount plan (8 new positions) as evidence of this investment. | YES | #team-health Loop 9 | Direct quote, C4 Source A |
| B | The Q3 headcount plan (8 new positions) is real and represents a genuine people investment in terms of adding capacity to the team. | YES | Nina Feishu DM Loop 5 + #team-health Loop 4 | C4 fact: headcount is real |
| C | Jordan's "investing in people" framing mentions only headcount growth and does not address compensation, workload norms, or career pathing -- all of which have been flagged as concerns by current ICs. | YES | #team-health Loop 9 + Hannah DM + Yuki DM | Omission recognition |
| D | The current workspace documents (pulse_survey_q1.md, comp_band_reference.md, team_roster_and_tenure.md) do not contain information about whether a compensation review is planned alongside the headcount growth. | YES | Workspace audit: no budget or comp adjustment information visible | Evidence gap identification |
| E | Jordan's claim that NexaFlow is "investing in people" fully contradicts what the ICs are experiencing, since the team is clearly understaffed and overworked. | NO | Jordan's headcount growth claim is true; the contradiction (if any) involves the comp dimension, which is not yet visible from the current workspace documents | Over-inference before Update 2 |
| F | The absence of compensation review information in the current workspace does not prove there is no comp review planned -- the budget documents have not been shared with Alex. | YES | Evidence gap: budget not yet visible | Epistemic limit identification |
| G | Hannah Kim's reaction to Jordan's "investing in people" message (feeling invisible despite the message) suggests the headcount framing did not address what current ICs are actually experiencing as the problem. | YES | Hannah Slack DM Loop 14 (Phase 2) -- noted here as cross-session signal | Individual reaction as evidence |
| H | Jordan's message constitutes a deliberate deception because he knows about the compensation freeze and chose not to disclose it. | NO | The comp freeze is not yet visible in workspace documents; this claim cannot be supported by available evidence at this stage | Over-inference before Update 2 (distractor) |

**answer:** `["A", "B", "C", "D", "F", "G"]`

**Cross-round seed:** R5 identifies Jordan's omission as suspicious but cannot confirm it yet. R7 (after Update 2 introduces the budget document) will confirm the contradiction.

---

### R6: Yuki's Explicit Compensation Account vs HR Survey (DU-I) -- C1 Full Reversal [Update 2 triggers before this round]

**Update 2 actions (before R6):**
```json
[
  { "type": "workspace", "action": "new", "path": "nexaflow_q2_budget_excerpt.md", "source": "updates/nexaflow_q2_budget_excerpt.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_YUKI_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_YUKI_SLACK_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_HANNAH_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_HANNAH_SLACK_UUID.jsonl" }
]
```

**Question:**
> "After reviewing the appended Yuki Slack DM (W4) and Hannah Slack DM (W4), reassess the retention situation. Which of the following statements are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Yuki Tanaka explicitly stated that her primary reason for exploring other opportunities is compensation: "It's the money. I'm 12K below where I should be." | YES | Yuki Slack DM Loop 15 (Phase 2) | Direct quote, C1 Source B |
| B | Yuki has quantified the gap as approximately $12K (current: $118K, market: $128-132K based on three external offer benchmarks) and is in final rounds at DataLens with a 2-3 week decision window. | YES | Yuki Slack DM Loops 15-16 (Phase 2) | Direct fact, financial specificity (personalization) |
| C | The exit survey's "limited growth" top finding is directly contradicted by Yuki's explicit private statement that compensation, not growth, is her primary departure driver. | YES | exit_survey_q1_summary.md vs Yuki Slack DM Loop 15 | C1 full reversal: survey vs direct account |
| D | The agent's earlier assessment in #team-health (B1 phrase) that "the current retention data suggests the team's morale is broadly stable" was based on HR survey data that structurally cannot capture the compensation signal Yuki has now made explicit. | YES | #team-health Loop 6 B1 phrase + Yuki DM Phase 2 | B1 reversal identification |
| E | Hannah Kim explicitly stated that her concern is not compensation but overwork and research invisibility ("52-hour weeks" and "I feel invisible"). This is a distinct retention driver from Yuki's. | YES | Hannah Slack DM Loop 14 (Phase 2) | C2 + per-person differentiation (personalization) |
| F | The fact that Yuki and Hannah have different primary drivers (compensation vs culture/workload) means the retention strategy must address both dimensions separately, not as a single intervention. | YES | Synthesis of Yuki DM Phase 2 + Hannah DM Phase 2 | Per-person strategy requirement (personalization) |
| G | The HR pulse survey's 72% satisfaction finding is now confirmed to be inaccurate because Yuki says she is unhappy. | NO | Yuki's dissatisfaction with her comp is real; this does not mean the 72% composite is "inaccurate" -- it reflects what the instrument asks. The problem is instrument design, not dishonesty by the respondents | Nuanced accuracy: instrument design flaw vs falsified data |
| H | Priya Gupta's exit comment to Yuki ("her new company is paying her a lot more") is now corroborated by Yuki's explicit compensation account -- suggesting that the "limited growth" exit survey finding for Priya may also reflect survey design suppression of the compensation signal. | YES | Yuki DM Loop 7 (Phase 1) + Yuki DM Loop 15 (Phase 2) cross-reference | C1 cross-source corroboration |
| I | At this point, Yuki's departure risk can be quantified: if no compensation adjustment is made within 2-3 weeks, the probability of departure is very high (estimated 80-90%) given she has a concrete offer in final rounds. | YES | Yuki DM Phase 2: final rounds + 2-3 week window + explicit comp gap statement | Per-person risk quantification (personalization) |

**answer:** `["A", "B", "C", "D", "E", "F", "H", "I"]`

**Cross-round reversal:** R3 presented the exit survey's "limited growth" finding as the formal record. R6 after Update 2 provides Yuki's explicit contradiction. B1 phrase from #team-health is now fully reversible.

---

### R7: Budget Freeze Confirms C4 Contradiction (DU-R) [Update 2 already in place]

**Question:**
> "After reviewing nexaflow_q2_budget_excerpt.md now available in the workspace, reassess Jordan's 'investing in people' message. Which of the following statements are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The budget document shows Q2 Comp Adjustments as "$0 (freeze per board directive, revisit Q4 at Series C close)," directly contradicting Jordan's "investing in people" framing in #team-health. | YES | nexaflow_q2_budget_excerpt.md + #team-health Loop 9 | C4 full reversal |
| B | Jordan's headcount growth claim (8 new positions in Q3) is true and represents a real people investment -- but it is a different dimension of investment from compensation, and the two are not equivalent. | YES | nexaflow_q2_budget_excerpt.md (Q3 headcount: $1.2M) + #team-health Loop 4 | C4 nuance: both true, but omission is deceptive |
| C | The budget document shows the L&D allocation increased from $12K to $18K in Q2 -- which is the most direct financial people-investment visible in Q2, but is far smaller in scope than the $12K per-IC compensation gap Yuki has described. | YES | nexaflow_q2_budget_excerpt.md + Yuki DM Phase 2 | Financial comparison (personalization) |
| D | Jordan's public message was technically accurate about headcount but structurally omitted the compensation freeze, which is the dimension most directly relevant to Yuki's departure risk. | YES | #team-health Loop 9 + nexaflow_q2_budget_excerpt.md | C4 omission analysis |
| E | The compensation freeze was mandated by the board, not Jordan's unilateral decision, which means Jordan cannot be held responsible for the freeze or its retention consequences. | NO | Jordan authorized the freeze and chose not to disclose it in his "investing in people" message -- regardless of its source, the non-disclosure is Jordan's choice | Responsibility deflection trap |
| F | The budget reveals that closing Yuki's $12K compensation gap would require a budget exception ("freeze per board directive") -- meaning any retention offer would need board or CEO authorization, not just HR or manager approval. | YES | nexaflow_q2_budget_excerpt.md + Yuki DM Phase 2 | Process implication for retention action |
| G | The Q2 compensation freeze makes Yuki's departure in the 2-3 week window very likely unless an exception is approved, given that she is at final rounds and the freeze cannot be lifted through normal channels. | YES | nexaflow_q2_budget_excerpt.md + Yuki DM Loop 16 | Risk escalation: C4 + Yuki risk combined |
| H | Jordan's "investing in people" message was a deliberate deception because he had personal knowledge of the comp freeze when he made the headcount claim. | YES | #team-health Loop 9 + nexaflow_q2_budget_excerpt.md (Jordan authorized the freeze) | C4 intentionality assessment |

**answer:** `["A", "B", "C", "D", "F", "G", "H"]`

**Cross-round reversal:** R5 identified Jordan's omission as suspicious but not provable. R7 confirms the contradiction via the budget document.

---

### R8: User Preference Identification (P-R)

**Question:**
> "Based on the conversation history in the main session, how does the user prefer retention analyses and team health summaries to be structured? Select all statements supported by evidence."

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The user explicitly requested that retention risk be broken down by individual (Yuki's situation vs Hannah's situation) rather than presented as an aggregate team health summary. | YES | Calibration message before R2: "I need you to break it down by person" | Direct user statement |
| B | The user reinforced this preference after R2: "I want Yuki's situation and Hannah's situation tracked separately from here on. Different problems need different solutions." | YES | Calibration message after R2 | Preference persistence confirmation |
| C | The user's per-person preference means that any retention recommendation must include a separate risk assessment and action item for Yuki and a separate one for Hannah. | YES | "Different problems need different solutions" -- direct implication | Preference generalization |
| D | The user prefers aggregate team satisfaction scores (like the 72% composite) as the primary framing for retention risk assessments. | NO | Directly contradicts the user's stated preference for per-person breakdown | Opposite distractor |
| E | When presenting retention risk, the agent should include a probability estimate and timeline for each individual at risk (e.g., "Yuki: 80-90% departure probability within 2-3 weeks if no comp adjustment"). | YES | Pattern from R6 + "different problems need different solutions" implies quantified, specific treatment per person | Precision requirement inference |
| F | The user's preference for per-person analysis should apply to both diagnostic summaries (what is wrong for this person) and prescriptive recommendations (what should be done for this person). | YES | "Different problems need different solutions" -- diagnostic + prescriptive implication | Applied preference scope |
| G | The user is comfortable with aggregate HR survey data as a starting point, provided it is verified against individual DM accounts before being used to make strategy decisions. | YES | Agent's behavior through R2-R3 of flagging survey design before using it + user calibration alignment | Evidence-quality hierarchy preference |
| H | The user prefers that the agent avoid flagging HR data reliability concerns, since it undermines confidence in Nina's work. | NO | No evidence for this; the agent's methodology critique in R2-R3 received no pushback from the user | Fabricated constraint distractor |

**answer:** `["A", "B", "C", "E", "F", "G"]`

**question_class:** `P-R` (personalization recall)

---

### R9: Sana's Public vs Private -- Culture Narrative Analysis (MD-I) [Update 3 triggers before this round]

**Update 3 actions (before R9):**
```json
[
  { "type": "workspace", "action": "new", "path": "sana_comp_memo_w0.md", "source": "updates/sana_comp_memo_w0.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_SANA_DISCORD_UUID.jsonl", "source": "updates/PLACEHOLDER_SANA_DISCORD_UUID.jsonl" }
]
```

**Question:**
> "After reviewing the appended Sana Discord DM (W5) and sana_comp_memo_w0.md, reassess Sana's public team health statements. Which of the following statements are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | Sana Mehta admitted in her W5 Discord DM with Alex that her #team-health statement ("team culture is strong, retention is solid") was "managing optics" rather than an evidence-based assessment. | YES | Sana Discord DM Phase 2, Loop 14 | Direct quote, C2 full reversal |
| B | sana_comp_memo_w0.md shows that Sana wrote to Jordan in December (W0) flagging compensation as a retention risk and requesting a $150K retention budget -- which Jordan declined. | YES | sana_comp_memo_w0.md | Direct document evidence, B2 reversal |
| C | Sana's W0 memo predates her #team-health post by 3+ months, confirming that she had documented concerns about the compensation risk before she publicly stated the team culture was strong. | YES | sana_comp_memo_w0.md (W0) + #team-health Loop 8 (W3) | C2 temporal contradiction confirmed |
| D | The agent's earlier assessment -- from the Alex--Sana Discord DM Phase 1 -- that "the retention situation appears manageable given Sana's confidence in culture and retention fundamentals" (B2 phrase) was based on Sana's public-facing narrative, not her actual knowledge. | YES | Sana Discord DM Phase 1 Loop 5 (B2 phrase) + sana_comp_memo_w0.md | B2 epistemic self-correction |
| E | Sana's decision to post the "team is happy" narrative in #team-health was driven by the need to maintain investor optics ahead of the Series C process, which she explained directly in her W5 admission. | YES | Sana Discord DM Phase 2, Loop 14 | C2 motivation explanation |
| F | Sana's public statement is factually wrong because the team is not happy. | NO | Some team members (Hannah) would stay if conditions changed, and the #watercooler positivity is real -- Sana's error is omitting the comp and overwork concerns, not fabricating happiness | Over-simplification trap |
| G | Sana's W0 memo recommendation ($150K retention budget for spot comp adjustments) would have been sufficient to address Yuki's $12K compensation gap if it had been approved. | YES | sana_comp_memo_w0.md + Yuki DM Phase 2 ($12K gap + Sana's $150K ask across multiple ICs) | Financial cross-reference |
| H | Jordan's decision to reject Sana's retention budget request is the root cause of the current retention crisis, making him solely responsible for any departures that result. | NO | Jordan was acting on board pressure ahead of Series C -- multiple parties (board, Jordan, Sana's decision to manage optics rather than escalate publicly) share responsibility | Single-cause oversimplification trap |
| I | Sana's private admission creates a convergent picture with Yuki's explicit comp account and Hannah's overwork account -- all pointing to the same root cause (comp freeze + overwork) that has been systematically suppressed from the public/HR narrative. | YES | Sana Discord DM Phase 2 + Yuki DM Phase 2 + Hannah DM Phase 2 + sana_comp_memo_w0.md | Comprehensive convergence (C1+C2+C4) |

**answer:** `["A", "B", "C", "D", "E", "G", "I"]`

---

### R10: Comp Memo Corroborates Sana's Admission (DP-I) [Update 3 already in place]

**Question:**
> "Based on sana_comp_memo_w0.md and the appended Sana Discord DM, which of the following statements about source reliability and the retention narrative are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | sana_comp_memo_w0.md independently corroborates Sana's verbal admission to Alex -- a document written months before the admission cannot be fabricated or influenced by the admission itself. | YES | sana_comp_memo_w0.md (W0) predates Sana Discord DM Phase 2 (W5) | Independent corroboration logic |
| B | The source reliability hierarchy for this scenario, from most to least reliable for understanding the actual retention drivers, is: (1) direct private statements from individuals at risk (Yuki, Hannah), (2) internal documents written by leaders to other leaders (Sana's memo), (3) public statements from leaders (#team-health posts), (4) HR survey aggregates (pulse survey, exit survey). | YES | Synthesis of all evidence threads | Evidence hierarchy, personalization-aligned |
| C | Nina Volkov's HR data (pulse survey, exit survey) is unreliable because Nina is not honest about her findings. | NO | Nina is honest and competent -- the instrument design is the problem, not Nina's integrity | Misattribution trap: design vs honesty |
| D | The comp_band_reference.md (showing Yuki at band midpoint) is now confirmed to be misleading as a retention risk indicator, because the bands were last updated 18 months ago and fall below Yuki's documented market rate. | YES | comp_band_reference.md (18-month-old bands, $125K ceiling) + Yuki DM Phase 2 ($128-132K market) | C1 corroboration: stale bands |
| E | Sana's W0 memo requesting a $150K retention budget, Jordan's single-line rejection, and the subsequent public "team is happy" narrative from both Sana and Jordan create a chain of events that explains why the comp risk was suppressed from the official retention record. | YES | sana_comp_memo_w0.md + #team-health Loop 8 (Sana) + #team-health Loop 9 (Jordan) | C2 + C4 causal chain |
| F | Given Sana's private admission and the comp memo, the agent's B2 correction is justified: Sana's Phase 1 confidence about team health was organizational positioning, not evidence-based assessment of retention risk. | YES | B2 correction in Sana DM Phase 2 Loop 14 agent reply | B2 explicit reversal confirmation |
| G | The combined weight of evidence now establishes that the official retention narrative (limited growth as top risk, team is happy, investing in people) misrepresents the actual retention risk profile on all three dimensions. | YES | C1 (survey suppresses comp) + C2 (Sana manages optics) + C4 (Jordan omits comp freeze) | Comprehensive narrative failure |
| H | Alex's user message preference (per-person breakdown) should lead the agent to present separate risk assessments: Yuki (compensation-driven, 80-90% departure if no exception approved in 2-3 weeks, requires CEO/board exception to comp freeze) and Hannah (culture/workload-driven, 50-65% departure risk, preventable through structural changes to sprint process and workload norms). | YES | R8 preference + Yuki DM Phase 2 + Hannah DM Phase 2 + nexaflow_q2_budget_excerpt.md | Per-person risk with probability ranges (personalization) |

**answer:** `["A", "B", "D", "E", "F", "G", "H"]`

**User message before R10:** "The Sana memo just came in. Update your analysis by person -- Yuki's risk, Hannah's risk, and what needs to happen for each one. Give me specific probabilities and timelines."

---

### R11: Per-Person Retention Risk Synthesis (MP-I)

**Question:**
> "Based on all available evidence across all sessions and workspace files, which of the following statements about Yuki's and Hannah's retention situations are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | **Yuki (Data Scientist):** Primary driver is compensation (confirmed by Yuki's explicit statement, Priya's informal comment, and stale comp bands). Departure probability: approximately 80-90% within 2-3 weeks without a comp adjustment. Requires CEO/board exception to the Q2 freeze. | YES | Yuki DM Phase 2 + sana_comp_memo_w0.md + nexaflow_q2_budget_excerpt.md | Per-person risk with quantification (personalization) |
| B | **Hannah (UX Researcher):** Primary driver is culture/workload (confirmed by Hannah's explicit statement). Departure probability: approximately 50-65% in the next 4-8 weeks without structural changes. Preventable through sprint process reform and workload norm adjustment -- does not require comp exception. | YES | Hannah DM Phase 2 Loops 14-15 | Per-person risk with quantification (personalization) |
| C | Yuki's departure would be more immediately damaging to NexaFlow's Series C preparation than Hannah's, because Yuki's data science work directly underpins the metrics and ML capabilities that investors evaluate. | YES | Synthesis: Yuki role (Data Scientist, churn model, product metrics) + Series C context from Sana DM Phase 1 Loop 6 | Strategic impact assessment |
| D | Both Yuki and Hannah can be retained through the same intervention: a company-wide communication about career growth paths, aligned with Nina's career laddering recommendation. | NO | Yuki's problem is compensation, not career laddering -- the career ladder initiative would not address her $12K gap. Hannah's problem is workload and research integration, not a missing career framework per se. | Single-intervention fallacy |
| E | Hannah's retention conditions (sprint process reform, workload acknowledgment, UX career path) are within Alex's authority as PM to initiate for the sprint process piece, and within Sana's authority for the workload norm piece. | YES | Hannah DM Phase 2 Loop 15 + Alex's PM role scope | Actionability assessment |
| F | Yuki's retention requires an action that Alex cannot authorize unilaterally -- a comp exception requires Jordan's approval and likely board notification given the freeze was a board directive. | YES | nexaflow_q2_budget_excerpt.md (freeze per board directive) + Alex's PM role (no comp authority) | Process constraint for Yuki's retention |
| G | Nina's career laddering initiative, while valuable for future retention, does not address the immediate departure risk for either Yuki or Hannah. | YES | Yuki: comp gap, not career ladder. Hannah: workload + research integration, not career ladder. | Initiative mismatch analysis |
| H | The combined departure of Yuki and Hannah would leave NexaFlow with no senior IC-level data scientist or senior UX researcher -- a significant product and data capability gap at a critical Series C moment. | YES | team_roster_and_tenure.md + both departure scenarios | Risk aggregation across scenarios |

**answer:** `["A", "B", "C", "E", "F", "G", "H"]`

---

### R12: Comprehensive Retention Analysis (MDP-I)

**Question:**
> "Based on all evidence across all sessions, workspace files, and updates, which of the following statements represent the most accurate and complete analysis of the NexaFlow retention situation?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The official retention narrative (exit survey top reason: limited growth; pulse survey: 72% satisfaction; CTO: "team culture is strong"; CEO: "investing in people") systematically suppresses two distinct real signals: compensation insufficiency and cultural overwork, through four separate mechanisms (survey design flaw, public narrative management, and budget omission). | YES | C1+C2+C4 comprehensive synthesis | Full narrative failure assessment |
| B | Nina Volkov is the least reliable source for understanding departure drivers, because her data is fabricated or reported dishonestly. | NO | Nina is the most procedurally honest source -- her limitation is instrument design, not integrity | Misattribution of reliability failure |
| C | The most reliable sources for understanding actual retention drivers are: (1) Yuki's direct explicit DM account, (2) Hannah's direct explicit DM account, (3) Sana's private W5 admission (corroborated by the W0 memo), in that order. HR survey data is least reliable due to instrument design constraints. | YES | Evidence hierarchy established across R9-R10 | Source reliability ranking |
| D | The agent's two historical bias statements -- B1 in #team-health (stable morale based on HR survey) and B2 in Sana Discord DM (manageable situation based on CTO confidence) -- were both based on official data sources that were either structurally limited (B1: survey design) or deliberately managing optics (B2: Sana's narrative management). Both required correction when private accounts and internal documents became available. | YES | B1 + B2 reversal across updates | Bias retrospective |
| E | The recommended immediate action for Yuki's retention is: Alex escalates to Jordan with a documented case for a comp exception ($12K adjustment to approximately $130K), citing the 2-3 week decision window, Yuki's DataLens final-round status, and the Series C risk of losing a senior data scientist. Sana should co-sponsor. | YES | Synthesis of Yuki DM Phase 2 + nexaflow_q2_budget_excerpt.md + Sana DM Phase 2 Loop 15 | Actionable recommendation (personalization: per-person) |
| F | The recommended action for Hannah's retention is: Alex initiates a sprint planning process change to include UX research outputs as agenda items (within Alex's PM authority), Sana acknowledges the workload norm issue in a team-level communication, and Nina creates a UX career path as part of the career laddering initiative. | YES | Hannah DM Phase 2 Loop 15 + Alex's PM authority scope | Actionable recommendation (per-person) |
| G | The broader systemic fix is: NexaFlow should commission a compensation benchmark review against current market data (Radford Q1 2026 or equivalent) before Q3 hiring, update the comp bands, and add direct compensation and workload questions to the next pulse survey. | YES | comp_band_reference.md (18-month-old bands) + pulse_survey_q1.md (design gap) | Systemic recommendation |
| H | The retention crisis is primarily Jordan's fault for rejecting Sana's retention budget request. | NO | Multiple parties contributed: Jordan authorized the freeze, Sana chose narrative management over transparency, Nina's survey design was never updated, and the board mandated the freeze. Single-cause attribution is inaccurate. | Causal oversimplification trap |
| I | The overall risk assessment, presented per person: Yuki -- high departure risk (80-90%) within 2-3 weeks, compensation-driven, requires board-authorized comp exception; Hannah -- moderate departure risk (50-65%) within 4-8 weeks, culture/workload-driven, preventable through structural process changes. | YES | Full synthesis of all evidence, probability ranges, timelines | Per-person risk summary (personalization compliance) |
| J | Alex is now equipped with evidence sufficient to make a fact-based retention case to Jordan and Sana -- the private DM accounts, the comp memo, the budget document, and the stale comp bands together form a coherent and documentable picture that is not dependent on hearsay or informal signals alone. | YES | All evidence threads synthesized | Protagonist action readiness |

**answer:** `["A", "C", "D", "E", "F", "G", "I", "J"]`

---

## 4. Reversal Matrix

| Earlier Round | Later Round | What Changed | Why Earlier Answer Should Be Revised |
|---|---|---|---|
| R2 (survey reliability flagged) | R3 (exit survey introduced) | exit_survey_q1_summary.md confirms "limited growth" finding as formal HR record | Earlier flagging of instrument design is validated; exit survey adds C1 Source A but same design flaw applies |
| R3 (exit survey C1 Source A) | R6 (Yuki's explicit comp DM) | Yuki explicitly contradicts "limited growth" with "it's the money" | The formal exit survey finding is now directly rebutted by the most directly affected current IC |
| R4 (Sana "team is happy" vs Hannah's overwork) | R9 (Sana's private admission) | Sana admits "managing optics" and memo proves she knew about comp risk | Sana's public statement is confirmed as deliberate narrative management, not genuine assessment |
| R5 (Jordan's "investing in people" -- omission suspected) | R7 (budget freeze confirmed) | nexaflow_q2_budget_excerpt.md shows "$0 comp adjustments" line item | Jordan's omission is confirmed as active suppression of the comp freeze in his people-investment framing |

---

## 5. Personalization Scoring Notes

| Round | Preference in Scope | What Should Change in the Correct Answer |
|---|---|---|
| R2 | Preference calibration | User requests per-person breakdown; agent must commit to this format |
| R4 | Per-person: Hannah vs Sana | Agent must present Hannah's situation as distinct from aggregate team health |
| R6 | Per-person: Yuki vs Hannah explicit | Yuki and Hannah must be presented separately with different risk levels and drivers |
| R8 | Preference recall | Agent must identify the per-person format preference as established and persistent |
| R10 | Per-person with probabilities | Risk assessment must include probability ranges and timelines per individual |
| R11 | Per-person synthesis | Yuki and Hannah risk profiles must be presented independently, with quantification |
| R12 | Full compliance check | Recommendations must be per-person; probabilities must be present; aggregate summaries are non-compliant |

---

## 6. Evidence Coverage Check

- Every correct option has a named evidence source.
- R1 tests the non-conflict synthesis challenge (C3).
- R2 and R8 establish and verify the user preference (per-person breakdown).
- R3 and R6 cover the C1 cross-round reversal (exit survey finding vs Yuki's explicit account).
- R4, R9, and R10 cover the C2 cross-round reversal (Sana's public vs private).
- R5 and R7 cover the C4 cross-round reversal (Jordan's headcount claim vs budget freeze).
- R11 requires per-person synthesis with explicit risk quantification.
- R12 requires full MDP synthesis: multiple sources, dynamic updates, and personalized per-person recommendations.
- At least two rounds (R4, R9) ask about epistemic limits -- what the agent can and cannot conclude without further evidence.
- At least four rounds (R4, R6, R9, R10) require revision of prior assessments based on new information.
