# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R6 | Deliver Zhang Lin's defense email and timeline comparison evidence -- triggers C1 full resolution (timestamps debunk "verbal recommendation") and B1 reversal | Yes: Zhang Lin Email Phase 2 append (confrontation + defense collapse) | Yes: zhang-lin-defense-email.md | R2->R6 (C1: source attribution definitively resolved; CRM timestamps predate agency email); R5->R9 (B1: contractual defense overridden by factual evidence) |
| U2 | Before R8 | Deliver spam filter discovery and approval gap root cause -- triggers C4 full resolution (mail migration explains communication failure; neither party fully at fault) and B2 reversal | Yes: Zhao Lin Email Phase 2 append (spam filter discovery + process improvement) | Yes: approval-gap-evidence.md | R4->R8 (C4: approval gap definitively explained as systemic process failure + mail migration); B2 reversal (informal process is not "standard" but a control gap) |
| U3 | Before R11 | Deliver external pattern evidence from peer company -- confirms systematic fraud pattern, strengthens C1+C2 fraud interpretation, extends B1 reversal | Yes: Liu Yang IM Phase 2 append (external contact report + prevention measures) | Yes: pattern-evidence-external.md | Extends C1+C2 (fraud is systematic, not one-time); strengthens B1 reversal (pattern discredits "honest mistake" interpretation) |
| U4 | Before R21 | Deliver VP escalation and formal investigation request -- triggers comprehensive assessment with report framework | Yes: None (VP communication captured in workspace file) | Yes: vp-escalation-summary.md | Enables comprehensive R21-R30 assessment; frames dual-track remediation (vendor fraud + internal process) |

---

## 2. Action Lists

### Update 1 (before R6)

**Trigger timing:** After R5 answer is submitted, before R6 question is injected.
**Purpose:** Introduces Zhang Lin's formal defense email and the timeline comparison that debunks it. The agent can now see Zhang Lin's evolving defense (verbal recommendation -> talent pool -> simultaneous application) and the definitive timeline evidence showing CRM timestamps predate the agency email by 5-7 days with no prior communication.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "zhang-lin-defense-email.md",
    "source": "updates/zhang-lin-defense-email.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHANGLIN_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHANGLIN_EMAIL_UUID.jsonl"
  }
]
```

### Update 2 (before R8)

**Trigger timing:** After R7 answer is submitted, before R8 question is injected.
**Purpose:** Introduces the approval gap root cause evidence: Zhao Lin's original confirmation email found in Chen Jing's spam folder, the IT department's mail migration log showing the company-wide migration on 2026-02-21, and Zhao Lin's acknowledgment of the process gap. This resolves C4 definitively: neither party was negligent, but the informal process lacked safeguards. Also appends Phase 2 content to Zhao Lin Email session.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "approval-gap-evidence.md",
    "source": "updates/approval-gap-evidence.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_ZHAOLIN_EMAIL_UUID.jsonl",
    "source": "updates/PLACEHOLDER_ZHAOLIN_EMAIL_UUID.jsonl"
  }
]
```

### Update 3 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** Introduces external pattern evidence from a peer company confirming that RuiCai has used identical tactics elsewhere. This shifts the interpretation from "contractual ambiguity" or "one-time error" to "systematic fraud practice." Also appends Phase 2 content to Liu Yang IM session (external contact report, prevention measures, operational planning).

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "pattern-evidence-external.md",
    "source": "updates/pattern-evidence-external.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LIUYANG_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LIUYANG_IM_UUID.jsonl"
  }
]
```

### Update 4 (before R21)

**Trigger timing:** After R20 answer is submitted, before R21 question is injected.
**Purpose:** Introduces VP Zhang Wei's formal investigation request and report framework. Zhang Wei frames the investigation as both a vendor fraud case and an internal process improvement opportunity, requiring: (1) comprehensive evidence report, (2) financial impact analysis, (3) vendor relationship recommendation, (4) internal control improvements. This triggers the comprehensive assessment rounds R21-R30.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "vp-escalation-summary.md",
    "source": "updates/vp-escalation-summary.md"
  }
]
```

---

## 3. Source File Content Summaries

### updates/zhang-lin-defense-email.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C1 (full resolution -- Zhang Lin's defense debunked by timeline), B1 reversal trigger
**Content key points:**
- Title: "邮件线程导出 -- 张琳回复候选人来源质疑 | 2026-03-05"
- Zhang Lin's defense email with three claims: (1) "candidates in talent pool," (2) "verbal recommendation before their applications," (3) "headhunter value is screening not just forwarding"
- Chen Jing's response with timeline evidence: CRM entries (Jan 18-20) predate agency email (Jan 25) by 5-7 days; no prior communication found
- Zhang Lin's shifting position from defense to negotiation (offer to refund partial fees)
- No supporting documentation for any of Zhang Lin's claims

**Length estimate:** ~600 words, ~900 tokens

---

### updates/approval-gap-evidence.md (Update 2)

**File type:** workspace new
**Associated contradictions:** C4 (full resolution -- spam filter + mail migration root cause), B2 reversal trigger
**Content key points:**
- Title: "审批流程追溯 -- 发票确认邮件 + 邮件迁移日志 | 2026-03-06"
- Zhao Lin's original email (2026-02-22, 10:15): "请确认：锐才猎头Q1发票 #RC-2026-0220"
- IT mail migration log: company-wide migration 2026-02-21, known spam filter issues for 48 hours post-migration
- Chen Jing's spam folder: email found dated 2026-02-22, never opened
- Zhao Lin's approval timestamp: 2026-02-25, after 3-day waiting period
- Analysis: systemic process gap (no confirmation receipt), compounded by IT migration timing

**Length estimate:** ~500 words, ~750 tokens

---

### updates/pattern-evidence-external.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C1+C2 (systematic fraud pattern), extends B1 reversal
**Content key points:**
- Title: "外部信息 -- 同行公司反馈锐才猎头类似行为 | 2026-03-07"
- Liu Yang's contact (小赵, HR at peer company): similar experience with RuiCai
- Identical tactics: direct applicants billed as agency referrals; "talent pool" and "verbal recommendation" defense language
- Peer company response: contract termination, no legal pursuit
- Pattern strengthens fraud interpretation over honest mistake

**Length estimate:** ~400 words, ~600 tokens

---

### updates/vp-escalation-summary.md (Update 4)

**File type:** workspace new
**Associated contradictions:** Comprehensive trigger for R21-R30
**Content key points:**
- Title: "VP汇报纪要 -- 张薇对猎头发票问题的指示 | 2026-03-08"
- Zhang Wei's 4-point directive: evidence report, payment suspension, process review, vendor recommendation
- Framing: "不只是供应商问题，也是内部流程问题" (not just vendor issue, also internal process issue)
- Timeline: report due within 1 week
- Scope: financial impact + evidence chain + prevention measures + vendor relationship decision

**Length estimate:** ~500 words, ~750 tokens

---

## 4. Runtime Checks

After all updates are applied:
- [ ] C1 has evidence in CRM (auto-tags), invoice (all 8 as referral), candidate emails (direct application), and zhang-lin-defense-email.md (defense + debunking)
- [ ] C2 has evidence in invoice (8 candidates), CRM (5 agency), budget tracker (variance), and pattern-evidence-external.md (systematic)
- [ ] C3 has NO contradictions -- payment date, amount, and reference are consistent across bank records, invoice, and budget tracker
- [ ] C4 has evidence in bank records (approval note), Zhao Lin session, and approval-gap-evidence.md (spam filter + mail migration)
- [ ] B1 phrase appears verbatim in Zhang Lin Email session Loop 4
- [ ] B2 phrase appears verbatim in Zhao Lin Email session Loop 3
- [ ] All 4 updates have correct action type/path/source fields
- [ ] Financial figures consistent: Invoice ¥386,000 = 5 legit (¥250,000) + 3 fraud (¥136,000); individual fees match 20% of stated salaries
- [ ] Timeline consistent: Job posting 01-15, direct apps 01-18 to 01-20, agency email 01-25, interviews 02-01 to 02-15, invoice 02-20, approval email 02-22, payment 02-25, discovery 03-01
