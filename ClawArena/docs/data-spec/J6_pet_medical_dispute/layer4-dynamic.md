# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger | Goal | New Sessions? | New Workspace? | Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | second-opinion-notes.md (骨科专科判断技术问题) | No | Yes | R1->R5 |
| U2 | Before R6 | vet-communication-email.md (consent standard) | No | Yes | R2->R6 |
| U3 | Before R8 | 陈医生 rebuttal + 周芳 challenge | Yes: 陈医生 Phase 2 | No | R8->R11 seed |
| U4 | Before R21 | Similar complaints from 室友 | Yes: 室友 Phase 2 | No | R8->R11 full |

---

## 2. Action Lists

### Update 1 (before R5)
```json
[
  { "type": "workspace", "action": "new", "path": "second-opinion-notes.md", "source": "updates/second-opinion-notes.md" }
]
```

### Update 2 (before R6)
```json
[
  { "type": "workspace", "action": "new", "path": "vet-communication-email.md", "source": "updates/vet-communication-email.md" }
]
```

### Update 3 (before R8)
```json
[
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CHENVET_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_CHENVET_WECHAT_UUID.jsonl" }
]
```

### Update 4 (before R21)
```json
[
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ROOMMATE_WECHAT_UUID.jsonl", "source": "updates/PLACEHOLDER_ROOMMATE_WECHAT_UUID.jsonl" }
]
```

---

## 4. Runtime Checks

- [x] Screw angulation: 15 degrees, standard ±5 degrees
- [x] Plate displacement: 2mm
- [x] Plate specs: 3.5mm locking plate, 6 screws
- [x] Affected screws: #2 and #4
- [x] Medications: amoxicillin-clavulanate 7d, meloxicam 5d, dressings x3
- [x] Consent missing: implant failure, non-union, revision surgery
- [x] Prior complaints: 2 similar cases in 3 months at same clinic
