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
    :param files: (optional) Dictionary of ``'name': file-like-objects`` for multipart encoding upload.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data.
    :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/HEAD/POST/PUT/PATCH/DELETE redirects.
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify the server's TLS certificate.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem).
    :type method: str
    :return: :py:class:`Response <Response>` object
    :rtype: requests.Response

    Usage::

      >>> import requests
      >>> req = requests.request('GET', 'https://httpbin.org/get')
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
