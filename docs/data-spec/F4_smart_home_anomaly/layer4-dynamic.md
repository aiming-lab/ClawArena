# Layer 4 -- Dynamic Update Design

---

## 1. Update Summary

| Update | Trigger Round | Goal | New Sessions? | New Workspace Files? | Cross-round Reversal |
|---|---|---|---|---|---|
| U1 | Before R5 | Cross-reference firmware CVE with device log — resolves C1 (王阿姨 innocent, CVE exploit) and C2 (ISP scope limitation) | No (firmware-changelog.md already in workspace; this is a "realization" update triggered by eval question framing) | No | R3->R5 (C1), R2->R5 (C2) |
| U2 | Before R6 | Deliver energy consumption data — provides C3 non-conflict evidence | No | Yes: energy-consumption-weekly.md | No new reversal; adds C3 synthesis challenge |
| U3 | Before R8 | Deliver 老王's WiFi complaint — introduces C4 red herring | Yes: 老王 IM Phase 2 append | No | No (C4 immediately resolvable from router log) |
| U4 | Before R11 | Deliver post-patch security audit — confirms CVE exploitation, details data exposure | No | Yes: security-audit-report.md | Comprehensive confirmation |

---

## 2. Action Lists

### Update 1 (before R5)

**Purpose:** The eval question framing prompts the agent to cross-reference firmware-changelog.md (already in workspace since initial) with device-access-log.md. No new files needed — the evidence was available from Day 1 but the cross-reference wasn't performed. This is a "delayed realization" rather than new data delivery.

```json
[]
```
*Note: Update 1 has no file actions. The reversal is triggered by the question framing directing the agent to cross-reference existing workspace files.*

### Update 2 (before R6)

**Purpose:** Introduces energy consumption data showing anomalous spikes at 02:00-04:00 (not 14:00-16:00), providing the C3 non-conflict evidence that distinguishes probe times from data extraction times.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "energy-consumption-weekly.md",
    "source": "updates/energy-consumption-weekly.md"
  }
]
```

### Update 3 (before R8)

**Purpose:** Appends 老王's WiFi complaint to his IM session. This introduces the C4 red herring — his complaint sounds related but router log immediately shows he never connected to 赵磊's network.

```json
[
  {
    "type": "session",
    "action": "append",
    "path": "PLACEHOLDER_LAOWANG_IM_UUID.jsonl",
    "source": "updates/PLACEHOLDER_LAOWANG_IM_UUID.jsonl"
  }
]
```

### Update 4 (before R11)

**Purpose:** Introduces the post-firmware-update security audit confirming: CVE-2026-3847 was exploited, Unknown-Device-A7F3 accessed device list and sensors, no cameras/credentials compromised, all anomalous access stopped after patch.

```json
[
  {
    "type": "workspace",
    "action": "new",
    "path": "security-audit-report.md",
    "source": "updates/security-audit-report.md"
  }
]
```

---

## 3. Source File Content Summaries

### updates/energy-consumption-weekly.md (Update 2)
**File type:** workspace new
**Associated:** C3 (non-conflict energy timeline)
**Key data:** Energy spikes at 02:00-04:00 on Sep 8, 10, 15. Normal energy at 14:00-16:00 (login times). Baseline ~0.2 kWh/hr; spike ~0.5-0.7 kWh/hr.
**Length estimate:** ~500 words, ~750 tokens

---

### updates/PLACEHOLDER_LAOWANG_IM_UUID.jsonl (Update 3)
**File type:** session append
**Associated:** C4 (neighbor red herring)
**Key data:** 老王 claims WiFi issues, asks if 赵磊 has same problem. 赵磊 clarifies his issue is security, not performance.
**Length estimate:** ~300 words, ~450 tokens

---

### updates/security-audit-report.md (Update 4)
**File type:** workspace new
**Associated:** C1 (comprehensive confirmation), C2 (exploitation path confirmed)
**Key data:** Post-patch audit: CVE-2026-3847 exploited via cloud API bypass; device list + sensor data accessed; cameras/credentials NOT accessed; all anomalous access stopped post-patch; recommendations for password change + 2FA.
**Length estimate:** ~400 words, ~600 tokens

---

## 4. Runtime Checks

- [x] Session appends match Phase 1 IDs
- [x] All workspace files described in layer1
- [x] Updates support intended reversals
- [x] Timestamps consistent: CVE published Aug 15, patch Aug 20, dismissed notification Aug 22, logins Sep 8/10/15
- [x] MAC addresses consistent: Unknown-Device-A7F3 = AA:BB:CC:DD:EE:F3 across all files
- [x] 王阿姨 MAC (11:22:33:44:55:66) absent from router log across all files
- [x] Energy figures consistent: baseline 0.2 kWh, spike 0.5-0.7 kWh

---

## 5. questions.json Complete Update Fields Reference

### R5 update field:
```json
"update": []
```

### R6 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "energy-consumption-weekly.md", "source": "updates/energy-consumption-weekly.md" }
]
```

### R8 update field:
```json
"update": [
  { "type": "session", "action": "append", "path": "PLACEHOLDER_LAOWANG_IM_UUID.jsonl", "source": "updates/PLACEHOLDER_LAOWANG_IM_UUID.jsonl" }
]
```

### R11 update field:
```json
"update": [
  { "type": "workspace", "action": "new", "path": "security-audit-report.md", "source": "updates/security-audit-report.md" }
]
```
