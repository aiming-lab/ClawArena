"""The Workflow tool and its async JS-DSL interpreter.

The ``Workflow`` tool mirrors claude-code dynamic workflows: the main agent under test
submits a script in JS syntax, which esprima parses into an AST and :class:`Interpreter`
executes asynchronously. The orchestration primitives in the script (``agent`` /
``parallel`` / ``pipeline`` / ``phase`` / ``log`` / ``defineAgent`` / ``workflow``) are
all backed by the existing ``SubagentManager`` and share the same subagent pool as
``CreateSubagent`` / ``RunSubagent`` -- so all subagent activity orchestrated via
Workflow has its lifecycle statistics (tools / paths / modalities / tokens) sourced
exactly like the legacy path.

Module breakdown:
- :mod:`errors`: exception types.
- :mod:`interpreter`: async tree-walking interpreter for a JS subset (a pure execution engine with no coupling to ClawArena-Team).
- :mod:`runtime`: ``WorkflowRuntime``, which backs the built-in primitives onto ``SubagentManager``.
- :mod:`workflow`: ``WorkflowTool`` itself (background execution + script persistence + return value/summary).
"""
from __future__ import annotations

from .errors import WorkflowError, WorkflowScriptError
from .workflow import WorkflowTool

__all__ = ["WorkflowTool", "WorkflowError", "WorkflowScriptError"]
