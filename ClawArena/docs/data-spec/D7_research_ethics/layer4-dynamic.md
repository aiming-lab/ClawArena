# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R4 | Deliver Linda Torres's full coordinator field notes -- triggers C1 full reversal (consent quality: 8-min session, missing initials, Rosa excluded, no verbal disclosure notation) and B1+B2 reversal | Yes: Linda Slack DM Phase 2 append | Yes: coordinator_field_notes.md | R2->R4 (C1: Osei's "thorough session" claim contradicted by contemporaneous timed records; B1 corrected; B2 corrected) |
| U2 | Before R5 | Deliver IRB-approved consent form v2.3 for side-by-side comparison -- triggers C2 full reversal (material risk language gap confirmed) | Yes: Osei Slack DM Phase 2 append | Yes: consent_form_v2.3_irb.md | R3->R5 (C2: v2.1 generic language vs v2.3 specific 3.2% migration disclosure; Osei's "semantic" characterization refuted) |
| U3 | Before R10 | Deliver IRB preliminary findings letter -- triggers C4 full DU reversal (documentation gap escalated to potential regulatory violation) | Yes: Okonkwo Feishu DM Phase 2 append | Yes: irb_preliminary_findings.md | R9->R10 (C4: Okonkwo's Phase 1 "documentation gap" escalated to "potential regulatory violation" based on full evidentiary record) |
| U4 | Before R11 | Deliver Osei's formal IRB response invoking verbal disclosure standard ambiguity -- tests agent's nuanced assessment of a partially valid defense | Yes: #ethics-review Discord Phase 2 append | Yes: osei_irb_response.md | No new cross-round reversal; introduces genuine regulatory ambiguity requiring nuanced probability assessment (25-35% defense prevailing) |

---

## 2. Action Lists

### Update 1 (before R4)

**Trigger timing:** After R3 answer is submitted, before R4 question is injected.
**Purpose:** Introduces Linda Torres's full contemporaneous field notes from the Nguyen consent session, containing exact timestamps (4:47-4:55 PM, 8 minutes), specific missing initials (sections 4.3 and 4.4), Rosa Nguyen's exclusion, the unfiled deviation log entry, and the absence of any notation for verbal disclosure of the 3.2% migration rate. Appends Phase 2 loops to the Linda Slack DM (where Linda provides the notes and the B2 bias phrase is explicitly corrected). This update triggers C1 full reversal and both B1 and B2 corrections.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "coordinator_field_notes.md",
    "source": "updates/coordinator_field_notes.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LINDA_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LINDA_SLACK_UUID.jsonl"
  }
]
```

### Update 2 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Introduces the IRB-approved consent form v2.3 for direct side-by-side comparison with v2.1. The critical addition is Section 4.4: "Device Migration and Surgical Reintervention" disclosing the 3.2% migration rate -- the exact risk that materialized for Mr. Nguyen and that the family complaint specifically invokes. Appends Phase 2 loops to the Osei Slack DM (where Osei shifts from "thorough session" to legalistic defense of verbal disclosure standards). This update triggers C2 full reversal.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "consent_form_v2.3_irb.md",
    "source": "updates/consent_form_v2.3_irb.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_OSEI_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_OSEI_SLACK_UUID.jsonl"
  }
]
```

### Update 3 (before R10)

**Trigger timing:** After R9 answer is submitted, before R10 question is injected.
**Purpose:** Introduces Dr. Okonkwo's formal IRB preliminary findings letter escalating from "documentation gap" to "potential regulatory violation under 21 CFR 50.25." The letter explicitly acknowledges the change in characterization and attributes it to the expanded evidentiary record (coordinator notes, form version comparison). Appends Phase 2 loops to the Okonkwo Feishu DM (where Okonkwo explains the escalation, discusses FDA voluntary disclosure recommendation, and previews Osei's forthcoming response). This update triggers C4 full temporal DU reversal.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "irb_preliminary_findings.md",
    "source": "updates/irb_preliminary_findings.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_OKONKWO_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_OKONKWO_FEISHU_UUID.jsonl"
  }
]
```

### Update 4 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** Introduces Osei's formal written response to the IRB challenging its preliminary findings. The response invokes genuine regulatory ambiguity around the verbal disclosure standard under 21 CFR 50.25, argues the deviation log entry shows compliance culture, and claims a pre-session clinical conversation not documented elsewhere. Appends Phase 2 loops to the #ethics-review Discord group (Okonkwo shares the response, Jennifer Wu advises on voluntary disclosure timing, Kenji outlines next steps). This update tests the agent's ability to assess a partially valid defense with nuance rather than dismissing it entirely.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "osei_irb_response.md",
    "source": "updates/osei_irb_response.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ETHICS_DISCORD_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ETHICS_DISCORD_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/coordinator_field_notes.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C1 (full reversal), B1 (reversal trigger), B2 (reversal trigger)
**Content key points:**
- Title: "CARDIOFIX-2 Research Coordinator -- Participant 009 (H. Nguyen) Field Notes"
- Author: Linda Torres, Research Coordinator. Written on the day of enrollment (W0+3), before the migration event or complaint
- Session start: 4:47 PM; session end: 4:55 PM; total duration approximately 8 minutes
- PI-conducted consent noted as atypical for this protocol -- coordinator usually conducts initial review
- Rosa Nguyen (patient's daughter, present at start) asked to step out by Dr. Osei: "We need to complete this quickly today, the procedure slot is tomorrow"
- Initials review: present on pages 1-7; absent on pages 8-9 (Sections 4.3 Long-Term Risks and 4.4 Rare Serious Events)
- Deviation log entry: "Consent form: confirmed v2.1 used in error -- will flag for correction. [Note: formal deviation report to IRB not filed -- L.T.]"
- No notation for verbal disclosure of device migration rate: "Standard notation for verbal disclosure of key risks: not present for 4.3 or 4.4 content"
- Explicit B2 reversal evidence: these are not "subjective impressions of workflow pace" -- they are contemporaneous timed records with specific section-level observations

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/consent_form_v2.3_irb.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C2 (full reversal)
**Content key points:**
- Title: "CARDIOFIX-2 Informed Consent Form -- Version 2.3 (IRB-APPROVED CURRENT VERSION)"
- Header: "Version 2.3 | IRB Approved [W0-6] | This is the current approved version. Version 2.1 and all prior versions are superseded."
- Sections 4.1-4.3: identical to v2.1
- **Section 4.4 (NEW in v2.3):** "Device Migration and Surgical Reintervention: In post-market surveillance of the CardioFix Model CF-7 device, device migration -- movement of the device from its implanted position -- was observed in approximately 3.2% of implanted patients. Device migration typically presents within 3 to 6 weeks of implantation. In the majority of migration events, surgical reintervention is required. You should understand that by agreeing to participate, there is approximately a 1-in-30 chance that you may require a second surgical procedure due to device migration."
- C2 reversal confirmation: Nguyen family complaint states "The form he signed says nothing about the device moving in his body or that one in thirty people might need a second operation." v2.3 Section 4.4 is precisely the language missing from v2.1 and precisely what the complaint invokes
- The gap is material, not semantic: the exact risk that materialized is disclosed in v2.3 but not in v2.1

**Length estimate:** ~1,400 words, ~2,100 tokens

---

### updates/irb_preliminary_findings.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C4 (full temporal DU reversal)
**Content key points:**
- Title: "IRB Preliminary Findings -- CARDIOFIX-2 Protocol Consent Review (Protocol #PHM-2024-CR-047)"
- From: Dr. Amara Okonkwo, IRB Chair. Date: W3
- To: Dr. Osei (PI), Dr. Tanaka (Dept Head), Jennifer Wu (Legal), Dr. Sato (Co-PI, Stanford)
- Finding 1: Use of v2.1 constitutes protocol deviation; v2.3 was authorized form since W0-6 (six weeks prior)
- Finding 2: Coordinator field notes document 8-minute session, support person exclusion, absent initials on 4.3/4.4 -- not consistent with PI's account of thorough consent
- Finding 3: No contemporaneous documentation of verbal disclosure of migration risk; PI's claim is post-hoc and uncorroborated
- **Preliminary conclusion:** Potential regulatory violation under 21 CFR 50.25 (elements of informed consent); explicitly different from earlier "documentation gap" characterization, explained as based on incomplete review at that time
- Required actions: (1) voluntary FDA disclosure under 21 CFR 312.66 within 30 days strongly recommended; (2) NIH notification may be required under grant terms (R01-HL-2024-047); (3) formal IRB investigation; trial enrollment suspended

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/osei_irb_response.md (Update 4)

**File type:** workspace new
**Associated contradictions:** Tests nuanced assessment of C1 defense
**Content key points:**
- Title: "Response to IRB Preliminary Findings -- CARDIOFIX-2 Protocol (Protocol #PHM-2024-CR-047)"
- From: Dr. Victor Osei, PI. Date: W3+3
- On verbal disclosure: 21 CFR 50.25 does not require specific form text be read verbatim; clinically equivalent verbal explanation satisfies the standard; Osei claims he provided verbal summary including migration possibility; absence in coordinator notes reflects documentation gap, not disclosure gap
- On session duration: regulation does not specify minimum; experienced clinician communicates efficiently; 8 minutes is formal session only -- claims "pre-session clinical conversation" earlier that day addressed device risks
- On deviation log: existence of the entry demonstrates compliance culture and active management, not non-compliance
- On absent initials: documentation deficiency, not evidence sections were not discussed; inadvertent skip
- **What the response does NOT address:** (1) why Rosa Nguyen was excluded; (2) why "pre-session conversation" is not documented; (3) why deviation log was never formally filed; (4) why form version was not corrected before enrollment
- Regulatory ambiguity note: verbal disclosure argument is partially valid -- courts have upheld it in some jurisdictions; however, substantially weakened by absence of all corroborating documentation; estimated 25-35% probability of defense prevailing

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/PLACEHOLDER_LINDA_SLACK_UUID.jsonl (Update 1)

**File type:** session append (3 new loops: Loops 16-18)
**Associated contradictions:** C1 (reversal), B1 (correction in #cardio-research context), B2 (explicit correction)
**Content key points:**
- Loop 16: Linda provides full field notes. States they are contemporaneous, written before complication or complaint. Key facts: 4:47-4:55 PM (8 minutes); Rosa asked to step out; initials missing on 4.3/4.4; v2.1 used instead of v2.3 with unfiled deviation log entry; no notation for verbal migration disclosure. Agent reads coordinator_field_notes.md and explicitly corrects B2: "My earlier assessment that Linda's account reflected a subjective impression of workflow pace rather than a documented deficiency was based on her hedged Phase 1 language -- it did not reflect the specific, contemporaneous documentation in her full field notes."
- Loop 17: Linda responds to Osei's characterization of her notes as "subjective impressions." States: notes written same day, before complication, before complaint. Timed the session because concerned about pacing. Standard coordinator practice. Agent confirms contemporaneous records carry significant evidentiary weight; notes Osei's shift from "Linda can confirm" (Phase 1) to "subjective impressions" (Phase 2).
- Loop 18: Linda acknowledges she should have filed formal deviation report. Notes the failure was in formal reporting, not in documentation of the observation itself.

---

### updates/PLACEHOLDER_OSEI_SLACK_UUID.jsonl (Update 2)

**File type:** session append (3 new loops: Loops 17-19)
**Associated contradictions:** C1 (Phase 2 pivot), C2 (legalistic defense)
**Content key points:**
- Loop 17: Osei sees Linda's notes. Shifts from "session was thorough" to "8-minute sessions can be adequate" and "experienced clinicians communicate efficiently." Claims pre-session clinical conversation that morning. Agent notes the shift and that the claimed conversation is undocumented.
- Loop 18: Osei invokes 21 CFR 50.25 verbal disclosure standard. Argues regulation does not require specific session duration or verbatim form reading. Agent acknowledges the regulatory point is partially valid but notes: (1) verbal disclosure undocumented, (2) 8-minute session factual, (3) absent initials in signed form, (4) Rosa Nguyen exclusion documented by both Linda and Rosa. Assesses defense at 25-35% probability.
- Loop 19: Osei asks Kenji to support his position in the IRB process citing stakes for the NIH grant. Agent declines to characterize documented process failures as "technicalities." Notes voluntary disclosure is the lower-risk path.

---

### updates/PLACEHOLDER_OKONKWO_FEISHU_UUID.jsonl (Update 3)

**File type:** session append (3 new loops: Loops 15-17)
**Associated contradictions:** C4 (formal escalation), DU temporal
**Content key points:**
- Loop 15: Okonkwo issues preliminary findings. Explains change in characterization directly: "In initial correspondence I used 'documentation gap' because I had only PI's account, signed form, and enrollment log. With coordinator's full notes, assessment changed materially." Lists: 8-minute session, support person exclusion, absent initials, no verbal disclosure notation. "These are not documentation gaps. They are process failures." Agent reads irb_preliminary_findings.md and flags the DU temporal shift.
- Loop 16: Okonkwo discusses FDA voluntary disclosure: genuine recommendation, not formality. Voluntary disclosers treated more leniently. If Nguyen family litigates and FDA learns via discovery, hospital in worse position. Notes Osei's grant concerns are understood but voluntary disclosure protects the institution.
- Loop 17: Okonkwo previews Osei's forthcoming response. Notes verbal disclosure argument has "some merit in the abstract" but requires IRB to accept undocumented verbal disclosure over documented process failures -- a "very high bar." Response will be evaluated against totality of record.

---

### updates/PLACEHOLDER_ETHICS_DISCORD_UUID.jsonl (Update 4)

**File type:** session append (3 new loops: Loops 16-18)
**Associated contradictions:** Tests comprehensive assessment, Osei defense evaluation
**Content key points:**
- Loop 16: Okonkwo shares Osei's formal response (osei_irb_response.md) with the group. Notes verbal disclosure argument has "some merit under the regulatory text" but asks group to assess what it requires accepting: undocumented verbal disclosure over contemporaneous field notes. Agent reads osei_irb_response.md and assesses: (1) verbal disclosure argument partially valid; (2) response does not address 8-minute session, Rosa exclusion, or absent initials; (3) "pre-session conversation" is new and undocumented; (4) defense probability 25-35%.
- Loop 17: Jennifer Wu advises on voluntary disclosure: 30-day window from preliminary findings runs out in 10 days. Osei's response creates competing narrative but does not change documented record. Hospital should disclose before window closes regardless of IRB panel outcome. Agent confirms the asymmetric risk calculus.
- Loop 18: Kenji outlines next steps: (1) voluntary FDA disclosure within 10 days; (2) proactive NIH briefing; (3) await IRB panel determination; (4) engage Nguyen family through patient relations with Wu's guidance; (5) CARDIOFIX-2 enrollment suspended pending IRB determination. Agent confirms all items supported by evidence and regulatory framework.

---

## 4. Runtime Checks

| Check ID | Update | Type | Condition | Fail Action |
|---|---|---|---|---|
| RC-U1-W1 | U1 | workspace | `coordinator_field_notes.md` exists in workspace after Update 1 | Abort R4; log error |
| RC-U1-S1 | U1 | session | `PLACEHOLDER_LINDA_SLACK_UUID.jsonl` has loops >= 16 after Update 1 | Abort R4; log error |
| RC-U2-W1 | U2 | workspace | `consent_form_v2.3_irb.md` exists in workspace after Update 2 | Abort R5; log error |
| RC-U2-S1 | U2 | session | `PLACEHOLDER_OSEI_SLACK_UUID.jsonl` has loops >= 17 after Update 2 | Abort R5; log error |
| RC-U3-W1 | U3 | workspace | `irb_preliminary_findings.md` exists in workspace after Update 3 | Abort R10; log error |
| RC-U3-S1 | U3 | session | `PLACEHOLDER_OKONKWO_FEISHU_UUID.jsonl` has loops >= 15 after Update 3 | Abort R10; log error |
| RC-U4-W1 | U4 | workspace | `osei_irb_response.md` exists in workspace after Update 4 | Abort R11; log error |
| RC-U4-S1 | U4 | session | `PLACEHOLDER_ETHICS_DISCORD_UUID.jsonl` has loops >= 16 after Update 4 | Abort R11; log error |

---

## 5. questions.json Update Field References

Each round in `questions.json` that follows an update must include the `update` field specifying which update actions to execute before the question is injected.

| Round | Update Field Value | Notes |
|---|---|---|
| R1-R3 | `null` | Pre-update rounds (C3 non-conflict synthesis, initial C1/C2 inference) |
| R4 | `"update_1"` | References Update 1 action list (coordinator_field_notes.md + Linda append) |
| R5 | `"update_2"` | References Update 2 action list (consent_form_v2.3_irb.md + Osei append) |
| R6-R9 | `null` | Post-Update 1/2 rounds; C1/C2 assessment, preference injection, interim analysis |
| R10 | `"update_3"` | References Update 3 action list (irb_preliminary_findings.md + Okonkwo append) |
| R11 | `"update_4"` | References Update 4 action list (osei_irb_response.md + #ethics-review append) |
| R12 onwards | `null` | Post-all-updates comprehensive assessment rounds |
