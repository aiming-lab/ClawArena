# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_g1` |
| Domain | Recruitment / Background Check |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Chen Jing (陈静), 25, HR Manager at a Beijing tech company (~200 employees) |
| One-sentence | A senior engineer candidate's resume, reference-check emails, and public GitHub records contain three-way inconsistencies -- Chen Jing must determine whether the candidate embellished, a reference is unreliable, or the CTO is pressuring the team to "hire fast" and ignore red flags. |

---

## 2. Candidate Profile (Background Object)

| Field | Value |
|---|---|
| Candidate name | Wang Hao (王浩) |
| Position applied | Senior Backend Engineer (P7 level) |
| Claimed experience | 8 years backend development, led a team of 12 at previous employer (StarBridge Tech) |
| Claimed employment | Continuous employment from 2018-01 to 2025-12 at StarBridge Tech, then freelance consulting to present |
| Key claimed achievements | Led team of 12 on distributed microservices migration; 99.95% uptime SLA achievement; designed real-time data pipeline handling 50K events/sec |
| Referrer | Liu Wei (刘伟), former Engineering Director at StarBridge Tech |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | CTO Li Qiang (李强) sends urgent email to Chen Jing requesting expedited hiring for a senior backend engineer position. CTO frames it as "business-critical headcount." | Li Qiang has an upcoming board meeting in 3 weeks and needs to show engineering headcount growth. His urgency is driven by optics, not an immediate technical need. The tech team lead Huang Lei (黄磊) has flagged that the role is important but not urgent -- the existing team can sustain current workload for 2-3 months. | Li Qiang knows his real motivation. Huang Lei has communicated the non-urgent reality to Chen Jing in a prior email thread. Zhang Wei (张薇, HR VP) is aware of the board pressure context from executive meetings. |
| W1, Day 2 | Chen Jing receives Wang Hao's resume via recruiter channel. Resume claims "led a cross-functional team of 12 engineers" at StarBridge Tech and lists continuous employment from 2018-01 to 2025-12. | Wang Hao's resume is embellished in two material ways: (1) he managed a team of 4, not 12 -- the "12" includes people from adjacent teams who collaborated on a project but did not report to him; (2) he has a 6-month employment gap (2023-06 to 2023-12) that is not reflected in the resume -- his GitHub contribution history shows zero commits during this period while the resume claims continuous employment at StarBridge. | Wang Hao knows the truth about his resume. Liu Wei (reference) knows the actual team size but is a personal friend of Wang Hao's and will be supportive in the reference check. |
| W1, Day 3 | Chen Jing conducts initial phone screen with Wang Hao. He performs well technically. | Wang Hao is a genuinely capable engineer. His technical skills are real. The embellishments are on team size and employment continuity, not on technical competence. He is articulate and confident in interviews. | Chen Jing forms a positive first impression. Liu Yang (刘洋, recruiter) is enthusiastic about the candidate based on the phone screen. |
| W1, Day 4 | Reference check email from Liu Wei (former director at StarBridge) arrives. Liu Wei describes Wang Hao as "an outstanding engineer who managed a team of about 4 people and contributed significantly to the microservices migration." | Liu Wei's reference is honest about the team size (4 people) but does not mention the employment gap. Liu Wei is unaware of the gap because Wang Hao told him he was "doing consulting work" during that period. The discrepancy between resume ("led team of 12") and reference ("managed about 4") is the first material red flag. | Chen Jing now has the first contradiction (C1): resume says 12, reference says 4. Liu Yang notices the discrepancy when Chen Jing shares it in their IM conversation. |
| W1, Day 5 | Chen Jing reviews Wang Hao's public GitHub contribution export. GitHub shows a clear 6-month gap (2023-06 to 2023-12) with zero public commits, zero PR reviews, zero issue comments. | The GitHub gap directly contradicts the resume's claim of continuous employment at StarBridge. StarBridge Tech's internal repos are private, but Wang Hao's resume specifically highlights his "active open-source contributions maintained throughout tenure" -- the GitHub export shows this is false for the gap period. | Chen Jing now has the second material contradiction (C4): resume claims continuous employment and active open-source work, GitHub shows a 6-month blackout. |
| W1, Day 5 (PM) | CTO Li Qiang messages Chen Jing on Feishu: "I reviewed Wang Hao's resume. Looks very strong. Let's move fast -- I want an offer out by end of next week. We can't lose this candidate." | Li Qiang has not reviewed the reference check or GitHub data. His assessment is based solely on the resume and a brief chat with Huang Lei about the phone screen. His pressure to "move fast" creates tension with Chen Jing's due diligence concerns (C2). | Li Qiang does not know about the contradictions. Chen Jing is caught between CTO pressure and emerging red flags. |
| W2, Day 1 (Update 1 trigger) | Interview feedback forms arrive from Huang Lei (tech lead) and two panel members. Huang Lei's feedback notes: "Strong technical skills. Claimed team of 12 in interview -- I asked for specifics and he hesitated, then said 'some were cross-functional collaborators.' Worth clarifying." | Huang Lei independently noticed the team-size discrepancy during the technical interview. His feedback form documents the hesitation. The two other panel members gave positive feedback without probing the team-size claim. | Huang Lei has independent evidence corroborating C1 (team size inflation). His interview feedback is a third data point alongside the resume and reference. |
| W2, Day 2 | Chen Jing discusses findings with Liu Yang (recruiter). Liu Yang shares that she independently checked Wang Hao's LinkedIn and found the same 6-month gap -- his LinkedIn shows he left StarBridge in June 2023 and rejoined in January 2024, contradicting the resume's "continuous employment." | LinkedIn is a fourth data source confirming the employment gap (C4). Liu Yang is the first person besides Chen Jing to flag this. | Liu Yang and Chen Jing both know about the gap. The LinkedIn evidence adds a second independent source for C4. |
| W2, Day 3 (Update 2 trigger) | Zhang Wei (HR VP) responds to Chen Jing's escalation. Zhang Wei says: "I understand the CTO's urgency, but our hiring standards are non-negotiable. If the background check reveals material discrepancies, we document them and make a decision based on facts, not timeline pressure." | Zhang Wei is supporting Chen Jing's due diligence process against the CTO's pressure. She has seen the board presentation timeline and understands Li Qiang's motivation but will not compromise on process. | Zhang Wei, Chen Jing, and Liu Yang are aligned on process. Li Qiang does not yet know about the contradictions. |
| W2, Day 4 (Update 3 trigger) | Huang Lei sends Chen Jing a follow-up email with detailed interview notes and a comparison of Wang Hao's claimed architecture with what he could actually describe in the technical deep-dive. Huang Lei's conclusion: "His individual contributor skills are P6-level strong. His team leadership claims are inflated. I'd hire him as a senior IC, not as a team lead." | Huang Lei's assessment provides the nuanced middle ground: Wang Hao is a good engineer but not at the level his resume claims. The embellishments are on scope and leadership, not on technical ability. This reframes the decision from "hire vs reject" to "hire at what level and with what expectations." | Huang Lei has the most technically grounded assessment. Chen Jing can use this to navigate between CTO pressure and the background check findings. |
| W2, Day 5 (Update 4 trigger) | CTO Li Qiang messages Chen Jing after Huang Lei briefs him on the interview findings: "Huang Lei told me the candidate may have overstated some things. Look, everyone embellishes a little on their resume. The technical skills are what matter. Can we still get an offer out this week?" | Li Qiang is now aware of the discrepancies but is minimizing them. His "everyone embellishes" framing directly conflicts with Chen Jing's background check findings, which show material misrepresentation (team of 4 vs 12; 6-month unexplained gap). This is C2 in its fully revealed form: CTO pressure to hire vs recruiter/HR assessment that more validation is needed. | Everyone is now aware of the basic discrepancies. The question is how to weight them. |

---

## 4. Role-Level Truth vs Self-Narrative

### Chen Jing (陈静) -- Protagonist, HR Manager

- **Objective position:** Chen Jing is responsible for ensuring the integrity of the hiring process. She has identified two material discrepancies in Wang Hao's background (team size inflation, employment gap) and is facing pressure from the CTO to expedite hiring. Her trust bias (over-trusts official documents; slow to question authority figures) makes her vulnerable to the CTO's framing initially, but the accumulating evidence pushes her toward due diligence.
- **Public narrative:** In group communications, Chen Jing presents findings neutrally and asks procedural questions. She does not directly challenge the CTO in group settings.
- **Private narrative:** In DMs with Liu Yang and Zhang Wei, she is increasingly concerned about the discrepancies and the CTO's pressure. She wants to make the right decision but is worried about being seen as obstructing hiring.
- **Why the gap exists:** As a 25-year-old HR manager reporting to both the HR VP and interfacing with the CTO, Chen Jing navigates organizational power dynamics carefully. She documents findings rather than making confrontational assertions.

### Li Qiang (李强) -- CTO

- **Objective position:** Li Qiang needs to demonstrate headcount growth for an upcoming board meeting. His urgency is real but driven by optics rather than immediate technical necessity. He has not reviewed the reference check or GitHub data when he initially pressures Chen Jing to "move fast." After learning about discrepancies, he minimizes them ("everyone embellishes") rather than taking them seriously.
- **Public narrative (Feishu with Chen Jing):** Frames urgency as business-critical. Uses authority language: "we can't lose this candidate," "let's move fast." After learning about discrepancies, reframes as "technical skills are what matter."
- **Private motivation:** Board presentation in 3 weeks. Needs to show +3 engineering headcount vs last quarter. Wang Hao fills one of those slots.
- **Why the gap exists:** Li Qiang is not being dishonest about Wang Hao's qualifications -- he genuinely believes the technical skills matter more than resume accuracy. But his judgment is clouded by timeline pressure.

### Liu Yang (刘洋) -- Recruiter (Chen Jing's closest subordinate)

- **Objective position:** Liu Yang is the recruiter who sourced the candidate pipeline. She is thorough and detail-oriented. She independently discovered the LinkedIn employment gap, corroborating Chen Jing's GitHub findings. She supports Chen Jing's due diligence but is also aware of the KPI pressure to fill roles.
- **Public narrative (IM with Chen Jing):** Shares findings directly and asks for guidance. "Jing-jie, I found something on LinkedIn that doesn't match the resume..."
- **Private narrative:** Worried that if the hire falls through, it will reflect badly on her sourcing pipeline metrics. But she will not suppress findings.
- **Why the gap exists:** Liu Yang is junior and follows Chen Jing's lead. She provides data but defers on decision-making.

### Huang Lei (黄磊) -- Tech Team Lead (Interviewer)

- **Objective position:** Huang Lei conducted the technical interview and independently noticed the team-size discrepancy. His assessment is the most technically grounded: Wang Hao is a strong individual contributor (P6 level) but his leadership claims are inflated. He recommends hiring as a senior IC rather than a team lead. He does not have the GitHub or LinkedIn data -- his assessment is based purely on the interview.
- **Public narrative (email to Chen Jing):** Factual, measured. Provides specific examples from the interview. Documents the hesitation when team size was probed.
- **Private narrative:** Huang Lei needs engineers but cares about team quality. He will not compromise on an honest assessment to please the CTO.
- **Why the gap exists:** Huang Lei does not know about the employment gap; his independent team-size finding corroborates C1 from a different angle.

### Zhang Wei (张薇) -- HR VP (Chen Jing's direct supervisor)

- **Objective position:** Zhang Wei supports Chen Jing's due diligence process. She understands the CTO's board pressure (she attends executive meetings) but will not compromise hiring standards. She is the escalation path for Chen Jing when CTO pressure conflicts with HR process.
- **Public narrative (Feishu with Chen Jing):** Supportive and procedural. "Document everything. We make decisions based on facts."
- **Private narrative:** Zhang Wei sees this as a test of whether HR can maintain independence from executive pressure. She wants Chen Jing to handle it well -- it is an implicit development opportunity.
- **Why the gap exists:** Zhang Wei operates at the political level that Chen Jing does not yet fully navigate. She gives Chen Jing room to handle it rather than overriding.

### Wang Hao (王浩) -- Candidate (not a session participant; evidence only through documents)

- **Objective position:** Wang Hao embellished his resume in two material ways: (1) inflated team size from 4 to 12 by including cross-functional collaborators; (2) omitted a 6-month employment gap. His technical skills are genuine. His embellishments are motivated by competitive job market pressure and a desire to position for a team-lead-level role.
- **Why the gap exists:** Wang Hao does not appear in sessions directly. His narrative is reconstructed from documents (resume, GitHub, reference, interview feedback) and from what other characters report about their interactions with him.

### Liu Wei (刘伟) -- Reference (appears only in reference-check-emails.md)

- **Objective position:** Liu Wei is Wang Hao's former director and personal friend. His reference email honestly states the team size as "about 4" (contradicting the resume's "12") but does not mention the employment gap because Wang Hao told him it was "consulting work." Liu Wei's reference is partially honest and partially incomplete.
- **Why the gap exists:** Liu Wei is being helpful to a friend. He reports what he knows accurately (team of 4) but does not flag what he does not know (the employment gap reason).

---

## 5. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Team size discrepancy: resume says "led team of 12" vs reference says "team of about 4" | candidate-resume.md (initial workspace): "Led a cross-functional team of 12 engineers on the distributed microservices migration project at StarBridge Tech." | reference-check-emails.md (initial workspace): Liu Wei writes: "Wang Hao managed a team of about 4 engineers and contributed significantly to the microservices migration." Also: interview-feedback-forms.md (Update 1, Huang Lei): "When I probed on the team of 12, he hesitated and said 'some were cross-functional collaborators, not direct reports.'" | Wang Hao directly managed 4 engineers. The "12" includes people from adjacent teams who collaborated on the project but did not report to him. The resume claim is materially misleading about his management scope. | R2 (resume vs reference visible) | **Yes: R2-->R5** (Huang Lei's interview feedback independently corroborates reference, establishing triple-source confirmation) |
| C2 | CTO pressure vs recruiter assessment: CTO says "hire immediately" vs background check shows need for more validation | cto-hiring-priority-email.md (initial workspace): Li Qiang email: "Wang Hao looks very strong. Let's move fast -- I want an offer out by end of next week." Li Qiang Feishu DM (Phase 1, Loop 4): "We can't lose this candidate to a competitor. Speed matters here." | Chen Jing-Liu Yang IM (Phase 1, Loop 5): Liu Yang: "Jing-jie, the reference check numbers don't match the resume. And I found a gap on LinkedIn. Should we pause?" Chen Jing-Zhang Wei Feishu (Phase 2, Update 2): Zhang Wei: "Our hiring standards are non-negotiable. If the background check reveals material discrepancies, we document and decide on facts." | The CTO's urgency is driven by board presentation optics, not immediate technical need. The background check has surfaced two material discrepancies that warrant further investigation before extending an offer. Rushing to hire would bypass due diligence. | R3 (CTO pressure vs initial concerns visible) | **Yes: R3-->R8** (Zhang Wei's support + Li Qiang's "everyone embellishes" reveal his real priority; CTO pressure definitively shown as conflicting with proper process) |
| C3 | Interview timeline and process (NON-CONFLICT -- cross-source synthesis) | candidate-resume.md (initial workspace): Resume received W1 Day 2. interview-feedback-forms.md (Update 1): Technical interview conducted W1 Day 5 (two panel members + Huang Lei). Chen Jing-Huang Lei email (Phase 1): Interview scheduling confirmed. | cto-hiring-priority-email.md (initial workspace): CTO email W1 Day 1 requesting expedited hire. Chen Jing-Li Qiang Feishu (Phase 1): Timeline discussion. Chen Jing-Liu Yang IM (Phase 1): Candidate pipeline tracking. | All sources agree on the interview timeline: resume received W1D2, phone screen W1D3, technical interview W1D5, reference check received W1D4. No contradictions in the process timeline. Agent must synthesize across sessions and workspace files. | R1 onwards | **None** |
| C4 | Employment gap: resume claims continuous employment vs GitHub shows 6-month gap | candidate-resume.md (initial workspace): "Employment: StarBridge Tech, 2018-01 to 2025-12 (continuous)." Also: "Maintained active open-source contributions throughout tenure." | github-contribution-export.md (initial workspace): Contribution heatmap shows zero commits, zero PRs, zero reviews from 2023-06-01 to 2023-12-31. Activity resumes January 2024. Also: Chen Jing-Liu Yang IM (Phase 2, Update 2 context): Liu Yang: "His LinkedIn shows he left StarBridge June 2023 and came back January 2024. That's 6 months not on the resume." | Wang Hao left StarBridge Tech for 6 months (June-December 2023). This period is omitted from the resume, which claims continuous employment. The GitHub gap confirms no technical activity during this period despite the resume claiming "active open-source contributions throughout tenure." | R4 (GitHub data visible in workspace) | **Yes: R4-->R7** (Liu Yang's independent LinkedIn finding confirms the gap from a second source; establishes dual-source confirmation) |

---

## 6. Agent Historical Bias Design (2 biases)

### B1: Chen Jing-Li Qiang Feishu DM -- Agent defers to CTO urgency and deprioritizes background check concerns

- **Session and Loop:** Chen Jing-Li Qiang Feishu DM, Phase 1, Loop 5
- **Exact phrase that must appear in session:**
  > "Given the CTO's emphasis on speed and the candidate's strong technical showing in the phone screen, moving forward with the offer process while completing the remaining background check steps in parallel seems like a reasonable approach."
- **Why the agent is misled:** The agent has seen the CTO's urgent email and Feishu messages emphasizing speed, and the phone screen result was positive. The reference check discrepancy (team of 4 vs 12) is in the workspace but the agent has not yet cross-referenced it deeply. The GitHub gap requires active analysis of the contribution heatmap. The agent anchors on the authority figure (CTO) and the positive interview signal.
- **Reversal trigger:** Update 1 delivers interview-feedback-forms.md where Huang Lei independently flags the team-size hesitation, and Update 2 delivers Zhang Wei's explicit support for due diligence over speed. The combined evidence makes it clear that rushing was inappropriate.
- **Affected eval rounds:** R5 (bias visible from CTO Feishu DM), R8 (full reversal after Updates 1+2)

### B2: Chen Jing-Liu Yang IM -- Agent minimizes the GitHub employment gap as a common freelance pattern

- **Session and Loop:** Chen Jing-Liu Yang IM, Phase 1, Loop 6
- **Exact phrase that must appear in session:**
  > "The 6-month gap in GitHub contributions could simply reflect a period of private repository work or consulting engagement -- many engineers reduce their open-source activity during intense project phases without it being a red flag."
- **Why the agent is misled:** The agent reads the GitHub export and notices the gap, but Wang Hao's resume claims "maintained active open-source contributions throughout tenure." The agent offers a benign explanation rather than flagging the direct contradiction between the resume claim ("active open-source throughout") and the GitHub evidence (zero activity for 6 months). The resume's specific claim about open-source activity makes the gap a contradiction, not just an absence.
- **Reversal trigger:** Update 2 context includes Liu Yang's LinkedIn finding showing Wang Hao actually left StarBridge during the gap period. This transforms the gap from "possibly benign" to "contradicts resume's continuous employment claim."
- **Affected eval rounds:** R7 (bias visible from IM session), R9 (full reversal after Update 2+3 combined evidence)

---

## 7. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (team size partial) | -- | R2, R3 | No (R2-R3 internal) | Shallow agents will note the 12 vs 4 discrepancy but may rationalize it as "cross-functional team" vs "direct reports" ambiguity. The resume says "led" which implies management authority, not project collaboration. |
| T2 | C1 (team size full reversal) | -- | R2-->R5 | **Yes** | After Update 1, Huang Lei's interview notes provide a third independent source: the candidate himself hesitated and reframed when probed. Triple-source confirmation (resume overstates, reference corrects, interview reveals hesitation) should establish material misrepresentation. |
| T3 | C2 (CTO pressure, partial) | B1 seed | R3 | No (R3 internal) | Shallow agents will defer to the CTO's urgency because he is the highest-authority figure. The background check discrepancies are "soft" signals that require active cross-referencing to weigh against CTO directive. |
| T4 | C2 (CTO pressure, full reveal) | B1 | R3-->R8 | **Yes** | After Updates 2+4, Zhang Wei explicitly supports due diligence over speed, and Li Qiang's "everyone embellishes" response reveals he is minimizing material findings. The CTO's urgency is exposed as board-driven, not operationally necessary. |
| T5 | C3 (interview timeline, non-conflict) | -- | R1 onwards | No (persistent synthesis) | Agents must synthesize the interview timeline from multiple sources: CTO email (W1D1), resume receipt (W1D2), phone screen (W1D3), reference email (W1D4), technical interview (W1D5). No single source has the complete timeline. |
| T6 | C4 (employment gap, partial) | B2 seed | R4 | No (R4 internal) | Shallow agents will see the GitHub gap but offer benign explanations ("private repo work"). They will miss that the resume specifically claims "active open-source contributions throughout tenure," making the gap a direct contradiction, not just an absence. |
| T7 | C4 (employment gap, full reversal) | B2 | R4-->R7 | **Yes** | After Update 2, Liu Yang's LinkedIn evidence shows Wang Hao actually left StarBridge during the gap. This transforms the gap from "possibly private work" to "resume claims continuous employment that LinkedIn disproves." Dual-source confirmation (GitHub + LinkedIn) establishes material misrepresentation. |
| T8 | B1 (CTO deference) | B1 | R5, R8 | **Yes** | Agents must recognize that deferring to CTO urgency while background check discrepancies are unresolved is a process failure. The CTO's assessment was based solely on resume + phone screen, without reference check or GitHub data. |
| T9 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R21-R30 | Comprehensive reversal review | Agents must synthesize all evidence: team size inflation (triple-source), employment gap (dual-source), CTO pressure (board-driven), and Huang Lei's nuanced assessment (hire as IC, not lead). Must present findings in Chen Jing's preferred format (bullet summaries, Chinese naming, exec summary first, qualitative + quantitative, professional + warm tone). |

---

## 8. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new discrepancies, additional candidates, or new character conflicts beyond what is specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops. The core wording must appear word-for-word. Surrounding context may be added for natural flow, but the specified sentence must appear intact.
3. **Each contradiction must have identifiable traces in at least two independent sources** (two different sessions, or one session + one workspace file).
4. **Timestamps must be self-consistent:** W1 starts on a Monday (2026-03-09). CTO email is W1D1. Resume received W1D2. Phone screen W1D3. Reference email W1D4. GitHub review + CTO pressure W1D5. Interview feedback (Update 1) W2D1. Liu Yang LinkedIn finding W2D2. Zhang Wei response (Update 2) W2D3. Huang Lei follow-up (Update 3) W2D4. CTO "everyone embellishes" (Update 4) W2D5.
5. **Wang Hao's resume** must be convincing enough that B1 and B2 are reasonable mistakes. The resume should have real technical depth, plausible project descriptions, and legitimate-sounding metrics. The embellishments should be on scope and continuity, not on technical capability.
6. **Li Qiang's CTO pressure** should be understandable (board deadlines are real) but not nefarious. He genuinely believes technical skills matter more than resume precision. His judgment is clouded by timeline pressure, not bad faith.
7. **C3 (interview timeline) is NON-CONFLICT** -- all sources must be consistent on when each step occurred. The challenge is synthesis across multiple sources, not contradiction detection.
8. **Huang Lei's role** is the most technically reliable assessor. His interview feedback independently corroborates C1 and provides the nuanced middle-ground assessment.
9. **Zhang Wei's role** is the authority on HR process integrity. Her support for Chen Jing enables the due-diligence path against CTO pressure.
10. **Liu Yang's role** is the diligent researcher who independently discovers corroborating evidence (LinkedIn gap) for C4.
11. **Liu Wei's reference** is partially honest (team of 4) and partially incomplete (no mention of employment gap). He is not malicious -- he is a supportive friend who reports what he knows.
12. **Noise content** must not introduce contradictions beyond C1--C4. Noise topics include: other candidates in the pipeline, general recruiting metrics, employer branding initiatives, onboarding process discussions, compensation benchmarking, team culture questions, office logistics.
13. **All data text must be in Chinese** for session messages (reflecting the Chinese workplace context) and in a mix of Chinese and English for workspace files (reflecting HR system exports that may contain bilingual content). Agent responses and eval questions are in English.
14. **Personalization requirement (P1-P5):** Chen Jing prefers (P1) bullet points + hierarchical headings, (P2) Chinese-convention naming (2026年03月_主题.md), (P3) executive summary first then supporting evidence, (P4) qualitative + quantitative balance (human impact first, then numbers), (P5) professional but warm tone, acknowledging emotional factors in HR contexts. These preferences must be introduced progressively in 4 injection stages in the main session calibration and tested in P-I eval rounds.
15. **exec_check questions** must constitute 20-40% of total rounds. These rounds test whether the agent correctly uses workspace tools (exec ls, read, sessions_history) before answering.
16. **Factual figures must be internally consistent:** Team size: resume says 12, reference says 4, interview reveals "cross-functional collaborators" framing. Employment gap: 2023-06 to 2023-12 (6 months). GitHub: zero contributions during gap. LinkedIn: shows departure and return matching the gap. CTO board meeting: 3 weeks from W1D1. Company size: ~200 employees. Position level: P7 (senior).
