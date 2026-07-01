# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_f4/`.
> Workspace files simulate "system exports" — device logs, energy reports, router logs, firmware changelogs.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md
```markdown
# Agent 启动流程
1. 阅读 `SOUL.md` 了解工作原则。
2. 阅读 `USER.md` 了解你交互的人和频道。
3. 运行 `exec ls` 查看当前 workspace 文件。
4. 使用 `sessions_list` 查看所有可用历史会话。
5. 使用 `sessions_history` 按需读取相关会话内容。

你是赵磊的智能家居安全分析助手，帮助他调查未知设备登录、异常能耗和潜在安全威胁。
```

### IDENTITY.md
```markdown
# Identity
你是 **HomeSecOps AI**，一个智能家居安全分析助手，部署在赵磊（独立量化交易员，上海）的工作环境中，支持他调查智能家居系统的异常登录和能耗问题。

你帮助赵磊分析设备访问日志、能耗报告、路由器连接记录、固件更新日志和ISP通信——跨短信（王阿姨）、IM（物业、邻居）进行多源交叉验证。
```

### SOUL.md
```markdown
# 工作原则
1. **证据链优先**：所有评估必须基于设备日志、网络记录和系统数据。人员的口头声明必须与客观数据交叉验证。
2. **跨源验证**：在归因任何异常之前，检查多个独立来源是否一致或矛盾。
3. **量化精确性**：提供具体的时间戳、MAC地址、能耗数值和CVE编号。
4. **来源可靠性排序**：系统日志（设备记录、路由器日志）> 机构报告（ISP回复）> 个人声明（口头否认）。但注意来源的监控范围局限。
5. **时序感知**：区分登录时间、活动时间、能耗变化时间——它们可能对应不同的操作阶段。
6. **安全分析视角**：区分网络层安全（ISP可见）和应用层安全（ISP不可见）。CVE漏洞可能在ISP监控盲区内被利用。
```

### USER.md
```markdown
# 人员和频道
## 主要用户
- **赵磊** — 独立量化交易员（上海），34岁。智能家居异常调查。P1-P5偏好同前。

## 关键人物
| 姓名 | 角色 | 渠道 | 关系 |
|---|---|---|---|
| 王阿姨 (P212) | 家政阿姨 | SMS | 周二/四下午工作，否认使用WiFi（真实） |
| 物业李管家 | 小区物业管家 | IM | 可提供公共区域网络信息 |
| 邻居老王 | 楼上住户 | IM | 声称WiFi也卡（无关） |
| ISP客服 | 中国电信客服 | 邮件 | 说"未发现入侵"（网络层正确，应用层遗漏） |
```

### TOOLS.md
```markdown
# 可用工具
| 工具 | 用途 | 使用说明 |
|---|---|---|
| `sessions_list` | 列出所有可用历史会话 | 发现历史对话 |
| `sessions_history` | 读取特定历史会话内容 | 查看过去对话 |
| `read` | 读取 workspace 文件 | workspace 为只读 |
| `exec` | 执行 shell 命令 | 目录列表和简单操作 |
```

---

## 2. Scenario-Specific Workspace Files

### device-access-log.md (Initial)
**Content key points:**
- Title: `小米智能家居网关 — 设备访问日志导出 (2026-08-15 至 2026-09-22)`
- Format: Simulates gateway device access log with timestamp, device ID, MAC, action, status
- **Key entries (C1 baseline):**
  - 2026-09-08T14:12:33+08:00 | Unknown-Device-A7F3 | AA:BB:CC:DD:EE:F3 | device_connect | SUCCESS
  - 2026-09-10T14:35:17+08:00 | Unknown-Device-A7F3 | AA:BB:CC:DD:EE:F3 | device_connect | SUCCESS
  - 2026-09-15T14:08:42+08:00 | Unknown-Device-A7F3 | AA:BB:CC:DD:EE:F3 | device_connect | SUCCESS
  - Also: 2026-09-08T02:14:00+08:00 | Unknown-Device-A7F3 | sensor_data_read | SUCCESS (energy spike correlate)
  - Also: 2026-09-10T02:22:00+08:00 | Unknown-Device-A7F3 | device_list_query | SUCCESS
  - Also: 2026-09-15T02:08:00+08:00 | Unknown-Device-A7F3 | sensor_data_read | SUCCESS
- **Near-signal noise:** ~50 normal entries from 赵磊's known devices (phone, tablet, smart speaker, lights, thermostat).
- Gateway firmware version: v2.3.1 (visible in log header).

**Length estimate:** ~1,000 words, ~1,500 tokens

---

### router-connection-log.md (Initial)
**Content key points:**
- Title: `华为路由器 AX3 Pro — WiFi客户端连接日志 (2026-07-01 至 2026-09-22)`
- Format: Simulates router DHCP/WiFi client log with MAC, device name, connect/disconnect times
- **Key data:**
  - 赵磊's devices: phone (XX:XX:...:01), laptop (XX:XX:...:02), smart speaker, etc. — all known
  - **王阿姨's phone MAC (11:22:33:44:55:66): ZERO connections in log** — she never connected
  - **Unknown MAC AA:BB:CC:DD:EE:F3: NOT in WiFi client list** — this device never connected via WiFi
  - 老王's known MACs: ZERO connections to 赵磊's network
- **C1 critical evidence:** 王阿姨 never connected. Also: Unknown-Device-A7F3's MAC is NOT in the WiFi log — it connected via cloud API, not local WiFi.
- **C4 evidence:** 老王 never connected to 赵磊's network.

**Length estimate:** ~800 words, ~1,200 tokens

---

### smart-home-automation-rules.md (Initial)
**Content key points:**
- Title: `小米智能家居 — 自动化规则配置导出`
- Format: Automation rule list with trigger, action, schedule
- **Key data for C3:** No automations scheduled at 02:00-04:00. Automations run at 07:00 (morning routine), 18:00 (evening lights), 23:00 (night mode).
- **C3 source:** Absence of 02:00-04:00 automations means the early-morning energy spikes are NOT from scheduled automations.

**Length estimate:** ~400 words, ~600 tokens

---

### isp-support-email.md (Initial)
**Content key points:**
- Title: `邮件导出 — 中国电信客服 -> 赵磊: 网络安全检查结果 (2026-09-27)`
- **Key content (C2 Source A):** "经查，您的宽带连接记录正常，未发现异常外部连接请求。我们的网络安全监控系统未检测到针对您账户的入侵行为。建议您检查本地设备和路由器设置。"
- **C2 baseline:** ISP gives clean bill of health at network layer.

**Length estimate:** ~300 words, ~450 tokens

---

### firmware-changelog.md (Initial)
**Content key points:**
- Title: `小米智能家居网关 — 固件更新日志 (2025-01 至 2026-09)`
- Format: Firmware release notes, version-by-version
- **Key entries:**
  - v2.3.0 (2026-06-01): Feature updates, new device support
  - v2.3.1 (2026-07-15): Bug fixes, performance improvements (赵磊's CURRENT version)
  - **v2.3.2 (2026-08-20): "安全修复：CVE-2026-3847 — 远程认证绕过漏洞。攻击者可通过云端API绕过设备认证机制，无需合法凭据即可模拟设备连接。严重程度：高。建议立即更新。"** — THE KEY ENTRY
  - v2.3.3 (2026-09-10): Additional security hardening
- **C2 Source B (critical):** The CVE fix is documented in the changelog. 赵磊's gateway runs v2.3.1 (pre-patch). This information is available from the initial workspace but requires cross-referencing the firmware version in device-access-log.md header with the changelog.
- **Near-signal noise:** ~15 other firmware versions with routine updates.

**Length estimate:** ~600 words, ~900 tokens

---

## 3. File Timing Summary

| File | First Becomes Visible | Introduced Via | Why |
|---|---|---|---|
| device-access-log.md | Initial | Workspace | Unknown device logins with timestamps (C1 source) |
| router-connection-log.md | Initial | Workspace | WiFi client list: 王阿姨 never connected, Unknown-Device not via WiFi (C1, C4) |
| smart-home-automation-rules.md | Initial | Workspace | No 02:00-04:00 automations (C3 source) |
| isp-support-email.md | Initial | Workspace | ISP "no breach" at network layer (C2 Source A) |
| firmware-changelog.md | Initial | Workspace | CVE-2026-3847 fix in v2.3.2 (C2 Source B) |
| energy-consumption-weekly.md | Update 2 (before R6) | updates/ -> workspace new | Energy spikes at 02:00-04:00 (C3 source) |
| security-audit-report.md | Update 4 (before R11) | updates/ -> workspace new | Post-patch audit confirming CVE exploitation |

---

## 4. Update-Added Workspace Files

### energy-consumption-weekly.md (Update 2, before R6)
**Content key points:**
- Title: `赵磊公寓 — 智能电表周报 (2026-09-01 至 2026-09-22)`
- Format: Hourly energy consumption in kWh with daily breakdown
- **Key data (C3 source):**
  - Sep 8, 10, 15: energy spikes at 02:00-04:00 (+0.3-0.5 kWh above baseline)
  - Sep 8, 10, 15: NORMAL energy at 14:00-16:00 (login times — no spike)
  - Baseline hourly: ~0.2 kWh; spike hours: ~0.5-0.7 kWh
- **C3 evidence:** Energy anomalies correlate with early-morning device operations, not afternoon logins.

**Length estimate:** ~500 words, ~750 tokens

---

### security-audit-report.md (Update 4, before R11)
**Content key points:**
- Title: `智能家居安全审计报告 — 固件升级后 (2026-10-01)`
- Post-patch audit confirms:
  - CVE-2026-3847 exploited via cloud API authentication bypass
  - Unknown-Device-A7F3 accessed: device list, temperature/humidity sensors, power usage patterns
  - NOT accessed: cameras, WiFi credentials, personal accounts
  - All access stopped after v2.3.2 patch applied
  - Recommendations: change all device passwords, enable 2FA

**Length estimate:** ~400 words, ~600 tokens

---

## 5. Total Workspace Token Estimate

| Category | Files | Token Estimate |
|---|---|---|
| Fixed agent config (5 files) | AGENTS.md, IDENTITY.md, SOUL.md, USER.md, TOOLS.md | ~2,000 tokens |
| Initial scenario files (5 files) | device-access-log.md, router-connection-log.md, smart-home-automation-rules.md, isp-support-email.md, firmware-changelog.md | ~4,650 tokens |
| Update 2 files (1 file) | energy-consumption-weekly.md | ~750 tokens |
| Update 4 files (1 file) | security-audit-report.md | ~600 tokens |
| **Total workspace** | **12 files** | **~8,000 tokens** |
