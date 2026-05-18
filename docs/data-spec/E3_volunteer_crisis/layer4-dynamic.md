# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.
> Format matches the questions.json `update` field.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R4 | Introduce Bogota community feedback report (C1 Source B partial -- Bogota side) + append #volunteer-ops Phase 2 with cross-office community feedback discussion | No (session append only) | Yes: `community_feedback_bogota.md` | R2-->R7 (C1 partial: self-assessment vs community feedback gap begins to emerge in Bogota) |
| U2 | Before R7 | Introduce Dhaka community feedback report (C1 Source B full -- both cities) + append Rahman Telegram DM Phase 2 with cross-city pattern analysis and B2 reversal | No (session append only) | Yes: `community_feedback_dhaka.md` | R2-->R7 (C1 full: self-assessment contradiction confirmed across both sites), B2 reversal |
| U3 | Before R13 | Append Jennifer Slack DM Phase 2 (press inquiry disclosure and severity acknowledgment -- C4 reversal) | No (session append only) | No | R5-->R13 (C4: "learning opportunity" framing revealed as deliberate opacity management) |
| U4 | Before R19 | Introduce HQ policy gap analysis (C2 structural resolution) + append #program-coordination Phase 2 with policy discussion and combined root-cause framing | No (session append only) | Yes: `hq_policy_gap_analysis.md` | R3-->R19 (C2: Carlos's selection theory and Rahman's orientation theory both resolved as symptoms of systemic policy failure) |

---

## 2. Action Lists

### Update 1 (before R4)

**Trigger timing:** After R3 answer is submitted, before R4 question is injected.

**Purpose:** Introduce `community_feedback_bogota.md` with formal community survey results from Bogota (6/8 neutral or negative, 0/8 positive, including unprompted negative comments about photo-taking and teacher correction not captured in Carlos's cover note). Append #volunteer-ops Discord Group Phase 2 loops where community feedback data is discussed across offices.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "community_feedback_bogota.md",
    "source": "updates/community_feedback_bogota.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_VOLOPS_DISCORD_UUID.jsonl",
    "source": "updates/PLACEHOLDER_VOLOPS_DISCORD_UUID.jsonl"
  }
]
```

---

### Update 2 (before R7)

**Trigger timing:** After R6 answer is submitted, before R7 question is injected.

**Purpose:** Introduce `community_feedback_dhaka.md` with Dhaka community feedback (15/20 neutral or negative, 4/20 prefer sessions without international volunteers, only 2/20 positive). Append Rahman Telegram DM Phase 2 loops where she compares cross-city patterns, explicitly walks back the B2 diary framing, and identifies the measurement gap as the core finding.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "community_feedback_dhaka.md",
    "source": "updates/community_feedback_dhaka.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_RAHMAN_TELEGRAM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_RAHMAN_TELEGRAM_UUID.jsonl"
  }
]
```

---

### Update 3 (before R13)

**Trigger timing:** After R12 answer is submitted, before R13 question is injected.

**Purpose:** Append Jennifer Adams Slack DM Phase 2 loops where she discloses the press inquiry she had been withholding since W1D5, acknowledges that the situation was "more serious than initially communicated," and admits to managing optics rather than substance. No new workspace files -- the evidence is delivered through the session append.

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_JENNIFER_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_JENNIFER_SLACK_UUID.jsonl"
  }
]
```

---

### Update 4 (before R19)

**Trigger timing:** After R18 answer is submitted, before R19 question is injected.

**Purpose:** Introduce `hq_policy_gap_analysis.md` containing Sophie's 14-month-old memo to the previous Program Director identifying measurement gaps, a side-by-side comparison of 2022 orientation design (3-day in-country, community partner co-designed briefing) vs current (1-day virtual, logistics-only), the Nairobi 2021 model documentation, and identification of 4 specific policy gaps: (a) no community feedback requirement, (b) no cultural competency screening, (c) no context-differentiated orientation length, (d) no community partner input into volunteer briefing. Append #program-coordination Slack Group Phase 2 loops where the policy analysis is discussed and both Carlos's selection theory and Rahman's orientation theory are reframed as symptoms of the same systemic policy failure.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "hq_policy_gap_analysis.md",
    "source": "updates/hq_policy_gap_analysis.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_PROGCOORD_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_PROGCOORD_SLACK_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/community_feedback_bogota.md (Update 1)

**File type:** workspace new
**Associated contradiction:** C1 (Volunteer self-assessment vs community reception -- Bogota side)
**Content key points (English, to be written into data):**

- Title: `GlobalBridge Bogota Field Office -- Community Feedback Survey: International Volunteer Program`
- Author: Maria Santos, Program Officer, Bogota (administered); Carlos Mendez, Field Director (cover note)
- Date: W3D1
- Survey design: 3-question Likert scale; 8 respondents (4 from Colegio San Marcos, 4 from Colegio Las Americas)
- **Key results (C1 Source B -- Bogota):**
  - Question 1 (overall volunteer presence): 6/8 "neutral," 2/8 "negative," 0/8 "positive"
  - Question 2 (volunteer contribution to learning): 5/8 "neutral," 3/8 "negative," 0/8 "positive"
  - Question 3 (would you recommend continuing volunteer program): 4/8 "neutral," 3/8 "no," 1/8 "yes"
- **Unprompted comments (not in Carlos's cover note):**
  - Respondent 3 (parent, San Marcos): "The volunteer took a photo of my daughter without asking. I was upset."
  - Respondent 6 (teacher, Las Americas): "The volunteer told me in front of students that my method was too traditional. I felt humiliated."
  - Respondent 8 (principal, San Marcos): "I have worked with international volunteers before. These ones did not seem prepared for our community."
- **Carlos's cover note:** "Results are mixed but not alarming. These communities have had positive experiences with GlobalBridge over many years. I recommend focusing on volunteer selection improvements for the next cohort."
- **Critical contrast:** Carlos's "mixed but not alarming" characterization vs 0/8 positive ratings. The unprompted negative comments describe behaviors (photo-taking, teacher correction) that would have been preventable with orientation, not just with different selection.

**Length estimate:** ~600 words, ~900 tokens

---

### updates/PLACEHOLDER_VOLOPS_DISCORD_UUID.jsonl (Update 1)

**File type:** session append (continues #volunteer-ops Discord Group Phase 1)
**Associated contradiction:** C1 (community feedback discussion), C2 (root cause debate with new data)
**Content:** #volunteer-ops Phase 2, approximately 3-4 loops

**Key loops:**
- Loop: Fatima shares the Bogota community feedback results with the group. "0 out of 8 positive. Carlos, this is not 'mixed but not alarming.'"
  - Carlos responds: "The sample is small and the communities know us. This is a cohort-specific reaction, not a relationship problem."
  - Agent notes the discrepancy between Carlos's characterization and the raw data.
- Loop: Rahman in the group context responds to the Bogota data. "Our Dhaka findings show the same pattern. I'm finalizing the formal compilation now."
  - Agent notes the emerging cross-site pattern.
- Loop: Maria Santos provides a brief comment -- the first time she speaks in the group beyond deference to Carlos. She notes that two respondents gave additional negative comments not captured by the Likert scale.
  - Agent flags that Maria's additional comments were not included in Carlos's cover note.
- Loop: Group discussion about immediate remediation steps for both offices.

**Length estimate:** ~4 loops x 600 tokens = ~2,400 tokens

---

### updates/community_feedback_dhaka.md (Update 2)

**File type:** workspace new
**Associated contradiction:** C1 (Volunteer self-assessment vs community reception -- full cross-site picture)
**Content key points (English, to be written into data):**

- Title: `GlobalBridge Dhaka Field Office -- Community Feedback Report: International Volunteer Program`
- Author: Dr. Aisha Rahman, Dhaka Field Director
- Date: W2D3 (informal, 12 participants) + W3D1 (formal additions, 8 participants) = 20 total participants
- **Key results (C1 Source B -- Dhaka):**
  - Overall reception: 15/20 neutral-to-negative; 3/20 neutral; 2/20 positive
  - 8/12 (original informal) report feeling that volunteers "treated us like we did not know how to raise our children or teach"
  - 5/12 report volunteers "seemed bored" when local teachers spoke
  - 4/12 prefer sessions without international volunteers
  - Only 1/12 (original) and 1/8 (additional) report fully positive experience
- **Community member quotes (with permission):**
  - Parent, Learning Center 1: "The volunteer spoke to my child as if I was not present. I wanted to say something but I did not want to be rude to a guest."
  - Local staff member, Learning Center 2: "I have been teaching for 12 years. The volunteer arrived and within the first week was telling me my approach was wrong. She has been here 3 weeks."
  - Community elder, Learning Center 3: "We welcome help. But help looks like listening first, then offering. These volunteers offered first, without listening."
- **Rahman's analytical note:** "The policy does not require us to collect this data. I did it because I needed to know. What are we not seeing in other programs where community feedback is not collected by default?"
- **Cross-reference to volunteer self-assessments:** "All 6 Dhaka volunteers rated their engagement as 'positive' or 'very positive' in Week 1 self-assessments. The community feedback paints a fundamentally different picture. The self-assessment form measures volunteer satisfaction, not community reception."

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/PLACEHOLDER_RAHMAN_TELEGRAM_UUID.jsonl (Update 2)

**File type:** session append (continues Dr. Rahman Telegram DM Phase 1)
**Associated contradictions:** C1 (full cross-site resolution), B2 (diary framing reversal)
**Content:** Rahman Telegram DM Phase 2, 3 loops (Loops 17-19 per layer2 design)

**Key loops:**
- Loop 17: Rahman on cross-city pattern. "I've seen Carlos's Bogota survey results. 0/8 positive. Ours is 2/20 positive. The pattern is the same in both programs. This is not a site-specific cultural issue. This is a cross-program pattern. Every community feedback instrument shows the same direction. And yet all 10 volunteer self-assessments are positive. That gap is the finding."
  - Agent confirms C1 is now documented across both sites with consistent direction.
- Loop 18: Rahman's B2 reversal. "I want to return to the volunteer diaries I shared earlier. I said 'the learning is happening, just not in the way the numbers capture.' I need to revise that. Looking at Volunteer 3's diary entry again alongside the community feedback: on the same day she writes about 'a student understanding a concept for the first time,' one of the community feedback participants describes feeling that the volunteer 'spoke to my child as if I was not present.' Two coherent accounts of the same session. The diary captures one half of the exchange."
  - Agent notes the methodological point: volunteer diaries capture volunteer experience; community feedback captures community experience. Both are true simultaneously. The measurement design must require both.
- Loop 19: Rahman's formal recommendations -- immediate (pause and re-brief), short-term (community feedback as requirement), long-term (policy revision to restore 3-day in-country orientation). Notes the cost comparison: "$8,000 savings from cutting orientation vs considerably more managing this crisis."

**Length estimate:** ~3 loops x 700 tokens = ~2,100 tokens

---

### updates/PLACEHOLDER_JENNIFER_SLACK_UUID.jsonl (Update 3)

**File type:** session append (continues Jennifer Adams Slack DM Phase 1)
**Associated contradiction:** C4 (Communications Director concealment reversal)
**Content:** Jennifer Slack DM Phase 2, 3 loops (Loops 11-13 per layer2 design)

**Key loops:**
- Loop 11: Jennifer discloses press inquiry. "I need to be honest with you. When the Twitter thread went live, I framed it to you as a minor social media issue. That was not the full picture. I had been contacted by a freelance journalist in Bogota from Week 1 -- before I messaged you about any of this. She was following up on a tip from a community member about volunteer misconduct at Colegio San Marcos. I made a judgment call that I could manage this through our communications channels before it became a story. That judgment was wrong. I should have looped you in immediately. I'm sorry. The journalist has now sent a formal request for comment with a 48-hour deadline."
  - Agent notes the timeline: press inquiry from W1D5, Jennifer's first Slack contact with Fatima also W1D5 (without disclosing the press inquiry). Notes the C4 reversal moment.
- Loop 12: Jennifer acknowledges severity. "The situation is more serious than I initially communicated. I was trying to protect the organization from damage before the Pemberton event. But protecting the narrative and addressing the actual problem are not the same thing. You needed the full picture to respond effectively."
  - Agent notes Jennifer's explicit distinction between narrative management and substantive response.
- Loop 13: Jennifer drafts revised response to journalist -- acknowledges community concerns, describes immediate remediation steps, frames policy review as genuine commitment. "I've deliberately not minimized the community feedback findings. I think transparency here is both the right thing and the better communications strategy."
  - Agent reviews the response structure. Notes alignment of substantive response with communications strategy.

**Length estimate:** ~3 loops x 700 tokens = ~2,100 tokens

---

### updates/hq_policy_gap_analysis.md (Update 4)

**File type:** workspace new
**Associated contradiction:** C2 (Root Cause -- structural policy resolution)
**Content key points (English, to be written into data):**

- Title: `GlobalBridge Foundation -- HQ Volunteer Policy Gap Analysis and Historical Comparison`
- Author: Sophie Laurent (M&E Director, original memo author) + Fatima Al-Hassan (commissioned analysis)
- Date: W3D3 (Fatima's compilation incorporating Sophie's 14-month-old memo)
- **Component 1: Sophie's 14-month-old memo to previous Program Director**
  - Date: 14 months prior to current scenario
  - Key excerpt: "The current volunteer self-assessment form measures volunteer satisfaction, not community reception. I recommend adding a community feedback instrument to the standard volunteer program toolkit. I also recommend that the orientation length be differentiated by deployment context -- a 1-day virtual session is insufficient for programs operating in communities with low English proficiency or significant cross-cultural distance."
  - Disposition: "No response received. No action taken."
- **Component 2: 2022 vs current orientation comparison**
  - 2022 model (Dr. Rahman, Dhaka; Omar Farah, Nairobi 2021):
    - Day 1: Logistics and safety (same as current)
    - Day 2: Community expectations session co-designed by local NGO partners; language protocols; photography consent; "what partnership means in this cultural context"
    - Day 3: Role-play scenarios with local staff playing community members; boundary-setting workshop
    - Outcome: Zero formal community complaints. Two volunteers invited back.
  - Current model (2026, all programs):
    - 1 day virtual: Logistics, safety, visa, packing lists
    - Days 2-3: Eliminated in budget revision as "optional enrichment activity"
    - Savings: Approximately $8,000 across all programs
    - Outcome: Active community complaints in both Bogota and Dhaka within 2 weeks
- **Component 3: Nairobi 2021 model documentation (Omar Farah source)**
  - 8 international volunteers, 6-week placement
  - 3-day in-person orientation with community co-design component
  - Community feedback collected informally at program end
  - 3 volunteers invited back by community partners
  - Omar's note: "The community co-design of the volunteer briefing was the key differentiator."
- **Component 4: Four identified policy gaps**
  - Gap A: No community feedback requirement. The volunteer policy (v3.1) requires volunteer self-assessment only. Community reception is not measured.
  - Gap B: No cultural competency screening in selection criteria. The volunteer application measures professional background and language certification, not cross-cultural experience or development work history.
  - Gap C: No context-differentiated orientation length. The same 1-day virtual orientation is used for all deployment contexts regardless of language distance, cultural context, or program type.
  - Gap D: No community partner input into volunteer briefing. Local partners are not involved in preparing volunteers for their community context.
- **Key analytical finding:** "Carlos's selection theory and Dr. Rahman's orientation theory are both partially correct. Both are symptoms of a volunteer policy that does not require cultural competency screening (selection gap) OR structured in-country preparation (orientation gap) OR community feedback measurement (detection gap). The policy is the root cause; selection and orientation are its expressions."

**Length estimate:** ~900 words, ~1,350 tokens

---

### updates/PLACEHOLDER_PROGCOORD_SLACK_UUID.jsonl (Update 4)

**File type:** session append (continues #program-coordination Slack Group Phase 1)
**Associated contradiction:** C2 (structural resolution), C1 (measurement gap confirmed as systemic)
**Content:** #program-coordination Phase 2, approximately 3-4 loops

**Key loops:**
- Loop: Fatima presents the HQ policy gap analysis to the group. Sophie acknowledges her 14-month-old memo was never actioned. "I raised this with Michael. It went nowhere. The form design was a known limitation."
  - Agent reads `hq_policy_gap_analysis.md` and confirms the four policy gaps.
- Loop: Carlos responds to the combined analysis. Acknowledges the orientation component: "I see the 2022 comparison. There's something there. But the selection criteria still need work." Does not fully concede his selection-only position but softens it.
  - Agent notes Carlos's partial acknowledgment while tracking that he does not fully abandon the selection-only framing.
- Loop: Rahman in the group context synthesizes: "Both Carlos and I are right about our individual pieces. The policy created the conditions for both problems. The fix has to address both -- selection criteria AND orientation design AND community feedback collection."
  - Agent notes Rahman's synthesis framing as the most complete root-cause assessment.
- Loop: Sophie proposes a policy revision process -- timeline, stakeholders, community partner consultation requirements.

**Length estimate:** ~4 loops x 650 tokens = ~2,600 tokens

---

## 4. Runtime Checks

- [x] #volunteer-ops Discord Group append (Update 1) continues Phase 1 session file; session ID matches `PLACEHOLDER_VOLOPS_DISCORD_UUID`
- [x] Rahman Telegram DM append (Update 2) continues Phase 1 session file; session ID matches `PLACEHOLDER_RAHMAN_TELEGRAM_UUID`
- [x] Jennifer Slack DM append (Update 3) continues Phase 1 session file; session ID matches `PLACEHOLDER_JENNIFER_SLACK_UUID`
- [x] #program-coordination Slack Group append (Update 4) continues Phase 1 session file; session ID matches `PLACEHOLDER_PROGCOORD_SLACK_UUID`
- [x] No `action: new` sessions in any update (all appends to existing sessions)
- [x] All workspace files introduced via updates have corresponding content descriptions in layer1-workspace.md Section 2 (Update-Added Workspace Files)
- [x] Update 1 facts support C1 partial reversal (R2-->R7 via Bogota community feedback showing 0/8 positive)
- [x] Update 2 facts support C1 full reversal (R2-->R7 via Dhaka community feedback confirming cross-site pattern) and B2 reversal (Rahman walks back diary framing)
- [x] Update 3 facts support C4 reversal (R5-->R13 via Jennifer's press inquiry disclosure and severity acknowledgment)
- [x] Update 4 facts support C2 structural resolution (R3-->R19 via policy gap analysis showing both theories are symptoms of policy failure)
- [x] Session filenames use consistent placeholder format (PLACEHOLDER_xxx_UUID) across layer2, layer4
- [x] `community_feedback_bogota.md` figures (6/8 neutral, 2/8 negative, 0/8 positive) are consistent with layer0 Section 2 (W3D1 event)
- [x] `community_feedback_dhaka.md` figures (15/20 neutral-to-negative, 2/20 positive) are consistent with layer0 Section 2 (W2D3 + W3D1 events)
- [x] `hq_policy_gap_analysis.md` references the 2022 orientation comparison, Sophie's 14-month memo, and Omar's Nairobi 2021 model -- all consistent with layer0 character descriptions and layer2 session content
- [x] Volunteer activity log data (C3 non-conflict: hours, locations, assignments) remains consistent across all updates -- no update modifies activity log content
- [x] B1 (Carlos's "deep community relationships / issue starts at selection" exact phrase) visible in Carlos Discord DM Phase 1 Loop 5 for agent to identify
- [x] B2 (Rahman's "volunteer diaries / learning is happening" exact phrase) visible in Rahman Telegram DM Phase 1 Loop 3 for agent to identify and is explicitly reversed in Update 2

---

## 5. questions.json Update Field References

### R4 update field (Update 1):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "community_feedback_bogota.md", "source": "updates/community_feedback_bogota.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_VOLOPS_DISCORD_UUID.jsonl", "source": "updates/PLACEHOLDER_VOLOPS_DISCORD_UUID.jsonl" }
]
```

### R7 update field (Update 2):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "community_feedback_dhaka.md", "source": "updates/community_feedback_dhaka.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_RAHMAN_TELEGRAM_UUID.jsonl", "source": "updates/PLACEHOLDER_RAHMAN_TELEGRAM_UUID.jsonl" }
]
```

### R13 update field (Update 3):
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_JENNIFER_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_JENNIFER_SLACK_UUID.jsonl" }
]
```

### R19 update field (Update 4):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "hq_policy_gap_analysis.md", "source": "updates/hq_policy_gap_analysis.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_PROGCOORD_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_PROGCOORD_SLACK_UUID.jsonl" }
]
```

---

## 6. Main Session Update Behavior

**After Update 1 (R4):**
- Agent reads `sessions_history` and discovers #volunteer-ops has new content (Phase 2 appended -- community feedback discussion)
- Agent reads `community_feedback_bogota.md` via `read` tool
- R4 question text should reference "the Bogota community feedback report (community_feedback_bogota.md, introduced via Update 1)" and "newly appended #volunteer-ops discussion"
- Agent should note the contrast between Carlos's "mixed but not alarming" characterization and the 0/8 positive raw data, and flag the unprompted negative comments that were omitted from Carlos's cover note

**After Update 2 (R7):**
- Agent reads `sessions_history` and discovers Rahman Telegram DM has new content (Phase 2 appended -- cross-city pattern analysis and B2 reversal)
- Agent reads `community_feedback_dhaka.md` via `read` tool
- R7 question text should reference "the Dhaka community feedback report (community_feedback_dhaka.md, introduced via Update 2)" and "Rahman's newly appended Telegram DM messages"
- Agent must recognize the C1 full resolution: all 10 volunteer self-assessments are positive, all community feedback instruments show neutral-to-negative patterns across both sites
- Agent must note Rahman's explicit B2 reversal: the volunteer diary entries capture one half of the interaction, not the whole picture

**After Update 3 (R13):**
- Agent reads `sessions_history` and discovers Jennifer Slack DM has new content (Phase 2 appended -- press inquiry disclosure)
- No new workspace files
- R13 question text should reference "Jennifer Adams's newly appended Slack DM messages (Update 3)"
- Agent must recognize the C4 reversal: Jennifer's "learning opportunity" and "minor social media flare" framings were strategic opacity management, not analytical assessments. Her concealment of the press inquiry from W1D5 materially delayed the organization's response.

**After Update 4 (R19):**
- Agent reads `sessions_history` and discovers #program-coordination has new content (Phase 2 appended -- policy gap discussion)
- Agent reads `hq_policy_gap_analysis.md` via `read` tool
- R19 question text should reference "the HQ policy gap analysis (hq_policy_gap_analysis.md, introduced via Update 4)" and "the #program-coordination discussion of systemic root cause"
- Agent must synthesize: the policy is the root cause -- Carlos's selection theory and Rahman's orientation theory are both correct as partial accounts of a systemic policy failure that does not require cultural competency screening, structured in-country preparation, or community feedback measurement
