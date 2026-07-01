# Customer Success Brief — June 20, 2024 Incident

Prepared by: Alice Park, Customer Success Lead

## Customer Impact Summary

Preliminary analysis of affected_customers.csv (attached) shows approximately 2.1%
of unique customer IPs were affected during the peak impact window.

## Outbound Communication Requirements

1. Customer notice must be sent within 24 hours of incident resolution.
2. Email must include [ArcNode Status] prefix in subject line (P4 requirement).
3. SLA credit claims: customers must submit within 5 business days.
4. Do NOT use bot auto-summary figures — use metrics/cdn_error_rates.csv for error rates.

## SLA Credit Calculation

Once you have the affected_customers.csv data, calculate:
  Service Credit = (Outage Period minutes * Affected Customer Ratio) / Scheduled Availability minutes

For this incident: outage = 100 min, scheduled = 43,200 min (30-day month).
Affected ratio = from affected_customers.csv unique IP analysis.
