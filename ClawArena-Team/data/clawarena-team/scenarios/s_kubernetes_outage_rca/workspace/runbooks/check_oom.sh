#!/usr/bin/env bash
# check_oom.sh — Query recent OOM-killer events from kubelet logs
# Usage: ./check_oom.sh [namespace]
set -euo pipefail
NS="${1:-payments}"
echo "[INFO] Querying OOM events in namespace ${NS}"
kubectl get events -n "${NS}" --field-selector reason=OOMKilling \
  --sort-by='.lastTimestamp' | tail -20
echo ""
echo "[INFO] Checking kubelet journal for oom_kill entries"
journalctl -u kubelet --since "1 hour ago" | grep -i "oom\|killed\|memory" | tail -30
