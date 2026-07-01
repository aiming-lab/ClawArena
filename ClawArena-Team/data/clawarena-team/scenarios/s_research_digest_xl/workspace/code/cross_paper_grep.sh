#!/usr/bin/env bash
# cross_paper_grep.sh — Cross-paper keyword search (background task simulation)
#
# Usage: bash cross_paper_grep.sh <keyword> <papers_dir>
#
# This script searches for a given keyword across all paper chapter files under
# <papers_dir>, tallies per-paper occurrence counts, and writes a summary to
# output/cross_paper_grep_result.txt.
#
# The simulated grep scan includes a deliberate 60-second sleep to model the
# latency of a real distributed grep job over large corpora.  The main agent
# should launch this script as a background subagent and continue with other
# work while this runs.

set -euo pipefail

KEYWORD="${1:-reproducibility}"
PAPERS_DIR="${2:-papers}"
RESULT_FILE="output/cross_paper_grep_result.txt"

echo "[cross_paper_grep] Starting background scan for keyword: '$KEYWORD'"
echo "[cross_paper_grep] Scanning directory: $PAPERS_DIR"
echo "[cross_paper_grep] Simulating distributed grep latency (60s)..."

# Simulate long-running distributed grep across large corpora
sleep 60

echo "[cross_paper_grep] Scan complete. Tallying results..."

mkdir -p output

{
    echo "# Cross-Paper Keyword Grep Results"
    echo "# Keyword: $KEYWORD"
    echo "# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo ""
    total=0
    for paper_dir in "$PAPERS_DIR"/paper_*/; do
        paper_id=$(basename "$paper_dir")
        count=$(grep -ri --include="*.md" "$KEYWORD" "$paper_dir" 2>/dev/null | wc -l || echo 0)
        echo "- $paper_id: $count occurrences"
        total=$((total + count))
    done
    echo ""
    echo "Total occurrences across all papers: $total"
    if [ "$total" -ge 3 ]; then
        echo "STATUS: THRESHOLD_MET (>= 3 papers contain the keyword)"
    else
        echo "STATUS: THRESHOLD_NOT_MET (< 3 papers contain the keyword)"
    fi
} > "$RESULT_FILE"

echo "[cross_paper_grep] Results written to $RESULT_FILE"
