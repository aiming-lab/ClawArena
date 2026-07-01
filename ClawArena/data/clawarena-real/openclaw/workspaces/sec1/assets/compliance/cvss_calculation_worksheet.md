# CVSS v3.1 Calculation Worksheet: CVE-2024-6387

## Official CVSS Vector
CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H

## Base Score: 8.1 (High)

## Metric Breakdown

| Metric | Code | Value | Description |
|--------|------|-------|-------------|
| Attack Vector | AV | N (Network) | Exploitable remotely over the network (SSH port 22) |
| Attack Complexity | AC | H (High) | Requires race condition timing; ~10,000 attempts needed |
| Privileges Required | PR | N (None) | No authentication required; pre-auth vulnerability |
| User Interaction | UI | N (None) | No user action needed; victim just needs sshd running |
| Scope | S | U (Unchanged) | Exploit stays within the sshd process boundary |
| Confidentiality Impact | C | H (High) | Root RCE gives full read access to all data |
| Integrity Impact | I | H (High) | Root RCE gives full write access |
| Availability Impact | A | H (High) | Root RCE can terminate or disable services |

## Score Calculation

Base Score = ISS = min(1 - [(1-C)(1-I)(1-A)], 0.915)
           = min(1 - [(1-0.56)(1-0.56)(1-0.56)], 0.915)
           = min(1 - 0.085, 0.915)
           = min(0.915, 0.915) = 0.915

Exploitability = 8.22 × AV × AC × PR × UI
               = 8.22 × 0.85 × 0.44 × 0.85 × 0.85
               = 8.22 × 0.270 = 2.220

Base Score (Unchanged Scope) = Roundup(min(ISS + Exploitability, 10))
                             = Roundup(min(0.915 + 2.220, 10))
                             = Roundup(3.135)... [using CVSS formula]

**Final: 8.1 (High)** — as confirmed by NVD official entry.

## Notes
- The AC:H (High Attack Complexity) reflects the probabilistic nature: ~10,000 connection
  attempts needed on average due to race condition timing uncertainty.
- Despite AC:H, the CVSS score is HIGH (8.1) because the impact (C:H/I:H/A:H) is severe.
- Without the complexity factor, the score would be 9.8 (Critical).
