Usage
-----

There are two different clients available in the :py:mod:`bankid` package: the
:py:class:`bankid.client.BankIDClient`, which uses the SOAP-based API that is being deprecated
in February 2020, and the :py:class:`bankid.jsonclient.BankIDJSONClient`, which uses the new
JSON API released in February 2018.

**Any new deployment using PyBankID should use the JSON Client!**

.. toctree::
   :maxdepth: 2

   jsonclient
   soapclient
