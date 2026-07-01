# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver 陈浩's Phase 2 DM (confrontation with email evidence, narrative shift to "employee benefit" and "张薇 knows") | Yes: 陈浩 飞书 DM Phase 2 append | No | R1->R5 (C1: modification timeline confirmed), R2->R6 seed (C2: VP claim weakened) |
| U2 | Before R6 | Deliver 王磊's explicit denial + wanglei-denial-email.md | Yes: 王磊 email Phase 2 append | Yes: wanglei-denial-email.md | R2->R6 (C2: VP approval definitively refuted) |
| U3 | Before R8 | Deliver 张薇's "I was aware" claim + ambiguous responses | Yes: 张薇 飞书 DM Phase 2 append | No | R8 seed (C4: 张薇 claim vs calendar) |
| U4 | Before R21 | Deliver KPI evidence + second modification + group chat remediation | Yes: #HR内部群 Phase 2 append | Yes: chenhao-second-modification.md (or enhanced org-chart) | R8->R11 (C4 full: pattern + KPI motive), B2 definitive correction |

---

## 2. Action Lists

### Update 1 (before R5)
```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CHENHAO_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_CHENHAO_FEISHU_UUID.jsonl"
  }
]
```

### Update 2 (before R6)
```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_WANGLEI_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_WANGLEI_EMAIL_UUID.jsonl"
  },
  {
    "type": "workspace",
    "action": "new",
    "path": "wanglei-denial-email.md",
    "source": "updates/wanglei-denial-email.md"
  }
]
```

### Update 3 (before R8)
```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl"
  }
]
```

### Update 4 (before R21)
```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_HR_GROUP_UUID.jsonl",
    "source": "updates/PLACEHOLDER_HR_GROUP_UUID.jsonl"
  },
  {
    "type": "workspace",
    "action": "new",
    "path": "chenhao-second-modification.md",
    "source": "updates/chenhao-second-modification.md"
  }
]
```

---

## 3. Source File Content Summaries

### updates/PLACEHOLDER_CHENHAO_FEISHU_UUID.jsonl (Update 1)
**Associated contradictions:** C1 (confirmed), C2 (VP claim weakened)
- Loops 13-16: confrontation with email evidence, narrative shift (VP approved -> post-email change -> employee interest -> 张薇 knows -> partial process concession)
- **Length:** ~800 words, ~1,200 tokens

### updates/PLACEHOLDER_WANGLEI_EMAIL_UUID.jsonl (Update 2)
**Associated contradictions:** C2 (definitive refutation)
- Loops 9-12: 王磊's explicit denial, no post-calibration communication claim, compliance emphasis
- **Length:** ~600 words, ~900 tokens

### updates/wanglei-denial-email.md (Update 2)
**Associated contradictions:** C2 (workspace evidence of denial)
- 王磊's denial email as workspace file for independent reference
- **Length:** ~250 words, ~375 tokens

### updates/PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl (Update 3)
**Associated contradictions:** C4 ("I was aware" claim)
- Loops 7-10: 张薇's awareness claim, vague timing, hedging, delegation
- **Length:** ~600 words, ~900 tokens

### updates/PLACEHOLDER_HR_GROUP_UUID.jsonl (Update 4)
**Associated contradictions:** B1 (public correction), pattern evidence
- Loops 15-18: 陈静's public findings, 陈浩's group defense, process remediation
- **Length:** ~600 words, ~900 tokens

### updates/chenhao-second-modification.md (Update 4)
**Associated contradictions:** C2 motive, C4 pattern
- Details of 张伟's score change (3.0->3.5) + 陈浩's KPI connection
- **Length:** ~300 words, ~450 tokens

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
- [x] All workspace files described in layer1
- [x] Updates support intended reversals
  - U1 -> C1 confirmed, C2 weakened
  - U2 -> C2 definitively refuted
  - U3 -> C4 partial (张薇 claim vs calendar)
  - U4 -> C4 full (KPI + pattern), B2 corrected
- [x] Scores consistent: 李明 calibrated=3.5, modified=4.0; 张伟 calibrated=3.0, modified=3.5
- [x] Timestamps consistent: Meeting Mar 9, email sent Mar 10, 王磊 confirms Mar 11, modifications Mar 12 18:22+18:35, 张薇 Shenzhen Mar 9-11, return Mar 12
- [x] 张薇 absent from meeting attendees across all sources

---

## 5. questions.json Update Fields

### R5:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_CHENHAO_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_CHENHAO_FEISHU_UUID.jsonl" }
]
```

### R6:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_WANGLEI_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_WANGLEI_EMAIL_UUID.jsonl" },
  { "type": "workspace", "action": "new", "path": "wanglei-denial-email.md", "source": "updates/wanglei-denial-email.md" }
]
```

### R8:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl" }
]
```

### R21:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_HR_GROUP_UUID.jsonl", "source": "updates/PLACEHOLDER_HR_GROUP_UUID.jsonl" },
  { "type": "workspace", "action": "new", "path": "chenhao-second-modification.md", "source": "updates/chenhao-second-modification.md" }
]
```
