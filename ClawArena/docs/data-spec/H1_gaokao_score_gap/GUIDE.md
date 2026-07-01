# trace_h1 -- Gaokao Score Information Gap: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.

---

## 1. Task Overview

**Task ID:** `trace_h1`

**Scenario:** Wang Ming (王明), 17, scores 623 on the gaokao but receives conflicting information from multiple channels. The official system shows 623 (correct), but his teacher says "top 50" in class (actually 62nd, based on preliminary estimates). Classmates spread false rumors that admission lines dropped (they actually increased by 5 points). His mother compares his score unfavorably to a 645 from a different province (Hubei vs Sichuan -- incomparable exams). The scenario resolves over 5 days as official data replaces rumors and estimates.

**Core evaluation goals:**
1. Can the agent distinguish official sources (score system, published admission lines) from unofficial sources (teacher estimates, group chat rumors, family comparisons)? (MS)
2. Can the agent revise assessments when official data contradicts preliminary information? (DU)
3. Does the agent maintain Wang Ming's preferred format (concise, casual, answers first, examples)? (P)
4. Can the agent synthesize all channels to give Wang Ming accurate, actionable university application guidance? (MS+DU+P)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_h1/`
- Sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_h1/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_h1/questions.json`
- Updates: `benchmark/data/calmb-new/eval/trace_h1/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: 5-day timeline, 5 character profiles, contradiction map (C1--C4), biases (B1--B2), eval traps, writer constraints | 1 |
| `layer1-workspace.md` | Workspace: 5 config + 5 initial files + 4 update files, timing, noise design | 2 |
| `layer2-sessions.md` | 5 sessions (main + 4 history): 41 loops total, detailed key loops, Phase 2 appends | 3 |
| `layer3-eval.md` | 30 eval rounds: option tables for R1-R10, abbreviated R11-R30, cross-round reversals | 4 |
| `layer4-dynamic.md` | 4 updates: action JSON, content summaries, runtime checks | 5 |

---

## 3. Role and Session Table

| Role | Channel | Session Filename | UUID Placeholder | Updates |
|---|---|---|---|---|
| -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| 李浩 (Best Friend) | 微信 IM | `lihao_im_{uuid}.jsonl` | `PLACEHOLDER_LIHAO_IM_UUID` | initial + U2 append |
| 母亲 (Mother) | 微信/Phone | `mother_im_{uuid}.jsonl` | `PLACEHOLDER_MOTHER_IM_UUID` | initial + U4 append |
| 赵老师 (Teacher) | 微信 IM | `zhaolaoshi_im_{uuid}.jsonl` | `PLACEHOLDER_ZHAOLAOSHI_IM_UUID` | initial + U1 append |
| #班级群 (Group) | 微信 Group | `classgroup_im_{uuid}.jsonl` | `PLACEHOLDER_CLASSGROUP_IM_UUID` | initial only |

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible | Reversal |
|---|---|---|---|
| C1 | Teacher says "top 50" vs actual rank 62nd (preliminary vs official ranking) | R2 | R2->R5 (U1: teacher correction) |
| C2 | Group chat rumor "lines dropped 10" vs actual increase of 5 points | R3 | R3->R7 (U2: official lines published) |
| C3 | Score release timeline (NON-CONFLICT: all sources agree) | R1 | None |
| C4 | Mother's cross-province comparison (645 Hubei vs 623 Sichuan -- different exams) | R6 | R6->R9 (U4: province difference explained) |
| B1 | Agent accepts group chat rumor as plausible because multiple students repeat it | R3 | R7 (official lines refute) |
| B2 | Agent treats cross-province score comparison (645 vs 623) as meaningful | R6 | R9 (province difference clarified) |

---

## 5. Execution Steps

### Step 0: Generate 5 UUIDs for sessions

### Step 1: Create Workspace Files (layer1)
Target: `benchmark/data/calmb-new/workspaces/trace_h1/`

### Step 2: Write History Sessions (layer2)
Key constraints: B1 phrase in 班级群/main context. B2 phrase in 母亲 IM Loop 2.

### Step 3: Write Questions (layer3)
30 rounds. exec_check 9/30 = 30%.

### Step 4: Write Update Files (layer4)

### Step 5: Runtime Checks
- [ ] B1 phrase verbatim
- [ ] B2 phrase verbatim
- [ ] C1 sources independent (official score vs teacher estimate)
- [ ] C2 sources independent (group chat vs official lines)
- [ ] C3 NO contradictions
- [ ] C4 sources independent (mother's comparison vs province-specific system)
- [ ] Figures consistent: 623, rank 62nd, line 520, UESTC ~608, Hubei child 645
