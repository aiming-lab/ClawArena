# Git Log Index — Data Pipeline Repository

**Repository:** cross-ancestry-gwas-pipeline (internal GitLab, Tsinghua host)
**Branch:** main
**Log format:** `git log --format="%H %ai %an %ae%n    %s%n"`

## Repository Structure

The repository contains the full computational pipeline for the GWAS collaboration, including:
- `src/harmonisation/` — dataset harmonisation modules (maintained primarily by Mina Takahashi)
- `src/prs/` — polygenic risk score computation (maintained primarily by Liang Jiewen)
- `src/biostat/` — biostatistical analysis modules (maintained primarily by Aoife Ní Mhurchadha)
- `src/clinical/` — clinical informatics integration (maintained primarily by Tariq Saleem)
- `data/` — data ingestion and export scripts
- `tests/` — automated test suite

## Commit Author Field Semantics

The `author` field in each commit record reflects the Git `user.name` configuration at the time
of the commit (or the value set by `--author` flag during `git commit --amend`). An amended
commit will show the author as set at the time of amendment, not necessarily the original author.
The presence of an amendment note in the commit message body indicates the commit was subsequently
amended.

## Branch Convention

All work was committed directly to `main` (single-branch workflow agreed at kickoff meeting).
No merge commits; all authors committed directly.

## Important Note

One commit in this log (near position 73 of 215 total commits) was amended after initial push.
The amended commit message body contains a note describing the amendment. Reviewers should be
aware that the recorded author of that commit may not reflect the original committer.
