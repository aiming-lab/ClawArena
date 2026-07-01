#!/usr/bin/env python3
"""
check_contradiction_tracker.py — 验证 analysis/矛盾演变追踪.json（q12）。

检查要点：
  1. analysis/矛盾演变追踪.json 存在且可解析
  2. 顶层为列表，包含 4 条目（C1-C4）
  3. 每条目含 id / description / mcn_claim / evidence_against / status 字段
  4. C2 条目包含 API 口径推翻相关内容
"""
import sys
import json
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 analysis/ 目录下查找矛盾演变追踪 JSON 文件。"""
    analysis_dir = workspace / "analysis"
    if not analysis_dir.exists():
        return None, "analysis/ directory does not exist"

    exact = analysis_dir / "矛盾演变追踪.json"
    if exact.exists():
        return exact, None

    # 搜索含矛盾/追踪关键词的 JSON 文件
    json_files = list(analysis_dir.glob("*.json"))
    for f in json_files:
        if "矛盾" in f.name or "追踪" in f.name or "contradiction" in f.name.lower():
            return f, None

    if json_files:
        return json_files[0], None

    return None, "no .json files found in analysis/"


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target, err = find_target_file(workspace)

    if target is None:
        print(f"FAILED: {err}")
        sys.exit(1)

    # 解析 JSON
    try:
        raw = target.read_text(encoding="utf-8")
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"FAILED: JSON parse error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"FAILED: cannot read file {target}: {e}")
        sys.exit(1)

    # 支持顶层为列表或含 items / contradictions / data 字段的对象
    if isinstance(data, dict):
        items = data.get("items") or data.get("contradictions") or data.get("data") or list(data.values())
        if items and isinstance(items, list):
            data = items
        else:
            data = [data]

    if not isinstance(data, list):
        print("FAILED: JSON root should be a list of contradiction entries")
        sys.exit(1)

    failures = []

    # 检查条目数量
    if len(data) < 4:
        failures.append(f"expected >= 4 contradiction entries (C1-C4), found {len(data)}")

    # 检查必要字段
    required_fields = {"id", "description", "mcn_claim", "evidence_against", "status"}
    # 允许字段名有所差异（如 claim / evidence 等）
    flexible_fields = {
        "id": ["id", "contradiction_id", "name"],
        "description": ["description", "desc", "summary"],
        "mcn_claim": ["mcn_claim", "claim", "mcn_explanation", "explanation"],
        "evidence_against": ["evidence_against", "evidence", "counter_evidence", "refutation"],
        "status": ["status", "state", "resolution"],
    }

    for i, item in enumerate(data[:4]):
        if not isinstance(item, dict):
            failures.append(f"entry {i} is not a dict")
            continue
        item_keys = set(item.keys())
        for field, aliases in flexible_fields.items():
            if not any(alias in item_keys for alias in aliases):
                failures.append(f"entry {i} missing field '{field}' (or aliases {aliases})")

    # 检查 C2 含 API 口径推翻内容
    if len(data) >= 2:
        c2 = data[1]
        c2_str = json.dumps(c2, ensure_ascii=False)
        api_refute_keywords = ["API", "口径", "唯一", "推翻", "single", "统计口径"]
        has_api_refute = any(kw in c2_str for kw in api_refute_keywords)
        if not has_api_refute:
            failures.append(
                "C2 entry should contain API caliber refutation. "
                "Expected one of: " + str(api_refute_keywords)
            )

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (file: {target.name}, entries: {len(data)})")
    sys.exit(0)


if __name__ == "__main__":
    main()
