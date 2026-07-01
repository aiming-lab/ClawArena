"""q6: analysis/validation_score.md 存在 + 含偏差数值（bias/rmse/mae）+ 含脚本执行引用。

通过条件（全部满足，exit 0）：
  1. analysis/validation_score.md 存在，长度 >= 100 字符
  2. 含至少 1 个浮点数（偏差数值）
  3. 含 'bias' 或 'rmse' 或 'mae' 或 'error' 或 '偏差' 等统计字眼
  4. 含 'validate_against_obs' 或 'observed' 或 'obs' 或 'script' 关键字（脚本引用）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, has_phrase_any, passed, workspace_root


def main() -> int:
    ws = workspace_root()
    val_md = ws / "analysis" / "validation_score.md"
    if not val_md.exists():
        fail("missing analysis/validation_score.md")

    text = val_md.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 100:
        fail(f"validation_score.md too short: {len(text.strip())} chars < 100")

    # 含浮点数（偏差数值）
    floats = re.findall(r"-?\d+\.\d+", text)
    if not floats:
        fail("no numeric bias/deviation value found in validation_score.md")

    # 统计字眼
    if not has_phrase_any(text, ["bias", "rmse", "mae", "error", "偏差", "均方", "绝对误差", "deviation", "accuracy"]):
        fail("missing statistical metric keyword (bias/rmse/mae/error/偏差) in validation_score.md")

    # 脚本引用
    if not has_phrase_any(text, ["validate_against_obs", "validate_against", "observed", "obs", ".py", "script", "run", "执行"]):
        fail("missing reference to validate_against_obs.py script execution in validation_score.md")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
