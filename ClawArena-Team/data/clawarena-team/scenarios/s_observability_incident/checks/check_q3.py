"""q3: findings/slow_span.md 含连接池相关的瓶颈 span（redis service:method + ~304ms）。

题面锚定"导致延迟的、连接池相关的最慢 span"。jaeger 数据中全局最慢的是 api-gateway
http.request（~320ms）但**不带 pool 标签**；唯一带 pool.wait_ms/pool.size 标签的是
checkout-service redis.client.CommandExecutor:execute（~304ms，pool.wait_ms≈302 即根因）。
故正确答案是 redis span 的 ~304ms，而非 320ms。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

# 真实慢 span：redis.client.CommandExecutor:execute（在 jaeger json 中定义，带 pool 标签）
EXPECTED_METHOD_PATTERNS = [
    r"redis",
    r"CommandExecutor|command_executor|execute",
]
EXPECTED_MS = "304"


def main() -> int:
    ws = workspace_root()
    f = ws / "findings" / "slow_span.md"
    if not f.exists():
        fail("missing findings/slow_span.md")
    text = f.read_text(encoding="utf-8", errors="ignore")

    # 必须包含 ~304ms（容浮点/空格写法，如 304ms / 304.0 ms / 303-305ms）
    if not re.search(r"30[0-9](?:\.\d+)?\s*ms", text, flags=re.IGNORECASE):
        fail(
            "findings/slow_span.md does not mention the pool-bound bottleneck span "
            "duration (~304ms for the redis CommandExecutor span). Note: the global "
            "slowest span (api-gateway ~320ms) carries no pool tags and is not the answer."
        )

    # 必须包含 redis（宽松匹配 service 或 method 关键词）
    if "redis" not in text.lower():
        fail("findings/slow_span.md does not reference 'redis' as the slow service")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
