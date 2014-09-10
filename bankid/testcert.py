#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`bankid`
==================

.. module:: bankid
   :platform: Unix, Windows
   :synopsis:

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2014-09-09, 16:55

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import tempfile
import subprocess
import sys
import requests

_TEST_CERT_PASSWORD = 'qwerty123'
_CERT_URL = "http://www.bankid.com/Global/wwwbankidcom/RP/FPTestcert1.pfx"


def create_test_server_cert_and_key(destination_path):
    if sys.platform == 'win32':
        raise NotImplementedError("Test certificate fetching in Windows not supported. "
                                  "See documentation for details.")
    cert_tmp_path = os.path.abspath(
        os.path.join(tempfile.gettempdir(),
                     os.path.basename(_CERT_URL)))
    out_cert_path = os.path.abspath(
        os.path.join(os.path.abspath(destination_path),
                     'cert.pem'))
    out_key_path = os.path.abspath(
        os.path.join(os.path.abspath(destination_path),
                     'key.pem'))

    r = requests.get(_CERT_URL)
    with open(cert_tmp_path, 'wb') as f:
        f.write(r.content)
    p = subprocess.Popen(['openssl', 'pkcs12',
                          '-in', "'{0}'".format(cert_tmp_path),
                          '-passin', 'pass:{0}'.format(_TEST_CERT_PASSWORD),
                          '-out', "'{0}'".format(out_cert_path),
                          '-passout', 'pass:{0}'.format(_TEST_CERT_PASSWORD)])
    p = subprocess.Popen(['openssl', 'pkcs12',
                          '-in', "'{0}'".format(cert_tmp_path),
                          '-passin', 'pass:{0}'.format(_TEST_CERT_PASSWORD),
                          '|', 'openssl', 'rsa', '-des3',
                          '-out', "'{0}'".format(out_key_path),
                          '-passout', 'pass:{0}'.format(_TEST_CERT_PASSWORD)])

    # TODO: Check if processes exited correctly.

    return out_cert_path, out_key_path


def main():
    create_test_server_cert_and_key(os.path.expanduser('~'))

if __name__ == "__main__":
    main()
