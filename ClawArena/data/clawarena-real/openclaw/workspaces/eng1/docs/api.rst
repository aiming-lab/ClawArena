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


Supplemental Reference (Section 01)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 01. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 01
"""""""""""""""""""""""""""""""""""

The subsystem 01 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 02)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 02. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 02
"""""""""""""""""""""""""""""""""""

The subsystem 02 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 03)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 03. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 03
"""""""""""""""""""""""""""""""""""

The subsystem 03 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 04. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 04
"""""""""""""""""""""""""""""""""""

The subsystem 04 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 05)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 05. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 05
"""""""""""""""""""""""""""""""""""

The subsystem 05 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 06. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 06
"""""""""""""""""""""""""""""""""""

The subsystem 06 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 07)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 07. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 07
"""""""""""""""""""""""""""""""""""

The subsystem 07 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 08)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 08. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 08
"""""""""""""""""""""""""""""""""""

The subsystem 08 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 09)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 09. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 09
"""""""""""""""""""""""""""""""""""

The subsystem 09 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 10. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 10
"""""""""""""""""""""""""""""""""""

The subsystem 10 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 11)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 11. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 11
"""""""""""""""""""""""""""""""""""

The subsystem 11 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 12)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 12. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 12
"""""""""""""""""""""""""""""""""""

The subsystem 12 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 13)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 13. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 13
"""""""""""""""""""""""""""""""""""

The subsystem 13 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 14)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 14. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 14
"""""""""""""""""""""""""""""""""""

The subsystem 14 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 15)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 15. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 15
"""""""""""""""""""""""""""""""""""

The subsystem 15 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 16)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 16. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 16
"""""""""""""""""""""""""""""""""""

The subsystem 16 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 17)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 17. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 17
"""""""""""""""""""""""""""""""""""

The subsystem 17 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 18)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 18. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 18
"""""""""""""""""""""""""""""""""""

The subsystem 18 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 19)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 19. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 19
"""""""""""""""""""""""""""""""""""

The subsystem 19 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 20. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 20
"""""""""""""""""""""""""""""""""""

The subsystem 20 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 21)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 21. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 21
"""""""""""""""""""""""""""""""""""

The subsystem 21 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 22)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 22. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 22
"""""""""""""""""""""""""""""""""""

The subsystem 22 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 23)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 23. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 23
"""""""""""""""""""""""""""""""""""

The subsystem 23 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 24)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 24. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 24
"""""""""""""""""""""""""""""""""""

The subsystem 24 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 25)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 25. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 25
"""""""""""""""""""""""""""""""""""

The subsystem 25 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 26)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 26. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 26
"""""""""""""""""""""""""""""""""""

The subsystem 26 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 27)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 27. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 27
"""""""""""""""""""""""""""""""""""

The subsystem 27 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 28)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 28. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 28
"""""""""""""""""""""""""""""""""""

The subsystem 28 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 29)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 29. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 29
"""""""""""""""""""""""""""""""""""

The subsystem 29 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 30)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 30. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 30
"""""""""""""""""""""""""""""""""""

The subsystem 30 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 31)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 31. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 31
"""""""""""""""""""""""""""""""""""

The subsystem 31 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 32)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 32. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 32
"""""""""""""""""""""""""""""""""""

The subsystem 32 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 33)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 33. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 33
"""""""""""""""""""""""""""""""""""

The subsystem 33 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 34)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 34. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 34
"""""""""""""""""""""""""""""""""""

The subsystem 34 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 35)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 35. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 35
"""""""""""""""""""""""""""""""""""

The subsystem 35 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 36)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 36. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 36
"""""""""""""""""""""""""""""""""""

The subsystem 36 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 37)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 37. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 37
"""""""""""""""""""""""""""""""""""

The subsystem 37 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 38)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 38. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 38
"""""""""""""""""""""""""""""""""""

The subsystem 38 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.


Supplemental Reference (Section 39)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section documents additional internal details, constants, and configuration
hooks used in the Requests library subsystem 39. These are primarily for
developers extending or integrating with Requests at a low level.

Constants and Defaults
""""""""""""""""""""""

The following constants are defined in ``requests.utils`` and ``requests.compat``
and influence library behaviour at module level:

- ``NETRC_FILES``: Tuple of filenames to search for netrc credentials. Default
  is ``(".netrc", "_netrc")``. On Windows, ``_netrc`` is checked first.
- ``DEFAULT_PORTS``: Mapping of scheme to default port number. ``{"http": 80,
  "https": 443}``.
- ``DEFAULT_CA_BUNDLE_PATH``: Path to the default CA bundle, set at import time
  from ``certifi``.

Configuration for subsystem 39
"""""""""""""""""""""""""""""""""""

The subsystem 39 configuration follows the standard Requests pattern of
reading from environment variables first, then session-level configuration,
then request-level overrides. This layered approach allows flexible deployment
across different network environments.

