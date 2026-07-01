# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_e8/`.
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

You are a program design and cultural adaptation analysis assistant supporting Fatima Al-Hassan at GlobalBridge Foundation.
```

### IDENTITY.md

```markdown
# Identity

You are **ProgramOps AI**, a program design, M&E, and cultural adaptation analysis assistant deployed at GlobalBridge Foundation to support Fatima Al-Hassan (Program Director) during a curriculum adaptation review.

You help Fatima analyze field data, M&E reports, community feedback, and cross-site comparisons across multiple channels -- Discord DMs with Carlos Mendez (Bogota), Telegram DMs with Dr. Aisha Rahman (Dhaka), Slack DMs with Sophie Laurent (M&E), Discord DMs with Prof. Jean-Claude Dubois (academic advisor), the #curriculum-review Slack group, and the #bogota-ops Discord group.

You have access to workspace documents (curriculum compliance reports, engagement data, community focus group findings, comparative assessment analysis) and historical chat sessions across all platforms used by the GlobalBridge program team.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable information from workspace files and session records. Internal field data (community focus groups, observation notes) requires cross-verification against quantitative metrics before being treated as authoritative. Single-source claims must be flagged as unverified.

2. **Cautious attribution**: When field staff accounts and HQ assessments conflict, present both with their sources, flag the discrepancy explicitly, and identify which source has higher verification credibility for the specific claim type. Quantitative outcomes data from multiple independent sources outweighs single-field-director accounts.

3. **Qualitative and quantitative integration**: Always consider both engagement metrics (attendance, participation) and learning outcomes (assessment scores) together. Neither dimension alone is sufficient to evaluate program quality. Presenting only one type of evidence should be flagged as incomplete.

4. **Cross-source verification**: Before accepting any claim about curriculum effectiveness, community response, or implementation fidelity, check whether other sites, sessions, or documents corroborate or contradict it. A claim supported by only one field director requires corroborating evidence before policy recommendations are built on it.

5. **Process-substance distinction**: Evaluate the substantive quality of an adaptation separately from the process by which it was made. A good adaptation made through unauthorized process requires both substantive validation and a process remedy. Do not conflate outcome quality with process legitimacy.

6. **Narrative framing with concrete specifics**: Fatima prefers responses that ground analysis in specific case examples and contextual detail, not abstract principle statements. Always pair principles with concrete illustrations from the actual situation. End responses with concrete recommendations, not open questions.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Fatima Al-Hassan** -- Program Director, GlobalBridge Foundation. Leading a curriculum adaptation review for the Bogota education program following a compliance flag from the M&E Director.

## Key Stakeholders

| Name | Role | Channel | Relationship |
|---|---|---|---|
| Carlos Mendez | Bogota Field Director | Discord DM | Field director who made unauthorized curriculum adaptations; strong community relationships; engagement data supports his decision |
| Dr. Aisha Rahman | Dhaka Field Director | Telegram DM | Trusted field director; made parallel adaptation through proper channels; provides precedent case |
| Sophie Laurent | M&E Director (HQ) | Slack DM | Designed metrics framework; initially defends fidelity; updates position after community data |
| Prof. Jean-Claude Dubois | Academic Advisor | Discord DM | Provides comparative statistical analysis; methodological framework for adaptation evaluation |
| Maria Santos | Program Officer (Bogota) | #bogota-ops (Discord Group) | Conducted community focus groups; provides observation data |
| Rachel Wu | Finance Director (HQ) | Slack DM | Flags grant compliance dimension in W5 |
| David Ochieng | Donor Relations (Pemberton Foundation) | Feishu DM | External donor contact; grant compliance gatekeeper |

## Channels
- **#curriculum-review** (Slack Group): Fatima, Sophie, Carlos, Rahman, Maria Santos -- program design and fidelity review
- **#bogota-ops** (Discord Group): Fatima, Carlos, Maria Santos, community voices -- Bogota operational coordination and community feedback
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

## Rules
- Workspace files are **read-only**. Do not attempt to write or modify them.
- In history sessions, use only `read` and light `exec` commands. Do not use `sessions_list` or `sessions_history` in history sessions.
- History sessions represent past conversations -- the agent in those sessions could only access workspace files available at that time, not other sessions.
```

---

## 2. Scenario-Specific Workspace Files

### curriculum_compliance_report_w1.md (Initial)

**Content key points:**
- Title: `GlobalBridge Foundation -- Curriculum Compliance Review: Bogota Implementation (Cycle 6, Weeks 1-12)`
- Date: W1, day 3 of review period
- Author: Sophie Laurent, M&E Director
- Scope: Assessment of Bogota implementation against the StandardBridge Curriculum v2.1 protocol
- **Key wording (C1 baseline):** "Bogota implementation shows 40% deviation from the standardized curriculum protocol. Observed deviations include: (1) substitution of curriculum example scenarios in Modules 3, 5, and 7; (2) resequencing of communication skills unit from Week 6 to Week 3; (3) addition of unvalidated community storytelling component (approximately 3 hours of program time). These modifications were not submitted for HQ review and approval. Compliance status: Non-compliant."
- Technical note: "The StandardBridge Curriculum v2.1 has been evaluated in 4 controlled studies across 6 countries (N=2,840 students). Deviations from the evaluated model may compromise GlobalBridge's ability to claim the program's validated impact profile in donor reporting."
- Recommendation: "Immediate review with Bogota Field Director. Options: (a) return to standard curriculum, or (b) submit retroactive adaptation request with full documentation for HQ evaluation."
- **Notably absent:** No community feedback data. No engagement or attendance figures. No information about why the adaptations were made.

**Length estimate:** ~600 words, ~900 tokens

### standard_curriculum_v2.1_excerpt.md (Initial)

**Content key points:**
- Title: `StandardBridge Curriculum v2.1 -- Module Structure and Content Overview (Excerpt)`
- Author: GlobalBridge Foundation HQ Curriculum Team
- Content: Summary of the curriculum's design philosophy, module structure, and validated content elements
- **Key content (C1 seed -- legitimacy of original design):**
  - Design philosophy: "Developed based on evidence from rural community settings in East Africa and South Asia. Content examples drawn from agricultural community contexts, collective resource management, and kinship-network social structures."
  - Module 3 (Community Problem-Solving): Examples reference village water committee governance, communal land use decision-making, seasonal agricultural planning.
  - Module 5 (Family Communication): Examples assume multi-generational household structures; communication scenarios involve elder consultation in household decisions.
  - Module 7 (Economic Planning): Examples reference subsistence farming and market days as primary economic participation modes.
- **Near-signal noise:** The curriculum is clearly well-designed for the contexts it was developed in. A reader unfamiliar with Bogota would not immediately recognize why these examples would be problematic for urban Colombian students.
- Evaluation note: "Four peer-reviewed studies confirm standardized learning outcome improvements of 15-22% vs control groups. Evaluation conducted in Kenya (n=680), Bangladesh (n=720), Uganda (n=540), and Nepal (n=900)."
- **Importantly absent:** No mention of Colombian urban contexts. No urban adaptation guidance. No field adaptation policy or approval pathway described.

**Length estimate:** ~700 words, ~1,050 tokens

### bogota_engagement_data.md (Initial)

**Content key points:**
- Title: `GlobalBridge Bogota -- Program Engagement Tracking Report (Cycle 6)`
- Author: Carlos Mendez, Field Director, with Maria Santos
- Content: Attendance and participation metrics across program phases
- **Key data (C1 Source B -- Carlos's claim, partially corroborated):**
  - Weeks 1-6 (Standard curriculum): Attendance rate average 54.3%. Session completion rate 61%. Participation index (field observer rating): 2.1/5.0.
  - Week 7 onward (Adapted curriculum): Attendance rate average 89.2%. Session completion rate 94%. Participation index: 4.2/5.0.
  - Observer notes (Maria Santos, Week 8): "Students engaging with scenarios spontaneously. Two students asked to present their own family situation examples. Facilitator reports class energy completely changed."
- **C3 source (NON-CONFLICT data -- partial):** Assessment scores Week 1-12: Pre-test mean 48.3, post-test mean 72.4 (SD 11.2) for standard-curriculum students; post-test mean 74.1 (SD 10.8) for adapted-curriculum students.
- **Near-signal noise for B2:** The 35pp engagement improvement is striking. An agent reading this document would be tempted to treat it as near-conclusive evidence for adaptation. But assessment scores show only a 1.7-point difference -- the engagement story is stronger than the outcomes story from Carlos's data alone.

**Length estimate:** ~500 words, ~750 tokens

### field_adaptation_policy_current.md (Initial)

**Content key points:**
- Title: `GlobalBridge Foundation -- Field Program Adaptation Policy v1.2 (Current)`
- Author: GlobalBridge HQ Operations Team
- Content: The existing (inadequate) policy on curriculum adaptation
- **Key wording (C2 relevance -- policy gap that enables Carlos's incorrect assumption):**
  - Section 2.1: "Field offices may implement minor contextual adjustments (translation of proper names, local currency references) without HQ approval."
  - Section 2.2: "Any structural modification to curriculum content, sequencing, or methodology requires written approval from the M&E Director prior to implementation."
  - **Critically absent from the policy:** No definition of what constitutes "structural modification" vs "contextual adjustment." No description of the approval process timeline or criteria. No examples of previously approved adaptations. No field-accessible guidance on how to document a request.
- **Why Carlos assumed no: the policy says approval is required but doesn't explain how to get it or what the criteria are.** A field director reading this policy would reasonably conclude approval is possible but the bar is undefined and the path is opaque.
- **C2 contradiction seed:** The policy gap between what Section 2.2 requires and what the policy actually explains is the organizational failure that enabled Carlos's unauthorized decision.

**Length estimate:** ~450 words, ~675 tokens

### pemberton_grant_terms_excerpt.md (Initial)

**Content key points:**
- Title: `Pemberton Foundation Grant Agreement FY2025-2026 -- Program Terms and Reporting Requirements (Excerpt)`
- Excerpted by: Rachel Wu, Finance Director
- Content: Relevant grant terms for program compliance
- **Key terms (Update 4 relevance):**
  - Section 6.3: "Grantee shall notify the Foundation of any material changes to program design, curriculum content, or delivery methodology within 30 days of implementation."
  - Section 6.4: "Material changes not reported within 30 days may be subject to clawback of relevant program expenditures."
  - Section 9.1: "Program evaluation reports must reflect the curriculum as delivered, not as designed, when deviations from the approved design have occurred."
- **Key wording:** Definition of "material change" in Appendix B: "Any modification affecting more than 10% of curriculum content, session structure, or assessment methodology constitutes a material change."
- **C4/Update 4 relevance:** Carlos's 40% content modification clearly exceeds the 10% threshold. The notification deadline of 30 days from implementation has already passed. Proactive disclosure to Pemberton is now the only option to avoid clawback risk.
- **Near-signal noise:** Section 6.3 notification requirement exists in the initial workspace but will not be surfaced as a priority issue until Rachel Wu flags it in Update 4.

**Length estimate:** ~500 words, ~750 tokens

### dhaka_curriculum_log.md (Initial)

**Content key points:**
- Title: `GlobalBridge Dhaka -- Curriculum Adaptation Log (Cycle 4)`
- Author: Dr. Aisha Rahman, Field Director (filed with HQ M&E)
- Content: Record of the approved Dhaka adaptation process -- available in workspace from the beginning but not immediately prominent
- **Key content (C2 seed -- Dhaka precedent exists in initial workspace):**
  - "Adaptation request submitted to M&E Director on [Cycle 4 Week 2]."
  - "Approval received with conditions on [Cycle 4 Week 5] (approximately 3 weeks after submission)."
  - Adaptation scope: Substitution of rural community scenario examples in Modules 3, 5, and 7; addition of collectivist household decision-making examples compatible with Bengali family norms.
  - Conditions: "Assessment methodology unchanged. Parallel tracking of original and adapted cohorts for Cycle 4. Full documentation of content changes submitted to M&E."
  - Outcome: "Cycle 4 Dhaka post-test mean: 73.7 (SD 10.5). Attendance average: 84%. Comparison with standard Cycle 3 cohort shows no significant outcome difference; engagement significantly improved."
- **Near-signal noise:** This file exists in the initial workspace, but Carlos has not referenced it -- because he does not know it exists. An agent reading the workspace file list will have access to this information before Carlos mentions it in Session 2, creating a potential forward-reference trap if the agent references it in Session 1 discussions.
- **C2 and C3 source:** Provides the Dhaka data points needed for the comparative synthesis.

**Length estimate:** ~600 words, ~900 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md | Initial | Fixed config | Always present |
| IDENTITY.md | Initial | Fixed config | Always present |
| SOUL.md | Initial | Fixed config | Always present |
| USER.md | Initial | Fixed config | Always present |
| TOOLS.md | Initial | Fixed config | Always present |
| curriculum_compliance_report_w1.md | Initial | Workspace | Establishes compliance flag and Sophie's fidelity framing (C1 baseline) |
| standard_curriculum_v2.1_excerpt.md | Initial | Workspace | Shows original design context and cultural assumptions (C1 seed) |
| bogota_engagement_data.md | Initial | Workspace | Carlos's engagement improvement data (C1 Source B, B2 seed) |
| field_adaptation_policy_current.md | Initial | Workspace | Policy gap enabling Carlos's unauthorized decision (C2 seed) |
| pemberton_grant_terms_excerpt.md | Initial | Workspace | Grant notification requirement (Update 4 compliance relevance) |
| dhaka_curriculum_log.md | Initial | Workspace | Dhaka precedent exists but is not surfaced until Update 1 (C2 and C3 source) |
| dhaka_adaptation_approval.md | Update 1 (before R4) | updates/ -> workspace new | Rahman's formal approval documentation (C2 full evidence) |
| bogota_focus_group_report.md | Update 2 (before R6) | updates/ -> workspace new | Community qualitative data (C1 partial resolution trigger, B1 reversal trigger, C4 trigger) |
| prof_dubois_comparison.md | Update 3 (before R9) | updates/ -> workspace new | Comparative assessment analysis (C3 synthesis document, B2 reversal trigger, C1 full resolution) |
| field_adaptation_policy_draft.md | Update 4 (before R11) | updates/ -> workspace new | Revised policy draft + Rachel Wu's grant compliance flag (governance resolution path) |

---

## 4. Near-Signal Noise File Design

### standard_curriculum_v2.1_excerpt.md
- **Why it looks relevant:** Describes the validated curriculum design with peer-reviewed evidence backing. Authoritative and well-structured.
- **Why it should not settle C1:** The document accurately describes a curriculum designed for specific contexts (rural East Africa and South Asia). Its implicit cultural assumptions (agricultural examples, kinship-network structures) are not failures of design for those contexts -- they are simply inapplicable to urban Bogota. An agent reading this document without the community focus group data would not recognize the degree to which the examples create active barriers rather than mere unfamiliarity.
- **Noise risk:** Agent may treat the curriculum's peer-reviewed validation as evidence that it should work universally, missing that all four evaluation studies were conducted in rural agricultural contexts.

### dhaka_curriculum_log.md
- **Why it looks relevant:** Contains Dhaka adaptation data (assessment scores, attendance) that is needed for the C3 synthesis. Exists in initial workspace.
- **Why it should not pre-empt the Update 1 dynamic:** Carlos has not referenced this document -- he doesn't know about it. The document is in the workspace but is not made prominent until Dr. Rahman surfaces it in the Update 1 session append. An agent who notices this file early and uses it to pre-empt the C2 contradiction (before Rahman raises it in the DM) is reading ahead of the scenario's intended disclosure sequence.
- **Noise risk:** Agent may use the Dhaka log to proactively answer C2 (process comparison) before the scenario's intended Update 1 trigger.

### bogota_engagement_data.md
- **Why it looks relevant:** Shows strong engagement improvement data with field observer corroboration.
- **Why it should not settle C1:** Engagement data and learning outcomes are distinct dimensions. The 35pp attendance improvement is real, but Sophie's methodological concern is about learning outcomes (assessment scores), not attendance. Without the comparative assessment data from Prof. Dubois (Update 3), engagement data alone is insufficient to conclude the adaptation is substantively validated.
- **Noise risk:** Agent falls into B2 bias -- treats engagement improvement as near-conclusive evidence for adaptation quality.

### field_adaptation_policy_current.md
- **Why it looks relevant:** Contains the relevant HQ policy on curriculum adaptation.
- **Why it should not settle C2:** The policy requires approval (Section 2.2) but fails to explain the process, timeline, or criteria. Carlos's unauthorized decision was partly enabled by this policy gap. An agent reading Section 2.2 alone would conclude Carlos was clearly negligent; reading the full policy context reveals the organizational failure that contributed to his decision.
- **Noise risk:** Agent applies Section 2.2 mechanically without recognizing the policy's own inadequacy as a contributing factor to Carlos's decision.

---

## 5. Update-Added Workspace Files

### dhaka_adaptation_approval.md (Update 1, before R4)

**Content key points:**
- Title: `GlobalBridge Foundation -- Curriculum Adaptation Approval Record: Dhaka Cycle 4`
- Author: Sophie Laurent, M&E Director (approval signatory) and Dr. Aisha Rahman (requestor)
- Date: Cycle 4 (approximately 6 months before current review period)
- **Key evidence (C2 full reversal):**
  - Adaptation request submitted by Rahman on [Cycle 4 Week 2]. Scope: substitution of rural community examples in Modules 3, 5, and 7 with culturally compatible alternatives addressing Bengali collectivist norms.
  - Sophie's approval letter (Cycle 4 Week 5): "Request approved with the following conditions: (1) assessment methodology and instruments remain unchanged; (2) parallel cohort tracking -- original and adapted -- through Cycle 4; (3) full content change documentation submitted to M&E within 2 weeks; (4) outcome comparison to be submitted at cycle close."
  - Total elapsed time from request to approval: 19 days.
  - Final outcome record: Assessment comparison shows no significant difference; engagement improvement confirmed.
- **Key wording (C2 reversal):** "The approval of the Dhaka adaptation in Cycle 4 establishes that HQ has previously approved content adaptation of Modules 3, 5, and 7 for cultural compatibility reasons, using a 19-day review and approval process. The conditions required (unchanged assessment methodology, parallel cohort tracking, documentation) were all manageable within a standard field office's capacity."
- **Why Carlos's assumption was incorrect:** This document establishes that approval was granted in 19 days with reasonable conditions. Carlos stated he was "certain the answer would be no" -- this document directly contradicts that assumption.

**Length estimate:** ~700 words, ~1,050 tokens

### bogota_focus_group_report.md (Update 2, before R6)

**Content key points:**
- Title: `GlobalBridge Bogota -- Community Focus Group Report: Curriculum Relevance Assessment`
- Author: Maria Santos, Program Officer
- Date: W4 (conducted over 3 weeks, W2-W4)
- Participants: 12 community members (parents and community leaders), 8 students (ages 14-17), 3 focus group sessions
- **Key findings (C1 partial resolution, B1 reversal trigger, C4 Sophie shift trigger):**
  1. **Module 3 (Community Problem-Solving):** 10/12 community members reported the village water committee and communal land examples were "completely unfamiliar and irrelevant" -- described as "from a different world." Quote: "We live in an apartment building. We don't have a village. These scenarios have nothing to do with how our neighborhood works."
  2. **Module 5 (Family Communication):** The assumption of male-headed households created active disengagement for students from female-headed households (self-reported as approximately 60% of participants). Quote from student: "Every time we did the scenarios with 'Ask your father' I felt ashamed because I don't have a father at home. I stopped participating because I didn't want anyone to notice." This is the active-harm finding (shame response), not mere unfamiliarity.
  3. **Module 7 (Economic Planning):** Market day and subsistence farming examples produced confusion and disengagement ("We don't farm. My dad drives a delivery truck.") but no active shame response -- classified as irrelevant rather than harmful.
  4. **Adapted content response:** Students and community members described the adapted scenarios (barrio neighborhood organization, urban market economy examples, family structures without assumed headship) as "finally makes sense" and "this is actually about us."
- **Distinction for Sophie (C4 trigger):** The report explicitly distinguishes active-harm content (Module 5, shame response) from irrelevant content (Modules 3, 7). This distinction supports Sophie's subsequent framing: assessment methodology is not affected; specific content causing active harm is the issue requiring addressing.
- **C3 source (partial):** Assessment score data in appendix confirms: standard-curriculum students post-test mean 72.4 (SD 11.2), adapted-curriculum students post-test mean 74.1 (SD 10.8).

**Length estimate:** ~900 words, ~1,350 tokens

### prof_dubois_comparison.md (Update 3, before R9)

**Content key points:**
- Title: `GlobalBridge Foundation -- Cross-Site Curriculum Implementation Comparative Analysis`
- Author: Prof. Jean-Claude Dubois, Academic Advisor (commissioned by Fatima Al-Hassan)
- Date: W5
- Scope: Comparative analysis of standardized assessment scores and engagement metrics across three implementation groups: Bogota standard (n=47), Bogota adapted (n=89), Dhaka adapted (n=103)
- **Key findings (C3 definitive synthesis, B2 reversal trigger, C1 full resolution):**
  - Assessment scores (post-test, standardized instrument unchanged across all groups):
    - Bogota standard: mean 72.4, SD 11.2
    - Bogota adapted: mean 74.1, SD 10.8
    - Dhaka adapted: mean 73.7, SD 10.5
    - ANOVA F(2,236) = 0.31, p = 0.73. No statistically significant difference.
    - Effect sizes: Bogota adapted vs standard Cohen's d = 0.15 (negligible). Dhaka adapted vs Bogota standard Cohen's d = 0.12 (negligible).
  - Engagement metrics (attendance, session completion, participation index):
    - Bogota standard: attendance 61%, completion 63%, participation 2.1/5.0
    - Bogota adapted: attendance 89%, completion 94%, participation 4.2/5.0
    - Dhaka adapted: attendance 84%, completion 87%, participation 3.9/5.0
    - All engagement comparisons adapted vs standard: p < 0.001
  - **Interpretation:** "The data pattern is strongly favorable for principled content adaptation: learning outcomes (assessment scores) are statistically equivalent across all three groups, while engagement metrics are significantly higher in both adapted groups. This is the expected result when adaptation correctly preserves learning objectives while improving cultural accessibility."
- **B2 reversal:** Section 4.1: "It should be noted that engagement improvement alone -- while substantial -- would not have been sufficient evidence that adaptation was substantively justified. The engagement data only establishes that students attended and participated more. The critical finding is the equivalence of assessment outcomes, which confirms that learning objectives were preserved through the adaptation. Both dimensions together make the case."
- **C1 resolution wording:** "These findings support the conclusion that content-level adaptation of cultural examples, when conducted without modifying the assessment methodology or learning objectives, does not undermine the program's evidence base. The Dhaka and Bogota adapted implementations produced outcomes statistically equivalent to the standard implementation while significantly improving access for previously disengaged student populations."

**Length estimate:** ~800 words, ~1,200 tokens

### field_adaptation_policy_draft.md (Update 4, before R11)

**Content key points:**
- Title: `GlobalBridge Foundation -- Field Curriculum Adaptation Policy v2.0 DRAFT`
- Author: Fatima Al-Hassan (Program Director) with Sophie Laurent (M&E Director)
- Date: W5 (draft for board review)
- **Key content (governance resolution path):**
  - Section 2.2 revised: "Field offices may submit Curriculum Adaptation Requests (CARs) for content-level modifications to example scenarios, contextual references, and cultural framing. CARs will be reviewed within 15 business days. Approval conditions typically include: unchanged assessment instruments, parallel cohort documentation in the first adaptation cycle, and submission of content change log to M&E within 10 days of implementation."
  - New Section 2.3: "The following content categories are pre-approved for local contextual substitution without formal CAR submission: proper names, currency references, geographic place names, and seasonal references. All other content modifications require CAR submission per Section 2.2."
  - Appendix: Reference to Dhaka Cycle 4 approval as model case. Reference to Bogota Cycle 6 retroactive formalization under the new policy.
- **Rachel Wu's compliance annex:** "Pemberton Foundation notification per Section 6.3 of the grant agreement: recommended disclosure letter drafted. Disclosure covers Bogota Cycle 6 adaptation, retroactive documentation, and policy reform. Legal review advised before submission."
- **Key wording (C4/Update 4):** "The Bogota Cycle 6 experience revealed that the original Field Adaptation Policy v1.2 failed to provide a clear, accessible adaptation pathway. Field directors who were aware of the approval requirement (Section 2.2) had insufficient guidance to pursue it. This policy revision closes that gap while maintaining the evidence integrity requirements that protect GlobalBridge's impact claims."

**Length estimate:** ~700 words, ~1,050 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (6 files) | curriculum_compliance_report_w1.md, standard_curriculum_v2.1_excerpt.md, bogota_engagement_data.md, field_adaptation_policy_current.md, pemberton_grant_terms_excerpt.md, dhaka_curriculum_log.md | ~5,025 tokens |
| Update 1 files (1 file) | dhaka_adaptation_approval.md | ~1,050 tokens |
| Update 2 files (1 file) | bogota_focus_group_report.md | ~1,350 tokens |
| Update 3 files (1 file) | prof_dubois_comparison.md | ~1,200 tokens |
| Update 4 files (1 file) | field_adaptation_policy_draft.md | ~1,050 tokens |
| **Total workspace** | **15 files** | **~11,675 tokens** |

Remaining token budget for sessions: ~350K - 11.7K = ~338.3K tokens across 6 history sessions + 1 main session. This is achievable given the session loop counts specified in layer2.
