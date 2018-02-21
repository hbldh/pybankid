.. _getstarted:

Getting Started
===============

Installation
------------

PyBankID can be installed though pip:

.. code-block:: bash

    pip install pybankid

To remedy the ``InsecurePlatformWarning`` problem detailed below
(`Python 2, urllib3 and certificate verification`_), you can install
``pybankid`` with the ``security`` extras:

.. code-block:: bash

    pip install pybankid[security]

This installs the ``pyopenssl``, ``ndg-httpsclient`` and ``pyasn1`` packages
as well.

In Linux, this does however require the installation of some additional
system packages:

.. code-block:: bash

    sudo apt-get install build-essential libssl-dev libffi-dev python-dev

See the `cryptography package's documentation for details <https://cryptography.io/en/latest/installation/#building-cryptography-on-linux>`_.

Dependencies
------------

PyBankID makes use of the following external packages:

* `requests>=2.7.0 <https://docs.python-requests.org/>`_
* `zeep>=1.3.0 <https://docs.python-zeep.org/en/master/>`_
* `six>=1.9.0 <https://pythonhosted.org/six/>`_


Python 2, urllib3 and certificate verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An ``InsecurePlatformWarning`` is issued when using the client in Python 2 (See
`urllib3 documentation <https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning>`_).
This can be remedied by installing ``pyopenssl`` according to
`this issue <https://github.com/kennethreitz/requests/issues/749>`_ and
`docstrings in requests <https://github.com/kennethreitz/requests/blob/master/requests/packages/urllib3/contrib/pyopenssl.py>`_.

Optionally, the environment variable ``PYBANKID_DISABLE_WARNINGS`` can be set to disable these warnings.
