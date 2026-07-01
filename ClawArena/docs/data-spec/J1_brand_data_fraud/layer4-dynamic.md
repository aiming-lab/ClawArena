# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver brand-received-data.md (screenshot evidence) + 赵敏's material sharing | Yes: 赵敏 DM Phase 2 append (Loop 9-10) | Yes: brand-received-data.md | R1->R5 (C1: unverifiable screenshot + inflated data confirmed) |
| U2 | Before R6 | Deliver mcn-contract-excerpt.md (verified data requirement) | No new sessions | Yes: mcn-contract-excerpt.md | R2->R6 (C2/C4: contract defines data standard; MCN violates it) |
| U3 | Before R11 | Deliver 刘姐's admission ("内部估算") | Yes: 刘姐 DM Phase 2 append (Loop 13-16) | No | R8->R11 seed (C2 full: "different metrics" collapses; C4: contract violation confirmed by admission) |
| U4 | Before R21 | Deliver cross-platform + cross-creator pattern + group chat | Yes: 赵敏 DM Phase 2 append (Loop 11-12), Creator group Phase 2 append (Loop 11-14) | No | R8->R11 full (B2 "industry practice" refuted by systematic pattern); comprehensive R21-R30 |

---

## 2. Action Lists

### Update 1 (before R5)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "brand-received-data.md",
    "source": "updates/brand-received-data.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHAOMIN_WECHAT_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHAOMIN_WECHAT_UUID_u1.jsonl"
  }
]
```

### Update 2 (before R6)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "mcn-contract-excerpt.md",
    "source": "updates/mcn-contract-excerpt.md"
  }
]
```

### Update 3 (before R11)
```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LIUJIE_WECHAT_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LIUJIE_WECHAT_UUID.jsonl"
  }
]
```

### Update 4 (before R21)
```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHAOMIN_WECHAT_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHAOMIN_WECHAT_UUID_u4.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CREATOR_GROUP_UUID.jsonl",
    "source": "updates/PLACEHOLDER_CREATOR_GROUP_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/brand-received-data.md (Update 1)
**Associated contradictions:** C1 (unverifiable format), C4 (screenshot vs verified data)
- Brand materials forwarded by 赵敏
- Screenshot image of purported 小红书 backend showing 120K
- No API export, no backend link, no verification token
- 赵敏's note about trust-based process
- **Length:** ~400 words, ~600 tokens

### updates/PLACEHOLDER_ZHAOMIN_WECHAT_UUID_u1.jsonl (Update 1)
**Associated contradictions:** C1 (brand cooperation)
- Loops 9-10: 赵敏 shares materials, acknowledges verification gap
- **Length:** ~300 words, ~450 tokens

### updates/mcn-contract-excerpt.md (Update 2)
**Associated contradictions:** C4 (verified data definition)
- Contract clauses 7.3 (data standard), 4.2 (brand agreement), 9.1 (termination right)
- Explicitly excludes screenshots from "verified data"
- **Length:** ~400 words, ~600 tokens

### updates/PLACEHOLDER_LIUJIE_WECHAT_UUID.jsonl (Update 3)
**Associated contradictions:** C2 (admission destroys "different metrics"), C4 (contract violation confirmed)
- Loops 13-16: 刘姐 admits "内部估算", defends as "industry practice", appeals to relationship, 周芳 maintains position
- **Length:** ~800 words, ~1,200 tokens

### updates/PLACEHOLDER_ZHAOMIN_WECHAT_UUID_u4.jsonl (Update 4)
**Associated contradictions:** Pattern evidence (cross-creator)
- Loops 11-12: 赵敏 reveals 小林's similar data discrepancy (30K->70K), brand's remediation plan
- **Length:** ~300 words, ~450 tokens

### updates/PLACEHOLDER_CREATOR_GROUP_UUID.jsonl (Update 4)
**Associated contradictions:** B1 correction (public), pattern evidence (cross-creator validation)
- Loops 11-14: 周芳 shares findings, 小林 confirms, 创作者A provides context ("20-30% is common, 2x+ is extreme"), 周芳 advises evidence preservation
- **Length:** ~400 words, ~600 tokens

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
  - U1: appends to PLACEHOLDER_ZHAOMIN_WECHAT_UUID
  - U3: appends to PLACEHOLDER_LIUJIE_WECHAT_UUID
  - U4: appends to PLACEHOLDER_ZHAOMIN_WECHAT_UUID and PLACEHOLDER_CREATOR_GROUP_UUID
- [x] All workspace files described in layer1
- [x] Updates support intended reversals
  - U1 -> C1 screenshot evidence (R1->R5)
  - U2 -> C4 contract definition (R2->R6)
  - U3 -> C2 admission (R8->R11 seed)
  - U4 -> Cross-platform + cross-creator pattern (R8->R11 full)
- [x] Numbers consistent across all sources
  - XHS views: 50,234 (platform) vs 120,000 (MCN) = 2.39x
  - XHS likes: 3,812 vs 8,500 = 2.23x
  - XHS saves: 1,423 vs 3,200 = 2.25x
  - Bilibili views: 32,178 vs 65,000 = 2.02x
  - 小林 XHS: 30K vs 70K = 2.33x
  - Growth curve: Day 18 = 45K, Day 23 = 50K
- [x] Contract clauses: 7.3 (data standard), 4.2 (brand agreement), 9.1 (termination)
- [x] Timeline: Published Feb 15, MCN report Mar 5, analytics export Mar 10

---

## 5. questions.json Update Fields

### R5:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "brand-received-data.md", "source": "updates/brand-received-data.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHAOMIN_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHAOMIN_WECHAT_UUID_u1.jsonl" }
]
```

### R6:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "mcn-contract-excerpt.md", "source": "updates/mcn-contract-excerpt.md" }
]
```

### R11:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LIUJIE_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_LIUJIE_WECHAT_UUID.jsonl" }
]
```

### R21:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHAOMIN_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHAOMIN_WECHAT_UUID_u4.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CREATOR_GROUP_UUID.jsonl", "source": "updates/PLACEHOLDER_CREATOR_GROUP_UUID.jsonl" }
]
```
