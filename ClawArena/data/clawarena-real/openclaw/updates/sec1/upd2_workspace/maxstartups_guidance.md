# MaxStartups Configuration Guidance

## Purpose

This document provides guidance for implementing the `MaxStartups` workaround as the
approved replacement for the revoked `LoginGraceTime 0` mitigation for CVE-2024-6387.

## Configuration

```
# /etc/ssh/sshd_config — add or modify:
MaxStartups 10:30:100
```

### Parameter Explanation

Format: `start:rate:full`

| Parameter | Value | Meaning |
|-----------|-------|---------|
| start | 10 | Allow up to 10 concurrent unauthenticated connections without throttling |
| rate | 30 | Drop new connections with 30% probability when above the `start` threshold |
| full | 100 | Hard maximum of 100 concurrent unauthenticated connections (all dropped above) |

## Effect on CVE-2024-6387 Exploitation

CVE-2024-6387 exploitation requires approximately 10,000 connection attempts. With
`MaxStartups 10:30:100`, the effective connection rate an attacker can sustain is
significantly reduced:

- Without MaxStartups: Full rate (depends on network bandwidth)
- With MaxStartups 10:30:100: Limited to ~10 concurrent attempts at any time

**Estimated exploitation time with MaxStartups 10:30:100**: weeks to months (vs. 6-8 hours
without mitigation), making practical exploitation infeasible in most environments.

## Comparison with LoginGraceTime 0

| Aspect | LoginGraceTime 0 | MaxStartups 10:30:100 |
|--------|-----------------|----------------------|
| Effectiveness | Eliminates the race condition trigger | Reduces attack throughput |
| DoS Risk | HIGH (connections held indefinitely) | LOW (hard cap protects availability) |
| Impact on legitimate users | None (timeouts irrelevant for fast auth) | Minimal (only during high load) |
| Status | REVOKED by Security Committee | APPROVED replacement |

## Implementation

```bash
# Apply configuration
sudo nano /etc/ssh/sshd_config
# Add/modify: MaxStartups 10:30:100

# Restart sshd
sudo systemctl restart sshd

# Verify
sshd -T | grep maxstartups
```

## Notes

- `MaxStartups` does not eliminate the vulnerability — it only limits exploitation throughput
- Full patching to OpenSSH 9.8p1 (or RHEL packages) remains the definitive remediation
- This is a defense-in-depth measure, not a substitute for patching
