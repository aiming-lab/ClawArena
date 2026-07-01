#!/usr/bin/env bash
# run_varcall.sh — varcall-2026q2 pipeline launcher
# Usage: bash run_varcall.sh [--samples-db data/samples.sqlite] [--ref GRCh38.p15.fa.gz]
#
# Behaviour: iterate over all PENDING samples in the sqlite DB, run align + call + filter.
# Long-running: typical full cohort takes 6–12 hours depending on coverage.

set -euo pipefail

DB="${SAMPLES_DB:-data/samples.sqlite}"
REF="${REF_GENOME:-GRCh38.p15.fa.gz}"
OUTDIR="${OUTDIR:-results/varcall-2026q2}"
THREADS="${THREADS:-8}"
LOG="${LOG:-reports/run_log.txt}"

echo "# Pipeline run log — varcall-2026q2" > "$LOG"
echo "# Started: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
echo "# Ref genome: $REF" >> "$LOG"

# Query pending samples from sqlite
SAMPLES=$(sqlite3 "$DB" "SELECT sample_id FROM samples WHERE status='pending_rerun' ORDER BY sample_id;")

TOTAL=$(echo "$SAMPLES" | wc -l | tr -d ' ')
echo "# Total samples: $TOTAL" >> "$LOG"

COUNT=0
for SID in $SAMPLES; do
    COUNT=$((COUNT + 1))
    echo "[$SID] align:RUNNING call:PENDING filter:PENDING" >> "$LOG"

    # Stage 1: BWA-MEM2 alignment
    python pipeline/stages/align.py --sample "$SID" --ref "$REF" --threads "$THREADS" >> "$LOG" 2>&1

    # Stage 2: GATK HaplotypeCaller variant calling
    python pipeline/stages/call.py --sample "$SID" --threads "$THREADS" >> "$LOG" 2>&1

    # Stage 3: VQSR filter
    python pipeline/stages/filter.py --sample "$SID" >> "$LOG" 2>&1

    echo "[$SID] align:DONE call:DONE filter:DONE" >> "$LOG"

    # Update status in sqlite
    sqlite3 "$DB" "UPDATE samples SET status='complete', ref_genome='$REF' WHERE sample_id='$SID';"
done

echo "Pipeline complete: $COUNT samples processed." >> "$LOG"
