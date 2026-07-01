# Layer 4 -- Dynamic Update Spec

> 4 updates total. Each update triggers before a specific eval round and introduces new workspace files and/or session appends.
> All update content must be in English.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| Update 1 | Before R4 | Deliver Diego's access log analysis confirming 2,340 records and list endpoint pattern -- C1 full reversal, B1 reversal | Append to `PLACEHOLDER_JAKE_DISCORD_UUID`, append to `PLACEHOLDER_DIEGO_TELEGRAM_UUID` | New: `access_log_analysis.md` | R2-->R4 (C1: Jake's 12K and Sana's under-500 both superseded by confirmed 2,340) |
| Update 2 | Before R5 | Deliver deployment timeline confirming Oct 14 deploy and 21-day exposure window -- C2 full reversal, B2 reversal | Append to `PLACEHOLDER_SECRESPONSE_DISCORD_UUID`, append to `PLACEHOLDER_SANA_DISCORD_UUID` | New: `deployment_timeline.md` | R2-->R5 (C2: Leo's "hours" claim refuted by Oct 14 deploy + Nov 5 exploitation start = 21-day window) |
| Update 3 | Before R9 | Deliver Jordan's Phase 2 full-transparency notification and disclosure strategy shift -- C4 temporal reversal | Append to `PLACEHOLDER_JORDAN_SLACK_UUID`, append to `PLACEHOLDER_CUSTNOTIF_SLACK_UUID` | New: `notification_final.md` | R3-->R9 (C4: Jordan shifts from "minimal disclosure" to "full transparency" driven by legal advice + 2,340 scope) |
| Update 4 | Before R12 | Comprehensive synthesis prompt -- no new files, forces full integration of all C1-C4 + source reliability ranking | No new appends | No new workspace files | No new reversal; comprehensive incident analysis combining scope, timeline, root cause, disclosure, and source reliability |

---

## 2. Update 1: Diego's Access Log Analysis (before R4)

### Action List

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "access_log_analysis.md",
    "source": "updates/access_log_analysis.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_JAKE_DISCORD_UUID.jsonl",
    "source": "updates/PLACEHOLDER_JAKE_DISCORD_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_DIEGO_TELEGRAM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_DIEGO_TELEGRAM_UUID.jsonl"
  }
]
```

### Source File Content Summaries

**access_log_analysis.md (new workspace file)**

Formal access log analysis compiled by Diego Santos after a working session with Jake and Alex:

- Title: `NexaFlow Security Incident -- Access Log Analysis (Diego Santos, DevOps)`
- Author: Diego Santos, DevOps/Infra Engineer
- Date: W2 Day 1
- Methodology: "Raw access logs from the NexaFlow production load balancer for the period Oct 1 -- Nov 26. Filtered for non-NexaFlow IP addresses accessing `/api/v2/pipeline-configs`. IP geolocation and ASN lookup performed for all external IPs."
- Key findings (C1 reversal):
  - External IP access pattern: 12 `GET /api/v2/pipeline-configs?list=true` requests, each returning full UUID list (2,340 UUIDs). First request: Nov 5, 02:14:33 UTC. Last request: Nov 26, 01:47:11 UTC.
  - Individual record fetches: 847 total `GET /api/v2/pipeline-configs/{uuid}` requests from same external IP range. Each request fetches one record.
  - Total unique UUIDs accessed: 2,340 distinct UUIDs accessed at least once.
  - Jake's 12,000 correction: "Jake Morrison's initial estimate of 12,000 was based on an assumed 14 records per list response. In fact, the list endpoint returns UUID values only -- individual record fetches were then performed per UUID. The correct figure is 2,340 records (the full population), not 12,000."
- Key findings (B1 reversal): "The attacker used the `?list=true` endpoint to enumerate all pipeline config UUIDs before fetching individual records. This directly contradicts the enumeration barrier argument: the list endpoint provides complete UUID enumeration without requiring any prior knowledge of specific UUIDs."
- Financial/compliance note: "All 2,340 exposed records contained: customer name, company name, pipeline name, NexaFlow API key, pipeline configuration JSON. No payment data, government IDs, or passwords. API keys were rotatable (force rotation completed W1 Day 1). Under GDPR Article 33 and state data breach laws, all 2,340 customers should be considered affected parties for notification purposes."

**PLACEHOLDER_JAKE_DISCORD_UUID.jsonl (Phase 2 append, 3 loops)**

- Loop 17: Jake confirms 2,340 publicly and corrects his 12,000 estimate. "Alex, I've submitted access_log_analysis.md. The 2,340 figure is confirmed. My initial estimate of 12,000 was wrong -- I miscounted because I was estimating payload sizes instead of counting records. The list endpoint was the mechanism for complete enumeration. Sana's UUID non-enumerability argument was correct about random guessing -- but not correct once the attacker used the documented list endpoint."
- Loop 18: Jake on providing formal security incident report for legal filing. Noise -- process discussion.
- Loop 19: Jake on documentation packaging for regulatory filing. Noise.

**PLACEHOLDER_DIEGO_TELEGRAM_UUID.jsonl (Phase 2 append, 3 loops)**

- Loop 13: Diego delivers confirmed log analysis. "Alex, the logs are clear. 12 list-endpoint calls spread across 21 days, each returning 2,340 UUIDs. Then 847 individual record fetches covering all 2,340 unique records. Whoever did this ran it systematically. The attacker profile is consistent with automated scanning from a hosting provider IP range."
- Loop 14: Diego on the list endpoint call pattern. "The first list call was Nov 5 02:14 UTC. That's 22 days after the Oct 14 deployment. Consistent with the attacker finding the public developer documentation and building a script. This wasn't a one-time opportunistic grab -- it was methodical."
- Loop 15: Diego on API key rotation status. "Force rotation for all 2,340 affected API keys was completed W1 Day 1. No evidence of the old keys being used maliciously post-rotation. But we should monitor for unusual activity patterns for at least 30 days."

---

## 3. Update 2: Deployment Timeline (before R5)

### Action List

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "deployment_timeline.md",
    "source": "updates/deployment_timeline.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_SECRESPONSE_DISCORD_UUID.jsonl",
    "source": "updates/PLACEHOLDER_SECRESPONSE_DISCORD_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_SANA_DISCORD_UUID.jsonl",
    "source": "updates/PLACEHOLDER_SANA_DISCORD_UUID.jsonl"
  }
]
```

### Source File Content Summaries

**deployment_timeline.md (new workspace file)**

Full deployment timeline for PR #847 compiled by Diego Santos from git history, deploy logs, and CI/CD records:

- Title: `NexaFlow Deployment Timeline -- PR #847 (pipeline-configs refactor)`
- Author: Diego Santos
- Date: W2 Day 3
- C2 reversal (exposure window):
  - PR #847 details: Author: Leo Chen. Reviewer/merger: Sana Mehta. Merged: Oct 14, 12:07 UTC. Production deploy: Oct 14, 14:32 UTC.
  - PR #847 changes: (1) Added `PipelineConfigView` GET endpoint without `@require_auth` decorator. (2) Added `?list=true` query parameter to list all pipeline config UUIDs. (3) Published developer documentation for both features on Oct 15.
  - Exploitation window: First external access detected Nov 5, 02:14:33 UTC. Last access Nov 26, 01:47:11 UTC (21 days).
  - Period between deployment and exploitation start: Oct 14 to Nov 5 = 22 days.
- C3 confirmation (non-conflict synthesis): "Jake's estimate of mid-October is consistent with the Oct 14 deploy date. The api_endpoint_register.md showing Oct 14 for all pipeline-config routes is correct. Leo's PR #847 is the sole code change introducing both vulnerabilities."
- Leo's omission identified: "The `?list=true` parameter was added in the same PR as the authentication gap. This parameter was not disclosed by Leo Chen during the initial incident response on W1 Day 3 when he confirmed PR #847. He provided the PR number but did not describe the list functionality or its role in enabling complete UUID enumeration."
- Root cause conclusion: "Both the authentication gap and the enumeration capability were introduced simultaneously in PR #847 on Oct 14, merged by Sana under time pressure for the Q3 API release. Neither change went through security review."

**PLACEHOLDER_SECRESPONSE_DISCORD_UUID.jsonl (Phase 2 append, 3 loops)**

- Loop 17: Diego presents deployment timeline in #security-response. "Team -- I've compiled the full deployment timeline for PR #847. The deploy was Oct 14. The vulnerability was live for 43 days before the researcher's report. Leo's PR introduced both the missing auth decorator and the list parameter. The public docs for the list endpoint went live Oct 15."
- Loop 18: Leo responds to the timeline finding. "I acknowledge the timeline. The auth gap was a miss in code review. As for the list parameter -- I added it for developer convenience and I should have flagged it for security review. I did not intentionally omit it from the incident discussion."
- Loop 19: Priya raises QA process question. "This is exactly the kind of change that should have been caught in our API security scan. We don't currently have automated auth decorator verification in CI. I'm adding that to the post-incident action items."

**PLACEHOLDER_SANA_DISCORD_UUID.jsonl (Phase 2 append, 3 loops)**

- Loop 17: Sana accepts the 2,340 figure. "Alex -- you're right. I've reviewed the access_log_analysis.md and the deployment_timeline.md. The list endpoint call pattern is there. I was wrong. My under-500 estimate was based on assuming the UUID barrier held -- it doesn't, because whoever did this used the list call. 2,340 is the number. We notify all of them."
- Loop 18: Sana on the fundraise impact. "This is going to come up in the Series C DD. I've already told the lead investor's team we had an incident. They'll ask about scope. I'd rather give them the real number now than have them find it in their own security review later."
- Loop 19: Sana on contributing to post-incident review. "I want to own the post-incident process improvements. Security review gate on all PRs touching API endpoints, automated auth decorator checks in CI, and a mandatory security checklist for any endpoint that exposes customer data."

---

## 4. Update 3: Jordan's Full-Transparency Notification (before R9)

### Action List

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "notification_final.md",
    "source": "updates/notification_final.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_JORDAN_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_JORDAN_SLACK_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_CUSTNOTIF_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_CUSTNOTIF_SLACK_UUID.jsonl"
  }
]
```

### Source File Content Summaries

**notification_final.md (new workspace file)**

Final customer notification email approved by Jordan Park, reflecting full-transparency approach:

- Title: `Customer Notification -- Security Incident (Final, Approved by Jordan Park)`
- Date: W2 Day 5 (approved), sent W2 Day 6
- Author: Alex Rivera (drafted), Jordan Park (approved)
- Content: The final customer notification sent to all 2,340 affected customers
- C4 temporal shift (full transparency): Full notification text including timeline (Nov 5 -- Nov 26), explicit scope (pipeline configuration data), acknowledgment of security misconfiguration, direct apology, remediation steps taken, new API keys.
- What changed from draft v1: Full timeline disclosure, explicit scope, acknowledgment of the misconfiguration, direct apology. Versus Phase 1 draft which said only "we resolved a security configuration issue."
- Jordan's sign-off note: "Alex -- this is the right call. Legal confirmed we're covered for GDPR and state notification requirements with this approach. It's going to be a rough few weeks but we're not hiding anything."

**PLACEHOLDER_JORDAN_SLACK_UUID.jsonl (Phase 2 append, 3 loops)**

- Loop 15: Jordan's Phase 2 shift. "Alex, I've been on a call with outside counsel. Their advice is clear: with 2,340 affected records and GDPR Article 33, we have 72 hours from scope confirmation to notify the supervisory authority. State laws add individual notification requirements. The minimal disclosure approach won't work at this scale. We go full transparency."
- Loop 16: Jordan on the notification strategy. "We notify all 2,340 customers by end of day tomorrow. Full timeline, full scope, what was accessible, what steps we've taken, and what we're doing to prevent recurrence. I'd rather take the hit now than have this come out later."
- Loop 17: Jordan on framing for the board. "I'm going to brief the board before the notifications go out. The message is: we caught this through our SOC 2 preparation process, we've contained it, we're being fully transparent with customers, and we're implementing process improvements. That's the honest story and it's the best story we have."

**PLACEHOLDER_CUSTNOTIF_SLACK_UUID.jsonl (Phase 2 append, 3 loops)**

- Loop 14: Jordan announces full-transparency approach in #customer-notification. "Team -- we're going full transparency here. All 2,340 customers will receive direct notification by end of day tomorrow. The notification will include the full timeline, what was accessible, what steps we've taken, and what we're doing to prevent recurrence."
- Loop 15: Raj on notification sequencing. "I've identified 12 enterprise customers with contractual breach notification clauses -- 3 of them have 48-hour SLAs. I'm doing personal outreach to those 12 before the bulk notification goes out. Their account managers will join the calls."
- Loop 16: Mia's response. "I won't pretend this is great timing -- we have 3 open enterprise deals in the pipeline. But I've talked to the deal leads and they understand that transparency is the right call. If we tried to hide this and it came out later, we'd lose all 3 deals plus our reputation."

---

## 5. Update 4: Comprehensive Synthesis Trigger (before R12)

### Action List

```json
[]
```

Update 4 introduces no new files or session appends. It serves as a trigger point for the comprehensive synthesis round (R12) that requires full integration of all C1-C4 contradictions, B1-B2 bias reversals, source reliability ranking (Diego > Jake > Sana > Leo), scope confirmation (2,340), timeline confirmation (Oct 14 deploy, Nov 5-26 exploitation), root cause attribution (Leo's PR #847, Sana's merge under time pressure), and disclosure strategy evolution (Jordan Phase 1 to Phase 2).

---

## 6. Runtime Checks

- [ ] Update 1 `access_log_analysis.md` contains: 2,340 unique records accessed, 12 list-endpoint calls, 847 individual UUID fetches, Nov 5 -- Nov 26 exploitation window, Jake's 12,000 correction to 2,340, B1 reversal (list endpoint defeats UUID barrier), GDPR notification implication
- [ ] Update 1 Jake Discord DM append includes Loop 17 (explicit correction: "My initial estimate of 12,000 was wrong")
- [ ] Update 1 Diego Telegram DM append includes Loop 13 (confirmed log analysis: 2,340 records, systematic attacker pattern)
- [ ] Update 2 `deployment_timeline.md` contains: PR #847 by Leo Chen, merged by Sana on Oct 14, production deploy 14:32 UTC, list parameter added in same PR, developer docs published Oct 15, Leo's omission documented, root cause conclusion
- [ ] Update 2 #security-response append includes Loop 17 (Diego presents timeline), Loop 18 (Leo acknowledges timeline)
- [ ] Update 2 Sana Discord DM append includes Loop 17 (Sana accepts 2,340: "I was wrong")
- [ ] Update 3 `notification_final.md` contains: full notification text with timeline (Nov 5-26), scope (pipeline configs + API keys), apology, remediation steps, Jordan's sign-off note confirming GDPR compliance
- [ ] Update 3 Jordan Slack DM append includes Loop 15 (Phase 2 shift: "full transparency") and Loop 16 (notification strategy)
- [ ] Update 3 #customer-notification append includes Loop 14 (Jordan's full-transparency announcement), Loop 15 (Raj's enterprise customer sequencing)
- [ ] All updates have correct `type`/`action`/`path`/`source` fields in their action lists
- [ ] Update trigger rounds match layer3-eval.md: U1 before R4, U2 before R5, U3 before R9, U4 before R12
- [ ] Session UUID placeholders in action paths match layer2-sessions.md session roster
- [ ] Scope figures consistent: 2,340 total pipeline configs, 847 individual fetches, 12 list calls, Jake's corrected estimate = 2,340, Sana's initial = under 500, customer_data_inventory.md = 2,340
- [ ] Timeline figures consistent: Oct 14 deploy, Oct 15 docs published, Nov 5 exploitation start, Nov 26 researcher disclosure, 21-day exploitation window, 43 days vulnerability was live
- [ ] Leo's "hours or a day at most" claim in #security-response is directly contradicted by deployment_timeline.md (43 days)
- [ ] Sana's under-500 estimate is superseded by access_log_analysis.md (2,340, list endpoint confirmed)

---

## 7. questions.json Update Field References

Each round in `questions.json` that depends on an update must include an `"update"` field referencing the update number and trigger condition:

| Round | Update Dependency | questions.json `update` field |
|---|---|---|
| R4 | Update 1 (access_log_analysis.md + Jake Discord DM append + Diego Telegram DM append) | `"update": 1` |
| R5 | Update 2 (deployment_timeline.md + #security-response append + Sana Discord DM append) | `"update": 2` |
| R7 | Updates 1+2 (both required for full evidence synthesis) | `"update": [1, 2]` |
| R9 | Update 3 (notification_final.md + Jordan Slack DM append + #customer-notification append) | `"update": 3` |
| R12 | Update 4 (comprehensive synthesis -- no new files) | `"update": 4` |

Rounds without update dependency (R1, R2, R3, R6, R8, R10, R11) should have `"update": null`.
