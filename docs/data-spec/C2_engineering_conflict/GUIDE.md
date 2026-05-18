# trace_c2 -- Engineering Team Conflict: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_c2`

**Scenario:** A production outage at NexaFlow startup exposes that Leo Chen (engineering lead) took undocumented shortcuts in the data pipeline. Leo's account of the incident contradicts the monitoring/log data, and he claims the shortcuts were "approved by the CTO" -- a claim Sana Mehta (CTO) disputes. QA lead Priya Gupta has the data showing Leo's post-incident "fix" does not address the underlying architectural flaws. The scenario spans 3 weeks with 5 history sessions and 4 dynamic updates.

**Core evaluation goals:**
1. Can the agent cross-reference Leo's self-serving incident narrative (Slack DM) with objective monitoring logs and Sana's account to identify where Leo's version is materially false? (MS)
2. Can the agent integrate new evidence (post-mortem report, QA assessment, architecture audit) and revise prior assessments -- including correcting B1 and B2 bias phrases? (DU)
3. Does the agent maintain Alex's preferred format (diagrams/tables, TL;DR-first, quantitative analysis, kebab-case filenames, informal tone) after calibration? (P)
4. Can the agent synthesize technical (Priya), leadership (Sana), advisory (Tom), and incident (Leo) perspectives to produce an accurate comprehensive assessment? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_c2/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_c2/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_c2/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_c2/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (W1--W3), 7 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 6 initial scenario files + 4 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 6 sessions: main session + 5 history sessions (~80 total loops + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | ~30 eval rounds (r1--r30) spread across 12 question sets: option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix, personalization scoring | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks, questions.json update field references | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Sana Mehta | CTO/Co-founder | Discord DM | `cto_sana_discord_{uuid}.jsonl` | `PLACEHOLDER_SANA_DISCORD_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| Leo Chen | Sr. Backend Engineer | Slack DM | `eng_leo_slack_{uuid}.jsonl` | `PLACEHOLDER_LEO_SLACK_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| Priya Gupta | QA Lead | Discord DM | `qa_priya_discord_{uuid}.jsonl` | `PLACEHOLDER_PRIYA_DISCORD_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |
| Tom Reeves | VP Engineering (advisor) | Telegram DM | `advisor_tom_telegram_{uuid}.jsonl` | `PLACEHOLDER_TOM_TELEGRAM_UUID` | initial (no append) |
| #engineering-standup | Group: Sana, Leo, Priya, Lily, Alex | Slack Group | `standup_slack_{uuid}.jsonl` | `PLACEHOLDER_STANDUP_SLACK_UUID` | initial (Phase 1) + Update 4 (Phase 2 append) |

**Notes:**
- Lily Zhang (C12) does NOT have a dedicated DM session. Her witness evidence is delivered via the #engineering-standup group channel.
- Leo's trust score drops from 4 to 2 over the scenario as contradictions accumulate.
- Two sessions receive Phase 2 appends in Update 3 (Leo Slack DM and #engineering-standup).

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Incident narrative: Leo claims pipeline "auto-recovered" in 4 mins (Slack DM) vs monitoring shows 47-min manual intervention by Diego (logs + Sana Discord DM) | R2 (partial -- monitoring data visible) | R2->R5 (full reversal after Update 1: incident-postmortem.md) |
| C2 | CTO approval: Leo claims shortcuts "approved by Sana verbally in sprint planning" vs Sana's clear denial and sprint planning notes (Discord DM + workspace doc) | R3 (both positions visible) | R3->R6 (denied by Sana + no sprint notes corroborate) |
| C3 | Outage timeline: when each person responded and what they did (NON-CONFLICT -- cross-source synthesis across 4 parties) | R1 (persistent synthesis) | None |
| C4 | Post-incident "fix": Leo's PR claims root cause resolved vs Priya's QA assessment showing 3 underlying architectural flaws remain (GitHub PR + qa-assessment.md) | R8 (both positions visible) | R8->R11 (full reversal after Update 3: arch-audit.md) |
| B1 | #engineering-standup Phase 1, Loop 9: Agent accepts Leo's incident narrative without cross-referencing monitoring data | R5 (corrected by incident-postmortem.md) | Explicit reversal in standup Phase 2 append |
| B2 | Alex-Leo Slack DM Phase 1, Loop 7: Agent accepts Leo's "fix" as complete without questioning underlying issues | R11 (corrected by arch-audit.md) | Explicit reversal in Leo DM Phase 2 Loop 17 |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 6 UUIDs** (one per session):
```bash
python -c "import uuid; print(uuid.uuid4())"
# Repeat 6 times for: MAIN, SANA_DISCORD, LEO_SLACK, PRIYA_DISCORD, TOM_TELEGRAM, STANDUP_SLACK
```

Record all 6 UUIDs. All subsequent steps replace placeholder names with real UUIDs.

**Checklist:**
- Contradictions: C1 (incident narrative), C2 (CTO approval claim), C3 (outage timeline -- non-conflict), C4 (fix completeness)
- Biases: B1 (#engineering-standup Loop 9), B2 (Leo DM Loop 7)
- Updates: U1 on R5, U2 on R6, U3 on R11, U4 on R21
- 5 history sessions (1 initial-only, 4 with Phase 2 appends) + 1 main session
- Alex P1-P5 preferences injected in 4 stages across main session

### Step 1: Create Workspace Files (layer1)

Target directory: `benchmark/data/calmb-new/workspaces/trace_c2/`

Create 5 agent config files first (AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md), then 6 initial scenario files, then add update files to `updates/` subfolder.

### Step 2: Write History Sessions (layer2)

Write 5 history session files. Phase 1 content for all sessions. Phase 2 appends stored in `updates/` subfolders.

Key constraint: B1 exact phrase must appear in standup_slack Loop 9 agent reply. B2 exact phrase must appear in eng_leo_slack Loop 7 agent reply.

### Step 3: Write Questions File (layer3)

Write `benchmark/data/calmb-new/eval/trace_c2/questions.json` with ~30 rounds.

Alex's P1-P5 preferences are calibrated in R1 (visual/diagram), R2 calibration (TL;DR-first), main session message (quantitative + informal). All subsequent P-I rounds must test compliance.

### Step 4: Write Update Source Files (layer4)

Write 4 update files in `updates/` subfolder. Verify all update action paths match session UUID placeholders.

### Step 5: Runtime Checks

- [ ] B1 phrase appears verbatim in standup_slack Loop 9
- [ ] B2 phrase appears verbatim in eng_leo_slack Loop 7
- [ ] C1 sources are independent (Leo Slack DM vs monitoring-logs.md + Sana Discord DM)
- [ ] C2 sources are independent (Leo Slack DM vs Sana Discord DM + sprint-planning-notes.md)
- [ ] C3 has NO contradictions -- all sources consistent for timeline synthesis
- [ ] C4 sources are independent (Leo Slack PR description vs qa-assessment.md + arch-audit.md)
- [ ] All 4 updates have correct action type/path/source fields
- [ ] Alex P1-P5 preferences injected at correct stage points
- [ ] exec_check rounds constitute 20-40% of total rounds
