#!/usr/bin/env bash
# Common helpers for MetaClawBench-Small experiment scripts (12-day subset).
# Source via: source "$(dirname "$0")/_common.sh"

set -euo pipefail

_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAWA_ROOT="$(cd "$_SCRIPT_DIR/../.." && pwd)"
DATA_PATH="$CLAWA_ROOT/data/metaclaw-bench-small/tests.json"

# Source env if not already set
if [[ -z "${BENCHMARK_API_KEY:-}" ]]; then
    echo "[warn] BENCHMARK_API_KEY not set — sourcing env.sh"
    # shellcheck source=env.sh
    source "$_SCRIPT_DIR/env.sh"
fi

# Verify required vars
: "${BENCHMARK_BASE_URL:?BENCHMARK_BASE_URL must be set}"
: "${BENCHMARK_API_KEY:?BENCHMARK_API_KEY must be set}"
: "${BENCHMARK_MODEL:?BENCHMARK_MODEL must be set}"
: "${GATEWAY_MODULES_DIR:?GATEWAY_MODULES_DIR must be set}"

RUN_TAG="${RUN_TAG:-$(date +%Y%m%d_%H%M%S)}"
# Results written to gateway-modules/results/ for experiment tracking
OUT_BASE="${OUT_BASE:-$GATEWAY_MODULES_DIR/results/metaclaw-bench-small}"

# Model-specific extra config (caller can override via env var).
# These are passed to --model-config and injected into the openclaw model entry.
# Adjust for non-reasoning models or Anthropic models by setting MODEL_CONFIG="{}".
MODEL_CONFIG="${MODEL_CONFIG:-{\"reasoning\": true, \"contextWindow\": 200000}}"

_run_clawarena() {
    local label="$1"
    local out_dir="$OUT_BASE/${label}_${RUN_TAG}"
    shift
    echo ""
    echo "================================================================"
    echo " MetaClawBench-Small | $label"
    echo " output: $out_dir"
    echo "================================================================"
    clawarena run \
        --data "$DATA_PATH" \
        --frameworks openclaw \
        --out "$out_dir" \
        --concurrency 1 \
        --timeout 600 \
        --retry 2 \
        --model-config "$MODEL_CONFIG" \
        "$@"
    echo ""
    echo "Done: $out_dir"
}
