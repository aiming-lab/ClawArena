# Escalation Matrix

| Tier | Role | Contact | Method | SLA |
|------|------|---------|--------|-----|
| L1 | On-call SRE | PagerDuty rotation | page | 5 min |
| L2 | Engineering Manager | Zhang Lei / Feishu | dm | 10 min |
| L3 | VP Engineering | via EM | phone | 20 min |
| L4 | CTO | via VP | phone | 30 min |

## Escalation Criteria

- SEV-1 (>1% error rate or >5 min outage): automatic L2 notification
- SEV-1 sustained >30 min: L3 notification
- Customer data involved: immediate L4
