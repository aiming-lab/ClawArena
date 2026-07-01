# ArcNode Business Service Level Agreement

_Based on Cloudflare Business SLA (https://www.cloudflare.com/business-sla/)._

## Uptime Commitment / 正常运行时间承诺

ArcNode commits to 100% uptime for covered services.

## Service Credit Formula / 积分计算公式

When an incident causes a measurable outage, customers may claim service credits
calculated as:

> **Service Credit = (Outage Period minutes * Affected Customer Ratio) / Scheduled Availability minutes**

Where:
- **Outage Period minutes** = duration in minutes of the confirmed outage
- **Affected Customer Ratio** = unique customer IPs affected / total unique customer IPs
- **Scheduled Availability minutes** = total minutes in the billing period

## Claim Deadline / 申领截止日期

Customers must submit credit claims within **5 business days** of the
incident date. Claims submitted after this deadline will not be processed.

## Maximum Annual Credits / 年度最高积分

Total credits in any 12-month period may not exceed one month's cumulative service fees.

## Exclusions / 排除条款

Service credits do not apply to outages caused by:
- Customer-controlled infrastructure failures
- Third-party service interruptions outside ArcNode's reasonable control
- Scheduled maintenance windows (announced ≥ 72 hours in advance)

## SLA for the June 20, 2024 Incident

- Outage period: 100 minutes
- Affected customer ratio: to be determined from affected_customers.csv (see Update 1)
- Scheduled availability: 43200 minutes (30-day billing month)
