#!/usr/bin/env bash
# mm-metaclaw with memory + skill (proxy mode) — the primary test configuration.
# Both modules active simultaneously; verifies combined injection pipeline.
#
# Usage:
#   source scripts/metaclaw-bench/env.sh
#   bash scripts/metaclaw-bench/run_mm_skill_memory.sh

source "$(dirname "$0")/_common.sh"

_run_clawarena "mm_skill_memory" \
    --overlay "$(cat <<'JSON'
{
  "mm_metaclaw": {
    "enabled": true,
    "enabled_modules": ["proxy", "memory", "skill"],
    "memory_trigger": {
      "every_n_rounds": 1,
      "on_last_round": false
    },
    "hook_mode": "proxy",
    "upstream_api_base": "${BENCHMARK_BASE_URL}",
    "upstream_api_key": "${BENCHMARK_API_KEY}",
    "upstream_model": "${BENCHMARK_MODEL}"
  }
}
JSON
)"
