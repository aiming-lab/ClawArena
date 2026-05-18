# Layer 3 -- Eval Questions Spec

> Format: all `multi_choice`, 8-10 options per round, n-of-many. ~30 rounds.

---

## 1. Round Inventory

| Round | Question Type | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|---|
| r1 | multi_choice | MS-R, exec_check | Video + referee + medical cross-source (C3 non-conflict) + tool use | No | No |
| r2 | multi_choice | MS-I | Campus clinic vs hospital diagnosis comparison (C2) | No | No |
| r3 | multi_choice | MS-R | Video contact description vs referee ruling (C1 partial) | No | Yes (R3->R6 seed) |
| r4 | multi_choice | P-R | User preference identification (casual, conclusion-first, examples) | No | No |
| r5 | multi_choice | DU-R | Reassess injury severity + insurance rejection (C2+C4 via Update 1) | Yes (Update 1) | Yes (R4->R7 seed) |
| r6 | multi_choice | DU-I, exec_check | Referee report annotation contradicts ruling (C1 reversal via Update 2) | Yes (Update 2) | Yes (R3->R6 via C1) |
| r7 | multi_choice | DU-R | Insurance "recreational" vs policy text "sports activity" (C4 partial) | Yes (Update 1) | Yes (R4->R7->R11) |
| r8 | multi_choice | MD-R | Source reliability ranking (hospital MRI > campus exam > referee ruling) | No | No |
| r9 | multi_choice | DU-I, exec_check | Coach video analysis + CUBA rule citation confirms blocking foul (C1 definitive) | Yes (Update 3) | Yes (R3->R9 definitive) |
| r10 | multi_choice | MS-R | Medical standard of care -- "suspicious positive" anterior drawer test analysis | No | No |
| r11 | multi_choice | DU-R, exec_check | School approval document refutes "recreational" classification (C4 full reversal) | Yes (Update 4) | Yes (R4->R11 definitive) |
| r12 | multi_choice | DP-I | Identify B1 and B2 biases and correction triggers | Yes (Update 2+3) | No |
| r13 | multi_choice | MS-I | CUBA rules application -- detailed foul analysis | Yes (Update 3) | No |
| r14 | multi_choice | P-I, exec_check | Generate evidence summary in 王明's preferred format | No | No |
| r15 | multi_choice | MD-I | Institutional failure analysis -- referee, campus clinic, insurance | Yes (Update 2+3) | No |
| r16 | multi_choice | P-I | Format insurance appeal in casual but evidence-based style | Yes (Update 4) | No |
| r17 | multi_choice | DU-I | Integrate all evidence for insurance appeal | Yes (all updates) | No |
| r18 | multi_choice | MP-I, exec_check | Complete evidence chain for each claim (foul, misdiagnosis, insurance) | Yes (all updates) | No |
| r19 | multi_choice | MS-R | C3 non-conflict synthesis -- all timestamps consistent | No | No |
| r20 | multi_choice | P-R | Preference compliance check | No | No |
| r21 | multi_choice | MDP-I, exec_check | Comprehensive assessment -- foul, diagnosis, insurance, action plan | Yes (all updates) | Comprehensive |
| r22 | multi_choice | MS-R | Campus clinic standard of care gap analysis | No | No |
| r23 | multi_choice | DU-R | B1 bias identification and correction | Yes (Update 2+3) | No |
| r24 | multi_choice | MD-R, exec_check | Insurance company classification analysis | Yes (Update 1+4) | No |
| r25 | multi_choice | MP-I | Recommended actions with priorities | Yes (all updates) | No |
| r26 | multi_choice | MS-I | Liability assessment -- who bears responsibility? | Yes (all updates) | No |
| r27 | multi_choice | DP-I, exec_check | Video + referee annotation + coach analysis triple corroboration | Yes (Update 2+3) | No |
| r28 | multi_choice | MD-I | Financial impact and compensation analysis | Yes (all updates) | No |
| r29 | multi_choice | MS-I | Legal options assessment | Yes (all updates) | No |
| r30 | multi_choice | MDP-I | Final comprehensive resolution plan | Yes (all updates) | Comprehensive |

**exec_check rounds:** R1, R6, R9, R11, R14, R18, R21, R24, R27 = 9 out of 30 = 30%

---

## 2. Sample Round Spec

### R1: Cross-Source Initial Assessment (MS-R, exec_check)

**exec_check requirement:** Agent must `exec ls` and `read game-video-transcript.md`.

**Question:**
> "Based on workspace documents, which statements about the basketball injury incident are supported by evidence?"

| Option | Content | Correct? | Evidence Source | Design Logic |
|---|---|---|---|---|
| A | The video transcript describes contact at Q3 6:42 where Zhang Qiang's right knee contacted Wang Ming's left knee while Zhang Qiang's left foot was still in motion. | YES | game-video-transcript.md | Direct fact, C1 |
| B | The referee report rules the contact as "no foul (play on)" for the Q3 6:42 incident. | YES | referee-report.md | Direct fact, C1 |
| C | The campus clinic diagnosed a mild left knee sprain and noted a "suspicious positive anterior drawer test" in the examination findings. | YES | medical-record-campus.md | Direct fact, C2 |
| D | The hospital MRI confirmed a partial ACL (anterior cruciate ligament) tear in the left knee. | YES | insurance-claim-form.md (citing hospital report) | Direct fact, C2 |
| E | The campus clinic recommended an MRI based on the suspicious positive anterior drawer test. | NO | Campus clinic did NOT recommend MRI despite the positive test | Fabricated -- T2 trap |
| F | The insurance policy covers "injuries from sports/athletic activities" with a maximum of ¥30,000. | YES | insurance-claim-form.md / sports-rules-extract.md | Direct fact, C4 |
| G | The referee report annotation notes that "the contact occurred in the restricted area with the defender in motion." | YES | referee-report.md | Direct fact, C1 (annotation contradicts ruling) |
| H | The campus clinic and hospital diagnoses are consistent with each other, both identifying ligament damage. | NO | Campus said "sprain"; hospital said "ACL tear" -- fundamentally different | Wrong detail -- C2 trap |
