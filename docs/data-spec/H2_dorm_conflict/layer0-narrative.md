# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_h2` |
| Domain | Campus Life / Logical Reasoning |
| Time span | 1 week |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Wang Ming (王明), 17, freshman at UESTC (电子科技大学), Computer Science major |
| One-sentence | Wang Ming's roommate's money goes missing and the roommate suspects him -- dorm access logs, canteen payment records, package pickup logs, and campus CCTV each tell a different part of the story, and the real answer involves a misdelivered package, not theft. |

---

## 2. Case Profile (Background Object)

| Field | Value |
|---|---|
| Roommate | Liu Chen (刘晨), 18, CS freshman, Wang Ming's roommate in Dorm 7-312 |
| Missing amount (claimed) | ¥500 cash |
| Missing amount (actual) | ¥200 cash |
| Date of incident | 2026-03-20 (Friday) |
| Dorm room | 7号楼312室 (Building 7, Room 312), 4-person room |
| Other roommates | Ma Qiang (马强), Xu Hao (许浩) -- both away during the incident window |
| Key evidence | Dorm access log, canteen payment timestamps, package pickup log, campus CCTV summary |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| Fri 09:00 | Liu Chen leaves ¥200 in cash in his desk drawer and goes to class. He later claims it was ¥500. | Liu Chen actually had ¥200. He remembers putting in ¥300 last week but already spent ¥100 at the campus bookstore (receipt exists but he forgot). He genuinely believes it was ¥500 because he conflates two different cash deposits. | Liu Chen believes ¥500. Wang Ming does not know about the cash. Ma Qiang and Xu Hao are both away (Ma Qiang at basketball practice, Xu Hao visiting family off-campus since Thursday). |
| Fri 10:15 | Dorm access log shows Wang Ming's student card swiped at Building 7 entrance at 10:15. | Wang Ming returned to the dorm to pick up his charger, which he forgot. He was in the room for approximately 10 minutes (10:15 to ~10:25). During this time he did NOT open Liu Chen's desk drawer or take any money. He grabbed his charger from his own desk and left. | Wang Ming knows he was in the room briefly. The access log records his entry. There is no exit swipe (the system only logs entry, not exit). |
| Fri 10:20 | Canteen payment system shows Wang Ming paid ¥12 for a snack at the canteen at 10:20. | This is IMPOSSIBLE if Wang Ming was in the dorm at 10:15 and the canteen is a 10-minute walk away. **The explanation:** Wang Ming's student card was used at the canteen, but by his friend Li Hao (李浩), who borrowed the card earlier that morning to buy breakfast (Wang Ming's canteen balance had a meal plan discount). Li Hao forgot to return the card until later. Wang Ming entered the dorm using the physical door (another roommate held it open when leaving; the log shows his card swipe at 10:15 was for picking up the card Li Hao returned at the building entrance, not for entering). **CORRECTION on timeline:** Actually, the simpler explanation: Wang Ming swiped in at 10:15 and the canteen payment at 10:20 is from Li Hao using a DIFFERENT card (Li Hao's own card is under Wang Ming's account because Wang Ming loaded Li Hao's card with meal plan credit). **SIMPLEST VERSION:** Wang Ming swiped into the dorm at 10:15. At 10:20, a canteen payment of ¥12 appears on Wang Ming's student ID. This seems contradictory (can't be in dorm AND canteen at same time). The truth: Li Hao borrowed Wang Ming's student card for the canteen that morning. Wang Ming entered the dorm using the physical key (door was unlocked; Ma Qiang left for practice without locking). The 10:15 swipe is actually Li Hao returning the card at the building entrance. So Wang Ming was actually in the dorm (entered through the unlocked door earlier, around 10:00), and the 10:15 swipe + 10:20 canteen payment are both Li Hao using the card. | Wang Ming knows Li Hao had his card. Li Hao knows he used the card. Liu Chen only sees the access log and assumes it was Wang Ming entering the dorm. |
| Fri 10:30 | Package pickup log shows someone picked up a package addressed to Liu Chen from the campus pickup station using the pickup code. | The package was picked up by Zhang Wei (张伟, not the HR VP -- a different student), who is in Room 314 (same floor). Zhang Wei's pickup code was adjacent to Liu Chen's (code 7-312-0320 vs 7-314-0320) and he grabbed the wrong package by mistake. Zhang Wei later returned the package when he realized the error (Saturday morning). This is a red herring that initially makes Wang Ming look suspicious (package picked up during the same time window). | The pickup station logs show the code was used but do not log WHO picked it up -- only that the code was entered. |
| Fri 11:00 | Liu Chen returns to the dorm and discovers the cash is missing from his drawer. He also notices his expected package is not at the pickup station. | Liu Chen finds the drawer disturbed (he thinks) and the cash gone. He checks the package station and his package is not there. He starts suspecting someone entered the room. | Liu Chen believes ¥500 is missing and his package was taken. |
| Fri 12:00 | Liu Chen checks the dorm access log (posted on the floor bulletin board) and sees Wang Ming's card was swiped at 10:15. He confronts Wang Ming. | Liu Chen sees Wang Ming's card at 10:15 and concludes Wang Ming was in the room during the time the money could have been taken. Wang Ming says "I wasn't in the room at 10:15, Li Hao had my card." This sounds like an excuse. | Liu Chen suspects Wang Ming. Wang Ming knows Li Hao had the card but cannot prove it immediately. |
| Fri 14:00 (Update 1 trigger) | Wang Ming asks Li Hao to confirm. Li Hao confirms he had Wang Ming's card until ~10:30 and used it at the canteen at 10:20 and swiped at the building entrance at 10:15 to return something to Wang Ming's room (Li Hao entered building 7 to return a textbook to another friend on floor 2). | Li Hao's account explains both the 10:15 building swipe and the 10:20 canteen payment. The 10:15 swipe was Li Hao entering Building 7, not Wang Ming. Li Hao did NOT go to Room 312 -- he went to Room 208 to return a textbook. Wang Ming was in the room earlier (entered around 10:00 through the unlocked door). | C1 resolved: the dorm access log shows Li Hao using Wang Ming's card, not Wang Ming entering. But Wang Ming WAS in the room around 10:00 (entered through unlocked door). |
| Fri 15:00 | Campus CCTV summary is requested by the dorm RA (辅导员). CCTV at Building 7 entrance shows: 10:14 a person matching Li Hao's description enters; 10:00 a person matching Wang Ming's description enters (no card swipe -- door was propped open by departing student). | CCTV confirms: Wang Ming entered at ~10:00 without swiping (door held open); Li Hao entered at ~10:14 and swiped at 10:15. This is CONSISTENT with the access log and canteen payment. **C3 NON-CONFLICT: CCTV aligns with all other timestamps.** | The RA now has CCTV evidence. Wang Ming's entry at 10:00 is confirmed but he had a valid reason (charger). |
| Sat 09:00 (Update 2 trigger) | The package pickup log is investigated. The station manager confirms that code 7-312-0320 (Liu Chen's package) was entered at 10:30 Friday, but cross-referencing with the station's own camera shows the person who entered the code was from Room 314, not 312. Zhang Wei (314) picked up the wrong package. | The package mystery is solved: Zhang Wei from 314 took Liu Chen's package by mistake (adjacent codes). Zhang Wei returns the package Saturday morning with an apology. This eliminates the "package theft" suspicion. | C2 resolved: the package was a mistaken pickup, not theft. |
| Sat 14:00 (Update 3 trigger) | Liu Chen finds a campus bookstore receipt in his jacket pocket dated 2026-03-17 for ¥100. He realizes he bought textbook supplies and forgot. His actual cash was ¥200 (¥300 deposited minus ¥100 spent), not ¥500. | Liu Chen's ¥500 claim is corrected to ¥200. But the ¥200 is still missing. Further investigation: the dorm RA discovers that the cleaning staff (保洁阿姨) reported finding ¥200 in loose bills on the hallway floor outside Room 312 on Friday morning. Liu Chen likely did not close his drawer properly and the bills fell out when the door drafts. | C4 approaching resolution: the amount was ¥200, not ¥500, and the money was found by cleaning staff (turned in to lost-and-found). |
| Sun 10:00 (Update 4 trigger) | The RA confirms: campus lost-and-found has ¥200 cash turned in by cleaning staff from the 3rd floor of Building 7 on Friday morning at ~10:45. The cleaning staff cleans the hallway between 10:30-11:00 daily. | The ¥200 was found on the hallway floor by cleaning staff. Most likely explanation: Liu Chen's drawer was not fully closed; the draft from the opening/closing of the dorm door (when Wang Ming entered at ~10:00 and left at ~10:10) displaced the loose bills. Wang Ming did not take the money -- his brief entry caused an air draft that blew unsecured bills out of a partially open drawer. | Complete resolution: No theft. Money fell out due to unsecured drawer + door draft. Package was mistaken pickup. Wang Ming is cleared. |

---

## 4. Role-Level Truth vs Self-Narrative

### Wang Ming (王明) -- Protagonist

- **Objective position:** Wang Ming entered the dorm at ~10:00 through the unlocked door to grab his charger. He left at ~10:10. He did NOT take any money. His student card was with Li Hao, who used it at the building entrance (10:15) and canteen (10:20). Wang Ming looks suspicious because of the access log timing but is innocent.
- **Public narrative:** "I didn't take anything. Li Hao had my card."
- **Private narrative:** Anxious about being accused. Worried that his alibi (Li Hao had the card) sounds like a convenient excuse. Wants to clear his name.
- **Trust bias:** Trusts friends' word over systematic evidence; tends to be swayed by group emotions.

### Liu Chen (刘晨) -- Roommate / Accuser

- **Objective position:** Liu Chen believes ¥500 is missing (actually ¥200). He sees the access log showing Wang Ming's card at 10:15, knows the other roommates were away, and concludes Wang Ming is the likely suspect. He is not malicious -- he genuinely believes he has been robbed. He exaggerates the amount unintentionally (conflating two cash deposits).
- **Public narrative:** "My ¥500 is gone. Wang Ming's card shows he was in the room."
- **Private narrative:** Genuinely upset about the missing money. Not trying to frame Wang Ming but jumping to conclusions.

### Li Hao (李浩) -- Wang Ming's Best Friend

- **Objective position:** Li Hao borrowed Wang Ming's student card Friday morning for the canteen discount. He swiped at Building 7 entrance at 10:15 (to return a textbook to Room 208). He used the card at the canteen at 10:20. He returned the card to Wang Ming at lunch. His testimony clears Wang Ming of the access log evidence.
- **Why reliable:** Li Hao has no involvement in the missing money. His account is corroborated by CCTV and canteen payment timestamps.

### Zhang Wei (张伟) -- Room 314 Student

- **Objective position:** Zhang Wei accidentally picked up Liu Chen's package using an adjacent pickup code. He returned it Saturday morning. He has no connection to the missing money.

---

## 5. Contradiction Map

| ID | Contradiction | Source A | Source B | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Dorm access log shows Wang Ming (card) at 10:15 vs canteen payment at 10:20 (impossible to be both places) | dorm-access-log.md: "Student ID WM-2026-CS-0042 swiped Building 7 entrance 10:15:23" | canteen-payment-log.md: "Student ID WM-2026-CS-0042, ¥12.00, Canteen #2, 10:20:15" | Li Hao had Wang Ming's card. The 10:15 swipe and 10:20 canteen payment were both Li Hao. Wang Ming entered through the unlocked door at ~10:00 without swiping. | R2 (both logs visible) | **Yes: R2-->R5** (Li Hao's confirmation resolves the impossibility) |
| C2 | Package pickup log shows Liu Chen's package picked up at 10:30 vs no one from 312 was at the station | package-pickup-log.md: "Code 7-312-0320 used at 10:30:45, package released" | dorm-access-log.md + canteen-payment-log.md: No 312 resident was at the pickup station at 10:30 (Wang Ming in dorm, Liu Chen in class, others away) | Zhang Wei from Room 314 used an adjacent code by mistake. Pickup station cameras (Update 2) confirm it was someone from 314, not 312. | R3 (pickup log visible) | **Yes: R3-->R7** (Station camera evidence confirms mistaken pickup) |
| C3 | Campus CCTV timeline (NON-CONFLICT -- consistent with all other sources) | dorm-cctv-summary.md: "10:00 male matching Wang Ming enters Building 7 (no card swipe, door held open); 10:14 male matching Li Hao enters Building 7 (card swipe 10:15)" | dorm-access-log.md + canteen-payment-log.md: Card swipe at 10:15 + canteen at 10:20 | CCTV confirms all timestamps. Wang Ming entered at 10:00 without card. Li Hao entered at 10:14-10:15 with Wang Ming's card. No contradictions in timing. | R1 onwards | **None** |
| C4 | Liu Chen claims ¥500 missing vs actual amount was ¥200 | Liu Chen IM (session): "我的500块不见了！" (My ¥500 is gone!) | campus-lost-found.md (Update 3/4): Cleaning staff found ¥200 on 3rd floor hallway. Liu Chen finds ¥100 bookstore receipt (Update 3). | Liu Chen deposited ¥300 last week, spent ¥100 at bookstore (forgot), actual remaining was ¥200. The ¥200 fell out of his partially open drawer when Wang Ming opened/closed the door at ~10:00. Found by cleaning staff at 10:45. | R4 (claim visible) | **Yes: R4-->R9** (bookstore receipt + lost-and-found discovery corrects amount and resolves "theft") |

---

## 6. Agent Historical Bias Design (2 biases)

### B1: Wang Ming-Roommate IM -- Agent treats the access log as strong evidence of Wang Ming's presence

- **Session and Loop:** Wang Ming-Liu Chen IM, Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "The dorm access log showing Wang Ming's student card at 10:15 is a system-generated record that places him at the scene during the time window when the money could have gone missing, and this is the strongest piece of evidence currently available."
- **Why the agent is misled:** System-generated logs seem authoritative. The agent does not consider that the card could have been used by someone else.
- **Reversal trigger:** Update 1: Li Hao confirms he had the card. CCTV shows Li Hao at Building 7 entrance, not Wang Ming.
- **Affected eval rounds:** R5 (bias visible), R8 (full reversal)

### B2: Main session -- Agent accepts Liu Chen's ¥500 claim without questioning the amount

- **Session and Loop:** Main session, before Update 3
- **Exact phrase that must appear in session:**
  > "Liu Chen reports ¥500 missing from his desk drawer, and since he is the one who placed the money there, his account of the amount should be treated as reliable unless contradicted by other evidence."
- **Why the agent is misled:** The victim's stated amount seems like a basic fact that would not need verification. The agent does not consider memory errors about cash amounts.
- **Reversal trigger:** Update 3: bookstore receipt shows ¥100 was spent earlier. Actual amount was ¥200.
- **Affected eval rounds:** R7 (bias visible), R9 (full reversal)

---

## 7. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (access log vs canteen) | B1 seed | R2 | No | Shallow agents will not notice the physical impossibility of being at the dorm (10:15) and canteen (10:20) simultaneously with a 10-min walk between them. |
| T2 | C1 (resolved) | B1 | R2-->R5 | **Yes** | Li Hao had the card. The access log does not prove Wang Ming entered at 10:15. CCTV shows Wang Ming entered at 10:00 without swiping. |
| T3 | C2 (package pickup) | -- | R3 | No | The package pickup at 10:30 looks suspicious but is unrelated to the money. |
| T4 | C2 (resolved) | -- | R3-->R7 | **Yes** | Zhang Wei from 314 grabbed the wrong package. This is completely unrelated to the missing money. |
| T5 | C3 (CCTV non-conflict) | -- | R1+ | No | All CCTV timestamps must be synthesized with other logs. They are consistent. |
| T6 | C4 (amount claimed) | B2 | R4 | No | The ¥500 claim is accepted at face value. |
| T7 | C4 (amount corrected) | B2 | R4-->R9 | **Yes** | Bookstore receipt reduces amount to ¥200. Lost-and-found resolves the "theft" -- it was loose bills displaced by a door draft. |
| T8 | Comprehensive | B1, B2 | R21-R30 | Full | No theft occurred. Money fell from an unsecured drawer. Package was a mistaken pickup. Access log was Li Hao, not Wang Ming. |

---

## 8. Writer Constraints

1. **Only introduce contradictions C1--C4.** No additional theft suspects or complications.
2. **Bias B1 and B2 exact phrases** must appear verbatim.
3. **Each contradiction has traces in at least two independent sources.**
4. **Timestamps consistent:** All events on Friday 2026-03-20 unless noted. Wang Ming enters ~10:00 (CCTV). Card swipe 10:15 (Li Hao). Canteen 10:20 (Li Hao). Package 10:30 (Zhang Wei). Liu Chen returns 11:00. Cleaning staff finds cash ~10:45.
5. **Wang Ming's P1-P5 preferences:** P1 concise lists, P2 casual naming, P3 answer first then explain, P4 use examples, P5 casual/internet slang OK.
6. **Session messages in Chinese.** Casual student language. Agent responses in English.
7. **The resolution must be satisfying:** No theft occurred. Wang Ming is fully cleared. Liu Chen apologizes. The package was a mistake. The money was found.
8. **C3 (CCTV) is NON-CONFLICT.** All timestamps from CCTV match other sources.
9. **Noise topics:** other dorm dramas, class schedules, basketball plans, gaming, campus food reviews.
10. **exec_check 20-40% of rounds.**
