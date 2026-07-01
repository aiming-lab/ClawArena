# Dashboards

Snapshots exported from the on-call Grafana board, covering 2026-05-12 13:50–14:50 UTC (the incident window). All four are PNGs at 1100×620.

- `memory_pressure.png` — per-service rss as percentage of memory limit.
- `cache_evictions.png` — `redis-fleet-2` (and `-1` for reference) evictions/sec.
- `p99_latency_payments.png` — payments-api p50 and p99 latency.
- `network_throughput.png` — cdn-router edge nodes.
- `_summary_auto.md` — auto-exported text digest. **Unreliable** — misorders
  the leading signal. The PNG panels are authoritative; see q3 honey-pot.
