# Processing Activities — Detailed Compliance Dossier

> Per-activity compliance analysis supporting the Art. 30 record. Each section assesses lawful
> basis, data-minimisation, retention, transfers, processor agreements (Art. 28) and the
> applicable Art. 83 fining tier. Reviewed annually by the DPO (accountability, Art. 5(2)).

## ACT-001 — CRM Contact Management (CRM)

**Purpose.** B2B customer relationship management and sales pipeline tracking. The processing is carried out within the CRM subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(f) legitimate interests. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: B2B client contacts, Prospective customers. Categories of personal data: Name, Email, Phone, Company, Job title, Interaction history. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** AWS EU (processor), Salesforce EU (sub-processor). Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** This activity transfers personal data to a third country. The transfer relies on Standard Contractual Clauses (SCCs) under Art. 46, supplemented by a transfer-impact assessment (TIA) per the Schrems II ruling. Where the TIA identifies residual risk, supplementary measures (encryption with EU-held keys, pseudonymisation) are applied.

**Retention.** Contract duration + 2 years. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-002 — HR Employee Records (HR)

**Purpose.** Employment administration, payroll and benefits management. The processing is carried out within the HR subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(b) contract; Art. 6(1)(c) legal obligation. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Employees, Former employees, Job applicants. Categories of personal data: Name, Address, Bank details, Salary, Tax ID, Social security number. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Workday EU (processor), Tax authority. Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Employment + 10 years (tax law). The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-003 — Occupational Health Records (HR_HEALTH)

**Purpose.** Workplace health and safety, sick-leave management. The processing is carried out within the HR_HEALTH subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 9(2)(b) employment law. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Employees. Categories of personal data: Health status, Sick-leave records, Occupational injuries. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** YES — this activity processes special categories of personal data under Art. 9 (e.g. health). It therefore requires an Art. 9(2) condition, heightened security, strict access control, and is a strong indicator that a DPIA under Art. 35 is required.

**Recipients and processors.** Company physician, Statutory health insurance. Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Employment + 30 years (occupational safety). The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-004 — Subscription Billing (BILLING)

**Purpose.** Invoicing, payment processing and revenue recognition. The processing is carried out within the BILLING subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(b) contract. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Paying customers. Categories of personal data: Name, Billing address, Payment card token, VAT ID, Transaction history. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Stripe EU (processor), Tax authority. Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Invoice date + 10 years (commercial law). The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-005 — Email Marketing Campaigns (MARKETING)

**Purpose.** Newsletter distribution and lead nurturing. The processing is carried out within the MARKETING subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(a) consent. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Newsletter subscribers, Trial users. Categories of personal data: Name, Email, Open/click events, Marketing preferences. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Mailchimp US (processor). Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** This activity transfers personal data to a third country. The transfer relies on Standard Contractual Clauses (SCCs) under Art. 46, supplemented by a transfer-impact assessment (TIA) per the Schrems II ruling. Where the TIA identifies residual risk, supplementary measures (encryption with EU-held keys, pseudonymisation) are applied.

**Retention.** Until consent withdrawn. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-006 — Product Usage Analytics (ANALYTICS)

**Purpose.** Feature adoption analysis and product improvement. The processing is carried out within the ANALYTICS subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(f) legitimate interests. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Registered users. Categories of personal data: User ID, Session events, Device info, IP address. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Amplitude US (processor). Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** This activity transfers personal data to a third country. The transfer relies on Standard Contractual Clauses (SCCs) under Art. 46, supplemented by a transfer-impact assessment (TIA) per the Schrems II ruling. Where the TIA identifies residual risk, supplementary measures (encryption with EU-held keys, pseudonymisation) are applied.

**Retention.** 26 months. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-007 — HR Performance Analytics (HR_ANALYTICS)

**Purpose.** Employee performance evaluation and workforce planning. The processing is carried out within the HR_ANALYTICS subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(f) legitimate interests. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Employees. Categories of personal data: Performance scores, Goal completion, Manager feedback. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Internal HR system. Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Employment + 3 years. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-008 — Customer Support Tickets (SUPPORT)

**Purpose.** Technical support and issue resolution. The processing is carried out within the SUPPORT subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(b) contract. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Customers, End users. Categories of personal data: Name, Email, Ticket content, Account ID. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Zendesk EU (processor). Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Ticket close + 3 years. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-009 — Authentication and Access Logs (AUTH)

**Purpose.** Account security, fraud prevention and audit. The processing is carried out within the AUTH subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(f) legitimate interests. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: All users. Categories of personal data: User ID, Login timestamps, IP address, Device fingerprint. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Auth0 EU (processor). Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** 12 months. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-010 — Recruitment and Applicant Tracking (RECRUITMENT)

**Purpose.** Hiring, candidate evaluation and talent pipeline. The processing is carried out within the RECRUITMENT subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(b) pre-contract; Art. 6(1)(a) consent. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Job applicants. Categories of personal data: CV, Cover letter, Interview notes, References. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Greenhouse EU (processor). Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Rejection + 6 months. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-011 — Data Backup and Disaster Recovery (BACKUP)

**Purpose.** Business continuity and data resilience. The processing is carried out within the BACKUP subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(f) legitimate interests. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: All data subjects. Categories of personal data: Full database snapshots. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** AWS EU (processor). Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** This activity transfers personal data to a third country. The transfer relies on Standard Contractual Clauses (SCCs) under Art. 46, supplemented by a transfer-impact assessment (TIA) per the Schrems II ruling. Where the TIA identifies residual risk, supplementary measures (encryption with EU-held keys, pseudonymisation) are applied.

**Retention.** 35-day rolling. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-012 — Office CCTV Surveillance (CCTV)

**Purpose.** Physical premises security. The processing is carried out within the CCTV subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(f) legitimate interests. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Employees, Visitors. Categories of personal data: Video footage, Access-card events. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Security contractor (processor). Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** 30 days. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-013 — Cookie Consent Management (CONSENT)

**Purpose.** Lawful basis tracking for web tracking. The processing is carried out within the CONSENT subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(c) legal obligation. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Website visitors. Categories of personal data: Consent records, Cookie preferences, IP address. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** OneTrust EU (processor). Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Consent + 3 years (proof). The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-014 — Churn Prediction Model (CHURN)

**Purpose.** Customer retention and proactive intervention. The processing is carried out within the CHURN subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(f) legitimate interests. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Paying customers. Categories of personal data: Usage features, Support sentiment, Billing history. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Internal ML platform. Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Account active + 2 years. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-015 — Referral Program (REFERRAL)

**Purpose.** Customer acquisition via referrals. The processing is carried out within the REFERRAL subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(a) consent. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Referrers, Referred prospects. Categories of personal data: Name, Email, Referral status. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Internal. Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Program participation + 1 year. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-016 — Vendor and Supplier Management (VENDOR)

**Purpose.** Procurement and third-party risk management. The processing is carried out within the VENDOR subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(b) contract. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Vendor contacts. Categories of personal data: Name, Email, Contract terms, Bank details. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Internal procurement. Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Contract end + 6 years. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-017 — Webinar and Events (WEBINAR)

**Purpose.** Event registration and follow-up. The processing is carried out within the WEBINAR subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(a) consent. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Event attendees. Categories of personal data: Name, Email, Company, Attendance. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Zoom US (processor). Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** This activity transfers personal data to a third country. The transfer relies on Standard Contractual Clauses (SCCs) under Art. 46, supplemented by a transfer-impact assessment (TIA) per the Schrems II ruling. Where the TIA identifies residual risk, supplementary measures (encryption with EU-held keys, pseudonymisation) are applied.

**Retention.** Event + 18 months. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-018 — Customer Satisfaction Surveys (SURVEY)

**Purpose.** Service quality measurement (NPS). The processing is carried out within the SURVEY subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(f) legitimate interests. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Customers. Categories of personal data: Survey responses, NPS score, User ID. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** SurveyMonkey US (processor). Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** This activity transfers personal data to a third country. The transfer relies on Standard Contractual Clauses (SCCs) under Art. 46, supplemented by a transfer-impact assessment (TIA) per the Schrems II ruling. Where the TIA identifies residual risk, supplementary measures (encryption with EU-held keys, pseudonymisation) are applied.

**Retention.** 24 months. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-019 — Payment Fraud Detection (FRAUD)

**Purpose.** Detecting and preventing fraudulent transactions. The processing is carried out within the FRAUD subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(f) legitimate interests. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Paying customers. Categories of personal data: Transaction patterns, Device info, Geolocation. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Stripe Radar (processor). Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** This activity transfers personal data to a third country. The transfer relies on Standard Contractual Clauses (SCCs) under Art. 46, supplemented by a transfer-impact assessment (TIA) per the Schrems II ruling. Where the TIA identifies residual risk, supplementary measures (encryption with EU-held keys, pseudonymisation) are applied.

**Retention.** Transaction + 5 years. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-020 — Compliance Audit Logging (AUDIT_LOG)

**Purpose.** Regulatory audit trail and accountability. The processing is carried out within the AUDIT_LOG subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(c) legal obligation. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: All users, Employees. Categories of personal data: Action logs, Admin operations, Data access events. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Internal SIEM. Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** 6 years. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-021 — Partner Portal Access (PARTNER)

**Purpose.** Channel partner enablement. The processing is carried out within the PARTNER subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(b) contract. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Partner staff. Categories of personal data: Name, Email, Partner org, Access scope. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Internal. Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Partnership + 2 years. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-022 — Employee Training Records (TRAINING)

**Purpose.** Mandatory compliance and skills training. The processing is carried out within the TRAINING subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(c) legal obligation. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Employees. Categories of personal data: Course completion, Certification, Scores. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** LMS provider EU (processor). Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Employment + 5 years. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-023 — Expense and Travel Management (EXPENSE)

**Purpose.** Reimbursement and travel booking. The processing is carried out within the EXPENSE subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(b) contract. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Employees. Categories of personal data: Receipts, Travel itinerary, Bank details. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** SAP Concur EU (processor). Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Fiscal year + 10 years. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-024 — Data Subject Request Handling (DSR)

**Purpose.** Fulfilment of GDPR rights (Art. 15-22). The processing is carried out within the DSR subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(c) legal obligation. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: All data subjects. Categories of personal data: Request details, Identity verification, Response records. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Internal DPO system. Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Request + 3 years (proof). The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-025 — Security Incident Management (INCIDENT)

**Purpose.** Breach detection, response and notification. The processing is carried out within the INCIDENT subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(c) legal obligation. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Affected data subjects. Categories of personal data: Incident details, Affected records, Remediation logs. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Internal SOC. Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Incident + 6 years. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-026 — Office Biometric Access (BIOMETRIC)

**Purpose.** High-security area access control. The processing is carried out within the BIOMETRIC subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 9(2)(a) explicit consent. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Employees with secure-area access. Categories of personal data: Fingerprint template, Access events. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** YES — this activity processes special categories of personal data under Art. 9 (e.g. health). It therefore requires an Art. 9(2) condition, heightened security, strict access control, and is a strong indicator that a DPIA under Art. 35 is required.

**Recipients and processors.** Access-control vendor (processor). Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Access revocation + 30 days. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-027 — International Payroll Transfers (PAYROLL_INTL)

**Purpose.** Cross-border salary payment for remote staff. The processing is carried out within the PAYROLL_INTL subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(b) contract. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Remote employees (non-EU). Categories of personal data: Name, Bank details, Salary, Tax residency. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Deel US (processor). Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** This activity transfers personal data to a third country. The transfer relies on Standard Contractual Clauses (SCCs) under Art. 46, supplemented by a transfer-impact assessment (TIA) per the Schrems II ruling. Where the TIA identifies residual risk, supplementary measures (encryption with EU-held keys, pseudonymisation) are applied.

**Retention.** Employment + 10 years. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-028 — A/B Testing Platform (AB_TEST)

**Purpose.** Product experimentation and optimisation. The processing is carried out within the AB_TEST subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(f) legitimate interests. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Registered users. Categories of personal data: User ID, Variant assignment, Conversion events. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Internal experimentation platform. Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** 18 months. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-029 — Enterprise SSO Integration (SSO)

**Purpose.** Federated identity for enterprise customers. The processing is carried out within the SSO subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(b) contract. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: Enterprise end users. Categories of personal data: Email, SAML attributes, Group membership. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Customer IdP, Auth0 EU. Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** Account active. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).

## ACT-030 — Geolocation-based Compliance (GEO)

**Purpose.** Data residency and regional feature gating. The processing is carried out within the GEO subsystem of the VeritasCloud SaaS platform and is necessary to deliver the contracted service and meet the company's legal and operational obligations.

**Lawful basis.** Art. 6(1)(c) legal obligation. The basis has been assessed for validity: where consent is relied upon (Art. 6(1)(a) or Art. 9(2)(a)), records of consent are maintained and withdrawal is honoured; where legitimate interests are relied upon (Art. 6(1)(f)), a legitimate-interests assessment (LIA) balances the controller's interest against the rights and freedoms of the data subjects.

**Data subjects and data categories.** Data subjects: All users. Categories of personal data: IP address, Country, Region. The data set has been reviewed for data-minimisation (Art. 5(1)(c)); fields not strictly necessary for the stated purpose are not collected.

**Special category data.** No special categories of personal data (Art. 9) are processed in this activity.

**Recipients and processors.** Internal. Each external processor is bound by a written processor agreement under Art. 28 containing the mandatory clauses (processing only on documented instructions, confidentiality, security, sub-processor authorisation, assistance with data-subject requests, deletion or return at end of service, and audit rights).

**International transfers.** No transfers to third countries occur; all processing and storage remain within the EU/EEA.

**Retention.** 12 months. The retention period is assessed against the storage-limitation principle (Art. 5(1)(e)); data are deleted or anonymised when the period elapses, subject to legal-hold exceptions documented in the retention schedule.

**Security measures (Art. 32).** Encryption at rest (AES-256) and in transit (TLS 1.2+), role-based access control with least-privilege, comprehensive audit logging, pseudonymisation where feasible, and regular restore testing of backups. Access to this activity's data is restricted to the roles with a documented need-to-know.

**Compliance status and fining exposure.** Gaps identified for this activity are logged in findings_log.csv and mapped to the applicable Art. 83 tier: record-keeping or processor-agreement gaps fall under the tier-1 ceiling (Art. 83(4), up to EUR 10,000,000 or 2% of worldwide annual turnover); breaches of the basic principles or data-subject rights fall under the tier-2 ceiling (Art. 83(5), up to EUR 20,000,000 or 4%).
