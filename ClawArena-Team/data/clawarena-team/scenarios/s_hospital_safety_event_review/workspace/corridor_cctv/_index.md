# corridor_cctv/ — ICU Corridor CCTV Recording

**File**: `corridor_cctv_2026-06-14T23-48.mp4`
**Duration**: 30 seconds (23:47:56 – 23:48:26)
**Camera**: CAM-04, MICU Hallway

## Contents

The recording covers the period immediately before and after the
device alarm event. Key information is visible ONLY in the video
frames — the audio track contains only HVAC noise and is not
relevant to the investigation.

## Ground Truth (visible in frames)

- **Alarm timestamp**: visible on frame at approximately t=11 s
  (wall clock 2026-06-14T23:48:07)
- **Alarm status**: ALARM_RED (device alarm indicator visible
  from t=11 s onward)

## Pre-extracted Frames

`frames/frame_*.png` — 30 frames (one per second) extracted from
the mp4 for use with vision-capable subagents.

Use a vision-capable (vlm) subagent to read the on-screen
timestamp and alarm status from the video frames.
