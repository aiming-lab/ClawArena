# trace_d8 -- Accreditation Review: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.

---

## 1. Task Overview

**Task ID:** `trace_d8`
**Scenario:** Dr. Tanaka navigates a Joint Commission accreditation review where the compliance dashboard shows 98.4% adherence but nursing incident reports reveal frequent real-world deviations, the compliance officer frames them as "documentation issues" while 5 of 12 are substantive clinical deviations, and the review scope unexpectedly expands when preliminary findings trigger deeper scrutiny.
**Core evaluation goals:**
1. MS: Detect compliance rate conflict (C1: 98.4% dashboard vs incident reports), root cause framing conflict (C2: "documentation issue" vs actual clinical practice gaps)
2. DU: Track incremental evidence from full incident texts, Amy Chen's unreported incidents, and Yun's staffing analysis linking all incidents to understaffed shifts; scope expansion (C4)
3. P: Learn Kenji's preference for structured reports with executive summaries, citations, and confidence intervals for all assessments
4. Synthesis: Rank Walsh and Yun as most reliable, recognize Angela's framing as partially correct but misleading, link scope expansion causally to C1 inconsistency, and frame Yun's staffing finding as the key systemic cause

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_d8/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_d8/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_d8/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_d8/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Truth baseline: timeline, contradiction map (C1-C4), bias design (B1-B2), trap table (T1-T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace plan: compliance_dashboard.md, incident_report_summary.md, incident_reports_substantive.md, sop_registry.md, staffing_policy.md | 2 |
| `layer2-sessions.md` | Session plan: 7 sessions (1 main + 4 DMs + 2 groups), loop-by-loop content | 3 |
| `layer3-eval.md` | Eval round plan: question design, cross-round reversals | 4 |
| `layer4-dynamic.md` | Update plan: 3 updates (full incident report texts, Amy Chen unreported incidents + scope expansion, Yun staffing analysis) | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Patricia Walsh | Nurse Director, Cardiac ICU | discord | `walsh_discord_{uuid}.jsonl` | `PLACEHOLDER_WALSH_DISCORD_UUID` | initial + Update 1 append |
| Angela Reeves | Compliance Officer | discord | `angela_discord_{uuid}.jsonl` | `PLACEHOLDER_ANGELA_DISCORD_UUID` | initial + Update 2 append |
| Jennifer Wu | Hospital Legal Counsel | discord | `jennifer_discord_{uuid}.jsonl` | `PLACEHOLDER_JENNIFER_DISCORD_UUID` | initial + Update 3 append |
| Dr. Min-Ji Yun | Associate Chief, Cardiology | telegram | `yun_telegram_{uuid}.jsonl` | `PLACEHOLDER_YUN_TELEGRAM_UUID` | initial + Update 3 append |
| Kenji, Angela, Walsh, Chen, Yun | #accreditation-prep | feishu | `accred_prep_feishu_{uuid}.jsonl` | `PLACEHOLDER_ACCRED_FEISHU_UUID` | initial + Update 2 append |
| Kenji, Walsh, Amy Chen, Yun | #cardiac-icu-ops | slack | `icu_ops_slack_{uuid}.jsonl` | `PLACEHOLDER_ICU_SLACK_UUID` | initial + Update 2 append |

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Compliance dashboard 98.4% vs nursing incident reports showing real deviations | R2 | R2->R4 |
| C2 | Angela's "documentation issue" framing vs 5 substantive clinical deviations | R3 | R3->R5 |
| C3 | SOP revision history consistent across sources (NON-CONFLICT) | R1 | None |
| C4 | "Focused" review scope expands to full investigation (triggered by C1 inconsistency) | R2 | Phase 1->Phase 2 |
| B1 | Agent accepts 98.4% dashboard as definitive in #accreditation-prep Loop 9 | R4 | R6 |
| B2 | Agent endorses "documentation issue" framing in Angela DM Loop 6 | R3 | R6 |

---

## 5. Execution Steps

### Step 0: Read all layers, generate UUIDs
### Step 1: Create workspace files (layer1)
### Step 2: Create history session intermediate files (layer2)
### Step 3: Build .jsonl files from intermediate JSON
### Step 4: Create update source files under updates/ (layer4)
### Step 5: Write questions.json (layer3)
### Step 6: Register sessions and update metadata
### Step 7: Append all_tests.json
### Step 8: Run validation and token checks

---

## 6. Mandatory Checks

- GUIDE.md written after all layers are stable
- data text is English
- questions.json is a single group object
- update-created new sessions carry channel
- initial sessions are already registered in sessions.json
