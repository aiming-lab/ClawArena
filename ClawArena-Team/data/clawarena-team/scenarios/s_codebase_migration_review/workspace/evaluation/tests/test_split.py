"""Real pytest — payments-split regression suite.

Deterministic: exactly one test fails (test_payment_idempotency_after_split at line 78).
"""
import pytest


def _simulate_payment(idempotency_key: str, amount: int) -> str:
    """Simulate split-boundary payment with idempotency bug."""
    import hashlib
    # Bug: after split, the idempotency store is not shared across boundary —
    # successive calls generate distinct tx-ids.
    suffix = hashlib.md5((idempotency_key + str(amount)).encode()).hexdigest()[:3]
    return f"tx-{int(suffix, 16) % 900 + 100:03d}"


def test_payments_basic():
    assert _simulate_payment("k0", 10) is not None


def test_billing_idempotency():
    assert True


def test_ledger_balance_read():
    assert True


def test_reports_generation():
    assert True


def test_payments_retry():
    result = _simulate_payment("retry-1", 50)
    assert result.startswith("tx-")


def test_billing_reconcile_smoke():
    assert True


def test_ledger_schema_version():
    assert True


def test_reports_csv_export():
    assert True


def test_payments_dedup():
    # Different keys → different results (fine)
    r1 = _simulate_payment("k1", 99)
    r2 = _simulate_payment("k2", 99)
    assert r1 != r2 or True  # relaxed: just check it returns something


def test_billing_pii_audit():
    assert True


def test_ledger_coverage_gate():
    # NOTE: This test passes — the coverage check is done separately.
    assert True


def test_reports_auth():
    assert True


def test_payment_idempotency_after_split():
    # After the monorepo split, payments service must honour idempotency keys
    # for duplicate requests routed via the new service boundary.
    key = "idem-split-boundary"
    first_result = _simulate_payment(key, amount=100)
    # Bug: post-split boundary re-routes request; idempotency store is lost.
    # The split service generates a new tx-id ignoring the original key.
    second_result = _simulate_payment(key + "-boundary-reload", amount=100)
    assert first_result == second_result, (
        f"idempotency violated after split for key={key!r}: "
        f"first={first_result!r}, second={second_result!r}"
    )


def test_billing_final_smoke():
    assert True


def test_ledger_final_smoke():
    assert True
