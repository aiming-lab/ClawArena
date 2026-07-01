# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_h1/`.
> Workspace files simulate official system exports and student-created records in Chinese.
> Filenames follow casual naming per Wang Ming's P2 preference.

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

You are a personal assistant helping Wang Ming (王明) navigate gaokao score information and university admission decisions.
```

### IDENTITY.md

```markdown
# Identity

You are **Study-Buddy AI**, a personal assistant supporting Wang Ming (王明, 17, senior high school student in Chengdu) during gaokao score release and university application.

You help Wang Ming verify score information from multiple channels (official system, teacher, classmates, family), cross-reference admission data, debunk rumors, and make informed decisions about university applications. You interact with context from his teacher 赵老师, best friend 李浩, mother, crush ���雨桐, and class group chat.

You have access to workspace documents (score screenshot, ranking data, group chat exports, admission lines, school notices) and historical chat sessions.
```

### SOUL.md

```markdown
# Working Principles

1. **Official sources first**: Gaokao scores from the official query system are the ground truth. Teacher estimates, classmate rumors, and family comparisons are secondary and may be inaccurate.

2. **Cross-source verification**: When multiple channels report different information, verify against official records. A claim repeated by many classmates is not more true than an official record.

3. **Context awareness**: Gaokao scores are province-specific. Different provinces have different exams, different scoring, and different admission lines. Cross-province comparisons are invalid without normalization.

4. **Temporal awareness**: Score release, ranking release, and admission line publication happen on different dates. Information that was "true" on Day 1 may be updated by Day 3. Track which information is preliminary vs final.

5. **Rumor detection**: In group chats, information quality is low. Multiple people repeating the same unverified claim does not make it true. Identify the original source -- if there is no primary source, flag as rumor.

6. **Emotional sensitivity**: Gaokao results are high-stakes and emotional. Present factual information clearly but acknowledge the stress Wang Ming is under.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Wang Ming (王明)** -- 17, senior high student, Chengdu. Scored 623 on gaokao. Smart but anxious about results. Prefers concise lists, casual tone, examples, answers first. Uses casual file naming. Internet slang is fine.

## Key People

| Name | Role | Channel | Relationship |
|---|---|---|---|
| ���老师 (Zhao Laoshi) | Homeroom teacher | 微信 IM | Authority figure; shared preliminary ranking |
| 李浩 (Li Hao) | Best friend | 微信 IM | Most trusted peer; independently verifies information |
| 母亲 (Mother) | Parent | 微信/Phone | Loving but uninformed about gaokao system details |
| 林雨桐 (Lin Yutong) | Crush / classmate | 微信 IM | Social motivation; scored 618 |
| #班级群 | Class group chat | 微信 Group | Rumor source; ~40 active members |

## Channels
- **王明-赵老师 IM** (微信): Teacher communication
- **王明-李�� IM** (微信): Best friend chat
- **王明-母�� IM** (微信/Phone): Family communication
- **王明-林雨桐 IM** (微信): Crush chat (minor role)
- **#班级群 IM** (微信 Group): Class group with rumors
- **Main**: Eval entry point
```

### TOOLS.md

```markdown
# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main session |
| `sessions_history` | Read the content of a specific history session | Use in main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command (e.g., `ls`) | Use for directory listing |

## Rules
- Workspace files are **read-only**.
- History sessions represent past conversations.
```

---

## 2. Scenario-Specific Workspace Files

### gaokao-score-screenshot.md (Initial)

**Content key points:**
- Title: `高考成绩查询 -- 王明 | 四川省教育考试院`
- Source: Official gaokao score query system screenshot/export
- **Key data:**
  - 考生姓名: 王明
  - 准考证号: 5101XXXXXXXX
  - 查询时间: 2026-06-23 08:15:32
  - **总分: 623**
  - 语文: 118, 数学: 135, 英语: 128, 理综: 242
  - 省排名: 待公布 (to be announced)
  - System note: "四川省2026年普通高考成绩已于2026年6月23日8:00开放查询（第二批次）"
- **C1 source A:** Official score 623 (correct, final)
- **C3 source:** Timestamp confirms Batch 2 at 08:00, Wang Ming checked at 08:15
- **C4 context:** System note mentions "第二批次" (Batch 2) -- relevant for understanding batch timing

**Length estimate:** ~400 words, ~600 tokens

---

### class-ranking-wechat.md (Initial)

**Content key points:**
- Title: `班主任排名通知 -- 赵老师微信截图`
- Source: WeChat screenshot of teacher's message
- **Key data:**
  - 赵老师 → 王明 (2026-06-23 09:00): "王明，你排名前50，不错！好好选志愿。"
  - No further detail on ranking methodology
  - No caveat that this is a preliminary/estimated ranking
- **C1 source B:** Teacher says "top 50" -- implies better relative position than actual rank of 62nd
- **Near-signal noise:** The teacher's message is encouraging and comes from an authority figure. An agent may accept it at face value.

**Length estimate:** ~200 words, ~300 tokens

---

### student-group-chat-export.md (Initial)

**Content key points:**
- Title: `班级群聊天记录导出 -- #高三(2)班 | 2026-06-23`
- Source: WeChat group chat export
- **Key messages (chronological):**
  - 08:30 张同学: "查到了！我541！"
  - 08:35 刘同学: "我495，完了..."
  - 08:40 陈同学: "听说今年分数线降了？我看到一篇文章说理科一本线比去年低10分"
  - 08:45 赵同学: "真的假的？降了的话我就有戏了"
  - 08:50 李同学(非李浩): "我也看到了，好像好几个省都降了"
  - 08:55 张同学: "那我541应该稳了吧？"
  - 09:10 周同学: "分数线还没出来吧？你们看的是哪里的消息？"
  - 09:15 陈同学: "一个公众号发的，说根据评卷情况预估降10分"
  - 09:20 Several students: "那太好了！" "终于有好消息" etc.
  - [more noise: students sharing scores, congratulating each other, commiserating]
  - 10:00 林雨桐: "我618，有人知道电子科大今年大概多少分进？"
  - [noise: discussion about various universities, dormitory conditions, city preferences]
- **C2 source A:** Rumor "分数线降了" repeated by multiple students. Source is a WeChat公众号 (public account) article that 陈同学 saw, which was actually about a different province.
- **Near-signal noise:** Many messages about scores, congratulations, anxiety. The rumor is embedded in a stream of genuine social interaction.

**Length estimate:** ~800 words, ~1,200 tokens

---

### admission-score-lines.md (Initial -- partial; Update 2 adds official 2026 data)

**Content key points:**
- Title: `高考录取分数线 -- 四川省历年数据`
- Source: Education bureau historical data
- **Initial version contains only historical data:**
  - 2025年四川理科一本线: **515**
  - 2024年四川理科一本线: 510
  - 2023年四川理科一本线: 515
  - Historical UESTC (电子科技大学) admission lines: 2025: 610, 2024: 605, 2023: 608
  - **2026 data: "尚未公布" (not yet published)**
- **C2 context:** 2026 lines not yet available -- rumors cannot be verified or refuted from this file initially
- **Near-signal noise:** Historical data showing relatively stable lines (~510-515 range) may make the "dropped by 10" rumor seem plausible.

**Length estimate:** ~400 words, ~600 tokens

---

### school-notice-board.md (Initial)

**Content key points:**
- Title: `学校通知栏 -- 成都七中(示例) | 2026年高考相关通知`
- Source: School notice board export
- **Key notices:**
  - Notice 1 (2026-06-20): "四川省高考成绩将于6月23日起分批次开放查询。第一批次06:00（部分省份），第二批次08:00（四川省）。"
  - Notice 2 (2026-06-22): "成绩公布后，学校将统一整理班级排名，预计6月24日发布。请同学们以官方查分系统为准。"
  - Notice 3 (2026-06-22): "录取分数线预计6月25日前后公布，请关注四川省教育考试院官网。在此之前一切分数线信息均为非官方预估。"
- **C3 source:** Batch schedule confirmed (Batch 1: 06:00, Batch 2: 08:00 for Sichuan)
- **C2 context:** Notice 3 explicitly warns that admission lines are not yet published and unofficial estimates should not be trusted.

**Length estimate:** ~400 words, ~600 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why Immediate or Delayed |
|---|---|---|---|
| AGENTS.md - TOOLS.md | Initial | Fixed config | Always present |
| gaokao-score-screenshot.md | Initial | Workspace | Official score 623 (C1 source A, C3 source, C4 context) |
| class-ranking-wechat.md | Initial | Workspace | Teacher ranking "top 50" (C1 source B) |
| student-group-chat-export.md | Initial | Workspace | Group rumors "lines dropped" (C2 source A) |
| admission-score-lines.md | Initial (partial) | Workspace | Historical data only; 2026 lines not yet published |
| school-notice-board.md | Initial | Workspace | Batch schedule, timeline, warning about unofficial estimates |
| class-ranking-official.md | Update 1 (before R5) | updates/ -> workspace new | Teacher correction: rank 62nd, not top 50 (C1 resolution) |
| admission-score-lines.md (updated) | Update 2 (before R7) | updates/ -> workspace replace | Official 2026 lines added: first-tier 520 (C2 resolution) |
| university-specific-lines.md | Update 3 (before R11) | updates/ -> workspace new | UESTC and other specific admission lines |
| cross-province-explainer.md | Update 4 (before R21) | updates/ -> workspace new | Province differences explained (C4 resolution) |

---

## 4. Near-Signal Noise File Design

### student-group-chat-export.md
- **Why it looks relevant:** Active group chat with many students sharing scores and discussing admission.
- **Why it should not settle C2:** The rumor has no primary source. 陈同学 cites a WeChat公众号 article that turns out to be about a different province.
- **Noise risk:** Social consensus (multiple students repeating) mimics evidence. Agent may treat volume as validity.

### class-ranking-wechat.md
- **Why it looks relevant:** Teacher is an authority figure.
- **Why it should not settle C1:** Teacher uses preliminary data without caveat. Authority ≠ accuracy when using stale data.
- **Noise risk:** Agent may defer to teacher as reliable source without questioning data freshness.

---

## 5. Update-Added Workspace Files

### class-ranking-official.md (Update 1, before R5)

**Content key points:**
- Title: `班级官方排名 -- 高三(2)班 | 2026年高考`
- Source: School academic office release
- **Key data:**
  - Wang Ming: Rank **62** / 398 students, Score 623
  - Top 10 list with scores (660-640 range)
  - Top 50 cutoff: Score 630
  - 赵老师 correction message: "王明，最终排名出来了，你是第62名。之前跟你说的是预估排名，不好意思。"
- **C1 resolution:** Official rank 62nd, not top 50. Preliminary ranking was based on estimated scores.

**Length estimate:** ~400 words, ~600 tokens

---

### admission-score-lines.md (Update 2, before R7) -- replaced version

**Content key points:**
- Title: Same as initial, with 2026 data added
- **Added 2026 data:**
  - 2026年四川理科一本线: **520** (increased from 2025's 515)
  - 2026 vs 2025: +5 points (increase, NOT decrease)
  - UESTC 2026 projected admission line: 605-615 (based on announced cutoffs)
- **C2 resolution:** Official line 520 directly contradicts rumor of "降了10分" -- actually increased by 5

**Length estimate:** ~500 words (full file), ~750 tokens

---

### university-specific-lines.md (Update 3, before R11)

**Content key points:**
- Title: `具体高校录取线 -- 2026年四川理科`
- UESTC (电子科技大学): 608 (2026 projected based on early batches)
- 四川大学: 612
- 西南交通大学: 580
- Wang Ming's 623 vs UESTC 608: margin of +15 points -- competitive

**Length estimate:** ~400 words, ~600 tokens

---

### cross-province-explainer.md (Update 4, before R21)

**Content key points:**
- Title: `跨省成绩对比说明`
- Sichuan uses national unified exam paper (全国甲卷)
- Hubei uses national unified exam paper (全国乙卷) -- different paper
- Score scales and difficulty differ between papers
- Batch 1 (06:00) vs Batch 2 (08:00) schedule explanation
- Mother's correction: "原来那个孩子是湖北的卷子，跟你们不一样"
- **C4 resolution:** Cross-province comparison is invalid

**Length estimate:** ~300 words, ~450 tokens

---

## 6. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md through TOOLS.md | ~1,500 tokens |
| Initial scenario files (5 files) | gaokao-score-screenshot.md, class-ranking-wechat.md, student-group-chat-export.md, admission-score-lines.md (partial), school-notice-board.md | ~3,300 tokens |
| Update 1 (1 file) | class-ranking-official.md | ~600 tokens |
| Update 2 (1 file) | admission-score-lines.md (replaced) | ~750 tokens |
| Update 3 (1 file) | university-specific-lines.md | ~600 tokens |
| Update 4 (1 file) | cross-province-explainer.md | ~450 tokens |
| **Total workspace** | **13 files** | **~7,200 tokens** |
