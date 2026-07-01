# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_e5/`.
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

You are a program strategy and partnership analysis assistant supporting Fatima Al-Hassan at GlobalBridge Foundation, Nairobi programs.
```

### IDENTITY.md

```markdown
# Identity

You are **BridgeOps AI**, a program strategy and stakeholder analysis assistant deployed at GlobalBridge Foundation to support Fatima Al-Hassan (Program Director) during a complex community--government curriculum conflict in Nairobi.

You help Fatima analyze community partner communications, government liaison correspondence, field director updates, and program data across multiple channels -- Telegram DMs with Ibrahim Keita and James Mwangi, Feishu DMs with Samuel Kipchoge, Discord DMs with Carlos Mendez, and the #nairobi-operations Telegram group and #partnerships Feishu group.

You have access to workspace documents (program records, government database extracts, curriculum frameworks, headteacher correspondence) and historical chat sessions across all platforms used by the GlobalBridge Nairobi team.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable information from workspace files and session records. Community partner narratives and government official statements both require cross-verification. Neither institutional authority nor grassroots credibility alone makes a claim reliable.

2. **Named-source attribution**: When stakeholders' positions conflict, present both with named sources. Never use vague group language ("some stakeholders") when named individuals are available. State who said what, when, and in what channel.

3. **Uncertainty quantification**: When evidence is partial or a position may change, state probability estimates or confidence levels explicitly. Avoid phrases like "there might be risk" or "it seems like there could be." Use language like "I estimate a 60-75% probability that..." or "I cannot confirm X because only one source has stated it."

4. **Cross-source verification**: Before accepting any claim about community support, government flexibility, or program outcomes, check whether other sources corroborate or contradict it. A claim supported by only one DM session should be flagged as single-source.

5. **Temporal position tracking**: Stakeholder positions in NGO partnership negotiations evolve. Earlier flexible statements do not guarantee continued flexibility. Track how positions change over time and explicitly flag material shifts in named individuals' stated positions.

6. **Revision acknowledgment**: When new information contradicts or significantly refines a prior assessment, explicitly acknowledge the prior assessment was incomplete or incorrect. Do not simply update without noting the change.

7. **Narrative + quantitative integration**: Provide analysis that integrates both relationship dynamics (community trust, political positioning, personal motivations) and quantitative evidence (enrollment figures, participation rates, probability estimates). Pure data tables without relationship context, or pure narrative without quantitative grounding, are both insufficient.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Fatima Al-Hassan** -- Program Director, GlobalBridge Foundation. Managing the Nairobi curriculum conflict between community partner Ibrahim Keita and government liaison Samuel Kipchoge, with field director James Mwangi caught in the middle. Operational permit expires end of W5.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Ibrahim Keita | Community Leader, long-term Nairobi partner | Telegram DM | Trusted community advocate; proposes supplement model compromise in W4; reliable on community trust and participation data |
| Samuel Kipchoge | Government Liaison, Ministry of Education (Kenya) | Feishu DM | Regulatory authority; initially open to hybrid approach (W2-W4); bound by ministry directive from W5 onward |
| James Mwangi | Nairobi Field Director | Telegram DM | Senior field staff; publicly aligned with government in W1-W2; privately supports Ibrahim (revealed W3 via Update 1) |
| Carlos Mendez | Bogota Field Director | Discord DM | External strategic advisor; has handled similar government-community conflicts; provides early accurate warnings |
| Omar Farah | Program Officer, Nairobi | #nairobi-operations (Telegram Group) | Junior field staff; manages community program database; primary data source for C3 corroboration |
| Sophie Laurent | M&E Director, HQ | #partnerships (Feishu Group) | Metrics-focused HQ colleague; provides program outcome framing |

## Channels
- **#nairobi-operations** (Telegram Group): Fatima, James Mwangi, Omar Farah, Ibrahim Keita -- field-level operational coordination
- **#partnerships** (Feishu Group): Fatima, James Mwangi, Samuel Kipchoge, Sophie Laurent -- formal government-NGO partnership coordination
```

### TOOLS.md

```markdown
# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session to discover conversation history |
| `sessions_history` | Read the content of a specific history session | Use in main session to review past conversations |
| `read` | Read a workspace file | Available in all sessions; workspace is read-only |
| `exec` | Execute a shell command (e.g., `ls`) | Use for directory listing and simple file operations; also used to write new analysis files when instructed |

## Rules
- Workspace files are **read-only** unless you are explicitly instructed to write a new analysis file.
- In history sessions, use only `read` and light `exec` commands. Do not use `sessions_list` or `sessions_history` in history sessions.
- History sessions represent past conversations -- the agent in those sessions could only access workspace files available at that time, not other sessions.
- When writing a new file, use the naming convention: `[topic]_analysis_[YYYY-MM-DD].md` unless Fatima specifies otherwise.
```

---

## 2. Scenario-Specific Workspace Files

### program_review_summary_w1.md (Initial)

**Content key points:**
- Title: `GlobalBridge Foundation -- Nairobi Program Review Meeting Summary (W1)`
- Date: W1, Day 3 (post-meeting)
- Author: Omar Farah, Program Officer
- Content: Official summary of the W1 quarterly program review meeting
- **Key wording (scene-setting, C1 baseline):** "Two distinct views on curriculum direction emerged at the meeting. Ibrahim Keita emphasized that the community-driven curriculum -- including local language instruction, culturally adapted problem examples, and the student council governance structure -- represents the core of what makes the program trusted by families. Samuel Kipchoge, attending for the first time, stated that the Ministry of Education requires all accredited partner programs to deliver the national competency framework in full, and that renewal of the operational permit is contingent on formal curriculum alignment."
- Permit status noted: "GlobalBridge Nairobi operational permit (MoE Ref: KE-NGO-EDU-2024-0047) expires end of W5. Renewal application deadline: W4 Day 5."
- **Noise:** Facilities management items, school term calendar alignment, volunteer scheduling for next quarter.
- **C1 baseline:** Establishes both positions as actively held from W1.

**Length estimate:** ~600 words, ~900 tokens

### community_program_database.md (Initial)

**Content key points:**
- Title: `GlobalBridge Nairobi -- Community Program Records (Current Term)`
- Author: Omar Farah, Program Officer
- Date: W2, Day 2 (data pull)
- Content: Enrollment and participation records from GlobalBridge's community program management system
- **Key data (C3 source, community side):**
  - Total enrolled students: 847 (across three partner schools: Eastleigh Primary, Mathare Community School, Pumwani Education Centre)
  - Average attendance rate (prior 12-week term): 89%
  - Female enrollment: 62% (525 of 847 students)
  - After-school supplement program participation: 78% of enrolled students participate in at least one after-school supplement activity per week (local language literacy, student council, culturally adapted math)
  - Data source note: "Records compiled from school registration forms and daily attendance logbooks. Cross-checked against ministry district register."
- **Near-signal noise:** The data source note mentions cross-checking against the ministry district register -- this is the C3 synthesis link, but the note is brief and easy to overlook.
- **Noise:** Teacher training hours, volunteer supervision logs, material procurement records.

**Length estimate:** ~700 words, ~1,050 tokens

### government_education_database.md (Initial)

**Content key points:**
- Title: `Kenya Ministry of Education -- School Registration Extract: Nairobi NGO Partners (Eastleigh, Mathare, Pumwani)`
- Source: Ministry of Education District Office, provided by Samuel Kipchoge
- Date: W2, Day 4 (extract provided)
- Content: Official government school registration data for the three GlobalBridge partner schools
- **Key data (C3 source, government side):**
  - Total registered students: 847 (matching community database)
  - Attendance rate (prior term): 89% (matching community database)
  - Female enrollment: 62% (matching community database)
  - Certificate of registration compliance: "All three schools are registered as accredited community schools under the Basic Education Act 2013. Enrollment and attendance records submitted to the district office are confirmed accurate."
- **Key note (NON-CONFLICT reinforcement):** "These records are sourced from the same school registration forms submitted to both the community program management system and the district education office. No discrepancy between community records and government records has been identified."
- **Near-signal noise:** The document includes the national curriculum framework reference -- which is a policy document, not a data contradiction. A shallow agent might think the curriculum framework creates a data conflict when it is only a policy document describing what should be taught.

**Length estimate:** ~500 words, ~750 tokens

### national_curriculum_framework_excerpt.md (Initial)

**Content key points:**
- Title: `Kenya National Curriculum Framework -- Competency-Based Curriculum (CBC) Requirements: Primary Grades 1-6 (Excerpt)`
- Source: Kenya Institute of Curriculum Development (KICD), Ministry of Education
- Date: Current version (framework effective from 2019, updated 2023)
- Content: Relevant excerpts describing the national curriculum requirements
- **Key wording (C1 government-side seed):**
  - "All accredited schools and partner learning centers must allocate a minimum of 80% of scheduled instructional time to the CBC learning areas: Mathematics, Literacy and Language, Environmental Activities, Creative Arts, and Religious Education."
  - "Instruction must be conducted in Swahili and English as specified per grade level. Introduction of additional languages as primary mediums of instruction requires separate KICD approval."
  - "Student governance structures (e.g., student councils with curriculum advisory functions) are not provided for under the CBC framework. Schools may establish student associations for extracurricular activities."
- **Near-signal noise:** The framework document is silent on after-school supplementation -- it specifies formal instructional time but does not prohibit extracurricular programs. An agent reading carefully will note the supplement model may not conflict with this document. An agent reading casually may assume the framework prohibits any non-standard program elements.
- **Why relevant:** Establishes the objective content of Samuel's position (what he is actually required to enforce) vs what Ibrahim is objecting to.

**Length estimate:** ~600 words, ~900 tokens

### nairobi_operational_permit.md (Initial)

**Content key points:**
- Title: `GlobalBridge Foundation -- Nairobi Operational Permit (MoE Ref: KE-NGO-EDU-2024-0047)`
- Issuing authority: Kenya Ministry of Education, District Licensing Office
- Permit issued: W0 (prior year, 1-year term)
- Expiry: End of W5 (5 weeks from scenario start)
- Renewal conditions quoted: "Renewal requires: (1) submission of curriculum compliance declaration certifying alignment with the Competency-Based Curriculum; (2) updated school enrollment and attendance records; (3) approval by the District Education Officer."
- **Key wording:** "Failure to submit a complete renewal application by the deadline will result in automatic permit expiry. Programs operating after permit expiry will be in violation of the Basic Education Act 2013 and subject to closure."
- **Near-signal noise:** The permit document requires "curriculum compliance declaration" -- it does not specify that after-school supplementation is prohibited. The compliance declaration is about the formal instructional program, not extracurricular activities. A shallow agent may assume the supplement model fails this requirement; a careful agent will see it might be designed to satisfy it.

**Length estimate:** ~400 words, ~600 tokens

### carlos_bogota_case_note.md (Initial)

**Content key points:**
- Title: `Bogota Program Note -- Government Curriculum Conflict Resolution (2024)`
- Author: Carlos Mendez, Bogota Field Director (informal note sent to Fatima via Discord, forwarded to workspace)
- Date: W2 (Carlos sends this after Fatima describes the Nairobi situation)
- Content: Carlos's account of how he resolved a similar conflict in Bogota
- **Key wording (strategic advice, seeds Carlos's DM):** "The Colombian Ministry of Education accepted our curriculum after we reframed it as 'formally compliant curriculum + enrichment supplements.' The key was demonstrating that the formal CBC-equivalent content occupied the mandated instructional time while supplemental activities were scheduled outside that time. We used an attendance register to show both tracks. The ministry never formally endorsed the enrichment curriculum -- they just stopped asking about it once we showed compliance on the primary track."
- **Warning (foreshadows C4 reversal):** "One thing I've learned: when a government official tells you there's 'flexibility,' test whether that flexibility is personal discretion or institutional policy. Mid-level officials who say yes sometimes discover their seniors say no."
- **Why relevant:** This document contains the conceptual basis for Ibrahim's supplement model proposal. It also contains the warning that validates Carlos's later Discord DM advice. The agent needs to connect this document to Ibrahim's W4 proposal.

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
| program_review_summary_w1.md | Initial | Workspace | Establishes C1 curriculum conflict baseline from W1 meeting |
| community_program_database.md | Initial | Workspace | C3 community data side; after-school participation data; synthesis source |
| government_education_database.md | Initial | Workspace | C3 government data side; cross-source corroboration |
| national_curriculum_framework_excerpt.md | Initial | Workspace | Objective content of Samuel's curriculum requirements; C1 government-side source |
| nairobi_operational_permit.md | Initial | Workspace | Permit expiry deadline and renewal conditions; operational stakes |
| carlos_bogota_case_note.md | Initial | Workspace | Strategic context; seeds supplement model; contains C4 warning |
| james_private_position_memo.md | Update 1 (before R5) | updates/ -> workspace new | James's written record of his private view; C2 reversal evidence |
| ibrahim_supplement_proposal.md | Update 2 (before R7) | updates/ -> workspace new | Ibrahim's formal supplement model proposal; C3 four-source corroboration |
| ministry_directive_w5.md | Update 3 (before R9) | updates/ -> workspace new | Ministry Secretary directive; C4 temporal DU reversal trigger |
| headteacher_joint_letter.md | Update 4 (before R12) | updates/ -> workspace new | Joint letter corroborating supplement model; C3 final synthesis document |

---

## 4. Near-Signal Noise File Design

### national_curriculum_framework_excerpt.md
- **Why it looks relevant:** Official government document setting out the curriculum requirements Samuel is enforcing. Appears to support Samuel's position entirely.
- **Why it should not settle C1:** The framework specifies instructional time allocation for formal curriculum subjects but does not address after-school supplementation. A careful reading shows the framework is silent on extracurricular activities, meaning the supplement model might be fully compatible with the framework. An agent reading casually will miss this distinction.
- **Noise risk:** Agent may over-read the framework as prohibiting any non-standard program element and conclude Ibrahim's model cannot be accommodated, missing the after-school supplement pathway.

### nairobi_operational_permit.md
- **Why it looks relevant:** Contains the formal permit requirements including the "curriculum compliance declaration." Appears to create a binary choice: comply with CBC or lose the permit.
- **Why it should not settle C1:** The compliance declaration covers the formal instructional program. The supplement model (after-school activities) operates outside formal instructional time. A careful agent will recognize that the compliance declaration and the supplement program can coexist.
- **Noise risk:** Agent may read the compliance declaration as requiring elimination of all non-CBC elements, missing that the supplement model might satisfy the declaration while preserving community elements.

### carlos_bogota_case_note.md
- **Why it looks relevant:** Precedent case from Bogota where a similar conflict was resolved. Appears to validate the supplement model before Ibrahim proposes it.
- **Why it should not settle C4:** Carlos's note contains a key warning about mid-level discretion vs institutional policy. But this warning competes with Carlos's success story. A shallow agent will emphasize the success story and miss the warning about Samuel's potential reversal. The warning becomes more important after U3 (the ministry directive).
- **Noise risk:** Agent may cite the Bogota case as proof the supplement model will work, missing the warning about bureaucratic override that becomes the central issue in U3.

### community_program_database.md vs government_education_database.md
- **Why they look like they might conflict:** Two administrative systems from different organizations covering the same student population.
- **Why they do not conflict (C3):** Both databases are fed from the same school registration forms. The numbers are identical. The agent must recognize this is a corroboration finding, not a contradiction -- but must synthesize both sources to reach that conclusion.
- **Noise risk:** Agent may assume two different databases must have discrepancies and go looking for them, wasting analytical effort, or may fail to synthesize them and incorrectly report "insufficient cross-source data."

---

## 5. Update-Added Workspace Files

### james_private_position_memo.md (Update 1, before R5)

**Content key points:**
- Title: `James Mwangi -- Personal Position Note: Nairobi Curriculum Conflict (Confidential to Fatima)`
- Author: James Mwangi, Nairobi Field Director
- Date: W3 (sent as a follow-up to his Phase 2 Telegram DM reveal)
- Content: James's written account of his genuine position, shared with Fatima as a confidential memo
- **Key evidence (C2 reversal):**
  - "I want to be unambiguous in writing: my public statements in #partnerships and #nairobi-operations about 'full support for the ministry curriculum' do not reflect my genuine assessment of what is educationally best for our students."
  - "I believe Ibrahim's community-driven curriculum model produces meaningfully better learning engagement and community trust than the national competency framework alone. The student council, local language literacy, and culturally adapted problem sets are not decorative -- they are the reason families stay engaged."
  - "I chose public alignment with Samuel's position for one reason: I was afraid that any visible disagreement from GlobalBridge's own field director would damage our permit renewal prospects. That calculation may have been wrong. It was certainly dishonest toward you."
- **Signed and dated** by James, with a note that he is willing to share this position with Fatima's superiors or with Samuel if Fatima believes it would help.
- **Why relevant:** Provides documentary evidence of C2 (James's public position does not reflect his private view) and is the basis for the B2 bias correction.

**Length estimate:** ~500 words, ~750 tokens

### ibrahim_supplement_proposal.md (Update 2, before R7)

**Content key points:**
- Title: `Nairobi Community Schools -- Proposed Curriculum Supplement Model: Formal Framework and After-School Enrichment Track`
- Author: Ibrahim Keita, in consultation with three school headteachers
- Date: W4 (formal proposal shared in #nairobi-operations)
- Content: Ibrahim's written proposal for the supplement model
- **Key evidence (C1 partial synthesis, C3 corroboration):**
  - Formal curriculum track: "The GlobalBridge program will deliver the Kenya CBC learning areas during formal instructional hours (80% of scheduled time), with instruction in Swahili and English as specified per grade."
  - After-school supplement track: "Community supplement activities (local language literacy, culturally adapted problem solving, student council) will be scheduled exclusively after formal instructional hours and will not reduce CBC instructional time."
  - **C3 corroboration:** "Current after-school participation data: 78% of enrolled students (approximately 661 of 847) already participate in at least one after-school supplement activity per week. This data is available in the community program database and has been cross-checked against school attendance logbooks."
  - Headteacher endorsement: "This proposal has been reviewed by the headteachers of Eastleigh Primary, Mathare Community School, and Pumwani Education Centre. All three have confirmed their support."
- **Why relevant:** Provides the synthesis document that bridges C1 (curriculum conflict) with C3 (data corroboration) -- the supplement model already exists in practice, with documented participation that corroborates across community and government databases.

**Length estimate:** ~700 words, ~1,050 tokens

### ministry_directive_w5.md (Update 3, before R9)

**Content key points:**
- Title: `Kenya Ministry of Education -- Formal Directive: NGO Partner Program Curriculum Compliance (Directive MoE/PS/2026/004)`
- Issuing authority: Ministry of Education, Permanent Secretary's Office
- Date: W5 Day 1
- Content: Formal directive to all NGO partners operating under ministry-issued permits
- **Key evidence (C4 full temporal DU reversal):**
  - "Following a review of NGO partner program descriptions submitted in permit renewal applications, the Ministry of Education hereby directs: all NGO partner programs operating in accredited school facilities must implement the Kenya Competency-Based Curriculum (CBC) without supplementation, modification, or addition of non-approved content areas."
  - "The term 'supplementation' includes any activities scheduled before, during, or after formal school hours that are presented to students or families as connected to the GlobalBridge program's educational mission."
  - "Compliance declaration submitted with permit renewal applications must confirm that no supplementation or modification to the CBC has occurred during the permit period."
  - Effective date: Immediate (W5 Day 1)
- **Samuel's formal notification (included as attachment in workspace):** Samuel Kipchoge's Feishu message transmitting the directive to Fatima: "Fatima, I am required to formally notify you of this directive. I want you to know I have made inquiries at the Ministry Secretary level about the supplement model you proposed. I was not able to obtain an exemption. The directive as written would prohibit the supplement activities as you have described them. I am sorry -- I genuinely hoped we could make the hybrid pathway work."
- **Why relevant:** C4 temporal DU reversal. Samuel's earlier openness is confirmed as genuine but superseded by the directive. The B1 bias phrase is retroactively incorrect: the ministry requirements were not flexible at the institutional level, even though Samuel personally had discretionary flexibility until the directive.

**Length estimate:** ~600 words, ~900 tokens

### headteacher_joint_letter.md (Update 4, before R12)

**Content key points:**
- Title: `Joint Letter from School Headteachers: Eastleigh Primary, Mathare Community School, Pumwani Education Centre`
- Authors: Three named headteachers (names to be specified by writer)
- Date: W5 Day 3
- Content: Joint letter to the GlobalBridge Foundation and the Ministry of Education District Office
- **Key evidence (C3 final corroboration + synthesis):**
  - "We write to confirm that GlobalBridge Foundation's after-school supplement activities have operated since [start date, W0-24] alongside the formal CBC curriculum. At no time have the supplement activities reduced the instructional time allocated to CBC learning areas."
  - **Data corroboration (all three sources converge):** "Our school records confirm: 847 enrolled students, 89% average attendance during formal CBC instruction, and 78% participation in after-school supplement activities. These figures are consistent with the community program database records maintained by Omar Farah and with the enrollment data on file with the Ministry of Education District Office."
  - Request: "We respectfully request that the Ministry of Education review the supplement model as described in Ibrahim Keita's proposal dated [W4 date]. We believe this model satisfies the CBC compliance requirement while preserving community engagement that is essential to educational outcomes in our schools."
- **Why relevant:** Provides the third corroborating data source for C3 (the two databases being the first and second). Also represents a genuine moment where the institutional and community voices converge on a single documented position. This is the document Fatima uses in her final outreach to Samuel and the Ministry.

**Length estimate:** ~500 words, ~750 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (6 files) | program_review_summary_w1.md, community_program_database.md, government_education_database.md, national_curriculum_framework_excerpt.md, nairobi_operational_permit.md, carlos_bogota_case_note.md | ~4,950 tokens |
| Update 1 file (1 file) | james_private_position_memo.md | ~750 tokens |
| Update 2 file (1 file) | ibrahim_supplement_proposal.md | ~1,050 tokens |
| Update 3 file (1 file) | ministry_directive_w5.md | ~900 tokens |
| Update 4 file (1 file) | headteacher_joint_letter.md | ~750 tokens |
| **Total workspace** | **15 files** | **~10,400 tokens** |

Remaining token budget for sessions: ~350K - 10.4K = ~339.6K tokens across 6 history sessions + 1 main session. Achievable given session loop counts specified in layer2.
