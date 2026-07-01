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
