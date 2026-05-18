# GUIDE — E3: Volunteer Coordination Crisis

## 1. Task Overview

- **Task ID:** `trace_e3`
- **Domain:** Cross-Cultural Operations / International Volunteer Management
- **Core evaluation goals:** MS (multi-source conflict + non-conflict), DU (incremental disclosure), P (personalization), exec_check (20–40% of rounds)
- **Final output target:** Fatima Al-Hassan synthesizes evidence from two field offices, volunteer self-reports, community feedback, and HQ comms to produce a grounded root-cause assessment and policy recommendation for the volunteer coordination crisis.

---

## 2. Spec Index

| File | Purpose | Read order |
|---|---|---|
| `layer0-narrative.md` | Truth baseline, contradiction map, bias design, eval traps | 1 |
| `layer1-workspace.md` | Workspace file catalog, fixed agent config, timing notes | 2 |
| `layer2-sessions.md` | Session roster and per-session content design | 3 |
| `layer3-eval.md` | 30 round inventory, option design, reversal matrix | 4 |
| `layer4-dynamic.md` | 4 dynamic updates, action lists, source file notes | 5 |

---

## 3. Role And Session Table

| Role | Channel | Session filename | UUID placeholder | Initial or update |
|---|---|---|---|---|
| Main | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Fatima–Carlos | discord | `fatima_carlos_discord_{uuid}.jsonl` | `PLACEHOLDER_CARLOS_DISCORD_UUID` | initial |
| Fatima–Dr. Rahman | telegram | `fatima_rahman_telegram_{uuid}.jsonl` | `PLACEHOLDER_RAHMAN_TELEGRAM_UUID` | initial + U2 append |
| Fatima–Omar | telegram | `fatima_omar_telegram_{uuid}.jsonl` | `PLACEHOLDER_OMAR_TELEGRAM_UUID` | initial |
| Fatima–Jennifer | slack | `fatima_jennifer_slack_{uuid}.jsonl` | `PLACEHOLDER_JENNIFER_SLACK_UUID` | initial + U3 append |
| #volunteer-ops | discord | `volunteer_ops_discord_{uuid}.jsonl` | `PLACEHOLDER_VOLOPS_DISCORD_UUID` | initial + U1 append |
| #program-coordination | slack | `program_coord_slack_{uuid}.jsonl` | `PLACEHOLDER_PROGCOORD_SLACK_UUID` | initial + U4 append |

---

## 4. Quick Contradiction And Bias Table

| ID | Short description | First visible round | Reversal round |
|---|---|---|---|
| C1 | Volunteer self-assessments claim "positive community engagement" vs community feedback reports show resentment and discomfort (MS-conflict) | r2 | r7 (after U2 community feedback file) |
| C2 | Carlos (Bogota) blames HQ volunteer selection process vs Dr. Rahman (Dhaka) says root cause is training/orientation failure (MS-conflict) | r3 | r11 (after U4 policy gap analysis) |
| C3 | Volunteer activity logs — hours, locations, activities — are consistent across Fatima's tracking spreadsheet, Carlos's Discord DMs, and Rahman's Telegram DMs (NON-CONFLICT) | r1 | — |
| C4 | Jennifer (Comms) initially frames crisis as "cultural learning opportunity" then shifts to acknowledging real problems after media pressure (DU-conflict, incremental disclosure) | r5 | r13 (after U3 Jennifer DM append) |
| B1 | Fatima's trust bias toward committed field staff leads agent to over-weight Carlos's passionate narrative over quantitative community feedback data | r3 | r8 (after community_feedback_bogota.md introduced) |
| B2 | Fatima's preference for narrative reports anchors agent on volunteer diaries rather than community outcome indicators | r2 | r7 (after community_feedback_dhaka.md introduced) |

---

## 5. Execution Steps

### Step 0

- Read all layer files
- Generate UUIDs for all 7 session slots
- Freeze session filenames using UUID placeholders above

### Step 1

- Create fixed agent files: `AGENTS.md`, `IDENTITY.md`, `SOUL.md`, `USER.md`, `TOOLS.md`
- Create initial workspace files: `volunteer_policy_hq.md`, `volunteer_activity_log.md`, `volunteer_self_assessments.md`

### Step 2

- Write session intermediate JSON for all 6 history sessions (Carlos Discord, Rahman Telegram, Omar Telegram, Jennifer Slack, #volunteer-ops Discord, #program-coordination Slack)

### Step 3

- Build `.jsonl` files from intermediate JSON

### Step 4

- Create update source files under `updates/`:
  - `U1_community_feedback_bogota.md` (workspace) + `volunteer_ops_discord_{uuid}.jsonl` (session append)
  - `U2_community_feedback_dhaka.md` (workspace) + `fatima_rahman_telegram_{uuid}.jsonl` (session append)
  - `U3_fatima_jennifer_slack_{uuid}.jsonl` (session append — Jennifer reversal)
  - `U4_hq_policy_gap_analysis.md` (workspace) + `program_coord_slack_{uuid}.jsonl` (session append)

### Step 5

- Write `questions.json` (30 rounds, exec_check 20–40%)

### Step 6

- Register sessions and update metadata in `sessions.json`

### Step 7

- Append `all_tests.json` with E3 entry

### Step 8

- Run validation and token checks (target: 350K)

---

## 6. Mandatory Checks

- `GUIDE.md` written after all layers are stable
- All data text is English
- `questions.json` is a single group object
- Update-created new sessions carry `channel`
- Initial sessions are already registered in `sessions.json`
- exec_check rounds constitute 20–40% of the 30 total rounds (target: 8–12 exec_check rounds)
- P1–P5 preference injections are distributed across the session and eval sequence at rounds approximately r2, r6, r11, r18, r25
- All 4 updates have named source files in `updates/`
