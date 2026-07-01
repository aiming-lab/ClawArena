# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Li Hao's statement confirming card borrowing -- resolves C1 | Yes: Li Hao IM Phase 2 append | Yes: lihao-statement.md | R2->R5 (C1: access log was Li Hao, not Wang Ming) |
| U2 | Before R7 | Package station camera showing Zhang Wei from 314 -- resolves C2 | Yes: RA IM Phase 2 append | Yes: package-station-camera.md | R3->R7 (C2: package was mistaken pickup) |
| U3 | Before R11 | Liu Chen's bookstore receipt correcting amount to ¥200 | Yes: Liu Chen IM Phase 2 append | Yes: bookstore-receipt.md | R4->R9 seed (C4: amount was ¥200 not ¥500) |
| U4 | Before R21 | Lost-and-found ¥200 found by cleaning staff -- resolves C4 | Yes: RA IM Phase 2 append (final) | Yes: campus-lost-found.md (replaced with updated version) | R4->R9 complete (C4: money found, no theft) |

---

## 2. Action Lists

### Update 1 (before R5)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "lihao-statement.md",
    "source": "updates/lihao-statement.md"
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
    "path": "package-station-camera.md",
    "source": "updates/package-station-camera.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_RA_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_RA_IM_UUID_part1.jsonl"
  }
]
```

### Update 3 (before R11)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "bookstore-receipt.md",
    "source": "updates/bookstore-receipt.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LIUCHEN_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LIUCHEN_IM_UUID.jsonl"
  }
]
```

### Update 4 (before R21)
```json
[
  {
    "type": "workspace",
    "action": "replace",
    "path": "campus-lost-found.md",
    "source": "updates/campus-lost-found.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_RA_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_RA_IM_UUID_part2.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/lihao-statement.md (U1)
- Li Hao's written statement confirming card borrowing, 10:15 building swipe, 10:20 canteen payment, visit to Room 208 only.
- ~750 tokens

### updates/package-station-camera.md (U2)
- Station camera description: person at 10:30 wearing 314 basketball jacket. Station manager confirms Zhang Wei. Package returned Saturday.
- ~600 tokens

### updates/bookstore-receipt.md (U3)
- Campus bookstore receipt: March 17, ¥100 cash, notebooks + folder. Liu Chen confirms he forgot this purchase.
- ~450 tokens

### updates/campus-lost-found.md (U4)
- Updated lost-and-found with new entry: "03-20 10:45: ¥200 cash, 3rd floor hallway outside Room 312, found by cleaning staff."
- ~525 tokens

---

## 4. Runtime Checks

- [x] Session appends use correct UUIDs
- [x] All workspace files described in layer1
- [x] Updates support reversals:
  - U1 -> C1 (card was Li Hao's usage)
  - U2 -> C2 (package was Zhang Wei's mistake)
  - U3 -> C4 partial (amount corrected ¥500→¥200)
  - U4 -> C4 complete (¥200 found in lost-and-found)
- [x] Factual consistency:
  - Wang Ming enters: ~10:00 (CCTV, no swipe)
  - Wang Ming exits: ~10:10 (CCTV)
  - Li Hao swipes: 10:15:23 (access log = CCTV ~10:14:30)
  - Li Hao canteen: 10:20:15 (canteen log)
  - Li Hao exits: ~10:25 (CCTV)
  - Package pickup: 10:30:45 (Zhang Wei using 312 code)
  - Cleaning finds cash: ~10:45
  - Liu Chen returns: 11:02 (access log + CCTV)
  - Cash: ¥300 deposited - ¥100 bookstore = ¥200 actual
  - Lost-and-found: ¥200

---

## 5. questions.json Update Fields

### R5: `"update": [lihao-statement.md new, LIHAO_IM append]`
### R7: `"update": [package-station-camera.md new, RA_IM append]`
### R11: `"update": [bookstore-receipt.md new, LIUCHEN_IM append]`
### R21: `"update": [campus-lost-found.md replace, RA_IM append]`
