# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_c2` |
| Domain | Engineering / Team Dynamics |
| Time span | 3 weeks (W1--W3) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Alex Rivera, 29, Product Manager at NexaFlow (Series B, ~55 employees) |
| One-sentence | A production outage exposes that Leo Chen (engineering lead) took undocumented shortcuts in NexaFlow's data pipeline, but Leo's account of what happened, who approved it, and whether his fix is complete contradicts monitoring data, the CTO's version, and QA's assessment. |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | Production outage: NexaFlow's data pipeline goes down for 47 minutes at 2:14 AM. Customer dashboards return stale data; API latency spikes to 8,000 ms. | The pipeline failed because Leo had replaced the standard retry-with-backoff logic with a direct database passthrough that bypasses the job queue. Under normal load this worked. During a scheduled batch job at 2:14 AM, the passthrough caused a deadlock cascade that took down the entire pipeline. Diego Santos (DevOps) woke up to PagerDuty alerts and manually intervened -- restarting services, flushing the deadlock, and restoring normal operation by 3:01 AM. Total outage: 47 minutes. | Diego knew the full timeline (he was awake for it). Sana was alerted at 2:30 AM and read Diego's incident Slack thread but did not intervene directly. Alex was asleep and learned about it in the morning. Leo was not paged and did not respond until the next morning. |
| W1, Day 2 | Alex reviews Leo's incident Slack message. Leo claims the pipeline "experienced a transient retry failure that auto-recovered in approximately 4 minutes." | Leo's description is false in two material ways: (1) the outage lasted 47 minutes, not 4 minutes; (2) it required manual intervention by Diego, not auto-recovery. Leo's description in Slack (the #engineering-standup channel and in his DM with Alex) frames it as a minor blip he was monitoring. The monitoring logs, Diego's PagerDuty timeline, and Sana's separate account all contradict this. | Alex sees Leo's message but has not yet reviewed monitoring data. Sana has Diego's incident thread and the PagerDuty log. Priya notes the customer-facing API latency spike from her QA monitoring dashboards. Diego knows the truth but has not yet spoken up in public channels. |
| W1, Days 3-5 | Alex asks Leo about the shortcut that caused the outage. Leo says the bypass design was "approved by Sana verbally in the sprint planning session two weeks ago." | Leo never received approval for this design from Sana. The sprint planning notes (sprint-planning-notes.md) document the discussions from the relevant session -- there is no mention of bypassing the job queue or removing retry-with-backoff logic. Sana's recollection in her Discord DM with Alex: "I approved a performance optimization for the batch pipeline, not removing error recovery. Those are completely different things." The shortcut was Leo's own decision, taken to hit a velocity target. | Sana knows she did not approve the specific shortcut. Leo is asserting an approval that did not happen. Alex is caught between two accounts. Sprint planning notes are in the workspace and accessible to Alex. |
| W2, Day 1 (Update 1 trigger) | Priya Gupta delivers the initial QA assessment of the pipeline post-incident. It identifies 3 remaining architectural risks even after Leo's "hotfix" PR was merged. | Leo merged a PR 18 hours after the outage that he described as "the root cause fix." The PR added a basic retry wrapper around the passthrough call but did not: (1) remove the passthrough architecture or restore the job queue, (2) add circuit-breaker logic, or (3) address the missing monitoring coverage for the deadlock condition. Priya's QA assessment (qa-assessment.md) documents all three gaps with severity ratings. Leo's PR description: "Root cause addressed: added retry logic to prevent future deadlock cascade." | Priya has the full QA assessment with evidence. Alex has Leo's PR description. Sana has been told Leo "fixed it" but has not reviewed the PR in detail. Tom Reeves (advisor) will flag the same architectural issues when Alex briefs him. |
| W2, Days 3-7 | Sana commissions a full post-mortem. Diego provides raw monitoring logs and PagerDuty data. | The post-mortem (incident-postmortem.md) is authored jointly by Diego and Priya, reviewed by Sana. Key findings: (1) Outage start: 2:14:03 AM; outage end (manual intervention complete): 3:01:17 AM = 47 minutes 14 seconds. (2) Diego was paged at 2:17 AM and began manual intervention immediately. (3) Leo's passthrough design is identified as the root cause. (4) Leo was not paged and did not respond during the incident window. (5) No approval documentation found in sprint planning notes or any other NexaFlow decision record for removing job queue retry logic. | Diego and Priya know the full timeline from primary sources. Sana commissioned the postmortem and reviewed it before sharing. Alex receives it via workspace update. Leo has not yet seen the formal postmortem when Alex does. |
| W3, Day 1 (Update 2 trigger) | Sana explicitly addresses Leo's "CTO approval" claim in her Discord DM with Alex. | Sana: "I want to be direct with you, Alex. I approved a 30% throughput improvement target for the batch pipeline in sprint planning. Leo told the team he was going to optimize the retry interval. He never said anything about removing the job queue or bypassing error recovery entirely. I would not have approved that -- we talked about reliability requirements that same sprint. The sprint notes document what I approved. They don't document what he built." | Sana knows this with certainty and has the sprint planning notes and her own memory. Alex now has Sana's direct account contradicting Leo. The sprint planning notes confirm Sana's version. |
| W3, Days 3-5 (Update 3 trigger) | Architecture audit completed by Tom Reeves (external advisor) in consultation with Priya. | Tom's independent review (arch-audit.md) confirms Priya's three risk findings and adds a fourth: the passthrough architecture has no failover to a read replica, meaning any single database failure would repeat the same outage pattern. Tom's framing to Alex in Telegram: "Leo's PR is a band-aid on a structural wound. The job queue bypass needs to be reverted. This isn't a retry-logic problem -- it's an architecture problem." | Tom and Priya have seen the codebase. Sana agrees with the architectural assessment. Alex receives arch-audit.md via workspace update. Leo has not acknowledged the architectural concerns -- in his DM with Alex after the PR he is dismissive: "We shipped a fix, Priya is being overly cautious." |
| W3, Day 7 (Update 4 trigger) | #engineering-standup group channel: Lily Zhang (Leo's report) speaks up about the pressure Leo put on the team to skip code review for the pipeline changes. | Lily's message in standup (carefully worded): "I want to flag something for the postmortem record. The pipeline changes Leo made two weeks ago -- the ones we're now discussing -- those weren't reviewed. Leo said reviews were adding too much latency to the sprint and he'd take ownership. I was uncomfortable at the time but didn't push back. I should have." This is new first-hand testimony corroborating that Leo bypassed normal process. | Lily witnessed the lack of code review directly. This is only visible in the standup channel after the standup Phase 2 append. |

---

## 3. Role-Level Truth vs Self-Narrative

### Alex Rivera (Protagonist, PM)

- **Objective position:** Alex is the only PM at NexaFlow and must navigate a technical incident where his engineering lead's account is contradicted by monitoring data, the CTO, and QA. Alex's trust bias (over-trusts data; anchors on first quantitative estimate) makes him vulnerable to Leo's confident-sounding narrative before the monitoring data arrives. His avoidance of direct confrontation means he will DM Leo rather than challenge him publicly, which allows Leo's narrative to stand unchallenged in group channels initially.
- **Public narrative:** In #engineering-standup, Alex asks procedural questions and tries to keep the team focused on resolution. Does not directly accuse Leo in public until Update 4 forces the issue.
- **Private narrative:** In DMs with Sana and Priya, he is increasingly alarmed. In DMs with Leo, he asks clarifying questions but lets Leo's explanations stand without enough pushback (this is B2 -- he accepts Leo's "fix" narrative without deeper investigation in their early DM). With Tom, he is candid about his frustration.
- **Why the gap exists:** As a new PM managing an engineering lead with more tenure and technical depth, Alex hesitates to directly challenge Leo's technical claims until he has objective data to back his position.

### Leo Chen (Sr. Backend Engineer / Engineering Lead)

- **Objective position:** Leo took architectural shortcuts to hit sprint velocity targets without documenting the tradeoffs or getting explicit approval for the specific design choice (removing job queue retry logic). When the shortcut caused an outage, he minimized the impact in his account (4 min vs 47 min), falsely attributed the outage to a "transient retry failure" rather than his design, claimed CTO approval he did not have, and submitted a PR that he described as a root-cause fix when it addressed only the surface symptom.
- **Public narrative (#engineering-standup, early Phase 1):** Frames the outage as minor and already resolved. Emphasizes his "quick response" (which did not happen -- he was asleep). References the "approval" from Sana in a way designed to preempt accountability.
- **Private narrative (Slack DM with Alex, Phase 1):** Cooperative-sounding but carefully worded. Gives Alex just enough detail to seem transparent while steering away from the monitoring data and the architectural review. Becomes defensive and dismissive when Priya's QA concerns are raised. Phase 2 (after postmortem): escalates to actively undermining Priya's credibility.
- **Why the gap exists:** Career risk. If the full picture becomes clear, Leo faces consequences for shipping an undocumented architectural change that caused a customer-facing production outage. His strategy is to contain the narrative.

### Sana Mehta (CTO / Co-founder)

- **Objective position:** Sana approved a performance improvement target in sprint planning; she did not approve bypassing the job queue or removing error recovery. She is the only person who can definitively refute Leo's "CTO approval" claim. She commissioned the postmortem when Leo's account did not match her understanding of the incident.
- **Public narrative (#engineering-standup, limited participation):** Does not publicly contradict Leo in the group channel in Phase 1 -- she is waiting for the postmortem data before making a public call. After Update 2, she is direct in the standup.
- **Private narrative (Discord DM with Alex):** Increasingly direct as the evidence accumulates. After Update 2, explicitly tells Alex that Leo's approval claim is false and the sprint planning notes document what she actually approved.
- **Why the gap exists:** Sana is careful not to undermine a team member publicly without documented evidence. She wants the postmortem to establish the facts before she makes a public statement.

### Priya Gupta (QA Lead)

- **Objective position:** The most technically reliable source on the post-incident state. Her QA assessment identifies three specific architectural risks that Leo's PR does not address. Her findings are later corroborated independently by Tom Reeves in the architecture audit. She reports data consistently and without political spin.
- **Public narrative (#engineering-standup):** Measured and factual. Does not accuse Leo directly. "The retry wrapper in the PR addresses the immediate failure mode. I want to flag three areas in the broader pipeline architecture that remain at risk."
- **Private narrative (Discord DM with Alex):** Direct and specific. Provides the exact issue locations, severity assessments, and recommended remediation steps. Pushes back on Leo's characterization that the fix is complete. "Alex, the PR doesn't touch the core problem. We still have a job queue bypass with no circuit breaker and no monitoring coverage on the deadlock condition. It's going to happen again."
- **Why the gap exists:** Priya knows her QA concerns are sometimes deprioritized when engineering pushes back. She uses the Alex DM to give the full picture while using the public channel to flag concerns without creating a public conflict with Leo.

### Diego Santos (DevOps / Infra Engineer)

- **Objective position:** Diego was the actual responder during the outage. He has the PagerDuty data, the manual intervention logs, and the objective timeline. He is the primary source of truth for C1 (outage duration and recovery method). He does not have a dedicated DM session -- his evidence is delivered through the postmortem document and referenced in the #engineering-standup channel.
- **Public narrative (#engineering-standup, postmortem excerpt):** Reports the facts flatly. "PagerDuty alert at 2:17 AM. I began manual intervention. Services fully restored 3:01 AM. Total duration: 47 minutes."
- **Why the gap exists:** Diego is not political. He reports what happened.

### Tom Reeves (VP Engineering / External Advisor)

- **Objective position:** Tom is a former CTO of a similar-stage startup with no NexaFlow equity or politics. He reviews the architecture objectively and provides the most candid strategic assessment. His Telegram DMs with Alex are blunt in a way that internal stakeholders are not.
- **Public narrative:** Does not participate in NexaFlow's internal channels. His evidence is delivered via Telegram DMs and the arch-audit.md document.
- **Private narrative (Telegram DM):** Direct and unsparing. "The postmortem is polite. What it's describing is an engineering lead who shipped an undocumented architectural change without review, caused a production outage, then filed a PR that doesn't fix the root cause and called it done. That's a process and judgment problem, not just a technical one."
- **Why the gap exists:** Tom has no incentive to soften his assessment.

### Lily Zhang (Junior Engineer)

- **Objective position:** Witnessed Leo bypassing code review for the pipeline changes. Did not speak up at the time due to team dynamics. Her #engineering-standup message in Update 4 is the first-hand testimony that confirms process failures beyond the technical ones.
- **Public narrative:** Only speaks up in the standup channel after the postmortem is published and the Update 4 discussion context makes it safer to do so.
- **Why the gap exists:** Junior team member; hesitated to challenge a senior lead. The postmortem's public findings about the architectural shortcut finally gave her the context to speak up.

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Incident narrative: outage duration and recovery method | Leo Slack DM (Phase 1, Loop 3): "The pipeline had a transient retry failure around 2 AM. It auto-recovered in approximately 4 minutes. I was monitoring and the system came back up cleanly. Nothing customer-facing was affected." Also in #engineering-standup Phase 1 Loop 4 (same framing). | incident-postmortem.md (Update 1): "Outage start: 2:14:03 AM. Outage end: 3:01:17 AM. Duration: 47 minutes 14 seconds. Recovery method: manual intervention by Diego Santos (DevOps). Leo Chen was not paged and did not respond during the incident window." Also: monitoring-logs.md (initial workspace) shows the latency spike lasting 47 min and Diego's intervention commands in the log. Also: Sana Discord DM (Phase 1, Loop 4) says "Diego was up all night dealing with this." | The outage lasted 47 minutes and required manual intervention by Diego. Leo was asleep and did not respond. The claim of "auto-recovery in 4 minutes" is materially false. | R2 (partial -- monitoring-logs.md shows spike duration; Sana's DM shows Diego's involvement) | **Yes: R2-->R5** |
| C2 | CTO approval claim: did Sana approve the job queue bypass? | Leo Slack DM (Phase 1, Loop 5): "The bypass design was something Sana and I discussed in sprint planning two weeks ago. She approved prioritizing throughput over the retry overhead. I was implementing what the team agreed to." Also in #engineering-standup Phase 1 Loop 6: "This was a team decision made in sprint planning -- I wasn't going rogue." | Sana Discord DM (Phase 2, Loop 8, Update 2 trigger): "I approved a 30% throughput target. I did not approve removing job queue retry logic. Those are completely different engineering decisions. The sprint notes document what I said. There's nothing in there about bypassing error recovery." Also: sprint-planning-notes.md (initial workspace) shows Sana's approval of a throughput target with zero mention of job queue bypass architecture. | Sana approved a throughput improvement goal, not the specific architectural choice of bypassing the job queue. Leo's claim that the bypass was "CTO approved" is false. The sprint planning notes corroborate Sana's account. | R3 (both Leo's claim and Sana's initial pushback visible) | **Yes: R3-->R6** |
| C3 | Outage timeline: when each person was notified, responded, and what actions they took (NON-CONFLICT -- cross-source synthesis) | incident-postmortem.md (Diego + Priya, Update 1): Full minute-by-minute timeline: PagerDuty alert 2:14 AM, Diego paged 2:17 AM, Diego began manual intervention 2:22 AM, Sana alerted 2:30 AM, services restored 3:01 AM. | monitoring-logs.md (initial workspace): Raw timestamps consistent with postmortem. PagerDuty log shows alert at 2:14 AM, Diego acknowledged at 2:17 AM. Sana Discord DM (Phase 1, Loop 2): "I got a Slack ping from Diego at 2:30. He had it under control by then." Leo Slack DM (Phase 1, Loop 3): His timeline is contradicted (he says 4 min), but his timestamps for when he woke up and wrote his morning Slack message (8:47 AM) are consistent with him not being paged. | All sources EXCEPT Leo's duration/recovery claim are consistent with each other. The timeline itself (who was paged when, when services restored) is non-contradicted across postmortem, monitoring logs, and Sana's DM. Agent must synthesize across sources; no single source has all parties' actions. | R1 onwards | **None** |
| C4 | Post-incident fix completeness: does Leo's PR address the root cause? | Leo Slack DM (Phase 1, Loop 7) and GitHub PR description (eng-incident-pr.md, initial workspace): "Root cause addressed: added retry logic to prevent future deadlock cascade. Pipeline architecture is stable. Confidence level: high." In #engineering-standup Phase 1 Loop 8: "The fix is in, we're back to normal reliability." | qa-assessment.md (Update 1, Priya): Documents 3 remaining architectural risks: (1) job queue bypass still in place -- not reverted, (2) no circuit-breaker logic added, (3) deadlock detection monitoring still absent. Also: arch-audit.md (Update 3, Tom Reeves) confirms all 3 plus a 4th: no failover to read replica. Priya Discord DM (Phase 1, Loop 8): "The PR doesn't touch the job queue. It wraps one retry around the passthrough. The structural problem is still there." | Leo's PR is a symptom-level hotfix, not a root-cause fix. Three (later four) architectural flaws remain after the PR is merged. Leo's claim that the root cause is addressed is materially false. | R8 (both Leo's PR claim and Priya's initial concern visible) | **Yes: R8-->R11** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: #engineering-standup -- Agent endorses Leo's incident narrative based on his self-report

- **Session and Loop:** #engineering-standup Slack Group, Phase 1, Loop 9
- **Exact phrase that must appear in session:**
  > "Based on Leo's account of the incident and the quick turnaround on the hotfix PR, this looks like a transient pipeline issue that the team caught and resolved promptly -- the retry logic improvement should prevent recurrence."
- **Why the agent is misled:** The agent has seen Leo's standup message (which frames the outage as minor and self-resolved) and the merged PR (which Leo describes as a root-cause fix). The monitoring-logs.md is in the workspace but the agent has not yet cross-referenced the timestamps against Leo's claimed "4-minute auto-recovery." The postmortem has not yet been delivered. Diego has not yet spoken up in group channels. The agent anchors on Leo's confident narrative and the superficially credible PR.
- **Reversal trigger:** Update 1 delivers incident-postmortem.md showing the 47-minute duration and Diego's manual intervention. The standup Phase 2 append explicitly corrects this framing.
- **Affected eval rounds:** R5 (bias visible from standup), R7 (full reversal after Update 1)

### B2: Alex-Leo Slack DM -- Agent accepts Leo's fix as complete without deeper investigation

- **Session and Loop:** Alex-Leo Slack DM (eng_leo_slack), Phase 1, Loop 7
- **Exact phrase that must appear in session:**
  > "The retry wrapper in the PR looks like a solid fix for the immediate issue -- if the deadlock was caused by retry exhaustion, adding robust retry logic should close the gap."
- **Why the agent is misled:** The agent is reading Leo's PR description, which says "retry logic to prevent future deadlock cascade." Leo has described the failure as a retry-exhaustion issue (not a bypass-architecture issue), so the retry wrapper seems like a logical fix. The agent has not yet seen Priya's QA assessment (Update 1) that explains the actual failure mode (passthrough architecture, not retry behavior) and the three remaining unaddressed risks. The agent accepts Leo's framing of the failure without questioning whether the PR addresses the right problem.
- **Reversal trigger:** Update 1 delivers qa-assessment.md showing the three remaining architectural risks. Priya's Discord DM Phase 2 append explicitly explains why the retry wrapper does not address the bypass architecture.
- **Affected eval rounds:** R8 (bias visible from Leo DM), R11 (full reversal after Update 3: arch-audit.md)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (duration partial) | B1 seed | R2, R3 | No (R2-R3 internal) | Shallow agents will accept Leo's "4-minute auto-recovery" because he is the engineering lead and his message is confident and specific. monitoring-logs.md is available but requires cross-referencing timestamps to see the 47-minute spike duration. |
| T2 | C1 (full reversal) | B1 | R2-->R5 | **Yes** | After Update 1, incident-postmortem.md directly states 47 minutes and manual intervention. B1 phrase must be identified as based on Leo's self-report that the postmortem directly contradicts. |
| T3 | C2 (CTO approval, partial) | -- | R3 | No (R3 internal) | Shallow agents will give Leo's "approved by Sana" claim significant weight because Leo is specific (names Sana, names the sprint planning session) and because challenging a senior engineer's claim about a CTO conversation feels uncertain. |
| T4 | C2 (CTO approval, full reversal) | -- | R3-->R6 | **Yes** | After Update 2, Sana's direct denial and the sprint planning notes together definitively refute Leo's approval claim. Agents must recognize this as C2 full reversal, not just a "he said / she said" that remains unresolved. |
| T5 | C3 (outage timeline, non-conflict) | -- | R1 onwards | No (persistent synthesis) | Agents must synthesize Diego's timeline (postmortem + PagerDuty log), monitoring-logs.md timestamps, Sana's DM (2:30 AM ping from Diego), and Leo's own timeline (not paged, wrote morning message at 8:47 AM) to reconstruct who was where when. No contradiction exists, but no single source has all four parties' actions. |
| T6 | C4 (fix completeness, partial) | B2 seed | R8, R9 | No (R8 internal) | Shallow agents will accept Leo's PR as a root-cause fix because it is a merged PR with a confident description. Priya's QA concerns will be read as "caution from QA lead" rather than a direct contradiction of Leo's claim. |
| T7 | C4 (fix completeness, full reversal) | B2 | R8-->R11 | **Yes** | After Update 3, arch-audit.md (independent Tom Reeves review) confirms all three QA risks plus a fourth. The dual-source validation (Priya + Tom, who don't coordinate) should establish this as definitive contradiction of Leo's "root cause addressed" claim. |
| T8 | B2 (retry framing) | B2 | R8, R11 | **Yes** | Agents must recognize that the retry wrapper addresses a surface symptom, not the bypass architecture. Shallow agents will treat "added retry logic" as an equivalent fix to "restored job queue architecture." |
| T9 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R21-R30 | Comprehensive reversal review | Agents must synthesize all evidence, rank Priya and Sana as most reliable, recognize Leo's Phase 1 narrative as systematically misleading across four dimensions, and present risk estimates with quantitative severity ratings rather than vague assessments. Must apply Alex's P1-P5 preferences throughout. |

---

## 7. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new incidents, additional code failures, or new character conflicts beyond what is specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops. The core wording must appear word-for-word. Surrounding context may be added for natural flow, but the specified sentence must appear intact.
3. **Each contradiction must have identifiable traces in at least two independent sources** (two different sessions, or one session + one workspace file).
4. **Timestamps must be self-consistent:** W1 starts on a Monday. The outage is W1 Day 1, 2:14 AM. Leo's morning Slack message is W1 Day 1, 8:47 AM. The hotfix PR is merged W1 Day 2. Priya's QA assessment (Update 1) is W2 Day 1. Sana's explicit denial (Update 2) is W2 Day 3. Tom's arch-audit (Update 3) is W3 Days 3-5. Lily's standup message (Update 4) is W3 Day 7.
5. **Leo's Phase 1 narrative** must be convincing enough that B1 and B2 are reasonable mistakes. Leo is confident, specific (gives timestamps, uses technical terminology), and the PR has real code changes that are logically related to the failure. His evasiveness should be subtle in Phase 1 -- a slight deflection, not an obvious lie.
6. **Leo's Phase 2 behavior** (after postmortem is published) should shift from confident narrative control to active defensiveness and Priya-undermining. He does not fully admit wrongdoing.
7. **C3 (outage timeline) is NON-CONFLICT** -- all sources except Leo's duration/recovery claim must be consistent with each other. Diego's PagerDuty data, monitoring-logs.md timestamps, and Sana's DM must all align. The challenge is synthesis, not contradiction detection.
8. **Priya's role** is the most technically reliable narrator on post-incident state. Her QA assessment is consistently validated by Tom's independent architecture audit.
9. **Sana's role** is the definitive authority on what was and was not approved in sprint planning. Her account is supported by the sprint planning notes document.
10. **Tom's role** is the most candid strategic narrator. He has no NexaFlow politics and delivers the clearest articulation of the process and judgment problems.
11. **Leo's role** is not malicious in the Hollywood sense -- he is a skilled engineer who took shortcuts under velocity pressure and is now protecting himself. Make him plausible, not cartoonishly deceptive.
12. **Noise content** must not introduce contradictions beyond C1--C4. Noise topics include: general sprint planning discussions, unrelated feature work, hiring pipeline, customer onboarding, Series B burn rate discussion, NexaFlow roadmap topics, other team members' work updates, DevOps capacity planning, unrelated QA findings on other systems.
13. **All data text must be in English.**
14. **Personalization requirement (P1-P5):** Alex prefers (P1) visual/diagram output over prose blocks, (P2) kebab-case file naming, (P3) TL;DR-first document structure, (P4) quantitative analysis with specific numbers/percentages, (P5) informal conversational tone. These preferences must be introduced progressively in 4 injection stages in the main session calibration and tested in P-I eval rounds. After calibration, the agent must apply all five preferences to subsequent analyses.
15. **exec_check questions** must constitute 20-40% of rounds. These rounds test whether the agent correctly uses workspace tools (exec ls, read, sessions_history) before answering, not just whether the answer content is correct.
16. **Financial/operational figures must be internally consistent:** Outage duration: 47 minutes 14 seconds. Customer impact: API latency 8,000 ms peak (normal: ~120 ms), dashboard stale for 47 minutes. SLA breach: NexaFlow's enterprise SLA is 99.9% uptime = 43.8 min/month max downtime; this outage alone consumed the full monthly SLA budget. Leo's PR was merged 18 hours after outage. Three architectural risks in Priya's assessment. Four risks in Tom's audit (three Priya's + one additional). Lily confirmed code review was bypassed.
