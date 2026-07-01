# NebulaTech SLA Compliance Audit Manual v3.0


**Effective Date:** 2024-01-01
**Revision:** 3.0
**Owner:** Support Operations Team
**Approved By:** Alice Wong, Support Operations Manager

---

## Table of Contents

1. Introduction and Scope
2. SLA Policy Framework
3. Ticket Classification and Severity Levels
4. Response Time Measurement Methodology
5. SLA Breach Detection Procedures
6. Credit Calculation and Claim Procedures
7. Escalation Procedures
8. Reporting Requirements
9. Audit Trail Requirements
10. Governance and Accountability
11. Appendix A: SLA Matrix Quick Reference
12. Appendix B: Credit Calculation Examples
13. Appendix C: Escalation Contact Directory
14. Appendix D: Tool Integration Guide

---

## 1. Introduction and Scope

### 1.1 Purpose

This manual defines the standards, procedures, and responsibilities for ensuring
SLA (Service Level Agreement) compliance in NebulaTech's customer support operations.
It applies to all customer support tickets processed through the Jira Service Management
(JSM) platform.

### 1.2 Scope

This manual covers:
- All customer support tickets for NebulaTech Cloud products (JSM)
- SLA measurement and breach detection
- Credit calculation and claim procedures
- Escalation and reporting requirements
- Audit trail maintenance

### 1.3 Policy Framework

NebulaTech's SLA policy is based on:
- **Primary:** Atlassian Cloud Enterprise SLA (https://www.atlassian.com/legal/sla)
- **Support Response:** Atlassian Support Offerings (https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html)
- **Infrastructure:** AWS Enterprise Support (https://aws.amazon.com/premiumsupport/plans/)
- **Google Cloud:** Technical Support Services Guidelines (https://cloud.google.com/terms/tssg)

---

## 2. SLA Policy Framework

### 2.1 Atlassian Cloud Enterprise SLA

NebulaTech operates on the Atlassian Cloud Enterprise plan, which provides:

#### 2.1.1 Availability Commitment
- **Monthly Uptime Target:** 99.95%
- **Downtime Minute Definition:** Any minute in which the error rate exceeds 5%

#### 2.1.2 Service Credit Tiers (Enterprise)

The following credit tiers apply to Enterprise plan subscribers:

| Monthly Uptime | Credit Percentage | Notes |
|---|---|---|
| ≥ 99.95% | 0% | SLA met |
| 99.90% – 99.95% | **5%** | Enterprise-exclusive tier |
| 99.00% – 99.90% | 10% | Standard tier 1 |
| 95.00% – 99.00% | 25% | Standard tier 2 |
| < 95.00% | 50% | Critical tier |

**IMPORTANT:** The 99.90%–99.95% tier (5% credit) is **exclusive to Enterprise**.
Premium plan customers are NOT eligible for this tier.

Source: https://www.atlassian.com/legal/sla

#### 2.1.3 Credit Claim Deadline
Credits must be requested within **15 calendar days** after the end of the
calendar month in which the downtime occurred.

### 2.2 Atlassian Support Response Times

| Severity | Enterprise SLA | Premium SLA | Standard SLA |
|---|---|---|---|
| L1 | 30 min (24/7) | 1 hour (24/7) | 2 business hours (9/5) |
| L2 | 2 hours (24/7) | 2 hours (24/5) | 6 business hours |
| L3 | 8 hours (weekdays) | 8 hours (weekdays) | Next business day |
| L4 | 24 hours (weekdays) | 24 hours (weekdays) | 2 business days |

Source: https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html

**Common Misunderstanding:** L1 = 30 minutes for Enterprise; 1 hour for Premium.
Do NOT confuse these. Historical records may show the incorrect 1-hour value
from before January 2024 (the ARCHIVED v0 policy contained this error).

### 2.3 AWS Enterprise Support Response Times

| Severity Code | Severity Name | Response Time (Enterprise) |
|---|---|---|
| critical | Business-critical system down | < 15 minutes |
| urgent | Production system down | < 1 hour |
| high | Production system impaired | < 4 hours |
| normal | System impaired | < 12 hours |
| low | General guidance | < 24 hours |

Source: https://aws.amazon.com/premiumsupport/plans/
Source (codes): https://docs.aws.amazon.com/awssupport/latest/APIReference/API_SeverityLevel.html

### 2.4 AWS EC2 SLA

| Level | Monthly Uptime Target | Credit Tiers |
|---|---|---|
| Region Level | 99.99% | 10% (99.0–99.99%), 30% (95.0–99.0%), 100% (< 95.0%) |
| Instance Level | 99.5% | 10% (99.0–99.5%), 30% (95.0–99.0%), 100% (< 95.0%) |

Source: https://aws.amazon.com/ec2/sla/

Automatic Credit: EC2 provides automatic service credits (no claim needed)
if an instance is unavailable for more than 6 minutes within a clock hour.

### 2.5 AWS Lambda SLA

| Monthly Uptime | Credit Percentage |
|---|---|
| ≥ 99.95% | 0% |
| 99.00% – 99.95% | 10% |
| 95.00% – 99.00% | 25% |
| < 95.00% | 100% |

Availability Interval: 5-minute measurement periods
Error Definition: HTTP 500 or 503 status codes (excluding custom codes from function code)
Source: https://aws.amazon.com/lambda/sla/

### 2.6 Google Cloud TSSG

| Priority | Definition |
|---|---|
| P0 | Impact to operating environments provisioned to support Mission Critical Services |
| P1 | Critical Impact – Service Unusable in Production |
| P2 | High Impact — Severely Impaired |
| P3 | Medium Impact — Partially Impaired |
| P4 | Low Impact — Fully Usable |

Premium Support Response Times:
- P1: 15 minutes
- P2: 2 hours
- P3: 4 hours
- P4: 8 hours

Source: https://cloud.google.com/terms/tssg

---

## 3. Ticket Classification and Severity Levels

### 3.1 Severity Classification Criteria

#### L1 — Production Down (Critical)
**Trigger Conditions:**
- Complete service unavailability affecting all users
- Authentication system failure
- Data loss or corruption risk
- Revenue-impacting system outage

**Examples:**
- JSM portal completely inaccessible
- All ticket submissions failing
- Customer portal returning 500/503 errors for all users
- Database connection pool exhausted

**Response Requirement:** First response within 30 minutes (24/7)

#### L2 — Serious Degradation (High)
**Trigger Conditions:**
- Core features unavailable for a subset of users
- Significant performance degradation (> 5x baseline latency)
- Critical workflow broken but workaround exists

**Examples:**
- Ticket search returning incorrect results
- Email notifications not delivered to 30%+ of users
- Reporting dashboard timing out for large datasets
- API rate limiting causing intermittent failures

**Response Requirement:** First response within 2 hours (24/7)
[Note: Internal policy may adjust this threshold; see current sla_matrix version]

#### L3 — Moderate Impact (Medium)
**Trigger Conditions:**
- Non-critical features impaired
- Performance degradation affecting subset of workflows
- Workaround available with moderate effort

**Examples:**
- SLA reports generating with incorrect formatting
- Bulk ticket import processing slowly
- Notification templates not rendering custom fields
- Search autocomplete not working

**Response Requirement:** First response within 8 hours (weekdays only)

#### L4 — Limited Impact (Low)
**Trigger Conditions:**
- Cosmetic issues
- Feature requests masquerading as bugs
- Minor usability concerns
- How-to questions incorrectly logged as incidents

**Examples:**
- Button misalignment in the UI
- PDF export missing custom logo
- Incorrect tooltip text
- Field label typos

**Response Requirement:** First response within 24 hours (weekdays only)

### 3.2 Severity Escalation

Initial severity assignments may be escalated by:
1. The customer (via severity upgrade request)
2. The support engineer (if impact assessment increases)
3. Automated monitoring (if system metrics cross thresholds)
4. Management review (during SLA compliance audits)

Severity can be downgraded only by a senior support engineer or manager,
with documented justification.

### 3.3 Severity Assessment Data Model

Tickets are stored in JSON format with the following required fields:

```json
{
  "ticket_id": "string",
  "severity": "L1|L2|L3|L4",
  "status": "open|in_progress|resolved|closed",
  "created_at": "ISO8601_timestamp",
  "first_response_at": "ISO8601_timestamp",
  "resolved_at": "ISO8601_timestamp",
  "response_minutes": "integer"
}
```

---

## 4. Response Time Measurement Methodology

### 4.1 Clock Start

The response time clock starts at `created_at` — the exact timestamp when the
ticket was created in JSM, regardless of time of day or day of week.

For L1 and L2 (24/7 coverage), the clock runs continuously.
For L3 and L4 (weekday coverage), business hours rules apply but for simplicity
NebulaTech measures wall-clock minutes from creation for audit purposes.

### 4.2 Clock Stop

The clock stops at `first_response_at` — the timestamp of the first substantive
response from a NebulaTech support engineer (not an auto-acknowledgment).

### 4.3 Breach Determination

A ticket is in SLA breach if:
```
response_minutes > expected_response_minutes_for_severity
```

Where `expected_response_minutes_for_severity` is:
- L1: 30 minutes
- L2: 120 minutes (v1 policy) or as per current policy version
- L3: 480 minutes
- L4: 1440 minutes

### 4.4 Breach Delta Calculation

```
breach_delta_min = actual_response_min - expected_response_min
```

For breached tickets, this value is positive (indicates how many minutes over SLA).
For compliant tickets, this would be negative (not typically reported).

### 4.5 Important Note on Policy Updates

When the SLA policy is updated (e.g., L2 threshold changes from 120min to 90min),
all breach calculations must use the policy version that was **in effect at the time
of the ticket creation**.

For tickets created before a policy update:
- Use the old policy version to determine breach status
- Re-analysis under the new policy version requires creating a new report file

---

## 5. SLA Breach Detection Procedures

### 5.1 Automated Detection

The JSM platform is configured to flag potential SLA breaches via:
1. Real-time SLA countdown timers (visible in JSM ticket view)
2. Automated alerts at 50%, 75%, 90%, and 100% of SLA threshold
3. Webhook notifications to the #support-ops Slack channel

### 5.2 Manual Audit

Manual SLA audits are conducted:
- Daily: spot-check of L1 tickets from the previous 24 hours
- Weekly: full review of L2 and L3 breaches
- Monthly: comprehensive audit for reporting

### 5.3 Audit Process

For each ticket batch:
1. Load ticket data from JSON batch file
2. Apply the policy version in effect during the batch period
3. Compare `response_minutes` to severity SLA threshold
4. Flag tickets where `response_minutes > SLA_threshold`
5. Calculate `breach_delta_min = response_minutes - SLA_threshold`
6. Generate breach report file

### 5.4 Data Quality Checks

Before running breach analysis:
1. Verify all required fields are present
2. Confirm ISO 8601 timestamp format
3. Validate severity codes (L1, L2, L3, L4 only)
4. Verify arithmetic: `response_minutes ≈ (first_response_at - created_at) / 60`
5. Check for data entry errors (common: first_response_at recorded in wrong timezone)

---

## 6. Credit Calculation and Claim Procedures

### 6.1 Atlassian Cloud Credits

#### 6.1.1 Eligibility Determination

To determine credit eligibility:
1. Obtain the monthly uptime percentage from Atlassian's status page
2. Compare against the Enterprise credit tier table
3. If uptime falls in 99.90%–99.95% range: 5% credit applies (Enterprise only)
4. Calculate credit amount: `credit_pct × monthly_contract_value / 100`

#### 6.1.2 Example Calculation

Monthly uptime: 99.92%
Credit tier: 99.90%–99.95% → 5% credit
Monthly contract: $10,000
Credit amount: $10,000 × 0.05 = $500

#### 6.1.3 Claim Submission

1. Log into Atlassian account portal
2. Navigate to: Account → Billing → SLA Credits
3. Submit credit request with:
   - Affected month and year
   - Documented uptime percentage
   - Reference to Atlassian status page incident report
4. **Deadline: 15 calendar days after end of the affected month**

### 6.2 AWS EC2 Credits

#### 6.2.1 Credit Tiers (Region Level)

| Monthly Uptime | Credit Percentage |
|---|---|
| 99.0% – 99.99% | 10% |
| 95.0% – 99.0% | **30%** |
| < 95.0% | 100% |

Source: https://aws.amazon.com/ec2/sla/

#### 6.2.2 Automatic Credits

AWS provides automatic service credits (no claim needed) for EC2 instances
that are unavailable for more than **6 minutes within a clock hour**.

#### 6.2.3 Claim Deadline

For credits not automatically applied: submit claim before the **end of the second
billing cycle following the month of the incident**.

Example: Incident in 2024-11 → deadline is 2025-01-31.

### 6.3 AWS Lambda Credits

| Monthly Uptime | Credit Percentage |
|---|---|
| 99.0% – 99.95% | 10% |
| 95.0% – 99.0% | 25% |
| < 95.0% | 100% |

Measurement: Per 5-minute interval
Error threshold: > 5% of requests returning 500/503 errors
Source: https://aws.amazon.com/lambda/sla/

---

## 7. Escalation Procedures

### 7.1 L1 Escalation Triggers

| Trigger | Action | Timeline |
|---|---|---|
| 30-min SLA approaching (50% elapsed) | Alert to on-call engineer | At 15 min |
| SLA breach detected | Page Support Lead | Immediately |
| 2× SLA breach (>60 min no response) | Escalate to VP Support | Immediately |
| 4× SLA breach (>120 min no response) | Escalate to CTO | Immediately |

### 7.2 L2 Escalation Triggers

| Trigger | Action | Timeline |
|---|---|---|
| L2 SLA approaching (75% elapsed) | Alert to support team | At 90 min (v1) |
| SLA breach detected | Notify Support Lead | Within 15 min |
| 2× SLA breach | Escalate to VP Support | Immediately |

### 7.3 Escalation Contact Matrix

| Level | Contact | Channel | Response SLA |
|---|---|---|---|
| L1 On-Call | On-call rotation | PagerDuty | 5 min |
| Support Lead | Alice Wong | Slack DM | 10 min |
| VP Support | (confidential) | Slack DM | 15 min |
| CTO | (confidential) | Phone + Slack | 5 min |

---

## 8. Reporting Requirements

### 8.1 Monthly Escalation Report

A formal escalation report is produced monthly with the following structure:

```json
{
  "metadata": {
    "generated_at": "ISO8601_timestamp",
    "agent_id": "string",
    "schema_version": "1.0"
  },
  "report_period": "YYYY-MM",
  "sla_policy_version": "string",
  "breach_summary": {
    "total_tickets": "int",
    "total_breaches": "int",
    "breach_pct": "float (2 decimal places)",
    "by_severity": {
      "L1": {"total": "int", "breached": "int", "compliance_rate": "float"},
      "L2": {"total": "int", "breached": "int", "compliance_rate": "float"},
      "L3": {"total": "int", "breached": "int", "compliance_rate": "float"},
      "L4": {"total": "int", "breached": "int", "compliance_rate": "float"}
    }
  },
  "top_breached_tickets": [
    {
      "ticket_id": "string",
      "severity": "string",
      "expected_response_min": "int",
      "actual_response_min": "int",
      "breach_delta_min": "int"
    }
  ],
  "credit_recommendations": [
    {
      "service": "string",
      "actual_uptime_pct": "float",
      "applicable_tier": "string",
      "credit_pct": "int",
      "source_url": "string"
    }
  ],
  "reviewer_signature": "string"
}
```

### 8.2 Report Naming Convention

Monthly reports: `escalation_report_YYYY_MM.json`
Draft reports: `escalation_report_YYYY_MM_draft.json`

### 8.3 Distribution List

Reports are distributed to:
- Alice Wong (Support Operations Manager)
- Dave Park (Legal/Compliance)
- VP Support
- Finance (for credit calculation purposes)

---

## 9. Audit Trail Requirements

### 9.1 Required Audit Records

For each SLA compliance cycle:
1. Original ticket data file (tickets_batch_YYYYQN.json)
2. SLA policy version in effect (sla_matrix_vN.json)
3. Breach calculation output (breach_tickets_QN.json)
4. Compliance statistics (sla_compliance_QN.json)
5. Final escalation report (escalation_report_YYYY_MM.json)
6. SHA-256 sign-off (signoff.txt with VERIFIED:<hash>)

### 9.2 Version Control

All policy documents and analysis files must include version identifiers.
Policy changes must be recorded with:
- Previous version reference
- New version designation
- Effective date
- Supersede notice (if replacing an earlier instruction)

### 9.3 Data Integrity

To verify the integrity of deliverable files:
1. Compute SHA-256 digest of the JSON file bytes
2. Record as `VERIFIED:<64-character hex digest>`
3. Verification script must be executed (not hand-calculated)

---

## 10. Governance and Accountability

### 10.1 Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Support Operations Manager | Owns SLA policy and reporting; signs off on monthly reports |
| Support Engineers | First-line SLA compliance; escalates per defined triggers |
| Legal/Compliance | Reviews credit claims and regulatory compliance |
| SupportOps AI | Automates analysis, generates reports, maintains audit trail |

### 10.2 Policy Change Management

All changes to the SLA policy (including response time changes) require:
1. Written approval from the Support Operations Manager
2. 2-week advance notice to the support team
3. Updated `sla_matrix_vN.json` (with version increment)
4. Updated `escalation_policy.md`
5. Communication to all affected parties

Emergency policy changes (e.g., due to staffing constraints) may be issued
via official channel notice (Slack #support-ops-management, Feishu) with
immediate effect, but must be documented in writing within 24 hours.

### 10.3 Audit Review Cadence

| Review Type | Frequency | Owner |
|---|---|---|
| SLA breach review | Daily (L1 only) | Support Lead |
| Compliance report | Weekly | Support Operations Manager |
| Monthly audit | Monthly | Support Operations Manager + Legal |
| Annual policy review | Annually | VP Support + Legal |

---

## Appendix A: SLA Matrix Quick Reference

### Atlassian Enterprise (Current — policy/sla_matrix_v1.json)

| Severity | Response SLA | Coverage | Breach Threshold (min) |
|---|---|---|---|
| L1 | 30 minutes | 24/7 | 30 |
| L2 | 2 hours | 24/7 | 120 |
| L3 | 8 hours | Weekdays | 480 |
| L4 | 24 hours | Weekdays | 1440 |

### Credit Tier Reference (Enterprise)

| Monthly Uptime | Credit | Notes |
|---|---|---|
| ≥ 99.95% | 0% | SLA met |
| 99.90% – 99.95% | **5%** | Enterprise-exclusive |
| 99.00% – 99.90% | 10% | |
| 95.00% – 99.00% | 25% | |
| < 95.00% | 50% | |

### AWS EC2 Credit Reference

| Monthly Uptime | Credit |
|---|---|
| 99.0% – 99.99% | 10% |
| 95.0% – 99.0% | **30%** |
| < 95.0% | 100% |

### AWS Lambda Credit Reference

| Monthly Uptime | Credit |
|---|---|
| 99.0% – 99.95% | 10% |
| 95.0% – 99.0% | 25% |
| < 95.0% | 100% |

---

## Appendix B: Credit Calculation Examples

### Example 1: Atlassian Enterprise at 99.92%

```
actual_uptime_pct = 99.92
tier = "99.90%-99.95% (Enterprise-exclusive)"
credit_pct = 5
monthly_contract = 10000
credit_amount = 10000 * 5 / 100 = 500.00
```

### Example 2: AWS EC2 at 98.5%

```
actual_uptime_pct = 98.5
tier = "95.0%-99.0%"
credit_pct = 30
monthly_ec2_spend = 5000
credit_amount = 5000 * 30 / 100 = 1500.00
claim_deadline_note = "End of second billing cycle after incident month"
```

For incident in November 2024:
- First billing cycle: December 2024 (ends 2024-12-31)
- Second billing cycle: January 2025 (ends 2025-01-31)
- **Claim deadline: 2025-01-31**

### Example 3: AWS Lambda at 97.0%

```
actual_uptime_pct = 97.0
tier = "95.0%-99.0%"
credit_pct = 25
```

---

## Appendix C: Escalation Contact Directory

(Contacts redacted for privacy — refer to internal directory)

| Level | Team/Role | Contact Method |
|---|---|---|
| L1 First Response | On-call Support | PagerDuty rotation |
| L1 Escalation | Support Lead (Alice Wong) | Slack: @alice-wong |
| L2 Escalation | VP Support | Slack: @vp-support |
| AWS Cases | AWS TAM (Technical Account Manager) | AWS Support portal |
| Atlassian Cases | Atlassian Enterprise Support | JSM premium portal |
| Legal Review | Dave Park | Feishu: Dave Park |
| External Partners | Partner Success | Email: partner@nebulatech.com |

---

## Appendix D: Tool Integration Guide

### Jira Service Management Integration

NebulaTech uses JSM REST API for automated ticket processing:

```python
# Example: fetch ticket details
import requests
headers = {"Authorization": f"Bearer {API_TOKEN}"}
resp = requests.get(
    f"https://nebulatech.atlassian.net/rest/api/3/issue/{ticket_id}",
    headers=headers
)
ticket = resp.json()
created_at = ticket["fields"]["created"]
first_response_at = ticket["fields"]["resolutiondate"]  # JSM SLA first response
```

### SLA Calculation Script Integration

Use `scripts/validate_ticket_sla.py` for batch validation:

```bash
python scripts/validate_ticket_sla.py output/breach_tickets_Q4_v3.json
```

Output format:
```json
{
  "validated_count": 185,
  "error_count": 2,
  "invalid_ticket_ids": ["Q4-L2-BREACH-007", "Q4-L1-BREACH-003"]
}
```

---

*End of SLA Compliance Audit Manual v3.0*
*Next revision due: 2025-01-01*
*Questions: sla-policy@nebulatech.com*
