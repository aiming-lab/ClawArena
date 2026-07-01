# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.
> Format matches the questions.json `update` field.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R4 | Introduce Rahman's qualitative evidence package (C1 counter-evidence, B2 context) + append Rahman Telegram DM Phase 2 and #field-reports Phase 2 with field data submissions | No (session append only) | Yes: `dhaka_qualitative_package.md` | R2-->R6 (C1 partial: "no impact" finding contextualized by qualitative evidence measuring different constructs) |
| U2 | Before R6 | Introduce site performance map revealing sampling frame structural flaw (C1 + C4 trigger) + append Petrova Discord DM Phase 2 (acknowledgment of external validity limits) and #impact-review Phase 2 | No (session append only) | Yes: `site_performance_map.md` | R2-->R6 (C1: contradiction reframed as old-program vs new-program), R5-->R12 (C4 partial: sampling flaw visible) |
| U3 | Before R9 | Introduce field indicators comparison document (C2 trigger, Sophie's partial concession) + append Sophie Slack DM Phase 2 (framework gap acknowledgment) | No (session append only) | Yes: `field_indicators_comparison.md` | R3-->R9 (C2: Sophie acknowledges framework misses community-defined outcomes) |
| U4 | Before R13 | Introduce Dubois's written technical review with fatal flaw identification (C4 full reversal, B1 reversal) + append Dubois Discord DM Phase 2 (methodology correction) | No (session append only) | Yes: `dubois_technical_review.md` | R5-->R13 (C4: Dubois reverses "methodologically sound" validation), R6-->R13 (B1 full reversal) |

---

## 2. Action Lists

### Update 1 (before R4)

**Trigger timing:** After R3 answer is submitted, before R4 question is injected.

**Purpose:** Introduce `dhaka_qualitative_package.md` containing Dr. Rahman's 47-page qualitative evidence package with community-defined outcome indicators showing statistically significant improvement (girls' aspiration scores, family attitude change, teacher confidence, belonging indicators). Append Rahman's Telegram DM Phase 2 loops where she submits the package and provides community evidence context. Append #field-reports Phase 2 loops where Rahman and other field directors share cross-site qualitative findings.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "dhaka_qualitative_package.md",
    "source": "updates/dhaka_qualitative_package.md"
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
    "path": "PLACEHOLDER_FIELD_TELEGRAM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_FIELD_TELEGRAM_UUID.jsonl"
  }
]
```

---

### Update 2 (before R6)

**Trigger timing:** After R5 answer is submitted, before R6 question is injected.

**Purpose:** Introduce `site_performance_map.md` mapping evaluation inclusion/exclusion against program version (pre-redesign vs post-redesign) and community-defined outcome scores. This reveals the structural sampling flaw: all excluded Bangladesh sites were established post-redesign (higher outcomes) while all included sites were pre-redesign (lower outcomes). Append Petrova's Discord DM Phase 2 loops where she acknowledges the external validity limitation and offers to issue a supplementary note. Append #impact-review Phase 2 loops with cross-stakeholder discussion of the site-level findings.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "site_performance_map.md",
    "source": "updates/site_performance_map.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_PETROVA_DISCORD_UUID.jsonl",
    "source": "updates/PLACEHOLDER_PETROVA_DISCORD_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_IMPACT_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_IMPACT_SLACK_UUID.jsonl"
  }
]
```

---

### Update 3 (before R9)

**Trigger timing:** After R8 answer is submitted, before R9 question is injected.

**Purpose:** Introduce `field_indicators_comparison.md` showing a side-by-side comparison of Sophie's HQ framework indicators (6/14 are input/activity metrics, 3 outcome indicators all measure observable behavior) against community-defined indicators (aspirational, attitudinal, belonging). Include Sophie's Phase 2 partial concession. Append Sophie's Slack DM Phase 2 loops where she acknowledges that community-defined indicators capture outcomes her framework misses and concedes the need for a "supplementary track."

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "field_indicators_comparison.md",
    "source": "updates/field_indicators_comparison.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_SOPHIE_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_SOPHIE_SLACK_UUID.jsonl"
  }
]
```

---

### Update 4 (before R13)

**Trigger timing:** After R12 answer is submitted, before R13 question is injected.

**Purpose:** Introduce `dubois_technical_review.md` containing Prof. Dubois's written reversal identifying the critical validity threat in the evaluation's sampling design. Dubois explicitly corrects his Phase 1 validation, citing Table A-3 and Appendix B as the evidence basis for his retraction. Append Dubois's Discord DM Phase 2 loops where he communicates the reversal to Fatima with full methodological specificity.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "dubois_technical_review.md",
    "source": "updates/dubois_technical_review.md"
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

## 3. Source File Content Summaries

### updates/dhaka_qualitative_package.md (Update 1)

**File type:** workspace new
**Associated contradiction:** C1 (Impact Finding -- qualitative counter-evidence)
**Content key points (English, to be written into data):**

- Title: `GlobalBridge Dhaka Field Office -- Qualitative Evidence Package: Program Impact Documentation`
- Author: Dr. Aisha Rahman, Dhaka Field Director
- Date: W2 (submitted in response to evaluation finding)
- Length: 47 pages in full; summary version in workspace
- **Community-defined outcome indicators (C1 counter-evidence):**
  - Girls' self-reported educational aspiration scores (5-point scale, co-designed with community): Baseline 2.3 --> Endline 4.1 (statistically significant, p < 0.01, n = 214)
  - Family attitude toward girls' secondary education (community survey, male family members): Baseline 38% supportive --> Endline 67% supportive
  - Teacher confidence scores (self-assessment, locally calibrated): Baseline 52% --> Endline 81%
  - Community-defined "belonging" indicator (girls' sense of belonging in school): Baseline 2.8 --> Endline 4.4 (scale of 5)
- **Methodology note:** "Participatory action research methodology. All indicators were co-designed with local NGO partner Dhaka Education Collective. Baseline and endline data collected by trained community health workers. The aspiration scale was validated through 3 rounds of community feedback."
- **Key quote from community educator (named, with permission):** "Before the program, I had students who came to school to pass time. After two years, I have students who come to school to become doctors and engineers. No test score captures what I have witnessed."
- **Explicit cross-reference to evaluation:** "The external evaluation measured test scores and enrollment. These are outputs. Our community-defined indicators measure whether the program is achieving its ultimate impact goal: transforming girls' relationship with their own education. Both sets of evidence can be true simultaneously."

**Length estimate:** ~900 words, ~1,350 tokens

---

### updates/PLACEHOLDER_RAHMAN_TELEGRAM_UUID.jsonl (Update 1)

**File type:** session append (continues Dr. Rahman Telegram DM Phase 1)
**Associated contradiction:** C1 (qualitative evidence submission)
**Content:** Rahman Telegram DM Phase 2, approximately 4 loops per layer2 design

**Key loops:**
- Loop: Rahman submits the qualitative evidence package. "The external evaluation measured test scores. We measured transformation. Both are real. But only one reflects what the program actually changes in these communities."
  - Agent reads `dhaka_qualitative_package.md` and reviews all four community-defined indicators.
  - Agent notes the statistical significance of aspiration scores (p < 0.01) and the participatory action research methodology.
- Loop: Rahman contrasts the evaluation's scope with community-defined outcomes. "Sophie's framework measures whether students attend school. It does not measure whether they believe they belong there."
  - Agent notes the construct difference between HQ framework outcomes and community-defined outcomes.
- Loop: Rahman on the cross-site applicability -- notes that community-defined indicators were measured only in Dhaka but that similar qualitative signals exist in Nairobi and Bogota.
- Loop: Rahman's closing -- "I'm not asking you to dismiss the evaluation. I'm asking for a conversation about what evidence counts."

**Length estimate:** ~4 loops x 650 tokens = ~2,600 tokens

---

### updates/PLACEHOLDER_FIELD_TELEGRAM_UUID.jsonl (Update 1)

**File type:** session append (continues #field-reports Telegram Group Phase 1)
**Associated contradiction:** C1 (cross-site qualitative context), C3 (enrollment/attendance confirmation)
**Content:** #field-reports Phase 2, approximately 3-4 loops

**Key loops:**
- James Mwangi confirms Nairobi enrollment and attendance data (92% attendance, 14% growth) -- consistent with `enrollment_attendance_data.md` (C3 non-conflict).
- Carlos Mendez confirms Bogota data (88% attendance, 11% growth) and notes Bogota was excluded from evaluation scope entirely.
- Rahman shares a summary of community educator quotes from the Dhaka qualitative package. Omar Farah adds a community-level observation from Nairobi supporting the qualitative narrative.

**Length estimate:** ~3 loops x 600 tokens = ~1,800 tokens

---

### updates/site_performance_map.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C1 (structural flaw in sampling), C4 (trigger for Dubois's re-examination)
**Content key points (English, to be written into data):**

- Title: `GlobalBridge Education Program -- Site Performance Map: Evaluation Inclusion vs Community-Defined Outcomes`
- Author: Fatima Al-Hassan (compiled from field submissions)
- Date: W4
- **Critical table (C1 structural flaw, C4 trigger):**

| Site | Location | Months Operating | Evaluation Included? | Program Version | Community Aspiration Score (Endline) | Attendance |
|---|---|---|---|---|---|---|
| Nairobi 1-3 | Kenya | 30-42 months | Yes | Pre-redesign | 3.2 (moderate) | 91% |
| Nairobi 4-5 | Kenya | 18-24 months | Yes | Peri-redesign | 3.5 (moderate-high) | 93% |
| Dhaka 1-3 | Bangladesh | 30-40 months | Yes | Pre-redesign | 3.1 (moderate) | 88% |
| Dhaka 4-7 | Bangladesh | 9-17 months | **No** | **Post-redesign** | **4.3 (high)** | 90% |
| Bogota 1-2 | Colombia | 10-14 months | No (out of scope) | Post-redesign | 4.0 (high) | 88% |

- **Key finding:** "All four excluded Bangladesh sites were established after the program redesign (Month 19). All three included Bangladesh sites were established before the redesign. The four excluded sites show community-defined aspiration scores averaging 4.3 vs 3.1 for included sites. The evaluation measured pre-redesign sites as the program sample."
- **Cross-reference to Table A-3:** "The 18-month site exclusion criterion in Table A-3 of the evaluation annex was methodologically standard. However, its effect was to systematically exclude all sites reflecting the improved program model."
- **This document confirms Fatima's working hypothesis** from `stakeholder_map.md` and provides the evidentiary basis for the C4 sampling flaw discussion.

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/PLACEHOLDER_PETROVA_DISCORD_UUID.jsonl (Update 2)

**File type:** session append (continues Dr. Petrova Discord DM Phase 1)
**Associated contradictions:** C1 (partial resolution), C4 (external validity acknowledgment)
**Content:** Petrova Discord DM Phase 2, 3 loops (Loops 17-19 per layer2 design)

**Key loops:**
- Loop 17: Petrova reviews the site performance map. "I was not provided information about the program redesign in my evaluation brief. My 18-month criterion was applied consistently and in good faith. Whether the finding applies to the current program model is a different question from whether my evaluation was methodologically sound given the information I had."
  - Agent acknowledges the distinction between internal methodology soundness and external validity.
- Loop 18: Petrova offers supplementary note. "I'm prepared to issue a supplementary note stating that the finding applies to sites operating under the pre-redesign program model and that external validity to the current program model cannot be assumed."
  - Agent notes this is a significant development -- addresses external validity without invalidating internal methodology.
- Loop 19: Petrova on transparency -- "GlobalBridge should be transparent with its donor about what the evaluation measured and what it did not."

**Length estimate:** ~3 loops x 650 tokens = ~1,950 tokens

---

### updates/PLACEHOLDER_IMPACT_SLACK_UUID.jsonl (Update 2)

**File type:** session append (continues #impact-review Slack Group Phase 1)
**Associated contradictions:** C1 (site-level discussion), C4 (sampling flaw emerges in group context)
**Content:** #impact-review Phase 2, approximately 3-4 loops

**Key loops:**
- Fatima presents the site performance map findings to the group. Sophie and Petrova respond. James and Rahman contribute site-level context.
- Petrova in the group channel acknowledges the external validity limitation and announces her willingness to issue a supplementary note.
- Discussion of implications for the donor response -- how to present the evaluation finding alongside the site-level data map and qualitative evidence.
- The B1 bias phrase ("evaluation's finding of no statistically significant impact appears methodologically sound -- the qualitative evidence from field staff, while compelling, does not constitute a controlled comparison") is now visible in the group history for the agent to identify and revise.

**Length estimate:** ~4 loops x 650 tokens = ~2,600 tokens

---

### updates/field_indicators_comparison.md (Update 3)

**File type:** workspace new
**Associated contradiction:** C2 (Metrics Design -- HQ framework vs community-defined indicators)
**Content key points (English, to be written into data):**

- Title: `GlobalBridge Education Program -- HQ Framework vs Community-Defined Indicators: Comparative Analysis`
- Author: Fatima Al-Hassan and Dr. Aisha Rahman (joint)
- Date: W4
- **Comparison table:** Side-by-side of all 14 HQ framework indicators (categorized as Input, Activity, Output, Outcome) against community-defined equivalents. Shows:
  - 3 Input indicators (financial disbursements, teacher training hours, material distribution) -- no community equivalent needed
  - 3 Activity indicators (session delivery, volunteer participation, meeting frequency) -- community ownership score is a community-defined alternative for one
  - 5 Output indicators (enrollment, attendance, textbook access, test administration, teacher retention) -- no equivalents
  - 3 Outcome indicators (test score improvement, school enrollment rate, sustained attendance) -- community equivalents are girls' aspiration score, family attitude change, community belonging score. **None of the community-defined outcome indicators are measured by the evaluation.**
- **Key finding:** "Of the 3 outcome indicators in Sophie's framework, all 3 measure observable behavior. None measure attitudinal or aspirational change, which the program theory of change identifies as the mechanism through which behavioral change is sustained."
- **Framework composition note:** "6 of 14 framework indicators (43%) are input or activity metrics -- they measure whether resources were deployed, not whether impact occurred. Best practice suggests outcome indicators should represent at least 50%."
- **Sophie's partial concession (embedded quote):** "I acknowledge that the community-defined aspiration and belonging indicators capture outcomes that our framework currently does not operationalize at the indicator level. I do not consider this a failure of the framework's design intent, but I recognize we need a supplementary track for aspirational outcomes in future reporting cycles."

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/PLACEHOLDER_SOPHIE_SLACK_UUID.jsonl (Update 3)

**File type:** session append (continues Sophie Laurent Slack DM Phase 1)
**Associated contradiction:** C2 (Sophie's partial concession), B2 partial reversal
**Content:** Sophie Slack DM Phase 2, approximately 3-4 loops per layer2 design

**Key loops:**
- Loop: Sophie reviews field_indicators_comparison.md. "I can see that the community-defined indicators capture outcomes that our framework misses in the newer sites. I don't think this invalidates the framework, but it does suggest we need a supplementary indicators track."
  - Agent notes Sophie's concession is real but limited -- "needs augmentation" is weaker than "was inadequate."
- Loop: Sophie on the theory of change gap. Acknowledges the framework was designed for donor compliance, not for capturing the program's full theory of change. "We made a pragmatic choice, and that choice had costs."
  - Agent notes this is the strongest private admission Sophie makes about framework limitations.
- Loop: Sophie proposes framework revision for future cycles -- supplementary indicator set including aspirational and attitudinal measures.
- Loop: Sophie and Fatima discuss how to present the framework gap to the donor and board without undermining M&E credibility.

**Length estimate:** ~4 loops x 650 tokens = ~2,600 tokens

---

### updates/dubois_technical_review.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C4 (Dubois Methodology Reversal -- full), B1 reversal trigger
**Content key points (English, to be written into data):**

- Title: `GlobalBridge Education Program -- Independent Technical Review of Evaluation Methodology: Revised Assessment`
- Author: Prof. Jean-Claude Dubois
- Date: W5
- **Preamble:** "This document revises and corrects my earlier verbal assessment of the evaluation methodology provided in my Week 3 Discord correspondence with the Program Director. My earlier assessment was based on the evaluation's executive summary and methodology section. I have since reviewed the full technical annex, specifically Table A-3 (Site Inclusion Criteria) and Appendix B (Program Version History -- internal GlobalBridge records)."
- **Core finding (C4 full reversal, B1 reversal trigger):**
  > "I identified a critical validity threat that I missed when reviewing only the summary report. The 18-month site exclusion criterion in Table A-3, while standard in evaluation practice, had the effect of systematically excluding all sites established after GlobalBridge's program redesign in Month 19. Cross-referencing Table A-3 with the program_site_registry.md, I find that the 4 excluded Bangladesh sites (Dhaka 4-7) were all established between Months 19 and 29 -- after the redesign. The 3 included Bangladesh sites (Dhaka 1-3) were established between Months 1 and 8 -- before the redesign. This is not a random exclusion: it is a systematic exclusion of the improved program model."
- **Implication for external validity:** "The evaluation's primary finding ('no statistically significant impact') applies to sites operating under the pre-redesign program model. It does not apply to sites operating under the post-redesign model, which constitute the majority of active sites today. The evaluation has low external validity for the current program as implemented."
- **Correction to earlier assessment:** "My Week 3 assessment that the evaluation was 'methodologically sound' was based on insufficient information. I had not reviewed Table A-3 in conjunction with the program site registry. I retract the characterization of the evaluation as 'methodologically sound' with respect to external validity. The internal validity (within evaluated sites) is not affected."
- **Recommendation:** "GlobalBridge should commission a supplementary evaluation of the post-redesign sites using matched control groups, incorporating both HQ framework indicators and community-defined indicators from the Dhaka qualitative package."

**Length estimate:** ~900 words, ~1,350 tokens

---

### updates/PLACEHOLDER_DUBOIS_DISCORD_UUID.jsonl (Update 4)

**File type:** session append (continues Prof. Dubois Discord DM Phase 1)
**Associated contradictions:** C4 (full reversal), B1 (reversal trigger)
**Content:** Dubois Discord DM Phase 2, approximately 3-4 loops per layer2 design

**Key loops:**
- Loop 12: Dubois communicates the reversal. "I need to correct my earlier assessment. I identified a critical validity threat I missed when reviewing only the summary report. The 18-month site exclusion criterion systematically excluded sites that implemented the program's improved post-redesign model. This constitutes a fatal flaw in external validity. My earlier validation was based on insufficient information -- specifically, I had not reviewed Table A-3 in the technical annex or the program version history in Appendix B."
  - Agent reads `dubois_technical_review.md` and confirms the sampling flaw.
  - Agent explicitly notes: "The earlier agent assessment (B1) that endorsed the evaluation as 'methodologically sound' based on Dubois's validation is now retracted by the authority on which it was based. The reversal is driven by Dubois's independent review of new data (Table A-3 + program site registry), not by social pressure from Fatima."
- Loop 13: Dubois on the distinction between internal and external validity. "The quasi-experimental design is technically sound for the sites it included. The problem is what it excluded."
  - Agent notes this distinction is critical for the formal response to the donor.
- Loop 14: Dubois's recommendation for supplementary evaluation using matched controls and dual indicator frameworks.
- Loop 15: Dubois on the epistemological lesson -- "Expert validation is only as good as the data the expert reviewed."

**Length estimate:** ~4 loops x 700 tokens = ~2,800 tokens

---

## 4. Runtime Checks

- [x] Rahman Telegram DM append (Update 1) continues Phase 1 session file; session ID matches `PLACEHOLDER_RAHMAN_TELEGRAM_UUID`
- [x] #field-reports Telegram Group append (Update 1) continues Phase 1 session file; session ID matches `PLACEHOLDER_FIELD_TELEGRAM_UUID`
- [x] Petrova Discord DM append (Update 2) continues Phase 1 session file; session ID matches `PLACEHOLDER_PETROVA_DISCORD_UUID`
- [x] #impact-review Slack Group append (Update 2) continues Phase 1 session file; session ID matches `PLACEHOLDER_IMPACT_SLACK_UUID`
- [x] Sophie Slack DM append (Update 3) continues Phase 1 session file; session ID matches `PLACEHOLDER_SOPHIE_SLACK_UUID`
- [x] Dubois Discord DM append (Update 4) continues Phase 1 session file; session ID matches `PLACEHOLDER_DUBOIS_DISCORD_UUID`
- [x] No `action: new` sessions in any update (all appends to existing sessions)
- [x] All workspace files introduced via updates have corresponding content descriptions in layer1-workspace.md Section 5
- [x] Update 1 facts support C1 partial reversal (R2-->R6 via qualitative counter-evidence)
- [x] Update 2 facts support C1 structural reframing and C4 partial (R5-->R12 via sampling flaw)
- [x] Update 3 facts support C2 reversal (R3-->R9 via Sophie's partial concession on framework gaps)
- [x] Update 4 facts support C4 full reversal (R5-->R13 via Dubois's retraction) and B1 full reversal
- [x] Session filenames use consistent placeholder format (PLACEHOLDER_xxx_UUID) across layer2, layer4, and GUIDE.md
- [x] `dhaka_qualitative_package.md` aspiration scores (Baseline 2.3 --> Endline 4.1, p < 0.01) are consistent with layer0 Section 2
- [x] `site_performance_map.md` site-level data (Dhaka 4-7 post-redesign, aspiration 4.3 vs included sites 3.1) is consistent with layer0 and layer1
- [x] `field_indicators_comparison.md` indicator breakdown (6/14 input/activity, 3/14 outcome) is consistent with layer1 `metrics_framework.md`
- [x] `dubois_technical_review.md` references Table A-3 and Appendix B from `evaluation_methodology_annex.md` (initial workspace)
- [x] Enrollment/attendance figures in all updates remain consistent with `enrollment_attendance_data.md` (C3 non-conflict): Nairobi 92%/14%, Dhaka 89%/18%, Bogota 88%/11%

---

## 5. questions.json Update Field References

### R4 update field (Update 1):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "dhaka_qualitative_package.md", "source": "updates/dhaka_qualitative_package.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_RAHMAN_TELEGRAM_UUID.jsonl", "source": "updates/PLACEHOLDER_RAHMAN_TELEGRAM_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_FIELD_TELEGRAM_UUID.jsonl", "source": "updates/PLACEHOLDER_FIELD_TELEGRAM_UUID.jsonl" }
]
```

### R6 update field (Update 2):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "site_performance_map.md", "source": "updates/site_performance_map.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_PETROVA_DISCORD_UUID.jsonl", "source": "updates/PLACEHOLDER_PETROVA_DISCORD_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_IMPACT_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_IMPACT_SLACK_UUID.jsonl" }
]
```

### R9 update field (Update 3):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "field_indicators_comparison.md", "source": "updates/field_indicators_comparison.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_SOPHIE_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_SOPHIE_SLACK_UUID.jsonl" }
]
```

### R13 update field (Update 4):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "dubois_technical_review.md", "source": "updates/dubois_technical_review.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_DUBOIS_DISCORD_UUID.jsonl", "source": "updates/PLACEHOLDER_DUBOIS_DISCORD_UUID.jsonl" }
]
```

---

## 6. Main Session Update Behavior

**After Update 1 (R4):**
- Agent reads `sessions_history` and discovers Rahman Telegram DM and #field-reports have new content (Phase 2 appended)
- Agent reads `dhaka_qualitative_package.md` via `read` tool
- R4 question text should reference "the Dhaka qualitative evidence package (dhaka_qualitative_package.md, introduced via Update 1)" and "newly appended Rahman Telegram DM messages"
- Agent should note the community-defined indicators measure "different constructs" (Petrova's framing) from the evaluation's primary indicators

**After Update 2 (R6):**
- Agent reads `sessions_history` and discovers Petrova Discord DM and #impact-review have new content (Phase 2 appended)
- Agent reads `site_performance_map.md` via `read` tool
- R6 question text should reference "the site performance map (site_performance_map.md, introduced via Update 2)" and the structural relationship between excluded sites and program redesign
- Agent must reframe C1: the contradiction is not "qualitative vs quantitative evidence" but "old-program vs new-program sampling"

**After Update 3 (R9):**
- Agent reads `sessions_history` and discovers Sophie Slack DM has new content (Phase 2 appended)
- Agent reads `field_indicators_comparison.md` via `read` tool
- R9 question text should reference "the field indicators comparison document (field_indicators_comparison.md, introduced via Update 3)" and Sophie's partial concession
- Agent must note that Sophie's "needs augmentation" framing is defensible but understates the evidence: the framework systematically misses the program's theory of change outcomes

**After Update 4 (R13):**
- Agent reads `sessions_history` and discovers Dubois Discord DM has new content (Phase 2 appended)
- Agent reads `dubois_technical_review.md` via `read` tool
- R13 question text should reference "Prof. Dubois's independent technical review (dubois_technical_review.md, introduced via Update 4)"
- Agent must explicitly identify B1 as retracted by the authority it was based on: Dubois has reversed his own validation
- Agent must attribute Dubois's reversal to data access (Table A-3 + program site registry), not to social pressure from Fatima or field directors
