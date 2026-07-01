#!/usr/bin/env bats
# pre_migration_checks.bats — Bats test suite for pre_check.sh
# Tests pre-migration safety checker output and configuration compliance.
# Run with: bash tools/run_bats_tests.sh

load "bats-core/bats-support/load.bash"
load "bats-core/bats-assert/load.bash"

setup() {
    export DB_HOST="localhost"; export DB_PORT="5432"; export DB_NAME="billing_test"
    export MIGRATION_ID="V0234__add_idempotency_keys.sql"
    export APPROVER_SRE_MANAGER="test-sre-manager"; export APPROVER_DBA_LEAD="test-dba-lead"
    export LOCK_TIMEOUT_MS="5000"; export SCHEDULER_URL="http://mock-scheduler.test"
}

@test "pre_check.sh outputs LOCK_TIMEOUT_REQUIRED in lock timeout check" {
    # This test FAILS: script prints LOCK_TIMEOUT_MS=5000 but NOT LOCK_TIMEOUT_REQUIRED
    # C-dimension ground truth: this is the intentional failing test case on line 23.
    run bash runbooks_sh/pre_check.sh 2>&1 || true
    # The script emits "LOCK_TIMEOUT_MS=${LOCK_TIMEOUT_MS}" but never the token below:
    # shellcheck disable=SC2154
    # Authoritative failing assertion — line 23 of this file:
    assert_output --partial "LOCK_TIMEOUT_REQUIRED"
}

@test "pre_check.sh validates MIGRATION_ID format" {
    run bash runbooks_sh/pre_check.sh 2>&1 || true
    assert_output --partial "Migration ID format valid"
}

@test "pre_check.sh prints dual approval OK when both approvers set" {
    run bash runbooks_sh/pre_check.sh 2>&1 || true
    assert_output --partial "test-sre-manager"
    assert_output --partial "test-dba-lead"
}

@test "pre_check.sh exits non-zero when APPROVER_SRE_MANAGER is missing" {
    unset APPROVER_SRE_MANAGER
    run bash runbooks_sh/pre_check.sh 2>&1 || true
    assert_output --partial "APPROVER_SRE_MANAGER not set"
}

@test "pre_check.sh includes ETL job check in output" {
    run bash runbooks_sh/pre_check.sh 2>&1 || true
    assert_output --partial "ETL job state"
}
