# Security Incident Report — Template

**[INCIDENT ID]**: IR-2024-XXXX
**[DATE]**: YYYY-MM-DD
**[SEVERITY]**: Critical / High / Medium / Low
**[STATUS]**: Open / Investigating / Remediated / Closed

---

## TL;DR

[Insert standalone TL;DR paragraph here, ≤200 words. Required for all executive summaries.]

---

## 1. Incident Summary

- **CVE**: [CVE ID in format CVE-YYYY-NNNNN]
- **CVSS Score**: [Score] ([Severity])
- **CVSS Vector**: [Verbatim CVSS vector string]
- **Affected Systems**: [Count and description]
- **Discovery Date**: [YYYY-MM-DD]
- **Disclosure Date**: [YYYY-MM-DD]
- **Remediation Deadline**: [YYYY-MM-DD]

## 2. Technical Details

[Technical description of the vulnerability, exploitation mechanism, and impact]

## 3. Affected Asset Inventory

| Environment | Total Hosts | Vulnerable | Patched | Priority |
|-------------|------------|-----------|---------|----------|
| prod        | X          | Y         | Z       | P1       |
| staging     | X          | Y         | Z       | P2       |
| dev         | X          | Y         | Z       | P3       |

## 4. Remediation Actions

- [ ] Apply vendor patch [ERRATA ID] to all affected hosts
- [ ] Verify patch version [PACKAGE VERSION]
- [ ] Update compliance records
- [ ] Close risk register entry

## 5. References

- [CVE NVD link]
- [Vendor advisory link]
- [Internal documentation links]
