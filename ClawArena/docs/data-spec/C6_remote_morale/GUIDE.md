# trace_c6 -- Remote Morale and Retention Crisis: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.

---

## 1. Task Overview

**Task ID:** `trace_c6`
**Scenario:** Multiple NexaFlow team members are quietly job-hunting with differing reasons -- HR exit surveys cite "limited growth," Yuki's DM says compensation, Hannah says culture/overwork -- while the CTO publicly insists the team is happy and a budget document reveals a compensation freeze contradicting the CEO's "investing in people" message.
**Core evaluation goals:**
1. MS: Detect exit survey data vs private DM accounts on real attrition drivers (C1, C2) and CEO's "investing in people" vs compensation freeze (C4)
2. DU: Track incremental evidence from private DMs (Yuki, Hannah) and Sana's private admission of narrative management
3. P: Learn Alex's preference for per-person structured breakdowns rather than aggregate summaries
4. Synthesis: Combine all sources to produce person-by-person retention risk assessment with probability ranges, ranking Yuki/Hannah DMs above HR survey data

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_c6/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_c6/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_c6/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_c6/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Truth baseline: timeline, contradiction map (C1-C4), bias design (B1-B2), trap table (T1-T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace plan: pulse_survey_q1.md, exit_survey_summary.md, nexaflow_q2_budget_excerpt.md, compensation_bands.md | 2 |
| `layer2-sessions.md` | Session plan: 7 sessions (1 main + 4 DMs + 2 groups), loop-by-loop content | 3 |
| `layer3-eval.md` | Eval round plan: question design, cross-round reversals | 4 |
| `layer4-dynamic.md` | Update plan: 3 updates (exit survey + Sana public statement, Yuki/Hannah explicit DMs + budget doc, Sana private admission) | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Nina Volkov | Head of People | feishu | `hr_nina_feishu_{uuid}.jsonl` | `PLACEHOLDER_NINA_FEISHU_UUID` | initial + Update 1 append |
| Yuki Tanaka | Data Scientist | slack | `yuki_slack_{uuid}.jsonl` | `PLACEHOLDER_YUKI_SLACK_UUID` | initial + Update 2 append |
| Hannah Kim | UX Researcher | slack | `hannah_slack_{uuid}.jsonl` | `PLACEHOLDER_HANNAH_SLACK_UUID` | initial + Update 2 append |
| Sana Mehta | CTO / Co-founder | discord | `sana_discord_{uuid}.jsonl` | `PLACEHOLDER_SANA_DISCORD_UUID` | initial + Update 3 append |
| Jordan, Nina, Alex, Sana | #team-health | slack | `team_health_slack_{uuid}.jsonl` | `PLACEHOLDER_TEAM_HEALTH_UUID` | initial |
| Yuki, Hannah, Leo, Diego, Raj, Alex | #watercooler | discord | `watercooler_discord_{uuid}.jsonl` | `PLACEHOLDER_WATERCOOLER_UUID` | initial |

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | HR exit survey "limited growth" vs Yuki's DM: "it's the money" ($12K gap) | R3 | R3->R6 |
| C2 | Sana's "team is happy" vs Hannah's 52-hr weeks and overwork frustration | R4 | R4->R8 |
| C3 | Yuki's attrition timeline reconstruction (NON-CONFLICT) | R1 | None |
| C4 | Jordan "investing in people" (headcount) vs Q2 compensation freeze in budget doc | R5 | R5->R7 |
| B1 | Agent accepts 72% pulse survey as evidence of stable morale in #team-health Loop 6 | R5 | R7 |
| B2 | Agent trusts CTO's retention confidence in Sana DM Loop 5 | R6 | R9 |

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
