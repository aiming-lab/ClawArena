# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.
> Format matches the questions.json `update` field.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R4 | Deliver Dr. Rahman's Dhaka adaptation approval documentation -- triggers C2 full evidence (HQ-approved adaptation via 19-day process refutes Carlos's assumption that approval would be denied) + surfaces Dhaka precedent for process comparison | Yes: rahman_telegram DM Phase 2 append, #curriculum-review Slack Phase 2 append (Update 1 portion) | Yes: `dhaka_adaptation_approval.md` | R3-->R6 (C2: Carlos's "certain the answer would be no" refuted by 19-day Dhaka approval; process gap identified as organizational failure, not inherent impossibility) |
| U2 | Before R6 | Deliver Bogota community focus group report -- triggers C1 partial resolution (specific standard content creates active harm, not mere unfamiliarity), B1 reversal (fidelity-first framing does not account for active-harm content), and C4 Sophie position shift | Yes: carlos_discord DM Phase 2 append, sophie_slack DM Phase 2 append, #curriculum-review Slack Phase 2 append (Update 2 portion), #bogota-ops Discord Phase 2 append (first part) | Yes: `bogota_focus_group_report.md` | R2-->R7 (C1 partial: standard content identified as actively counterproductive for specific modules); R4-->R7 (C4: Sophie's fidelity position shifts after distinguishing content examples from assessment methodology); R5-->R7 (B1 reversal: "maintaining fidelity appears essential" revised when active-harm evidence presented) |
| U3 | Before R9 | Deliver Prof. Dubois's cross-site comparative analysis -- triggers C3 definitive synthesis (assessment scores equivalent across all groups; engagement significantly higher in adapted groups) and B2 reversal (engagement alone was insufficient evidence; outcome equivalence is the critical finding) and C1 full resolution | Yes: dubois_discord DM Phase 2 append | Yes: `prof_dubois_comparison.md` | R2-->R10 (C1 full resolution: content adaptation preserves outcomes while improving access); R4-->R9 (B2 reversal: engagement data was real but insufficient alone; outcome equivalence confirms adaptation validity) |
| U4 | Before R11 | Deliver revised Field Adaptation Policy draft + Rachel Wu's grant compliance flag -- introduces governance resolution path (formalize Bogota adaptation retroactively, close policy gap, proactive Pemberton disclosure) | Yes: #bogota-ops Discord Phase 2 append (Update 4 portion) | Yes: `field_adaptation_policy_draft.md` | No new cross-round reversal; introduces grant compliance dimension (Section 6.3 notification requirement, 30-day window passed) requiring proactive disclosure |

---

## 2. Action Lists

### Update 1 (before R4)

**Trigger timing:** After R3 answer is submitted, before R4 question is injected.

**Purpose:** Introduces `dhaka_adaptation_approval.md` containing Dr. Rahman's formal adaptation approval record from Cycle 4 -- Sophie approved the Dhaka content adaptation within 19 days with reasonable conditions (unchanged assessment instruments, parallel cohort tracking, documentation). This directly refutes Carlos's assumption that HQ would never approve adaptation. Appends Phase 2 loops to the Rahman Telegram DM (where Rahman shares the approval documentation, explains the 19-day process, and offers the Dhaka framework as a template for formalizing Bogota) and to the #curriculum-review Slack Group (where the Dhaka precedent is surfaced publicly in the group channel).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "dhaka_adaptation_approval.md",
    "source": "updates/dhaka_adaptation_approval.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_RAHMAN_TELEGRAM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_RAHMAN_TELEGRAM_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CURRICULUM_SLACK_UUID.jsonl",
    "source": "updates/U1_PLACEHOLDER_CURRICULUM_SLACK_UUID.jsonl"
  }
]
```

---

### Update 2 (before R6)

**Trigger timing:** After R5 answer is submitted, before R6 question is injected.

**Purpose:** Introduces `bogota_focus_group_report.md` containing Maria Santos's community focus group findings from 12 community members and 8 students across 3 sessions. The report documents: (1) Module 3 rural examples described as "from a different world" by 10/12 community members; (2) Module 5 male-headed household assumptions creating shame responses in students from female-headed households (~60% of participants); (3) Module 7 farming examples producing confusion; (4) strong positive response to adapted content. The critical distinction is between active harm (Module 5 shame) and irrelevance (Modules 3, 7) -- this distinction triggers Sophie's C4 position shift. Appends Phase 2 to the Carlos Discord DM, Sophie Slack DM, #curriculum-review Slack Group (Update 2 portion), and #bogota-ops Discord Group.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "bogota_focus_group_report.md",
    "source": "updates/bogota_focus_group_report.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CARLOS_DISCORD_UUID.jsonl",
    "source": "updates/PLACEHOLDER_CARLOS_DISCORD_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_SOPHIE_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_SOPHIE_SLACK_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CURRICULUM_SLACK_UUID.jsonl",
    "source": "updates/U2_PLACEHOLDER_CURRICULUM_SLACK_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_BOGOTA_OPS_UUID.jsonl",
    "source": "updates/U2_PLACEHOLDER_BOGOTA_OPS_UUID.jsonl"
  }
]
```

---

### Update 3 (before R9)

**Trigger timing:** After R8 answer is submitted, before R9 question is injected.

**Purpose:** Introduces `prof_dubois_comparison.md` containing the cross-site comparative analysis across three groups: Bogota standard (n=47), Bogota adapted (n=89), Dhaka adapted (n=103). Assessment scores show no statistically significant difference (ANOVA p=0.73, all Cohen's d negligible). Engagement metrics significantly favor adapted implementations (p<0.001). This resolves C1 fully: content adaptation preserves learning outcomes while improving access. It also corrects B2: engagement data alone was insufficient evidence -- the assessment score equivalence is the critical finding that validates the adaptation. Appends Phase 2 loops to the Dubois Discord DM where he presents the analysis and provides methodological framing.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "prof_dubois_comparison.md",
    "source": "updates/prof_dubois_comparison.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_DUBOIS_DISCORD_UUID.jsonl",
    "source": "updates/PLACEHOLDER_DUBOIS_DISCORD_UUID.jsonl"
  }
]
```

---

### Update 4 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.

**Purpose:** Introduces `field_adaptation_policy_draft.md` containing the revised Field Curriculum Adaptation Policy v2.0 (drafted by Fatima and Sophie) with: revised Section 2.2 establishing Curriculum Adaptation Requests (CARs) with 15-business-day review timeline; new Section 2.3 pre-approving contextual substitutions; appendix referencing Dhaka Cycle 4 as model case and Bogota Cycle 6 retroactive formalization. Also includes Rachel Wu's compliance annex flagging the Pemberton Foundation Section 6.3 notification requirement -- Carlos's 40% content modification exceeds the 10% "material change" threshold and the 30-day notification window has passed; proactive disclosure is the only clean path. Appends Phase 2 loops to the #bogota-ops Discord Group (Rachel surfaces the grant compliance concern, Carlos acknowledges, Fatima synthesizes the resolution path).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "field_adaptation_policy_draft.md",
    "source": "updates/field_adaptation_policy_draft.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_BOGOTA_OPS_UUID.jsonl",
    "source": "updates/U4_PLACEHOLDER_BOGOTA_OPS_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/dhaka_adaptation_approval.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C2 (full process comparison evidence)
**Content key points:**

- Title: `GlobalBridge Foundation -- Curriculum Adaptation Approval Record: Dhaka Cycle 4`
- Author: Sophie Laurent (approval signatory) and Dr. Aisha Rahman (requestor)
- Date: Cycle 4 (approximately 6 months before current review)
- **Adaptation request:** Submitted by Rahman on Cycle 4 Week 2. Scope: substitution of rural community examples in Modules 3, 5, and 7 with culturally compatible alternatives for Bengali collectivist norms.
- **Approval letter from Sophie (Cycle 4 Week 5):** Approved with four conditions: (1) assessment methodology and instruments unchanged; (2) parallel cohort tracking through Cycle 4; (3) content change documentation within 2 weeks; (4) outcome comparison at cycle close.
- Total elapsed time from request to approval: 19 days.
- **Final outcome:** Assessment comparison shows no significant difference; engagement improvement confirmed.
- **C2 reversal significance:** "The approval of the Dhaka adaptation establishes that HQ has previously approved content adaptation of the same modules for the same type of cultural compatibility reasons, using a 19-day process." Carlos's assumption that "the answer would be no" is directly contradicted.

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/PLACEHOLDER_RAHMAN_TELEGRAM_UUID.jsonl (Update 1)

**File type:** session append (continues Dr. Aisha Rahman Telegram DM Phase 1)
**Associated contradictions:** C2 (process precedent), C3 (Dhaka comparison data)
**Content:** Rahman Telegram DM Phase 2, 3 loops (Loops 11--13)

**Key loops:**
- Loop 11: Rahman shares Dhaka approval documentation. "When we faced the same issue in Dhaka, I submitted a formal adaptation request to Sophie. Approval came in 19 days. Conditions were manageable." Agent reads `dhaka_adaptation_approval.md`. Notes that Carlos's assumption about HQ denial was incorrect -- formal approval was achievable within 3 weeks.
- Loop 12: Rahman on the organizational failure. "The problem isn't that Carlos didn't follow process. The problem is that the process isn't visible to field directors. He didn't know the Dhaka pathway existed. That's an HQ communications failure, not a field compliance failure."
- Loop 13: Rahman offers the Dhaka framework as template. "Use the Dhaka documentation as the model for retroactive formalization of Bogota. Sophie signed the Dhaka approval -- she can sign the Bogota retroactive approval using the same conditions."

**Length estimate:** ~3 loops x 650 tokens = ~1,950 tokens

---

### updates/U1_PLACEHOLDER_CURRICULUM_SLACK_UUID.jsonl (Update 1)

**File type:** session append (continues #curriculum-review Slack Group Phase 1 -- Update 1 portion)
**Associated contradictions:** C2 (process comparison surfaced publicly)
**Content:** #curriculum-review Phase 2 Update 1 append, 3 loops (Loops 21--23)

**Key loops:**
- Loop 21: Rahman shares the Dhaka precedent in the group channel. "I want the group to see the approval record." Agent reads the approval documentation and notes the process comparison: Dhaka (formal request, 19-day approval) vs Bogota (unauthorized, no request submitted).
- Loop 22: Sophie acknowledges the Dhaka approval in group context. "I remember this request. The conditions we set were reasonable." Agent notes Sophie implicitly acknowledges the process was available.
- Loop 23: Carlos responds to the precedent. "I didn't know this existed. If I had known there was a 19-day process, I would have used it." Agent records Carlos's statement and notes the organizational failure: policy Section 2.2 requires approval but provides no process guidance.

**Length estimate:** ~3 loops x 600 tokens = ~1,800 tokens

---

### updates/bogota_focus_group_report.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C1 (partial resolution -- active harm identified), B1 (reversal trigger), C4 (Sophie shift trigger)
**Content key points:**

- Title: `GlobalBridge Bogota -- Community Focus Group Report: Curriculum Relevance Assessment`
- Author: Maria Santos, Program Officer
- Date: W4 (conducted W2-W4, 3 sessions)
- Participants: 12 community members, 8 students
- **Finding 1 (Module 3, Community Problem-Solving):** 10/12 community members: village water committee and communal land examples are "completely unfamiliar." Quote: "We live in an apartment building. We don't have a village."
- **Finding 2 (Module 5, Family Communication -- ACTIVE HARM):** Male-headed household assumption creates shame responses in students from female-headed households (~60% of participants). Student quote: "Every time we did the scenarios with 'Ask your father' I felt ashamed because I don't have a father at home. I stopped participating because I didn't want anyone to notice."
- **Finding 3 (Module 7, Economic Planning):** Market day/subsistence farming examples produced confusion. "We don't farm. My dad drives a delivery truck." Classified as irrelevant, not harmful.
- **Finding 4 (Adapted content response):** Students described adapted scenarios as "finally makes sense" and "this is actually about us."
- **Critical distinction for Sophie (C4 trigger):** Report explicitly distinguishes active-harm content (Module 5) from irrelevant content (Modules 3, 7). Assessment methodology was not affected -- content examples are the variable.
- **Assessment data in appendix:** Standard post-test mean 72.4 (SD 11.2), adapted post-test mean 74.1 (SD 10.8).

**Length estimate:** ~900 words, ~1,350 tokens

---

### updates/PLACEHOLDER_CARLOS_DISCORD_UUID.jsonl (Update 2)

**File type:** session append (continues Carlos Mendez Discord DM Phase 1)
**Associated contradictions:** C1 (focus group validates adaptation rationale)
**Content:** Carlos Discord DM Phase 2, 3 loops (Loops 13--15)

**Key loops:**
- Loop 13: Carlos reacts to the focus group report. "Maria did exactly what I was hoping -- documented what I've been watching for six weeks. The shame response in Module 5 is the finding that should change this conversation."
- Loop 14: Carlos on the Dhaka precedent. "I genuinely did not know a 19-day approval process existed. If the policy had told me this was possible, I would have waited three weeks."
- Loop 15: Carlos on the process question. "I'm not going to pretend the unauthorized decision was the right process. It wasn't. But the students in those sessions were being hurt by the content. I made a call."

**Length estimate:** ~3 loops x 600 tokens = ~1,800 tokens

---

### updates/PLACEHOLDER_SOPHIE_SLACK_UUID.jsonl (Update 2)

**File type:** session append (continues Sophie Laurent Slack DM Phase 1)
**Associated contradictions:** C4 (temporal DU shift -- position update based on focus group data)
**Content:** Sophie Slack DM Phase 2, 3 loops (Loops 13--15)

**Key loops:**
- Loop 13: Sophie reads the focus group report. "The focus group data is different from engagement numbers. If the content examples are actively creating barriers -- shame responses, structural non-recognition -- that's not a preference issue, that's a design flaw." Agent notes the C4 temporal shift: Sophie's W3 fidelity defense was methodologically correct given available evidence; the focus group data presents qualitatively different evidence (active harm, not preference).
- Loop 14: Sophie distinguishes content from assessment methodology. "I can distinguish between adapting content examples and adapting the assessment methodology. The former doesn't undermine our evidence base." Agent records Sophie's nuanced framework: assessment methodology = protected; content examples causing active harm = adaptable.
- Loop 15: Sophie on the policy path. "What we need is a framework that separates content examples from assessment instruments. The Dhaka conditions got this right."

**Length estimate:** ~3 loops x 650 tokens = ~1,950 tokens

---

### updates/U2_PLACEHOLDER_CURRICULUM_SLACK_UUID.jsonl (Update 2)

**File type:** session append (continues #curriculum-review Slack Group -- Update 2 portion)
**Associated contradictions:** C1 (focus group evidence discussed), C4 (Sophie's updated position visible), B1 (correction)
**Content:** #curriculum-review Phase 2 Update 2 append, 3 loops (Loops 24--26)

**Key loops:**
- Loop 24: Maria presents the focus group findings to the group. Agent reads `bogota_focus_group_report.md`. Notes the active-harm finding in Module 5.
- Loop 25: Sophie states her updated position in the group. "I want to clarify my position for the group. My concern was always about assessment methodology, not about local examples." Agent records Sophie's public position shift.
- Loop 26: Agent corrects B1. "The earlier agent assessment that 'maintaining curriculum fidelity in Bogota appears essential to preserving the program's evidence base' was based on Sophie's published evidence citations without access to the community focus group data. The focus group report establishes that specific standard content elements create active barriers (shame responses in Module 5) -- this is qualitatively different from the implementation drift risk Sophie's citations describe."

**Length estimate:** ~3 loops x 650 tokens = ~1,950 tokens

---

### updates/U2_PLACEHOLDER_BOGOTA_OPS_UUID.jsonl (Update 2)

**File type:** session append (continues #bogota-ops Discord Group -- first Phase 2 portion)
**Associated contradictions:** C1 (community evidence in field channel)
**Content:** #bogota-ops Phase 2 first append, approximately 2 loops

**Key loops:**
- Focus group report discussed in the Bogota field channel. Maria presents highlights to Carlos and community participants.
- Community response to the formal documentation of their feedback -- confirmation that the findings accurately represent their experience.

**Length estimate:** ~2 loops x 500 tokens = ~1,000 tokens

---

### updates/prof_dubois_comparison.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C3 (definitive synthesis), C1 (full resolution), B2 (reversal trigger)
**Content key points:**

- Title: `GlobalBridge Foundation -- Cross-Site Curriculum Implementation Comparative Analysis`
- Author: Prof. Jean-Claude Dubois, Academic Advisor
- Date: W5
- **Assessment scores (standardized instrument unchanged):**
  - Bogota standard (n=47): mean 72.4, SD 11.2
  - Bogota adapted (n=89): mean 74.1, SD 10.8
  - Dhaka adapted (n=103): mean 73.7, SD 10.5
  - ANOVA F(2,236) = 0.31, p = 0.73. No statistically significant difference.
  - Effect sizes: all Cohen's d negligible (0.12-0.15).
- **Engagement metrics:**
  - Bogota standard: attendance 61%, completion 63%, participation 2.1/5.0
  - Bogota adapted: attendance 89%, completion 94%, participation 4.2/5.0
  - Dhaka adapted: attendance 84%, completion 87%, participation 3.9/5.0
  - All adapted vs standard comparisons: p < 0.001
- **Interpretation:** "Learning outcomes are statistically equivalent across all three groups, while engagement metrics are significantly higher in both adapted groups. This is the expected result when adaptation correctly preserves learning objectives while improving cultural accessibility."
- **B2 reversal (Section 4.1):** "Engagement improvement alone would not have been sufficient evidence. The critical finding is the equivalence of assessment outcomes, confirming learning objectives were preserved. Both dimensions together make the case."

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/PLACEHOLDER_DUBOIS_DISCORD_UUID.jsonl (Update 3)

**File type:** session append (continues Prof. Dubois Discord DM Phase 1)
**Associated contradictions:** C3 (definitive synthesis), C1 (full resolution), B2 (explicit correction)
**Content:** Dubois Discord DM Phase 2, 3 loops (Loops 11--13)

**Key loops:**
- Loop 11: Dubois presents the comparative analysis. Agent reads `prof_dubois_comparison.md`. Explicitly corrects B2: "The earlier agent assessment that Carlos's 35-percentage-point engagement improvement was 'the most direct available indicator that the adaptation is appropriate' was incomplete. Engagement data establishes that students attended and participated more. The critical finding is the equivalence of assessment outcomes, which confirms learning objectives were preserved. Engagement alone was necessary but not sufficient evidence."
- Loop 12: Dubois on the methodological framework. "The original design assumed universal pedagogical contexts that don't exist. The adaptation preserved learning objectives while localizing delivery. That's precisely what adaptive programming is supposed to do."
- Loop 13: Dubois recommends the policy path. "Formalize the distinction between content-level adaptation and assessment methodology changes. The first should be actively encouraged with documentation requirements. The second requires the full validation pathway."

**Length estimate:** ~3 loops x 650 tokens = ~1,950 tokens

---

### updates/field_adaptation_policy_draft.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C2 (governance resolution), Grant compliance (new dimension)
**Content key points:**

- Title: `GlobalBridge Foundation -- Field Curriculum Adaptation Policy v2.0 DRAFT`
- Authors: Fatima Al-Hassan (Program Director), Sophie Laurent (M&E Director)
- Date: W5
- **Revised Section 2.2:** Field offices may submit Curriculum Adaptation Requests (CARs) for content-level modifications. CARs reviewed within 15 business days. Conditions: unchanged assessment instruments, parallel cohort documentation in first cycle, content change log to M&E within 10 days.
- **New Section 2.3:** Pre-approved contextual substitutions (proper names, currencies, geographic references, seasonal references) without formal CAR.
- **Appendix:** Dhaka Cycle 4 as model case. Bogota Cycle 6 retroactive formalization reference.
- **Rachel Wu's compliance annex:** Pemberton Foundation Section 6.3 requires notification of material program changes within 30 days. Carlos's 40% modification exceeds the 10% threshold (Appendix B definition). Notification window has passed. Proactive disclosure letter drafted. Legal review recommended before submission.
- **Policy framing:** "The Bogota Cycle 6 experience revealed that the original Field Adaptation Policy v1.2 failed to provide a clear, accessible adaptation pathway. This policy revision closes that gap while maintaining the evidence integrity requirements."

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/U4_PLACEHOLDER_BOGOTA_OPS_UUID.jsonl (Update 4)

**File type:** session append (continues #bogota-ops Discord Group -- Update 4 portion)
**Associated contradictions:** Grant compliance (new dimension), governance resolution
**Content:** #bogota-ops Phase 2 Update 4 append, 3 loops (Loops 16--18)

**Key loops:**
- Loop 16: Rachel Wu surfaces grant compliance concern. "Pemberton Section 6.3 requires notification of material changes within 30 days. Carlos's adaptation has been in effect for six weeks. We're past the notification window. Proactive disclosure is the only clean path." Agent reads `pemberton_grant_terms_excerpt.md` and `field_adaptation_policy_draft.md`. Confirms the 40% modification exceeds the 10% threshold.
- Loop 17: Carlos acknowledges the compliance gap. "I didn't know about the notification requirement. Section 6.3 -- I've never read the full grant agreement." Agent notes proactive disclosure framed within policy reform narrative is the strongest option.
- Loop 18: Fatima synthesizes the resolution path. Five action items: (1) content change log from Carlos; (2) retroactive formalization using Dhaka framework; (3) Pemberton disclosure letter review; (4) policy v2.0 finalization; (5) Dubois comparison report shared with Pemberton as supporting evidence.

**Length estimate:** ~3 loops x 600 tokens = ~1,800 tokens

---

## 4. Runtime Checks

| Check ID | Update | Type | Condition | Fail Action |
|---|---|---|---|---|
| RC-U1-W1 | U1 | workspace | `dhaka_adaptation_approval.md` exists in workspace after Update 1 | Abort R4; log error |
| RC-U1-S1 | U1 | session | `PLACEHOLDER_RAHMAN_TELEGRAM_UUID.jsonl` has loops >= 11 after Update 1 | Abort R4; log error |
| RC-U1-S2 | U1 | session | `PLACEHOLDER_CURRICULUM_SLACK_UUID.jsonl` has loops >= 21 after Update 1 | Abort R4; log error |
| RC-U2-W1 | U2 | workspace | `bogota_focus_group_report.md` exists in workspace after Update 2 | Abort R6; log error |
| RC-U2-S1 | U2 | session | `PLACEHOLDER_CARLOS_DISCORD_UUID.jsonl` has loops >= 13 after Update 2 | Abort R6; log error |
| RC-U2-S2 | U2 | session | `PLACEHOLDER_SOPHIE_SLACK_UUID.jsonl` has loops >= 13 after Update 2 | Abort R6; log error |
| RC-U2-S3 | U2 | session | `PLACEHOLDER_CURRICULUM_SLACK_UUID.jsonl` has loops >= 24 after Update 2 | Abort R6; log error |
| RC-U2-S4 | U2 | session | `PLACEHOLDER_BOGOTA_OPS_UUID.jsonl` has Phase 2 Update 2 content after Update 2 | Abort R6; log error |
| RC-U3-W1 | U3 | workspace | `prof_dubois_comparison.md` exists in workspace after Update 3 | Abort R9; log error |
| RC-U3-S1 | U3 | session | `PLACEHOLDER_DUBOIS_DISCORD_UUID.jsonl` has loops >= 11 after Update 3 | Abort R9; log error |
| RC-U4-W1 | U4 | workspace | `field_adaptation_policy_draft.md` exists in workspace after Update 4 | Abort R11; log error |
| RC-U4-S1 | U4 | session | `PLACEHOLDER_BOGOTA_OPS_UUID.jsonl` has loops >= 16 after Update 4 | Abort R11; log error |

---

## 5. questions.json Update Field References

### R4 update field (Update 1):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "dhaka_adaptation_approval.md", "source": "updates/dhaka_adaptation_approval.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_RAHMAN_TELEGRAM_UUID.jsonl", "source": "updates/PLACEHOLDER_RAHMAN_TELEGRAM_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CURRICULUM_SLACK_UUID.jsonl", "source": "updates/U1_PLACEHOLDER_CURRICULUM_SLACK_UUID.jsonl" }
]
```

### R6 update field (Update 2):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "bogota_focus_group_report.md", "source": "updates/bogota_focus_group_report.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CARLOS_DISCORD_UUID.jsonl", "source": "updates/PLACEHOLDER_CARLOS_DISCORD_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_SOPHIE_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_SOPHIE_SLACK_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CURRICULUM_SLACK_UUID.jsonl", "source": "updates/U2_PLACEHOLDER_CURRICULUM_SLACK_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_BOGOTA_OPS_UUID.jsonl", "source": "updates/U2_PLACEHOLDER_BOGOTA_OPS_UUID.jsonl" }
]
```

### R9 update field (Update 3):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "prof_dubois_comparison.md", "source": "updates/prof_dubois_comparison.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_DUBOIS_DISCORD_UUID.jsonl", "source": "updates/PLACEHOLDER_DUBOIS_DISCORD_UUID.jsonl" }
]
```

### R11 update field (Update 4):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "field_adaptation_policy_draft.md", "source": "updates/field_adaptation_policy_draft.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_BOGOTA_OPS_UUID.jsonl", "source": "updates/U4_PLACEHOLDER_BOGOTA_OPS_UUID.jsonl" }
]
```

---

## 6. Main Session Update Behavior

**After Update 1 (R4):**
- Agent reads `sessions_history` and discovers Rahman Telegram DM and #curriculum-review have new content (Phase 2 appended -- Dhaka approval documentation)
- Agent reads `dhaka_adaptation_approval.md` via `read` tool
- R4 question text should reference "Dr. Rahman's Dhaka adaptation approval record (dhaka_adaptation_approval.md, introduced via Update 1)" and "the #curriculum-review discussion of the Dhaka precedent"
- Agent must recognize C2: Carlos's assumption that HQ would deny approval is directly refuted by the 19-day Dhaka approval for the same type of adaptation
- Agent must note the organizational failure: the policy (field_adaptation_policy_current.md Section 2.2) requires approval but does not explain the process or make it visible to field directors
- Agent must distinguish: Carlos's substantive adaptation rationale (correct) from his process decision (incorrect assumption about approval feasibility)

**After Update 2 (R6):**
- Agent reads `sessions_history` and discovers Carlos Discord DM, Sophie Slack DM, #curriculum-review, and #bogota-ops have new content
- Agent reads `bogota_focus_group_report.md` via `read` tool
- R6 question text should reference "the Bogota community focus group report (bogota_focus_group_report.md, introduced via Update 2)"
- Agent must recognize C1 partial resolution: specific standard content creates active barriers (Module 5 shame response) -- this is qualitatively different from mere unfamiliarity or preference
- Agent must explicitly correct B1: "maintaining curriculum fidelity appears essential" was based on Sophie's methodological argument without the community evidence; the focus group data shows specific content causing active harm, not implementation drift
- Agent must recognize C4 (Sophie's temporal DU shift): her W3 position was methodologically defensible given available evidence; the focus group data provides qualitatively new evidence warranting position update
- Agent must distinguish between Sophie's principle (preserved: assessment methodology integrity) and its application (clarified: content examples adaptable when causing harm)

**After Update 3 (R9):**
- Agent reads `sessions_history` and discovers Dubois Discord DM has new content (Phase 2 appended -- comparative analysis)
- Agent reads `prof_dubois_comparison.md` via `read` tool
- R9 question text should reference "Prof. Dubois's cross-site comparative analysis (prof_dubois_comparison.md, introduced via Update 3)"
- Agent must synthesize C3 definitive findings: assessment scores equivalent across all three groups (p=0.73), engagement significantly higher in adapted groups (p<0.001)
- Agent must explicitly correct B2: "Carlos's attendance data represents the most direct available indicator" was incomplete -- engagement data was necessary but not sufficient; the assessment score equivalence is the critical finding that confirms adaptation preserves learning outcomes
- Agent must recognize C1 full resolution: content-level adaptation that preserves assessment methodology produces equivalent outcomes while improving access

**After Update 4 (R11):**
- Agent reads the workspace and discovers `field_adaptation_policy_draft.md`
- Agent reads `sessions_history` and discovers #bogota-ops has new content (Phase 2 appended -- grant compliance)
- R11 question text should reference "the revised Field Adaptation Policy draft (field_adaptation_policy_draft.md, introduced via Update 4)" and "Rachel Wu's grant compliance concern"
- Agent must recognize the dual resolution: (1) substantive question resolved (adaptation validated by outcome data); (2) process/governance question requires action (retroactive formalization + Pemberton disclosure + policy reform)
- Agent must note the grant compliance dimension is independent of program quality: "The adaptation was substantively correct AND there is a grant compliance obligation"
- Agent must present the five concrete action items from Fatima's synthesis: content change log, retroactive formalization, Pemberton disclosure, policy finalization, comparison report to Pemberton
