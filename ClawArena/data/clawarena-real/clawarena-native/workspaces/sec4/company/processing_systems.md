# VeritasCloud — Data Processing Systems Inventory

## System Overview

VeritasCloud operates four primary data processing systems, each with distinct
data flows and compliance obligations.

### 1. CRM Module (VeritasCloud CRM)

**Purpose**: Customer relationship management for B2B clients across the EU.
**Data Subjects**: End customers of VeritasCloud's B2B clients (~800,000 EU individuals)
**Personal Data**: Name, email, phone, company affiliation, interaction history,
  behavioral analytics data (page visits, email opens, click tracking)
**Legal Ground**: Legitimate interests (Art. 6(1)(f)) for B2B CRM; consent for
  behavioral analytics
**Third-Country Transfers**: Data processed via US-based sub-processors (AWS US-East,
  Salesforce Marketing Cloud)
**Retention**: Active contacts: duration of B2B contract + 2 years;
  Interaction logs: 6 months rolling

### 2. HR Module (VeritasCloud HR)

**Purpose**: Human resources management for VeritasCloud internal employees (1,200 staff)
**Data Subjects**: VeritasCloud employees
**Personal Data**: Name, employment contract, salary, performance reviews, health/sick leave
  records (special category per Art. 9), disciplinary records
**Legal Ground**: Contract performance (Art. 6(1)(b)) for employment;
  Legal obligation (Art. 6(1)(c)) for statutory reporting
**Third-Country Transfers**: None; EU-hosted only
**Retention**: Employment records: contract duration + 10 years (tax compliance)

### 3. Analytics Platform

**Purpose**: Platform usage analytics and product improvement
**Data Subjects**: All platform users (B2B clients + VeritasCloud employees)
**Personal Data**: Pseudonymous usage events, feature usage metrics
**Legal Ground**: Legitimate interests (Art. 6(1)(f))
**Third-Country Transfers**: Analytics processed via US-based vendor (Mixpanel)

### 4. Billing System

**Purpose**: Subscription billing and payment processing
**Data Subjects**: B2B client billing contacts and payment administrators
**Personal Data**: Name, email, billing address, payment method reference (tokenized)
**Legal Ground**: Contract performance (Art. 6(1)(b))
**Third-Country Transfers**: Payment processor Stripe (US entity, SCCs in place)

## Compliance Gaps Identified (Preliminary)

1. CRM Module: RoPA entry missing `recipient_categories` and `retention_periods` fields
2. HR Module: RoPA entry missing `security_measures` field
3. Analytics Platform: Third-country transfer documentation incomplete (Mixpanel SCC not executed)
4. HR Module: AI-powered HR Analytics sub-feature requires separate DPIA assessment
