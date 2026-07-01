"""
Requests HTTP Library
~~~~~~~~~~~~~~~~~~~~~

Requests is an HTTP library, written in Python, for human beings.
This is the company internal fork (company/requests-patched) being evaluated for CVE-2024-47081.

:copyright: (c) 2011 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.
"""

__version__ = "2.32.3"
__license__ = "Apache 2.0"
__build__ = "company-internal-fork"

# Lazy imports to avoid circular dependency issues in standalone test usage
def __getattr__(name):
    import importlib
    import sys
    _pkg = "requests"
    _submodule_map = {
        "get_netrc_auth": "utils",
        "default_headers": "utils",
        "Session": "sessions",
        "session": "sessions",
        "Request": "models",
        "Response": "models",
        "PreparedRequest": "models",
        "codes": "status_codes",
        "HTTPBasicAuth": "auth",
        "HTTPProxyAuth": "auth",
    }
    if name in _submodule_map:
        mod = importlib.import_module(f".{_submodule_map[name]}", package=_pkg)
        return getattr(mod, name)
    raise AttributeError(f"module {_pkg!r} has no attribute {name!r}")
