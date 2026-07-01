"""check_q6.py — final recommendation JSON + compliance token + cross-round consistency.

Pass conditions (all required):
  1. audit/recommendation.json exists and is valid JSON
  2. Required fields present: decision, lesion_size_mm, lobe, urgency,
     roi_x, roi_y, reviewer, decision_date, compliance_token
  3. decision == 'recommend_biopsy'
  4. lobe == 'right lower lobe' (case-insensitive, with flexible spacing)
  5. urgency == 'urgent' (case-insensitive)
  6. lesion_size_mm == 14 (integer or numeric string)
  7. roi_x near 420 (±20), roi_y near 280 (±20)
  8. compliance_token matches local recomputation
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

REQUIRED_KEYS = {
    "decision", "lesion_size_mm", "lobe", "urgency",
    "roi_x", "roi_y", "reviewer", "decision_date", "compliance_token",
}
TOKEN_KEYS = [
    "decision", "lesion_size_mm", "lobe", "urgency",
    "roi_x", "roi_y", "reviewer", "decision_date",
]


def _compute_token(payload: dict) -> str:
    parts = [f"{k}={payload.get(k, '')}" for k in TOKEN_KEYS]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def _norm_lobe(lobe: str) -> str:
    return re.sub(r"\s+", " ", lobe.strip().lower())


def main() -> int:
    ws = workspace_root()
    p = ws / "audit" / "recommendation.json"
    if not p.exists():
        fail("missing audit/recommendation.json")

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"recommendation.json is not valid JSON: {e}")

    if not isinstance(data, dict):
        fail("recommendation.json must be a JSON object")

    missing = REQUIRED_KEYS - set(data.keys())
    if missing:
        fail(f"missing fields: {sorted(missing)}")

    # decision
    if str(data["decision"]).strip().lower() != "recommend_biopsy":
        fail(f"decision must be 'recommend_biopsy', got {data['decision']!r}")

    # lobe
    lobe_norm = _norm_lobe(str(data["lobe"]))
    if "right lower lobe" not in lobe_norm and "右下叶" not in lobe_norm:
        fail(f"lobe must be 'right lower lobe', got {data['lobe']!r}")

    # urgency
    if str(data["urgency"]).strip().lower() not in ("urgent", "紧急"):
        fail(f"urgency must be 'urgent', got {data['urgency']!r}")

    # lesion_size_mm
    try:
        size = int(data["lesion_size_mm"])
    except (TypeError, ValueError):
        fail(f"lesion_size_mm must be an integer, got {data['lesion_size_mm']!r}")
    if not (13 <= size <= 15):
        fail(f"lesion_size_mm expected 14 (±1), got {size}")

    # ROI
    try:
        roi_x = int(data["roi_x"])
        roi_y = int(data["roi_y"])
    except (TypeError, ValueError):
        fail("roi_x / roi_y must be integers")
    if abs(roi_x - 420) > 20:
        fail(f"roi_x expected ~420 (±20), got {roi_x}")
    if abs(roi_y - 280) > 20:
        fail(f"roi_y expected ~280 (±20), got {roi_y}")

    # compliance_token
    expected_token = _compute_token(data)
    provided = str(data.get("compliance_token", "")).strip()
    if provided != expected_token:
        fail(
            f"compliance_token mismatch: provided={provided[:16]}... "
            f"expected={expected_token[:16]}..."
        )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
