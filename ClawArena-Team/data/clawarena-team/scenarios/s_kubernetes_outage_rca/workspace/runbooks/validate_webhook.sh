#!/usr/bin/env bash
# validate_webhook.sh — Test admission webhook with a dry-run pod spec
# Usage: ./validate_webhook.sh <webhook-name>
set -euo pipefail
WEBHOOK="${1:-payment-admission-webhook}"
echo "[INFO] Checking webhook configuration:"
kubectl get validatingwebhookconfigurations "${WEBHOOK}" -o yaml
echo ""
echo "[INFO] Dry-run pod creation in payments namespace:"
kubectl run test-pod --image=nginx:alpine --dry-run=server -n payments \
  --restart=Never 2>&1 || true
echo "[DONE] Webhook validation complete."
