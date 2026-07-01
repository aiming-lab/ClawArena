# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger | Goal | New Sessions? | New Workspace? | Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Batch timeline confirmation + regulator weight | No | No (data in initial files) | R1->R5 |
| U2 | Before R6 | mcn-legal-response.md (contract 30-day clause) | Yes: 李姐 Phase 2 | Yes: mcn-legal-response.md | R2->R6 |
| U3 | Before R8 | Brand settlement proposal (封口协议) | Yes: 张品牌 Phase 2 | No | R8->R11 seed |
| U4 | Before R21 | Fan comment escalation + comprehensive | Yes: 粉丝群 Phase 2 | No | R8->R11 full |

---

## 2. Action Lists

### Update 1 (before R5)
```json
[]
```
*(Regulator vs brand reversal uses initial files already available; update is interpretive.)*

### Update 2 (before R6)
```json
[
  { "type": "workspace", "action": "new", "path": "mcn-legal-response.md", "source": "updates/mcn-legal-response.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LIJIE_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_LIJIE_WECHAT_UUID_u2.jsonl" }
]
```

### Update 3 (before R8)
```json
[
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHANGBRAND_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANGBRAND_EMAIL_UUID_u3.jsonl" }
]
```

### Update 4 (before R21)
```json
[
  { "type": "session", "action": "append", "path": "PLACEHOLDER_FANGROUP_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_FANGROUP_WECHAT_UUID.jsonl" }
]
```

---

## 4. Runtime Checks

- [x] E.coli: brand <10 CFU/g vs consumer 230/380/510 CFU/g vs standard 100 CFU/g
- [x] Batch: BN-20260201 within recall BN-20260115~BN-20260228
- [x] Contract: clause 8.3 (30-day notice), 8.4 (creator right to demand explanation)
- [x] Regulator: "systemic," "multiple batches," "3 production lines," "停产整改"
