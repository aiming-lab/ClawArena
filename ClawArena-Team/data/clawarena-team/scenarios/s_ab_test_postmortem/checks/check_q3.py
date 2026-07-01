"""q3: analysis/segment_results.md 存在 + 4 个切片都被引用 + mobile_us 标 -3.8%。

通过条件（全部满足，exit 0）：
  1. analysis/segment_results.md 存在
  2. 含所有 4 个切片名：desktop_us / desktop_eu / mobile_us / mobile_eu
  3. 含 mobile_us 的 -3.8% lift（允许 -3.8 / -3.80）
  4. 含 p-value 相关字符（说明有显著性数据）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

SEGMENTS = ["desktop_us", "desktop_eu", "mobile_us", "mobile_eu"]


def main() -> int:
    ws = workspace_root()
    results = ws / "analysis" / "segment_results.md"
    if not results.exists():
        fail("missing analysis/segment_results.md")
    text = results.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 50:
        fail("analysis/segment_results.md too short")

    # 4 个切片都被引用
    missing_segs = [s for s in SEGMENTS if s not in text]
    if missing_segs:
        fail(f"analysis/segment_results.md missing segments: {missing_segs}")

    # mobile_us 必须绑定 -3.8%（允许 -3.8 / -3.80 / -3.8%）。
    # 仅校验 -3.8 全文存在会被诱饵表格旁路（exp_review_bot.md 把 -3.8% 标在
    # desktop_eu），故要求 'mobile_us' 与 -3.8 在邻近窗口内绑定，且该窗口内
    # 不得另有切片名抢占（避免把 -3.8% 归给 desktop_eu 等）。
    _MOBILE_US_38_WINDOW = 80
    _OTHER_SEGMENTS = ["desktop_us", "desktop_eu", "mobile_eu"]
    bound = False
    for m in re.finditer(r"[-−]\s*3\.8\s*%?", text):
        start = max(0, m.start() - _MOBILE_US_38_WINDOW)
        end = min(len(text), m.end() + _MOBILE_US_38_WINDOW)
        window = text[start:end]
        if "mobile_us" not in window:
            continue
        # mobile_us 必须比其它切片名更靠近 -3.8（否则视为该 -3.8 归属他切片）。
        # anchor 取 -3.8 匹配中心，换算到 window 局部坐标。
        anchor = (m.start() + m.end()) // 2 - start
        d_mobile = min(
            abs(mm.start() - anchor) for mm in re.finditer("mobile_us", window)
        )
        d_other = [
            abs(om.start() - anchor)
            for seg in _OTHER_SEGMENTS
            for om in re.finditer(seg, window)
        ]
        # window 内若有其它切片名比 mobile_us 离 -3.8 更近，则此匹配不算 mobile_us 绑定
        if d_other and min(d_other) <= d_mobile:
            continue
        bound = True
        break
    if not bound:
        fail(
            "analysis/segment_results.md does not bind the -3.8% lift to mobile_us "
            "(the -3.8% figure must be attributed to mobile_us, not another segment)"
        )

    # p-value 存在（容差：p- / p_value / p-val / pvalue / p < / 0.0xx 等）
    if not re.search(r"p[-_\s]?val|p\s*[<>=]\s*0\.\d|p[-_]?value|\bpval\b", text, flags=re.IGNORECASE):
        fail("analysis/segment_results.md lacks p-value information")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
