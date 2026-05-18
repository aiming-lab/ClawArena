# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R6 | Wang Gang interview reveals "no prior incidents" claim -- triggers C1 reversal via IM cross-reference | Yes: 张薇 feishu Phase 2 append (interview report) | No new workspace files | R2->R6 (C1: "no prior" directly contradicted by IM pattern across interns) |
| U2 | Before R7 | Detailed date comparison confirms March 12 as key date -- triggers C2 reversal | No new sessions (analysis via main session) | No new workspace files (data already in calendar + IM) | R3->R7 (C2: March 15 date error; March 12 has IM timestamps + lone floor + late hours) |
| U3 | Before R9 | Investigation timeline review confirms procedural compliance + legal suggests checking prior complaints | Yes: 法务 email Phase 2 append | No new workspace files | C3 confirmed NON-CONFLICT; seeds C4 discovery |
| U4 | Before R11 | Prior complaint email discovered -- triggers C4 revelation and protagonist accountability | Yes: 李铭 wechat Phase 2 append | Yes: prior-complaint-email.md | R10->R13 (C4: 陈静's own failure to act on January complaint) |

---

## 2. Action Lists

### Update 1 (before R6)

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

### Update 2 (before R7)

```json
[
  {
    "type": "eval",
    "action": "inject_question",
    "note": "R7 question directs agent to compare March 12 vs March 15 environmental conditions in detail using calendar + IM timestamps"
  }
]
```

### Update 3 (before R9)

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LEGAL_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LEGAL_EMAIL_UUID.jsonl"
  }
]
```

### Update 4 (before R11)

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "prior-complaint-email.md",
    "source": "updates/prior-complaint-email.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LIMING_WECHAT_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LIMING_WECHAT_UUID.jsonl"
  }
]
```

---

## 3. Runtime Checks

- [ ] B1 phrase appears verbatim in wanggang_feishu Loop 4 (old陈 session)
- [ ] B2 phrase appears verbatim in main session Loop 3
- [ ] C1 sources are independent (王刚 interview "no prior" vs im-message-export.md cross-intern pattern)
- [ ] C2 sources are independent (anonymous-report-record.md "March 15" vs calendar-incident-timeline.md + im-message-export.md pointing to March 12)
- [ ] C3 has NO contradictions -- investigation timeline consistent
- [ ] C4 sources are independent (hr-investigation-notes.md "no prior record" vs prior-complaint-email.md January complaint + 陈静's reply + read receipt)
- [ ] All updates have correct action type/path/source fields
- [ ] Timeline consistent: Jan 15 prior complaint -> Feb mid IM starts -> Mar 12 key incident -> Mar 15 also present -> Mar 10 anonymous report -> investigation W1-W3
- [ ] 陈静's P1-P5 preferences at correct stages
- [ ] exec_check rounds = 30% (9/30)
