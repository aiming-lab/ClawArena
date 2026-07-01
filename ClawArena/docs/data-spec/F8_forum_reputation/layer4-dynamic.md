# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Moderator refuses to handle search cache -- triggers C2 reversal and B2 correction | Yes: 韩版主 IM Phase 2 append | Yes: moderator-response-email.md append (回复2) | R2->R6 (C2: moderator's "deleted" claim insufficient; rule 5.1 violated) |
| U2 | Before R7 | IP investigation results confirm impersonation -- corroborates C1 | Yes: 小周 WeChat DM Phase 2 append | Yes: ip-investigation-report.md | Strengthens C1 (independent technical evidence) |
| U3 | Before R9 | Secondary spread to another forum -- triggers B1 reversal | Yes: #量化策略群 Phase 2 append | Yes: secondary-spread-evidence.md | R5->R9 (B1: "minor noise" assessment proven wrong by viral spread) |
| U4 | Before R11 | Platform formal response reveals internal timeline contradicting moderator -- triggers C4 full reversal | No new sessions | Yes: platform-formal-response.md | R3->R8->R11 (C4: platform's internal log shows moderator delay; commits to search engine deletion) |

---

## 2. Action Lists

### Update 1 (before R5)

```json
[
  {
    "type": "workspace",
    "action": "append",
    "path": "moderator-response-email.md",
    "source": "updates/moderator-response-email-append.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_HANMOD_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_HANMOD_IM_UUID.jsonl"
  }
]
```

### Update 2 (before R7)

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "ip-investigation-report.md",
    "source": "updates/ip-investigation-report.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_XIAOZHOU_WECHAT_UUID.jsonl",
    "source": "updates/PLACEHOLDER_XIAOZHOU_WECHAT_UUID.jsonl"
  }
]
```

### Update 3 (before R9)

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "secondary-spread-evidence.md",
    "source": "updates/secondary-spread-evidence.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_QUANT_GROUP_UUID.jsonl",
    "source": "updates/PLACEHOLDER_QUANT_GROUP_UUID.jsonl"
  }
]
```

### Update 4 (before R11)

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "platform-formal-response.md",
    "source": "updates/platform-formal-response.md"
  }
]
```

---

## 3. Runtime Checks

- [ ] B1 phrase appears verbatim in quant_strategy_group Loop 5
- [ ] B2 phrase appears verbatim in hanmoderator_im Loop 4
- [ ] C1 sources are independent (forum-post-screenshot.md vs verified-performance-record.md + ip-investigation-report.md)
- [ ] C2 sources are independent (韩版主 IM "deleted" vs search-engine-cache.md + platform-content-policy.md rule 5.1)
- [ ] C3 has NO contradictions -- all timestamps consistent
- [ ] C4 sources are independent (platform-content-policy.md "48hr" vs 韩版主 IM timeline + platform-formal-response.md internal log)
- [ ] All 4 updates have correct action type/path/source fields
- [ ] Quantitative figures consistent: fake 300% vs real 23.4%, views 2,347, comments 89, search position #3
- [ ] Timeline consistent: 3/1 post -> 3/1 evening discovery -> 3/3 deletion -> 3/5 cache confirmed -> W2D1 cache refusal -> W2D3 IP evidence -> W2D5 secondary spread -> W2D7 platform response
- [ ] exec_check rounds = 30% (9/30)
