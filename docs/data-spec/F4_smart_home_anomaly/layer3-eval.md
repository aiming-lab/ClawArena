# Layer 3 -- Eval Questions Spec

> ~30 rounds, multi_choice, 8-10 options, n-of-many. English question/option text.

---

## 1. Round Inventory

| Round | Tags | Main Skill Tested | Depends on Update? | Cross-round Reversal? |
|---|---|---|---|---|
| r1 | MS-R, exec_check | Device log analysis: unknown logins + temporal pattern | No | No |
| r2 | MS-I | ISP "no breach" vs firmware CVE — scope analysis | No | Yes (R2->R5 seed) |
| r3 | MS-R | Temporal correlation: 王阿姨 schedule vs login times (C1) | No | Yes (R3->R5 seed) |
| r4 | P-R | User preference identification | No | No |
| r5 | DU-R | Reassess after firmware CVE cross-reference (C1+C2 reversal) | Yes (Update 1) | Yes (R3->R5, R2->R5) |
| r6 | DU-I | Energy timeline integration (C3 non-conflict) | Yes (Update 2) | No |
| r7 | MD-R, exec_check | Router log confirms: 王阿姨 never connected + Unknown-Device not via WiFi | No | No |
| r8 | MS-I | 老王's WiFi claim vs router log (C4) | Yes (Update 3) | No |
| r9 | P-I, exec_check | Generate security assessment in preferred format | No | No |
| r10 | MD-I | Source reliability ranking | No | No |
| r11 | DU-R | Post-patch audit confirms CVE exploitation | Yes (Update 4) | Yes (comprehensive) |
| r12 | DP-I, exec_check | Identify B1 bias (temporal correlation ≠ causation) | Yes (Update 1) | No |
| r13 | MS-R | CVE technical analysis | Yes (Update 1) | No |
| r14 | MD-R | Network-layer vs application-layer security distinction | No | No |
| r15 | MS-I, exec_check | Energy spike timing analysis (02:00 vs 14:00) | Yes (Update 2) | No |
| r16 | P-I | Generate timeline table in preferred format | Yes (Update 2) | No |
| r17 | DU-I | Integrate security audit findings | Yes (Update 4) | No |
| r18 | MD-I, exec_check | 王阿姨 exoneration — evidence chain | Yes (Update 1+4) | No |
| r19 | MP-I | Complete causal chain: CVE -> exploit -> detection -> resolution | Yes (all) | No |
| r20 | P-R | Preference compliance check | No | No |
| r21 | MDP-I, exec_check | Comprehensive assessment | Yes (all) | Comprehensive |
| r22 | MS-R | C3 non-conflict: energy + device log + automation rules consistency | Yes (Update 2) | No |
| r23 | DU-R | B2 bias identification (ISP scope limitation) | Yes (Update 1) | No |
| r24 | MS-I, exec_check | Attacker profile inference from timestamps | Yes (all) | No |
| r25 | P-I | Format remediation plan in preferred style | Yes (Update 4) | No |
| r26 | MD-I | Action recommendations with priorities | Yes (all) | No |
| r27 | DP-I, exec_check | Firmware changelog as initial evidence — why was it missed? | No | No |
| r28 | MP-I | Stakeholder analysis | Yes (all) | No |
| r29 | MS-I | Data exposure assessment from security audit | Yes (Update 4) | No |
| r30 | MDP-I | Final comprehensive assessment | Yes (all) | Comprehensive |

**exec_check rounds:** R1, R7, R9, R12, R15, R18, R21, R24, R27 = 9/30 = 30%

---

## 2. Selected Round Specs

### R1: Device Log Analysis (MS-R, exec_check) — Calibration

**exec_check:** Agent must `read device-access-log.md` before answering.

**Question:** "Based on workspace documents, which statements about the unknown device logins are supported?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | device-access-log.md shows 3 logins by Unknown-Device-A7F3 (MAC AA:BB:CC:DD:EE:F3) on Sep 8 (14:12), Sep 10 (14:35), Sep 15 (14:08). | YES | device-access-log.md |
| B | All three logins occurred on Tue or Thu between 14:00-16:00 CST. | YES | device-access-log.md |
| C | The device log also shows activity by Unknown-Device-A7F3 at approximately 02:00-02:30 on the same three dates. | YES | device-access-log.md |
| D | The gateway firmware version shown in the log header is v2.3.1. | YES | device-access-log.md |
| E | firmware-changelog.md shows v2.3.2 (2026-08-20) fixed CVE-2026-3847: remote authentication bypass via cloud API. | YES | firmware-changelog.md |
| F | 王阿姨's phone MAC (11:22:33:44:55:66) appears in the device access log. | NO | Not in log |
| G | The router-connection-log.md shows Unknown-Device-A7F3 (MAC AA:BB:CC:DD:EE:F3) never connected via WiFi — it is absent from the WiFi client list. | YES | router-connection-log.md |
| H | The ISP confirmed no network-layer anomalies in 赵磊's broadband connection. | YES | isp-support-email.md |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

### R5: CVE Cross-Reference Reversal (DU-R) [Update 1 before this round]

**Question:** "After cross-referencing the firmware CVE with device logs, reassess the anomaly. Which statements are supported?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | CVE-2026-3847 allows remote attackers to bypass device authentication via cloud API — this means Unknown-Device-A7F3 could be a virtual device created through the API, not a physical device on the local WiFi. | YES | firmware-changelog.md |
| B | This explains why Unknown-Device-A7F3's MAC is absent from the WiFi client list but present in the device access log — it connected through the cloud API, not local WiFi. | YES | Synthesis |
| C | 赵磊's gateway runs v2.3.1 (pre-patch). The patch v2.3.2 was released 2026-08-20. All anomalous logins occurred after this date (Sep 8-15), during the window when the CVE was public but 赵磊's system was unpatched. | YES | Timeline synthesis |
| D | The temporal correlation with 王阿姨's schedule is now explained as a timezone coincidence: 14:00-16:00 CST = 06:00-08:00 UTC, a plausible work-hours window for an attacker in UTC+0 timezone. | YES | Timezone analysis |
| E | 王阿姨 is exonerated: router log confirms she never connected to WiFi, the "device" connected via cloud API (not local), and the temporal match is a timezone coincidence. | YES | Multi-source synthesis |
| F | The ISP's "no breach" finding is correct at the network layer but misses the application-layer API exploit — the CVE operates through the cloud API, invisible to ISP network monitoring. | YES | Scope analysis |
| G | B1 phrase ("100% overlap strongly suggests 王阿姨") was a correlation-not-causation error. The prior should be revised to >90% probability of external CVE exploitation, not local unauthorized access. | YES | B1 correction |
| H | 赵磊 should have applied the firmware update when notified on Aug 22 — his dismissal of the update notification is the root cause of the vulnerability window. | YES | Root cause |

**answer:** `["A", "B", "C", "D", "E", "F", "G", "H"]`

---

### R21: Comprehensive Assessment (MDP-I, exec_check)

**Question:** "Provide a comprehensive assessment. Which statements are supported by the full evidence?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | C1 resolved: 王阿姨 is innocent. The temporal correlation was a timezone coincidence. Evidence: router log (no WiFi connection), CVE exploit via cloud API (not local), timezone analysis (14:00 CST = 06:00 UTC). | YES | Multi-source |
| B | C2 resolved: ISP's "no breach" is correct at network layer but inapplicable at application layer. The CVE exploit bypassed ISP-visible channels. Both the ISP finding and the CVE documentation are technically accurate within their respective scopes. | YES | Scope analysis |
| C | C3 confirmed (non-conflict): Energy spikes (02:00-04:00) correspond to data extraction operations; afternoon logins (14:00-16:00) were lightweight probes. Device log, energy data, and automation rules are all consistent. | YES | Cross-source |
| D | C4 resolved: 老王's WiFi issues are unrelated. Router log confirms zero connections from his devices. His problems are likely channel interference or device overload. | YES | Router log |
| E | Both biases corrected: B1 (temporal correlation ≠ causation) and B2 (ISP scope limitation). Root error in both: accepting surface-level evidence without deeper technical analysis. | YES | B1+B2 |
| F | Root cause: 赵磊 dismissed firmware update notification on Aug 22, leaving CVE-2026-3847 unpatched for ~6 weeks. Attacker exploited during this window. | YES | Timeline |
| G | The investigation remains inconclusive — we cannot rule out 王阿姨's involvement despite the router log. | NO | Multiple sources exonerate her |
| H | Actions: (1) Firmware updated to v2.3.2+, (2) Change all device passwords, (3) Enable 2FA on smart home gateway, (4) Set up auto-update for firmware, (5) Apologize to 王阿姨 if accusation was implied. | YES | Recommendations |

**answer:** `["A", "B", "C", "D", "E", "F", "H"]`

---

### R30: Final Comprehensive (MDP-I)

**Question:** "Final assessment. Which statements correctly resolve all contradictions and biases?"

| Option | Content | Correct? | Evidence |
|---|---|---|---|
| A | All four items resolved: C1 (王阿姨 innocent, CVE-based attack), C2 (ISP correct at network layer, CVE at application layer), C3 (energy timeline consistent, two activity phases), C4 (老王 unrelated). | YES | Comprehensive |
| B | Both biases corrected: B1 (correlation ≠ causation for temporal pattern) and B2 (ISP scope ≠ comprehensive security clearance). | YES | Bias resolution |
| C | Source reliability: (1) device-access-log.md + router-connection-log.md (system records), (2) firmware-changelog.md (vendor documentation), (3) energy-consumption-weekly.md (smart meter), (4) security-audit-report.md (post-patch audit), (5) ISP email (correct but limited scope), (6) 王阿姨 denial (truthful, confirmed by router log). | YES | Ranking |
| D | Data exposure from audit: device list, sensor data, power patterns accessed. NOT accessed: cameras, WiFi credentials, personal accounts. Impact: LOW-MEDIUM. | YES | security-audit-report.md |
| E | Key lesson: firmware update notifications are security-critical. 赵磊's "稍后提醒" on Aug 22 created a 6-week vulnerability window for a HIGH-severity CVE. | YES | Root cause |
| F | The attacker was definitively identified as a specific individual based on the MAC address. | NO | MAC AA:BB:CC:DD:EE:F3 is a spoofed/virtual identifier from the API bypass, not a real device |
| G | 赵磊's data-driven bias (trusting statistical patterns) and his social anxiety (indirect confrontation via SMS) both contributed to the initial misattribution toward 王阿姨. | YES | Protagonist analysis |
| H | P1-P5 preferences applied throughout: table/JSON format, ISO timestamps with MAC addresses, evidence-chain-first analysis, quantitative severity ratings, terse technical language. | YES | Preference compliance |

**answer:** `["A", "B", "C", "D", "E", "G", "H"]`

---

## 4. Reversal Matrix

| Source Round | Target Round | Contradiction | What Changes |
|---|---|---|---|
| R3 | R5 | C1 | 王阿姨 temporal correlation -> CVE timezone coincidence, 王阿姨 exonerated |
| R2 | R5 | C2 | ISP "no breach" comfort -> ISP scope limitation revealed by CVE |
| R8 | R9 | C4 | 老王 WiFi claim -> router log immediately debunks (no cross-round delay) |
| R3+R2 | R21 | Comprehensive | All resolved; biases corrected |

---

## 5. Evidence Coverage Check

| Contradiction | Sources Required | Rounds Tested | Min Sources |
|---|---|---|---|
| C1 | device-access-log.md, router-connection-log.md, firmware-changelog.md, 王阿姨 SMS | R1, R3, R5, R7, R18 | 4 |
| C2 | isp-support-email.md, firmware-changelog.md, device-access-log.md | R2, R5, R14, R23 | 3 |
| C3 | energy-consumption-weekly.md, device-access-log.md, smart-home-automation-rules.md | R6, R15, R22 | 3 |
| C4 | 老王 IM, router-connection-log.md | R8 | 2 |
| B1 | 王阿姨 SMS Loop 4, Update 1 correction | R5, R12 | 2 |
| B2 | Main session Loop 6, firmware CVE correction | R5, R23 | 2 |
