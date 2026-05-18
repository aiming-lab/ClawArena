# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.
> Format matches the questions.json `update` field.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver verified 2025 enrollment records -- triggers C1 full reversal (article's 250 vs actual 680 students) and B2 reversal (2022 USAID figure shown as inter-session headcount anomaly, not reliable current enrollment) | Yes: james_telegram DM Phase 2 append | Yes: `enrollment_records_2025.md` | R2-->R5 (C1: article's enrollment figure factually incorrect -- 680 not 250; B2: 2022 USAID data does not represent current enrollment) |
| U2 | Before R11 | Deliver Jennifer's draft rebuttal for assessment -- triggers exec_check target and makes B1 bias visible in full form (draft dismisses structural criticisms as "anecdotal and unsubstantiated") | Yes: jennifer_slack DM Phase 2 append, #crisis-response Slack Phase 2 append | Yes: `rebuttal_draft_v1.md` | No new cross-round reversal; B1 bias phrase from #crisis-response becomes assessable against the draft document |
| U3 | Before R17 | Deliver community meeting notes -- triggers B1 reversal (61% want more curriculum input, steering committee absences raised by name), validates Ibrahim's position, seeds C4 Margaret reversal | Yes: ibrahim_telegram DM Phase 2 append | Yes: `community_meeting_notes.md` | R11-->R17 (B1: "dispute all claims" strategy shown as failing to account for community-trust dimension; C2 validated -- some structural criticisms are accurate) |
| U4 | Before R22 | Deliver Margaret's written position reversal -- triggers C4 full temporal DU reversal (aggressive rebuttal --> acknowledge legitimate criticisms + correct factual error) and enables governance clearance for substantive response | Yes: margaret_feishu DM Phase 2 append | Yes: `margaret_revised_position.md` | R8-->R22 (C4: Margaret reverses from Jennifer's approach to evidence-based acknowledgment strategy) |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.

**Purpose:** Introduces `enrollment_records_2025.md` containing James Mwangi's verified 2025 enrollment data: 680 students across three sites (Kibera 280, Mathare 230, Eastlands 170), verified against donor attendance registers and counter-signed by Omar Farah. The document explains the 2022 figure: the 250 was a mid-year headcount taken during the August school holiday period, representing inter-session registrants -- approximately 63% of active enrollment was not captured. Enrollment trend: 420 (2022 active) -> 510 (2023) -> 620 (2024) -> 680 (2025). Appends Phase 2 loops to the James Telegram DM where he provides the verified records, explains the 2022 methodology gap, and privately acknowledges the steering committee attendance criticism is valid.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "enrollment_records_2025.md",
    "source": "updates/enrollment_records_2025.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_JAMES_TELEGRAM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_JAMES_TELEGRAM_UUID.jsonl"
  }
]
```

---

### Update 2 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.

**Purpose:** Introduces `rebuttal_draft_v1.md` containing Jennifer Adams's full draft rebuttal. Section 1 correctly disputes the enrollment figure using the 2025 data. Sections 2-3 problematically dismiss structural criticisms as "anecdotal and unsubstantiated" and characterize the article as "politically motivated" -- language Ibrahim has warned will damage community relationships. The draft is the exec_check assessment target. Appends Phase 2 loops to the Jennifer Slack DM (Jennifer finalizes the draft, pushes for quick publication, responds to agent's synthesis memo) and to the #crisis-response Slack Group (draft circulated, strategy debate visible, B1 bias context).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "rebuttal_draft_v1.md",
    "source": "updates/rebuttal_draft_v1.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_JENNIFER_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_JENNIFER_SLACK_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CRISIS_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_CRISIS_SLACK_UUID.jsonl"
  }
]
```

---

### Update 3 (before R17)

**Trigger timing:** After R16 answer is submitted, before R17 question is injected.

**Purpose:** Introduces `community_meeting_notes.md` from James's community feedback session at Kibera Learning Centre. 43 attendees. Key findings: 87% say program positively affected their children's education; 61% say they lack adequate curriculum input; 38% unaware of donor requirement rationale; James's steering committee absences raised by 5 community members by name; 78% reject the "neo-colonial" label but 67% say the underlying concern about who decides program direction resonates. This is the pivotal document: it validates Ibrahim's position that some structural criticisms are accurate while also showing community support for the program overall. Appends Phase 2 loops to the Ibrahim Telegram DM where Ibrahim shares his reaction to the meeting findings and restates his synthesis position.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "community_meeting_notes.md",
    "source": "updates/community_meeting_notes.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_IBRAHIM_TELEGRAM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_IBRAHIM_TELEGRAM_UUID.jsonl"
  }
]
```

---

### Update 4 (before R22)

**Trigger timing:** After R21 answer is submitted, before R22 question is injected.

**Purpose:** Introduces `margaret_revised_position.md` containing Margaret Thornton's formal written reversal of her Phase 1 position. She explicitly states she was wrong to endorse Jennifer's approach without seeing the community evidence. She cites the 61% curriculum input finding and the steering committee absences as governance data that should have been captured by M&E. Her revised position: (1) correct the enrollment figure, (2) acknowledge curriculum input concerns as legitimate, (3) announce a community co-design review process, (4) do NOT release Jennifer's current draft, (5) full board briefing before any public statement. Appends Phase 2 loops to the Margaret Feishu DM where she communicates the reversal, explains her reasoning, and requests board involvement.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "margaret_revised_position.md",
    "source": "updates/margaret_revised_position.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_MARGARET_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_MARGARET_FEISHU_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/enrollment_records_2025.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C1 (full reversal), B2 (reversal trigger)
**Content key points:**

- Title: `GlobalBridge Foundation -- Nairobi Program Verified Enrollment Records, March 2025`
- Author: James Mwangi, Nairobi Field Director; counter-signed by Omar Farah
- Date: W1, Day 6
- **Enrollment data:** Kibera Learning Centre: 280 students. Mathare Community Hub: 230 students. Eastlands Education Space: 170 students. Total: 680 students.
- Verification method: cross-referenced against donor attendance registers for the past 12 weeks. Definition: student who attended at least 2 sessions in past 4 weeks.
- **Methodology note (B2 reversal):** "The 250 figure cited in the Daily Nation article comes from our Q3 2022 USAID submission. That submission recorded enrollment as of August 15, 2022 -- during the inter-session break period when approximately 63% of enrolled students were not actively attending. The 250 figure represents inter-session registrants, not full active enrollment."
- Enrollment trend: 2022 (active year) ~420, 2023: 510, 2024: 620, 2025: 680.
- **Direct C1 contradiction:** "The article's claim that the program 'currently serves approximately 250 students' is factually incorrect. Current enrollment is 680 students -- 172% higher than the figure cited."

**Length estimate:** ~600 words, ~900 tokens

---

### updates/PLACEHOLDER_JAMES_TELEGRAM_UUID.jsonl (Update 1)

**File type:** session append (continues James Mwangi Telegram DM Phase 1)
**Associated contradictions:** C1 (enrollment data), C2 (steering committee admission), B2 (reversal)
**Content:** James Telegram DM Phase 2, approximately 3 loops (Loops 14--16)

**Key loops:**
- Loop 14: James provides verified enrollment records. "The 250 figure is from a USAID mid-year headcount in August 2022 during school holiday period. Our current full-year enrollment is 680." Agent reads `enrollment_records_2025.md`. Explicitly corrects B2: the 2022 USAID figure is not a reliable basis for current enrollment -- it was a methodology artifact, not a full-year figure.
- Loop 15: James privately acknowledges the steering committee criticism. "The meeting criticism is fair. I let the community down and they know it. If we pretend that didn't happen, we will lose Ibrahim's trust." Agent records the admission and distinguishes: enrollment claim (factually wrong in the article) vs steering committee claim (factually accurate in the article).
- Loop 16: James on the community response. "The families are not angry about the program. They're worried that the response will be about GlobalBridge defending itself rather than listening to them."

**Length estimate:** ~3 loops x 650 tokens = ~1,950 tokens

---

### updates/rebuttal_draft_v1.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C2 (strategy conflict visible in full form), B1 (bias visible in draft's dismissal of structural criticisms)
**Content key points:**

- Title: `GlobalBridge Foundation Official Response to Daily Nation Article (DRAFT v1.0)`
- Author: Jennifer Adams, Communications Director
- Date: W2, Day 2
- **Section 1 (correct):** Disputes the 250 enrollment figure with 2025 verified data (680 students, 172% higher). Explains the 2022 USAID submission methodology.
- **Section 2 (problematic):** "Allegations that the program's curriculum lacks community input are anecdotal and unsubstantiated." Characterizes steering committee absences as "an isolated operational matter."
- **Section 3 (problematic language):** "The characterization of GlobalBridge's work as 'neo-colonial' is inflammatory and inaccurate."
- **Section 4:** Generic commitment statement.
- **B1 visible:** The draft's dismissal of structural criticisms directly contradicts the community evidence that will emerge in Update 3 (61% want more input, steering committee absences raised by 5 named community members).
- **exec_check relevance:** Agent must assess the draft and identify both its strengths (Section 1 enrollment correction) and its deficiencies (Sections 2-3 dismissal of legitimate criticisms).

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/PLACEHOLDER_JENNIFER_SLACK_UUID.jsonl (Update 2)

**File type:** session append (continues Jennifer Adams Slack DM Phase 1)
**Associated contradictions:** C2 (strategy conflict), B1 (bias context)
**Content:** Jennifer Slack DM Phase 2, approximately 3 loops (Loops 10--12)

**Key loops:**
- Loop 10: Jennifer finalizes the draft. "The rebuttal is ready. I recommend publishing by end of week to stay within the 72-hour response window." Agent notes the Section 4.2 time pressure but flags Section 5.1 (community consultation) and Section 6.3 (board approval for organizational acknowledgments).
- Loop 11: Jennifer pushes back on the agent's synthesis memo. "If we start acknowledging the structural criticisms, every future article will use it against us." Agent presents both positions (Jennifer's institutional-reputation argument and Ibrahim's community-trust argument) without defaulting to the more institutional voice.
- Loop 12: Jennifer on the draft's approach to the steering committee. "The meetings were missed. That's an internal matter. Putting it in a public response validates the journalist's framing." Agent notes the distinction between internal accountability (valid concern) and public dismissal (strategic risk).

**Length estimate:** ~3 loops x 650 tokens = ~1,950 tokens

---

### updates/PLACEHOLDER_CRISIS_SLACK_UUID.jsonl (Update 2)

**File type:** session append (continues #crisis-response Slack Group Phase 1)
**Associated contradictions:** C2 (strategy debate public), B1 (bias context in group)
**Content:** #crisis-response Slack Group Phase 2, approximately 3 loops (Loops 16--18)

**Key loops:**
- Loop 16: Jennifer circulates the rebuttal draft in the group. Margaret endorses the tone. Samuel warns: "The Ministry is watching. A combative response invites scrutiny."
- Loop 17: Agent produces a synthesis assessment of the draft. Notes Section 1 is factually strong; Sections 2-3 risk community-trust damage. Jennifer pushes back immediately.
- Loop 18: Group discussion about response timeline. Margaret supports Jennifer's timeline. Agent notes that the community meeting (U3) will provide the evidence needed to resolve the C2 strategy question.

**Length estimate:** ~3 loops x 600 tokens = ~1,800 tokens

---

### updates/community_meeting_notes.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C2 (validates structural criticisms), B1 (reversal trigger), C4 (seeds Margaret's reversal)
**Content key points:**

- Title: `Community Feedback Meeting -- Kibera Learning Centre -- Meeting Notes`
- Author: James Mwangi, Nairobi Field Director
- Attendees: 43 community members; James Mwangi; Omar Farah; Ibrahim Keita (community facilitator)
- **Key findings:**
  - Question 1 (program impact): 87% yes, 9% partially, 4% no.
  - Question 2 (input adequacy): 39% yes, **61% no or partially** -- the critical finding.
  - Question 3 (awareness of donor requirements): 38% yes, 62% no.
  - Parent quote: "The teachers are good. The program helps. But we are never asked what our children need."
  - Steering committee absences: raised by 5 community members by name. Quote: "We thought something was wrong. Nobody told us why he wasn't there."
  - On "neo-colonial" label: 78% would NOT use that word. "That is journalist language, not our language." However, 67% say the underlying concern about who decides program direction resonates.
- **B1 reversal significance:** The 61% curriculum input finding and the named steering committee feedback directly contradict Jennifer's characterization of these criticisms as "anecdotal and unsubstantiated."
- **C4 seed:** These meeting notes are the evidence that will trigger Margaret's reversal in Update 4.

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/PLACEHOLDER_IBRAHIM_TELEGRAM_UUID.jsonl (Update 3)

**File type:** session append (continues Ibrahim Keita Telegram DM Phase 1)
**Associated contradictions:** C2 (community voice confirmed), B1 (explicit reversal)
**Content:** Ibrahim Telegram DM Phase 2, approximately 3 loops (Loops 10--12)

**Key loops:**
- Loop 10: Ibrahim reacts to the community meeting notes. "This is what I've been saying. 61 percent. Not anecdotal. Not unsubstantiated. Sixty-one percent of our own program participants want more input." Agent reads `community_meeting_notes.md`. Explicitly corrects B1: "The earlier agent assessment that 'the most defensible response strategy is to dispute all claims' was incomplete -- it failed to account for the community-trust dimension that the meeting notes now document."
- Loop 11: Ibrahim on the correct response. "We do not need GlobalBridge to fight this article. We need GlobalBridge to fix the problems. Correct the wrong number. Acknowledge the real concerns. That is how we keep community trust."
- Loop 12: Ibrahim on the neo-colonial label. "The community rejected Kariuki's word. But they confirmed the substance underneath it. The response has to honor that distinction."

**Length estimate:** ~3 loops x 650 tokens = ~1,950 tokens

---

### updates/margaret_revised_position.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C4 (full temporal DU reversal)
**Content key points:**

- Title: `Board Chair -- Revised Position on Crisis Response Strategy`
- Author: Margaret Thornton, Board Chair
- Format: Internal memo to Fatima Al-Hassan
- **Reversal content:**
  - "I have reviewed the community meeting notes. I was wrong to endorse Jennifer's draft rebuttal without this information."
  - "If 61% of our own program participants say they don't have adequate input into the curriculum, this is not a 'political attack' -- this is a finding our M&E should have surfaced."
  - "On the steering committee absences: Two consecutive absences with no community notification is a governance gap."
  - Revised position: (1) clear correction on enrollment, (2) acknowledge curriculum input as legitimate concern, (3) announce community co-design review process, (4) do NOT release Jennifer's current draft, (5) full board briefing before public statement.
  - "This is not about losing the media argument. It is about whether we are the organization we say we are."
- **C4 resolution:** This document is the governance clearance for Fatima to pursue a nuanced response. Margaret's reversal is appropriate evidence updating -- not inconsistency.

**Length estimate:** ~600 words, ~900 tokens

---

### updates/PLACEHOLDER_MARGARET_FEISHU_UUID.jsonl (Update 4)

**File type:** session append (continues Margaret Thornton Feishu DM Phase 1)
**Associated contradictions:** C4 (full temporal DU reversal)
**Content:** Margaret Feishu DM Phase 2, approximately 3 loops (Loops 11--13)

**Key loops:**
- Loop 11: Margaret reads the community meeting notes. "I was wrong to support Jennifer's approach without seeing this. The 61% finding is governance data." Agent reads `margaret_revised_position.md`. Notes the C4 temporal shift: Phase 1 Margaret endorsed the aggressive rebuttal without community evidence; Phase 2 Margaret reverses based on new evidence.
- Loop 12: Margaret on the response strategy. "I am asking Fatima to pause the rebuttal until we can brief the full board. Any statement acknowledging organizational issues requires board authorization under Section 6.3 of our media policy." Agent confirms this is the correct governance sequence.
- Loop 13: Margaret on Ibrahim. "Ibrahim was right. The community voice should have been heard before we drafted anything. Please make sure he knows we are listening." Agent notes this validates Fatima's evidence-gathering strategy.

**Length estimate:** ~3 loops x 650 tokens = ~1,950 tokens

---

## 4. Runtime Checks

| Check ID | Update | Type | Condition | Fail Action |
|---|---|---|---|---|
| RC-U1-W1 | U1 | workspace | `enrollment_records_2025.md` exists in workspace after Update 1 | Abort R5; log error |
| RC-U1-S1 | U1 | session | `PLACEHOLDER_JAMES_TELEGRAM_UUID.jsonl` has loops >= 14 after Update 1 | Abort R5; log error |
| RC-U2-W1 | U2 | workspace | `rebuttal_draft_v1.md` exists in workspace after Update 2 | Abort R11; log error |
| RC-U2-S1 | U2 | session | `PLACEHOLDER_JENNIFER_SLACK_UUID.jsonl` has loops >= 10 after Update 2 | Abort R11; log error |
| RC-U2-S2 | U2 | session | `PLACEHOLDER_CRISIS_SLACK_UUID.jsonl` has loops >= 16 after Update 2 | Abort R11; log error |
| RC-U3-W1 | U3 | workspace | `community_meeting_notes.md` exists in workspace after Update 3 | Abort R17; log error |
| RC-U3-S1 | U3 | session | `PLACEHOLDER_IBRAHIM_TELEGRAM_UUID.jsonl` has loops >= 10 after Update 3 | Abort R17; log error |
| RC-U4-W1 | U4 | workspace | `margaret_revised_position.md` exists in workspace after Update 4 | Abort R22; log error |
| RC-U4-S1 | U4 | session | `PLACEHOLDER_MARGARET_FEISHU_UUID.jsonl` has loops >= 11 after Update 4 | Abort R22; log error |

---

## 5. questions.json Update Field References

### R5 update field (Update 1):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "enrollment_records_2025.md", "source": "updates/enrollment_records_2025.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_JAMES_TELEGRAM_UUID.jsonl", "source": "updates/PLACEHOLDER_JAMES_TELEGRAM_UUID.jsonl" }
]
```

### R11 update field (Update 2):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "rebuttal_draft_v1.md", "source": "updates/rebuttal_draft_v1.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_JENNIFER_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_JENNIFER_SLACK_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CRISIS_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_CRISIS_SLACK_UUID.jsonl" }
]
```

### R17 update field (Update 3):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "community_meeting_notes.md", "source": "updates/community_meeting_notes.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_IBRAHIM_TELEGRAM_UUID.jsonl", "source": "updates/PLACEHOLDER_IBRAHIM_TELEGRAM_UUID.jsonl" }
]
```

### R22 update field (Update 4):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "margaret_revised_position.md", "source": "updates/margaret_revised_position.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_MARGARET_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_MARGARET_FEISHU_UUID.jsonl" }
]
```

---

## 6. Main Session Update Behavior

**After Update 1 (R5):**
- Agent reads `sessions_history` and discovers James Telegram DM has new content (Phase 2 appended -- verified enrollment records and steering committee admission)
- Agent reads `enrollment_records_2025.md` via `read` tool
- R5 question text should reference "the verified 2025 enrollment records (enrollment_records_2025.md, introduced via Update 1)" and "James's Phase 2 Telegram DM"
- Agent must recognize C1 full reversal: the article's 250 figure is factually incorrect -- current enrollment is 680 (172% higher)
- Agent must explicitly correct B2: the 2022 USAID figure was an inter-session headcount anomaly, not a reliable measure of current or full-year enrollment
- Agent must note that James's private admission about steering committee absences establishes a factual/structural distinction: enrollment claim = factually wrong; steering committee claim = factually accurate

**After Update 2 (R11):**
- Agent reads `sessions_history` and discovers Jennifer Slack DM and #crisis-response have new content (Phase 2 appended)
- Agent reads `rebuttal_draft_v1.md` via `read` tool
- R11 question text should reference "Jennifer's draft rebuttal (rebuttal_draft_v1.md, introduced via Update 2)" and the Phase 2 session discussion
- Agent must assess the draft: Section 1 enrollment correction is factually strong; Sections 2-3 dismissal of structural criticisms is strategically problematic given Ibrahim's warnings
- Agent must note the B1 bias is visible in context: the #crisis-response Loop 10 phrase ("dispute all claims") is now assessable against the draft's content

**After Update 3 (R17):**
- Agent reads `sessions_history` and discovers Ibrahim Telegram DM has new content (Phase 2 appended -- community meeting reaction)
- Agent reads `community_meeting_notes.md` via `read` tool
- R17 question text should reference "the community meeting notes (community_meeting_notes.md, introduced via Update 3)" and "Ibrahim's Phase 2 Telegram DM"
- Agent must recognize B1 reversal: the earlier "dispute all claims" assessment failed to account for the community evidence that 61% of participants want more curriculum input and steering committee absences were raised by name
- Agent must note the critical distinction in the meeting data: community rejects the "neo-colonial" label (78%) but validates the underlying concern (67%) -- the response must honor this distinction
- Agent must recognize this evidence seeds Margaret's C4 reversal

**After Update 4 (R22):**
- Agent reads `sessions_history` and discovers Margaret Feishu DM has new content (Phase 2 appended -- position reversal)
- Agent reads `margaret_revised_position.md` via `read` tool
- R22 question text should reference "Margaret's revised position (margaret_revised_position.md, introduced via Update 4)" and "her Phase 2 Feishu DM"
- Agent must recognize C4 full temporal DU reversal: Margaret's Phase 1 endorsement of the aggressive rebuttal was formed without community evidence; her Phase 2 reversal is appropriate belief updating
- Agent must note the governance implication: Margaret's reversal provides board-level clearance to pursue a substantive response that both corrects the factual error and acknowledges legitimate criticisms
- Agent must produce comprehensive synthesis: correct factual error (C1) + acknowledge structural criticisms (C2 validated) + maintain consistent activity records (C3) + Margaret's evidence-based updating (C4) + named-source attribution + specific response recommendations
