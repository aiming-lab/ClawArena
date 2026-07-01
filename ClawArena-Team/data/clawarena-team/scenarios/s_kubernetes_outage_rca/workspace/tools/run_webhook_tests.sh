#!/usr/bin/env bash
# run_webhook_tests.sh — Run Go webhook tests with race detection.
# If the 'go' binary is not available, falls back to a pre-generated stderr
# that contains the expected failing test output.
#
# Usage: bash tools/run_webhook_tests.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS_ROOT="$(dirname "$SCRIPT_DIR")"
WEBHOOK_DIR="$WS_ROOT/webhook_src"
PREGENERATED="$WEBHOOK_DIR/pregenerated_test_stderr.txt"

if command -v go &>/dev/null; then
    cd "$WEBHOOK_DIR"
    # -race enables the Go race detector; test WILL fail on ConcurrentAccess
    go test -race ./... 2>&1 || true
else
    echo "[INFO] 'go' binary not found — using pre-generated test output" >&2
    cat "$PREGENERATED"
fi
