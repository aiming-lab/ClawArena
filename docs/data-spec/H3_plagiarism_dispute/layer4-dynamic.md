# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver TA's side-by-side git comparison -- corroborates timeline, seeds common-source hypothesis | No | Yes: ta-git-comparison-notes.md | R2->R5 intermediate (timeline confirmed + common source hinted) |
| U2 | Before R6 | Deliver SO answer discovery -- resolves C1 and C2 via C3 common-source explanation, triggers B1 reversal | Yes: Li Hao IM Phase 2 append | Yes: stackoverflow-answer-screenshot.md (full replacement) | R2->R6 (C1/C2 resolved via C3); B1 reversal |
| U3 | Before R11 | Deliver Chen Wei's admission and narrative shift -- corroborates C3 from the accused party | Yes: Chen Wei IM Phase 2 append | No | Corroborates C3; extends C2 resolution |
| U4 | Before R21 | Deliver TA resolution email and group reaction -- triggers C4 full reversal and B2 correction | Yes: TA Email Phase 2 append, CS101群 Phase 2 append | Yes: ta-resolution-email.md | R8->R11 (C4: zero tolerance not applied literally); B2 reversal |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Introduces the TA's side-by-side git comparison notes. The TA confirms Wang Ming's earlier timeline and, critically, observes the shared `prev_node`/`curr_node`/`next_temp` naming pattern that is "not textbook standard" -- seeding the common-source hypothesis. This corroborates the timeline evidence and prepares the agent for the SO discovery in Update 2.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "ta-git-comparison-notes.md",
    "source": "updates/ta-git-comparison-notes.md"
  }
]
```

### Update 2 (before R6)

**Trigger timing:** After R5 answer is submitted, before R6 question is injected.
**Purpose:** Replaces the SO placeholder with the full Stack Overflow answer screenshot, and appends Li Hao's IM Phase 2 content where he discovers the SO answer and shares it with Wang Ming. This is the key turning point: the SO answer explains the 95% similarity as common-source reference, not inter-student plagiarism. The agent must revise B1 ("Chen Wei likely copied Wang Ming") to "both independently referenced SO #48291037." This update resolves C1 and C2 simultaneously via C3.

```json
[
  {
    "type": "workspace",
    "action": "replace",
    "path": "stackoverflow-answer-screenshot.md",
    "source": "updates/stackoverflow-answer-screenshot.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LIHAO_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LIHAO_IM_UUID.jsonl"
  }
]
```

### Update 3 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** Appends Chen Wei's IM Phase 2 content where he implicitly admits referencing the SO answer ("那个prev_node的写法确实是从那学的") and shifts his narrative from accusation to deflection. This corroborates the C3 common-source explanation from the accused party's own admission and shows Chen Wei's narrative evolution.

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CHENWEI_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_CHENWEI_IM_UUID.jsonl"
  }
]
```

### Update 4 (before R21)

**Trigger timing:** After R20 answer is submitted, before R21 question is injected.
**Purpose:** Introduces the TA's resolution email (warning, not zero grade) and appends the TA Email Phase 2 content (resolution + TA's policy explanation) and CS101群 Phase 2 content (group reaction to the resolution). This triggers C4 full reversal: the "zero tolerance" policy text is not applied literally. The TA's distinction between Section 4.2 (plagiarism) and Section 4.3 (citation) is the key reasoning. B2 ("prepare for a zero grade") is definitively corrected.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "ta-resolution-email.md",
    "source": "updates/ta-resolution-email.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_TA_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_TA_EMAIL_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CS101_GROUP_UUID.jsonl",
    "source": "updates/PLACEHOLDER_CS101_GROUP_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/ta-git-comparison-notes.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C2 (corroboration), C3 (seeds common-source hypothesis)
**Content key points:**
- Title: "助教 Git 对比笔记 -- 王明 vs 陈伟 提交时间线分析"
- Author: Zhang Hao (TA), D5
- Side-by-side timeline: Wang Ming first commit D-2 14:22 vs Chen Wei first GitLab commit D-1 20:00 (30-hour gap)
- Chen Wei GitHub push D1 22:30 is 56+ hours after Wang Ming's first commit
- Observes shared `prev_node`/`curr_node`/`next_temp` naming convention
- Key TA note: "这组变量命名不是教材标准写法" (not textbook standard naming)
- Suspects "共同参考来源" (common reference source) but has not identified it yet
- Interim conclusion: timeline favors Wang Ming; naming pattern requires further investigation

**Length estimate:** ~400 words, ~600 tokens

---

### updates/stackoverflow-answer-screenshot.md (Update 2)

**File type:** workspace replace (replaces initial placeholder)
**Associated contradictions:** C3 (definitive evidence), C1 resolution, C2 resolution
**Content key points:**
- Title: "Stack Overflow Answer Screenshot -- Question #48291037"
- SO Question: "How to reverse a singly linked list in Python using iterative approach?"
- Accepted answer by "algo_master_42", posted 2 years ago, 847 upvotes
- Code uses exact same `prev_node`/`curr_node`/`next_temp` naming convention
- Three-pointer iterative technique matches both students' `reverse_linked_list()` implementations
- The SO answer explains ~85% of the structural similarity flagged by MOSS
- This is the common source that resolves the "who copied whom" question

**Length estimate:** ~350 words, ~525 tokens

---

### updates/PLACEHOLDER_LIHAO_IM_UUID.jsonl (Update 2)

**File type:** session append (continues friend_lihao_im session)
**Associated contradictions:** C3 (discovery moment), B1 (reversal trigger)
**Content key points:**
- Loops 13-16 of Li Hao's IM with Wang Ming
- Loop 13: Li Hao discovers SO #48291037 by searching "linked list reversal three pointer." Wang Ming confirms this is the answer he referenced. Key reframe: "你们俩都是从SO上抄的" (both of you copied from SO)
- Loop 14: Li Hao advises forwarding the SO link to the TA immediately
- Loop 15: Discussion about citation requirements -- Wang Ming realizes he should have cited SO
- Loop 16: Li Hao reassures Wang Ming that citation violation is much less serious than plagiarism
- Must continue session_id PLACEHOLDER_LIHAO_IM_UUID and maintain Li Hao's voice (casual, supportive, over-confident but ultimately helpful)

**Length estimate:** ~600 words, ~900 tokens

---

### updates/PLACEHOLDER_CHENWEI_IM_UUID.jsonl (Update 3)

**File type:** session append (continues opponent_chenwei_im session)
**Associated contradictions:** C3 (corroboration from accused party), C2 (narrative shift)
**Content key points:**
- Loops 11-13 of Chen Wei's IM with Wang Ming
- Loop 11: Wang Ming shares the SO discovery. Chen Wei implicitly admits: "那个prev_node的写法确实是从那学的" (the prev_node writing style was indeed learned from that). This is the accused party confirming the common-source explanation
- Loop 12: Chen Wei shifts narrative from "you copied me" to "这种公开的算法谁都会写一样的" (everyone writes this kind of public algorithm the same way). Deflection, not apology
- Loop 13: Both agree to explain the SO connection to the TA
- Must continue session_id PLACEHOLDER_CHENWEI_IM_UUID and maintain Chen Wei's voice (aggressive->deflective, never apologizes)

**Length estimate:** ~400 words, ~600 tokens

---

### updates/ta-resolution-email.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C4 (full reversal -- warning not zero), B2 (definitive reversal)
**Content key points:**
- Title: "助教通知 -- CS101 作业3 查重案件处理结果"
- Author: Zhang Hao (TA), D9
- Resolution: (1) similarity from common SO reference, not inter-student plagiarism; (2) both students violated Section 4.3 (uncited reference); (3) first-offense formal warning, no grade penalty; (4) future violations will follow zero-tolerance strictly
- Cc: Professor Liu
- This directly contradicts B2's "prepare for a zero grade" assessment
- The TA's distinction: Section 4.2 (plagiarism) vs Section 4.3 (citation violation)

**Length estimate:** ~350 words, ~525 tokens

---

### updates/PLACEHOLDER_TA_EMAIL_UUID.jsonl (Update 4)

**File type:** session append (continues ta_zhanghao_email session)
**Associated contradictions:** C4 (TA's explicit reasoning), B2 (reversal)
**Content key points:**
- Loops 9-11 of TA email session
- Loop 9: Zhang Hao delivers the formal resolution email (see ta-resolution-email.md)
- Loop 10: Wang Ming thanks the TA and commits to proper citation
- Loop 11: Zhang Hao explains his reasoning: "学院政策确实写的零容忍，但这种情况不算同学间抄袭" (policy says zero tolerance, but this situation does not count as inter-student plagiarism). This is the explicit C4 policy interpretation
- Must continue session_id PLACEHOLDER_TA_EMAIL_UUID and maintain Zhang Hao's voice (formal, fair, procedural)

**Length estimate:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_CS101_GROUP_UUID.jsonl (Update 4)

**File type:** session append (continues cs101_group_im session)
**Associated contradictions:** C4 (social reaction to policy interpretation)
**Content key points:**
- Loops 13-16 of #CS101群 group chat
- Loop 13: Resolution leaks -- students learn about the warning. Some question: "不是说零容忍吗" (isn't it supposed to be zero tolerance?)
- Loop 14: Policy debate -- 同学G defends TA's decision; 同学F reads policy literally; 同学H astutely identifies the 4.2 vs 4.3 distinction
- Loop 15: Wang Ming makes a brief public statement ("谢谢大家关心 事情解决了")
- Loop 16: Group returns to normal topics
- Must continue session_id PLACEHOLDER_CS101_GROUP_UUID and maintain the group's voice (mixed opinions, speculative, some astute observations)

**Length estimate:** ~500 words, ~750 tokens

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
  - Update 2 appends to PLACEHOLDER_LIHAO_IM_UUID (friend_lihao_im session)
  - Update 3 appends to PLACEHOLDER_CHENWEI_IM_UUID (opponent_chenwei_im session)
  - Update 4 appends to PLACEHOLDER_TA_EMAIL_UUID (ta_zhanghao_email session)
  - Update 4 appends to PLACEHOLDER_CS101_GROUP_UUID (cs101_group_im session)
- [x] All workspace files have content descriptions in layer1
  - ta-git-comparison-notes.md: layer1 Section 5, Update 1
  - stackoverflow-answer-screenshot.md (full): layer1 Section 5, Update 2
  - ta-resolution-email.md: layer1 Section 5, Update 4
- [x] Updates support intended reversals
  - U1 -> C2 corroboration (R2->R5 intermediate): TA confirms timeline
  - U2 -> C1/C2 resolution via C3 (R2->R6): SO explains similarity
  - U3 -> C3 corroboration: Chen Wei admits SO reference
  - U4 -> C4 reversal (R8->R11): warning not zero; B2 reversal
- [x] Session filenames use consistent PLACEHOLDER format
  - PLACEHOLDER_LIHAO_IM_UUID, PLACEHOLDER_CHENWEI_IM_UUID, PLACEHOLDER_TA_EMAIL_UUID, PLACEHOLDER_CS101_GROUP_UUID
- [x] Figures are internally consistent
  - Similarity: 95% (MOSS report) across all references
  - Wang Ming first commit: D-2 14:22 (consistent across git history, TA notes, all sessions)
  - Chen Wei first GitLab commit: D-1 20:00 (consistent)
  - Chen Wei GitHub push: D1 22:30 (consistent)
  - SO answer: #48291037, 847 upvotes, 2 years old (consistent)
  - SO-to-student similarity: ~85% (consistent between TA notes and SO analysis)
  - Policy: zero tolerance (Section 4.2) vs citation norms (Section 4.3)
  - Resolution: first-offense warning, no grade penalty (consistent)

---

## 5. questions.json Complete Update Fields Reference

### R5 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "ta-git-comparison-notes.md", "source": "updates/ta-git-comparison-notes.md" }
]
```

### R6 update field:
```json
"update": [
  { "type": "workspace", "action": "replace", "path": "stackoverflow-answer-screenshot.md", "source": "updates/stackoverflow-answer-screenshot.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LIHAO_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_LIHAO_IM_UUID.jsonl" }
]
```

### R11 update field:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CHENWEI_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_CHENWEI_IM_UUID.jsonl" }
]
```

### R21 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "ta-resolution-email.md", "source": "updates/ta-resolution-email.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_TA_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_TA_EMAIL_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CS101_GROUP_UUID.jsonl", "source": "updates/PLACEHOLDER_CS101_GROUP_UUID.jsonl" }
]
```
