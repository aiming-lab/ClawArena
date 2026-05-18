#!/usr/bin/env bash
# mm-metaclaw with memory + skill + multimodal_image (proxy mode).
# Full feature set for testing multimodal augmentation alongside
# memory and skill modules.
#
# Usage:
#   source scripts/metaclaw-bench/env.sh
#   bash scripts/metaclaw-bench/run_mm_multimodal.sh

source "$(dirname "$0")/_common.sh"

_run_clawarena "mm_multimodal" \
    --overlay "$(cat <<'JSON'
{
  "mm_metaclaw": {
    "enabled": true,
    "enabled_modules": ["proxy", "memory", "skill", "multimodal_image"],
    "hook_mode": "proxy",
    "upstream_api_base": "${BENCHMARK_BASE_URL}",
    "upstream_api_key": "${BENCHMARK_API_KEY}",
    "upstream_model": "${BENCHMARK_MODEL}"
  }
}
JSON
)"
