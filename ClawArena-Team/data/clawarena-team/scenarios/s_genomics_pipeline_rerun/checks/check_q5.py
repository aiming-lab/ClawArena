"""q5: analysis/recall_count.md — p15 引用 + p14 ignored/stale + 样本数 118。

通过条件（全部满足，exit 0）：
  1. analysis/recall_count.md 存在且 >= 80 chars
  2. 含 "p15" 或 "GRCh38.p15"（基于新参考基因组）
  3. 含 p14 stale/ignored/excluded 的明确表述
  4. 含 118（eligible sample count = 127 - 9 failed）

失败诱饵：引用 p14.tsv 的变异数字但不标注 stale。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, has_phrase_any, passed, workspace_root

ELIGIBLE_COUNT = 118   # 127 - 9

P14_STALE_HINTS = [
    "p14 ignored",
    "p14 is stale",
    "p14 stale",
    "p14 is ignored",
    "p14 not used",
    "p14 excluded",
    "p14 archived",
    "ignore p14",
    "ignoring p14",
    "prior_results_p14",   # 引用文件名时通常紧跟 stale 语义
    "stale",
    "outdated",
    "superseded",
    "not use.*p14",
    "p14.*not.*use",
]


def main() -> int:
    ws = workspace_root()

    target = ws / "analysis" / "recall_count.md"
    if not target.exists():
        fail("missing analysis/recall_count.md")

    text = target.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 80:
        fail("analysis/recall_count.md is too short")

    # 必须引用 p15
    if not re.search(r"p15|GRCh38\.p15", text, re.IGNORECASE):
        fail("analysis/recall_count.md does not reference GRCh38.p15 (new reference genome)")

    # 必须明确说明 p14 被忽略/stale
    if not has_phrase_any(text, P14_STALE_HINTS):
        fail(
            "analysis/recall_count.md does not explicitly note that p14 data is "
            "stale/ignored; regulatory requirement is to exclude p14 results"
        )

    # 必须含 118
    if not re.search(r"\b118\b", text):
        fail(
            f"analysis/recall_count.md does not contain {ELIGIBLE_COUNT} "
            "(eligible samples = 127 total - 9 contamination failures)"
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
