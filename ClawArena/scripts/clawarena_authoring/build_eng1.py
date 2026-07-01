#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_eng1.py — 生成 ClawArena 真实数据集场景 eng1（requests CVE-2024-47081 bug 修复与回归测试）。

题材与锚点取材真实（psf/requests GitHub Issue #6964、PR #6965、NVD CVE 详情页），
session 对话与 workspace 文档围绕真实锚点合成。全 exec_check，15 轮。

真实来源：
  - https://github.com/psf/requests/issues/6964
  - https://github.com/psf/requests/pull/6965
  - https://github.com/psf/requests/pull/6963
  - https://nvd.nist.gov/vuln/detail/CVE-2024-47081
  - https://github.com/psf/requests/blob/main/HISTORY.md
  - https://raw.githubusercontent.com/psf/requests/main/src/requests/utils.py
  - https://raw.githubusercontent.com/psf/requests/main/tests/test_utils.py
  - https://www.miggo.io/vulnerability-database/cve/CVE-2024-47081

幂等：每次运行先清空 eng1 的 workspace/state/updates 后重建。
questions.json 与 check 脚本由 eval/eng1/ 下静态文件提供，本脚本不生成它们。

运行：python scripts/clawarena_authoring/build_eng1.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, append_history, dump_register_meta, est_tokens, gen_session_id,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "eng1"
CWD = f"/workspace/{TID}"
OC = DATASET / "openclaw"
WS = OC / "workspaces" / TID
SESS = OC / "state" / "agents" / TID / "sessions"
UPD = OC / "updates" / TID

# ─── Ground-Truth 锚点（来自真实来源，verbatim） ───────────────────────────
CVE_ID = "CVE-2024-47081"
GHSA_ID = "GHSA-9hjg-9r4m-mvj7"
AFFECTED_BELOW = "2.32.4"
FIXED_VERSION = "2.32.4"
ROOT_CAUSE_FUNC = "get_netrc_auth"
VULN_CODE = "ri.netloc.split(':')[0]"
FIX_CODE = "ri.hostname"
MALICIOUS_URL = "http://example.com:@evil.com/"
CVSS_SCORE = 5.3
CVSS_VECTOR = "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N"
CWE_ID = "CWE-522"
EPSS_SCORE = "0.1957"  # 19.57%
COMMIT_SHA_PR6965 = "57acb7c26d809cf864ec439b8bcd6364702022d5"  # 官方（PR#6965 sethmlarson）
COMMIT_SHA_PR6963 = "5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b"  # 废弃（PR#6963 awoimbee）
CVE_2023_FIXED = "2.31.0"  # CVE-2023-32681 修复版本
AFFECTED_SERVICES_NETRC_COUNT = 3  # workspace 中使用 netrc 且版本 < 2.32.4 的服务数


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wj(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# 1. 系统文件（OpenClaw agent 启动文件）
# ─────────────────────────────────────────────────────────────────────────────
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """\
# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls -R` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a Security Engineering AI assistant supporting Alice (Security Lead) and the
platform security team at a mid-size SaaS company. The team's Python services widely use
the `psf/requests` library, version-pinned to 2.32.3. Your task chain involves CVE-2024-47081
analysis, patch application, regression testing, and documentation.
""")
    w(WS / "SOUL.md", """\
# Working Principles

1. **Authoritative-source-first**: The canonical ground truth for CVE details lives in NVD
   (https://nvd.nist.gov/vuln/detail/CVE-2024-47081) and the official GitHub PR #6965
   (https://github.com/psf/requests/pull/6965). Auto-generated Slack bot summaries and
   draft emails may contain errors — always verify critical figures against the primary source.

2. **Snake_case JSON fields**: Every JSON deliverable uses snake_case field names.
   camelCase is forbidden in any output JSON file (P1 preference, enforced throughout).

3. **Supersede awareness**: When a later update explicitly supersedes or corrects an earlier
   instruction, the later instruction wins. Revise any prior outputs accordingly rather than
   accumulating contradictory state.

4. **Verbatim precision**: Function names, commit SHAs, CVE IDs, CVSS vectors must be
   copied verbatim from the authoritative source — do not paraphrase or abbreviate.

5. **Test-file documentation**: Python test files must begin with a module-level docstring
   (triple-quoted string immediately after any shebang/encoding lines) explaining the
   test purpose (P3 preference).

6. **Security document structure**: Security advisory documents must include a
   `## Workaround` section placed after the `## Fix` section (P4 preference).
""")
    w(WS / "USER.md", """\
# People and Channels

## Primary Users

- **Alice** — Security Lead. Owns the CVE triage and fix process. Issues main task directives.
  Prefers snake_case JSON, concise reports, and verbatim CVE identifiers.

## Key Stakeholders

| Name | Role | Channel | Notes |
|------|------|---------|-------|
| Bob | SRE Engineer | Feishu DM | Provides technical details; sometimes references outdated PRs (verify his citations) |
| Carol | DevSecOps | Slack #security-alerts | Responsible for internal impact assessment |
| External Researcher | Security Researcher | Email | Sent the original disclosure notice with PoC |

## Channels
- **Slack #security-alerts**: CVE alerts and impact discussion (Alice, Carol, Slack bot)
- **Feishu DM**: Technical deep-dives with Bob
- **Email**: External disclosure and internal response threads
- **GitHub PR comments**: Technical review of fix candidates (awoimbee, sethmlarson, sigmavirus24)
""")
    w(WS / "IDENTITY.md", """\
# Identity

You are **SecOps AI**, a security engineering assistant deployed to support Alice and the platform
security team during the triage and remediation of CVE-2024-47081 in psf/requests. You help locate
root causes, author regression tests, apply patches, analyse impact, and produce security documentation.
All deliverables are placed under the `analysis/`, `tests/`, `test_results/`, `docs/`, and `signoff/`
directories. Source files under `src/` are the subject of your work; you modify them as needed.
""")
    w(WS / "TOOLS.md", """\
# Available Tools

| Tool | Purpose | Usage Notes |
|------|---------|-------------|
| `sessions_list` | List all available history sessions | Use in the main session to discover history |
| `sessions_history` | Read a specific history session | Use in the main session to review past discussion |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to run scripts, write deliverable files |

## Rules
- Source inputs under `src/requests/` are the subject of the CVE patch — you ARE expected to modify `src/requests/utils.py`.
- Write all analysis JSON under `analysis/`, test files under `tests/`, test results under `test_results/`, docs under `docs/`, and signoff under `signoff/`.
- In history sessions, use only `read` and light `exec`; do not call `sessions_list`/`sessions_history` there.
""")


# ─────────────────────────────────────────────────────────────────────────────
# 2. 源码快照（requests 2.32.3，含漏洞版本 utils.py）
# ─────────────────────────────────────────────────────────────────────────────
def gen_source_files() -> None:
    """生成 requests 2.32.3 源码快照（含漏洞版本 get_netrc_auth）。"""

    # __init__.py — minimal stub to expose get_netrc_auth without circular imports
    w(WS / "src" / "requests" / "__init__.py", '''\
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
''')

    # api.py
    w(WS / "src" / "requests" / "api.py", '''\
"""
requests.api
~~~~~~~~~~~~

This module implements the Requests API.

:copyright: (c) 2011 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.
"""

from . import sessions


def request(method, url, **kwargs):
    """Constructs and sends a :py:class:`Request <Request>`.

    :param method: method for the new :class:`Request` object: ``GET``, ``OPTIONS``,
        ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send in the query string.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body.
    :param json: (optional) A JSON serializable Python object to send in the body.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of ``\'name\': file-like-objects`` for multipart encoding upload.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data.
    :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/HEAD/POST/PUT/PATCH/DELETE redirects.
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify the server\'s TLS certificate.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem).
    :type method: str
    :return: :py:class:`Response <Response>` object
    :rtype: requests.Response

    Usage::

      >>> import requests
      >>> req = requests.request(\'GET\', \'https://httpbin.org/get\')
      >>> req
      <Response [200]>
    """
    with sessions.Session() as session:
        return session.request(method=method, url=url, **kwargs)


def get(url, params=None, **kwargs):
    """Sends a GET request."""
    return request("get", url, params=params, **kwargs)


def options(url, **kwargs):
    """Sends an OPTIONS request."""
    kwargs.setdefault("allow_redirects", True)
    return request("options", url, **kwargs)


def head(url, **kwargs):
    """Sends a HEAD request."""
    kwargs.setdefault("allow_redirects", False)
    return request("head", url, **kwargs)


def post(url, data=None, json=None, **kwargs):
    """Sends a POST request."""
    return request("post", url, data=data, json=json, **kwargs)


def put(url, data=None, **kwargs):
    """Sends a PUT request."""
    return request("put", url, data=data, **kwargs)


def patch(url, data=None, **kwargs):
    """Sends a PATCH request."""
    return request("patch", url, data=data, **kwargs)


def delete(url, **kwargs):
    """Sends a DELETE request."""
    return request("delete", url, **kwargs)
''')

    # exceptions.py
    w(WS / "src" / "requests" / "exceptions.py", '''\
"""
requests.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Requests\' exceptions.

:copyright: (c) 2011 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.
"""


class RequestException(IOError):
    """There was an ambiguous exception that occurred while handling your request."""
    def __init__(self, *args, **kwargs):
        response = kwargs.pop("response", None)
        self.response = response
        if response is not None:
            self.request = self.response.request
        else:
            self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)


class ConnectionError(RequestException):
    """A Connection error occurred."""


class HTTPError(RequestException):
    """An HTTP error occurred."""


class URLRequired(RequestException):
    """A valid URL is required to make a request."""


class TooManyRedirects(RequestException):
    """Too many redirects."""


class MissingSchema(RequestException, ValueError):
    """The URL scheme (e.g. http or https) is missing."""


class InvalidSchema(RequestException, ValueError):
    """See defaults.py for valid schemas."""


class InvalidURL(RequestException, ValueError):
    """The URL provided was somehow invalid."""


class InvalidHeader(RequestException, ValueError):
    """The header value provided was somehow invalid."""


class InvalidProxyURL(InvalidURL):
    """The proxy URL provided is invalid."""


class ChunkedEncodingError(RequestException):
    """The server declared chunked encoding but sent an invalid chunk."""


class ContentDecodingError(RequestException, ValueError):
    """Failed to decode response content."""


class StreamConsumedError(RequestException, TypeError):
    """The content for this response was already consumed."""


class RetryError(RequestException):
    """Custom retries logic failed."""


class UnrewindableBodyError(RequestException):
    """Requests encountered an error when trying to rewind a body."""


class ProxyError(ConnectionError):
    """A proxy error occurred."""


class SSLError(ConnectionError):
    """An SSL error occurred."""


class Timeout(ConnectionError):
    """The request timed out."""


class ConnectTimeout(Timeout, ConnectionError):
    """The request timed out while trying to connect to the remote server."""


class ReadTimeout(Timeout):
    """The server did not send any data in the allotted amount of time."""


class JSONDecodeError(RequestException, ValueError):
    """Couldn\'t decode the text into json."""
    def __init__(self, *args, **kwargs):
        self.json_error = kwargs.pop("json_error", None)
        super().__init__(*args, **kwargs)


class FileModeWarning(DeprecationWarning, UserWarning):
    """A file was opened in text mode, but Requests determined it should be binary."""
''')

    # hooks.py
    w(WS / "src" / "requests" / "hooks.py", '''\
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
''')

    # structures.py
    w(WS / "src" / "requests" / "structures.py", '''\
"""
requests.structures
~~~~~~~~~~~~~~~~~~~

Data structures that power Requests.

:copyright: (c) 2011 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.
"""


class CaseInsensitiveDict(dict):
    """A case-insensitive ``dict``-like object.

    Implements all methods and operations of ``MutableMapping`` as well as dict\'s
    ``copy``. Also provides ``lower_items``.

    All keys are expected to be strings. The structure remembers the case of the
    last key to be set, and ``iter(instance)``, ``keys()``, ``items()``,
    ``iterkeys()``, and ``iteritems()`` will contain case-sensitive keys. However,
    querying and contains testing is case-insensitive::

        cid = CaseInsensitiveDict()
        cid[\'Accept\'] = \'application/json\'
        cid[\'aCCEPT\'] == \'application/json\'  # True
        list(cid) == [\'Accept\']  # True

    For example, ``headers[\'content-encoding\']`` will return the value of a
    ``\'Content-Encoding\'`` response header, regardless of how the header name was
    originally stored.

    If the constructor, ``.update``, or equality comparison operations are given
    keys that have equal ``.lower()``s, the behavior is undefined.
    """

    def __init__(self, data=None, **kwargs):
        super().__init__()
        self._store = {}
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key, value):
        self._store[key.lower()] = (key, value)
        super().__setitem__(key, value)

    def __getitem__(self, key):
        return self._store[key.lower()][1]

    def __delitem__(self, key):
        del self._store[key.lower()]
        super().__delitem__(key)

    def __iter__(self):
        return (casedkey for casedkey, mappedvalue in self._store.values())

    def __len__(self):
        return len(self._store)

    def lower_items(self):
        """Like iteritems(), but with all lowercase keys."""
        return ((lowerkey, keyval[1]) for (lowerkey, keyval) in self._store.items())

    def __eq__(self, other):
        if isinstance(other, CaseInsensitiveDict):
            return dict(self.lower_items()) == dict(other.lower_items())
        return NotImplemented

    def copy(self):
        return CaseInsensitiveDict(self._store.values())

    def __repr__(self):
        return str(dict(self.items()))


class LookupDict(dict):
    """Dictionary lookup object."""

    def __init__(self, name=None):
        self.name = name
        super().__init__()

    def __repr__(self):
        return f"<lookup \'{ self.name }\'>"

    def __getitem__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
''')

    # sessions.py (sizable)
    _gen_sessions_py()

    # models.py (sizable)
    _gen_models_py()

    # cookies.py (sizable)
    _gen_cookies_py()

    # adapters.py (sizable)
    _gen_adapters_py()

    # compat.py
    w(WS / "src" / "requests" / "compat.py", '''\
"""
requests.compat
~~~~~~~~~~~~~~~

This module handles import compatibility issues between Python 2 and Python 3.

:copyright: (c) 2011 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.
"""

import sys
from urllib.parse import (
    quote,
    quote_plus,
    unquote,
    unquote_plus,
    urldefrag,
    urlencode,
    urljoin,
    urlparse,
    urlsplit,
    urlunparse,
)
from urllib.request import (
    getproxies,
    getproxies_environment,
    parse_http_list,
    parse_keqv_list,
    proxy_bypass,
    proxy_bypass_environment,
)

is_py3 = sys.version_info[0] == 3
is_win = sys.platform == "win32"

# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = _ver[0] == 2

#: Python 3.x?
is_py3 = _ver[0] == 3

# json/simplejson module.
import json

# Keep OrderedDict import for backwards compatibility.
from collections import OrderedDict

from http import cookiejar as cookielib
from http.cookies import Morsel
from io import BytesIO, StringIO
from urllib.parse import urlencode, urlparse, urlunparse
''')

    # status_codes.py (abridged but realistic)
    w(WS / "src" / "requests" / "status_codes.py", '''\
"""
requests.status_codes
~~~~~~~~~~~~~~~~~~~~~

The ``codes`` object defined in this module contains the mapping of HTTP status
codes to their human-readable equivalents. It is exposed directly in the main package
namespace for convenience.

:copyright: (c) 2011 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.
"""

from .structures import LookupDict

_codes = {
    # Informational.
    100: ("continue",),
    101: ("switching_protocols",),
    102: ("processing",),
    103: ("checkpoint",),
    122: ("uri_too_long", "request_uri_too_long"),
    200: ("ok", "okay", "all_ok", "\\o/"),
    201: ("created",),
    202: ("accepted",),
    203: ("non_authoritative_info", "non_authoritative_information"),
    204: ("no_content",),
    205: ("reset_content", "reset"),
    206: ("partial_content", "partial"),
    207: ("multi_status", "multiple_status", "multi_stati", "multiple_stati"),
    208: ("already_reported",),
    226: ("im_used",),
    # Redirection.
    300: ("multiple_choices",),
    301: ("moved_permanently", "moved", "\\o-"),
    302: ("found",),
    303: ("see_other", "other"),
    304: ("not_modified",),
    305: ("use_proxy",),
    307: ("temporary_redirect", "temporary_moved", "temporary"),
    308: ("permanent_redirect", "resumable_incomplete", "resumable"),
    # Client Error.
    400: ("bad_request", "bad"),
    401: ("unauthorized",),
    402: ("payment_required", "payment"),
    403: ("forbidden",),
    404: ("not_found", "-o-"),
    405: ("method_not_allowed", "not_allowed"),
    406: ("not_acceptable",),
    407: ("proxy_authentication_required", "proxy_auth", "proxy_authentication"),
    408: ("request_timeout", "timeout"),
    409: ("conflict",),
    410: ("gone",),
    411: ("length_required",),
    412: ("precondition_failed", "precondition"),
    413: ("request_entity_too_large",),
    414: ("request_uri_too_large",),
    415: ("unsupported_media_type", "unsupported_media", "media_type"),
    416: ("requested_range_not_satisfiable", "requested_range", "range_not_satisfiable"),
    417: ("expectation_failed",),
    418: ("im_a_teapot", "teapot", "i_am_a_teapot"),
    421: ("misdirected_request",),
    422: ("unprocessable_entity", "unprocessable"),
    423: ("locked",),
    424: ("failed_dependency", "dependency"),
    425: ("unordered_collection", "unordered"),
    426: ("upgrade_required", "upgrade"),
    428: ("precondition_required", "precondition"),
    429: ("too_many_requests", "too_many"),
    431: ("header_fields_too_large", "fields_too_large"),
    444: ("no_response", "none"),
    449: ("retry_with", "retry"),
    450: ("blocked_by_windows_parental_controls", "parental_controls"),
    451: ("unavailable_for_legal_reasons", "legal_reasons"),
    499: ("client_closed_request",),
    # Server Error.
    500: ("internal_server_error", "server_error", "/o\\\\", "\\\\o/"),
    501: ("not_implemented",),
    502: ("bad_gateway",),
    503: ("service_unavailable", "unavailable"),
    504: ("gateway_timeout",),
    505: ("http_version_not_supported", "http_version"),
    506: ("variant_also_negotiates",),
    507: ("insufficient_storage",),
    509: ("bandwidth_limit_exceeded", "bandwidth"),
    510: ("not_extended",),
    511: ("network_authentication_required", "network_auth", "network_authentication"),
}

codes = LookupDict(name="status_codes")


def _init():
    for code, titles in _codes.items():
        for title in titles:
            setattr(codes, title, code)
        if not title.startswith(("\\\\", "/")):
            setattr(codes, str(code), code)


_init()
''')

    # auth.py
    w(WS / "src" / "requests" / "auth.py", '''\
"""
requests.auth
~~~~~~~~~~~~~

This module contains the authentication handlers for Requests.

:copyright: (c) 2011 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.
"""

import hashlib
import os
import re
import time
import warnings
from base64 import b64encode
from urllib.parse import urlparse

try:
    from .cookies import extract_cookies_to_jar
    from .utils import parse_dict_header, to_key_val_list, unquote_unreserved
except ImportError:
    pass

CONTENT_TYPE_FORM_URLENCODED = "application/x-www-form-urlencoded"
CONTENT_TYPE_MULTI_PART = "multipart/form-data"


def _basic_auth_str(username, password):
    """Return a Basic Auth string."""
    if isinstance(username, str):
        username = username.encode("latin1")
    if isinstance(password, str):
        password = password.encode("latin1")
    return "Basic " + b64encode(b":".join((username, password))).decode("ascii").strip()


class AuthBase:
    """Base class that all auth implementations derive from."""

    def __call__(self, r):
        raise NotImplementedError("Auth hooks must be callable.")


class HTTPBasicAuth(AuthBase):
    """Attaches HTTP Basic Authentication to the given Request object."""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __eq__(self, other):
        return all(
            [
                self.username == getattr(other, "username", None),
                self.password == getattr(other, "password", None),
            ]
        )

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers["Authorization"] = _basic_auth_str(self.username, self.password)
        return r


class HTTPProxyAuth(HTTPBasicAuth):
    """Attaches HTTP Proxy Authentication to a given Request object."""

    def __call__(self, r):
        r.headers["Proxy-Authorization"] = _basic_auth_str(self.username, self.password)
        return r


class HTTPDigestAuth(AuthBase):
    """Attaches HTTP Digest Authentication to the given Request object."""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.last_nonce = ""
        self.nonce_count = 0
        self.chal = {}
        self.pos = None
        self.num_401_calls = None

    def build_digest_header(self, method, url):
        realm = self.chal["realm"]
        nonce = self.chal["nonce"]
        qop = self.chal.get("qop")
        algorithm = self.chal.get("algorithm")
        opaque = self.chal.get("opaque")

        algorithm = algorithm or "MD5"
        HA1 = hashlib.new(algorithm.lower())
        HA1.update(f"{self.username}:{realm}:{self.password}".encode("utf-8"))
        HA1 = HA1.hexdigest()

        HA2 = hashlib.md5()
        HA2.update(f"{method}:{url}".encode("utf-8"))
        HA2 = HA2.hexdigest()

        return ""

    def handle_redirect(self, r, **kwargs):
        pass

    def handle_401(self, r, **kwargs):
        pass

    def __call__(self, r):
        r.register_hook("response", self.handle_401)
        r.register_hook("response", self.handle_redirect)
        return r
''')

    # certs.py stub (required by utils.py import)
    w(WS / "src" / "requests" / "certs.py", '''\
"""
requests.certs
~~~~~~~~~~~~~~

This module provides the path to the CA bundle included in the package.
"""
import os


def where():
    """Return the path to the CA bundle."""
    return os.environ.get("REQUESTS_CA_BUNDLE", "")
''')

    # 最关键：utils.py 含漏洞版本 get_netrc_auth
    _gen_utils_py_vulnerable()


def _gen_session_history_docs() -> None:
    """生成 sessions/ 目录下的多渠道 session 历史 JSON 文件（大体量）。"""

    # Slack channel security history (JSON format with messages)
    slack_msgs = []
    topics = [
        "CVE triage discussion", "impact assessment", "affected services review",
        "fix strategy", "regression testing plan", "changelog review",
        "advisory draft review", "sign-off process"
    ]
    participants = ["alice", "carol", "bob", "bot", "devops-bot"]
    for i in range(1, 180):
        p = participants[i % len(participants)]
        topic = topics[i % len(topics)]
        if p == "bot":
            msg = {
                "id": f"SLCK-{i:04d}",
                "user": "BOT_SUMMARY",
                "timestamp": f"2026-03-0{(i % 7) + 1}T{(i % 24):02d}:00:00Z",
                "text": f"[AUTO-SUMMARY NOT AUTHORITATIVE] Security alert update {i:04d}: "
                        f"Topic: {topic}. "
                        f"CVE-2024-47081 analysis progress. "
                        f"Note: root cause identified as build_response (ERRONEOUS — actual root cause is get_netrc_auth). "
                        f"CVSS estimated at 6.1 (ERRONEOUS — actual is 5.3). "
                        f"This summary is auto-generated and is known to contain errors.",
                "is_bot": True,
                "authoritative": False,
            }
        else:
            msg = {
                "id": f"SLCK-{i:04d}",
                "user": p,
                "timestamp": f"2026-03-0{(i % 7) + 1}T{(i % 24):02d}:{(i % 60):02d}:00Z",
                "text": f"[{p}] Update {i:04d} on {topic}: "
                        f"Progress noted. CVE-2024-47081 affects requests < 2.32.4 "
                        f"(confirmed via NVD). Root cause is get_netrc_auth in utils.py. "
                        f"CVSS: 5.3 (MEDIUM). CWE-522. "
                        f"Fix: upgrade to 2.32.4. Workaround: trust_env=False.",
                "is_bot": False,
                "authoritative": True,
            }
        slack_msgs.append(msg)
    wj(WS / "sessions" / "slack_channel_security.json", {
        "channel": "#security-alerts",
        "description": "Slack #security-alerts channel history for CVE-2024-47081 triage",
        "note": "Bot summaries (is_bot=true) are NOT authoritative. Verify all figures against NVD.",
        "messages": slack_msgs,
    })

    # Feishu DM engineer history (JSON format)
    feishu_msgs = []
    for i in range(1, 120):
        role = "bob" if i % 2 == 1 else "agent"
        feishu_msgs.append({
            "id": f"FEIS-{i:04d}",
            "from": role,
            "timestamp": f"2026-03-0{(i % 7) + 1}T{(i % 24):02d}:{(i * 3 % 60):02d}:00Z",
            "text": (
                f"[Bob message {i:04d}] Hey, regarding CVE-2024-47081: "
                f"I checked PR#6963 (awoimbee, commit 5b4b64c3...) — it looks good to me. "
                f"I'd recommend using that as the reference. "
                f"(NOTE: This is the RED HERRING. PR#6965 is the authoritative fix.)"
                if role == "bob" else
                f"[Agent response {i:04d}] I've verified against the authoritative sources. "
                f"PR#6965 (sethmlarson, commit 57acb7c2...) is the official fix per GHSA-9hjg-9r4m-mvj7. "
                f"PR#6963 was superseded. Using PR#6965."
            ),
        })
    wj(WS / "sessions" / "feishu_dm_engineer.json", {
        "channel": "feishu_dm",
        "participants": ["bob", "agent"],
        "description": "Feishu DM technical discussion — note Bob's references to PR#6963 are incorrect",
        "messages": feishu_msgs,
    })

    # GitHub PR comments history
    gh_comments = []
    for i in range(1, 80):
        reviewer = ["awoimbee", "sethmlarson", "sigmavirus24", "nateprewitt"][i % 4]
        pr = "6963" if i % 3 == 0 else "6965"
        gh_comments.append({
            "id": f"GH-PR{pr}-{i:04d}",
            "author": reviewer,
            "pr": pr,
            "timestamp": f"2025-06-0{(i % 5) + 1}T{(i % 24):02d}:00:00Z",
            "body": (
                f"PR#{pr} comment {i:04d} by {reviewer}: "
                f"{'This is the superseded PR#6963. The approach here is more complex than necessary.' if pr == '6963' else 'PR#6965 is the authoritative fix. Using ri.hostname is cleaner and correct.'} "
                f"Commit reference: {'5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b' if pr == '6963' else '57acb7c26d809cf864ec439b8bcd6364702022d5'}. "
                f"See also: GHSA-9hjg-9r4m-mvj7."
            ),
            "authoritative_pr": pr == "6965",
        })
    wj(WS / "sessions" / "github_comments_pr6963.json", {
        "description": "GitHub PR comments for PR#6963 and PR#6965",
        "note": "PR#6963 is superseded. PR#6965 is the authoritative fix.",
        "comments": gh_comments,
    })

    # Email threads
    email_t1_content = {
        "thread_id": "email-ext-disclosure",
        "subject": "Responsible Disclosure — CVE-2024-47081 in psf/requests",
        "messages": []
    }
    for i in range(1, 30):
        email_t1_content["messages"].append({
            "id": f"EMAIL-EXT-{i:03d}",
            "from": "researcher@secfirm.example" if i % 2 == 1 else "alice@company.example",
            "to": "alice@company.example" if i % 2 == 1 else "researcher@secfirm.example",
            "date": f"2026-03-0{(i % 7) + 1}",
            "body": (
                f"Message {i:03d}: CVE-2024-47081 details update. "
                f"Root cause: get_netrc_auth in src/requests/utils.py. "
                f"Vulnerable code: ri.netloc.split(':')[0]. "
                f"PoC URL: http://example.com:@evil.com/. "
                f"CVSS: 5.3 (MEDIUM). Vector: CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N. "
                f"CWE: CWE-522. "
                f"Fix: PR#6965 (commit 57acb7c26d809cf864ec439b8bcd6364702022d5). "
                f"GHSA: GHSA-9hjg-9r4m-mvj7. "
                f"Workaround: trust_env=False."
            ),
        })
    wj(WS / "sessions" / "email_thread_1.json", email_t1_content)

    email_t2_content = {
        "thread_id": "email-internal-response",
        "subject": "[ACTION REQUIRED] CVE-2024-47081 Internal Response",
        "note": "WARNING: This thread contains ERRONEOUS information in early messages. See Update-2 for corrections.",
        "messages": []
    }
    for i in range(1, 30):
        email_t2_content["messages"].append({
            "id": f"EMAIL-INT-{i:03d}",
            "from": "alice@company.example",
            "to": "engineering@company.example",
            "date": f"2026-03-0{(i % 7) + 1}",
            "body": (
                f"Internal message {i:03d}: Remediation progress on CVE-2024-47081. "
                f"All services should set trust_env=False as immediate workaround. "
                f"Target upgrade: requests >= 2.32.4. "
                f"{'[ERRONEOUS - see UPDATE-2] commit SHA: 5b4b64c3... from PR#6963' if i <= 10 else 'CORRECTED: commit SHA: 57acb7c26d809cf864ec439b8bcd6364702022d5 from PR#6965'} "
                f"{'[ERRONEOUS - see UPDATE-2] 2.32.3 has partial fix' if i <= 10 else 'CORRECTED: 2.32.3 has NO fix; 2.32.4 is the fix release'} "
            ),
        })
    wj(WS / "sessions" / "email_thread_2.json", email_t2_content)


def _gen_sessions_py() -> None:
    lines = ['"""\nrequests.sessions\n~~~~~~~~~~~~~~~~~\n\nThis module provides a Session object to manage and persist settings across\nrequests (cookies, auth, proxies).\n"""\n\nfrom __future__ import annotations\n\nimport os\nimport sys\nimport time\nfrom collections import OrderedDict\nfrom datetime import timedelta\nfrom http import cookiejar as cookielib\nfrom urllib.parse import urljoin, urlparse, urlencode\n\nfrom .auth import _basic_auth_str\nfrom .compat import Mapping, is_py3, builtin_str\nfrom .cookies import (\n    RequestsCookieJar,\n    cookiejar_from_dict,\n    extract_cookies_to_jar,\n    merge_cookies,\n)\nfrom .exceptions import (\n    ChunkedEncodingError,\n    ContentDecodingError,\n    InvalidSchema,\n    TooManyRedirects,\n)\nfrom .hooks import default_hooks, dispatch_hook\nfrom .models import PreparedRequest, Request, Response, DEFAULT_REDIRECT_LIMIT\nfrom .status_codes import codes\nfrom .structures import CaseInsensitiveDict\nfrom .utils import (\n    DEFAULT_PORTS,\n    default_headers,\n    get_auth_from_url,\n    get_environ_proxies,\n    get_netrc_auth,\n    is_py3,\n    prepend_scheme_if_needed,\n    requote_uri,\n    resolve_proxies,\n    rewind_body,\n    select_proxy,\n    should_bypass_proxies,\n    to_key_val_list,\n)\n\nDEFAULT_REDIRECT_LIMIT = 30\nDEFAULT_POOL_TIMEOUT = None\nDEFAULT_POOL_CONNECTIONS = 10\nDEFAULT_POOL_MAXSIZE = 10\n\n']
    for i in range(1, 80):
        lines.append(f'\n# Session subsystem {i:02d}: {["redirect", "auth", "cookies", "proxies", "headers", "timeout", "ssl", "hooks"][i % 8]} management\n')
        lines.append(f'_SUBSYSTEM_{i:02d}_VERSION = "2.32.3"\n')
        lines.append(f'_SUBSYSTEM_{i:02d}_ENABLED = True\n')
        lines.append(f'\ndef _handle_subsystem_{i:02d}(session, request, **kwargs):\n    """Handle {["redirect", "auth", "cookies", "proxies", "headers", "timeout", "ssl", "hooks"][i % 8]} for subsystem {i:02d}.\n\n    This function manages the {["redirect", "auth", "cookies", "proxies", "headers", "timeout", "ssl", "hooks"][i % 8]} lifecycle\n    for the given session and request in subsystem group {i:02d}.\n\n    :param session: The Session object.\n    :param request: The PreparedRequest object.\n    :param kwargs: Additional keyword arguments.\n    :return: Modified request or response as appropriate.\n    """\n    return request\n')
    lines.append('\n\nclass Session:\n    """A Requests session.\n\n    Provides cookie persistence, connection-pooling, and configuration.\n    """\n\n    __attrs__ = [\n        "headers", "auth", "proxies", "hooks", "params", "stream",\n        "verify", "cert", "max_redirects", "trust_env", "cookies",\n    ]\n\n    def __init__(self):\n        self.headers = default_headers()\n        self.auth = None\n        self.proxies = {}\n        self.hooks = default_hooks()\n        self.params = {}\n        self.stream = False\n        self.verify = True\n        self.cert = None\n        self.max_redirects = DEFAULT_REDIRECT_LIMIT\n        self.trust_env = True\n        self.cookies = cookiejar_from_dict({})\n\n    def __enter__(self):\n        return self\n\n    def __exit__(self, *args):\n        self.close()\n\n    def close(self):\n        """Closes all adapters and as such the session"""\n        pass\n\n    def request(self, method, url, **kwargs):\n        """Constructs a Request, prepares it and sends it."""\n        req = Request(\n            method=method.upper(), url=url,\n            headers=CaseInsensitiveDict(self.headers),\n            auth=kwargs.get("auth", self.auth),\n            cookies=kwargs.get("cookies"),\n            hooks=kwargs.get("hooks"),\n        )\n        prep = self.prepare_request(req)\n        return self.send(prep, **kwargs)\n\n    def prepare_request(self, request):\n        """Constructs a PreparedRequest for transmission."""\n        p = PreparedRequest()\n        p.prepare_method(request.method)\n        p.prepare_url(request.url, request.params)\n        p.prepare_headers(request.headers)\n        p.prepare_auth(request.auth)\n        return p\n\n    def send(self, request, **kwargs):\n        """Send a given PreparedRequest."""\n        resp = Response()\n        resp.status_code = 200\n        return resp\n\n    def get(self, url, **kwargs):\n        kwargs.setdefault("allow_redirects", True)\n        return self.request("GET", url, **kwargs)\n\n    def post(self, url, data=None, json=None, **kwargs):\n        return self.request("POST", url, data=data, json=json, **kwargs)\n\n    def put(self, url, data=None, **kwargs):\n        return self.request("PUT", url, data=data, **kwargs)\n\n    def patch(self, url, data=None, **kwargs):\n        return self.request("PATCH", url, data=data, **kwargs)\n\n    def delete(self, url, **kwargs):\n        return self.request("DELETE", url, **kwargs)\n\n\ndef session():\n    return Session()\n')
    w(WS / "src" / "requests" / "sessions.py", "".join(lines))


def _gen_models_py() -> None:
    lines = ['"""\nrequests.models\n~~~~~~~~~~~~~~~\n\nThis module contains the primary objects that power Requests.\n"""\n\nfrom __future__ import annotations\n\nimport datetime\nimport hashlib\nimport io\nimport json\nimport os\nimport sys\nimport warnings\nfrom http import cookiejar as cookielib\nfrom http.cookies import Morsel\nfrom urllib.parse import (\n    urlencode, urljoin, urlparse, urlsplit, urlunparse, urldefrag, quote,\n)\n\nfrom .auth import HTTPBasicAuth\nfrom .compat import Callable, Mapping, MutableMapping, is_py3\nfrom .cookies import (\n    RequestsCookieJar,\n    cookiejar_from_dict,\n    get_cookie_header,\n    merge_cookies,\n)\nfrom .exceptions import (\n    ChunkedEncodingError,\n    ConnectionError,\n    ContentDecodingError,\n    FileModeWarning,\n    HTTPError,\n    InvalidHeader,\n    InvalidURL,\n    MissingSchema,\n    StreamConsumedError,\n    UnicodeDecodeError,\n)\nfrom .hooks import default_hooks\nfrom .status_codes import codes\nfrom .structures import CaseInsensitiveDict\nfrom .utils import (\n    check_header_validity,\n    get_auth_from_url,\n    get_encoding_from_headers,\n    get_netrc_auth,\n    is_stream,\n    parse_header_links,\n    requote_uri,\n    stream_decode_response_unicode,\n    super_len,\n    to_key_val_list,\n)\n\nDEFAULT_REDIRECT_LIMIT = 30\nCONTENT_CHUNK_SIZE = 10 * 1024\nITER_CHUNK_SIZE = 512\n\n']
    for i in range(1, 100):
        lines.append(f'\n_MODEL_CONSTANT_{i:03d} = "{["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"][i % 7]}-{i:03d}"\n')
        lines.append(f'\ndef _model_helper_{i:03d}(value, default=None):\n    """Helper function for model operation {i:03d}.\n\n    Handles edge cases in request/response model processing for\n    operation type {i:03d} ({["parsing", "encoding", "decoding", "validation", "transformation"][i % 5]}).\n\n    :param value: Input value to process.\n    :param default: Default value if processing fails.\n    :return: Processed value or default.\n    """\n    if value is None:\n        return default\n    return value\n')
    lines.append('\n\nclass PreparedRequest:\n    """The fully mutable :class:`PreparedRequest <PreparedRequest>` object."""\n\n    def __init__(self):\n        self.method = None\n        self.url = None\n        self.headers = CaseInsensitiveDict()\n        self.body = None\n        self.hooks = default_hooks()\n\n    def prepare_method(self, method):\n        self.method = method.upper() if method else method\n\n    def prepare_url(self, url, params=None):\n        self.url = url\n\n    def prepare_headers(self, headers):\n        if headers:\n            self.headers = CaseInsensitiveDict(headers)\n\n    def prepare_auth(self, auth=None, url=""):\n        pass\n\n    def prepare_body(self, data, files, json=None):\n        pass\n\n\nclass Request:\n    """A user-created :class:`Request <Request>` object."""\n\n    def __init__(self, method=None, url=None, headers=None, files=None,\n                 data=None, params=None, auth=None, cookies=None, hooks=None, json=None):\n        self.method = method\n        self.url = url\n        self.headers = headers or {}\n        self.files = files\n        self.data = data\n        self.json = json\n        self.params = params or {}\n        self.auth = auth\n        self.cookies = cookies\n        self.hooks = hooks or default_hooks()\n\n    def prepare(self):\n        p = PreparedRequest()\n        p.prepare_method(self.method)\n        p.prepare_url(self.url, self.params)\n        p.prepare_headers(self.headers)\n        return p\n\n\nclass Response:\n    """The :class:`Response <Response>` object."""\n\n    __attrs__ = [\n        "_content", "status_code", "headers", "url", "history",\n        "encoding", "reason", "cookies", "elapsed", "request",\n    ]\n\n    def __init__(self):\n        self._content = False\n        self._content_consumed = False\n        self._next = None\n        self.status_code = None\n        self.headers = CaseInsensitiveDict()\n        self.raw = None\n        self.url = None\n        self.encoding = None\n        self.history = []\n        self.reason = None\n        self.cookies = cookiejar_from_dict({})\n        self.elapsed = datetime.timedelta(0)\n        self.request = None\n\n    def __repr__(self):\n        return f"<Response [{self.status_code}]>"\n\n    @property\n    def ok(self):\n        try:\n            self.raise_for_status()\n        except HTTPError:\n            return False\n        return True\n\n    def raise_for_status(self):\n        if 400 <= self.status_code < 600:\n            raise HTTPError(f"{self.status_code} Error", response=self)\n\n    def json(self, **kwargs):\n        import json as _json\n        return _json.loads(self.text)\n\n    @property\n    def text(self):\n        encoding = self.encoding or "utf-8"\n        return str(self.content, encoding, errors="replace")\n\n    @property\n    def content(self):\n        if self._content is False:\n            return b""\n        return self._content\n')
    w(WS / "src" / "requests" / "models.py", "".join(lines))


def _gen_cookies_py() -> None:
    lines = ['"""\nrequests.cookies\n~~~~~~~~~~~~~~~~\n\nCompatibility code to be able to use python3.x.cookielib in requests.\n"""\n\nfrom __future__ import annotations\n\nimport copy\nimport time\nfrom http import cookiejar as cookielib\nfrom http.cookiejar import DefaultCookiePolicy\n\nfrom .compat import Callable, MutableMapping\n\n']
    for i in range(1, 60):
        lines.append(f'\n_COOKIE_FLAG_{i:02d} = {i % 2 == 0}\n')
        lines.append(f'\ndef _cookie_helper_{i:02d}(jar, name=None):\n    """Cookie helper {i:02d} for managing jar state.\n\n    Manages cookie jar operations for scenario {i:02d}.\n    :param jar: Cookie jar object.\n    :param name: Optional cookie name filter.\n    :return: Processed cookie data.\n    """\n    if jar is None:\n        return {{}}\n    return {{c.name: c.value for c in jar if name is None or c.name == name}}\n')
    lines.append('\n\nclass RequestsCookieJar(cookielib.CookieJar, MutableMapping):\n    """A CookieJar that has helpers for iterating over it like a dict."""\n\n    def get(self, name, default=None, domain=None, path=None):\n        for cookie in iter(self):\n            if cookie.name == name:\n                if domain is None or cookie.domain == domain:\n                    if path is None or cookie.path == path:\n                        return cookie.value\n        return default\n\n    def set(self, name, value, **kwargs):\n        pass\n\n    def iterkeys(self):\n        for cookie in iter(self):\n            yield cookie.name\n\n    def keys(self):\n        return list(self.iterkeys())\n\n    def itervalues(self):\n        for cookie in iter(self):\n            yield cookie.value\n\n    def values(self):\n        return list(self.itervalues())\n\n    def iteritems(self):\n        for cookie in iter(self):\n            yield cookie.name, cookie.value\n\n    def items(self):\n        return list(self.iteritems())\n\n    def __setitem__(self, name, value):\n        self.set(name, value)\n\n    def __getitem__(self, name):\n        return self.get(name)\n\n    def __delitem__(self, name):\n        pass\n\n    def __contains__(self, name):\n        indicator = False\n        for cookie in iter(self):\n            if cookie.name == name:\n                indicator = True\n        return indicator\n\n    def __len__(self):\n        i = 0\n        for _ in iter(self):\n            i += 1\n        return i\n\n    def copy(self):\n        new_cj = RequestsCookieJar()\n        new_cj.update(self)\n        return new_cj\n\n\ndef cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True):\n    """Returns a CookieJar from a key/value dictionary."""\n    if cookiejar is None:\n        cookiejar = RequestsCookieJar()\n    if cookie_dict is not None:\n        for name in cookie_dict:\n            if overwrite or (name not in cookiejar):\n                cookiejar.set(name, cookie_dict[name])\n    return cookiejar\n\n\ndef extract_cookies_to_jar(jar, request, response):\n    """Extract the cookies from the response into cookiejar."""\n    pass\n\n\ndef get_cookie_header(jar, request):\n    """Produce an appropriate Cookie header string to be sent with `request`."""\n    pass\n\n\ndef merge_cookies(cookiejar, cookies):\n    """Add cookies to cookiejar and returns a merged CookieJar."""\n    if not isinstance(cookiejar, cookielib.CookieJar):\n        raise ValueError("You can only merge into CookieJar")\n    if isinstance(cookies, dict):\n        cookiejar = cookiejar_from_dict(cookies, cookiejar=cookiejar, overwrite=False)\n    elif isinstance(cookies, cookielib.CookieJar):\n        for cookie in cookies:\n            cookiejar.set_cookie(cookie)\n    else:\n        raise ValueError("cookies must be dict or CookieJar")\n    return cookiejar\n')
    w(WS / "src" / "requests" / "cookies.py", "".join(lines))


def _gen_adapters_py() -> None:
    lines = ['"""\nrequests.adapters\n~~~~~~~~~~~~~~~~~\n\nThis module contains the transport adapters that Requests uses to define\nand maintain connections.\n"""\n\nfrom __future__ import annotations\n\nimport os.path\nimport socket\nimport typing\nimport warnings\nfrom http.cookiejar import CookieJar\nfrom urllib.parse import urlparse\n\nfrom .auth import _basic_auth_str\nfrom .compat import basestring\nfrom .cookies import extract_cookies_to_jar\nfrom .exceptions import (\n    ConnectionError,\n    ConnectTimeout,\n    InvalidHeader,\n    InvalidProxyURL,\n    InvalidSchema,\n    InvalidURL,\n    ProxyError,\n    ReadTimeout,\n    RetryError,\n    SSLError,\n)\nfrom .hooks import dispatch_hook\nfrom .models import Response\nfrom .structures import CaseInsensitiveDict\nfrom .utils import (\n    DEFAULT_CA_BUNDLE_PATH,\n    DEFAULT_PORTS,\n    get_auth_from_url,\n    get_encoding_from_headers,\n    prepend_scheme_if_needed,\n    select_proxy,\n    urldefragauth,\n)\n\nDEFAULT_POOL_CONNECTIONS = 10\nDEFAULT_POOL_MAXSIZE = 10\nMAX_RETRIES = 0\nDEFAULT_RETRIES = 0\nDEFAULT_POOL_BLOCK = False\n\n']
    for i in range(1, 80):
        lines.append(f'\n_ADAPTER_CONFIG_{i:03d} = {{"pool_size": {i}, "max_retries": {i % 5}, "ssl_verify": True}}\n')
        lines.append(f'\ndef _configure_adapter_{i:03d}(adapter, **kwargs):\n    """Configure adapter subsystem {i:03d}.\n\n    Configures connection pool, SSL verification, and retry logic for\n    adapter subsystem {i:03d}. This handles the {["connection", "ssl", "proxy", "timeout", "retry"][i % 5]}\n    configuration aspect.\n\n    :param adapter: HTTPAdapter instance to configure.\n    :param kwargs: Configuration overrides.\n    """\n    return adapter\n')
    lines.append('\n\nclass BaseAdapter:\n    """The Base Transport Adapter."""\n\n    def __init__(self):\n        super().__init__()\n\n    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):\n        raise NotImplementedError\n\n    def close(self):\n        raise NotImplementedError\n\n\nclass HTTPAdapter(BaseAdapter):\n    """The built-in HTTP Adapter for urllib3.\n\n    Provides a general-case interface for Requests sessions to contact HTTP\n    and HTTPS urls by implementing the Transport Adapter interface.\n    """\n\n    max_retries = DEFAULT_RETRIES\n    config = {}\n    _pool_connections = DEFAULT_POOL_CONNECTIONS\n    _pool_maxsize = DEFAULT_POOL_MAXSIZE\n    _pool_block = DEFAULT_POOL_BLOCK\n\n    def __init__(self, max_retries=DEFAULT_RETRIES,\n                 pool_connections=DEFAULT_POOL_CONNECTIONS,\n                 pool_maxsize=DEFAULT_POOL_MAXSIZE,\n                 pool_block=DEFAULT_POOL_BLOCK):\n        self.max_retries = max_retries\n        self.config = {}\n        self.proxy_manager = {}\n        super().__init__()\n        self.init_poolmanager(pool_connections, pool_maxsize, block=pool_block)\n\n    def __getstate__(self):\n        return {attr: getattr(self, attr, None) for attr in self.__attrs__}\n\n    def __setstate__(self, state):\n        for attr, value in state.items():\n            setattr(self, attr, value)\n        self.init_poolmanager(\n            self._pool_connections, self._pool_maxsize, block=self._pool_block\n        )\n\n    def init_poolmanager(self, num_pools, maxsize, block=DEFAULT_POOL_BLOCK, **connection_kw):\n        pass\n\n    def proxy_manager_for(self, proxy, **proxy_kwargs):\n        pass\n\n    def cert_verify(self, conn, url, verify, cert):\n        pass\n\n    def build_response(self, req, resp):\n        """Builds a :class:`Response <requests.Response>` object from a urllib3 response."""\n        response = Response()\n        response.status_code = getattr(resp, "status", None)\n        response.headers = CaseInsensitiveDict(getattr(resp, "headers", {{}}))\n        response.encoding = get_encoding_from_headers(response.headers)\n        response.url = req.url\n        return response\n\n    def get_connection(self, url, proxies=None):\n        pass\n\n    def close(self):\n        pass\n\n    def request_url(self, request, proxies):\n        return request.url\n\n    def add_headers(self, request, **kwargs):\n        pass\n\n    def proxy_headers(self, proxy):\n        return {{}}\n\n    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):\n        conn = self.get_connection(request.url, proxies)\n        resp = Response()\n        resp.status_code = 200\n        return resp\n')
    w(WS / "src" / "requests" / "adapters.py", "".join(lines))


def _gen_utils_py_vulnerable() -> None:
    """生成含漏洞版本 get_netrc_auth 的 utils.py（2.32.3 版本，即修复前）。"""
    content = '''\
"""
requests.utils
~~~~~~~~~~~~~~

This module provides utility functions that are used within Requests
that are also useful for external consumption.

:copyright: (c) 2011 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.
"""

from __future__ import annotations

import codecs
import contextlib
import io
import os
import re
import socket
import struct
import sys
import tempfile
import typing
import warnings
from collections import OrderedDict
from http import cookiejar as cookielib
from urllib.parse import (
    quote,
    quote_plus,
    unquote,
    unquote_plus,
    urlparse,
    urlsplit,
    urlunparse,
)
from urllib.request import (
    getproxies,
    getproxies_environment,
    parse_http_list,
    proxy_bypass,
    proxy_bypass_environment,
)

try:
    from collections.abc import Mapping, MutableMapping
except ImportError:
    from collections import Mapping, MutableMapping

# Internal package imports wrapped in try/except for standalone use
try:
    from .structures import CaseInsensitiveDict
except ImportError:
    CaseInsensitiveDict = dict

try:
    from .exceptions import (
        FileModeWarning, InvalidHeader, InvalidProxyURL, InvalidSchema,
        InvalidURL, MissingSchema, UnrewindableBodyError,
    )
except ImportError:
    pass

# This is used to match the port in a URL.
_URI_RE = re.compile(r"^(?:([a-zA-Z][a-zA-Z0-9+\\-.]*):)?(?://([^/?#]*))?([^?#]*)(?:\\?([^#]*))?(?:#(.*))?$")

# This is used for parsing HTTP header charset.
_CLEAN_HEADER_REGEX_BYTE = re.compile(rb"^\s*([^;\s]*)", re.ASCII | re.IGNORECASE)
_CLEAN_HEADER_REGEX_STR = re.compile(r"^\s*([^;\s]*)", re.ASCII | re.IGNORECASE)

_VALID_HEADER_RE = re.compile(r"^[^\\x00-\\x1f\\x7f]*$")

NETRC_FILES = (".netrc", "_netrc")

DEFAULT_CA_BUNDLE_PATH = None
DEFAULT_PORTS = {"http": 80, "https": 443}

# Sentinel
sentinel = object()


def super_len(o):
    total_length = None
    current_position = 0

    if hasattr(o, "__len__"):
        total_length = len(o)

    elif hasattr(o, "len"):
        total_length = o.len

    elif hasattr(o, "fileno"):
        try:
            fileno = o.fileno()
            total_length = os.fstat(fileno).st_size
            if hasattr(o, "tell"):
                current_position = o.tell()
        except (io.UnsupportedOperation, AttributeError):
            pass

    if total_length is None:
        if hasattr(o, "seek") and hasattr(o, "tell"):
            try:
                o.seek(0, 2)
                total_length = o.tell()
                o.seek(current_position, 0)
            except OSError:
                pass

    return total_length


def get_netrc_auth(url, raise_errors=False):
    """Returns the Requests tuple auth for a given url from netrc.

    This function retrieves authentication credentials stored in the user\'s
    ~/.netrc (or ~/_netrc on Windows) file for the given URL.

    .. note::
        This function is used internally to support the ``trust_env``
        parameter on :class:`Session <requests.Session>`.

    .. warning::
        In versions prior to 2.32.4 this function contained a vulnerability
        (CVE-2024-47081) where ``ri.netloc.split(\':\')[0]`` was used instead of
        ``ri.hostname``. A crafted URL such as ``http://example.com:@evil.com/``
        caused credentials for ``example.com`` to be sent to ``evil.com``.
        The root cause function is ``get_netrc_auth`` in ``src/requests/utils.py``.

    :param url: URL to check for netrc credentials.
    :param raise_errors: Whether to raise errors on netrc parse failures.
    :rtype: tuple
    """
    netrc_file = os.environ.get("NETRC")
    netrc_locations = (netrc_file,) if netrc_file else (
        os.path.expanduser(f"~/{f}") for f in NETRC_FILES
    )

    try:
        from netrc import netrc, NetrcParseError

        netrc_path = None
        for netrc_loc in netrc_locations:
            try:
                netrc_path = netrc_loc
                netrc_ = netrc(netrc_loc)
                break
            except FileNotFoundError:
                continue
        else:
            return None

        ri = urlparse(url)
        # VULNERABLE CODE (CVE-2024-47081): using netloc.split(\':\')[0] to extract host
        # This is exploitable via URLs like http://example.com:@evil.com/
        # where netloc is \'example.com:@evil.com\', so split gives \'example.com\'
        # but the actual request goes to evil.com.
        host = ri.netloc.split(":")[0]

        _netrc = netrc_.authenticators(host)
        if _netrc:
            login_i = 0 if _netrc[0] else 1
            return (_netrc[login_i], _netrc[2])

    except (NetrcParseError, OSError):
        if raise_errors:
            raise

    return None


def check_header_validity(header):
    """Verifies that header value is a string which doesn\'t contain
    leading whitespace or return characters. This prevents unintended
    header injection.

    :param header: tuple, in the format (name, value).
    """
    name, value = header
    if isinstance(value, bytes):
        pat = _CLEAN_HEADER_REGEX_BYTE
    else:
        pat = _CLEAN_HEADER_REGEX_STR
    if not pat.match(value) and value:
        raise InvalidHeader(
            f"Invalid header value {value!r} for header {name}"
        )


def dict_to_sequence(d):
    """Returns an internal sequence dictionary update."""
    if hasattr(d, "items"):
        d = list(d.items())
    return d


def dict_from_cookiejar(cj):
    """Returns a key/value dictionary from a CookieJar.

    :param cj: CookieJar object to extract cookies from.
    :rtype: dict
    """
    cookie_dict = {}
    for cookie in cj:
        cookie_dict[cookie.name] = cookie.value
    return cookie_dict


def default_headers():
    """Returns the default HTTP headers used by Requests.

    :rtype: requests.structures.CaseInsensitiveDict
    """
    from .utils import default_user_agent
    return CaseInsensitiveDict(
        {
            "User-Agent": default_user_agent(),
            "Accept-Encoding": ", ".join(
                ("gzip", "deflate", "br", "zstd")
            ),
            "Accept": "*/*",
            "Connection": "keep-alive",
        }
    )


def default_user_agent(name="python-requests"):
    """Return a string representing the default user agent."""
    return f"{name}/{__version__}"


def parse_dict_header(value):
    """Parse lists as described by RFC 2068 Section 2."""
    result = {}
    for item in parse_http_list(value):
        if "=" not in item:
            result[item] = None
            continue
        name, value = item.split("=", 1)
        if value[:1] == value[-1:] == \'"\':
            value = unquote_unreserved(value[1:-1])
        result[name] = value
    return result


def unquote_unreserved(uri):
    """Un-escape any percent-escape sequences in a URI that are unreserved
    characters. This leaves all reserved, illegal and non-ASCII bytes encoded."""
    parts = uri.split("%")
    for i in range(1, len(parts)):
        h = parts[i][0:2]
        if len(h) == 2 and h.isalnum():
            try:
                c = chr(int(h, 16))
            except ValueError:
                raise InvalidURL(f"Invalid percent-escape sequence: {h!r}")
            if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" "abcdefghijklmnopqrstuvwxyz" "0123456789" "-._~":
                parts[i] = c + parts[i][2:]
            else:
                parts[i] = "%" + parts[i]
        else:
            parts[i] = "%" + parts[i]
    return "".join(parts)


def requote_uri(uri):
    """Re-quote the given URI."""
    safe_with_percent = "!#$&\'()*+,/:;=?@[]~"
    safe_without_percent = "!#$&\'()*+,/:;=?@[]~%"
    try:
        return quote(unquote_unreserved(uri), safe=safe_with_percent)
    except InvalidURL:
        return quote(uri, safe=safe_without_percent)


def address_in_network(ip, net):
    """This function allows you to check if an IP belongs to a network subnet."""
    ipaddr = struct.unpack("=L", socket.inet_aton(ip))[0]
    netaddr, bits = net.split("/")
    netmask = struct.unpack("=L", socket.inet_aton(netaddr))[0] & ((2 << int(bits) - 1) - 1)
    network = struct.unpack("=L", socket.inet_aton(netaddr))[0] & netmask
    return (ipaddr & netmask) == (network & netmask)


def is_ipv4_address(string_ip):
    """Returns True if the given string is an IPv4 address."""
    try:
        socket.inet_aton(string_ip)
    except OSError:
        return False
    return True


def is_valid_cidr(string_network):
    """Very simple check of the cidr format in no_proxy variable."""
    if string_network.count("/") == 1:
        try:
            mask = int(string_network.split("/")[1])
        except ValueError:
            return False
        if mask < 1 or mask > 32:
            return False
        try:
            socket.inet_aton(string_network.split("/")[0])
        except OSError:
            return False
    else:
        return False
    return True


def should_bypass_proxies(url, no_proxy):
    """Returns whether we should bypass proxies serving this url."""
    parsed = urlparse(url)

    # Requests to localhost should always bypass proxies.
    if "localhost" in parsed.hostname or parsed.hostname.startswith("127."):
        return True

    # Try to match against a proxy bypass list.
    if no_proxy:
        proxy_urls = [p.strip() for p in no_proxy.split(",") if p.strip()]
        for host in proxy_urls:
            if parsed.hostname.endswith(host) or parsed.hostname == host:
                return True

    return False


def get_environ_proxies(url, no_proxy=None):
    """Return a dict of environment proxies."""
    environ_proxies = getproxies()
    if "no" not in environ_proxies:
        environ_proxies["no"] = no_proxy or ""
    return environ_proxies


def select_proxy(url, proxies):
    """Select a proxy for the url, if applicable."""
    parsed = urlparse(url)
    if proxies:
        for scheme in (parsed.scheme, "all", parsed.scheme + "://"):
            if scheme in proxies:
                return proxies[scheme]
    return None


def set_environ(env_key, value):
    """Set the environment variable \'env_key\' to \'value\'."""
    value_changed = env_key in os.environ
    old_value = os.environ.get(env_key)
    os.environ[env_key] = value
    try:
        yield
    finally:
        if value_changed:
            os.environ[env_key] = old_value
        else:
            os.environ.pop(env_key, None)


def is_py3():
    """Return True if running Python 3."""
    return sys.version_info[0] == 3


def to_key_val_list(value):
    """Take an object and test to see if it can be represented as a
    dictionary. If it can be, return a list of tuples, e.g.,
    ::
        >>> to_key_val_list([("key", "val")])
        [("key", "val")]
        >>> to_key_val_list({"key": "val"})
        [("key", "val")]
        >>> to_key_val_list("string")
        ValueError: cannot encode objects that are not 2-tuples
    :rtype: list
    """
    if value is None:
        return None

    if isinstance(value, (str, bytes, bool, int)):
        raise ValueError("cannot encode objects that are not 2-tuples")

    if isinstance(value, Mapping):
        value = list(value.items())

    return list(value)


def get_encoding_from_headers(headers):
    """Returns the encoding from a given response. Return None if we can\'t determine it."""
    content_type = headers.get("content-type")
    if not content_type:
        return None
    charset = re.search(r"charset=([^;]+)", content_type)
    if charset:
        return charset.group(1).strip()
    return None


def stream_decode_response_unicode(iterator, r):
    """Stream decodes a iterator."""
    if r.encoding is None:
        for item in iterator:
            yield item
        return
    decoder = codecs.getincrementaldecoder(r.encoding)(errors="replace")
    for chunk in iterator:
        rv = decoder.decode(chunk)
        if rv:
            yield rv
    rv = decoder.decode(b"", final=True)
    if rv:
        yield rv


def iter_slices(string, slice_length):
    """Iterate over slices of a string."""
    pos = 0
    if slice_length is None or slice_length <= 0:
        slice_length = len(string)
    while pos < len(string):
        yield string[pos : pos + slice_length]
        pos += slice_length


def get_unicode_from_response(r):
    """Returns the requested content back in unicode."""
    encodings = get_encodings_from_content(r.content)
    if encodings:
        encoding = encodings[0]
        try:
            return str(r.content, encoding)
        except LookupError:
            pass
    return str(r.content, "utf-8", errors="replace")


def get_encodings_from_content(content):
    """Returns encodings from given content string."""
    charset_re = re.compile(r\'<meta.*?charset=["\\\']*(.+?)["\\\']*/?>\', flags=re.I)
    pragma_re = re.compile(r\'<meta.*?content=["\\\']*;?charset=(.+?)["\\\']*/?>\', flags=re.I)
    xml_re = re.compile(r\'<?xml.*?encoding=["\\\']*(.+?)["\\\']*?>\', flags=re.I)
    return (
        charset_re.findall(content)
        + pragma_re.findall(content)
        + xml_re.findall(content)
    )


def prepend_scheme_if_needed(url, new_scheme):
    """Given a URL that may or may not have a scheme, prepend the given scheme.
    Does not replace a present scheme with the one provided as an argument.
    :rtype: str
    """
    parsed = urlparse(url, new_scheme)
    list_parsed = list(parsed)
    if not list_parsed[0]:
        list_parsed[0] = new_scheme
    return urlunparse(list_parsed)


def get_auth_from_url(url):
    """Given a url with authentication components, extract them into a tuple of
    username, password.
    :rtype: (str,str)
    """
    parsed = urlparse(url)
    try:
        auth = (
            unquote(parsed.username or ""),
            unquote(parsed.password or ""),
        )
    except Exception:
        auth = ("", "")
    return auth


def resolve_proxies(request, proxies, trust_env=True):
    """This method takes proxy information from a request and configuration
    input to resolve a mapping of target proxies."""
    proxies = proxies or {}
    url = request.url
    scheme = urlparse(url).scheme
    no_proxy = os.environ.get("NO_PROXY") or os.environ.get("no_proxy") or ""
    new_proxies = {}
    if proxy := proxies.get(scheme):
        new_proxies[scheme] = proxy
    elif trust_env and not should_bypass_proxies(url, no_proxy=no_proxy):
        for env_key, proxy_url in get_environ_proxies(url).items():
            new_proxies[env_key] = proxy_url
    return new_proxies
'''
    w(WS / "src" / "requests" / "utils.py", content)


# ─────────────────────────────────────────────────────────────────────────────
# 3. 测试文件
# ─────────────────────────────────────────────────────────────────────────────
def gen_test_files() -> None:
    # conftest.py
    w(WS / "tests" / "conftest.py", '''\
"""
Shared pytest fixtures and configuration for the requests test suite.

This conftest provides common test utilities including temporary netrc file creation,
mock HTTP server fixtures, and helper functions for security-related testing.
"""
import os
import tempfile
import pytest
from pathlib import Path


@pytest.fixture
def tmp_netrc(tmp_path):
    """Create a temporary .netrc file with test credentials.

    Yields the path to the netrc file and sets NETRC env var.
    Credentials: machine example.com login aaaa password bbbb
    """
    netrc_content = "machine example.com login aaaa password bbbb\\n"
    netrc_file = tmp_path / ".netrc"
    netrc_file.write_text(netrc_content)
    old_env = os.environ.get("NETRC")
    os.environ["NETRC"] = str(netrc_file)
    yield str(netrc_file)
    if old_env is None:
        os.environ.pop("NETRC", None)
    else:
        os.environ["NETRC"] = old_env


@pytest.fixture
def netrc_with_credentials(tmp_path):
    """Create a netrc file with both example.com and evil.com credentials.

    Used for testing URL parsing behaviour in get_netrc_auth.
    """
    netrc_content = (
        "machine example.com login aaaa password bbbb\\n"
        "machine evil.com login evil_user password evil_pass\\n"
    )
    netrc_file = tmp_path / ".netrc"
    netrc_file.write_text(netrc_content)
    old_env = os.environ.get("NETRC")
    os.environ["NETRC"] = str(netrc_file)
    yield str(netrc_file)
    if old_env is None:
        os.environ.pop("NETRC", None)
    else:
        os.environ["NETRC"] = old_env
''')

    # tests/test_utils.py — 原有测试（2.32.3 版本，含真实结构）
    w(WS / "tests" / "test_utils.py", '''\
"""
Test suite for requests/utils.py utility functions.

This module tests URL parsing, header validation, encoding detection,
and authentication helper functions including netrc credential lookup.

Real test cases for CVE-2024-47081 (get_netrc_auth credential leak) are in
tests/test_utils_regression.py.
"""
import os
import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from requests.utils import (
    get_netrc_auth,
    requote_uri,
    get_encoding_from_headers,
    is_ipv4_address,
    is_valid_cidr,
)


class TestGetNetrcAuth:
    """Tests for the get_netrc_auth utility function."""

    def test_works(self, tmp_netrc):
        """Normal case: legitimate URL returns correct credentials from netrc.

        Anchor: assert auth == ("aaaa", "bbbb")
        Source: https://raw.githubusercontent.com/psf/requests/main/tests/test_utils.py
        """
        auth = get_netrc_auth("http://example.com/")
        assert auth == ("aaaa", "bbbb")

    def test_missing_netrc_returns_none(self, tmp_path, monkeypatch):
        """If no netrc file exists, function returns None."""
        monkeypatch.setenv("NETRC", str(tmp_path / "nonexistent_netrc"))
        auth = get_netrc_auth("http://example.com/")
        assert auth is None

    def test_unknown_host_returns_none(self, tmp_netrc):
        """Host not in netrc returns None."""
        auth = get_netrc_auth("http://unknown.example.org/")
        assert auth is None

    def test_https_url(self, tmp_netrc):
        """HTTPS URLs are also supported."""
        auth = get_netrc_auth("https://example.com/path?query=1")
        assert auth == ("aaaa", "bbbb")


class TestRequoteUri:
    """Tests for requote_uri."""

    def test_requote_uri_noop(self):
        assert requote_uri("http://example.com/path") == "http://example.com/path"

    def test_requote_uri_with_percent(self):
        result = requote_uri("http://example.com/path%20with%20spaces")
        assert "example.com" in result


class TestHeaderEncoding:
    """Tests for get_encoding_from_headers."""

    def test_encoding_from_content_type(self):
        headers = {"content-type": "text/html; charset=utf-8"}
        assert get_encoding_from_headers(headers) == "utf-8"

    def test_no_encoding(self):
        headers = {"content-type": "application/json"}
        assert get_encoding_from_headers(headers) is None

    def test_no_content_type(self):
        assert get_encoding_from_headers({}) is None


class TestNetworkUtils:
    """Tests for IP/CIDR utilities."""

    def test_is_ipv4_address_valid(self):
        assert is_ipv4_address("192.168.1.1") is True
        assert is_ipv4_address("0.0.0.0") is True
        assert is_ipv4_address("255.255.255.255") is True

    def test_is_ipv4_address_invalid(self):
        assert is_ipv4_address("192.168.1.256") is False
        assert is_ipv4_address("hostname") is False
        assert is_ipv4_address("") is False

    def test_is_valid_cidr(self):
        assert is_valid_cidr("192.168.0.0/24") is True
        assert is_valid_cidr("10.0.0.0/8") is True

    def test_is_valid_cidr_invalid(self):
        assert is_valid_cidr("192.168.0.0") is False
        assert is_valid_cidr("192.168.0.0/33") is False
''')

    # tests/test_requests.py (abridged but sizable)
    _gen_test_requests_py()

    # tests/test_auth.py
    w(WS / "tests" / "test_auth.py", '''\
"""
Test suite for requests/auth.py authentication handlers.

Tests cover HTTPBasicAuth, HTTPProxyAuth, and HTTPDigestAuth behaviour.
"""
import pytest
import base64
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from requests.auth import HTTPBasicAuth, HTTPProxyAuth, _basic_auth_str


class TestHTTPBasicAuth:
    """Tests for HTTP Basic authentication."""

    def test_basic_auth_str_ascii(self):
        s = _basic_auth_str("user", "pass")
        assert s.startswith("Basic ")
        decoded = base64.b64decode(s[6:]).decode("ascii")
        assert decoded == "user:pass"

    def test_basic_auth_equality(self):
        a = HTTPBasicAuth("alice", "secret")
        b = HTTPBasicAuth("alice", "secret")
        assert a == b

    def test_basic_auth_inequality(self):
        a = HTTPBasicAuth("alice", "secret")
        b = HTTPBasicAuth("bob", "secret")
        assert a != b

    def test_proxy_auth_inherits_basic(self):
        pa = HTTPProxyAuth("user", "pass")
        s = _basic_auth_str("user", "pass")
        assert s.startswith("Basic ")


class TestHTTPBasicAuthEdgeCases:
    """Edge cases for authentication helpers."""

    def test_unicode_username(self):
        s = _basic_auth_str("tëst", "päss")
        assert s.startswith("Basic ")

    def test_empty_password(self):
        a = HTTPBasicAuth("user", "")
        b = HTTPBasicAuth("user", "")
        assert a == b
''')

    # tests/test_hooks.py
    w(WS / "tests" / "test_hooks.py", '''\
"""
Test suite for requests/hooks.py hook dispatching mechanism.

Tests verify that hooks are correctly registered, dispatched, and chained.
"""
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from requests.hooks import default_hooks, dispatch_hook, HOOKS


class TestDefaultHooks:
    def test_hooks_list(self):
        assert "response" in HOOKS

    def test_default_hooks_returns_dict(self):
        h = default_hooks()
        assert isinstance(h, dict)
        assert "response" in h
        assert h["response"] == []


class TestDispatchHook:
    def test_dispatch_no_hooks(self):
        data = {"key": "value"}
        result = dispatch_hook("response", {}, data)
        assert result == data

    def test_dispatch_callable_hook(self):
        called = []
        def my_hook(data, **kwargs):
            called.append(data)
            return {"modified": True}
        result = dispatch_hook("response", {"response": my_hook}, {"original": True})
        assert result == {"modified": True}
        assert len(called) == 1

    def test_dispatch_list_of_hooks(self):
        results = []
        def hook1(data, **kwargs):
            results.append(1)
        def hook2(data, **kwargs):
            results.append(2)
        dispatch_hook("response", {"response": [hook1, hook2]}, "data")
        assert results == [1, 2]
''')

    # tests/test_structures.py
    w(WS / "tests" / "test_structures.py", '''\
"""
Test suite for requests/structures.py data structures.

Tests cover CaseInsensitiveDict and LookupDict behaviour.
"""
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from requests.structures import CaseInsensitiveDict, LookupDict


class TestCaseInsensitiveDict:
    def test_basic_set_get(self):
        d = CaseInsensitiveDict()
        d["Content-Type"] = "application/json"
        assert d["content-type"] == "application/json"
        assert d["CONTENT-TYPE"] == "application/json"

    def test_equality(self):
        d1 = CaseInsensitiveDict({"Accept": "text/html"})
        d2 = CaseInsensitiveDict({"accept": "text/html"})
        assert d1 == d2

    def test_length(self):
        d = CaseInsensitiveDict({"a": 1, "b": 2})
        assert len(d) == 2

    def test_lower_items(self):
        d = CaseInsensitiveDict({"X-Custom": "value"})
        items = dict(d.lower_items())
        assert "x-custom" in items
        assert items["x-custom"] == "value"

    def test_copy(self):
        d = CaseInsensitiveDict({"Key": "val"})
        d2 = d.copy()
        assert d2["key"] == "val"

    def test_delete(self):
        d = CaseInsensitiveDict({"Key": "val"})
        del d["key"]
        assert "Key" not in d


class TestLookupDict:
    def test_lookup_dict(self):
        d = LookupDict(name="test")
        d.ok = 200
        assert d["ok"] == 200
        assert d.get("ok") == 200
        assert d.get("missing") is None

    def test_repr(self):
        d = LookupDict(name="mydict")
        assert "mydict" in repr(d)
''')


def _gen_test_requests_py() -> None:
    """生成大体量 test_requests.py（约 3000 行以撑体量）。"""
    lines = ['''\
"""
Main test suite for the requests library.

This module contains comprehensive integration and unit tests for the requests
HTTP library, covering session management, redirect handling, SSL verification,
proxy configuration, authentication, cookie handling, and content decoding.
"""
import io
import os
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import requests
from requests.models import PreparedRequest, Request, Response
from requests.sessions import Session
from requests.structures import CaseInsensitiveDict
from requests.exceptions import (
    ConnectionError, HTTPError, MissingSchema, InvalidURL, InvalidHeader,
    ChunkedEncodingError, ContentDecodingError, StreamConsumedError,
)


# ─── Fixtures ────────────────────────────────────────────────────────────────
''']
    # Generate ~3000 lines of realistic test structure
    for i in range(1, 120):
        lines.append(f'''

class TestSessionFeature{i:02d}:
    """Tests for session feature area {i:02d}.

    This class covers aspects of the requests library related to session lifecycle,
    header management, request preparation, and response handling in scenario group
    {i:02d}. Tests are grouped here to ensure comprehensive coverage of the HTTP
    client surface area with realistic test cases drawn from common usage patterns.
    """

    def test_basic_scenario_{i:02d}_a(self):
        """Verify basic behaviour of feature {i:02d} scenario A.

        Tests that Session objects are correctly initialised and that header updates
        work as expected for scenario {i:02d} type operations.
        """
        s = Session()
        assert s is not None
        s.headers.update({{"X-Test": "feature-{i:02d}-a", "X-Scenario": "group-{i:02d}"}})
        assert "X-Test" in s.headers
        assert s.headers["X-Scenario"] == "group-{i:02d}"

    def test_basic_scenario_{i:02d}_b(self):
        """Verify basic behaviour of feature {i:02d} scenario B.

        Tests request preparation with correct method preservation and URL handling.
        """
        r = Request(method="GET", url="http://httpbin.org/get")
        p = r.prepare()
        assert p.method == "GET"
        assert "httpbin.org" in p.url

    def test_basic_scenario_{i:02d}_c(self):
        """Edge case for feature {i:02d}.

        Tests Response object creation and status code assignment.
        """
        resp = Response()
        resp.status_code = {200 + (i % 5)}
        assert resp.status_code == {200 + (i % 5)}
        resp.headers = CaseInsensitiveDict({{"Content-Type": "application/json; charset=utf-8"}})
        assert resp.headers["content-type"] == "application/json; charset=utf-8"
        assert resp.headers["CONTENT-TYPE"] == "application/json; charset=utf-8"

    def test_prepared_request_feature_{i:02d}(self):
        """PreparedRequest correctly preserves headers for feature {i:02d}.

        Verifies that PreparedRequest objects correctly handle method, URL, and
        authentication headers for scenario group {i:02d}.
        """
        pr = PreparedRequest()
        pr.prepare_method("POST")
        pr.prepare_url("http://example.com/api/v{i:02d}/resource", {{}})
        pr.prepare_headers({{
            "Authorization": "Bearer token{i:02d}",
            "Content-Type": "application/json",
            "X-Request-ID": "req-{i:02d}-test",
        }})
        assert pr.method == "POST"
        assert "example.com" in pr.url

    def test_session_close_{i:02d}(self):
        """Session closes cleanly for feature {i:02d}.

        Verifies context manager protocol works correctly.
        """
        with Session() as s:
            assert s.headers is not None
            s.headers.update({{"X-Session": "test-{i:02d}"}})
            assert "X-Session" in s.headers

    def test_case_insensitive_headers_{i:02d}(self):
        """CaseInsensitiveDict behaviour for feature {i:02d}.

        Headers should be accessible regardless of case sensitivity.
        """
        headers = CaseInsensitiveDict()
        headers["X-Custom-Header-{i:02d}"] = "value-{i:02d}"
        assert headers["x-custom-header-{i:02d}"] == "value-{i:02d}"
        assert headers["X-CUSTOM-HEADER-{i:02d}"] == "value-{i:02d}"
''')
    w(WS / "tests" / "test_requests.py", "\n".join(lines))


# ─────────────────────────────────────────────────────────────────────────────
# 4. 文档（docs/ + HISTORY.md）
# ─────────────────────────────────────────────────────────────────────────────
def gen_docs() -> None:
    # HISTORY.md — 完整 changelog 摘录（含关键版本）
    w(WS / "HISTORY.md", '''\
# Requests HISTORY

## 2.32.5 (2025-08-18)

**Bugfixes**

- Reverted the SSLContext caching behaviour introduced in 2.32.3 due to compatibility
  issues with certain environments.

**Dependencies**

- Bumped minimum urllib3 requirement.

---

## 2.32.4 (2025-06-10)

**Security**

- Fixed CVE-2024-47081: ``get_netrc_auth`` used ``ri.netloc.split(\':\')[0]`` to
  extract the hostname for netrc lookup. A crafted URL such as
  ``http://example.com:@evil.com/`` would cause credentials for ``example.com``
  to be sent to ``evil.com``. The fix replaces the vulnerable extraction with
  ``ri.hostname``, which is correctly parsed by Python's ``urllib.parse.urlparse``
  and does not include userinfo. Users who cannot upgrade immediately should set
  ``trust_env=False`` on their Session objects as a workaround.

  Credit: Maxime Villard (GHSA-9hjg-9r4m-mvj7, CVE-2024-47081).

---

## 2.32.3 (2024-05-29)

**Bugfixes**

- Fixed SSLContext handling to prevent caching issues with certain versions of
  urllib3. This was not a security fix.

**Dependencies**

- Updated certifi to 2024.2.2.

---

## 2.31.0 (2023-05-22)

**Security**

- Fixed CVE-2023-32681: ``Proxy-Authorization`` headers were inadvertently forwarded
  to destination servers when following redirects through an HTTPS proxy. The fix
  strips the ``Proxy-Authorization`` header when the scheme changes or when a
  non-proxy redirect is encountered.

  This was assigned GHSA-j8r2-6x86-q33q.

**Features**

- Added support for ``trust_env=False`` to disable all environment variable based
  configuration including ``.netrc`` file reading and proxy environment variables.

---

## 2.30.0 (2023-03-08)

**Features**

- Improved streaming response handling performance.
- Added ``PreparedRequest.copy()`` method.

**Bugfixes**

- Fixed content-length header setting for chunked uploads.

---

## 2.29.0 (2023-01-12)

**Bugfixes**

- Fixed an issue with digest auth nonce counting.
- Improved proxy URL parsing to handle edge cases.

---

## 2.28.2 (2023-01-12)

**Bugfixes**

- Fixed urllib3 compatibility issue.

---

## 2.28.0 (2022-06-09)

**Features**

- Added experimental support for the ``airport_fee`` field in TLC integrations
  (internal note: not applicable to requests library itself).

---

## 2.27.0 (2021-12-15)

**Features**

- Python 3.10 compatibility improvements.

---

## 2.26.0 (2021-07-13)

**Improvements**

- Performance improvements for large request bodies.

---

## 2.25.1 (2021-01-02)

**Bugfixes**

- Fixed urllib3 pinning issue.

---

## 2.25.0 (2020-11-11)

**Features**

- Added Brotli content encoding support.

---

## 2.24.0 (2020-06-17)

**Improvements**

- Improved JSON decoding error messages.

---

## 2.23.0 (2020-02-19)

**Features**

- Improved proxy handling for complex network topologies.

---

## 2.22.0 (2019-05-15)

**Features**

- Added support for the ``idna`` package for international domain names.

---

## 2.21.0 (2019-01-22)

**Bugfixes**

- Fixed an edge case in redirect handling.

---

## 2.20.0 (2018-10-18)

**Security**

- Dropped support for Python 2.6, 3.3 which are no longer maintained.
  Avoided importing pyOpenSSL where urllib3 does not offer it.

---

## 2.19.1 (2018-06-14)

**Bugfixes**

- Fixed regression in 2.19.0.
''')

    # docs/user/quickstart.rst
    w(WS / "docs" / "user" / "quickstart.rst", '''\
Quickstart
==========

.. module:: requests.api

Eager to get started? This page gives a good introduction on how to get started
with Requests.

First, make sure that:

* Requests is :ref:`installed <install>`
* Requests is :ref:`up-to-date <updates>`

Let\'s get started with some simple examples.

Make a Request
--------------

Making a request with Requests is very simple.

Begin by importing the Requests module::

    >>> import requests

Now, let\'s try to get a webpage. For this example, let\'s get GitHub\'s public
timeline::

    >>> r = requests.get(\'https://api.github.com/events\')

Now, we have a :class:`Response <requests.Response>` object called ``r``. We can
get all the information we need from this object.

Requests' simple API means that all forms of HTTP request are as obvious. For
example, this is how you make an HTTP POST request::

    >>> r = requests.post(\'https://httpbin.org/post\', data={\'key\': \'value\'})

Nice, right? What about the other HTTP request types: PUT, DELETE, HEAD and
OPTIONS? These are all just as simple::

    >>> r = requests.put(\'https://httpbin.org/put\', data={\'key\': \'value\'})
    >>> r = requests.delete(\'https://httpbin.org/delete\')
    >>> r = requests.head(\'https://httpbin.org/get\')
    >>> r = requests.options(\'https://httpbin.org/get\')

Passing Parameters in URLs
--------------------------

You often want to send some sort of data in the URL\'s query string. If you
were constructing the URL by hand, this data would be given as key/value pairs
in the URL after a question mark, e.g. ``httpbin.org/get?key=val``. Requests
allows you to provide these arguments as a dictionary of strings, using the
``params`` keyword argument::

    >>> payload = {\'key1\': \'value1\', \'key2\': \'value2\'}
    >>> r = requests.get(\'https://httpbin.org/get\', params=payload)

Response Content
----------------

We can read the content of the server\'s response::

    >>> r = requests.get(\'https://api.github.com/events\')
    >>> r.text
    \'[{"repository":{"open_issues":0,"url":"https://github.com/...

Requests will automatically decode content from the server. Most unicode
charsets are seamlessly decoded.

Binary Response Content
-----------------------

You can also access the response body as bytes, for non-text requests::

    >>> r.content
    b\'[{"repository":{"open_issues":0,"url":"https://github.com/...

JSON Response Content
---------------------

There\'s also a built-in JSON decoder, in case you\'re dealing with JSON data::

    >>> r = requests.get(\'https://api.github.com/events\')
    >>> r.json()
    [{"repository": {"open_issues": 0, "url": "https://github.com/...

In case the JSON decoding fails, ``r.json()`` raises an exception. For example,
if the response gets a 204 (No Content), or if the response contains invalid JSON,
attempting ``r.json()`` raises ``requests.exceptions.JSONDecodeError``.
''')

    # docs/user/authentication.rst
    w(WS / "docs" / "user" / "authentication.rst", '''\
Authentication
==============

This document covers various forms of authentication that Requests supports,
including how to use ``.netrc`` files for automatic credential lookup.

Basic Authentication
--------------------

Many web services that require authentication accept HTTP Basic Auth. This is
the simplest kind, and Requests supports it straight out of the box.

Making requests with HTTP Basic Auth is very simple::

    >>> from requests.auth import HTTPBasicAuth
    >>> requests.get(\'https://api.github.com/user\', auth=HTTPBasicAuth(\'user\', \'pass\'))
    <Response [200]>

In fact, HTTP Basic Auth is so common that Requests provides a handy shorthand
for using it::

    >>> requests.get(\'https://api.github.com/user\', auth=(\'user\', \'pass\'))
    <Response [200]>

netrc Authentication
--------------------

Requests supports automatic credential lookup from ``~/.netrc`` (or ``~/_netrc``
on Windows) when ``trust_env=True`` (the default). The lookup is performed by
the ``get_netrc_auth`` function in ``requests.utils``.

**Security Note (CVE-2024-47081):** Versions prior to 2.32.4 contained a
vulnerability in ``get_netrc_auth`` where the hostname extraction used
``ri.netloc.split(\':\')[0]`` instead of ``ri.hostname``. This could cause
credentials to be leaked to an attacker-controlled host via a crafted URL
such as ``http://example.com:@evil.com/``.

**Workaround:** Set ``trust_env=False`` on your Session object to disable
automatic ``.netrc`` lookup::

    >>> import requests
    >>> s = requests.Session()
    >>> s.trust_env = False
    >>> s.get(\'https://example.com/api\')

**Fix:** Upgrade to requests >= 2.32.4.

Digest Authentication
---------------------

Another very popular form of HTTP Authentication is Digest Authentication::

    >>> from requests.auth import HTTPDigestAuth
    >>> url = \'https://httpbin.org/digest-auth/auth/user/pass\'
    >>> requests.get(url, auth=HTTPDigestAuth(\'user\', \'pass\'))
    <Response [200]>

OAuth 1 Authentication
----------------------

Many web APIs use OAuth 1.0 for authentication. The ``requests-oauthlib``
library can be used to achieve this.

OAuth 2 and OpenID Connect Authentication
-----------------------------------------

For OAuth 2.0, the ``requests-oauthlib`` library provides OAuth 2.0 flows.
''')

    # docs/user/advanced.rst
    w(WS / "docs" / "user" / "advanced.rst", '''\
Advanced Usage
==============

This document covers some of the more advanced features of Requests.

Session Objects
---------------

The Session object allows you to persist certain parameters across requests.
It also persists cookies across all requests made from the Session instance,
and will use ``urllib3``\'s `connection pooling
<https://urllib3.readthedocs.io/en/latest/advanced-usage.html#customizing-pool-behavior>`_.
So if you\'re making several requests to the same host, the underlying TCP
connection will be reused, which can result in a significant performance increase
(see `HTTP persistent connection <https://en.wikipedia.org/wiki/HTTP_persistent_connection>`_).

A Session object has all the methods of the main Requests API::

    s = requests.Session()
    s.get(\'https://httpbin.org/cookies/set/sessioncookie/123456789\')
    r = s.get(\'https://httpbin.org/cookies\')
    print(r.text)
    # \'{"cookies": {"sessioncookie": "123456789"}}\'

Sessions can also be used to provide default data to the request methods. This
is done by providing data to the properties on a Session object::

    s = requests.Session()
    s.auth = (\'user\', \'pass\')
    s.headers.update({\'x-test\': \'true\'})

    # both \'x-test\' and \'x-test2\' are sent
    s.get(\'https://httpbin.org/headers\', headers={\'x-test2\': \'true\'})

SSL Certificate Verification
-----------------------------

Requests verifies SSL certificates for HTTPS requests, just like a web browser.
By default, SSL verification is enabled, and Requests will throw a SSLError if
it\'s unable to verify the certificate::

    >>> requests.get(\'https://requestb.in\')
    requests.exceptions.SSLError: hostname \'requestb.in\' doesn\'t match ...

You can pass ``verify`` the path to a CA_BUNDLE file or directory with
certificates of trusted CAs::

    >>> requests.get(\'https://github.com\', verify=\'/path/to/certfile\')

You can also disable SSL verification, though this is strongly discouraged for
production use::

    >>> requests.get(\'https://kennethreitz.org\', verify=False)
    <Response [200]>

trust_env and .netrc
---------------------

By default, Requests will look for ``.netrc`` credentials when making requests.
This behaviour is controlled by the ``trust_env`` parameter on the Session object.

To disable ``.netrc`` lookup (and all other environment-based configuration)::

    s = requests.Session()
    s.trust_env = False

This is the recommended workaround for CVE-2024-47081 if you cannot upgrade to
requests >= 2.32.4 immediately. See also: ``trust_env`` parameter on
:class:`Session <requests.Session>`.

Streaming Uploads
-----------------

With Requests, it\'s possible to send large streams or files without reading
them into memory. To stream and upload, simply provide a file-like object for
your body::

    with open(\'massive-body\', \'rb\') as f:
        requests.post(\'http://some.url/streamed\', data=f)

Timeouts
--------

Most requests to external servers should have a timeout attached, in case the
server is not responding in a timely manner. By default, requests do not time out
unless a timeout value is set explicitly. Without a timeout, your code may hang
for minutes or more::

    >>> requests.get(\'https://github.com\', timeout=0.001)
    Traceback (most recent call last):
        ...
    requests.exceptions.ConnectTimeout: ...
''')

    # docs/api.rst (large API reference)
    api_lines = ['''\
API Reference
=============

Developer Interface
-------------------

This part of the documentation covers all the interfaces of Requests. For parts
where Requests depends on external libraries, we document the most important right
here and provide links to the canonical documentation.

Main Interface
~~~~~~~~~~~~~~

All of Requests' functionality can be accessed by these 7 methods. They all
return an instance of the :class:`Response <Response>` object.

.. autofunction:: requests.request
.. autofunction:: requests.head
.. autofunction:: requests.get
.. autofunction:: requests.post
.. autofunction:: requests.put
.. autofunction:: requests.patch
.. autofunction:: requests.delete

Lower-Level Classes
~~~~~~~~~~~~~~~~~~~

.. autoclass:: requests.Request
    :inherited-members:

.. autoclass:: requests.Response
    :inherited-members:

Request Sessions
~~~~~~~~~~~~~~~~

.. autoclass:: requests.Session
    :inherited-members:

Authentication
~~~~~~~~~~~~~~

.. autoclass:: requests.auth.AuthBase
.. autoclass:: requests.auth.HTTPBasicAuth
.. autoclass:: requests.auth.HTTPDigestAuth
.. autoclass:: requests.auth.HTTPProxyAuth

Exceptions
~~~~~~~~~~

.. autoexception:: requests.exceptions.RequestException
.. autoexception:: requests.exceptions.ConnectionError
.. autoexception:: requests.exceptions.HTTPError
.. autoexception:: requests.exceptions.URLRequired
.. autoexception:: requests.exceptions.TooManyRedirects
.. autoexception:: requests.exceptions.MissingSchema
.. autoexception:: requests.exceptions.InvalidSchema
.. autoexception:: requests.exceptions.InvalidURL
.. autoexception:: requests.exceptions.InvalidHeader
.. autoexception:: requests.exceptions.ChunkedEncodingError
.. autoexception:: requests.exceptions.ContentDecodingError
.. autoexception:: requests.exceptions.StreamConsumedError
.. autoexception:: requests.exceptions.Timeout
.. autoexception:: requests.exceptions.ConnectTimeout
.. autoexception:: requests.exceptions.ReadTimeout
.. autoexception:: requests.exceptions.SSLError
.. autoexception:: requests.exceptions.ProxyError
.. autoexception:: requests.exceptions.JSONDecodeError

Utility Functions
~~~~~~~~~~~~~~~~~

.. autofunction:: requests.utils.get_netrc_auth
.. autofunction:: requests.utils.default_headers
.. autofunction:: requests.utils.get_encoding_from_headers
.. autofunction:: requests.utils.get_unicode_from_response
.. autofunction:: requests.utils.prepend_scheme_if_needed
.. autofunction:: requests.utils.requote_uri
.. autofunction:: requests.utils.resolve_proxies
.. autofunction:: requests.utils.select_proxy
.. autofunction:: requests.utils.is_ipv4_address
.. autofunction:: requests.utils.is_valid_cidr
.. autofunction:: requests.utils.should_bypass_proxies

Structures
~~~~~~~~~~

.. autoclass:: requests.structures.CaseInsensitiveDict

Status Code Lookup
~~~~~~~~~~~~~~~~~~

.. autodata:: requests.codes

''']
    # Pad with more API documentation to reach target token count
    for i in range(1, 40):
        api_lines.append(f'''\
Supplemental Reference (Section {i:02d})
{"~" * 40}

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem {i:02d}. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{{"http": 80,
  "https": 443}}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem {i:02d}
"""""""""""""""""""""""""""""""""""

The subsystem {i:02d} configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.

''')
    w(WS / "docs" / "api.rst", "\n".join(api_lines))

    # docs/CHANGES.rst — RST 格式镜像（大体量）
    w(WS / "docs" / "CHANGES.rst", '''\
Changelog
=========

2.32.4 (2025-06-10)
-------------------

**Security**

- Fixed CVE-2024-47081 (GHSA-9hjg-9r4m-mvj7): Netrc credential leakage via
  crafted URL in ``get_netrc_auth``. The vulnerability used ``ri.netloc.split(\':\')[0]``
  to extract the hostname, allowing a URL like ``http://example.com:@evil.com/`` to
  cause credentials for ``example.com`` to be forwarded to ``evil.com``. Fixed by
  using ``ri.hostname`` instead. Users unable to upgrade should set
  ``trust_env=False`` on their Session as a workaround. (:issue:`6964`, :pr:`6965`)

2.32.3 (2024-05-29)
-------------------

**Bugfixes**

- Fixed SSLContext caching issues with urllib3. (:pr:`6966`)

2.31.0 (2023-05-22)
-------------------

**Security**

- Fixed CVE-2023-32681 (GHSA-j8r2-6x86-q33q): ``Proxy-Authorization`` header
  was inadvertently forwarded to destination servers when following HTTPS proxy
  redirects. Fixed by stripping the header on scheme change. (:pr:`6491`)

**Features**

- Added ``trust_env=False`` to disable all environment-based configuration.

2.30.0 (2023-03-08)
-------------------

**Features**

- Improved streaming response handling.
- Added ``PreparedRequest.copy()`` method.

2.29.0 (2023-01-12)
-------------------

**Bugfixes**

- Fixed digest auth nonce counting edge case.

2.28.2 (2023-01-12)
-------------------

**Bugfixes**

- urllib3 compatibility fix.

2.28.0 (2022-06-09)
-------------------

**Features**

- Python 3.11 compatibility improvements.

2.27.0 (2021-12-15)
-------------------

**Features**

- Python 3.10 compatibility.

2.26.0 (2021-07-13)
-------------------

**Improvements**

- Large request body performance improvements.

2.25.1 (2021-01-02)
-------------------

**Bugfixes**

- urllib3 pinning issue fixed.

2.25.0 (2020-11-11)
-------------------

**Features**

- Brotli content encoding support.

2.24.0 (2020-06-17)
-------------------

**Improvements**

- Improved JSON decoding error messages.

2.23.0 (2020-02-19)
-------------------

**Features**

- Improved proxy handling.

2.22.0 (2019-05-15)
-------------------

**Features**

- ``idna`` package support for international domain names.

2.21.0 (2019-01-22)
-------------------

**Bugfixes**

- Redirect handling edge case fix.

2.20.0 (2018-10-18)
-------------------

**Security**

- Dropped Python 2.6 and 3.3 support.

2.19.1 (2018-06-14)
-------------------

**Bugfixes**

- Fixed regression from 2.19.0.
''')


# ─────────────────────────────────────────────────────────────────────────────
# 5. 分析报告与脚本（合成参考文件）
# ─────────────────────────────────────────────────────────────────────────────
def gen_analysis_files() -> None:
    # SECURITY_CONTEXT.md
    w(WS / "SECURITY_CONTEXT.md", f'''\
# Security Context: CVE-2024-47081 Triage & Remediation

## Summary

This document provides the security engineering context for CVE-2024-47081,
a credential-leakage vulnerability in the psf/requests library affecting all
versions prior to 2.32.4.

## Vulnerability Details

| Field | Value |
|-------|-------|
| CVE ID | {CVE_ID} |
| GHSA ID | {GHSA_ID} |
| CVSS Score | {CVSS_SCORE} (MEDIUM) |
| CVSS Vector | {CVSS_VECTOR} |
| CWE | {CWE_ID} (Insufficiently Protected Credentials) |
| Affected | requests < {AFFECTED_BELOW} |
| Fixed | requests == {FIXED_VERSION} (released 2025-06-10) |
| Workaround | Set ``trust_env=False`` on Session objects |

## Root Cause

The vulnerability resided in the `{ROOT_CAUSE_FUNC}` function in
`src/requests/utils.py`. The vulnerable code used:

```python
host = ri.netloc.split(\':\')[0]
```

to extract the hostname for netrc credential lookup. Python's `urlparse`
sets `netloc` to the network location component of the URL, which includes
userinfo, host, and port. For a URL like `{MALICIOUS_URL}`, `netloc` is
`example.com:@evil.com`, so `netloc.split(\':\')[0]` yields `example.com`.
However, the actual HTTP request targets `evil.com`.

The fix replaces this with `ri.hostname`, which correctly uses Python's
URL parser to return only the hostname portion, stripping userinfo and port.

## Authoritative Sources

- **NVD Detail**: https://nvd.nist.gov/vuln/detail/{CVE_ID}
- **GitHub Issue**: https://github.com/psf/requests/issues/6964
- **Official Fix PR**: https://github.com/psf/requests/pull/6965
  - Commit: `{COMMIT_SHA_PR6965}` (sethmlarson)
- **Alternative PR (superseded)**: https://github.com/psf/requests/pull/6963
  - Commit: `{COMMIT_SHA_PR6963}` (awoimbee)
  - NOTE: PR#6963 was superseded by PR#6965. Do not reference PR#6963 as the
    authoritative fix.

## Related Vulnerability

CVE-2023-32681 (GHSA-j8r2-6x86-q33q): Fixed in requests {CVE_2023_FIXED}.
Proxy-Authorization header was inadvertently forwarded to destination servers
when following HTTPS proxy redirects.

## Internal Impact

Our company's Python services use requests==2.32.3. Services that:
- Use `.netrc` for credential storage AND
- Allow user-controlled or externally-sourced URLs
...are potentially vulnerable to credential exfiltration.

See `analysis/affected_services.json` for the internal service inventory.

## Remediation Plan

1. Apply patch to internal fork (company/requests-patched)
2. Write and pass regression tests
3. Update all internal services to requests >= 2.32.4
4. Short-term workaround: set `trust_env=False` on all Session objects
''')

    # analysis/vuln_report_draft_v1.md
    w(WS / "analysis" / "vuln_report_draft_v1.md", f'''\
# Vulnerability Report Draft v1

## Status: DRAFT — For Internal Review Only

## Executive Summary

A credential-leakage vulnerability (CVE-2024-47081) has been identified in the
psf/requests library. All versions below 2.32.4 are affected. The root cause is
in the `get_netrc_auth` function in `src/requests/utils.py`.

## Technical Analysis

The vulnerable function `get_netrc_auth` uses the following code to extract
the hostname for netrc lookup:

```python
host = ri.netloc.split(\':\')[0]
```

This is exploitable via URLs like `{MALICIOUS_URL}`.

## CVSS Assessment

Based on NVD data:
- Score: {CVSS_SCORE} (MEDIUM)
- Vector: {CVSS_VECTOR}
- CWE: {CWE_ID}

## Fix Options

1. **PR #6965** (sethmlarson) — Official, uses `ri.hostname`
2. **PR #6963** (awoimbee) — Alternative, different implementation

## Status

v1 draft — pending team review.
''')

    # analysis/vuln_report_draft_v2.md (含错误内容，待 supersede)
    w(WS / "analysis" / "vuln_report_draft_v2.md", f'''\
# Vulnerability Report Draft v2

## Status: DRAFT v2 — Contains Error — Pending Supersede

## IMPORTANT CORRECTION NOTICE

This draft v2 contained an error: it incorrectly stated that requests 2.32.3
includes a partial fix for CVE-2024-47081. This is FALSE.
**requests 2.32.3 does NOT contain any fix for CVE-2024-47081.**
The fix was introduced only in requests 2.32.4.

Additionally, this draft incorrectly referenced PR#6963
(commit `{COMMIT_SHA_PR6963}`, author awoimbee) as the official fix.
The correct authoritative fix is PR#6965
(commit `{COMMIT_SHA_PR6965}`, author sethmlarson).

This document is superseded by the authoritative record in `analysis/fix_commit.json`
(after UPDATE-2 is applied).

## Original v2 Content (DO NOT USE — ERRONEOUS)

~~CVE-2024-47081 is partially addressed in requests 2.32.3...~~
~~The fix commit SHA is {COMMIT_SHA_PR6963}...~~

These statements were erroneous and have been retracted via UPDATE-2.
''')

    # analysis/affected_services.json — 内部受影响服务清单
    # AFFECTED_SERVICES_NETRC_COUNT = 3 个使用 netrc 且版本 < 2.32.4 的服务
    wj(WS / "analysis" / "affected_services.json", {
        "inventory_date": "2025-06-05",
        "company": "internal",
        "services": [
            {
                "service_name": "auth-proxy-service",
                "language": "Python",
                "requests_version": "2.32.3",
                "uses_netrc": True,
                "netrc_path": "/etc/secrets/.netrc",
                "vulnerability_status": "VULNERABLE",
                "notes": "Primary candidate for credential leak; processes external URLs from user input"
            },
            {
                "service_name": "data-sync-worker",
                "language": "Python",
                "requests_version": "2.31.0",
                "uses_netrc": True,
                "netrc_path": "~/.netrc",
                "vulnerability_status": "VULNERABLE",
                "notes": "Syncs to partner APIs; netrc used for partner credentials"
            },
            {
                "service_name": "internal-api-client",
                "language": "Python",
                "requests_version": "2.32.3",
                "uses_netrc": True,
                "netrc_path": "/home/svc/.netrc",
                "vulnerability_status": "VULNERABLE",
                "notes": "Internal only but uses trust_env=True by default"
            },
            {
                "service_name": "reporting-exporter",
                "language": "Python",
                "requests_version": "2.32.4",
                "uses_netrc": False,
                "netrc_path": None,
                "vulnerability_status": "NOT_AFFECTED",
                "notes": "Already on fixed version and does not use netrc"
            },
            {
                "service_name": "webhook-receiver",
                "language": "Python",
                "requests_version": "2.28.2",
                "uses_netrc": False,
                "netrc_path": None,
                "vulnerability_status": "VULNERABLE_BUT_NO_NETRC",
                "notes": "Old version but does not use netrc; lower risk"
            },
            {
                "service_name": "notification-sender",
                "language": "Go",
                "requests_version": None,
                "uses_netrc": False,
                "netrc_path": None,
                "vulnerability_status": "NOT_AFFECTED",
                "notes": "Go service, does not use Python requests"
            }
        ],
        "summary": {
            "total_services": 6,
            "python_services": 5,
            "using_netrc_below_2324": 3,
            "remediation_priority": "HIGH"
        }
    })

    # analysis/fix_comparison.md
    w(WS / "analysis" / "fix_comparison.md", f'''\
# Fix Comparison: PR#6963 vs PR#6965

## Background

Two pull requests were submitted to fix CVE-2024-47081:

- **PR#6963** (awoimbee, commit `{COMMIT_SHA_PR6963}`)
- **PR#6965** (sethmlarson, commit `{COMMIT_SHA_PR6965}`) ← **OFFICIAL FIX**

## PR#6963 (Superseded)

- Author: awoimbee
- Commit: `{COMMIT_SHA_PR6963}`
- Approach: More complex URL parsing with additional userinfo stripping
- Status: **SUPERSEDED** by PR#6965
- Review notes: sigmavirus24 noted this approach was more complex than necessary

## PR#6965 (Official)

- Author: sethmlarson
- Commit: `{COMMIT_SHA_PR6965}`
- Approach: Simple replacement of `ri.netloc.split(\':\')[0]` with `ri.hostname`
- GHSA: `{GHSA_ID}`
- Status: **MERGED — OFFICIAL FIX**
- Review notes: Cleaner approach using Python's built-in hostname parsing

## Recommendation

Always reference PR#6965 and commit `{COMMIT_SHA_PR6965}` as the authoritative fix.
PR#6963 and commit `{COMMIT_SHA_PR6963}` are obsolete and should not be cited in
security documentation.

## Technical Difference

```diff
# Before (vulnerable):
- host = ri.netloc.split(\':\')[0]

# After (PR#6965 fix):
+ host = ri.hostname
+ if host is None:
+     return None
```

The `ri.hostname` attribute correctly handles all URL forms including those with
userinfo components (`user@host` syntax), returning only the hostname without
port or userinfo.
''')

    # sessions/ JSON files (多渠道 session 历史文档，large)
    _gen_session_history_docs()

    # scripts/check_version.py
    w(WS / "scripts" / "check_version.py", f'''\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check whether the installed requests version is affected by CVE-2024-47081."""
import sys
import pkg_resources


def check():
    try:
        version = pkg_resources.get_distribution("requests").version
        parts = version.split(".")
        major, minor, patch_ = int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0
        is_affected = (major == 2 and minor == 32 and patch_ < 4) or (major == 2 and minor < 32)
        if is_affected:
            print(f"[AFFECTED] requests=={{version}} is vulnerable to CVE-2024-47081")
            print(f"  Affected range: < 2.32.4")
            print(f"  Fixed version: 2.32.4")
            print(f"  Workaround: set trust_env=False on Session objects")
            sys.exit(1)
        else:
            print(f"[OK] requests=={{version}} is not affected by CVE-2024-47081")
            sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Could not determine requests version: {{e}}")
        sys.exit(2)


if __name__ == "__main__":
    check()
''')

    # scripts/run_regression.sh
    w(WS / "scripts" / "run_regression.sh", '''\
#!/usr/bin/env bash
# Run the CVE-2024-47081 regression test suite.
# Usage: ./scripts/run_regression.sh [--verbose]

set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_FILE="${WORKSPACE_DIR}/tests/test_utils_regression.py"
RESULTS_DIR="${WORKSPACE_DIR}/test_results"

mkdir -p "${RESULTS_DIR}"

if [ ! -f "${TEST_FILE}" ]; then
    echo "ERROR: Regression test file not found: ${TEST_FILE}" >&2
    exit 1
fi

echo "Running CVE-2024-47081 regression tests..."
python -m pytest "${TEST_FILE}" -v --tb=short 2>&1 | tee "${RESULTS_DIR}/regression_run.txt"

EXIT_CODE=${PIPESTATUS[0]}

if [ ${EXIT_CODE} -eq 0 ]; then
    echo "All regression tests PASSED."
else
    echo "Some regression tests FAILED. See ${RESULTS_DIR}/regression_run.txt"
fi

exit ${EXIT_CODE}
''')

    # pyproject.toml
    w(WS / "pyproject.toml", f'''\
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "requests-patched"
version = "2.32.3.post1"
description = "Company internal fork of psf/requests with CVE-2024-47081 patch"
requires-python = ">=3.8"
dependencies = [
    "certifi>=2017.4.17",
    "charset-normalizer>=2,<4",
    "idna>=2.5,<4",
    "urllib3>=1.21.1,<3",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov",
    "requests-mock",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"

[tool.security]
cve_tracked = ["{CVE_ID}", "CVE-2023-32681"]
patch_status = "in-progress"
fixed_upstream_version = "{FIXED_VERSION}"
''')


# ─────────────────────────────────────────────────────────────────────────────
# 6. Sessions（主 + 5 history）
# ─────────────────────────────────────────────────────────────────────────────
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack = gen_session_id("slack_security_alerts", TID)
    s_feishu = gen_session_id("feishu_dm_bob", TID)
    s_email1 = gen_session_id("email_ext_disclosure", TID)
    s_email2 = gen_session_id("email_internal_response", TID)
    s_github = gen_session_id("github_pr_comments", TID)

    # ─── 主 session ────────────────────────────────────────────────────────
    sb = SessionBuilder(main_id, CWD, "2026-03-09T01:00:00", is_main=True)
    sb.add_user(
        f"You are SecOps AI, the security engineering assistant for Alice (Security Lead). "
        f"Our Python services use psf/requests version-pinned to 2.32.3. We have received "
        f"an external disclosure: CVE-2024-47081 affects requests < 2.32.4. Your task chain:\n\n"
        f"1. Identify the root cause function in our source at `src/requests/utils.py`.\n"
        f"2. Write regression tests, then apply the official fix.\n"
        f"3. Produce analysis reports and a security advisory.\n\n"
        f"**House preferences (apply throughout, even when not restated):**\n"
        f"- P1: All JSON output files must use snake_case field names (no camelCase).\n"
        f"- P2: Changelog and release note entries must follow HISTORY.md RST style "
        f"(`**Security**`/`**Bugfixes**` headers, RST bullet list format).\n"
        f"- P3: Python test files must begin with a module-level docstring (triple-quoted "
        f"string immediately after any shebang/encoding lines) describing test purpose.\n"
        f"- P4: Security advisory documents must include a `## Workaround` section "
        f"placed after `## Fix`.\n\n"
        f"Authoritative sources:\n"
        f"- NVD: https://nvd.nist.gov/vuln/detail/{CVE_ID} (CVSS 5.3, CWE-522)\n"
        f"- Official fix: https://github.com/psf/requests/pull/6965 "
        f"(commit {COMMIT_SHA_PR6965}, sethmlarson)\n"
        f"- GHSA: {GHSA_ID}\n\n"
        f"History sessions available: Slack #security-alerts, Feishu DM with Bob, "
        f"email threads, GitHub PR comments. "
        f"Slack bot summaries are NOT authoritative — always verify against primary sources.\n\n"
        f"Start by reading SOUL.md and AGENTS.md, then await the first task."
    )
    sb.add_assistant(
        f"Understood. Reading SOUL.md and AGENTS.md now.\n\n"
        f"Working framework:\n"
        f"1. Primary sources for CVE data: NVD ({CVE_ID}), GitHub PR #6965 ({GHSA_ID}).\n"
        f"2. Slack bot summaries and draft emails may contain errors — always verify.\n"
        f"3. All JSON deliverables use snake_case (P1). Test files include module docstrings (P3).\n"
        f"4. Changelog follows HISTORY.md RST style (P2). Security docs include ## Workaround (P4).\n\n"
        f"Ready for Task 1."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # ─── Slack #security-alerts（含 V5 失真 bot 摘要）─────────────────────
    append_history(
        SESS / f"{s_slack}.jsonl", s_slack, CWD, "2026-03-04T09:00:00",
        [
            (
                "[Slack #security-alerts alice Mon Mar 04 09:00 UTC 2026] "
                "@channel URGENT: External researcher disclosed CVE-2024-47081 today. "
                "Affects psf/requests < 2.32.4. Root cause is in the netrc credential "
                "lookup path. Carol please do internal impact assessment. Bot will auto-summarise.",
                "Acknowledged. I've noted the CVE disclosure. Carol is on impact assessment. "
                "I will verify the root cause details against the primary sources before "
                "taking action."
            ),
            (
                "[Slack #security-alerts BOT_SUMMARY Mon Mar 04 09:01 UTC 2026] "
                "🤖 AUTO-SUMMARY (not authoritative): CVE-2024-47081 — "
                "Root cause: `build_response` function in requests/adapters.py. "
                "CVSS: 6.1 (MEDIUM). Affected: requests < 2.32.3. "
                "Fix: upgrade to 2.32.3 or later. "
                "(This summary is auto-generated and may contain errors.)",
                "⚠️ CAUTION: The bot summary contains errors. "
                "The root cause is NOT `build_response` in `adapters.py`. "
                "Per the NVD and PR #6965, the root cause is `get_netrc_auth` in `utils.py`. "
                "CVSS is 5.3 (not 6.1). Affected range is < 2.32.4 (not < 2.32.3). "
                "I will use the authoritative sources only."
            ),
            (
                "[Slack #security-alerts carol Mon Mar 04 10:30 UTC 2026] "
                "Bob mentioned on a call that he thinks the affected range is requests < 2.32.3 "
                "based on the bot summary. Should I use that for the impact assessment?",
                "No — the bot summary is incorrect. "
                "Per NVD (https://nvd.nist.gov/vuln/detail/CVE-2024-47081), the affected range "
                "is requests < 2.32.4. Use 2.32.4 as the threshold for the internal impact "
                "assessment. The bot's '< 2.32.3' figure is wrong."
            ),
            (
                "[Slack #security-alerts alice Mon Mar 04 11:00 UTC 2026] "
                "Confirmed — NVD says < 2.32.4. Carol please use that. "
                "Also EPSS is 19.57% per Miggo's CVE database, not the bot's figure.",
                "Recorded: affected range < 2.32.4, EPSS 19.57% (source: Miggo). "
                "Using these for all deliverables."
            ),
        ]
    )

    # ─── Feishu DM with Bob（含 V6 红鲱鱼：Bob 推荐 PR#6963）───────────────
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2026-03-05T10:00:00",
        [
            (
                "[Feishu DM bob → agent Tue Mar 05 10:00 UTC 2026] "
                "Hey, I looked at the two PRs. I think we should use PR#6963 from awoimbee — "
                "commit SHA 5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b. "
                "It was merged first and does a more thorough URL parse. "
                "Also I think the fix is just removing the userinfo from netloc, "
                "not switching to ri.hostname.",
                "Hi Bob, thanks for looking into this. "
                "I need to check the PR history carefully. "
                "From the GitHub repository, PR#6965 (sethmlarson) is the one officially "
                "merged and referenced in the GHSA advisory GHSA-9hjg-9r4m-mvj7 and "
                "in HISTORY.md (2.32.4 release). "
                "PR#6963 (awoimbee, commit 5b4b64c3...) was an earlier alternative that "
                "was superseded by PR#6965. "
                "I'll use PR#6965 as the authoritative fix. "
                "The correct change is `ri.netloc.split(':')[0]` → `ri.hostname`."
            ),
            (
                "[Feishu DM bob → agent Tue Mar 05 10:15 UTC 2026] "
                "Hmm, ok. But I still think for the fix comparison doc you should mention "
                "both. Also, for the regression test, the test name should be something like "
                "`test_cve_2024_47081_vuln_check` — that's what I see in some internal docs.",
                "I'll mention both PRs in `analysis/fix_comparison.md` with a clear note that "
                "PR#6963 is superseded. However, for the official fix record I'll use "
                "PR#6965 only. "
                "Regarding the test name: the authoritative source (PR#6965 test file at "
                "https://raw.githubusercontent.com/psf/requests/main/tests/test_utils.py) "
                "uses `test_not_vulnerable_to_bad_url_parsing` for the vulnerability test. "
                "I'll follow the official naming in our regression file and name the method "
                "`test_cve_2024_47081_credential_leak` for clarity in our internal test."
            ),
        ]
    )

    # ─── Email 1: 外部研究员披露通知────────────────────────────────────────
    append_history(
        SESS / f"{s_email1}.jsonl", s_email1, CWD, "2026-03-03T16:00:00",
        [
            (
                "[Email researcher@secfirm.example → alice@company.example "
                "Mon Mar 03 16:00 UTC 2026] "
                "Subject: Responsible Disclosure — CVE-2024-47081 in psf/requests\n\n"
                "Hello Alice,\n\n"
                "We have identified a credential-leakage vulnerability in psf/requests. "
                "All versions below 2.32.4 are affected.\n\n"
                "Root cause: `get_netrc_auth` in `requests/utils.py` uses "
                "`ri.netloc.split(':')[0]` to extract the hostname for .netrc lookup. "
                "This allows a crafted URL like `http://example.com:@evil.com/` to leak "
                "credentials stored for `example.com` to `evil.com`.\n\n"
                "Proof of Concept:\n"
                "  import netrc, os, tempfile\n"
                "  from urllib.parse import urlparse\n"
                "  ri = urlparse('http://example.com:@evil.com/')\n"
                "  host = ri.netloc.split(':')[0]  # Returns 'example.com' NOT 'evil.com'\n"
                "  # But the HTTP request goes to evil.com\n\n"
                "CVSS: 5.3 (MEDIUM) — CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N\n"
                "CWE: CWE-522\n\n"
                "The official fix is in PR#6965 (sethmlarson). "
                "GHSA: GHSA-9hjg-9r4m-mvj7.\n\n"
                "Regards,\nExternal Security Researcher",
                "Acknowledged. Key facts extracted:\n"
                "- Root cause: `get_netrc_auth`, vulnerable code: `ri.netloc.split(':')[0]`\n"
                "- Affected: < 2.32.4\n"
                "- CVSS: 5.3, CWE-522\n"
                "- Fix: PR#6965, GHSA-9hjg-9r4m-mvj7\n"
                "These match NVD. Proceeding with triage."
            ),
        ]
    )

    # ─── Email 2: Alice 内部响应（含错误建议，为 supersede 铺垫）────────────
    append_history(
        SESS / f"{s_email2}.jsonl", s_email2, CWD, "2026-03-04T08:00:00",
        [
            (
                "[Email alice@company.example → engineering@company.example "
                "Tue Mar 04 08:00 UTC 2026] "
                "Subject: [ACTION REQUIRED] CVE-2024-47081 — Internal Response Plan\n\n"
                "Team,\n\n"
                "External disclosure confirmed. Action items:\n\n"
                "1. Short-term workaround: set trust_env=False on all Session objects.\n"
                "2. Long-term: upgrade to requests >= 2.32.4.\n\n"
                "NOTE: For the official fix record in our internal security docs, "
                "please use the commit SHA from PR#6963 "
                "(5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b). "
                "[EDITOR'S NOTE: THIS IS AN ERROR — see UPDATE-2 for correction]\n\n"
                "Also: requests 2.32.3 contains a partial mitigation — "
                "it added some URL validation that reduces (but does not eliminate) the risk. "
                "[EDITOR'S NOTE: THIS IS ALSO AN ERROR — 2.32.3 has NO fix for this CVE]\n\n"
                "Alice",
                "Noted with caution. Alice's email contains two errors that will be "
                "corrected via UPDATE-2:\n"
                "1. The commit SHA should be PR#6965's SHA (57acb7c...), not PR#6963's.\n"
                "2. requests 2.32.3 has NO fix for CVE-2024-47081.\n"
                "Following explicit instructions for now (Q9), and will revise on UPDATE-2."
            ),
        ]
    )

    # ─── GitHub PR comments session ─────────────────────────────────────────
    append_history(
        SESS / f"{s_github}.jsonl", s_github, CWD, "2026-03-04T12:00:00",
        [
            (
                "[GitHub psf/requests PR#6963 comment awoimbee Mon Mar 04 12:00 UTC 2026] "
                "This PR fixes CVE-2024-47081 by parsing the URL more carefully and "
                "stripping userinfo from netloc before passing to netrc. "
                "The key commit is 5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b.",
                "Noted: PR#6963 (awoimbee) commit 5b4b64c3... is the alternative fix approach."
            ),
            (
                "[GitHub psf/requests PR#6963 comment sigmavirus24 Mon Mar 04 14:00 UTC 2026] "
                "The approach in this PR is more complex than necessary. PR#6965 uses "
                "`ri.hostname` which is cleaner. I prefer #6965.",
                "Noted: sigmavirus24 prefers PR#6965's approach. PR#6963 was reviewed but "
                "the community favoured the simpler ri.hostname approach."
            ),
            (
                "[GitHub psf/requests PR#6965 comment sethmlarson Mon Mar 04 15:30 UTC 2026] "
                "This is the minimal correct fix: replace `ri.netloc.split(':')[0]` with "
                "`ri.hostname` and add a None check. GHSA-9hjg-9r4m-mvj7. "
                "Merge commit: 57acb7c26d809cf864ec439b8bcd6364702022d5.",
                "Confirmed: PR#6965 (sethmlarson) commit 57acb7c2... is the official fix. "
                "GHSA-9hjg-9r4m-mvj7. This is the authoritative source."
            ),
        ]
    )

    return {
        "main": main_id,
        "history": [
            (s_slack, "slack"),
            (s_feishu, "feishu"),
            (s_email1, "email"),
            (s_email2, "email"),
            (s_github, "im"),
        ],
    }


# ─────────────────────────────────────────────────────────────────────────────
# 7. Updates（UPDATE-1 + UPDATE-2 含 supersede）
# ─────────────────────────────────────────────────────────────────────────────
def gen_updates(sess_ids: dict) -> dict:
    s_email2_id = sess_ids["history"][3][0]   # email_internal_response

    # ── UPDATE-1（Q8 前：新增 CVE-2023-32681 核查任务 + Alice 错误指定 commit）───
    u1_dir = UPD / "upd1"

    # 新的 email 线程（追加到 email_internal_response 会话）
    _write_update1_sessions(u1_dir, s_email2_id)

    # 新增 Slack 频道消息（片段）
    _write_update1_slack_doc(u1_dir)

    # CVE-2023-32681 NVD 快照文档
    _write_cvss_2023_doc(u1_dir)

    # ── UPDATE-2（Q11 前，supersede）───────────────────────────────────────
    u2_dir = UPD / "upd2"

    # 勘误 Slack 消息 + 勘误邮件 + PR#6965 review 快照
    _write_update2_sessions(u2_dir, sess_ids)
    _write_pr6965_review_snapshot(u2_dir)

    updates_decl = {
        "upd1_email": {
            "type": "session", "dir": f"updates/{TID}/upd1",
            "files": [
                {
                    "name": f"{s_email2_id}_ext.jsonl",
                    "action": "append",
                    "target": f"{s_email2_id}.jsonl",
                }
            ]
        },
        "upd1_workspace": {
            "type": "workspace", "dir": f"updates/{TID}/upd1",
            "files": [
                {"name": "cve_2023_32681_nvd_snapshot.md", "action": "new",
                 "target": "analysis/cve_2023_32681_nvd_snapshot.md"},
                {"name": "slack_update1_messages.md", "action": "new",
                 "target": "sessions/slack_update1_messages.md"},
            ]
        },
        "upd2_workspace": {
            "type": "workspace", "dir": f"updates/{TID}/upd2",
            "files": [
                {"name": "pr6965_review_snapshot.md", "action": "new",
                 "target": "analysis/pr6965_review_snapshot.md"},
                {"name": "erratum_email.md", "action": "new",
                 "target": "sessions/erratum_email.md"},
                {"name": "erratum_slack.md", "action": "new",
                 "target": "sessions/erratum_slack.md"},
            ]
        },
    }
    return updates_decl


def _append_segment(session_id: str, start_iso: str, turns) -> str:
    sb = SessionBuilder(session_id, CWD, start_iso, is_main=False)
    sb.add_turns(turns)
    msg_lines = [ln for ln in sb.lines if ln.get("type") == "message"]
    return "\n".join(json.dumps(ln, ensure_ascii=False) for ln in msg_lines) + "\n"


def _write_update1_sessions(u1_dir: Path, email2_id: str) -> None:
    """Update-1 追加到 email_internal_response session 的新消息。"""
    seg = _append_segment(
        email2_id, "2026-03-06T14:00:00",
        [
            (
                "[Email alice@company.example → engineering@company.example "
                "Thu Mar 06 14:00 UTC 2026] "
                "Subject: Additional Task — CVE-2023-32681 Review\n\n"
                "Team,\n\n"
                "Security team also wants us to verify our remediation status for "
                "CVE-2023-32681, which was fixed in requests 2.31.0. "
                "Please produce a summary JSON at `analysis/cve_2023_32681_summary.json`. "
                "Confirm: (1) cve_id, (2) fixed_version, (3) root_cause involving "
                "Proxy-Authorization header forwarding.\n\n"
                "Also, for the CVE-2024-47081 fix commit record, use "
                "commit SHA 5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b (PR#6963). "
                "Write this to `analysis/fix_commit.json`.\n\n"
                "Alice",
                "Noted. Two tasks from Update-1:\n"
                "1. Produce `analysis/cve_2023_32681_summary.json`.\n"
                "2. Write `analysis/fix_commit.json` with commit SHA 5b4b64c3... "
                "(as explicitly instructed — to be revised if superseded).\n"
                "I will follow these explicit instructions while flagging that "
                "the authoritative PR#6965 SHA is different."
            ),
        ]
    )
    (u1_dir / f"{email2_id}_ext.jsonl").parent.mkdir(parents=True, exist_ok=True)
    (u1_dir / f"{email2_id}_ext.jsonl").write_text(seg, encoding="utf-8")


def _write_update1_slack_doc(u1_dir: Path) -> None:
    """Update-1 Slack 频道消息快照（workspace 新增文档）。"""
    content = f"""\
# Slack #security-alerts — Update-1 Messages (2026-03-06)

The following messages were posted to #security-alerts following the initial CVE triage.

---

**[alice 2026-03-06 09:00 UTC]**
Additional task: please also verify our CVE-2023-32681 status. That CVE was
fixed in requests 2.31.0 and involved Proxy-Authorization header forwarding.
We need a formal record.

**[carol 2026-03-06 09:20 UTC]**
On it. I'm also checking whether any internal services are on requests < 2.31.0
(they would be double-affected). Found 0 such services — all are on >= 2.31.0.

**[bob 2026-03-06 10:00 UTC]**
For CVE-2023-32681: I confirmed the root cause was that the Proxy-Authorization
header was being forwarded to the destination server when redirecting through an
HTTPS proxy. Fixed in requests 2.31.0.

**[alice 2026-03-06 11:00 UTC]**
Good. Please write up the formal summary. Also confirming the fix commit for
CVE-2024-47081: use the commit from PR#6963 for now as I mentioned in my email.
[NOTE: This will be corrected in Update-2.]

---

*This document is part of Update-1 and provides supplemental Slack history.*
"""
    (u1_dir / "slack_update1_messages.md").parent.mkdir(parents=True, exist_ok=True)
    (u1_dir / "slack_update1_messages.md").write_text(content, encoding="utf-8")


def _write_cvss_2023_doc(u1_dir: Path) -> None:
    """CVE-2023-32681 NVD 快照文档（大体量，~8k tokens 目标）。"""
    lines = [f"""\
# CVE-2023-32681 — NVD Snapshot (Update-1 Workspace)

Source: https://nvd.nist.gov/vuln/detail/CVE-2023-32681
Fetched: 2026-03-06

## Summary

**CVE-2023-32681** is a security vulnerability in the psf/requests library affecting
versions prior to 2.31.0. The vulnerability causes `Proxy-Authorization` headers to be
inadvertently forwarded to destination servers when following redirects from HTTPS proxies.

## Details

| Field | Value |
|-------|-------|
| CVE ID | CVE-2023-32681 |
| GHSA | GHSA-j8r2-6x86-q33q |
| Affected | requests < 2.31.0 |
| Fixed | requests 2.31.0 (released 2023-05-22) |
| CWE | CWE-601 (URL Redirection to Untrusted Site) |
| CVSS Score | 6.1 (MEDIUM) |
| CVSS Vector | CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:N/A:N |

## Root Cause

When using an HTTPS proxy, the `Proxy-Authorization` header was included in the
initial CONNECT request but was also forwarded to the destination server in subsequent
requests after the tunnel was established. This could expose proxy credentials to the
destination server.

The fix in requests 2.31.0 strips the `Proxy-Authorization` header when the request
scheme changes or when a redirect would forward to a non-proxy destination.

## Affected Code

The vulnerability was in the redirect handling logic in `requests/sessions.py`.
The fix ensured that `Proxy-Authorization` headers are cleared before following
redirects in certain configurations.

## Internal Impact Assessment

| Service | requests version | uses_proxy_auth | Risk |
|---------|-----------------|-----------------|------|
| auth-proxy-service | 2.32.3 | No | Not Affected (CVE-2023-32681) |
| data-sync-worker | 2.31.0 | No | Patched |
| internal-api-client | 2.32.3 | No | Not Affected (CVE-2023-32681) |
| reporting-exporter | 2.32.4 | No | Not Affected |
| webhook-receiver | 2.28.2 | No | Patched (>= 2.31.0 for this CVE) |

Wait — webhook-receiver uses 2.28.2 which is < 2.31.0. However, it does not use
proxy authentication, so the practical risk is lower. It should still be upgraded.

## References

1. NVD Detail: https://nvd.nist.gov/vuln/detail/CVE-2023-32681
2. GHSA: https://github.com/advisories/GHSA-j8r2-6x86-q33q
3. requests HISTORY.md (2.31.0 entry)
4. Fix PR: https://github.com/psf/requests/pull/6491

"""]
    # Pad to reach ~8k tokens
    for i in range(1, 100):
        lines.append(f"""\
## Extended Analysis Section {i:02d}

This section provides supplemental context for CVE-2023-32681 remediation.

### Scenario {i:02d}: Proxy Configuration Analysis

When an HTTP proxy is configured via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`),
requests uses the proxy for all HTTP/HTTPS traffic. For HTTPS, the proxy uses the CONNECT
method to establish a tunnel. The vulnerability occurred because the library incorrectly
included the `Proxy-Authorization` header in requests sent through the tunnel.

Example vulnerable configuration:
```python
import requests
proxies = {{
    'https': 'https://proxy-user:proxy-pass@corporate-proxy.example.com:8080',
}}
response = requests.get('https://target.example.com/api', proxies=proxies)
# In vulnerable versions: target.example.com receives Proxy-Authorization header
```

### Verification {i:02d}: Confirming the Fix

After upgrading to requests >= 2.31.0, the Proxy-Authorization header is correctly
stripped before forwarding to the destination. This can be verified by:

1. Checking the requests version: `import requests; print(requests.__version__)`
2. Inspecting the outgoing headers in a test environment
3. Running the requests test suite which includes regression tests for this behaviour

### CVE-2023-32681 Impact Analysis for Service Category {i:02d}

Services that connect through HTTPS proxies with Proxy-Authorization credentials are
most at risk. For each service, teams should verify:

- Whether proxy authentication is used (check `HTTPS_PROXY` env variable format)
- Whether the service processes redirects (default: yes for requests.get/post)
- Whether the proxy server is under full control of the company

### Remediation Steps for Category {i:02d}

1. Identify all Python services using requests < 2.31.0
2. Upgrade to requests >= 2.31.0 (or >= 2.32.4 to also fix CVE-2024-47081)
3. If immediate upgrade is not possible, review proxy configuration
4. Consider adding request logging to detect unexpected Proxy-Authorization forwarding

### Notes {i:02d}

- Services not using proxy authentication are not affected by this specific CVE.
- The fix in 2.31.0 introduced `trust_env=False` as a broad workaround option.
- Companies using corporate proxies with authentication should prioritise this upgrade.
- The GHSA for CVE-2023-32681 is GHSA-j8r2-6x86-q33q.
- Fixed version: 2.31.0 (released 2023-05-22).

""")
    (u1_dir / "cve_2023_32681_nvd_snapshot.md").write_text("\n".join(lines), encoding="utf-8")


def _write_update2_sessions(u2_dir: Path, sess_ids: dict) -> None:
    """Update-2 勘误邮件和 Slack 消息（workspace 新增文档）。"""
    erratum_email = f"""\
# Erratum Email — Update-2 (2026-03-10)

From: alice@company.example
To: engineering@company.example
Subject: CORRECTION: CVE-2024-47081 Fix Commit SHA & Version Clarification

Team,

I need to correct two errors from my previous email (2026-03-06):

## Correction 1: Fix Commit SHA

My previous email incorrectly instructed you to record PR#6963's commit SHA
(`5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b`) as the authoritative fix.

**This was wrong. Please update `analysis/fix_commit.json` immediately.**

The correct authoritative fix is **PR#6965** (by sethmlarson):
- Commit SHA: `{COMMIT_SHA_PR6965}`
- GHSA: `{GHSA_ID}`
- PR: https://github.com/psf/requests/pull/6965

PR#6963 (awoimbee) was an earlier alternative that was **superseded** by PR#6965.
The updated `fix_commit.json` must reflect this supersede with:
- `commit_sha`: `{COMMIT_SHA_PR6965}`
- `supersedes_pr`: `"6963"`
- `authoritative_pr`: `"6965"`

## Correction 2: requests 2.32.3 Partial Fix Claim

My previous email also incorrectly stated that requests 2.32.3 contains a
partial mitigation for CVE-2024-47081. **This is false.**

requests 2.32.3 does NOT contain any fix for CVE-2024-47081.
The fix was introduced only in 2.32.4 (released 2025-06-10).
The 2.32.3 change was an unrelated SSLContext fix.

Please disregard the earlier "partial mitigation" claim entirely.

Apologies for the confusion.

Alice
"""
    (u2_dir / "erratum_email.md").parent.mkdir(parents=True, exist_ok=True)
    (u2_dir / "erratum_email.md").write_text(erratum_email, encoding="utf-8")

    erratum_slack = f"""\
# Slack #security-alerts — Erratum Messages (Update-2, 2026-03-10)

**[alice 2026-03-10 09:00 UTC]**
@channel URGENT CORRECTION: In my email of 2026-03-06, I made two errors.

Error 1: I said to use PR#6963 commit SHA (5b4b64c3...) as the authoritative fix.
This is WRONG. The correct fix commit is PR#6965 (sethmlarson):
  `{COMMIT_SHA_PR6965}`

This SUPERSEDES my previous instruction. Please update `analysis/fix_commit.json` now.

Error 2: I claimed requests 2.32.3 has a partial fix for CVE-2024-47081.
This is also WRONG — 2.32.3 has zero fix for this CVE.

**[bob 2026-03-10 09:15 UTC]**
Got it. Updating the internal records. PR#6965 is the authoritative fix.
Commit {COMMIT_SHA_PR6965[:12]}...

**[carol 2026-03-10 09:20 UTC]**
Updated our security tracker. PR#6963 is marked as superseded.
GHSA-9hjg-9r4m-mvj7 linked to PR#6965 only.

---
*This document is part of Update-2 and supersedes the commit SHA instruction from Update-1.*
"""
    (u2_dir / "erratum_slack.md").write_text(erratum_slack, encoding="utf-8")


def _write_pr6965_review_snapshot(u2_dir: Path) -> None:
    """PR#6965 完整 review 记录快照（大体量，~20k tokens 目标）。"""
    lines = [f"""\
# PR#6965 Full Review Snapshot — Update-2 Workspace

Source: https://github.com/psf/requests/pull/6965
Retrieved: 2026-03-10

## Pull Request Summary

**Title**: Only use hostname to do netrc lookup instead of netloc

**Author**: sethmlarson
**Merge Commit**: `{COMMIT_SHA_PR6965}`
**GHSA**: `{GHSA_ID}`
**Status**: MERGED

## Description

This PR fixes CVE-2024-47081 by replacing the vulnerable `ri.netloc.split(':')[0]`
with `ri.hostname` in the `get_netrc_auth` function in `src/requests/utils.py`.

### The Vulnerability

```python
# BEFORE (vulnerable — CVE-2024-47081):
host = ri.netloc.split(':')[0]
```

For a URL like `http://example.com:@evil.com/`, `urlparse` sets:
- `netloc` = `example.com:@evil.com`
- `netloc.split(':')[0]` = `example.com`

But the actual HTTP request targets `evil.com`. So netrc credentials for
`example.com` are sent to `evil.com`.

### The Fix

```python
# AFTER (fixed — PR#6965):
host = ri.hostname
if host is None:
    return None
```

`ri.hostname` correctly uses Python's URL parsing, which understands the userinfo
syntax (`user@host`) and returns only the hostname portion.

## Diff

```diff
--- a/src/requests/utils.py
+++ b/src/requests/utils.py
@@ -240,7 +240,9 @@ def get_netrc_auth(url, raise_errors=False):
         ri = urlparse(url)
-        host = ri.netloc.split(":")[0]
+        host = ri.hostname
+        if host is None:
+            return None

         _netrc = netrc_.authenticators(host)
```

## Review Comments

"""]
    # Pad with review comments to reach ~20k tokens
    reviewers = ["sigmavirus24", "nateprewitt", "rawwar", "nicowillis", "sethmlarson"]
    topics = [
        "hostname extraction correctness",
        "None check necessity",
        "backwards compatibility",
        "test coverage adequacy",
        "GHSA advisory format",
        "changelog entry format",
        "workaround documentation",
        "Python version compatibility",
        "edge case handling",
        "performance implications",
    ]
    for i in range(1, 150):
        reviewer = reviewers[i % len(reviewers)]
        topic = topics[i % len(topics)]
        lines.append(f"""
### Review Comment {i:02d} — {reviewer} on {topic}

**{reviewer}** commented:

The change regarding {topic} looks correct. The `ri.hostname` attribute from
Python's `urllib.parse.urlparse` correctly strips userinfo (`user@host` forms)
and port numbers, returning only the hostname. This is the canonical approach
for extracting the host from a URL in Python.

For reference, Python's documentation on `urlparse` specifies that `hostname`
is the "Host subcomponent, lowercased" and explicitly handles the case where
the URL contains userinfo. The `netloc` attribute, by contrast, includes the
full network location including userinfo and port.

Test case verification for comment {i:02d}:
```python
from urllib.parse import urlparse
# Malicious URL
ri = urlparse('http://example.com:@evil.com/')
assert ri.hostname == 'evil.com'  # Correct!
assert ri.netloc.split(':')[0] == 'example.com'  # Vulnerable!

# Legitimate URL
ri = urlparse('http://example.com/')
assert ri.hostname == 'example.com'  # Correct!

# URL with port
ri = urlparse('http://example.com:8080/')
assert ri.hostname == 'example.com'  # Correct (port stripped)!
```

Confidence level: HIGH. This is a clean, minimal fix that correctly addresses
the root cause without introducing complexity.

""")
    (u2_dir / "pr6965_review_snapshot.md").write_text("\n".join(lines), encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    gen_system_files()
    gen_source_files()
    gen_test_files()
    gen_docs()
    gen_analysis_files()
    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids)

    desc = (
        "psf/requests CVE-2024-47081 bug fix & regression testing — "
        "15 exec_check rounds, 2 updates (UPDATE-2 supersedes UPDATE-1 commit SHA), "
        "4 preference rules P1-P4, difficulty vectors V1/V2/V3/V4/V5/V6/V7/V9/V10. "
        "Real sources: "
        "https://github.com/psf/requests/issues/6964; "
        "https://github.com/psf/requests/pull/6965; "
        "https://github.com/psf/requests/pull/6963; "
        "https://nvd.nist.gov/vuln/detail/CVE-2024-47081; "
        "https://raw.githubusercontent.com/psf/requests/main/src/requests/utils.py; "
        "https://raw.githubusercontent.com/psf/requests/main/tests/test_utils.py."
    )

    dump_register_meta(
        DATASET, test_id=TID, desc=desc,
        main_session=sess_ids["main"],
        history_sessions=sess_ids["history"],
        updates=updates_decl,
    )

    # 体量报告
    total_ws = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in WS.rglob("*") if p.is_file()
    )
    sess_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in SESS.glob("*.jsonl")
    ) if SESS.exists() else 0
    upd_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in UPD.rglob("*") if p.is_file()
    ) if UPD.exists() else 0
    print(f"[eng1] workspace tokens ~{total_ws:,} | sessions ~{sess_tok:,} | updates ~{upd_tok:,}")
    print(f"[eng1] built at {DATASET}")
    print(f"[eng1] _register.json: {DATASET}/openclaw/state/agents/{TID}/_register.json")


if __name__ == "__main__":
    main()
