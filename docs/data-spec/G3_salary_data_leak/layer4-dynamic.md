# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace? | Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | File version history — confirms C1 (full v1.1 downloaded) and provides C3 timeline | No | Yes: file-version-history.md | R2->R5 (C1) |
| U2 | Before R6 | IT security report — introduces C4 (scope-limited "no external shares") | Yes: IT email Phase 2 append | Yes: it-security-report.md | R6->R8 seed (C4) |
| U3 | Before R7 | Salary spreadsheet metadata — definitive C2 evidence (hash match) | No | Yes: salary-spreadsheet-metadata.md | R3->R7 (C2) |
| U4 | Before R11 | 林小雅's partial admission + 张薇's decision — comprehensive resolution | Yes: 林小雅 IM Phase 2 + 张薇 飞书 Phase 2 | Yes: linxiaoya-partial-admission.md | Comprehensive |

---

## 2. Action Lists

### Update 1 (before R5)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "file-version-history.md",
    "source": "updates/file-version-history.md"
  }
]
```

### Update 2 (before R6)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "it-security-report.md",
    "source": "updates/it-security-report.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ITSEC_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ITSEC_EMAIL_UUID.jsonl"
  }
]
```

### Update 3 (before R7)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "salary-spreadsheet-metadata.md",
    "source": "updates/salary-spreadsheet-metadata.md"
  }
]
```

### Update 4 (before R11)
```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "linxiaoya-partial-admission.md",
    "source": "updates/linxiaoya-partial-admission.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LINXIAOYA_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LINXIAOYA_IM_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/file-version-history.md (Update 1)
**File type:** workspace new
**Associated:** C1 (version confirmation), C3 (non-conflict timeline)
**Key data:** Full version v1.0 (9/20), v1.1 (9/24, +3 new employees, 2.3MB). Anonymized v1.0 (9/22, 0.8MB). 林小雅 downloaded v1.1 on 9/25.
**Length:** ~350 words, ~525 tokens

---

### updates/it-security-report.md (Update 2)
**File type:** workspace new
**Associated:** C4 (scope-limited finding)
**Key data:** "未发现通过云盘渠道的外部数据分享." Scope: cloud sharing only, NOT email.
**Length:** ~500 words, ~750 tokens

---

### updates/PLACEHOLDER_ITSEC_EMAIL_UUID.jsonl (Update 2)
**File type:** session append
**Associated:** C4 (IT delivers report + scope clarification)
**Key data:** IT delivers report, 陈静 asks about email scope, IT confirms email was excluded.
**Length:** ~400 words, ~600 tokens

---

### updates/salary-spreadsheet-metadata.md (Update 3)
**File type:** workspace new
**Associated:** C2 (definitive hash match)
**Key data:** Full version hash `a3f7b2c8e9d1...` = email attachment hash. Anonymized hash different. Creator: 陈静.
**Length:** ~400 words, ~600 tokens

---

### updates/linxiaoya-partial-admission.md (Update 4)
**File type:** workspace new
**Associated:** C1 (partial admission), C2 (final denial refuted by hash)
**Key data:** 林小雅 admits downloading full version but claims modification before sending — refuted by hash match.
**Length:** ~300 words, ~450 tokens

---

### updates/PLACEHOLDER_LINXIAOYA_IM_UUID.jsonl (Update 4)
**File type:** session append
**Key data:** Loops 11-12: partial admission + hash confrontation + narrative collapse.
**Length:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl (Update 4)
**File type:** session append
**Key data:** Loops 7-8: 陈静 presents complete evidence, 张薇 initiates formal investigation.
**Length:** ~350 words, ~525 tokens

---

## 4. Runtime Checks

- [x] Session appends match Phase 1 IDs
- [x] All workspace files described in layer1
- [x] File sizes consistent: full 2.3MB, anonymized 0.8MB, email attachment 2.3MB
- [x] Hashes consistent: full = email attachment (a3f7b2c8e9d1...), anonymized different (7b4c8f2d1a9e...)
- [x] Timestamps consistent: full created 9/20, updated 9/24, anonymized 9/22, download 9/25 14:22, email 9/25 15:03
- [x] Domain names consistent: lxy@company.com (internal), zhangling@headhunter-corp.com (external)
- [x] IT report scope explicitly stated: cloud sharing only

---

## 5. questions.json Update Fields

### R5:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "file-version-history.md", "source": "updates/file-version-history.md" }
]
```

### R6:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "it-security-report.md", "source": "updates/it-security-report.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ITSEC_EMAIL_UUID.jsonl", "source": "updates/PLACEHOLDER_ITSEC_EMAIL_UUID.jsonl" }
]
```

### R7:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "salary-spreadsheet-metadata.md", "source": "updates/salary-spreadsheet-metadata.md" }
]
```

### R11:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "linxiaoya-partial-admission.md", "source": "updates/linxiaoya-partial-admission.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LINXIAOYA_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_LINXIAOYA_IM_UUID.jsonl" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl", "source": "updates/PLACEHOLDER_ZHANGWEI_FEISHU_UUID.jsonl" }
]
```
