# NebulaTech Escalation Policy v2.0 (Revised)

## Change Log

v2.0 (2025-02-01): L2 response time tightened from 2 hours to **90 minutes** based on
internal capacity review. New escalation trigger added for L2 at 90-minute threshold.

## 1. Scope

This policy applies to all Jira Service Management (JSM) tickets under the
Atlassian Enterprise plan. SLA thresholds are drawn from the official
Atlassian Support Offerings documentation, with NebulaTech internal adjustments.

## 2. Severity Classification (v2)

| Severity | Definition | Response SLA | Coverage |
|----------|-----------|--------------|----------|
| L1 | Production system completely unavailable | 30 minutes | 24/7 |
| L2 | Serious degradation — core features impaired | **90 minutes** (revised from 2h) | 24/7 |
| L3 | Moderate impact — some features affected | 8 hours | Weekdays |
| L4 | Limited impact — minor or cosmetic issue | 24 hours | Weekdays |

## 3. L2 Upgrade Trigger (NEW in v2)

A ticket is automatically escalated to Level 1 when L2 first response has not been
received within **90 minutes** of ticket creation. This is tighter than the Atlassian
Enterprise baseline of 2 hours, reflecting NebulaTech's internal customer commitment.

## 4. Escalation Triggers (all severities)

A ticket is escalated when `first_response_at - created_at > response_sla_minutes`.

Escalation levels:
- **Level 1 Escalation**: SLA breach detected → auto-alert to L1 Support Lead
- **Level 2 Escalation**: Breach > 2× SLA → escalate to VP Support
- **Level 3 Escalation**: Breach > 4× SLA → escalate to CTO

## 5. Credit Calculation

(Unchanged from v1 — credit tiers based on Atlassian Enterprise SLA)

For Atlassian Cloud Enterprise:
- Monthly uptime 99.90%–99.95%: 5% service credit
- Monthly uptime 99.00%–99.90%: 10% service credit
- Monthly uptime 95.00%–99.00%: 25% service credit
- Monthly uptime < 95.00%: 50% service credit

Source: https://www.atlassian.com/legal/sla
