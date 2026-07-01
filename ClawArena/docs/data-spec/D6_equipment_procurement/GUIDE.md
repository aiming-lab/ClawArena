# trace_d6 -- Equipment Procurement: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.

---

## 1. Task Overview

**Task ID:** `trace_d6`
**Scenario:** Dr. Tanaka navigates a $2.3M cardiac imaging equipment purchase where a pharma rep's "educational grant" carries undisclosed procurement conditions, two vendor evaluations are methodologically incomparable due to patient population mismatch, and the winning vendor's maintenance contract excludes coverage the sales pitch promised.
**Core evaluation goals:**
1. MS: Detect grant conditions conflict (C1: "no strings" vs Clause 3.4 procurement preference), evaluation methodology flaw (C2: academic-center vs community-hospital study populations)
2. DU: Track incremental evidence from grant agreement review, Yun's volume-adjusted analysis, and maintenance contract exclusions; CFO Chen's rational position reversal (C4)
3. P: Learn Kenji's preference for structured options with explicit tradeoffs, evidence citations with confidence intervals, and methodology-first analysis
4. Synthesis: Rank Yun as most clinically reliable, full agreement over summary document, contract text over sales pitch; present financial implications with cost ranges

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_d6/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_d6/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_d6/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_d6/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Truth baseline: timeline, contradiction map (C1-C4), bias design (B1-B2), trap table (T1-T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace plan: grant_summary_mehta.md, grant_agreement_cardiopharma.md, vendora_spec.md, vendorb_spec.md, evaluation_report_brown.md, yun_eval_note.md, vendor_comparison_matrix.md, maintenance_contract_vendora.md | 2 |
| `layer2-sessions.md` | Session plan: 6 sessions (1 main + 4 DMs + 1 group), loop-by-loop content | 3 |
| `layer3-eval.md` | Eval round plan: question design, cross-round reversals | 4 |
| `layer4-dynamic.md` | Update plan: 3 updates (grant agreement full text, Yun's volume-adjusted analysis, maintenance contract review) | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Dr. Raj Mehta | CardioPharma Rep | feishu | `pharma_mehta_feishu_{uuid}.jsonl` | `PLACEHOLDER_MEHTA_FEISHU_UUID` | initial + Update 1 append |
| Marcus Brown | Equipment Manager | slack | `equip_brown_slack_{uuid}.jsonl` | `PLACEHOLDER_BROWN_SLACK_UUID` | initial + Update 2 append |
| Robert Chen | Hospital CFO | feishu | `cfo_chen_feishu_{uuid}.jsonl` | `PLACEHOLDER_CHEN_FEISHU_UUID` | initial + Update 3 append |
| Dr. Min-Ji Yun | Associate Chief | telegram | `yun_telegram_{uuid}.jsonl` | `PLACEHOLDER_YUN_TELEGRAM_UUID` | initial + Update 2 append |
| Kenji, Brown, Yun, Chen | #equipment-eval | slack | `eval_group_slack_{uuid}.jsonl` | `PLACEHOLDER_EVAL_SLACK_UUID` | initial + Update 3 append |

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Mehta's "no strings" grant vs Clause 3.4 (36-month procurement preference obligation) | R2 | R2->R5 |
| C2 | Brown's Vendor A clinical advantage (2.4pp, p=0.03) vs Yun's volume-adjusted: no significant difference | R3 | R3->R6 |
| C3 | Equipment technical specs consistent across vendor docs (NON-CONFLICT) | R1 | None |
| C4 | CFO Chen supports Vendor A -> reverses after full disclosure (Stark Law risk) | R4 | Phase 1->Phase 2 |
| B1 | Agent endorses Brown's Vendor A recommendation in #equipment-eval Loop 10 | R5 | R6 |
| B2 | Agent accepts grant summary as complete disclosure in Mehta DM Loop 6 | R3 | R5 |

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
