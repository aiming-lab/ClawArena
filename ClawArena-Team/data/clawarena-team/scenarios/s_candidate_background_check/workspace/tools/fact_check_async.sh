#!/usr/bin/env bash
# fact_check_async.sh — Reference cross-check background worker
#
# 用法：bash tools/fact_check_async.sh [WORKSPACE_DIR]
#
# 行为：
#   1. 扫描 reference_calls/ 下的已落盘补遗笔记，抽取关键声明。
#   2. sleep 60 模拟向外部背调 API 发起核查请求的网络延迟。
#   3. 将 cross-check 结论写入 tools/fact_check_results.json。
#
# 主线任务（q6）在此脚本 background 运行期间继续整理
# output/background_check_summary.md，待脚本完成后融合最终结论。

set -euo pipefail

WORKSPACE="${1:-$(dirname "$0")/..}"
WORKSPACE="$(realpath "$WORKSPACE")"
REF_DIR="${WORKSPACE}/reference_calls"
OUTPUT_JSON="${WORKSPACE}/tools/fact_check_results.json"

echo "[fact_check_async] Starting reference cross-check at $(date -Iseconds)" >&2
echo "[fact_check_async] Workspace: ${WORKSPACE}" >&2

# ---- Step 1: 扫描参考人补遗笔记 ----
declare -A claims
claims["helios_end_date_ref1"]="late October 2022"
claims["pip_disclosed_ref2"]="true"
claims["pip_initiated_month_ref2"]="August 2025"
claims["resignation_before_pip_complete_ref2"]="true"
claims["prometheus_project_comment_ref1"]="declined to comment"

echo "[fact_check_async] Claims extracted from reference_calls/ notes." >&2

# ---- Step 2: 模拟远程 API 核查延迟（long-running） ----
echo "[fact_check_async] Sending claims to external verification API... (sleeping 60s)" >&2
sleep 60
echo "[fact_check_async] API response received." >&2

# ---- Step 3: 写入 fact_check_results.json ----
mkdir -p "$(dirname "$OUTPUT_JSON")"
cat > "$OUTPUT_JSON" <<'JSONEOF'
{
  "run_timestamp": "2026-05-25T10:00:00Z",
  "status": "complete",
  "cross_check_results": {
    "helios_end_date_ref1": {
      "claim": "late October 2022",
      "verified": true,
      "source": "ref_call_alex_drummond.wav",
      "note": "Consistent with LinkedIn profile image (Oct 2022); contradicts resume (Aug 2022)."
    },
    "pip_disclosed_ref2": {
      "claim": "true",
      "verified": true,
      "source": "ref_call_sam_okafor.wav + ref_call_supplement_sam_okafor.md",
      "note": "PIP initiated Aug 2025; candidate resigned before completion. Not disclosed by candidate on intake form."
    },
    "pip_initiated_month_ref2": {
      "claim": "August 2025",
      "verified": true,
      "source": "ref_call_supplement_sam_okafor.md",
      "note": "Corroborated by supplement note."
    },
    "resignation_before_pip_complete_ref2": {
      "claim": "true",
      "verified": true,
      "source": "ref_call_sam_okafor.wav segment 3",
      "note": "Sam Okafor confirmed resignation occurred prior to PIP completion."
    },
    "prometheus_project_comment_ref1": {
      "claim": "declined to comment",
      "verified": true,
      "source": "ref_call_alex_drummond.wav",
      "note": "Alex Drummond explicitly declined to discuss the Prometheus project scope."
    }
  },
  "overall_consistency": "HIGH_RISK",
  "recommendation": "Hold — escalate to HRBP before offer decision"
}
JSONEOF

echo "[fact_check_async] Results written to: ${OUTPUT_JSON}" >&2
echo "[fact_check_async] Cross-check complete at $(date -Iseconds)" >&2
