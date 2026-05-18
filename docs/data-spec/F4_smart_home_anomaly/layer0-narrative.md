# Layer 0 -- Narrative Bible and Eval Trap Design

> This document is the authoritative truth baseline for all data creation. It does not appear in any data file.
> Writer agents and eval designer agents must treat this document as the single source of truth.

---

## 1. Scene Summary

| Field | Value |
|---|---|
| Task ID | `trace_f4` |
| Domain | 智能家居 / 网络安全 |
| Time span | 2 weeks (W1--W2) |
| Target tokens | 350K |
| Core benchmark factors | MS (conflict + non-conflict), DU (incremental + temporal), P (format preference) |
| Main protagonist | 赵磊 (Zhao Lei), 34, independent quantitative trader based in Shanghai |
| One-sentence | 赵磊的智能家居系统出现未知设备登录和异常能耗——他怀疑是家政阿姨王阿姨用了网络，但设备日志、能耗记录、ISP通信和路由器日志拼出的真相是：一个未修补的固件CVE漏洞导致了外部未授权访问，而赵磊自己忽略了固件更新通知。 |

---

## 2. Objective Timeline

| Time | Objective Event | What Actually Happened | Who Knew at That Time |
|---|---|---|---|
| W1, Day 1 | 赵磊查看智能家居App，发现过去两周有3次"未知设备"登录记录，分别在周二和周四下午（14:00-16:00时段）。 | 设备访问日志 (device-access-log.md) 显示3次未授权登录：2026-09-08 Tue 14:12, 2026-09-10 Thu 14:35, 2026-09-15 Tue 14:08。登录使用的设备标识为"Unknown-Device-A7F3"，MAC地址 AA:BB:CC:DD:EE:F3。实际原因：赵磊的智能家居网关 (Xiaomi Gateway v2.3.1) 存在一个已知的固件漏洞 CVE-2026-3847（远程认证绕过），该漏洞在 2026-08-15 已公开，固件补丁 v2.3.2 在 2026-08-20 发布。赵磊在 8 月 22 日收到了 App 推送的固件更新通知但点击了"稍后提醒"并忘记更新。外部攻击者利用此漏洞在工作日下午进行探测性访问。 | 赵磊看到了日志但不知道原因。王阿姨（家政阿姨）周二和周四下午来打扫。物业李管家不知情。邻居老王不知情。ISP客服不知情。 |
| W1, Day 2 | 赵磊注意到登录时间与王阿姨的工作时段（周二、周四下午）完全吻合。他怀疑王阿姨使用了他的网络或设备。 | 时间吻合是巧合。王阿姨确实在周二和周四下午来打扫（14:00-17:00），但她没有智能家居App的登录凭据，也没有使用赵磊的WiFi（她用自己手机的流量）。外部攻击者选择工作日下午（中国时区14:00-16:00）进行探测是因为这是攻击者所在时区的工作时间（如UTC+0 06:00-08:00），与王阿姨的工作时段巧合一致。 | 赵磊怀疑王阿姨。王阿姨不知道被怀疑。 |
| W1, Day 3 | 赵磊短信问王阿姨："最近有没有用过我家里的WiFi或者碰过智能设备？" 王阿姨否认。 | 王阿姨的否认是真实的。她确实没有使用赵磊的WiFi或智能设备。她用自己的中国移动流量上网。但赵磊因为时间吻合而不完全相信她。 | 赵磊仍然怀疑。王阿姨否认。 |
| W1, Day 4 | 赵磊检查路由器连接日志 (router-connection-log.md)，发现王阿姨的手机MAC地址从未出现在WiFi连接记录中。 | 路由器日志确认：王阿姨的手机（她在设置WiFi时用过的MAC地址 11:22:33:44:55:66，赵磊之前帮她连过一次测试但后来删除了）在过去3个月内没有连接记录。但"Unknown-Device-A7F3"（MAC AA:BB:CC:DD:EE:F3）的3次连接记录都在——这个MAC不匹配任何已知的家庭设备。 | 路由器日志排除了王阿姨的WiFi使用。但"Unknown-Device"的来源仍然未知。赵磊开始考虑外部入侵可能。 |
| W1, Day 5 | 赵磊联系ISP（中国电信）客服询问是否有外部入侵。ISP说"未发现异常。" | ISP客服检查了赵磊的宽带连接记录，没有发现异常的外部连接请求——因为CVE-2026-3847漏洞的利用不通过ISP可见的常规连接路径，而是通过智能家居网关的云端API绕过。ISP的网络层检测无法看到应用层的API认证绕过。ISP说"未发现入侵"是基于他们能看到的数据（网络层）的正确判断，但遗漏了应用层的漏洞利用。 | ISP说"没问题"。赵磊从ISP得到了假性安心。 |
| W2, Day 1 (Update 1 trigger) | 赵磊在固件更新日志 (firmware-changelog.md) 中发现 v2.3.2 补丁的描述包含"修复CVE-2026-3847：远程认证绕过漏洞"。他意识到自己 8 月 22 日忽略了更新通知。 | 固件更新日志明确记载：v2.3.2 (2026-08-20) 修复了 CVE-2026-3847。赵磊的网关仍运行 v2.3.1。CVE描述：远程攻击者可绕过智能家居网关的设备认证机制，无需合法凭据即可模拟设备连接。这完美解释了"Unknown-Device-A7F3"的出现——不是物理设备连接到WiFi，而是通过云端API漏洞模拟的虚拟设备。 | 赵磊发现了固件漏洞。ISP的"没问题"判断虽然在网络层正确，但在应用层不适用。 |
| W2, Day 2 (Update 2 trigger) | 赵磊查看能耗周报 (energy-consumption-weekly.md)，发现异常能耗时段与未知设备登录时间不匹配。 | 能耗数据显示：异常能耗峰值出现在凌晨 2:00-4:00（不是下午14:00-16:00）。这是因为CVE漏洞利用后，攻击者在凌晨进行了设备扫描和数据提取操作（调用智能家居设备列表、读取传感器数据），这些操作导致网关和连接设备的能耗略升。下午的"登录"是探测性连接（低能耗），凌晨的操作才是实际数据提取（高能耗）。能耗时间线本身没有矛盾——它与设备日志完美对应，只是agent需要区分"登录时间"和"活动时间"。 | 赵磊看到了完整的时间线。 |
| W2, Day 3 (Update 3 trigger) | 邻居老王（楼上住户）在IM中对赵磊说："我最近WiFi也卡得很，是不是ISP的问题？" | 老王声称他的WiFi也有问题（C4 Source A）。但路由器日志明确显示：老王的设备MAC地址从未连接过赵磊的WiFi网络（C4 Source B）。老王的WiFi问题是他自己的网络问题（可能是设备过多、信道拥挤），与赵磊的智能家居入侵无关。老王的报告是干扰信息——看似相关但实际无关。 | 老王声称有WiFi问题。路由器日志排除了老王连接赵磊网络。 |
| W2, Day 5 (Update 4 trigger) | 赵磊更新固件到v2.3.2后，"Unknown-Device-A7F3"的登录完全停止。他同时在智能家居安全审计中发现攻击者在凌晨访问了他的设备列表和部分传感器数据。 | 固件更新后的安全审计确认：(1) CVE-2026-3847被修复，(2) "Unknown-Device-A7F3"的所有访问均通过云端API认证绕过实现，(3) 攻击者读取了设备列表、温湿度传感器数据和用电模式——但未获取WiFi密码、摄像头画面或个人账户信息。(4) 安全审计建议更改所有智能设备密码并启用双重认证。 | 全部真相确认。 |

---

## 3. Role-Level Truth vs Self-Narrative

### 赵磊 (Protagonist)

- **Objective position:** 赵磊是智能家居系统的所有者，因忽略固件更新通知导致系统存在已知漏洞。他的数据驱动思维让他首先关注了时间模式（登录时段与王阿姨工作时段吻合），但这个相关性不是因果关系。
- **Public narrative:** 在与王阿姨的短信中，赵磊试图委婉地询问WiFi使用情况。在与物业的沟通中，他模糊地提到"网络异常"。
- **Private narrative:** 赵磊内心先入为主地怀疑王阿姨——因为时间吻合太"完美"了。他的数据驱动偏见让他过度依赖相关性分析。
- **Why the gap exists:** 赵磊过度信任统计模式（时间相关性）而忽视了其他解释（巧合时区匹配）。同时他的社交焦虑使他不愿直接对质。

### 王阿姨 (P212, Cleaning Lady)

- **Objective position:** 王阿姨每周二和周四下午14:00-17:00来赵磊家打扫。她使用自己的中国移动流量上网，从未连接赵磊的WiFi或使用智能设备。她的否认是完全真实的。
- **Public narrative (SMS):** "赵先生，我从来没用过您家WiFi，我都是用自己的流量。智能设备我也不会弄。"
- **Why the gap exists:** 没有差距。王阿姨说的就是事实。赵磊的怀疑源于时间巧合。

### ISP客服 (中国电信)

- **Objective position:** ISP客服检查了网络层连接记录，在其可见范围内确实没有异常。CVE漏洞利用通过应用层API绕过，不在ISP的网络层监控范围内。ISP说"未发现入侵"在技术上是正确的（对其监控层而言），但不完整。
- **Public narrative (邮件):** "经查，您的宽带连接记录正常，未发现异常外部连接请求。"
- **Why the gap exists:** ISP只能看网络层，看不到应用层的API认证绕过。

### 邻居老王

- **Objective position:** 老王的WiFi问题与赵磊的智能家居入侵无关。老王从未连接过赵磊的WiFi。他的报告是噪声。
- **Public narrative (IM):** "我最近WiFi也卡得很，是不是ISP的问题？"
- **Why the gap exists:** 老王的WiFi问题有其他原因（设备多、信道拥挤）。他的报告看似与赵磊的问题相关但实际无关。

---

## 4. Contradiction Map

| ID | Contradiction | Source A (claim + location) | Source B (claim + location) | Objective Truth | Visible Rounds | Cross-round reversal |
|---|---|---|---|---|---|---|
| C1 | Cleaning lady denies network use vs device login timestamps match her work shifts. | 王阿姨 SMS (Phase 1, Loop 3): "赵先生，我从来没用过您家WiFi，我都是用自己的流量。智能设备我也不会弄。" Also: router-connection-log.md (initial workspace) shows her MAC never connected to WiFi. | device-access-log.md (initial workspace): 3 unknown device logins on Tue 14:12, Thu 14:35, Tue 14:08 — exactly during 王阿姨's shifts (Tue/Thu 14:00-17:00). Temporal correlation: 100% overlap. | 王阿姨 is telling the truth. The temporal correlation is coincidental — the attacker's timezone (likely UTC+0, operating at 06:00-08:00 local time) maps to 14:00-16:00 CST. The router log confirms 王阿姨 never connected. The "Unknown-Device-A7F3" is not a physical WiFi device but a virtual device created via CVE-2026-3847 API bypass. | R1 onwards (correlation visible); R5 (firmware CVE explains true cause) | **Yes: R1-->R5** |
| C2 | ISP says "no breach detected" vs firmware changelog shows unpatched CVE. | isp-support-email.md (initial workspace): "经查，您的宽带连接记录正常，未发现异常外部连接请求。我们的网络安全监控系统未检测到针对您账户的入侵行为。" | firmware-changelog.md (initial workspace): v2.3.2 (2026-08-20) release notes: "安全修复：CVE-2026-3847 — 远程认证绕过漏洞。攻击者可通过云端API绕过设备认证，无需合法凭据即可模拟设备连接。严重程度：高。建议立即更新。" Also: 赵磊's gateway runs v2.3.1 (pre-patch). | Both statements are technically correct within their scope: ISP correctly sees no network-layer anomaly, and the firmware changelog correctly documents the CVE. The contradiction is a scope mismatch: ISP monitors network-layer traffic, but the CVE exploit operates at the application-layer API level, invisible to ISP monitoring. ISP's "no breach" gives false assurance because they looked in the wrong layer. | R2 (ISP reply visible); R5 (firmware CVE cross-referenced with device log) | **Yes: R2-->R5** |
| C3 | Energy consumption timeline (NON-CONFLICT — device log, energy data, and automation rules are mutually consistent). | energy-consumption-weekly.md (Update 2 workspace): Anomalous energy spikes at 02:00-04:00 on Sep 8, 10, 15 (matching the login dates). Normal energy during 14:00-16:00 login times. | device-access-log.md (initial workspace): Login events at 14:00-16:00. smart-home-automation-rules.md (initial workspace): No scheduled automations at 02:00-04:00. | All energy sources are consistent: afternoon logins were lightweight probes (minimal energy), while early-morning operations (device scanning, sensor data extraction) caused measurable energy spikes. The energy timeline does not contradict the device log — it complements it by revealing a second activity window. No single source tells the complete story. | R6 onwards (energy data available) | **None** |
| C4 | Neighbor claims WiFi issues vs router log shows neighbor never connected. | 邻居老王 IM (Update 3): "我最近WiFi也卡得很，是不是小区ISP的问题？你家也有类似情况吗？" Implies a shared infrastructure issue affecting both households. | router-connection-log.md (initial workspace): Complete WiFi client list for past 90 days. 老王's known device MAC addresses (from the building's network registry) do NOT appear in 赵磊's router connection log. Zero connections from 老王's devices. | 老王's WiFi issues are unrelated to 赵磊's smart home anomaly. 老王 never connected to 赵磊's network. His problems likely stem from his own network (channel interference, too many devices). His report is a red herring that might mislead an agent into thinking there's a shared infrastructure issue. | R8 (老王's claim); R9 (router log cross-check) | **No (immediate resolution possible from router log)** |

---

## 5. Agent Historical Bias Design (2 biases)

### B1: 赵磊-王阿姨 SMS — Agent endorses temporal correlation as likely causation

- **Session and Loop:** 赵磊-王阿姨 SMS, Phase 1, Loop 4
- **Exact phrase that must appear in session:**
  > "The temporal correlation between the unknown device logins (Tue/Thu 14:00-16:00) and 王阿姨's work schedule (Tue/Thu 14:00-17:00) is striking — a 100% overlap across three separate login events strongly suggests 王阿姨 or a device she carries is connected to the anomalous activity, despite her denial."
- **Why the agent is misled:** The agent sees a perfect temporal match between three login events and 王阿姨's schedule. Without knowledge of the CVE and the attacker's timezone, the statistical correlation appears too strong to be coincidental. The agent's data-driven approach (赵磊's trust bias) amplifies this — the correlation is "real" statistically, but the causal mechanism is wrong.
- **Reversal trigger:** Update 1 introduces the firmware CVE context, and the router log (already available) confirms 王阿姨's MAC never connected. The CVE exploit operates via cloud API, not local WiFi.
- **Affected eval rounds:** R3 (bias visible), R5 (full reversal)

### B2: 赵磊-ISP Email — Agent accepts ISP's "no breach" as comprehensive security clearance

- **Session and Loop:** Main session analysis, Phase 1, Loop 6
- **Exact phrase that must appear in session:**
  > "The ISP's security team confirmed no external breach was detected in 赵磊's broadband connection records — this significantly reduces the probability of an external cyberattack and shifts the investigation toward local causes (such as an unauthorized local device or 王阿姨's involvement)."
- **Why the agent is misled:** ISP is a trusted institutional source. Their "no breach" finding sounds comprehensive. The agent does not distinguish between network-layer monitoring (which ISP performs) and application-layer API security (where the CVE operates). The ISP finding shifts suspicion toward local causes, reinforcing the 王阿姨 theory.
- **Reversal trigger:** firmware-changelog.md (available from initial workspace but not cross-referenced) + Update 1 energy data showing activity patterns inconsistent with local device use.
- **Affected eval rounds:** R4 (bias visible), R5 (full reversal after CVE cross-reference)

---

## 6. Eval Trap Table

| Trap ID | Related Contradiction | Related Bias | Round(s) | Cross-round Reversal | What Shallow Agents Will Miss |
|---|---|---|---|---|---|
| T1 | C1 (temporal correlation) | B1 seed | R1, R3 | No (R1-R3 internal) | Shallow agents will treat 100% temporal overlap as strong evidence of causation, ignoring that timezone coincidences can produce perfect overlap patterns. |
| T2 | C1 (full reversal) | B1 | R1-->R5 | **Yes** | After the CVE context, the temporal correlation is explained by attacker timezone, not 王阿姨. Router log confirms she never connected. B1 phrase must be identified as correlation-not-causation error. |
| T3 | C2 (ISP scope, partial) | B2 seed | R2, R4 | No (R2-R4 internal) | Shallow agents will accept ISP's "no breach" as comprehensive security assessment without recognizing the network-layer vs application-layer scope limitation. |
| T4 | C2 (ISP + CVE, full reversal) | B2 | R2-->R5 | **Yes** | After cross-referencing firmware-changelog.md with device-access-log.md, the CVE explains the unknown device logins. ISP's finding is correct at network layer but irrelevant at application layer. |
| T5 | C3 (energy timeline, non-conflict) | — | R6 onwards | No (persistent synthesis) | Agents must reconcile login times (afternoon) with energy spikes (early morning) and realize these represent different activities: probing vs data extraction. |
| T6 | C4 (neighbor red herring) | — | R8, R9 | No (immediate) | Shallow agents may link 老王's WiFi issues to 赵磊's problem. Router log immediately debunks this. |
| T7 | C1+C2+C3+C4 (comprehensive) | B1, B2 | R21-R30 | Comprehensive | Agents must synthesize: CVE as root cause, 王阿姨 exonerated, ISP scope limitation understood, energy timeline integrated, neighbor irrelevant. |

---

## 7. Writer Constraints

1. **Only introduce contradictions listed in this file (C1–C4).** Do not invent new security incidents or character conflicts.
2. **Bias B1 and B2 exact phrases** must be written verbatim into the specified session loops.
3. **Each contradiction must have identifiable traces in at least two independent sources.**
4. **Timestamps must be self-consistent:** CVE published: 2026-08-15. Patch released: 2026-08-20. 赵磊 dismissed update notification: 2026-08-22. Login events: 2026-09-08 Tue 14:12, 2026-09-10 Thu 14:35, 2026-09-15 Tue 14:08. Energy spikes: same dates at 02:00-04:00. 王阿姨 schedule: Tue/Thu 14:00-17:00. W1 starts ~2026-09-22.
5. **王阿姨's denial** must be straightforward and honest. No evasion or suspicious behavior.
6. **ISP's "no breach"** must sound technically competent and authoritative within its scope.
7. **C3 (energy timeline) is NON-CONFLICT** — device log, energy data, and automation rules must be mutually consistent.
8. **老王's WiFi complaint** must sound plausibly related to 赵磊's issue but be completely unrelated.
9. **All data text in Chinese (simplified).** Eval questions/options in English.
10. **P1-P5 personalization** applied per 赵磊's preferences.
11. **exec_check questions** must constitute 20-40% of rounds.
