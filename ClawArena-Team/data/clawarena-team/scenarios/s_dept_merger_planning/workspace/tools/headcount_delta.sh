#!/usr/bin/env bash
# headcount_delta.sh — Cross-departmental headcount delta ETL simulator.
#
# Usage: bash tools/headcount_delta.sh <workspace_dir>
#
# This script simulates a long-running ETL job that scans the full HR exports
# from both hospitals, computes the per-department headcount delta (pre- vs
# post-merger), and renders a bar chart to figures/org_headcount_delta.png.
#
# The ~60-second sleep models real-world I/O wait (large parquet scan).
# The main agent should launch this via RunSubagent with run_in_background=true
# and continue assembling output/merger_status.md in parallel.

set -euo pipefail

WORKSPACE="${1:-$(pwd)}"
FIGURES_DIR="${WORKSPACE}/figures"
CHART_OUT="${FIGURES_DIR}/org_headcount_delta.png"

echo "[headcount_delta] Starting ETL scan of HR exports..."
echo "[headcount_delta] Workspace: ${WORKSPACE}"

# Simulate ETL processing delay (scanning merged HR CSVs, computing deltas).
sleep 60

echo "[headcount_delta] ETL complete. Rendering headcount delta chart..."

mkdir -p "${FIGURES_DIR}"

python3 - <<'PYEOF'
import sys, os
workspace = os.environ.get("WORKSPACE", sys.argv[1] if len(sys.argv) > 1 else ".")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

departments = [
    "Cardiology-Tier1",
    "Cath Lab",
    "Electrophysiology",
    "Cardiac ICU",
    "Radiology-Cardiac",
    "Admin/Support",
]
hosp_a = [28, 9, 6, 4, 6, 12]
hosp_b = [26, 8, 7, 5, 5, 11]
unified = [47, 15, 11, 7, 9, 20]

x = np.arange(len(departments))
width = 0.28
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width, hosp_a, width, label="Hospital A (pre-merger)", color="#4E79A7")
ax.bar(x,         hosp_b, width, label="Hospital B (pre-merger)", color="#F28E2B")
ax.bar(x + width, unified, width, label="Unified plan (post-merger)", color="#59A14F")
ax.set_xticks(x)
ax.set_xticklabels(departments, rotation=28, ha="right", fontsize=9)
ax.set_xlabel("Department")
ax.set_ylabel("Headcount")
ax.set_title("Org Headcount Delta — Pre- vs Post-Merger by Department")
ax.legend(loc="upper right", fontsize=9)
ax.grid(True, alpha=0.3)
fig.tight_layout()

out = os.path.join(workspace, "figures", "org_headcount_delta.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, dpi=140, bbox_inches="tight")
plt.close(fig)
print(f"[headcount_delta] Chart saved to: {out}")
PYEOF

echo "[headcount_delta] Done. Chart written to: ${CHART_OUT}"
