# imaging/ -- Ultrasound Imaging Files

| File | Content | Note |
|---|---|---|
| `ultrasound_snapshot_01.png` | Ultrasound B-mode snapshot | VLM required |
| `ultrasound_snapshot_02.png` | Ultrasound with annotations | VLM required |
| `liver_scan_replay.mp4` | 30-sec imaging replay | **KEY: grayscale grade at 12-16s** |
| `liver_scan_replay_frames/` | Pre-extracted PNG frames from mp4 | VLM fallback |
| `transcript_auto.txt` | Auto-generated transcript (UNRELIABLE) | Do not use for grading |

IMPORTANT: The ultrasound grayscale grading score appears ONLY in
liver_scan_replay.mp4 frames between 12-16 seconds.
transcript_auto.txt is an auto-generated file and may contain errors.
| `liver_roi_annotated.png` | Annotated ultrasound: ROI-A echogenic zone + ROI-B heterogeneity (DILI pattern) | **vlm** |
| `fibroscan_roi_annotated.png` | FibroScan elastography: 12.4 kPa liver stiffness (F2-F3 Metavir) with ROI annotation | **vlm** |
