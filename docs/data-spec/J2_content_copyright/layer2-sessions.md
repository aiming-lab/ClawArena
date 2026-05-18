# Layer 2 -- Session Content Design

> Sessions under `benchmark/data/calmb-new/openclaw_state/agents/trace_j2/sessions/`.
> Dialogue in Chinese (simplified). 周芳 style: lively, expressive, but fact-focused when needed.

---

## Session Roster

| Session Filename | Session ID Placeholder | Type | Participant(s) | Phase(s) |
|---|---|---|---|---|
| `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | Main | -- | Eval entry point |
| `zhoufang_laowang_wechat_{uuid}.jsonl` | `PLACEHOLDER_LAOWANG_WECHAT_UUID` | DM / WeChat | 摄影师老王 | Phase 1 + Phase 2 (Update 3 append) |
| `zhoufang_lijie_wechat_{uuid}.jsonl` | `PLACEHOLDER_LIJIE_WECHAT_UUID` | DM / WeChat | 李姐 (MCN) | Phase 1 |
| `zhoufang_platform_email_{uuid}.jsonl` | `PLACEHOLDER_PLATFORM_EMAIL_UUID` | DM / Email | 平台客服 | Phase 1 + Phase 2 (Update 1 append) |
| `zhoufang_roommate_wechat_{uuid}.jsonl` | `PLACEHOLDER_ROOMMATE_WECHAT_UUID` | DM / WeChat | 大学室友 | Phase 1 + Phase 2 (Update 4 append) |

---

## Main Session Design

**Loop 0:**

User message:
```
你是周芳的内容版权维权助手 (CreatorGuard AI)。周芳是上海的美食旅行博主（小红书+B站）。

核心情况：周芳2月15日10点发布了一条"花园里"法式餐厅探店视频，同日15点另一个博主"美食小K"发布了几乎一样的内容。美食小K声称"巧合"。摄影师对比显示95%角度相似。

历史会话：
- `PLACEHOLDER_LAOWANG_WECHAT_UUID` -- 摄影师老王（微信）
- `PLACEHOLDER_LIJIE_WECHAT_UUID` -- 李姐，MCN（微信）
- `PLACEHOLDER_PLATFORM_EMAIL_UUID` -- 平台客服（邮件）
- `PLACEHOLDER_ROOMMATE_WECHAT_UUID` -- 大学室友（微信）

请综合会话和workspace文件回答问题。先运行 exec ls。
```

**Preference injection Stage 1:** "输出活泼一点，先说结论再展开，数据和故事结合。"

---

## Session 1: 周芳--摄影师老王 WeChat DM (Technical Expert)

**Phase 1 content (10 loops: 5 key + 5 noise)**

**Loop 1: 老王 delivers comparison [C2 evidence]**
- User (周芳): "[微信 周芳 Tue W1D2 10:00:00 CST 2026] 老王，你看了美食小K的视频吗？是不是太像了？"
- User (老王): "[微信 老王 Tue W1D2 11:00:00 CST 2026] 我做了专业对比。6道菜品拍摄角度完全一致，95%相似。3个装潢角度一致。运镜路线也一样——从门口到吧台到座位到甜品台。这不可能是巧合。"

**Loop 2: Technical detail [C2 depth]**
- User (老王): "[微信 老王 Tue W1D2 14:00:00 CST 2026] 我出了一份详细对比报告。每个镜头我都标了角度和构图对应。同一家餐厅可以有无限种拍法，但他们连'哪道菜放前景、用什么景深'都一样。这是参考拍摄，不是独立创作。"

**Loop 3: 美食小K's defense [C2 Source A]**
- User (周芳): "[微信 周芳 Wed W1D3 10:00:00 CST 2026] 美食小K说是巧合——'同一家餐厅，同样的招牌菜，拍出来当然像'。她说2月12号去的。"
- User (老王): "[微信 老王 Wed W1D3 10:30:00 CST 2026] 巧合？那我问你，为什么连运镜路线都一样？从门口开始，经过吧台，到座位，最后甜品台。这是你的独特创意路线，不是餐厅的标准动线。"

**Loop 4: Reservation date observation [C3 context]**
- User (周芳): "[微信 周芳 Fri W1D5 10:00:00 CST 2026] 我查了预约记录。我2月10号去的，她2月12号去的。不同日期。但这反而说明不是'同一天同一桌'。那为什么拍出来一模一样？"

**Loop 5: Agent assessment [B1 loop -- must contain exact B1 phrase]**
- Agent reply: **Exact B1 phrase:** "The 95% angle similarity is notable but not conclusive on its own -- when two creators visit the same restaurant featuring the same signature dishes and architectural highlights, a high degree of visual similarity in their content is expected, and the 5-hour publication gap could reflect independent parallel creation rather than copying."
- **B1 bias embedded here.**

**Loops 6-10: Noise** (equipment discussion, other restaurant recommendations, upcoming shooting schedule, editing software tips, Instagram vs 小红书 algorithm)

---

**Phase 2 content (Update 3 append -- before R8): 2 loops**

**Loop 11: 老王 discovers scene element evidence [C4 strengthening]**
- User (老王): "[微信 老王 Wed W2D3 10:00:00 CST 2026] 周芳，我发现了更关键的证据。美食小K视频的第3和第7镜头里，桌上的花瓶位置和餐巾折法跟你的完全一样。我问了餐厅，他们说每桌的摆设每天都不同。"
- Agent reply: Notes daily-changing props matching = either direct copying or deliberate scene recreation.

**Loop 12: 老王 assessment [technical conclusion]**
- User (老王): "[微信 老王 Wed W2D3 11:00:00 CST 2026] 结合元数据（相同相机参数）、角度对比（95%）和场景元素（每天不同的花瓶和餐巾），我的专业判断是：美食小K的视频是参考你的视频后有计划地翻拍的。"

---

## Session 2: 周芳--平台客服 Email (Platform -- Bureaucratic)

**Phase 1 content (6 loops: 2 key + 4 noise)**

**Loop 1: 周芳 submits complaint [context]**
- User (周芳): "[邮件 周芳 Thu W1D4 10:00:00 CST 2026] 我要举报小红书笔记 XHS-20260215-MK-FLR 抄袭我的笔记 XHS-20260215-ZF-FLR。附件：发布时间对比、内容相似度分析报告。"

**Loop 2: Platform response [C4 Source A seed]**
- User (平台客服): "[邮件 平台客服 Mon W2D1 10:00:00 CST 2026] 您好，经审核，两条内容存在相似之处，但无法认定为直接抄袭。相似可能源于同一拍摄场所。建议双方协商解决。"

**Loops 3-6: Noise + Loop 4 B2**

**Loop 4: Agent assessment [B2 loop -- must contain exact B2 phrase]**
- Agent reply: **Exact B2 phrase:** "The platform's assessment that visual similarity alone is insufficient to establish copyright infringement has a reasonable basis -- content platforms must balance creator protection with the risk of false takedowns, and without clear evidence of direct copying (such as identical audio, watermarks, or frame-by-frame matches), similarity in restaurant review content may not meet the threshold for actionable infringement."
- **B2 bias embedded here.**

---

## Session 3: 周芳--李姐 MCN DM / Session 4: 周芳--大学室友 DM

**Session 3:** Li Jie provides MCN perspective (mostly noise, some advice on legal options).

**Session 4 Phase 2 (Update 4 append -- before R21): 2 loops**

**Loop 7: 室友 discovers prior complaint [pattern evidence]**
- User (室友): "[微信 室友 Fri W2D5 14:00:00 CST 2026] 周芳！我发现美食小K三个月前也被一个叫'吃货阿明'的博主指控过翻拍日料店视频。微博上有讨论帖截图，但原帖已经被删了。"
- Agent reply: Notes prior complaint pattern.

**Loop 8: 室友 provides details [corroboration]**
- User (室友): "[微信 室友 Fri W2D5 14:30:00 CST 2026] 吃货阿明当时也发了角度对比截图，相似度也很高。后来帖子被删了，不知道是不是被公关了。美食小K可能有翻拍的惯性行为。"
