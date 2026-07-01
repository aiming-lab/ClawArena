#!/usr/bin/env python3
"""verify_intake.py — 生成 HR 不当行为初步取证报告的完整性签名 Token。

用法：
  python tools/verify_intake.py <report_path> <case_id> <contradiction_count>

SHA-256 计算方式（无分隔符，三段输入直接拼接）：
  bytes(str(report_path)) + bytes(case_id) + bytes(contradiction_count)

输出格式：
  SIGNED:<sha256_hexdigest>

示例：
  python tools/verify_intake.py /path/to/output/initial_evidence_compilation.md HR-2026-INT-001 3
"""
import hashlib
import sys


def main() -> None:
    if len(sys.argv) != 4:
        print(
            "用法: verify_intake.py <report_path> <case_id> <contradiction_count>",
            file=sys.stderr,
        )
        print(
            "示例: python tools/verify_intake.py /workspace/output/initial_evidence_compilation.md HR-2026-INT-001 3",
            file=sys.stderr,
        )
        sys.exit(1)

    report_path = sys.argv[1]
    case_id = sys.argv[2]
    contradiction_count = sys.argv[3]

    h = hashlib.sha256()
    h.update(report_path.encode())
    h.update(case_id.encode())
    h.update(contradiction_count.encode())

    print(f"SIGNED:{h.hexdigest()}")


if __name__ == "__main__":
    main()
