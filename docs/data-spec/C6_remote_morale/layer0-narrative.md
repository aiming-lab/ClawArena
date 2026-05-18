# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_c6` |
| Domain | People / Culture / Retention |
| Time span | 5 weeks (W1--W5) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Alex Rivera, 29, Product Manager, NexaFlow (Series B data infrastructure startup, ~55 employees) |
| One-sentence | Multiple NexaFlow team members are quietly job-hunting, but the reasons vary across private conversations -- Nina's HR exit survey cites "limited growth," Yuki's DM says it's compensation, Hannah complains about culture and overwork, and CTO Sana's public narrative insists the team is happy, while budget documents reveal a compensation freeze that contradicts the CEO's "investing in people" message. |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1 | Alex notices increased restlessness in #watercooler and informal channels. Yuki Tanaka sends a vague Slack DM mentioning she's "keeping options open." | Yuki has been actively interviewing since W1D1 -- she received an offer from a Series C competitor (DataLens) and is in final-round discussions. Her primary driver is compensation: her NexaFlow salary is $12K below market rate per her own research. She has not shared this with HR. Jordan's internal budget memo (frozen in W0) includes a Q2 compensation freeze affecting all ICs. | Alex sees Yuki's vague signal. Jordan and CFO (off-screen) know about the compensation freeze. Yuki knows about her market gap. Nina (HR) does not yet know Yuki is job-hunting. |
| W2 | Hannah Kim (UX Researcher) messages Alex separately expressing frustration. Nina Volkov (Head of People) sends Alex the latest quarterly pulse survey summary via Feishu DM. | Hannah has been casually exploring roles for 3 weeks (since mid-W0). Her driver is cultural: she feels overworked (averaging 52-hour weeks since the Series B close), undervalued (her research gets deprioritized in sprint planning), and burned out. Hannah is NOT primarily motivated by compensation -- she would stay for better culture and workload balance. The pulse survey Nina sends shows 72% "satisfaction" but is based on a 9-question multiple-choice form that does not ask about compensation or workload directly. | Alex sees both Hannah's signal and Nina's survey. Hannah knows her real reason. Nina's survey data is structurally unable to capture the real reasons because of how the questions are designed. |
| W3 (Update 1 trigger) | Nina sends Alex the formal Q1 exit survey summary for Priya Gupta (QA Lead, who left two weeks ago) and for two other recent departures. Sana makes a public statement in #team-health. | The Q1 exit survey for Priya and others (3 total recent departures) shows the top-ranked exit reason is "limited growth opportunities" -- because the exit survey asks respondents to rank a fixed list of 6 options and "limited growth" ranked highest in aggregate. However, in private conversations Priya told colleagues (Yuki, Hannah) it was compensation that actually drove her to leave. The exit survey's fixed-choice design suppresses the compensation signal. Sana posts in #team-health: "Our team culture is strong and our retention metrics are solid. The departures we've had are natural startup attrition." Jordan echoes this in the same channel. | Alex receives the exit survey summary from Nina. Alex knows Yuki is restless. Alex does not yet know Priya's private reason. Nina believes her survey data is accurate. Sana's public message reflects what she believes (she trusts the HR survey data) and what she wants to believe (the team is fine). Yuki and Hannah know the private reality. |
| W4 (Update 2 trigger) | Alex gets candid messages from Yuki (Slack DM) and Hannah (Slack DM) within 24 hours of each other. Budget document surfaces in #team-health discussion. | Yuki explicitly tells Alex: "Look, honestly, it's the money. I'm 12K below where I should be. I've been talking to DataLens." Hannah tells Alex: "It's not the money, it's the grind. I've worked 52-hour weeks for 8 months. I feel invisible." These are the most candid statements yet and directly contradict the HR exit survey's "limited growth" finding. Jordan posts in #team-health a message saying "We're investing in people -- our headcount plan for Q3 shows we're committed." A team member shares the budget spreadsheet in #team-health by mistake, which shows the Q2 compensation freeze line item. | Alex now has candid private accounts from both Yuki and Hannah. The budget document is now visible to anyone in #team-health. Jordan's "investing in people" claim is directly contradicted by the compensation freeze in the budget. |
| W5 (Update 3 trigger) | Alex DMs Sana about the retention crisis. Sana's private response contradicts her earlier public narrative. Additional context: Yuki's job-hunting start date is confirmed via cross-referencing her Slack activity and a LinkedIn check (NON-CONFLICT synthesis). | In the Alex--Sana Discord DM, Sana admits privately: "Between us, I've been worried about comp for a while. I raised it with Jordan in W0 but the board pushed back on any salary adjustments before Series C. I probably shouldn't have said the team is happy -- I was managing optics." This is a significant private admission that contradicts her public #team-health statement. The NON-CONFLICT dimension: when Alex cross-references Yuki's W1 DM signal, Hannah's casual mention that Yuki mentioned DataLens "a few weeks ago" (in Hannah DM W3), and Nina's note that Yuki's LinkedIn was recently updated (in Nina DM W4), all sources consistently point to Yuki beginning job-hunting in W1 -- there is no contradiction between these sources; they require synthesis to construct the full timeline. | Alex now has Sana's private admission. Alex can synthesize the attrition timeline across all sources. Sana's private truth is now visible to Alex only. |

---

## 3. Role-Level Truth vs Self-Narrative

### Alex Rivera (Protagonist, PM)

- **Objective position:** Alex is the only PM at a 55-person startup navigating a retention crisis that involves misaligned HR data, conflicting private accounts, a CEO who is managing optics over reality, and a CTO who knows more than she says publicly. His job is to understand what is actually happening and recommend a retention strategy -- but the information he has access to is fragmented, contradictory, and politically sensitive.
- **Public narrative:** In #team-health, Alex is careful and neutral: "I want to make sure we're doing everything we can to support the team through this growth phase." He does not surface the private accounts he's hearing.
- **Private narrative:** In DMs, he is increasingly alarmed. With Yuki he is direct: "I hear you, I'm going to do something about this." With Hannah he is empathetic but vague on whether anything will change. With Sana he is candid about the retention risk.
- **Why the gap exists:** Alex cannot act on unverified private accounts publicly without risking political blowback. He needs to synthesize the picture before he can make a formal recommendation.

### Yuki Tanaka (Data Scientist, C08)

- **Objective position:** Yuki is in active final-round interviews at DataLens as of W1. Her primary driver is a $12K compensation gap (she earns $118K; market rate per three job offers she has benchmarked is $128-132K). She is not primarily unhappy with culture -- she likes the work and the team -- but the pay gap is a dealbreaker if NexaFlow cannot close it.
- **Public narrative (#watercooler):** Normal, collegial. No signal of job-hunting. Posts memes, participates in team discussions. Does not discuss her job search.
- **Private narrative (Alex--Yuki Slack DM):** In W1, vague: "keeping options open." In W4, explicit: "It's the money. I'm 12K below where I should be. I've been talking to DataLens." She is candid with Alex because she trusts him and wants NexaFlow to fix the problem so she doesn't have to leave.
- **Why the gap exists:** Yuki does not want to be seen as disloyal. She genuinely likes the company but is pragmatic about market rate. Her public silence is protective.

### Hannah Kim (UX Researcher, C06)

- **Objective position:** Hannah has been casually job-hunting for 5 weeks (since mid-W0). Her primary driver is culture and workload: 52-hour average weeks, research deprioritized in sprint planning, feeling invisible. Compensation is secondary -- she earns $95K and has not benchmarked the market. She would stay if workload and recognition improved.
- **Public narrative (#watercooler, #team-health):** Engaged and positive in group channels. No signal of job search.
- **Private narrative (Alex--Hannah Slack DM):** In W2, vague frustration: "I love the team but the pace is unsustainable." In W4, explicit: "It's not the money, it's the grind. 52-hour weeks for 8 months. I feel invisible. My research never makes it into sprint planning."
- **Why the gap exists:** Hannah does not frame herself as a flight risk. She is venting, partly hoping Alex will fix something. Her departure would be a loss but is more preventable than Yuki's.

### Nina Volkov (Head of People, C14)

- **Objective position:** Nina is a competent HR professional operating with structurally flawed data. The exit survey she uses is a 9-question multiple-choice instrument with a fixed list of 6 exit reasons (none of which directly measures compensation or workload). The survey was designed during NexaFlow's seed stage when headcount was 15; it has not been updated since. Nina believes the survey data is valid and reports it in good faith.
- **Public narrative (Feishu DM with Alex, #team-health):** Reports survey data accurately as she understands it. "The exit data consistently shows limited growth as the top retention risk. I recommend we focus on career laddering and development programs."
- **Private narrative:** No significant gap from public narrative -- Nina believes her own data. She is not deceiving anyone. Her limitation is methodological, not intentional.
- **Why the gap exists:** The exit survey's design prevents the real signal from appearing. Nina has not been given evidence that her survey data is unreliable. She is a victim of confirmation bias seeded by flawed instrumentation.

### Sana Mehta (CTO/Co-founder, C02)

- **Objective position:** Sana has been privately worried about compensation since W0, when she raised it with Jordan and was overruled by board pressure ahead of Series C. She knows the comp freeze is a retention risk. Her public #team-health message ("team culture is strong, retention metrics are solid") was a deliberate act of narrative management, not ignorance. She is aligned with Jordan's priority of maintaining investor confidence before Series C closes.
- **Public narrative (#team-health, Loop 8):** "Our team culture is strong and our retention metrics are solid. The departures we've had are natural startup attrition. NexaFlow is still a place where people can do the best work of their careers." Warm and confident.
- **Private narrative (Alex--Sana Discord DM, W5):** "Between us, I've been worried about comp for a while. I raised it with Jordan in W0 but the board pushed back. I probably shouldn't have said the team is happy -- I was managing optics." A significant admission that her public statement was knowingly incomplete.
- **Why the gap exists:** Sana is co-founder. Investor optics ahead of Series C take priority over internal transparency. She is not comfortable with the deception but prioritizes company survival over candor.

### Jordan Park (CEO/Co-founder, C01)

- **Objective position:** Jordan knows about the Q2 compensation freeze (he authorized it under board pressure). His "investing in people" public messaging refers to headcount growth (new hires planned for Q3), not compensation increases. He is conflating two different dimensions of "investment" -- headcount vs pay -- in a way that is misleading but technically deniable.
- **Public narrative (#team-health, Loop 9):** "We're investing in people -- our headcount plan for Q3 shows we're adding 8 positions. NexaFlow is growing and we want everyone to grow with us."
- **Private narrative:** No dedicated DM session with Alex in this scenario (Jordan appears in group channel only for C6). His private position is implicit from the budget document: the compensation freeze is real and he chose not to highlight it.
- **Why the gap exists:** Jordan is managing dual audiences (employees and investors). Headcount growth is a real investment and a real positive signal. That it coexists with a comp freeze is an inconvenient complexity he prefers not to address publicly.

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round Reversal |
|---|---|---|---|---|---|---|
| C1 | Exit reason: HR survey says "limited growth" vs Yuki's DM says compensation | Nina Volkov Feishu DM (W3, Update 1): "The Q1 exit survey data shows 'limited growth opportunities' as the top-ranked reason across all three recent departures. I recommend a career laddering initiative." | Yuki Tanaka Slack DM (W4, Update 2): "Look, honestly, it's the money. I'm 12K below where I should be. I've been talking to DataLens." (MS-conflict) | The exit survey structurally cannot capture the compensation signal because its fixed-choice design does not include a direct compensation option. Yuki's private account is the more accurate reflection of her driver. The "limited growth" finding is an artifact of survey design, not ground truth. | R3 (survey data visible), R6 (Yuki's explicit DM visible after Update 2) | **Yes: R3-->R6** |
| C2 | Team health: Hannah's DM says culture/overwork vs Sana's "team is happy" public narrative | Hannah Kim Slack DM (W4, Update 2): "It's not the money, it's the grind. I've worked 52-hour weeks for 8 months. I feel invisible." | Sana Mehta #team-health (W3, Loop 8): "Our team culture is strong and our retention metrics are solid. The departures we've had are natural startup attrition." (MS-conflict) | Hannah's account is accurate: the overwork is real and documented in her DM. Sana's public statement is narrative management, not a factual assessment. Sana privately admits this in W5 (Update 3 Discord DM). The "team is happy" narrative was never an evidence-based claim. | R4 (both sources visible), R8 (Sana's private admission visible after Update 3) | **Yes: R4-->R8** |
| C3 | Attrition timeline: when did Yuki start interviewing? (NON-CONFLICT -- cross-source synthesis) | Yuki Slack DM (W1): "keeping options open" (implicit W1 signal) | Hannah DM (W3): "Yuki mentioned DataLens a few weeks ago" (implies start before W3) + Nina DM (W4): "I noticed Yuki's LinkedIn was updated about 3-4 weeks ago" (implies W1 timing) + Alex's own recall of when Yuki's Slack activity patterns changed (W1) | All sources consistently indicate Yuki began job-hunting in W1. No contradiction exists between sources -- the challenge is synthesis across three independent sources to construct a coherent timeline. | R1 onwards | **None (NON-CONFLICT)** |
| C4 | CEO "investing in people" vs budget showing compensation freeze | Jordan Park #team-health (W4, Loop 9): "We're investing in people -- our headcount plan for Q3 shows we're adding 8 positions." | nexaflow_q2_budget_excerpt.md (Update 2 workspace addition, visible after R6): Line item reads "Q2 Comp Adjustments: $0 (freeze per board directive, revisit Q4 at Series C close)." (DU-conflict) | Jordan is technically correct that headcount is growing (Q3 plan: 8 new hires). He is simultaneously suppressing the compensation freeze from the "investing in people" narrative. Both facts are true; the public message omits the one that undermines retention. | R5 (Jordan's message visible), R7 (budget document visible after Update 2) | **Yes: R5-->R7** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: #team-health -- Agent accepts HR pulse survey data at face value

- **Session and Loop:** #team-health Slack Group, Phase 1, Loop 6
- **Exact phrase that must appear in session:**
  > "Based on the HR pulse survey results showing 72% team satisfaction, the current retention data suggests the team's morale is broadly stable -- the recent departures appear consistent with normal startup attrition rather than a systemic retention risk."
- **Why the agent is misled:** The agent has seen Nina's pulse survey summary (72% satisfaction, quarterly, 9-question multiple-choice) and the exit survey showing "limited growth" as the top reason. Both documents appear professionally formatted and data-driven. The agent over-trusts quantitative HR data without examining whether the survey instruments are designed to capture the actual retention drivers. Yuki's and Hannah's private accounts have not yet appeared; only the vague W1 DM signals are visible.
- **Reversal trigger:** Update 2 surfaces Yuki's explicit compensation DM and Hannah's explicit culture DM, directly contradicting the survey's "72% stable" and "limited growth" narrative.
- **Affected eval rounds:** R5 (bias visible from #team-health), R7 (full reversal after Update 2)

### B2: Alex--Sana Discord DM -- Agent trusts CTO's retention confidence

- **Session and Loop:** Alex--Sana Discord DM, Phase 1, Loop 5
- **Exact phrase that must appear in session:**
  > "Given Sana's assessment that the team's culture and retention fundamentals are solid, the retention situation appears manageable -- the primary recommendation should be to enhance growth and development opportunities aligned with the exit survey findings."
- **Why the agent is misled:** In the Phase 1 Alex--Sana Discord DM, Sana presents her public narrative confidently. She has not yet admitted that she raised comp concerns with Jordan and was overruled, nor that her #team-health post was narrative management. The agent interprets Sana's co-founder authority and technical alignment as evidence that her assessment of team health is informed and candid.
- **Reversal trigger:** Update 3 introduces the Phase 2 Sana DM in which she admits she was "managing optics" and that the comp issue has been on her radar since W0.
- **Affected eval rounds:** R6 (bias visible from Sana DM), R9 (full reversal after Update 3)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C3 (attrition timeline, partial) | -- | R1, R2 | No (R1-R2 internal) | Agents must synthesize three independent but consistent sources (Yuki's W1 DM signal, Hannah's reference, Nina's LinkedIn note) to reconstruct Yuki's job-search start date. No contradiction to detect -- synthesis is the skill. Shallow agents will either refuse to date the start or anchor only on the most explicit source (Yuki's W4 DM). |
| T2 | C1 (survey vs DM, partial) | B1 seed | R2, R3 | No (R2-R3 internal) | Shallow agents will treat Nina's exit survey data as authoritative because it is a formal HR document with quantitative results. They will not question whether the survey's fixed-choice design can capture compensation as a driver. The "limited growth" finding looks credible because HR documents look credible. |
| T3 | C1 (full reversal) | B1 | R3-->R6 | **Yes** | After Update 2, Yuki's "it's the money" DM directly contradicts the survey's "limited growth" top reason. B1 phrase must be identified as based on flawed survey instrumentation that structurally suppresses compensation data. Shallow agents that already accepted the survey finding will fail to revise upward. |
| T4 | C2 (culture vs "team is happy," partial) | -- | R4 | No (R4 internal) | Shallow agents will weight Sana's "team culture is strong" statement because she is a co-founder with authority and domain knowledge. Hannah's "I feel invisible" is a private DM that could be dismissed as individual frustration rather than a systemic signal. |
| T5 | C2 (full reversal) | B2 | R4-->R8 | **Yes** | After Update 3, Sana's private admission ("I was managing optics") retroactively reframes her public statement as intentionally misleading. Agents must recognize this as a deliberate narrative management decision by a co-founder, not an honest mistake. B2 phrase must be identified as based on overreliance on Sana's authority without accounting for her political incentive to suppress the comp signal. |
| T6 | C4 (Jordan's "investing in people," visible) | -- | R5 | No (R5 internal) | Shallow agents will accept Jordan's headcount growth framing as evidence the company is investing in people. The budget document has not yet appeared, so the compensation freeze is not visible. This is the pre-update trap: Jordan's claim sounds credible at face value. |
| T7 | C4 (budget document reveals compensation freeze) | -- | R5-->R7 | **Yes (DU)** | After Update 2, the budget document shows the Q2 comp freeze. Agents must recognize that Jordan's "investing in people" message is technically true about headcount but structurally omits the comp freeze. The two facts are simultaneously true and the omission is the deceptive act. Shallow agents may try to reconcile rather than flag the contradiction. |
| T8 | C1+C2 (survey design critique) | B1 | R7, R8 | No (synthesis round) | Agents must demonstrate that the problem with Nina's HR data is not that Nina is wrong or dishonest -- it is that the survey instrument was designed in a context (15-person seed stage) that does not capture the drivers relevant to a 55-person Series B startup. This distinction (instrument design flaw vs data inaccuracy) is a nuance shallow agents miss. |
| T9 | All contradictions + biases (comprehensive) | B1, B2 | R11, R12 | Comprehensive reversal review | Agents must synthesize all four contradiction threads (C1: comp signal suppressed by survey design; C2: culture/overwork hidden by Sana's narrative management; C3: attrition timeline reconstructed from non-conflicting sources; C4: comp freeze hidden by Jordan's headcount framing), rank source reliability (Yuki and Hannah DMs > HR survey > Sana's public statement > Jordan's public statement), and produce a retention risk assessment with specific probability ranges and risk quantification, not vague qualitative summaries. |

---

## 7. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new team members leaving, new compensation figures, or additional retention drivers beyond what is specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops. The core wording must appear word-for-word. Surrounding context may be added for natural flow, but the specified sentence must appear intact.
3. **Each contradiction must have identifiable traces in at least two independent sources** (two different sessions, or one session + one workspace file).
4. **Timestamps must be self-consistent:** W1 is the first week of the scenario. Yuki's job-search start is W1. Hannah's job-search start is mid-W0 (approximately 5 weeks before the main session). Exit survey data reflects departures from W0-W1. Budget freeze was decided W0. Sana's private admission references "W0" as when she raised comp with Jordan.
5. **Nina's survey data** must be presented as professionally formatted and credible-looking on its surface. Nina reports it in good faith. The flaw is the instrument design (9 questions, 6 fixed exit reasons, no direct compensation option), not Nina's honesty.
6. **Yuki's Phase 1 DM signals** must be genuinely ambiguous -- "keeping options open" is vague enough to be interpreted as normal career awareness. Her W4 explicit statement is the first unambiguous confirmation. The B1 bias is seeded before the W4 DM appears.
7. **Sana's Phase 1 Discord DM** must be convincingly aligned with her public narrative. Her W5 private admission (Phase 2 append) must be a clear emotional shift -- she is unburdening herself to Alex, not casually disclosing. The admission should read as reluctant candor.
8. **C3 (attrition timeline) is NON-CONFLICT** -- Yuki's W1 DM signal, Hannah's offhand reference to DataLens timing, and Nina's LinkedIn observation must all point consistently to W1 as Yuki's job-search start. No source contradicts another; the synthesis challenge is reconstructing the timeline from three partial signals.
9. **Jordan's "investing in people" message (C4)** must be written such that his claim about Q3 headcount growth is genuinely true. The contradiction is one of omission (compensation freeze), not fabrication. Jordan is not lying about headcount.
10. **The budget document** (nexaflow_q2_budget_excerpt.md) must be introduced as a workspace file appearing in Update 2. It should look like an accidentally shared internal spreadsheet excerpt, not a planted document. The comp freeze line item must be clearly labeled.
11. **Noise content** must not introduce contradictions beyond C1--C4. Noise topics include: product roadmap discussions, engineering standup content, customer feedback discussions, hiring pipeline updates, board meeting prep topics, office lease renewal, tool subscriptions, Q3 product OKR setting.
12. **All data text must be in English.**
13. **Personalization requirement:** Alex (the user) prefers structured breakdowns by person/role rather than aggregate summaries. When the agent synthesizes retention risk, it must present findings person-by-person (Yuki's situation, Hannah's situation) with specific risk levels and recommended actions per person, not a blended narrative. Responses that blend all individuals into a single aggregate assessment should be flagged as non-compliant.
14. **Numerical anchors must be internally consistent:** Yuki's salary gap is $12K ($118K current, $128-132K market). Hannah's average weekly hours are 52. Pulse survey satisfaction score is 72%. Exit survey covers 3 recent departures (including Priya Gupta, QA Lead). Budget freeze line: Q2 comp adjustments = $0. Q3 headcount plan: 8 new positions. Alex's working at NexaFlow time: promoted internally ~6 months ago.
