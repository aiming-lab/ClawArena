# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger | Goal | New Sessions? | New Workspace? | Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Itinerary confirms signage existed; regulation weight established | No | No (data in initial files) | R1->R5 |
| U2 | Before R6 | mcn-legal-response.md (inadequate legal advice) | No | Yes: mcn-legal-response.md | R2->R6 |
| U3 | Before R8 | 阿杰 expert advice on formal procedure | Yes: 阿杰 Phase 2 | No | R8->R11 seed |
| U4 | Before R21 | 父亲 legal analysis + comprehensive | Yes: 父亲 Phase 2 | No | R8->R11 full |

---

## 2. Action Lists

### Update 1 (before R5)
```json
[]
```
*(Reversal uses initial files already available; interpretive.)*

### Update 2 (before R6)
```json
[
  { "type": "workspace", "action": "new", "path": "mcn-legal-response.md", "source": "updates/mcn-legal-response.md" }
]
```

### Update 3 (before R8)
```json
[
  { "type": "session", "action": "append", "path": "PLACEHOLDER_AJIE_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_AJIE_WECHAT_UUID.jsonl" }
]
```

### Update 4 (before R21)
```json
[
  { "type": "session", "action": "append", "path": "PLACEHOLDER_FATHER_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_FATHER_WECHAT_UUID.jsonl" }
]
```

---

## 4. Runtime Checks

- [x] 14-day deadline from warning letter
- [x] Filming date: March 5, location: Kiyomizu-dera (清水寺)
- [x] Warning letter from: 京都市文化財保護課
- [x] Permit fee range: ¥5,000-¥20,000 JPY
- [x] Signage: Japanese only, A4 size, at ticket counter side
- [x] Travel agency said "no restrictions"; regulation says "commercial permit required"
- [x] MCN says "apologize"; warning letter says "formal written explanation within 14 days"
- [x] Equipment: Sony A7IV + stabilizer (not tripod)

---

## 5. questions.json Update Fields

### R5:
```json
"update": []
```

### R6:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "mcn-legal-response.md", "source": "updates/mcn-legal-response.md" }
]
```

### R8:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_AJIE_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_AJIE_WECHAT_UUID.jsonl" }
]
```

### R21:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_FATHER_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_FATHER_WECHAT_UUID.jsonl" }
]
```
