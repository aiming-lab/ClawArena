"""check_q3.py — analysis/area_change.md 含 ROI 坐标 + area delta +18.4 ha。

通过条件（全部满足，exit 0）：
  1. analysis/area_change.md 存在且 >= 150 字符。
  2. ROI box 坐标（140, 200, 380, 420）在文件中可识别（至少出现 3 个数字）。
  3. 面积增量 +18.4 hectares（允许 18.4，±0.1 容差，且有 hect / ha 单位词）。
  4. 引用了 area-7。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

# ROI 四个坐标数字
_ROI_COORDS = [140, 200, 380, 420]
# 面积增量匹配：必须为 18.3–18.5（即 18.4 ±0.1）。
#   收紧动机：旧式 r"1[89](?:\.\d)?\s*(?:hect|ha)" 会把 '18 ha'、'19 ha'、
#   '19.9 ha' 等错误数值一并放过（任何 18/19 开头都命中）。这里改为：
#     (a) _DELTA_NUM_RE 精确枚举 18.3/18.4/18.5，并用前后非数字断言
#         (?<![\d.]) / (?![\d.]) 防止吞入 118.4、18.45、2018.4 等子串误匹配；
#     (b) _UNIT_RE 单独校验文件中存在 hectare/ha 单位词（带词边界，
#         避免命中 'shard'、'chart' 等含 'ha' 的子串）。
#   通过条件改为「目标数值 AND 单位词」同时存在，移除旧 or 漏洞。
_DELTA_NUM_RE = re.compile(r"(?<![\d.])18\.[3-5](?![\d.])")
_UNIT_RE = re.compile(r"\b(?:hect(?:are)?s?|ha)\b", re.IGNORECASE)


def main() -> int:
    ws = workspace_root()
    target = ws / "analysis" / "area_change.md"

    # 1. 存在 + 最小长度
    if not target.exists():
        fail("missing analysis/area_change.md")
    content = target.read_text(encoding="utf-8", errors="ignore")
    if len(content.strip()) < 150:
        fail("analysis/area_change.md too short (< 150 chars)")

    # 2. ROI 坐标：至少 3 个坐标数字出现在文件中
    coord_hits = sum(
        1 for coord in _ROI_COORDS
        if re.search(rf"\b{coord}\b", content)
    )
    if coord_hits < 3:
        fail(
            f"area_change.md references only {coord_hits}/4 ROI coordinates "
            f"{_ROI_COORDS}; need >= 3"
        )

    # 3. 面积增量 18.4 ha（±0.1）：需同时出现目标数值（18.3–18.5）与单位词。
    has_delta_num = _DELTA_NUM_RE.search(content)
    has_unit = _UNIT_RE.search(content)
    if not (has_delta_num and has_unit):
        fail(
            "area_change.md does not contain area delta +18.4 ha "
            "(need value 18.3-18.5 AND a 'hectares'/'ha' unit word)"
        )

    # 4. area-7 引用
    if not re.search(r"area[-_\s]?7", content, re.IGNORECASE):
        fail("area_change.md does not reference area-7")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
