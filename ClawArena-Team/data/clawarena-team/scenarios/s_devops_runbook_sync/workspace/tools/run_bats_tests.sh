#!/usr/bin/env bash
# tools/run_bats_tests.sh — Run shellcheck + bats tests on runbook shell scripts.
#
# Usage: bash tools/run_bats_tests.sh
# Output: stderr merged into stdout for capture by calling agent.
#
# This script:
# 1. Runs shellcheck on runbooks_sh/pre_check.sh (catches SC2086 on line 31)
# 2. Runs the bats test suite in runbooks_sh/tests/
#    (pre_migration_checks.bats:23 assertion FAILS — LOCK_TIMEOUT_REQUIRED not emitted)
#
# The agent MUST run this script via Bash to capture the real stderr output.
# Do not attempt to infer results without running the script.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
RUNBOOKS_SH="${WORKSPACE_ROOT}/runbooks_sh"
TESTS_DIR="${RUNBOOKS_SH}/tests"
BATS_CORE="${TESTS_DIR}/bats-core"

echo "=== ShellCheck Analysis ==="
echo "Running shellcheck on ${RUNBOOKS_SH}/pre_check.sh"
echo ""

# Run shellcheck — will emit SC2086 warning on pre_check.sh line 31
if command -v shellcheck >/dev/null 2>&1; then
    shellcheck "${RUNBOOKS_SH}/pre_check.sh" 2>&1 || true
else
    # Fallback: emit the expected shellcheck output manually
    # (for environments where shellcheck is not in PATH)
    echo "In ${RUNBOOKS_SH}/pre_check.sh line 31:"
    echo "if ! ls migrations/\$MIGRATION_ID 2>/dev/null; then"
    echo "                  ^-----------^ SC2086 (warning): Double quote to prevent globbing"
    echo "                  and word splitting."
    echo "  Double quote to prevent globbing and word splitting."
    echo "For more information:"
    echo "  https://www.shellcheck.net/wiki/SC2086 -- Double quote to prevent globbing ..."
    echo ""
    echo "pre_check.sh line 31: SC2086: Double quote to prevent globbing and word splitting"
fi

echo ""
echo "=== Bats Test Suite ==="
echo "Running: ${TESTS_DIR}/pre_migration_checks.bats"
echo ""

# Run bats tests using vendored bats-core
# Test 1 (line 23) WILL FAIL: assert_output --partial "LOCK_TIMEOUT_REQUIRED"
# The script outputs "LOCK_TIMEOUT_MS=5000" not the literal "LOCK_TIMEOUT_REQUIRED"

cd "${WORKSPACE_ROOT}"

# Source bats helpers and run tests manually (vendored stub runner)
run_bats_test() {
    local test_name="$1"
    local test_body="$2"
    local line_no="$3"

    # Set up environment
    export DB_HOST="localhost"
    export DB_PORT="5432"
    export DB_NAME="billing_test"
    export MIGRATION_ID="V0234__add_idempotency_keys.sql"
    export APPROVER_SRE_MANAGER="test-sre-manager"
    export APPROVER_DBA_LEAD="test-dba-lead"
    export LOCK_TIMEOUT_MS="5000"
    export SCHEDULER_URL="http://mock-scheduler.test"

    echo "=== RUN   ${test_name}"
    local output
    output=$(bash "${RUNBOOKS_SH}/pre_check.sh" 2>&1 || true)

    case "$test_name" in
        *LOCK_TIMEOUT_REQUIRED*)
            # This test FAILS: the script does not print "LOCK_TIMEOUT_REQUIRED"
            if echo "$output" | grep -q "LOCK_TIMEOUT_REQUIRED"; then
                echo "    ${TESTS_DIR}/pre_migration_checks.bats:${line_no}: PASS"
                echo "--- PASS: ${test_name} (0.01s)"
                return 0
            else
                echo "    ${TESTS_DIR}/pre_migration_checks.bats:${line_no}: assert_output --partial \"LOCK_TIMEOUT_REQUIRED\" failed"
                echo "    Expected partial output: LOCK_TIMEOUT_REQUIRED"
                echo "    Actual output (first 3 lines):"
                echo "$output" | head -3 | sed 's/^/      /'
                echo "--- FAIL: ${test_name} (0.01s)"
                return 1
            fi
            ;;
        *MIGRATION_ID*)
            if echo "$output" | grep -q "Migration ID format valid"; then
                echo "--- PASS: ${test_name} (0.01s)"
                return 0
            else
                echo "    ${TESTS_DIR}/pre_migration_checks.bats: assert_output failed"
                echo "--- FAIL: ${test_name} (0.01s)"
                return 1
            fi
            ;;
        *dual\ approval*)
            if echo "$output" | grep -q "test-sre-manager"; then
                echo "--- PASS: ${test_name} (0.01s)"
                return 0
            else
                echo "--- FAIL: ${test_name} (0.01s)"
                return 1
            fi
            ;;
        *APPROVER_SRE_MANAGER*)
            local out2
            out2=$(APPROVER_SRE_MANAGER="" bash "${RUNBOOKS_SH}/pre_check.sh" 2>&1 || true)
            if echo "$out2" | grep -q "APPROVER_SRE_MANAGER not set"; then
                echo "--- PASS: ${test_name} (0.01s)"
                return 0
            else
                echo "--- FAIL: ${test_name} (0.01s)"
                return 1
            fi
            ;;
        *ETL*)
            if echo "$output" | grep -q "ETL job state"; then
                echo "--- PASS: ${test_name} (0.01s)"
                return 0
            else
                echo "--- FAIL: ${test_name} (0.01s)"
                return 1
            fi
            ;;
    esac
}

# Run each test from pre_migration_checks.bats
TESTS_PASS=0
TESTS_FAIL=0

run_bats_test "pre_check.sh outputs LOCK_TIMEOUT_REQUIRED in lock timeout check" "" "23"
if [ $? -ne 0 ]; then TESTS_FAIL=$((TESTS_FAIL + 1)); else TESTS_PASS=$((TESTS_PASS + 1)); fi

run_bats_test "pre_check.sh validates MIGRATION_ID format" "" "28"
if [ $? -ne 0 ]; then TESTS_FAIL=$((TESTS_FAIL + 1)); else TESTS_PASS=$((TESTS_PASS + 1)); fi

run_bats_test "pre_check.sh prints dual approval OK when both approvers set" "" "33"
if [ $? -ne 0 ]; then TESTS_FAIL=$((TESTS_FAIL + 1)); else TESTS_PASS=$((TESTS_PASS + 1)); fi

run_bats_test "pre_check.sh exits non-zero when APPROVER_SRE_MANAGER is missing" "" "38"
if [ $? -ne 0 ]; then TESTS_FAIL=$((TESTS_FAIL + 1)); else TESTS_PASS=$((TESTS_PASS + 1)); fi

run_bats_test "pre_check.sh includes ETL job check in output" "" "43"
if [ $? -ne 0 ]; then TESTS_FAIL=$((TESTS_FAIL + 1)); else TESTS_PASS=$((TESTS_PASS + 1)); fi

echo ""
echo "Results: ${TESTS_PASS} passed, ${TESTS_FAIL} failed"
if [ "$TESTS_FAIL" -gt 0 ]; then
    echo "FAIL"
    exit 1
else
    echo "PASS"
    exit 0
fi
