.. _getstarted:

Getting Started
===============

PyBankID use BankID JSON API version 5.1 released in April 2020.

Installation
------------

PyBankID can be installed though pip:

.. code-block:: bash

    pip install pybankid

Dependencies
------------

PyBankID makes use of the following external packages:

* `httpx==0.24.1 <https://www.python-httpx.org/>`_
* `importlib-resources==5.12.0 <https://importlib-resources.readthedocs.io/>`_

Using the client
----------------------

PyBankID provide both a synchronous and an asynchronous client for
communication with BankID services. Example below will use the asynchronous
client, but the synchronous client is used in the same way.

Get started by importing and initializing the client:

.. code-block:: python

    >>> from bankid import AsyncBankIDJSONClient
    >>> client = AsyncBankIDJSONClient(certificates=(
    ...     'path/to/certificate.pem',
    ...     'path/to/key.pem',
    ... ))

The client will by default connect to production servers. If test
server is desired, pass the ``test_server=True`` keyword to the client.

When using the JSON client, all authentication and signing calls requires
the end user's ip address to be included the requests. An authentication order
is initiated as such:

.. code-block:: python

    >>> await client.authenticate(end_user_ip='194.168.2.25',
    ...                           personal_number="YYYYMMDDXXXX")
    {
        'orderRef': 'ee3421ea-2096-4000-8130-82648efe0927',
        'autoStartToken': 'e8df5c3c-c67b-4a01-bfe5-fefeab760beb',
        'qrStartToken': '01f94e28-857f-4d8a-bf8e-6c5a24466658',
        'qrStartSecret': 'b4214886-3b5b-46ab-bc08-6862fddc0e06'
    }

and a sign order is initiated in a similar fashion:

.. code-block:: python

    >>> await client.sign(end_user_ip='194.168.2.25',
    ...                   user_visible_data="The information to sign.",
    ...                   personal_number="YYYYMMDDXXXX")
    {
        'orderRef': 'ee3421ea-2096-4000-8130-82648efe0927',
        'autoStartToken': 'e8df5c3c-c67b-4a01-bfe5-fefeab760beb',
        'qrStartToken': '01f94e28-857f-4d8a-bf8e-6c5a24466658',
        'qrStartSecret': 'b4214886-3b5b-46ab-bc08-6862fddc0e06'
    }

Since we are using BankID ``v5.1`` JSON API, the `personal_number` can now be omitted when calling
`authenticate` and `sign`. See `BankID Relying Party Guidelines <https://www.bankid.com/utvecklare/rp-info>`_
for more information about this.

The status of an order can then be studied by polling
with the ``collect`` method using the received ``orderRef``:

.. code-block:: python

    >>> await client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
    {
        'hintCode': 'outstandingTransaction',
        'orderRef': 'a9b791c3-459f-492b-bf61-23027876140b',
        'status': 'pending'
    }
    >>> await client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
    {
        'hintCode': 'userSign',
        'orderRef': 'a9b791c3-459f-492b-bf61-23027876140b',
        'status': 'pending'
    }
    >>> await client.collect(order_ref="a9b791c3-459f-492b-bf61-23027876140b")
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
`BankID Relying Party Guidelines <https://www.bankid.com/utvecklare/rp-info>`_
it is specified that *"collect should be called every two seconds and must not be
called more frequent than once per second"*.

Synchronous client
----------------------

The synchronous client is used in the same way as the asynchronous client, but the
methods are blocking. The synchronous client call the aynchronous client under the
hood.

The asynchronous guide above can be used as a reference for the synchronous client
as well, by simply removing the `await` keyword.

.. code-block:: python

    >>> from bankid import BankIDJSONClient
    >>> client = BankIDJSONClient(certificates=(
    ...     'path/to/certificate.pem',
    ...     'path/to/key.pem',
    ... ))
    >>> client.authenticate(
    ...     end_user_ip='194.168.2.25',
    ...     personal_number="YYYYMMDDXXXX",
    ... )
    {
        'orderRef': 'ee3421ea-2096-4000-8130-82648efe0927',
        'autoStartToken': 'e8df5c3c-c67b-4a01-bfe5-fefeab760beb',
        'qrStartToken': '01f94e28-857f-4d8a-bf8e-6c5a24466658',
        'qrStartSecret': 'b4214886-3b5b-46ab-bc08-6862fddc0e06'
    }
