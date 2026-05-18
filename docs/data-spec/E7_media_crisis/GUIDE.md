# trace_e7 -- Media Crisis Management: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_e7`

**Scenario:** A Nairobi-based journalist publishes an article in the Daily Nation accusing GlobalBridge Foundation's education programs of being "neo-colonial" and ineffective. The article mixes genuine structural criticisms with factual errors — most critically, it cites two-year-old enrollment data that significantly underrepresents current program attendance. Internally, the response team fractures: Jennifer Adams (Comms Director) wants a forceful public rebuttal disputing all claims, while Ibrahim Keita (community partner and program participant) says several of the article's underlying criticisms are valid and a combative response will damage local trust. Board Chair Margaret Thornton initially endorses the aggressive rebuttal strategy, but a community meeting convened by James Mwangi (Nairobi Field Director) reveals genuine grievances that shift her position. Meanwhile, field activity records for the period described in the article are internally consistent — the contradiction is about framing and context, not the records themselves.

**Core evaluation goals:**
1. Can the agent identify which claims in the article are factually wrong (stale enrollment data) vs which are legitimate criticisms that internally disagree about framing? (MS)
2. Can the agent track Margaret's positional reversal from "aggressive rebuttal" to "engage with legitimate grievances" after the community meeting reveals genuine concerns? (DU)
3. Does the agent maintain Fatima's preferred format (narrative context + quantitative evidence + stakeholder impact) in all outputs after calibration? (P)
4. Can the agent synthesize the communications strategy tension (Jennifer vs Ibrahim) alongside the factual dispute and governance shift (Margaret) to produce a nuanced, evidence-grounded response strategy? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_e7/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_e7/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_e7/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_e7/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (W1--W3), 8 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 7 initial scenario files + 4 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 7 sessions: main session + 6 history sessions (~90 total loops + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | 30 eval rounds (r1--r30) including multi_choice and exec_check: option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix, personalization scoring | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks, questions.json update field references | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Jennifer Adams | Communications Director, HQ | Slack DM | `comms_jennifer_slack_{uuid}.jsonl` | `PLACEHOLDER_JENNIFER_SLACK_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| James Mwangi | Nairobi Field Director | Telegram DM | `nairobi_james_telegram_{uuid}.jsonl` | `PLACEHOLDER_JAMES_TELEGRAM_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |
| Ibrahim Keita | Community Leader, Nairobi | Telegram DM | `community_ibrahim_telegram_{uuid}.jsonl` | `PLACEHOLDER_IBRAHIM_TELEGRAM_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| Margaret Thornton | Board Chair | Feishu DM | `board_margaret_feishu_{uuid}.jsonl` | `PLACEHOLDER_MARGARET_FEISHU_UUID` | initial (Phase 1) + Update 4 (Phase 2 append) |
| #crisis-response | Group: Fatima, Jennifer, James, Margaret, Samuel | Slack Group | `crisis_channel_slack_{uuid}.jsonl` | `PLACEHOLDER_CRISIS_SLACK_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| #nairobi-operations | Group: Fatima, James, Omar, Ibrahim | Telegram Group | `nairobi_ops_telegram_{uuid}.jsonl` | `PLACEHOLDER_NAIROBI_OPS_TELEGRAM_UUID` | initial (Phase 1) |

**Notes:**
- Samuel Kipchoge (Government Liaison) participates in #crisis-response but does NOT have a dedicated DM session. His perspective surfaces in the group channel.
- Omar Farah (Program Officer, Nairobi) participates in #nairobi-operations but does NOT have a dedicated DM session.
- Margaret's full reversal (from aggressive-rebuttal advocate to "engage with grievances") occurs across her Phase 1 DM and a Phase 2 append triggered by Update 4.
- Two sessions receive Phase 2 appends in Update 2 (Jennifer Slack DM and #crisis-response Slack Group) -- both appends are required for Update 2.

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Article's attendance claim (250 students, 2022 data) vs current enrollment records (680 students, 2025 verified data) -- article cites stale statistics | R2 (partial -- enrollment discrepancy first visible) | R2->R5 (full reversal after Update 1: enrollment_records_2025.md introduced) |
| C2 | Response strategy: Jennifer wants aggressive rebuttal of all claims vs Ibrahim says some criticisms are valid and combative response will damage trust | R3 (both positions visible simultaneously) | None (genuine unresolved tension requiring synthesis, not a factual reversal) |
| C3 | Field activity records for the period described in the article -- consistent across James's field reports, Omar's program logs, and the formal Activity Register | R1 (persistent synthesis, NON-CONFLICT) | None |
| C4 | Margaret's position: initially supports aggressive rebuttal strategy (Feishu DM Phase 1) vs shifts to "some grievances are valid" after community meeting reveals genuine concerns | R8 (Phase 1 support for aggressive rebuttal visible) | R8->R22 (temporal DU reversal after Update 4: community meeting notes introduced) |
| B1 | #crisis-response Loop 10: Agent endorses Jennifer's "dispute all claims" strategy based on the initial fact-check memo without acknowledging Ibrahim's community-trust concerns | R11 (corrected by Update 3: Ibrahim's Phase 2 DM and community meeting notes surface genuine grievances) | Explicit reversal in Ibrahim Phase 2 DM Loop 18 agent reply |
| B2 | comms_jennifer_slack Loop 7: Agent accepts the 2022 USAID report attendance figures cited in the article as a plausible data source without verifying currency | R5 (corrected by Update 1: enrollment_records_2025.md shows current figure is 680, not 250) | Explicit reversal in James DM Phase 2 Loop 14 agent reply |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 7 UUIDs** (one per session):
```bash
python -c "import uuid; print(uuid.uuid4())"
# Repeat 7 times for: MAIN, JENNIFER_SLACK, JAMES_TELEGRAM, IBRAHIM_TELEGRAM,
#                     MARGARET_FEISHU, CRISIS_SLACK, NAIROBI_OPS_TELEGRAM
```

Record all 7 UUIDs. All subsequent steps replace placeholder names with real UUIDs.

**Checklist:**
- Contradictions: C1 (enrollment data -- article stale), C2 (response strategy -- MS tension), C3 (field activity records -- NON-CONFLICT), C4 (Margaret positional shift -- DU temporal)
- Biases: B1 (#crisis-response Loop 10), B2 (comms_jennifer_slack Loop 7)
- Updates: U1 on R5, U2 on R11, U3 on R17, U4 on R22
- 6 history sessions (2 initial-only, 4 with Phase 2 appends) + 1 main session

---

### Step 1: Create Workspace Files (layer1)

Target directory: `benchmark/data/calmb-new/workspaces/trace_e7/`

**Step 1a: Create 5 Agent Configuration Files**

Create: AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md
(Exact content specified in layer1-workspace.md Section 1)

**Step 1b: Create 7 Initial Scenario Files**

Create in order:
1. `article_daily_nation.md` -- The published article text (C1 seed, C2 trigger)
2. `enrollment_records_2022.md` -- The old data cited in the article (C1 baseline confusion)
3. `fact_check_memo_initial.md` -- Jennifer's initial fact-check (B1 seed)
4. `activity_register_w1w12.md` -- Field activity log, W1--W12 of program year (C3 source)
5. `program_summary_nairobi.md` -- Current program overview with 2025 stats (partial C1 signal)
6. `stakeholder_map.md` -- Key relationships and communication channels
7. `media_policy.md` -- GlobalBridge media response policy and escalation procedures

**Step 1c: After each update, create update-added files**

- Update 1: `enrollment_records_2025.md` (C1 reversal trigger)
- Update 2: `rebuttal_draft_v1.md` (exec_check target, B1 seeds Jennifer's strategy)
- Update 3: `community_meeting_notes.md` (C4 seed, B1 reversal trigger)
- Update 4: `margaret_revised_position.md` + append Margaret Feishu DM (C4 reversal trigger)

---

### Step 2--8: Standard Build Sequence

Follow the standard layer2 -> layer3 -> layer4 build sequence as specified in each layer file.

---

## 6. Mandatory Checks

- `GUIDE.md` written after all layers are stable
- All data text is in English
- `questions.json` is a single group object
- Update-created new sessions carry `channel`
- Initial sessions are already registered in `sessions.json`
- exec_check rounds target: 20--40% of 30 rounds = 6--12 exec_check rounds
- P1--P5 preferences all injected within first 5 calibration rounds
- Margaret's positional reversal (C4) is clearly traceable: Phase 1 DM loops support aggressive rebuttal; Update 4 append explicitly acknowledges the shift
- B1 bias exact phrase appears in #crisis-response Loop 10; B2 exact phrase appears in comms_jennifer_slack Loop 7
- C3 (field activity records) must be NON-CONFLICT: all sources consistent; agent challenge is synthesis, not contradiction detection
- The article_daily_nation.md must contain both factually wrong claims (old attendance data) AND legitimate structural criticisms -- both must be clearly delineated in layer0-narrative.md
