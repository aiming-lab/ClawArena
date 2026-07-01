#!/usr/bin/env bash
# run_npm_tests.sh — Run the JS test suite for mase-js-bridge (pre-vendored).
# Usage: bash tools/run_npm_tests.sh
# The test suite is in source_code/js_pkg/.
# test_input_sanitizer is expected to fail (broken sanitizeHtml).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"
JS_PKG="$WORKSPACE_ROOT/source_code/js_pkg"

echo "=== npm test — mase-js-bridge ==="
echo "Working directory: $JS_PKG"
echo ""

# If node is available, run it. Otherwise emit the pre-generated stderr.
if command -v node &>/dev/null 2>&1; then
    node "$JS_PKG/tests/sanitizer.test.js" 2>&1 || true
else
    # Sandbox fallback: emit pre-generated stderr output
    cat <<'PREGEN'
  ✓ test_sanitize_text
  ✓ test_sanitize_path
  ✗ test_input_sanitizer
    AssertionError [ERR_ASSERTION]: sanitizeHtml failed to fully strip obfuscated script: got "<scr>ipt>alert(document.cookie)</scr>ipt>"
    at sanitizer.test.js:47
  ✓ test_sanitize_html_basic

Tests: 4 | Passed: 3 | Failed: 1

FAIL
PREGEN
fi
