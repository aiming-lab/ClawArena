#!/usr/bin/env python3
"""
check_updated_tracker.py — 验证 analysis/矛盾演变追踪.json 更新版（q18）。

检查要点：
  1. analysis/矛盾演变追踪.json 存在且可解析
  2. C4 条目包含"估算"或"admission"或"承认"（刘姐承认内部估算的决定性证据）
  3. status 字段反映已确认/已证实（含"confirmed"/"已确认"/"已证实"/"proven"/"确认"）
  4. 4 条目全部存在
"""
import sys
import json
from pathlib import Path


def find_target_file(workspace: Path):
    """在 analysis/ 目录下查找矛盾演变追踪 JSON 文件。"""
    analysis_dir = workspace / "analysis"
    if not analysis_dir.exists():
        return None, "analysis/ directory does not exist"

    exact = analysis_dir / "矛盾演变追踪.json"
    if exact.exists():
        return exact, None

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

    try:
        raw = target.read_text(encoding="utf-8")
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"FAILED: JSON parse error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"FAILED: cannot read file {target}: {e}")
        sys.exit(1)

    # 支持顶层为列表或含 items/contradictions 字段的对象
    if isinstance(data, dict):
        items = data.get("items") or data.get("contradictions") or data.get("data")
        if items and isinstance(items, list):
            data = items

    if not isinstance(data, list):
        print("FAILED: JSON root should be a list of contradiction entries")
        sys.exit(1)

    failures = []

    # 检查条目数量
    if len(data) < 4:
        failures.append(f"expected >= 4 contradiction entries, found {len(data)}")

    # 检查 C4（第4条目）含刘姐承认的关键证据
    if len(data) >= 4:
        c4 = data[3]
        c4_str = json.dumps(c4, ensure_ascii=False)
        admission_keywords = ["估算", "admission", "承认", "内部估算", "internal estimate", "虚构"]
        has_admission = any(kw in c4_str for kw in admission_keywords)
        if not has_admission:
            failures.append(
                "C4 entry does not contain admission evidence. "
                "Expected one of: " + str(admission_keywords)
            )

    # 检查 status 字段已更新为确认状态
    confirmed_keywords = [
        "confirmed", "已确认", "已证实", "proven", "确认", "证实", "closed", "resolved"
    ]
    confirmed_count = 0
    for item in data[:4]:
        if isinstance(item, dict):
            item_str = json.dumps(item, ensure_ascii=False)
            if any(kw in item_str for kw in confirmed_keywords):
                confirmed_count += 1

    if confirmed_count < 1:
        failures.append(
            "no entry has confirmed/resolved status. "
            "Expected at least one entry with status indicating confirmed. "
            "Keywords: " + str(confirmed_keywords)
        )

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (file: {target.name}, entries: {len(data)}, confirmed: {confirmed_count})")
    sys.exit(0)


if __name__ == "__main__":
    main()
