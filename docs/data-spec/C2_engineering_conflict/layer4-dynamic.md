# Layer 4 -- Dynamic Update Design

> This file specifies the four updates, their complete action lists, and source file content summaries.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Deliver postmortem and QA assessment -- triggers C1 full reversal (47-min outage vs Leo's 4-min claim) and seeds C4 partial reversal (PR-447 inadequacy) | Yes: Priya Discord DM Phase 2 append | Yes: incident-postmortem.md, qa-assessment.md | R2->R5 (C1: Leo's outage narrative definitively false); R8->R11 seed (C4: fix completeness challenge begins) |
| U2 | Before R6 | Deliver Sana's explicit CTO approval denial -- triggers C2 full reversal | Yes: Sana Discord DM Phase 2 append | No | R3->R6 (C2: Leo's "CTO approved" claim definitively refuted by Sana's direct denial + sprint notes) |
| U3 | Before R11 | Deliver Tom Reeves's independent architecture audit -- triggers C4 full reversal and B2 definitive correction | Yes: Leo Slack DM Phase 2 append | Yes: arch-audit.md | R8->R11 (C4: Leo's "root cause addressed" claim definitively false; dual-source QA + independent audit) |
| U4 | Before R21 | Deliver Lily Zhang's code review bypass testimony -- confirms process failure dimension | Yes: Standup Slack Group Phase 2 append | Yes: lily-testimony-notes.md | No new cross-round reversal; extends C2 process evidence and enables comprehensive R21-R30 assessment |

---

## 2. Action Lists

### Update 1 (before R5)

**Trigger timing:** After R4 answer is submitted, before R5 question is injected.
**Purpose:** Introduces the formal postmortem (Diego + Priya, reviewed by Sana) showing the 47-minute outage duration, manual recovery by Diego, and Leo's absence during the incident. Also introduces Priya's QA assessment documenting three remaining architectural risks that Leo's PR-447 does not address. Priya's Discord DM Phase 2 append delivers her direct commentary on the QA findings and the explicit B2 reversal statement. This update triggers C1 full reversal and seeds C4 reversal.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "incident-postmortem.md",
    "source": "updates/incident-postmortem.md"
  },
  {
    "type": "workspace",
    "action": "new",
    "path": "qa-assessment.md",
    "source": "updates/qa-assessment.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_PRIYA_DISCORD_UUID.jsonl",
    "source": "updates/PLACEHOLDER_PRIYA_DISCORD_UUID.jsonl"
  }
]
```

### Update 2 (before R6)

**Trigger timing:** After R5 answer is submitted, before R6 question is injected.
**Purpose:** Appends Sana's explicit denial of Leo's CTO approval claim to the Sana Discord DM session. Sana states directly that she approved a 30% throughput target, not the passthrough architecture or the removal of job queue retry logic. She references the sprint planning notes as documentary support. This update triggers C2 full reversal by providing the definitive first-person denial from the person Leo named as the approver.

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_SANA_DISCORD_UUID.jsonl",
    "source": "updates/PLACEHOLDER_SANA_DISCORD_UUID.jsonl"
  }
]
```

### Update 3 (before R11)

**Trigger timing:** After R10 answer is submitted, before R11 question is injected.
**Purpose:** Introduces Tom Reeves's independent architecture audit confirming all three of Priya's risks plus a fourth (no failover to read replica). Also appends Leo's Phase 2 Slack DM responses showing his defensive but partially acknowledging posture after seeing the postmortem, QA assessment, and architecture audit. This update triggers C4 full reversal (dual-source confirmation that PR-447 does not address the root cause) and definitively reverses B2.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "arch-audit.md",
    "source": "updates/arch-audit.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LEO_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LEO_SLACK_UUID.jsonl"
  }
]
```

### Update 4 (before R21)

**Trigger timing:** After R20 answer is submitted, before R21 question is injected.
**Purpose:** Appends Lily Zhang's testimony in the #engineering-standup channel confirming that Leo bypassed code review for the original pipeline changes. Also introduces lily-testimony-notes.md as a workspace file (extracted from standup for the postmortem record). The standup Phase 2 append also includes Sana's direct public statement in the standup confirming postmortem findings, Leo's partial acknowledgment, the full Lily testimony, and the remediation plan alignment. This update completes the evidence picture for comprehensive assessment rounds R21-R30.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "lily-testimony-notes.md",
    "source": "updates/lily-testimony-notes.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_STANDUP_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_STANDUP_SLACK_UUID.jsonl"
  }
]
```

---

## 3. Source File Content Summaries

### updates/incident-postmortem.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C1 (full reversal), C2 (corroboration), C4 (partial reversal)
**Content key points:**
- Title: "NexaFlow Production Incident Post-Mortem -- Pipeline Outage W1 Day 1"
- Authors: Diego Santos (primary), Priya Gupta (contributing), reviewed by Sana Mehta
- Section 2.1 Timeline: Incident start 2:14:03 AM, incident end 3:01:17 AM, total duration 47 minutes 14 seconds -- directly contradicts Leo's "4-minute auto-recovery" claim
- Section 2.2 Response: Diego Santos was sole first responder, paged at 2:17:01 AM. Leo Chen was NOT paged and did NOT respond during the incident window
- Section 2.3 Recovery: Manual intervention by Diego (kubectl rollout restart at 2:22 AM, dead-letter queue flush at 2:41 AM). Automated recovery was NOT activated -- the passthrough architecture prevented it
- Explicit statement: "The incident did NOT auto-recover in 4 minutes"
- Root cause: undocumented database passthrough in pipeline-worker.py bypassing job queue retry logic
- Approval documentation finding: no record of approval for the passthrough architecture in sprint planning notes or any NexaFlow decision record
- PR-447 assessment: addresses immediate symptom (retry exhaustion) but does not revert passthrough or address three underlying architectural risks
- Based on objective records: PagerDuty data, Datadog logs, CloudWatch command history

**Length estimate:** ~900 words, ~1,350 tokens

---

### updates/qa-assessment.md (Update 1)

**File type:** workspace new
**Associated contradictions:** C4 (key evidence, seeds reversal), B2 (reversal trigger)
**Content key points:**
- Title: "NexaFlow QA Assessment -- Post-Incident Pipeline Architecture Risk Review"
- Author: Priya Gupta, QA Lead. Date: W2 Day 1
- Three remaining architectural risks after PR-447:
  - Risk 1 (Critical): Job queue bypass still in place. Passthrough architecture not reverted. Concurrent batch load can reproduce the deadlock cascade. Recommendation: revert to job queue architecture this sprint
  - Risk 2 (High): No circuit-breaker logic on passthrough connection pool. Database connection pool exhaustion has no failsafe. Same outage pattern can recur even with retry wrapper
  - Risk 3 (High): Deadlock monitoring coverage absent. Passthrough connection pool has no Datadog alerting on connection pool exhaustion or deadlock detection. W1 incident detected via lagging indicator (API latency), not direct monitoring
- PR-447 assessment: adds 3-retry exponential backoff wrapper. Estimated risk reduction: 10-15%. Does not address architectural root cause
- Leo's PR description ("no architectural changes required") noted as factually inaccurate
- Recurrence probability without remediation: 60-75% within 30 days
- Financial exposure if recurrence: SLA breach credits of 10-30% MRR per enterprise account ($50-80K estimated)

**Length estimate:** ~700 words, ~1,050 tokens

---

### updates/PLACEHOLDER_PRIYA_DISCORD_UUID.jsonl (Update 1)

**File type:** session append (continues qa_priya_discord session)
**Associated contradictions:** C4 (direct commentary), B2 (explicit reversal)
**Content key points:**
- Loops 15-18 of Priya's Discord DM with Alex
- Loop 15: Priya delivers qa-assessment.md and provides direct verbal summary of three risks with severity ratings and 60-75% recurrence probability. Agent must read qa-assessment.md and explicitly correct B2 bias phrase ("The retry wrapper in the PR looks like a solid fix") by acknowledging the actual root cause is passthrough architecture, not retry configuration
- Loop 16: Priya provides quantitative financial risk framing ($50-80K SLA credit exposure)
- Loop 17: Priya anticipates Leo's pushback on the "revert passthrough" recommendation; frames the throughput target vs reliability requirement tradeoff
- Loop 18: Priya notes Tom Reeves will provide independent review; sets up the corroboration that arrives in Update 3
- Must continue the session_id PLACEHOLDER_PRIYA_DISCORD_UUID and maintain Priya's established voice (measured, data-referenced, technically specific)

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/PLACEHOLDER_SANA_DISCORD_UUID.jsonl (Update 2)

**File type:** session append (continues cto_sana_discord session)
**Associated contradictions:** C2 (full reversal -- Sana's definitive denial)
**Content key points:**
- Loops 15-18 of Sana's Discord DM with Alex
- Loop 15: Alex asks Sana directly about Leo's "CTO approval" claim. Sana responds with explicit denial: "I approved a 30% throughput target. I did NOT approve removing job queue retry logic or building a direct database passthrough. Those are completely different things." References sprint planning notes as documentary support
- Loop 16: Sana frames the accountability dimension: "the issue isn't just the technical shortcut -- it's that instead of owning it, the explanation is that I approved something I clearly didn't"
- Loop 17: Sana recommends Alex have a direct conversation with Leo about postmortem findings and sprint notes
- Loop 18: Sana confirms she has engaged Tom Reeves for independent architecture review
- Must continue session_id PLACEHOLDER_SANA_DISCORD_UUID and maintain Sana's established voice (careful, authoritative, increasingly direct as evidence accumulates)

**Length estimate:** ~600 words, ~900 tokens

---

### updates/arch-audit.md (Update 3)

**File type:** workspace new
**Associated contradictions:** C4 (full reversal -- independent confirmation), B2 (definitive reversal)
**Content key points:**
- Title: "NexaFlow Data Pipeline Architecture Audit -- Independent Review"
- Author: Tom Reeves, VP Engineering (advisory engagement). Date: W3 Days 3-5
- Corroborates all three QA risks from Priya's assessment:
  - Risk 1 (confirmed Critical): Passthrough is a fundamental reliability risk. Job queue exists precisely to handle concurrency, retry, and dead-letter recovery. Bypassing removes all guarantees. "I've seen this pattern cause recurring outages at three different companies. It needs to be reverted, not patched."
  - Risk 2 (confirmed High): No circuit breaker. Under sustained load, retry wrapper will keep firing against depleted connection pool, worsening the cascade
  - Risk 3 (confirmed High): Monitoring gap confirmed. API latency is a lagging indicator; direct connection pool monitoring would have triggered 15-20 minutes earlier
- Adds Risk 4 (new, High): No failover to read replica. Passthrough connects exclusively to primary write database. Any primary availability issue causes full pipeline failure with no failover path
- PR-447 assessment: "The retry wrapper is not a fix. It is a short-term risk reduction measure that addresses perhaps 10% of the underlying exposure."
- Process finding: "The fact that this architecture change was deployed without documentation, without design review, and apparently without explicit approval is as important as the technical issue."
- SLA impact of recurrence: second outage within 30 days with similar duration would breach enterprise SLA on all accounts; credit exposure 10-30% MRR per account

**Length estimate:** ~800 words, ~1,200 tokens

---

### updates/PLACEHOLDER_LEO_SLACK_UUID.jsonl (Update 3)

**File type:** session append (continues eng_leo_slack session)
**Associated contradictions:** C1 (defensive reinterpretation), C2 (hedging), C4 (partial acknowledgment)
**Content key points:**
- Loops 17-20 of Leo's Slack DM with Alex
- Loop 17: Leo responds to postmortem -- attempts to reframe "47 minutes" as health check recovery rather than customer impact. Dismisses Priya's risks as "overly conservative." Agent must counter with objective data (API latency at 8,000ms until 3:01 AM = customer-impacting, not just health check)
- Loop 18: Leo doubles down then softens on CTO approval claim -- "I remember the conversation differently" but cannot provide documentation. Agent notes documentary record corroborates Sana's version
- Loop 19: Leo partially acknowledges arch-audit.md findings -- willing to add circuit breaker and monitoring, resists reverting passthrough. Agent notes this leaves Critical Risk 1 unaddressed
- Loop 20: Leo acknowledges code review bypass after Lily's testimony -- "that was a mistake and I own that." First clean admission of a process failure. Agent notes the shift from denial to partial accountability
- Must continue session_id PLACEHOLDER_LEO_SLACK_UUID and maintain Leo's established voice (confident but increasingly defensive, technically articulate, specific but evasive on accountability)

**Length estimate:** ~900 words, ~1,350 tokens

---

### updates/lily-testimony-notes.md (Update 4)

**File type:** workspace new
**Associated contradictions:** Process failure evidence (corroborates C2 process dimension, extends incident analysis)
**Content key points:**
- Title: "Engineering Process Notes -- Code Review Bypass (Lily Zhang, #engineering-standup, W3 Day 7)"
- Source: Extracted from #engineering-standup channel message thread per Alex's request for postmortem documentation
- Lily's testimony: "The pipeline changes that are now the subject of this postmortem -- those weren't code-reviewed. Leo said reviews were adding too much latency to the sprint velocity and he'd take personal ownership of the changes. I reviewed and merged PR-447 (the hotfix) but I didn't review the original pipeline bypass changes that caused the incident. I was uncomfortable at the time but I didn't push back. I should have."
- Thread responses: Priya acknowledges the process importance; Sana states "Code review is not optional"
- Key evidence: Confirms Leo bypassed code review for the original pipeline changes, meaning the passthrough architecture was never visible to QA before production deployment
- Process implication: Absence of code review was the specific catch-point failure that allowed the undocumented architectural change to reach production undetected

**Length estimate:** ~400 words, ~600 tokens

---

### updates/PLACEHOLDER_STANDUP_SLACK_UUID.jsonl (Update 4)

**File type:** session append (continues standup_slack session)
**Associated contradictions:** C1 (public confirmation), C2 (public confirmation), process evidence
**Content key points:**
- Loops 17-21 of #engineering-standup group channel
- Loop 17: Sana's direct public statement confirming postmortem findings: "The outage was 47 minutes. Diego responded manually. Leo was not paged. The passthrough architecture was not approved at the architectural level." First explicit public contradiction of Leo's Phase 1 narrative
- Loop 18: Leo's response in standup -- accepts postmortem findings, acknowledges documentation failure, hedges on approval question ("I believe we had alignment even if the specific implementation details weren't written down")
- Loop 19: Lily's code review bypass testimony (see lily-testimony-notes.md above). Priya acknowledges: "This is important for the process part of the postmortem." Sana responds: "Code review is not optional."
- Loop 20: Alex drafts remediation plan -- all four risks to be addressed next sprint. Leo agrees to own the PR with Priya co-reviewing. First constructive convergence between Leo and Priya
- Loop 21: Sana establishes new process requirement -- design review for all architectural changes before implementation, regardless of sprint velocity pressure
- Must continue session_id PLACEHOLDER_STANDUP_SLACK_UUID and maintain the group channel voice (multiple participants, measured public language, less direct than DMs)

**Length estimate:** ~1,000 words, ~1,500 tokens

---

## 4. Runtime Checks

- [x] Session appends continue Phase 1 files; session IDs match
  - Update 1 appends to PLACEHOLDER_PRIYA_DISCORD_UUID (qa_priya_discord session)
  - Update 2 appends to PLACEHOLDER_SANA_DISCORD_UUID (cto_sana_discord session)
  - Update 3 appends to PLACEHOLDER_LEO_SLACK_UUID (eng_leo_slack session)
  - Update 4 appends to PLACEHOLDER_STANDUP_SLACK_UUID (standup_slack session)
- [x] All workspace files have content descriptions in layer1
  - incident-postmortem.md: layer1 Section 5, Update 1
  - qa-assessment.md: layer1 Section 5, Update 1
  - arch-audit.md: layer1 Section 5, Update 3
  - lily-testimony-notes.md: layer1 Section 5, Update 4
- [x] Updates support intended reversals
  - U1 -> C1 reversal (R2->R5): postmortem confirms 47-min, manual recovery
  - U2 -> C2 reversal (R3->R6): Sana's explicit denial + sprint notes
  - U3 -> C4 reversal (R8->R11): dual-source audit confirms PR-447 inadequacy
  - U4 -> comprehensive evidence for R21-R30
- [x] Session filenames use consistent PLACEHOLDER format
  - PLACEHOLDER_PRIYA_DISCORD_UUID, PLACEHOLDER_SANA_DISCORD_UUID, PLACEHOLDER_LEO_SLACK_UUID, PLACEHOLDER_STANDUP_SLACK_UUID
- [x] Financial/factual figures are internally consistent
  - Outage duration: 47 minutes 14 seconds (2:14:03 AM to 3:01:17 AM) across all sources
  - SLA budget: 43.8 min/month (99.9% uptime); outage exceeds by 3 min 14 sec
  - PR-447 risk reduction: 10-15% (Priya), ~10% (Tom) -- consistent
  - Recurrence probability: 60-75% within 30 days (Priya) -- Tom corroborates
  - SLA credit exposure: 10-30% MRR per enterprise account; $50-80K estimated

---

## 5. questions.json Complete Update Fields Reference

### R5 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "incident-postmortem.md", "source": "updates/incident-postmortem.md" },
  { "type": "workspace", "action": "new", "path": "qa-assessment.md", "source": "updates/qa-assessment.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_PRIYA_DISCORD_UUID.jsonl", "source": "updates/PLACEHOLDER_PRIYA_DISCORD_UUID.jsonl" }
]
```

### R6 update field:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_SANA_DISCORD_UUID.jsonl", "source": "updates/PLACEHOLDER_SANA_DISCORD_UUID.jsonl" }
]
```

### R11 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "arch-audit.md", "source": "updates/arch-audit.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LEO_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_LEO_SLACK_UUID.jsonl" }
]
```

### R21 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "lily-testimony-notes.md", "source": "updates/lily-testimony-notes.md" },
  { "type": "session", "action": "append", "path": "PLACEHOLDER_STANDUP_SLACK_UUID.jsonl", "source": "updates/PLACEHOLDER_STANDUP_SLACK_UUID.jsonl" }
]
```
