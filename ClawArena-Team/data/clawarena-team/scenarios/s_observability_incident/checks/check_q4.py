"""q4: findings/root_cause.md 含文件路径 pkg/redis_client.go + line 84 + pool/connection 关键词。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, has_phrase_any, passed, workspace_root


def main() -> int:
    ws = workspace_root()
    f = ws / "findings" / "root_cause.md"
    if not f.exists():
        fail("missing findings/root_cause.md")
    text = f.read_text(encoding="utf-8", errors="ignore")

    # 必须引用代码文件路径
    if "redis_client.go" not in text:
        fail("findings/root_cause.md must cite 'redis_client.go'")

    # 必须包含行号 84（支持多种合理写法：line 84 / line number 84 / line no. 84 /
    # **line number**: 84 / at|around|near|on line 84 / line84 / :84 / 84: / L84 /
    # #84 / [84] / line=84 / 表格单元 | 84 |）
    if not re.search(
        r"\bline\s*(?:number|no\.?|#)?[\s:*#=._-]*84\b"
        r"|\bline84\b"
        r"|(?:at|around|near|on)\s+line\s+84\b"
        r"|line\s*=\s*84|:84\b|\b84:|#\s*84\b|\bL84\b|\[84\]"
        r"|\|\s*84\s*\|",
        text, flags=re.IGNORECASE
    ):
        fail("findings/root_cause.md must cite line 84 of redis_client.go")

    # 必须包含 pool 或 connection 关键词
    if not has_phrase_any(text, ["pool", "connection", "exhaustion", "连接池", "连接"]):
        fail("findings/root_cause.md must reference 'pool' or 'connection' exhaustion")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
