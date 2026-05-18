# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Health app data reveals gym/SPA date non-overlap for 3 employees; 2 employees have no gym history at all -- weakens "innocent mistake" narrative | No new sessions | No new workspace files (health-app-data.md already initial) | B2 partial correction: mislabeling is not innocent |
| U2 | Before R7 | Employee reveals VP oral approval claim + finance redirects responsibility -- triggers C2 reversal and C4 seed | Yes: 赵琳 email Phase 2 append + 员工小李 IM Phase 2 append | No new workspace files | R2->R7 (C2: finance "flexibility" originates from VP comment); C4 seed |
| U3 | Before R9 | Calendar and email search finds no written record of VP authorization -- triggers C4 escalation | Yes: (implicit via main session context) | Yes: calendar-email-search-results.md | R6->R9 (C4: VP oral claim unsupported by any written record) |
| U4 | Before R11 | VP gives ambiguous response -- partially acknowledges but denies specific SPA authorization | Yes: 张薇 feishu Phase 2 append | Yes: vp-feishu-response.md | R6->R9->R11 (C4 full: VP neither confirms nor fully denies) |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Agent re-examines health-app-data.md with specific attention to date overlap between gym activity and SPA invoice dates. The data was already available but the agent had not deeply analyzed it. This is a "depth" update rather than a new file update.

```json
[
  {
    "type": "eval",
    "action": "inject_question",
    "note": "R5 question specifically directs agent to re-examine health-app-data.md for date-level analysis"
  }
]
```

### Update 2 (before R7)

**Trigger timing:** After R6 answer is submitted, before R7 question is injected.

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHAOLIN_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHAOLIN_EMAIL_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_EMPLOYEE_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_EMPLOYEE_IM_UUID.jsonl"
  }
]
```

### Update 3 (before R9)

**Trigger timing:** After R8 answer is submitted, before R9 question is injected.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "calendar-email-search-results.md",
    "source": "updates/calendar-email-search-results.md"
  }
]
```

### Update 4 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "vp-feishu-response.md",
    "source": "updates/vp-feishu-response.md"
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

## 3. Runtime Checks

- [ ] B1 phrase appears verbatim in zhaolin_email Loop 5
- [ ] B2 phrase appears verbatim in employee_im Loop 3
- [ ] C1 sources are independent (expense-claims-export.md vs vendor-invoices.md)
- [ ] C2 sources are independent (赵琳 email "follows policy" vs wellness-policy.md section 3.2 + finance-approval-log.md)
- [ ] C3 has NO contradictions -- all dates consistent
- [ ] C4 sources are independent (员工小李 IM "VP said" vs calendar-email-search-results.md "no record" vs vp-feishu-response.md "maybe mentioned wellbeing")
- [ ] All updates have correct action type/path/source fields
- [ ] Financial figures consistent: total ¥28,500, individual claims ¥3,000-¥8,000, 5 employees, 3 departments
- [ ] 陈静's P1-P5 preferences injected at correct stages
- [ ] exec_check rounds = 30% (9/30)
