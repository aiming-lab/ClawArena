#!/bin/bash
# cache_key_gen.sh - Generate cache keys for GitLab CI jobs
# Usage: ./cache_key_gen.sh <file1> [file2]

set -euo pipefail

if [ $# -eq 0 ]; then
    echo "Usage: $0 <file1> [file2]" >&2
    exit 1
fi

# GitLab CI cache:key:files supports maximum 2 file paths
if [ $# -gt 2 ]; then
    echo "Warning: cache:key:files supports maximum 2 files. Using first 2 only." >&2
fi

KEY=""
for f in "${@:1:2}"; do
    if [ -f "$f" ]; then
        HASH=$(sha256sum "$f" | cut -d' ' -f1 | head -c 16)
        KEY="${KEY}${HASH}-"
    fi
done

echo "${KEY%%-}"  # Remove trailing dash
