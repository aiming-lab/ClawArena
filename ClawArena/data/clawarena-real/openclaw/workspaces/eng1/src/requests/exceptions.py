"""
requests.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Requests' exceptions.

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
    """Couldn't decode the text into json."""
    def __init__(self, *args, **kwargs):
        self.json_error = kwargs.pop("json_error", None)
        super().__init__(*args, **kwargs)


class FileModeWarning(DeprecationWarning, UserWarning):
    """A file was opened in text mode, but Requests determined it should be binary."""
