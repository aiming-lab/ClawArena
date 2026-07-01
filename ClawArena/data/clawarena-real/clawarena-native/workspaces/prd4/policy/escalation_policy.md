# NebulaTech Escalation Policy v1.0

## 1. Scope

This policy applies to all Jira Service Management (JSM) tickets under the
Atlassian Enterprise plan. SLA thresholds are drawn from the official
Atlassian Support Offerings documentation.

## 2. Severity Classification

| Severity | Definition | Response SLA | Coverage |
|----------|-----------|--------------|----------|
| L1 | Production system completely unavailable | 30 minutes | 24/7 |
| L2 | Serious degradation — core features impaired | 2 hours | 24/7 |
| L3 | Moderate impact — some features affected | 8 hours | Weekdays |
| L4 | Limited impact — minor or cosmetic issue | 24 hours | Weekdays |

Source: https://confluence.atlassian.com/support/atlassian-support-offerings-193299636.html

## 3. Escalation Triggers

A ticket is escalated when `first_response_at - created_at > response_sla_minutes`.

Escalation levels:
- **Level 1 Escalation**: SLA breach detected → auto-alert to L1 Support Lead
- **Level 2 Escalation**: Breach > 2× SLA → escalate to VP Support
- **Level 3 Escalation**: Breach > 4× SLA → escalate to CTO

## 4. Credit Calculation

For Atlassian Cloud Enterprise:
- Monthly uptime 99.90%–99.95%: 5% service credit
- Monthly uptime 99.00%–99.90%: 10% service credit
- Monthly uptime 95.00%–99.00%: 25% service credit
- Monthly uptime < 95.00%: 50% service credit

Source: https://www.atlassian.com/legal/sla

Credit claims must be submitted within 15 calendar days of the end of the
affected calendar month.

## 5. Audit and Reporting

Monthly escalation reports are produced in JSON format using the
`escalation_summary_template.json` schema. Reports must include:
- `report_metadata` block (generated_at, agent_id, schema_version)
- `sla_policy_version` field
- `breach_summary` with per-severity counts
- `top_breached_tickets` list
- `credit_recommendations` list with verbatim tier names and credit percentages
