# bats-core/bats-support/load.bash — minimal bats-support stub
# Real bats-support provides: assert_*, refute_*, etc.
# This stub defines the minimum needed for the test runner.

bats_support_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Re-export load helper
load() {
    local name="$1"
    # Resolve relative to test file location
    local base_dir
    base_dir="$(cd "$(dirname "${BASH_SOURCE[1]}")" && pwd)"
    source "${base_dir}/${name}" 2>/dev/null ||     source "${bats_support_root}/${name}" 2>/dev/null || true
}
