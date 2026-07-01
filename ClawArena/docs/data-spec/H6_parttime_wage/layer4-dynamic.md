# Layer 4 -- Dynamic Update Design

> Four updates, action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Platform confirms contract 20% rate -- formal acknowledgment of posting/contract discrepancy | Yes: 平台客服 IM Phase 2 append (Loop 9) | No new workspace files | R2->R6 (C2: platform confirms but deflects with "refer to contract") |
| U2 | Before R7 | Parent confirms paying ¥3,000 -- three-party reconciliation complete | Yes: 张女士 IM Phase 2 append (Loop 11) | No new workspace files | R3->R7 (C4: both parent and tutor truthful; platform fee is the sole cause of gap) |
| U3 | Before R9 | 周姐姐 reveals systemic fee change + posting retroactive edits | Yes: 周姐姐 IM Phase 2 append (Loop 7) | No new workspace files | R2->R9 (C2 pattern: systemic platform practice, not isolated error) |
| U4 | Before R10 | Platform posting modified after complaint -- concealment evidence | Yes: 平台客服 IM Phase 2 append (Loop 10) | Yes: platform-posting-comparison.md | R2->R10 (C2 definitive: posting modification = evidence of platform awareness of deception) |

---

## 2. Action Lists

### Update 1 (before R5)

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_PLATFORM_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_PLATFORM_IM_UUID_u1.jsonl"
  }
]
```

### Update 2 (before R7)

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_PARENT_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_PARENT_IM_UUID.jsonl"
  }
]
```

### Update 3 (before R9)

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHOUJIEJIE_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHOUJIEJIE_IM_UUID.jsonl"
  }
]
```

### Update 4 (before R10)

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "platform-posting-comparison.md",
    "source": "updates/platform-posting-comparison.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_PLATFORM_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_PLATFORM_IM_UUID_u4.jsonl"
  }
]
```

---

## 3. Runtime Checks

- [ ] B1 phrase appears verbatim in platform_im Loop 4
- [ ] B2 phrase appears verbatim in main session Loop 3
- [ ] C1 sources: wechat-payment-history.md (¥2,400 received) vs chat-with-parent.md (¥3,000 agreed) vs platform-fee-breakdown.md (¥600 deducted)
- [ ] C2 sources: job-posting-screenshot.md (10%) vs tutoring-platform-rules.md (20%) vs platform_im (confirms 20%) vs platform-posting-comparison.md (posting modified)
- [ ] C3 has NO contradictions -- schedule, hours, payment dates all consistent
- [ ] C4 sources: 张女士 IM ("paid ¥3,000 full") vs wechat-payment-history.md (¥2,400 to Wang Ming) vs platform-fee-breakdown.md (¥600 fee)
- [ ] All updates correct
- [ ] Financial figures consistent: parent pays ¥3,000, platform fee 20% = ¥600, tutor gets ¥2,400, posting says 10% = ¥300, difference ¥300
- [ ] 王明's P1-P5 preferences at correct stages
- [ ] exec_check = 30% (9/30)
