#!/usr/bin/env bash
# lint_release.sh — Run repository lint checks for pre-release audit.
# Usage: bash tools/lint_release.sh [repo_src_path]
# Scans for common issues: bare except, print statements, TODO comments.

REPO_SRC=${1:-repo/src}

echo "=== lint_release.sh started at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "Scanning: $REPO_SRC"

echo ""
echo "--- bare except clauses ---"
grep -rn "except:" "$REPO_SRC" 2>/dev/null | head -20 || echo "(none found)"

echo ""
echo "--- print() statements ---"
grep -rn "^[[:space:]]*print(" "$REPO_SRC" 2>/dev/null | head -20 || echo "(none found)"

echo ""
echo "--- TODO / FIXME comments ---"
grep -rn "TODO\|FIXME" "$REPO_SRC" 2>/dev/null | head -20 || echo "(none found)"

echo ""
echo "=== lint_release.sh completed at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
