PyBankID
========

PyBankID is a client for performing BankID signing.

The Swedish BankID solution for digital signing uses a SOAP
connection solution, and this module aims at providing a simplifying
client for making authentication, signing and collect requests to
the BankID servers.

For more details about BankID implementation, see the `official documentation
<http://www.bankid.com/rp/info/>`_. There, one can find information 
about how the BankID methods are defined, how to set up the test environment
and obtain the SSL certificate for the test server.

.. highlights::
    
    Test the use of this module using the BankID test server solution. See
    the documentation linked to above.


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
    >>> client = BankIDClient(certificates=('certificate.pem', 'key.pem'))

Connection to test server is the default in the client. If production 
server is desired, send in the ``test_server=False`` keyword in the init
of the client.

A sign order is then placed by

.. code-block:: python

    >>> client.sign(user_visible_data="The information to sign.", 
                    personal_number="YYYYMMDDXXXX")
    {'autoStartToken': u'798c1ea1-e67a-4df6-a2f6-164ac223fd52', 
     'orderRef': u'a9b791c3-459f-492b-bf61-23027876140b'}

The status of the order can then be studied by polling 
with the ``collect`` method:

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

Documentation
-------------

No documentation is available yet. Read the docstrings until then.
