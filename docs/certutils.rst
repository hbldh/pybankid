.. _certutils:

Certificates
============

Production certificates
-----------------------

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
    ...     dir_to_save_cert_and_key_in
    ... )
    >>> print(cert_and_key)
    ['/home/hbldh/certificate.pem', '/home/hbldh/key.pem']
    >>> client = bankid.BankIDJSONClient(
    ...     certificates=cert_and_key,
    ...     test_server=True
    ... )

The test certificate is available on `BankID Technical Information webpage
<https://www.bankid.com/utvecklare/rp-info>`_. The
:py:func:`bankid.certutils.create_bankid_test_server_cert_and_key` in the
:py:mod:`bankid.certutils` module fetches that test certificate, splits it
into one certificate and one key part and converts it from
`.p12 or .pfx <https://en.wikipedia.org/wiki/PKCS_12>`_ format to
`pem <https://en.wikipedia.org/wiki/X.509#Certificate_filename_extensions>`_.
These can then be used for testing purposes, by sending in ``test_server=True``
keyword in the :py:class:`~BankIDClient` or :py:class:`~BankIdAsyncClient`.


Splitting certificates
~~~~~~~~~~~~~~~~~~~~~~

To convert your production certificate from PKCS_12 format to two ``pem``,
ready to be used by PyBankID, one can do the following:

.. code-block:: python

   >>> from bankid.certutils import split_certificate
   >>> split_certificate(
   ...     '/path/to/certificate.p12',
   ...     '/destination/folder/',
   ...     'password_for_certificate_p12',
   ... )
   ('/destination/folder/certificate.pem', '/destination/folder/key.pem')

It can also be done via regular OpenSSL terminal calls:

.. code-block:: bash

   openssl pkcs12 -in /path/to/certificate.p12 -passin pass:password_for_certificate_p12 -out /destination/folder/certificate.pem -clcerts -nokeys
   openssl pkcs12 -in /path/to/certificate.p12 -passin pass:password_for_certificate_p12 -out /destination/folder/key.pem -nocerts  -nodes

.. note::
   This also removes the password from the private key in the certificate,
   which is a requirement for using the PyBankID package in an automated way.


API
---

.. automodule:: bankid.certutils
   :members:

