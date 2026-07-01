#!/bin/bash
# scan_repo.sh — TruffleHog repository secret scanner
# Source: https://github.com/trufflesecurity/trufflehog
# Ground-truth: --fail flag causes exit code 183 when secrets are found
# Ground-truth: verified secrets show status field "Verified"

set -euo pipefail

REPO_PATH="${1:-.}"
OUTPUT_FILE="${2:-trufflehog_results.json}"

echo "Starting TruffleHog scan on: ${REPO_PATH}"
echo "Output: ${OUTPUT_FILE}"

# Run TruffleHog with JSON output and fail-on-findings mode
# Exit code 183 = credentials found (--fail flag)
# Exit code 0 = no credentials found
# The DetectorName field identifies the secret type
trufflehog git "file://${REPO_PATH}" \
    --json \
    --fail \
    --results=verified \
    2>&1 | tee "${OUTPUT_FILE}"

EXIT_CODE=$?
if [ $EXIT_CODE -eq 183 ]; then
    echo "ALERT: TruffleHog found verified secrets (exit code 183)"
    echo "Check ${OUTPUT_FILE} for findings with 'Verified': true"
elif [ $EXIT_CODE -eq 0 ]; then
    echo "CLEAN: No verified secrets found (exit code 0)"
else
    echo "ERROR: TruffleHog exited with code ${EXIT_CODE}"
fi

exit $EXIT_CODE
