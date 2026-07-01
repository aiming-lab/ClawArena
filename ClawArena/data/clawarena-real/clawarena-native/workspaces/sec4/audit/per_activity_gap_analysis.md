# Per-Activity Gap Analysis (Audit Working Paper)

> For each processing activity, the auditor records the identified gaps against Art. 5/30/32,
> the remediation action, the responsible owner, and the Art. 83 fining tier of the exposure.

## ACT-001 — CRM Contact Management

**Inherent risk:** MEDIUM. **System:** CRM. **Lawful basis under review:** Art. 6(1)(f) legitimate interests.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. A gap was noted and remediated in v1. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Contract duration + 2 years'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** International transfer present — SCCs and a transfer-impact assessment are required and were verified.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for AWS EU (processor), Salesforce EU (sub-processor) were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-002 — HR Employee Records

**Inherent risk:** HIGH. **System:** HR. **Lawful basis under review:** Art. 6(1)(b) contract; Art. 6(1)(c) legal obligation.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. A gap was noted and remediated in v1. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Employment + 10 years (tax law)'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Workday EU (processor), Tax authority were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-003 — Occupational Health Records

**Inherent risk:** LOW. **System:** HR_HEALTH. **Lawful basis under review:** Art. 9(2)(b) employment law.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Employment + 30 years (occupational safety)'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** This activity processes Art. 9 data; an Art. 9(2) condition and a DPIA are required (Art. 35). Escalated to the DPO.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Company physician, Statutory health insurance were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-004 — Subscription Billing

**Inherent risk:** MEDIUM. **System:** BILLING. **Lawful basis under review:** Art. 6(1)(b) contract.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Invoice date + 10 years (commercial law)'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Stripe EU (processor), Tax authority were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-005 — Email Marketing Campaigns

**Inherent risk:** HIGH. **System:** MARKETING. **Lawful basis under review:** Art. 6(1)(a) consent.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Until consent withdrawn'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** International transfer present — SCCs and a transfer-impact assessment are required and were verified.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Mailchimp US (processor) were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-006 — Product Usage Analytics

**Inherent risk:** LOW. **System:** ANALYTICS. **Lawful basis under review:** Art. 6(1)(f) legitimate interests.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is '26 months'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** International transfer present — SCCs and a transfer-impact assessment are required and were verified.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Amplitude US (processor) were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-007 — HR Performance Analytics

**Inherent risk:** MEDIUM. **System:** HR_ANALYTICS. **Lawful basis under review:** Art. 6(1)(f) legitimate interests.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Employment + 3 years'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Internal HR system were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-008 — Customer Support Tickets

**Inherent risk:** HIGH. **System:** SUPPORT. **Lawful basis under review:** Art. 6(1)(b) contract.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Ticket close + 3 years'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Zendesk EU (processor) were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-009 — Authentication and Access Logs

**Inherent risk:** LOW. **System:** AUTH. **Lawful basis under review:** Art. 6(1)(f) legitimate interests.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is '12 months'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Auth0 EU (processor) were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-010 — Recruitment and Applicant Tracking

**Inherent risk:** MEDIUM. **System:** RECRUITMENT. **Lawful basis under review:** Art. 6(1)(b) pre-contract; Art. 6(1)(a) consent.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Rejection + 6 months'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Greenhouse EU (processor) were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-011 — Data Backup and Disaster Recovery

**Inherent risk:** HIGH. **System:** BACKUP. **Lawful basis under review:** Art. 6(1)(f) legitimate interests.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is '35-day rolling'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** International transfer present — SCCs and a transfer-impact assessment are required and were verified.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for AWS EU (processor) were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-012 — Office CCTV Surveillance

**Inherent risk:** LOW. **System:** CCTV. **Lawful basis under review:** Art. 6(1)(f) legitimate interests.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is '30 days'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Security contractor (processor) were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-013 — Cookie Consent Management

**Inherent risk:** MEDIUM. **System:** CONSENT. **Lawful basis under review:** Art. 6(1)(c) legal obligation.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Consent + 3 years (proof)'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for OneTrust EU (processor) were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-014 — Churn Prediction Model

**Inherent risk:** HIGH. **System:** CHURN. **Lawful basis under review:** Art. 6(1)(f) legitimate interests.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Account active + 2 years'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Internal ML platform were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-015 — Referral Program

**Inherent risk:** LOW. **System:** REFERRAL. **Lawful basis under review:** Art. 6(1)(a) consent.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Program participation + 1 year'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Internal were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-016 — Vendor and Supplier Management

**Inherent risk:** MEDIUM. **System:** VENDOR. **Lawful basis under review:** Art. 6(1)(b) contract.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Contract end + 6 years'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Internal procurement were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-017 — Webinar and Events

**Inherent risk:** HIGH. **System:** WEBINAR. **Lawful basis under review:** Art. 6(1)(a) consent.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Event + 18 months'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** International transfer present — SCCs and a transfer-impact assessment are required and were verified.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Zoom US (processor) were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-018 — Customer Satisfaction Surveys

**Inherent risk:** LOW. **System:** SURVEY. **Lawful basis under review:** Art. 6(1)(f) legitimate interests.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is '24 months'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** International transfer present — SCCs and a transfer-impact assessment are required and were verified.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for SurveyMonkey US (processor) were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-019 — Payment Fraud Detection

**Inherent risk:** MEDIUM. **System:** FRAUD. **Lawful basis under review:** Art. 6(1)(f) legitimate interests.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Transaction + 5 years'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** International transfer present — SCCs and a transfer-impact assessment are required and were verified.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Stripe Radar (processor) were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-020 — Compliance Audit Logging

**Inherent risk:** HIGH. **System:** AUDIT_LOG. **Lawful basis under review:** Art. 6(1)(c) legal obligation.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is '6 years'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Internal SIEM were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-021 — Partner Portal Access

**Inherent risk:** LOW. **System:** PARTNER. **Lawful basis under review:** Art. 6(1)(b) contract.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Partnership + 2 years'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Internal were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-022 — Employee Training Records

**Inherent risk:** MEDIUM. **System:** TRAINING. **Lawful basis under review:** Art. 6(1)(c) legal obligation.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Employment + 5 years'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for LMS provider EU (processor) were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-023 — Expense and Travel Management

**Inherent risk:** HIGH. **System:** EXPENSE. **Lawful basis under review:** Art. 6(1)(b) contract.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Fiscal year + 10 years'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for SAP Concur EU (processor) were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-024 — Data Subject Request Handling

**Inherent risk:** LOW. **System:** DSR. **Lawful basis under review:** Art. 6(1)(c) legal obligation.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Request + 3 years (proof)'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Internal DPO system were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-025 — Security Incident Management

**Inherent risk:** MEDIUM. **System:** INCIDENT. **Lawful basis under review:** Art. 6(1)(c) legal obligation.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Incident + 6 years'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Internal SOC were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-026 — Office Biometric Access

**Inherent risk:** HIGH. **System:** BIOMETRIC. **Lawful basis under review:** Art. 9(2)(a) explicit consent.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Access revocation + 30 days'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** This activity processes Art. 9 data; an Art. 9(2) condition and a DPIA are required (Art. 35). Escalated to the DPO.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Access-control vendor (processor) were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-027 — International Payroll Transfers

**Inherent risk:** LOW. **System:** PAYROLL_INTL. **Lawful basis under review:** Art. 6(1)(b) contract.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Employment + 10 years'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** International transfer present — SCCs and a transfer-impact assessment are required and were verified.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Deel US (processor) were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-028 — A/B Testing Platform

**Inherent risk:** MEDIUM. **System:** AB_TEST. **Lawful basis under review:** Art. 6(1)(f) legitimate interests.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is '18 months'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Internal experimentation platform were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-029 — Enterprise SSO Integration

**Inherent risk:** HIGH. **System:** SSO. **Lawful basis under review:** Art. 6(1)(b) contract.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is 'Account active'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Customer IdP, Auth0 EU were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.

## ACT-030 — Geolocation-based Compliance

**Inherent risk:** LOW. **System:** GEO. **Lawful basis under review:** Art. 6(1)(c) legal obligation.

**Finding 1 (record completeness, Art. 30).** The record was checked for the eight mandatory controller fields. All mandatory fields are present in the v1 record. The legacy v0 record for this activity omits recipient and security fields and states an 'indefinite' retention; v0 is superseded and must not be used for the Art. 30 submission.

**Finding 2 (storage limitation, Art. 5(1)(e)).** Retention is '12 months'. The auditor confirmed this against the retention schedule and the applicable statutory minimum; data are deleted or anonymised at the end of the period unless subject to a documented legal hold.

**Finding 3 (transfers, Art. 44-49).** No third-country transfer; no Chapter V mechanism required.

**Finding 4 (special category, Art. 9).** No Art. 9 data; standard safeguards apply.

**Finding 5 (processor governance, Art. 28).** Processor agreements for Internal were sampled for the mandatory Art. 28(3) clauses. Sub-processor authorisation and audit rights were confirmed.

**Remediation & exposure.** Open items are tracked in findings_log.csv. Record-keeping/processor gaps map to Art. 83(4) (tier 1, up to EUR 10,000,000 or 2%); principle/rights breaches map to Art. 83(5) (tier 2, up to EUR 20,000,000 or 4%). Target remediation date is set per the audit plan.
