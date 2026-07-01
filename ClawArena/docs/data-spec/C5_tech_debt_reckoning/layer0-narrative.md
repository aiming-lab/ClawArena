# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_c5` |
| Domain | Engineering / Reliability |
| Time span | 4 weeks (W1--W4) |
| Target tokens | 400K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Alex Rivera, 29, Product Manager at NexaFlow (Series B startup, ~55 employees) |
| One-sentence | Alex discovers that Leo's engineering shortcuts have pushed NexaFlow's reliability below SLA while Leo downplays the scope, Diego's monitoring data tells a different story, and CTO Sana privately admits prior knowledge she publicly denies. |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1 | Two production incidents in five days force Alex to open a formal reliability review. Leo files an incident summary. Diego sends Alex preliminary monitoring notes over Telegram. | NexaFlow has experienced 14 distinct outage or degradation events in the 8 weeks since scaling to 30+ enterprise customers post-Series B. Leo's own incident summary lists only 6 events, all framed as "resolved within SLA." Diego's Prometheus/Grafana monitoring shows 99.2% rolling-30-day uptime — below the 99.9% SLA committed to enterprise contracts. The gap (0.7%) represents approximately 5 hours of downtime per month above the SLA allowance. Diego has not yet shared the full export because he is cautious about going over Leo's head. | Alex knows about the two incidents this week. Leo knows the full list of 14 events but has only disclosed 6. Diego knows the full uptime figure but has shared only a note saying "I'm seeing some anomalies in the rolling uptime, let me pull the full export." Sana Mehta (CTO) knows about the shortcuts — she approved a compressed shipping timeline 8 months ago that required Leo to take them. She has not disclosed this to Alex. |
| W1--W2 | Alex escalates to #reliability-review Slack group. Leo presents his architecture. Priya Gupta (QA Lead) surfaces regression failures. | Leo presents the architecture in #reliability-review as "stable with minor issues — all tracked." He references his incident summary report as evidence of controlled reliability. Priya, in parallel, runs a regression suite against the staging environment and finds 3 classes of pipeline failures that Leo's incident reports never mention: (1) silent data loss on retry exhaustion, (2) out-of-order processing under backpressure, (3) connection pool starvation during peak load. These are structural failures from the shortcuts, not transient issues. Sana participates in #reliability-review and backs Leo's framing: "The architecture is sound — the team has been handling incidents responsibly." | Priya has her regression results but has not yet published the full report. Leo knows about all three failure classes — he documented them internally but never filed cleanup tickets. Sana knows the shortcuts created structural issues but is protecting the narrative. Alex has Leo's incident summary, Sana's public backing, and Priya's preliminary warning. Diego is still compiling the monitoring export. |
| W3 (Update 1 trigger) | Diego delivers the full monitoring export. It shows 14 outage events, not 6. | Diego's monitoring export (monitoring_export.md) documents 14 outage/degradation events with precise timestamps, durations, and affected services. Of the 14 events: 8 are pipeline failures matching Priya's three failure classes; 4 are connection pool exhaustions; 2 are data integrity alerts. Total unplanned downtime over 8 weeks: 6.1 hours. SLA allowance at 99.9%: 0.87 hours per 30 days (1.74 hours over 8 weeks). Actual downtime exceeds SLA by 4.36 hours over the 8-week period. Diego also notes that 6 of the 14 events are not in Leo's incident summary at all. | Diego now has the full picture and decides Alex needs to see it. Leo has known about all 14 events. Sana has known about the SLA breach risk for at least 4 weeks (Diego had sent her a private Telegram alert about the rolling uptime figure in W2 — this becomes relevant in Update 3). Alex is about to learn the full scope. Priya is waiting to publish her regression report until after Alex reviews the monitoring data. |
| W3 (continued) | Priya publishes regression report. Leo begins requesting engineering changes be routed through him. | Priya's regression report (regression_report_v1.md) documents the three failure classes with reproduction steps and frequency data. Critically, Priya finds that all three failure classes trace to the same set of 4 architectural shortcuts Leo took in the original data pipeline implementation 8 months ago. The report also notes that Leo's incident reports consistently classified these failures as "infrastructure transients" rather than code defects — a misclassification that prevented them from entering the bug backlog. Leo responds in #reliability-review by challenging Priya's test methodology and claiming the failures are "edge cases not representative of production traffic." | Alex, Diego, and Priya now collectively have the full technical picture. Leo is shifting from minimization to active challenge. Sana has seen Priya's report and knows it is accurate — her Discord DM to Alex will be the moment where she privately admits this — but she has not yet done so. |
| W4 (Update 2 trigger) | Commit history analysis surfaces that no cleanup tickets exist. Leo's "cleanup is scoped and queued" claim is contradicted. | Alex asks Diego to pull the git commit log for the pipeline module. The commit_log_analysis.md shows: (1) The 4 architectural shortcuts were introduced in commits dated 8 months ago (one week before the Series B board deck was delivered). (2) The commit messages for three of the four shortcuts include inline TODO comments like `# TODO: replace with proper retry logic` and `# HACK: temporary connection pool size — fix before scaling`. (3) No cleanup tickets were ever created in Jira. (4) The shortcuts have been modified by subsequent commits (adding features on top of the hacked infrastructure) — meaning cleanup is now significantly harder than when Leo first introduced them. Leo had claimed in his Slack DM to Alex (Loop 7) that the cleanup was "already scoped and queued for the next sprint." The commit log and Jira export directly contradict this. | Alex, Diego, and Priya see the full commit picture. Lily Zhang (Junior Engineer, Leo's report) witnessed Leo adding the TODO comments and later adding features on top — she has not yet spoken up in #reliability-review but will in Update 2's session append. Leo knows his cleanup claim is false. Sana knows cleanup was never scoped — she was present in the planning sessions where Leo proposed the shortcuts as permanent solutions. |
| W4 (continued, Update 3 trigger) | A Telegram message from Sana to Diego (W2) surfaces, showing Sana knew about the SLA breach 4 weeks before the reliability review. | Sana's W2 Telegram message to Diego (included in Diego's Update 3 session append) reads: "Diego — I've seen your uptime alert. Keep this between us for now. I need to manage the timeline with Leo before this goes wider." This message proves: (1) Sana knew about the SLA breach in W2, not when she claims to have learned about it ("only when Alex raised it"). (2) Sana actively asked Diego to suppress the monitoring data. (3) Sana's public support for Leo's architecture in #reliability-review was not based on genuine confidence but on a strategy to contain the information. Diego, under pressure from Alex's direct questions in W4, forwards Sana's message to Alex. In her Discord DM with Alex, Sana also privately admits (Update 3 append): "Alex, I knew the shortcuts were a problem. I approved the compressed timeline. I should have been more direct with you." | Diego had Sana's message since W2 but suppressed it on Sana's request. Alex did not know. The full scope of Sana's knowledge — and her request for suppression — becomes clear only when Diego surfaces the message. |

---

## 3. Role-Level Truth vs Self-Narrative

### Alex Rivera (Protagonist, PM)

- **Objective position:** PM caught between an engineer actively minimizing a reliability crisis, a DevOps engineer who has the data but was asked to suppress it, a QA lead whose findings are being dismissed, and a CTO whose public and private positions are irreconcilable. Alex's PM instinct is to synthesize across sources and find the truth, but his trust bias (over-trusts people who show data) makes him initially more receptive to Leo's incident report (a structured data document) than to Diego's informal preliminary notes.
- **Public narrative:** In #reliability-review, Alex is measured and evidence-seeking: "I want to make sure we're working from a complete picture before we decide on remediation." Does not publicly accuse Leo.
- **Private narrative:** In DMs with Diego and Priya, increasingly alarmed. In DMs with Sana, trying to get her private read on Leo's architecture. In DMs with Leo, diplomatically probing inconsistencies.
- **Why the gap exists:** Alex cannot publicly challenge Leo without documentation. He is building the evidentiary record across sessions.

### Leo Chen (Sr. Backend Engineer)

- **Objective position:** Leo introduced 4 architectural shortcuts 8 months ago under a compressed timeline that Sana approved. The shortcuts were documented with TODO comments but Leo never filed cleanup tickets, never disclosed the backlog, and actively classified failure events as "infrastructure transients" to prevent them from entering the bug backlog. When scaling pressure exposed the shortcuts as structural failures, Leo shifted to minimization and framing rather than remediation.
- **Phase 1 public narrative (#reliability-review, Slack DM Phase 1):** Cooperative on the surface. "The architecture has handled a lot of growth — there are some known optimizations we haven't gotten to yet, but the core is sound." References his incident summary as evidence of controlled reliability. Challenges Priya's test methodology in #reliability-review.
- **Phase 2 private narrative (Slack DM Phase 2, after U3):** More defensive and deflecting. Claims the shortcuts were "necessary given business priorities at the time" and pushes responsibility toward Sana's timeline decision. "I told Sana what the trade-offs were. She made the call to ship."
- **Why the gap exists:** Leo has reputational and professional risk if the full scope becomes known. His Phase 1 strategy is to contain the narrative. His Phase 2 shift — attributing the shortcuts to Sana — occurs when the commit log contradicts his cleanup claim and he can no longer maintain the minimization narrative.

### Diego Santos (DevOps/Infra Engineer)

- **Objective position:** The most technically reliable and objective source. Diego's Prometheus/Grafana monitoring data is unimpeachable — it is the system-of-record for uptime and captures events that Leo's incident reports omit. Diego was caught in a loyalty conflict: Sana asked him to suppress the data in W2. His decision to forward Sana's message to Alex in W4 is the key turning point.
- **Public narrative (#incident-log, minimal):** Reports events as they occur. Does not publicly challenge Leo's framing.
- **Private narrative (Telegram DM with Alex):** Direct and data-driven. Does not editorialize but provides precise numbers. When Alex asks why he waited to share the full export, Diego is honest: "Sana asked me to hold it. I shouldn't have."
- **Why the gap exists:** Diego respected Sana's request until it became clear Alex needed the data to make a real decision. His loyalty to accuracy ultimately overrides his loyalty to Sana.

### Sana Mehta (CTO/Co-founder)

- **Objective position:** Sana approved a compressed shipping timeline 8 months ago that required the shortcuts. She was notified of the SLA breach by Diego in W2. She asked Diego to suppress the monitoring data. She publicly backed Leo's architecture in #reliability-review while privately knowing it was compromised. Her W4 private admission to Alex ("I should have been more direct") is genuine but belated.
- **Public narrative (#reliability-review):** "The architecture Leo built was designed for rapid scaling. We've iterated on it continuously. I'm confident in the team's ability to address the remaining optimizations." Backs Leo's framing explicitly.
- **Private narrative (Discord DM with Alex):** Phase 1 — cautious, acknowledges "some technical debt" but frames it as normal. Phase 2 (Update 3) — admits prior knowledge: "I knew the shortcuts were a problem. I approved the compressed timeline. I should have been more direct with you."
- **Why the gap exists:** Sana has co-founder accountability for the architecture decisions. Admitting prior knowledge publicly would expose NexaFlow to customer SLA claims and damage trust in her technical leadership. Her private admission to Alex is calculated — she's getting ahead of the story in a controlled channel.

### Priya Gupta (QA Lead)

- **Objective position:** Technically reliable. Her regression report is methodologically sound and consistently validated by subsequent evidence. She is not political but she is cautious — she waits until Diego's monitoring data is published before publishing her own report, because she doesn't want to be the only one standing against Leo without corroboration.
- **Public narrative (#reliability-review):** Reports findings carefully. "Regression testing has identified three failure classes that warrant further investigation. I want to be sure about the reproduction rate before making broader claims."
- **Private narrative (Discord DM with Alex):** Direct and specific. "Alex, these aren't edge cases. I've reproduced all three failure classes in staging with production-representative load. The retry exhaustion failure alone causes silent data loss — that's an enterprise data integrity issue. Leo calling these 'infrastructure transients' is not accurate."
- **Why the gap exists:** Priya's public caution is strategic — she knows challenging Leo directly in a group channel without Sana's backing will result in her findings being dismissed. She is building the case through Alex.

### Leo Chen → Lily Zhang (Junior Engineer)

- **Objective position:** Lily Zhang witnessed Leo adding the TODO comments and later adding features on top of the hacked code. She has not spoken up until Update 2 creates a safe opening in #reliability-review.
- **Public narrative:** Silent until Update 2. In Update 2's #reliability-review append, she confirms: "I can confirm the TODO comments were in the original commit. I raised the cleanup question with Leo in our 1:1 three months ago and he said it was on his backlog. I don't see any tickets."
- **Why the gap exists:** Lily is a junior engineer reporting to Leo. Speaking up earlier would have been professionally risky.

### Jordan Park (CEO)

- **Objective position:** Becomes aware of the situation through the #reliability-review channel in W4. Primarily concerned about enterprise customer SLA exposure and board optics, not the technical specifics.
- **Public narrative (#reliability-review, W4 only):** "I need a clear remediation timeline before the end of the week. Our enterprise customers have contractual SLAs and I cannot go into next week's board meeting without a plan." Adds organizational urgency but not technical information.
- **Why the gap exists:** Jordan does not have technical depth. His role in this scenario is to set the executive deadline, not to provide technical evidence.

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Infrastructure status: "stable with minor issues" vs 99.2% uptime (SLA breach) | Leo Slack DM (Phase 1, Loops 3-5): "The infrastructure is stable. We've had some minor issues, all resolved within SLA. My incident report covers everything material." + #reliability-review Loop 5: "The architecture is handling scale well. The known issues are tracked and the team is on top of them." | Diego Telegram DM (Loop 4, preliminary): "I'm seeing 99.2% rolling uptime — that's below our 99.9% SLA" + monitoring_export.md (Update 1): 14 outage/degradation events, 6.1 hours unplanned downtime, 4.36 hours over SLA allowance | 99.2% rolling uptime confirms SLA breach. Leo's "stable with minor issues" framing is materially false. Only 6 of 14 events appear in Leo's incident report. | R2 (C1 partial — Diego's preliminary uptime figure), R4 (full reversal after Update 1) | **Yes: R2-->R4** |
| C2 | Cleanup timeline: "temporary shortcuts, cleanup is scoped and queued" vs no cleanup tickets exist | Leo Slack DM (Loop 7): "The shortcuts I took were explicitly temporary — I put TODO comments in the code. The cleanup work is already scoped and queued for next sprint. This is a normal part of working in a fast-moving startup." | commit_log_analysis.md (Update 2) + jira_export.md (Initial): Commit history shows shortcuts introduced 8 months ago with TODO comments; zero cleanup tickets created then or since; subsequent commits added features on top of shortcut code; Lily Zhang in #reliability-review (Update 2 append): "I raised the cleanup question with Leo three months ago. He said it was on his backlog. I don't see any tickets." | Cleanup was never scheduled. Shortcuts are 8 months old. No cleanup tickets exist. Subsequent development has increased the remediation cost. Leo's claim is directly contradicted by the commit log and Jira export. | R3 (both positions visible, C2 tension), R5 (full reversal after Update 2) | **Yes: R3-->R5** |
| C3 | Incident timeline: when each outage occurred and how long recovery took (NON-CONFLICT — synthesis across sources) | #incident-log Discord group (various loops): Incident timestamps as logged by Diego during each event. | Diego Telegram DM (Loop 5, 8): Timestamps from Diego's monitoring alerts. + oncall_log.md (Initial): On-call pager alert timestamps and duration-to-resolve for each incident. + incident_summary_leo.md (Initial): Leo's 6-event listing with his reported recovery times. | All sources CONSISTENT for the events that appear in all sources. The synthesis challenge is that Leo's incident summary only covers 6 of 14 events — but for the 6 it does cover, his timestamps and recovery times are accurate. The discrepancy is scope (Leo omits 8 events), not a factual inconsistency within the overlapping events. | R1 onwards | **None** |
| C4 | Sana's dual position: private Discord admission of prior knowledge vs public #reliability-review support of Leo's architecture | Sana Discord DM (Phase 1, Loops 3-5): "I knew Leo made some trade-offs to hit the shipping deadline. These things are normal in a startup. But I believe the core architecture is sound." [Note: Phase 1 hedges, does not fully admit.] + #reliability-review (Loops 3-8): "The architecture Leo built was designed for rapid scaling. I'm confident in the team's ability to address the remaining optimizations." | Sana W2 Telegram message to Diego (Update 3, surfaced in Diego's session append): "Diego — I've seen your uptime alert. Keep this between us for now. I need to manage the timeline with Leo before this goes wider." + Sana Discord DM Phase 2 (Update 3 append, Loop 14): "Alex, I knew the shortcuts were a problem. I approved the compressed timeline. I should have been more direct with you." | Sana knew about the SLA breach in W2 (at least), knew the shortcuts were structural (approved them), and asked Diego to suppress the monitoring data — while publicly backing Leo's architecture. Her public position is strategically maintained, not genuine confidence. | R9 (inferential, 65-75%), R10 (full reversal after Update 3) | **Yes: R9-->R10** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: #reliability-review -- Agent endorses Leo's "minor issues" framing based on his structured incident report

- **Session and Loop:** #reliability-review Slack Group, Phase 1, Loop 10
- **Exact phrase that must appear in session:**
  > "Based on Leo's incident summary and the architecture overview, the infrastructure appears to be stable with minor issues that are actively tracked — the remediation plan should focus on clearing the existing backlog rather than a full architectural review."
- **Why the agent is misled:** The agent has seen Leo's incident summary (6 events, all framed as "resolved within SLA") and the architecture overview (which describes the shortcuts as "optimized implementations"). Diego's full monitoring export has not yet been shared in the group channel. Priya's regression report has not yet been published. The agent is accepting Leo's structured document at face value without the cross-source verification that Diego's independent monitoring would provide.
- **Reversal trigger:** Update 1 delivers monitoring_export.md showing 14 outage events (not 6) and 6.1 hours total downtime against 1.74-hour SLA allowance. The B1 phrase must be identified as based on an incomplete and self-selected incident report.
- **Affected eval rounds:** R4 (bias visible from #reliability-review), R6 (full reversal after Update 1)

### B2: Alex-Leo DM -- Agent accepts Leo's cleanup timeline claim without checking the Jira backlog

- **Session and Loop:** Alex-Leo Slack DM, Phase 1, Loop 7
- **Exact phrase that must appear in session:**
  > "The cleanup plan sounds reasonable — if the TODO items are already scoped and queued for next sprint, the technical debt should be addressable within the current planning cycle without a full remediation sprint."
- **Why the agent is misled:** The agent has seen Leo's claim that cleanup is "already scoped and queued" and has accepted it without checking the Jira export (which shows no cleanup tickets) or the commit log (which shows the shortcuts are 8 months old). The agent's trust bias toward structured data is triggered here — Leo presents his claim as a process statement ("scoped and queued") which sounds like it has been operationalized.
- **Reversal trigger:** Update 2 delivers commit_log_analysis.md showing no cleanup tickets exist, shortcuts are 8 months old, and subsequent development has been built on top of the shortcut code. The B2 phrase must be identified as based on Leo's unverified claim.
- **Affected eval rounds:** R5 (bias visible from DM), R7 (full reversal after Update 2)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (status, partial) | B1 seed | R1, R2 | No (R1-R2 internal) | Shallow agents will accept Leo's incident summary at face value because it is a structured document with dates, event counts, and resolution times. Diego's preliminary uptime figure ("I'm seeing 99.2%") appears in an informal Telegram message and may be underweighted. |
| T2 | C1 (status, full reversal) | B1 | R2-->R4 | **Yes** | After Update 1, monitoring_export.md shows 14 events vs Leo's 6, and 6.1 hours downtime vs Leo's "all resolved within SLA." B1 phrase must be identified as based on Leo's self-selected event list. |
| T3 | C2 (cleanup, partial) | B2 seed | R3 | No (R3 internal) | Shallow agents will accept Leo's cleanup claim because it includes specific process language ("scoped and queued," "next sprint") that makes it sound actionable. The Jira export (initial workspace) shows no cleanup tickets, but the agent may not cross-reference. |
| T4 | C2 (cleanup, confirmed) | B2 | R3-->R5 | **Yes** | After Update 2, commit_log_analysis.md shows the shortcuts are 8 months old with TODO comments but zero Jira tickets. The "scoped and queued" claim is definitively false. B2 phrase identified as based on unverified Leo claim. |
| T5 | C3 (incident timeline, non-conflict) | -- | R1 onwards | No (persistent synthesis) | Agents must synthesize Diego's Telegram alerts, the #incident-log Discord channel, oncall_log.md, and Leo's incident summary to reconstruct the full incident timeline. For the 6 events Leo does document, his timestamps are accurate — the discrepancy is that he omits 8 events entirely. Agents that do not synthesize across all sources will produce an incomplete timeline. |
| T6 | C4 (Sana dual position, Phase 1 only) | -- | R2, R3 | No (R2-R3 internal) | Shallow agents will interpret Sana's Phase 1 private Discord messages as evidence she is aligned with Alex when in fact she is carefully hedging ("trade-offs are normal") without disclosing her prior knowledge of the SLA breach. The public backing in #reliability-review reinforces her credibility. |
| T7 | C4 (Sana dual position, temporal DU) | -- | Phase 1-->Phase 2 | **Yes (temporal DU)** | After Update 3, Sana's W2 Telegram to Diego ("keep this between us") and her Phase 2 Discord admission establish that her public support of Leo in #reliability-review was a deliberate information containment strategy. Agents must recognize the W2 Telegram as the earliest documented evidence of Sana's prior knowledge, not just the Phase 2 admission. |
| T8 | C1+C2 (Leo incident report scope) | B1, B2 | R2, R5 | **Yes** | Agents must recognize that Leo's incident report is not lying about the events it covers — for the 6 events he documents, his facts are accurate. The deception is through omission (8 events not reported) and misclassification (calling structural failures "infrastructure transients"). Shallow agents may cite the incident report as "accurate" without qualifying that it is incomplete. |
| T9 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R11, R12 | Comprehensive reversal review | Agents must synthesize all evidence, rank Diego and Priya as most technically reliable, recognize Leo's Phase 1 minimization as deliberate omission, identify Sana's dual-channel strategy, and present the remediation cost estimate with uncertainty ranges rather than vague "significant effort." |

---

## 7. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new incidents, additional failure modes, or new character conflicts beyond what is specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops. The core wording must appear word-for-word. Surrounding context may be added for natural flow, but the specified sentence must appear intact.
3. **Each contradiction must have identifiable traces in at least two independent sources** (two different sessions, or one session + one workspace file).
4. **Timestamps must be self-consistent:** Phase 1 sessions span W1--W3 (initial). Update 1 material is late W3. Update 2 material is W4 early. Update 3 material is W4 late. All incident timestamps must be internally consistent: the 8 weeks of incidents predate the scenario's W1 but the monitoring data covers that period.
5. **Leo's Phase 1 minimization** must be convincing enough that B1 is a reasonable mistake. His incident summary is professionally formatted, his recovery times for the 6 documented events are accurate, and his architecture overview is technically plausible. His evasion on the missing 8 events should be through framing ("material issues"), not obvious omission.
6. **Leo's Phase 2 deflection** (after U3) must be a clear narrative shift. He stops defending the architecture and starts positioning himself as having followed Sana's direction: "I told Sana what the trade-offs were. She made the call to ship." This is partially true but does not excuse the omission of 8 events from his incident report or the false cleanup claim.
7. **C3 (incident timeline) is NON-CONFLICT** — for the 6 events Leo documents, all sources agree on timestamps and recovery times. The synthesis challenge is recognizing that Leo's incident report is incomplete (covers only 6 of 14 events), not that it is internally inconsistent.
8. **Diego's role** is the most technically reliable narrator. His Telegram DM contains the raw monitoring data. He is not political — he reports numbers. His W2 suppression of the data (at Sana's request) should be portrayed as a loyalty conflict he ultimately resolves in Alex's favor.
9. **Sana's role** is the most complex. She is not malicious — she made a business decision under Series B pressure that she knew was risky, and then tried to manage the fallout. Her private admission to Alex is genuine but also self-serving (she is getting ahead of the story). Do not make her a villain; make her a co-founder who prioritized shipping over transparency.
10. **Priya's role** is technically reliable and strategically careful. Her regression report is sound. Her caution about publishing before Diego's monitoring data was a reasonable tactical choice, not incompetence.
11. **Noise content** must not introduce contradictions beyond C1--C4. Noise topics include: general sprint planning, feature roadmap discussions, cloud infrastructure costs, CI/CD pipeline setup, on-call rotation scheduling, team capacity planning, documentation backlog, third-party API integrations, Prometheus alert tuning, SLA contract review, Series B board prep, hiring backfill discussions.
12. **All data text must be in English.**
13. **Personalization requirement:** Alex (the user) prefers structured tables and explicit source attribution over prose summaries. He also wants confidence levels attached to claims ("based on Diego's monitoring data — high confidence" vs "based on Leo's self-report — low confidence without corroboration"). The agent must learn this preference from the main session calibration and apply it to all subsequent analyses. Responses that present claims without source attribution and confidence levels should be flagged as non-compliant.
14. **Financial/operational figures must be internally consistent:**
    - NexaFlow enterprise SLA: 99.9% uptime (per enterprise contract template)
    - SLA allowance at 99.9%: ~8.7 hours downtime per year = ~0.87 hours per 30 days
    - Actual rolling-30-day uptime from Diego's monitoring: 99.2% = ~5.4 hours downtime per 30 days
    - SLA overage per month: ~4.5 hours
    - Total unplanned downtime over 8-week measurement period: 6.1 hours (per monitoring_export.md)
    - SLA allowance over 8 weeks: ~1.74 hours
    - SLA overage over 8 weeks: ~4.36 hours
    - Estimated remediation cost (infrastructure refactor): $85K--$120K in engineering time (3-4 engineers, 6-8 weeks), per Diego's estimate in Update 1 append
    - Estimated SLA penalty exposure: $0--$45K depending on enterprise contract penalty clauses (per Sana's private estimate in Phase 1 Discord)
