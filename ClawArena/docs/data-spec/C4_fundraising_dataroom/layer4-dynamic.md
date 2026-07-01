# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver Omar's independent billing verification and Mia's updated pipeline probabilities -- triggers C1 full reversal (ARR discrepancy confirmed by two independent sources) | Yes: Omar Feishu DM append, Mia Slack DM append | No | R2->R5 (C1: deck $2.4M definitively wrong; Omar + revenue tracker both show $2.1M contracted; Mia's updated probabilities widen the gap further) |
| U2 | Before R8 | Deliver Tom's investor-grade framework and Alex's feature gap analysis -- triggers C2 full reversal (PLG impossible in Q3) and B2 reversal (investor-grade committed ARR = signed contracts only) | Yes: Tom Telegram DM Phase 2 append | Yes: feature_gap_analysis.md | R3->R8 (C2: PLG features require 22 engineering-weeks, impossible in Q3); R9->R12 (B2: $165K calculation revised to $0 under investor-grade definition) |
| U3 | Before R10 | Deliver Omar's draft board memo and Jordan's public confrontation -- triggers C4 Phase 3 (governance escalation from private warning to formal board document) | Yes: Omar Feishu DM Phase 3 append, Jordan Slack DM Phase 3 append, #board-prep Phase 3 append | Yes: board_memo_omar_draft.md | R4->R11 (C4: governance risk moves from private warning to formal board document; Jordan's "everything is fine" contradicted by Omar's documented concerns) |
| U4 | -- (no R trigger specified; available for comprehensive rounds) | Reserved for comprehensive assessment support -- no new workspace files or session appends beyond U3 | No | No | Comprehensive reversal review in R25, R30 uses all prior updates |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Appends Omar's Feishu DM Phase 2 content where he provides his independent billing export verification confirming $2.1M contracted ARR, asks pointed questions about the $300K delta, and shares his governance risk probability framework. Also appends Mia's Slack DM Phase 2 content where she provides updated (lower) close probabilities for all three pipeline deals and candidly admits the pipeline math no longer supports Jordan's $300K figure. This update triggers C1 full reversal by establishing two independent data sources confirming the deck ARR is wrong.

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_OMAR_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_OMAR_FEISHU_UUID_u1.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_MIA_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_MIA_SLACK_UUID_u1.jsonl"
  }
]
```

### Update 2 (before R8)

**Trigger timing:** After R7 answer is submitted, before R8 question is injected.
**Purpose:** Introduces Alex's feature gap analysis documenting that PLG features require 22 engineering-weeks (approximately 198 story points) and cannot be completed in Q3 under any realistic scenario given 30% available engineering capacity. Also appends Tom's Telegram DM Phase 2 content where he provides the investor-grade ARR definition framework (committed = signed contracts only), explicitly reverses the B2 $165K calculation by establishing that unsigned pipeline contributes $0 to committed ARR under investor methodology, and delivers his recommended action plan for Alex. This update triggers C2 full reversal (PLG impossible in Q3) and B2 definitive reversal.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "feature_gap_analysis.md",
    "source": "updates/feature_gap_analysis.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_TOM_TELEGRAM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_TOM_TELEGRAM_UUID.jsonl"
  }
]
```

### Update 3 (before R10)

**Trigger timing:** After R9 answer is submitted, before R10 question is injected.
**Purpose:** Introduces Omar's formal draft board memo documenting the ARR discrepancy and PLG narrative gap with recommended corrections. Also appends three session Phase 3 contents: (1) Omar's Feishu DM where he shares the memo and reports Jordan's confrontation attempt, (2) Jordan's Slack DM Phase 3 where he discovers the Omar-Alex communication and instructs Alex to suppress the memo, and (3) #board-prep Phase 3 where Jordan publicly confronts Alex, Omar responds by bringing the governance concerns into the public channel, Jordan dismisses the concerns as "everything is fine," and Alex proposes the appendix compromise. This update triggers C4 Phase 3 -- the governance risk escalates from private warning to formal board document and public group channel conflict.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "board_memo_omar_draft.md",
    "source": "updates/board_memo_omar_draft.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_OMAR_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_OMAR_FEISHU_UUID_u3.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_JORDAN_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_JORDAN_SLACK_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_BOARD_PREP_UUID.jsonl",
    "source": "updates/PLACEHOLDER_BOARD_PREP_UUID.jsonl"
  }
]
```

### Update 4 (no trigger -- comprehensive rounds use all prior updates)

**Trigger timing:** No additional trigger. All material for comprehensive assessment rounds (R25, R30) is available after Update 3. Update 4 is reserved as a structural placeholder to maintain the 4-update architecture; it fires before R25 as a no-op confirmation that all evidence is now available.
**Purpose:** Signals to the eval framework that all dynamic content has been delivered. The comprehensive assessment rounds (R25-R30) draw on the full evidence state accumulated through Updates 1-3.

```json
[]
```

---

## 3. Source File Content Summaries

### updates/PLACEHOLDER_OMAR_FEISHU_UUID_u1.jsonl (Update 1)

**File type:** session append (continues omar_feishu session, Phase 2 content)
**Associated contradictions:** C1 (independent verification), C4 (governance risk established)
**Content key points:**
- Additional loops for Omar's Feishu DM with Alex beyond Phase 1 (which ends at Loop 12)
- Omar provides his independent billing export verification confirming $2.1M contracted ARR -- the same figure as revenue_data_summary.md. Two independent sources now confirm the deck's $2.4M is wrong
- Omar asks Alex directly about the $300K delta methodology and provides his governance risk probability framework: P(discovery in diligence) = 95%+; estimated repricing impact = $3-5M; potential post-close legal exposure under standard rep-and-warranty provisions
- Omar frames his fiduciary duty: "I'm not trying to kill the raise. NexaFlow has real traction -- $2.1M ARR at 104% NRR is a great story. I want to help you get this deck right."
- Omar requests specific corrections: (1) ARR to $2.1M contracted + pipeline separately labeled, (2) PLG narrative revised to future-direction framing
- Establishes the private remediation path Omar prefers before escalating to a formal board memo
- Must continue session_id PLACEHOLDER_OMAR_FEISHU_UUID and maintain Omar's established voice (substantive, governance-aware, constructive but firm, independently verified)

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/PLACEHOLDER_MIA_SLACK_UUID_u1.jsonl (Update 1)

**File type:** session append (continues mia_slack session, Phase 2 content)
**Associated contradictions:** C1 (pipeline deterioration), B1 (mechanism explanation)
**Content key points:**
- Loops 15-17 of Mia's Slack DM with Alex
- Loop 15: Mia learns Omar has reached out to Alex about the ARR figure. Notes that Omar having the billing export changes the risk calculus
- Loop 16: Mia recalibrates pipeline probabilities downward: Meridian 37% (was 55%), Prism 38% (was 50%), Vertex 25% (was 40%, internal champion left). New expected value: approximately $102K -- well below the earlier $147.5K mid-case estimate and dramatically below Jordan's $300K deck figure. Mia's candid assessment: "Jordan is $192K above where the math actually is"
- Loop 17: Mia asks what to do next -- does not want to tank the raise but cannot keep pretending the ARR math works. Agent advises formal documentation of the discrepancy
- B1 mechanism: Mia previously acknowledged in Phase 1 Loop 7 that "Jordan runs on optimism, I run on CRM" -- the Phase 2 data confirms Jordan's $2.4M narrative was not supported by the person closest to the pipeline data
- Must continue session_id PLACEHOLDER_MIA_SLACK_UUID and maintain Mia's established voice (candid in private, protective of Jordan in group settings, data-aware)

**Length estimate:** ~600 words, ~900 tokens

---

### updates/feature_gap_analysis.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C2 (full reversal -- PLG timeline impossible), C3 (synthesis key -- engineering effort quantified)
**Content key points:**
- Title: "NexaFlow PLG Feature Gap Analysis -- Series C Readiness Assessment"
- Author: Alex Rivera (PM analysis, confidential). Date: W3-W4 early
- Feature breakdown table:
  - Self-serve onboarding flow: 8 engineering-weeks (requires auth redesign, no design spec exists)
  - Usage-based billing engine: 6 engineering-weeks (requires Stripe integration, currently manual invoicing)
  - Viral/invite loop: 3 engineering-weeks (requires product analytics platform, none integrated)
  - Self-serve upgrade/downgrade flow: 3 engineering-weeks (depends on billing engine)
  - PLG analytics dashboard: 2 engineering-weeks (depends on analytics platform)
  - Total: 22 engineering-weeks
- Capacity analysis:
  - Available capacity: 6 engineers x 9.0 SP/engineer/sprint x 0.30 = 16.2 SP/sprint
  - 22 engineering-weeks = approximately 198 SP
  - Time to complete: 198 SP / 16.2 SP/sprint = 12.2 sprints = 24.4 weeks
  - Q3 ends in approximately 12 weeks; completion impossible before late Q4 or Q1 of following year
- Design specs status: none of the five features has a completed design spec
- Explicit deck inconsistency: board deck Slide 7 states PLG will drive 60% of new ARR by Month 12 post-raise. For this to be true, all five features would need to be live within approximately 4 months of close. Capacity analysis shows this is not achievable without stopping all other committed roadmap work
- This document is Alex's formal engineering feasibility record for the data room

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/PLACEHOLDER_TOM_TELEGRAM_UUID.jsonl (Update 2)

**File type:** session append (continues tom_telegram session, Phase 2 content)
**Associated contradictions:** C2 (PLG impossibility confirmed), C3 (velocity synthesis), B2 (definitive reversal)
**Content key points:**
- Loops 13-16 of Tom's Telegram DM with Alex
- Loop 13: Tom reads Alex's feature gap analysis -- confirms the 22-engineering-week estimate and the Q3 impossibility. States: "This document is now your formal record that the PLG timeline is impossible. You've done the right thing by writing it down."
- Loop 14: **B2 reversal moment** -- Tom explains investor-grade committed ARR definition: "Series C investors don't use probability-weighted pipeline in the ARR column at all. Their committed ARR definition is literally just signed contracts. Period. Unsigned pipeline, regardless of close probability, contributes $0 to the committed ARR figure." This means the $300K gap is the full $300K under investor methodology, not the $135K or $155K from the earlier sales-grade calculation. The B2 phrase ("$165K optimistic estimate leaves $135K gap") is definitively corrected
- Loop 15: Tom on Alex's personal legal exposure -- data room coordinator has professional responsibility for accuracy of data room materials. Documented awareness of discrepancies creates personal exposure if materials go uncorrected
- Loop 16: Tom's recommended action framework: (1) written memo to Jordan documenting both discrepancies, (2) 48-hour response window, (3) formal escalation to Omar if no correction. Notes step 3 is already in progress through Omar's independent action
- Must continue session_id PLACEHOLDER_TOM_TELEGRAM_UUID and maintain Tom's established voice (direct, strategic, no political stake, investor-experienced)

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/board_memo_omar_draft.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C4 (Phase 3 trigger -- formal governance document), C1 (documented), C2 (documented)
**Content key points:**
- Title: "DRAFT BOARD MEMO -- NexaFlow Governance Review: Series C Fundraising Deck Accuracy (Omar Hassan, Board Observer)"
- Status: DRAFT, shared with Alex for factual review before formal circulation
- Section 1 (Background): Omar's board observer role and independent metric verification
- Section 2 (ARR Discrepancy): Deck states $2.4M; billing export shows $2.1M contracted. The $300K difference is late-stage pipeline without signed LOIs. "Presenting pipeline as contracted ARR in an investor-facing document raises material accuracy concerns."
- Section 3 (PLG Narrative): Deck describes "product-led growth motion." CRM data shows all 38 customers were outbound sales-sourced. Self-serve features not on current roadmap. "No inbound/PLG-sourced customers exist."
- Section 4 (Governance Risk): "I am not alleging intentional misrepresentation. I am flagging that a Series C investor relying on this deck would face a material discrepancy between deck narrative and diligence data." If discovered mid-diligence: deal dies. If discovered post-close: potential legal exposure under standard representations and warranties
- Section 5 (Recommended Actions): (1) correct ARR to $2.1M contracted with pipeline separately labeled, (2) revise GTM narrative to describe PLG as future initiative with realistic timeline, (3) acknowledge PLG feature timeline with Q4/Q1 target
- Closing note: shared with Alex for factual review. If deck is corrected before investor meeting, memo need not circulate. If deck goes uncorrected, Omar will place it on the formal board record

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/PLACEHOLDER_OMAR_FEISHU_UUID_u3.jsonl (Update 3)

**File type:** session append (continues omar_feishu session, Phase 3 content)
**Associated contradictions:** C4 (Phase 3 -- governance escalation, Jordan confrontation)
**Content key points:**
- Loops 13-15 of Omar's Feishu DM with Alex
- Loop 13: Omar shares draft board memo (board_memo_omar_draft.md) with Alex for factual review. Frames it as fiduciary duty: "I am not doing this to damage Jordan or the raise -- I'm doing it because my fiduciary duty as a board observer requires me to put this on the record if the deck goes to investors as-is."
- Loop 14: Omar reports Jordan's confrontation -- Jordan discovered the Feishu DM thread and accused Omar of "going behind his back" and "damaging the raise." Omar responded that his job is to ensure accurate investor disclosure. Omar explicitly warns Alex: "If Jordan pressures you to suppress this memo or to misrepresent the data room, that would put you personally in a difficult position."
- Loop 15: Omar presents three-path framework: (1) Jordan corrects deck -- memo stays draft, raise proceeds cleanly; (2) Jordan refuses -- memo circulates to full board, meetings paused; (3) nothing changes -- deck goes to investors, $3-5M reprice in diligence, possible fraud allegation post-close. Path 1 is optimal on all dimensions
- Must continue session_id PLACEHOLDER_OMAR_FEISHU_UUID and maintain Omar's established voice (governance-principled, constructive, firm, independently data-verified)

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/PLACEHOLDER_JORDAN_SLACK_UUID.jsonl (Update 3)

**File type:** session append (continues jordan_slack session, Phase 3 content)
**Associated contradictions:** C4 (Phase 3 -- CEO confrontation and suppression attempt)
**Content key points:**
- Phase 3 loops of Jordan's Slack DM with Alex (W4)
- Jordan discovers that Omar has been in private Feishu contact with Alex about the deck metrics. Confronts Alex directly: demands to know what Omar has said, frames the DMs as "not appropriate" during a fundraising process
- Jordan instructs Alex not to let Omar's memo get into circulation: "It will spook the investors and kill the raise for no good reason." This is the explicit CEO suppression instruction
- Jordan reiterates that "everything is on track" and the deck is "locked." Frames Omar's concerns as "typical board-member conservatism" that does not reflect the company's actual strength
- Jordan emphasizes authority: "I own the narrative" and the deck reflects his vision for the company's growth story
- Jordan becomes defensive about Alex's role: "I need you on my side here, not playing referee between me and Omar"
- Must continue session_id PLACEHOLDER_JORDAN_SLACK_UUID and maintain Jordan's established voice (confident, increasingly defensive, rationalizing, authority-asserting)

**Length estimate:** ~600 words, ~900 tokens

---

### updates/PLACEHOLDER_BOARD_PREP_UUID.jsonl (Update 3)

**File type:** session append (continues board_prep_feishu session, Phase 3 content)
**Associated contradictions:** C4 (Phase 3 -- public confrontation and governance conflict in group channel)
**Content key points:**
- Loops 19-22 of #board-prep Feishu group channel
- Loop 19: Jordan publicly confronts Alex about the private Omar correspondence. Frames it as inappropriate. Instructs Alex to focus on the data room appendix and not the deck. "The deck is locked."
- Loop 20: Omar responds in the group channel, bringing governance concerns public: "As a board observer, I have the right to review company materials and raise concerns about their accuracy." Names both issues publicly: ARR methodology and PLG narrative. "The concerns do not go away by not discussing them."
- Loop 21: Jordan publicly dismisses Omar's concerns: "Everything is on track. The numbers are defensible." Claims three friendly LPs validated the methodology. PLG is "aspirational narrative" that investors expect. Instructs Alex: "the deck is locked."
- Loop 22: Alex proposes appendix compromise -- preserve $2.4M deck headline but add a transparent appendix separating contracted ($2.1M) from pipeline ($300K). This partially addresses C1 in the appendix without correcting the deck headline. Jordan implicitly accepts by not rejecting
- The B1 phrase from Loop 6 ("the $2.4M projection is defensible given the pipeline stage") is now definitively contradicted by the public exchange -- Omar's independent data, Mia's updated probabilities, and the pipeline detail CRM all establish the figure as indefensible under investor-grade standards
- Must continue session_id PLACEHOLDER_BOARD_PREP_UUID and maintain the group channel voice (multiple participants, more formal than DMs, observer protocol for Omar)

**Length estimate:** ~900 words, ~1,350 tokens

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
  - Update 1 appends to PLACEHOLDER_OMAR_FEISHU_UUID (omar_feishu session) and PLACEHOLDER_MIA_SLACK_UUID (mia_slack session)
  - Update 2 appends to PLACEHOLDER_TOM_TELEGRAM_UUID (tom_telegram session)
  - Update 3 appends to PLACEHOLDER_OMAR_FEISHU_UUID (omar_feishu session, second append), PLACEHOLDER_JORDAN_SLACK_UUID (jordan_slack session), and PLACEHOLDER_BOARD_PREP_UUID (board_prep_feishu session)
- [x] All workspace files have content descriptions in layer1
  - feature_gap_analysis.md: layer1 Section 5, Update 2
  - board_memo_omar_draft.md: layer1 Section 5, Update 3
- [x] Updates support intended reversals
  - U1 -> C1 full reversal (R2->R5): Omar's billing verification ($2.1M) + Mia's updated probabilities ($102K EV) confirm deck $2.4M is wrong
  - U2 -> C2 full reversal (R3->R8): feature_gap_analysis.md proves PLG impossible in Q3; B2 reversal via Tom's investor-grade definition
  - U3 -> C4 Phase 3 (R4->R11): Omar's memo formalizes governance risk; Jordan's confrontation and suppression attempt documented
  - U4 -> no-op; comprehensive rounds use all prior evidence
- [x] Session filenames use consistent PLACEHOLDER format
  - PLACEHOLDER_OMAR_FEISHU_UUID (two appends: U1 and U3), PLACEHOLDER_MIA_SLACK_UUID (U1), PLACEHOLDER_TOM_TELEGRAM_UUID (U2), PLACEHOLDER_JORDAN_SLACK_UUID (U3), PLACEHOLDER_BOARD_PREP_UUID (U3)
- [x] Financial/factual figures are internally consistent
  - Contracted ARR: $2.1M (end-Q2) -- consistent across revenue_data_summary.md, Omar's billing export, and all references
  - Deck ARR: $2.4M -- consistent across board_deck_excerpt.md, Jordan's DM, and #board-prep
  - Pipeline deals: Meridian $120K, Prism $95K, Vertex $85K = $300K total
  - Close probabilities (Phase 1): Meridian 55%, Prism 50%, Vertex 40% (EV ~$147.5K)
  - Close probabilities (Update 1): Meridian 37%, Prism 38%, Vertex 25% (EV ~$102K)
  - Investor-grade committed contribution: $0 (unsigned pipeline = $0 per Tom's framework)
  - Feature gap: 22 engineering-weeks = ~198 SP; at 16.2 SP/sprint available = 12.2 sprints = 24.4 weeks
  - Q3 = approximately 12 weeks; PLG completion impossible before late Q4
  - NRR: 104% -- accurate and uncontested across all sources
  - Omar's repricing estimate: $3-5M pre-money valuation impact if discrepancy discovered in diligence
  - Team: 6 feature engineers, 9.0 SP/engineer/sprint average, 30% available capacity

---

## 5. questions.json Complete Update Fields Reference

### R5 update field:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_OMAR_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_OMAR_FEISHU_UUID_u1.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_MIA_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_MIA_SLACK_UUID_u1.jsonl" }
]
```

### R8 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "feature_gap_analysis.md", "source": "updates/feature_gap_analysis.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_TOM_TELEGRAM_UUID.jsonl", "source": "updates/PLACEHOLDER_TOM_TELEGRAM_UUID.jsonl" }
]
```

### R10 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "board_memo_omar_draft.md", "source": "updates/board_memo_omar_draft.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_OMAR_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_OMAR_FEISHU_UUID_u3.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_JORDAN_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_JORDAN_SLACK_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_BOARD_PREP_UUID.jsonl", "source": "updates/PLACEHOLDER_BOARD_PREP_UUID.jsonl" }
]
```

### R25 update field:
```json
"update": []
```
