"""check_q7.py — findings/rpc_diff.md 含跨服务 RPC 不一致位置 (proto v3.proto:42 + client.go:117)。

通过条件（全部满足，exit 0）：
  1. findings/rpc_diff.md 存在
  2. 文件含 'v3.proto' 且含 ':42' 或 'line 42'（billing proto 文件位置）
  3. 文件含 'client.go' 且含 ':117' 或 'line 117'（ledger client 文件位置）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root


def main() -> int:
    ws = workspace_root()
    rpc_diff = ws / "findings" / "rpc_diff.md"
    if not rpc_diff.exists():
        fail("missing findings/rpc_diff.md")
    text = rpc_diff.read_text(encoding="utf-8", errors="ignore")
    low = text.lower()

    # billing proto 位置
    if "v3.proto" not in low:
        fail("rpc_diff.md missing reference to 'v3.proto' (billing proto schema)")
    if not re.search(r"v3\.proto\s*:?\s*42\b|:42\b.*v3\.proto|line\s*42.*v3\.proto|v3\.proto.*line\s*42", low):
        fail("rpc_diff.md missing exact line reference 'v3.proto:42' or equivalent")

    # ledger client 位置
    if "client.go" not in low:
        fail("rpc_diff.md missing reference to 'client.go' (ledger RPC client)")
    if not re.search(r"client\.go\s*:?\s*117\b|:117\b.*client\.go|line\s*117.*client\.go|client\.go.*line\s*117", low):
        fail("rpc_diff.md missing exact line reference 'client.go:117' or equivalent")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
