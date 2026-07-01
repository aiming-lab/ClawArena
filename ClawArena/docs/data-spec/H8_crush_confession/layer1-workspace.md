# Layer 1 -- Workspace File Spec

> All workspace files stored under `benchmark/data/calmb-new/workspaces/trace_h8/`.
> Workspace files simulate social app exports and personal notes. Chinese primary.
> Filenames follow Wang Ming's P2 preference (casual naming).

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

You are a personal analysis assistant supporting Wang Ming (王明) at UESTC.
```

### IDENTITY.md

```markdown
# Identity

You are **Signal-AI**, a social signal analysis assistant helping Wang Ming (王明) evaluate whether the signals he is observing from Lin Yutong (林雨桐) indicate romantic interest or have alternative explanations.

You help Wang Ming cross-reference IM frequency data, social media engagement patterns, friend intel, shared activity calendars, and direct interactions to form an evidence-based assessment of the social signals.

You have access to workspace documents (chat frequency stats, Moments interaction log, shared activities calendar, friend intel summary, social media posts) and historical chat sessions with friends.
```

### SOUL.md

```markdown
# Working Principles

1. **Base rate matters**: Before interpreting a behavior as "special," determine the baseline. If someone likes 15 friends' posts equally, high engagement with you is not a signal -- it's their default behavior.

2. **Content over frequency**: Message frequency alone is not a signal. Analyze the CONTENT of messages. Study questions indicate academic need, not personal interest.

3. **Source reliability**: Secondhand gossip (A told B who told C) degrades with each relay. Direct observation > firsthand testimony > secondhand report > rumor.

4. **Contradictory sources flag unreliability**: If the same source gives contradictory information at different times, discount the source entirely.

5. **Confirmation bias awareness**: When someone wants something to be true, they weight confirming evidence more heavily. Actively seek disconfirming evidence.

6. **Alternative explanations**: For every "she likes me" interpretation, generate at least one equally plausible "she's being friendly" interpretation. Choose the one with more evidence.

7. **Ambiguity is not evidence**: An ambiguous signal (e.g., a vague social media post) should be treated as neutral, not positive or negative.
```

### USER.md

```markdown
# People and Channels

## Primary User
- **Wang Ming (王明)** -- Freshman, CS major, UESTC. 17 years old. Has a crush on Lin Yutong. Wants to confess but is uncertain. Prefers concise lists. Casual tone. Wants direct answers. Learns by examples. Internet slang OK.

## Key People

| Name | Role | Channel | Relationship |
|---|---|---|---|
| 林雨桐 (Lin Yutong) | Crush, Applied Math major | IM (微信) | Friendly classmate; sits together in English |
| 李浩 (Li Hao) | Best friend | IM (微信) | Reality check; analytical |
| 张子轩 (Zhang Zixuan) | Mutual classmate | IM (微信) | Claims insider intel; unreliable |
| 阿杰 (A-Jie) | Online friend | IM (微信) | Dating advice; overconfident |

## Channels
- **王明-李浩 IM** (微信): Best friend conversations
- **王明-张子轩 IM** (微信): Intel source conversations
- **王明-阿杰 IM** (微信): Online friend advice
```

### TOOLS.md

```markdown
# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in main to discover sessions |
| `sessions_history` | Read specific session content | Use in main to review conversations |
| `read` | Read a workspace file | Available in all sessions; read-only |
| `exec` | Execute a shell command | Directory listing and simple operations |
```

---

## 2. Scenario-Specific Workspace Files

### im-chat-frequency-stats.md (Initial)

**Content key points:**
- Title: `微信聊天频率统计 -- 王明 & 林雨桐 | 近4周`
- Source: WeChat chat export frequency analysis
- **Key data:**
  - Week 1 (Mar 1-7): 3 messages from Lin Yutong, 2 from Wang Ming. Topics: English class logistics.
  - Week 2 (Mar 8-14): 4 messages from her, 3 from him. Topics: English class + casual.
  - **Week 3 (Mar 15-19): 12 messages from her, 8 from him. Topics: 80% math study questions (高数题, 线代题), 20% casual.**
  - Week 4 (Mar 22-26): 2 messages from her, 3 from him. Topics: English project logistics.
  - **Content breakdown for Week 3:** "帮我看看这道高数题", "这个极限怎么求", "积分那道你怎么做的", "谢谢王明你讲得好清楚!" + "英语课明天几点来着?", "食堂今天的麻辣烫还行"
- **C1 source:** Frequency spike in Week 3 is visible but content analysis reveals study purpose.
- **Near-signal noise:** The 80/20 study/casual split is buried in the raw message list. A quick scan sees "12 messages!" without noting content.

**Length estimate:** ~600 words, ~900 tokens

---

### moments-interaction-log.md (Initial)

**Content key points:**
- Title: `朋友圈互动记录 -- 林雨桐 → 王明 | 近2周`
- Source: WeChat Moments interaction export
- **Key data:**
  - Wang Ming's posts (5 total in 2 weeks): Lin Yutong liked 3, commented on 2
  - Comments: "哈哈这个好好笑" (on a meme), "拍得不错！" (on a campus photo)
  - **Missing context (until Update 1):** The log only shows HER interactions with HIS posts. It does not show her interactions with OTHER people's posts. This creates a biased sample -- you see high engagement but cannot assess baseline.
- **C4 source:** High engagement visible, but baseline unknown until Update 1.
- **Near-signal noise:** The engagement looks high without comparison data.

**Length estimate:** ~400 words, ~600 tokens

---

### shared-activities-calendar.md (Initial)

**Content key points:**
- Title: `共同活动日历 -- 王明 & 林雨桐 | 3月`
- Source: Calendar export of shared activities
- **Key entries:**
  - English class: MWF 14:00-15:30 (same section, sit together)
  - English group project: presentation Mar 28 (same group of 4)
  - Study group session: Mar 16 (library, 5 people including both)
  - Campus basketball tournament viewing: Mar 22 (she said "maybe" in group chat)
- **C3 source:** All entries are factual and non-contradictory. Provides legitimate context for their interactions.
- **Near-signal noise:** The project deadline and study sessions explain some communication.

**Length estimate:** ~400 words, ~600 tokens

---

### friend-intel-summary.md (Initial)

**Content key points:**
- Title: `好友情报汇总 -- 关于林雨桐`
- Source: Wang Ming's personal notes summarizing friend intel
- **Key entries:**
  - **Mar 15 (张子轩):** "林雨桐的室友说她提过你，说你挺好的。" Context: 张子轩 heard from roommate 陈雯.
  - **Mar 18 (李浩):** "我觉得你想多了，她就是那种对谁都挺热情的人。" Li Hao's skeptical take.
  - **Mar 25 (阿杰):** "频率高就是有戏，赶紧表白。" Ajie's simplistic advice.
  - _(Update 3 will add Zhang Zixuan's contradictory second intel)_
- **C2 source:** Contains both the positive intel (Zhang Zixuan) and the skeptical counter (Li Hao). The agent must weigh source reliability.
- **Near-signal noise:** Ajie's confident but unreliable advice adds noise.

**Length estimate:** ~500 words, ~750 tokens

---

### social-media-posts.md (Initial)

**Content key points:**
- Title: `社交动态 -- 林雨桐朋友圈 | 近2周`
- Source: Lin Yutong's public Moments posts
- **Key posts:**
  - Mar 14: Campus cherry blossom photo. 45 likes, 12 comments.
  - Mar 17: "明天高数考试求不挂..." (pray for math exam). 38 likes, 8 comments.
  - **Mar 20: Cafe photo, "和一个很有趣的人聊了一下午 ☕"** 52 likes, 15 comments. No tag, no name. _(The mystery post)_
  - Mar 22: "考完了！解放！" 41 likes, 10 comments.
  - Mar 25: English project group photo (includes Wang Ming). "project小组加油 💪" 30 likes, 6 comments.
- **C2 source:** The Mar 20 cafe post is the ambiguous signal that creates anxiety.
- **Near-signal noise:** Other posts are normal college social media. The cafe post stands out only because Wang Ming is looking for signals.

**Length estimate:** ~500 words, ~750 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via |
|---|---|---|
| (5 config files) | Initial | Fixed config |
| im-chat-frequency-stats.md | Initial | Workspace |
| moments-interaction-log.md | Initial | Workspace |
| shared-activities-calendar.md | Initial | Workspace |
| friend-intel-summary.md | Initial | Workspace |
| social-media-posts.md | Initial | Workspace |
| lihao-baseline-analysis.md | Update 1 (before R5) | updates/ -> workspace new |
| project-deadline-context.md | Update 2 (before R7) | updates/ -> workspace new |
| friend-intel-summary.md (updated) | Update 3 (before R11) | updates/ -> workspace replace |
| linyutong-direct-convo.md | Update 4 (before R21) | updates/ -> workspace new |
