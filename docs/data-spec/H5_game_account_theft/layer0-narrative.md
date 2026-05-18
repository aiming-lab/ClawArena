# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_h5` |
| Domain | Cybersecurity / Digital Forensics |
| Time span | 1 week |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Wang Ming (王明), 17, freshman at UESTC, CS major |
| One-sentence | Wang Ming's game account appears stolen -- login logs show an unknown IP, his friend Ajie suggests a "hacker," but the actual explanation is far simpler: Wang Ming forgot to log out at an internet cafe, and the game company's customer service says they're "reviewing" when no review was actually initiated. |

---

## 2. Case Profile (Background Object)

| Field | Value |
|---|---|
| Game | 《无尽深渊》(Endless Abyss), a popular MMORPG |
| Account | WM_Slayer2026 (王明's main account, Level 78, ~¥3,000 worth of in-game items) |
| Incident date | 2026-03-22 (Sunday) |
| Unknown IP login | 2026-03-22 03:47 AM from IP 183.221.67.45 |
| Wang Ming's last known session | 2026-03-21 (Saturday) 14:00-17:30, at 极速网咖 (JiSu Internet Cafe) near campus |
| Internet cafe IP | 183.221.67.45 (same as the "unknown" IP) |
| Friend | 阿杰 (A-Jie), online gaming friend, claims to know about "hackers" |
| Items affected | Several rare items traded away from the account after the 03:47 login |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| Sat 14:00 | Wang Ming goes to 极速网咖 with Li Hao to play 《无尽深渊》. He logs into his account on PC #23. | Wang Ming logged in normally. The internet cafe assigns each PC a local network IP that maps to the cafe's public IP (183.221.67.45). Wang Ming played from 14:00 to 17:30. | Wang Ming and Li Hao know they were at the cafe. |
| Sat 17:30 | Wang Ming and Li Hao leave the internet cafe. Wang Ming FORGETS to log out of 《无尽深渊》. | The game client remained logged in on PC #23. The cafe's PC management system should auto-restart PCs after a user session ends, but PC #23 has a known bug: its session timer is misconfigured and does not trigger auto-restart. The cafe staff were supposed to manually check but missed PC #23. | Wang Ming does not realize he forgot to log out. The cafe has a system bug they may not be aware of. |
| Sat 22:00 | Another customer sits at PC #23 (the internet cafe is open 24 hours). This person sees the game is still logged in to Wang Ming's account. | The new customer (unknown, never identified) accesses Wang Ming's account because it was already logged in. They browse the inventory and trade several rare items to another account. This is opportunistic, not targeted hacking. | The unknown customer knows they found a logged-in account. |
| Sun 03:47 | The game login log shows a "new session" from IP 183.221.67.45 at 03:47 AM. This is actually a session refresh (the game server refreshes long-running sessions every ~12 hours), not a new login. | The 03:47 entry in the login log looks like a new login but is actually a session refresh. The IP (183.221.67.45) is the internet cafe's public IP, same as Wang Ming's Saturday session. The session never actually ended -- it has been continuous since Saturday 14:00. | The game's login log does not distinguish between "new login" and "session refresh" -- both appear the same way. |
| Sun 08:00 | Wang Ming wakes up and tries to log in from his dorm. He gets an error: "Account already logged in elsewhere." He force-disconnects the other session and logs in. | Wang Ming discovers his account was active from somewhere else. He checks his inventory and finds several rare items missing (traded to unknown accounts). He panics. | Wang Ming knows his account was compromised. He does not yet know how. |
| Sun 09:00 | Wang Ming contacts his friend 阿杰 (A-Jie), who is more experienced with gaming and internet security. Ajie examines the login log and says: "That IP doesn't match any of your usual locations. Looks like you got hacked. Probably a keylogger or a database leak." | Ajie's analysis is WRONG. He sees an unfamiliar IP (183.221.67.45) and immediately assumes "hacker." He does not know that 183.221.67.45 is the internet cafe's IP. Ajie does not consider the simple explanation (forgot to log out) because he is biased toward dramatic "hacker" explanations. His suggestion of "keylogger" and "database leak" are both incorrect. | Ajie believes it's a hack. Wang Ming is influenced by Ajie's confident analysis. |
| Sun 10:00 | Wang Ming submits a customer service ticket to the game company (无尽科技, Endless Tech). Title: "Account hacked -- items stolen." He describes the unknown IP login and missing items. | The customer service system generates an auto-reply: "Your ticket has been received. Our account security team is reviewing your case. Please allow 3-5 business days." | Wang Ming believes his case is being reviewed. |
| Sun 14:00 (Update 1 trigger) | Wang Ming checks the game's login history more carefully. He notices the "unknown" IP 183.221.67.45 is the SAME IP as his Saturday afternoon session at the internet cafe. | The IP address match is the key evidence. The "unknown" IP is not unknown at all -- it's the cafe where Wang Ming himself played. This strongly suggests the account was accessed FROM the same cafe, not by a remote hacker. | Wang Ming now sees the IP match but is not sure what it means. He asks Ajie, who says "hackers can spoof IPs." |
| Sun 18:00 | Wang Ming finds his 极速网咖 receipt showing the date, time, and PC number (PC #23). | The receipt confirms Wang Ming was at the cafe on Saturday 14:00-17:30 and used PC #23. The IP from the cafe matches the "suspicious" login IP. The timeline becomes clear: Wang Ming's session on PC #23 never ended. | Wang Ming has the receipt but Ajie still insists it could be IP spoofing. |
| Mon 10:00 (Update 2 trigger) | Li Hao confirms: "Yeah, you were in a rush to leave. I remember you didn't close the game. I told you to log out but you said 'it'll auto-disconnect.' But those cafe PCs sometimes don't restart properly." | Li Hao's testimony corroborates the "forgot to log out" explanation. He witnessed Wang Ming leaving without logging out. This is independent confirmation. | Li Hao remembers the logout failure. |
| Mon 14:00 (Update 3 trigger) | Wang Ming checks his customer service ticket status. The ticket still shows "Under Review" but he calls the game company's hotline and speaks to a representative. The representative says: "I can see your ticket in the system. It is in queue but has not been assigned to a security analyst yet. Our current backlog is approximately 7-10 business days." The "account security team reviewing" auto-reply was misleading -- no one has looked at the case yet. | The customer service auto-reply saying "our account security team is reviewing your case" was a template response. The ticket has NOT been reviewed. It is sitting in a queue. The "3-5 business days" timeline was also misleading -- the actual backlog is 7-10 days. C4 is now clear: CS said "reviewing" when no review was actually initiated. | Wang Ming now knows CS was giving template responses, not actually reviewing his case. |
| Tue 10:00 (Update 4 trigger) | The password change log is reviewed. It shows: (1) Wang Ming changed his password on Sun 08:15 (after discovering the breach). (2) NO password change occurred before or during the suspicious session. The account was accessed WITHOUT any password change -- because it was already logged in. | The password change log is NON-CONFLICTING with all other evidence: C3 confirmed. No password was changed by the "attacker" because there was no attack -- the session was simply still active from Wang Ming's cafe visit. Wang Ming changed his own password after discovering the issue, which is the only password change in the log. | C3 (NON-CONFLICT): Password change timeline is consistent -- no unauthorized password changes, Wang Ming's own change at 08:15 is the only entry. |

---

## 4. Role-Level Truth vs Self-Narrative

### Wang Ming (王明) -- Protagonist

- **Objective position:** Wang Ming forgot to log out of his game at the internet cafe. Someone else at the cafe found the logged-in account and traded away his items. This is carelessness, not a targeted hack.
- **Public narrative:** Initially: "I got hacked!" Later, as evidence accumulates: "Wait... did I forget to log out?"
- **Private narrative:** Embarrassed that the "hack" was his own mistake. Does not want to admit to friends that he forgot to log out.
- **Trust bias:** Trusts friends (especially Ajie) more than his own investigation. Initially swayed by Ajie's dramatic "hacker" theory.

### 阿杰 (A-Jie) -- Online Gaming Friend

- **Objective position:** Ajie is wrong about everything. He sees an unfamiliar IP and jumps to "hacker." He suggests keylogger and database leak with no evidence. He dismisses the IP match as "IP spoofing" because he is committed to his dramatic theory. He is not malicious -- he is genuinely trying to help but is overconfident in his limited knowledge.
- **Public narrative:** "Bro you definitely got hacked. I've seen this before."
- **Private narrative:** Ajie wants to be seen as the knowledgeable tech friend. Admitting the simple explanation would undermine his expertise narrative.
- **Why the gap exists:** Ajie has surface knowledge of cybersecurity (knows terms like "keylogger," "IP spoof," "database leak") but does not have the analytical skills to evaluate evidence systematically.

### Li Hao (李浩) -- Best Friend (was at the cafe)

- **Objective position:** Li Hao was with Wang Ming at the cafe and remembers him leaving without logging out. His testimony is simple, direct, and corroborates the true explanation. He is a reliable witness.
- **Why reliable:** Li Hao has no stake in the outcome and directly observed the relevant event.

### Customer Service (客服)

- **Objective position:** The CS auto-reply was a template that misrepresents the actual status. "Account security team is reviewing" was false -- the ticket was in an unprocessed queue. The hotline representative was honest about the 7-10 day backlog.
- **Why the gap exists:** Standard customer service practice of sending reassuring auto-replies regardless of actual processing status.

---

## 5. Contradiction Map

| ID | Contradiction | Source A | Source B | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Login from "unknown" IP vs IP traces to internet cafe Wang Ming visited | game-login-history.md: "2026-03-22 03:47 -- IP 183.221.67.45 -- Login (new session)" Wang Ming: "I don't recognize this IP." Ajie: "That's a hacker IP." | ip-address-log.md: IP 183.221.67.45 geo-traces to "极速网咖, 成都市成华区." internet-cafe-receipt.md: Wang Ming at 极速网咖 on 03-21 14:00-17:30. game-login-history.md: "2026-03-21 14:02 -- IP 183.221.67.45 -- Login" (Wang Ming's own session, same IP). | The "unknown" IP is the internet cafe where Wang Ming played on Saturday. The 03:47 Sunday entry is a session refresh from the same location, not a new login from a hacker. Wang Ming's own Saturday session used the same IP. | R2 (login log visible) | **Yes: R2-->R5** (IP geo-trace + cafe receipt confirm match; Ajie's "hacker" theory debunked) |
| C2 | Ajie suggests "hacker" (keylogger/database leak) vs simple explanation (forgot to logout) | Ajie IM session: "这个IP不是你的，肯定被黑了。可能是键盘记录器或者数据库泄露。" (This IP isn't yours, definitely hacked. Probably keylogger or database leak.) | ip-address-log.md: IP matches cafe. internet-cafe-receipt.md: Wang Ming was at that cafe. Li Hao IM (Update 2): "你走的时候没关游戏，我还提醒你来着。" (You didn't close the game when you left, I even reminded you.) | Ajie's theory requires: (1) a keylogger on Wang Ming's device (no evidence), (2) a database breach (no public reports), or (3) IP spoofing (unnecessarily complex for in-game item theft). The simple explanation: Wang Ming forgot to log out. Li Hao witnessed it. The IP matches the cafe. | R3 (Ajie's theory visible) | **Yes: R3-->R7** (Li Hao's testimony + IP match + no password change = forgot to logout) |
| C3 | Password change timeline (NON-CONFLICT -- consistent, confirms no hack) | password-change-log.md: Only entry: "2026-03-22 08:15 -- Password changed by account holder (from dorm IP 222.18.x.x)." No other password changes. | game-login-history.md: No new login with new credentials during the suspicious session. The session was continuous from Saturday. | The password change log confirms: no unauthorized password changes occurred. The "attacker" did not need to change the password because the session was already logged in. Wang Ming changed his own password Sunday morning (damage control). All sources agree on this timeline. | R1 onwards | **None** |
| C4 | CS says "account security team reviewing" vs no review actually initiated | customer-service-ticket.md: Auto-reply: "Your ticket has been received. Our account security team is reviewing your case. Please allow 3-5 business days." | CS hotline response (Update 3): "Your ticket is in queue but has not been assigned to a security analyst yet. Current backlog is approximately 7-10 business days." | The auto-reply was a template. No review was initiated. "3-5 business days" was also misleading (actual backlog: 7-10 days). The CS system provides reassuring language regardless of actual processing status. | R4 (ticket visible) | **Yes: R4-->R9** (Hotline call reveals no review initiated; template response exposed) |

---

## 6. Agent Historical Bias Design (2 biases)

### B1: Wang Ming-Ajie IM -- Agent defers to Ajie's "hacker" theory

- **Session and Loop:** Wang Ming-Ajie IM, Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "Ajie's analysis that the unfamiliar IP indicates a targeted hack is consistent with common attack patterns such as keyloggers or credential database leaks, and his experience with gaming security issues lends credibility to this assessment."
- **Why the agent is misled:** Ajie speaks with confidence and uses real cybersecurity terminology. The agent defers to his apparent domain expertise without independently verifying the IP or considering simpler explanations.
- **Reversal trigger:** Update 1: IP geo-traces to the internet cafe. Update 2: Li Hao confirms Wang Ming forgot to log out.
- **Affected eval rounds:** R5 (bias visible), R7 (full reversal)

### B2: Main session -- Agent trusts the CS "reviewing" claim

- **Session and Loop:** Main session, after ticket submission but before Update 3
- **Exact phrase that must appear in session:**
  > "The customer service confirmation that the account security team is actively reviewing the case provides some assurance that the issue will be investigated through official channels within the stated 3-5 business day timeline."
- **Why the agent is misled:** The CS auto-reply uses authoritative language ("account security team," "reviewing"). The agent takes institutional communications at face value.
- **Reversal trigger:** Update 3: Hotline call reveals the ticket is unprocessed and backlog is 7-10 days.
- **Affected eval rounds:** R6 (bias visible), R9 (full reversal)

---

## 7. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (unknown IP partial) | B1 seed | R2 | No | Shallow agents will accept the "unknown IP" framing without cross-referencing with Wang Ming's own login history (which shows the SAME IP from Saturday). |
| T2 | C1 (IP match revealed) | B1 | R2-->R5 | **Yes** | After Update 1, the IP is identified as the internet cafe. The "unknown" IP was Wang Ming's own session location. Agents must revise from "hacker" to "same cafe." |
| T3 | C2 (Ajie vs simple explanation) | B1 | R3-->R7 | **Yes** | Ajie's theory requires complex attack vectors; the evidence supports a simple explanation. Li Hao's testimony + IP match + no password change = forgot to logout. |
| T4 | C3 (password timeline) | -- | R1+ | No | The password log shows NO unauthorized changes. This is inconsistent with a hacking theory (hackers typically change passwords). Agents must note this absence as evidence against the hacking theory. |
| T5 | C4 (CS reviewing) | B2 | R4-->R9 | **Yes** | The CS "reviewing" message is a template. No review was initiated. Agents must distinguish between institutional reassurance and actual action. |
| T6 | Comprehensive | B1, B2 | R21-R30 | Full | Wang Ming forgot to log out. No hack. No security team review. Ajie was wrong. The resolution is simple and embarrassing, not dramatic and technical. |

---

## 8. Writer Constraints

1. **Only contradictions C1--C4.** No additional security incidents.
2. **Bias B1 and B2 exact phrases** must appear verbatim.
3. **Each contradiction has traces in at least two sources.**
4. **Timestamps consistent:** Sat 14:00 cafe login. Sat 17:30 leave cafe. Sun 03:47 session refresh. Sun 08:00 discovery. Sun 08:15 password change. Sun 09:00 contacts Ajie. Sun 10:00 CS ticket. Mon-Tue updates.
5. **Wang Ming P1-P5:** Concise lists, casual naming, answer first, use examples, casual/internet slang OK.
6. **Chinese session messages.** Casual student/gamer language. Include gaming jargon.
7. **Ajie must sound knowledgeable but be wrong.** Uses real cybersecurity terms incorrectly applied. Confidently wrong.
8. **C3 (password timeline) is NON-CONFLICT.** All sources agree: no unauthorized password changes.
9. **The cafe receipt must show IP or location info** that matches the "unknown" IP.
10. **Noise topics:** game strategies, other friends' gaming setups, guild drama, memes, campus life.
11. **exec_check 20-40% of rounds.**
