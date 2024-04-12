# -*- coding: utf-8 -*-
"""
:mod:`bankid`
=============

Created 2016-11-28 by hbldh

PyBankID is a client for providing BankID services as a Relying Party, i.e.
providing authentication and signing functionality to end users. This package
provides a simplifying interface for initiating authentication
and signing orders and then collecting the results from the BankID servers.

If you intend to use PyBankID in your project, you are advised to read
the `BankID Relying Party Integration Guide
<https://www.bankid.com/en/utvecklare/guider/teknisk-integrationsguide>`_ before
doing anything else. There, one can find information
about how the BankID methods are defined and how to use them.

"""

from bankid import exceptions
from bankid.__version__ import __version__, version
from bankid.certutils import create_bankid_test_server_cert_and_key
from bankid.syncclient import BankIDClient
from bankid.asyncclient import BankIDAsyncClient
from bankid.qr import generate_qr_code_content

__all__ = [
    "BankIDClient",
    "BankIDAsyncClient",
    "exceptions",
    "create_bankid_test_server_cert_and_key",
    "generate_qr_code_content",
    "__version__",
    "version",
]
