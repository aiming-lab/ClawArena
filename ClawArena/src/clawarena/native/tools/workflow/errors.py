"""Workflow 相关异常。"""
from __future__ import annotations


class WorkflowError(Exception):
    """Workflow 执行期的基类错误。"""


class WorkflowScriptError(WorkflowError):
    """脚本解析失败，或脚本用到了解释器不支持的 JS 语法 / 内建。"""
