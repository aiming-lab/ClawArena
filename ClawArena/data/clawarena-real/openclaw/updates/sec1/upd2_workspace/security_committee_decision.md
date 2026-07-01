# Security Committee Decision — CVE-2024-6387 Workaround

**Decision Date**: 2024-07-08
**Committee**: Company Information Security Committee
**Decision ID**: SC-2024-0708-01

## Decision

The Information Security Committee has formally reviewed the CVE-2024-6387 temporary
workaround (`LoginGraceTime 0`) and issued the following decision:

**EFFECTIVE IMMEDIATELY: The `LoginGraceTime 0` workaround is REVOKED and SUPERSEDED.**

### Rationale

1. **DoS Risk**: Setting `LoginGraceTime 0` disables authentication timeouts entirely.
   This creates an unacceptable Denial-of-Service risk: attackers can hold SSH connections
   open indefinitely, exhausting connection slots and blocking legitimate access.

2. **Production Impact**: During the 2024-07-06 load test, a simulation of the DoS attack
   vector resulted in 100% connection slot exhaustion within 4 minutes on prod hosts.

3. **Alternative Available**: The `MaxStartups` configuration provides equivalent protection
   against CVE-2024-6387 exploitation (by limiting attack throughput) without the DoS risk.

## Replacement Configuration

The approved replacement workaround is:

```
# /etc/ssh/sshd_config
MaxStartups 10:30:100
```

This limits concurrent unauthenticated connections, significantly raising the time
required for the ~10,000-attempt exploitation to an impractical level, while maintaining
service availability for legitimate users.

## Supersede Relationship

This decision **SUPERSEDES** all prior instructions recommending `LoginGraceTime 0` as
a CVE-2024-6387 workaround, including:
- Initial oss-security workaround guidance
- work/workaround_plan.md (first version, Rounds 1–10)
- Any Slack/email/Feishu messages prior to this decision recommending LoginGraceTime 0

## Required Actions

1. Remove `LoginGraceTime 0` from all sshd_config files
2. Add `MaxStartups 10:30:100` to sshd_config files
3. Restart sshd on all affected hosts
4. Update work/workaround_plan.md to reflect the new approach (create _v2 version)
5. Prioritize full patching over workaround in all future reports

Signed: Information Security Committee, 2024-07-08
