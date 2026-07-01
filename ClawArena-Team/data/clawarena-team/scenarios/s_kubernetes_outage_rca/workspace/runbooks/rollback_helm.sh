#!/usr/bin/env bash
# rollback_helm.sh — Roll back a helm release to the previous revision
# Usage: ./rollback_helm.sh <release-name> [namespace]
set -euo pipefail
RELEASE="${1:?Usage: $0 <release-name> [namespace]}"
NS="${2:-payments}"
echo "[INFO] Current helm history for ${RELEASE} in ${NS}:"
helm history "${RELEASE}" -n "${NS}"
PREV=$(helm history "${RELEASE}" -n "${NS}" --output json | \
  python3 -c "import sys,json; h=json.load(sys.stdin); print(sorted(h,key=lambda x:x['revision'])[-2]['revision'])")
echo "[INFO] Rolling back to revision ${PREV}"
helm rollback "${RELEASE}" "${PREV}" -n "${NS}" --wait --timeout 5m
echo "[DONE] Rollback complete."
