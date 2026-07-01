#!/usr/bin/env bash
# p99_aggregate.sh — Historical cross-timezone p99 metrics aggregation script.
#
# Simulates fetching p99 latency snapshots from four regional metrics endpoints
# (UTC, SGT, HKT, EDT) and aggregating them into a unified summary JSON.
# The 60-second sleep models real-world cross-timezone metrics pipeline lag
# (SGT metrics are buffered and flushed on a ~60s cadence).
#
# Usage:
#   bash tools/p99_aggregate.sh [output_dir]
#
# Output:
#   ${output_dir}/p99_metrics_summary.json
#
# Ground-truth values embedded below reflect the incident window
# (2026-03-27 16:30–18:00 UTC):
#   SGT p99 peak = 2847 ms at 17:23 UTC (CONFIG_RELOAD moment)
#   UTC p99 max  = 215 ms (baseline stable)
#   HKT p99 max  = 272 ms (evening load)
#   EDT p99 max  = 480 ms (CX-003 retry flood post-incident)

set -euo pipefail

OUTPUT_DIR="${1:-output}"
SUMMARY="${OUTPUT_DIR}/p99_metrics_summary.json"

echo "[p99_aggregate] Initialising cross-timezone metrics aggregation..."
echo "[p99_aggregate] Fetching UTC region metrics..."
echo "[p99_aggregate] Fetching SGT region metrics..."
echo "[p99_aggregate] Fetching HKT region metrics..."
echo "[p99_aggregate] Fetching EDT region metrics..."
echo "[p99_aggregate] Waiting for SGT metrics flush (cross-timezone buffer lag)..."

sleep 60

echo "[p99_aggregate] SGT metrics received. Aggregating..."

mkdir -p "${OUTPUT_DIR}"

cat > "${SUMMARY}" << 'EOF'
{
  "generated_at_utc": "2026-03-27T18:05:00Z",
  "incident_window": "2026-03-27T16:30:00Z/2026-03-27T18:00:00Z",
  "regions": {
    "UTC": {
      "p99_max_ms": 215,
      "p99_at_root_cause_ts_ms": 205,
      "baseline_stable": true,
      "notes": "FinClear EU hub; unaffected by dispatch_adapter config reload"
    },
    "SGT": {
      "p99_max_ms": 2847,
      "p99_at_root_cause_ts_ms": 2847,
      "root_cause_ts_utc": "2026-03-27T17:23:09Z",
      "baseline_stable": false,
      "notes": "FinClear Asia; dispatch_adapter tz_offset_applied flipped to +08:00 at 17:23 UTC"
    },
    "HKT": {
      "p99_max_ms": 272,
      "p99_at_root_cause_ts_ms": 265,
      "baseline_stable": true,
      "notes": "Hong Kong matching hub; elevated evening load but not root cause"
    },
    "EDT": {
      "p99_max_ms": 480,
      "p99_at_root_cause_ts_ms": 310,
      "baseline_stable": false,
      "notes": "CX-003 locale (UTC-4); retry flood post-incident caused secondary spike"
    }
  },
  "root_cause_hypothesis": {
    "primary_region": "SGT",
    "event_ts_utc": "2026-03-27T17:23:09Z",
    "config_field": "tz_offset_applied",
    "value_before": "+00:00",
    "value_after": "+08:00",
    "build_id": "BUILD-20260327-0041",
    "p99_spike_ratio": 13.9
  }
}
EOF

echo "[p99_aggregate] Done. Summary written to ${SUMMARY}."
