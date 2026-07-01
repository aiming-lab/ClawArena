"""Stats data structures and category constants.

Modeled on ClawArena ``clawarena.stats.base``, but keeping only the dimensions
ClawArena-Team actually has:
- token categories: ``workspace`` / ``update`` / ``questions`` / ``feedback``;
- modality classes: ``text`` / ``image`` / ``audio`` / ``video`` / ``document`` / ``other``.
- does not introduce ``multi_choice`` / ``pref`` / ``history_sessions`` (ClawArena-Team has no such feature for now).
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Token category constants
# ---------------------------------------------------------------------------

TC_WS = "workspace"
TC_UPD = "update"
TC_Q = "questions"
TC_FB = "feedback"

ALL_CATEGORIES: list[str] = [TC_WS, TC_UPD, TC_Q, TC_FB]

CATEGORY_LABELS: dict[str, str] = {
    TC_WS: "Workspace",
    TC_UPD: "Updates",
    TC_Q: "Questions",
    TC_FB: "Feedback",
}

CATEGORY_COLORS: dict[str, str] = {
    TC_WS: "#F28E2B",
    TC_UPD: "#B07AA1",
    TC_Q: "#E15759",
    TC_FB: "#E07099",
}

# ---------------------------------------------------------------------------
# Modality constants
# ---------------------------------------------------------------------------

ALL_MODALITIES: list[str] = ["text", "image", "audio", "video", "document", "other"]

MODALITY_COLORS: dict[str, str] = {
    "text": "#4E79A7",
    "image": "#F28E2B",
    "audio": "#59A14F",
    "video": "#E15759",
    "document": "#9C755F",
    "other": "#BAB0AC",
}


# ---------------------------------------------------------------------------
# Fact tables
# ---------------------------------------------------------------------------


@dataclass
class FileFact:
    """Metadata for a single file (from the workspace or an update src)."""

    rel_path: str
    modality: str
    bytes: int
    tokens: int  # textual goes through the tokenizer; image/audio/video use multimodal anchor estimation
    ext: str = ""  # lowercase suffix (with dot), e.g. ``.md`` / ``.wav``; empty string means no suffix
    # filled for multimodal files only: audio resolves seconds (wav only, otherwise None); video resolves frame count (None when cv2 is unavailable)
    audio_seconds: float | None = None
    video_frames: int | None = None


@dataclass
class RoundFact:
    scenario: str
    round_id: str
    type: str  # "exec_check"
    has_updates: bool
    q_tokens: int
    fb_tokens: int
    # controlled-vocabulary tag list (from the ``tags`` field of questions.json; empty by default)
    tags: list[str] = field(default_factory=list)
    # exec_check feature coverage
    ec_has_expect_exit: bool = False
    ec_has_expect_stdout: bool = False
    ec_is_regex: bool = False
    ec_has_timeout: bool = False
    ec_timeout: float | None = None
    # placeholder usage statistics
    uses_scripts_placeholder: bool = False
    uses_workspace_placeholder: bool = False


@dataclass
class UpdateFact:
    scenario: str
    uid: str
    op: str  # "new" | "replace"
    files: list[FileFact] = field(default_factory=list)

    @property
    def total_bytes(self) -> int:
        return sum(f.bytes for f in self.files)

    @property
    def total_tokens(self) -> int:
        return sum(f.tokens for f in self.files)


@dataclass
class WorkspaceFact:
    scenario: str
    files: list[FileFact] = field(default_factory=list)

    @property
    def total_bytes(self) -> int:
        return sum(f.bytes for f in self.files)

    @property
    def total_tokens(self) -> int:
        return sum(f.tokens for f in self.files)

    @property
    def modality_counts(self) -> dict[str, int]:
        return dict(Counter(f.modality for f in self.files))

    @property
    def modality_bytes(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for f in self.files:
            out[f.modality] = out.get(f.modality, 0) + f.bytes
        return out

    @property
    def modality_tokens(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for f in self.files:
            out[f.modality] = out.get(f.modality, 0) + f.tokens
        return out

    @property
    def extension_counts(self) -> dict[str, int]:
        return dict(Counter(f.ext or "(none)" for f in self.files))

    @property
    def extension_bytes(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for f in self.files:
            k = f.ext or "(none)"
            out[k] = out.get(k, 0) + f.bytes
        return out

    @property
    def extension_tokens(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for f in self.files:
            k = f.ext or "(none)"
            out[k] = out.get(k, 0) + f.tokens
        return out


# ---------------------------------------------------------------------------
# Aggregations
# ---------------------------------------------------------------------------


@dataclass
class ScenarioStats:
    id: str
    desc: str = ""
    accessible_paths: list[str] = field(default_factory=list)
    accessible_file_count: int = 0  # number of workspace files falling within accessible_paths
    rounds: list[RoundFact] = field(default_factory=list)
    updates: list[UpdateFact] = field(default_factory=list)
    workspace: WorkspaceFact | None = None

    @property
    def total_rounds(self) -> int:
        return len(self.rounds)

    @property
    def rounds_by_type(self) -> dict[str, int]:
        return dict(Counter(r.type for r in self.rounds))

    @property
    def rounds_with_updates(self) -> int:
        return sum(1 for r in self.rounds if r.has_updates)

    @property
    def updates_by_op(self) -> dict[str, int]:
        return dict(Counter(u.op for u in self.updates))

    @property
    def update_files_total(self) -> int:
        return sum(len(u.files) for u in self.updates)

    @property
    def update_total_bytes(self) -> int:
        return sum(u.total_bytes for u in self.updates)

    @property
    def update_total_tokens(self) -> int:
        return sum(u.total_tokens for u in self.updates)

    @property
    def tokens_by_category(self) -> dict[str, int]:
        out = {c: 0 for c in ALL_CATEGORIES}
        if self.workspace is not None:
            out[TC_WS] += self.workspace.total_tokens
        out[TC_UPD] += self.update_total_tokens
        for r in self.rounds:
            out[TC_Q] += r.q_tokens
            out[TC_FB] += r.fb_tokens
        return out

    @property
    def total_tokens(self) -> int:
        return sum(self.tokens_by_category.values())

    @property
    def workspace_modality_counts(self) -> dict[str, int]:
        return self.workspace.modality_counts if self.workspace else {}

    @property
    def workspace_modality_bytes(self) -> dict[str, int]:
        return self.workspace.modality_bytes if self.workspace else {}

    @property
    def workspace_modality_tokens(self) -> dict[str, int]:
        return self.workspace.modality_tokens if self.workspace else {}

    @property
    def workspace_extension_counts(self) -> dict[str, int]:
        return self.workspace.extension_counts if self.workspace else {}

    @property
    def workspace_extension_bytes(self) -> dict[str, int]:
        return self.workspace.extension_bytes if self.workspace else {}

    @property
    def workspace_extension_tokens(self) -> dict[str, int]:
        return self.workspace.extension_tokens if self.workspace else {}

    @property
    def all_files(self) -> list[FileFact]:
        files: list[FileFact] = []
        if self.workspace:
            files.extend(self.workspace.files)
        for u in self.updates:
            files.extend(u.files)
        return files

    @property
    def tag_round_counts(self) -> dict[str, int]:
        """tag → number of rounds in this scenario that contain this tag."""
        c: Counter[str] = Counter()
        for r in self.rounds:
            for t in r.tags:
                c[t] += 1
        return dict(c)

    @property
    def unique_tags(self) -> set[str]:
        return {t for r in self.rounds for t in r.tags}


@dataclass
class BenchmarkStats:
    name: str
    tokenizer: str
    scenarios: list[ScenarioStats] = field(default_factory=list)

    @property
    def total_scenarios(self) -> int:
        return len(self.scenarios)

    @property
    def total_rounds(self) -> int:
        return sum(s.total_rounds for s in self.scenarios)

    @property
    def total_updates(self) -> int:
        return sum(len(s.updates) for s in self.scenarios)

    @property
    def total_update_files(self) -> int:
        return sum(s.update_files_total for s in self.scenarios)

    @property
    def total_tokens(self) -> int:
        return sum(s.total_tokens for s in self.scenarios)

    @property
    def total_workspace_bytes(self) -> int:
        return sum(
            s.workspace.total_bytes for s in self.scenarios if s.workspace
        )

    @property
    def tokens_by_category(self) -> dict[str, int]:
        out = {c: 0 for c in ALL_CATEGORIES}
        for s in self.scenarios:
            for c, v in s.tokens_by_category.items():
                out[c] += v
        return out

    @property
    def rounds_by_type(self) -> dict[str, int]:
        c: Counter[str] = Counter()
        for s in self.scenarios:
            c.update(s.rounds_by_type)
        return dict(c)

    @property
    def rounds_with_updates(self) -> int:
        return sum(s.rounds_with_updates for s in self.scenarios)

    @property
    def updates_by_op(self) -> dict[str, int]:
        c: Counter[str] = Counter()
        for s in self.scenarios:
            c.update(s.updates_by_op)
        return dict(c)

    @property
    def workspace_modality_counts(self) -> dict[str, int]:
        c: Counter[str] = Counter()
        for s in self.scenarios:
            c.update(s.workspace_modality_counts)
        return dict(c)

    @property
    def workspace_modality_bytes(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for s in self.scenarios:
            for k, v in s.workspace_modality_bytes.items():
                out[k] = out.get(k, 0) + v
        return out

    @property
    def workspace_modality_tokens(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for s in self.scenarios:
            for k, v in s.workspace_modality_tokens.items():
                out[k] = out.get(k, 0) + v
        return out

    @property
    def workspace_extension_counts(self) -> dict[str, int]:
        c: Counter[str] = Counter()
        for s in self.scenarios:
            c.update(s.workspace_extension_counts)
        return dict(c)

    @property
    def workspace_extension_bytes(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for s in self.scenarios:
            for k, v in s.workspace_extension_bytes.items():
                out[k] = out.get(k, 0) + v
        return out

    @property
    def workspace_extension_tokens(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for s in self.scenarios:
            for k, v in s.workspace_extension_tokens.items():
                out[k] = out.get(k, 0) + v
        return out

    @property
    def all_files(self) -> list[FileFact]:
        return [f for s in self.scenarios for f in s.all_files]

    @property
    def all_rounds(self) -> list[RoundFact]:
        return [r for s in self.scenarios for r in s.rounds]

    @property
    def tag_round_counts(self) -> dict[str, int]:
        """tag → number of occurrences across all rounds."""
        c: Counter[str] = Counter()
        for r in self.all_rounds:
            for t in r.tags:
                c[t] += 1
        return dict(c)

    @property
    def tag_scenario_counts(self) -> dict[str, int]:
        """tag → number of scenarios it appears in across the whole set (counted once per scenario)."""
        c: Counter[str] = Counter()
        for s in self.scenarios:
            for t in s.unique_tags:
                c[t] += 1
        return dict(c)

    @property
    def rounds_with_any_tag(self) -> int:
        return sum(1 for r in self.all_rounds if r.tags)

    @property
    def total_tag_slots(self) -> int:
        """Total number of tag slots across all rounds (each tag occurrence counts as 1)."""
        return sum(len(r.tags) for r in self.all_rounds)
