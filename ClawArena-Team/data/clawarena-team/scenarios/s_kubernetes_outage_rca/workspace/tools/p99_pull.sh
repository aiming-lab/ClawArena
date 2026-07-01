#!/usr/bin/env bash
# p99_pull.sh — Historical p99 latency aggregation across clusters.
#
# Usage:   bash tools/p99_pull.sh [--out <path>] [--window <minutes>]
#
# This script simulates cross-cluster metrics aggregation.
# Each cluster endpoint requires ~20s to respond; total runtime
# is ~60s for 3 clusters.  Run in background while the main agent
# continues synthesising evidence:
#
#   bash tools/p99_pull.sh --out output/p99_metrics.json &
#   P99_PID=$!
#   # ... do other work ...
#   wait $P99_PID

set -euo pipefail

OUT_FILE="output/p99_metrics.json"
WINDOW_MINUTES=30
INCIDENT_START="2026-05-14T03:00:00Z"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out)    OUT_FILE="$2";       shift 2 ;;
    --window) WINDOW_MINUTES="$2"; shift 2 ;;
    *)        shift ;;
  esac
done

mkdir -p "$(dirname "$OUT_FILE")"

CLUSTERS=(
  "cluster-eu-west-2:https://prometheus.eu-west-2.internal/api/v1/query_range"
  "cluster-us-east-1:https://prometheus.us-east-1.internal/api/v1/query_range"
  "cluster-ap-southeast-1:https://prometheus.ap-southeast-1.internal/api/v1/query_range"
)

QUERY='histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{service="payment-svc"}[1m]))'

echo "[p99_pull] Starting historical p99 aggregation — window=${WINDOW_MINUTES}m from ${INCIDENT_START}" >&2

# Simulated cross-cluster aggregation delay
# (real endpoints would each take ~15-25s due to long-range query)
echo "[p99_pull] Querying cluster-eu-west-2 ..." >&2
sleep 20
echo "[p99_pull] Querying cluster-us-east-1 ..." >&2
sleep 20
echo "[p99_pull] Querying cluster-ap-southeast-1 ..." >&2
sleep 20

# Emit pre-computed results (sandbox: actual Prometheus not available)
cat > "$OUT_FILE" <<'EOF_JSON'
{
  "incident": "INC-2026-0514-001",
  "window_start": "2026-05-14T03:00:00Z",
  "window_end":   "2026-05-14T03:30:00Z",
  "resolution":   "1m",
  "clusters": {
    "cluster-eu-west-2": {
      "p99_peak_ms":    850,
      "p99_peak_at":    "2026-05-14T03:15:00Z",
      "p99_baseline_ms": 95,
      "spike_duration_minutes": 10,
      "note": "OOM cascade 03:10-03:20 UTC; validateNamespace race + helm 1.18.3 regression"
    },
    "cluster-us-east-1": {
      "p99_peak_ms":    128,
      "p99_peak_at":    null,
      "p99_baseline_ms": 118,
      "spike_duration_minutes": 0,
      "note": "Unaffected — different helm chart version deployed"
    },
    "cluster-ap-southeast-1": {
      "p99_peak_ms":    172,
      "p99_peak_at":    "2026-05-14T03:12:00Z",
      "p99_baseline_ms": 145,
      "spike_duration_minutes": 2,
      "note": "Minor ripple from shared cache invalidation; recovered quickly"
    }
  },
  "root_cause_cluster": "cluster-eu-west-2",
  "figures": ["figures/p99_cluster_view.png"]
}
EOF_JSON

echo "[p99_pull] Done. Results written to ${OUT_FILE}" >&2
