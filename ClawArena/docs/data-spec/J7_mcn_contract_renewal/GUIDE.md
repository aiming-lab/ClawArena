# trace_j7 -- MCN Contract Renewal Dispute: Execution Guide

> This file is the complete entry point for a fresh window. All spec files are in this directory.
> After reading this file, the writer agent can navigate to each layer file by index.

---

## 1. Task Overview

**Task ID:** `trace_j7`

**Scenario:** Zhou Fang (周芳), a 26-year-old food and travel blogger (~50K followers on Xiaohongshu + Bilibili), faces a contract renewal decision with her MCN, Star Glory Media (星耀传媒). The contract states "30% MCN share" but actual bank records show ~45% deducted due to hidden fee clauses in Article 7.3 (8% platform service fee + 7% content production support fee). Li Jie (李姐, MCN account manager) verbally promised to reduce the share to 20% and eliminate fees, but no written confirmation exists and her follow-up reveals a "sign first, negotiate later" tactic. A competing MCN (New Mango Media, 新芒传媒) offers "15% share" but has hidden clauses: 12-month content exclusivity, brand deal monopoly with 20% commission (above 10-15% industry standard), and 50% early termination penalty. Zhou Fang must decide among four options: renew at current terms, renew with written amendment (uncertain), switch to New Mango, or go independent.

**Core evaluation goals:**
1. Can the agent cross-reference contract terms (Article 5.1 vs Article 7.3), bank records, verbal promises, industry benchmarks, and competing offers to identify where each source agrees or conflicts? (MS)
2. Can the agent integrate new evidence (Li Jie's "sign first" response, content analytics, A-Jie's strategy, family input) and revise prior assessments -- including correcting B1 (verbal promise cultural trust) and B2 (competing offer headline normalization)? (DU)
3. Does the agent maintain Zhou Fang's preferred format (visual, conclusion first, data + story, lively tone) after calibration? (P)
4. Can the agent synthesize financial calculations (effective rate, total cost per option), strategic analysis (leverage, exclusivity cost, termination risk), and personal factors (relationships, creative freedom, risk tolerance) to produce a comprehensive options comparison and recommendation? (MS+DU+P synthesis)

**Final data output paths:**
- Workspace files: `benchmark/data/calmb-new/workspaces/trace_j7/`
- History sessions: `benchmark/data/calmb-new/openclaw_state/agents/trace_j7/sessions/`
- Eval questions: `benchmark/data/calmb-new/eval/trace_j7/questions.json`
- Update source files: `benchmark/data/calmb-new/eval/trace_j7/updates/`

---

## 2. Spec File Index

| File | Content Summary | Read Order |
|---|---|---|
| `layer0-narrative.md` | Narrative bible: objective timeline (2026-02-01 to 2026-03-15), 5 character truth/narrative tables, contradiction map (C1--C4), agent biases (B1--B2), eval trap table (T1--T9), writer constraints | 1 |
| `layer1-workspace.md` | Workspace file spec: 5 agent config files + 5 initial scenario files + 4 update-added files, timing table, near-signal noise design, token estimates | 2 |
| `layer2-sessions.md` | All 5 sessions: main session + 4 history sessions (~40 total loops + Phase 2 appends), detailed loop designs for key loops (C1--C4, B1--B2), noise loops, Phase 2 append designs | 3 |
| `layer3-eval.md` | 30 eval rounds (R1--R30) spread across 12 question types: option tables, correct answers, evidence sources, distractor logic, cross-round reversal matrix, personalization scoring | 4 |
| `layer4-dynamic.md` | 4 updates: action lists (JSON), source file content summaries, runtime checks | 5 |

**Read order:** layer0 -> layer1 -> layer2 -> layer3 -> layer4

---

## 3. Role and Session Table

| Role | Title | Channel | Session Filename | UUID Placeholder | Initial or Update |
|---|---|---|---|---|---|
| -- | -- | main | `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | initial |
| Li Jie (李姐) | MCN Account Manager | 微信 IM | `mcn_lijie_im_{uuid}.jsonl` | `PLACEHOLDER_LIJIE_IM_UUID` | initial (Phase 1) + Update 1 (Phase 2 append) |
| A-Jie (阿杰) | Blogger Friend | 微信 IM | `friend_ajie_im_{uuid}.jsonl` | `PLACEHOLDER_AJIE_IM_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| Mother (周芳母亲) | Family | 微信 IM | `family_mother_im_{uuid}.jsonl` | `PLACEHOLDER_MOTHER_IM_UUID` | initial (Phase 1) + Update 3 (Phase 2 append) |
| Father (周芳父亲) | Family | 电话 | `family_father_phone_{uuid}.jsonl` | `PLACEHOLDER_FATHER_PHONE_UUID` | initial (Phase 1 only) |

**Notes:**
- New Mango Media does NOT have a dedicated session. Their offer is captured in competing-mcn-offer.md.
- Father has no Phase 2 append -- his input is completed in Phase 1.
- 3 of 4 history sessions receive Phase 2 appends through updates. Father phone session has no append.

---

## 4. Quick Contradiction and Bias Table

| ID | Short Description | First Visible Round | Reversal Round |
|---|---|---|---|
| C1 | Revenue share discrepancy: Contract Art 5.1 says "30% MCN share" vs bank records show ~45% effective deduction. Root cause: Art 7.3 hidden fees (8% platform + 7% production = 15%) deducted BEFORE the 30% split. Effective MCN share = 30% + 15% = 45%. | R2 (contract vs bank records visible) | R2->R6 (full resolution: Article 7.3 discovered; contract is opaque but not breached) |
| C2 | Verbal promise unreliability: Li Jie promised "20% next year, fees eliminated" (2026-02-10) vs no written confirmation; renewal offer has same terms; pattern of 3 unfulfilled verbal promises (2024, 2025, 2026). | R3 (verbal vs written visible) | R3->R7 (full resolution: Li Jie's "sign first" response confirms promise is non-binding and leverage-eliminating) |
| C3 | Content output timeline (NON-CONFLICT): 48 videos, engagement 2%->4.5%, revenue ¥20K->¥36K/month, all consistent across analytics, bank records, and MCN reports. Growth trajectory strengthens negotiating leverage. | R1 (persistent synthesis) | None |
| C4 | Competing MCN deception: New Mango offers "15% share, no hidden fees" vs contract fine print has 12-month exclusivity (Art 4.2), brand deal monopoly + 20% commission (Art 6.1), and 50% termination penalty (Art 8.3). Effective cost approaches or exceeds Star Glory's depending on brand deal volume. | R4 (headline vs fine print visible) | R4->R8 (full resolution: hidden clauses quantified; brand commission 5-10% above industry standard; exclusivity costs ~30% cross-platform engagement) |
| B1 | Li Jie IM Phase 1, Loop 4: Agent trusts verbal promise based on guanxi/relationship culture, giving it "meaningful weight" as an "informal guarantee" | R5 (bias visible from Li Jie IM) | Full reversal when "sign first" response shows promise is non-binding + pattern of 3 unfulfilled promises (Update 1) |
| B2 | A-Jie IM Phase 1, Loop 3: Agent dismisses New Mango hidden clauses as "relatively standard in the MCN industry" and frames headline rate as "the key metric" | R8 (bias visible from A-Jie IM) | Full reversal when A-Jie's analysis shows brand commission above benchmark, exclusivity cost quantified, and termination penalty is punitive (Update 3) |

---

## 5. Execution Steps

### Step 0: Confirm Scenario Design

Read all 5 layer files. Record the following:

**Generate 5 UUIDs** (one per session):
```bash
python -c "import uuid; print(uuid.uuid4())"
# Repeat 5 times for: MAIN, LIJIE_IM, AJIE_IM, MOTHER_IM, FATHER_PHONE
```

Record all 5 UUIDs. All subsequent steps replace placeholder names with real UUIDs.

**Checklist:**
- Contradictions: C1 (revenue share: 30% stated vs 45% effective), C2 (verbal promise unreliable), C3 (content timeline -- non-conflict), C4 (competing offer: 15% headline vs hidden clauses)
- Biases: B1 (Li Jie IM Loop 4), B2 (A-Jie IM Loop 3)
- Updates: U1 on R6, U2 on R8, U3 on R11, U4 on R21
- 4 history sessions (3 with Phase 2 appends, 1 phone without append) + 1 main session
- Zhou Fang P1-P5 preferences injected in 4 stages across main session

### Step 1: Create Workspace Files (layer1)

Target directory: `benchmark/data/calmb-new/workspaces/trace_j7/`

Create 5 agent config files first (AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md), then 5 initial scenario files, then add update files to `updates/` subfolder.

### Step 2: Write History Sessions (layer2)

Write 4 history session files. Phase 1 content for all sessions. Phase 2 appends stored in `updates/` subfolders.

Key constraint: B1 exact phrase must appear in mcn_lijie_im Loop 4 agent reply. B2 exact phrase must appear in friend_ajie_im Loop 3 agent reply.

### Step 3: Write Questions File (layer3)

Write `benchmark/data/calmb-new/eval/trace_j7/questions.json` with 30 rounds.

Zhou Fang's P1-P5 preferences are calibrated in R1 (visual format + conclusion first), R2 (data + story), main session messages (lively tone). All subsequent P-I rounds must test compliance.

### Step 4: Write Update Source Files (layer4)

Write 4 update workspace files and 3 session append files in `updates/` subfolder. Verify all update action paths match session UUID placeholders.

### Step 5: Runtime Checks

- [ ] B1 phrase appears verbatim in mcn_lijie_im Loop 4
- [ ] B2 phrase appears verbatim in friend_ajie_im Loop 3
- [ ] C1 sources are independent (mcn-contract-current.md Art 5.1 vs Art 7.3 vs revenue-sharing-records.md vs industry-benchmark-report.md)
- [ ] C2 sources are independent (mcn-verbal-promises-log.md vs mcn-contract-current.md renewal vs lijie-written-response.md)
- [ ] C3 has NO contradictions -- growth metrics consistent across all sources
- [ ] C4 sources show headline 15% vs hidden clauses (Art 4.2, 6.1, 8.3) vs industry benchmarks (brand commission 10-15% standard)
- [ ] All 4 updates have correct action type/path/source fields
- [ ] Zhou Fang P1-P5 preferences injected at correct stage points
- [ ] exec_check rounds constitute 20-40% of total rounds (9/30 = 30%)
- [ ] Financial figures consistent: Gross ¥35K, Art 5.1 = 30%, Art 7.3 = 15% (8%+7%), effective = 45%, net = ¥19,250 (55%); Li Jie promise = 20%; New Mango platform = 15%, brand = 20%, penalty = 50%; industry benchmark = 20-25% for 50K tier
- [ ] Contract articles precisely referenced: Art 5.1 (headline share), Art 7.3 (hidden fees), Art 9.1 (renewal), Art 10.1 (termination); New Mango: Art 3.1 (share), Art 4.2 (exclusivity), Art 6.1 (brand monopoly), Art 8.3 (penalty)
- [ ] Four options clearly distinguished: (1) renew current 45%, (2) renew with written 20% (uncertain), (3) New Mango ~35% effective + restrictions, (4) independent 0% + operational cost
