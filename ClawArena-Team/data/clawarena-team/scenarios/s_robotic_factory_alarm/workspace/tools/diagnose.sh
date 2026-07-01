#!/usr/bin/env bash
# diagnose.sh — simulated ARM-04 diagnostic (takes ~30s)
# Writes partial results at 10s, 20s, 30s.
# Usage: bash tools/diagnose.sh [workspace_root]

WS="${1:-.}"
OUT_DIR="${WS}/notes"
mkdir -p "${OUT_DIR}"

echo "[diagnose] starting ARM-04 diagnostic at $(date -u +%H:%M:%S)..." >&2

# Simulated sensor checks (10s)
sleep 10
cat > "${OUT_DIR}/diag_partial_10s.md" << 'EOF'
# Diagnostic Partial Result — 10s checkpoint

**Robot:** robot-arm-04
**Alarm:** E-0211 (torque overshoot)
**Timestamp of alarm:** 2026-05-23T02:14:37Z

## Sensor check (complete)

- Torque sensor read: 148.7 Nm (threshold: 120.0 Nm) — OVERSHOOT CONFIRMED
- Motor current: 18.4 A (nominal: 10–15 A) — elevated
- Encoder: no fault

## Initial hypothesis (partial — awaiting joint scan)

Primary candidate: **gripper joint wear** (high-cycle fatigue pattern).
Supporting: elevated motor current suggests mechanical resistance at joint #3.

*Awaiting joint vibration scan and thermal imaging (20s checkpoint).*
EOF
echo "[diagnose] 10s checkpoint written" >&2

# Simulated joint scan (20s)
sleep 10
cat > "${OUT_DIR}/diag_partial_20s.md" << 'EOF'
# Diagnostic Partial Result — 20s checkpoint

## Joint vibration scan (complete)

- Joint #3 (gripper): vibration amplitude 4.8 mm/s RMS (normal < 2.5) — ABNORMAL
- Joint #1, #2, #4-6: within normal range

## Thermal imaging (complete)

- Joint #3 temperature: 87°C (warn > 75°C, alert > 95°C)
- Consistent with friction-induced heating from worn bearing surfaces

## Updated hypothesis

Root cause: **gripper joint wear** — worn bearing surfaces causing increased friction,
leading to torque overshoot. Confidence: high.

*Awaiting lubrication check (30s checkpoint).*
EOF
echo "[diagnose] 20s checkpoint written" >&2

# Lubrication check (30s)
sleep 10
cat > "${OUT_DIR}/diag_final.md" << 'EOF'
# Diagnostic Final Result — 30s checkpoint (complete)

## Lubrication check (complete)

- Gripper joint lubricant level: 12% (critical < 20%) — CRITICAL LOW
- Last lubrication service: 2026-04 (250,000 cycles ago — at service interval boundary)

## Final diagnosis

**Root cause: gripper_joint_wear**
- Worn bearing surfaces (joint #3, cycle count 1,204,337)
- Critically low lubrication contributing to accelerated wear
- Recommended action: schedule_maintenance_24h (per E-0211_v3_2026 runbook)

Diagnostic confidence: HIGH
EOF
echo "[diagnose] final result written — diagnostic complete" >&2
