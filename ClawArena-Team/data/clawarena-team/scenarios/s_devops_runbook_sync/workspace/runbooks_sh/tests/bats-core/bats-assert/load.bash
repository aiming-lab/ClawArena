# bats-core/bats-assert/load.bash — minimal bats-assert stub

# assert_output: check that $output contains the expected string
assert_output() {
    local partial=false
    local expected=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --partial) partial=true; shift ;;
            *) expected="$1"; shift ;;
        esac
    done
    if $partial; then
        if [[ "$output" != *"$expected"* ]]; then
            echo "assert_output failed: expected partial match for '${expected}'" >&2
            echo "  actual output: ${output}" >&2
            return 1
        fi
    else
        if [[ "$output" != "$expected" ]]; then
            echo "assert_output failed: expected '${expected}'" >&2
            echo "  actual output: ${output}" >&2
            return 1
        fi
    fi
}
