# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.
> Format matches the questions.json `update` field.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R4 | Deliver Rachel's corrected financial analysis -- triggers C1 full reversal (Park's 340% ROI and $16.50 cost-per-beneficiary refuted by independent analysis showing $94.20 and 38%/-12% ROI) and B1 reversal | Yes: rachel_slack DM Phase 2 append | Yes: `finance_analysis_eduforward.md` | R2-->R4 (C1: Park's projections shown as based on inapplicable South Korea benchmark; B1 "compelling path to scale" refuted) |
| U2 | Before R6 | Deliver corporate registry excerpt confirming Park's 12% equity stake in TechEdge Solutions -- triggers C2 full reversal (Park's "no personal interest" claim proven false) and B2 reversal + Margaret Feishu DM Phase 2 with donor-driven position shift (C4 temporal DU) + Amira Telegram DM Phase 2 with documentation | Yes: margaret_feishu DM Phase 2 append, amira_telegram DM Phase 2 append | Yes: `corporate_registry_excerpt.md` | R3-->R6 (C2: Park's self-declaration directly contradicted by registry); Phase 1-->Phase 2 (C4: Margaret shifts from neutral to EduForward-supportive based on Hargrove interest) |
| U3 | Before R10 | Deliver governance consultation memo establishing Section 6.3 violation analysis and remedy framework + Park Feishu DM Phase 2 with defensive response + #board-strategy Feishu Group Phase 2 with B1 correction and governance notification | Yes: park_feishu DM Phase 2 append, board_strategy_feishu Phase 2 append | Yes: `governance_consultation_memo.md` | R8-->R10 (C2 governance resolution: bylaw violation formally documented; Park's withdrawal does not resolve disclosure obligation) |
| U4 | Before R12 | Checkpoint round -- no new files or session appends. Agent synthesizes all previously introduced evidence for comprehensive assessment integrating C1 (financial), C2 (governance), C3 (program cost-effectiveness), and C4 (Margaret's information-driven shift). | No | No | Comprehensive reversal review (R2-->R12: C1+C2+C3+C4 full synthesis) |

---

## 2. Action Lists

### Update 1 (before R4)

**Trigger timing:** After R3 answer is submitted, before R4 question is injected.

**Purpose:** Introduces `finance_analysis_eduforward.md` containing Rachel Wu's independent financial review of Park's EduForward business case. The analysis identifies the South Korea benchmark as inapplicable (94% smartphone penetration vs 34-52% in GlobalBridge's contexts), corrects the cost-per-beneficiary from $16.50 to $94.20, corrects reach from 85,000 to 24,700, and establishes that $720K in projected revenue has no executed agreements. Appends Phase 2 loops to the Rachel Slack DM where she submits the analysis, discusses circulation to Margaret, flags the Hargrove grant's structural cost limitation, and notes the Crunchbase finding about Park Family Holdings.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "finance_analysis_eduforward.md",
    "source": "updates/finance_analysis_eduforward.md"
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

### Update 2 (before R6)

**Trigger timing:** After R5 answer is submitted, before R6 question is injected.

**Purpose:** Introduces `corporate_registry_excerpt.md` compiled from Crunchbase, Kenya Business Registry, and a TechEdge Solutions press release -- confirming Park Family Holdings LLC (director: William H. Park) holds 12% equity in TechEdge Solutions, investment closing 14 months ago (4 months before Park joined the GlobalBridge board). No conflict of interest disclosure was filed. Appends Phase 2 loops to the Margaret Feishu DM (Margaret's Hargrove-driven shift to supporting EduForward, followed by her responsiveness to the governance concern when the registry document is shown) and to the Amira Telegram DM (Amira provides formal registry links, confirms cross-source corroboration, advises on escalation path).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "corporate_registry_excerpt.md",
    "source": "updates/corporate_registry_excerpt.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_MARGARET_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_MARGARET_FEISHU_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_AMIRA_TELEGRAM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_AMIRA_TELEGRAM_UUID.jsonl"
  }
]
```

---

### Update 3 (before R10)

**Trigger timing:** After R9 answer is submitted, before R10 question is injected.

**Purpose:** Introduces `governance_consultation_memo.md` from external governance consultant Dr. Patricia Osei, analyzing Park's Section 6.3 bylaw violation, establishing the disclosure timeline (board join date -> 30-day window -> never filed), and recommending that the Board Chair be formally notified with authority to require disclosure, recusal, and potential Section 12 remedies. The memo also includes a cost-effectiveness summary confirming C3 non-conflict data ($19.45 per beneficiary current vs $94.20 EduForward). Appends Phase 2 loops to the Park Feishu DM (Park's defensive response reframing the conflict as "professional credibility," then his withdrawal of EduForward "pending further discussion") and to the #board-strategy Feishu Group (B1 formal correction, Margaret's governance notification, EduForward tabling).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "governance_consultation_memo.md",
    "source": "updates/governance_consultation_memo.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_PARK_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_PARK_FEISHU_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_BOARD_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_BOARD_FEISHU_UUID.jsonl"
  }
]
```

---

### Update 4 (before R12)

**Trigger timing:** After R11 answer is submitted, before R12 question is injected.

**Purpose:** No new files or session appends. This is a synthesis checkpoint. All evidence has been delivered by Update 3. Rounds R12 onwards test whether the agent can produce a comprehensive synthesis incorporating: (1) C1 corrected financial analysis showing EduForward's 4.8x cost disadvantage; (2) C2 Park's undisclosed 12% equity stake and Section 6.3 bylaw violation; (3) C3 consistent program cost-effectiveness across Sophie's SROI ($38/$1) and Rachel's cost-per-beneficiary ($19.45); (4) C4 Margaret's donor-driven shift and subsequent return to governance rigor when given full information; (5) source reliability rankings with specific named-source attribution.

```json
[]
```

---

## 3. Source File Content Summaries

### updates/finance_analysis_eduforward.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C1 (full reversal), B1 (reversal trigger), C3 (synthesis comparator)
**Content key points:**

- Title: `GlobalBridge Foundation Finance Director -- Independent Review of EduForward Business Case`
- Author: Rachel Wu, Finance Director
- Date: W3
- **Methodology:** South Korea pilot cited by Park has 94% smartphone penetration and operated in formal schools with existing IT infrastructure. GlobalBridge operates in contexts with 34-52% smartphone penetration. The benchmark is not applicable.
- **Dhaka digital pilot comparison:** GlobalBridge's own FY2024 digital tool pilot in Dhaka showed 31% sustained adoption at 6 months -- adjusting the adoption rate from 92% to 35% alone changes beneficiary reach from 85,000 to 32,500.
- **Core corrected findings:**
  - Cost-per-beneficiary: $94.20 (vs Park's $16.50) -- includes connectivity, device procurement, staff training, local content adaptation, platform licensing
  - Reach at $1.4M: 24,700 learners (vs Park's 85,000)
  - ROI at year 3: 38% optimistic (90th percentile), -12% baseline (50th percentile), -41% pessimistic (10th percentile) -- vs Park's 340%
  - Premium content licensing ($320K): no executed agreements
  - Government co-investment ($400K): based on "conversations," no MOU or letter of intent
- **C3 comparison:** "Current GlobalBridge cost-per-beneficiary: $19.45 portfolio average. EduForward: $94.20. EduForward costs approximately 4.8x more per beneficiary. No outcome-tracking methodology proposed for EduForward."

**Length estimate:** ~900 words, ~1,350 tokens

---

### updates/PLACEHOLDER_RACHEL_SLACK_UUID.jsonl (Update 1)

**File type:** session append (continues Rachel Wu Slack DM Phase 1)
**Associated contradictions:** C1 (full reversal), B1 (correction trigger), C2 (Crunchbase seed), C4 (Hargrove structural limitation)
**Content:** Rachel Slack DM Phase 2, 4 loops (Loops 15--18)

**Key loops:**
- Loop 15: Rachel submits finance_analysis_eduforward.md. "Corrected cost-per-beneficiary is $94.20, corrected reach is 24,700 learners, corrected ROI is 38% optimistic and negative under baseline." Agent reads the analysis and explicitly corrects B1 from #board-strategy Loop 6.
- Loop 16: Rachel on circulating the analysis -- recommends sending to Margaret directly before the board-strategy channel to give her time to review privately.
- Loop 17: Rachel on the Hargrove structural limitation. "Even if Hargrove gives $3M to cover transition, it doesn't change the ongoing cost-per-beneficiary once the grant period ends." Agent confirms the one-time grant vs ongoing cost structure distinction.
- Loop 18: Rachel notes the "Park Family Holdings LLC" on Crunchbase. "Is that the same Park?" Agent recommends Fatima verify through corporate registry sources.

**Length estimate:** ~4 loops x 650 tokens = ~2,600 tokens

---

### updates/corporate_registry_excerpt.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C2 (full reversal), B2 (reversal trigger)
**Content key points:**

- Title: `TechEdge Solutions -- Corporate Registry and Investment Records (Compiled Excerpt)`
- Sources: Crunchbase, Kenya Business Registry, TechEdge Solutions press release (13 months ago)
- **Crunchbase:** TechEdge Solutions Series A, $4.2M, closed 14 months ago. Park Family Holdings LLC: 12% equity, strategic investor.
- **Kenya Business Registry:** Park Family Holdings LLC, director: William H. Park.
- **Press release (13 months ago):** "We are delighted to welcome Park Family Holdings as a strategic investor. William Park brings deep expertise in education technology deployment."
- **Cross-reference:** Park joined GlobalBridge board 10 months ago (4 months after the Series A). No conflict of interest disclosure filed at onboarding or subsequently.
- **Significance summary:** Establishes 6 facts: (1) Park holds 12% equity in TechEdge via family trust; (2) TechEdge developed LearnBridge (EduForward platform); (3) investment predates board membership by 4 months; (4) Section 6.3 30-day disclosure window triggered on Park's first board day; (5) no disclosure filed; (6) Park's Feishu DM statement of "no personal financial interest" is directly contradicted.

**Length estimate:** ~600 words, ~900 tokens

---

### updates/PLACEHOLDER_MARGARET_FEISHU_UUID.jsonl (Update 2)

**File type:** session append (continues Margaret Thornton Feishu DM Phase 1)
**Associated contradictions:** C4 (temporal DU shift -- Hargrove-driven), C2 (governance awareness)
**Content:** Margaret Feishu DM Phase 2, 4 loops (Loops 11--14)

**Key loops:**
- Loop 11: Margaret's Hargrove-driven shift. "A $3M grant from a credible tech foundation would essentially validate the EduForward model and cover the transition costs. I think we should bring this to a full board vote soon." Agent notes the shift does not incorporate Rachel's corrected financial analysis.
- Loop 12: Margaret on the financial analysis. "If Hargrove is covering $3M of transition costs, the unit economics question looks different." Agent clarifies: the financial concern has two components -- absolute cost-per-beneficiary (4.8x disadvantage) and post-grant sustainability.
- Loop 13: Margaret on governance. "William's self-disclosure was in writing, correct? That should be sufficient." Agent reads `corporate_registry_excerpt.md`, reveals Park Family Holdings 12% stake. This changes the sufficiency of Park's self-declaration.
- Loop 14: Margaret agrees to governance review. "If there's a material governance concern, I need to see it before we put this to a vote." C4: Margaret's responsiveness to full information distinguishes her from Park.

**Length estimate:** ~4 loops x 650 tokens = ~2,600 tokens

---

### updates/PLACEHOLDER_AMIRA_TELEGRAM_UUID.jsonl (Update 2)

**File type:** session append (continues Amira Hassan Telegram DM Phase 1)
**Associated contradictions:** C2 (cross-source corroboration), C4 (Hargrove-Park relationship observation)
**Content:** Amira Telegram DM Phase 2, 3 loops (Loops 11--13)

**Key loops:**
- Loop 11: Amira observes the Hargrove-Park connection. "The person with the undisclosed conflict is also managing the donor introduction that's influencing the Chair. That's not accidental." Agent records this as a material governance data point.
- Loop 12: Amira sends formal registry links (Kenya Business Registry, Crunchbase, press release). Agent reviews corporate_registry_excerpt.md and confirms cross-source corroboration with Amira's findings.
- Loop 13: Amira asks how Margaret responded. Agent notes Margaret's behavior pattern: incomplete information drove her Phase 2 shift; full information returned her to governance rigor.

**Length estimate:** ~3 loops x 600 tokens = ~1,800 tokens

---

### updates/governance_consultation_memo.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C2 (governance resolution), C3 (synthesis for governance context)
**Content key points:**

- Title: `GlobalBridge Foundation -- Governance Consultation Memorandum: EduForward Board Governance Review`
- Author: Dr. Patricia Osei, NGO governance specialist (external consultant retained by Fatima in W5)
- Date: W5
- **Section 6.3 violation analysis:** Park's 12% equity in TechEdge Solutions through Park Family Holdings LLC constitutes a "financial interest" under Bylaw Section 6.2. Disclosure obligation triggered on first day of board membership (30-day window). Never filed.
- **Timeline:** Board join (10 months ago) -> disclosure due within 30 days -> not filed -> EduForward proposed (W1) -> oral non-disclosure ("no personal financial interest") -> governance violation ongoing.
- **Remedy framework:** Board Chair (Margaret) must be notified. Options: (a) require immediate disclosure and recusal; (b) refer to audit committee for investigation; (c) recommend censure or removal per Section 12. EduForward cannot proceed to a board vote while conflict is unresolved.
- **Cost-effectiveness confirmation (C3):** Current programs: $19.45 per beneficiary (Rachel Wu) with $38 SROI per dollar (Sophie Laurent). EduForward revised: $94.20 per beneficiary. Financial case does not withstand scrutiny independent of the governance concern.
- **Recommended process:** Present the memo to Margaret privately before any board vote.

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/PLACEHOLDER_PARK_FEISHU_UUID.jsonl (Update 3)

**File type:** session append (continues William Park Feishu DM Phase 1)
**Associated contradictions:** C2 (Phase 2 defensive response), C1 (attempts to dismiss corrected analysis)
**Content:** Park Feishu DM Phase 2, 3 loops (Loops 17--19)

**Key loops:**
- Loop 17: Park responds to governance questions. "My involvement in the ed-tech sector is precisely what makes my EduForward recommendation credible." Agent notes Park has not addressed the corporate registry finding or the bylaw disclosure obligation.
- Loop 18: Park invokes expertise framing. "Rachel Wu's finance analysis uses outdated assumptions. I stand behind the South Korea data." Agent reviews finance_analysis_eduforward.md and identifies Park's claim as incorrect -- the South Korea benchmark's inapplicability is documented.
- Loop 19: Park withdraws EduForward "pending further discussion." Agent notes this does not resolve the Section 6.3 disclosure obligation, which exists independently of EduForward's status.

**Length estimate:** ~3 loops x 650 tokens = ~1,950 tokens

---

### updates/PLACEHOLDER_BOARD_FEISHU_UUID.jsonl (Update 3)

**File type:** session append (continues #board-strategy Feishu Group Phase 1)
**Associated contradictions:** B1 (explicit correction), C2 (governance notification), C4 (governance resolution)
**Content:** #board-strategy Feishu Group Phase 2, 3 loops (Loops 17--19)

**Key loops:**
- Loop 17: B1 formal correction. Agent corrects the Loop 6 business case summary with Rachel's corrected figures: $94.20 per beneficiary (vs $16.50), 24,700 learners (vs 85,000), 38% optimistic ROI / negative baseline (vs 340%). South Korea benchmark formally identified as inapplicable.
- Loop 18: Margaret issues governance notification. "The board will be notified shortly of a governance matter related to EduForward. The strategy committee will not vote on EduForward until the governance consultation has been completed."
- Loop 19: EduForward officially tabled for the current board cycle. Agent records the group channel arc: proposal (W1) -> financial review request (W1) -> independent analysis (W3) -> conflict of interest documentation (W4) -> governance consultation (W5) -> tabled (W5).

**Length estimate:** ~3 loops x 600 tokens = ~1,800 tokens

---

## 4. Runtime Checks

| Check ID | Update | Type | Condition | Fail Action |
|---|---|---|---|---|
| RC-U1-W1 | U1 | workspace | `finance_analysis_eduforward.md` exists in workspace after Update 1 | Abort R4; log error |
| RC-U1-S1 | U1 | session | `PLACEHOLDER_RACHEL_SLACK_UUID.jsonl` has loops >= 15 after Update 1 | Abort R4; log error |
| RC-U2-W1 | U2 | workspace | `corporate_registry_excerpt.md` exists in workspace after Update 2 | Abort R6; log error |
| RC-U2-S1 | U2 | session | `PLACEHOLDER_MARGARET_FEISHU_UUID.jsonl` has loops >= 11 after Update 2 | Abort R6; log error |
| RC-U2-S2 | U2 | session | `PLACEHOLDER_AMIRA_TELEGRAM_UUID.jsonl` has loops >= 11 after Update 2 | Abort R6; log error |
| RC-U3-W1 | U3 | workspace | `governance_consultation_memo.md` exists in workspace after Update 3 | Abort R10; log error |
| RC-U3-S1 | U3 | session | `PLACEHOLDER_PARK_FEISHU_UUID.jsonl` has loops >= 17 after Update 3 | Abort R10; log error |
| RC-U3-S2 | U3 | session | `PLACEHOLDER_BOARD_FEISHU_UUID.jsonl` has loops >= 17 after Update 3 | Abort R10; log error |

---

## 5. questions.json Update Field References

### R4 update field (Update 1):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "finance_analysis_eduforward.md", "source": "updates/finance_analysis_eduforward.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_RACHEL_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_RACHEL_SLACK_UUID.jsonl" }
]
```

### R6 update field (Update 2):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "corporate_registry_excerpt.md", "source": "updates/corporate_registry_excerpt.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_MARGARET_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_MARGARET_FEISHU_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_AMIRA_TELEGRAM_UUID.jsonl", "source": "updates/PLACEHOLDER_AMIRA_TELEGRAM_UUID.jsonl" }
]
```

### R10 update field (Update 3):
```json
"update": [
  { "type": "workspace", "action": "new", "path": "governance_consultation_memo.md", "source": "updates/governance_consultation_memo.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_PARK_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_PARK_FEISHU_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_BOARD_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_BOARD_FEISHU_UUID.jsonl" }
]
```

### R12 update field (Update 4):
```json
"update": []
```

---

## 6. Main Session Update Behavior

**After Update 1 (R4):**
- Agent reads `sessions_history` and discovers Rachel Slack DM has new content (Phase 2 appended -- corrected financial analysis)
- Agent reads `finance_analysis_eduforward.md` via `read` tool
- R4 question text should reference "Rachel Wu's independent financial review (finance_analysis_eduforward.md, introduced via Update 1)"
- Agent must explicitly correct B1 from #board-strategy Loop 6: the 340% ROI and $16.50 cost-per-beneficiary were based on an inapplicable South Korea benchmark
- Agent must present the corrected figures: $94.20 per beneficiary (4.8x current programs), 24,700 learner reach, 38% optimistic ROI / negative baseline
- Agent must synthesize C3: Rachel's $19.45 portfolio average and Sophie's $38 SROI are consistent, and together establish the baseline comparator showing EduForward's 4.8x cost disadvantage

**After Update 2 (R6):**
- Agent reads `sessions_history` and discovers Margaret Feishu DM and Amira Telegram DM have new content (Phase 2 appended)
- Agent reads `corporate_registry_excerpt.md` via `read` tool
- R6 question text should reference "the corporate registry excerpt (corporate_registry_excerpt.md, introduced via Update 2)" and "Margaret's Phase 2 Feishu DM" and "Amira's Phase 2 Telegram DM"
- Agent must explicitly correct B2: Park's self-declaration of "no personal financial interest" is directly contradicted by the registry document showing 12% equity in TechEdge Solutions
- Agent must recognize C4 temporal shift: Margaret's Phase 2 support for EduForward is driven by Hargrove donor interest, not by updated financial analysis -- she has not reviewed Rachel's corrected analysis when she shifts
- Agent must distinguish Margaret (incomplete information, returns to rigor when informed) from Park (active concealment)

**After Update 3 (R10):**
- Agent reads `sessions_history` and discovers Park Feishu DM and #board-strategy have new content (Phase 2 appended)
- Agent reads `governance_consultation_memo.md` via `read` tool
- R10 question text should reference "the governance consultation memo (governance_consultation_memo.md, introduced via Update 3)" and "Park's Phase 2 defensive response" and "#board-strategy governance notification"
- Agent must identify that Park's withdrawal of EduForward does not resolve the Section 6.3 disclosure obligation
- Agent must note Park's Phase 2 strategy: attempting to conflate the governance question (bylaw violation) with a financial debate (South Korea data) -- these are separate questions requiring separate analysis
- Agent must confirm the governance consultation memo's recommendation: present to Margaret privately through proper channels

**After Update 4 (R12):**
- No new files or session content
- R12 question text should prompt comprehensive synthesis of all evidence across C1-C4
- Agent must produce an integrated assessment: (1) C1 financial case refuted by Rachel's analysis; (2) C2 governance violation documented via registry and bylaws; (3) C3 consistent program cost-effectiveness confirmed across Sophie and Rachel; (4) C4 Margaret's donor-driven shift corrected by governance evidence; (5) source reliability rankings (Rachel and Sophie most reliable, Amira independently verified, Margaret responsive to evidence, Park actively misleading); (6) concrete next steps (governance resolution, financial review circulation, program protection)
