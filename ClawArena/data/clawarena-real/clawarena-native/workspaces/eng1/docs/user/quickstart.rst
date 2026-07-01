Quickstart
==========

.. module:: requests.api

Eager to get started? This page gives a good introduction on how to get started
with Requests.

First, make sure that:

* Requests is :ref:`installed <install>`
* Requests is :ref:`up-to-date <updates>`

Let's get started with some simple examples.

Make a Request
--------------

Making a request with Requests is very simple.

Begin by importing the Requests module::

    >>> import requests

Now, let's try to get a webpage. For this example, let's get GitHub's public
timeline::

    >>> r = requests.get('https://api.github.com/events')

Now, we have a :class:`Response <requests.Response>` object called ``r``. We can
get all the information we need from this object.

Requests' simple API means that all forms of HTTP request are as obvious. For
example, this is how you make an HTTP POST request::

    >>> r = requests.post('https://httpbin.org/post', data={'key': 'value'})

Nice, right? What about the other HTTP request types: PUT, DELETE, HEAD and
OPTIONS? These are all just as simple::

    >>> r = requests.put('https://httpbin.org/put', data={'key': 'value'})
    >>> r = requests.delete('https://httpbin.org/delete')
    >>> r = requests.head('https://httpbin.org/get')
    >>> r = requests.options('https://httpbin.org/get')

Passing Parameters in URLs
--------------------------

You often want to send some sort of data in the URL's query string. If you
were constructing the URL by hand, this data would be given as key/value pairs
in the URL after a question mark, e.g. ``httpbin.org/get?key=val``. Requests
allows you to provide these arguments as a dictionary of strings, using the
``params`` keyword argument::

    >>> payload = {'key1': 'value1', 'key2': 'value2'}
    >>> r = requests.get('https://httpbin.org/get', params=payload)

Response Content
----------------

We can read the content of the server's response::

    >>> r = requests.get('https://api.github.com/events')
    >>> r.text
    '[{"repository":{"open_issues":0,"url":"https://github.com/...

Requests will automatically decode content from the server. Most unicode
charsets are seamlessly decoded.

Binary Response Content
-----------------------

You can also access the response body as bytes, for non-text requests::

    >>> r.content
    b'[{"repository":{"open_issues":0,"url":"https://github.com/...

JSON Response Content
---------------------

There's also a built-in JSON decoder, in case you're dealing with JSON data::

    >>> r = requests.get('https://api.github.com/events')
    >>> r.json()
    [{"repository": {"open_issues": 0, "url": "https://github.com/...

In case the JSON decoding fails, ``r.json()`` raises an exception. For example,
if the response gets a 204 (No Content), or if the response contains invalid JSON,
attempting ``r.json()`` raises ``requests.exceptions.JSONDecodeError``.
