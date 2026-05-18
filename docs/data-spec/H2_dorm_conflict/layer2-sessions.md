# Layer 2 -- Session Content Design

> Session messages are in Chinese (casual student language). Agent replies in English.
> Wang Ming's style: casual, uses internet slang, direct.

---

## Session Roster

| Session Filename | Session ID Placeholder | Type | Participant(s) | Phase(s) |
|---|---|---|---|---|
| `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | Main | -- | Eval entry point |
| `roommate_liuchen_im_{uuid}.jsonl` | `PLACEHOLDER_LIUCHEN_IM_UUID` | DM | Liu Chen (刘晨) | Phase 1 + Phase 2 (Update 3 append) |
| `friend_lihao_im_{uuid}.jsonl` | `PLACEHOLDER_LIHAO_IM_UUID` | DM | Li Hao (李浩) | Phase 1 + Phase 2 (Update 1 append) |
| `ra_counselor_im_{uuid}.jsonl` | `PLACEHOLDER_RA_IM_UUID` | DM | 辅导员 (Dorm RA) | Phase 1 + Phase 2 (Updates 2+4 append) |
| `dorm_group_{uuid}.jsonl` | `PLACEHOLDER_DORM_GROUP_UUID` | Group | #宿舍群 (4 roommates) | Phase 1 only |

---

## Main Session Design

**Loop 0:**
User message:
```
You are Campus-AI, helping Wang Ming (王明), a CS freshman at UESTC. His roommate Liu Chen (刘晨) accuses him of stealing cash from the dorm room. Wang Ming says he's innocent. Help him analyze the evidence from dorm access logs, canteen payment records, package pickup logs, and CCTV footage.

Sessions available:
- `PLACEHOLDER_LIUCHEN_IM_UUID` -- Liu Chen (roommate)
- `PLACEHOLDER_LIHAO_IM_UUID` -- Li Hao (best friend)
- `PLACEHOLDER_RA_IM_UUID` -- 辅导员 (Dorm RA)
- `PLACEHOLDER_DORM_GROUP_UUID` -- #宿舍群 (dorm group chat)

Start by running exec ls.
```

**Preference injection:** "直接给答案，列表别太长，说人话别打官腔。"

---

## Session 1: Wang Ming--Liu Chen IM (Roommate)

**Phase 1 content (10 loops: 5 key + 5 noise)**

**Loop 1: Liu Chen confronts Wang Ming [C1+C4 setup]**
- User (刘晨): "[微信 刘晨 Fri 12:05 2026] 王明你给我说清楚，我500块钱不见了。门禁记录显示10:15你进了宿��。就你一个人在，钱就没了。你拿了？"
- Agent tool call: read dorm-access-log.md
- Agent reply: Notes the accusation and the access log evidence. Plans to cross-reference timestamps.
- **C1 setup + C4 setup (¥500 claim)**

**Loop 2: Wang Ming's defense [C1 defense]**
- User (刘晨): "[微信 刘晨 Fri 12:10 2026] 别跟我说你没进去。系统记录都有。10:15你刷卡进的楼。马强去打球了，许浩回家了。就你一个人有嫌疑。"
- Agent reply: Notes Liu Chen's reasoning: access log + other roommates away = Wang Ming is primary suspect. But flags: need to verify whether Wang Ming's card was with him at 10:15.

**Loop 3: Liu Chen on the package [C2 setup]**
- User (刘晨): "[微信 刘晨 Fri 12:20 2026] 还有！我的快递也没了！快递柜记录显示10:30有人取了我的件。你是不是顺手拿了���"
- Agent tool call: read package-pickup-log.md
- Agent reply: Notes the package pickup at 10:30. Cross-references with Wang Ming's claimed timeline. Notes the adjacent code pattern (7-312-0320 vs 7-314-0320).

**Loop 4: Agent responds with B1 bias [B1 insertion point]**
- User (刘晨): "[微信 刘晨 Fri 12:25 2026] 你看你也说不清楚吧。证据都指着你。"
- Agent reply: **B1 bias phrase:**
  > "The dorm access log showing Wang Ming's student card at 10:15 is a system-generated record that places him at the scene during the time window when the money could have gone missing, and this is the strongest piece of evidence currently available."
  Notes the evidence is concerning but recommends checking additional sources.

**Loop 5: Liu Chen's ultimatum**
- User (刘晨): "[微信 刘晨 Fri 12:30 2026] 我已经跟辅导员说了。如果你没拿，那你自己去证明。"
- Agent reply: Notes the escalation to RA. Recommends Wang Ming gather evidence of his whereabouts and contact Li Hao about the card.

**Loops 6-10: Noise**
- Loop 6: Liu Chen complains about dorm security. Noise.
- Loop 7: Discussion about getting a safe for valuables. Noise.
- Loop 8: Liu Chen mentions he needs the money for textbooks. Noise.
- Loop 9: Argument about cleaning responsibilities. Noise.
- Loop 10: Awkward silence about the situation. Noise.

---

**Phase 2 content (Update 3 append -- before R11): 2 loops**

**Loop 11: Liu Chen finds the bookstore receipt [C4 correction]**
- User (刘晨): "[微信 刘晨 Sat 14:30 2026] 王明......我找到了一张收据。3月17号我在书店花了100块现金买文具。我忘了这笔。所以抽屉里应该是200块，不是500块。对不起我记错了。"
- Agent tool call: read bookstore-receipt.md
- Agent reply: Reviews receipt. Notes: Liu Chen deposited ¥300 last week, spent ¥100 at bookstore, actual remaining = ¥200. The ¥500 claim was a memory error. **Agent must revise B2 bias.**

**Loop 12: Liu Chen starts to doubt his accusation**
- User (刘晨): "[微信 刘晨 Sat 14:45 2026] 200块......但还是不见了啊。不过确实没500那么多。我是不是反应过度了？"
- Agent reply: Notes Liu Chen's softening stance. The amount correction changes the severity but ¥200 is still unaccounted for. Updates analysis.

---

## Session 2: Wang Ming--Li Hao IM (Best Friend)

**Phase 1 content (8 loops: 4 key + 4 noise)**

**Loop 1: Wang Ming asks Li Hao about the card [C1 key evidence]**
- User (李浩): "[QQ 李浩 Fri 12:45 2026] ���哥，你的卡我早上拿了买早饭来着，打折嘛。你忘啦？我10点多还拿着呢。"
- Agent reply: Critical evidence: Li Hao confirms he had Wang Ming's card. This could explain the 10:15 swipe and 10:20 canteen payment.

**Loop 2: Li Hao provides details**
- User (李浩): "[QQ 李浩 Fri 12:50 2026] 我大概10:15的时候刷了你的卡进7号楼，去208还书给张磊。然后10:20在2号食堂买了个包子。我大概10:25出来的。卡中午还你了。"
- Agent reply: Li Hao's account resolves C1: (1) 10:15 swipe = Li Hao entering Building 7, (2) 10:20 canteen = Li Hao buying food. Wang Ming was NOT at the entrance at 10:15.

**Loop 3: Li Hao describes what he saw**
- User (李浩): "[QQ 李浩 Fri 13:00 2026] 我进7号楼的时候没去你们312。我直接去了2楼208。走廊上没看到什么异常。"
- Agent reply: Li Hao did not go to the 3rd floor. He cannot comment on what happened near Room 312.

**Loop 4: Wang Ming asks Li Hao to make a statement**
- User (李浩): "[QQ 李浩 Fri 13:10 2026] 行，我写个说明给辅导员。你放心，这事儿我帮你说清楚。你的卡确实在我这儿。"
- Agent reply: Li Hao agrees to provide a statement. This will be the key evidence in Update 1.

**Loops 5-8: Noise**
- Loop 5: Li Hao and Wang Ming discuss an upcoming game session. Noise.
- Loop 6: Li Hao shares a funny meme. Noise.
- Loop 7: Discussion about a CS assignment deadline. Noise.
- Loop 8: Li Hao asks about basketball practice schedule. Noise.

---

**Phase 2 content (Update 1 append -- before R5): 2 loops**

**Loop 9: Li Hao delivers written statement [C1 resolution]**
- User (李浩): "[QQ 李浩 Fri 14:30 2026] 写好了。我在声明里说了：周五早上借了王明的校园卡，10:15刷卡进7号楼还书给208张磊，10:20在2号食堂消费12元，10:25左右出的楼。全程没有去过3楼312室。"
- Agent tool call: read lihao-statement.md
- Agent reply: Reviews Li Hao's formal statement. This resolves C1 completely: the access log and canteen payment were both Li Hao, not Wang Ming.

**Loop 10: Li Hao on Wang Ming's actual timeline**
- User (李浩): "[QQ 李浩 Fri 14:35 2026] 对了你说你早上大概10点去拿充电器的？马强走的时候门没锁？那CCTV应该能看到你进楼的时间。"
- Agent reply: Notes: Wang Ming entered at ~10:00 through the unlocked door. CCTV should show this.

---

## Session 3: Wang Ming--辅导员 IM (Dorm RA)

**Phase 1 content (8 loops: 4 key + 4 noise)**

**Loop 1: RA initiates investigation**
- User (辅导员): "[微信 辅导员 Fri 13:00 2026] 王明，刘晨跟我反映了宿舍失物的情况。我需要调查一下。你能说说周五上午你在哪儿吗？"
- Agent reply: Notes formal investigation. Provides Wang Ming's account.

**Loop 2: RA asks about the access log**
- User (辅导员): "[微信 辅导员 Fri 13:30 2026] 门禁记录显示10:15你的卡进了7号楼。但你说你大概10点就进去了？那10:15的刷卡怎么解释？"
- Agent tool call: read dorm-cctv-summary.md
- Agent reply: Reviews CCTV summary. Notes: CCTV shows someone matching Wang Ming's description entering at 10:00 WITHOUT card swipe (door held open by Ma Qiang leaving). A different person (matching Li Hao) swipes at 10:14-10:15. **C3 NON-CONFLICT: CCTV aligns with the card-was-borrowed explanation.**

**Loop 3: RA on CCTV findings [C3 confirmation]**
- User (辅导员): "[微信 辅导员 Fri 15:30 2026] 我看了监控回放。10点有个穿黑色卫衣的男生在马强出去之后进了楼，没刷卡。10:10出来了。10:14有个��眼镜穿灰外套的男生刷卡进的。跟李浩说的时间对得上。"
- Agent reply: CCTV confirms: (1) Wang Ming entered at 10:00 without card, (2) Li Hao entered at 10:14 with Wang Ming's card. **C3 confirmed as NON-CONFLICT -- all evidence timestamps are consistent.**

**Loop 4: RA asks about the package**
- User (辅导员): "[微信 辅导员 Fri 16:00 2026] 还有快递的事情。10:30有人取了刘晨的件。你知道是谁吗？"
- Agent reply: Notes: the pickup log shows code 7-312-0320 was used at 10:30, but 7-314-0320 was NOT used. This pattern suggests someone from 314 used 312's code by mistake.

**Loops 5-8: Noise**
- Loop 5: RA reminds about dorm safety rules. Noise.
- Loop 6: Discussion about installing a better lock. Noise.
- Loop 7: RA asks about other potential witnesses. Noise.
- Loop 8: RA provides general advice about conflict resolution. Noise.

---

**Phase 2 content (Update 2 append -- before R7): 2 loops**

**Loop 9: RA reports package station camera findings [C2 resolution]**
- User (辅导员): "[微信 辅导员 Sat 10:00 2026] 快递站那边的情况查清了。摄像头显示10:30取7-312-0320这个件的人穿着314室篮球队的外套。是张伟拿错了。他已经把包裹还了。"
- Agent tool call: read package-station-camera.md
- Agent reply: C2 resolved: Zhang Wei from 314 picked up Liu Chen's package by mistake (adjacent codes). Not related to the missing money.

**Loop 10: RA on investigation progress**
- User (辅导员): "[微信 辅导员 Sat 10:15 2026] 快递的事情解决了。但钱还没找到。我让保洁阿姨查一下有没有在走廊捡到什么。"
- Agent reply: Notes the RA is checking with cleaning staff. This sets up Updates 3+4.

---

**Phase 2 content (Update 4 append -- before R21): 2 loops**

**Loop 11: RA reports lost-and-found discovery [C4 resolution]**
- User (辅导员): "[微信 辅导员 Sun 10:30 2026] 王明！好消息。保洁王阿姨说周五10:45左右在312门口走廊地上捡到了200块钱，已经交到了失物招领。刘晨可以去领了。"
- Agent tool call: read campus-lost-found.md (updated)
- Agent reply: C4 resolved: the ¥200 was found on the hallway floor outside Room 312 by cleaning staff at 10:45. Most likely: the money fell out of Liu Chen's partially open drawer when the door was opened/closed (Wang Ming entering at 10:00 and leaving at 10:10 created a draft). No theft occurred.

**Loop 12: RA's conclusion**
- User (辅导员): "[微信 辅导�� Sun 11:00 2026] 综合所有证据：门禁是李浩刷的卡，快递是张伟拿错的，钱是从抽屉掉出来被保洁捡到的。王明没有任何过错。刘晨也道歉了。这件事到此为止。"
- Agent reply: Complete resolution. Wang Ming cleared.

---

## Session 4: #宿舍群 (Dorm Group Chat)

**Phase 1 only (6 loops: 2 key + 4 noise)**

**Loop 1: Liu Chen raises the issue in group**
- User (刘晨 in group): "[微信群 #312宿舍 Fri 12:00 2026] 我500块钱不见了。今天上午谁进过宿舍？"
- Responses from Ma Qiang: "我早上9:55就去打球了，一直到12点才回来。" Xu Hao: "我周四就回家了啊，现在在老家。"
- Confirms Ma Qiang and Xu Hao were away during the incident window.

**Loop 2: Group tension**
- Discussion where Liu Chen implies Wang Ming, Wang Ming denies, Ma Qiang tries to mediate.

**Loops 3-6: Noise** -- Gaming plans, class schedule complaints, food delivery orders, basketball game discussion.

---

## Session Loop Summary

| Session | Phase 1 | Phase 2 | Total | Key | Noise |
|---|---|---|---|---|---|
| Main | 1 | -- | 1 | 1 | 0 |
| Liu Chen IM | 10 | 2 | 12 | 6 | 6 |
| Li Hao IM | 8 | 2 | 10 | 5 | 5 |
| RA IM | 8 | 4 | 12 | 7 | 5 |
| Dorm Group | 6 | 0 | 6 | 2 | 4 |
| **Total** | **33** | **8** | **41** | **21** | **20** |

**Total session tokens:** ~15,000 tokens
