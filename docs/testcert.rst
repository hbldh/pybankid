.. _testcert:

Test Certificate methods
========================

There is a test certificate available on `BankID Technical Information webpage
<https://www.bankid.com/bankid-i-dina-tjanster/rp-info>`_, which can be used for
testing authorization and signing. The methods in the :py:mod:`bankid.testcert`
module fetches that test certificate, splits it into one certificate and one key part and
converts it from `pxf <https://en.wikipedia.org/wiki/PKCS_12>`_ format to
`pem <https://en.wikipedia.org/wiki/X.509#Certificate_filename_extensions>`_.

.. note::
   It also removes the password from the private key in the certificate,
   which is a requirement for using the PyBankID package in an automated way.

.. automodule:: bankid.testcert
   :members:

