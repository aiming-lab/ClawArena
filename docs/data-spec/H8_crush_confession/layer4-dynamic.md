# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver Li Hao's baseline engagement analysis -- proves C4 (engagement not special) and seeds B1 challenge | Yes: Li Hao IM Phase 2 append | Yes: lihao-baseline-analysis.md | R4->R8 (C4: engagement is baseline, not special) |
| U2 | Before R7 | Deliver project deadline context -- reinforces C3 (shared activities) and explains some recent communication | No | Yes: project-deadline-context.md | No direct reversal; strengthens C3 |
| U3 | Before R11 | Deliver Zhang Zixuan's contradictory intel -- triggers C2 full contradiction and B2 challenge | Yes: Zhang Zixuan IM Phase 2 append | Yes: friend-intel-summary.md (replaced with updated version) | R3->R7 (C2: intel source formally unreliable) |
| U4 | Before R21 | Deliver Lin Yutong's direct conversation -- triggers C1 resolution (exam prep confirmed) and B1/B2 full reversal | No | Yes: linyutong-direct-convo.md | R2->R6 (C1: frequency was exam-driven); B1 full reversal; B2 full reversal |

---

## 2. Action Lists

### Update 1 (before R5)

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "lihao-baseline-analysis.md",
    "source": "updates/lihao-baseline-analysis.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LIHAO_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LIHAO_IM_UUID.jsonl"
  }
]
```

### Update 2 (before R7)

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "project-deadline-context.md",
    "source": "updates/project-deadline-context.md"
  }
]
```

### Update 3 (before R11)

```json
[
  {
    "type": "workspace",
    "action": "replace",
    "path": "friend-intel-summary.md",
    "source": "updates/friend-intel-summary.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHANGZIXUAN_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHANGZIXUAN_IM_UUID.jsonl"
  }
]
```

### Update 4 (before R21)

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "linyutong-direct-convo.md",
    "source": "updates/linyutong-direct-convo.md"
  }
]
```

---

## 3. Source File Content Summaries

### updates/lihao-baseline-analysis.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C4 (definitive resolution)
**Content key points:**
- Title: "朋友圈互动基线分析 -- 李浩整理"
- Li Hao's comparative data: Lin Yutong's Moments engagement across 15+ friends in the same week
- Engagement with Wang Ming: 3 likes, 2 comments
- Engagement with others: 小赵 4 likes 2 comments, 班长 3 likes 1 comment, 学委 2 likes 2 comments, etc.
- Average across sample: ~2.5 likes, ~1.5 comments per person
- Wang Ming is within 1 standard deviation of the mean -- not an outlier
- Conclusion: her engagement is uniformly warm, not special

**Length estimate:** ~400 words, ~600 tokens

---

### updates/project-deadline-context.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C3 (reinforcement)
**Content key points:**
- Title: "英语课项目进度 -- Group 3 (包含王明、林雨桐)"
- Project deadline: Mar 28 presentation
- Group members: Wang Ming, Lin Yutong, + 2 others
- Recent messages about project: topic assignments, source sharing, rehearsal scheduling
- Some of Lin Yutong's recent messages to Wang Ming were about project coordination
- Project provides legitimate collaborative context

**Length estimate:** ~300 words, ~450 tokens

---

### updates/friend-intel-summary.md (Update 3)

**File type:** workspace replace (adds Zhang Zixuan's contradictory report)
**Associated contradictions:** C2 (contradiction formalized)
**Content key points:**
- Same as initial version PLUS new entry:
- **Mar 24 (张子轩):** "陈雯说林雨桐好像在追一个学长，数学系大三的。" CONTRADICTS Mar 15 entry.
- Note: Zhang Zixuan's two reports from the same source (roommate Chen Wen) give opposite signals. Source reliability = LOW.

**Length estimate:** ~600 words, ~900 tokens

---

### updates/linyutong-direct-convo.md (Update 4)

**File type:** workspace new
**Associated contradictions:** C1 (resolution), C2 (partial resolution)
**Content key points:**
- Title: "与林雨桐直接对话记录 -- 2026-03-26"
- Wang Ming asks about the cafe photo person
- Lin Yutong: "那是我高中闺蜜（男的），从小一起长大的，他来成都玩我带他逛。"
- Lin Yutong: "最近考完试轻松了，不用天天问你数学题了哈哈。谢谢你之前帮我复习！"
- Lin Yutong mentions the English project: "对了project的事周五rehearsal你能来吗？"
- Tone: friendly, grateful, casual. No flirtatious signals. Consistent with platonic friendship.
- **Ground truth from Lin Yutong herself:** messaging was for exam prep, cafe person is platonic friend, she appreciates Wang Ming's help.

**Length estimate:** ~400 words, ~600 tokens

---

## 4. Runtime Checks

| Check | What to Verify |
|---|---|
| Post-U1 | lihao-baseline-analysis.md accessible; Li Hao IM has baseline discussion |
| Post-U2 | project-deadline-context.md accessible |
| Post-U3 | friend-intel-summary.md updated with contradictory entry; Zhang Zixuan IM has new loops |
| Post-U4 | linyutong-direct-convo.md accessible; C1 and C2 evidence complete |
