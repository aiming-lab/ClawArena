#!/usr/bin/env bash
# tax_agg.sh — Cross-quarter tax aggregate computation for Liu Wei TY 2026.
#
# Usage:
#     bash tools/tax_agg.sh [output_dir]
#
# This script aggregates cross-quarter income components:
#   Q1-Q4 salary, dividends, capital gains, German rental income.
# It performs a deliberate sleep to simulate large-dataset aggregation.
#
# Output: ${output_dir}/tax_aggregate_2026.json (JSON summary)
# Exit: 0 on success, 1 on error.

set -euo pipefail

OUTPUT_DIR="${1:-output}"
mkdir -p "${OUTPUT_DIR}"

echo "[tax_agg] Starting cross-quarter tax aggregate for TY 2026 ..."
echo "[tax_agg] Phase 1/4: Loading Q1 income data ..."
sleep 15
echo "[tax_agg] Phase 2/4: Loading Q2-Q3 income data ..."
sleep 15
echo "[tax_agg] Phase 3/4: Loading Q4 income data + German rental ..."
sleep 15
echo "[tax_agg] Phase 4/4: Aggregating and reconciling cross-quarter totals ..."
sleep 15

# Aggregate constants (fixed for reproducibility)
SALARY_USD=195000
DIVIDENDS_USD=5120
CAP_GAINS_USD=14300
INTEREST_USD=2100
RENTAL_EUR=18420
FX_RATE=1.0913
RENTAL_USD=$(echo "scale=2; ${RENTAL_EUR} * ${FX_RATE}" | bc)
TOTAL_INCOME=$(echo "scale=2; ${SALARY_USD} + ${DIVIDENDS_USD} + ${CAP_GAINS_USD} + ${INTEREST_USD} + ${RENTAL_USD}" | bc)

cat > "${OUTPUT_DIR}/tax_aggregate_2026.json" << JSONEOF
{
  "generated_by": "tools/tax_agg.sh",
  "tax_year": 2026,
  "client": "Liu Wei",
  "engagement": "MT-ENG-2026-0042",
  "status": "COMPLETE",
  "quarters": {
    "Q1": {"salary_usd": 48750.00, "dividends_usd": 0.00, "cap_gains_usd": 3575.00},
    "Q2": {"salary_usd": 48750.00, "dividends_usd": 1280.00, "cap_gains_usd": 3575.00},
    "Q3": {"salary_usd": 48750.00, "dividends_usd": 1280.00, "cap_gains_usd": 3575.00},
    "Q4": {"salary_usd": 48750.00, "dividends_usd": 2560.00, "cap_gains_usd": 3575.00}
  },
  "annual_totals": {
    "salary_usd": ${SALARY_USD},
    "dividends_usd": ${DIVIDENDS_USD},
    "cap_gains_usd": ${CAP_GAINS_USD},
    "interest_usd": ${INTEREST_USD},
    "german_rental_eur": ${RENTAL_EUR},
    "fx_rate_eur_usd": ${FX_RATE},
    "german_rental_usd": ${RENTAL_USD},
    "total_gross_income_usd": ${TOTAL_INCOME}
  },
  "pfic": {
    "holding": "DE Immobilien AG (DEIMM)",
    "shares": 250,
    "pfic_applies": true,
    "threshold_pct": 50,
    "passive_income_pct": 53.52
  }
}
JSONEOF

echo "[tax_agg] Aggregate complete. Output: ${OUTPUT_DIR}/tax_aggregate_2026.json"
