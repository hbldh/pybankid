PyBankID
========

.. image:: https://dev.azure.com/hbldh/github/_apis/build/status/hbldh.pybankid?branchName=master
    :target: https://dev.azure.com/hbldh/github/_build/latest?definitionId=2&branchName=master
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
<https://www.bankid.com/bankid-i-dina-tjanster/rp-info>`_ before
doing anything else. There, one can find information
about how the BankID methods are defined and how to use them.

An `example web application using PyBankID <https://github.com/hbldh/pybankid-example-app>`_
exists and can be found in deployed state on `Heroku <https://bankid-example-app.herokuapp.com/>`_.

**If you use PyBankID in production and want updates on new releases and
notifications about important changes to the BankID service, send a mail to
the developer of this package to be added to the PyBankID mailing list.**

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

There are two different clients available in the ``bankid`` package: the
``BankIDClient``, which uses the SOAP-based API that is being deprecated
in February 2020,  and the ``BankIDJSONClient``, which uses the new
JSON API released in February 2018.

**Any new deployment using PyBankID should use the** ``BankIDJSONClient``.

JSON client
~~~~~~~~~~~

.. code-block:: python

    >>> from bankid import BankIDJSONClient
    >>> client = BankIDJSONClient(certificates=('path/to/certificate.pem',
                                                'path/to/key.pem'))

Connection to production server is the default in the client. If test
server is desired, send in the ``test_server=True`` keyword in the init
of the client.

WHen using the JSON client, all authentication and signing calls requires
the end user's ip address to be included in all calls. An authentication order
is initiated as such:

.. code-block:: python

    >>> client.authenticate(end_user_ip='194.168.2.25',
                            personal_number="YYYYMMDDXXXX")
    {
        'autoStartToken': '798c1ea1-e67a-4df6-a2f6-164ac223fd52',
        'orderRef': 'a9b791c3-459f-492b-bf61-23027876140b'
    }

and a sign order is initiated in a similar fashion:

.. code-block:: python

    >>> client.sign(end_user_ip='194.168.2.25',
                    user_visible_data="The information to sign.",
                    personal_number="YYYYMMDDXXXX")
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
it states that *"collect should be called every two seconds and must not be
called more frequent than once per second"*.

SOAP client
~~~~~~~~~~~

For documentation about how to use the SOAP client, see the
`documentation <https://pybankid.readthedocs.io/>`_.

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

    py.test tests/
