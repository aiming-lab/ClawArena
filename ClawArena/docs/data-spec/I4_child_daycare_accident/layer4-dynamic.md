# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger | Goal | Sessions? | Workspace? | Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Lin Yi's detailed wound analysis with medical reasoning | No | Yes: linyi-wound-analysis.md | Seeds C1 medical forensic evidence |
| U2 | Before R7 | Detailed Dou Dou testimony with specifics | Yes: Parent Liu IM Phase 2 | Yes: doudou-detailed-testimony.md | Seeds C4 corroboration |
| U3 | Before R11 | CCTV footage -- phone use confirmed, location confirmed | Yes: Husband IM Phase 2 | Yes: cctv-footage-description.md (replace) | R2->R6 (location), R3->R7 (phone), seeds C4 |
| U4 | Before R21 | Teacher Zhao confession | Yes: Teacher Zhao IM Phase 2 | Yes: teacher-zhao-confession.md | R4->R8 complete; comprehensive |

---

## 2. Action Lists

### Update 1
```json
[{"type": "workspace", "action": "new", "path": "linyi-wound-analysis.md", "source": "updates/linyi-wound-analysis.md"}]
```

### Update 2
```json
[
  {"type": "workspace", "action": "new", "path": "doudou-detailed-testimony.md", "source": "updates/doudou-detailed-testimony.md"},
  {"type": "session", "action": "append", "path": "PLACEHOLDER_PARENT_LIU_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_PARENT_LIU_IM_UUID.jsonl"}
]
```

### Update 3
```json
[
  {"type": "workspace", "action": "replace", "path": "cctv-footage-description.md", "source": "updates/cctv-footage-description.md"},
  {"type": "session", "action": "append", "path": "PLACEHOLDER_HUSBAND_LINWEI_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_HUSBAND_LINWEI_IM_UUID.jsonl"}
]
```

### Update 4
```json
[
  {"type": "workspace", "action": "new", "path": "teacher-zhao-confession.md", "source": "updates/teacher-zhao-confession.md"},
  {"type": "session", "action": "append", "path": "PLACEHOLDER_TEACHER_ZHAO_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_TEACHER_ZHAO_IM_UUID.jsonl"}
]
```

---

## 3. Source File Content Summaries

### linyi-wound-analysis.md (U1)
- Lin Yi's professional wound assessment:
  - 2cm linear laceration, clean edges, right lateral forehead
  - No friction/abrasion marks (rules out slide surface contact)
  - Contusion pattern: single-point impact against straight edge
  - Consistent with: fall onto metal edge of climbing structure
  - Inconsistent with: slide fall (would produce abrasion, not clean laceration)
  - Height estimate: ~80cm fall (consistent with climbing structure, slide is ~120cm)

### doudou-detailed-testimony.md (U2)
- Mother Liu's recording/notes of Dou Dou's account:
  - "乐乐和小明在攀爬架上玩，小明要他的小汽车" (playing on climbing structure, Xiao Ming wanted toy car)
  - "小明推了乐乐，乐乐就摔下来了" (Xiao Ming pushed, Le Le fell)
  - "赵老师不在，她在那边打电话" (Teacher Zhao wasn't there, she was on the phone over there)
  - "后来赵老师听到哭跑过来了" (Then Teacher Zhao heard crying and ran over)
  - Details are specific, consistent, and match wound pattern + location

### cctv-footage-description.md (U3, replaces placeholder)
- CCTV footage review summary:
  - 10:00: Outdoor play begins, Teacher Zhao visible near slide area
  - 10:10: Teacher Zhao answers phone, walks ~5m away from play area
  - 10:10-10:18: Teacher Zhao on phone, back partially turned to children
  - 10:15-10:16: **Climbing structure area partially blocked by tree.** Cannot see the actual fall clearly. But at 10:16, Le Le visible on ground near climbing structure base, NOT near slide.
  - 10:16: Teacher Zhao hears crying, hangs up, runs to Le Le
  - **Key evidence:** (1) Teacher on phone = "I was watching" is false (2) Le Le's location = climbing structure, not slide (3) Push not visible due to tree obstruction

### teacher-zhao-confession.md (U4)
- Teacher Zhao's statement after CCTV review:
  - "对不起，我当时确实在接电话，没有看到乐乐是怎么摔的"
  - "我跑过去的时候他在攀爬架旁边，但我当时以为是从滑梯摔的...因为滑梯就在旁边"
  - "我不应该撒谎说我在看着，我害怕被开除"
  - "张老师请假了就我一个人，我不该接那个电话"
  - Admits: not watching, assumed mechanism, lied out of fear
