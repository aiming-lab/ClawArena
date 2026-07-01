#!/usr/bin/env bash
# drain_node.sh — Cordon and drain a node safely
# Usage: ./drain_node.sh <node-name>
set -euo pipefail
NODE="${1:?Usage: $0 <node-name>}"
echo "[INFO] Cordoning node ${NODE}"
kubectl cordon "${NODE}"
echo "[INFO] Draining node ${NODE} (ignore daemonsets, delete emptydir)"
kubectl drain "${NODE}" \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --grace-period=60 \
  --timeout=300s
echo "[DONE] Node ${NODE} drained. Safe to perform maintenance."
