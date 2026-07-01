#!/usr/bin/env bash
# collect_logs.sh — Collect logs from all payment-svc pods
# Usage: ./collect_logs.sh [output-dir]
set -euo pipefail
OUT="${1:-/tmp/incident-logs}"
NS="payments"
mkdir -p "${OUT}"
echo "[INFO] Collecting logs from namespace ${NS}"
for POD in $(kubectl get pods -n "${NS}" -l app=payment-svc -o name); do
  PODNAME=$(basename "${POD}")
  echo "[INFO] Collecting ${PODNAME}"
  kubectl logs "${POD}" -n "${NS}" --since=2h > "${OUT}/${PODNAME}.log" 2>&1 || true
  kubectl logs "${POD}" -n "${NS}" --previous > "${OUT}/${PODNAME}.previous.log" 2>&1 || true
done
echo "[DONE] Logs saved to ${OUT}"
