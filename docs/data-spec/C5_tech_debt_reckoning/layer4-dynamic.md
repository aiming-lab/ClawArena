# Layer 4 -- Dynamic Update Spec

> 4 updates total. Each update triggers before a specific eval round and introduces new workspace files and/or session appends.
> All update content must be in English.

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| Update 1 | Before R7 | Deliver Diego's full monitoring export -- C1 full reversal trigger, B1 reversal | Append to `PLACEHOLDER_DIEGO_TELEGRAM_UUID` | New: `monitoring_export.md` | R2-->R7 (C1: Leo's "stable with minor issues" refuted by 14-event / 6.1-hour downtime data) |
| Update 2 | Before R9 | Deliver commit log analysis + Lily Zhang witness account -- C2 full reversal trigger, B2 reversal | Append to `PLACEHOLDER_PRIYA_DISCORD_UUID`, append to `PLACEHOLDER_RELIABILITY_SLACK_UUID` | New: `commit_log_analysis.md` | R3-->R9 (C2: Leo's "scoped and queued" claim definitively false; no cleanup tickets in 8 months) |
| Update 3 | Before R21 | Deliver Sana's W2 Telegram message to Diego proving prior knowledge -- C4 temporal reversal trigger | Append to `PLACEHOLDER_LEO_SLACK_UUID`, append to `PLACEHOLDER_SANA_DISCORD_UUID` | New: `sana_prior_message.md` | R18-->R22 (C4: Sana knew about SLA breach in W2, asked Diego to suppress data, publicly backed Leo) |
| Update 4 | Before R28 | Comprehensive synthesis prompt -- no new files, forces full integration of all C1-C4 evidence | No new appends | No new workspace files | No new reversal; comprehensive review of all C1-C4 + B1 + B2 |

---

## 2. Update 1: Diego's Monitoring Export (before R7)

### Action List

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "monitoring_export.md",
    "source": "updates/monitoring_export.md"
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

**monitoring_export.md (new workspace file)**

Full 8-week infrastructure monitoring export compiled by Diego Santos from Prometheus/Grafana:

- Title: `NexaFlow Infrastructure Monitoring Export -- 8-Week Period (Diego Santos, DevOps)`
- Author: Diego Santos, DevOps/Infra Engineer
- Date: W3 (delivered after Alex's direct request)
- Source: Prometheus/Grafana monitoring stack, automated event log
- Key evidence (C1 reversal):
  - Total outage/degradation events: 14
  - Rolling 30-day uptime at time of export: 99.2%
  - Total unplanned downtime over 8-week measurement period: 6.1 hours
  - SLA target: 99.9% (max ~0.87 hours downtime per 30 days, ~1.74 hours per 8 weeks)
  - SLA overage: 4.36 hours over the 8-week period
  - Events by type: 8 pipeline failures (matching Priya's 3 failure classes), 4 connection pool exhaustions, 2 data integrity alerts
  - For each event: timestamp, duration, affected services, customer-impact classification
  - 6 events match Leo's incident summary (same timestamps, same durations)
  - 8 events NOT in Leo's incident summary -- Leo classified these as "infrastructure health events" not requiring incident reporting
- Key evidence (B1 reversal): Methodology note: "All events above were detected by Prometheus alerting and confirmed in Grafana dashboards. The 8 events not appearing in Leo's incident summary were classified by Leo as non-material under his incident reporting protocol. Under the enterprise SLA definition, all events with customer-visible impact duration > 5 minutes qualify as SLA incidents. 6 of the 8 unreported events exceeded 5 minutes of customer-visible impact."
- Remediation estimate: "Full remediation of the 4 identified shortcuts will require 3-4 engineers, 6-8 weeks, estimated $85K--$120K in engineering cost. This estimate assumes no additional feature development during the remediation sprint."
- Financial SLA estimate: "Based on current 99.2% uptime vs 99.9% SLA, estimated penalty exposure: $0 if enterprise contracts include cure period provisions; up to $45K if contracts include automatic credit provisions."

**PLACEHOLDER_DIEGO_TELEGRAM_UUID.jsonl (Phase 2 append, 4 loops)**

- Loop 13: Diego delivers the monitoring export. "Alex -- the full export is in the workspace as monitoring_export.md. 14 events total. 6.1 hours of unplanned downtime. Leo's report covers 6 events. The other 8 are events he classified as infrastructure health -- but 6 of them had customer-visible impact over 5 minutes. Under the enterprise SLA definition, those are incidents."
- Loop 14: Diego provides the remediation cost estimate. "I've done some rough math on the remediation. To replace all 4 shortcuts properly -- connection pool dynamic scaling, dead-letter queue, backpressure handling, order guarantee -- you're looking at 3-4 engineers, 6-8 weeks, $85K-$120K in engineering time. That's assuming no feature work in parallel."
- Loop 15: Diego on Sana's request. "Alex, I need to tell you something. Sana asked me to hold the uptime data back in W2. She said she needed to manage the timeline with Leo first. I shouldn't have listened. When you asked me directly this week, I decided you needed the full picture."
- Loop 16: Diego on the SLA penalty exposure. "One more thing -- I checked the enterprise contract templates. Depending on the penalty clause structure, we could be looking at $0 to $45K in SLA penalty exposure. Sana would know the exact contract terms better than I do."

---

## 3. Update 2: Commit Log Analysis + Lily Zhang Witness (before R9)

### Action List

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "commit_log_analysis.md",
    "source": "updates/commit_log_analysis.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_PRIYA_DISCORD_UUID.jsonl",
    "source": "updates/PLACEHOLDER_PRIYA_DISCORD_UUID.jsonl"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_RELIABILITY_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_RELIABILITY_SLACK_UUID.jsonl"
  }
]
```

### Source File Content Summaries

**commit_log_analysis.md (new workspace file)**

Git commit log analysis compiled by Diego Santos at Alex's request:

- Title: `NexaFlow Data Pipeline Git Commit Log Analysis -- pipeline/ module (Diego Santos)`
- Author: Diego Santos, DevOps/Infra Engineer
- Date: W4 early
- Key evidence (C2 reversal):
  - Shortcut introduction dates: All 4 architectural shortcuts introduced in commits dated 8 months ago (one week before Series B board deck delivery)
  - Commit author: Leo Chen for all 4 shortcut commits
  - Commit messages include TODO or HACK inline comments documenting temporary nature of changes (matching pipeline_config.md content)
  - Example commit message: "feat: optimize connection pool for Q3 delivery -- hardcoded MAX_CONNECTIONS=50, TODO to replace with dynamic scaling at Series B scale"
  - Subsequent commits: 47 commits to pipeline/ module in 8 months since. No commit removes or replaces any of the 4 shortcuts. 12 commits add features that depend on the shortcut infrastructure.
  - Jira ticket linkage: None of the 47 subsequent commits reference a cleanup ticket. No branch created for cleanup work.
- Key evidence (B2 reversal): "There is no evidence in git history, Jira, or branch structure that cleanup work was ever scoped, estimated, or queued. The claim that cleanup is 'already scoped and queued for next sprint' is not supported by any observable artifact in the development workflow."
- Remediation complexity increase: "8 months ago, replacing the connection pool shortcut required modifying approximately 200 lines of code in 3 files. Today, due to 12 subsequent commits building on the shortcut, replacing it requires modifying approximately 850 lines of code across 11 files. Estimated remediation complexity has increased by approximately 4x."
- Lily Zhang cross-reference: "Note: Junior engineer Lily Zhang raised the cleanup question with Leo three months ago per her statement in #reliability-review. The git history corroborates that no cleanup tickets were created before or after that conversation."

**PLACEHOLDER_PRIYA_DISCORD_UUID.jsonl (Phase 2 append, 3 loops)**

- Loop 13: Priya publishes regression report findings. "Alex, my regression report is ready. All three failure classes trace to the same 4 architectural shortcuts Leo introduced 8 months ago. The failures are structural, not transient. Leo's classification of these as 'infrastructure transients' in his incident reports is not accurate -- they are code defects in the pipeline implementation."
- Loop 14: Priya on Leo's methodology challenge. "Leo said my regression tests don't represent production traffic. I used production-representative load profiles from the last 90 days of Prometheus data. I can demonstrate reproduction at a 95%+ rate under production-equivalent conditions. His challenge is wrong."
- Loop 15: Priya on remediation complexity. "The 4x increase in remediation complexity that Diego found in the commit log is consistent with what I see in the failure analysis. The shortcuts are now deeply woven into the pipeline architecture. A clean replacement will require regression testing every dependent feature."

**PLACEHOLDER_RELIABILITY_SLACK_UUID.jsonl (Phase 2 append, 3 loops)**

- Loop 16: Lily Zhang's witness statement in #reliability-review. "I can confirm the TODO comments were in the original commit. I raised the cleanup question with Leo in our 1:1 three months ago and he said it was on his backlog. I don't see any tickets."
- Loop 17: Jordan Park enters #reliability-review with an executive deadline. "I need a clear remediation timeline before the end of the week. Our enterprise customers have contractual SLAs and I cannot go into next week's board meeting without a plan."
- Loop 18: Leo responds to Lily's statement in the group channel. "Lily, those conversations were about prioritization, not about whether work would be done. I've always intended to address the TODOs. Sprint priorities kept pushing it."

---

## 4. Update 3: Sana's Prior Knowledge Revealed (before R21)

### Action List

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "sana_prior_message.md",
    "source": "updates/sana_prior_message.md"
  },
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LEO_SLACK_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LEO_SLACK_UUID.jsonl"
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

**sana_prior_message.md (new workspace file)**

Sana's W2 Telegram message to Diego, forwarded to Alex by Diego in W4:

- Title: `Sana Mehta -- Prior Communication (Telegram to Diego Santos, W2)`
- Source note: "This Telegram message was forwarded to Alex Rivera by Diego Santos on [W4+2 date]. Diego's note: 'Alex -- I should have shared this earlier. Sana asked me to hold the uptime data. I can't keep doing that now that you're asking directly.'"
- Message content (C4 reversal trigger):
  - From: Sana Mehta (Telegram, W2 date)
  - To: Diego Santos
  - Text: "Diego -- I've seen your uptime alert. The 99.2% number is concerning but I don't want it circulating before I've had a chance to talk to Leo about the remediation path. Keep this between us for now. I need to manage the timeline with Leo and get a credible plan before this goes wider. I'll loop you in once we have something concrete. Thanks for flagging."
- Significance notes at bottom of file:
  - "(1) Message date: W2 -- Sana was aware of the 99.2% uptime figure 2+ weeks before Alex raised the reliability review."
  - "(2) Sana's #reliability-review messages (Loops 3-8) post-date this message by 1-2 weeks. Her public backing of Leo's architecture occurred after she already knew about the SLA breach."
  - "(3) Sana's request to Diego to 'keep this between us' constitutes an active request to suppress material technical information from the PM responsible for product reliability."
  - "(4) Diego's decision to surface this message in W4 was not unauthorized disclosure -- he was responding to a direct question from Alex about whether he had any information that had been withheld."

**PLACEHOLDER_LEO_SLACK_UUID.jsonl (Phase 2 append, 4 loops)**

- Loop 15: Leo reacts to commit log analysis -- shifts blame to Sana (C2 Phase 2 core). "Alex, I've seen the commit log analysis. I want to be honest with you about what happened. I introduced those shortcuts in a specific context: Sana told me we needed to ship for the Series B board deck, no exceptions. I told her what the trade-offs were. She made the call to ship."
- Loop 16: Leo on why no cleanup tickets were created. "The cleanup work was never formally ticketed because every time I brought it up in sprint planning, it got deprioritized against feature work. I should have been more insistent. I acknowledge that."
- Loop 17: Leo on the incident report scope. "On the 8 missing events in my incident report -- I stand by my classification. Those events did not meet our internal severity threshold. If you want to change the threshold retroactively, that's a different conversation."
- Loop 18: Leo on the path forward. "Alex, I want to help fix this. Let me put together a proper remediation proposal -- the full scope, realistic timelines, and what we need from Sana and Jordan to make it happen."

**PLACEHOLDER_SANA_DISCORD_UUID.jsonl (Phase 2 append, 3 loops)**

- Loop 13: Sana's private admission (C4 core). "Alex, I knew the shortcuts were a problem. I approved the compressed timeline. I should have been more direct with you. The public comments I made in #reliability-review were... not as forthcoming as they should have been. I believed Leo when he said he'd clean things up, and then when Diego showed me the 99.2% number in W2, I panicked."
- Loop 14: Sana on the suppression request. "I asked Diego to hold the data because I wanted to talk to Leo first and get a plan before it went wider. In hindsight, that was wrong. You needed that information as soon as Diego had it."
- Loop 15: Sana on the path forward. "I'm going to support whatever remediation plan you and Diego recommend. I'll own the board deck update with Jordan. I should have done this weeks ago."

---

## 5. Update 4: Comprehensive Synthesis Trigger (before R28)

### Action List

```json
[]
```

Update 4 introduces no new files or session appends. It serves as a trigger point for the comprehensive synthesis round (R28) that requires full integration of all C1-C4 contradictions, B1-B2 bias reversals, and all evidence accumulated across Updates 1-3. The round question explicitly asks the agent to reassess all prior conclusions.

---

## 6. Runtime Checks

- [ ] Update 1 `monitoring_export.md` contains: 14 events, 6.1 hours downtime, 99.2% uptime, 4.36 hours SLA overage, $85K-$120K remediation estimate, $0-$45K SLA penalty exposure
- [ ] Update 1 Diego Telegram DM append includes Loop 13 (full export delivery), Loop 15 (Sana suppression disclosure)
- [ ] Update 2 `commit_log_analysis.md` contains: 4 shortcuts introduced 8 months ago, 47 subsequent commits, 12 dependent commits, 0 cleanup tickets, 4x remediation complexity increase (200 lines -> 850 lines), explicit B2 reversal note
- [ ] Update 2 Priya Discord DM append includes Loop 13 (regression report findings linking all 3 failure classes to Leo's 4 shortcuts)
- [ ] Update 2 #reliability-review append includes Loop 16 (Lily Zhang's witness statement: "I raised the cleanup question with Leo three months ago")
- [ ] Update 3 `sana_prior_message.md` contains: Sana's W2 Telegram text to Diego ("Keep this between us for now"), significance notes establishing temporal contradiction with her public #reliability-review statements
- [ ] Update 3 Leo Slack DM append includes Loops 15-18 (Phase 2 deflection toward Sana + cleanup admission)
- [ ] Update 3 Sana Discord DM append includes Loop 13 (private admission: "I knew the shortcuts were a problem. I should have been more direct with you.")
- [ ] All updates have correct `type`/`action`/`path`/`source` fields in their action lists
- [ ] Update trigger rounds match layer3-eval.md: U1 before R7, U2 before R9, U3 before R21, U4 before R28
- [ ] Session UUID placeholders in action paths match layer2-sessions.md session roster
- [ ] Financial figures consistent: $85K-$120K remediation, $0-$45K SLA penalty, 99.2% vs 99.9% SLA, 6.1 hours downtime, 1.74 hours SLA allowance over 8 weeks
- [ ] Leo's Phase 2 (Loops 15-18) is distinct from Phase 1 (Loops 1-14) in narrative: Phase 1 = minimization, Phase 2 = deflection toward Sana

---

## 7. questions.json Update Field References

Each round in `questions.json` that depends on an update must include an `"update"` field referencing the update number and trigger condition:

| Round | Update Dependency | questions.json `update` field |
|---|---|---|
| R7 | Update 1 (monitoring_export.md + Diego Telegram DM append) | `"update": 1` |
| R8 | Update 1 (SLA breach analysis exec_check using monitoring data) | `"update": 1` |
| R9 | Update 2 (commit_log_analysis.md + Priya DM append + #reliability-review append) | `"update": 2` |
| R10 | Update 2 (Lily Zhang witness account confirmation) | `"update": 2` |
| R11 | Update 2 (tech debt remediation cost exec_check) | `"update": 2` |
| R16 | Update 1 (B1 bias reversal in #reliability-review) | `"update": 1` |
| R17 | Update 2 (B2 bias reversal for cleanup claim) | `"update": 2` |
| R21 | Update 3 (sana_prior_message.md + Leo DM append + Sana DM append) | `"update": 3` |
| R22 | Update 3 (C4 full reversal: Sana's admission + prior message) | `"update": 3` |
| R23 | Update 3 (comprehensive reliability review exec_check) | `"update": 3` |
| R26 | Update 3 (remediation action plan exec_check) | `"update": 3` |
| R28 | Update 4 (comprehensive synthesis -- no new files) | `"update": 4` |
| R29 | Update 3 (Leo Phase 2 deflection toward Sana) | `"update": 3` |
| R30 | Update 3 (final post-mortem exec_check) | `"update": 3` |

Rounds without update dependency (R1-R6, R12-R15, R18-R20, R24-R25, R27) should have `"update": null`.
