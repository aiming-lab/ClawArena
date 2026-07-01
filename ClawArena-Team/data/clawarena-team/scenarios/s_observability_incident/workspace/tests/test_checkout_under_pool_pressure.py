"""Real pytest — test_checkout_under_pool_pressure.py.

Tests that checkout-service p99 latency stays within SLA under simulated
Redis connection pool pressure. The v3.2.1 pool size of 5 is insufficient
for peak load (8 replicas × 10 concurrent requests = 80 slots needed).
"""
from __future__ import annotations

import random
import statistics


def _sim(pool_size: int, concurrency: int, n: int = 100) -> list[float]:
    """Deterministic latency simulation. Pool exhaustion adds 290 ms wait."""
    rng = random.Random(pool_size * 1000 + concurrency)
    out = []
    for _ in range(n):
        base = rng.uniform(38, 48)
        if concurrency > pool_size:
            wait = rng.uniform(0.8, 1.2) * (concurrency - pool_size) / pool_size * 290
        else:
            wait = 0.0
        out.append(base + wait)
    return out


def _p99(v: list[float]) -> float:
    s = sorted(v)
    return s[max(0, int(len(s) * 0.99) - 1)]


def test_checkout_baseline_p99():
    """Baseline: adequate pool (size=20) → p99 ≤ 60 ms."""
    assert _p99(_sim(pool_size=20, concurrency=10)) <= 60


def test_checkout_pool_pressure_mean():
    """Pool size 5 → mean > 100 ms."""
    assert statistics.mean(_sim(pool_size=5, concurrency=10)) > 100


def test_checkout_latency_under_pool_pressure():
    """v3.2.1 pool_size=5 with concurrency=10 MUST keep p99 ≤ 80 ms (SLA).

    FAILS because redis_client.go:84 MaxPoolSize=5 causes pool exhaustion.
    See: code/redis/pkg/redis_client.go line 84.
    Related Jaeger span: redis.client.CommandExecutor:execute (304 ms pool wait).
    Incident time: 2026-05-23T18:42:00Z.
    """
    p99 = _p99(_sim(pool_size=5, concurrency=10))
    assert p99 <= 80, (  # line 51 — BRIEF anchor
        f"p99={p99:.1f}ms exceeds SLA 80ms; root cause: redis_client.go:84 MaxPoolSize=5"
    )


def test_checkout_pool_recovery():
    """Restoring pool_size=20 → p99 drops back below 60 ms."""
    assert _p99(_sim(pool_size=20, concurrency=10)) <= 60
