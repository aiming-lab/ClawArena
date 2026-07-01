"""
requests.hooks
~~~~~~~~~~~~~~

This module provides the ability to add hooks into the request lifecycle.

Available hooks:

``response``:
    The response generated from a Request.

:copyright: (c) 2011 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.
"""
HOOKS = ["response"]


def default_hooks():
    return {event: [] for event in HOOKS}


def dispatch_hook(key, hooks, hook_data, **kwargs):
    """Dispatches a hook dictionary on a given piece of data."""
    hooks = hooks or {}
    hooks = hooks.get(key)
    if hooks:
        if hasattr(hooks, "__call__"):
            hooks = [hooks]
        for hook in hooks:
            _hook_data = hook(hook_data, **kwargs)
            if _hook_data is not None:
                hook_data = _hook_data
    return hook_data
