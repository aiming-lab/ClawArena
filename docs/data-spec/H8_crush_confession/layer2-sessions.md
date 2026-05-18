# Layer 2 -- Session Content Design

> Session messages in Chinese. Agent replies in English.
> Wang Ming's style: casual, earnest, sometimes anxious, uses internet slang.

---

## Session Roster

| Session Filename | Session ID Placeholder | Type | Participant(s) | Phase(s) |
|---|---|---|---|---|
| `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | Main | -- | Eval entry point |
| `lihao_im_{uuid}.jsonl` | `PLACEHOLDER_LIHAO_IM_UUID` | DM / 微信 | 李浩 (Li Hao, best friend) | Phase 1 + Phase 2 (Update 1 append) |
| `zhangzixuan_im_{uuid}.jsonl` | `PLACEHOLDER_ZHANGZIXUAN_IM_UUID` | DM / 微信 | 张子轩 (Zhang Zixuan, intel source) | Phase 1 + Phase 2 (Update 3 append) |
| `ajie_im_{uuid}.jsonl` | `PLACEHOLDER_AJIE_IM_UUID` | DM / 微信 | 阿杰 (A-Jie, online friend) | Phase 1 (initial only) |

---

## Main Session Design

**Loop 0:** User provides context about Wang Ming's crush on Lin Yutong and asks AI to analyze the signals from available data.

**Preference injection Stage 1 (before R1):** "直接告诉我结论，她到底对我有没有意思？列个清单分析一下。"

---

## Session 1: Wang Ming--Li Hao IM (Best Friend / Reality Check)

**Session meta:**
- channel: 微信 IM
- participant: 李浩 (Li Hao)
- session_id: `PLACEHOLDER_LIHAO_IM_UUID`
- Time range: Mar 18-22 (Phase 1), Mar 22 (Phase 2 append via Update 1)

**Phase 1 content (10 loops: 5 key + 5 noise)**

**Loop 1: Wang Ming tells Li Hao about frequency increase**
- User (Li Hao): "[微信 李浩 Wed Mar 18 20:00 CST 2026] 你说林雨桐最近给你发消息多了？让我看看...哥们，你把聊天记录给我看看。"
- Agent tool call: read im-chat-frequency-stats.md
- Agent reply: Reviews frequency data. Notes the increase from 3 to 12 messages per week.

**Loop 2: Li Hao points out content is study-related**
- User (Li Hao): "[微信 李浩 Wed Mar 18 20:15 CST 2026] 我看了你们的聊天...哥们，她发的大部分都是问数学题的啊。'帮我看看这道高数题'、'这个极限怎么求'，这是在请教你不是在撩你。下周不是高数期中吗？"
- Agent reply: Notes Li Hao's observation about content being study-focused. Cross-references with exam schedule.

**Loop 3: Wang Ming mentions Zhang Zixuan's intel**
- User (Li Hao): "[微信 李浩 Wed Mar 18 20:30 CST 2026] 张子轩说的？他那消息你也信？他听室友说的，室友听林雨桐说的，传了两手了。人家说'王明人挺好的'可能就是客气话，不一定是对你有意思。"
- Agent reply: Notes Li Hao's skepticism about secondhand intel and the information relay chain degradation.

**Loop 4: Li Hao's honest assessment**
- User (Li Hao): "[微信 李浩 Wed Mar 18 20:45 CST 2026] 我跟你说实话啊，林雨桐就是那种对谁都挺热情的女生。我跟她同一个英语口语小组，她对每个人都很nice。你别因为她对你friendly就觉得是对你有意思。"
- Agent reply: Documents Li Hao's broader observation about Lin Yutong's general warmth. Notes this challenges the "special treatment" interpretation.

**Loop 5: Wang Ming asks about the cafe post**
- User (Li Hao): "[微信 李浩 Fri Mar 20 21:00 CST 2026] 那个朋友圈？'有趣的人'？我也看到了。不知道是谁，但你别瞎想。可能是她闺蜜或者老同学什么的。你直接问她不就知道了？别在这猜来猜去。"
- Agent reply: Notes Li Hao's pragmatic advice to ask directly rather than speculate.

**Loops 6-10: Noise (5 loops)**
- Loop 6: Discussion about gaming (LOL ranked match). Noise.
- Loop 7: Li Hao complains about his own assignment deadline. Noise.
- Loop 8: They discuss weekend basketball plans. Noise.
- Loop 9: Li Hao sends a meme about exam stress. Noise.
- Loop 10: Brief exchange about cafeteria recommendations. Noise.

---

**Phase 2 content (Update 1 append -- before R5): 4 loops**

**Loop 11: Li Hao shows baseline engagement data [C4 resolution evidence]**
- User (Li Hao): "[微信 李浩 Sun Mar 22 15:00 CST 2026] 哥们，我帮你做了个分析。我翻了林雨桐最近一周的朋友圈互动。她不止点赞你的，她几乎每个人的朋友圈都点赞评论。我数了一下，这一周她给至少15个不同的人点赞了。你不是特殊的那个。"
- Agent tool call: read lihao-baseline-analysis.md
- Agent reply: Reviews Li Hao's baseline data. Confirms Lin Yutong's engagement with Wang Ming is not statistically different from her baseline with others. C4 evidence.

**Loop 12: Li Hao gives specific numbers**
- User (Li Hao): "[微信 李浩 Sun Mar 22 15:15 CST 2026] 我列了几个：她给小赵点赞了4次评论2次，给你3次2次，给班长3次1次，给学委2次2次...基本上都差不多。她就是社交达人，不是对你有special attention。"
- Agent reply: Documents the comparative engagement data.

**Loop 13: Wang Ming's messaging frequency also dropped**
- User (Li Hao): "[微信 李浩 Sun Mar 22 15:30 CST 2026] 还有，你不是说她这周消息变少了吗？因为高数考完了啊！她不用问你题了。你自己看看上周的消息内容，是不是大部分都是问数学的？"
- Agent reply: Notes the correlation between exam completion and messaging drop.

**Loop 14: Li Hao's summary advice**
- User (Li Hao): "[微信 李浩 Sun Mar 22 16:00 CST 2026] 我不是说她一定对你没意思，我是说你现在看到的这些'信号'都不能说明什么。如果你真想知道，要么直接问，要么继续观察真正的特殊信号。别用confirmation bias蒙自己。"
- Agent reply: Documents Li Hao's evidence-based conclusion.

---

## Session 2: Wang Ming--Zhang Zixuan IM (Intel Source)

**Session meta:**
- channel: 微信 IM
- participant: 张子轩 (Zhang Zixuan)
- session_id: `PLACEHOLDER_ZHANGZIXUAN_IM_UUID`
- Time range: Mar 15-18 (Phase 1), Mar 24 (Phase 2 append via Update 3)

**Phase 1 content (8 loops: 3 key + 5 noise)**

**Loop 1: Zhang Zixuan delivers first intel**
- User (Zhang Zixuan): "[微信 张子轩 Sat Mar 15 14:00 CST 2026] 哥们，我跟林雨桐的室友陈雯聊天，她说林雨桐提过你！说你人挺好的。你懂吧？这就是信号！"
- Agent reply: Documents Zhang Zixuan's report. Notes the information chain: Lin Yutong -> roommate Chen Wen -> Zhang Zixuan -> Wang Ming.

**Loop 2: Wang Ming asks for details**
- User (Zhang Zixuan): "[微信 张子轩 Sat Mar 15 14:15 CST 2026] 具体说什么？就说'王明人挺好的'，好像还说你数学讲得好。哎呀这不重要，重要的是她主动提起你了！说明心里有你。"
- Agent reply: Notes the actual content ("人挺好的，数学讲得好") could be a factual assessment of study helpfulness rather than romantic interest.

**Loop 3: Zhang Zixuan encourages confession**
- User (Zhang Zixuan): "[微信 张子轩 Wed Mar 18 12:00 CST 2026] 怎么样？考虑表白了吗？她消息也多了对吧？窗口期啊兄弟，过了就没了。"
- Agent reply: Notes Zhang Zixuan is encouraging action based on his interpretation.

**Loops 4-8: Noise (5 loops)**
- Loop 4: Discussion about a basketball game. Noise.
- Loop 5: Zhang Zixuan asks about a CS assignment. Noise.
- Loop 6: Campus gossip about another couple. Noise.
- Loop 7: Discussion about upcoming class schedule changes. Noise.
- Loop 8: Sharing memes. Noise.

---

**Phase 2 content (Update 3 append -- before R11): 4 loops**

**Loop 9: Zhang Zixuan delivers contradictory intel [C2 reversal trigger]**
- User (Zhang Zixuan): "[微信 张子轩 Tue Mar 24 18:00 CST 2026] 兄弟...我又跟陈雯聊了一下。她说最近林雨桐好像在追一个学长，数学系大三的，好像是她TA。"
- Agent reply: Documents the contradictory intel. Notes that Zhang Zixuan's Mar 15 report said "she likes you" and his Mar 24 report says "she likes a senior." These directly contradict each other.

**Loop 10: Wang Ming reacts**
- User (Zhang Zixuan): "[微信 张子轩 Tue Mar 24 18:10 CST 2026] 我也不确定啊，陈雯说的也可能是乱猜。但你要是想表白，可能得抓紧了？反正别怪我没告诉你。"
- Agent reply: Notes Zhang Zixuan himself acknowledges uncertainty. His intel is formally unreliable -- two contradictory reports from the same source chain.

**Loop 11: Wang Ming questions source reliability**
- User (Zhang Zixuan): "[微信 张子轩 Tue Mar 24 18:20 CST 2026] 哎你别怀疑我啊，我就是转述。陈雯跟林雨桐住一个宿舍，她说什么我就转告什么。也许两个都是真的呢？她可能同时觉得你不错但也在追学长？"
- Agent reply: Notes Zhang Zixuan's attempt to reconcile his contradictory reports, which actually makes his analysis even less reliable.

**Loop 12: Zhang Zixuan exits**
- User (Zhang Zixuan): "[微信 张子轩 Tue Mar 24 18:30 CST 2026] 反正你自己判断吧，我就是情报员，分析是你自己的事。加油！"
- Agent reply: Documents Zhang Zixuan's self-demotion from analyst to mere relay.

---

## Session 3: Wang Ming--Ajie IM (Online Friend / Bad Advisor)

**Session meta:**
- channel: 微信 IM
- participant: 阿杰 (A-Jie)
- session_id: `PLACEHOLDER_AJIE_IM_UUID`
- Time range: Mar 25 (Phase 1 only, no Phase 2 append)

**Phase 1 content (8 loops: 4 key + 4 noise)**

**Loop 1: Wang Ming asks Ajie for advice**
- User (Ajie): "[微信 阿杰 Wed Mar 25 20:00 CST 2026] 老弟你这还用分析？消息频率从一周3条涨到12条，这不是明牌吗？"
- Agent reply: Notes Ajie's confidence in the frequency-as-signal heuristic.

**Loop 2: Ajie applies online dating logic**
- User (Ajie): "[微信 阿杰 Wed Mar 25 20:15 CST 2026] 我跟你说，网上约过几十次了，女生如果对你有意思就是消息变多、回复变快、主动找话题。你这三条都中了。"
- Agent reply: Notes Ajie is applying online dating heuristics to a real-life friendship, which may not transfer.

**Loop 3: Wang Ming mentions the content is study-related**
- User (Ajie): "[微信 阿杰 Wed Mar 25 20:30 CST 2026] 问数学题也是找话题啊！你想想，她班上那么多数学好的，为什么偏偏问你？就是找借口跟你聊天！"
- Agent reply: Notes Ajie's interpretation ignores that Wang Ming may actually be the most accessible helper (same English class, sits together).

**Loop 4: Ajie pushes for confession [B1 insertion context]**
- User (Ajie): "[微信 阿杰 Wed Mar 25 20:45 CST 2026] 我的建议：趁热打铁，这周就表白。拖久了她可能就被别人追走了。频率高+朋友圈互动多+朋友说她提过你=明牌了。"
- Agent reply: **B1 bias phrase appears here:**
  > "The increased messaging frequency (from 3 to 12 messages per week) combined with Zhang Zixuan's report that Lin Yutong mentioned you positively to her roommate suggests growing personal interest beyond the academic context. While the exam preparation provides an alternative explanation, the magnitude of the frequency increase and the positive roommate report together form a pattern consistent with developing interest."

**Loops 5-8: Noise (4 loops)**
- Loop 5: Ajie talks about his own dating app experiences. Noise.
- Loop 6: Gaming discussion. Noise.
- Loop 7: Ajie recommends a Netflix show. Noise.
- Loop 8: Random memes and jokes. Noise.
