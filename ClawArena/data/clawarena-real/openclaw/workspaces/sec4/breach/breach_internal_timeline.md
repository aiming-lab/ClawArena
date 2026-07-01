# Breach Incident — Internal Timeline

**Incident**: INC-2025-0314 | CRM Database Unauthorized Access
**Status**: CONTAINED | Notification submitted to BayLDA

---

## Chronological Timeline

### 2025-03-12 (Wednesday)

- **02:00 UTC**: Attacker uses stolen API credential to authenticate to CRM DB (source IP: 203.0.113.45)
- **02:05 UTC**: Automated SIEM rule: API auth from new IP — alert **NOT triggered** (threshold too high)

### 2025-03-14 (Friday)

- **08:50 UTC**: Second anomaly pattern detected by ML-based anomaly detection
- **09:00 UTC**: SIEM high-severity alert fired — Security Engineer on-call paged
- **09:25 UTC**: Security Engineer Fabian Müller confirms active unauthorized session
- **09:30 UTC**: Containment: credential revoked, session terminated, IP blocked
- **09:45 UTC**: DPO Lena Fischer notified by Fabian Müller
- **10:00 UTC**: Incident response team convened
- **10:30 UTC**: All affected credentials rotated; perimeter secured
- **11:00 UTC**: Digital forensics commenced; log extraction from SIEM
- **14:00 UTC**: Forensic analysis complete:
  - Exfiltration: No evidence of data leaving the environment (no outbound anomalies)
  - Exposure: Read queries executed on contact tables (~15,000 subjects, ~45,000 records)
  - Root cause: Phishing email compromised employee API key
- **18:00 UTC**: Risk assessment completed: HIGH risk to data subjects (contact data quality)
- **20:00 UTC**: DPO decision: Article 33 notification required; Art. 34 assessment: notification to data subjects NOT required (low risk of harm from contact data exposure alone)

### 2025-03-15 (Saturday)

- **09:00 UTC**: DPO and Legal Counsel finalize notification content
- **22:30 UTC**: Formal Art. 33 notification submitted to BayLDA online portal (Portal-ID: BayLDA-2025-0315-8847)

**Total elapsed from discovery to notification**: 37.5 hours (within 72-hour Art. 33(1) deadline)

---

## Root Cause Analysis (Preliminary)

1. **Insufficient MFA enforcement**: API keys not subject to MFA requirement
2. **Overly broad API key permissions**: Key granted read access to entire contact table
3. **Alert threshold misconfiguration**: SIEM threshold for "new IP auth" too high
4. **Missing data minimisation**: API key scope should have been restricted to specific client's data

## Corrective Measures

1. Mandatory MFA for all API key usage (implemented 2025-03-15)
2. Principle of least privilege: API key scoping by client ID (implemented 2025-03-16)
3. SIEM alert threshold recalibrated (implemented 2025-03-14)
4. Security awareness training relaunch (scheduled 2025-04-01)
