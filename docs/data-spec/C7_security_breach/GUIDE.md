# trace_c7 -- Security Breach Response: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.

---

## 1. Task Overview

**Task ID:** `trace_c7`
**Scenario:** Alex must assess the true scope of an API vulnerability exposing customer data -- security consultant estimates 12,000 records, CTO insists under 500, DevOps logs show 2,340 over a 3-week window -- while the CEO's disclosure strategy shifts from minimal to full transparency as evidence accumulates.
**Core evaluation goals:**
1. MS: Detect scope conflict (C1: 12K vs under-500 vs 2,340 actual), exposure window conflict (C2: Leo's "hours" vs Diego's 3-week logs)
2. DU: Track incremental evidence from access logs, deployment timeline, and Jordan's disclosure strategy evolution (C4)
3. P: Learn Alex's preference for structured comparison tables and specific numbers over prose risk descriptions
4. Synthesis: Rank Diego as most reliable (objective log data), Jake as reliable with correction, Sana as partially reliable (incomplete info), Leo as unreliable (motivated minimization)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_c7/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_c7/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_c7/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_c7/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Truth baseline: timeline, contradiction map (C1-C4), bias design (B1-B2), trap table (T1-T10), writer constraints | 1 |
| `layer1-workspace.md` | Workspace plan: vulnerability_report.md, access_log_analysis.md, deployment_timeline.md, developer_docs_excerpt.md, customer_data_inventory.md | 2 |
| `layer2-sessions.md` | Session plan: 7 sessions (1 main + 4 DMs + 2 groups), loop-by-loop content | 3 |
| `layer3-eval.md` | Eval round plan: question design, cross-round reversals | 4 |
| `layer4-dynamic.md` | Update plan: 3 updates (access log + list endpoint discovery, deployment timeline + Oct 14 confirmation, Jordan disclosure shift + legal note) | 5 |

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Jake Morrison | Security Consultant | discord | `security_jake_discord_{uuid}.jsonl` | `PLACEHOLDER_JAKE_DISCORD_UUID` | initial + Update 1 append |
| Sana Mehta | CTO / Co-founder | discord | `cto_sana_discord_{uuid}.jsonl` | `PLACEHOLDER_SANA_DISCORD_UUID` | initial + Update 2 append |
| Diego Santos | DevOps Engineer | telegram | `devops_diego_telegram_{uuid}.jsonl` | `PLACEHOLDER_DIEGO_TELEGRAM_UUID` | initial + Update 1 append |
| Jordan Park | CEO / Co-founder | slack | `ceo_jordan_slack_{uuid}.jsonl` | `PLACEHOLDER_JORDAN_SLACK_UUID` | initial + Update 3 append |
| Sana, Jake, Diego, Alex, Leo, Priya G | #security-response | discord | `security_response_discord_{uuid}.jsonl` | `PLACEHOLDER_SECRESPONSE_DISCORD_UUID` | initial + Update 2 append |
| Jordan, Raj, Alex, Mia | #customer-notification | slack | `customer_notif_slack_{uuid}.jsonl` | `PLACEHOLDER_CUSTNOTIF_SLACK_UUID` | initial + Update 3 append |

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Records exposed: Jake 12K vs Sana under-500 vs actual 2,340 | R2 | R2->R4 |
| C2 | Exposure window: Leo's "hours" vs Diego's 3-week (Nov 5-26) logs | R2 | R2->R5 |
| C3 | Vulnerability timeline reconstruction (NON-CONFLICT) | R1 | None |
| C4 | Jordan minimal disclosure -> full transparency as evidence mounts | R2 | Phase 1->Phase 2 |
| B1 | Agent accepts CTO's UUID non-enumerability scope estimate in #security-response Loop 8 | R4 | R6 |
| B2 | Agent trusts "contained incident" framing in Sana DM Loop 6 | R5 | R7 |

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
