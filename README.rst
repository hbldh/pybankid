PyBankID
========

.. image:: https://travis-ci.org/hbldh/pybankid.svg?branch=master
    :target: https://travis-ci.org/hbldh/pybankid

PyBankID is a client for performing BankID signing.

The Swedish BankID solution for digital signing uses a SOAP
connection solution, and this module aims at providing a simplifying
client for making authentication, signing and collect requests to
the BankID servers.

For more details about BankID implementation, see the `official documentation
<https://www.bankid.com/bankid-i-dina-tjanster/rp-info>`_. There, one can find information
about how the BankID methods are defined, how to set up the test environment
and obtain the SSL certificate for the test server.

Installation
------------
To install PyBankID, install it from this GitHub repository via pip:

.. code-block:: bash

    pip install git+https://github.com/hbldh/pybankid.git

Usage
-----

First, create a BankIDClient:

.. code-block:: python

    >>> from bankid.client import BankIDClient
    >>> client = BankIDClient(certificates=('path/to/certificate.pem',
                                            'path/to/key.pem'))

Connection to production server is the default in the client. If test
server is desired, send in the ``test_server=True`` keyword in the init
of the client.

A sign order is then placed by

.. code-block:: python

    >>> client.sign(user_visible_data="The information to sign.",
                    personal_number="YYYYMMDDXXXX")
    {'autoStartToken': u'798c1ea1-e67a-4df6-a2f6-164ac223fd52',
     'orderRef': u'a9b791c3-459f-492b-bf61-23027876140b'}

and an authentication order is initiated by

.. code-block:: python

    >>> client.authenticate(personal_number="YYYYMMDDXXXX")
    {'autoStartToken': u'798c1ea1-e67a-4df6-a2f6-164ac223fd52',
     'orderRef': u'a9b791c3-459f-492b-bf61-23027876140b'}

The status of an order can then be studied by polling
with the ``collect`` method using the received ``orderRef``:

.. code-block:: python

    >>> client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
    {'progressStatus': u'OUTSTANDING_TRANSACTION'}
    >>> client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
    {'progressStatus': u'USER_SIGN'}
    >>> client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
    {'ocspResponse': u'MIIHfgoBAKCCB3cw[...]',
     'progressStatus': u'COMPLETE',
     'signature': u'PD94bWwgdmVyc2lvbj0[...]',
     'userInfo': {'givenName': u'Namn',
                  'ipAddress': u'195.84.248.212',
                  'name': u'Namn Namsson',
                  'notAfter': datetime.datetime(2016, 9, 9, 22, 59, 59),
                  'notBefore': datetime.datetime(2014, 9, 9, 23, 0),
                  'personalNumber': u'YYYYMMDDXXXX',
                  'surname': u'Namnsson'}}

The ``collect`` should be used sparingly, as not to burden the server unnecessarily.

Testing
-------

The PyBankID solution can be tested with ``nosetests``:

.. code-block:: bash

    nosetests tests/

Documentation
-------------

No documentation is available yet. Read the docstrings until then.
