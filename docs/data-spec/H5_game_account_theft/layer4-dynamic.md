# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | IP definitively matched to internet cafe -- resolves C1 | Yes: 阿杰 IM Phase 2 append | Yes: ip-cafe-confirmation.md | R2->R5 (C1: "unknown" IP is the cafe) |
| U2 | Before R7 | Li Hao confirms forgot-to-logout -- resolves C2 | Yes: Li Hao IM Phase 2 (new session) | Yes: lihao-witness-statement.md | R3->R7 (C2: simple explanation confirmed) |
| U3 | Before R11 | CS hotline reveals no review initiated -- resolves C4 | Yes: CS IM Phase 2 append | Yes: cs-hotline-transcript.md | R6->R9 (C4: "reviewing" was template) |
| U4 | Before R21 | Cafe PC management log confirms session persistence bug | No | Yes: cafe-pc-management-log.md | Enables comprehensive R21-R30 |

---

## 2. Action Lists

### Update 1 (before R5)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "ip-cafe-confirmation.md",
    "source": "updates/ip-cafe-confirmation.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_AJIE_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_AJIE_IM_UUID.jsonl"
  }
]
```

### Update 2 (before R7)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "lihao-witness-statement.md",
    "source": "updates/lihao-witness-statement.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LIHAO_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LIHAO_IM_UUID.jsonl"
  }
]
```

### Update 3 (before R11)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "cs-hotline-transcript.md",
    "source": "updates/cs-hotline-transcript.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CS_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_CS_IM_UUID.jsonl"
  }
]
```

### Update 4 (before R21)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "cafe-pc-management-log.md",
    "source": "updates/cafe-pc-management-log.md"
  }
]
```

---

## 3. Source File Content Summaries

### updates/ip-cafe-confirmation.md (U1)
- Definitive IP match: 183.221.67.45 = 极速网咖
- Forum post corroboration + address match
- Same IP in both Sat 14:02 (Wang Ming) and Sun 03:47 (suspicious) entries
- ~600 tokens

### updates/PLACEHOLDER_AJIE_IM_UUID.jsonl (U1)
- Loops 11-12: Ajie learns about IP match, reluctantly considers simpler explanation, mentions cafe PCs not auto-restarting
- ~500 tokens

### updates/lihao-witness-statement.md (U2)
- Li Hao's written statement: confirmed at cafe, Wang Ming did not log out, Li Hao warned him, Wang Ming said "auto-disconnect"
- ~600 tokens

### updates/PLACEHOLDER_LIHAO_IM_UUID.jsonl (U2)
- Loops 1-4: Li Hao confirms cafe visit, logout failure, no password sharing, straightforward conclusion
- ~800 tokens

### updates/cs-hotline-transcript.md (U3)
- Hotline transcript: ticket in queue, not assigned, 7-10 day backlog, "auto-reply is template"
- ~600 tokens

### updates/PLACEHOLDER_CS_IM_UUID.jsonl (U3)
- Loops 7-8: Hotline reveals truth, Wang Ming reacts, CS suggests evaluating whether to keep ticket open
- ~500 tokens

### updates/cafe-pc-management-log.md (U4)
- PC #23 session timer disabled since March 15 maintenance
- Session persisted past 17:30; next user at 21:45 found game running
- Definitive technical proof of the session persistence
- ~750 tokens

---

## 4. Runtime Checks

- [x] Session UUIDs consistent
- [x] All workspace files described in layer1
- [x] Updates support reversals:
  - U1 -> C1 (IP = cafe)
  - U2 -> C2 (forgot to logout, witnessed)
  - U3 -> C4 (CS template, not reviewing)
  - U4 -> Technical proof (PC #23 bug)
- [x] Factual consistency:
  - Wang Ming cafe login: Sat 14:02, IP 183.221.67.45
  - Wang Ming leaves: Sat 17:30 (no logout)
  - Session refresh: Sun 03:47, same IP
  - Wang Ming discovers: Sun 08:00 (force disconnect)
  - Wang Ming password change: Sun 08:15 (campus IP)
  - CS ticket: Sun 10:00
  - IP confirmed: Sun 14:00
  - Li Hao confirms: Mon 10:00
  - Hotline call: Mon 14:15
  - PC #23: auto-restart disabled since Mar 15
  - Next user on PC #23: Sat 21:45

---

## 5. questions.json Update Fields

### R5: `"update": [ip-cafe-confirmation.md new, AJIE_IM append]`
### R7: `"update": [lihao-witness-statement.md new, LIHAO_IM append]`
### R11: `"update": [cs-hotline-transcript.md new, CS_IM append]`
### R21: `"update": [cafe-pc-management-log.md new]`
