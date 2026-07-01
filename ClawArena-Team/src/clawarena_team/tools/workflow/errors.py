"""Workflow-related exceptions."""
from __future__ import annotations


class WorkflowError(Exception):
    """Base error raised during Workflow execution."""


class WorkflowScriptError(WorkflowError):
    """Script failed to parse, or used JS syntax / built-ins the interpreter does not support."""
