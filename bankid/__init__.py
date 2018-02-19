#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
