#!/usr/bin/env bash
# mm-metaclaw with skill module only (proxy mode).
# The gateway injects relevant skill context before each LLM call and
# evolves skills based on interaction outcomes.
#
# Usage:
#   source scripts/metaclaw-bench/env.sh
#   bash scripts/metaclaw-bench/run_mm_skill.sh

source "$(dirname "$0")/_common.sh"

_run_clawarena "mm_skill" \
    --overlay "$(cat <<'JSON'
{
  "mm_metaclaw": {
    "enabled": true,
    "enabled_modules": ["proxy", "skill"],
    "hook_mode": "proxy",
    "upstream_api_base": "${BENCHMARK_BASE_URL}",
    "upstream_api_key": "${BENCHMARK_API_KEY}",
    "upstream_model": "${BENCHMARK_MODEL}"
  }
}
JSON
)"
