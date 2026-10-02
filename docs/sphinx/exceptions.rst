Exceptions & Warnings
=====================

.. py:currentmodule:: elastic_transport

Transport Errors
----------------

When a request fails, the raised transport error's ``errors`` tuple contains
the errors from all failed attempts, including the final attempt, newest first.
Each attempt retains its own underlying errors, such as a TLS certificate error.
This also applies when ``max_retries=0``.

.. autoclass:: TransportError
   :members:

.. autoclass:: TlsError
   :members:

.. autoclass:: ConnectionError
   :members:

.. autoclass:: ConnectionTimeout
   :members:

.. autoclass:: SerializationError
   :members:

.. autoclass:: SniffingError
   :members:

.. autoclass:: ApiError
   :members:

Warnings
--------

.. py:currentmodule:: elastic_transport

.. autoclass:: TransportWarning

.. autoclass:: SecurityWarning
