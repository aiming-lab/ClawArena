# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | bank-payment-records.md (周芳 only received ¥3,240) | No | Yes: bank-payment-records.md | R1->R5 |
| U2 | Before R6 | mcn-contract-excerpt.md (no management fee clause) + brand confirms full payment | Yes: 张品牌 email append (Loop 7-8) | Yes: mcn-contract-excerpt.md | R2->R6 |
| U3 | Before R8 | 李姐 admits management fee is "new, not yet in contract" | Yes: 李姐 IM Phase 2 append (Loop 13-16) | No | R8->R11 seed |
| U4 | Before R21 | Complete fund flow analysis | No | No | R8->R11 full; comprehensive |

---

## 2. Action Lists

### Update 1 (before R5)
```json
[
  { "type": "workspace", "action": "new", "path": "bank-payment-records.md", "source": "updates/bank-payment-records.md" }
]
```

### Update 2 (before R6)
```json
[
  { "type": "workspace", "action": "new", "path": "mcn-contract-excerpt.md", "source": "updates/mcn-contract-excerpt.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHANGBRAND_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANGBRAND_EMAIL_UUID_u2.jsonl" }
]
```

### Update 3 (before R8)
```json
[
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LIJIE_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_LIJIE_WECHAT_UUID.jsonl" }
]
```

### Update 4 (before R21)
```json
[]
```

---

## 4. Runtime Checks

- [x] Numbers consistent: Invoice ¥4,800 (¥4,248+¥552). MCN pre-tax ¥3,600. Fee ¥360. Net ¥3,240. Brand ¥5,000. Brand total ¥25,000. MCN commission ¥5,000.
- [x] Travel dates: 2026-03-10 to 03-14 (consistent everywhere)
- [x] Fund flow: Brand→MCN ¥5,000 → MCN retains ¥1,760 → 周芳 ¥3,240
- [x] Contract: 5.2 (commission from brand payment), 5.4 (actual expense reimbursement per receipts), no management fee

---

## 5. questions.json Update Fields

### R5:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "bank-payment-records.md", "source": "updates/bank-payment-records.md" }
]
```

### R6:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "mcn-contract-excerpt.md", "source": "updates/mcn-contract-excerpt.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHANGBRAND_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANGBRAND_EMAIL_UUID_u2.jsonl" }
]
```

### R8:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LIJIE_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_LIJIE_WECHAT_UUID.jsonl" }
]
```
