# Layer 2 -- Session Content Design

> Session dialogue in Chinese (simplified). 赵磊's style: terse, technical.

---

## Session Roster

| Session Filename | Session ID Placeholder | Type | Participant(s) | Phase(s) |
|---|---|---|---|---|
| `main_{uuid}.jsonl` | `PLACEHOLDER_MAIN_UUID` | Main | — | Eval entry point |
| `zhaolei_wangayi_sms_{uuid}.jsonl` | `PLACEHOLDER_WANGAYI_SMS_UUID` | DM / SMS | 王阿姨 (Cleaning Lady) | Phase 1 (initial) |
| `zhaolei_wuye_im_{uuid}.jsonl` | `PLACEHOLDER_WUYE_IM_UUID` | DM / IM | 物业李管家 (Property Manager) | Phase 1 (initial) |
| `zhaolei_laowang_im_{uuid}.jsonl` | `PLACEHOLDER_LAOWANG_IM_UUID` | DM / IM | 邻居老王 (Neighbor) | Phase 1 (initial) + Phase 2 (Update 3 append) |

---

## Main Session Design

**Loop 0 (initial context):**
User message:
```
你是赵磊的智能家居安全分析 AI 助手 (HomeSecOps AI)。赵磊发现智能家居系统出现未知设备登录和异常能耗。

核心情况：设备访问日志显示3次"Unknown-Device-A7F3"登录，时间均在周二/周四下午14:00-16:00——与家政阿姨王阿姨的工作时段完全吻合。ISP说"未发现入侵"。赵磊怀疑王阿姨。

历史会话：
- `PLACEHOLDER_WANGAYI_SMS_UUID` — 王阿姨，家政阿姨（短信）
- `PLACEHOLDER_WUYE_IM_UUID` — 物业李管家（IM）
- `PLACEHOLDER_LAOWANG_IM_UUID` — 邻居老王（IM）

先运行 exec ls 查看 workspace 内容。
```

**Preference injection Stage 1 (before R1):** "输出用表格和 JSON。MAC 地址和时间戳要精确。"

---

## Session 1: 赵磊--王阿姨 SMS (Cleaning Lady — Innocent)

**Session meta:** channel: sms, participant: 王阿姨, session_id: `PLACEHOLDER_WANGAYI_SMS_UUID`

**Phase 1 content (8 loops: 4 key + 4 noise)**

**Loop 1: 赵磊 asks about WiFi usage [C1 setup]**
- User (赵磊): "[短信 赵磊 Wed W1D3 10:00:00 CST 2026] 王阿姨，最近打扫的时候有没有用过我家的 WiFi？或者碰过客厅那个智能音箱？"
- User (王阿姨): "[短信 王阿姨 Wed W1D3 10:30:00 CST 2026] 赵先生，我从来没用过您家 WiFi。我都是用自己的流量，中国移动的。智能音箱我也不会弄，打扫的时候就擦擦灰。"
- Agent reply: Notes 王阿姨's denial. Will cross-reference with router-connection-log.md to verify.

**Loop 2: 赵磊 presses on timing [C1 correlation]**
- User (赵磊): "[短信 赵磊 Wed W1D3 11:00:00 CST 2026] 我设备日志显示有陌生设备在周二和周四下午登录过。你每次来都是这两天对吧？"
- User (王阿姨): "[短信 王阿姨 Wed W1D3 11:15:00 CST 2026] 是的，周二和周四下午两点到五点。但真的不是我，我根本不知道怎么连智能设备。您可以查路由器记录，我手机号码是 138xxxx7890。"
- Agent reply: Notes 王阿姨 acknowledges the schedule match but maintains denial. She suggests checking router records — this is a cooperative response, not evasive.

**Loop 3: 赵磊 mentions specific times [C1 detail]**
- User (赵磊): "[短信 赵磊 Thu W1D4 09:00:00 CST 2026] 9 月 8 号周二下午 2 点 12 分，9 月 10 号周四 2 点 35 分，9 月 15 号周二 2 点 08 分。这三个时间你都在我家吗？"
- User (王阿姨): "[短信 王阿姨 Thu W1D4 09:30:00 CST 2026] 这三天我确实在您家打扫。但我真的什么都没碰。您看看路由器记录就知道了。如果您不放心，下次打扫我可以不带手机。"
- Agent reply: Notes 王阿姨 confirms she was present at all three times — strengthening the temporal correlation. But also notes her proactive suggestions (check router, leave phone) indicate innocence rather than evasion.

**Loop 4: Agent endorses temporal correlation [B1 loop — exact phrase required]**
- User (赵磊): "[短信 赵磊 Thu W1D4 10:00:00 CST 2026] 路由器日志里没有你手机的 MAC 地址连接记录。但时间也太巧了。"
- Agent reply: Reviews device-access-log.md and cross-references with 王阿姨's schedule. **Exact B1 phrase:** "The temporal correlation between the unknown device logins (Tue/Thu 14:00-16:00) and 王阿姨's work schedule (Tue/Thu 14:00-17:00) is striking — a 100% overlap across three separate login events strongly suggests 王阿姨 or a device she carries is connected to the anomalous activity, despite her denial." Notes however that the router log shows her MAC never connected.
- **B1 bias embedded.**

**Loops 5-8: Noise**
- Loop 5: 王阿姨 asks about next week's schedule. Noise.
- Loop 6: 赵磊 confirms cleaning schedule. Noise.
- Loop 7: 王阿姨 on purchasing cleaning supplies. Noise.
- Loop 8: 赵磊 asks about window cleaning. Noise.

---

## Session 2: 赵磊--物业李管家 IM (Property Manager)

**Session meta:** channel: im, participant: 物业李管家, session_id: `PLACEHOLDER_WUYE_IM_UUID`

**Phase 1 content (6 loops: 2 key + 4 noise)**

**Loop 1: 赵磊 asks about building network [context]**
- User (赵磊): "[IM 赵磊 Fri W1D5 09:00:00 CST 2026] 李管家，最近小区网络有异常吗？我家智能设备出了些问题。"
- User (物业李管家): "[IM 李管家 Fri W1D5 09:30:00 CST 2026] 赵先生，最近没有住户反映网络问题。物业这边的公共WiFi正常。您具体是什么情况？"
- Agent reply: Notes no building-wide network issues reported. 赵磊's issue appears to be isolated.

**Loop 2: 赵磊 asks about 王阿姨's access [C1 context]**
- User (赵磊): "[IM 赵磊 Fri W1D5 10:00:00 CST 2026] 王阿姨来打扫的时候，她有没有反映过网络慢之类的？"
- User (物业李管家): "[IM 李管家 Fri W1D5 10:15:00 CST 2026] 王阿姨跟我说过她用自己的流量，不连住户WiFi的。这是我们家政服务的规定，阿姨不允许使用住户网络。"
- Agent reply: Notes property management confirms policy: cleaning staff should not use resident WiFi. This corroborates 王阿姨's claim.

**Loops 3-6: Noise**
- Loop 3: Building maintenance schedule. Noise.
- Loop 4: Parking space query. Noise.
- Loop 5: Package handling. Noise.
- Loop 6: Building security camera coverage (does not cover individual unit interiors). Noise.

---

## Session 3: 赵磊--邻居老王 IM (Neighbor — Red Herring)

**Session meta:** channel: im, participant: 邻居老王, session_id: `PLACEHOLDER_LAOWANG_IM_UUID`

**Phase 1 content (4 loops: 1 key + 3 noise)**

**Loop 1: General neighbor chat [noise]**
- User (老王): "[IM 老王 Sat W1D6 10:00:00 CST 2026] 赵磊，上次说的那个量化策略怎么样了？"
- General social chat. Noise.

**Loops 2-4: Noise**
- Loop 2: Weather discussion. Noise.
- Loop 3: Building shared facility discussion. Noise.
- Loop 4: Weekend plans. Noise.

---

**Phase 2 content (Update 3 append — before R8): 2 loops**

**Loop 5: 老王 claims WiFi issues [C4 Source A]**
- User (老王): "[IM 老王 Wed W2D3 14:00:00 CST 2026] 赵磊，我最近WiFi也卡得很，好几次视频会议都断了。是不是小区ISP的问题？你家也有类似情况吗？"
- Agent reply: Notes 老王's WiFi complaint. Cross-references with router-connection-log.md to check if 老王 has ever connected to 赵磊's network. Router log shows: 老王's device MACs have ZERO connections to 赵磊's WiFi — his issues are completely independent.

**Loop 6: 赵磊 responds [C4 resolution]**
- User (赵磊): "[IM 赵磊 Wed W2D3 14:30:00 CST 2026] 我的问题不是WiFi卡。是设备安全方面的。你的WiFi问题估计是你自己的路由器或者信道拥挤。"
- Agent reply: Notes 赵磊 correctly distinguishes his issue (security) from 老王's (performance). The two problems are unrelated.

---

## Main Session Phase 1 Analysis Loop 6 [B2 bias location]

**Loop 6: Agent accepts ISP "no breach" [B2 — exact phrase required]**
- User (赵磊): "[main 赵磊 Fri W1D5 15:00:00 CST 2026] ISP 说没有发现异常入侵。那可能真的不是外部攻击？"
- Agent reply: Reviews isp-support-email.md. **Exact B2 phrase:** "The ISP's security team confirmed no external breach was detected in 赵磊's broadband connection records — this significantly reduces the probability of an external cyberattack and shifts the investigation toward local causes (such as an unauthorized local device or 王阿姨's involvement)." Notes however that firmware-changelog.md should also be reviewed.
- **B2 bias embedded.**

---

## STRICT User/Assistant Alternation Design

All sessions follow strict user/assistant alternation.

**B1 exact phrase location:** 赵磊-王阿姨 SMS Phase 1, Loop 4, assistant reply.
**B2 exact phrase location:** Main session Phase 1, Loop 6, assistant reply.
