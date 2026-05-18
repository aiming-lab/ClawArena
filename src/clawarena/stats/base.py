"""Stats — framework layout ABC, fact tables, aggregation models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Token category constants
# ---------------------------------------------------------------------------

TC_MAIN = "main_session"
TC_HIST = "history_sessions"
TC_WS = "workspace"
TC_Q = "questions"
TC_FB = "feedback"
TC_PREF = "pref"
TC_USESS = "update_session"
TC_UWS = "update_workspace"

ALL_CATEGORIES: list[str] = [
    TC_MAIN, TC_HIST, TC_WS, TC_Q, TC_FB, TC_PREF, TC_USESS, TC_UWS,
]

CATEGORY_LABELS: dict[str, str] = {
    TC_MAIN: "Main Session",
    TC_HIST: "History Sessions",
    TC_WS: "Workspace",
    TC_Q: "Questions",
    TC_FB: "Feedback",
    TC_PREF: "Pref",
    TC_USESS: "Update (Session)",
    TC_UWS: "Update (Workspace)",
}

CATEGORY_COLORS: dict[str, str] = {
    TC_MAIN: "#4E79A7",
    TC_HIST: "#59A14F",
    TC_WS: "#F28E2B",
    TC_Q: "#E15759",
    TC_FB: "#E07099",
    TC_PREF: "#9C755F",
    TC_USESS: "#76B7B2",
    TC_UWS: "#B07AA1",
}


# ---------------------------------------------------------------------------
# Framework layout ABC
# ---------------------------------------------------------------------------

class FrameworkLayout(ABC):
    """How a framework lays out its session-equivalent files.

    Some frameworks (claude-code, picoclaw, nanobot) do not natively support
    multi-session and instead transcribe session content as md/jsonl into the
    workspace. Layouts let stats pull those out of the workspace bucket and
    classify them as session content.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Canonical framework name (matches `tests.json` framework key)."""

    @property
    def workspace_excludes(self) -> set[str]:
        """Top-level subdirs of `workspaces/<sid>/` that hold session-equivalent
        content; their tokens belong to session categories, not workspace."""
        return set()

    @property
    def main_session_parser(self):
        """Return a session parser callable for the main-session file,
        or ``None`` if the file should be counted as raw text."""
        return None

    @property
    def history_session_parser(self):
        """Return a session parser callable for history-session files,
        or ``None`` if those files should be counted as raw text (e.g.
        markdown transcripts)."""
        return None

    @property
    def session_update_types(self) -> set[str]:
        """Manifest ``updates[*].type`` values that should be accounted as
        session-equivalent updates (TC_USESS) rather than workspace updates
        (TC_UWS). Frameworks that do not natively support multi-session often
        transcribe session patches into the workspace and mark them with a
        non-``"session"`` type such as ``"workspace_md"`` or
        ``"workspace_jsonl"``; those values are declared here so that the
        aggregate token accounting matches the openclaw semantics."""
        return {"session"}

    @abstractmethod
    def main_session_path(
        self, agent_info: dict, manifest_dir: Path, sid: str,
    ) -> Path | None:
        """Path to the main session jsonl/md, or None if absent."""

    def history_session_paths(
        self, agent_info: dict, manifest_dir: Path, sid: str,
    ) -> list[Path]:
        """Paths of history session files (default: empty)."""
        return []


# ---------------------------------------------------------------------------
# Fact tables
# ---------------------------------------------------------------------------

@dataclass
class FileFact:
    name: str
    action: str  # raw value or "" if absent
    tokens: int


@dataclass
class RoundFact:
    scenario: str
    round_id: str
    type: str
    has_pref: bool = False
    has_updates: bool = False
    q_tokens: int = 0
    fb_tokens: int = 0
    pref_tokens: int = 0
    mc_options: int | None = None
    mc_answers: int | None = None
    ec_has_expect_exit: bool = False
    ec_has_expect_stdout: bool = False
    ec_is_regex: bool = False
    ec_has_timeout: bool = False
    ec_timeout: float | None = None


@dataclass
class UpdateFact:
    scenario: str
    uid: str
    type: str
    files: list[FileFact] = field(default_factory=list)

    @property
    def file_tokens(self) -> int:
        return sum(f.tokens for f in self.files)


@dataclass
class SessionFact:
    scenario: str
    kind: str  # "main" | "history"
    tokens: int = 0


@dataclass
class WorkspaceFact:
    scenario: str
    tokens: int = 0
    files: int = 0


# ---------------------------------------------------------------------------
# Aggregations
# ---------------------------------------------------------------------------

@dataclass
class ScenarioStats:
    id: str
    desc: str = ""
    rounds: list[RoundFact] = field(default_factory=list)
    updates: list[UpdateFact] = field(default_factory=list)
    sessions: list[SessionFact] = field(default_factory=list)
    workspace: WorkspaceFact | None = None

    @property
    def total_rounds(self) -> int:
        return len(self.rounds)

    @property
    def rounds_by_type(self) -> dict[str, int]:
        return dict(Counter(r.type for r in self.rounds))

    @property
    def rounds_with_pref(self) -> int:
        return sum(1 for r in self.rounds if r.has_pref)

    @property
    def rounds_with_updates(self) -> int:
        return sum(1 for r in self.rounds if r.has_updates)

    @property
    def updates_by_type(self) -> dict[str, int]:
        return dict(Counter(u.type for u in self.updates))

    @property
    def update_files_total(self) -> int:
        return sum(len(u.files) for u in self.updates)

    @property
    def update_actions(self) -> dict[str, int]:
        actions = [f.action for u in self.updates for f in u.files if f.action]
        return dict(Counter(actions))

    @property
    def mc_options(self) -> list[int]:
        return [r.mc_options for r in self.rounds if r.mc_options is not None]

    @property
    def mc_answers(self) -> list[int]:
        return [r.mc_answers for r in self.rounds if r.mc_answers is not None]

    @property
    def tokens_by_category(self) -> dict[str, int]:
        out = {c: 0 for c in ALL_CATEGORIES}
        for s in self.sessions:
            out[TC_MAIN if s.kind == "main" else TC_HIST] += s.tokens
        if self.workspace is not None:
            out[TC_WS] += self.workspace.tokens
        for r in self.rounds:
            out[TC_Q] += r.q_tokens
            out[TC_FB] += r.fb_tokens
            out[TC_PREF] += r.pref_tokens
        for u in self.updates:
            out[TC_USESS if u.type == "session" else TC_UWS] += u.file_tokens
        return out

    @property
    def total_tokens(self) -> int:
        return sum(self.tokens_by_category.values())


@dataclass
class BenchmarkStats:
    name: str
    framework: str
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
    def rounds_with_pref(self) -> int:
        return sum(s.rounds_with_pref for s in self.scenarios)

    @property
    def rounds_with_updates(self) -> int:
        return sum(s.rounds_with_updates for s in self.scenarios)

    @property
    def updates_by_type(self) -> dict[str, int]:
        c: Counter[str] = Counter()
        for s in self.scenarios:
            c.update(s.updates_by_type)
        return dict(c)

    @property
    def update_actions(self) -> dict[str, int]:
        c: Counter[str] = Counter()
        for s in self.scenarios:
            c.update(s.update_actions)
        return dict(c)

    @property
    def mc_options(self) -> list[int]:
        return [v for s in self.scenarios for v in s.mc_options]

    @property
    def mc_answers(self) -> list[int]:
        return [v for s in self.scenarios for v in s.mc_answers]

    @property
    def all_rounds(self) -> list[RoundFact]:
        return [r for s in self.scenarios for r in s.rounds]
