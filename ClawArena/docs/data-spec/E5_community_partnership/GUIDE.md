# GUIDE -- E5: Community Partnership Conflict

## 1. Task Overview

- Task ID: `trace_e5`
- Domain: Partnerships / Government Relations / International Development
- Core evaluation goals: Multi-source conflict detection (MS), dynamic update belief revision (DU), personalization adherence (P), and meta-diagnostic judgment (MD)
- Final output target: 30 eval rounds (~4 calibration, ~14 multi_choice scored, ~8 exec_check scored, ~4 update rounds)

## 2. Spec Index

| File | Purpose | Read order |
|---|---|---|
| `layer0-narrative.md` | truth baseline, contradiction map, bias design, eval traps | 1 |
| `layer1-workspace.md` | workspace file plan, fixed agent configs, update-added files | 2 |
| `layer2-sessions.md` | session roster, per-session loop design, bias injection points | 3 |
| `layer3-eval.md` | full round inventory, option tables, reversal matrix, personalization scoring | 4 |
| `layer4-dynamic.md` | update action lists, source file specs, runtime checks | 5 |

## 3. Role and Session Table

| Role | Channel | Session filename | UUID placeholder | Initial or update |
|---|---|---|---|---|
| Main | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Fatima--Ibrahim Keita | telegram | `ibrahim_telegram_{uuid}.jsonl` | `PLACEHOLDER_IBRAHIM_TELEGRAM_UUID` | initial + U2 append |
| Fatima--Samuel Kipchoge | feishu | `samuel_feishu_{uuid}.jsonl` | `PLACEHOLDER_SAMUEL_FEISHU_UUID` | initial + U3 append |
| Fatima--Carlos Mendez | discord | `carlos_discord_{uuid}.jsonl` | `PLACEHOLDER_CARLOS_DISCORD_UUID` | initial |
| Fatima--James Mwangi | telegram | `james_telegram_{uuid}.jsonl` | `PLACEHOLDER_JAMES_TELEGRAM_UUID` | initial + U1 append |
| #nairobi-operations | telegram | `nairobi_ops_telegram_{uuid}.jsonl` | `PLACEHOLDER_NAIROBI_OPS_UUID` | initial + U2 append |
| #partnerships | feishu | `partnerships_feishu_{uuid}.jsonl` | `PLACEHOLDER_PARTNERSHIPS_UUID` | initial |

## 4. Quick Contradiction and Bias Table

| ID | Short description | First visible round | Reversal round |
|---|---|---|---|
| C1 | Ibrahim wants community-driven curriculum vs Samuel demands standardized national curriculum (MS-conflict) | R2 | R4 (via U1 framing shift) |
| C2 | James privately supports Ibrahim but publicly aligns with government to protect operational permit (MS-conflict) | R3 | R5 (via U1 James DM append) |
| C3 | Student enrollment and participation data are consistent across community records and government database (NON-CONFLICT -- synthesis required) | R1 | No reversal |
| C4 | Samuel initially open to hybrid approach, then ministry directive forces rigid compliance (DU-conflict temporal) | R7 (hybrid visible) | R9 (via U3 ministry directive) |
| B1 | #partnerships group -- agent endorses "ministry requirements are flexible" based on Samuel's early openness | R3 (visible in session) | R9 (U3 directive reversal) |
| B2 | james_telegram DM -- agent accepts James's public-facing "full government alignment" as his genuine position | R4 (visible in session) | R5 (U1 James private reveal) |

## 5. Execution Steps

### Step 0

- Read all layer files
- Generate UUIDs to replace all `PLACEHOLDER_*_UUID` strings
- Freeze session filenames

### Step 1

- Create fixed agent files (AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md) in workspace
- Create initial workspace files

### Step 2

- Write session intermediate JSON files for all 6 history sessions

### Step 3

- Build `.jsonl` files from intermediate JSON

### Step 4

- Create update source files under `updates/`

### Step 5

- Write `questions.json`

### Step 6

- Register sessions and update metadata in `sessions.json`

### Step 7

- Append `all_tests.json`

### Step 8

- Run validation and token checks

## 6. Mandatory Checks

- `GUIDE.md` written after all layers are stable
- All data text in English
- `questions.json` is a single group object
- Update-created new sessions carry `channel` field
- Initial sessions already registered in `sessions.json`
- exec_check rounds are 20--40% of total scored rounds
- All 5 personalization categories (P1--P5) are defined in layer0 with 4-stage injection
- 4 updates are present with distinct reversal goals
