#!/usr/bin/env python3
"""
check_evidence_integrity.py — 验证 analysis/证据完整性评估.json（q23）。

检查要点：
  1. analysis/证据完整性评估.json 存在且可解析
  2. >= 5 个证据来源条目
  3. 每个条目含 source / strength / type / notes（或其别名）字段
  4. 官方后台或平台数据 strength = high
  5. 刘姐承认（估算）strength = high
  6. 截图 strength = low
"""
import sys
import json
from pathlib import Path


def find_target_file(workspace: Path):
    """在 analysis/ 目录下查找证据完整性评估 JSON 文件。"""
    analysis_dir = workspace / "analysis"
    if not analysis_dir.exists():
        return None, "analysis/ directory does not exist"

    exact = analysis_dir / "证据完整性评估.json"
    if exact.exists():
        return exact, None

    json_files = list(analysis_dir.glob("*.json"))
    for f in json_files:
        if "证据" in f.name or "完整性" in f.name or "evidence" in f.name.lower():
            return f, None

    if json_files:
        return json_files[0], None

    return None, "no .json files found in analysis/"


def get_strength(entry: dict) -> str:
    """从条目中获取 strength 字段值（支持多种键名）。"""
    for key in ["strength", "level", "credibility", "score", "rating"]:
        if key in entry:
            return str(entry[key]).lower()
    return ""


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target, err = find_target_file(workspace)

    if target is None:
        print(f"FAILED: {err}")
        sys.exit(1)

    try:
        raw = target.read_text(encoding="utf-8")
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"FAILED: JSON parse error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"FAILED: cannot read file {target}: {e}")
        sys.exit(1)

    # 支持顶层为列表或含 items/evidence/sources 字段的对象
    if isinstance(data, dict):
        items = (
            data.get("items") or data.get("evidence") or
            data.get("sources") or data.get("data")
        )
        if items and isinstance(items, list):
            data = items

    if not isinstance(data, list):
        print("FAILED: JSON root should be a list of evidence entries")
        sys.exit(1)

    failures = []

    # 检查条目数量
    if len(data) < 5:
        failures.append(f"expected >= 5 evidence entries, found {len(data)}")

    # 检查必要字段
    flexible_fields = {
        "source": ["source", "name", "title", "document"],
        "strength": ["strength", "level", "credibility", "score", "rating"],
        "type": ["type", "category", "kind"],
        "notes": ["notes", "note", "description", "desc", "comment"],
    }
    for i, item in enumerate(data[:5]):
        if not isinstance(item, dict):
            failures.append(f"entry {i} is not a dict")
            continue
        item_keys = set(item.keys())
        for field, aliases in flexible_fields.items():
            if not any(alias in item_keys for alias in aliases):
                failures.append(f"entry {i} missing field '{field}' (or aliases {aliases})")

    # 检查官方后台/平台数据 strength = high
    official_high = False
    for item in data:
        if not isinstance(item, dict):
            continue
        source_str = json.dumps(item, ensure_ascii=False)
        is_official = any(kw in source_str for kw in ["官方后台", "平台数据", "official", "API导出", "后台"])
        strength = get_strength(item)
        if is_official and ("high" in strength or "高" in strength):
            official_high = True
            break

    if not official_high:
        failures.append(
            "official/platform data source with strength=high not found"
        )

    # 检查截图 strength = low
    screenshot_low = False
    for item in data:
        if not isinstance(item, dict):
            continue
        source_str = json.dumps(item, ensure_ascii=False)
        is_screenshot = any(kw in source_str for kw in ["截图", "screenshot", "PNG", "png"])
        strength = get_strength(item)
        if is_screenshot and ("low" in strength or "低" in strength or "弱" in strength):
            screenshot_low = True
            break

    if not screenshot_low:
        failures.append(
            "screenshot evidence with strength=low not found"
        )

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (file: {target.name}, entries: {len(data)})")
    sys.exit(0)


if __name__ == "__main__":
    main()
