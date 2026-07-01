# ArcNode Incident Response Runbook

## SEV-1 Initial Response (0-15 minutes)

1. Acknowledge PagerDuty alert within 5 minutes.
2. Post incident start message to #incidents Slack channel.
3. Start incident timeline in postmortem/DRAFT.md.
4. Identify impacted services from raw_alerts.jsonl.
5. Page EM (Zhang Lei) via Feishu DM if SEV-1.

## Investigation (15-60 minutes)

1. Identify root cause chain(s) from alert and metric logs.
2. Check for multi-causal incidents — look for concurrent events in backbone_events.jsonl.
3. Isolate Traffic Manager route convergence issues via traffic_manager_log.jsonl.
4. Escalate to relevant on-call engineers via #incidents or Feishu group.

## Mitigation

1. Disable triggering rule if identified (DDoS rule, etc.).
2. Restart poisoned worker processes.
3. Monitor cdn_error_rates.csv for recovery.

## Communication

- Post status updates to #incidents every 15 minutes.
- Send customer-facing notice via email_thread.eml template.
- Tag all messages with [ArcNode Status] prefix.

## Post-Incident

1. Mark incident resolved when error rate returns to baseline.
2. Begin postmortem within 24 hours.
3. Submit corrective actions to corrective_actions/action_items_v1.json.
4. SLA claims: customers must submit within 5 business days.
