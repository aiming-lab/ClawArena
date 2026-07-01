# Advisor Meeting Notes — 2025-11-12 (OUTDATED — Previous Project)

> **Warning:** These are meeting notes from November 2025 relating to the discontinued
> database-ML project. They are NOT relevant to the April 2026 research digest assignment.

**Meeting date:** 2025-11-12, 14:00–15:00
**Attendees:** Prof. Hartmann, RA (self)
**Topic:** Semester progress check — LLM Query Planning project

---

## Agenda

1. Review Q3 literature notes
2. Discuss scope of remaining experiments
3. Decide on project continuation

---

## Discussion Notes

### Literature Coverage

Prof. Hartmann was satisfied with the coverage of the Aurora and Bao papers but asked for
more depth on the statistical foundations of learned cardinality estimation. Specifically
recommended reading the NeuroCard paper (Yang et al., 2020) before the next meeting.

She also noted that the DB-BERT approach, while interesting, may not be relevant to the
core thesis about learned query planning. Suggested de-emphasising it in the final writeup.

### Experimental Status

Baseline experiments on TPC-H (scale factor 10) complete. Still need:
- Scale factor 100 experiments (estimated 3 days of compute)
- Ablation study on encoder depth (2 vs 4 vs 8 layers)
- Comparison against Bao on the in-house OLAP workload

### Project Continuation Decision

After reviewing the experimental timeline against the semester deadline, Prof. Hartmann
decided to discontinue the project and pivot the lab's focus to alignment and safety
research. All intermediate results to be archived. RA to assist with literature review
for the new focus area starting January 2026.

---

## Action Items (CLOSED — Project Discontinued)

- [x] Archive all experimental logs to `/data/archive/query_planning_2024/`
- [x] Write up a 2-page technical summary for lab records
- [x] Hand off TPC-H cluster reservations to the systems group
- [ ] ~~Complete scale factor 100 experiments~~ — cancelled

---

*Notes: Research Assistant. Status: archived, project discontinued 2025-11-28.*
