#!/usr/bin/env bash
# get_metrics.sh — Dump resource usage for payment-svc pods
# Usage: ./get_metrics.sh
set -euo pipefail
NS="payments"
echo "[INFO] Pod resource usage in namespace ${NS}:"
kubectl top pods -n "${NS}" --containers 2>/dev/null || \
  echo "[WARN] metrics-server may be unavailable"
echo ""
echo "[INFO] Node resource usage:"
kubectl top nodes
echo ""
echo "[INFO] HPA status:"
kubectl get hpa -n "${NS}" -o wide
