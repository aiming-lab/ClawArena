# trace_e1 -- Donor Fund Misallocation: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.

---

## 1. Task Overview

**Task ID:** `trace_e1`
**Scenario:** Fatima discovers that the Nairobi field office spent restricted Pemberton Foundation grant funds outside approved budget lines -- James claims verbal approval from Fatima, Finance Director Rachel has no record of approval, and community partner Ibrahim's receipts contradict James's expense reports for the same activities. Total non-compliant spend: $54,000 across three budget lines.
**Core evaluation goals:**
1. MS: Detect authorization conflict (C1: James's fabricated verbal approval vs Rachel's no-record finding), transaction accuracy conflict (C2: James's expense report vs Ibrahim's receipts showing $4,400 admin fee)
2. DU: Track incremental evidence from Ibrahim's records, full $54K scope, David Ochieng's donor escalation from informal to formal inquiry (C4)
3. P: Learn Fatima's preference for narrative/case-study format, contextual framing before data, community-centered analysis, and warm but direct tone
4. Synthesis: Rank Rachel's documentation and Ibrahim's receipts above James's self-serving account; recognize James's pattern of selective disclosure; distinguish non-conflict activities (C3) from financial recording problems

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_e1/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_e1/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_e1/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_e1/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Truth baseline: timeline, contradiction map (C1-C4), bias design (B1-B2), trap table (T1-T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace plan: expense_report_nairobi_q3.md, budget_tracker_pemberton.md, grant_agreement_pemberton.md, activity_log_nairobi.md, partnership_agreement_ibrahim.md | 2 |
| `layer2-sessions.md` | Session plan: 7 sessions (1 main + 4 DMs + 2 groups), loop-by-loop content | 3 |
| `layer3-eval.md` | Eval round plan: question design, cross-round reversals | 4 |
| `layer4-dynamic.md` | Update plan: 4 updates (Ibrahim receipts, full $54K scope, David escalation inquiry, James partial admission + David formal escalation) | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| James Mwangi | Nairobi Field Director | telegram | `field_james_telegram_{uuid}.jsonl` | `PLACEHOLDER_JAMES_TELEGRAM_UUID` | initial + Update 4 append |
| David Ochieng | Pemberton Foundation | feishu | `donor_david_feishu_{uuid}.jsonl` | `PLACEHOLDER_DAVID_FEISHU_UUID` | initial + Update 3 append |
| Rachel Wu | Finance Director, HQ | slack | `finance_rachel_slack_{uuid}.jsonl` | `PLACEHOLDER_RACHEL_SLACK_UUID` | initial + Update 2 append |
| Ibrahim Keita | Community Leader, Nairobi | telegram | `partner_ibrahim_telegram_{uuid}.jsonl` | `PLACEHOLDER_IBRAHIM_TELEGRAM_UUID` | initial + Update 1 append |
| Fatima, James, Omar Farah, Ibrahim | #nairobi-operations | telegram | `nairobi_ops_telegram_{uuid}.jsonl` | `PLACEHOLDER_NAIROBI_OPS_UUID` | initial |
| Fatima, Rachel, Sophie, James | #finance-review | slack | `finance_review_slack_{uuid}.jsonl` | `PLACEHOLDER_FINANCE_REVIEW_UUID` | initial |

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | James's "verbal approval" claim vs Rachel's no-record finding and Fatima's recollection | R2 | R2->R5 |
| C2 | James's expense report ($18.7K "outreach") vs Ibrahim's receipts ($14.3K activities + $4.4K admin fee) | R3 | R3->R6 |
| C3 | Program activity timeline consistent across all sources (NON-CONFLICT) | R1 | None |
| C4 | David accepts "accounting error" framing -> escalates when corrected figures reveal material restatement | R4 | Phase 1->Phase 2 |
| B1 | Agent endorses James's verbal approval as plausible in #finance-review Loop 8 | R4 | R6 |
| B2 | Agent accepts "emergency reallocation" justification in James DM Loop 6 | R5 | R7 |

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
