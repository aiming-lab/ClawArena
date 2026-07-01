"""q4: findings/peak_frame.md 存在 + 含 frame 142 ± 3 + 含视频帧分析关键词。

通过条件（全部满足，exit 0）：
  1. findings/peak_frame.md 存在，长度 >= 80 字符
  2. 含帧号近 142（±3 容差）
  3. 含 'spi_heatmap_anim' 或 'heatmap' 或 'spi' 参照
  4. 含 'peak' 或 '峰值' 或 'drought' 或 '干旱' 等关键字
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, find_first_int_near, has_phrase_any, passed, workspace_root


def main() -> int:
    ws = workspace_root()
    peak_md = ws / "findings" / "peak_frame.md"
    if not peak_md.exists():
        fail("missing findings/peak_frame.md")

    text = peak_md.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 80:
        fail(f"peak_frame.md too short: {len(text.strip())} chars < 80")

    # 帧号检验（±3 容差）
    frame_found = find_first_int_near(text, 142, tolerance=3)
    if frame_found is None:
        fail("peak frame number near 142 (±3) not found in findings/peak_frame.md")

    # 视频引用
    if not has_phrase_any(text, ["spi_heatmap_anim", "heatmap", "spi", "mp4", "video"]):
        fail("missing reference to spi heatmap animation or video in peak_frame.md")

    # 关键语义
    if not has_phrase_any(text, ["peak", "峰值", "drought", "干旱", "maximum", "最大", "worst", "severe"]):
        fail("missing drought/peak keyword in peak_frame.md")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
