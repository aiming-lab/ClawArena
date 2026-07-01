#!/usr/bin/env bash
# Run the CVE-2024-47081 regression test suite.
# Usage: ./scripts/run_regression.sh [--verbose]

set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_FILE="${WORKSPACE_DIR}/tests/test_utils_regression.py"
RESULTS_DIR="${WORKSPACE_DIR}/test_results"

mkdir -p "${RESULTS_DIR}"

if [ ! -f "${TEST_FILE}" ]; then
    echo "ERROR: Regression test file not found: ${TEST_FILE}" >&2
    exit 1
fi

echo "Running CVE-2024-47081 regression tests..."
python -m pytest "${TEST_FILE}" -v --tb=short 2>&1 | tee "${RESULTS_DIR}/regression_run.txt"

EXIT_CODE=${PIPESTATUS[0]}

if [ ${EXIT_CODE} -eq 0 ]; then
    echo "All regression tests PASSED."
else
    echo "Some regression tests FAILED. See ${RESULTS_DIR}/regression_run.txt"
fi

exit ${EXIT_CODE}
