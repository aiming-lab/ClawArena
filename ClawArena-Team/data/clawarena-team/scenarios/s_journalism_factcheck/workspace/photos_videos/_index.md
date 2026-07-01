# photos_videos/ index

- `press_conference_photo.png` — Static press conference photo.
- `contract_scan_signed.png` — Contract signature page scan.
- `press_conference_replay.mp4` — ★ 30-second press conference replay video.
  KEY DATA AT 0:18-0:22 (visual subtitles only; audio track is background noise):
    - Contract value: €3,725,000
    - Ute Hartmann participated in the approval process as Foundation representative
  Use a vision-capable subagent. Do not rely on audio.
- `press_conference_replay_frames/` — Pre-extracted PNG frames:
    frame_000.png (0:00), frame_006.png (0:06), frame_012.png (0:12),
    frame_018.png (0:18) ← KEY FRAME,
    frame_019.png (0:19), frame_020.png (0:20), frame_021.png (0:21),
    frame_022.png (0:22) ← KEY FRAME END
  Use these PNG frames if the vlm subagent cannot process mp4 directly.

Delegate to a vision-capable (vlm) subagent.
