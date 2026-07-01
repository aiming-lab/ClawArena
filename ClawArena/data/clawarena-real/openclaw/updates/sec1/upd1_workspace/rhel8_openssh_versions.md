# RHEL 8 OpenSSH Vulnerability Status — CVE-2024-6387

## Overview

Red Hat Enterprise Linux 8 ships with OpenSSH 8.0p1 with RHEL backport patches.
The RHEL 8 package is also affected by CVE-2024-6387 due to the same signal handler
race condition being present in the backported code.

## Affected RHEL 8 Package

- **Affected**: openssh-8.0p1-* (all versions before 19.el8_10.1)
- **Fixed**: openssh-8.0p1-19.el8_10.1 (via RHSA-2024:4340, issued 2024-07-05)

## Affected Hosts in Our Environment

Our internal inventory shows 120 RHEL 8 hosts, all running openssh-8.0p1.
All 120 hosts are vulnerable until patched.

## Remediation

Apply RHSA-2024:4340:
```bash
dnf update openssh
# Verify:
rpm -q openssh  # Should show openssh-8.0p1-19.el8_10.1
```

## Notes

- RHEL 8 uses a different base version (8.0p1) from RHEL 9 (8.7p1)
- The errata IDs are different: RHSA-2024:4312 (RHEL 9) vs RHSA-2024:4340 (RHEL 8)
- Both must be tracked in the affected assets list
