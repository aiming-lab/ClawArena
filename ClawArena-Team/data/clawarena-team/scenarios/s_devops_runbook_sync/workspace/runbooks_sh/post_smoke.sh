#!/usr/bin/env bash
# post_smoke.sh — Post-migration smoke test (wave3)

set -euo pipefail

PAYMENT_URL="${PAYMENT_URL:-https://payment-service.mercatorrobotics.internal}"
BILLING_URL="${BILLING_URL:-https://billing-service.mercatorrobotics.internal}"

check_health() {
    local name="$1" url="$2"
    code=$(curl -sf -o /dev/null -w "%{http_code}" "$url/healthz" 2>/dev/null) || code="000"
    if [ "$code" = "200" ]; then
        echo "  OK: $name health check ($code)"
    else
        echo "  FAIL: $name returned HTTP $code"
        return 1
    fi
}

echo "[SMOKE] Running post-migration health checks..."
check_health "payment-service" "$PAYMENT_URL"
check_health "billing-service" "$BILLING_URL"
echo "[SMOKE] All smoke tests passed."
