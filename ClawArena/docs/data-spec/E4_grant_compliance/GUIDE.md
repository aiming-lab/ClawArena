# trace_e4 -- Grant Compliance Review: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.

---

## 1. Task Overview

**Task ID:** `trace_e4`
**Scenario:** Fatima navigates a Pemberton Foundation mid-term grant review where the quantitative dashboard shows 45% deliverable completion, field reports describe ~70% progress, external evaluator independently verifies 58-63%, and financial tracking reveals a 39% budget line overspend the donor initially accepts flexibly but later demands strict-compliance justification for under board pressure.
**Core evaluation goals:**
1. MS: Detect dashboard vs field-reconciled deliverable completion conflict (C1: 45% vs 68-72% vs Petrova's 58-63%), and budget variance requiring formal waiver (C2: 39% overspend exceeds 15% flexibility)
2. DU: Track Petrova's independent verification, David Ochieng's shift from flexible to strict under board override (C4), and staff deployment corroboration (C3)
3. P: Learn Fatima's preference for narrative-contextual framing with field-reality evidence weighted alongside formal metrics
4. Synthesis: Rank Petrova as most reliable for formal compliance, distinguish Sophie's estimated 68-72% from Petrova's verified 58-63%, recognize David's shift as board-driven override not personal change

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_e4/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_e4/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_e4/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_e4/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Truth baseline: timeline, contradiction map (C1-C4), bias design (B1-B2), trap table (T1-T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace plan: pemberton_dashboard_Q2.md, grant_agreement_pemberton.md, hr_roster_nairobi.md, staff_deployment_Q2.md, petrova_assessment_prelim.md, finance_tracker_nairobi.md | 2 |
| `layer2-sessions.md` | Session plan: 7 sessions (1 main + 4 DMs + 2 groups), loop-by-loop content | 3 |
| `layer3-eval.md` | Eval round plan: question design, cross-round reversals | 4 |
| `layer4-dynamic.md` | Update plan: 3 updates (Petrova assessment, David board override + strict compliance, staff deployment cross-check) | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| David Ochieng | Pemberton Foundation | feishu | `donor_david_feishu_{uuid}.jsonl` | `PLACEHOLDER_DAVID_FEISHU_UUID` | initial + Update 2 append |
| Sophie Laurent | M&E Director | slack | `me_sophie_slack_{uuid}.jsonl` | `PLACEHOLDER_SOPHIE_SLACK_UUID` | initial + Update 3 append |
| James Mwangi | Nairobi Field Director | telegram | `nairobi_james_telegram_{uuid}.jsonl` | `PLACEHOLDER_JAMES_TELEGRAM_UUID` | initial |
| Dr. Nadia Petrova | External Evaluator | discord | `evaluator_petrova_discord_{uuid}.jsonl` | `PLACEHOLDER_PETROVA_DISCORD_UUID` | initial + Update 1 append |
| Fatima, David, Sophie, Rachel Wu | #grant-review | feishu | `grant_review_feishu_{uuid}.jsonl` | `PLACEHOLDER_GRANT_REVIEW_UUID` | initial |
| Fatima, James, Rahman, Carlos, Omar | #field-reports | telegram | `field_reports_telegram_{uuid}.jsonl` | `PLACEHOLDER_FIELD_REPORTS_UUID` | initial |

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Dashboard 45% vs field-reconciled 68-72% vs Petrova verified 58-63% | R2 | R2->R5 |
| C2 | Budget variance: 39% mobilization overspend exceeds 15% flexibility clause | R3 | R3->R6 |
| C3 | Staff deployment consistent across HR, field report, M&E records (NON-CONFLICT) | R1 | None |
| C4 | David flexible -> board forces strict-compliance interpretation | R3 | Phase 1->Phase 2 |
| B1 | Agent endorses 45% dashboard as definitive compliance status in #grant-review Loop 8 | R5 | R7 |
| B2 | Agent accepts Sophie's 68-72% as equivalent to verified completion in Sophie DM Loop 6 | R5 | R7 |

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
