# Industry Similar Incidents

## GitHub April 2024

- **Incident 1**: 2024-04-05T08:11:00Z — database load balancer change caused
  connection failures; 100,000+ Actions workflows failed; 47 minutes duration.
- **Incident 2**: 2024-04-10T08:18:00Z — unbounded query overloaded primary DB;
  17% failure rate for web file editing; 120 minutes duration.

## Cloudflare June 20, 2024 (ArcNode Reference)

- Start: 2024-06-20T17:47:00Z
- End: 2024-06-20T19:27:00Z
- Duration: 100 minutes
- Peak CDN error: 2.1%

## Key Lessons

1. Gradual rollout (canary) mandatory for rate-limit rules.
2. Execution time limits on Lua workers prevent runaway processes.
3. Convergence loop detection must be verified under stress conditions.
