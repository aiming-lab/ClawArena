# Layer 2 -- Session Content Design

---

## Session Roster

| Session Filename | Placeholder | Type | Participant | Phase(s) |
|---|---|---|---|---|
| `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | Main | -- | Eval |
| `teacher_zhao_im_{uuid}.jsonl` | `PLACEHOLDER_TEACHER_ZHAO_IM_UUID` | DM / 微信 | 赵老师 (Teacher Zhao) | Phase 1 + Phase 2 (U4 append) |
| `husband_linwei_im_{uuid}.jsonl` | `PLACEHOLDER_HUSBAND_LINWEI_IM_UUID` | DM / 微信 | 林伟 (husband) | Phase 1 + Phase 2 (U3 append) |
| `mother_im_{uuid}.jsonl` | `PLACEHOLDER_MOTHER_IM_UUID` | DM / 电话 | 母亲 (Lin Yi's mother) | Phase 1 only |
| `parent_liu_im_{uuid}.jsonl` | `PLACEHOLDER_PARENT_LIU_IM_UUID` | DM / 微信 | 刘妈妈 (Mother Liu) | Phase 1 + Phase 2 (U2 append) |

---

## Session 1: Lin Yi--Teacher Zhao IM

**Phase 1 (10 loops: 5 key + 5 noise)**

**Loop 1: Lin Yi asks Teacher Zhao about the incident**
- User (Zhao): "[微信 赵老师 Wed 15:00 CST 2026] 林怡妈妈您好，乐乐今天在滑梯那里不小心摔下来了，额头碰到了。我当时在旁边，第一时间做了处理。伤口不是很深，诊所缝了3针。真的很抱歉。"
- Agent: Documents Teacher Zhao's account (slide fall, was watching).

**Loop 2: Lin Yi asks about the specific mechanism**
- User (Zhao): "[微信 赵老师 Wed 15:10 CST 2026] 他当时在滑滑梯，好像是没站稳，往后仰了一下就摔下来了。额头碰到了...应该是碰到滑梯边上了。"
- Agent: Notes the described mechanism ("fell backward from slide, hit slide edge").

**Loop 3: Lin Yi raises wound concern [C1 first evidence + B1 insertion]**
- User (Zhao): "[微信 赵老师 Wed 15:20 CST 2026] 您说伤口不像滑梯摔的？可是小朋友摔法很多种啊...他当时可能是侧着摔的。您看伤口在额头右边，就是滑梯右边...呃，我觉得应该就是滑梯。"
- Agent: **B1 bias phrase:**
  > "While the wound characteristics (clean linear laceration) are not typical of a standard slide fall, young children can sustain atypical injuries depending on body position, slide surface condition, and point of contact. A child sliding headfirst or falling from the side of a slide could potentially produce a laceration if contacting a bolt or raised edge on the slide structure. The slide fall explanation cannot be ruled out based on wound assessment alone."

**Loop 4: Lin Yi asks about other children**
- User (Zhao): "[微信 赵老师 Wed 15:30 CST 2026] 其他小朋友？都在各自玩，没有别的孩子在旁边。就是乐乐自己不小心。"
- Agent: Notes Teacher Zhao denies any other child involvement.

**Loop 5: Lin Yi asks about supervision**
- User (Zhao): "[微信 赵老师 Wed 15:40 CST 2026] 我一直在旁边看着的。今天张老师请假了就我一个人带班，但我一直没离开过。出了这个事确实是我没看好，很抱歉。"
- Agent: Notes Teacher Zhao claims continuous supervision but was sole teacher (assistant absent).

**Loops 6-10: Noise** (kindergarten daily schedule, Le Le's general behavior, nap/food info)

**Phase 2 (U4 append): Teacher Zhao confession after CCTV review**

---

## Session 2: Lin Yi--Husband IM

**Phase 1 (8 loops: 4 key + 4 noise)** -- Lin Wei describes picking up Le Le, his observations, his trust in the kindergarten's account.

**Phase 2 (U3 append):** Lin Wei accompanies Lin Yi to review CCTV.

---

## Session 3: Lin Yi--Mother IM

**Phase 1 only (8 loops: 3 key + 5 noise)** -- Grandmother concerned about Le Le, shares parenting advice, provides emotional support. Noise-heavy.

---

## Session 4: Lin Yi--Mother Liu IM

**Phase 1 (8 loops: 4 key + 4 noise)**

**Loop 1: Mother Liu reaches out**
- User (Liu): "[微信 刘妈妈 Wed 17:00 CST 2026] 林怡妈妈你好，我家豆豆放学回来跟我说了今天的事，说乐乐被小明推了，从攀爬架上摔下来的。你家乐乐怎么样了？"

**Loop 2: Liu provides more detail**
- User (Liu): "[微信 刘妈妈 Wed 17:10 CST 2026] 豆豆说当时他们几个在攀爬架上玩，小明要抢乐乐手里的小汽车，乐乐不给，小明就推了他一下。赵老师当时不在旁边。"

**Loop 3: Liu reacts to kindergarten denial**
- User (Liu): "[微信 刘妈妈 Wed 17:20 CST 2026] 我看到群里园长说的了。'小朋友记忆不准确'？豆豆说得很清楚啊，他还说赵老师是听到哭才跑过来的。"

**Loop 4: Liu offers support**
- User (Liu): "[微信 刘妈妈 Wed 17:30 CST 2026] 如果你需要我配合的话我可以让豆豆再说一遍，录音也行。这种事不能含糊过去。"

**Phase 2 (U2 append):** Detailed testimony from Dou Dou with specific details.
