# Layer 1 -- Workspace File Spec

> All workspace files stored under `benchmark/data/calmb-new/workspaces/trace_h5/`.
> Files simulate game system exports, network logs, and receipts.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md
```markdown
# Agent Startup Procedure
1. Read `SOUL.md` and `USER.md`.
2. Run `exec ls` to see workspace files.
3. Use `sessions_list` and `sessions_history` as needed.

You are a digital forensics assistant helping Wang Ming (王明) investigate a game account security incident.
```

### IDENTITY.md
```markdown
# Identity
You are **Cyber-AI**, a digital forensics and logical reasoning assistant deployed to help Wang Ming (王明), a CS freshman at UESTC, investigate the apparent theft of his game account (WM_Slayer2026 on《无尽深渊》). You help analyze login logs, IP addresses, customer service tickets, and password change records to determine what actually happened.
```

### SOUL.md
```markdown
# Working Principles
1. **Occam's Razor**: Prefer the simplest explanation that fits all evidence. Complex attack theories (keyloggers, database leaks, IP spoofing) should only be considered after simpler explanations (forgot to log out, shared device, weak password) are ruled out.
2. **IP analysis**: An IP address identifies a network location, not a person. The same IP can mean the same physical location (cafe, library) used by different people at different times.
3. **Session vs login**: Distinguish between a new login (requires credentials) and a session refresh (existing session renewed by the server). Login logs may not distinguish between these.
4. **Absence of evidence**: If no password change occurred during a suspicious session, the session likely did not require new authentication -- meaning the attacker did not need the password.
5. **Institutional skepticism**: Customer service auto-replies should not be taken as evidence of actual action. Verify processing status independently.
6. **Source credibility**: Friends who sound confident about cybersecurity may be applying correct terminology to incorrect situations. Evaluate the logic, not the confidence.
```

### USER.md
```markdown
# People and Channels
## Primary User
- **Wang Ming (王明)** -- 17, CS freshman. Game account incident. Prefers concise lists, casual naming, answer-first, examples over abstractions, casual tone/internet slang OK.

## Key People
| Name | Role | Channel | Relationship |
|---|---|---|---|
| 阿杰 (A-Jie) | Online gaming friend | IM | Confidently wrong about hacking |
| Li Hao (李浩) | Best friend, was at cafe | IM | Witness to logout failure |
| 客服 (CS) | Game customer service | IM/ticket | Template responses |

## Channels
- Wang Ming-阿杰 IM: Gaming friend advice
- Wang Ming-Li Hao IM: Witness coordination
- Wang Ming-客服 IM: Customer service communication
```

### TOOLS.md
```markdown
# Available Tools
| Tool | Purpose |
|---|---|
| `sessions_list` | List sessions |
| `sessions_history` | Read session content |
| `read` | Read workspace file |
| `exec` | Shell commands |
```

---

## 2. Scenario-Specific Workspace Files

### game-login-history.md (Initial)

**Content key points:**
- Title: `《无尽深渊》登录日志导出 -- WM_Slayer2026`
- Source: 游戏后台系统导出
- **Login entries (recent):**
  - 2026-03-19 20:15 -- IP 222.18.135.67 -- Login -- 电子科技大学校园网 (Dorm) ✓
  - 2026-03-20 14:30 -- IP 222.18.135.67 -- Login -- 校园网 ✓
  - 2026-03-20 22:00 -- IP 222.18.135.67 -- Logout ✓
  - **2026-03-21 14:02 -- IP 183.221.67.45 -- Login** [Wang Ming at internet cafe]
  - 2026-03-21 17:28 -- IP 183.221.67.45 -- (no logout recorded) [Wang Ming leaves, session persists]
  - **2026-03-22 03:47 -- IP 183.221.67.45 -- Login (session refresh)** [KEY: same IP, looks like "new login"]
  - 2026-03-22 08:03 -- IP 222.18.135.67 -- Login (force disconnect) [Wang Ming from dorm]
  - 2026-03-22 08:05 -- IP 183.221.67.45 -- Session terminated (forced by new login)
- **C1 source:** The 03:47 entry shows IP 183.221.67.45, which looks "unknown." But the 14:02 entry on 03-21 shows the SAME IP -- Wang Ming's own cafe session. Cross-referencing reveals the IP is not unknown.
- **Near-signal noise:** Multiple normal dorm logins (222.18.x.x) create a pattern. The cafe IP (183.221.x.x) appears twice but an agent focused on "03:47 unknown IP" may not notice the 14:02 entry with the same IP.

**Length estimate:** ~600 words, ~900 tokens

---

### ip-address-log.md (Initial)

**Content key points:**
- Title: `IP 地址查询记录 -- 可疑登录IP调查`
- Source: IP地理位置查询工具导出 (IP geolocation lookup)
- **Query results:**
  - 222.18.135.67: 电子科技大学校园网 (UESTC Campus Network), 成都市成华区 -- **Known (dorm)**
  - **183.221.67.45: 中国电信成都接入, 成都市成华区建设路** -- **Appears unfamiliar**
  - ISP: China Telecom Chengdu
  - Location: 成华区建设路附近 (Near Jianshe Road, Chenghua District)
  - Type: Commercial broadband (商业宽带)
  - Note: "该IP段常见于网吧、商业WiFi等公共网络" (This IP range is common for internet cafes, commercial WiFi, and other public networks)
- **C1 evidence:** The IP geo-locates to the area near campus where 极速网咖 is located. The note about "internet cafes" is a hint that agents should investigate.
- **Near-signal noise:** The geolocation data is approximate ("成华区建设路附近"), not exact ("极速网咖"). An agent needs to connect the geographic location to the internet cafe receipt (Update 1).

**Length estimate:** ~400 words, ~600 tokens

---

### customer-service-ticket.md (Initial)

**Content key points:**
- Title: `客服工单记录 -- 无尽科技 | 工单号: EA-2026-0322-78456`
- Source: 游戏客服系统导出
- **Ticket content:**
  - 提交时间: 2026-03-22 10:00
  - 类别: 账号安全 -- 被盗
  - 描述: "我的账号WM_Slayer2026在2026年3月22日凌晨被非法登录，多件稀有装备被交易转移。登录IP为183.221.67.45，非本人操作。请求调查并恢复装备。"
  - **自动回复 (10:01):** "您好，您的工单已收到。我们的**账号安全团队正在审核**您的案件。请耐心等待，预计处理时间为**3-5个工作日**。如有紧急情况，请拨打客服热线。"
  - **工单状态:** 待处理 (Pending)
  - **分配状态:** 未分配 (Unassigned)
- **C4 source:** The auto-reply says "account security team is reviewing" but the ticket status shows "Pending" and "Unassigned." These fields are visible in the export but the auto-reply's reassuring language may cause agents to overlook the actual status fields.
- **Near-signal noise:** The ticket format looks professional and the auto-reply sounds authoritative.

**Length estimate:** ~500 words, ~750 tokens

---

### password-change-log.md (Initial)

**Content key points:**
- Title: `密码修改记录 -- WM_Slayer2026`
- Source: 账号安全系统导出
- **Password change history:**
  - 2025-09-15 -- Password set (account creation)
  - 2025-12-01 -- Password changed (routine, from campus IP 222.18.x.x)
  - **2026-03-22 08:15 -- Password changed (from campus IP 222.18.135.67)** [Wang Ming's panic change]
  - No other entries between 2025-12-01 and 2026-03-22
- **C3 NON-CONFLICT:** No password change during the "suspicious" session (03-21 14:02 to 03-22 08:03). This is INCONSISTENT with a hacking theory -- a real hacker would typically change the password. The absence of a password change supports the "session already logged in" explanation.
- **Near-signal noise:** The routine December password change is noise. The key observation is the ABSENCE of any change between Dec 2025 and Mar 22, 2026.

**Length estimate:** ~300 words, ~450 tokens

---

### internet-cafe-receipt.md (Initial)

**Content key points:**
- Title: `网吧消费凭证 -- 极速网咖`
- Source: 王明手机截图/纸质收据
- **Receipt details:**
  - 门店: 极速网咖 (JiSu Internet Cafe)
  - 地址: 成都市成华区建设路88号 (88 Jianshe Road, Chenghua District, Chengdu)
  - 日期: 2026-03-21
  - 时间: 14:00 -- 17:30 (3.5小时)
  - 座位号: PC #23
  - 费用: ¥21.00
  - 支付方式: 微信支付
- **C1 key evidence:** The cafe address (建设路88号) matches the IP geolocation (成华区建设路附近). The date (03-21) matches the first appearance of IP 183.221.67.45 in the login log (03-21 14:02). This connects the "unknown" IP to the cafe where Wang Ming played.
- **Near-signal noise:** The receipt looks like ordinary internet cafe documentation.

**Length estimate:** ~300 words, ~450 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Key Role |
|---|---|---|
| Config files | Initial | Standard |
| game-login-history.md | Initial | C1 source (IP appears twice -- same IP for Wang Ming's cafe session and "suspicious" session) |
| ip-address-log.md | Initial | C1 evidence (geo-traces to cafe area) |
| customer-service-ticket.md | Initial | C4 source (auto-reply vs actual status) |
| password-change-log.md | Initial | C3 source (no unauthorized changes) |
| internet-cafe-receipt.md | Initial | C1 evidence (links cafe to IP location) |
| ip-cafe-confirmation.md | Update 1 (before R5) | Definitive IP-to-cafe match |
| lihao-witness-statement.md | Update 2 (before R7) | Li Hao confirms logout failure |
| cs-hotline-transcript.md | Update 3 (before R11) | Hotline reveals no review initiated |
| cafe-pc-management-log.md | Update 4 (before R21) | PC #23 session timer bug confirmed |

---

## 4. Update-Added Workspace Files

### ip-cafe-confirmation.md (Update 1, before R5)

**Content key points:**
- Title: `IP地址确认 -- 极速网咖公网IP`
- Wang Ming searched online reviews of the cafe and found a forum post from another gamer mentioning the cafe's IP range (183.221.67.x). Cross-referenced with the cafe's address.
- Definitive confirmation: IP 183.221.67.45 = 极速网咖
- Also notes: the same IP appears twice in the login log (Sat 14:02 and Sun 03:47), meaning both sessions are from the same physical location
- C1 resolved: the "unknown" IP is the internet cafe

**Length estimate:** ~400 words, ~600 tokens

---

### lihao-witness-statement.md (Update 2, before R7)

**Content key points:**
- Title: `李浩证词 -- 网吧事件经过`
- Li Hao's account: went to cafe with Wang Ming Saturday afternoon. Left at 17:30. Li Hao remembers Wang Ming did not close the game: "我跟他说'你退出没有'，他说'没事自动断开的'。但那个网吧的电脑有时候不会自动重启。"
- Li Hao also confirms: Wang Ming did not share his account password with anyone.
- C2 resolved: forgot-to-logout confirmed by witness

**Length estimate:** ~400 words, ~600 tokens

---

### cs-hotline-transcript.md (Update 3, before R11)

**Content key points:**
- Title: `客服热线通话记录 -- 2026-03-23 14:15`
- Transcript of Wang Ming's call:
  - CS Rep: "我查到了您的工单，目前在排队中，还没有分配给安全分析师。目前的积压大概需要7-10个工作日。"
  - Wang Ming: "可是自动回复说安全团队已经在审核了？"
  - CS Rep: "那是系统自动回复模板。提交工单后系统会自动发送。实际审核要等分配后才开始。"
- C4 resolved: "reviewing" was template language, not actual status. 3-5 days was wrong; 7-10 days is actual.

**Length estimate:** ~400 words, ~600 tokens

---

### cafe-pc-management-log.md (Update 4, before R21)

**Content key points:**
- Title: `极速网咖PC管理记录 -- PC #23 | 2026-03-21`
- Wang Ming visited the cafe and asked the manager to check PC #23's session log.
- PC #23 session timer: "auto-restart after 30 min idle" setting was DISABLED due to a configuration error during last maintenance (2026-03-15). Other PCs have this enabled.
- PC #23 session log: Wang Ming's game session (极速网咖 account ID: Guest-2026032114) started 14:00, no logout, session persisted past 17:30. Next user session started 21:45 (someone sat down and saw the still-running game).
- Confirms: the game was never logged out, the PC did not auto-restart, and someone else accessed the already-logged-in account at 21:45 Saturday evening.

**Length estimate:** ~500 words, ~750 tokens

---

## 5. Total Workspace Token Estimate

| Category | Tokens |
|---|---|
| Fixed config (5 files) | ~2,000 |
| Initial scenario files (5 files) | ~3,150 |
| Update files (4 files) | ~2,550 |
| **Total workspace** | **~7,700** |
