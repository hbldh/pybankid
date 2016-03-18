#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`bankid.testcert` -- Test Certificate fetching
===================================================

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
_TEST_CERT_URL = "https://www.bankid.com/assets/bankid/rp/FPTestcert2_20150818_102329.pfx"


def create_bankid_test_server_cert_and_key(destination_path):
    """Fetch the P12 certificate from BankID servers, split it into
    a certificate part and a key part and save them as separate files,
    stored in PEM format.

    :param destination_path: The directory to save certificate and key files to.
    :type destination_path: str
    :returns: The path tuple ``(cert_path, key_path)``.
    :rtype: tuple

    """
    if sys.platform == 'win32':
        raise NotImplementedError(
            "Test certificate fetching in Windows not supported. "
            "See documentation for details.")

    certificate, key = split_test_cert_and_key()

    # Paths to output files.
    out_cert_path = os.path.join(os.path.abspath(
        os.path.expanduser(destination_path)), 'cert.pem')
    out_key_path = os.path.join(os.path.abspath(
        os.path.expanduser(destination_path)), 'key.pem')

    with open(out_cert_path, 'wt') as f:
        f.write(certificate)
    with open(out_key_path, 'wt') as f:
        f.write(key)

    # Return path tuples.
    return out_cert_path, out_key_path


def split_test_cert_and_key():
    """Fetch the P12 certificate from BankID servers, split it into
    a certificate part and a key part and return the two components as text data.

    :returns: Tuple of certificate and key string data.
    :rtype: tuple

    """
    # Paths to temporary files.
    cert_tmp_path = os.path.join(tempfile.gettempdir(), os.path.basename(_TEST_CERT_URL))
    cert_conv_tmp_path = os.path.join(tempfile.gettempdir(), 'certificate.pem')
    key_conv_tmp_path = os.path.join(tempfile.gettempdir(), 'key.pem')

    # Fetch P12 certificate and store in temporary folder.
    r = requests.get(_TEST_CERT_URL)
    with open(cert_tmp_path, 'wb') as f:
        f.write(r.content)

    # Use openssl for converting to pem format.
    pipeline_1 = [
        'openssl', 'pkcs12',
        '-in', "{0}".format(cert_tmp_path),
        '-passin', 'pass:{0}'.format(_TEST_CERT_PASSWORD),
        '-out', "{0}".format(cert_conv_tmp_path),
        '-clcerts', '-nokeys'
    ]
    p = subprocess.Popen(pipeline_1,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.communicate()
    pipeline_2 = [
        'openssl', 'pkcs12',
        '-in', "{0}".format(cert_tmp_path),
        '-passin', 'pass:{0}'.format(_TEST_CERT_PASSWORD),
        '-out', "{0}".format(key_conv_tmp_path),
        '-nocerts', '-nodes'
    ]
    p = subprocess.Popen(pipeline_2,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.communicate()

    # Open the newly created PEM certificate in the temporary folder.
    with open(cert_conv_tmp_path, 'rt') as f:
        certificate = f.read()
    with open(key_conv_tmp_path, 'rt') as f:
        key = f.read()

    # Try to remove all temporary files.
    try:
        os.remove(cert_tmp_path)
        os.remove(cert_conv_tmp_path)
        os.remove(key_conv_tmp_path)
    except:
        pass

    return certificate, key


def main():
    paths = create_bankid_test_server_cert_and_key(os.path.expanduser('~'))
    print('Saved certificate as {0}'.format(paths[0]))
    print('Saved key as {0}'.format(paths[1]))

if __name__ == "__main__":
    main()
