#!/usr/bin/env bash
# mm-metaclaw HTTP mode — explicitly calls inject/collect endpoints every round.
# Use this to test individual module endpoints in isolation and verify
# request/response formats rather than relying on transparent proxy behavior.
#
# Suitable for: endpoint conformance testing, debugging module behavior.
# Not suitable for: performance or accuracy comparison with baseline.
#
# Usage:
#   source scripts/metaclaw-bench/env.sh
#   bash scripts/metaclaw-bench/run_mm_http_test.sh

source "$(dirname "$0")/_common.sh"

_run_clawarena "mm_http_test" \
    --overlay "$(cat <<'JSON'
{
  "mm_metaclaw": {
    "enabled": true,
    "enabled_modules": ["proxy", "memory", "skill"],
    "hook_mode": "http",
    "upstream_api_base": "${BENCHMARK_BASE_URL}",
    "upstream_api_key": "${BENCHMARK_API_KEY}",
    "upstream_model": "${BENCHMARK_MODEL}"
  }
}
JSON
)"
