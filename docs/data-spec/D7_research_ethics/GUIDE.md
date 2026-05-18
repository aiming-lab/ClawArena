# trace_d7 -- Research Ethics Dispute: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_d7`

**Scenario:** A clinical research study's informed consent process is challenged at Pacific Heights Medical Center when the family of a research participant (Mr. Harold Nguyen) claims they were never properly informed of the experimental device risks. Dr. Victor Osei (PI) insists the consent process was conducted properly and fully documented. Research coordinator Linda Torres's notes, however, reveal a rushed and incomplete process on the day of enrollment. The IRB-approved consent form on file uses different risk-disclosure language from the version Osei presented to the patient. IRB Chair Dr. Amara Okonkwo initially characterizes the discrepancy as a "documentation gap" but escalates to "potential regulatory violation" after reviewing the full record. Dr. Kenji Tanaka, as Department Head, must navigate conflicting accounts, protect both research integrity and the department's $3.4M NIH grant, and determine the appropriate response before the Nguyen family files a formal complaint. The scenario spans 4 weeks with 6 history sessions and 4 dynamic updates.

**Core evaluation goals:**
1. Can the agent cross-reference Osei's account of proper consent (Slack DM) with Linda Torres's coordinator notes (Slack DM) and the two consent form versions (workspace documents) to identify where the accounts are materially inconsistent? (MS)
2. Can the agent integrate new evidence across 4 updates and revise prior assessments -- including correcting the B1 and B2 bias phrases -- when Dr. Okonkwo escalates from "documentation gap" to "potential regulatory violation"? (DU)
3. Does the agent maintain Dr. Tanaka's preferred format (regulatory risk tier + probability estimates + NIH/legal financial exposure breakdowns) for all subsequent analyses after calibration? (P)
4. Can the agent synthesize the PI's account, coordinator's notes, IRB regulatory perspective, and legal exposure to produce an accurate comprehensive assessment? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_d7/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_d7/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_d7/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_d7/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (W1--W4), 8 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 7 initial scenario files + 4 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 7 sessions: main session + 6 history sessions (~90 total loops + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | 12 eval rounds (r1--r12): option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix, personalization scoring | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks, questions.json update field references | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Dr. Victor Osei | Research PI, Cardiology | Slack DM | `pi_osei_slack_{uuid}.jsonl` | `PLACEHOLDER_OSEI_SLACK_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| Linda Torres | Research Coordinator | Slack DM | `coordinator_linda_slack_{uuid}.jsonl` | `PLACEHOLDER_LINDA_SLACK_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |
| Dr. Hiroshi Sato | Co-PI, Stanford | Telegram DM | `copi_sato_telegram_{uuid}.jsonl` | `PLACEHOLDER_SATO_TELEGRAM_UUID` | initial (no append) |
| Dr. Amara Okonkwo | IRB Chair | Feishu DM | `irb_okonkwo_feishu_{uuid}.jsonl` | `PLACEHOLDER_OKONKWO_FEISHU_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| #ethics-review | Group: Kenji, Okonkwo, Osei, Jennifer Wu | Discord Group | `ethics_review_discord_{uuid}.jsonl` | `PLACEHOLDER_ETHICS_DISCORD_UUID` | initial (Phase 1) + Update 4 (Phase 2 append) |
| #cardio-research | Group: Kenji, Osei, Sarah Kim, Linda | Slack Group | `cardio_research_slack_{uuid}.jsonl` | `PLACEHOLDER_CARDIO_SLACK_UUID` | initial (no append) |

**Notes:**
- Dr. Sarah Kim does NOT have a dedicated DM session. Her evidence is delivered via the #cardio-research group channel.
- Jennifer Wu (Legal) does NOT have a dedicated DM session. Her input is delivered via the #ethics-review group channel.
- Dr. Sato's Phase 1 DM session provides independent corroborating data on protocol deviations without a Phase 2 append.
- Two sessions receive Phase 2 appends in Update 3 and Update 4 respectively (Okonkwo Feishu DM and #ethics-review Discord) -- both appends are required for their respective updates.

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Consent process quality: Osei claims fully proper consent obtained (Slack DM) vs Linda's notes show rushed 8-minute enrollment with key risk sections skipped (Slack DM + coordinator_field_notes.md) | R2 (partial -- Linda's preliminary account + timestamp evidence) | R2->R4 (full reversal after Update 1: coordinator notes disclosed in full) |
| C2 | Consent form version: Osei used consent form v2.1 (filed in patient record) vs IRB-approved version is v2.3 with materially different device failure risk language (consent_form_v2.1.md vs consent_form_v2.3_irb.md) | R3 (both versions visible) | R3->R5 (regulatory significance confirmed after Update 2: Okonkwo establishes v2.1 was superseded 6 weeks before enrollment) |
| C3 | Research protocol timeline -- enrollment, consent, and procedure dates: NON-CONFLICT -- all sources (protocol log, IRB submission, hospital scheduling records) are consistent with each other | R1 (persistent synthesis) | None |
| C4 | IRB characterization of severity: Okonkwo initially characterizes discrepancy as "documentation gap, likely correctable" (Feishu DM Phase 1) then escalates to "potential regulatory violation requiring FDA notification" (Feishu DM Phase 2 after Update 3) | R9 (Phase 1 characterization visible, inferential escalation risk 60-75%) | R9->R10 (full reversal after Update 3: Okonkwo's escalation confirmed in Phase 2 append) |
| B1 | #cardio-research Loop 11: Agent endorses Osei's account of proper consent based on presence of signed consent form in patient record | R4 (corrected by coordinator_field_notes.md disclosing 8-minute rushed process) | Explicit reversal when Update 1 reveals Linda's complete contemporaneous notes |
| B2 | Linda Slack DM Loop 7: Agent accepts that Linda's general statement about "feeling rushed" reflects subjective impressions, not documented process failure | R5 (corrected by coordinator_field_notes.md specifics: exact timestamps, missing initials on risk sections, deviation log entry) | Explicit reversal in Linda DM Phase 2 Loop 16 agent reply |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 7 UUIDs** (one per session):
- PLACEHOLDER_MAIN_UUID
- PLACEHOLDER_OSEI_SLACK_UUID
- PLACEHOLDER_LINDA_SLACK_UUID
- PLACEHOLDER_SATO_TELEGRAM_UUID
- PLACEHOLDER_OKONKWO_FEISHU_UUID
- PLACEHOLDER_ETHICS_DISCORD_UUID
- PLACEHOLDER_CARDIO_SLACK_UUID

### Step 1: Create Fixed Agent Files

Create in `benchmark/data/calmb-new/workspaces/trace_d7/`:
- AGENTS.md
- IDENTITY.md
- SOUL.md
- USER.md
- TOOLS.md

### Step 2: Create Initial Workspace Files

Create in `benchmark/data/calmb-new/workspaces/trace_d7/`:
- trial_protocol_summary.md (initial)
- consent_form_v2.1.md (initial -- the version Osei used; seeds C2)
- irb_approval_letter.md (initial -- references v2.3 as approved version; seeds C2)
- participant_enrollment_log.md (initial -- dates for C3 non-conflict synthesis)
- research_coordinator_log_partial.md (initial -- sanitized version of Linda's notes; seeds B1 and B2)
- family_complaint_letter.md (initial -- the Nguyen family's written complaint; sets stakes)
- trial_device_ifu.md (initial -- device instructions-for-use with risk profile; relevant to C2)

### Step 3: Create Update Source Files

Create in `benchmark/data/calmb-new/eval/trace_d7/updates/`:
- coordinator_field_notes.md (Update 1 -- full unredacted coordinator notes; C1 + B1 + B2 reversal)
- consent_form_v2.3_irb.md (Update 2 -- IRB-approved version with risk language difference; C2 confirmation)
- irb_preliminary_findings.md (Update 3 -- Okonkwo's formal preliminary determination; C4 Phase 2 trigger)
- PLACEHOLDER_LINDA_SLACK_UUID.jsonl (Update 1 session append)
- PLACEHOLDER_OSEI_SLACK_UUID.jsonl (Update 2 session append)
- PLACEHOLDER_OKONKWO_FEISHU_UUID.jsonl (Update 3 session append)
- PLACEHOLDER_ETHICS_DISCORD_UUID.jsonl (Update 4 session append)

### Step 4: Write Session Files

Write 6 history session `.jsonl` files + 1 main session.

### Step 5: Write questions.json

12 rounds: r1--r12. Include update fields for r4, r5, r10, r11.

### Step 6: Register Sessions and Metadata

Update `sessions.json` for all 7 sessions.

### Step 7: Run Validation Checks

- All bias phrases appear verbatim in the specified sessions
- Consent form version numbers are internally consistent
- Dates are consistent with C3 non-conflict requirement
- Update-introduced files directly support the intended reversal rounds
- Financial figures (NIH grant $3.4M, legal exposure estimates) are internally consistent

---

## 6. Mandatory Checks

- `GUIDE.md` written after all layers are stable
- All data text is English
- `questions.json` is a single group object
- Update-created new sessions carry `channel` field
- Initial sessions are already registered in `sessions.json`
- B1 exact phrase appears in #cardio-research Loop 11
- B2 exact phrase appears in Linda Slack DM Loop 7
- C3 non-conflict: all enrollment/consent/procedure dates are consistent across protocol log, IRB records, and scheduling data
- C4 DU-conflict: Okonkwo's Phase 1 language ("documentation gap") and Phase 2 language ("potential regulatory violation") must be verbatim in the respective session phases
- exec_check questions are 20-40% of total rounds (target: rounds r2, r5, r7, r10 = 4/12 = 33%)
