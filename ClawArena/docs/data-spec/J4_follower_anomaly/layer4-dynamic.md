# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | platform-announcement.md (cleanup timing match) | No | Yes | R1->R5 (83% cleared = bot) |
| U2 | Before R6 | follower-demographics.md (detailed demographic mismatch) | No | Yes | R2->R6 |
| U3 | Before R8 | 小美 confirms same-day +3000 (cross-creator) | Yes: 小美 Phase 2 | No | R8->R11 seed |
| U4 | Before R21 | 李姐 indirect admission + comprehensive | Yes: 李姐 Phase 2 | No | R8->R11 full |

---

## 2. Action Lists

### Update 1 (before R5)
```json
[
  { "type": "workspace", "action": "new", "path": "platform-announcement.md", "source": "updates/platform-announcement.md" }
]
```

### Update 2 (before R6)
```json
[
  { "type": "workspace", "action": "new", "path": "follower-demographics.md", "source": "updates/follower-demographics.md" }
]
```

### Update 3 (before R8)
```json
[
  { "type": "session", "action": "append", "path": "PLACEHOLDER_XIAOMEI_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_XIAOMEI_WECHAT_UUID.jsonl" }
]
```

### Update 4 (before R21)
```json
[
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LIJIE_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_LIJIE_WECHAT_UUID.jsonl" }
]
```

---

## 4. Runtime Checks

- [x] Numbers: +3,012 gain, -2,500 loss (83% cleared), 78% bot indicators, 小美 +3,000/-2,400 (80% cleared)
- [x] Timing: growth 3/15 2-5AM, cleanup 3/18, announcement 3/18
- [x] MCN growth report: no campaign for 3/15 period
- [x] 周芳 base: ~52K pre-spike, normal daily +20-50
