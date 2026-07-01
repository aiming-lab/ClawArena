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
    >>> requests.get('https://api.github.com/user', auth=HTTPBasicAuth('user', 'pass'))
    <Response [200]>

In fact, HTTP Basic Auth is so common that Requests provides a handy shorthand
for using it::

    >>> requests.get('https://api.github.com/user', auth=('user', 'pass'))
    <Response [200]>

netrc Authentication
--------------------

Requests supports automatic credential lookup from ``~/.netrc`` (or ``~/_netrc``
on Windows) when ``trust_env=True`` (the default). The lookup is performed by
the ``get_netrc_auth`` function in ``requests.utils``.

**Security Note (CVE-2024-47081):** Versions prior to 2.32.4 contained a
vulnerability in ``get_netrc_auth`` where the hostname extraction used
``ri.netloc.split(':')[0]`` instead of ``ri.hostname``. This could cause
credentials to be leaked to an attacker-controlled host via a crafted URL
such as ``http://example.com:@evil.com/``.

**Workaround:** Set ``trust_env=False`` on your Session object to disable
automatic ``.netrc`` lookup::

    >>> import requests
    >>> s = requests.Session()
    >>> s.trust_env = False
    >>> s.get('https://example.com/api')

**Fix:** Upgrade to requests >= 2.32.4.

Digest Authentication
---------------------

Another very popular form of HTTP Authentication is Digest Authentication::

    >>> from requests.auth import HTTPDigestAuth
    >>> url = 'https://httpbin.org/digest-auth/auth/user/pass'
    >>> requests.get(url, auth=HTTPDigestAuth('user', 'pass'))
    <Response [200]>

OAuth 1 Authentication
----------------------

Many web APIs use OAuth 1.0 for authentication. The ``requests-oauthlib``
library can be used to achieve this.

OAuth 2 and OpenID Connect Authentication
-----------------------------------------

For OAuth 2.0, the ``requests-oauthlib`` library provides OAuth 2.0 flows.
