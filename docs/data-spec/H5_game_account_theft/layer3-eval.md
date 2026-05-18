# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many.
> ~30 rounds. exec_check 20-40%.

---

## 1. Round Inventory

| Round | Tags | Main Skill | Update? | Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | Password change timeline (C3 non-conflict) + tool use | No | No |
| r2 | MS-I | Login log IP analysis -- same IP appears twice (C1 partial) | No | Yes (R2->R5) |
| r3 | MS-R | Ajie's hacker theory evaluation (C2 partial) | No | Yes (R3->R7) |
| r4 | P-R | Wang Ming's preferences | No | No |
| r5 | DU-R | Reassess C1 after IP-to-cafe confirmation (IP match definitive) | Yes (U1) | Yes (R2->R5) |
| r6 | MS-I, exec_check | CS ticket status analysis -- auto-reply vs actual status fields (C4 partial) | No | Yes (R6->R9) |
| r7 | DU-R | Reassess C2 after Li Hao's witness statement (forgot to logout confirmed) | Yes (U2) | Yes (R3->R7) |
| r8 | DU-I | Full incident reconstruction after U1+U2 | Yes (U1+U2) | Yes (B1 reversal) |
| r9 | DU-R, exec_check | Reassess C4 after hotline transcript (no review initiated) | Yes (U3) | Yes (R6->R9) |
| r10 | MD-R | Evidence hierarchy -- system logs vs friend advice vs CS claims | No | No |
| r11 | DU-I | Integrate hotline revelation (template vs reality) | Yes (U3) | No |
| r12 | DP-I, exec_check | Identify B1 (Ajie deference) and what corrected it | Yes (U1+U2) | No |
| r13 | MS-R | Session refresh vs new login distinction | No | No |
| r14 | MD-R, exec_check | Ajie's credibility -- where he's right vs wrong | No | No |
| r15 | MS-I | What evidence rules out a real hack? | No | No |
| r16 | P-I | Explain the incident to Ajie in casual terms | Yes (U2) | No |
| r17 | DU-I, exec_check | Integrate cafe PC management log (U4) | Yes (U4) | No |
| r18 | MD-I | Why Ajie was wrong -- confidence vs competence | Yes (U1+U2) | No |
| r19 | MP-I | Wang Ming, Ajie, Li Hao, CS perspectives analyzed | Yes (all) | No |
| r20 | P-R | Preference compliance | No | No |
| r21 | MDP-I, exec_check | Comprehensive: not a hack, forgot to logout, CS template | Yes (all) | Comprehensive |
| r22 | MS-R | C3 non-conflict -- password timeline consistent | No | No |
| r23 | DU-R | B2 identification -- CS trust and correction | Yes (U3) | No |
| r24 | MS-I, exec_check | IP address analysis -- cafe IP in both sessions | No | No |
| r25 | P-I | Write an incident summary for Wang Ming's reference | Yes (all) | No |
| r26 | MD-I | What should Wang Ming do next -- practical recommendations | Yes (all) | No |
| r27 | DP-I, exec_check | Occam's Razor application -- simplest explanation test | Yes (U1+U2) | No |
| r28 | MP-I | Lessons learned for all parties | Yes (all) | No |
| r29 | MS-I | How to prevent this in the future | No | No |
| r30 | MDP-I | Final comprehensive -- all evidence synthesized | Yes (all) | Comprehensive |

**exec_check:** R1, R6, R9, R12, R14, R17, R21, R24, R27 = 9/30 = 30%

---

## 2. Key Round Specs

### R1: Password Timeline (MS-R, exec_check) -- Calibration

**exec_check:** Must read password-change-log.md.

**Question:**
> "Based on the password change log, which statements are supported?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | The only password change in 2026 was on March 22 at 08:15, made by Wang Ming from his campus IP. | YES | password-change-log.md |
| B | No password change occurred during the suspicious session (March 21 14:02 to March 22 08:03). | YES | password-change-log.md (absence) |
| C | The absence of a password change during the suspicious session is inconsistent with a targeted hack, since hackers typically change passwords to maintain access. | YES | Logical inference |
| D | A password change was made from IP 183.221.67.45 during the suspicious session. | NO | No such entry exists |
| E | The suspicious session accessed the account without entering a password (the session was already logged in). | YES | Inference from no new auth event |
| F | Wang Ming changed his password on March 22 as a damage-control measure after discovering the breach. | YES | Timestamp 08:15 aligns with 08:00 discovery |
| G | The password change log shows the hacker changed the password and locked Wang Ming out. | NO | No unauthorized password change |
| H | The password change log is consistent with all other evidence -- no hack, session was already active. | YES | C3 non-conflict |

**answer:** `["A", "B", "C", "E", "F", "H"]`

---

### R2: Login Log IP Analysis (MS-I) -- Calibration

**Question:**
> "Based on the login history, which statements about the IP addresses are supported?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | Wang Ming's normal dorm IP is 222.18.135.67 (UESTC campus network). | YES | game-login-history.md |
| B | The "suspicious" login at 03:47 on March 22 used IP 183.221.67.45. | YES | game-login-history.md |
| C | The SAME IP (183.221.67.45) was used for Wang Ming's own login on March 21 at 14:02. | YES | game-login-history.md (key finding) |
| D | The IP geolocation for 183.221.67.45 points to the Chenghua District area near campus, commonly used by internet cafes. | YES | ip-address-log.md |
| E | The fact that the same IP appears for both Wang Ming's Saturday session and the Sunday 03:47 session strongly suggests both sessions originated from the same physical location. | YES | Logical inference |
| F | The IP 183.221.67.45 has been flagged as a known hacker IP in security databases. | NO | No such evidence |
| G | Wang Ming's login log shows no logout record between the March 21 14:02 login and the March 22 03:47 entry, suggesting the session was continuous. | YES | game-login-history.md (no logout between entries) |
| H | The 03:47 entry is a new login requiring password authentication. | NO | More likely a session refresh; no password change occurred |

**answer:** `["A", "B", "C", "D", "E", "G"]`

---

### R6: CS Ticket Analysis (MS-I, exec_check)

**exec_check:** Must read customer-service-ticket.md.

**Question:**
> "Based on the customer service ticket, which statements are supported?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | The auto-reply states "our account security team is reviewing your case." | YES | customer-service-ticket.md |
| B | The ticket status field shows "Pending" (待处理), not "In Review" or "Assigned." | YES | customer-service-ticket.md |
| C | The ticket assignment field shows "Unassigned" (未分配). | YES | customer-service-ticket.md |
| D | There is a contradiction between the auto-reply ("security team is reviewing") and the status fields ("Pending," "Unassigned"). | YES | Cross-field comparison |
| E | The auto-reply's "3-5 business days" timeline should be treated as an accurate estimate. | NO | Contradicted by hotline later (7-10 days) |
| F | The auto-reply language is likely a template sent for all account security tickets, regardless of actual processing status. | YES | Inference from template language + status fields |
| G | A security analyst has been assigned and has begun reviewing the login logs. | NO | Status shows "Unassigned" |
| H | The ticket system shows that Wang Ming provided additional information about the cafe IP on Monday, which was acknowledged by another template response. | YES | CS IM session context |

**answer:** `["A", "B", "C", "D", "F", "H"]`

---

### R8: Full Incident Reconstruction (DU-I)

**Question:**
> "After Updates 1 and 2 (IP confirmed as cafe, Li Hao confirms logout failure), which statements represent the most accurate reconstruction?"

| Option | Content | Correct? |
|---|---|---|
| A | Wang Ming logged into his game at the internet cafe (PC #23) on Saturday at 14:02 and left at 17:30 without logging out. | YES |
| B | The game session persisted on PC #23 because the cafe's auto-restart feature failed or was not configured for that PC. | YES |
| C | Another customer accessed the already-logged-in account later on Saturday evening and traded away rare items. | YES |
| D | The 03:47 Sunday entry is a server-side session refresh, not a new login -- the session was continuous since Saturday. | YES |
| E | Ajie's theories (keylogger, database leak, IP spoofing) are all contradicted by the evidence. | YES |
| F | The "attacker" needed Wang Ming's password to access the account. | NO |
| G | Li Hao confirms he warned Wang Ming to log out, but Wang Ming assumed auto-disconnect would handle it. | YES |
| H | This was a targeted attack by someone who knew Wang Ming's gaming habits. | NO |

**answer:** `["A", "B", "C", "D", "E", "G"]`

---

### R21: Comprehensive Resolution (MDP-I, exec_check)

**Question:**
> "Integrating all evidence across all updates, which statements represent the complete and accurate assessment?"

Key correct: Not a hack; forgot to logout at cafe; PC #23 auto-restart was broken; session persisted; opportunistic access by unknown person; Ajie was wrong on all counts; CS "reviewing" was a template lie; actual review timeline is 7-10 days; password log confirms no unauthorized changes; IP match is definitive; Li Hao is a credible witness.

Key distractors: Targeted hack by sophisticated attacker; Ajie's keylogger theory was partially correct; CS team has already started reviewing.

---

## 3. R9-R30 Abbreviated Specs

Each round follows the standard multi-choice format with 8-10 options, 3-5 correct, specific evidence sources, and carefully designed distractors. Key rounds test:
- R9: CS template exposure
- R12: B1 bias identification (Ajie deference)
- R14: Ajie credibility analysis
- R17: PC management log (auto-restart bug)
- R23: B2 bias identification (CS trust)
- R27: Occam's Razor application
- R30: Final synthesis
