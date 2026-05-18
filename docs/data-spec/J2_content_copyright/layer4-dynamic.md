# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver platform-report-record.md (rejection) | Yes: platform email append | Yes: platform-report-record.md | R1->R5 (C4: platform standard identified) |
| U2 | Before R6 | Deliver original-footage-metadata.md (identical camera settings) | No | Yes: original-footage-metadata.md | R2->R6 (C2/C4: metadata contradicts "coincidence" and exceeds platform evidence standard) |
| U3 | Before R8 | Deliver scene element evidence (flower vase + napkin) | Yes: 老王 DM Phase 2 append (Loop 11-12) | No | R8->R11 seed |
| U4 | Before R21 | Deliver prior complaint pattern (美食小K history) | Yes: 室友 DM Phase 2 append (Loop 7-8) | No | R8->R11 full; comprehensive R21-R30 |

---

## 2. Action Lists

### Update 1 (before R5)
```json
[
  { "type": "workspace", "action": "new", "path": "platform-report-record.md", "source": "updates/platform-report-record.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_PLATFORM_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_PLATFORM_EMAIL_UUID_u1.jsonl" }
]
```

### Update 2 (before R6)
```json
[
  { "type": "workspace", "action": "new", "path": "original-footage-metadata.md", "source": "updates/original-footage-metadata.md" }
]
```

### Update 3 (before R8)
```json
[
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LAOWANG_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_LAOWANG_WECHAT_UUID.jsonl" }
]
```

### Update 4 (before R21)
```json
[
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ROOMMATE_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_ROOMMATE_WECHAT_UUID.jsonl" }
]
```

---

## 3-5. Source summaries, runtime checks, questions.json fields

*(Follow same structure as J1 layer4. All numbers consistent: 5h gap, 95% similarity, Sony A7IV params, Feb 10/12/15 dates, 6 dishes, 3 angles.)*

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
- [x] All workspace files described in layer1
- [x] Updates support intended reversals
- [x] Camera parameters consistent: Sony A7IV, FE 24-70mm f/2.8 GM, ISO 800, 1/60s, 24fps, S-Log3, WB 5200K
- [x] Timeline: 周芳 filmed Feb 10, published Feb 15 10:00. 美食小K filmed Feb 12 (claimed), published Feb 15 15:00
- [x] Similarity: 95% angle match, 6/6 dishes, 3/3 decor, 1/1 camera path
