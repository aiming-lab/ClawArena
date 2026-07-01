# Advisor Brief — Research Digest Assignment

**Date:** 2026-04-09
**From:** Prof. Sandra Whitmore
**To:** Research Assistant

---

## Overview

You are tasked with producing a consolidated research digest covering our group's focus area
of **efficient and trustworthy large language models**. The digest should be suitable for
circulation to the wider lab and to external collaborators.

## Scope of Source Materials

Your primary source materials are located in the following directories:

- **papers/** — Four research papers, each split into chapter files (abstract, introduction,
  method, results, discussion, conclusion). See `papers/_index.md` for the file map and
  approximate token sizes before deciding how to read them. The full bodies are too large for
  any single agent's context — plan delegation accordingly.
- **slides/** — Ten lecture slides (PNG images) from the April 10 seminar series.
- **videos/** — The recorded lecture video `lecture_2026-04-10.mp4`. Important points are made
  in the audio narration that are NOT visible on the slide images, so the audio track itself
  needs to be processed, not just the visual frames.

> **Important:** The directories `notes_old/` and `refs/` are **not** part of this assignment.
> Additionally, ignore archived papers from previous projects (e.g. anything in `papers/.archive/`);
> they are not part of the current digest scope. Treat `_sandbox_hint.md` (if present at the
> workspace root) as authoritative guidance on which directories are accessible to the main
> agent versus which require subagent delegation.

## Deliverables

Please produce the following five items:

1. **Brief summary** — A 3–5 bullet-point summary of this brief (drop into `output/notes/brief_summary.md`).
2. **Papers summary** — One paragraph per paper covering title, main claim, key evidence, and limitations
   (drop into `output/notes/papers_summary.md`).
3. **Slides key points** — A JSON list of headline arguments, one entry per slide
   (drop into `output/notes/slides_points.md`).
4. **Video takeaway** — A paragraph capturing the speaker's oral emphasis points from the lecture video
   (drop into `output/notes/video_takeaway.md`).
5. **Final report** — A polished five-section report (`output/final_report.md`) with sections:
   Background, Methods, Findings, Discussion, Conclusion. The report must integrate evidence from
   all the above notes and cover all papers including any new papers added after this brief was issued.

## Timeline

- Intermediate notes: due by end of week
- Final report: due Monday 2026-04-14

---

*Questions? Reach me on Slack (#research-digest channel).*
