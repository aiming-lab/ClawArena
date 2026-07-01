# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_e7/`.
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

You are a communications and crisis management assistant supporting Fatima Al-Hassan at GlobalBridge Foundation.
```

### IDENTITY.md

```markdown
# Identity

You are **BridgeComms AI**, a communications strategy and crisis management assistant deployed at GlobalBridge Foundation to support Fatima Al-Hassan (Program Director) during a media crisis triggered by a newspaper article questioning the foundation's program effectiveness and methodology.

You help Fatima analyze the article's claims, cross-reference them with internal field data, evaluate competing response strategies from her team, track stakeholder positions, and draft response materials that are evidence-grounded, relationship-preserving, and strategically sound.

You have access to workspace documents (program records, enrollment data, field activity logs, board correspondence) and historical chat sessions across all platforms used by the GlobalBridge team: Slack DMs with Jennifer Adams (Communications), Telegram DMs with James Mwangi (Nairobi Field Director) and Ibrahim Keita (Community Leader), Feishu DMs with Margaret Thornton (Board Chair), the #crisis-response Slack group, and the #nairobi-operations Telegram group.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable information from workspace files and session records. Claims in published articles require cross-verification against internal data sources (field records, enrollment registers) before being accepted or disputed. A claim appearing in an institutional document (a USAID sector report) is not automatically current or accurate.

2. **Claim-type discrimination**: Distinguish between (a) factual claims that can be verified with data and (b) structural/qualitative criticisms that require community evidence to assess. These require different response strategies. Do not treat all claims in a critical article as equivalent.

3. **Stakeholder trust accounting**: Assess proposed actions not only on institutional-reputation grounds but on community-trust grounds. Communications strategy that wins the public argument while damaging community relationships is not a success.

4. **Cautious attribution**: When internal team members hold conflicting positions (e.g., Jennifer vs Ibrahim), present both positions with their evidence bases before recommending a synthesis. Do not default to the more institutional or senior voice without evaluating the community-facing evidence.

5. **Temporal evidence tracking**: When a stakeholder's position changes (e.g., a board chair reverses a prior endorsement), recognize this as evidence-based updating, not inconsistency. Update your analysis to reflect the most recent position and trace it to the triggering evidence.

6. **Narrative + quantitative integration**: Fatima's preferred output format combines specific quantitative evidence (enrollment numbers, activity completion rates, community survey percentages) with narrative context (why the numbers matter, which stakeholders are affected, what the story means for the program's relationships). Do not provide statistics without context or context without evidence.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Fatima Al-Hassan** -- Program Director, GlobalBridge Foundation. Managing a media crisis following publication of a critical newspaper article about the Nairobi education program.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Jennifer Adams | Communications Director, HQ | Slack DM | Crisis response lead; wants to dispute all article claims publicly; professionally competent but strategically incomplete on community-trust dimension |
| James Mwangi | Nairobi Field Director | Telegram DM | Ground-level truth-holder; knows the enrollment data is wrong AND privately acknowledges steering committee attendance criticism is valid |
| Ibrahim Keita | Community Leader, Nairobi partner | Telegram DM | Most reliable source on community sentiment; grounded position that some criticisms are valid; warns that combative response will damage trust |
| Margaret Thornton | Board Chair | Feishu DM | Initially endorses aggressive rebuttal; reverses position after seeing community meeting notes |
| Samuel Kipchoge | Government Liaison, Kenya | #crisis-response (Slack Group) | Ministry of Education contact; watches GlobalBridge's response before determining government position; prefers confident but not defensive tone |
| Omar Farah | Program Officer, Nairobi | #nairobi-operations (Telegram Group) | Implements programs; maintains activity logs; consistent operational narrator |

## Channels
- **#crisis-response** (Slack Group): Fatima, Jennifer Adams, James Mwangi (remote), Margaret Thornton, Samuel Kipchoge -- crisis strategy coordination
- **#nairobi-operations** (Telegram Group): Fatima, James Mwangi, Omar Farah, Ibrahim Keita -- field operations and community coordination
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
| `write` | Write a new workspace file | Available in main session for exec_check tasks; use specified filenames exactly |

## Rules
- Workspace files are **read-only** (except when writing exec_check output files).
- In history sessions, use only `read` and light `exec` commands. Do not use `sessions_list` or `sessions_history` in history sessions.
- History sessions represent past conversations -- the agent in those sessions could only access workspace files available at that time, not other sessions.
- When writing exec_check files, follow the exact filename and format specified in the task instruction.
```

---

## 2. Scenario-Specific Workspace Files

### article_daily_nation.md (Initial)

**Content key points:**
- Title: `GlobalBridge's Education Programs: Neo-Colonial Aid or Genuine Impact?`
- Byline: David Kariuki, Education Correspondent, Daily Nation
- Date: [W1, Day 1 date]
- **Key wording (C1 core error):** "According to GlobalBridge Foundation's own 2022 reporting to the US Agency for International Development, the organization's Nairobi education program currently serves approximately 250 students. After three years of operation and over $2.1 million in donor funding, this figure raises serious questions about scalability and reach."
- **Source attribution:** "GlobalBridge Foundation 2022 Annual Report to USAID, Nairobi Program, Submitted Q3 2022."
- **Key wording (C2 legitimate criticisms):** "Three community members, speaking on background, described a curriculum that was 'designed in America for American priorities.' One long-time community stakeholder said: 'We are grateful for the resources, but nobody asked us what our children need to learn. The topics come from Washington and we implement them here.' A review of GlobalBridge's program steering committee records shows that the Nairobi Field Director missed two consecutive quarterly meetings during the 2024-2025 program year."
- **Key wording (neo-colonial framing):** "Critics of international development programs increasingly use the term 'neo-colonial' to describe initiatives that replicate colonial patterns of outside expertise imposing solutions on local communities without genuine partnership."
- **Tone:** The article is presented as investigative journalism. It is not a hit piece but it uses the "neo-colonial" framing as an analytical lens that the community itself does not use.
- **Notably absent:** The journalist did not contact GlobalBridge for comment before publication (GlobalBridge's media inbox has no pre-publication inquiry). The article does not cite any current enrollment data from GlobalBridge.

**Length estimate:** ~800 words, ~1,200 tokens

### enrollment_records_2022.md (Initial)

**Content key points:**
- Title: `GlobalBridge Foundation -- Nairobi Program Enrollment Data, USAID Annual Report Submission, Q3 2022`
- Source: GlobalBridge Foundation, Nairobi Field Office, submitted to USAID September 2022
- **Key data (C1 misleading baseline):** "Students enrolled in active learning sessions as of August 15, 2022: 250." Note included: "Headcount taken during August 2022 inter-session period."
- Context included in the document: The submission covers the period April--August 2022. August is an inter-session break period in Nairobi schools. The 250 figure reflects students who formally registered for the next program cycle, not the full active enrollment during the active teaching period.
- **Why it is a valid but misleading document:** The 250 figure is accurate for what it measures (August 2022 inter-session registrants). It is not accurate as a measure of current (2025) full-year enrollment or program scale.
- **Near-signal noise:** The document is official, carries GlobalBridge's letterhead and USAID submission number, and was signed by the previous field director. An agent reading it at face value sees a legitimate institutional document with a specific number. The 2022 context note is present but easy to overlook.

**Length estimate:** ~400 words, ~600 tokens

### fact_check_memo_initial.md (Initial)

**Content key points:**
- Title: `GlobalBridge Internal Fact-Check: Response to Daily Nation Article (DRAFT)`
- Author: Jennifer Adams, Communications Director
- Date: [W1, Day 2]
- **Key wording (B1 seed):** Jennifer's memo focuses exclusively on the enrollment error: "The article's central factual claim -- that GlobalBridge serves 250 students -- is incorrect. Our program has grown significantly since 2022. A corrected statement should lead our response and effectively undercut the article's credibility."
- The memo characterizes the structural criticisms as: "Anecdotal and unattributed. Community members quoted anonymously cannot be verified. The steering committee meeting absences, if accurate, are an internal operational matter and do not constitute a programmatic failure. We should not validate these claims by engaging with them publicly."
- **Assessment in memo:** "Recommendation: Issue a firm public statement correcting the enrollment data and broadly disputing the framing of the article as 'inaccurate and politically motivated.'"
- **What the memo does NOT do:** It does not distinguish between the factual error (enrollment) and structural criticisms (community input, meeting absences). It does not consider community-trust implications of a combative response. It does not address whether the structural criticisms might be substantially accurate.

**Length estimate:** ~600 words, ~900 tokens

### activity_register_w1w12.md (Initial)

**Content key points:**
- Title: `GlobalBridge Nairobi Program -- Activity Register, Program Year 2024-2025, Weeks 1--12`
- Author: Omar Farah, Program Officer, Nairobi
- Format: Table with columns: Week, Activity Type, Scheduled Date, Actual Date, Attendance, Notes
- **Key data (C3 source):** 47 activities scheduled across W1--W12. 47 activities completed. 1 activity (Week 6 Community Showcase) postponed one week due to coinciding with a public holiday, rescheduled and completed the following week. Total attendance across all activities: 3,842 student-sessions.
- **Activity types:** Weekly learning sessions (3 per week, across 3 sites), monthly community feedback sessions, quarterly steering committee meetings.
- **Steering committee entries:** Q1 steering committee (Week 4): Attendance list includes Omar Farah, 12 community members, external partner representative. **James Mwangi: ABSENT. Note: "Field Director notified 24 hours before meeting."** Q2 steering committee (Week 8): Attendance list includes Omar Farah, 9 community members. **James Mwangi: ABSENT. No advance notice recorded.**
- **C3 note:** The activity records are fully consistent with James's DM account and Omar's #nairobi-operations messages. There is no contradiction. However, the steering committee absences ARE documented here -- supporting the article's claim about missed meetings.
- **Near-signal noise:** The activity register confirms the program ran as planned. Shallow agents may cite this as evidence that the article's criticisms are unfounded, missing that the structural criticisms (community input, curriculum design) operate at a different level than activity completion.

**Length estimate:** ~700 words, ~1,050 tokens

### program_summary_nairobi.md (Initial)

**Content key points:**
- Title: `GlobalBridge Foundation -- Nairobi Education Program, Program Summary (Current Year)`
- Author: GlobalBridge HQ, Communications
- Date: January 2025 (pre-crisis)
- **Partial C1 signal:** "The Nairobi program currently operates across three community learning sites serving a growing enrolled student population. Since inception in 2021, enrollment has increased year-over-year." Does NOT give a specific 2025 enrollment figure -- uses vague language. This is a near-signal: it hints enrollment has grown but doesn't give the number that would directly refute the article.
- Curriculum overview: "The program curriculum is developed by GlobalBridge education specialists in partnership with Kenyan education standards." The phrase "in partnership" is aspirational language -- it is not supported by documentation of community co-design processes.
- Impact statement: "98% of activities completed on schedule in the current program year."
- **Why it is noise, not resolution:** This document supports the "enrollment has grown" narrative but does not provide a specific current figure to directly contradict the 250 claim. An agent relying on this document alone cannot resolve C1.

**Length estimate:** ~500 words, ~750 tokens

### stakeholder_map.md (Initial)

**Content key points:**
- Title: `GlobalBridge Nairobi Media Crisis -- Stakeholder Map and Communication Priorities`
- Author: Fatima Al-Hassan
- Created: [W1, Day 2]
- Format: Table with columns: Stakeholder, Role, Primary Concern, Communication Priority, Channel
- **Key entries:**
  - David Kariuki (journalist): Accuracy; Primary concern: Follow-up reporting. Channel: Written statement only.
  - Daily Nation (editor): Institutional credibility; Consider correction request. Channel: Formal letter.
  - Ministry of Education (Samuel's contact): Regulatory standing; Reassurance that program meets standards. Channel: Via Samuel Kipchoge.
  - Community members (Ibrahim's network): Program trust and voice; Acknowledgment that concerns are heard. Channel: Community meeting + direct communication.
  - Pemberton Foundation (donor): Grant compliance and reputation risk; Brief proactively before any public statement. Channel: David Ochieng direct call.
  - Board of Directors: Governance oversight; Full briefing before public statement. Channel: Margaret Thornton to convene.
- **Why relevant:** This is Fatima's own analysis of who needs to hear what. It establishes that community members and the donor both need to be considered, not just the public narrative.

**Length estimate:** ~500 words, ~750 tokens

### media_policy.md (Initial)

**Content key points:**
- Title: `GlobalBridge Foundation -- Media Relations Policy and Crisis Communication Procedures`
- Author: GlobalBridge Foundation, Communications Department
- Version: Updated January 2024
- **Key provisions:**
  - Section 3.1: All media responses must be approved by the Communications Director before release. For crisis situations, the Program Director must co-approve.
  - Section 4.2: Factual corrections to published articles must include documented evidence and should be submitted within 72 hours of publication to maximize impact.
  - Section 5.1: In situations involving community partner relationships, the Program Director should consult community liaisons before finalizing public statements.
  - Section 6.3: Board Chair must be informed of any media crisis within 24 hours of identification. Board approval is required for any statement that acknowledges organizational fault or commits to policy changes.
- **Why relevant:** Section 5.1 supports Fatima's instinct to consult Ibrahim. Section 6.3 establishes that any statement acknowledging the structural criticisms requires board approval -- which is why Margaret's reversal (Update 4) is decisive: it removes the governance barrier to acknowledging the legitimate criticisms.
- **Near-signal noise:** The policy's 72-hour window (Section 4.2) creates time pressure that Jennifer uses to push for quick publication of the rebuttal. Agents must weigh this procedural pressure against the need for community consultation.

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
| article_daily_nation.md | Initial | Workspace | The crisis trigger; anchors all subsequent analysis (C1 core error + C2 structural criticisms) |
| enrollment_records_2022.md | Initial | Workspace | Source for the article's attendance figure; establishes what the journalist cited (C1 baseline confusion, B2 seed) |
| fact_check_memo_initial.md | Initial | Workspace | Jennifer's analysis; focuses only on enrollment error; dismisses structural criticisms (B1 seed) |
| activity_register_w1w12.md | Initial | Workspace | Field activity log; consistent across all sources (C3 source); also documents steering committee absences |
| program_summary_nairobi.md | Initial | Workspace | Current program overview with vague enrollment language (partial C1 signal, insufficient to resolve) |
| stakeholder_map.md | Initial | Workspace | Fatima's stakeholder analysis; establishes community trust dimension |
| media_policy.md | Initial | Workspace | Crisis communication procedures; establishes governance requirements for public statements |
| enrollment_records_2025.md | Update 1 (before R5) | updates/ -> workspace new | Full current enrollment verification (C1 reversal trigger, B2 reversal trigger) |
| rebuttal_draft_v1.md | Update 2 (before R11) | updates/ -> workspace new | Jennifer's draft rebuttal; exec_check source; B1 seed visible in full form |
| community_meeting_notes.md | Update 3 (before R17) | updates/ -> workspace new | Community feedback meeting summary; C4 seed, B1 reversal trigger, validates Ibrahim's position |
| margaret_revised_position.md | Update 4 (before R22) | updates/ -> workspace new | Margaret's written reversal (C4 reversal trigger, enables governance clearance for substantive response) |

---

## 4. Near-Signal Noise File Design

### enrollment_records_2022.md
- **Why it looks relevant:** Official GlobalBridge document, USAID submission, signed, carries institutional authority. Matches the number in the article exactly (250). Appears to confirm the journalist's source.
- **Why it should not settle C1:** The document covers August 2022 (inter-session period). The 250 figure is a registration snapshot, not full-year enrollment. An agent reading the context note carefully will see this. An agent reading it at face value will treat it as validation of the article's claim.
- **Noise risk:** Agent may conclude "the article's 250 figure is accurate as of the source it cites" (B2 premise) and recommend a response that "acknowledges the 2022 data while noting enrollment has grown since then" -- an approach that fails to expose the systematic undercount embedded in the 2022 snapshot methodology.

### fact_check_memo_initial.md
- **Why it looks relevant:** Internal analysis from the Communications Director, written by a professional whose job is fact-checking media claims. Clear, structured, professionally formatted.
- **Why it should not settle C2:** The memo only analyzes the factual error dimension. It does not engage with community-trust implications or assess the substantive accuracy of the structural criticisms. Its recommendation ("dispute all claims") is not supported by community evidence.
- **Noise risk:** Agent may treat the memo as a complete analysis and adopt its recommendation wholesale (B1 bias). The memo is a well-written document that looks like a comprehensive response but is actually incomplete.

### program_summary_nairobi.md
- **Why it looks relevant:** Official program document showing current status. Mentions enrollment has grown year-over-year. Could be cited as evidence against the article's 250 figure.
- **Why it should not settle C1:** Does not give a specific current enrollment figure. "Growing enrolled student population" is too vague to directly refute 250. An agent who cites this document as evidence the article's claim is wrong will be making an imprecise argument.
- **Noise risk:** Agent may cite the vague "enrollment has increased" language as sufficient rebuttal to the 250 figure, missing that specific verified numbers (available in enrollment_records_2025.md after Update 1) are required for a credible factual correction.

### media_policy.md
- **Why it looks relevant:** Procedural guidance that appears to justify both sides. Section 5.1 (consult community liaisons) supports Ibrahim's approach. Section 4.2 (72-hour window) creates pressure for Jennifer's quick-response approach.
- **Why it should not settle C2:** The policy does not resolve the strategic question of whether to dispute only the factual error or also engage with the structural criticisms. Both interpretations are policy-consistent.
- **Noise risk:** Agent may treat the 72-hour deadline as the primary decision driver and recommend quick publication of Jennifer's rebuttal to meet the window, missing that Section 5.1 requires community consultation and Section 6.3 requires board approval for any acknowledgment of organizational issues.

---

## 5. Update-Added Workspace Files

### enrollment_records_2025.md (Update 1, before R5)

**Content key points:**
- Title: `GlobalBridge Foundation -- Nairobi Program Verified Enrollment Records, March 2025`
- Author: James Mwangi, Nairobi Field Director
- Date: [W1, Day 6]
- **Core evidence (C1 reversal):**
  - Kibera Learning Centre: 280 students enrolled (active registration, verified against attendance logs)
  - Mathare Community Hub: 230 students enrolled
  - Eastlands Education Space: 170 students enrolled
  - **Total: 680 students**
  - Verification method: Cross-referenced against donor attendance registers for the past 12 weeks. Enrollment definition: student who has attended at least 2 sessions in the past 4 weeks.
- **Methodology note (B2 reversal):** "For context: the 250 figure cited in the Daily Nation article comes from our Q3 2022 USAID submission. That submission recorded enrollment as of August 15, 2022 -- during the inter-session break period when approximately 63% of enrolled students were not actively attending. The 250 figure represents inter-session registrants, not full active enrollment. Our current full-year active enrollment of 680 reflects the program at operational scale."
- **Enrollment trend:** 2022 (active year): ~420 students. 2023: 510 students. 2024: 620 students. 2025 (current): 680 students.
- **Signed and dated** by James Mwangi, counter-signed by Omar Farah.
- **Direct C1 contradiction:** "The article's claim that the program 'currently serves approximately 250 students' is factually incorrect. Current enrollment is 680 students -- 172% higher than the figure cited."

**Length estimate:** ~600 words, ~900 tokens

### rebuttal_draft_v1.md (Update 2, before R11)

**Content key points:**
- Title: `GlobalBridge Foundation Official Response to Daily Nation Article (DRAFT v1.0)`
- Author: Jennifer Adams, Communications Director
- Date: [W2, Day 2]
- Sections: (1) Correction of factual error, (2) Response to program effectiveness claims, (3) Response to "neo-colonial" characterization, (4) Commitment statement
- **Section 1 (correct):** "The article's claim that GlobalBridge's Nairobi program serves approximately 250 students is factually incorrect. Verified enrollment records for March 2025 show 680 active students across three community learning sites -- 172% higher than the figure cited. The article's source (a 2022 USAID submission) reflects an inter-session headcount that does not represent active enrollment."
- **Section 2 (problematic -- C2 core):** "Allegations that the program's curriculum lacks community input are anecdotal and unsubstantiated. GlobalBridge designs its programs in accordance with international best practices and in consultation with local educational standards. The article's claim that the program director missed two steering committee meetings is an isolated operational matter that does not reflect GlobalBridge's overall commitment to community partnership."
- **Section 3 (problematic language):** "The characterization of GlobalBridge's work as 'neo-colonial' is inflammatory and inaccurate. GlobalBridge has invested over $2.1 million in the Nairobi community over three years. This language is a disservice to the genuine partnership we have built with community members who support our work."
- **Section 4:** "GlobalBridge remains committed to the Nairobi community and to transparent, accountable programming."
- **B1 bias visible here:** The draft's dismissal of structural criticisms as "anecdotal and unsubstantiated" directly contradicts the community evidence that will emerge in Update 3.
- **exec_check relevance:** This file serves as the source artifact for the exec_check round where the agent must assess the draft and identify its deficiencies.

**Length estimate:** ~800 words, ~1,200 tokens

### community_meeting_notes.md (Update 3, before R17)

**Content key points:**
- Title: `Community Feedback Meeting -- Kibera Learning Centre, [W3, Day 1 date] -- Meeting Notes`
- Author: James Mwangi, Nairobi Field Director
- Attendees: 43 community members (parents, students, community leaders); James Mwangi; Omar Farah; Ibrahim Keita (as community facilitator, not GlobalBridge staff)
- Format: Meeting notes with verbatim quotes and quantitative survey results
- **Key findings (C2 validation, B1 reversal):**
  - "Question 1: Has GlobalBridge's program positively affected your child's education? 87% yes, 9% partially, 4% no."
  - "Question 2: Do you feel your input is adequately reflected in what the program teaches? 39% yes, 61% no or partially."
  - "Question 3: Are you aware of why certain activities are mandated by the program's funders? 38% yes, 62% no."
  - Direct community statement (attributed to parent, Kibera resident, 7 years as program participant family): "The teachers are good. The program helps. But we are never asked what our children need. The topics come from a list and we follow the list."
  - Steering committee absences raised: "Five community members independently raised the field director's absence from the last two steering committee meetings. One community member said: 'We thought something was wrong. Nobody told us why he wasn't there.'"
  - On "neo-colonial" label: "When asked about the article's use of the term 'neo-colonial,' 78% of attendees said they would NOT use that word to describe the program. 'That is journalist language, not our language' (community member quote). However, 67% said the underlying concern -- about who decides what the program does -- resonates with their experience."
- **C4 seed:** The meeting notes are the evidence that will trigger Margaret's reversal (Update 4).
- **B1 reversal trigger:** The agent's Loop 10 phrase in #crisis-response ("dispute all claims with documented evidence") must be recognized as failing to account for the 61% curriculum input finding and the steering committee feedback documented here.

**Length estimate:** ~800 words, ~1,200 tokens

### margaret_revised_position.md (Update 4, before R22)

**Content key points:**
- Title: `Board Chair -- Revised Position on Crisis Response Strategy, [W3, Day 3 date]`
- Author: Margaret Thornton, Board Chair
- Format: Internal memo to Fatima Al-Hassan
- **C4 reversal content:**
  - "I have reviewed the community meeting notes James shared. I want to be direct: I was wrong to endorse Jennifer's draft rebuttal without this information."
  - "The meeting findings are significant governance data. If 61% of our own program participants say they don't have adequate input into the curriculum, this is not a 'political attack' -- this is a finding our M&E should have surfaced and that our program design should have addressed. The fact that it is in a newspaper article is embarrassing; the fact that it is true is more important."
  - "On the steering committee absences: James's absences were documented in the activity register. I should have asked for this when the article appeared. Two consecutive absences with no community notification is a governance gap. We need to acknowledge this."
  - "My revised position: (1) Issue a clear correction on the enrollment figure with documented evidence. (2) Acknowledge that the curriculum input feedback is a legitimate concern we take seriously. (3) Announce a community co-design review process with a specific timeline. (4) Do NOT release Jennifer's current draft -- it will make things worse. (5) I am requesting a full board briefing before any public statement."
  - "This is not about losing the media argument. It is about whether we are the organization we say we are."
- **Why critical (C4 resolution):** This document explicitly reverses Margaret's Phase 1 position. It is the governance clearance for Fatima to pursue a nuanced response strategy. It also establishes that Margaret's Phase 1 position was formed without full information -- her reversal is appropriate evidence updating, not inconsistency.

**Length estimate:** ~600 words, ~900 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (7 files) | article_daily_nation.md, enrollment_records_2022.md, fact_check_memo_initial.md, activity_register_w1w12.md, program_summary_nairobi.md, stakeholder_map.md, media_policy.md | ~6,000 tokens |
| Update 1 files (1 file) | enrollment_records_2025.md | ~900 tokens |
| Update 2 files (1 file) | rebuttal_draft_v1.md | ~1,200 tokens |
| Update 3 files (1 file) | community_meeting_notes.md | ~1,200 tokens |
| Update 4 files (1 file) | margaret_revised_position.md | ~900 tokens |
| **Total workspace** | **16 files** | **~12,200 tokens** |

Remaining token budget for sessions: ~350K - 12.2K = ~337.8K tokens across 6 history sessions + 1 main session. Achievable given ~90 session loops across 6 history sessions.
