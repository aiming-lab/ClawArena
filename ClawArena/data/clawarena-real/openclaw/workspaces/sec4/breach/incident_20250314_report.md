# Data Breach Incident Report — Initial Assessment

**Incident Reference**: INC-2025-0314
**Date Discovered**: 2025-03-14 at 09:00 UTC
**Discovery Method**: Automated anomaly detection alert (SIEM)
**Reported to DPO**: 2025-03-14 at 09:45 UTC
**Classification**: PERSONAL DATA BREACH (Art. 4(12) GDPR)

## Summary

An unauthorised third party gained read access to the VeritasCloud CRM database
(production instance, EU-West-1 region) between 2025-03-12 02:00 UTC and
2025-03-14 08:50 UTC (estimated 54 hours of exposure).

## Affected Data

- **Categories of Data Subjects**: B2B client contacts (~15,000 individuals)
- **Approximate Number of Data Subjects**: 15,000
- **Categories of Personal Data**: Name, email address, phone number, company affiliation
- **Approximate Number of Records**: ~45,000 records (3 data fields × 15,000 subjects)
- **Sensitive Data Involved**: No special category data (Art. 9) exposed

## Discovery Timeline

| Time (UTC) | Event |
|---|---|
| 2025-03-14 09:00 | SIEM alert triggered: anomalous read queries on CRM DB |
| 2025-03-14 09:30 | Security team confirms breach; containment initiated |
| 2025-03-14 09:45 | DPO Lena Fischer notified |
| 2025-03-14 10:30 | Access revoked; affected credentials rotated |
| 2025-03-14 14:00 | Full extent of breach determined: 15,000 subjects, 45,000 records |
| 2025-03-14 18:00 | Breach risk assessment completed |
| 2025-03-15 09:00 | Art. 33 notification decision: NOTIFY (risk to data subjects likely) |
| 2025-03-15 22:30 | Formal notification submitted to BayLDA via online portal |

## Notification Decision

Under **Art. 33(1) GDPR**: Controller must notify supervisory authority without undue
delay and, where feasible, not later than **72 hours** after becoming aware.

**Discovery time**: 2025-03-14T09:00Z
**Notification time**: 2025-03-15T22:30Z
**Elapsed hours**: approximately 37.5 hours
**Status**: WITHIN 72-HOUR WINDOW — COMPLIANT

---

*Note: See `breach/breach_internal_timeline.md` for full chronological detail.*
