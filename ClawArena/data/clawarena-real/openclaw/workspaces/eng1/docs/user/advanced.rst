Advanced Usage
==============

This document covers some of the more advanced features of Requests.

Session Objects
---------------

The Session object allows you to persist certain parameters across requests.
It also persists cookies across all requests made from the Session instance,
and will use ``urllib3``'s `connection pooling
<https://urllib3.readthedocs.io/en/latest/advanced-usage.html#customizing-pool-behavior>`_.
So if you're making several requests to the same host, the underlying TCP
connection will be reused, which can result in a significant performance increase
(see `HTTP persistent connection <https://en.wikipedia.org/wiki/HTTP_persistent_connection>`_).

A Session object has all the methods of the main Requests API::

    s = requests.Session()
    s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
    r = s.get('https://httpbin.org/cookies')
    print(r.text)
    # '{"cookies": {"sessioncookie": "123456789"}}'

Sessions can also be used to provide default data to the request methods. This
is done by providing data to the properties on a Session object::

    s = requests.Session()
    s.auth = ('user', 'pass')
    s.headers.update({'x-test': 'true'})

    # both 'x-test' and 'x-test2' are sent
    s.get('https://httpbin.org/headers', headers={'x-test2': 'true'})

SSL Certificate Verification
-----------------------------

Requests verifies SSL certificates for HTTPS requests, just like a web browser.
By default, SSL verification is enabled, and Requests will throw a SSLError if
it's unable to verify the certificate::

    >>> requests.get('https://requestb.in')
    requests.exceptions.SSLError: hostname 'requestb.in' doesn't match ...

You can pass ``verify`` the path to a CA_BUNDLE file or directory with
certificates of trusted CAs::

    >>> requests.get('https://github.com', verify='/path/to/certfile')

You can also disable SSL verification, though this is strongly discouraged for
production use::

    >>> requests.get('https://kennethreitz.org', verify=False)
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

With Requests, it's possible to send large streams or files without reading
them into memory. To stream and upload, simply provide a file-like object for
your body::

    with open('massive-body', 'rb') as f:
        requests.post('http://some.url/streamed', data=f)

Timeouts
--------

Most requests to external servers should have a timeout attached, in case the
server is not responding in a timely manner. By default, requests do not time out
unless a timeout value is set explicitly. Without a timeout, your code may hang
for minutes or more::

    >>> requests.get('https://github.com', timeout=0.001)
    Traceback (most recent call last):
        ...
    requests.exceptions.ConnectTimeout: ...
