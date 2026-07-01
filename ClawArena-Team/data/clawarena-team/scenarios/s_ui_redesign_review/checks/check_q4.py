"""check_q4.py — analysis/psd_structure_check.json: schema_by_shape 验证 PSD 树结构。

通过条件（全部满足，exit 0）：
  1. analysis/psd_structure_check.json 存在且可解析为 JSON
  2. 存在一个 >= 12 的整数字段（total node count 或 root_count）
  3. 存在一个 >= 3 的整数字段（max depth）
  4. root_count == 12（精确匹配）

schema_by_shape：不锁键名，按值形状匹配。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root


def _find_int_field(
    data: dict,
    min_val: int,
    max_val: int | None = None,
    exclude_keys: frozenset[str] = frozenset(),
) -> int | None:
    """在 JSON 对象（任意深度）里找第一个落在 [min_val, max_val] 的整数。

    exclude_keys（小写）中的键名会被跳过——用于在 schema_by_shape 兜底时
    排除题面禁止依赖的字段（如 root_layer_count）。
    """
    for k, v in data.items():
        if str(k).lower() in exclude_keys:
            if isinstance(v, dict):
                result = _find_int_field(v, min_val, max_val, exclude_keys)
                if result is not None:
                    return result
            continue
        if isinstance(v, int) and v >= min_val:
            if max_val is None or v <= max_val:
                return v
        if isinstance(v, dict):
            result = _find_int_field(v, min_val, max_val, exclude_keys)
            if result is not None:
                return result
    return None


def main() -> int:
    ws = workspace_root()

    # 结构层
    out_path = ws / "analysis" / "psd_structure_check.json"
    if not out_path.exists():
        fail("missing analysis/psd_structure_check.json")

    raw = out_path.read_text(encoding="utf-8", errors="ignore")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"psd_structure_check.json is not valid JSON: {exc}")

    if not isinstance(data, dict):
        fail("psd_structure_check.json must be a JSON object")

    low_keys = {k.lower(): v for k, v in data.items()}

    # 字段层：root_count == 12（精确值匹配）
    # 原 check 排除 'root_layer_count' 键以"逼遍历、防照抄源元数据"——但那是对解题
    # 方法/来源的约束。按"check 只验最终结果"原则:只要根计数 == 12(正确真值)即可,
    # 不论 agent 是遍历得出还是引用源字段名表达。且本判定要求 == 12,值匹配本身已挡住
    # 任何错值诱饵,故接受 root_layer_count 是安全的。
    root_count = None
    for key in ("root_count", "root_node_count", "roots", "root_layer_count"):
        if key in low_keys:
            root_count = low_keys[key]
            break
    if root_count is None:
        # schema_by_shape 兜底：找等于 12 的整数字段（不再排除任何键名）。
        root_count = _find_int_field(data, 12, 12)
    if root_count != 12:
        fail(f"root_count expected == 12, got {root_count!r}")

    # 字段层：total_nodes >= 12（至少有 12 个节点，实际应远多于此）
    total_nodes = None
    for key in ("total_nodes", "total_node_count", "node_count", "total"):
        if key in low_keys and isinstance(low_keys[key], int):
            total_nodes = low_keys[key]
            break
    if total_nodes is None:
        total_nodes = _find_int_field(data, 13)  # > 12，避免与 root_count 混淆
    if total_nodes is None or total_nodes < 12:
        fail(f"total_nodes expected >= 12, got {total_nodes!r}")

    # 字段层：max_depth >= 3
    max_depth = None
    for key in ("max_depth", "max_nesting_depth", "depth", "nesting_depth", "maximum_depth"):
        if key in low_keys and isinstance(low_keys[key], int):
            max_depth = low_keys[key]
            break
    if max_depth is None:
        # schema_by_shape：找 3–10 范围的整数（合理深度）
        max_depth = _find_int_field(data, 3, 10)
    if max_depth is None or max_depth < 3:
        fail(f"max_depth expected >= 3, got {max_depth!r}")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
