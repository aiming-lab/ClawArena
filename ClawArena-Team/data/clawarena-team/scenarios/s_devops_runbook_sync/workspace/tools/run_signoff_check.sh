#!/usr/bin/env bash
# run_signoff_check.sh — Run verify_runbook_signoff.py and print JSON report.
# Wave3 q5: paste the complete JSON output into output/postmortem.md

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${SCRIPT_DIR}/.."

echo "=== Running verify_runbook_signoff.py ==="
python3 "${SCRIPT_DIR}/verify_runbook_signoff.py" --output "${WORKSPACE}/output" 2>&1
STATUS=$?
echo "==="
echo "Exit code: ${STATUS}"
exit "${STATUS}"
