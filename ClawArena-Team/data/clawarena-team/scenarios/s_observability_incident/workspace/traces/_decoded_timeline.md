# Decoded Jaeger Timeline — 2026-05-23T18:42Z spike

Exported from `traces/jaeger_2026-05-23.json`.  Spans sorted by start time.

| span_id  | service           | operation                                | start offset (ms) | duration (ms) | note |
|---|---|---|---|---|---|
| span_01  | api-gateway       | http.request POST /api/v2/checkout       | 0.0               | 320.4         | root span |
| span_02  | checkout-service  | checkout.ProcessRequest                  | 1.0               | 318.9         | |
| span_03  | checkout-service  | redis.client.CommandExecutor:execute     | 2.5               | **304.0**     | **SLOW — pool.wait_ms=302** |
| span_04  | order-service     | order.createOrder                        | 310.0             | 6.2           | |
| span_05  | order-service     | postgres.INSERT                          | 310.8             | 5.1           | |

Key observations:
- span_03 accounts for 304 ms out of 320 ms total — the bottleneck.
- `pool.size=5`, `pool.active=5` → all slots occupied when GET session arrives.
- `pool.wait_ms=302` confirms connection pool exhaustion, not Redis server latency.
- postgres (span_05) is healthy at 5.1 ms — not the root cause.
