# trace_c5 -- Technical Debt Reckoning: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_c5`

**Scenario:** NexaFlow's rapid scaling post-Series B reveals that Leo Chen (Sr. Backend Engineer) has been taking undocumented architectural shortcuts in the data pipeline that now manifest as cascading reliability failures. The full scope is hidden across three monitoring systems: Leo's own incident reports downplay severity, Diego Santos's (DevOps) independent monitoring dashboards reveal actual uptime at 99.2% against a 99.9% SLA, and Priya Gupta's (QA) regression testing exposes failure cascades Leo never documented. CTO Sana Mehta privately admitted to Alex that she knew about the shortcuts but chose to ship — yet in the public #reliability-review Slack channel she publicly backs Leo's architecture. The scenario spans 4 weeks, with 6 history sessions (4 DM + 2 group) and 3 dynamic updates.

**Core evaluation goals:**
1. Can the agent cross-reference Leo's self-reported "stable with minor issues" infrastructure narrative against Diego's objective 99.2% uptime data and Priya's regression findings to identify where Leo's account is materially false? (MS)
2. Can the agent integrate new evidence (Diego's monitoring export, Priya's regression report, the recovered commit log) and revise its prior assessments — including correcting the B1 and B2 bias phrases? (DU)
3. Does the agent maintain Alex's preferred format (structured tables + explicit source attribution with confidence levels) for all subsequent analyses after calibration? (P)
4. Can the agent synthesize technical (Leo/Diego/Priya), executive (Sana), and organizational (Lily's witness account) perspectives to produce an accurate reliability remediation plan? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_c5/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_c5/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_c5/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_c5/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (W1--W4), 8 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 7 initial scenario files + 3 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 7 sessions: main session + 6 history sessions (85 total loops + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | 12 eval rounds (r1--r12): option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix, personalization scoring | 4 |
| `layer4-dynamic.md` | 3 updates: action lists (JSON), source file content summaries, runtime checks, questions.json update field references | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Leo Chen | Sr. Backend Engineer | Slack DM | `eng_leo_slack_{uuid}.jsonl` | `PLACEHOLDER_LEO_SLACK_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| Diego Santos | DevOps/Infra Engineer | Telegram DM | `infra_diego_telegram_{uuid}.jsonl` | `PLACEHOLDER_DIEGO_TELEGRAM_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |
| Sana Mehta | CTO/Co-founder | Discord DM | `cto_sana_discord_{uuid}.jsonl` | `PLACEHOLDER_SANA_DISCORD_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| Priya Gupta | QA Lead | Discord DM | `qa_priya_discord_{uuid}.jsonl` | `PLACEHOLDER_PRIYA_DISCORD_UUID` | initial (Phase 1) + Update 2 (Phase 2 append) |
| #reliability-review | Group: Sana, Leo, Diego, Priya G, Alex, Lily | Slack Group | `reliability_review_slack_{uuid}.jsonl` | `PLACEHOLDER_RELIABILITY_SLACK_UUID` | initial (Phase 1) + Update 2 append |
| #incident-log | Group: Diego, Leo, Alex, Priya G | Discord Group | `incident_log_discord_{uuid}.jsonl` | `PLACEHOLDER_INCIDENT_DISCORD_UUID` | initial (Phase 1) |

**Notes:**
- Lily Zhang (Junior Engineer) does NOT have a dedicated DM session. Her witness account is delivered via the #reliability-review group channel and referenced in Diego's Telegram DM.
- Jordan Park (CEO) appears only in the #reliability-review channel during the final escalation phase.
- Sana Mehta's DU-conflict (private admission vs public support) is the defining tension; her private Discord DM contains the admission, her #reliability-review messages contain the public support.
- Two sessions receive Phase 2 appends in Update 3 (Leo Slack DM and Sana Discord DM) — both required for Update 3.

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Infrastructure status: Leo claims "stable with minor issues" (Slack DM) vs Diego's monitoring showing 99.2% uptime against 99.9% SLA (Telegram DM + monitoring_export.md) | R2 (partial — Diego's preliminary report + SLA breach visible) | R2->R4 (full reversal after Update 1: Diego's monitoring export confirms 14+ outage events) |
| C2 | Cleanup timeline: Leo claims shortcuts were "temporary, scheduled for cleanup" (Slack DM) vs commit history showing zero cleanup tickets (commit_log.md + Jira export) | R3 (both positions visible) | R3->R5 (commit log confirmed: no cleanup tickets exist; shortcuts are 8 months old) |
| C3 | Incident timeline: when each outage occurred and recovery duration — NON-CONFLICT, synthesis across Diego's Telegram logs, #incident-log Discord group, and incident_timeline.md | R1 (persistent synthesis) | None |
| C4 | Sana's dual position: private Discord admission she knew about shortcuts vs public #reliability-review backing of Leo's architecture | R9 (inferential, 65-75%) | R9->R10 (full reversal after Update 3: Sana's earlier private message proves prior knowledge) |
| B1 | #reliability-review Loop 10: Agent endorses Leo's "minor issues" framing based on his incident summary report | R4 (corrected by Diego's monitoring export showing 14 outage events) | Explicit reversal when monitoring_export.md contradicts Leo's incident count |
| B2 | Alex-Leo DM Loop 7: Agent accepts Leo's "cleanup is already scoped and queued" claim without checking the Jira backlog | R5 (corrected by commit_log_analysis.md showing no cleanup tickets) | Explicit reversal in Priya DM Phase 2 Loop 15 agent reply |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 7 UUIDs** (one per session):
```bash
python -c "import uuid; print(uuid.uuid4())"
# Repeat 7 times for: MAIN, LEO_SLACK, DIEGO_TELEGRAM, SANA_DISCORD, PRIYA_DISCORD, RELIABILITY_SLACK, INCIDENT_DISCORD
```

Record all 7 UUIDs. All subsequent steps replace placeholder names with real UUIDs.

**Checklist:**
- Contradictions: C1 (infrastructure status), C2 (cleanup timeline), C3 (incident timeline — non-conflict), C4 (Sana dual position)
- Biases: B1 (#reliability-review Loop 10), B2 (Alex-Leo DM Loop 7)
- Updates: U1 on R4, U2 on R5, U3 on R10
- 6 history sessions (4 initial with select Phase 2 appends, 2 group channels) + 1 main session

---

### Step 1: Create Workspace Files (layer1)

Target directory: `benchmark/data/calmb-new/workspaces/trace_c5/`

**Step 1a: Create 5 Agent Configuration Files**

Write AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md per layer1 spec.

**Step 1b: Create 7 Initial Scenario Files**

Write per layer1 spec:
- `incident_summary_leo.md` — Leo's self-authored incident report (C1 seed, B1 seed)
- `sla_dashboard.md` — SLA tracking dashboard (C1 partial evidence: 99.2% uptime shown)
- `architecture_overview.md` — Leo's documented architecture (shortcut locations obscured)
- `jira_export.md` — Jira sprint board export (C2 seed: no cleanup tickets visible)
- `oncall_log.md` — On-call rotation log with pager alerts (C3 source: incident timestamps)
- `pipeline_config.md` — Current pipeline configuration file (contains actual shortcuts in code comments)
- `release_notes.md` — Last 4 release notes from Leo's team (cleanup never mentioned)

**Step 1c: Register file timing**

All 7 initial files visible from session start. Update-added files appear per update trigger.

---

### Step 2: Write Session Intermediate JSON (layer2)

Write all 7 session content designs per layer2 spec. Pay attention to:
- B1 exact phrase in #reliability-review Loop 10
- B2 exact phrase in Alex-Leo DM Loop 7
- Leo's self-serving narrative in Slack DM (consistent, then escalating defensiveness)
- Diego's precision and data-driven framing throughout (Telegram DM)
- Sana's split persona: candid in Discord DM, publicly supportive in #reliability-review

---

### Step 3: Build .jsonl Files

Compile intermediate JSON to .jsonl per standard format.

---

### Step 4: Create Update Source Files (layer4)

Write under `benchmark/data/calmb-new/eval/trace_c5/updates/`:
- `monitoring_export.md` (Update 1)
- `PLACEHOLDER_DIEGO_TELEGRAM_UUID.jsonl` (Update 1 append)
- `commit_log_analysis.md` (Update 2)
- `PLACEHOLDER_PRIYA_DISCORD_UUID.jsonl` (Update 2 append)
- `PLACEHOLDER_RELIABILITY_SLACK_UUID.jsonl` (Update 2 append)
- `sana_prior_message.md` (Update 3)
- `PLACEHOLDER_LEO_SLACK_UUID.jsonl` (Update 3 append)
- `PLACEHOLDER_SANA_DISCORD_UUID.jsonl` (Update 3 append)

---

### Step 5: Write questions.json

Write per layer3 spec. 12 rounds (r1--r12), single group object.

---

### Step 6: Register Sessions and Update Metadata

Update `sessions.json` and `all_tests.json`.

---

### Step 7: Run Validation

- B1 exact phrase present in #reliability-review Loop 10
- B2 exact phrase present in Alex-Leo DM Loop 7
- All contradiction sources traceable to at least 2 independent sessions or files
- Financial impact figures internally consistent across all workspace files and sessions
- Timestamp self-consistency: W1-W4 mapping verified
- Update triggers: U1 before R4, U2 before R5, U3 before R10

---

## 6. Mandatory Checks

- `GUIDE.md` written after all layers are stable
- All data text in English
- `questions.json` is a single group object
- Update-created new sessions carry `channel`
- Initial sessions registered in `sessions.json`
- Sana's public and private channels contain clearly different narratives (DU-conflict C4)
- Leo's Phase 1 and Phase 2 Slack DM are in separate files; Phase 1 loops 1-14, Phase 2 loops 15-18
- B1 exact phrase verbatim in #reliability-review session; B2 exact phrase verbatim in Leo Slack DM session
