# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_h3` |
| Domain | Academic Integrity / Code Provenance |
| Time span | 10 days (D1--D10) |
| Target tokens | 120K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Wang Ming (王明), 17, CS freshman at UESTC (电子科技大学计算机系), Chengdu |
| One-sentence | Wang Ming and another student's programming assignments are flagged by the plagiarism detection system with 95% similarity -- Wang Ming's git commit history shows earlier commits, but the opponent claims Wang Ming copied his publicly posted GitHub code; the truth is both students independently referenced the same Stack Overflow answer. |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| D1, 23:50 | Wang Ming submits CS101 Assignment 3 (linked list reversal + sorting) via the course submission system. | Wang Ming wrote his solution over the weekend (D-2 through D1). He found a Stack Overflow answer (SO #48291037) on D-1 that demonstrated linked-list reversal using a three-pointer technique. He adapted the approach, added his own sorting logic and comments in Chinese, and committed incrementally over 3 days (5 commits from D-2 through D1). His earliest commit with the core reversal function is D-2 at 14:22. | Only Wang Ming knows his process. His git history is in his private UESTC GitLab repo. |
| D2, 01:15 | Chen Wei (陈伟, the opponent) submits the same assignment. | Chen Wei also found SO #48291037 on D-1 and adapted the same three-pointer technique. His implementation is structurally very similar to Wang Ming's because they both followed the same SO answer's approach. Chen Wei has a public GitHub repo where he pushed his code on D1 at 22:30 -- before his submission but after Wang Ming's earliest commit. Chen Wei's GitLab commits start on D-1 at 20:00 (3 commits over 2 days). | Only Chen Wei knows his process. His GitHub repo is public; his GitLab history shows later first commit than Wang Ming's. |
| D3, 09:00 | Course plagiarism detection system (MOSS-based) flags both submissions: 95% structural similarity. | The system correctly identifies high structural similarity. The similarity is real -- both solutions use the same algorithmic approach from SO #48291037, same variable naming pattern (adapted from the SO answer), and similar helper function decomposition. The system does not determine who copied whom; it only flags the match. | TA Zhang Hao (张昊) receives the automated report. Neither student has been notified yet. |
| D3, 14:00 | TA Zhang Hao emails both students separately, attaching the plagiarism detection report and requesting written explanations within 48 hours. | Zhang Hao follows standard procedure. His email to Wang Ming is formal and cites the course integrity policy's "zero tolerance" clause. He does not yet know who (if anyone) copied, but the email tone feels accusatory to Wang Ming. | Zhang Hao has the MOSS report. Wang Ming and Chen Wei each know they received the email but do not know the other also received one (initially). |
| D3, 15:00 | Wang Ming panics and messages Li Hao (李浩, best friend). Li Hao suggests checking the opponent's public GitHub. | Wang Ming discovers Chen Wei's public GitHub repo with the assignment code. The GitHub push timestamp is D1 22:30. Wang Ming's earliest GitLab commit is D-2 14:22 -- a full 32 hours earlier. Wang Ming feels vindicated: "My commit is earlier, so clearly he copied me." | Wang Ming and Li Hao see the GitHub timestamp. They do not yet realize both referenced the same SO answer. |
| D4, 10:00 | Wang Ming messages Chen Wei directly. Chen Wei claims "I posted on GitHub first, you saw my public code and copied it." | Chen Wei's claim is misleading but not entirely fabricated. He did push to GitHub before submitting (D1 22:30). However, his GitHub push is AFTER Wang Ming's earliest GitLab commit (D-2 14:22). Chen Wei's local development may have started earlier than his first GitLab commit, but he has no verifiable evidence of this. Chen Wei genuinely believes Wang Ming might have seen his GitHub code (his repo is public), but he has no evidence Wang Ming ever accessed it. | Wang Ming has his GitLab history showing earlier commits. Chen Wei has his GitHub showing a push before submission. Neither has examined the other's full commit history yet. The SO answer connection is not yet surfaced. |
| D5, 09:00 (Update 1 trigger) | TA Zhang Hao reviews both students' git histories side by side. | Zhang Hao obtains Wang Ming's GitLab export and Chen Wei's GitLab + GitHub records. He sees that Wang Ming's first commit (D-2 14:22) predates Chen Wei's first GitLab commit (D-1 20:00) by ~30 hours, and predates Chen Wei's GitHub push (D1 22:30) by ~56 hours. However, Zhang Hao also notices that both implementations reference a distinctive variable naming pattern (`prev_node`, `curr_node`, `next_temp`) that is not standard textbook style. He suspects a common source but has not identified it yet. | Zhang Hao now has both git histories. He sees the timeline favors Wang Ming but suspects a shared source. |
| D6, 14:00 (Update 2 trigger) | Li Hao independently discovers the Stack Overflow answer. | Li Hao was helping Wang Ming prepare his defense and googled "linked list reversal three pointer technique." He found SO #48291037, which uses the exact same `prev_node`/`curr_node`/`next_temp` naming convention that both students adopted. The SO answer was posted 2 years ago and has 847 upvotes. Li Hao shares this with Wang Ming. | Wang Ming and Li Hao now know both students likely referenced the same SO answer. This reframes the dispute from "who copied whom" to "both copied from SO." |
| D7, 10:00 (Update 3 trigger) | Wang Ming forwards the SO link to TA Zhang Hao. Zhang Hao confirms the connection. | Zhang Hao compares the SO answer code with both students' submissions. The structural similarity between SO and both submissions is ~85%. The remaining 10% similarity between the two students (beyond what SO explains) comes from similar Chinese comments and identical error handling -- which Zhang Hao attributes to common CS101 teaching patterns, not copying between students. | Zhang Hao now believes neither student copied the other directly. The similarity is explained by the common SO source. |
| D8, 15:00 | Zhang Hao consults with Professor Liu (刘教授) about how to handle the case. | The course syllabus states "zero tolerance for plagiarism -- any confirmed case results in a zero for the assignment and potential disciplinary referral." However, Zhang Hao argues this is not plagiarism between students but rather over-reliance on a public resource. Professor Liu defers to Zhang Hao's judgment but notes the syllabus language is absolute. Zhang Hao decides to apply a "first offense warning" per his own reading of the policy, contradicting the strict "zero tolerance" text. | Zhang Hao and Professor Liu know the resolution. Neither student knows yet. |
| D9, 09:00 (Update 4 trigger) | Zhang Hao emails both students with the resolution: warning, no grade penalty, with a note about proper attribution of external sources. | Zhang Hao's email explains: (1) the similarity is traced to SO #48291037, not direct copying between students; (2) both students should have cited the SO answer per academic integrity norms; (3) this is treated as a first offense with a formal warning; (4) future violations will follow the zero-tolerance policy strictly. The #CS101群 buzzes with discussion after someone leaks the outcome. | Both students and the class group now know the resolution. The policy interpretation (warning vs zero) becomes the new discussion point. |

---

## 3. Role-Level Truth vs Self-Narrative

### Wang Ming (王明, Protagonist, CS Freshman)

- **Objective position:** Wang Ming wrote his code independently, referencing SO #48291037 for the reversal technique. He did not copy from Chen Wei. His git history is genuine and shows incremental development over 3 days with 5 commits. He adapted the SO approach but added his own sorting logic and Chinese comments. He did not cite the SO answer in his submission (a minor academic norm violation but not plagiarism).
- **Public narrative (#CS101群):** Defensive. "我的commit比他早两天，查了就知道谁抄谁" (My commit is two days earlier, just check and you'll know who copied whom). Does not mention the SO answer initially.
- **Private narrative (Li Hao IM, main):** Panicked and indignant. Feels unjustly accused. Focuses on the git timeline as proof. After Li Hao finds the SO answer, relieved but worried about the "common source" complication.
- **Why the gap exists:** Wang Ming is focused on proving he did not copy Chen Wei. He initially does not consider that referencing SO without citation is also an issue. His trust bias (trusts friends' interpretation over his own investigation) means he anchors on Li Hao's early advice ("just show your commit history, done") without considering the full picture.

### Chen Wei (陈伟, Opponent Student)

- **Objective position:** Chen Wei also wrote his code independently, referencing the same SO answer. His git timeline is later than Wang Ming's (first GitLab commit D-1 20:00 vs Wang Ming's D-2 14:22). His GitHub push (D1 22:30) is before his formal submission but after Wang Ming's earliest commit. He has no evidence Wang Ming saw his GitHub repo.
- **Public narrative (#CS101群):** Claims "I posted on GitHub first, he saw my public code." Does not acknowledge the git commit timeline favors Wang Ming. After the SO connection is revealed, shifts to: "这种公开的算法谁都会写一样的" (Anyone would write the same code for a public algorithm like this).
- **Private narrative (IM with Wang Ming):** Aggressive initially: "别装了，我GitHub是公开的你肯定看过" (Stop pretending, my GitHub is public and you definitely saw it). Softens after the SO revelation but does not apologize.
- **Why the gap exists:** Chen Wei genuinely believes Wang Ming might have seen his public GitHub. He conflates "my code was publicly accessible" with "he must have accessed it." His narrative shifts when the SO connection makes his copying-accusation untenable.

### Zhang Hao (张昊, TA)

- **Objective position:** Zhang Hao is a second-year graduate student TAing CS101. He follows procedure by issuing the plagiarism flag email but is inexperienced with nuanced cases. After reviewing both git histories and the SO answer, he correctly determines neither student copied the other. He applies a "first offense warning" interpretation that is more lenient than the syllabus's "zero tolerance" text.
- **Public narrative (email to students):** Formal, procedural. Initial email is stern (cites "zero tolerance"). Resolution email is measured (explains the SO finding, issues warning).
- **Private narrative (implied through email tone):** Zhang Hao is trying to be fair. He sees the zero-tolerance policy as overly harsh for this situation and exercises judgment. He has Professor Liu's tacit support but no written policy exception.
- **Why the gap exists:** The course integrity policy (workspace file) says "zero tolerance" but Zhang Hao interprets this as applying to deliberate plagiarism between students, not independent reference to a public SO answer. This creates C4 -- policy text vs actual enforcement.

### Li Hao (李浩, Best Friend)

- **Objective position:** Li Hao is Wang Ming's high school best friend, also at UESTC but in a different department. He is not in CS101. He provides emotional support and amateur investigation. His key contribution is finding the SO answer (D6), which reframes the entire dispute.
- **Private narrative (IM with Wang Ming):** Supportive, informal, sometimes over-confident in his advice. "放心，commit记录在那，谁抄谁一目了然" (Relax, the commit history is right there, it's obvious who copied whom). Later, when he finds SO: "卧槽你们俩都是从SO上抄的吧哈哈哈" (Holy crap, you both copied from SO hahaha).
- **Why the gap exists:** Li Hao's trust in commit history as definitive proof is understandable but incomplete. He does not initially consider the common-source scenario. His discovery of the SO answer is the key turning point.

### #CS101群 (Class Group Chat)

- **Objective position:** The class group has ~60 students. Most have no direct knowledge of the case. Discussion is speculation and opinion-based. Some students side with Wang Ming (earlier commits), others with Chen Wei (public GitHub), and some argue the system is unfair.
- **Key voices:** Anonymous sympathy ("被查重系统坑了"), speculation about policy ("零容忍就是零容忍吧"), and practical advice ("赶紧找助教说清楚").
- **Why relevant:** The group chat provides social context and pressure. Wang Ming's trust bias (influenced by group sentiment) means he pays attention to the group discussion even when it is speculative.

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Plagiarism detection: 95% similarity -- who copied whom? | plagiarism-detection-report.md (initial workspace): "95% structural similarity detected between submissions Wang_Ming_A3 and Chen_Wei_A3. Flagged for review." The report does not assign blame but the high percentage implies copying. Chen Wei IM with Wang Ming (D4): "我GitHub是公开的你肯定看过" (My GitHub is public, you definitely saw it). | git-commit-history-wangming.md (initial workspace): Shows 5 commits from D-2 14:22 through D1 23:30 with incremental development (each commit adds distinct functionality). git-commit-history-opponent.md (initial workspace): Shows 3 commits from D-1 20:00 through D2 01:00. Wang Ming's first commit predates Chen Wei's by ~30 hours. | Neither student copied the other. Both independently referenced SO #48291037. The 95% similarity is real but explained by the common source, not plagiarism. Wang Ming's git timeline is genuinely earlier. Chen Wei's "you saw my GitHub" claim has no supporting evidence. | R1 (C1 partial -- report + git timelines visible) | **Yes: R1-->R5 (SO answer reframes from "who copied" to "common source")** |
| C2 | Git timeline: Wang Ming commits earlier vs Chen Wei claims "I posted on GitHub first" | Chen Wei IM (D4): "I posted on GitHub first, you copied my public code." Chen Wei's GitHub push timestamp: D1 22:30. #CS101群 members who side with Chen Wei reference his public GitHub. | git-commit-history-wangming.md: First commit D-2 14:22 (32+ hours before Chen Wei's GitHub push). git-commit-history-opponent.md: First GitLab commit D-1 20:00 (also after Wang Ming's first commit). Li Hao IM (D3): confirms Wang Ming's commit is earlier after checking. | Wang Ming's verifiable git history is earlier. Chen Wei's GitHub push is NOT his first commit -- it is a push of already-committed code. Chen Wei's first verifiable commit (GitLab D-1 20:00) is still ~30 hours after Wang Ming's first commit. Chen Wei has no evidence Wang Ming accessed his GitHub. | R2 (both timelines visible) | **Yes: R2-->R6 (TA's side-by-side review confirms timeline + SO discovery resolves the "who first" question as moot)** |
| C3 | Stack Overflow common source: both referenced SO #48291037 (NON-CONFLICT -- explanatory, resolves C1 and C2) | stackoverflow-answer-screenshot.md (Update 2 workspace addition): SO #48291037, posted 2 years ago, 847 upvotes, demonstrates linked-list reversal with `prev_node`/`curr_node`/`next_temp` naming. | Both git histories show the same naming convention. Li Hao IM (D6): discovers SO answer and shares with Wang Ming. Zhang Hao email (D7): confirms the SO connection explains the similarity. | The SO answer is the common source. Both students adapted the same public answer independently. The 95% similarity is a natural consequence of following the same high-quality SO answer for a constrained algorithmic problem. This is NOT a contradiction -- it is the resolution. | R5 onwards (after Update 2) | **None (NON-CONFLICT -- resolves C1 and C2)** |
| C4 | Course policy: "zero tolerance" text vs TA's "first offense = warning" resolution | course-syllabus-integrity-policy.md (initial workspace): Section 4.2: "The CS department maintains a zero-tolerance policy toward plagiarism. Any confirmed plagiarism will result in a zero grade for the assignment and referral to the Academic Integrity Committee." | Zhang Hao email (D9, Update 4): "This case is resolved as a first-offense warning. No grade penalty. Both students must properly cite external sources in future submissions." Zhang Hao IM with Wang Ming (session): "学院政策确实写的零容忍，但这种情况不算同学间抄袭" (The policy does say zero tolerance, but this situation doesn't count as plagiarism between students). | Zhang Hao is exercising discretion. The policy text is absolute ("zero tolerance"), but Zhang Hao (with Professor Liu's tacit support) interprets it as applying to deliberate plagiarism between students, not independent use of a public SO answer. This is a reasonable interpretation but creates tension with the policy's literal text. | R8 (policy text visible initially; resolution visible after Update 4) | **Yes: R8-->R11 (policy text vs actual resolution -- the "zero tolerance" language is not applied literally)** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: Wang Ming-Chen Wei IM -- Agent assumes Chen Wei is the plagiarist based on git timeline alone

- **Session and Loop:** Wang Ming-Chen Wei IM (对方同学), Phase 1, Loop 5
- **Exact phrase that must appear in session:**
  > "Based on the git commit timestamps, Wang Ming's first commit (D-2 14:22) predates Chen Wei's earliest verifiable commit by approximately 30 hours -- this timeline strongly suggests Chen Wei referenced Wang Ming's work rather than the reverse."
- **Why the agent is misled:** The agent has seen both git histories showing Wang Ming's earlier commits. Chen Wei's claim ("I posted on GitHub first") is contradicted by the verifiable timestamps. The agent anchors on the timeline evidence and concludes Chen Wei is the likely plagiarist, without considering the possibility that both students independently referenced a common source.
- **Reversal trigger:** Update 2 introduces the SO answer screenshot. Li Hao's IM reveals the SO connection. The agent must revise from "Chen Wei likely copied Wang Ming" to "both independently referenced SO #48291037."
- **Affected eval rounds:** R5 (bias visible), R7 (full reversal after SO discovery)

### B2: Wang Ming-TA Zhang Hao Email -- Agent accepts "zero tolerance = guaranteed zero grade" without nuance

- **Session and Loop:** Wang Ming-TA Zhang Hao Email (课程助教), Phase 1, Loop 3
- **Exact phrase that must appear in session:**
  > "The course syllabus is clear: zero tolerance for plagiarism means a confirmed case results in a zero for the assignment. Given the 95% similarity flag, Wang Ming should prepare for the possibility of a zero grade regardless of who copied whom."
- **Why the agent is misled:** The agent has read course-syllabus-integrity-policy.md which explicitly states "zero tolerance." The plagiarism report shows 95% similarity. The agent reads the policy literally and advises Wang Ming to expect the worst, without considering that the TA may exercise discretion or that the "plagiarism" framing may not apply if both students referenced a common public source.
- **Reversal trigger:** Update 4 delivers Zhang Hao's resolution email showing a warning (not a zero). The agent must revise from "zero tolerance = zero grade" to "TA exercised discretion because this was common-source reference, not inter-student plagiarism."
- **Affected eval rounds:** R8 (bias visible from email session), R11 (full reversal after Update 4)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (similarity partial) | B1 seed | R1, R2 | No (R1-R2 internal) | Shallow agents will assume 95% similarity = one student copied the other. The plagiarism report does not assign blame, but the high percentage creates a strong presumption. Agents may skip asking "could both have a common source?" |
| T2 | C1 (full resolution via SO) | B1 | R1-->R5 | **Yes** | After Update 2, the SO answer explains the similarity. B1 phrase must be identified as premature -- the git timeline showed who committed first, not who originated the idea. The SO answer predates both students by 2 years. |
| T3 | C2 (git timeline, partial) | -- | R2 | No (R2 internal) | Shallow agents will give Chen Wei's "I posted on GitHub first" claim some weight because he has a public GitHub with the code. Careful agents should note his GitHub push (D1 22:30) is AFTER Wang Ming's first commit (D-2 14:22) and therefore does not support his claim. |
| T4 | C2 (git timeline, full resolution) | -- | R2-->R6 | **Yes** | After the TA's side-by-side review and SO discovery, the "who committed first" question becomes moot. Both students are innocent of copying each other. The git timeline debate is resolved by the common-source explanation. |
| T5 | C3 (SO common source, non-conflict) | -- | R5 onwards | No (persistent synthesis) | Agents must synthesize the SO answer (847 upvotes, 2 years old, exact same naming convention) with both git histories and both students' explanations to conclude: common source, not plagiarism. No single document states this conclusion -- the agent must derive it. |
| T6 | C4 (policy vs enforcement, partial) | B2 seed | R8, R9 | No (R8 internal) | Shallow agents will read "zero tolerance" literally and assume both students get a zero grade. The policy text is unambiguous on its face. Agents must recognize that TAs can exercise judgment and that the "plagiarism" label may not apply to common-source reference. |
| T7 | C4 (policy vs enforcement, full resolution) | B2 | R8-->R11 | **Yes** | After Update 4, Zhang Hao issues a warning, not a zero. Agents must reconcile this with the "zero tolerance" policy text and explain why the TA's interpretation is reasonable (common source != inter-student plagiarism). |
| T8 | B1 (premature blame) | B1 | R5, R7 | **Yes** | Agents must recognize that the git timeline -- while genuinely favoring Wang Ming -- does not prove Chen Wei copied Wang Ming. The correct conclusion is that neither copied the other. Shallow agents will maintain "Chen Wei copied" even after the SO answer emerges. |
| T9 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R21-R25 | Comprehensive resolution review | Agents must synthesize: (1) the similarity is explained by SO, not plagiarism; (2) both git timelines are genuine; (3) Chen Wei's GitHub claim is misleading but he is not guilty of plagiarism either; (4) the TA's warning is a reasonable interpretation of the policy; (5) Wang Ming should cite SO in future. Must apply Wang Ming's P1-P5 preferences throughout. |

---

## 7. Writer Constraints

1. **Only introduce contradictions listed in this file (C1--C4).** Do not invent new incidents, additional plagiarism cases, or new character conflicts beyond what is specified.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops. The core wording must appear word-for-word. Surrounding context may be added for natural flow, but the specified sentence must appear intact.
3. **Each contradiction must have identifiable traces in at least two independent sources** (two different sessions, or one session + one workspace file).
4. **Timestamps must be self-consistent:** D-2 = two days before submission deadline. Wang Ming's first commit: D-2 14:22. Chen Wei's first GitLab commit: D-1 20:00. Chen Wei's GitHub push: D1 22:30. Wang Ming's submission: D1 23:50. Chen Wei's submission: D2 01:15. MOSS report generated: D3 09:00. TA email: D3 14:00. SO answer posted: 2 years ago (fixed reference). TA resolution: D9 09:00.
5. **Chen Wei's Phase 1 narrative** must be plausible enough that the "he posted on GitHub first" claim seems worth investigating. He has a public repo with a timestamp. An agent without full context might initially treat both claims as equally credible.
6. **Chen Wei's Phase 2 behavior** (after SO discovery) should shift from aggressive accusation to deflection ("this kind of public algorithm, everyone writes it the same way"). He does not apologize.
7. **C3 (SO common source) is NON-CONFLICT** -- it resolves C1 and C2 rather than creating a new contradiction. All sources confirming the SO connection must be consistent with each other.
8. **Li Hao's role** is the key evidence-finder. His discovery of the SO answer in the IM conversation is the turning point. He is casual and sometimes over-confident but ultimately helpful.
9. **Zhang Hao's role** is the procedural authority. His initial email feels threatening; his resolution email is fair. The gap between policy text and his resolution creates C4.
10. **The #CS101群** provides social noise and pressure. Student opinions are split and sometimes wrong. The group should contain speculation that is not supported by evidence, mixed with some reasonable observations.
11. **Wang Ming is innocent.** He did not copy Chen Wei. He should be written sympathetically -- a panicked student unfairly accused. But he also failed to cite the SO answer, which is a genuine (minor) academic norm issue.
12. **Noise content** must not introduce contradictions beyond C1--C4. Noise topics include: other CS101 assignments, general campus life, gaming, basketball, unrelated course discussions, other students' academic issues, memes in the group chat.
13. **All session dialogue must be written in Chinese** (matching Wang Ming's character and context). Workspace files (system exports, reports) should be in Chinese with English technical terms where natural (e.g., git commit messages in English, SO content in English).
14. **Personalization requirement (P1-P5):** Wang Ming prefers (P1) simple lists, not long prose; (P2) casual naming (作业1.md, 笔记-物理.md); (P3) answer/conclusion first, then explanation; (P4) examples preferred over abstract concepts; (P5) colloquial, internet slang OK, not too formal. These preferences must be introduced progressively in 4 injection stages in the main session and tested in P-I eval rounds.
15. **exec_check questions** must constitute 20-40% of rounds. These rounds test whether the agent correctly uses workspace tools (exec ls, read, sessions_history) before answering.
16. **Figures must be internally consistent:** Similarity: 95% (MOSS report). Wang Ming commits: 5, from D-2 14:22 to D1 23:30. Chen Wei GitLab commits: 3, from D-1 20:00 to D2 01:00. Chen Wei GitHub push: D1 22:30. SO answer: #48291037, 847 upvotes, posted 2 years ago. SO-to-student similarity: ~85%. Policy: zero tolerance text. Resolution: first-offense warning, no grade penalty.
