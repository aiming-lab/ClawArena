#!/usr/bin/env bash
# Sequentially run the wave subsets of the merged clawarena-team dataset
# (demo / wave1 / wave3 / wave4; wave2 was superseded by wave3), each selected via
# --tests tests-<wave>.json. Output lands in results/<set>_full/run_*/ with separate logs.
# An overview goes to logs/run_all_datasets.log; each subset also gets logs/<set>_full.log.
set -euo pipefail

cd "$(dirname "$0")/.."

CONFIG="${CATEAM_CONFIG:-configs/local_debug.yaml}"
DATA="${CATEAM_DATA:-data/clawarena-team}"
SETS=(demo wave1 wave3 wave4)   # add "all" to also run the full tests.json

mkdir -p logs results

START_ALL=$(date +%s)
echo "=== run_all_datasets START $(date -Iseconds) ===" | tee -a logs/run_all_datasets.log

for s in "${SETS[@]}"; do
  if [ "$s" = "all" ]; then tests_arg=(); else tests_arg=(--tests "tests-${s}.json"); fi
  out_dir="results/${s}_full"
  per_log="logs/${s}_full.log"
  mkdir -p "$out_dir"

  echo "[$(date -Iseconds)] START ${s} -> ${out_dir}" | tee -a logs/run_all_datasets.log
  if clawarena-team run -d "$DATA" "${tests_arg[@]}" -o "$out_dir" --config "$CONFIG" >>"$per_log" 2>&1; then
    echo "[$(date -Iseconds)] OK    ${s}" | tee -a logs/run_all_datasets.log
  else
    echo "[$(date -Iseconds)] FAIL  ${s} (exit=$?)" | tee -a logs/run_all_datasets.log
    # keep going to the next subset; decide whether to resume afterwards
  fi
done

END_ALL=$(date +%s)
echo "=== run_all_datasets DONE $(date -Iseconds) (elapsed $((END_ALL - START_ALL))s) ===" | tee -a logs/run_all_datasets.log
