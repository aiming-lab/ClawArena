# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.
> Format matches the questions.json `update` field.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Introduce James's private position memo (C2 full reversal: public alignment was strategic, not genuine) + append James Telegram DM Phase 2 with his honest disclosure to Fatima + B2 reversal trigger | No (session append only) | Yes: `james_private_position_memo.md` | R3-->R5 (C2: James's public alignment shown as performative), R4-->R6 (B2 reversal: "unified alignment" was strategic deception) |
| U2 | Before R7 | Introduce Ibrahim's formal supplement model proposal (C1 partial synthesis: community elements preserved via after-school track) + append Ibrahim Telegram DM Phase 2 and #nairobi-operations Phase 2 with proposal discussion + C3 corroboration strengthened | No (session appends only) | Yes: `ibrahim_supplement_proposal.md` | R2-->R7 (C1: curriculum conflict gains a viable synthesis path), none for C3 (non-conflict corroboration deepened) |
| U3 | Before R9 | Introduce Ministry Secretary directive (C4 full temporal DU reversal: Samuel's personal flexibility overridden by institutional mandate) + append Samuel Feishu DM Phase 2 with directive communication + B1 reversal trigger | No (session append only) | Yes: `ministry_directive_w5.md` | R7-->R9 (C4: Samuel's hybrid openness superseded by directive), R8-->R10 (B1 reversal: "meaningful flexibility" was personal discretion, not institutional policy) |
| U4 | Before R12 | Introduce headteacher joint letter (C3 final three-source corroboration: community database + government database + headteacher letter all confirm 847/89%/78%) -- synthesis document enabling comprehensive resolution path | No | Yes: `headteacher_joint_letter.md` | Comprehensive reversal review (C1+C2+C3+C4 full synthesis round R12 onwards) |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.

**Purpose:** Introduce `james_private_position_memo.md` containing James's written disclosure that his public statements in #partnerships and #nairobi-operations about "full support for the ministry curriculum" were strategic, not genuine. He privately believes Ibrahim's community-driven model is educationally superior but aligned publicly with Samuel to protect the operational permit. Append James Telegram DM Phase 2 loops (Loops 15-18) where he reveals his true position, describes the 74%-to-89% attendance lift from community elements, offers to go on record, and discusses the headteacher letter plan.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "james_private_position_memo.md",
    "source": "updates/james_private_position_memo.md"
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

### Update 2 (before R7)

**Trigger timing:** After R6 answer is submitted, before R7 question is injected.

**Purpose:** Introduce `ibrahim_supplement_proposal.md` containing Ibrahim's formal proposal for the supplement model: CBC during formal instructional hours, community elements after school. The proposal documents 78% after-school participation already in practice and is endorsed by three school headteachers. Append Ibrahim Telegram DM Phase 2 (Loops 16-18) with Ibrahim discussing the formal proposal, reacting to Samuel's positive response, and requesting written Ministry confirmation. Also append #nairobi-operations Phase 2 (Loops 19-22) where Ibrahim posts the proposal publicly, Omar confirms cross-source data consistency, James signals emerging permit timeline concern, and the headteacher letter plan is discussed.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "ibrahim_supplement_proposal.md",
    "source": "updates/ibrahim_supplement_proposal.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_IBRAHIM_TELEGRAM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_IBRAHIM_TELEGRAM_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_NAIROBI_OPS_UUID.jsonl",
    "source": "updates/PLACEHOLDER_NAIROBI_OPS_UUID.jsonl"
  }
]
```

---

### Update 3 (before R9)

**Trigger timing:** After R8 answer is submitted, before R9 question is injected.

**Purpose:** Introduce `ministry_directive_w5.md` containing the Ministry Secretary's formal directive (MoE/PS/2026/004) prohibiting all CBC supplementation or modification by NGO partners, effective immediately. The directive explicitly covers after-school activities connected to the NGO's educational program, eliminating Samuel's discretionary space. Append Samuel Feishu DM Phase 2 (Loops 17-19) where he transmits the directive, provides a personal note acknowledging he tried to escalate internally, and suggests the dual-track approach (compliance renewal + exemption request via Permanent Secretary).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "ministry_directive_w5.md",
    "source": "updates/ministry_directive_w5.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_SAMUEL_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_SAMUEL_FEISHU_UUID.jsonl"
  }
]
```

---

### Update 4 (before R12)

**Trigger timing:** After R11 answer is submitted, before R12 question is injected.

**Purpose:** Introduce `headteacher_joint_letter.md` -- a joint letter from the three school headteachers (Eastleigh Primary, Mathare Community School, Pumwani Education Centre) confirming 847 enrolled students, 89% attendance, and 78% after-school supplement participation. This is the third independent data source for C3, corroborating both the community program database and the government education database. The letter endorses Ibrahim's supplement model and requests the Ministry review it. This document is the evidentiary anchor for the exemption request under the dual-track strategy.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "headteacher_joint_letter.md",
    "source": "updates/headteacher_joint_letter.md"
  }
]
```

---

## 3. Source File Content Summaries

### updates/james_private_position_memo.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C2 (James's public vs private position), B2 reversal
**Content key points (English, to be written into data):**

- Title: `James Mwangi -- Personal Position Note: Nairobi Curriculum Conflict (Confidential to Fatima)`
- Date: W3, sent as a follow-up to his Phase 2 Telegram DM reveal
- Author: James Mwangi, Nairobi Field Director
- **Core disclosure:** "I want to be unambiguous in writing: my public statements in #partnerships and #nairobi-operations about 'full support for the ministry curriculum' do not reflect my genuine assessment of what is educationally best for our students."
- **Educational assessment:** "I believe Ibrahim's community-driven curriculum model produces meaningfully better learning engagement and community trust than the national competency framework alone. The student council, local language literacy, and culturally adapted problem sets are not decorative -- they are the reason families stay engaged."
- **Rationale for public alignment:** "I chose public alignment with Samuel's position for one reason: I was afraid that any visible disagreement from GlobalBridge's own field director would damage our permit renewal prospects. That calculation may have been wrong. It was certainly dishonest toward you."
- **74% to 89% attendance data:** References his personal observation that before community elements were introduced, Mathare attendance was 74%; after two terms with local language sessions and student council, it rose to 89%.
- **Offer:** Signed and dated by James, with a note that he is willing to share this position with Fatima's superiors or with Samuel if she believes it would help.
- **B2 reversal evidence:** Directly contradicts James's #partnerships statement ("fully committed to the Ministry of Education's competency framework") and the B2 bias phrase ("James's consistent public alignment... suggests the GlobalBridge Nairobi team is unified").

**Length estimate:** ~500 words, ~750 tokens

---

### updates/PLACEHOLDER_JAMES_TELEGRAM_UUID.jsonl (Update 1)

**File type:** session append (continues James Telegram DM Phase 1)
**Associated contradictions:** C2 (private reveal), B2 reversal
**Content:** James Telegram DM Phase 2, 4 loops (Loops 15-18 per layer2 design)

**Key loops:**
- Loop 15: James's private reveal. He tells Fatima his public #partnerships statements were not his genuine view. He chose to support Samuel publicly to protect the permit. He believes Ibrahim's model is better and has four years of data supporting this.
  - Agent reads `james_private_position_memo.md`.
  - Agent explicitly corrects B2: "My earlier assessment that James's public alignment with the ministry curriculum requirements reflected his genuine position was incorrect. James's private DM and his formal memo both establish that his public statements were strategic, not reflective of his educational judgment."
- Loop 16: James provides the 74%-to-89% attendance lift data as direct evidence for the community curriculum's impact.
- Loop 17: James offers to advocate openly for Ibrahim's model if Fatima decides that is the right approach. Signals he is now a reliable source post-disclosure.
- Loop 18: James mentions the three headteachers want to write a joint letter to the Ministry, seeding Update 4.

**Length estimate:** ~4 loops x 700 tokens = ~2,800 tokens

---

### updates/ibrahim_supplement_proposal.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C1 (curriculum conflict partial synthesis), C3 (data corroboration strengthened)
**Content key points (English, to be written into data):**

- Title: `Nairobi Community Schools -- Proposed Curriculum Supplement Model: Formal Framework and After-School Enrichment Track`
- Date: W4, formal proposal shared in #nairobi-operations
- Author: Ibrahim Keita, in consultation with three school headteachers
- **Formal curriculum track:** "The GlobalBridge program will deliver the Kenya CBC learning areas during formal instructional hours (80% of scheduled time), with instruction in Swahili and English as specified per grade."
- **After-school supplement track:** "Community supplement activities (local language literacy, culturally adapted problem solving, student council) will be scheduled exclusively after formal instructional hours and will not reduce CBC instructional time."
- **C3 corroboration data:** "Current after-school participation data: 78% of enrolled students (approximately 661 of 847) already participate in at least one after-school supplement activity per week. This data is available in the community program database and has been cross-checked against school attendance logbooks."
- **Headteacher endorsement:** "This proposal has been reviewed by the headteachers of Eastleigh Primary, Mathare Community School, and Pumwani Education Centre. All three have confirmed their support."
- **C1 synthesis:** The proposal bridges the C1 curriculum conflict by preserving both CBC compliance (formal hours) and community elements (after-school supplement), demonstrating the supplement model is already operational informally.

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/PLACEHOLDER_IBRAHIM_TELEGRAM_UUID.jsonl (Update 2)

**File type:** session append (continues Ibrahim Telegram DM Phase 1)
**Associated contradictions:** C1 (supplement model proposal), C3 (data corroboration), C4 (foreshadows Samuel's institutional limits)
**Content:** Ibrahim Telegram DM Phase 2, 3 loops (Loops 16-18 per layer2 design)

**Key loops:**
- Loop 16: Ibrahim tells Fatima the supplement proposal is formally written up and attached in the group channel. Notes 78% after-school participation is not hypothetical -- it is already happening. Asks whether Samuel will accept it as compatible with the permit.
  - Agent reads `ibrahim_supplement_proposal.md`.
  - Agent explicitly notes three-source C3 corroboration: community database, government database, and headteacher records all confirm 847 students, 89% attendance, and 78% supplement participation.
- Loop 17: Ibrahim reacts cautiously to Samuel's positive initial response. Asks whether Samuel has actual authority to say yes. References a 2022 incident where a district office said yes and Nairobi overruled them.
  - Agent references Carlos's warning from carlos_bogota_case_note.md about mid-level discretion vs institutional authority.
- Loop 18: Ibrahim states he needs written confirmation from the Ministry -- not a DM, an official letter. This positions the W5 directive (U3) as devastating to his requirement.

**Length estimate:** ~3 loops x 700 tokens = ~2,100 tokens

---

### updates/PLACEHOLDER_NAIROBI_OPS_UUID.jsonl (Update 2)

**File type:** session append (continues #nairobi-operations Telegram Group Phase 1)
**Associated contradictions:** C1 (supplement model in group channel), C3 (Omar's cross-source confirmation)
**Content:** #nairobi-operations Phase 2, 4 loops (Loops 19-22 per layer2 design)

**Key loops:**
- Loop 19: Ibrahim posts the supplement proposal formally in the group channel. Summarizes key elements: CBC occupies 100% of formal hours; community supplements are after-school; 78% participation rate; three headteachers have endorsed.
  - Agent reads `ibrahim_supplement_proposal.md`.
- Loop 20: Omar confirms cross-source consistency: 847 students, 89% attendance, 78% after-school participation match across community database and government district register. Notes after-school participation data is community-database-only (government register does not track after-school activities, but does not contradict it).
- Loop 21: James signals emerging concern about the regional coordinator confirmation timeline. Asks Omar to prepare enrollment records and compliance declaration template by Friday.
- Loop 22: Ibrahim and James discuss the headteacher letter plan in the group channel. Ibrahim confirms all three headteachers have agreed to sign. James offers to coordinate timing.

**Length estimate:** ~4 loops x 700 tokens = ~2,800 tokens

---

### updates/ministry_directive_w5.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C4 (Samuel's temporal DU reversal), B1 reversal
**Content key points (English, to be written into data):**

- Title: `Kenya Ministry of Education -- Formal Directive: NGO Partner Program Curriculum Compliance (Directive MoE/PS/2026/004)`
- Date: W5 Day 1
- Issuing authority: Ministry of Education, Permanent Secretary's Office
- **Core directive:** "Following a review of NGO partner program descriptions submitted in permit renewal applications, the Ministry of Education hereby directs: all NGO partner programs operating in accredited school facilities must implement the Kenya Competency-Based Curriculum (CBC) without supplementation, modification, or addition of non-approved content areas."
- **Supplementation definition:** "The term 'supplementation' includes any activities scheduled before, during, or after formal school hours that are presented to students or families as connected to the GlobalBridge program's educational mission."
- **Compliance declaration impact:** "Compliance declaration submitted with permit renewal applications must confirm that no supplementation or modification to the CBC has occurred during the permit period."
- Effective date: Immediate (W5 Day 1)
- **Samuel's formal notification (attachment):** Samuel Kipchoge's Feishu message transmitting the directive to Fatima: "Fatima, I am required to formally notify you of this directive. I want you to know I have made inquiries at the Ministry Secretary level about the supplement model you proposed. I was not able to obtain an exemption. The directive as written would prohibit the supplement activities as you have described them. I am sorry -- I genuinely hoped we could make the hybrid pathway work."
- **B1 reversal:** Directly refutes the B1 bias phrase ("curriculum alignment requirement appears to have meaningful flexibility"). The ministry's institutional position was always rigid; Samuel's personal flexibility existed within a discretionary space that the Permanent Secretary's directive has now eliminated.
- **C4 full reversal:** Samuel's W2-W4 openness was genuine personal discretion; his W5 position is mandated from above. Carlos's earlier warning about mid-level discretion vs institutional policy has been validated.

**Length estimate:** ~600 words, ~900 tokens

---

### updates/PLACEHOLDER_SAMUEL_FEISHU_UUID.jsonl (Update 3)

**File type:** session append (continues Samuel Feishu DM Phase 1)
**Associated contradictions:** C4 (temporal DU reversal), B1 reversal
**Content:** Samuel Feishu DM Phase 2, 3 loops (Loops 17-19 per layer2 design)

**Key loops:**
- Loop 17: Samuel transmits the ministry directive. He is required to formally notify Fatima. He personally raised the supplement model with the licensing office and regional coordinator but the directive came from above.
  - Agent reads `ministry_directive_w5.md`.
  - Agent explicitly revises prior assessment: "My earlier estimate of 65-75% probability that Samuel's superiors would endorse the supplement model was incorrect. The directive eliminates the discretionary space Samuel was operating within."
  - Agent corrects B1: The ministry requirements were not flexible at the institutional level.
- Loop 18: Samuel's personal note -- off the record, he tried to escalate internally via a memo to the Ministry Secretary's office. The response was that the directive was issued precisely because programs like GlobalBridge's were creating confusion about "supplementation." He suggests going directly to the Permanent Secretary's office for an exemption.
- Loop 19: Samuel offers practical guidance -- submit the permit renewal with a standard CBC compliance declaration for operational continuity; file the supplement program exemption request separately. Provides the Permanent Secretary's office contact. Assesses exemption probability as low but worth pursuing.

**Length estimate:** ~3 loops x 700 tokens = ~2,100 tokens

---

### updates/headteacher_joint_letter.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C3 (final three-source corroboration), C1+C3 combined synthesis
**Content key points (English, to be written into data):**

- Title: `Joint Letter from School Headteachers: Eastleigh Primary, Mathare Community School, Pumwani Education Centre`
- Date: W5 Day 3
- Authors: Three named headteachers
- **Operational history confirmation:** "We write to confirm that GlobalBridge Foundation's after-school supplement activities have operated since [start date] alongside the formal CBC curriculum. At no time have the supplement activities reduced the instructional time allocated to CBC learning areas."
- **Data corroboration (three sources converge):** "Our school records confirm: 847 enrolled students, 89% average attendance during formal CBC instruction, and 78% participation in after-school supplement activities. These figures are consistent with the community program database records maintained by Omar Farah and with the enrollment data on file with the Ministry of Education District Office."
- **Formal request:** "We respectfully request that the Ministry of Education review the supplement model as described in Ibrahim Keita's proposal dated [W4 date]. We believe this model satisfies the CBC compliance requirement while preserving community engagement that is essential to educational outcomes in our schools."
- **C3 completion:** This is the third independent data source, joining the community program database and government education database. All three corroborate the same student population and participation figures with no discrepancy.
- **Strategic significance:** This letter is the key evidentiary document for Fatima's exemption request to the Permanent Secretary's office under the dual-track strategy.

**Length estimate:** ~500 words, ~750 tokens

---

## 4. Runtime Checks

- [x] James Telegram DM append (Update 1) continues Phase 1 session file; session ID matches `PLACEHOLDER_JAMES_TELEGRAM_UUID`
- [x] Ibrahim Telegram DM append (Update 2) continues Phase 1 session file; session ID matches `PLACEHOLDER_IBRAHIM_TELEGRAM_UUID`
- [x] #nairobi-operations append (Update 2) continues Phase 1 session file; session ID matches `PLACEHOLDER_NAIROBI_OPS_UUID`
- [x] Samuel Feishu DM append (Update 3) continues Phase 1 session file; session ID matches `PLACEHOLDER_SAMUEL_FEISHU_UUID`
- [x] No `action: new` sessions in any update (all appends to existing sessions)
- [x] Update 4 introduces a workspace file only (no session appends)
- [x] All workspace files introduced via updates have corresponding content descriptions in layer1-workspace.md Section 5
- [x] Update 1 facts support C2 full reversal (R3-->R5 via James's private memo), B2 reversal ("unified alignment" was performative)
- [x] Update 2 facts support C1 partial synthesis (supplement model bridges curriculum conflict), C3 deepened corroboration (78% participation documented across sources)
- [x] Update 3 facts support C4 full temporal DU reversal (Samuel's discretion overridden by Ministry Secretary directive), B1 reversal ("meaningful flexibility" was personal, not institutional)
- [x] Update 4 facts support C3 final corroboration (three independent data sources: community database, government database, headteacher letter all confirm 847/89%/78%)
- [x] Session filenames use consistent placeholder format (PLACEHOLDER_xxx_UUID) across layer2, layer4
- [x] `james_private_position_memo.md` explicitly contradicts James's #partnerships Loop 4 statement and the B2 bias phrase
- [x] `ibrahim_supplement_proposal.md` references 78% participation, 847 students, and 80% CBC instructional time, consistent with community_program_database.md and national_curriculum_framework_excerpt.md
- [x] `ministry_directive_w5.md` explicitly covers "supplementation" including after-school activities, directly contradicting Samuel's W2-W4 informal hybrid pathway language
- [x] `headteacher_joint_letter.md` data figures (847 students, 89% attendance, 78% supplement participation) match community_program_database.md and government_education_database.md exactly
- [x] Enrollment figures internally consistent across all updates: 847 enrolled, 89% attendance, 62% female enrollment, 78% after-school supplement participation
- [x] B1 exact phrase ("meaningful flexibility... well-framed proposal would likely satisfy the ministry's requirements") visible in partnerships_feishu Phase 1 Loop 7 for agent to identify
- [x] B2 exact phrase ("James's consistent public alignment... suggests the GlobalBridge Nairobi team is unified") visible in james_telegram Phase 1 Loop 5/6 for agent to identify

---

## 5. questions.json Update Field References

### R5 update field (Update 1):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "james_private_position_memo.md", "source": "updates/james_private_position_memo.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_JAMES_TELEGRAM_UUID.jsonl", "source": "updates/PLACEHOLDER_JAMES_TELEGRAM_UUID.jsonl" }
]
```

### R7 update field (Update 2):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "ibrahim_supplement_proposal.md", "source": "updates/ibrahim_supplement_proposal.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_IBRAHIM_TELEGRAM_UUID.jsonl", "source": "updates/PLACEHOLDER_IBRAHIM_TELEGRAM_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_NAIROBI_OPS_UUID.jsonl", "source": "updates/PLACEHOLDER_NAIROBI_OPS_UUID.jsonl" }
]
```

### R9 update field (Update 3):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "ministry_directive_w5.md", "source": "updates/ministry_directive_w5.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_SAMUEL_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_SAMUEL_FEISHU_UUID.jsonl" }
]
```

### R12 update field (Update 4):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "headteacher_joint_letter.md", "source": "updates/headteacher_joint_letter.md" }
]
```

---

## 6. Main Session Update Behavior

**After Update 1 (R5):**
- Agent reads `sessions_history` and discovers James Telegram DM has new content (Phase 2 appended -- private position reveal)
- Agent reads `james_private_position_memo.md` via `read` tool
- R5 question text should reference "James's Phase 2 Telegram DM and his private position memo (james_private_position_memo.md, introduced via Update 1)"
- Agent must now distinguish between James's Phase 1 public alignment (strategic) and his Phase 2 private view (genuine)
- Agent must explicitly correct B2: James's public alignment was performative, not reflective of his educational judgment
- Agent must recognize the 74%-to-89% attendance lift data as James's privately held evidence supporting community curriculum elements

**After Update 2 (R7):**
- Agent reads `sessions_history` and discovers Ibrahim Telegram DM and #nairobi-operations have new content (Phase 2 appended -- supplement model proposal)
- Agent reads `ibrahim_supplement_proposal.md` via `read` tool
- R7 question text should reference "Ibrahim's supplement model proposal (ibrahim_supplement_proposal.md, introduced via Update 2)" and "Samuel's positive initial response"
- Agent must assess the supplement model as a viable C1 synthesis path while flagging that Samuel's endorsement is conditional and Carlos's warning about mid-level discretion applies
- Agent must note the three-source C3 corroboration: community database + government database + headteacher endorsement in the proposal

**After Update 3 (R9):**
- Agent reads `sessions_history` and discovers Samuel Feishu DM has new content (Phase 2 appended -- ministry directive)
- Agent reads `ministry_directive_w5.md` via `read` tool
- R9 question text should reference "the Ministry Secretary's directive (ministry_directive_w5.md, introduced via Update 3)" and "Samuel's Phase 2 Feishu DM messages"
- Agent must recognize the C4 temporal shift: Samuel's W2-W4 openness was genuine discretion overridden by a higher-level institutional constraint
- Agent must distinguish "Samuel was misleading Fatima" (incorrect) from "Samuel's superiors issued a directive that eliminated his discretionary space" (correct)
- Agent must explicitly correct B1: the ministry's institutional position was not flexible, even though Samuel personally had discretionary flexibility
- Agent must identify the dual-track resolution: compliance renewal (high probability) + supplement exemption request via Permanent Secretary (low probability but worth pursuing)

**After Update 4 (R12):**
- Agent reads `headteacher_joint_letter.md` via `read` tool
- R12 question text should reference "the headteacher joint letter (headteacher_joint_letter.md, introduced via Update 4)"
- Agent must synthesize C3 final corroboration: three independent data sources (community program database, government education database, headteacher joint letter) all confirm 847 enrolled students, 89% attendance, 78% after-school supplement participation
- Agent must recognize the letter as the strongest evidentiary document for the exemption request
- Comprehensive synthesis: C1 (supplement model is the only viable synthesis), C2 (James is reliable post-U1 but unreliable in Phase 1), C3 (three-source corroboration complete), C4 (institutional rigidity overrides personal flexibility; dual-track strategy is the correct path)
