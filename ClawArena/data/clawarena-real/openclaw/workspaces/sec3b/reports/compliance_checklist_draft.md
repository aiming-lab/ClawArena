# Compliance Remediation Checklist — DRAFT

## ArtemisQ Capital — AROS v4.2 Timezone Incident

Date: 2024-11-05 (DRAFT)
Status: INCOMPLETE — Items marked [?] require completion

---

### Section 1: Immediate Fixes

- [x] Trading halted at 22:00 UTC on 2024-11-03
- [x] Root cause identified: hardcoded UTC_OFFSET = -4 in timezone_config.py
- [ ] UTC_OFFSET corrected to -5 in production
- [?] DST-aware library (e.g. pytz/zoneinfo) replacement scheduled

### Section 2: Regulatory Reporting

- [ ] MiFIR Field 28 error report submitted to FCA (OVERDUE)
- [?] T+1 settlement error notification to SEC (deadline TBD)
- [ ] Corrective transaction reports resubmitted in UTC

### Section 3: Root Cause Analysis

- [ ] Full RCA document completed
- [ ] Contributing factors documented
- [ ] Financial impact quantified

### Section 4: Long-Term Remediation

- [?] Rule 15c3-5(b) compliance review
- [?] Rule 15c6-1 T+1 compliance audit
- [ ] DST transition testing protocol established
- [ ] Annual CEO certification updated

---
*This checklist is incomplete and requires completion by compliance team.*
