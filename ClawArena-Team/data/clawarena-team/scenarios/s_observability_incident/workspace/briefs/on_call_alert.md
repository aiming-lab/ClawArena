# On-Call Alert — 2026-05-23T18:42:15Z

**Severity:** SEV-2
**Service:** checkout-service
**Signal:** p99 latency spike

## What fired

PagerDuty: `checkout-service.p99_latency > 200ms for 3 consecutive minutes`

## Metrics at alert time

| metric | baseline | current |
|---|---|---|
| p99 latency | 42 ms | 320 ms |
| error rate | 0.2% | 12% |
| req/s | 840 | 810 |

## Relevant links

- Jaeger trace: `traces/jaeger_2026-05-23.json`
- Dashboard: `dashboards/p99_chart.png`
- Slack thread: `briefs/slack_thread.md`

On-call rotation: **sre-team-2** → you are primary.
