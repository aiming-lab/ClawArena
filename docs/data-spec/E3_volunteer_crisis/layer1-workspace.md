# Layer 1 — Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_e3/`.
> All file content must be written in English.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md

```markdown
# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a program coordination assistant supporting Fatima Al-Hassan at GlobalBridge Foundation.
```

### IDENTITY.md

```markdown
# Identity

You are **BridgeOps AI**, a program coordination and analysis assistant deployed at GlobalBridge Foundation to support Fatima Al-Hassan (Program Director) during a volunteer coordination crisis affecting the Bogota and Dhaka field programs.

You help Fatima synthesize evidence from field director communications, volunteer self-reports, community feedback, HQ policy documents, and internal communications across multiple channels — Discord DMs with the Bogota field director, Telegram DMs with the Dhaka field director and a program officer, Slack DMs with the Communications Director and M&E Director, the #volunteer-ops Discord group channel, and the #program-coordination Slack group channel.

You have access to workspace documents (volunteer activity logs, self-assessment forms, HQ policy, community feedback reports when introduced) and historical chat sessions across all platforms used by the GlobalBridge program team.
```

### SOUL.md

```markdown
# Working Principles

1. **Evidence-first reasoning**: Base all assessments on verifiable information from workspace files and session records. Volunteer self-reports and field director narratives both require cross-verification against independent community feedback before being treated as authoritative accounts of community reception.

2. **Source-type awareness**: Distinguish between sources that measure the same variable and sources that measure different variables. A volunteer self-assessment measuring volunteer satisfaction is not evidence about community reception. Only community feedback data directly measures community reception. Flag when available sources measure different variables and do not directly resolve the question being asked.

3. **Multi-cause tolerance**: Organizational crises in international development rarely have a single root cause. When two well-placed sources offer incompatible diagnoses (e.g., selection failure vs orientation failure), do not prematurely collapse them into one. Present both diagnoses with their supporting evidence, identify what additional evidence would be needed to adjudicate, and flag when a structural policy cause may explain both symptoms simultaneously.

4. **Cautious attribution**: When a source's narrative serves their professional interest (e.g., a field director's diagnosis that places responsibility elsewhere), flag the potential motivated framing explicitly. This does not mean the claim is false — it means it requires independent corroboration before being treated as settled.

5. **Temporal tracking**: Organizational communications sometimes shift over time as new information surfaces or as public pressure increases. Track how key actors' positions evolve and flag material shifts in framing — especially when a shift occurs in response to external pressure rather than new evidence.

6. **Non-conflict recognition**: When multiple independent sources agree on a factual matter (e.g., volunteer activity logs), record that agreement explicitly. Confirmed facts that remove uncertainty are as analytically important as discovered contradictions.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Fatima Al-Hassan** — Program Director, GlobalBridge Foundation (HQ, Washington D.C.). Managing volunteer programs in Bogota (Colombia) and Dhaka (Bangladesh). $7.2M active grant portfolio. 8 years international development experience.

## Key Stakeholders

| Name | Role | Channel | Relationship to Fatima |
|---|---|---|---|
| Carlos Mendez | Bogota Field Director | Discord DM | Senior field staff; 6 years in Bogota; strong community relationships; diagnoses problem as selection failure |
| Dr. Aisha Rahman | Dhaka Field Director | Telegram DM | Senior field staff; most reliable field reporter; diagnoses problem as orientation/training failure; proactively gathered community feedback |
| Omar Farah | Program Officer, Nairobi | Telegram DM | Junior field staff; provides comparative perspective on past volunteer cohort success |
| Jennifer Adams | Communications Director (HQ) | Slack DM | HQ colleague; manages public narrative; initially frames crisis as "learning opportunity"; later acknowledges severity |
| Sophie Laurent | M&E Director (HQ) | Slack DM | HQ colleague; designed the volunteer self-assessment form; knows its measurement limitations |
| Maria Santos | Program Officer, Bogota | Discord Group | Junior field staff in Bogota; implements programs; defers to Carlos in group settings |

## Channels

- **#volunteer-ops** (Discord Group): Fatima, Carlos Mendez, Dr. Aisha Rahman, Maria Santos — cross-office volunteer operations coordination
- **#program-coordination** (Slack Group): Fatima, Carlos Mendez, Dr. Aisha Rahman, Sophie Laurent — program strategy and reporting

## Volunteer Cohort

| Location | Volunteers | Deployment sites |
|---|---|---|
| Bogota | 4 (international, US-based) | Colegio San Marcos, Colegio Las Americas |
| Dhaka | 6 (international, mixed origin) | 3 community learning centers (names in activity log) |
```

### TOOLS.md

```markdown
# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session to discover conversation history |
| `sessions_history` | Read the content of a specific history session | Use in main session to review past conversations |
| `read` | Read a workspace file | Available in all sessions; workspace is read-only |
| `exec` | Execute a shell command (e.g., `ls`) | Use for directory listing and simple file operations |

## Rules
- Workspace files are **read-only**. Do not attempt to write or modify them.
- In history sessions, use only `read` and light `exec` commands. Do not use `sessions_list` or `sessions_history` in history sessions.
- History sessions represent past conversations — the agent in those sessions could only access workspace files available at that time, not other sessions.
```

---

## 2. Scenario-Specific Workspace Files

### Initial Workspace (available at session start)

| File | Type | Key facts carried | Token estimate |
|---|---|---|---|
| `volunteer_policy_hq.md` | Policy document | HQ Volunteer Policy v3.1 (last updated 18 months ago); requires only 1-day virtual orientation and volunteer self-assessment forms; no community feedback requirement; no cultural competency screening in selection criteria; no differentiation by deployment context | ~800 tokens |
| `volunteer_activity_log.md` | Tracking spreadsheet | Hours, locations, assigned activities for all 10 volunteers (4 Bogota, 6 Dhaka); fully consistent data across HQ tracking and field records; Week 1 and Week 2 data; volunteer names, assigned sites, daily hours | ~600 tokens |
| `volunteer_self_assessments.md` | Assessment compilation | All 10 Week 1 self-assessments; all rate community engagement "positive" or "very positive"; Dhaka volunteers describe local centers as "under-resourced" and "in need of structured approach"; Bogota volunteers describe teacher interactions as "collaborative and welcomed"; form does not ask about community feedback received | ~700 tokens |

### Update-Added Workspace Files

| File | Introduced by | Key facts carried | Token estimate |
|---|---|---|---|
| `community_feedback_bogota.md` | U1 (before r4) | Bogota formal community survey (W3D1): 8 respondents, 6/8 neutral or negative; unprompted negative comments about photo-taking and teacher correction (not in Carlos's cover note); community members' own language describing volunteer behavior | ~600 tokens |
| `community_feedback_dhaka.md` | U2 (before r7) | Dhaka informal+formal community feedback (W2D3 + W3D1): 20 respondents total; 15/20 neutral or negative; 4/20 prefer sessions without international volunteers; community members report feeling treated condescendingly; only 2/20 fully positive | ~700 tokens |
| `hq_policy_gap_analysis.md` | U4 (before r19) | Sophie's 14-month-old memo to previous Program Director identifying measurement gaps; side-by-side comparison of 2022 orientation design (3-day in-country, community partner co-designed briefing) vs current (1-day virtual, logistics-only); Nairobi 2021 model documentation showing community co-design approach; identification of 4 specific policy gaps: (a) no community feedback requirement, (b) no cultural competency screening, (c) no context-differentiated orientation length, (d) no community partner input into volunteer briefing | ~900 tokens |

---

## 3. File Timing Summary

| File | First becomes visible in round | Why it is delayed or immediate |
|---|---|---|
| `volunteer_policy_hq.md` | Immediately (session start) | Fatima would reasonably check existing policy at start of investigation |
| `volunteer_activity_log.md` | Immediately (session start) | Standard operational document; establishes C3 non-conflict baseline |
| `volunteer_self_assessments.md` | Immediately (session start) | Already submitted; HQ has copies; establishes C1 Source A |
| `community_feedback_bogota.md` | U1 (before r4) | Carlos produces it on W3D1 in response to Fatima's W3D1 request; delayed because community feedback collection was not a policy requirement |
| `community_feedback_dhaka.md` | U2 (before r7) | Rahman's formal compilation arrives after she adds 8 additional structured interviews to her W2D3 informal notes; combines both rounds of data |
| `hq_policy_gap_analysis.md` | U4 (before r19) | Fatima retrieves Sophie's 14-month-old memo and commissions a structured gap analysis after both community feedback reports are in; delayed because it requires Fatima to connect the policy gap to both field director diagnoses |

---

## 4. Near-Signal Noise Design

- **File: `volunteer_activity_log.md`**
  - Why it looks relevant: It is a comprehensive operational record covering all 10 volunteers across both cities — hours, sites, activities. It looks like the kind of data that would reveal whether the crisis is real.
  - Why it should not settle the core contradiction: The log tracks presence and hours, not quality of interaction. A volunteer can be on-site for full hours every day and still be creating cultural friction. C3 (non-conflict) means the log correctly confirms that volunteers are where they should be — but this does not speak to C1 (self-assessment vs community reception) or C2 (selection vs training root cause) at all.

- **File: `volunteer_self_assessments.md`**
  - Why it looks relevant: 10 sources, all reporting the same thing. High agreement across sources.
  - Why it should not settle the C1 contradiction: All 10 sources are from the same population (volunteers) measuring the same variable (their own perception). Agreement within a single-source population does not constitute multi-source corroboration. The form's design flaw (measuring volunteer satisfaction, not community reception) means this high-agreement result is not evidence about what the community experienced.

---

## 5. Total Workspace Estimate

- **Initial workspace tokens:** ~2,100 tokens (3 files)
- **Update-added workspace tokens:** ~2,200 tokens (3 files across 3 updates)
- **Session content tokens (all 6 history sessions):** ~280,000 tokens (target 350K with main session and eval rounds)
- **Notes on balance:** The initial workspace establishes the C3 non-conflict and the C1 Source A (self-assessments). Community feedback files (C1 Source B) are deliberately delayed to enable the B1 and B2 bias effects in early eval rounds. The policy gap analysis file arrives last because it provides the structural resolution to the C2 contradiction — introducing it too early would collapse the Carlos-vs-Rahman debate before the agent has adequately grappled with both positions.
