#!/usr/bin/env bash
# etl_pause.sh — Pause / resume analytics ETL jobs (wave3)

set -euo pipefail

ACTION="${1:-status}"
SCHEDULER="https://scheduler.mercatorrobotics.internal"
JOBS=(
    "etl-analytics-billing-hourly"
    "etl-analytics-payments-daily"
    "etl-reporting-aggregate-weekly"
)

case "$ACTION" in
    pause)
        for job in "${JOBS[@]}"; do
            curl -sf -X POST "${SCHEDULER}/jobs/${job}/pause" && echo "Paused: $job" || true
        done ;;
    resume)
        for job in "${JOBS[@]}"; do
            curl -sf -X POST "${SCHEDULER}/jobs/${job}/resume" && echo "Resumed: $job" || true
        done ;;
    status)
        for job in "${JOBS[@]}"; do
            st=$(curl -sf "${SCHEDULER}/jobs/${job}/status" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('state','?'))" 2>/dev/null || echo "?")
            echo "${job}: ${st}"
        done ;;
    *)
        echo "Usage: $0 {pause|resume|status}"; exit 1 ;;
esac
