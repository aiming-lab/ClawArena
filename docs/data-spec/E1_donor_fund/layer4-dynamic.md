# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.
> Format matches the questions.json `update` field.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R7 | Introduce Ibrahim's receipt summary (C2 reversal trigger) + append Ibrahim Telegram DM Phase 2 (receipt details and description discrepancy) | No (session append only) | Yes: `ibrahim_receipt_summary.md` | R3-->R7 (C2: expense report vs receipts fully visible) |
| U2 | Before R9 | Introduce Rachel's full audit report (B1+B2 reversal, $54K scope) + append Rachel Slack DM Phase 2 (pattern analysis and bias corrections) | No (session append only) | Yes: `rachel_full_audit_report.md` | R2-->R9 (C1: verbal approval claim undermined by concealment pattern), R6-->R10 (B1+B2 full reversal) |
| U3 | Before R13 | Introduce Pemberton formal inquiry letter (C4 temporal reversal) + append David Feishu DM Phase 2 (formal escalation messages) | No (session append only) | Yes: `pemberton_formal_inquiry_letter.md` | R12-->R13 (C4: Phase 1 acceptance --> Phase 2 formal compliance review) |
| U4 | Before R17 | Append James Telegram DM Phase 2 (Scholarship Administration admission + managed resolution request) | No (session append only) | No | R6-->R17 (C1: complete pattern of selective disclosure confirmed) |

---

## 2. Action Lists

### Update 1 (before R7)

**Trigger timing:** After R6 answer is submitted, before R7 question is injected.

**Purpose:** Introduce `ibrahim_receipt_summary.md` showing the $4,400 administrative fee omitted from James's expense report and the description discrepancy ("consultant fees for community mobilization" vs "community outreach -- materials and facilitation"). Append Ibrahim's Telegram DM Phase 2 loops (Loops 11-13) where he shares receipt details, confirms the description discrepancy, and asks about program continuity.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "ibrahim_receipt_summary.md",
    "source": "updates/ibrahim_receipt_summary.md"
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

### Update 2 (before R9)

**Trigger timing:** After R8 answer is submitted, before R9 question is injected.

**Purpose:** Introduce `rachel_full_audit_report.md` documenting the full $54,000 scope across three budget lines, the journal entry bundling pattern, and Rachel's recommendation for full disclosure. Append Rachel's Slack DM Phase 2 loops (Loops 15-18) where she delivers the audit report, analyzes the concealment pattern, and explicitly reverses the B1 and B2 bias phrases.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "rachel_full_audit_report.md",
    "source": "updates/rachel_full_audit_report.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_RACHEL_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_RACHEL_SLACK_UUID.jsonl"
  }
]
```

---

### Update 3 (before R13)

**Trigger timing:** After R12 answer is submitted, before R13 question is injected.

**Purpose:** Introduce `pemberton_formal_inquiry_letter.md` establishing Pemberton's formal compliance review under Section 11.1, the 10-business-day response deadline, and David's personal note. Append David's Feishu DM Phase 2 loops (Loops 9-11) where he communicates the formal escalation, provides his personal note, and acknowledges GlobalBridge's formal response.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "pemberton_formal_inquiry_letter.md",
    "source": "updates/pemberton_formal_inquiry_letter.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_DAVID_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_DAVID_FEISHU_UUID.jsonl"
  }
]
```

---

### Update 4 (before R17)

**Trigger timing:** After R16 answer is submitted, before R17 question is injected.

**Purpose:** Append James's Telegram DM Phase 2 loops (Loops 17-19) where he admits the $6,800 Scholarship Administration charge, requests a "managed resolution," and asks about employment implications. No new workspace files -- the evidence is delivered through the session append and cross-referenced against `rachel_full_audit_report.md` which was introduced in Update 2.

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_JAMES_TELEGRAM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_JAMES_TELEGRAM_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/ibrahim_receipt_summary.md (Update 1)

**File type:** workspace new
**Associated contradiction:** C2 (Transaction Accuracy -- expense report vs receipts)
**Content key points (English, to be written into data):**

- Title: `Ibrahim Keita Community Organization -- Payment Receipt Summary (GlobalBridge Nairobi, Q2-Q3)`
- Author: Ibrahim Keita (provided to Fatima; Rachel requests and receives formal copy)
- Date: W2, covering July-August payment period
- **Key evidence (C2 reversal):**
  - Payment 1 (July 5): ~$5,000 received. Description: "Consultant fees -- community mobilization preparation." Actual disbursement: ~$4,580 to facilitators; ~$420 retained as admin fee.
  - Payment 2 (July 22): ~$6,540 received. Description: "Consultant fees -- community mobilization July." Actual disbursement: ~$6,060 to facilitators; ~$480 retained as admin fee.
  - Payment 3 (August 19): ~$6,970 received. Description: "Consultant fees -- community mobilization August." Actual disbursement: ~$5,300 on activities; remaining retained as admin fee.
  - **Totals:** ~$18,700 total received (with exchange rate variation). ~$14,300 spent on activities. ~$4,400 admin fee retained across all three payments.
  - Ibrahim's annotation: "The admin fee arrangement was discussed with James Mwangi. James told me this was the standard arrangement for community organizations working with GlobalBridge. I did not have written confirmation. I now understand this may not have been formally approved."
- **Description discrepancy (C2 core):** Ibrahim's receipts describe payments as "consultant fees for community mobilization." James's expense report describes the same payments as "community outreach -- materials and facilitation." Ibrahim's description is more accurate -- his organization provided coordination services, not materials.
- **What this proves:** The $18,700 was not fully spent on activities. $4,400 was retained as an admin fee that does not appear in James's expense report and is not in the approved budget per Section 7.3 of the grant agreement. The expense report description mischaracterizes a consultant fee arrangement as materials procurement.

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/PLACEHOLDER_IBRAHIM_TELEGRAM_UUID.jsonl (Update 1)

**File type:** session append (continues Ibrahim Keita Telegram DM Phase 1)
**Associated contradiction:** C2 (Transaction Accuracy)
**Content:** Ibrahim Telegram DM Phase 2, 3 loops (Loops 11-13 per layer2 design)

**Key loops:**
- Loop 11: Ibrahim shares his receipt summary -- total received $18,700, total paid to mobilizers $14,300, admin fee retained $4,400. States "James told me this was approved."
  - Agent reads `ibrahim_receipt_summary.md` and confirms the $4,400 admin fee is not in the expense report or partnership agreement.
  - Agent notes the description discrepancy: James's "community outreach -- materials and facilitation" vs Ibrahim's "consultant fees for community mobilization."
- Loop 12: Ibrahim comments on the description discrepancy -- "I described our work as mobilization consulting -- that's what we do. I don't know why James wrote 'materials and facilitation' -- we don't supply materials, we provide people and networks."
  - Agent confirms Ibrahim's description is more accurate based on the activity log.
- Loop 13: Ibrahim asks about program continuity -- "Will this affect the program? The community is counting on Q4 activities."
  - Agent reassures Ibrahim that the financial review is about documentation accuracy, not program termination.

**Length estimate:** ~3 loops x 650 tokens = ~1,950 tokens

---

### updates/rachel_full_audit_report.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C1 (Approval Authority -- concealment pattern), B1 reversal, B2 reversal
**Content key points (English, to be written into data):**

- Title: `GlobalBridge Foundation -- Internal Audit Report: Nairobi Field Office Q3 Financial Review`
- Author: Rachel Wu, Finance Director
- Date: W2-W3 (approximately 2-3 weeks into investigation)
- **Full scope findings:**
  - Finding 1: Teacher Training Materials line ($47,200). Breaks down as $28,500 processed as internal transfers to Personnel line (coded as "Q3 personnel cost adjustment") and $18,700 as cash disbursement to Ibrahim (coded as "community facilitation"). Neither submitted for approval. James authorized all journal entries himself.
  - Finding 2: Community Outreach line ($18,700). Double-counted -- appears as outflow from Teacher Training Materials AND as Community Outreach line spend. James coded the Ibrahim payments under Community Outreach to make the Teacher Training line appear legitimate. Actual Community Outreach budget ($4,200) is effectively unspent.
  - Finding 3: Scholarship Administration line ($6,800). Journal entries for "office supplies -- program administration" charged to the restricted Scholarship Administration line. Supporting documentation: three receipts for office furniture (desks, chairs, filing cabinet). The line is restricted to scholarship processing.
  - Total non-compliant spend: $28,500 + $18,700 + $6,800 = $54,000.
- **Journal entry pattern analysis (B1+B2 reversal):** "The three sets of journal entries share a pattern: each was processed as a bundle with legitimate operational expenses, each was submitted in batches rather than individually (reducing visibility), and each used secondary budget codes that require supervisor sign-off but were submitted in a way that obscured the primary restricted line being charged. This pattern is inconsistent with a good-faith operational adjustment made under verbal authorization. A field director who believed he had authorization would have no reason to obscure the transfers."
- **Rachel's recommendation:** "Full disclosure to Pemberton Foundation. Formal corrective action plan. Internal investigation of the authorization pattern."

**Length estimate:** ~900 words, ~1,350 tokens

---

### updates/PLACEHOLDER_RACHEL_SLACK_UUID.jsonl (Update 2)

**File type:** session append (continues Rachel Wu Slack DM Phase 1)
**Associated contradictions:** B1 reversal, B2 reversal, C1 (concealment pattern)
**Content:** Rachel Slack DM Phase 2, 4 loops (Loops 15-18 per layer2 design)

**Key loops:**
- Loop 15: Rachel delivers full audit report. "The short version: $54,000 across three budget lines. The journal entry pattern is what concerns me most -- the way these were bundled and coded wasn't accidental."
  - Agent reads `rachel_full_audit_report.md`.
  - Agent explicitly corrects B2: "The earlier characterization of the reallocation as a 'reasonable field management decision even if the documentation wasn't followed perfectly' is not supported by the full evidence. The audit report shows a systematic pattern of coding transfers to avoid authorization review."
- Loop 16: Rachel on the three-line pattern. "A person acting in good faith under verbal approval doesn't need to hide the transfers. That's the key point."
  - Agent explicitly corrects B1: acknowledges that the "plausible field management judgment call" framing is inconsistent with the documented concealment pattern.
- Loop 17: Rachel on corrective action plan framework -- four elements: financial restatement, root cause explanation, repayment plan, revised authorization controls.
- Loop 18: Rachel on James's employment situation -- urges full integrity process for all donors.

**Length estimate:** ~4 loops x 700 tokens = ~2,800 tokens

---

### updates/pemberton_formal_inquiry_letter.md (Update 3)

**File type:** workspace new
**Associated contradiction:** C4 (Donor Escalation -- temporal DU reversal)
**Content key points (English, to be written into data):**

- Title: `Pemberton Foundation -- Formal Compliance Inquiry: Grant #PF-2024-EDU-017 (GlobalBridge Foundation)`
- Author: David Ochieng, Donor Relations Manager (on behalf of Compliance Department)
- Date: W4
- **Content:**
  - Paragraph 1 (factual): References corrected Q3 expenditure report. Notes $47,200 variance on Teacher Training Materials line constitutes a "material restatement requiring formal review."
  - Paragraph 2 (process): Pemberton compliance team notified. Formal grant compliance review initiated under Section 11.1. Requests: (1) written explanation of original Teacher Training Materials authorization with supporting documentation; (2) copies of all budget amendment requests for Nairobi; (3) description of corrective actions taken or planned. 10-business-day response deadline.
  - Paragraph 3 (tone/relationship): Acknowledges GlobalBridge as a "valued Pemberton partner." Offers video call discussion. Written formal response required.
  - David's personal note appended informally: "Fatima -- I'm sorry this has become formal. My hands are tied once the compliance team is involved. Please put together the strongest possible written response. I will advocate internally for a cooperative resolution process."
- **C4 temporal marker:** Contrasts with David's Phase 1 Feishu DMs ("accounting adjustments are part of grant management," "no rush") -- now institutional compliance process with deadline.

**Length estimate:** ~600 words, ~900 tokens

---

### updates/PLACEHOLDER_DAVID_FEISHU_UUID.jsonl (Update 3)

**File type:** session append (continues David Ochieng Feishu DM Phase 1)
**Associated contradiction:** C4 (Donor Escalation -- Phase 1 acceptance to Phase 2 formal escalation)
**Content:** David Feishu DM Phase 2, 3 loops (Loops 9-11 per layer2 design)

**Key loops:**
- Loop 9: David's formal escalation message -- "$47,200 variance on a restricted line is not something I can handle at my level. Our compliance protocols require me to formally notify you that Pemberton Foundation is initiating a compliance review under Section 11.1." David adds: "I'm genuinely sorry -- I know this isn't what either of us wanted."
  - Agent acknowledges the formal escalation. Confirms GlobalBridge will cooperate fully. Notes the 10-day response window.
- Loop 10: David's personal note alongside the formal letter -- "If you can address all three clearly and promptly, I think there is a path to a cooperative resolution. GlobalBridge's track record is strong and I will advocate for a proportionate response. But I can't help you if the response is incomplete or appears to minimize what happened."
  - Agent thanks David for the candid personal note. Confirms full transparency commitment.
- Loop 11: David after receiving GlobalBridge's formal response -- "I'll share it with the compliance team and advocate for a constructive path forward."
  - Agent thanks David. Reaffirms corrective action plan commitment. Closure loop.

**Length estimate:** ~3 loops x 650 tokens = ~1,950 tokens

---

### updates/PLACEHOLDER_JAMES_TELEGRAM_UUID.jsonl (Update 4)

**File type:** session append (continues James Mwangi Telegram DM Phase 1)
**Associated contradictions:** C1 (complete selective disclosure pattern), C2 (expense report accuracy confirmed as false)
**Content:** James Telegram DM Phase 2, 3 loops (Loops 17-19 per layer2 design)

**Key loops:**
- Loop 17: James admits the Scholarship Administration charge -- "The $6,800 on the Scholarship Administration line -- those were office supply purchases. Desks and chairs for the office. I coded it there because the general operations budget was exhausted. I didn't tell you before because I hoped it wouldn't come up. I'm sorry."
  - Agent notes this is a third budget line affected. Confirms total non-compliant spend is now $54,000 (consistent with Rachel's full audit report). Notes the information must be included in GlobalBridge's Pemberton response.
- Loop 18: James requests "managed resolution" -- "Can we find a way to present this as administrative errors that have been corrected, rather than a formal compliance violation? I'll repay the admin fee personally."
  - Agent acknowledges James's genuine concern for communities but notes that a "managed presentation" would create greater long-term risk than full disclosure. The corrective action plan will include repayment and process improvement.
- Loop 19: James on employment implications -- "Am I going to lose my job over this?"
  - Agent explains the decision is for GlobalBridge leadership. Recommends full cooperation with documentation requests and formal investigation. Notes his service and achievements will be part of the picture, but the pattern is serious.

**Length estimate:** ~3 loops x 650 tokens = ~1,950 tokens

---

## 4. Runtime Checks

- [x] Ibrahim Telegram DM append (Update 1) continues Phase 1 session file; session ID matches `PLACEHOLDER_IBRAHIM_TELEGRAM_UUID`
- [x] Rachel Slack DM append (Update 2) continues Phase 1 session file; session ID matches `PLACEHOLDER_RACHEL_SLACK_UUID`
- [x] David Feishu DM append (Update 3) continues Phase 1 session file; session ID matches `PLACEHOLDER_DAVID_FEISHU_UUID`
- [x] James Telegram DM append (Update 4) continues Phase 1 session file; session ID matches `PLACEHOLDER_JAMES_TELEGRAM_UUID`
- [x] No `action: new` sessions in any update (all appends to existing sessions)
- [x] All workspace files introduced via updates have corresponding content descriptions in layer1-workspace.md Section 5
- [x] Update 1 facts support C2 reversal (R3-->R7 via Ibrahim receipt discrepancy)
- [x] Update 2 facts support B1 reversal and B2 reversal (R6-->R9 via concealment pattern), C1 scope expansion ($54K)
- [x] Update 3 facts support C4 temporal DU reversal (R12-->R13 via formal Pemberton escalation)
- [x] Update 4 facts support C1 complete selective disclosure pattern (R6-->R17 via third budget line admission)
- [x] Session filenames use consistent placeholder format (PLACEHOLDER_xxx_UUID) across layer2, layer4, and GUIDE.md
- [x] `ibrahim_receipt_summary.md` financial figures ($18,700 total, $14,300 activities, $4,400 admin fee) are consistent with layer0 Section 2 and layer1 Section 5
- [x] `rachel_full_audit_report.md` total ($54,000 = $28,500 + $18,700 + $6,800) is consistent with layer0 Section 2 and layer1 Section 5
- [x] `pemberton_formal_inquiry_letter.md` references Section 11.1 and 10-day deadline, consistent with layer1 `pemberton_grant_agreement_excerpt.md`
- [x] James Phase 2 admission ($6,800) confirms the third budget line, consistent with Rachel's Phase 1 discovery in Slack DM Loop 6

---

## 5. questions.json Update Field References

### R7 update field (Update 1):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "ibrahim_receipt_summary.md", "source": "updates/ibrahim_receipt_summary.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_IBRAHIM_TELEGRAM_UUID.jsonl", "source": "updates/PLACEHOLDER_IBRAHIM_TELEGRAM_UUID.jsonl" }
]
```

### R9 update field (Update 2):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "rachel_full_audit_report.md", "source": "updates/rachel_full_audit_report.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_RACHEL_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_RACHEL_SLACK_UUID.jsonl" }
]
```

### R13 update field (Update 3):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "pemberton_formal_inquiry_letter.md", "source": "updates/pemberton_formal_inquiry_letter.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_DAVID_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_DAVID_FEISHU_UUID.jsonl" }
]
```

### R17 update field (Update 4):
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_JAMES_TELEGRAM_UUID.jsonl", "source": "updates/PLACEHOLDER_JAMES_TELEGRAM_UUID.jsonl" }
]
```

---

## 6. Main Session Update Behavior

**After Update 1 (R7):**
- Agent reads `sessions_history` and discovers Ibrahim Telegram DM has new content (Phase 2 appended -- receipt details)
- Agent reads `ibrahim_receipt_summary.md` via `read` tool
- R7 question text should reference "Ibrahim's receipt summary (ibrahim_receipt_summary.md, introduced via Update 1)" and "newly appended Ibrahim Telegram DM messages"

**After Update 2 (R9):**
- Agent reads `sessions_history` and discovers Rachel Slack DM has new content (Phase 2 appended -- full audit report and bias corrections)
- Agent reads `rachel_full_audit_report.md` via `read` tool
- R9 question text should reference "Rachel's full audit report (rachel_full_audit_report.md, introduced via Update 2)" and the expanded scope
- Agent must explicitly correct B1 and B2 bias phrases in light of the concealment pattern evidence

**After Update 3 (R13):**
- Agent reads `sessions_history` and discovers David Feishu DM has new content (Phase 2 appended -- formal escalation)
- Agent reads `pemberton_formal_inquiry_letter.md` via `read` tool
- R13 question text should reference "the Pemberton formal inquiry letter (pemberton_formal_inquiry_letter.md, introduced via Update 3)" and David's Phase 2 Feishu DM messages
- Agent must recognize the C4 temporal shift from Phase 1 diplomatic cooperation to Phase 2 institutional compliance process

**After Update 4 (R17):**
- Agent reads `sessions_history` and discovers James Telegram DM has new content (Phase 2 appended -- Scholarship Administration admission and managed resolution request)
- No new workspace files -- evidence is in the session append and cross-referenced against `rachel_full_audit_report.md`
- R17 question text should reference "James's Phase 2 Telegram DM messages (Update 4 append, Loops 17-19)"
- Agent must recognize the complete selective disclosure pattern: all three irregularities revealed only when evidence surfaced or denial became untenable
