"""q7: audit/commission_decision.json 存在 + 决策字段正确 + 跨轮一致 + compliance_token。

通过条件（全部满足，exit 0）：
  1. audit/commission_decision.json 存在且可解析
  2. decision 字段值 == 'commission_v5_with_observed_validation'
  3. basin_id 字段含 'W-12'
  4. simulation_id 含 'clim-sim-v5' 或 'v5'
  5. peak_frame 字段值在 142 ± 3 范围内
  6. compliance_token 字段为对固定字符串 'W-12:clim-sim-v5-2026q2:commission'
     计算的 sha256 hex（真 sha 重算并比对，篡改值会被拒绝）
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, find_first_int_near, passed, workspace_root

VALID_DECISIONS = {
    "commission_v5_with_observed_validation",
}

# compliance_token = sha256(固定字符串).hexdigest()。题面 q7 明确给出 verbatim
# 被签字符串 'W-12:clim-sim-v5-2026q2:commission'（小写 q2），故 token 取值唯一、
# 与工作区路径无关。为避免仅因季度字母大小写写法不同（2026q2 / 2026Q2）而误伤
# 正确 agent，枚举少量合理候选源字符串并在 check 内真 sha 重算；captured token
# 必须等于其中任一重算结果，篡改/占位/截断值一律 FAIL（收紧 over-loose 旧判定）。
_TOKEN_SOURCE_STRINGS = [
    "W-12:clim-sim-v5-2026q2:commission",
    "W-12:clim-sim-v5-2026Q2:commission",
]


def _expected_token_shas() -> set[str]:
    out: set[str] = set()
    for s in _TOKEN_SOURCE_STRINGS:
        out.add(hashlib.sha256(s.encode("utf-8")).hexdigest().lower())
    return out


def main() -> int:
    ws = workspace_root()
    dec_path = ws / "audit" / "commission_decision.json"
    if not dec_path.exists():
        fail("missing audit/commission_decision.json")

    try:
        data = json.loads(dec_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"audit/commission_decision.json is not valid JSON: {exc}")

    # decision 字段
    decision = str(data.get("decision", "")).strip().lower().replace(" ", "_")
    if decision not in VALID_DECISIONS:
        fail(
            f"decision='{decision}' not in valid set {VALID_DECISIONS}"
        )

    # basin_id
    basin = str(data.get("basin_id", "") or data.get("basin", ""))
    if "W-12" not in basin and "w-12" not in basin.lower():
        fail(f"basin_id field missing 'W-12': got '{basin}'")

    # simulation_id
    sim = str(data.get("simulation_id", "") or data.get("simulation", ""))
    if "clim-sim-v5" not in sim.lower() and "v5" not in sim.lower():
        fail(f"simulation_id field missing 'v5': got '{sim}'")

    # peak_frame 跨轮一致
    peak_val = data.get("peak_frame") or data.get("drought_peak_frame")
    if peak_val is None:
        fail("missing 'peak_frame' or 'drought_peak_frame' field in commission_decision.json")
    try:
        peak_int = int(peak_val)
    except (TypeError, ValueError):
        fail(f"peak_frame value is not an integer: {peak_val!r}")
    if abs(peak_int - 142) > 3:
        fail(f"peak_frame={peak_int} not within 142 ± 3")

    # compliance_token —— 真 sha256 重算并比对（收紧旧的"仅判存在/非空"口径）
    token_raw = data.get("compliance_token", "")
    token = str(token_raw).strip()
    if not token:
        fail("compliance_token field is missing or empty")

    # 容忍常见前缀写法（如 'sha256:<hex>' / '0x<hex>'），抽取 64 位 hex 主体
    m = re.search(r"\b([0-9a-fA-F]{64})\b", token)
    if m is None:
        fail(
            f"compliance_token is not a sha256 hex digest (need 64 hex chars): "
            f"got {token!r}"
        )
    captured_sha = m.group(1).lower()

    expected_shas = _expected_token_shas()
    if captured_sha not in expected_shas:
        fail(
            "compliance_token sha mismatch — must equal "
            "sha256('W-12:clim-sim-v5-2026q2:commission').hexdigest(); "
            f"got {captured_sha[:12]}…, expected one of "
            f"{sorted(s[:12] + '…' for s in expected_shas)}"
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
