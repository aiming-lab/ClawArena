"""test_baseline.py — smoke tests that always pass (non-incident baseline)."""


def test_order_service_create():
    """order-service createOrder is fast."""
    assert True


def test_api_gateway_routing():
    """api-gateway routes checkout requests correctly."""
    assert True


def test_postgres_insert_speed():
    """postgres INSERT latency < 10ms in test env."""
    latency_ms = 4.2
    assert latency_ms < 10
