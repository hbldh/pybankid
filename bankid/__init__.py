#!/usr/bin/env python
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
the `BankID Relying Party Guidelines
<https://www.bankid.com/bankid-i-dina-tjanster/rp-info>`_ before
doing anything else. There, one can find information
about how the BankID methods are defined and how to use them.

"""

import warnings as _warnings

from requests.packages.urllib3.exceptions import SubjectAltNameWarning as _sanw

from .client import BankIDClient
from .jsonclient import BankIDJSONClient
from .certutils import create_bankid_test_server_cert_and_key
from .__version__ import __version__, version
import bankid.exceptions

__all__ = [
    'BankIDClient', 'BankIDJSONClient', 'exceptions',
    'create_bankid_test_server_cert_and_key',
    '__version__', 'version'
]

_warnings.simplefilter('ignore', _sanw)
