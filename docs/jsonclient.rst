.. _jsonclient:

BankID JSON Client
==================

The Relying Party client using the ``v5`` JSON API.

Usage
-----

Create a client:

.. code-block:: python

    >>> from bankid import BankIDJSONClient
    >>> client = BankIDJSONClient(certificates=('path/to/certificate.pem',
    ...                                         'path/to/key.pem'))

Connection to production server is the default in the client. If test
server is desired, send in the ``test_server=True`` keyword in the init
of the client.

When using the JSON client, all authentication and signing calls requires
the end user's ip address to be included the requests. An authentication order
is initiated as such:

.. code-block:: python

    >>> client.authenticate(end_user_ip='194.168.2.25',
    ...                     personal_number="YYYYMMDDXXXX")
    {
        'autoStartToken': '798c1ea1-e67a-4df6-a2f6-164ac223fd52',
        'orderRef': 'a9b791c3-459f-492b-bf61-23027876140b'
    }

and a sign order is initiated in a similar fashion:

.. code-block:: python

    >>> client.sign(end_user_ip='194.168.2.25',
    ...            user_visible_data="The information to sign.",
    ...            personal_number="YYYYMMDDXXXX")
    {
        'autoStartToken': '798c1ea1-e67a-4df6-a2f6-164ac223fd52',
        'orderRef': 'a9b791c3-459f-492b-bf61-23027876140b'
    }

Since the `BankIDJSONClient` is using the BankID ``v5`` JSON API, the `personal_number` can now be omitted when calling
`authenticate` and `sign`. See `BankID Relying Party Guidelines <https://www.bankid.com/bankid-i-dina-tjanster/rp-info>`_
for more information about this.

The status of an order can then be studied by polling
with the ``collect`` method using the received ``orderRef``:

.. code-block:: python

    >>> client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
    {
        'hintCode': 'outstandingTransaction',
        'orderRef': 'a9b791c3-459f-492b-bf61-23027876140b',
        'status': 'pending'
    }
    >>> client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
    {
        'hintCode': 'userSign',
        'orderRef': 'a9b791c3-459f-492b-bf61-23027876140b',
        'status': 'pending'
    }
    >>> c.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
    {
        'completionData': {
            'cert': {
                'notAfter': '1581289199000',
                'notBefore': '1518130800000'
            },
            'device': {
                'ipAddress': '0.0.0.0'
            },
            'ocspResponse': 'MIIHegoBAKCCB[...]',
            'signature': 'PD94bWwgdmVyc2lv[...]',
            'user': {
                'givenName': 'Namn',
                'name': 'Namn Namnsson',
                'personalNumber': 'YYYYMMDDXXXX',
                'surname': 'Namnsson'
            }
        },
        'orderRef': 'a9b791c3-459f-492b-bf61-23027876140b',
        'status': 'complete'
    }

Please note that the ``collect`` method should be used sparingly: in the
`BankID Relying Party Guidelines <https://www.bankid.com/bankid-i-dina-tjanster/rp-info>`_
it is specified that *"collect should be called every two seconds and must not be
called more frequent than once per second"*.

API
---

.. automodule:: bankid.jsonclient
   :members:
