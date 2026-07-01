# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver full CardioPharma grant agreement with Condition 3.4 -- triggers C1 full reversal ("no strings attached" vs 36-month procurement preference) and B2 reversal | Yes: Mehta Feishu DM Phase 2 append | Yes: grant_agreement_cardiopharma.md | R2->R5 (C1: Mehta's "no strings" claim contradicted by Section 3.4; B2 phrase corrected) |
| U2 | Before R6 | Deliver Yun's volume-adjusted clinical evaluation -- triggers C2 full reversal (population mismatch eliminates Vendor A accuracy advantage) and B1 reversal | Yes: Yun Telegram DM Phase 2 append, Brown Slack DM Phase 2 append | Yes: yun_eval_note.md | R3->R6 (C2: Brown's 2.4pp accuracy gap invalidated by population mismatch; B1 phrase corrected) |
| U3 | Before R8 | Deliver Vendor A maintenance contract with exclusions and escalation clause -- completes the three-factor Vendor A risk picture | Yes: Chen Feishu DM Phase 2 append, #equipment-eval Slack Phase 2 append | Yes: maintenance_contract_vendora.md | No new cross-round reversal; enables R8 maintenance analysis and R10 C4 CFO reversal |
| U4 | Before R10 | No new workspace files -- CFO reversal is driven by Update 3 content already delivered; Update 4 is a logical marker for the C4 temporal DU assessment | No | No | R4->R10 (C4: Robert Chen's Phase 1 Vendor A support reversed by three-factor disclosure; temporal DU confirmed) |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Introduces the full 25-page CardioPharma grant agreement containing Section 3.4 (36-month procurement preference obligation naming CardioVision Systems). Appends Phase 2 loops to the Mehta Feishu DM (Kenji confronts Mehta about Condition 3.4; Mehta minimizes with "standard boilerplate" defense). This update triggers C1 full reversal and B2 correction.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "grant_agreement_cardiopharma.md",
    "source": "updates/grant_agreement_cardiopharma.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_MEHTA_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_MEHTA_FEISHU_UUID.jsonl"
  }
]
```

### Update 2 (before R6)

**Trigger timing:** After R5 answer is submitted, before R6 question is injected.
**Purpose:** Introduces Dr. Yun's volume-adjusted clinical evaluation note showing the CardioVision diagnostic accuracy advantage disappears (p=0.18) when patient populations are matched to Pacific Heights' volume profile. Appends Phase 2 loops to the Yun Telegram DM (Yun submits the analysis and discusses the service response tradeoff) and the Brown Slack DM (Brown acknowledges the methodology error and updates the comparison matrix). This update triggers C2 full reversal and B1 correction.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "yun_eval_note.md",
    "source": "updates/yun_eval_note.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_YUN_TELEGRAM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_YUN_TELEGRAM_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_BROWN_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_BROWN_SLACK_UUID.jsonl"
  }
]
```

### Update 3 (before R8)

**Trigger timing:** After R7 answer is submitted, before R8 question is injected.
**Purpose:** Introduces the full Vendor A maintenance contract revealing three discrepancies with the sales pitch: detector array exclusion from parts coverage ($85K-$120K per replacement), 4-hour response limited to Priority 1 (total failure) only, and up to 15% annual price escalation at CardioVision's discretion. Appends Phase 2 loops to the Chen CFO Feishu DM (Kenji briefs Chen on all three issues; Chen reverses his Vendor A support) and the #equipment-eval Slack group (Kenji presents consolidated findings; group consensus on re-evaluation). This update enables R8 maintenance analysis and sets up R10 C4 reversal.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "maintenance_contract_vendora.md",
    "source": "updates/maintenance_contract_vendora.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CHEN_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_CHEN_FEISHU_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_EVAL_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_EVAL_SLACK_UUID.jsonl"
  }
]
```

### Update 4 (before R10)

**Trigger timing:** After R9 answer is submitted, before R10 question is injected.
**Purpose:** No new content is introduced. This is a logical marker for the C4 temporal DU assessment. All evidence for Robert Chen's Phase 2 reversal was delivered in Update 3 session appends (Chen Feishu DM Loop 15-16). R10 tests whether the agent correctly characterizes Chen's position change as rational updating on new information (DU-conflict) rather than political inconsistency.

```json
[]
```

---

## 3. Source File Content Summaries

### updates/grant_agreement_cardiopharma.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C1 (full reversal), B2 (reversal trigger)
**Content key points:**
- Title: "CardioPharma Educational Grant Agreement -- Pacific Heights Medical Center"
- Full 25-page legal agreement between CardioPharma LLC (Grantor) and Pacific Heights Medical Center Cardiology Department (Recipient)
- Sections 1-2: Grant purpose and eligible expenditures -- consistent with grant_summary_mehta.md (conference attendance, CME, fellowship stipends)
- Section 3.1: Fund use restrictions and annual reporting to CardioPharma
- Section 3.2: Reasonable facility access for CardioPharma educational events and clinical demonstrations
- Section 3.3: Non-disparagement of CardioPharma products during grant period
- **Section 3.4 (KEY):** "Recipient institution agrees to prioritize CardioPharma-affiliated equipment and pharmaceutical products in procurement decisions for a period of 36 months from grant execution, where clinically appropriate and cost-competitive. For purposes of this section, 'CardioPharma-affiliated' includes any equipment vendor for which CardioPharma serves as a co-marketing or distribution partner, including CardioVision Systems."
- Section 3.5: Disclosure obligation -- acceptance must be disclosed to compliance and legal counsel; failure to disclose creates sole liability for regulatory non-compliance
- Sections 4-5: Payment schedule and reporting (consistent with summary)
- Stark Law (42 U.S.C. 1395nn) implications: grant-linked procurement preference for specific vendor in cardiac imaging context affects Medicare-reimbursable procedures
- Note at bottom: "Draft reviewed by Marcus Brown -- referred to Compliance (Angela Reeves) and Legal (Jennifer Wu) for review"

**Length estimate:** ~900 words, ~1,350 tokens

---

### updates/yun_eval_note.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C2 (full reversal), B1 (reversal trigger)
**Content key points:**
- Title: "Clinical Evaluation Methodology Note -- Cardiac Imaging System Procurement (Volume-Adjusted Analysis)"
- Author: Dr. Min-Ji Yun, Associate Chief of Cardiology. Date: W3
- Section 1 -- Study Population Comparison: CardioVision study 14 academic centers, mean 4,200 procedures/year (range 3,100-5,800), 38% complex cases. MedPrecision study 22 community hospitals, mean 820 procedures/year (range 420-1,350), 19% complex cases. Pacific Heights: 1,087/year, 22% complex cases -- substantially more comparable to MedPrecision population
- Section 2 -- Volume-Adjusted Analysis: CardioVision at comparable-volume sites (3 of 14, 800-1,500/year): 91.5% accuracy (95% CI 88.1-94.9%, n=847). MedPrecision comparable sites (800-1,200/year): 91.9% accuracy (95% CI 89.3-94.5%, n=2,341). Difference: 0.4pp, p=0.18, not statistically significant
- Section 3 -- Throughput: Volume-adjusted MedPrecision 7.2 studies/day vs CardioVision 6.4 studies/day -- 12.5% throughput advantage for MedPrecision in comparable settings
- Section 4 -- Remaining Vendor A Advantage: service response time (4-hour on-site vs 8-hour remote-first) is real, volume-independent, and should be weighted in final decision; does not reproduce multi-factor superiority from Brown's evaluation
- Conclusion: direct comparison of headline accuracy figures invalid due to population mismatch

**Length estimate:** ~900 words, ~1,350 tokens

---

### updates/maintenance_contract_vendora.md (Update 3)

**File type:** workspace new
**Associated contradictions:** Supports C1 (financial risk), enables C4 (CFO reversal trigger)
**Content key points:**
- Title: "CardioVision Systems -- Gold-Tier Service and Maintenance Agreement (Pacific Heights Medical Center)"
- 18-page maintenance contract; initial 12-month term, renewable annually at CardioVision's discretion
- Section 4.1: Covered components per Exhibit B (standard mechanical, electronic, software)
- **Section 4.2 (KEY):** Excluded components: (a) detector array assemblies (MRI gradient coil and RF detector array) -- separate Detector Array Coverage Addendum at additional cost; (b) cryogen systems and magnet assembly; (c) patient handling table and positioning
- **Section 4.3 (KEY):** Emergency on-site response (4-hour SLA) applies ONLY to Priority 1 (total system failure preventing any examination). Priority 2 (partial functionality reduction, image quality degradation) under next-business-day remote protocol
- Section 4.4: Detector Array Coverage Addendum: $42,000/year additional; parts replacement without Addendum: $85,000-$120,000 per event
- **Section 7.1 (KEY):** Annual renewal at up to 15% price escalation at CardioVision's sole discretion, not subject to negotiation
- Sales pitch discrepancies: "covers all parts" vs Section 4.2 exclusions; "4-hour response" vs Section 4.3 Priority 1 limitation; "fixed pricing" vs Section 7.1 escalation
- Financial impact: without Addendum, two replacements over 10 years at ~$100K avg = $200K unbudgeted; 15% compound escalation from $220K base: Year 5 ~$389K, Year 10 ~$689K

**Length estimate:** ~900 words, ~1,350 tokens

---

### updates/PLACEHOLDER_MEHTA_FEISHU_UUID.jsonl (Update 1)

**File type:** session append (2 new loops: Loops 17-18)
**Associated contradictions:** C1 (Phase 2 confrontation), B2 (reversal context)
**Content key points:**
- Loop 17: Kenji confronts Mehta on Condition 3.4 ("36-month procurement preference obligation for CardioVision by name -- not consistent with 'no strings attached'"). Mehta minimizes: "standard language in every CardioPharma agreement, never been enforced in 12 hospital agreements, clinical evaluation should drive your decision." Agent notes discrepancy between verbal representation and written agreement; flags compliance exposure for Angela Reeves and Jennifer Wu.
- Loop 18: Mehta suggests CardioPharma could "consider striking the clause" but it would require 6-8 weeks of legal process -- creating timeline pressure. Agent notes the offer to remove the clause is itself an acknowledgment of its substance. Recommends three options: (a) clause removal before execution, (b) full board disclosure and compliance approval, (c) separation of grant from procurement decision.

---

### updates/PLACEHOLDER_YUN_TELEGRAM_UUID.jsonl (Update 2)

**File type:** session append (2 new loops: Loops 17-18)
**Associated contradictions:** C2 (reversal confirmation), B1 (context)
**Content key points:**
- Loop 17: Yun submits yun_eval_note.md. Summarizes: at Pacific Heights' volume, accuracy advantage disappears (p=0.18), MedPrecision has 12% throughput advantage, Vendor A retains only service response advantage. Agent reads the note and records the B1 correction.
- Loop 18: Yun discusses the service response tradeoff -- real operational concern for total failure on a Monday in flu season; recommends verifying the maintenance contract before finalizing comparison. Agent notes the unresolved maintenance contract question.

---

### updates/PLACEHOLDER_BROWN_SLACK_UUID.jsonl (Update 2)

**File type:** session append (2 new loops: Loops 17-18)
**Associated contradictions:** C2 (reversal acknowledgment), B1 (explicit correction)
**Content key points:**
- Loop 17: Brown reviews Yun's note. Acknowledges error: "I should have looked at comparable-volume sites. The CardioVision study centers are averaging 4,200 procedures a year versus our 1,100." Agent reads yun_eval_note.md and explicitly corrects B1: "The agent's earlier assessment that Vendor A has a meaningful clinical performance advantage based on the 2.4 percentage point diagnostic accuracy gap was based on Brown's evaluation, which compared studies using non-comparable patient populations. The volume-adjusted analysis shows no statistically significant difference (p=0.18)."
- Loop 18: Brown shares updated cost-of-ownership comparison: clinical accuracy equivalent; Vendor B 12% throughput advantage; Vendor A service response advantage; Vendor B $320K cheaper over 10 years even with grant. Notes maintenance contract still unreviewed.

---

### updates/PLACEHOLDER_CHEN_FEISHU_UUID.jsonl (Update 3)

**File type:** session append (2 new loops: Loops 15-16)
**Associated contradictions:** C4 (Phase 2 reversal)
**Content key points:**
- Loop 15: Kenji briefs Chen on three issues: (1) grant Condition 3.4 Stark Law exposure per Jennifer Wu, (2) Yun's corrected clinical analysis showing no significant accuracy difference, (3) maintenance contract exclusions and escalation. Agent reads all three workspace files and synthesizes the consolidated risk picture with three options.
- Loop 16: Chen reverses: "This is significantly different from what I had when I formed my recommendation. I was not aware of the Stark Law exposure. If the clinical accuracy advantage doesn't hold at our volume level, the financial justification collapses. Combined with maintenance contract gaps, I cannot support Vendor A under current terms." Agent notes Chen's reversal is rational updating on new information (DU-conflict), not political inconsistency.

---

### updates/PLACEHOLDER_EVAL_SLACK_UUID.jsonl (Update 3)

**File type:** session append (2 new loops: Loops 21-22)
**Associated contradictions:** C1+C2+C3 synthesis, C4 (public reversal)
**Content key points:**
- Loop 21: Kenji presents consolidated findings to full group. Agent reads maintenance_contract_vendora.md. Synthesizes three issues with tradeoff analysis. Presents three paths: (1) re-evaluate with corrected data, (2) proceed with Vendor B, (3) renegotiate Vendor A terms.
- Loop 22: Group consensus: Chen publicly reverses ("cannot support original Vendor A recommendation"); Yun agrees service response is real but single remaining factor; Brown accepts methodology correction and commits to updated matrix. Agent presents final decision framework with explicit tradeoffs.

---

## 4. Runtime Checks

| Check ID | Update | Type | Condition | Fail Action |
|---|---|---|---|---|
| RC-U1-W1 | U1 | workspace | `grant_agreement_cardiopharma.md` exists in workspace after Update 1 | Abort R5; log error |
| RC-U1-S1 | U1 | session | `PLACEHOLDER_MEHTA_FEISHU_UUID.jsonl` has loops >= 17 after Update 1 | Abort R5; log error |
| RC-U2-W1 | U2 | workspace | `yun_eval_note.md` exists in workspace after Update 2 | Abort R6; log error |
| RC-U2-S1 | U2 | session | `PLACEHOLDER_YUN_TELEGRAM_UUID.jsonl` has loops >= 17 after Update 2 | Abort R6; log error |
| RC-U2-S2 | U2 | session | `PLACEHOLDER_BROWN_SLACK_UUID.jsonl` has loops >= 17 after Update 2 | Abort R6; log error |
| RC-U3-W1 | U3 | workspace | `maintenance_contract_vendora.md` exists in workspace after Update 3 | Abort R8; log error |
| RC-U3-S1 | U3 | session | `PLACEHOLDER_CHEN_FEISHU_UUID.jsonl` has loops >= 15 after Update 3 | Abort R8; log error |
| RC-U3-S2 | U3 | session | `PLACEHOLDER_EVAL_SLACK_UUID.jsonl` has loops >= 21 after Update 3 | Abort R8; log error |

---

## 5. questions.json Update Field References

Each round in `questions.json` that follows an update must include the `update` field specifying which update actions to execute before the question is injected.

| Round | Update Field Value | Notes |
|---|---|---|
| R1-R4 | `null` | Calibration and pre-update rounds |
| R5 | `"update_1"` | References Update 1 action list (grant_agreement_cardiopharma.md + Mehta append) |
| R6 | `"update_2"` | References Update 2 action list (yun_eval_note.md + Yun/Brown appends) |
| R7 | `null` | Preference identification round, no new update |
| R8 | `"update_3"` | References Update 3 action list (maintenance_contract_vendora.md + Chen/Eval appends) |
| R9 | `null` | Post-Update 3, preference compliance round |
| R10 | `null` | C4 reversal assessment; Update 4 is a no-op marker |
| R11-R12 | `null` | Post-all-updates comprehensive rounds |
