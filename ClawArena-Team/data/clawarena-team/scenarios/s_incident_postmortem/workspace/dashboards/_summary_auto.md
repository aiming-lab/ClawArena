# Dashboard auto-summary (2026-05-12 incident)

> _AUTO-EXPORTED by the on-call Grafana digest job. This file is generated from
> dashboard panel titles + simple threshold heuristics and has known accuracy
> issues. The PNG panels are the authoritative artefacts; this text summary
> may misorder or mislabel the leading signal. Do not cite without
> cross-checking the panel images._

## Leading signal

First panel to cross an alert threshold during the 13:50–14:50 UTC window:

- **Service**: `redis-fleet-2`
- **Metric**: cache evictions/sec
- **First crossing**: 14:18 UTC
- **Peak**: ~18.7k evictions/sec at 14:21 UTC

## Other notable panels

| panel | service | window | observation |
|---|---|---|---|
| memory_pressure | payments-api | 14:23–14:46 | rss climbs past memory limit (~94%) |
| p99_latency_payments | payments-api | 14:24–14:46 | p99 climbs from ~120 ms to ~15 s |
| network_throughput | cdn-router edge-1..3 | 13:50–14:50 | nominal; no edge-node anomaly |

## Notes

The digest job orders panels by **earliest alert-threshold crossing**, not by
causality. Operators have repeatedly flagged that this ordering misidentifies
the leading signal during cascade incidents (a downstream symptom can cross
its threshold before the upstream root cause does). The PNG panels in this
directory contain the actual time-series data and should be inspected
directly when reconstructing the timeline.
