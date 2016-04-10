.. _certutils:

Certificate methods
===================

Converting/splitting certificates
---------------------------------

To convert your production certificate from PKCS_12 format to two ``pem``,
ready to be used by PyBankID, one can do the following:

.. code-block:: python

   In [1]: from bankid.certutils import split_certificate

   In [2]: split_certificate('/path/to/certificate.p12',
                             '/destination/folder/',
                             'password_for_certificate_p12')
   Out [2]: ('/destination/folder/certificate.pem',
             '/destination/folder/key.pem')

It can also be done via regular OpenSSL terminal calls:

.. code-block:: bash

   openssl pkcs12 -in /path/to/certificate.p12 -passin pass:password_for_certificate_p12 -out /destination/folder/certificate.pem -clcerts -nokeys
   openssl pkcs12 -in /path/to/certificate.p12 -passin pass:password_for_certificate_p12 -out /destination/folder/key.pem -nocerts  -nodes

.. note::
   This also removes the password from the private key in the certificate,
   which is a requirement for using the PyBankID package in an automated way.

Test server certificate
-----------------------

There is a test certificate available on `BankID Technical Information webpage
<https://www.bankid.com/bankid-i-dina-tjanster/rp-info>`_, which can be used for
testing authorization and signing. The
:py:func:`bankid.certutils.create_bankid_test_server_cert_and_key` in the
:py:mod:`bankid.certutils` module fetches that test certificate, splits it
into one certificate and one key part and converts it from
`.p12 or .pfx <https://en.wikipedia.org/wiki/PKCS_12>`_ format to
`pem <https://en.wikipedia.org/wiki/X.509#Certificate_filename_extensions>`_.
These can then be used for testing purposes, by sending in ``test_server=True``
keyword in the :py:class:`~BankIDClient`.


API
---

.. automodule:: bankid.certutils
   :members:

