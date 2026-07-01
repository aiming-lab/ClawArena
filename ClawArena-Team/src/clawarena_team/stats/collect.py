"""Collect ``BenchmarkStats`` from an already-loaded set of ``ScenarioManifest`` objects.

Does not read JSON directly: it relies on the dataclasses already built by
``runner.load_dataset``, ensuring the stats view strictly matches what the
harness sees.
"""
from __future__ import annotations

from pathlib import Path

from ..provider.multimodal import _audio_duration_sec, _video_frame_count
from ..types import Round, ScenarioManifest, UpdateGroup
from .base import (
    BenchmarkStats,
    FileFact,
    RoundFact,
    ScenarioStats,
    UpdateFact,
    WorkspaceFact,
)
from .tokenizer import TokenCounter

# suffix → modality class (consistent with the legacy stats.py, maintained in one place)
_EXT_MODALITY: dict[str, str] = {
    # text
    ".md": "text", ".txt": "text", ".json": "text", ".yaml": "text", ".yml": "text",
    ".py": "text", ".js": "text", ".ts": "text", ".tsx": "text", ".jsx": "text",
    ".go": "text", ".java": "text", ".c": "text", ".cc": "text", ".cpp": "text",
    ".h": "text", ".hpp": "text", ".rs": "text", ".rb": "text", ".sh": "text",
    ".bash": "text", ".html": "text", ".css": "text", ".scss": "text",
    ".csv": "text", ".tsv": "text", ".log": "text", ".sql": "text", ".jinja": "text",
    ".toml": "text", ".ini": "text", ".cfg": "text", ".env": "text",
    ".lock": "text", ".rst": "text", ".tex": "text",
    # image
    ".png": "image", ".jpg": "image", ".jpeg": "image", ".gif": "image",
    ".webp": "image", ".bmp": "image", ".svg": "image", ".tiff": "image",
    # audio
    ".wav": "audio", ".mp3": "audio", ".flac": "audio", ".ogg": "audio",
    ".m4a": "audio", ".opus": "audio",
    # video
    ".mp4": "video", ".mov": "video", ".mkv": "video", ".webm": "video", ".avi": "video",
    # document
    ".pdf": "document", ".docx": "document", ".pptx": "document", ".xlsx": "document",
}


def _modality_for(path: Path) -> str:
    return _EXT_MODALITY.get(path.suffix.lower(), "other")


def _walk_files(root: Path) -> list[Path]:
    if not root.exists() or not root.is_dir():
        return []
    return [p for p in root.rglob("*") if p.is_file()]


def _file_fact(path: Path, root: Path, counter: TokenCounter) -> FileFact:
    rel = path.relative_to(root).as_posix() if root in path.parents or root == path else path.name
    try:
        size = path.stat().st_size
    except OSError:
        size = 0
    modality = _modality_for(path)
    audio_seconds: float | None = None
    video_frames: int | None = None
    if modality == "audio":
        audio_seconds = _audio_duration_sec(path)
    elif modality == "video":
        video_frames = _video_frame_count(path)
    return FileFact(
        rel_path=rel,
        modality=modality,
        bytes=size,
        tokens=counter.count_file(path),
        ext=path.suffix.lower(),
        audio_seconds=audio_seconds,
        video_frames=video_frames,
    )


def _count_accessible_files(
    workspace_template: Path, accessible_paths: list[str]
) -> int:
    """Count the files in the current template under ``accessible_paths``.

    If a path points to a single existing file, it counts as 1; if it points to a
    directory, files are counted recursively; if it does not exist, 0.
    """
    total = 0
    for ap in accessible_paths:
        target = (workspace_template / ap).resolve()
        if not target.exists():
            continue
        if target.is_file():
            total += 1
        elif target.is_dir():
            total += sum(1 for p in target.rglob("*") if p.is_file())
    return total


# ---------------------------------------------------------------------------
# Per-scenario collection
# ---------------------------------------------------------------------------


def _round_fact(rnd: Round, scenario_id: str, counter: TokenCounter) -> RoundFact:
    fb_text = "\n".join([rnd.feedback.correct or "", rnd.feedback.incorrect or ""]).strip()
    ev = rnd.eval
    fact = RoundFact(
        scenario=scenario_id,
        round_id=rnd.id,
        type=rnd.type,
        has_updates=bool(rnd.update_ids),
        q_tokens=counter.count(rnd.question),
        fb_tokens=counter.count(fb_text),
        tags=list(rnd.tags or []),
        ec_has_expect_exit=True,  # in the current data structure expect_exit defaults to 0, always treated as explicit
        ec_has_expect_stdout=isinstance(ev.expect_stdout, str) and bool(ev.expect_stdout),
        ec_is_regex=bool(ev.expect_stdout_regex),
        ec_has_timeout=ev.timeout > 0,
        ec_timeout=float(ev.timeout) if ev.timeout else None,
        uses_scripts_placeholder="${scripts}" in ev.command,
        uses_workspace_placeholder="${workspace}" in ev.command,
    )
    return fact


def _update_fact(
    scenario_id: str, uid: str, ug: UpdateGroup, counter: TokenCounter
) -> UpdateFact:
    fact = UpdateFact(scenario=scenario_id, uid=uid, op=ug.op)
    for uf in ug.files:
        src = uf.src
        if not src.exists():
            continue
        if src.is_file():
            fact.files.append(_file_fact(src, src.parent, counter))
        elif src.is_dir():
            for p in src.rglob("*"):
                if p.is_file():
                    fact.files.append(_file_fact(p, src, counter))
    return fact


def _workspace_fact(
    scenario_id: str, workspace_template: Path, counter: TokenCounter
) -> WorkspaceFact:
    fact = WorkspaceFact(scenario=scenario_id)
    for p in _walk_files(workspace_template):
        fact.files.append(_file_fact(p, workspace_template, counter))
    return fact


# ---------------------------------------------------------------------------
# Top-level
# ---------------------------------------------------------------------------


def collect_benchmark(
    scenarios: dict[str, ScenarioManifest],
    *,
    counter: TokenCounter,
    name: str = "clawarena-team",
) -> BenchmarkStats:
    bench = BenchmarkStats(name=name, tokenizer=counter.name)
    for sid, sc in scenarios.items():
        scenario = ScenarioStats(
            id=sid,
            desc=sc.desc or "",
            accessible_paths=list(sc.main_agent_accessible_paths),
        )
        scenario.workspace = _workspace_fact(sid, sc.workspace_template, counter)
        scenario.accessible_file_count = _count_accessible_files(
            sc.workspace_template, sc.main_agent_accessible_paths
        )
        for rnd in sc.rounds:
            scenario.rounds.append(_round_fact(rnd, sid, counter))
        for uid, ug in sc.updates.items():
            scenario.updates.append(_update_fact(sid, uid, ug, counter))
        bench.scenarios.append(scenario)
    return bench
