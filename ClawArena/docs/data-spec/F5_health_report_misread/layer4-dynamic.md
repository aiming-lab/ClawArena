# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace? | Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Foreground doctor's calibration email + mother's reaction — resolves C1 scope issue and C2 premature genetic concern | Yes: 母亲 SMS Phase 2 (Loops 11) | No | R2->R5 (C1), R3->R5 (C2) |
| U2 | Before R7 | Deliver calibration technical report + doctor clarification on prescription — resolves C4 | Yes: 陈医生 email Phase 2 (Loops 7-8) | Yes: calibration-technical-report.md, doctor-clarification-email.md | R4->R7 (C4) |
| U3 | Before R9 | Deliver mother's acceptance — C2 social resolution | Yes: 母亲 SMS Phase 2 (Loop 12) | No | No new reversal |
| U4 | Before R11 | Hospital formal notice + recheck appointment — comprehensive confirmation | No | Yes: hospital-formal-notice.md | Comprehensive |

---

## 2. Action Lists

### Update 1 (before R5)
```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_MOTHER_SMS_UUID.jsonl",
    "source": "updates/PLACEHOLDER_MOTHER_SMS_UUID_u1.jsonl"
  }
]
```

### Update 2 (before R7)
```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CHENDR_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_CHENDR_EMAIL_UUID.jsonl"
  },
  {
    "type": "workspace",
    "action": "new",
    "path": "calibration-technical-report.md",
    "source": "updates/calibration-technical-report.md"
  },
  {
    "type": "workspace",
    "action": "new",
    "path": "doctor-clarification-email.md",
    "source": "updates/doctor-clarification-email.md"
  }
]
```

### Update 3 (before R9)
```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_MOTHER_SMS_UUID.jsonl",
    "source": "updates/PLACEHOLDER_MOTHER_SMS_UUID_u3.jsonl"
  }
]
```

### Update 4 (before R11)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "hospital-formal-notice.md",
    "source": "updates/hospital-formal-notice.md"
  }
]
```

---

## 3. Source File Content Summaries

### updates/PLACEHOLDER_MOTHER_SMS_UUID_u1.jsonl (Update 1)
- Loop 11: 赵磊 shares calibration email; mother skeptical ("why did pharmacy give you drugs then?")
- Length: ~300 words, ~450 tokens

### updates/PLACEHOLDER_CHENDR_EMAIL_UUID.jsonl (Update 2)
- Loops 7-8: Doctor clarifies auto-prescription vs his judgment, provides technical report
- Length: ~400 words, ~600 tokens

### updates/calibration-technical-report.md (Update 2)
- Beckman AU5800 calibration drift details, affected dates, offset values, corrective actions
- Length: ~400 words, ~600 tokens

### updates/doctor-clarification-email.md (Update 2)
- Doctor: "系统自动建议的预处方，不是我开的。请不要服用。"
- Length: ~300 words, ~450 tokens

### updates/PLACEHOLDER_MOTHER_SMS_UUID_u3.jsonl (Update 3)
- Loop 12: Mother accepts recheck plan, residual concern but no longer insisting on medication
- Length: ~250 words, ~375 tokens

### updates/hospital-formal-notice.md (Update 4)
- Hospital official calibration notice, free recheck offer, 赵磊's appointment Nov 15
- Length: ~350 words, ~525 tokens

---

## 4. Runtime Checks

- [x] Session appends match Phase 1 IDs
- [x] All workspace files described in layer1
- [x] Medical figures consistent: reported LDL 4.2, offset +0.8-1.0, corrected ~3.2-3.4, ref < 3.4
- [x] Other lipids consistent: HDL 1.5, TG 1.2, TC 5.1
- [x] Dates consistent: checkup Oct 3, results Oct 4, doctor email Oct 4, 赵磊 reads Oct 8, pharmacy Oct 7
- [x] Instrument ID consistent: Beckman AU5800, unit AU5800-SH-003

---

## 5. questions.json Update Fields

### R5:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_MOTHER_SMS_UUID.jsonl", "source": "updates/PLACEHOLDER_MOTHER_SMS_UUID_u1.jsonl" }
]
```

### R7:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CHENDR_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_CHENDR_EMAIL_UUID.jsonl" },
  { "type": "workspace", "action": "new", "path": "calibration-technical-report.md", "source": "updates/calibration-technical-report.md" },
  { "type": "workspace", "action": "new", "path": "doctor-clarification-email.md", "source": "updates/doctor-clarification-email.md" }
]
```

### R9:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_MOTHER_SMS_UUID.jsonl", "source": "updates/PLACEHOLDER_MOTHER_SMS_UUID_u3.jsonl" }
]
```

### R11:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "hospital-formal-notice.md", "source": "updates/hospital-formal-notice.md" }
]
```
