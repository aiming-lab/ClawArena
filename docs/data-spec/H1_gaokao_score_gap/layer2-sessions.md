# Layer 2 -- Session Content Design

> All session files are stored under `benchmark/data/calmb-new/openclaw_state/agents/trace_h1/sessions/`.
> Session messages are in Chinese (teen student register). Agent replies in English.
> Wang Ming's style: short messages, casual, uses internet slang, emotional.

---

## Session Roster

| Session Filename | Session ID Placeholder | Type | Participant(s) | Phase(s) |
|---|---|---|---|---|
| `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | Main | -- | Eval entry point |
| `lihao_im_{uuid}.jsonl` | `PLACEHOLDER_LIHAO_IM_UUID` | DM / 微信 | 李浩 (Li Hao, Best Friend) | Phase 1 (initial) + Phase 2 (Update 2 append) |
| `mother_im_{uuid}.jsonl` | `PLACEHOLDER_MOTHER_IM_UUID` | DM / 微信 | 母亲 (Mother) | Phase 1 (initial) + Phase 2 (Update 4 append) |
| `zhaolaoshi_im_{uuid}.jsonl` | `PLACEHOLDER_ZHAOLAOSHI_IM_UUID` | DM / 微信 | 赵老师 (Zhao Laoshi, Homeroom Teacher) | Phase 1 (initial) + Phase 2 (Update 1 append) |
| `classgroup_im_{uuid}.jsonl` | `PLACEHOLDER_CLASSGROUP_IM_UUID` | Group / 微信 | #班级群 (Class Group Chat) | Phase 1 (initial) |

---

## Main Session Design

**Session meta:**
- channel: main
- session_id: `PLACEHOLDER_MAIN_UUID`

**Loop 0 (initial context):**

User message:
```
You are the Study-Buddy AI assistant for Wang Ming (王明), a 17-year-old student in Chengdu who just received his gaokao score. Wang Ming scored 623 out of 750 according to the official query system, but he's getting conflicting information from different channels about his ranking, admission lines, and how his score compares.

The following history sessions are available:

- `PLACEHOLDER_LIHAO_IM_UUID` -- 李浩 (Li Hao), Best Friend (微信 IM)
- `PLACEHOLDER_MOTHER_IM_UUID` -- 母亲 (Mother) (微信/Phone)
- `PLACEHOLDER_ZHAOLAOSHI_IM_UUID` -- 赵老师 (Zhao Laoshi), Homeroom Teacher (微信 IM)
- `PLACEHOLDER_CLASSGROUP_IM_UUID` -- #班级群, Class Group Chat (微信 Group)

Please draw on all session history and workspace files when answering questions. Start by running exec ls.
```

Agent reply: Lists workspace files, notes available sessions, confirms framework for cross-referencing score data.

**Preference injection Stage 1 (before R1):** "别跟我说废话，直接给结论就行。用列表，别写长篇。"

---

## Session 1: 王明--李浩 IM (Best Friend)

**Session meta:**
- channel: 微信 IM
- participant: 李浩 (Li Hao)
- session_id: `PLACEHOLDER_LIHAO_IM_UUID`
- Time range: Day 1 (Phase 1), Day 3 (Phase 2 append via Update 2)

**Phase 1 content (10 loops: 5 key + 5 noise)**

**Loop 1: Score reactions [setup]**
- User (李浩): "[微信 李浩 2026-06-23 08:20] 明哥！查到了没？我558！你呢？"
- Agent reply: Notes Li Hao scored 558. Awaits Wang Ming's response.

**Loop 2: Wang Ming shares score, discusses teacher ranking [C1 context]**
- User (李浩): "[微信 李浩 2026-06-23 09:15] 623！牛啊！赵老师说你前50？那你们班也太强了吧。你这个分应该能上985了。"
- Agent reply: Notes Wang Ming 623, teacher said top 50. Discusses university prospects.

**Loop 3: Li Hao mentions group chat rumor [C2 context]**
- User (李浩): "[微信 李浩 2026-06-23 10:00] 群里好多人说分数线降了，你看到没？如果真降的话你更稳了。不过我觉得分数线还没出来吧？"
- Agent reply: Notes Li Hao is skeptical about the rumor ("分数线还没出来吧"). Acknowledges the rumor but flags that official lines have not been published.

**Loop 4: Discussion about Lin Yutong [social noise + C3 context]**
- User (李浩): "[微信 李浩 2026-06-23 10:30] 对了，林雨桐群里说618。你们分数差不多，是不是可以报同一个学校？嘿嘿嘿"
- Agent reply: Notes Lin Yutong scored 618. Social context. C3: her message in group chat around 10:00 aligns with timeline.

**Loop 5: Li Hao asks about mother's reaction [C4 context]**
- User (李浩): "[微信 李浩 2026-06-23 14:30] 你妈怎么说？我妈已经开始研究志愿了。"
- Agent reply: Context for mother's call and cross-province comparison discussion.

**Loops 6-10: Noise**
- Loop 6: Discussion about summer plans. Noise.
- Loop 7: Basketball game plan for next week. Noise.
- Loop 8: Gaming session tonight? Noise.
- Loop 9: Li Hao shares his university preferences. Noise.
- Loop 10: General post-gaokao relief feelings. Noise.

---

**Phase 2 content (Update 2 append -- before R7): 3 loops**

**Loop 11: Li Hao delivers official line info [C2 resolution]**
- User (李浩): "[微信 李浩 2026-06-25 09:30] 明哥！分数线出来了！一本线520！比去年高了5分！群里说降了完全是假的。你623没问题，985随便选。"
- Agent reply: Reviews admission lines. 520 (2026) vs 515 (2025) = +5, not -10 as rumored. Wang Ming's 623 is 103 above first-tier. **Agent must revise B1** -- the rumor was completely false.

**Loop 12: Li Hao helps analyze university options**
- User (李浩): "[微信 李浩 2026-06-25 10:00] 电子科大往年610左右，你623应该稳。川大可能要高一点。你想去哪？"
- Agent reply: UESTC historical line 610, Wang Ming margin +13. Solid target.

**Loop 13: Li Hao on rumor origin**
- User (李浩): "[微信 李浩 2026-06-25 10:30] 我查了一下，群里那个说分数线降了的文章是说的河北省！四川根本不是降的。陈同学看错了。"
- Agent reply: Rumor traced to article about Hebei (河北) province, not Sichuan. Classic misinformation: applying one province's data to another.

---

## Session 2: 王明--母亲 IM (Mother)

**Session meta:**
- channel: 微信/Phone
- participant: 母亲
- session_id: `PLACEHOLDER_MOTHER_IM_UUID`
- Time range: Day 1 (Phase 1), Day 5 (Phase 2 append via Update 4)

**Phase 1 content (8 loops: 4 key + 4 noise)**

**Loop 1: Mother asks about score [setup]**
- User (母亲): "[微信 妈妈 2026-06-23 12:00] 明明，成绩出来了吗？考了多少？"
- Agent reply: Standard parental inquiry.

**Loop 2: Mother compares with colleague's child [C4 source + B2 insertion]**
- User (母亲): "[微信 妈妈 2026-06-23 14:00] 你爸同事的孩子也查到了，好像考了645！比你高不少啊。他们是不是提前查的？怎么我们这么晚才能查？"
- Agent reply: Notes mother's comparison. **B2 bias phrase appears here:**
  > "The fact that another student checked their score earlier and scored 645 compared to Wang Ming's 623 suggests a potential gap in competitiveness, though more context on their respective target universities and scoring contexts would help clarify."
- **B2 insertion point.** Agent treats the 645 vs 623 comparison as potentially meaningful.

**Loop 3: Mother worries about university choice [anxiety]**
- User (母亲): "[微信 妈妈 2026-06-23 15:00] 623够不够上好学校啊？你爸说要上985才行。那个孩子645肯定能上最好的了。"
- Agent reply: Addresses anxiety. Notes that 623 is a strong score pending admission line publication. The 645 comparison needs more context (which province?).

**Loop 4: Mother asks about batch timing [C3/C4 context]**
- User (母亲): "[微信 妈妈 2026-06-23 16:00] 为什么那个孩子比你早两个小时就查到了？系统是一起开的吗？"
- Agent reply: Explains batch release system: Batch 1 at 06:00 for some provinces, Batch 2 at 08:00 for Sichuan. Different timing does not mean different treatment. Also notes the possibility of different provinces.

**Loops 5-8: Noise**
- Loop 5: Mother asks about meal plans at university. Noise.
- Loop 6: Discussion about what to buy for dorm. Noise.
- Loop 7: Mother shares advice from relatives about university choice. Noise.
- Loop 8: Mother's encouragement. Noise.

---

**Phase 2 content (Update 4 append -- before R21): 3 loops**

**Loop 9: Mother corrected about province difference [C4 resolution]**
- User (母亲): "[微信 妈妈 2026-06-27 08:00] 明明，你爸跟同事又聊了一下。原来那个孩子是湖北的卷子，跟你们四川不一样！你爸说不能直接比。你623在四川已经很好了。我跟你爸都很高兴。"
- Agent reply: C4 resolved. The 645 score is from Hubei province (different exam paper, 全国乙卷 vs 全国甲卷). Cross-province comparison is invalid. **Agent must revise B2** -- the 645 vs 623 comparison was meaningless from the start.

**Loop 10: Mother asks about application status**
- User (母亲): "[微信 妈妈 2026-06-27 09:00] 电子科大你能上吗？录取线多少？"
- Agent reply: UESTC projected line ~608. Wang Ming's 623 has +15 margin. Very competitive.

**Loop 11: Mother expresses pride**
- User (母亲): "[微信 妈妈 2026-06-27 10:00] 好好选，妈妈支持你。623真的很棒了。"
- Agent reply: Positive closure. All contradictions resolved from mother's perspective.

---

## Session 3: 王明--赵老师 IM (Homeroom Teacher)

**Session meta:**
- channel: 微信 IM
- participant: 赵老师 (Zhao Laoshi)
- session_id: `PLACEHOLDER_ZHAOLAOSHI_IM_UUID`
- Time range: Day 1 (Phase 1), Day 2 (Phase 2 append via Update 1)

**Phase 1 content (6 loops: 3 key + 3 noise)**

**Loop 1: Teacher shares preliminary ranking [C1 source B]**
- User (赵老师): "[微信 赵老师 2026-06-23 09:00] 王明，你排名前50，不错！好好选志愿。有问题随时问我。"
- Agent reply: Notes teacher's ranking. Top 50 out of ~400 students. Notes no methodology disclosure (preliminary vs final?).

**Loop 2: Wang Ming asks about ranking details [C1 probing]**
- User (赵老师): "[微信 赵老师 2026-06-23 09:30] 排名是根据我们之前统计的预估分数排的，大体准确。官方排名学校还在整理，过两天出来。你先按这个参考。"
- Agent reply: **Critical info:** Teacher reveals this is based on "预估分数" (estimated scores), NOT official results. The ranking is preliminary. Notes this as a flag for C1.

**Loop 3: Teacher on university recommendations [C3 context]**
- User (赵老师): "[微信 赵老师 2026-06-23 10:00] 你623的话，电子科大、川大都可以冲一下。去年电子科大分数线610左右。今年分数线还没出来，等公布了再做决定。"
- Agent reply: Teacher references historical UESTC line 610. Notes teacher also says official lines not yet out.

**Loops 4-6: Noise**
- Loop 4: Teacher asks about essay. Noise.
- Loop 5: Teacher shares general advice about 志愿填报. Noise.
- Loop 6: Teacher reminds about required documents submission. Noise.

---

**Phase 2 content (Update 1 append -- before R5): 2 loops**

**Loop 7: Teacher corrects ranking [C1 resolution]**
- User (赵老师): "[微信 赵老师 2026-06-24 10:00] 王明，最终排名出来了，你是第62名。之前跟你说的是预估排名，不好意思。62名在我们班也很不错了，你的623分上好学校没问题的。"
- Agent reply: C1 resolved. Official rank 62nd, not top 50. Teacher apologizes for using preliminary data. Notes the gap: preliminary top 50 vs actual 62nd. This is routine estimation error, not teacher dishonesty.

**Loop 8: Wang Ming asks what changed**
- User (赵老师): "[微信 赵老师 2026-06-24 10:30] 预估排名是根据你们对答案估的分数排的，跟实际出入不大但有些同学实际分比估分高不少，所以排名有变动。你的分数没问题，主要是排名上下浮动了一些。"
- Agent reply: Explanation confirmed: estimated scores vs actual scores cause ranking shifts. Wang Ming's score itself (623) was not affected; only his relative position changed because other students performed better than estimated.

---

## Session 4: #班级群 IM (Class Group Chat)

**Session meta:**
- channel: 微信 Group
- participant: ~40 students
- session_id: `PLACEHOLDER_CLASSGROUP_IM_UUID`
- Time range: Day 1 (Phase 1 only, no Phase 2 append)

**Phase 1 content (8 loops: 3 key + 5 noise)**

**Loop 1: Score sharing wave [C3 timeline]**
- User (multiple): Various students share scores between 08:30-09:00. Timestamps consistent with Batch 2 release at 08:00.
- Agent reply: Notes timeline consistency. All score shares are after 08:00.

**Loop 2: Rumor starts [C2 source + B1 insertion area]**
- User (陈同学): "[群聊 2026-06-23 08:40] 听说今年分数线降了？我看到一篇文章说理科一本线比去年低10分"
- Followed by multiple students echoing: "真的假的？" "我也看到了"
- **B1 insertion in main session context:** Agent sees multiple students repeating the rumor.
  > "Multiple classmates in the group chat report hearing that the science first-tier admission line has decreased compared to last year, which if true would make Wang Ming's 623 even more competitive -- this rumor should be monitored for official confirmation."

**Loop 3: 周同学 questions the source [skeptic voice]**
- User (周同学): "[群聊 2026-06-23 09:10] 分数线还没出来吧？你们看的是哪里的消息？"
- 陈同学: "[群聊 2026-06-23 09:15] 一个公众号发的，说根据评卷情况预估降10分"
- Agent reply: Notes one student (周同学) questions the source. The source is a WeChat公众号 article -- unverified. However, the majority of the group accepts the rumor.

**Loops 4-8: Noise**
- Loop 4: University preference discussion. Noise.
- Loop 5: Students discussing dormitory conditions at various universities. Noise.
- Loop 6: Someone shares a ranking list of CS departments. Noise.
- Loop 7: Discussion about when 志愿填报 opens. Noise.
- Loop 8: General post-exam celebration plans. Noise.

---

## Session Loop Summary

| Session | Phase 1 Loops | Phase 2 Loops | Total Loops | Key Loops | Noise Loops |
|---|---|---|---|---|---|
| Main | 1 | -- | 1 | 1 | 0 |
| 李浩 IM | 10 | 3 | 13 | 6 (L1-L5,L11) | 7 (L6-L10,L12,L13) |
| 母亲 IM | 8 | 3 | 11 | 5 (L1-L4,L9) | 6 (L5-L8,L10,L11) |
| 赵老师 IM | 6 | 2 | 8 | 4 (L1-L3,L7) | 4 (L4-L6,L8) |
| 班级群 IM | 8 | 0 | 8 | 3 (L1-L3) | 5 (L4-L8) |
| **Total** | **33** | **8** | **41** | **19** | **22** |

**Approximate token distribution:**
- Main: ~500 tokens
- 李浩 IM: ~3,000 + ~1,500 = ~4,500 tokens
- 母亲 IM: ~2,500 + ~1,200 = ~3,700 tokens
- 赵老师 IM: ~2,000 + ~800 = ~2,800 tokens
- 班级群 IM: ~3,000 tokens
- **Total session tokens:** ~14,500 tokens
