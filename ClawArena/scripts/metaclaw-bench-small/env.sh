#!/usr/bin/env bash
# MetaClawBench-Small environment variables — delegates to the full-benchmark env.sh.
#
#   source scripts/metaclaw-bench-small/env.sh

_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$_SCRIPT_DIR/../metaclaw-bench/env.sh"
