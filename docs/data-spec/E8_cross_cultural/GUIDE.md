# trace_e8 -- Cross-Cultural Curriculum Adaptation: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.

---

## 1. Task Overview

**Task ID:** `trace_e8`
**Scenario:** Fatima must determine whether Carlos's unauthorized curriculum adaptation in Bogota is a program fidelity violation or a necessary local adjustment. HQ insists on standardization while community data reveals cultural misalignment, a successful parallel adaptation in Dhaka (HQ-approved) complicates the policy, and student performance data shows no outcome difference between adapted and standard implementations.
**Core evaluation goals:**
1. MS: Detect fidelity vs adaptation conflict (C1: Sophie's evidence-base defense vs Carlos's 35pp engagement improvement), process conflict (C2: Rahman's approved Dhaka adaptation vs Carlos's unauthorized Bogota adaptation)
2. DU: Track Sophie's evidence-driven position shift after community focus group data (C4), and Prof. Dubois's comparative assessment confirming equivalent outcomes (C3)
3. P: Learn Fatima's preference for narrative framing with case-specific illustrations, qualitative richness, and concrete policy recommendations
4. Synthesis: Distinguish content adaptation (justified) from process deviation (governance concern); recognize Sophie's update as evidence-driven; identify Carlos's incorrect assumption about approval feasibility; present dual resolution path

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_e8/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_e8/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_e8/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_e8/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Truth baseline: timeline, contradiction map (C1-C4), bias design (B1-B2), trap table (T1-T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace plan: curriculum_compliance_report.md, curriculum_excerpt_standard.md, bogota_engagement_data.md, bogota_focus_group_report.md, dhaka_adaptation_approval.md, prof_dubois_comparison.md, field_adaptation_policy_draft.md | 2 |
| `layer2-sessions.md` | Session plan: 7 sessions (1 main + 4 DMs + 2 groups), loop-by-loop content | 3 |
| `layer3-eval.md` | Eval round plan: question design, cross-round reversals | 4 |
| `layer4-dynamic.md` | Update plan: 4 updates (Rahman Dhaka precedent, community focus group report + Sophie shift, Dubois comparison data, Rachel grant compliance flag) | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Carlos Mendez | Bogota Field Director | discord | `carlos_fatima_discord_{uuid}.jsonl` | `PLACEHOLDER_CARLOS_DISCORD_UUID` | initial + Update 2 append |
| Dr. Aisha Rahman | Dhaka Field Director | telegram | `rahman_fatima_telegram_{uuid}.jsonl` | `PLACEHOLDER_RAHMAN_TELEGRAM_UUID` | initial + Update 1 append |
| Sophie Laurent | M&E Director | slack | `sophie_fatima_slack_{uuid}.jsonl` | `PLACEHOLDER_SOPHIE_SLACK_UUID` | initial + Update 2 append |
| Prof. Jean-Claude Dubois | Academic Advisor | discord | `dubois_fatima_discord_{uuid}.jsonl` | `PLACEHOLDER_DUBOIS_DISCORD_UUID` | initial + Update 3 append |
| Fatima, Sophie, Carlos, Rahman, Maria | #curriculum-review | slack | `curriculum_review_slack_{uuid}.jsonl` | `PLACEHOLDER_CURRICULUM_SLACK_UUID` | initial + Update 1 + Update 2 appends |
| Fatima, Carlos, Maria, community | #bogota-ops | discord | `bogota_ops_discord_{uuid}.jsonl` | `PLACEHOLDER_BOGOTA_OPS_UUID` | initial + Update 2 append |

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Sophie's fidelity requirement vs Carlos's 54%->89% attendance improvement | R2 | R2->R7 (partial), R2->R10 (full) |
| C2 | Rahman's HQ-approved Dhaka adaptation vs Carlos's unauthorized Bogota process | R3 | R3->R6 |
| C3 | Student assessment scores equivalent across adapted/standard (NON-CONFLICT) | R1 | None |
| C4 | Sophie's W3 fidelity defense -> W4 partial position shift after focus group data | R4 | R4->R7 |
| B1 | Agent endorses "fidelity first" in #curriculum-review Loop 9 | R5 | R7 |
| B2 | Agent overweights 35pp engagement metric as primary evidence in Carlos DM Loop 6 | R4 | R9 |

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
