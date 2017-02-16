PyBankID
========

.. image:: https://travis-ci.org/hbldh/pybankid.svg?branch=master
    :target: https://travis-ci.org/hbldh/pybankid
.. image:: https://readthedocs.org/projects/pybankid/badge/?version=latest
    :target: http://pybankid.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: http://img.shields.io/pypi/v/pybankid.svg
    :target: https://pypi.python.org/pypi/pybankid/
.. image:: http://img.shields.io/pypi/dm/pybankid.svg
    :target: https://pypi.python.org/pypi/pybankid/
.. image:: http://img.shields.io/pypi/l/pybankid.svg
    :target: https://pypi.python.org/pypi/pybankid/
.. image:: https://coveralls.io/repos/github/hbldh/pybankid/badge.svg?branch=master
    :target: https://coveralls.io/github/hbldh/pybankid?branch=master

PyBankID is a client for performing BankID signing.

The Swedish BankID solution for digital signing uses a SOAP
connection solution, and this module aims at providing a simplifying
client for making authentication, signing and collect requests to
the BankID servers.

For more details about BankID implementation, see the `official documentation
<https://www.bankid.com/bankid-i-dina-tjanster/rp-info>`_. There, one can find information
about how the BankID methods are defined, how to set up the test environment
and obtain the SSL certificate for the test server.

An `example web application using PyBankID <https://github.com/hbldh/pybankid-example-app>`_
exists and can be found in deployed state on `Heroku <https://bankid-example-app.herokuapp.com/>`_.

Installation
------------
PyBankID can be installed though pip:

.. code-block:: bash

    pip install pybankid

The remedy the ``InsecurePlatformWarning`` problem detailed below (
`Python 2, urllib3 and certificate verification`_), you can install
``pybankid`` with the ``security`` extras:

.. code-block:: bash

    pip install pybankid[security]

This installs the ``pyopenssl``, ``ndg-httpsclient`` and ``pyasn1`` packages
as well.
This does however require the installation of some additional system packages:

.. code-block:: bash

    sudo apt-get install build-essential libssl-dev libffi-dev python-dev

See the `cryptography package's documentation for details <https://cryptography.io/en/latest/installation/#building-cryptography-on-linux>`_.

Usage
-----

First, create a BankIDClient:

.. code-block:: python

    >>> from bankid import BankIDClient
    >>> client = BankIDClient(certificates=('path/to/certificate.pem',
                                            'path/to/key.pem'))

Connection to production server is the default in the client. If test
server is desired, send in the ``test_server=True`` keyword in the init
of the client.

A sign order is then placed by

.. code-block:: python

    >>> client.sign(user_visible_data="The information to sign.",
                    personal_number="YYYYMMDDXXXX")
    {u'autoStartToken': u'798c1ea1-e67a-4df6-a2f6-164ac223fd52',
     u'orderRef': u'a9b791c3-459f-492b-bf61-23027876140b'}

and an authentication order is initiated by

.. code-block:: python

    >>> client.authenticate(personal_number="YYYYMMDDXXXX")
    {u'autoStartToken': u'798c1ea1-e67a-4df6-a2f6-164ac223fd52',
     u'orderRef': u'a9b791c3-459f-492b-bf61-23027876140b'}

The status of an order can then be studied by polling
with the ``collect`` method using the received ``orderRef``:

.. code-block:: python

    >>> client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
    {u'progressStatus': u'OUTSTANDING_TRANSACTION'}
    >>> client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
    {u'progressStatus': u'USER_SIGN'}
    >>> client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
    {u'ocspResponse': u'MIIHfgoBAKCCB3cw[...]',
     u'progressStatus': u'COMPLETE',
     u'signature': u'PD94bWwgdmVyc2lvbj0[...]',
     u'userInfo': {u'givenName': u'Namn',
                  u'ipAddress': u'195.84.248.212',
                  u'name': u'Namn Namsson',
                  u'notAfter': datetime.datetime(2016, 9, 9, 22, 59, 59),
                  u'notBefore': datetime.datetime(2014, 9, 9, 23, 0),
                  u'personalNumber': u'YYYYMMDDXXXX',
                  u'surname': u'Namnsson'}}

The ``collect`` should be used sparingly, as not to burden the server unnecessarily.

Python 2, urllib3 and certificate verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An ``InsecurePlatformWarning`` is issued when using the client in Python 2 (See
`urllib3 documentation <https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning>`_).
This can be remedied by installing ``pybankid`` with the ``security`` extras as
described above, or to manually install ``pyopenssl`` according to
`this issue <https://github.com/kennethreitz/requests/issues/749>`_ and
`docstrings in requests <https://github.com/kennethreitz/requests/blob/master/requests/packages/urllib3/contrib/pyopenssl.py>`_.

Optionally, the environment variable ``PYBANKID_DISABLE_WARNINGS`` can be set to disable these warnings.

Testing
-------

The PyBankID solution can be tested with `pytest <https://pytest.org/>`_:

.. code-block:: bash

    py.test tests/
