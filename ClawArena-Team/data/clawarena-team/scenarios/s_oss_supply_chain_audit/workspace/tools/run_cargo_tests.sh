#!/usr/bin/env bash
# run_cargo_tests.sh — Run the Rust test suite for mase-sim (pre-vendored).
# Usage: bash tools/run_cargo_tests.sh
# The test suite is in source_code/rust_pkg/.
# test_path_traversal_guard is expected to fail (CVE-2026-21847).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
RUST_PKG="$WORKSPACE_ROOT/source_code/rust_pkg"

echo "=== cargo test — mase-sim rust_pkg ==="
echo "Working directory: $RUST_PKG"
echo ""

# If cargo is available, run it. Otherwise emit the pre-generated stderr.
if command -v cargo &>/dev/null 2>&1; then
    cd "$RUST_PKG"
    cargo test --offline 2>&1 || true
else
    # Sandbox fallback: emit pre-generated stderr output
    cat <<'PREGEN'
running 3 tests
test tests::test_safe_path_resolution ... ok
test tests::test_null_byte_rejection ... ok
test tests::test_path_traversal_guard ... FAILED

failures:

---- tests::test_path_traversal_guard stdout ----
thread 'tests::test_path_traversal_guard' panicked at 'path traversal guard bypass detected for input: %2e%2e/etc/passwd', lib.rs:113
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace

failures:
    tests::test_path_traversal_guard

test result: FAILED. 2 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.003s

FAIL
PREGEN
fi
