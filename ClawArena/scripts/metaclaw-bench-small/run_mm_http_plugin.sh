#!/usr/bin/env bash
# mm-metaclaw HTTP+plugin mode — OpenClaw keeps its own provider config and
# reaches MM-MetaClaw only through the OpenClaw plugin HTTP hooks.

source "$(dirname "$0")/_common.sh"

_run_clawarena "mm_http_plugin" \
    --overlay "$(cat <<'JSON'
{
  "mm_metaclaw": {
    "enabled": true,
    "transport_mode": "http_plugin",
    "enabled_modules": ["memory", "skill"],
    "memory_trigger": {
      "every_n_rounds": 1,
      "on_last_round": false
    },
    "upstream_api_base": "${BENCHMARK_BASE_URL}",
    "upstream_api_key": "${BENCHMARK_API_KEY}",
    "upstream_model": "${BENCHMARK_MODEL}"
  }
}
JSON
)"
