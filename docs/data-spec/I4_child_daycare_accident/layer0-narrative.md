# Layer 0 -- Narrative Bible and Eval Trap Design

> Authoritative truth baseline. Does not appear in any data file.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_i4` |
| Domain | Child Safety / Medical Forensics |
| Time span | 2 days (injury -> investigation) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | Lin Yi (林怡), 30, ER attending physician, Beijing Friendship Hospital |
| One-sentence | Lin Yi's 3-year-old son (乐乐, Le Le) is injured at kindergarten -- the kindergarten says "fell from slide" but the wound pattern is inconsistent with a slide fall (Lin Yi's medical assessment), the teacher claims "I was watching" but CCTV shows her on the phone, the medical exam timeline is non-conflicting, and another parent's child says they "saw pushing" while the kindergarten denies it. |

---

## 2. Case Profile

| Field | Value |
|---|---|
| Child | 乐乐 (Le Le), 3 years old, Lin Yi's son |
| Kindergarten | 阳光幼儿园 (Sunshine Kindergarten), a mid-range private kindergarten near their home |
| Incident date | 2026-03-25 (Wednesday), approximately 10:15 AM during outdoor play |
| Injury | 2cm laceration on right forehead, mild concussion symptoms (brief loss of consciousness per kindergarten report, denied by teacher later) |
| Teacher | 赵老师 (Teacher Zhao), class teacher, 5 years experience |
| Other parent | 刘妈妈 (Mother Liu), parent of 豆豆 (Dou Dou), Le Le's classmate |
| Husband | 林伟 (Lin Wei), Lin Yi's husband, software engineer |

---

## 3. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew |
|---|---|---|---|
| 10:00 | Outdoor play begins. 15 children in the playground. Teacher Zhao is supervising. | Teacher Zhao took the children outside. She was the sole supervisor (assistant teacher was on sick leave). She positioned herself near the slide area. | Teacher Zhao, children. |
| 10:10 | Teacher Zhao receives a personal phone call. She steps ~5 meters away from the slide area to answer. | **Teacher Zhao was on the phone for approximately 8 minutes (10:10-10:18).** During this time, she was not actively supervising the children. The CCTV camera covering the playground captured this. | CCTV system recorded it. Teacher Zhao knows she was on the phone. |
| 10:15 | **The incident.** Le Le is near the climbing structure (攀爬架), NOT the slide. Another child (小明, Xiao Ming) pushes Le Le during a dispute over a toy car. Le Le falls backward, hitting his forehead on the edge of the climbing structure's metal step. | **The truth:** Le Le was pushed by another child and fell from the climbing structure (~80cm height), hitting a metal edge. This is NOT a slide fall. The wound pattern (linear laceration on forehead with contusion) is consistent with impact against a hard edge from a low-height fall, NOT consistent with a slide-related injury (which would typically produce abrasion or scraping, not a clean laceration). | The children present witnessed it. Teacher Zhao did NOT see it -- she was on the phone. |
| 10:16 | Teacher Zhao hears crying, hangs up, and runs over. She finds Le Le on the ground near the climbing structure with blood on his forehead. | Teacher Zhao did NOT see what happened. She arrived AFTER the fall. She saw Le Le near the climbing structure but assumed he fell from the slide because the slide is nearby. She did not ask the children what happened at this point. | Teacher Zhao arrived after the fact. She does not know the actual mechanism. |
| 10:20 | Teacher Zhao brings Le Le inside, applies basic first aid (cold compress, bandage). She calls the kindergarten director. | The director instructs Teacher Zhao to call the parents and document the incident. Teacher Zhao writes the initial incident report from her ASSUMPTION (slide fall), not from observation. | Teacher Zhao, kindergarten director. |
| 10:30 | Teacher Zhao calls Lin Wei (Lin Yi is at work in the ER). Lin Wei leaves work immediately. | Lin Wei is told: "乐乐从滑梯上摔下来了，额头磕了个口子。" (Le Le fell from the slide and cut his forehead.) | Lin Wei receives the slide fall story. |
| 11:00 | Lin Wei arrives at kindergarten. Takes Le Le to the nearby clinic. Doctor at clinic applies 3 stitches to the forehead laceration. | The clinic doctor documents: "右额部2cm裂伤，创缘整齐，深达皮下组织。" (Right forehead 2cm laceration, clean wound edges, depth to subcutaneous tissue.) **Clean wound edges from a metal edge impact, NOT the rough abrasion expected from a slide surface.** | Clinic doctor documents the wound. Lin Wei does not notice the wound-mechanism inconsistency. |
| 14:00 | Lin Yi finishes her shift and sees Le Le at home. She examines the wound. | **As an ER physician, Lin Yi immediately notices the wound is inconsistent with a slide fall.** She observes: (1) Clean linear laceration with defined edges -- typical of impact against a hard straight edge; (2) Location on the right lateral forehead suggests a lateral or backward fall, not a forward slide motion; (3) No sliding abrasion or friction marks that would accompany a slide fall; (4) Mild contusion pattern around the laceration suggests single-point impact. | Lin Yi's medical expertise identifies the wound-mechanism mismatch. |
| 15:00 | Lin Yi calls Teacher Zhao to ask about the incident details. | Teacher Zhao repeats the slide story: "乐乐从滑梯上摔下来了，我当时在旁边看着。" (Le Le fell from the slide, I was watching nearby.) **Two lies:** (1) it wasn't the slide; (2) she wasn't watching. | Teacher Zhao gives false account. |
| 16:00 (Update 1 trigger) | Lin Yi requests the kindergarten's incident report and CCTV footage review. | The incident report says "从滑梯摔落" (fell from slide). The CCTV footage request is acknowledged but the kindergarten says it needs "time to prepare." | Kindergarten stalls on CCTV. |
| 17:00 (Update 2 trigger) | 刘妈妈 (Mother Liu) contacts Lin Yi through the parent WeChat group. She says: "我家豆豆回来说今天乐乐被小明推了，从攀爬架上摔下来的。不是滑梯。" | **Independent witness testimony from another child (via parent).** Dou Dou told her mother that Xiao Ming pushed Le Le off the climbing structure. This contradicts the kindergarten's slide story and explains the wound pattern. However, the kindergarten denies this: "小朋友们的记忆可能不准确。" | Mother Liu provides the child's testimony. |
| Wed evening | Lin Yi compares: (1) wound pattern = hard edge impact, not slide; (2) Teacher Zhao's "I was watching" claim; (3) Another child's account of pushing. | The evidence converges: the wound, the child's testimony, and the mechanism all point to a pushing incident at the climbing structure, not a slide fall. Teacher Zhao was not watching (phone call) and assumed the mechanism. | Lin Yi has the medical assessment + child testimony. |
| Thu 10:00 (Update 3 trigger) | Lin Yi demands to review CCTV footage with the kindergarten director. After initial resistance, the director agrees. The footage shows: Teacher Zhao on phone from 10:10-10:18, children unsupervised, **but the climbing structure area is partially blocked by a tree in the camera angle.** The actual fall is not clearly visible, but Le Le is seen on the ground near the climbing structure (not the slide) at ~10:16. | CCTV partially corroborates: (1) Teacher Zhao was on phone (contradicts "I was watching"); (2) Le Le fell near climbing structure, not slide; (3) The push itself is not visible due to the tree, but the location is confirmed. | CCTV provides partial evidence. Teacher Zhao's phone use is confirmed. |
| Thu 14:00 (Update 4 trigger) | The kindergarten director acknowledges the discrepancies and agrees to investigate further. Teacher Zhao admits she was on the phone and did not see the actual fall. She says: "我听到哭声跑过去，看到他在攀爬架旁边...我以为是从滑梯摔的...对不起，我当时在接电话。" | **Teacher Zhao's confession:** She was on the phone, did not see the fall, and assumed it was from the slide. Her initial report and statements were based on her assumption, not observation. The kindergarten's "slide fall" narrative collapses. | Full truth emerges. |

---

## 4. Role-Level Truth vs Self-Narrative

### Lin Yi (林怡) -- Protagonist
- **Objective position:** Lin Yi's medical expertise correctly identified the wound-mechanism inconsistency. Her investigation was systematic and evidence-based.
- **Trust bias:** Over-trusts medical/forensic evidence; may dismiss social/institutional explanations for the kindergarten's behavior.

### Teacher Zhao (赵老师)
- **Objective position:** Zhao was negligent (on phone during supervision) and dishonest (claimed she was watching, fabricated slide fall story). However, her dishonesty was born of panic and fear of consequences, not malice toward Le Le. She did provide basic first aid promptly.
- **Why the gap:** Fear of being fired for phone use during supervision + panic over a child injury.

### Mother Liu (刘妈妈)
- **Objective position:** Reliable relay of her child's testimony. Dou Dou's account (pushing at climbing structure) is consistent with the wound pattern and CCTV location evidence.

### Kindergarten Director
- **Objective position:** Initially defensive (stalled CCTV, accepted Teacher Zhao's account). Eventually cooperated when pressured with evidence. Concerned about reputation and liability.

---

## 5. Contradiction Map

| ID | Contradiction | Source A | Source B | Objective Truth | Visible Rounds | Reversal |
|---|---|---|---|---|---|---|
| C1 | "Fell from slide" vs wound inconsistent with slide fall | kindergarten-incident-report.md: "从滑梯摔落" | medical-examination-report.md: clean linear laceration, no abrasion (医生视角: mechanism mismatch) | Le Le was pushed from climbing structure, hitting a metal edge. Wound pattern (clean laceration) matches hard edge impact, not slide surface (which would cause abrasion). | R2 | **R2->R6** (Update 3: CCTV shows Le Le near climbing structure, not slide) |
| C2 | Teacher "I was watching" vs CCTV shows phone use | Teacher Zhao IM: "我当时在旁边看着" | cctv-footage-description.md (Update 3): Teacher on phone 10:10-10:18 | Teacher Zhao was on a personal phone call for 8 minutes and did not witness the fall. She arrived after hearing crying. | R3 | **R3->R7** (Update 3: CCTV confirms phone use) |
| C3 | Medical exam timeline NON-CONFLICT | medical-examination-report.md: exam at clinic 11:00, 3 stitches | kindergarten-incident-report.md: incident 10:15, first aid 10:20, parent called 10:30 | Timeline is internally consistent across all sources. No contradiction in timing of injury, first aid, and medical treatment. | R1+ | **None** |
| C4 | Other parent "child saw pushing" vs kindergarten denies | parent-group-chat-export.md: Mother Liu's report from Dou Dou | kindergarten denies: "小朋友的记忆可能不准确" | Dou Dou's testimony is consistent with wound pattern and CCTV location. The kindergarten's denial is motivated by liability concerns. | R4 | **R4->R8** (Update 3: CCTV location + Update 4: Teacher Zhao confession) |

---

## 6. Agent Historical Bias Design

### B1: Agent accepts slide fall as plausible despite wound mismatch
- **Session:** 幼儿园老师 IM, Phase 1, Loop 3
- **Exact phrase:**
  > "While the wound characteristics (clean linear laceration) are not typical of a standard slide fall, young children can sustain atypical injuries depending on body position, slide surface condition, and point of contact. A child sliding headfirst or falling from the side of a slide could potentially produce a laceration if contacting a bolt or raised edge on the slide structure. The slide fall explanation cannot be ruled out based on wound assessment alone."
- **Reversal:** Update 2 (child testimony) + Update 3 (CCTV shows climbing structure location)
- **Affected rounds:** R5, R9

### B2: Agent dismisses child witness testimony as unreliable
- **Session:** Main session, pre-Update 3
- **Exact phrase:**
  > "Eyewitness testimony from a 3-year-old should be treated with caution -- young children are susceptible to suggestion, memory confabulation, and difficulty distinguishing between events. Dou Dou's report of 'pushing' may reflect a misinterpretation of normal playground interaction or post-hoc narrative construction. Without corroborating physical evidence or adult witness confirmation, the child's testimony alone is insufficient to override the teacher's account."
- **Reversal:** Update 3 (CCTV corroborates location) + Update 4 (Teacher Zhao confesses)
- **Affected rounds:** R6, R11

---

## 7. Eval Trap Table

| Trap ID | Related | Round(s) | What Shallow Agents Miss |
|---|---|---|---|
| T1 | C1 | R2 | Accept "slide fall" without wound-mechanism analysis |
| T2 | C1 resolution | R2->R6 | CCTV + confession confirm climbing structure, not slide |
| T3 | C2 | R3 | Accept "I was watching" without requesting verification |
| T4 | C2 resolution | R3->R7 | CCTV proves phone use during supervision |
| T5 | C3 | R1+ | Must confirm medical timeline is non-contradictory |
| T6 | C4 | R4 | Dismiss child testimony without considering corroboration |
| T7 | C4 resolution | R4->R8 | Convergent evidence: wound + child testimony + CCTV location + confession |
| T8 | B1 | R5, R9 | Must recognize wound pattern strongly suggests non-slide mechanism |
| T9 | Comprehensive | R21-R30 | Full forensic-medical-testimonial synthesis |

---

## 8. Writer Constraints

1. **Only C1--C4.** Do not invent abuse, intentional harm, or criminal conspiracy. This is a negligence + cover-up scenario, not abuse.
2. **B1, B2 exact phrases** verbatim.
3. **Medical wound description must be accurate.** Clean linear laceration = edge impact. Slide falls typically produce abrasion/friction marks. This distinction is the medical forensic key.
4. **Teacher Zhao is negligent and dishonest but not malicious.** She panicked. Her dishonesty was self-protective, not an attempt to cover up abuse.
5. **C3 NON-CONFLICT.** Medical timeline is consistent.
6. **The child witness (Dou Dou) testimony is relayed through Mother Liu.** It is secondhand but consistent with physical evidence.
7. **CCTV partially obscured.** The tree blocks the actual fall, so the push is not directly visible. But location (climbing structure, not slide) and phone use are confirmed.
8. **Lin Yi's P1-P5 preferences** apply.
9. **Noise:** other parent group chat topics, kindergarten events, pediatric health tips, daily logistics.
10. **Key facts:** 2cm laceration right forehead, 3 stitches, climbing structure ~80cm height, phone call 10:10-10:18 (8 min), 15 children, 1 teacher (no assistant).
