PyBankID
========

.. image:: https://github.com/hbldh/pybankid/workflows/Build%20and%20Test/badge.svg
    :target: https://github.com/hbldh/pybankid/actions?query=workflow%3A%22Build+and+Test%22
.. image:: https://readthedocs.org/projects/pybankid/badge/?version=latest
    :target: http://pybankid.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: http://img.shields.io/pypi/v/pybankid.svg
    :target: https://pypi.python.org/pypi/pybankid/
.. image:: http://img.shields.io/pypi/l/pybankid.svg
    :target: https://pypi.python.org/pypi/pybankid/
.. image:: https://coveralls.io/repos/github/hbldh/pybankid/badge.svg?branch=master
    :target: https://coveralls.io/github/hbldh/pybankid?branch=master

PyBankID is a client for providing BankID services as a Relying Party, i.e.
providing authentication and signing functionality to end users. This package
provides a simplifying interface for initiating authentication
and signing orders and then collecting the results from the BankID servers.

If you intend to use PyBankID in your project, you are advised to read
the `BankID Relying Party Guidelines
<https://www.bankid.com/utvecklare/rp-info>`_ before
doing anything else. There, one can find information
about how the BankID methods are defined and how to use them.

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

Usage
-----

``BankIDJSONClient`` is the client to be used to
communicate with the BankID service. It uses the JSON API released in February 2018.

JSON client
~~~~~~~~~~~

.. code-block:: python

    >>> from bankid import BankIDJSONClient
    >>> client = BankIDJSONClient(certificates=('path/to/certificate.pem',
                                                'path/to/key.pem'))

Connection to production server is the default in the client. If test
server is desired, send in the ``test_server=True`` keyword in the init
of the client.

When using the JSON client, authentication and signing calls requires
the end user's ip address to be included in all calls. An authentication order
is initiated as such:

.. code-block:: python

    >>> client.authenticate(end_user_ip='194.168.2.25',
                            personal_number="YYYYMMDDXXXX")
    {
        'orderRef': 'ee3421ea-2096-4000-8130-82648efe0927',
        'autoStartToken': 'e8df5c3c-c67b-4a01-bfe5-fefeab760beb',
        'qrStartToken': '01f94e28-857f-4d8a-bf8e-6c5a24466658',
        'qrStartSecret': 'b4214886-3b5b-46ab-bc08-6862fddc0e06'
    }

and a sign order is initiated in a similar fashion:

.. code-block:: python

    >>> client.sign(end_user_ip='194.168.2.25',
                    user_visible_data="The information to sign.",
                    personal_number="YYYYMMDDXXXX")
    {
        'orderRef': 'ee3421ea-2096-4000-8130-82648efe0927',
        'autoStartToken': 'e8df5c3c-c67b-4a01-bfe5-fefeab760beb',
        'qrStartToken': '01f94e28-857f-4d8a-bf8e-6c5a24466658',
        'qrStartSecret': 'b4214886-3b5b-46ab-bc08-6862fddc0e06'
    }

Since the ``BankIDJSONClient`` is using the BankID ``v5`` JSON API, the ``personal_number`` can now be omitted when calling
``authenticate`` and ``sign``. See BankID Relying Party Guidelines
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
BankID Relying Party Guidelines
it states that *"collect should be called every two seconds and must not be
called more frequent than once per second"*.

PyBankID and QR code
--------------------

PyBankID cannot generate QR codes for you, but there is an example application in the
`examples folder of the repo <https://github.com/hbldh/pybankid/tree/master/examples>`_ where a
Flask application called ``qrdemo`` shows one way to do authentication with animated QR codes.

The content for the QR code is generated by this method:

.. code-block:: python

    import hashlib
    import hmac
    from math import floor
    import time

    def generate_qr_code_content(qr_start_token: str, start_t: float, qr_start_secret: str):
    """Given QR start token, time.time() when initiated authentication call was made and the
    QR start secret, calculate the current QR code content to display.
    """
        elapsed_seconds_since_call = int(floor(time.time() - start_t))
        qr_auth_code = hmac.new(
            qr_start_secret.encode(),
            msg=str(elapsed_seconds_since_call).encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()
        return f"bankid.{qr_start_token}.{elapsed_seconds_since_call}.{qr_auth_code}"


Certificates
------------

Production certificates
~~~~~~~~~~~~~~~~~~~~~~~

If you want to use BankID in a production environment, then you will have to
purchase this service from one of the
`selling banks <https://www.bankid.com/kontakt/foeretag/saeljare>`_.
They will then provide you with a certificate that can be used to authenticate
your company/application with the BankID servers.

This certificate has to be processed somewhat to be able to use with PyBankID,
and how to do this depends on what the selling bank provides you with.

Test certificate
~~~~~~~~~~~~~~~~

The certificate to use when developing against the BankID test servers can
be obtained through PyBankID:

.. code-block:: python

    >>> import os
    >>> import bankid
    >>> dir_to_save_cert_and_key_in = os.path.expanduser('~')
    >>> cert_and_key = bankid.create_bankid_test_server_cert_and_key(
        dir_to_save_cert_and_key_in)
    >>> print(cert_and_key)
    ['/home/hbldh/certificate.pem', '/home/hbldh/key.pem']
    >>> client = bankid.BankIDJSONClient(
        certificates=cert_and_key, test_server=True)


Python 2, urllib3 and certificate verification
----------------------------------------------

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

    py.test
