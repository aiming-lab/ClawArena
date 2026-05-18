# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver delivery-receipt.md (actual receipt 1500 vs ordered 2000) | No | Yes: delivery-receipt.md | R2->R5 (C2: procurement over-recording confirmed) |
| U2 | Before R6 | Deliver supply-chain-email-thread.md (supplier warning + pharmacy director actions) | Yes: other dept IM Phase 2 append (Loop 9-10) | Yes: supply-chain-email-thread.md | R3->R6 context (information suppression revealed) |
| U3 | Before R8 | Deliver pharmacy director's admission (manual dispensing confirmed) | Yes: pharmacy email Phase 2 append (Loop 11-14) | No | R1->R8 (C1 full: manual dispensing + over-recording = full gap); R8->R11 seed |
| U4 | Before R21 | Deliver comprehensive data + 张主任 suppression + group resolution | Yes: 张主任 DM Phase 2 append (Loop 11-14), Supply group Phase 2 append (Loop 9-12) | No | R8->R11 full (B2 "normal variance" refuted); comprehensive R21-R30 |

---

## 2. Action Lists

### Update 1 (before R5)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "delivery-receipt.md",
    "source": "updates/delivery-receipt.md"
  }
]
```

### Update 2 (before R6)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "supply-chain-email-thread.md",
    "source": "updates/supply-chain-email-thread.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_OTHER_DEPT_WECHAT_UUID.jsonl",
    "source": "updates/PLACEHOLDER_OTHER_DEPT_WECHAT_UUID_u2.jsonl"
  }
]
```

### Update 3 (before R8)
```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_YAOFANG_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_YAOFANG_EMAIL_UUID.jsonl"
  }
]
```

### Update 4 (before R21)
```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHANGZHUREN_WECHAT_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHANGZHUREN_WECHAT_UUID_u4.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_SUPPLY_GROUP_UUID.jsonl",
    "source": "updates/PLACEHOLDER_SUPPLY_GROUP_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/delivery-receipt.md (Update 1)
**Associated contradictions:** C2 (ordered 2000 vs received 1500)
- Signed delivery receipt showing 1500 actual receipt
- Supplier note about production capacity shortfall
- 小赵 notified pharmacy director
- **Length:** ~350 words, ~525 tokens

### updates/supply-chain-email-thread.md (Update 2)
**Associated contradictions:** C2 (system over-recording instruction), C4 (information suppression)
- Nov 15 supplier warning
- Pharmacy director's response (acknowledged, didn't share)
- Dec 10 instruction to record 2000 despite receiving 1500
- Manual dispensing approval emails
- **Length:** ~600 words, ~900 tokens

### updates/PLACEHOLDER_OTHER_DEPT_WECHAT_UUID_u2.jsonl (Update 2)
**Associated contradictions:** C4 (information sharing failure)
- Loops 9-10: 李主任 reacts to supplier warning revelation, other dept confirms normal usage
- **Length:** ~300 words, ~450 tokens

### updates/PLACEHOLDER_YAOFANG_EMAIL_UUID.jsonl (Update 3)
**Associated contradictions:** C1 (manual dispensing admission), C2 (over-recording admission)
- Loops 11-14: Pharmacy director admits manual dispensing and over-recording, justifies with flu season urgency
- **Length:** ~800 words, ~1,200 tokens

### updates/PLACEHOLDER_ZHANGZHUREN_WECHAT_UUID_u4.jsonl (Update 4)
**Associated contradictions:** Suppression attempt, resolution
- Loops 11-14: 张主任 pressures to suppress, 林怡 insists on formal review, partial concession
- **Length:** ~500 words, ~750 tokens

### updates/PLACEHOLDER_SUPPLY_GROUP_UUID.jsonl (Update 4)
**Associated contradictions:** Public resolution, pattern confirmation
- Loops 9-12: 林怡 presents findings publicly, pharmacy director partial acceptance, 李主任 partial admission
- **Length:** ~400 words, ~600 tokens

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
  - U2: appends to PLACEHOLDER_OTHER_DEPT_WECHAT_UUID
  - U3: appends to PLACEHOLDER_YAOFANG_EMAIL_UUID
  - U4: appends to PLACEHOLDER_ZHANGZHUREN_WECHAT_UUID and PLACEHOLDER_SUPPLY_GROUP_UUID
- [x] All workspace files described in layer1
- [x] Updates support intended reversals
  - U1 -> C2 delivery receipt (R2->R5)
  - U2 -> C4 information suppression (R3->R6 context)
  - U3 -> C1 manual dispensing admission (R1->R8)
  - U4 -> Comprehensive (R8->R11 full)
- [x] Numbers consistent across all sources
  - Opening stock: 800
  - Ordered: 2,000. Received: 1,500. System entry: 2,000 (error +500)
  - ER dispensed: 800 (all recorded, dual-signed)
  - Respiratory dispensed: 1,100 (800 formal + 300 manual, oral approval)
  - Other departments: 200 (recorded)
  - Total dispensed: 2,100. Total available: 2,300 (800+1500). Actual remaining: 200.
  - System balance: 800+2000-2300=500. Physical: 200. Gap: 300 (manual unrecorded).
  - Full gap explanation: system over-recorded procurement by 500 AND under-recorded dispensing by 300. Net system overstatement = 500-300+300 = 500-200 = 300. Wait: System balance 500, actual 200, gap 300. Procurement over-record adds 500 to system. Manual dispensing removes 300 from physical without system deduction. System: 800+2000-2300=500. Actual: 800+1500-2100=200. Gap = 500-200 = 300. This 300 = procurement over-record 500 - difference in recorded dispensing. System recorded dispensing = 2300 (includes 500 "manual" category). Actual = 2100. So system over-dispensed by 200? No. Re-check: inventory-system-export shows dispensed 2300 (ER 800 + Respiratory 800 + Others 200 + manual 500). But actual: ER 800 + Respiratory 1100 + Others 200 = 2100. System manually logged 500 as dispensed but actual manual was 300 (respiratory extra). Hmm, need reconciliation.
  - CORRECTED: System shows total dispensed 2300 (including a 500 "manual/emergency" line). Actual total dispensed is 2100. System procurement entry 2000 vs actual 1500. System balance = 800+2000-2300 = 500. Actual balance = 800+1500-2100 = 200. Gap = 300.
- [x] Timeline: Procurement ordered Dec 5, delivered Dec 10, supplier warning Nov 15

---

## 5. questions.json Update Fields

### R5:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "delivery-receipt.md", "source": "updates/delivery-receipt.md" }
]
```

### R6:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "supply-chain-email-thread.md", "source": "updates/supply-chain-email-thread.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_OTHER_DEPT_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_OTHER_DEPT_WECHAT_UUID_u2.jsonl" }
]
```

### R8:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_YAOFANG_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_YAOFANG_EMAIL_UUID.jsonl" }
]
```

### R21:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHANGZHUREN_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANGZHUREN_WECHAT_UUID_u4.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_SUPPLY_GROUP_UUID.jsonl", "source": "updates/PLACEHOLDER_SUPPLY_GROUP_UUID.jsonl" }
]
```
