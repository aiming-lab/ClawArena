#!/usr/bin/env bash
# run_backtest_tests.sh — Run AlphaWave-7 backtest pytest suite.
#
# Usage: bash tools/run_backtest_tests.sh
#
# Runs pytest on backtest_code/tests/ and prints full output to stdout+stderr.
# Used by q4 to obtain the failing test name and line number.
#
# Expected: TestSignalAlignment FAILS (look-ahead bias test).
#           All risk tests (test_risk.py) PASS.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"

# Run pytest on the test suite
# -v: verbose output (test names)
# -x: stop at first failure (show full error)
# --tb=short: short traceback
python -m pytest "$WORKSPACE_ROOT/backtest_code/tests/" -v --tb=short 2>&1 || true

# Note: exit code is not passed up; the test output itself is the evidence.
echo ""
echo "run_backtest_tests.sh complete."
