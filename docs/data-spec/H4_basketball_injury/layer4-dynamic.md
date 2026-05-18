# Layer 4 -- Dynamic Update Design

> Four updates, action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Insurance rejection notice -- "recreational activity" classification | Yes: 母亲 wechat Phase 2 append | Yes: insurance-claim-form.md append (rejection) | R4->R7 (C4: insurance rejection with wrong classification) |
| U2 | Before R6 | Referee report detailed analysis -- annotation contradicts ruling | Yes: 马强 IM Phase 2 append | No new files (referee-report.md already has annotation) | R3->R6 (C1: referee's own notes contradict ruling) |
| U3 | Before R9 | Coach's video analysis with CUBA rule citation | Yes: 刘教练 IM Phase 2 append | Yes: coach-video-analysis.md | R3->R9 (C1 definitive: coach + rule + annotation triple confirmation) |
| U4 | Before R11 | School sports department approval document | Yes: 辅导员 IM Phase 2 append | Yes: sports-dept-approval.md | R4->R11 (C4 definitive: official "school-organized" status refutes "recreational") |

---

## 2. Action Lists

### Update 1 (before R5)

```json
[
  {
    "type": "workspace",
    "action": "append",
    "path": "insurance-claim-form.md",
    "source": "updates/insurance-claim-form-append.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_MOTHER_WECHAT_UUID.jsonl",
    "source": "updates/PLACEHOLDER_MOTHER_WECHAT_UUID.jsonl"
  }
]
```

### Update 2 (before R6)

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_MAQIANG_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_MAQIANG_IM_UUID.jsonl"
  }
]
```

### Update 3 (before R9)

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "coach-video-analysis.md",
    "source": "updates/coach-video-analysis.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_COACH_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_COACH_IM_UUID.jsonl"
  }
]
```

### Update 4 (before R11)

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "sports-dept-approval.md",
    "source": "updates/sports-dept-approval.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_COUNSELOR_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_COUNSELOR_IM_UUID.jsonl"
  }
]
```

---

## 3. Runtime Checks

- [ ] B1 phrase appears verbatim in maqiang_im Loop 4
- [ ] B2 phrase appears verbatim in main session Loop 3
- [ ] C1 sources: game-video-transcript.md + referee-report.md annotation + coach-video-analysis.md + CUBA rules
- [ ] C2 sources: medical-record-campus.md ("sprain") vs insurance-claim-form.md (hospital "ACL tear")
- [ ] C3 has NO contradictions -- game time, clinic time, hospital time, claim time all consistent
- [ ] C4 sources: insurance-claim-form.md rejection ("recreational") vs sports-rules-extract.md policy text ("sports activity") vs sports-dept-approval.md ("school-organized")
- [ ] All updates correct
- [ ] Medical figures consistent: campus ¥150, hospital MRI ¥800, treatment estimate ¥15,000-¥25,000, insurance max ¥30,000
- [ ] 王明's P1-P5 preferences at correct stages
- [ ] exec_check = 30% (9/30)
