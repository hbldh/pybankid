.. _soapclient:

BankID SOAP Client
==================

The Relying Party client using the ``v4`` SOAP API.

**This client will be deprecated in February 2020. Prior to this a**
:exc:`PendingDeprecationWarning` **will be issued on using.**

Usage
-----

First, create a ``BankIDClient``:

.. code-block:: python

    >>> from bankid import BankIDClient
    >>> client = BankIDClient(certificates=('path/to/certificate.pem',
    ...                                     'path/to/key.pem'))

Connection to production server is the default in the client. If test
server is desired, send in the ``test_server=True`` keyword in the init
of the client.

A sign order is then placed by

.. code-block:: python

    >>> client.sign(user_visible_data="The information to sign.",
    ...             personal_number="YYYYMMDDXXXX")
    {'autoStartToken': '798c1ea1-e67a-4df6-a2f6-164ac223fd52',
     'orderRef': 'a9b791c3-459f-492b-bf61-23027876140b'}

and an authentication order is initiated by

.. code-block:: python

    >>> client.authenticate(personal_number="YYYYMMDDXXXX")
    {'autoStartToken': '798c1ea1-e67a-4df6-a2f6-164ac223fd52',
     'orderRef': 'a9b791c3-459f-492b-bf61-23027876140b'}

The status of an order can then be studied by polling
with the ``collect`` method using the received ``orderRef``:

.. code-block:: python

    >>> client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
    {'progressStatus': 'OUTSTANDING_TRANSACTION'}
    >>> client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
    {'progressStatus': 'USER_SIGN'}
    >>> client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
    {'ocspResponse': 'MIIHfgoBAKCCB3cw[...]',
     'progressStatus': 'COMPLETE',
     'signature': 'PD94bWwgdmVyc2lvbj0[...]',
     'userInfo': {'givenName': 'Namn',
                  'ipAddress': '195.84.248.212',
                  'name': 'Namn Namnsson',
                  'notAfter': datetime.datetime(2016, 9, 9, 22, 59, 59),
                  'notBefore': datetime.datetime(2014, 9, 9, 23, 0),
                  'personalNumber': 'YYYYMMDDXXXX',
                  'surname': 'Namnsson'}}

Please note that the ``collect`` method should be used sparingly: in the
`BankID Relying Party Guidelines <https://www.bankid.com/bankid-i-dina-tjanster/rp-info>`_.
it states that *"collect should be called every two seconds and must not be
called more frequent than once per second"*.

API
---

.. automodule:: bankid.client
   :members:
